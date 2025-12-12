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
import aws_cdk.interfaces.aws_kinesisfirehose as _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d
import aws_cdk.interfaces.aws_logs as _aws_cdk_interfaces_aws_logs_ceddda9d
import aws_cdk.interfaces.aws_s3 as _aws_cdk_interfaces_aws_s3_ceddda9d
import constructs as _constructs_77d1e7e8
from ...aws_logs import ILogsDelivery as _ILogsDelivery_0d3c9e29
from ...core import IMixin as _IMixin_11e4b965, Mixin as _Mixin_a69446c0
from ...mixins import (
    CfnPropertyMixinOptions as _CfnPropertyMixinOptions_9cbff649,
    PropertyMergeStrategy as _PropertyMergeStrategy_49c157e8,
)


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnBrowserCustomMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "browser_signing": "browserSigning",
        "description": "description",
        "execution_role_arn": "executionRoleArn",
        "name": "name",
        "network_configuration": "networkConfiguration",
        "recording_config": "recordingConfig",
        "tags": "tags",
    },
)
class CfnBrowserCustomMixinProps:
    def __init__(
        self,
        *,
        browser_signing: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBrowserCustomPropsMixin.BrowserSigningProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        execution_role_arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        network_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBrowserCustomPropsMixin.BrowserNetworkConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        recording_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBrowserCustomPropsMixin.RecordingConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnBrowserCustomPropsMixin.

        :param browser_signing: Browser signing configuration.
        :param description: The custom browser.
        :param execution_role_arn: The Amazon Resource Name (ARN) of the execution role.
        :param name: The name of the custom browser.
        :param network_configuration: The network configuration for a code interpreter. This structure defines how the code interpreter connects to the network.
        :param recording_config: THe custom browser configuration.
        :param tags: The tags for the custom browser.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-browsercustom.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
            
            cfn_browser_custom_mixin_props = bedrockagentcore_mixins.CfnBrowserCustomMixinProps(
                browser_signing=bedrockagentcore_mixins.CfnBrowserCustomPropsMixin.BrowserSigningProperty(
                    enabled=False
                ),
                description="description",
                execution_role_arn="executionRoleArn",
                name="name",
                network_configuration=bedrockagentcore_mixins.CfnBrowserCustomPropsMixin.BrowserNetworkConfigurationProperty(
                    network_mode="networkMode",
                    vpc_config=bedrockagentcore_mixins.CfnBrowserCustomPropsMixin.VpcConfigProperty(
                        security_groups=["securityGroups"],
                        subnets=["subnets"]
                    )
                ),
                recording_config=bedrockagentcore_mixins.CfnBrowserCustomPropsMixin.RecordingConfigProperty(
                    enabled=False,
                    s3_location=bedrockagentcore_mixins.CfnBrowserCustomPropsMixin.S3LocationProperty(
                        bucket="bucket",
                        prefix="prefix"
                    )
                ),
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b9b70b48124be49e254582f50a9aa1538acbefb906dd3217ac665c28bd940a2)
            check_type(argname="argument browser_signing", value=browser_signing, expected_type=type_hints["browser_signing"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument execution_role_arn", value=execution_role_arn, expected_type=type_hints["execution_role_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network_configuration", value=network_configuration, expected_type=type_hints["network_configuration"])
            check_type(argname="argument recording_config", value=recording_config, expected_type=type_hints["recording_config"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if browser_signing is not None:
            self._values["browser_signing"] = browser_signing
        if description is not None:
            self._values["description"] = description
        if execution_role_arn is not None:
            self._values["execution_role_arn"] = execution_role_arn
        if name is not None:
            self._values["name"] = name
        if network_configuration is not None:
            self._values["network_configuration"] = network_configuration
        if recording_config is not None:
            self._values["recording_config"] = recording_config
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def browser_signing(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBrowserCustomPropsMixin.BrowserSigningProperty"]]:
        '''Browser signing configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-browsercustom.html#cfn-bedrockagentcore-browsercustom-browsersigning
        '''
        result = self._values.get("browser_signing")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBrowserCustomPropsMixin.BrowserSigningProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The custom browser.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-browsercustom.html#cfn-bedrockagentcore-browsercustom-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execution_role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the execution role.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-browsercustom.html#cfn-bedrockagentcore-browsercustom-executionrolearn
        '''
        result = self._values.get("execution_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the custom browser.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-browsercustom.html#cfn-bedrockagentcore-browsercustom-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBrowserCustomPropsMixin.BrowserNetworkConfigurationProperty"]]:
        '''The network configuration for a code interpreter.

        This structure defines how the code interpreter connects to the network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-browsercustom.html#cfn-bedrockagentcore-browsercustom-networkconfiguration
        '''
        result = self._values.get("network_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBrowserCustomPropsMixin.BrowserNetworkConfigurationProperty"]], result)

    @builtins.property
    def recording_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBrowserCustomPropsMixin.RecordingConfigProperty"]]:
        '''THe custom browser configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-browsercustom.html#cfn-bedrockagentcore-browsercustom-recordingconfig
        '''
        result = self._values.get("recording_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBrowserCustomPropsMixin.RecordingConfigProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The tags for the custom browser.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-browsercustom.html#cfn-bedrockagentcore-browsercustom-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBrowserCustomMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnBrowserCustomPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnBrowserCustomPropsMixin",
):
    '''AgentCore Browser tool provides a fast, secure, cloud-based browser runtime to enable AI agents to interact with websites at scale.

    For more information about using the custom browser, see `Interact with web applications using Amazon Bedrock AgentCore Browser <https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/browser-tool.html>`_ .

    See the *Properties* section below for descriptions of both the required and optional properties.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-browsercustom.html
    :cloudformationResource: AWS::BedrockAgentCore::BrowserCustom
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
        
        cfn_browser_custom_props_mixin = bedrockagentcore_mixins.CfnBrowserCustomPropsMixin(bedrockagentcore_mixins.CfnBrowserCustomMixinProps(
            browser_signing=bedrockagentcore_mixins.CfnBrowserCustomPropsMixin.BrowserSigningProperty(
                enabled=False
            ),
            description="description",
            execution_role_arn="executionRoleArn",
            name="name",
            network_configuration=bedrockagentcore_mixins.CfnBrowserCustomPropsMixin.BrowserNetworkConfigurationProperty(
                network_mode="networkMode",
                vpc_config=bedrockagentcore_mixins.CfnBrowserCustomPropsMixin.VpcConfigProperty(
                    security_groups=["securityGroups"],
                    subnets=["subnets"]
                )
            ),
            recording_config=bedrockagentcore_mixins.CfnBrowserCustomPropsMixin.RecordingConfigProperty(
                enabled=False,
                s3_location=bedrockagentcore_mixins.CfnBrowserCustomPropsMixin.S3LocationProperty(
                    bucket="bucket",
                    prefix="prefix"
                )
            ),
            tags={
                "tags_key": "tags"
            }
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnBrowserCustomMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::BedrockAgentCore::BrowserCustom``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06558b710350f8e759531238d023a2fe14ee09c31f10db6b01a09a80094616f4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1698a0066840ace9b4aad0b05ebfce60e613215a4247e9928d29e8c65f9d132c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47200bb4582982b3460352e94cc98060cff750aa87f7f52cecdd2525333d9dde)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnBrowserCustomMixinProps:
        return typing.cast(CfnBrowserCustomMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnBrowserCustomPropsMixin.BrowserNetworkConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"network_mode": "networkMode", "vpc_config": "vpcConfig"},
    )
    class BrowserNetworkConfigurationProperty:
        def __init__(
            self,
            *,
            network_mode: typing.Optional[builtins.str] = None,
            vpc_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBrowserCustomPropsMixin.VpcConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The network configuration.

            :param network_mode: The network mode.
            :param vpc_config: Network mode configuration for VPC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-browsercustom-browsernetworkconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                browser_network_configuration_property = bedrockagentcore_mixins.CfnBrowserCustomPropsMixin.BrowserNetworkConfigurationProperty(
                    network_mode="networkMode",
                    vpc_config=bedrockagentcore_mixins.CfnBrowserCustomPropsMixin.VpcConfigProperty(
                        security_groups=["securityGroups"],
                        subnets=["subnets"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e2723057ca2673184bfdfd04832a8499b356a8eca736330ae8e5c0160a6c177d)
                check_type(argname="argument network_mode", value=network_mode, expected_type=type_hints["network_mode"])
                check_type(argname="argument vpc_config", value=vpc_config, expected_type=type_hints["vpc_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if network_mode is not None:
                self._values["network_mode"] = network_mode
            if vpc_config is not None:
                self._values["vpc_config"] = vpc_config

        @builtins.property
        def network_mode(self) -> typing.Optional[builtins.str]:
            '''The network mode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-browsercustom-browsernetworkconfiguration.html#cfn-bedrockagentcore-browsercustom-browsernetworkconfiguration-networkmode
            '''
            result = self._values.get("network_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vpc_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBrowserCustomPropsMixin.VpcConfigProperty"]]:
            '''Network mode configuration for VPC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-browsercustom-browsernetworkconfiguration.html#cfn-bedrockagentcore-browsercustom-browsernetworkconfiguration-vpcconfig
            '''
            result = self._values.get("vpc_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBrowserCustomPropsMixin.VpcConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BrowserNetworkConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnBrowserCustomPropsMixin.BrowserSigningProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled"},
    )
    class BrowserSigningProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Browser signing configuration.

            :param enabled: Default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-browsercustom-browsersigning.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                browser_signing_property = bedrockagentcore_mixins.CfnBrowserCustomPropsMixin.BrowserSigningProperty(
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__53fbac5adc34bd7cf963db5456825e03933e8f7d344bd405f58bbf40357eab2c)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-browsercustom-browsersigning.html#cfn-bedrockagentcore-browsercustom-browsersigning-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BrowserSigningProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnBrowserCustomPropsMixin.RecordingConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled", "s3_location": "s3Location"},
    )
    class RecordingConfigProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            s3_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBrowserCustomPropsMixin.S3LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The recording configuration.

            :param enabled: The recording configuration for a browser. This structure defines how browser sessions are recorded. Default: - false
            :param s3_location: The S3 location.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-browsercustom-recordingconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                recording_config_property = bedrockagentcore_mixins.CfnBrowserCustomPropsMixin.RecordingConfigProperty(
                    enabled=False,
                    s3_location=bedrockagentcore_mixins.CfnBrowserCustomPropsMixin.S3LocationProperty(
                        bucket="bucket",
                        prefix="prefix"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ea2e3bf6ad31939ca40e9596a477ce81b59011ec4781ec32288eb919ef931a7e)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument s3_location", value=s3_location, expected_type=type_hints["s3_location"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if s3_location is not None:
                self._values["s3_location"] = s3_location

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''The recording configuration for a browser.

            This structure defines how browser sessions are recorded.

            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-browsercustom-recordingconfig.html#cfn-bedrockagentcore-browsercustom-recordingconfig-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def s3_location(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBrowserCustomPropsMixin.S3LocationProperty"]]:
            '''The S3 location.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-browsercustom-recordingconfig.html#cfn-bedrockagentcore-browsercustom-recordingconfig-s3location
            '''
            result = self._values.get("s3_location")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBrowserCustomPropsMixin.S3LocationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RecordingConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnBrowserCustomPropsMixin.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "prefix": "prefix"},
    )
    class S3LocationProperty:
        def __init__(
            self,
            *,
            bucket: typing.Optional[builtins.str] = None,
            prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The S3 location.

            :param bucket: The S3 location bucket name.
            :param prefix: The S3 location object prefix.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-browsercustom-s3location.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                s3_location_property = bedrockagentcore_mixins.CfnBrowserCustomPropsMixin.S3LocationProperty(
                    bucket="bucket",
                    prefix="prefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6db87d1e02e7aba9656052fdff62f48f2c2d112df1100d2b275b3f76db1b6bc9)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket is not None:
                self._values["bucket"] = bucket
            if prefix is not None:
                self._values["prefix"] = prefix

        @builtins.property
        def bucket(self) -> typing.Optional[builtins.str]:
            '''The S3 location bucket name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-browsercustom-s3location.html#cfn-bedrockagentcore-browsercustom-s3location-bucket
            '''
            result = self._values.get("bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''The S3 location object prefix.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-browsercustom-s3location.html#cfn-bedrockagentcore-browsercustom-s3location-prefix
            '''
            result = self._values.get("prefix")
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
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnBrowserCustomPropsMixin.VpcConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"security_groups": "securityGroups", "subnets": "subnets"},
    )
    class VpcConfigProperty:
        def __init__(
            self,
            *,
            security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Network mode configuration for VPC.

            :param security_groups: Security groups for VPC.
            :param subnets: Subnets for VPC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-browsercustom-vpcconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                vpc_config_property = bedrockagentcore_mixins.CfnBrowserCustomPropsMixin.VpcConfigProperty(
                    security_groups=["securityGroups"],
                    subnets=["subnets"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ce09060669c510a96e651e22fbcd3f5c26d7ef68d9c1aba262608f5c55d30908)
                check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
                check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if security_groups is not None:
                self._values["security_groups"] = security_groups
            if subnets is not None:
                self._values["subnets"] = subnets

        @builtins.property
        def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Security groups for VPC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-browsercustom-vpcconfig.html#cfn-bedrockagentcore-browsercustom-vpcconfig-securitygroups
            '''
            result = self._values.get("security_groups")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnets(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Subnets for VPC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-browsercustom-vpcconfig.html#cfn-bedrockagentcore-browsercustom-vpcconfig-subnets
            '''
            result = self._values.get("subnets")
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
    jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnCodeInterpreterCustomMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "execution_role_arn": "executionRoleArn",
        "name": "name",
        "network_configuration": "networkConfiguration",
        "tags": "tags",
    },
)
class CfnCodeInterpreterCustomMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        execution_role_arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        network_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCodeInterpreterCustomPropsMixin.CodeInterpreterNetworkConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnCodeInterpreterCustomPropsMixin.

        :param description: The code interpreter description.
        :param execution_role_arn: The Amazon Resource Name (ARN) of the execution role.
        :param name: The name of the code interpreter.
        :param network_configuration: The network configuration for a code interpreter. This structure defines how the code interpreter connects to the network.
        :param tags: The tags for the code interpreter.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-codeinterpretercustom.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
            
            cfn_code_interpreter_custom_mixin_props = bedrockagentcore_mixins.CfnCodeInterpreterCustomMixinProps(
                description="description",
                execution_role_arn="executionRoleArn",
                name="name",
                network_configuration=bedrockagentcore_mixins.CfnCodeInterpreterCustomPropsMixin.CodeInterpreterNetworkConfigurationProperty(
                    network_mode="networkMode",
                    vpc_config=bedrockagentcore_mixins.CfnCodeInterpreterCustomPropsMixin.VpcConfigProperty(
                        security_groups=["securityGroups"],
                        subnets=["subnets"]
                    )
                ),
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83b01cb25c7f75ec0c8c3a154c2882b6f4b58e0491056f259d2acb1e13ba982d)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument execution_role_arn", value=execution_role_arn, expected_type=type_hints["execution_role_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network_configuration", value=network_configuration, expected_type=type_hints["network_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if execution_role_arn is not None:
            self._values["execution_role_arn"] = execution_role_arn
        if name is not None:
            self._values["name"] = name
        if network_configuration is not None:
            self._values["network_configuration"] = network_configuration
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The code interpreter description.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-codeinterpretercustom.html#cfn-bedrockagentcore-codeinterpretercustom-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execution_role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the execution role.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-codeinterpretercustom.html#cfn-bedrockagentcore-codeinterpretercustom-executionrolearn
        '''
        result = self._values.get("execution_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the code interpreter.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-codeinterpretercustom.html#cfn-bedrockagentcore-codeinterpretercustom-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCodeInterpreterCustomPropsMixin.CodeInterpreterNetworkConfigurationProperty"]]:
        '''The network configuration for a code interpreter.

        This structure defines how the code interpreter connects to the network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-codeinterpretercustom.html#cfn-bedrockagentcore-codeinterpretercustom-networkconfiguration
        '''
        result = self._values.get("network_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCodeInterpreterCustomPropsMixin.CodeInterpreterNetworkConfigurationProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The tags for the code interpreter.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-codeinterpretercustom.html#cfn-bedrockagentcore-codeinterpretercustom-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCodeInterpreterCustomMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnCodeInterpreterCustomPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnCodeInterpreterCustomPropsMixin",
):
    '''The AgentCore Code Interpreter tool enables agents to securely execute code in isolated sandbox environments.

    It offers advanced configuration support and seamless integration with popular frameworks.

    For more information about using the custom code interpreter, see `Execute code and analyze data using Amazon Bedrock AgentCore Code Interpreter <https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/code-interpreter-tool.html>`_ .

    See the *Properties* section below for descriptions of both the required and optional properties.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-codeinterpretercustom.html
    :cloudformationResource: AWS::BedrockAgentCore::CodeInterpreterCustom
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
        
        cfn_code_interpreter_custom_props_mixin = bedrockagentcore_mixins.CfnCodeInterpreterCustomPropsMixin(bedrockagentcore_mixins.CfnCodeInterpreterCustomMixinProps(
            description="description",
            execution_role_arn="executionRoleArn",
            name="name",
            network_configuration=bedrockagentcore_mixins.CfnCodeInterpreterCustomPropsMixin.CodeInterpreterNetworkConfigurationProperty(
                network_mode="networkMode",
                vpc_config=bedrockagentcore_mixins.CfnCodeInterpreterCustomPropsMixin.VpcConfigProperty(
                    security_groups=["securityGroups"],
                    subnets=["subnets"]
                )
            ),
            tags={
                "tags_key": "tags"
            }
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnCodeInterpreterCustomMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::BedrockAgentCore::CodeInterpreterCustom``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3d40d4e9d5fa5eda6edd1151d8204fa8cba20cb9e98fd9821a55717c9b3180d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d913ae291a1dfefb89ad8db64d0523ad2f869fc58f92538420dd3b9241dd5fc)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d58ed371a2d11e8be90118e7839588aae50d62a64cc6c6ac561ad9c53f49a88e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnCodeInterpreterCustomMixinProps:
        return typing.cast(CfnCodeInterpreterCustomMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnCodeInterpreterCustomPropsMixin.CodeInterpreterNetworkConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"network_mode": "networkMode", "vpc_config": "vpcConfig"},
    )
    class CodeInterpreterNetworkConfigurationProperty:
        def __init__(
            self,
            *,
            network_mode: typing.Optional[builtins.str] = None,
            vpc_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCodeInterpreterCustomPropsMixin.VpcConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The network configuration.

            :param network_mode: The network mode.
            :param vpc_config: Network mode configuration for VPC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-codeinterpretercustom-codeinterpreternetworkconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                code_interpreter_network_configuration_property = bedrockagentcore_mixins.CfnCodeInterpreterCustomPropsMixin.CodeInterpreterNetworkConfigurationProperty(
                    network_mode="networkMode",
                    vpc_config=bedrockagentcore_mixins.CfnCodeInterpreterCustomPropsMixin.VpcConfigProperty(
                        security_groups=["securityGroups"],
                        subnets=["subnets"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fd5462e15ceaaffb0e972705f51b156d382f2ad97d671ab9a2a51bc51161a098)
                check_type(argname="argument network_mode", value=network_mode, expected_type=type_hints["network_mode"])
                check_type(argname="argument vpc_config", value=vpc_config, expected_type=type_hints["vpc_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if network_mode is not None:
                self._values["network_mode"] = network_mode
            if vpc_config is not None:
                self._values["vpc_config"] = vpc_config

        @builtins.property
        def network_mode(self) -> typing.Optional[builtins.str]:
            '''The network mode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-codeinterpretercustom-codeinterpreternetworkconfiguration.html#cfn-bedrockagentcore-codeinterpretercustom-codeinterpreternetworkconfiguration-networkmode
            '''
            result = self._values.get("network_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vpc_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCodeInterpreterCustomPropsMixin.VpcConfigProperty"]]:
            '''Network mode configuration for VPC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-codeinterpretercustom-codeinterpreternetworkconfiguration.html#cfn-bedrockagentcore-codeinterpretercustom-codeinterpreternetworkconfiguration-vpcconfig
            '''
            result = self._values.get("vpc_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCodeInterpreterCustomPropsMixin.VpcConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CodeInterpreterNetworkConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnCodeInterpreterCustomPropsMixin.VpcConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"security_groups": "securityGroups", "subnets": "subnets"},
    )
    class VpcConfigProperty:
        def __init__(
            self,
            *,
            security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Network mode configuration for VPC.

            :param security_groups: Security groups for VPC.
            :param subnets: Subnets for VPC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-codeinterpretercustom-vpcconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                vpc_config_property = bedrockagentcore_mixins.CfnCodeInterpreterCustomPropsMixin.VpcConfigProperty(
                    security_groups=["securityGroups"],
                    subnets=["subnets"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__098266e1c1ad82cfca97755bd93f405d511a848aab5e9e5f60cc0f0ef4a23fec)
                check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
                check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if security_groups is not None:
                self._values["security_groups"] = security_groups
            if subnets is not None:
                self._values["subnets"] = subnets

        @builtins.property
        def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Security groups for VPC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-codeinterpretercustom-vpcconfig.html#cfn-bedrockagentcore-codeinterpretercustom-vpcconfig-securitygroups
            '''
            result = self._values.get("security_groups")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnets(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Subnets for VPC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-codeinterpretercustom-vpcconfig.html#cfn-bedrockagentcore-codeinterpretercustom-vpcconfig-subnets
            '''
            result = self._values.get("subnets")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


class CfnGatewayApplicationLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnGatewayApplicationLogs",
):
    '''Builder for CfnGatewayLogsMixin to generate APPLICATION_LOGS for CfnGateway.

    :cloudformationResource: AWS::BedrockAgentCore::Gateway
    :logType: APPLICATION_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
        
        cfn_gateway_application_logs = bedrockagentcore_mixins.CfnGatewayApplicationLogs()
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toFirehose")
    def to_firehose(
        self,
        delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
    ) -> "CfnGatewayLogsMixin":
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39848dbcff7bcfc40d1a54882028de18bd79f07358d575e2f766474c41432799)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast("CfnGatewayLogsMixin", jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> "CfnGatewayLogsMixin":
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a344d11427e4c8db554328e8e359728d32dff227185be0c431f0e06c8092f457)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast("CfnGatewayLogsMixin", jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> "CfnGatewayLogsMixin":
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__333af1943f4d576fe2f6f5471c064f69666be8e6d9f2a424aa8e4bbf0a6e6c26)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast("CfnGatewayLogsMixin", jsii.invoke(self, "toS3", [bucket]))


@jsii.implements(_IMixin_11e4b965)
class CfnGatewayLogsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnGatewayLogsMixin",
):
    '''Amazon Bedrock AgentCore Gateway provides a unified connectivity layer between agents and the tools and resources they need to interact with.

    For more information about creating a gateway, see `Set up an Amazon Bedrock AgentCore gateway <https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-building.html>`_ .

    See the *Properties* section below for descriptions of both the required and optional properties.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-gateway.html
    :cloudformationResource: AWS::BedrockAgentCore::Gateway
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import aws_logs as logs
        from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
        
        # logs_delivery: logs.ILogsDelivery
        
        cfn_gateway_logs_mixin = bedrockagentcore_mixins.CfnGatewayLogsMixin("logType", logs_delivery)
    '''

    def __init__(
        self,
        log_type: builtins.str,
        log_delivery: _ILogsDelivery_0d3c9e29,
    ) -> None:
        '''Create a mixin to enable vended logs for ``AWS::BedrockAgentCore::Gateway``.

        :param log_type: Type of logs that are getting vended.
        :param log_delivery: Object in charge of setting up the delivery destination and delivery connection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4bd5d58e42dde39c0c9f95fa42cce3112291750c9c136a8a9cf2c91b01184db)
            check_type(argname="argument log_type", value=log_type, expected_type=type_hints["log_type"])
            check_type(argname="argument log_delivery", value=log_delivery, expected_type=type_hints["log_delivery"])
        jsii.create(self.__class__, self, [log_type, log_delivery])

    @jsii.member(jsii_name="applyTo")
    def apply_to(
        self,
        resource: _constructs_77d1e7e8.IConstruct,
    ) -> _constructs_77d1e7e8.IConstruct:
        '''Apply vended logs configuration to the construct.

        :param resource: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8707bee110c27b8a30232ab12f1dd6fa82318218289552523e2bef7e7d1124d5)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [resource]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct (has vendedLogs property).

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76cbea6936abcad9bd64780ec1b6cdaa37c3096acf1d0e0c8bb75ea40b400a88)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="APPLICATION_LOGS")
    def APPLICATION_LOGS(cls) -> CfnGatewayApplicationLogs:
        return typing.cast(CfnGatewayApplicationLogs, jsii.sget(cls, "APPLICATION_LOGS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="TRACES")
    def TRACES(cls) -> "CfnGatewayTraces":
        return typing.cast("CfnGatewayTraces", jsii.sget(cls, "TRACES"))

    @builtins.property
    @jsii.member(jsii_name="logDelivery")
    def _log_delivery(self) -> _ILogsDelivery_0d3c9e29:
        return typing.cast(_ILogsDelivery_0d3c9e29, jsii.get(self, "logDelivery"))

    @builtins.property
    @jsii.member(jsii_name="logType")
    def _log_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logType"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnGatewayMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "authorizer_configuration": "authorizerConfiguration",
        "authorizer_type": "authorizerType",
        "description": "description",
        "exception_level": "exceptionLevel",
        "kms_key_arn": "kmsKeyArn",
        "name": "name",
        "protocol_configuration": "protocolConfiguration",
        "protocol_type": "protocolType",
        "role_arn": "roleArn",
        "tags": "tags",
    },
)
class CfnGatewayMixinProps:
    def __init__(
        self,
        *,
        authorizer_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayPropsMixin.AuthorizerConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        authorizer_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        exception_level: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        protocol_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayPropsMixin.GatewayProtocolConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        protocol_type: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnGatewayPropsMixin.

        :param authorizer_configuration: 
        :param authorizer_type: The authorizer type for the gateway.
        :param description: The description for the gateway.
        :param exception_level: The exception level for the gateway.
        :param kms_key_arn: The KMS key ARN for the gateway.
        :param name: The name for the gateway.
        :param protocol_configuration: The protocol configuration for the gateway target.
        :param protocol_type: The protocol type for the gateway target.
        :param role_arn: 
        :param tags: The tags for the gateway.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-gateway.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
            
            cfn_gateway_mixin_props = bedrockagentcore_mixins.CfnGatewayMixinProps(
                authorizer_configuration=bedrockagentcore_mixins.CfnGatewayPropsMixin.AuthorizerConfigurationProperty(
                    custom_jwt_authorizer=bedrockagentcore_mixins.CfnGatewayPropsMixin.CustomJWTAuthorizerConfigurationProperty(
                        allowed_audience=["allowedAudience"],
                        allowed_clients=["allowedClients"],
                        discovery_url="discoveryUrl"
                    )
                ),
                authorizer_type="authorizerType",
                description="description",
                exception_level="exceptionLevel",
                kms_key_arn="kmsKeyArn",
                name="name",
                protocol_configuration=bedrockagentcore_mixins.CfnGatewayPropsMixin.GatewayProtocolConfigurationProperty(
                    mcp=bedrockagentcore_mixins.CfnGatewayPropsMixin.MCPGatewayConfigurationProperty(
                        instructions="instructions",
                        search_type="searchType",
                        supported_versions=["supportedVersions"]
                    )
                ),
                protocol_type="protocolType",
                role_arn="roleArn",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__560caa1f1eac070f9f9b5bc7d741a20666086f7f9cf4d5f6895d04ca519f2a6c)
            check_type(argname="argument authorizer_configuration", value=authorizer_configuration, expected_type=type_hints["authorizer_configuration"])
            check_type(argname="argument authorizer_type", value=authorizer_type, expected_type=type_hints["authorizer_type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument exception_level", value=exception_level, expected_type=type_hints["exception_level"])
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument protocol_configuration", value=protocol_configuration, expected_type=type_hints["protocol_configuration"])
            check_type(argname="argument protocol_type", value=protocol_type, expected_type=type_hints["protocol_type"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if authorizer_configuration is not None:
            self._values["authorizer_configuration"] = authorizer_configuration
        if authorizer_type is not None:
            self._values["authorizer_type"] = authorizer_type
        if description is not None:
            self._values["description"] = description
        if exception_level is not None:
            self._values["exception_level"] = exception_level
        if kms_key_arn is not None:
            self._values["kms_key_arn"] = kms_key_arn
        if name is not None:
            self._values["name"] = name
        if protocol_configuration is not None:
            self._values["protocol_configuration"] = protocol_configuration
        if protocol_type is not None:
            self._values["protocol_type"] = protocol_type
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def authorizer_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayPropsMixin.AuthorizerConfigurationProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-gateway.html#cfn-bedrockagentcore-gateway-authorizerconfiguration
        '''
        result = self._values.get("authorizer_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayPropsMixin.AuthorizerConfigurationProperty"]], result)

    @builtins.property
    def authorizer_type(self) -> typing.Optional[builtins.str]:
        '''The authorizer type for the gateway.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-gateway.html#cfn-bedrockagentcore-gateway-authorizertype
        '''
        result = self._values.get("authorizer_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description for the gateway.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-gateway.html#cfn-bedrockagentcore-gateway-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exception_level(self) -> typing.Optional[builtins.str]:
        '''The exception level for the gateway.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-gateway.html#cfn-bedrockagentcore-gateway-exceptionlevel
        '''
        result = self._values.get("exception_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''The KMS key ARN for the gateway.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-gateway.html#cfn-bedrockagentcore-gateway-kmskeyarn
        '''
        result = self._values.get("kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name for the gateway.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-gateway.html#cfn-bedrockagentcore-gateway-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayPropsMixin.GatewayProtocolConfigurationProperty"]]:
        '''The protocol configuration for the gateway target.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-gateway.html#cfn-bedrockagentcore-gateway-protocolconfiguration
        '''
        result = self._values.get("protocol_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayPropsMixin.GatewayProtocolConfigurationProperty"]], result)

    @builtins.property
    def protocol_type(self) -> typing.Optional[builtins.str]:
        '''The protocol type for the gateway target.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-gateway.html#cfn-bedrockagentcore-gateway-protocoltype
        '''
        result = self._values.get("protocol_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-gateway.html#cfn-bedrockagentcore-gateway-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The tags for the gateway.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-gateway.html#cfn-bedrockagentcore-gateway-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGatewayMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnGatewayPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnGatewayPropsMixin",
):
    '''Amazon Bedrock AgentCore Gateway provides a unified connectivity layer between agents and the tools and resources they need to interact with.

    For more information about creating a gateway, see `Set up an Amazon Bedrock AgentCore gateway <https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-building.html>`_ .

    See the *Properties* section below for descriptions of both the required and optional properties.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-gateway.html
    :cloudformationResource: AWS::BedrockAgentCore::Gateway
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
        
        cfn_gateway_props_mixin = bedrockagentcore_mixins.CfnGatewayPropsMixin(bedrockagentcore_mixins.CfnGatewayMixinProps(
            authorizer_configuration=bedrockagentcore_mixins.CfnGatewayPropsMixin.AuthorizerConfigurationProperty(
                custom_jwt_authorizer=bedrockagentcore_mixins.CfnGatewayPropsMixin.CustomJWTAuthorizerConfigurationProperty(
                    allowed_audience=["allowedAudience"],
                    allowed_clients=["allowedClients"],
                    discovery_url="discoveryUrl"
                )
            ),
            authorizer_type="authorizerType",
            description="description",
            exception_level="exceptionLevel",
            kms_key_arn="kmsKeyArn",
            name="name",
            protocol_configuration=bedrockagentcore_mixins.CfnGatewayPropsMixin.GatewayProtocolConfigurationProperty(
                mcp=bedrockagentcore_mixins.CfnGatewayPropsMixin.MCPGatewayConfigurationProperty(
                    instructions="instructions",
                    search_type="searchType",
                    supported_versions=["supportedVersions"]
                )
            ),
            protocol_type="protocolType",
            role_arn="roleArn",
            tags={
                "tags_key": "tags"
            }
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnGatewayMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::BedrockAgentCore::Gateway``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba3abd0219f9cebfb7aa16a400c731b3501a36ebc908f6f0bbc9c42af6ee25d2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__59c9507f233816216586022d2b682026d0c7b8ca4fb996890981947f2e798721)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d87466fb0ae037c6a9530a298ec294e3a6ba3ca2756eb53949950725893bda2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnGatewayMixinProps:
        return typing.cast(CfnGatewayMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnGatewayPropsMixin.AuthorizerConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"custom_jwt_authorizer": "customJwtAuthorizer"},
    )
    class AuthorizerConfigurationProperty:
        def __init__(
            self,
            *,
            custom_jwt_authorizer: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayPropsMixin.CustomJWTAuthorizerConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param custom_jwt_authorizer: The authorizer configuration for the gateway.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gateway-authorizerconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                authorizer_configuration_property = bedrockagentcore_mixins.CfnGatewayPropsMixin.AuthorizerConfigurationProperty(
                    custom_jwt_authorizer=bedrockagentcore_mixins.CfnGatewayPropsMixin.CustomJWTAuthorizerConfigurationProperty(
                        allowed_audience=["allowedAudience"],
                        allowed_clients=["allowedClients"],
                        discovery_url="discoveryUrl"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7780b5f278fbfa5dd7b19275cc49e773b3f769274712a5be92dd8a5805bb5068)
                check_type(argname="argument custom_jwt_authorizer", value=custom_jwt_authorizer, expected_type=type_hints["custom_jwt_authorizer"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if custom_jwt_authorizer is not None:
                self._values["custom_jwt_authorizer"] = custom_jwt_authorizer

        @builtins.property
        def custom_jwt_authorizer(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayPropsMixin.CustomJWTAuthorizerConfigurationProperty"]]:
            '''The authorizer configuration for the gateway.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gateway-authorizerconfiguration.html#cfn-bedrockagentcore-gateway-authorizerconfiguration-customjwtauthorizer
            '''
            result = self._values.get("custom_jwt_authorizer")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayPropsMixin.CustomJWTAuthorizerConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthorizerConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnGatewayPropsMixin.CustomJWTAuthorizerConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allowed_audience": "allowedAudience",
            "allowed_clients": "allowedClients",
            "discovery_url": "discoveryUrl",
        },
    )
    class CustomJWTAuthorizerConfigurationProperty:
        def __init__(
            self,
            *,
            allowed_audience: typing.Optional[typing.Sequence[builtins.str]] = None,
            allowed_clients: typing.Optional[typing.Sequence[builtins.str]] = None,
            discovery_url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param allowed_audience: The allowed audience authorized for the gateway target.
            :param allowed_clients: 
            :param discovery_url: The discovery URL for the authorizer configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gateway-customjwtauthorizerconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                custom_jWTAuthorizer_configuration_property = bedrockagentcore_mixins.CfnGatewayPropsMixin.CustomJWTAuthorizerConfigurationProperty(
                    allowed_audience=["allowedAudience"],
                    allowed_clients=["allowedClients"],
                    discovery_url="discoveryUrl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__09d306a8dade079a9b37559f6cc8fc453da9f07af16ad8de7b2fe3941913faad)
                check_type(argname="argument allowed_audience", value=allowed_audience, expected_type=type_hints["allowed_audience"])
                check_type(argname="argument allowed_clients", value=allowed_clients, expected_type=type_hints["allowed_clients"])
                check_type(argname="argument discovery_url", value=discovery_url, expected_type=type_hints["discovery_url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allowed_audience is not None:
                self._values["allowed_audience"] = allowed_audience
            if allowed_clients is not None:
                self._values["allowed_clients"] = allowed_clients
            if discovery_url is not None:
                self._values["discovery_url"] = discovery_url

        @builtins.property
        def allowed_audience(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The allowed audience authorized for the gateway target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gateway-customjwtauthorizerconfiguration.html#cfn-bedrockagentcore-gateway-customjwtauthorizerconfiguration-allowedaudience
            '''
            result = self._values.get("allowed_audience")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def allowed_clients(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gateway-customjwtauthorizerconfiguration.html#cfn-bedrockagentcore-gateway-customjwtauthorizerconfiguration-allowedclients
            '''
            result = self._values.get("allowed_clients")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def discovery_url(self) -> typing.Optional[builtins.str]:
            '''The discovery URL for the authorizer configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gateway-customjwtauthorizerconfiguration.html#cfn-bedrockagentcore-gateway-customjwtauthorizerconfiguration-discoveryurl
            '''
            result = self._values.get("discovery_url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomJWTAuthorizerConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnGatewayPropsMixin.GatewayProtocolConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"mcp": "mcp"},
    )
    class GatewayProtocolConfigurationProperty:
        def __init__(
            self,
            *,
            mcp: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayPropsMixin.MCPGatewayConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The protocol configuration.

            :param mcp: The gateway protocol configuration for MCP.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gateway-gatewayprotocolconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                gateway_protocol_configuration_property = bedrockagentcore_mixins.CfnGatewayPropsMixin.GatewayProtocolConfigurationProperty(
                    mcp=bedrockagentcore_mixins.CfnGatewayPropsMixin.MCPGatewayConfigurationProperty(
                        instructions="instructions",
                        search_type="searchType",
                        supported_versions=["supportedVersions"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b2fa668753da52653a0818828285e7cecac19ca8a4b2a3792f38db7df43ffa69)
                check_type(argname="argument mcp", value=mcp, expected_type=type_hints["mcp"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if mcp is not None:
                self._values["mcp"] = mcp

        @builtins.property
        def mcp(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayPropsMixin.MCPGatewayConfigurationProperty"]]:
            '''The gateway protocol configuration for MCP.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gateway-gatewayprotocolconfiguration.html#cfn-bedrockagentcore-gateway-gatewayprotocolconfiguration-mcp
            '''
            result = self._values.get("mcp")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayPropsMixin.MCPGatewayConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GatewayProtocolConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnGatewayPropsMixin.MCPGatewayConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "instructions": "instructions",
            "search_type": "searchType",
            "supported_versions": "supportedVersions",
        },
    )
    class MCPGatewayConfigurationProperty:
        def __init__(
            self,
            *,
            instructions: typing.Optional[builtins.str] = None,
            search_type: typing.Optional[builtins.str] = None,
            supported_versions: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The gateway configuration for MCP.

            :param instructions: 
            :param search_type: The MCP gateway configuration search type.
            :param supported_versions: The supported versions for the MCP configuration for the gateway target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gateway-mcpgatewayconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                m_cPGateway_configuration_property = bedrockagentcore_mixins.CfnGatewayPropsMixin.MCPGatewayConfigurationProperty(
                    instructions="instructions",
                    search_type="searchType",
                    supported_versions=["supportedVersions"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__03cc6dbf06d50f73aba296edc1a25298b46b34493386d3d157b280a61838f917)
                check_type(argname="argument instructions", value=instructions, expected_type=type_hints["instructions"])
                check_type(argname="argument search_type", value=search_type, expected_type=type_hints["search_type"])
                check_type(argname="argument supported_versions", value=supported_versions, expected_type=type_hints["supported_versions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if instructions is not None:
                self._values["instructions"] = instructions
            if search_type is not None:
                self._values["search_type"] = search_type
            if supported_versions is not None:
                self._values["supported_versions"] = supported_versions

        @builtins.property
        def instructions(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gateway-mcpgatewayconfiguration.html#cfn-bedrockagentcore-gateway-mcpgatewayconfiguration-instructions
            '''
            result = self._values.get("instructions")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def search_type(self) -> typing.Optional[builtins.str]:
            '''The MCP gateway configuration search type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gateway-mcpgatewayconfiguration.html#cfn-bedrockagentcore-gateway-mcpgatewayconfiguration-searchtype
            '''
            result = self._values.get("search_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def supported_versions(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The supported versions for the MCP configuration for the gateway target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gateway-mcpgatewayconfiguration.html#cfn-bedrockagentcore-gateway-mcpgatewayconfiguration-supportedversions
            '''
            result = self._values.get("supported_versions")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MCPGatewayConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnGatewayPropsMixin.WorkloadIdentityDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={"workload_identity_arn": "workloadIdentityArn"},
    )
    class WorkloadIdentityDetailsProperty:
        def __init__(
            self,
            *,
            workload_identity_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The workload identity details for the gateway.

            :param workload_identity_arn: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gateway-workloadidentitydetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                workload_identity_details_property = bedrockagentcore_mixins.CfnGatewayPropsMixin.WorkloadIdentityDetailsProperty(
                    workload_identity_arn="workloadIdentityArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__23fdb6c28327da2b10984c6b33f68cae77f1f92d611c594e46d86aca08cc5315)
                check_type(argname="argument workload_identity_arn", value=workload_identity_arn, expected_type=type_hints["workload_identity_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if workload_identity_arn is not None:
                self._values["workload_identity_arn"] = workload_identity_arn

        @builtins.property
        def workload_identity_arn(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gateway-workloadidentitydetails.html#cfn-bedrockagentcore-gateway-workloadidentitydetails-workloadidentityarn
            '''
            result = self._values.get("workload_identity_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WorkloadIdentityDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnGatewayTargetMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "credential_provider_configurations": "credentialProviderConfigurations",
        "description": "description",
        "gateway_identifier": "gatewayIdentifier",
        "name": "name",
        "target_configuration": "targetConfiguration",
    },
)
class CfnGatewayTargetMixinProps:
    def __init__(
        self,
        *,
        credential_provider_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayTargetPropsMixin.CredentialProviderConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        gateway_identifier: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        target_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayTargetPropsMixin.TargetConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnGatewayTargetPropsMixin.

        :param credential_provider_configurations: The OAuth credential provider configuration.
        :param description: The description for the gateway target.
        :param gateway_identifier: The gateway ID for the gateway target.
        :param name: The name for the gateway target.
        :param target_configuration: The target configuration for the Smithy model target.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-gatewaytarget.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
            
            # schema_definition_property_: bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.SchemaDefinitionProperty
            
            cfn_gateway_target_mixin_props = bedrockagentcore_mixins.CfnGatewayTargetMixinProps(
                credential_provider_configurations=[bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.CredentialProviderConfigurationProperty(
                    credential_provider=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.CredentialProviderProperty(
                        api_key_credential_provider=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.ApiKeyCredentialProviderProperty(
                            credential_location="credentialLocation",
                            credential_parameter_name="credentialParameterName",
                            credential_prefix="credentialPrefix",
                            provider_arn="providerArn"
                        ),
                        oauth_credential_provider=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.OAuthCredentialProviderProperty(
                            custom_parameters={
                                "custom_parameters_key": "customParameters"
                            },
                            provider_arn="providerArn",
                            scopes=["scopes"]
                        )
                    ),
                    credential_provider_type="credentialProviderType"
                )],
                description="description",
                gateway_identifier="gatewayIdentifier",
                name="name",
                target_configuration=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.TargetConfigurationProperty(
                    mcp=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.McpTargetConfigurationProperty(
                        lambda_=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.McpLambdaTargetConfigurationProperty(
                            lambda_arn="lambdaArn",
                            tool_schema=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.ToolSchemaProperty(
                                inline_payload=[bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.ToolDefinitionProperty(
                                    description="description",
                                    input_schema=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.SchemaDefinitionProperty(
                                        description="description",
                                        items=schema_definition_property_,
                                        properties={
                                            "properties_key": schema_definition_property_
                                        },
                                        required=["required"],
                                        type="type"
                                    ),
                                    name="name",
                                    output_schema=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.SchemaDefinitionProperty(
                                        description="description",
                                        items=schema_definition_property_,
                                        properties={
                                            "properties_key": schema_definition_property_
                                        },
                                        required=["required"],
                                        type="type"
                                    )
                                )],
                                s3=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.S3ConfigurationProperty(
                                    bucket_owner_account_id="bucketOwnerAccountId",
                                    uri="uri"
                                )
                            )
                        ),
                        mcp_server=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.McpServerTargetConfigurationProperty(
                            endpoint="endpoint"
                        ),
                        open_api_schema=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.ApiSchemaConfigurationProperty(
                            inline_payload="inlinePayload",
                            s3=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.S3ConfigurationProperty(
                                bucket_owner_account_id="bucketOwnerAccountId",
                                uri="uri"
                            )
                        ),
                        smithy_model=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.ApiSchemaConfigurationProperty(
                            inline_payload="inlinePayload",
                            s3=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.S3ConfigurationProperty(
                                bucket_owner_account_id="bucketOwnerAccountId",
                                uri="uri"
                            )
                        )
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19556b18f1f5cc739a0b467612594132917bcd7359c0c6cac83759803e3ac22a)
            check_type(argname="argument credential_provider_configurations", value=credential_provider_configurations, expected_type=type_hints["credential_provider_configurations"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument gateway_identifier", value=gateway_identifier, expected_type=type_hints["gateway_identifier"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument target_configuration", value=target_configuration, expected_type=type_hints["target_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if credential_provider_configurations is not None:
            self._values["credential_provider_configurations"] = credential_provider_configurations
        if description is not None:
            self._values["description"] = description
        if gateway_identifier is not None:
            self._values["gateway_identifier"] = gateway_identifier
        if name is not None:
            self._values["name"] = name
        if target_configuration is not None:
            self._values["target_configuration"] = target_configuration

    @builtins.property
    def credential_provider_configurations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayTargetPropsMixin.CredentialProviderConfigurationProperty"]]]]:
        '''The OAuth credential provider configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-gatewaytarget.html#cfn-bedrockagentcore-gatewaytarget-credentialproviderconfigurations
        '''
        result = self._values.get("credential_provider_configurations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayTargetPropsMixin.CredentialProviderConfigurationProperty"]]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description for the gateway target.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-gatewaytarget.html#cfn-bedrockagentcore-gatewaytarget-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gateway_identifier(self) -> typing.Optional[builtins.str]:
        '''The gateway ID for the gateway target.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-gatewaytarget.html#cfn-bedrockagentcore-gatewaytarget-gatewayidentifier
        '''
        result = self._values.get("gateway_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name for the gateway target.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-gatewaytarget.html#cfn-bedrockagentcore-gatewaytarget-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayTargetPropsMixin.TargetConfigurationProperty"]]:
        '''The target configuration for the Smithy model target.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-gatewaytarget.html#cfn-bedrockagentcore-gatewaytarget-targetconfiguration
        '''
        result = self._values.get("target_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayTargetPropsMixin.TargetConfigurationProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGatewayTargetMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnGatewayTargetPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnGatewayTargetPropsMixin",
):
    '''After creating a gateway, you can add targets, which define the tools that your gateway will host.

    For more information about adding gateway targets, see `Add targets to an existing gateway <https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-building-adding-targets.html>`_ .

    See the *Properties* section below for descriptions of both the required and optional properties.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-gatewaytarget.html
    :cloudformationResource: AWS::BedrockAgentCore::GatewayTarget
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
        
        # schema_definition_property_: bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.SchemaDefinitionProperty
        
        cfn_gateway_target_props_mixin = bedrockagentcore_mixins.CfnGatewayTargetPropsMixin(bedrockagentcore_mixins.CfnGatewayTargetMixinProps(
            credential_provider_configurations=[bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.CredentialProviderConfigurationProperty(
                credential_provider=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.CredentialProviderProperty(
                    api_key_credential_provider=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.ApiKeyCredentialProviderProperty(
                        credential_location="credentialLocation",
                        credential_parameter_name="credentialParameterName",
                        credential_prefix="credentialPrefix",
                        provider_arn="providerArn"
                    ),
                    oauth_credential_provider=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.OAuthCredentialProviderProperty(
                        custom_parameters={
                            "custom_parameters_key": "customParameters"
                        },
                        provider_arn="providerArn",
                        scopes=["scopes"]
                    )
                ),
                credential_provider_type="credentialProviderType"
            )],
            description="description",
            gateway_identifier="gatewayIdentifier",
            name="name",
            target_configuration=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.TargetConfigurationProperty(
                mcp=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.McpTargetConfigurationProperty(
                    lambda_=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.McpLambdaTargetConfigurationProperty(
                        lambda_arn="lambdaArn",
                        tool_schema=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.ToolSchemaProperty(
                            inline_payload=[bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.ToolDefinitionProperty(
                                description="description",
                                input_schema=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.SchemaDefinitionProperty(
                                    description="description",
                                    items=schema_definition_property_,
                                    properties={
                                        "properties_key": schema_definition_property_
                                    },
                                    required=["required"],
                                    type="type"
                                ),
                                name="name",
                                output_schema=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.SchemaDefinitionProperty(
                                    description="description",
                                    items=schema_definition_property_,
                                    properties={
                                        "properties_key": schema_definition_property_
                                    },
                                    required=["required"],
                                    type="type"
                                )
                            )],
                            s3=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.S3ConfigurationProperty(
                                bucket_owner_account_id="bucketOwnerAccountId",
                                uri="uri"
                            )
                        )
                    ),
                    mcp_server=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.McpServerTargetConfigurationProperty(
                        endpoint="endpoint"
                    ),
                    open_api_schema=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.ApiSchemaConfigurationProperty(
                        inline_payload="inlinePayload",
                        s3=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.S3ConfigurationProperty(
                            bucket_owner_account_id="bucketOwnerAccountId",
                            uri="uri"
                        )
                    ),
                    smithy_model=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.ApiSchemaConfigurationProperty(
                        inline_payload="inlinePayload",
                        s3=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.S3ConfigurationProperty(
                            bucket_owner_account_id="bucketOwnerAccountId",
                            uri="uri"
                        )
                    )
                )
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnGatewayTargetMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::BedrockAgentCore::GatewayTarget``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2ba80982a2a8945b00e3d59a8ecfc612aeb6e2cdce5212b16fcf10f9511c9c6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1500ade9b8a56b6041d403a141734dc27fdfae69423a391a044b933d679f0e2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07b78f3fa6f648b515e6867c55713eac6761ba88e466a95b55160f74101047a1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnGatewayTargetMixinProps:
        return typing.cast(CfnGatewayTargetMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnGatewayTargetPropsMixin.ApiKeyCredentialProviderProperty",
        jsii_struct_bases=[],
        name_mapping={
            "credential_location": "credentialLocation",
            "credential_parameter_name": "credentialParameterName",
            "credential_prefix": "credentialPrefix",
            "provider_arn": "providerArn",
        },
    )
    class ApiKeyCredentialProviderProperty:
        def __init__(
            self,
            *,
            credential_location: typing.Optional[builtins.str] = None,
            credential_parameter_name: typing.Optional[builtins.str] = None,
            credential_prefix: typing.Optional[builtins.str] = None,
            provider_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The API key credential provider for the gateway target.

            :param credential_location: The credential location for the gateway target.
            :param credential_parameter_name: The credential parameter name for the provider for the gateway target.
            :param credential_prefix: The API key credential provider for the gateway target.
            :param provider_arn: The provider ARN for the gateway target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-apikeycredentialprovider.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                api_key_credential_provider_property = bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.ApiKeyCredentialProviderProperty(
                    credential_location="credentialLocation",
                    credential_parameter_name="credentialParameterName",
                    credential_prefix="credentialPrefix",
                    provider_arn="providerArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6d6e78004d554f96bb5d69de161cbbc5cf3be027e3f39714b79c71b21208e7a7)
                check_type(argname="argument credential_location", value=credential_location, expected_type=type_hints["credential_location"])
                check_type(argname="argument credential_parameter_name", value=credential_parameter_name, expected_type=type_hints["credential_parameter_name"])
                check_type(argname="argument credential_prefix", value=credential_prefix, expected_type=type_hints["credential_prefix"])
                check_type(argname="argument provider_arn", value=provider_arn, expected_type=type_hints["provider_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if credential_location is not None:
                self._values["credential_location"] = credential_location
            if credential_parameter_name is not None:
                self._values["credential_parameter_name"] = credential_parameter_name
            if credential_prefix is not None:
                self._values["credential_prefix"] = credential_prefix
            if provider_arn is not None:
                self._values["provider_arn"] = provider_arn

        @builtins.property
        def credential_location(self) -> typing.Optional[builtins.str]:
            '''The credential location for the gateway target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-apikeycredentialprovider.html#cfn-bedrockagentcore-gatewaytarget-apikeycredentialprovider-credentiallocation
            '''
            result = self._values.get("credential_location")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def credential_parameter_name(self) -> typing.Optional[builtins.str]:
            '''The credential parameter name for the provider for the gateway target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-apikeycredentialprovider.html#cfn-bedrockagentcore-gatewaytarget-apikeycredentialprovider-credentialparametername
            '''
            result = self._values.get("credential_parameter_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def credential_prefix(self) -> typing.Optional[builtins.str]:
            '''The API key credential provider for the gateway target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-apikeycredentialprovider.html#cfn-bedrockagentcore-gatewaytarget-apikeycredentialprovider-credentialprefix
            '''
            result = self._values.get("credential_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def provider_arn(self) -> typing.Optional[builtins.str]:
            '''The provider ARN for the gateway target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-apikeycredentialprovider.html#cfn-bedrockagentcore-gatewaytarget-apikeycredentialprovider-providerarn
            '''
            result = self._values.get("provider_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApiKeyCredentialProviderProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnGatewayTargetPropsMixin.ApiSchemaConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"inline_payload": "inlinePayload", "s3": "s3"},
    )
    class ApiSchemaConfigurationProperty:
        def __init__(
            self,
            *,
            inline_payload: typing.Optional[builtins.str] = None,
            s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayTargetPropsMixin.S3ConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The API schema configuration for the gateway target.

            :param inline_payload: The inline payload for the gateway.
            :param s3: The API schema configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-apischemaconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                api_schema_configuration_property = bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.ApiSchemaConfigurationProperty(
                    inline_payload="inlinePayload",
                    s3=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.S3ConfigurationProperty(
                        bucket_owner_account_id="bucketOwnerAccountId",
                        uri="uri"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ec0b2b1fccc4d0c00228dc8c1b9e28a5838b14ee418ed961fd608551f407321f)
                check_type(argname="argument inline_payload", value=inline_payload, expected_type=type_hints["inline_payload"])
                check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if inline_payload is not None:
                self._values["inline_payload"] = inline_payload
            if s3 is not None:
                self._values["s3"] = s3

        @builtins.property
        def inline_payload(self) -> typing.Optional[builtins.str]:
            '''The inline payload for the gateway.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-apischemaconfiguration.html#cfn-bedrockagentcore-gatewaytarget-apischemaconfiguration-inlinepayload
            '''
            result = self._values.get("inline_payload")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayTargetPropsMixin.S3ConfigurationProperty"]]:
            '''The API schema configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-apischemaconfiguration.html#cfn-bedrockagentcore-gatewaytarget-apischemaconfiguration-s3
            '''
            result = self._values.get("s3")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayTargetPropsMixin.S3ConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApiSchemaConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnGatewayTargetPropsMixin.CredentialProviderConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "credential_provider": "credentialProvider",
            "credential_provider_type": "credentialProviderType",
        },
    )
    class CredentialProviderConfigurationProperty:
        def __init__(
            self,
            *,
            credential_provider: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayTargetPropsMixin.CredentialProviderProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            credential_provider_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The credential provider configuration for the gateway target.

            :param credential_provider: The credential provider for the gateway target.
            :param credential_provider_type: The credential provider type for the gateway target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-credentialproviderconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                credential_provider_configuration_property = bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.CredentialProviderConfigurationProperty(
                    credential_provider=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.CredentialProviderProperty(
                        api_key_credential_provider=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.ApiKeyCredentialProviderProperty(
                            credential_location="credentialLocation",
                            credential_parameter_name="credentialParameterName",
                            credential_prefix="credentialPrefix",
                            provider_arn="providerArn"
                        ),
                        oauth_credential_provider=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.OAuthCredentialProviderProperty(
                            custom_parameters={
                                "custom_parameters_key": "customParameters"
                            },
                            provider_arn="providerArn",
                            scopes=["scopes"]
                        )
                    ),
                    credential_provider_type="credentialProviderType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__82aa1cdeb6038e3bb7e8b5ecb70ef1f6ae37bf0cefe5a522b2e79525a51e2309)
                check_type(argname="argument credential_provider", value=credential_provider, expected_type=type_hints["credential_provider"])
                check_type(argname="argument credential_provider_type", value=credential_provider_type, expected_type=type_hints["credential_provider_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if credential_provider is not None:
                self._values["credential_provider"] = credential_provider
            if credential_provider_type is not None:
                self._values["credential_provider_type"] = credential_provider_type

        @builtins.property
        def credential_provider(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayTargetPropsMixin.CredentialProviderProperty"]]:
            '''The credential provider for the gateway target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-credentialproviderconfiguration.html#cfn-bedrockagentcore-gatewaytarget-credentialproviderconfiguration-credentialprovider
            '''
            result = self._values.get("credential_provider")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayTargetPropsMixin.CredentialProviderProperty"]], result)

        @builtins.property
        def credential_provider_type(self) -> typing.Optional[builtins.str]:
            '''The credential provider type for the gateway target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-credentialproviderconfiguration.html#cfn-bedrockagentcore-gatewaytarget-credentialproviderconfiguration-credentialprovidertype
            '''
            result = self._values.get("credential_provider_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CredentialProviderConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnGatewayTargetPropsMixin.CredentialProviderProperty",
        jsii_struct_bases=[],
        name_mapping={
            "api_key_credential_provider": "apiKeyCredentialProvider",
            "oauth_credential_provider": "oauthCredentialProvider",
        },
    )
    class CredentialProviderProperty:
        def __init__(
            self,
            *,
            api_key_credential_provider: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayTargetPropsMixin.ApiKeyCredentialProviderProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            oauth_credential_provider: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayTargetPropsMixin.OAuthCredentialProviderProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param api_key_credential_provider: The API key credential provider.
            :param oauth_credential_provider: The OAuth credential provider for the gateway target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-credentialprovider.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                credential_provider_property = bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.CredentialProviderProperty(
                    api_key_credential_provider=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.ApiKeyCredentialProviderProperty(
                        credential_location="credentialLocation",
                        credential_parameter_name="credentialParameterName",
                        credential_prefix="credentialPrefix",
                        provider_arn="providerArn"
                    ),
                    oauth_credential_provider=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.OAuthCredentialProviderProperty(
                        custom_parameters={
                            "custom_parameters_key": "customParameters"
                        },
                        provider_arn="providerArn",
                        scopes=["scopes"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__40f1df35e2b3ba63956b57d7e40a354571c1912ec13aeaf360c472669bb5a9a4)
                check_type(argname="argument api_key_credential_provider", value=api_key_credential_provider, expected_type=type_hints["api_key_credential_provider"])
                check_type(argname="argument oauth_credential_provider", value=oauth_credential_provider, expected_type=type_hints["oauth_credential_provider"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if api_key_credential_provider is not None:
                self._values["api_key_credential_provider"] = api_key_credential_provider
            if oauth_credential_provider is not None:
                self._values["oauth_credential_provider"] = oauth_credential_provider

        @builtins.property
        def api_key_credential_provider(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayTargetPropsMixin.ApiKeyCredentialProviderProperty"]]:
            '''The API key credential provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-credentialprovider.html#cfn-bedrockagentcore-gatewaytarget-credentialprovider-apikeycredentialprovider
            '''
            result = self._values.get("api_key_credential_provider")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayTargetPropsMixin.ApiKeyCredentialProviderProperty"]], result)

        @builtins.property
        def oauth_credential_provider(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayTargetPropsMixin.OAuthCredentialProviderProperty"]]:
            '''The OAuth credential provider for the gateway target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-credentialprovider.html#cfn-bedrockagentcore-gatewaytarget-credentialprovider-oauthcredentialprovider
            '''
            result = self._values.get("oauth_credential_provider")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayTargetPropsMixin.OAuthCredentialProviderProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CredentialProviderProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnGatewayTargetPropsMixin.McpLambdaTargetConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"lambda_arn": "lambdaArn", "tool_schema": "toolSchema"},
    )
    class McpLambdaTargetConfigurationProperty:
        def __init__(
            self,
            *,
            lambda_arn: typing.Optional[builtins.str] = None,
            tool_schema: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayTargetPropsMixin.ToolSchemaProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The Lambda target configuration.

            :param lambda_arn: The ARN of the Lambda target configuration.
            :param tool_schema: The tool schema configuration for the gateway target MCP configuration for Lambda.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-mcplambdatargetconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                # schema_definition_property_: bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.SchemaDefinitionProperty
                
                mcp_lambda_target_configuration_property = bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.McpLambdaTargetConfigurationProperty(
                    lambda_arn="lambdaArn",
                    tool_schema=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.ToolSchemaProperty(
                        inline_payload=[bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.ToolDefinitionProperty(
                            description="description",
                            input_schema=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.SchemaDefinitionProperty(
                                description="description",
                                items=schema_definition_property_,
                                properties={
                                    "properties_key": schema_definition_property_
                                },
                                required=["required"],
                                type="type"
                            ),
                            name="name",
                            output_schema=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.SchemaDefinitionProperty(
                                description="description",
                                items=schema_definition_property_,
                                properties={
                                    "properties_key": schema_definition_property_
                                },
                                required=["required"],
                                type="type"
                            )
                        )],
                        s3=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.S3ConfigurationProperty(
                            bucket_owner_account_id="bucketOwnerAccountId",
                            uri="uri"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ea6b6e539afb296fe5821099c77a2f79217939d36a87a996842d39469298f848)
                check_type(argname="argument lambda_arn", value=lambda_arn, expected_type=type_hints["lambda_arn"])
                check_type(argname="argument tool_schema", value=tool_schema, expected_type=type_hints["tool_schema"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if lambda_arn is not None:
                self._values["lambda_arn"] = lambda_arn
            if tool_schema is not None:
                self._values["tool_schema"] = tool_schema

        @builtins.property
        def lambda_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the Lambda target configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-mcplambdatargetconfiguration.html#cfn-bedrockagentcore-gatewaytarget-mcplambdatargetconfiguration-lambdaarn
            '''
            result = self._values.get("lambda_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tool_schema(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayTargetPropsMixin.ToolSchemaProperty"]]:
            '''The tool schema configuration for the gateway target MCP configuration for Lambda.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-mcplambdatargetconfiguration.html#cfn-bedrockagentcore-gatewaytarget-mcplambdatargetconfiguration-toolschema
            '''
            result = self._values.get("tool_schema")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayTargetPropsMixin.ToolSchemaProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "McpLambdaTargetConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnGatewayTargetPropsMixin.McpServerTargetConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"endpoint": "endpoint"},
    )
    class McpServerTargetConfigurationProperty:
        def __init__(self, *, endpoint: typing.Optional[builtins.str] = None) -> None:
            '''
            :param endpoint: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-mcpservertargetconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                mcp_server_target_configuration_property = bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.McpServerTargetConfigurationProperty(
                    endpoint="endpoint"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6f346fb508244d33d369be50d367d2a83b9b1a4956d25d91d33276637fe24465)
                check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if endpoint is not None:
                self._values["endpoint"] = endpoint

        @builtins.property
        def endpoint(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-mcpservertargetconfiguration.html#cfn-bedrockagentcore-gatewaytarget-mcpservertargetconfiguration-endpoint
            '''
            result = self._values.get("endpoint")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "McpServerTargetConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnGatewayTargetPropsMixin.McpTargetConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "lambda_": "lambda",
            "mcp_server": "mcpServer",
            "open_api_schema": "openApiSchema",
            "smithy_model": "smithyModel",
        },
    )
    class McpTargetConfigurationProperty:
        def __init__(
            self,
            *,
            lambda_: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayTargetPropsMixin.McpLambdaTargetConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            mcp_server: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayTargetPropsMixin.McpServerTargetConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            open_api_schema: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayTargetPropsMixin.ApiSchemaConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            smithy_model: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayTargetPropsMixin.ApiSchemaConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The MCP target configuration for the gateway target.

            :param lambda_: The Lambda MCP configuration for the gateway target.
            :param mcp_server: 
            :param open_api_schema: The OpenApi schema for the gateway target MCP configuration.
            :param smithy_model: The target configuration for the Smithy model target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-mcptargetconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                # schema_definition_property_: bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.SchemaDefinitionProperty
                
                mcp_target_configuration_property = bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.McpTargetConfigurationProperty(
                    lambda_=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.McpLambdaTargetConfigurationProperty(
                        lambda_arn="lambdaArn",
                        tool_schema=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.ToolSchemaProperty(
                            inline_payload=[bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.ToolDefinitionProperty(
                                description="description",
                                input_schema=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.SchemaDefinitionProperty(
                                    description="description",
                                    items=schema_definition_property_,
                                    properties={
                                        "properties_key": schema_definition_property_
                                    },
                                    required=["required"],
                                    type="type"
                                ),
                                name="name",
                                output_schema=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.SchemaDefinitionProperty(
                                    description="description",
                                    items=schema_definition_property_,
                                    properties={
                                        "properties_key": schema_definition_property_
                                    },
                                    required=["required"],
                                    type="type"
                                )
                            )],
                            s3=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.S3ConfigurationProperty(
                                bucket_owner_account_id="bucketOwnerAccountId",
                                uri="uri"
                            )
                        )
                    ),
                    mcp_server=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.McpServerTargetConfigurationProperty(
                        endpoint="endpoint"
                    ),
                    open_api_schema=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.ApiSchemaConfigurationProperty(
                        inline_payload="inlinePayload",
                        s3=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.S3ConfigurationProperty(
                            bucket_owner_account_id="bucketOwnerAccountId",
                            uri="uri"
                        )
                    ),
                    smithy_model=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.ApiSchemaConfigurationProperty(
                        inline_payload="inlinePayload",
                        s3=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.S3ConfigurationProperty(
                            bucket_owner_account_id="bucketOwnerAccountId",
                            uri="uri"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__419e954162a5c3cfb94aecf0d79ec2f8c07e746de6ce5752a57d2392001029a1)
                check_type(argname="argument lambda_", value=lambda_, expected_type=type_hints["lambda_"])
                check_type(argname="argument mcp_server", value=mcp_server, expected_type=type_hints["mcp_server"])
                check_type(argname="argument open_api_schema", value=open_api_schema, expected_type=type_hints["open_api_schema"])
                check_type(argname="argument smithy_model", value=smithy_model, expected_type=type_hints["smithy_model"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if lambda_ is not None:
                self._values["lambda_"] = lambda_
            if mcp_server is not None:
                self._values["mcp_server"] = mcp_server
            if open_api_schema is not None:
                self._values["open_api_schema"] = open_api_schema
            if smithy_model is not None:
                self._values["smithy_model"] = smithy_model

        @builtins.property
        def lambda_(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayTargetPropsMixin.McpLambdaTargetConfigurationProperty"]]:
            '''The Lambda MCP configuration for the gateway target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-mcptargetconfiguration.html#cfn-bedrockagentcore-gatewaytarget-mcptargetconfiguration-lambda
            '''
            result = self._values.get("lambda_")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayTargetPropsMixin.McpLambdaTargetConfigurationProperty"]], result)

        @builtins.property
        def mcp_server(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayTargetPropsMixin.McpServerTargetConfigurationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-mcptargetconfiguration.html#cfn-bedrockagentcore-gatewaytarget-mcptargetconfiguration-mcpserver
            '''
            result = self._values.get("mcp_server")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayTargetPropsMixin.McpServerTargetConfigurationProperty"]], result)

        @builtins.property
        def open_api_schema(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayTargetPropsMixin.ApiSchemaConfigurationProperty"]]:
            '''The OpenApi schema for the gateway target MCP configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-mcptargetconfiguration.html#cfn-bedrockagentcore-gatewaytarget-mcptargetconfiguration-openapischema
            '''
            result = self._values.get("open_api_schema")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayTargetPropsMixin.ApiSchemaConfigurationProperty"]], result)

        @builtins.property
        def smithy_model(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayTargetPropsMixin.ApiSchemaConfigurationProperty"]]:
            '''The target configuration for the Smithy model target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-mcptargetconfiguration.html#cfn-bedrockagentcore-gatewaytarget-mcptargetconfiguration-smithymodel
            '''
            result = self._values.get("smithy_model")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayTargetPropsMixin.ApiSchemaConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "McpTargetConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnGatewayTargetPropsMixin.OAuthCredentialProviderProperty",
        jsii_struct_bases=[],
        name_mapping={
            "custom_parameters": "customParameters",
            "provider_arn": "providerArn",
            "scopes": "scopes",
        },
    )
    class OAuthCredentialProviderProperty:
        def __init__(
            self,
            *,
            custom_parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            provider_arn: typing.Optional[builtins.str] = None,
            scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The OAuth credential provider for the gateway target.

            :param custom_parameters: The OAuth credential provider.
            :param provider_arn: The provider ARN for the gateway target.
            :param scopes: The OAuth credential provider scopes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-oauthcredentialprovider.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                o_auth_credential_provider_property = bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.OAuthCredentialProviderProperty(
                    custom_parameters={
                        "custom_parameters_key": "customParameters"
                    },
                    provider_arn="providerArn",
                    scopes=["scopes"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__72d4b7360437986df141ba04c58398cb3ec01211102469f73d58b351e6dfec3c)
                check_type(argname="argument custom_parameters", value=custom_parameters, expected_type=type_hints["custom_parameters"])
                check_type(argname="argument provider_arn", value=provider_arn, expected_type=type_hints["provider_arn"])
                check_type(argname="argument scopes", value=scopes, expected_type=type_hints["scopes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if custom_parameters is not None:
                self._values["custom_parameters"] = custom_parameters
            if provider_arn is not None:
                self._values["provider_arn"] = provider_arn
            if scopes is not None:
                self._values["scopes"] = scopes

        @builtins.property
        def custom_parameters(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''The OAuth credential provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-oauthcredentialprovider.html#cfn-bedrockagentcore-gatewaytarget-oauthcredentialprovider-customparameters
            '''
            result = self._values.get("custom_parameters")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def provider_arn(self) -> typing.Optional[builtins.str]:
            '''The provider ARN for the gateway target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-oauthcredentialprovider.html#cfn-bedrockagentcore-gatewaytarget-oauthcredentialprovider-providerarn
            '''
            result = self._values.get("provider_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def scopes(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The OAuth credential provider scopes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-oauthcredentialprovider.html#cfn-bedrockagentcore-gatewaytarget-oauthcredentialprovider-scopes
            '''
            result = self._values.get("scopes")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OAuthCredentialProviderProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnGatewayTargetPropsMixin.S3ConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket_owner_account_id": "bucketOwnerAccountId", "uri": "uri"},
    )
    class S3ConfigurationProperty:
        def __init__(
            self,
            *,
            bucket_owner_account_id: typing.Optional[builtins.str] = None,
            uri: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The S3 configuration for the gateway target.

            :param bucket_owner_account_id: The S3 configuration bucket owner account ID for the gateway target.
            :param uri: The configuration URI for the gateway target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-s3configuration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                s3_configuration_property = bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.S3ConfigurationProperty(
                    bucket_owner_account_id="bucketOwnerAccountId",
                    uri="uri"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fc24e04e603b6b463649742164a309f5f6a95f3834add9fcd491900eaa0127be)
                check_type(argname="argument bucket_owner_account_id", value=bucket_owner_account_id, expected_type=type_hints["bucket_owner_account_id"])
                check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_owner_account_id is not None:
                self._values["bucket_owner_account_id"] = bucket_owner_account_id
            if uri is not None:
                self._values["uri"] = uri

        @builtins.property
        def bucket_owner_account_id(self) -> typing.Optional[builtins.str]:
            '''The S3 configuration bucket owner account ID for the gateway target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-s3configuration.html#cfn-bedrockagentcore-gatewaytarget-s3configuration-bucketowneraccountid
            '''
            result = self._values.get("bucket_owner_account_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def uri(self) -> typing.Optional[builtins.str]:
            '''The configuration URI for the gateway target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-s3configuration.html#cfn-bedrockagentcore-gatewaytarget-s3configuration-uri
            '''
            result = self._values.get("uri")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3ConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnGatewayTargetPropsMixin.SchemaDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "description": "description",
            "items": "items",
            "properties": "properties",
            "required": "required",
            "type": "type",
        },
    )
    class SchemaDefinitionProperty:
        def __init__(
            self,
            *,
            description: typing.Optional[builtins.str] = None,
            items: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayTargetPropsMixin.SchemaDefinitionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayTargetPropsMixin.SchemaDefinitionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            required: typing.Optional[typing.Sequence[builtins.str]] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The schema definition for the gateway target.

            :param description: The workload identity details for the gateway.
            :param items: 
            :param properties: The schema definition properties for the gateway target.
            :param required: The schema definition.
            :param type: The scheme definition type for the gateway target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-schemadefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                # schema_definition_property_: bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.SchemaDefinitionProperty
                
                schema_definition_property = bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.SchemaDefinitionProperty(
                    description="description",
                    items=schema_definition_property_,
                    properties={
                        "properties_key": schema_definition_property_
                    },
                    required=["required"],
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b22363fe5c38adb2c65bce1301b554933a2f0ffeb4564940fb20fd7c004d4533)
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument items", value=items, expected_type=type_hints["items"])
                check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
                check_type(argname="argument required", value=required, expected_type=type_hints["required"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if description is not None:
                self._values["description"] = description
            if items is not None:
                self._values["items"] = items
            if properties is not None:
                self._values["properties"] = properties
            if required is not None:
                self._values["required"] = required
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The workload identity details for the gateway.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-schemadefinition.html#cfn-bedrockagentcore-gatewaytarget-schemadefinition-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def items(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayTargetPropsMixin.SchemaDefinitionProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-schemadefinition.html#cfn-bedrockagentcore-gatewaytarget-schemadefinition-items
            '''
            result = self._values.get("items")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayTargetPropsMixin.SchemaDefinitionProperty"]], result)

        @builtins.property
        def properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayTargetPropsMixin.SchemaDefinitionProperty"]]]]:
            '''The schema definition properties for the gateway target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-schemadefinition.html#cfn-bedrockagentcore-gatewaytarget-schemadefinition-properties
            '''
            result = self._values.get("properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayTargetPropsMixin.SchemaDefinitionProperty"]]]], result)

        @builtins.property
        def required(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The schema definition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-schemadefinition.html#cfn-bedrockagentcore-gatewaytarget-schemadefinition-required
            '''
            result = self._values.get("required")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The scheme definition type for the gateway target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-schemadefinition.html#cfn-bedrockagentcore-gatewaytarget-schemadefinition-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SchemaDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnGatewayTargetPropsMixin.TargetConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"mcp": "mcp"},
    )
    class TargetConfigurationProperty:
        def __init__(
            self,
            *,
            mcp: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayTargetPropsMixin.McpTargetConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The target configuration.

            :param mcp: The target configuration definition for MCP.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-targetconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                # schema_definition_property_: bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.SchemaDefinitionProperty
                
                target_configuration_property = bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.TargetConfigurationProperty(
                    mcp=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.McpTargetConfigurationProperty(
                        lambda_=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.McpLambdaTargetConfigurationProperty(
                            lambda_arn="lambdaArn",
                            tool_schema=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.ToolSchemaProperty(
                                inline_payload=[bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.ToolDefinitionProperty(
                                    description="description",
                                    input_schema=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.SchemaDefinitionProperty(
                                        description="description",
                                        items=schema_definition_property_,
                                        properties={
                                            "properties_key": schema_definition_property_
                                        },
                                        required=["required"],
                                        type="type"
                                    ),
                                    name="name",
                                    output_schema=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.SchemaDefinitionProperty(
                                        description="description",
                                        items=schema_definition_property_,
                                        properties={
                                            "properties_key": schema_definition_property_
                                        },
                                        required=["required"],
                                        type="type"
                                    )
                                )],
                                s3=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.S3ConfigurationProperty(
                                    bucket_owner_account_id="bucketOwnerAccountId",
                                    uri="uri"
                                )
                            )
                        ),
                        mcp_server=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.McpServerTargetConfigurationProperty(
                            endpoint="endpoint"
                        ),
                        open_api_schema=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.ApiSchemaConfigurationProperty(
                            inline_payload="inlinePayload",
                            s3=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.S3ConfigurationProperty(
                                bucket_owner_account_id="bucketOwnerAccountId",
                                uri="uri"
                            )
                        ),
                        smithy_model=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.ApiSchemaConfigurationProperty(
                            inline_payload="inlinePayload",
                            s3=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.S3ConfigurationProperty(
                                bucket_owner_account_id="bucketOwnerAccountId",
                                uri="uri"
                            )
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ca9b5efd2793f333b24c25666cfd4085fe90845f9c6c460c2b9089956e8625d2)
                check_type(argname="argument mcp", value=mcp, expected_type=type_hints["mcp"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if mcp is not None:
                self._values["mcp"] = mcp

        @builtins.property
        def mcp(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayTargetPropsMixin.McpTargetConfigurationProperty"]]:
            '''The target configuration definition for MCP.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-targetconfiguration.html#cfn-bedrockagentcore-gatewaytarget-targetconfiguration-mcp
            '''
            result = self._values.get("mcp")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayTargetPropsMixin.McpTargetConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnGatewayTargetPropsMixin.ToolDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "description": "description",
            "input_schema": "inputSchema",
            "name": "name",
            "output_schema": "outputSchema",
        },
    )
    class ToolDefinitionProperty:
        def __init__(
            self,
            *,
            description: typing.Optional[builtins.str] = None,
            input_schema: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayTargetPropsMixin.SchemaDefinitionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            name: typing.Optional[builtins.str] = None,
            output_schema: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayTargetPropsMixin.SchemaDefinitionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The tool definition for the gateway.

            :param description: 
            :param input_schema: The input schema for the gateway target.
            :param name: The tool name.
            :param output_schema: The tool definition output schema for the gateway target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-tooldefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                # schema_definition_property_: bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.SchemaDefinitionProperty
                
                tool_definition_property = bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.ToolDefinitionProperty(
                    description="description",
                    input_schema=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.SchemaDefinitionProperty(
                        description="description",
                        items=schema_definition_property_,
                        properties={
                            "properties_key": schema_definition_property_
                        },
                        required=["required"],
                        type="type"
                    ),
                    name="name",
                    output_schema=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.SchemaDefinitionProperty(
                        description="description",
                        items=schema_definition_property_,
                        properties={
                            "properties_key": schema_definition_property_
                        },
                        required=["required"],
                        type="type"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0e7466617717d2a857adab5cde5aeef03c3bd567b818132e47eb0b05706bc211)
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument input_schema", value=input_schema, expected_type=type_hints["input_schema"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument output_schema", value=output_schema, expected_type=type_hints["output_schema"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if description is not None:
                self._values["description"] = description
            if input_schema is not None:
                self._values["input_schema"] = input_schema
            if name is not None:
                self._values["name"] = name
            if output_schema is not None:
                self._values["output_schema"] = output_schema

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-tooldefinition.html#cfn-bedrockagentcore-gatewaytarget-tooldefinition-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def input_schema(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayTargetPropsMixin.SchemaDefinitionProperty"]]:
            '''The input schema for the gateway target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-tooldefinition.html#cfn-bedrockagentcore-gatewaytarget-tooldefinition-inputschema
            '''
            result = self._values.get("input_schema")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayTargetPropsMixin.SchemaDefinitionProperty"]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The tool name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-tooldefinition.html#cfn-bedrockagentcore-gatewaytarget-tooldefinition-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def output_schema(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayTargetPropsMixin.SchemaDefinitionProperty"]]:
            '''The tool definition output schema for the gateway target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-tooldefinition.html#cfn-bedrockagentcore-gatewaytarget-tooldefinition-outputschema
            '''
            result = self._values.get("output_schema")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayTargetPropsMixin.SchemaDefinitionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ToolDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnGatewayTargetPropsMixin.ToolSchemaProperty",
        jsii_struct_bases=[],
        name_mapping={"inline_payload": "inlinePayload", "s3": "s3"},
    )
    class ToolSchemaProperty:
        def __init__(
            self,
            *,
            inline_payload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayTargetPropsMixin.ToolDefinitionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayTargetPropsMixin.S3ConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The tool schema for the gateway target.

            :param inline_payload: The inline payload for the gateway target.
            :param s3: The S3 tool schema for the gateway target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-toolschema.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                # schema_definition_property_: bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.SchemaDefinitionProperty
                
                tool_schema_property = bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.ToolSchemaProperty(
                    inline_payload=[bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.ToolDefinitionProperty(
                        description="description",
                        input_schema=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.SchemaDefinitionProperty(
                            description="description",
                            items=schema_definition_property_,
                            properties={
                                "properties_key": schema_definition_property_
                            },
                            required=["required"],
                            type="type"
                        ),
                        name="name",
                        output_schema=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.SchemaDefinitionProperty(
                            description="description",
                            items=schema_definition_property_,
                            properties={
                                "properties_key": schema_definition_property_
                            },
                            required=["required"],
                            type="type"
                        )
                    )],
                    s3=bedrockagentcore_mixins.CfnGatewayTargetPropsMixin.S3ConfigurationProperty(
                        bucket_owner_account_id="bucketOwnerAccountId",
                        uri="uri"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8a3778d95b2b60099f86dfa32eb96663901bd2abb24c042bafdf6f24f8fc5824)
                check_type(argname="argument inline_payload", value=inline_payload, expected_type=type_hints["inline_payload"])
                check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if inline_payload is not None:
                self._values["inline_payload"] = inline_payload
            if s3 is not None:
                self._values["s3"] = s3

        @builtins.property
        def inline_payload(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayTargetPropsMixin.ToolDefinitionProperty"]]]]:
            '''The inline payload for the gateway target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-toolschema.html#cfn-bedrockagentcore-gatewaytarget-toolschema-inlinepayload
            '''
            result = self._values.get("inline_payload")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayTargetPropsMixin.ToolDefinitionProperty"]]]], result)

        @builtins.property
        def s3(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayTargetPropsMixin.S3ConfigurationProperty"]]:
            '''The S3 tool schema for the gateway target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-gatewaytarget-toolschema.html#cfn-bedrockagentcore-gatewaytarget-toolschema-s3
            '''
            result = self._values.get("s3")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayTargetPropsMixin.S3ConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ToolSchemaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


class CfnGatewayTraces(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnGatewayTraces",
):
    '''Builder for CfnGatewayLogsMixin to generate TRACES for CfnGateway.

    :cloudformationResource: AWS::BedrockAgentCore::Gateway
    :logType: TRACES
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
        
        cfn_gateway_traces = bedrockagentcore_mixins.CfnGatewayTraces()
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toXRay")
    def to_x_ray(self) -> CfnGatewayLogsMixin:
        '''Send traces to X-Ray.'''
        return typing.cast(CfnGatewayLogsMixin, jsii.invoke(self, "toXRay", []))


class CfnMemoryApplicationLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnMemoryApplicationLogs",
):
    '''Builder for CfnMemoryLogsMixin to generate APPLICATION_LOGS for CfnMemory.

    :cloudformationResource: AWS::BedrockAgentCore::Memory
    :logType: APPLICATION_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
        
        cfn_memory_application_logs = bedrockagentcore_mixins.CfnMemoryApplicationLogs()
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toFirehose")
    def to_firehose(
        self,
        delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
    ) -> "CfnMemoryLogsMixin":
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__533a3d66a676933e8c35334e4a0fe72487242446cd039c1e22c95749f0aff244)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast("CfnMemoryLogsMixin", jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> "CfnMemoryLogsMixin":
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d97379a3829ca32dd7989e0c3e7bf095ac6da663e9085d43b47ebfd720d90674)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast("CfnMemoryLogsMixin", jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> "CfnMemoryLogsMixin":
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb93e3d5eba71dee2742932d989deb728d771b8572a33bd3b7ec42e99158f2e1)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast("CfnMemoryLogsMixin", jsii.invoke(self, "toS3", [bucket]))


@jsii.implements(_IMixin_11e4b965)
class CfnMemoryLogsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnMemoryLogsMixin",
):
    '''Memory allows AI agents to maintain both immediate and long-term knowledge, enabling context-aware and personalized interactions.

    For more information about using Memory in Amazon Bedrock AgentCore, see `Host agent or tools with Amazon Bedrock AgentCore Memory <https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-getting-started.html>`_ .

    See the *Properties* section below for descriptions of both the required and optional properties.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-memory.html
    :cloudformationResource: AWS::BedrockAgentCore::Memory
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import aws_logs as logs
        from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
        
        # logs_delivery: logs.ILogsDelivery
        
        cfn_memory_logs_mixin = bedrockagentcore_mixins.CfnMemoryLogsMixin("logType", logs_delivery)
    '''

    def __init__(
        self,
        log_type: builtins.str,
        log_delivery: _ILogsDelivery_0d3c9e29,
    ) -> None:
        '''Create a mixin to enable vended logs for ``AWS::BedrockAgentCore::Memory``.

        :param log_type: Type of logs that are getting vended.
        :param log_delivery: Object in charge of setting up the delivery destination and delivery connection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ba1ef598af5d274cde246f021cccd97f3f9bacd72ca55bd4a2a655c256ffc02)
            check_type(argname="argument log_type", value=log_type, expected_type=type_hints["log_type"])
            check_type(argname="argument log_delivery", value=log_delivery, expected_type=type_hints["log_delivery"])
        jsii.create(self.__class__, self, [log_type, log_delivery])

    @jsii.member(jsii_name="applyTo")
    def apply_to(
        self,
        resource: _constructs_77d1e7e8.IConstruct,
    ) -> _constructs_77d1e7e8.IConstruct:
        '''Apply vended logs configuration to the construct.

        :param resource: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__346aafd94719a39bcd1b7e03f2d1d1c815b572bfa39b9a1b179e7c078ed109d1)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [resource]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct (has vendedLogs property).

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaa046b4cb4a127be4c06542eeae1311c588dd8afeba3af29448f52bdd1c24f3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="APPLICATION_LOGS")
    def APPLICATION_LOGS(cls) -> CfnMemoryApplicationLogs:
        return typing.cast(CfnMemoryApplicationLogs, jsii.sget(cls, "APPLICATION_LOGS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="TRACES")
    def TRACES(cls) -> "CfnMemoryTraces":
        return typing.cast("CfnMemoryTraces", jsii.sget(cls, "TRACES"))

    @builtins.property
    @jsii.member(jsii_name="logDelivery")
    def _log_delivery(self) -> _ILogsDelivery_0d3c9e29:
        return typing.cast(_ILogsDelivery_0d3c9e29, jsii.get(self, "logDelivery"))

    @builtins.property
    @jsii.member(jsii_name="logType")
    def _log_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logType"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnMemoryMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "encryption_key_arn": "encryptionKeyArn",
        "event_expiry_duration": "eventExpiryDuration",
        "memory_execution_role_arn": "memoryExecutionRoleArn",
        "memory_strategies": "memoryStrategies",
        "name": "name",
        "tags": "tags",
    },
)
class CfnMemoryMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        encryption_key_arn: typing.Optional[builtins.str] = None,
        event_expiry_duration: typing.Optional[jsii.Number] = None,
        memory_execution_role_arn: typing.Optional[builtins.str] = None,
        memory_strategies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMemoryPropsMixin.MemoryStrategyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnMemoryPropsMixin.

        :param description: Description of the Memory resource.
        :param encryption_key_arn: The memory encryption key Amazon Resource Name (ARN).
        :param event_expiry_duration: The event expiry configuration.
        :param memory_execution_role_arn: The memory role ARN.
        :param memory_strategies: The memory strategies.
        :param name: The memory name.
        :param tags: The tags for the resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-memory.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
            
            cfn_memory_mixin_props = bedrockagentcore_mixins.CfnMemoryMixinProps(
                description="description",
                encryption_key_arn="encryptionKeyArn",
                event_expiry_duration=123,
                memory_execution_role_arn="memoryExecutionRoleArn",
                memory_strategies=[bedrockagentcore_mixins.CfnMemoryPropsMixin.MemoryStrategyProperty(
                    custom_memory_strategy=bedrockagentcore_mixins.CfnMemoryPropsMixin.CustomMemoryStrategyProperty(
                        configuration=bedrockagentcore_mixins.CfnMemoryPropsMixin.CustomConfigurationInputProperty(
                            self_managed_configuration=bedrockagentcore_mixins.CfnMemoryPropsMixin.SelfManagedConfigurationProperty(
                                historical_context_window_size=123,
                                invocation_configuration=bedrockagentcore_mixins.CfnMemoryPropsMixin.InvocationConfigurationInputProperty(
                                    payload_delivery_bucket_name="payloadDeliveryBucketName",
                                    topic_arn="topicArn"
                                ),
                                trigger_conditions=[bedrockagentcore_mixins.CfnMemoryPropsMixin.TriggerConditionInputProperty(
                                    message_based_trigger=bedrockagentcore_mixins.CfnMemoryPropsMixin.MessageBasedTriggerInputProperty(
                                        message_count=123
                                    ),
                                    time_based_trigger=bedrockagentcore_mixins.CfnMemoryPropsMixin.TimeBasedTriggerInputProperty(
                                        idle_session_timeout=123
                                    ),
                                    token_based_trigger=bedrockagentcore_mixins.CfnMemoryPropsMixin.TokenBasedTriggerInputProperty(
                                        token_count=123
                                    )
                                )]
                            ),
                            semantic_override=bedrockagentcore_mixins.CfnMemoryPropsMixin.SemanticOverrideProperty(
                                consolidation=bedrockagentcore_mixins.CfnMemoryPropsMixin.SemanticOverrideConsolidationConfigurationInputProperty(
                                    append_to_prompt="appendToPrompt",
                                    model_id="modelId"
                                ),
                                extraction=bedrockagentcore_mixins.CfnMemoryPropsMixin.SemanticOverrideExtractionConfigurationInputProperty(
                                    append_to_prompt="appendToPrompt",
                                    model_id="modelId"
                                )
                            ),
                            summary_override=bedrockagentcore_mixins.CfnMemoryPropsMixin.SummaryOverrideProperty(
                                consolidation=bedrockagentcore_mixins.CfnMemoryPropsMixin.SummaryOverrideConsolidationConfigurationInputProperty(
                                    append_to_prompt="appendToPrompt",
                                    model_id="modelId"
                                )
                            ),
                            user_preference_override=bedrockagentcore_mixins.CfnMemoryPropsMixin.UserPreferenceOverrideProperty(
                                consolidation=bedrockagentcore_mixins.CfnMemoryPropsMixin.UserPreferenceOverrideConsolidationConfigurationInputProperty(
                                    append_to_prompt="appendToPrompt",
                                    model_id="modelId"
                                ),
                                extraction=bedrockagentcore_mixins.CfnMemoryPropsMixin.UserPreferenceOverrideExtractionConfigurationInputProperty(
                                    append_to_prompt="appendToPrompt",
                                    model_id="modelId"
                                )
                            )
                        ),
                        created_at="createdAt",
                        description="description",
                        name="name",
                        namespaces=["namespaces"],
                        status="status",
                        strategy_id="strategyId",
                        type="type",
                        updated_at="updatedAt"
                    ),
                    semantic_memory_strategy=bedrockagentcore_mixins.CfnMemoryPropsMixin.SemanticMemoryStrategyProperty(
                        created_at="createdAt",
                        description="description",
                        name="name",
                        namespaces=["namespaces"],
                        status="status",
                        strategy_id="strategyId",
                        type="type",
                        updated_at="updatedAt"
                    ),
                    summary_memory_strategy=bedrockagentcore_mixins.CfnMemoryPropsMixin.SummaryMemoryStrategyProperty(
                        created_at="createdAt",
                        description="description",
                        name="name",
                        namespaces=["namespaces"],
                        status="status",
                        strategy_id="strategyId",
                        type="type",
                        updated_at="updatedAt"
                    ),
                    user_preference_memory_strategy=bedrockagentcore_mixins.CfnMemoryPropsMixin.UserPreferenceMemoryStrategyProperty(
                        created_at="createdAt",
                        description="description",
                        name="name",
                        namespaces=["namespaces"],
                        status="status",
                        strategy_id="strategyId",
                        type="type",
                        updated_at="updatedAt"
                    )
                )],
                name="name",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e22348ed1151811aee5c79cc9680ed4f85736851bc7dd5d08c24d8f8d06405c3)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument encryption_key_arn", value=encryption_key_arn, expected_type=type_hints["encryption_key_arn"])
            check_type(argname="argument event_expiry_duration", value=event_expiry_duration, expected_type=type_hints["event_expiry_duration"])
            check_type(argname="argument memory_execution_role_arn", value=memory_execution_role_arn, expected_type=type_hints["memory_execution_role_arn"])
            check_type(argname="argument memory_strategies", value=memory_strategies, expected_type=type_hints["memory_strategies"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if encryption_key_arn is not None:
            self._values["encryption_key_arn"] = encryption_key_arn
        if event_expiry_duration is not None:
            self._values["event_expiry_duration"] = event_expiry_duration
        if memory_execution_role_arn is not None:
            self._values["memory_execution_role_arn"] = memory_execution_role_arn
        if memory_strategies is not None:
            self._values["memory_strategies"] = memory_strategies
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the Memory resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-memory.html#cfn-bedrockagentcore-memory-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_key_arn(self) -> typing.Optional[builtins.str]:
        '''The memory encryption key Amazon Resource Name (ARN).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-memory.html#cfn-bedrockagentcore-memory-encryptionkeyarn
        '''
        result = self._values.get("encryption_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_expiry_duration(self) -> typing.Optional[jsii.Number]:
        '''The event expiry configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-memory.html#cfn-bedrockagentcore-memory-eventexpiryduration
        '''
        result = self._values.get("event_expiry_duration")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_execution_role_arn(self) -> typing.Optional[builtins.str]:
        '''The memory role ARN.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-memory.html#cfn-bedrockagentcore-memory-memoryexecutionrolearn
        '''
        result = self._values.get("memory_execution_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def memory_strategies(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemoryPropsMixin.MemoryStrategyProperty"]]]]:
        '''The memory strategies.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-memory.html#cfn-bedrockagentcore-memory-memorystrategies
        '''
        result = self._values.get("memory_strategies")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemoryPropsMixin.MemoryStrategyProperty"]]]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The memory name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-memory.html#cfn-bedrockagentcore-memory-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The tags for the resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-memory.html#cfn-bedrockagentcore-memory-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMemoryMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnMemoryPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnMemoryPropsMixin",
):
    '''Memory allows AI agents to maintain both immediate and long-term knowledge, enabling context-aware and personalized interactions.

    For more information about using Memory in Amazon Bedrock AgentCore, see `Host agent or tools with Amazon Bedrock AgentCore Memory <https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-getting-started.html>`_ .

    See the *Properties* section below for descriptions of both the required and optional properties.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-memory.html
    :cloudformationResource: AWS::BedrockAgentCore::Memory
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
        
        cfn_memory_props_mixin = bedrockagentcore_mixins.CfnMemoryPropsMixin(bedrockagentcore_mixins.CfnMemoryMixinProps(
            description="description",
            encryption_key_arn="encryptionKeyArn",
            event_expiry_duration=123,
            memory_execution_role_arn="memoryExecutionRoleArn",
            memory_strategies=[bedrockagentcore_mixins.CfnMemoryPropsMixin.MemoryStrategyProperty(
                custom_memory_strategy=bedrockagentcore_mixins.CfnMemoryPropsMixin.CustomMemoryStrategyProperty(
                    configuration=bedrockagentcore_mixins.CfnMemoryPropsMixin.CustomConfigurationInputProperty(
                        self_managed_configuration=bedrockagentcore_mixins.CfnMemoryPropsMixin.SelfManagedConfigurationProperty(
                            historical_context_window_size=123,
                            invocation_configuration=bedrockagentcore_mixins.CfnMemoryPropsMixin.InvocationConfigurationInputProperty(
                                payload_delivery_bucket_name="payloadDeliveryBucketName",
                                topic_arn="topicArn"
                            ),
                            trigger_conditions=[bedrockagentcore_mixins.CfnMemoryPropsMixin.TriggerConditionInputProperty(
                                message_based_trigger=bedrockagentcore_mixins.CfnMemoryPropsMixin.MessageBasedTriggerInputProperty(
                                    message_count=123
                                ),
                                time_based_trigger=bedrockagentcore_mixins.CfnMemoryPropsMixin.TimeBasedTriggerInputProperty(
                                    idle_session_timeout=123
                                ),
                                token_based_trigger=bedrockagentcore_mixins.CfnMemoryPropsMixin.TokenBasedTriggerInputProperty(
                                    token_count=123
                                )
                            )]
                        ),
                        semantic_override=bedrockagentcore_mixins.CfnMemoryPropsMixin.SemanticOverrideProperty(
                            consolidation=bedrockagentcore_mixins.CfnMemoryPropsMixin.SemanticOverrideConsolidationConfigurationInputProperty(
                                append_to_prompt="appendToPrompt",
                                model_id="modelId"
                            ),
                            extraction=bedrockagentcore_mixins.CfnMemoryPropsMixin.SemanticOverrideExtractionConfigurationInputProperty(
                                append_to_prompt="appendToPrompt",
                                model_id="modelId"
                            )
                        ),
                        summary_override=bedrockagentcore_mixins.CfnMemoryPropsMixin.SummaryOverrideProperty(
                            consolidation=bedrockagentcore_mixins.CfnMemoryPropsMixin.SummaryOverrideConsolidationConfigurationInputProperty(
                                append_to_prompt="appendToPrompt",
                                model_id="modelId"
                            )
                        ),
                        user_preference_override=bedrockagentcore_mixins.CfnMemoryPropsMixin.UserPreferenceOverrideProperty(
                            consolidation=bedrockagentcore_mixins.CfnMemoryPropsMixin.UserPreferenceOverrideConsolidationConfigurationInputProperty(
                                append_to_prompt="appendToPrompt",
                                model_id="modelId"
                            ),
                            extraction=bedrockagentcore_mixins.CfnMemoryPropsMixin.UserPreferenceOverrideExtractionConfigurationInputProperty(
                                append_to_prompt="appendToPrompt",
                                model_id="modelId"
                            )
                        )
                    ),
                    created_at="createdAt",
                    description="description",
                    name="name",
                    namespaces=["namespaces"],
                    status="status",
                    strategy_id="strategyId",
                    type="type",
                    updated_at="updatedAt"
                ),
                semantic_memory_strategy=bedrockagentcore_mixins.CfnMemoryPropsMixin.SemanticMemoryStrategyProperty(
                    created_at="createdAt",
                    description="description",
                    name="name",
                    namespaces=["namespaces"],
                    status="status",
                    strategy_id="strategyId",
                    type="type",
                    updated_at="updatedAt"
                ),
                summary_memory_strategy=bedrockagentcore_mixins.CfnMemoryPropsMixin.SummaryMemoryStrategyProperty(
                    created_at="createdAt",
                    description="description",
                    name="name",
                    namespaces=["namespaces"],
                    status="status",
                    strategy_id="strategyId",
                    type="type",
                    updated_at="updatedAt"
                ),
                user_preference_memory_strategy=bedrockagentcore_mixins.CfnMemoryPropsMixin.UserPreferenceMemoryStrategyProperty(
                    created_at="createdAt",
                    description="description",
                    name="name",
                    namespaces=["namespaces"],
                    status="status",
                    strategy_id="strategyId",
                    type="type",
                    updated_at="updatedAt"
                )
            )],
            name="name",
            tags={
                "tags_key": "tags"
            }
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnMemoryMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::BedrockAgentCore::Memory``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3caaba0b37caf2f688269c0c0d1d483b8f701dfef20e3d18c5525458ee74a15b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4d97507cbfb28b7c260cb5d4006a33d804cc16335bf3144d89a1503118eca5d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3e4c90a594f7890d51fde0a39714f10ec02b31ae63a09e1a3b7a0642342c545)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnMemoryMixinProps:
        return typing.cast(CfnMemoryMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnMemoryPropsMixin.CustomConfigurationInputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "self_managed_configuration": "selfManagedConfiguration",
            "semantic_override": "semanticOverride",
            "summary_override": "summaryOverride",
            "user_preference_override": "userPreferenceOverride",
        },
    )
    class CustomConfigurationInputProperty:
        def __init__(
            self,
            *,
            self_managed_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMemoryPropsMixin.SelfManagedConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            semantic_override: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMemoryPropsMixin.SemanticOverrideProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            summary_override: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMemoryPropsMixin.SummaryOverrideProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            user_preference_override: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMemoryPropsMixin.UserPreferenceOverrideProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The memory configuration input.

            :param self_managed_configuration: The custom configuration input.
            :param semantic_override: The memory override configuration.
            :param summary_override: The memory configuration override.
            :param user_preference_override: The memory user preference override.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-customconfigurationinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                custom_configuration_input_property = bedrockagentcore_mixins.CfnMemoryPropsMixin.CustomConfigurationInputProperty(
                    self_managed_configuration=bedrockagentcore_mixins.CfnMemoryPropsMixin.SelfManagedConfigurationProperty(
                        historical_context_window_size=123,
                        invocation_configuration=bedrockagentcore_mixins.CfnMemoryPropsMixin.InvocationConfigurationInputProperty(
                            payload_delivery_bucket_name="payloadDeliveryBucketName",
                            topic_arn="topicArn"
                        ),
                        trigger_conditions=[bedrockagentcore_mixins.CfnMemoryPropsMixin.TriggerConditionInputProperty(
                            message_based_trigger=bedrockagentcore_mixins.CfnMemoryPropsMixin.MessageBasedTriggerInputProperty(
                                message_count=123
                            ),
                            time_based_trigger=bedrockagentcore_mixins.CfnMemoryPropsMixin.TimeBasedTriggerInputProperty(
                                idle_session_timeout=123
                            ),
                            token_based_trigger=bedrockagentcore_mixins.CfnMemoryPropsMixin.TokenBasedTriggerInputProperty(
                                token_count=123
                            )
                        )]
                    ),
                    semantic_override=bedrockagentcore_mixins.CfnMemoryPropsMixin.SemanticOverrideProperty(
                        consolidation=bedrockagentcore_mixins.CfnMemoryPropsMixin.SemanticOverrideConsolidationConfigurationInputProperty(
                            append_to_prompt="appendToPrompt",
                            model_id="modelId"
                        ),
                        extraction=bedrockagentcore_mixins.CfnMemoryPropsMixin.SemanticOverrideExtractionConfigurationInputProperty(
                            append_to_prompt="appendToPrompt",
                            model_id="modelId"
                        )
                    ),
                    summary_override=bedrockagentcore_mixins.CfnMemoryPropsMixin.SummaryOverrideProperty(
                        consolidation=bedrockagentcore_mixins.CfnMemoryPropsMixin.SummaryOverrideConsolidationConfigurationInputProperty(
                            append_to_prompt="appendToPrompt",
                            model_id="modelId"
                        )
                    ),
                    user_preference_override=bedrockagentcore_mixins.CfnMemoryPropsMixin.UserPreferenceOverrideProperty(
                        consolidation=bedrockagentcore_mixins.CfnMemoryPropsMixin.UserPreferenceOverrideConsolidationConfigurationInputProperty(
                            append_to_prompt="appendToPrompt",
                            model_id="modelId"
                        ),
                        extraction=bedrockagentcore_mixins.CfnMemoryPropsMixin.UserPreferenceOverrideExtractionConfigurationInputProperty(
                            append_to_prompt="appendToPrompt",
                            model_id="modelId"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__24b2d17307064123f93ac0ef040fdfb7e640b1dcfdefa2835a79b6584752bc8c)
                check_type(argname="argument self_managed_configuration", value=self_managed_configuration, expected_type=type_hints["self_managed_configuration"])
                check_type(argname="argument semantic_override", value=semantic_override, expected_type=type_hints["semantic_override"])
                check_type(argname="argument summary_override", value=summary_override, expected_type=type_hints["summary_override"])
                check_type(argname="argument user_preference_override", value=user_preference_override, expected_type=type_hints["user_preference_override"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if self_managed_configuration is not None:
                self._values["self_managed_configuration"] = self_managed_configuration
            if semantic_override is not None:
                self._values["semantic_override"] = semantic_override
            if summary_override is not None:
                self._values["summary_override"] = summary_override
            if user_preference_override is not None:
                self._values["user_preference_override"] = user_preference_override

        @builtins.property
        def self_managed_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemoryPropsMixin.SelfManagedConfigurationProperty"]]:
            '''The custom configuration input.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-customconfigurationinput.html#cfn-bedrockagentcore-memory-customconfigurationinput-selfmanagedconfiguration
            '''
            result = self._values.get("self_managed_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemoryPropsMixin.SelfManagedConfigurationProperty"]], result)

        @builtins.property
        def semantic_override(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemoryPropsMixin.SemanticOverrideProperty"]]:
            '''The memory override configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-customconfigurationinput.html#cfn-bedrockagentcore-memory-customconfigurationinput-semanticoverride
            '''
            result = self._values.get("semantic_override")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemoryPropsMixin.SemanticOverrideProperty"]], result)

        @builtins.property
        def summary_override(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemoryPropsMixin.SummaryOverrideProperty"]]:
            '''The memory configuration override.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-customconfigurationinput.html#cfn-bedrockagentcore-memory-customconfigurationinput-summaryoverride
            '''
            result = self._values.get("summary_override")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemoryPropsMixin.SummaryOverrideProperty"]], result)

        @builtins.property
        def user_preference_override(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemoryPropsMixin.UserPreferenceOverrideProperty"]]:
            '''The memory user preference override.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-customconfigurationinput.html#cfn-bedrockagentcore-memory-customconfigurationinput-userpreferenceoverride
            '''
            result = self._values.get("user_preference_override")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemoryPropsMixin.UserPreferenceOverrideProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomConfigurationInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnMemoryPropsMixin.CustomMemoryStrategyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "configuration": "configuration",
            "created_at": "createdAt",
            "description": "description",
            "name": "name",
            "namespaces": "namespaces",
            "status": "status",
            "strategy_id": "strategyId",
            "type": "type",
            "updated_at": "updatedAt",
        },
    )
    class CustomMemoryStrategyProperty:
        def __init__(
            self,
            *,
            configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMemoryPropsMixin.CustomConfigurationInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            created_at: typing.Optional[builtins.str] = None,
            description: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
            status: typing.Optional[builtins.str] = None,
            strategy_id: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
            updated_at: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The memory strategy.

            :param configuration: The memory strategy configuration.
            :param created_at: Creation timestamp of the memory strategy.
            :param description: The memory strategy description.
            :param name: The memory strategy name.
            :param namespaces: The memory strategy namespaces.
            :param status: The memory strategy status.
            :param strategy_id: The memory strategy ID.
            :param type: The memory strategy type.
            :param updated_at: The memory strategy update date and time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-custommemorystrategy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                custom_memory_strategy_property = bedrockagentcore_mixins.CfnMemoryPropsMixin.CustomMemoryStrategyProperty(
                    configuration=bedrockagentcore_mixins.CfnMemoryPropsMixin.CustomConfigurationInputProperty(
                        self_managed_configuration=bedrockagentcore_mixins.CfnMemoryPropsMixin.SelfManagedConfigurationProperty(
                            historical_context_window_size=123,
                            invocation_configuration=bedrockagentcore_mixins.CfnMemoryPropsMixin.InvocationConfigurationInputProperty(
                                payload_delivery_bucket_name="payloadDeliveryBucketName",
                                topic_arn="topicArn"
                            ),
                            trigger_conditions=[bedrockagentcore_mixins.CfnMemoryPropsMixin.TriggerConditionInputProperty(
                                message_based_trigger=bedrockagentcore_mixins.CfnMemoryPropsMixin.MessageBasedTriggerInputProperty(
                                    message_count=123
                                ),
                                time_based_trigger=bedrockagentcore_mixins.CfnMemoryPropsMixin.TimeBasedTriggerInputProperty(
                                    idle_session_timeout=123
                                ),
                                token_based_trigger=bedrockagentcore_mixins.CfnMemoryPropsMixin.TokenBasedTriggerInputProperty(
                                    token_count=123
                                )
                            )]
                        ),
                        semantic_override=bedrockagentcore_mixins.CfnMemoryPropsMixin.SemanticOverrideProperty(
                            consolidation=bedrockagentcore_mixins.CfnMemoryPropsMixin.SemanticOverrideConsolidationConfigurationInputProperty(
                                append_to_prompt="appendToPrompt",
                                model_id="modelId"
                            ),
                            extraction=bedrockagentcore_mixins.CfnMemoryPropsMixin.SemanticOverrideExtractionConfigurationInputProperty(
                                append_to_prompt="appendToPrompt",
                                model_id="modelId"
                            )
                        ),
                        summary_override=bedrockagentcore_mixins.CfnMemoryPropsMixin.SummaryOverrideProperty(
                            consolidation=bedrockagentcore_mixins.CfnMemoryPropsMixin.SummaryOverrideConsolidationConfigurationInputProperty(
                                append_to_prompt="appendToPrompt",
                                model_id="modelId"
                            )
                        ),
                        user_preference_override=bedrockagentcore_mixins.CfnMemoryPropsMixin.UserPreferenceOverrideProperty(
                            consolidation=bedrockagentcore_mixins.CfnMemoryPropsMixin.UserPreferenceOverrideConsolidationConfigurationInputProperty(
                                append_to_prompt="appendToPrompt",
                                model_id="modelId"
                            ),
                            extraction=bedrockagentcore_mixins.CfnMemoryPropsMixin.UserPreferenceOverrideExtractionConfigurationInputProperty(
                                append_to_prompt="appendToPrompt",
                                model_id="modelId"
                            )
                        )
                    ),
                    created_at="createdAt",
                    description="description",
                    name="name",
                    namespaces=["namespaces"],
                    status="status",
                    strategy_id="strategyId",
                    type="type",
                    updated_at="updatedAt"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a1feb21d4011acfa1b5ef0427e95a8fac7dc541f8fc03dbf2ab7479f19180fe2)
                check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
                check_type(argname="argument created_at", value=created_at, expected_type=type_hints["created_at"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument namespaces", value=namespaces, expected_type=type_hints["namespaces"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                check_type(argname="argument strategy_id", value=strategy_id, expected_type=type_hints["strategy_id"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument updated_at", value=updated_at, expected_type=type_hints["updated_at"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if configuration is not None:
                self._values["configuration"] = configuration
            if created_at is not None:
                self._values["created_at"] = created_at
            if description is not None:
                self._values["description"] = description
            if name is not None:
                self._values["name"] = name
            if namespaces is not None:
                self._values["namespaces"] = namespaces
            if status is not None:
                self._values["status"] = status
            if strategy_id is not None:
                self._values["strategy_id"] = strategy_id
            if type is not None:
                self._values["type"] = type
            if updated_at is not None:
                self._values["updated_at"] = updated_at

        @builtins.property
        def configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemoryPropsMixin.CustomConfigurationInputProperty"]]:
            '''The memory strategy configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-custommemorystrategy.html#cfn-bedrockagentcore-memory-custommemorystrategy-configuration
            '''
            result = self._values.get("configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemoryPropsMixin.CustomConfigurationInputProperty"]], result)

        @builtins.property
        def created_at(self) -> typing.Optional[builtins.str]:
            '''Creation timestamp of the memory strategy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-custommemorystrategy.html#cfn-bedrockagentcore-memory-custommemorystrategy-createdat
            '''
            result = self._values.get("created_at")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The memory strategy description.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-custommemorystrategy.html#cfn-bedrockagentcore-memory-custommemorystrategy-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The memory strategy name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-custommemorystrategy.html#cfn-bedrockagentcore-memory-custommemorystrategy-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def namespaces(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The memory strategy namespaces.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-custommemorystrategy.html#cfn-bedrockagentcore-memory-custommemorystrategy-namespaces
            '''
            result = self._values.get("namespaces")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''The memory strategy status.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-custommemorystrategy.html#cfn-bedrockagentcore-memory-custommemorystrategy-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def strategy_id(self) -> typing.Optional[builtins.str]:
            '''The memory strategy ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-custommemorystrategy.html#cfn-bedrockagentcore-memory-custommemorystrategy-strategyid
            '''
            result = self._values.get("strategy_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The memory strategy type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-custommemorystrategy.html#cfn-bedrockagentcore-memory-custommemorystrategy-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def updated_at(self) -> typing.Optional[builtins.str]:
            '''The memory strategy update date and time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-custommemorystrategy.html#cfn-bedrockagentcore-memory-custommemorystrategy-updatedat
            '''
            result = self._values.get("updated_at")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomMemoryStrategyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnMemoryPropsMixin.InvocationConfigurationInputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "payload_delivery_bucket_name": "payloadDeliveryBucketName",
            "topic_arn": "topicArn",
        },
    )
    class InvocationConfigurationInputProperty:
        def __init__(
            self,
            *,
            payload_delivery_bucket_name: typing.Optional[builtins.str] = None,
            topic_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The memory invocation configuration input.

            :param payload_delivery_bucket_name: The message invocation configuration information for the bucket name.
            :param topic_arn: The memory trigger condition topic Amazon Resource Name (ARN).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-invocationconfigurationinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                invocation_configuration_input_property = bedrockagentcore_mixins.CfnMemoryPropsMixin.InvocationConfigurationInputProperty(
                    payload_delivery_bucket_name="payloadDeliveryBucketName",
                    topic_arn="topicArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__def0b4707baa8a1bb7decbe3b8b23454627a194206645117c63573d610b82658)
                check_type(argname="argument payload_delivery_bucket_name", value=payload_delivery_bucket_name, expected_type=type_hints["payload_delivery_bucket_name"])
                check_type(argname="argument topic_arn", value=topic_arn, expected_type=type_hints["topic_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if payload_delivery_bucket_name is not None:
                self._values["payload_delivery_bucket_name"] = payload_delivery_bucket_name
            if topic_arn is not None:
                self._values["topic_arn"] = topic_arn

        @builtins.property
        def payload_delivery_bucket_name(self) -> typing.Optional[builtins.str]:
            '''The message invocation configuration information for the bucket name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-invocationconfigurationinput.html#cfn-bedrockagentcore-memory-invocationconfigurationinput-payloaddeliverybucketname
            '''
            result = self._values.get("payload_delivery_bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def topic_arn(self) -> typing.Optional[builtins.str]:
            '''The memory trigger condition topic Amazon Resource Name (ARN).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-invocationconfigurationinput.html#cfn-bedrockagentcore-memory-invocationconfigurationinput-topicarn
            '''
            result = self._values.get("topic_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InvocationConfigurationInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnMemoryPropsMixin.MemoryStrategyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "custom_memory_strategy": "customMemoryStrategy",
            "semantic_memory_strategy": "semanticMemoryStrategy",
            "summary_memory_strategy": "summaryMemoryStrategy",
            "user_preference_memory_strategy": "userPreferenceMemoryStrategy",
        },
    )
    class MemoryStrategyProperty:
        def __init__(
            self,
            *,
            custom_memory_strategy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMemoryPropsMixin.CustomMemoryStrategyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            semantic_memory_strategy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMemoryPropsMixin.SemanticMemoryStrategyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            summary_memory_strategy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMemoryPropsMixin.SummaryMemoryStrategyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            user_preference_memory_strategy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMemoryPropsMixin.UserPreferenceMemoryStrategyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The memory strategy.

            :param custom_memory_strategy: The memory strategy.
            :param semantic_memory_strategy: The memory strategy.
            :param summary_memory_strategy: The memory strategy summary.
            :param user_preference_memory_strategy: The memory strategy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-memorystrategy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                memory_strategy_property = bedrockagentcore_mixins.CfnMemoryPropsMixin.MemoryStrategyProperty(
                    custom_memory_strategy=bedrockagentcore_mixins.CfnMemoryPropsMixin.CustomMemoryStrategyProperty(
                        configuration=bedrockagentcore_mixins.CfnMemoryPropsMixin.CustomConfigurationInputProperty(
                            self_managed_configuration=bedrockagentcore_mixins.CfnMemoryPropsMixin.SelfManagedConfigurationProperty(
                                historical_context_window_size=123,
                                invocation_configuration=bedrockagentcore_mixins.CfnMemoryPropsMixin.InvocationConfigurationInputProperty(
                                    payload_delivery_bucket_name="payloadDeliveryBucketName",
                                    topic_arn="topicArn"
                                ),
                                trigger_conditions=[bedrockagentcore_mixins.CfnMemoryPropsMixin.TriggerConditionInputProperty(
                                    message_based_trigger=bedrockagentcore_mixins.CfnMemoryPropsMixin.MessageBasedTriggerInputProperty(
                                        message_count=123
                                    ),
                                    time_based_trigger=bedrockagentcore_mixins.CfnMemoryPropsMixin.TimeBasedTriggerInputProperty(
                                        idle_session_timeout=123
                                    ),
                                    token_based_trigger=bedrockagentcore_mixins.CfnMemoryPropsMixin.TokenBasedTriggerInputProperty(
                                        token_count=123
                                    )
                                )]
                            ),
                            semantic_override=bedrockagentcore_mixins.CfnMemoryPropsMixin.SemanticOverrideProperty(
                                consolidation=bedrockagentcore_mixins.CfnMemoryPropsMixin.SemanticOverrideConsolidationConfigurationInputProperty(
                                    append_to_prompt="appendToPrompt",
                                    model_id="modelId"
                                ),
                                extraction=bedrockagentcore_mixins.CfnMemoryPropsMixin.SemanticOverrideExtractionConfigurationInputProperty(
                                    append_to_prompt="appendToPrompt",
                                    model_id="modelId"
                                )
                            ),
                            summary_override=bedrockagentcore_mixins.CfnMemoryPropsMixin.SummaryOverrideProperty(
                                consolidation=bedrockagentcore_mixins.CfnMemoryPropsMixin.SummaryOverrideConsolidationConfigurationInputProperty(
                                    append_to_prompt="appendToPrompt",
                                    model_id="modelId"
                                )
                            ),
                            user_preference_override=bedrockagentcore_mixins.CfnMemoryPropsMixin.UserPreferenceOverrideProperty(
                                consolidation=bedrockagentcore_mixins.CfnMemoryPropsMixin.UserPreferenceOverrideConsolidationConfigurationInputProperty(
                                    append_to_prompt="appendToPrompt",
                                    model_id="modelId"
                                ),
                                extraction=bedrockagentcore_mixins.CfnMemoryPropsMixin.UserPreferenceOverrideExtractionConfigurationInputProperty(
                                    append_to_prompt="appendToPrompt",
                                    model_id="modelId"
                                )
                            )
                        ),
                        created_at="createdAt",
                        description="description",
                        name="name",
                        namespaces=["namespaces"],
                        status="status",
                        strategy_id="strategyId",
                        type="type",
                        updated_at="updatedAt"
                    ),
                    semantic_memory_strategy=bedrockagentcore_mixins.CfnMemoryPropsMixin.SemanticMemoryStrategyProperty(
                        created_at="createdAt",
                        description="description",
                        name="name",
                        namespaces=["namespaces"],
                        status="status",
                        strategy_id="strategyId",
                        type="type",
                        updated_at="updatedAt"
                    ),
                    summary_memory_strategy=bedrockagentcore_mixins.CfnMemoryPropsMixin.SummaryMemoryStrategyProperty(
                        created_at="createdAt",
                        description="description",
                        name="name",
                        namespaces=["namespaces"],
                        status="status",
                        strategy_id="strategyId",
                        type="type",
                        updated_at="updatedAt"
                    ),
                    user_preference_memory_strategy=bedrockagentcore_mixins.CfnMemoryPropsMixin.UserPreferenceMemoryStrategyProperty(
                        created_at="createdAt",
                        description="description",
                        name="name",
                        namespaces=["namespaces"],
                        status="status",
                        strategy_id="strategyId",
                        type="type",
                        updated_at="updatedAt"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7cfb716082b9dea2bf08f0664531cdff7d856f3b3ac17830566d4910fe48b81d)
                check_type(argname="argument custom_memory_strategy", value=custom_memory_strategy, expected_type=type_hints["custom_memory_strategy"])
                check_type(argname="argument semantic_memory_strategy", value=semantic_memory_strategy, expected_type=type_hints["semantic_memory_strategy"])
                check_type(argname="argument summary_memory_strategy", value=summary_memory_strategy, expected_type=type_hints["summary_memory_strategy"])
                check_type(argname="argument user_preference_memory_strategy", value=user_preference_memory_strategy, expected_type=type_hints["user_preference_memory_strategy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if custom_memory_strategy is not None:
                self._values["custom_memory_strategy"] = custom_memory_strategy
            if semantic_memory_strategy is not None:
                self._values["semantic_memory_strategy"] = semantic_memory_strategy
            if summary_memory_strategy is not None:
                self._values["summary_memory_strategy"] = summary_memory_strategy
            if user_preference_memory_strategy is not None:
                self._values["user_preference_memory_strategy"] = user_preference_memory_strategy

        @builtins.property
        def custom_memory_strategy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemoryPropsMixin.CustomMemoryStrategyProperty"]]:
            '''The memory strategy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-memorystrategy.html#cfn-bedrockagentcore-memory-memorystrategy-custommemorystrategy
            '''
            result = self._values.get("custom_memory_strategy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemoryPropsMixin.CustomMemoryStrategyProperty"]], result)

        @builtins.property
        def semantic_memory_strategy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemoryPropsMixin.SemanticMemoryStrategyProperty"]]:
            '''The memory strategy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-memorystrategy.html#cfn-bedrockagentcore-memory-memorystrategy-semanticmemorystrategy
            '''
            result = self._values.get("semantic_memory_strategy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemoryPropsMixin.SemanticMemoryStrategyProperty"]], result)

        @builtins.property
        def summary_memory_strategy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemoryPropsMixin.SummaryMemoryStrategyProperty"]]:
            '''The memory strategy summary.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-memorystrategy.html#cfn-bedrockagentcore-memory-memorystrategy-summarymemorystrategy
            '''
            result = self._values.get("summary_memory_strategy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemoryPropsMixin.SummaryMemoryStrategyProperty"]], result)

        @builtins.property
        def user_preference_memory_strategy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemoryPropsMixin.UserPreferenceMemoryStrategyProperty"]]:
            '''The memory strategy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-memorystrategy.html#cfn-bedrockagentcore-memory-memorystrategy-userpreferencememorystrategy
            '''
            result = self._values.get("user_preference_memory_strategy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemoryPropsMixin.UserPreferenceMemoryStrategyProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MemoryStrategyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnMemoryPropsMixin.MessageBasedTriggerInputProperty",
        jsii_struct_bases=[],
        name_mapping={"message_count": "messageCount"},
    )
    class MessageBasedTriggerInputProperty:
        def __init__(
            self,
            *,
            message_count: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The message based trigger input.

            :param message_count: The memory trigger condition input for the message based trigger message count.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-messagebasedtriggerinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                message_based_trigger_input_property = bedrockagentcore_mixins.CfnMemoryPropsMixin.MessageBasedTriggerInputProperty(
                    message_count=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__89bfddd3fe52dc0106411219d5a801fe3e8abaaf67f30d1a75ae6674b5495138)
                check_type(argname="argument message_count", value=message_count, expected_type=type_hints["message_count"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if message_count is not None:
                self._values["message_count"] = message_count

        @builtins.property
        def message_count(self) -> typing.Optional[jsii.Number]:
            '''The memory trigger condition input for the message based trigger message count.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-messagebasedtriggerinput.html#cfn-bedrockagentcore-memory-messagebasedtriggerinput-messagecount
            '''
            result = self._values.get("message_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MessageBasedTriggerInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnMemoryPropsMixin.SelfManagedConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "historical_context_window_size": "historicalContextWindowSize",
            "invocation_configuration": "invocationConfiguration",
            "trigger_conditions": "triggerConditions",
        },
    )
    class SelfManagedConfigurationProperty:
        def __init__(
            self,
            *,
            historical_context_window_size: typing.Optional[jsii.Number] = None,
            invocation_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMemoryPropsMixin.InvocationConfigurationInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            trigger_conditions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMemoryPropsMixin.TriggerConditionInputProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The self managed configuration.

            :param historical_context_window_size: The memory configuration for self managed.
            :param invocation_configuration: The self managed configuration.
            :param trigger_conditions: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-selfmanagedconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                self_managed_configuration_property = bedrockagentcore_mixins.CfnMemoryPropsMixin.SelfManagedConfigurationProperty(
                    historical_context_window_size=123,
                    invocation_configuration=bedrockagentcore_mixins.CfnMemoryPropsMixin.InvocationConfigurationInputProperty(
                        payload_delivery_bucket_name="payloadDeliveryBucketName",
                        topic_arn="topicArn"
                    ),
                    trigger_conditions=[bedrockagentcore_mixins.CfnMemoryPropsMixin.TriggerConditionInputProperty(
                        message_based_trigger=bedrockagentcore_mixins.CfnMemoryPropsMixin.MessageBasedTriggerInputProperty(
                            message_count=123
                        ),
                        time_based_trigger=bedrockagentcore_mixins.CfnMemoryPropsMixin.TimeBasedTriggerInputProperty(
                            idle_session_timeout=123
                        ),
                        token_based_trigger=bedrockagentcore_mixins.CfnMemoryPropsMixin.TokenBasedTriggerInputProperty(
                            token_count=123
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f2b92eacf901902387b61891ce0d3c9e9cb3632858166c9f05952f9f4cdee5e4)
                check_type(argname="argument historical_context_window_size", value=historical_context_window_size, expected_type=type_hints["historical_context_window_size"])
                check_type(argname="argument invocation_configuration", value=invocation_configuration, expected_type=type_hints["invocation_configuration"])
                check_type(argname="argument trigger_conditions", value=trigger_conditions, expected_type=type_hints["trigger_conditions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if historical_context_window_size is not None:
                self._values["historical_context_window_size"] = historical_context_window_size
            if invocation_configuration is not None:
                self._values["invocation_configuration"] = invocation_configuration
            if trigger_conditions is not None:
                self._values["trigger_conditions"] = trigger_conditions

        @builtins.property
        def historical_context_window_size(self) -> typing.Optional[jsii.Number]:
            '''The memory configuration for self managed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-selfmanagedconfiguration.html#cfn-bedrockagentcore-memory-selfmanagedconfiguration-historicalcontextwindowsize
            '''
            result = self._values.get("historical_context_window_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def invocation_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemoryPropsMixin.InvocationConfigurationInputProperty"]]:
            '''The self managed configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-selfmanagedconfiguration.html#cfn-bedrockagentcore-memory-selfmanagedconfiguration-invocationconfiguration
            '''
            result = self._values.get("invocation_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemoryPropsMixin.InvocationConfigurationInputProperty"]], result)

        @builtins.property
        def trigger_conditions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemoryPropsMixin.TriggerConditionInputProperty"]]]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-selfmanagedconfiguration.html#cfn-bedrockagentcore-memory-selfmanagedconfiguration-triggerconditions
            '''
            result = self._values.get("trigger_conditions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemoryPropsMixin.TriggerConditionInputProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SelfManagedConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnMemoryPropsMixin.SemanticMemoryStrategyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "created_at": "createdAt",
            "description": "description",
            "name": "name",
            "namespaces": "namespaces",
            "status": "status",
            "strategy_id": "strategyId",
            "type": "type",
            "updated_at": "updatedAt",
        },
    )
    class SemanticMemoryStrategyProperty:
        def __init__(
            self,
            *,
            created_at: typing.Optional[builtins.str] = None,
            description: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
            status: typing.Optional[builtins.str] = None,
            strategy_id: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
            updated_at: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The memory strategy.

            :param created_at: Creation timestamp of the memory strategy.
            :param description: The memory strategy description.
            :param name: The memory strategy name.
            :param namespaces: The memory strategy namespaces.
            :param status: Status of the memory strategy.
            :param strategy_id: The memory strategy ID.
            :param type: The memory strategy type.
            :param updated_at: Last update timestamp of the memory strategy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-semanticmemorystrategy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                semantic_memory_strategy_property = bedrockagentcore_mixins.CfnMemoryPropsMixin.SemanticMemoryStrategyProperty(
                    created_at="createdAt",
                    description="description",
                    name="name",
                    namespaces=["namespaces"],
                    status="status",
                    strategy_id="strategyId",
                    type="type",
                    updated_at="updatedAt"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__958370f575a589413fad6b2f89ca0578f3074bede0d607223001545982fddfa2)
                check_type(argname="argument created_at", value=created_at, expected_type=type_hints["created_at"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument namespaces", value=namespaces, expected_type=type_hints["namespaces"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                check_type(argname="argument strategy_id", value=strategy_id, expected_type=type_hints["strategy_id"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument updated_at", value=updated_at, expected_type=type_hints["updated_at"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if created_at is not None:
                self._values["created_at"] = created_at
            if description is not None:
                self._values["description"] = description
            if name is not None:
                self._values["name"] = name
            if namespaces is not None:
                self._values["namespaces"] = namespaces
            if status is not None:
                self._values["status"] = status
            if strategy_id is not None:
                self._values["strategy_id"] = strategy_id
            if type is not None:
                self._values["type"] = type
            if updated_at is not None:
                self._values["updated_at"] = updated_at

        @builtins.property
        def created_at(self) -> typing.Optional[builtins.str]:
            '''Creation timestamp of the memory strategy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-semanticmemorystrategy.html#cfn-bedrockagentcore-memory-semanticmemorystrategy-createdat
            '''
            result = self._values.get("created_at")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The memory strategy description.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-semanticmemorystrategy.html#cfn-bedrockagentcore-memory-semanticmemorystrategy-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The memory strategy name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-semanticmemorystrategy.html#cfn-bedrockagentcore-memory-semanticmemorystrategy-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def namespaces(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The memory strategy namespaces.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-semanticmemorystrategy.html#cfn-bedrockagentcore-memory-semanticmemorystrategy-namespaces
            '''
            result = self._values.get("namespaces")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''Status of the memory strategy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-semanticmemorystrategy.html#cfn-bedrockagentcore-memory-semanticmemorystrategy-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def strategy_id(self) -> typing.Optional[builtins.str]:
            '''The memory strategy ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-semanticmemorystrategy.html#cfn-bedrockagentcore-memory-semanticmemorystrategy-strategyid
            '''
            result = self._values.get("strategy_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The memory strategy type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-semanticmemorystrategy.html#cfn-bedrockagentcore-memory-semanticmemorystrategy-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def updated_at(self) -> typing.Optional[builtins.str]:
            '''Last update timestamp of the memory strategy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-semanticmemorystrategy.html#cfn-bedrockagentcore-memory-semanticmemorystrategy-updatedat
            '''
            result = self._values.get("updated_at")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SemanticMemoryStrategyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnMemoryPropsMixin.SemanticOverrideConsolidationConfigurationInputProperty",
        jsii_struct_bases=[],
        name_mapping={"append_to_prompt": "appendToPrompt", "model_id": "modelId"},
    )
    class SemanticOverrideConsolidationConfigurationInputProperty:
        def __init__(
            self,
            *,
            append_to_prompt: typing.Optional[builtins.str] = None,
            model_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The memory override configuration.

            :param append_to_prompt: The override configuration.
            :param model_id: The memory override model ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-semanticoverrideconsolidationconfigurationinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                semantic_override_consolidation_configuration_input_property = bedrockagentcore_mixins.CfnMemoryPropsMixin.SemanticOverrideConsolidationConfigurationInputProperty(
                    append_to_prompt="appendToPrompt",
                    model_id="modelId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dfee486b174cdb0ce3512caa083e969317d58b7915a45ba724a5c5c8196bf9bc)
                check_type(argname="argument append_to_prompt", value=append_to_prompt, expected_type=type_hints["append_to_prompt"])
                check_type(argname="argument model_id", value=model_id, expected_type=type_hints["model_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if append_to_prompt is not None:
                self._values["append_to_prompt"] = append_to_prompt
            if model_id is not None:
                self._values["model_id"] = model_id

        @builtins.property
        def append_to_prompt(self) -> typing.Optional[builtins.str]:
            '''The override configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-semanticoverrideconsolidationconfigurationinput.html#cfn-bedrockagentcore-memory-semanticoverrideconsolidationconfigurationinput-appendtoprompt
            '''
            result = self._values.get("append_to_prompt")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def model_id(self) -> typing.Optional[builtins.str]:
            '''The memory override model ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-semanticoverrideconsolidationconfigurationinput.html#cfn-bedrockagentcore-memory-semanticoverrideconsolidationconfigurationinput-modelid
            '''
            result = self._values.get("model_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SemanticOverrideConsolidationConfigurationInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnMemoryPropsMixin.SemanticOverrideExtractionConfigurationInputProperty",
        jsii_struct_bases=[],
        name_mapping={"append_to_prompt": "appendToPrompt", "model_id": "modelId"},
    )
    class SemanticOverrideExtractionConfigurationInputProperty:
        def __init__(
            self,
            *,
            append_to_prompt: typing.Optional[builtins.str] = None,
            model_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The memory override configuration.

            :param append_to_prompt: The extraction configuration.
            :param model_id: The memory override configuration model ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-semanticoverrideextractionconfigurationinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                semantic_override_extraction_configuration_input_property = bedrockagentcore_mixins.CfnMemoryPropsMixin.SemanticOverrideExtractionConfigurationInputProperty(
                    append_to_prompt="appendToPrompt",
                    model_id="modelId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7bb9a25a8649486d7b10f2873fd62b296535f402b8273f4dcbff0aabe625a787)
                check_type(argname="argument append_to_prompt", value=append_to_prompt, expected_type=type_hints["append_to_prompt"])
                check_type(argname="argument model_id", value=model_id, expected_type=type_hints["model_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if append_to_prompt is not None:
                self._values["append_to_prompt"] = append_to_prompt
            if model_id is not None:
                self._values["model_id"] = model_id

        @builtins.property
        def append_to_prompt(self) -> typing.Optional[builtins.str]:
            '''The extraction configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-semanticoverrideextractionconfigurationinput.html#cfn-bedrockagentcore-memory-semanticoverrideextractionconfigurationinput-appendtoprompt
            '''
            result = self._values.get("append_to_prompt")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def model_id(self) -> typing.Optional[builtins.str]:
            '''The memory override configuration model ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-semanticoverrideextractionconfigurationinput.html#cfn-bedrockagentcore-memory-semanticoverrideextractionconfigurationinput-modelid
            '''
            result = self._values.get("model_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SemanticOverrideExtractionConfigurationInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnMemoryPropsMixin.SemanticOverrideProperty",
        jsii_struct_bases=[],
        name_mapping={"consolidation": "consolidation", "extraction": "extraction"},
    )
    class SemanticOverrideProperty:
        def __init__(
            self,
            *,
            consolidation: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMemoryPropsMixin.SemanticOverrideConsolidationConfigurationInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            extraction: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMemoryPropsMixin.SemanticOverrideExtractionConfigurationInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The memory override.

            :param consolidation: The memory override consolidation.
            :param extraction: The memory override extraction.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-semanticoverride.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                semantic_override_property = bedrockagentcore_mixins.CfnMemoryPropsMixin.SemanticOverrideProperty(
                    consolidation=bedrockagentcore_mixins.CfnMemoryPropsMixin.SemanticOverrideConsolidationConfigurationInputProperty(
                        append_to_prompt="appendToPrompt",
                        model_id="modelId"
                    ),
                    extraction=bedrockagentcore_mixins.CfnMemoryPropsMixin.SemanticOverrideExtractionConfigurationInputProperty(
                        append_to_prompt="appendToPrompt",
                        model_id="modelId"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6d54203915ced368c5786dacbf41efee31c1b1ee99a1f83bfd8e36c455d6dc7c)
                check_type(argname="argument consolidation", value=consolidation, expected_type=type_hints["consolidation"])
                check_type(argname="argument extraction", value=extraction, expected_type=type_hints["extraction"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if consolidation is not None:
                self._values["consolidation"] = consolidation
            if extraction is not None:
                self._values["extraction"] = extraction

        @builtins.property
        def consolidation(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemoryPropsMixin.SemanticOverrideConsolidationConfigurationInputProperty"]]:
            '''The memory override consolidation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-semanticoverride.html#cfn-bedrockagentcore-memory-semanticoverride-consolidation
            '''
            result = self._values.get("consolidation")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemoryPropsMixin.SemanticOverrideConsolidationConfigurationInputProperty"]], result)

        @builtins.property
        def extraction(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemoryPropsMixin.SemanticOverrideExtractionConfigurationInputProperty"]]:
            '''The memory override extraction.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-semanticoverride.html#cfn-bedrockagentcore-memory-semanticoverride-extraction
            '''
            result = self._values.get("extraction")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemoryPropsMixin.SemanticOverrideExtractionConfigurationInputProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SemanticOverrideProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnMemoryPropsMixin.SummaryMemoryStrategyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "created_at": "createdAt",
            "description": "description",
            "name": "name",
            "namespaces": "namespaces",
            "status": "status",
            "strategy_id": "strategyId",
            "type": "type",
            "updated_at": "updatedAt",
        },
    )
    class SummaryMemoryStrategyProperty:
        def __init__(
            self,
            *,
            created_at: typing.Optional[builtins.str] = None,
            description: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
            status: typing.Optional[builtins.str] = None,
            strategy_id: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
            updated_at: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The memory strategy.

            :param created_at: Creation timestamp of the memory strategy.
            :param description: The memory strategy description.
            :param name: The memory strategy name.
            :param namespaces: The summary memory strategy.
            :param status: The memory strategy status.
            :param strategy_id: The memory strategy ID.
            :param type: The memory strategy type.
            :param updated_at: The memory strategy update date and time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-summarymemorystrategy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                summary_memory_strategy_property = bedrockagentcore_mixins.CfnMemoryPropsMixin.SummaryMemoryStrategyProperty(
                    created_at="createdAt",
                    description="description",
                    name="name",
                    namespaces=["namespaces"],
                    status="status",
                    strategy_id="strategyId",
                    type="type",
                    updated_at="updatedAt"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ee76910e6915808a5a40e6c89a2f9052a20080effa45f504138a111fc0af229d)
                check_type(argname="argument created_at", value=created_at, expected_type=type_hints["created_at"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument namespaces", value=namespaces, expected_type=type_hints["namespaces"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                check_type(argname="argument strategy_id", value=strategy_id, expected_type=type_hints["strategy_id"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument updated_at", value=updated_at, expected_type=type_hints["updated_at"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if created_at is not None:
                self._values["created_at"] = created_at
            if description is not None:
                self._values["description"] = description
            if name is not None:
                self._values["name"] = name
            if namespaces is not None:
                self._values["namespaces"] = namespaces
            if status is not None:
                self._values["status"] = status
            if strategy_id is not None:
                self._values["strategy_id"] = strategy_id
            if type is not None:
                self._values["type"] = type
            if updated_at is not None:
                self._values["updated_at"] = updated_at

        @builtins.property
        def created_at(self) -> typing.Optional[builtins.str]:
            '''Creation timestamp of the memory strategy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-summarymemorystrategy.html#cfn-bedrockagentcore-memory-summarymemorystrategy-createdat
            '''
            result = self._values.get("created_at")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The memory strategy description.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-summarymemorystrategy.html#cfn-bedrockagentcore-memory-summarymemorystrategy-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The memory strategy name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-summarymemorystrategy.html#cfn-bedrockagentcore-memory-summarymemorystrategy-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def namespaces(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The summary memory strategy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-summarymemorystrategy.html#cfn-bedrockagentcore-memory-summarymemorystrategy-namespaces
            '''
            result = self._values.get("namespaces")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''The memory strategy status.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-summarymemorystrategy.html#cfn-bedrockagentcore-memory-summarymemorystrategy-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def strategy_id(self) -> typing.Optional[builtins.str]:
            '''The memory strategy ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-summarymemorystrategy.html#cfn-bedrockagentcore-memory-summarymemorystrategy-strategyid
            '''
            result = self._values.get("strategy_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The memory strategy type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-summarymemorystrategy.html#cfn-bedrockagentcore-memory-summarymemorystrategy-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def updated_at(self) -> typing.Optional[builtins.str]:
            '''The memory strategy update date and time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-summarymemorystrategy.html#cfn-bedrockagentcore-memory-summarymemorystrategy-updatedat
            '''
            result = self._values.get("updated_at")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SummaryMemoryStrategyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnMemoryPropsMixin.SummaryOverrideConsolidationConfigurationInputProperty",
        jsii_struct_bases=[],
        name_mapping={"append_to_prompt": "appendToPrompt", "model_id": "modelId"},
    )
    class SummaryOverrideConsolidationConfigurationInputProperty:
        def __init__(
            self,
            *,
            append_to_prompt: typing.Optional[builtins.str] = None,
            model_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The consolidation configuration.

            :param append_to_prompt: The memory override configuration.
            :param model_id: The memory override configuration model ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-summaryoverrideconsolidationconfigurationinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                summary_override_consolidation_configuration_input_property = bedrockagentcore_mixins.CfnMemoryPropsMixin.SummaryOverrideConsolidationConfigurationInputProperty(
                    append_to_prompt="appendToPrompt",
                    model_id="modelId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a4030e8c8159cd5bff567fd5d0fae6fcbf437fe0a829eab29ce8d21c518335b5)
                check_type(argname="argument append_to_prompt", value=append_to_prompt, expected_type=type_hints["append_to_prompt"])
                check_type(argname="argument model_id", value=model_id, expected_type=type_hints["model_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if append_to_prompt is not None:
                self._values["append_to_prompt"] = append_to_prompt
            if model_id is not None:
                self._values["model_id"] = model_id

        @builtins.property
        def append_to_prompt(self) -> typing.Optional[builtins.str]:
            '''The memory override configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-summaryoverrideconsolidationconfigurationinput.html#cfn-bedrockagentcore-memory-summaryoverrideconsolidationconfigurationinput-appendtoprompt
            '''
            result = self._values.get("append_to_prompt")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def model_id(self) -> typing.Optional[builtins.str]:
            '''The memory override configuration model ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-summaryoverrideconsolidationconfigurationinput.html#cfn-bedrockagentcore-memory-summaryoverrideconsolidationconfigurationinput-modelid
            '''
            result = self._values.get("model_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SummaryOverrideConsolidationConfigurationInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnMemoryPropsMixin.SummaryOverrideProperty",
        jsii_struct_bases=[],
        name_mapping={"consolidation": "consolidation"},
    )
    class SummaryOverrideProperty:
        def __init__(
            self,
            *,
            consolidation: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMemoryPropsMixin.SummaryOverrideConsolidationConfigurationInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The memory summary override.

            :param consolidation: The memory override consolidation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-summaryoverride.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                summary_override_property = bedrockagentcore_mixins.CfnMemoryPropsMixin.SummaryOverrideProperty(
                    consolidation=bedrockagentcore_mixins.CfnMemoryPropsMixin.SummaryOverrideConsolidationConfigurationInputProperty(
                        append_to_prompt="appendToPrompt",
                        model_id="modelId"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8dabf19b9b2f375aa6b70ddbd1a91f6280aefd8a2d4712fee71052c08921bdbd)
                check_type(argname="argument consolidation", value=consolidation, expected_type=type_hints["consolidation"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if consolidation is not None:
                self._values["consolidation"] = consolidation

        @builtins.property
        def consolidation(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemoryPropsMixin.SummaryOverrideConsolidationConfigurationInputProperty"]]:
            '''The memory override consolidation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-summaryoverride.html#cfn-bedrockagentcore-memory-summaryoverride-consolidation
            '''
            result = self._values.get("consolidation")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemoryPropsMixin.SummaryOverrideConsolidationConfigurationInputProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SummaryOverrideProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnMemoryPropsMixin.TimeBasedTriggerInputProperty",
        jsii_struct_bases=[],
        name_mapping={"idle_session_timeout": "idleSessionTimeout"},
    )
    class TimeBasedTriggerInputProperty:
        def __init__(
            self,
            *,
            idle_session_timeout: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The memory trigger condition input for the time based trigger.

            :param idle_session_timeout: The memory trigger condition input for the session timeout.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-timebasedtriggerinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                time_based_trigger_input_property = bedrockagentcore_mixins.CfnMemoryPropsMixin.TimeBasedTriggerInputProperty(
                    idle_session_timeout=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b50f80e3bce99c8272b80749996e8b2d013f674d46c0ac8cde566cb6c87fac3e)
                check_type(argname="argument idle_session_timeout", value=idle_session_timeout, expected_type=type_hints["idle_session_timeout"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if idle_session_timeout is not None:
                self._values["idle_session_timeout"] = idle_session_timeout

        @builtins.property
        def idle_session_timeout(self) -> typing.Optional[jsii.Number]:
            '''The memory trigger condition input for the session timeout.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-timebasedtriggerinput.html#cfn-bedrockagentcore-memory-timebasedtriggerinput-idlesessiontimeout
            '''
            result = self._values.get("idle_session_timeout")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TimeBasedTriggerInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnMemoryPropsMixin.TokenBasedTriggerInputProperty",
        jsii_struct_bases=[],
        name_mapping={"token_count": "tokenCount"},
    )
    class TokenBasedTriggerInputProperty:
        def __init__(self, *, token_count: typing.Optional[jsii.Number] = None) -> None:
            '''The token based trigger input.

            :param token_count: The token based trigger token count.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-tokenbasedtriggerinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                token_based_trigger_input_property = bedrockagentcore_mixins.CfnMemoryPropsMixin.TokenBasedTriggerInputProperty(
                    token_count=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ab3ab521f197380bb08749252596df1c0d2962b66d994bc0664a6028853402d1)
                check_type(argname="argument token_count", value=token_count, expected_type=type_hints["token_count"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if token_count is not None:
                self._values["token_count"] = token_count

        @builtins.property
        def token_count(self) -> typing.Optional[jsii.Number]:
            '''The token based trigger token count.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-tokenbasedtriggerinput.html#cfn-bedrockagentcore-memory-tokenbasedtriggerinput-tokencount
            '''
            result = self._values.get("token_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TokenBasedTriggerInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnMemoryPropsMixin.TriggerConditionInputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "message_based_trigger": "messageBasedTrigger",
            "time_based_trigger": "timeBasedTrigger",
            "token_based_trigger": "tokenBasedTrigger",
        },
    )
    class TriggerConditionInputProperty:
        def __init__(
            self,
            *,
            message_based_trigger: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMemoryPropsMixin.MessageBasedTriggerInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            time_based_trigger: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMemoryPropsMixin.TimeBasedTriggerInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            token_based_trigger: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMemoryPropsMixin.TokenBasedTriggerInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The memory trigger condition input.

            :param message_based_trigger: The memory trigger condition input for the message based trigger.
            :param time_based_trigger: The memory trigger condition input.
            :param token_based_trigger: The trigger condition information for a token based trigger.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-triggerconditioninput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                trigger_condition_input_property = bedrockagentcore_mixins.CfnMemoryPropsMixin.TriggerConditionInputProperty(
                    message_based_trigger=bedrockagentcore_mixins.CfnMemoryPropsMixin.MessageBasedTriggerInputProperty(
                        message_count=123
                    ),
                    time_based_trigger=bedrockagentcore_mixins.CfnMemoryPropsMixin.TimeBasedTriggerInputProperty(
                        idle_session_timeout=123
                    ),
                    token_based_trigger=bedrockagentcore_mixins.CfnMemoryPropsMixin.TokenBasedTriggerInputProperty(
                        token_count=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ce9436814e9b2eb58e4c0a300580feae4d8fe8851be77e2d57fc40c4586a0d95)
                check_type(argname="argument message_based_trigger", value=message_based_trigger, expected_type=type_hints["message_based_trigger"])
                check_type(argname="argument time_based_trigger", value=time_based_trigger, expected_type=type_hints["time_based_trigger"])
                check_type(argname="argument token_based_trigger", value=token_based_trigger, expected_type=type_hints["token_based_trigger"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if message_based_trigger is not None:
                self._values["message_based_trigger"] = message_based_trigger
            if time_based_trigger is not None:
                self._values["time_based_trigger"] = time_based_trigger
            if token_based_trigger is not None:
                self._values["token_based_trigger"] = token_based_trigger

        @builtins.property
        def message_based_trigger(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemoryPropsMixin.MessageBasedTriggerInputProperty"]]:
            '''The memory trigger condition input for the message based trigger.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-triggerconditioninput.html#cfn-bedrockagentcore-memory-triggerconditioninput-messagebasedtrigger
            '''
            result = self._values.get("message_based_trigger")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemoryPropsMixin.MessageBasedTriggerInputProperty"]], result)

        @builtins.property
        def time_based_trigger(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemoryPropsMixin.TimeBasedTriggerInputProperty"]]:
            '''The memory trigger condition input.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-triggerconditioninput.html#cfn-bedrockagentcore-memory-triggerconditioninput-timebasedtrigger
            '''
            result = self._values.get("time_based_trigger")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemoryPropsMixin.TimeBasedTriggerInputProperty"]], result)

        @builtins.property
        def token_based_trigger(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemoryPropsMixin.TokenBasedTriggerInputProperty"]]:
            '''The trigger condition information for a token based trigger.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-triggerconditioninput.html#cfn-bedrockagentcore-memory-triggerconditioninput-tokenbasedtrigger
            '''
            result = self._values.get("token_based_trigger")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemoryPropsMixin.TokenBasedTriggerInputProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TriggerConditionInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnMemoryPropsMixin.UserPreferenceMemoryStrategyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "created_at": "createdAt",
            "description": "description",
            "name": "name",
            "namespaces": "namespaces",
            "status": "status",
            "strategy_id": "strategyId",
            "type": "type",
            "updated_at": "updatedAt",
        },
    )
    class UserPreferenceMemoryStrategyProperty:
        def __init__(
            self,
            *,
            created_at: typing.Optional[builtins.str] = None,
            description: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
            status: typing.Optional[builtins.str] = None,
            strategy_id: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
            updated_at: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The memory strategy.

            :param created_at: Creation timestamp of the memory strategy.
            :param description: The memory strategy description.
            :param name: The memory strategy name.
            :param namespaces: The memory namespaces.
            :param status: The memory strategy status.
            :param strategy_id: The memory strategy ID.
            :param type: The memory strategy type.
            :param updated_at: The memory strategy update date and time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-userpreferencememorystrategy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                user_preference_memory_strategy_property = bedrockagentcore_mixins.CfnMemoryPropsMixin.UserPreferenceMemoryStrategyProperty(
                    created_at="createdAt",
                    description="description",
                    name="name",
                    namespaces=["namespaces"],
                    status="status",
                    strategy_id="strategyId",
                    type="type",
                    updated_at="updatedAt"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bd938f1e1addc552b187c98501c5928d67daf3b4522aed4fa3d277aaf4b08f58)
                check_type(argname="argument created_at", value=created_at, expected_type=type_hints["created_at"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument namespaces", value=namespaces, expected_type=type_hints["namespaces"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                check_type(argname="argument strategy_id", value=strategy_id, expected_type=type_hints["strategy_id"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument updated_at", value=updated_at, expected_type=type_hints["updated_at"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if created_at is not None:
                self._values["created_at"] = created_at
            if description is not None:
                self._values["description"] = description
            if name is not None:
                self._values["name"] = name
            if namespaces is not None:
                self._values["namespaces"] = namespaces
            if status is not None:
                self._values["status"] = status
            if strategy_id is not None:
                self._values["strategy_id"] = strategy_id
            if type is not None:
                self._values["type"] = type
            if updated_at is not None:
                self._values["updated_at"] = updated_at

        @builtins.property
        def created_at(self) -> typing.Optional[builtins.str]:
            '''Creation timestamp of the memory strategy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-userpreferencememorystrategy.html#cfn-bedrockagentcore-memory-userpreferencememorystrategy-createdat
            '''
            result = self._values.get("created_at")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The memory strategy description.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-userpreferencememorystrategy.html#cfn-bedrockagentcore-memory-userpreferencememorystrategy-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The memory strategy name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-userpreferencememorystrategy.html#cfn-bedrockagentcore-memory-userpreferencememorystrategy-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def namespaces(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The memory namespaces.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-userpreferencememorystrategy.html#cfn-bedrockagentcore-memory-userpreferencememorystrategy-namespaces
            '''
            result = self._values.get("namespaces")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''The memory strategy status.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-userpreferencememorystrategy.html#cfn-bedrockagentcore-memory-userpreferencememorystrategy-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def strategy_id(self) -> typing.Optional[builtins.str]:
            '''The memory strategy ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-userpreferencememorystrategy.html#cfn-bedrockagentcore-memory-userpreferencememorystrategy-strategyid
            '''
            result = self._values.get("strategy_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The memory strategy type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-userpreferencememorystrategy.html#cfn-bedrockagentcore-memory-userpreferencememorystrategy-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def updated_at(self) -> typing.Optional[builtins.str]:
            '''The memory strategy update date and time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-userpreferencememorystrategy.html#cfn-bedrockagentcore-memory-userpreferencememorystrategy-updatedat
            '''
            result = self._values.get("updated_at")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UserPreferenceMemoryStrategyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnMemoryPropsMixin.UserPreferenceOverrideConsolidationConfigurationInputProperty",
        jsii_struct_bases=[],
        name_mapping={"append_to_prompt": "appendToPrompt", "model_id": "modelId"},
    )
    class UserPreferenceOverrideConsolidationConfigurationInputProperty:
        def __init__(
            self,
            *,
            append_to_prompt: typing.Optional[builtins.str] = None,
            model_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration input.

            :param append_to_prompt: The memory configuration.
            :param model_id: The memory override configuration model ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-userpreferenceoverrideconsolidationconfigurationinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                user_preference_override_consolidation_configuration_input_property = bedrockagentcore_mixins.CfnMemoryPropsMixin.UserPreferenceOverrideConsolidationConfigurationInputProperty(
                    append_to_prompt="appendToPrompt",
                    model_id="modelId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e3e7891ae977481d98b022c6fa981d06929da2731a1d393cffb6a07dcff87065)
                check_type(argname="argument append_to_prompt", value=append_to_prompt, expected_type=type_hints["append_to_prompt"])
                check_type(argname="argument model_id", value=model_id, expected_type=type_hints["model_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if append_to_prompt is not None:
                self._values["append_to_prompt"] = append_to_prompt
            if model_id is not None:
                self._values["model_id"] = model_id

        @builtins.property
        def append_to_prompt(self) -> typing.Optional[builtins.str]:
            '''The memory configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-userpreferenceoverrideconsolidationconfigurationinput.html#cfn-bedrockagentcore-memory-userpreferenceoverrideconsolidationconfigurationinput-appendtoprompt
            '''
            result = self._values.get("append_to_prompt")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def model_id(self) -> typing.Optional[builtins.str]:
            '''The memory override configuration model ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-userpreferenceoverrideconsolidationconfigurationinput.html#cfn-bedrockagentcore-memory-userpreferenceoverrideconsolidationconfigurationinput-modelid
            '''
            result = self._values.get("model_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UserPreferenceOverrideConsolidationConfigurationInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnMemoryPropsMixin.UserPreferenceOverrideExtractionConfigurationInputProperty",
        jsii_struct_bases=[],
        name_mapping={"append_to_prompt": "appendToPrompt", "model_id": "modelId"},
    )
    class UserPreferenceOverrideExtractionConfigurationInputProperty:
        def __init__(
            self,
            *,
            append_to_prompt: typing.Optional[builtins.str] = None,
            model_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The memory override configuration.

            :param append_to_prompt: The extraction configuration.
            :param model_id: The memory override for the model ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-userpreferenceoverrideextractionconfigurationinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                user_preference_override_extraction_configuration_input_property = bedrockagentcore_mixins.CfnMemoryPropsMixin.UserPreferenceOverrideExtractionConfigurationInputProperty(
                    append_to_prompt="appendToPrompt",
                    model_id="modelId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6f33a823344068e5781b7ae9fb9946525b289c962ed37f9c9a189863ead97445)
                check_type(argname="argument append_to_prompt", value=append_to_prompt, expected_type=type_hints["append_to_prompt"])
                check_type(argname="argument model_id", value=model_id, expected_type=type_hints["model_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if append_to_prompt is not None:
                self._values["append_to_prompt"] = append_to_prompt
            if model_id is not None:
                self._values["model_id"] = model_id

        @builtins.property
        def append_to_prompt(self) -> typing.Optional[builtins.str]:
            '''The extraction configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-userpreferenceoverrideextractionconfigurationinput.html#cfn-bedrockagentcore-memory-userpreferenceoverrideextractionconfigurationinput-appendtoprompt
            '''
            result = self._values.get("append_to_prompt")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def model_id(self) -> typing.Optional[builtins.str]:
            '''The memory override for the model ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-userpreferenceoverrideextractionconfigurationinput.html#cfn-bedrockagentcore-memory-userpreferenceoverrideextractionconfigurationinput-modelid
            '''
            result = self._values.get("model_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UserPreferenceOverrideExtractionConfigurationInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnMemoryPropsMixin.UserPreferenceOverrideProperty",
        jsii_struct_bases=[],
        name_mapping={"consolidation": "consolidation", "extraction": "extraction"},
    )
    class UserPreferenceOverrideProperty:
        def __init__(
            self,
            *,
            consolidation: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMemoryPropsMixin.UserPreferenceOverrideConsolidationConfigurationInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            extraction: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMemoryPropsMixin.UserPreferenceOverrideExtractionConfigurationInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The memory user preference override.

            :param consolidation: The memory override consolidation information.
            :param extraction: The memory user preferences for extraction.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-userpreferenceoverride.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                user_preference_override_property = bedrockagentcore_mixins.CfnMemoryPropsMixin.UserPreferenceOverrideProperty(
                    consolidation=bedrockagentcore_mixins.CfnMemoryPropsMixin.UserPreferenceOverrideConsolidationConfigurationInputProperty(
                        append_to_prompt="appendToPrompt",
                        model_id="modelId"
                    ),
                    extraction=bedrockagentcore_mixins.CfnMemoryPropsMixin.UserPreferenceOverrideExtractionConfigurationInputProperty(
                        append_to_prompt="appendToPrompt",
                        model_id="modelId"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__970d9a40e86f10a8effddfad4bca4832e6abbcaa713551d2989289ca6e9d7ca0)
                check_type(argname="argument consolidation", value=consolidation, expected_type=type_hints["consolidation"])
                check_type(argname="argument extraction", value=extraction, expected_type=type_hints["extraction"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if consolidation is not None:
                self._values["consolidation"] = consolidation
            if extraction is not None:
                self._values["extraction"] = extraction

        @builtins.property
        def consolidation(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemoryPropsMixin.UserPreferenceOverrideConsolidationConfigurationInputProperty"]]:
            '''The memory override consolidation information.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-userpreferenceoverride.html#cfn-bedrockagentcore-memory-userpreferenceoverride-consolidation
            '''
            result = self._values.get("consolidation")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemoryPropsMixin.UserPreferenceOverrideConsolidationConfigurationInputProperty"]], result)

        @builtins.property
        def extraction(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemoryPropsMixin.UserPreferenceOverrideExtractionConfigurationInputProperty"]]:
            '''The memory user preferences for extraction.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-memory-userpreferenceoverride.html#cfn-bedrockagentcore-memory-userpreferenceoverride-extraction
            '''
            result = self._values.get("extraction")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemoryPropsMixin.UserPreferenceOverrideExtractionConfigurationInputProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UserPreferenceOverrideProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


class CfnMemoryTraces(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnMemoryTraces",
):
    '''Builder for CfnMemoryLogsMixin to generate TRACES for CfnMemory.

    :cloudformationResource: AWS::BedrockAgentCore::Memory
    :logType: TRACES
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
        
        cfn_memory_traces = bedrockagentcore_mixins.CfnMemoryTraces()
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toXRay")
    def to_x_ray(self) -> CfnMemoryLogsMixin:
        '''Send traces to X-Ray.'''
        return typing.cast(CfnMemoryLogsMixin, jsii.invoke(self, "toXRay", []))


class CfnRuntimeApplicationLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnRuntimeApplicationLogs",
):
    '''Builder for CfnRuntimeLogsMixin to generate APPLICATION_LOGS for CfnRuntime.

    :cloudformationResource: AWS::BedrockAgentCore::Runtime
    :logType: APPLICATION_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
        
        cfn_runtime_application_logs = bedrockagentcore_mixins.CfnRuntimeApplicationLogs()
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toFirehose")
    def to_firehose(
        self,
        delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
    ) -> "CfnRuntimeLogsMixin":
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e26d0a37462ec4cab91d61182b516d7706c94f20b05770494a7bf34f1f340405)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast("CfnRuntimeLogsMixin", jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> "CfnRuntimeLogsMixin":
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baf26c8e9d08f77c0c132cfa2f9be98b4ced10acf2a9b28a07fd5fe2fdfda041)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast("CfnRuntimeLogsMixin", jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> "CfnRuntimeLogsMixin":
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45fb75951d996e803562ee5390a56b8736cdafd348f8d8ff221fe415d7f18306)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast("CfnRuntimeLogsMixin", jsii.invoke(self, "toS3", [bucket]))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnRuntimeEndpointMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "agent_runtime_id": "agentRuntimeId",
        "agent_runtime_version": "agentRuntimeVersion",
        "description": "description",
        "name": "name",
        "tags": "tags",
    },
)
class CfnRuntimeEndpointMixinProps:
    def __init__(
        self,
        *,
        agent_runtime_id: typing.Optional[builtins.str] = None,
        agent_runtime_version: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnRuntimeEndpointPropsMixin.

        :param agent_runtime_id: The agent runtime ID.
        :param agent_runtime_version: The version of the agent.
        :param description: Contains information about an agent runtime endpoint. An agent runtime is the execution environment for a Amazon Bedrock Agent.
        :param name: The name of the AgentCore Runtime endpoint.
        :param tags: The tags for the AgentCore Runtime endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-runtimeendpoint.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
            
            cfn_runtime_endpoint_mixin_props = bedrockagentcore_mixins.CfnRuntimeEndpointMixinProps(
                agent_runtime_id="agentRuntimeId",
                agent_runtime_version="agentRuntimeVersion",
                description="description",
                name="name",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fca95be55db0e91c922cb6bbc9845f34ea0a6a4a7f80978df1afa5b408a56fa)
            check_type(argname="argument agent_runtime_id", value=agent_runtime_id, expected_type=type_hints["agent_runtime_id"])
            check_type(argname="argument agent_runtime_version", value=agent_runtime_version, expected_type=type_hints["agent_runtime_version"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if agent_runtime_id is not None:
            self._values["agent_runtime_id"] = agent_runtime_id
        if agent_runtime_version is not None:
            self._values["agent_runtime_version"] = agent_runtime_version
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def agent_runtime_id(self) -> typing.Optional[builtins.str]:
        '''The agent runtime ID.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-runtimeendpoint.html#cfn-bedrockagentcore-runtimeendpoint-agentruntimeid
        '''
        result = self._values.get("agent_runtime_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def agent_runtime_version(self) -> typing.Optional[builtins.str]:
        '''The version of the agent.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-runtimeendpoint.html#cfn-bedrockagentcore-runtimeendpoint-agentruntimeversion
        '''
        result = self._values.get("agent_runtime_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Contains information about an agent runtime endpoint.

        An agent runtime is the execution environment for a Amazon Bedrock Agent.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-runtimeendpoint.html#cfn-bedrockagentcore-runtimeendpoint-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the AgentCore Runtime endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-runtimeendpoint.html#cfn-bedrockagentcore-runtimeendpoint-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The tags for the AgentCore Runtime endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-runtimeendpoint.html#cfn-bedrockagentcore-runtimeendpoint-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRuntimeEndpointMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnRuntimeEndpointPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnRuntimeEndpointPropsMixin",
):
    '''AgentCore Runtime is a secure, serverless runtime purpose-built for deploying and scaling dynamic AI agents and tools using any open-source framework including LangGraph, CrewAI, and Strands Agents, any protocol, and any model.

    For more information about using agent runtime endpoints in Amazon Bedrock AgentCore, see `AgentCore Runtime versioning and endpoints <https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agent-runtime-versioning.html>`_ .

    See the *Properties* section below for descriptions of both the required and optional properties.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-runtimeendpoint.html
    :cloudformationResource: AWS::BedrockAgentCore::RuntimeEndpoint
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
        
        cfn_runtime_endpoint_props_mixin = bedrockagentcore_mixins.CfnRuntimeEndpointPropsMixin(bedrockagentcore_mixins.CfnRuntimeEndpointMixinProps(
            agent_runtime_id="agentRuntimeId",
            agent_runtime_version="agentRuntimeVersion",
            description="description",
            name="name",
            tags={
                "tags_key": "tags"
            }
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnRuntimeEndpointMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::BedrockAgentCore::RuntimeEndpoint``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ee874d3104bef85b43ee825d40d603eaafbf54f8dc61fc2907d8ade76ca52cc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__16d86028542760e13c15b65ad68cf023c729af4c5df5d68f8a0d6b9cb0fdfb3a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4773465d21d7c8508bcc6963db2993d7474d2845fcff819ca39155aab58d4806)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnRuntimeEndpointMixinProps:
        return typing.cast(CfnRuntimeEndpointMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.implements(_IMixin_11e4b965)
class CfnRuntimeLogsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnRuntimeLogsMixin",
):
    '''Contains information about an agent runtime. An agent runtime is the execution environment for a Amazon Bedrock Agent.

    AgentCore Runtime is a secure, serverless runtime purpose-built for deploying and scaling dynamic AI agents and tools using any open-source framework including LangGraph, CrewAI, and Strands Agents, any protocol, and any model.

    For more information about using agent runtime in Amazon Bedrock AgentCore, see `Host agent or tools with Amazon Bedrock AgentCore Runtime <https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html>`_ .

    See the *Properties* section below for descriptions of both the required and optional properties.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-runtime.html
    :cloudformationResource: AWS::BedrockAgentCore::Runtime
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import aws_logs as logs
        from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
        
        # logs_delivery: logs.ILogsDelivery
        
        cfn_runtime_logs_mixin = bedrockagentcore_mixins.CfnRuntimeLogsMixin("logType", logs_delivery)
    '''

    def __init__(
        self,
        log_type: builtins.str,
        log_delivery: _ILogsDelivery_0d3c9e29,
    ) -> None:
        '''Create a mixin to enable vended logs for ``AWS::BedrockAgentCore::Runtime``.

        :param log_type: Type of logs that are getting vended.
        :param log_delivery: Object in charge of setting up the delivery destination and delivery connection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c929ee957c38ecb0579f34f4b66f6b56ef3ba96be84b3225d26fa2d3e7e422dd)
            check_type(argname="argument log_type", value=log_type, expected_type=type_hints["log_type"])
            check_type(argname="argument log_delivery", value=log_delivery, expected_type=type_hints["log_delivery"])
        jsii.create(self.__class__, self, [log_type, log_delivery])

    @jsii.member(jsii_name="applyTo")
    def apply_to(
        self,
        resource: _constructs_77d1e7e8.IConstruct,
    ) -> _constructs_77d1e7e8.IConstruct:
        '''Apply vended logs configuration to the construct.

        :param resource: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82afd6c4585e501a1f1696467983696efc0e5d38c4e491ede9ec6c24ec33b354)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [resource]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct (has vendedLogs property).

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffb1490e81fb92d5e598d8ba05358a0857f0478d107764d976388f3f5905d0d9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="APPLICATION_LOGS")
    def APPLICATION_LOGS(cls) -> CfnRuntimeApplicationLogs:
        return typing.cast(CfnRuntimeApplicationLogs, jsii.sget(cls, "APPLICATION_LOGS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="TRACES")
    def TRACES(cls) -> "CfnRuntimeTraces":
        return typing.cast("CfnRuntimeTraces", jsii.sget(cls, "TRACES"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="USAGE_LOGS")
    def USAGE_LOGS(cls) -> "CfnRuntimeUsageLogs":
        return typing.cast("CfnRuntimeUsageLogs", jsii.sget(cls, "USAGE_LOGS"))

    @builtins.property
    @jsii.member(jsii_name="logDelivery")
    def _log_delivery(self) -> _ILogsDelivery_0d3c9e29:
        return typing.cast(_ILogsDelivery_0d3c9e29, jsii.get(self, "logDelivery"))

    @builtins.property
    @jsii.member(jsii_name="logType")
    def _log_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logType"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnRuntimeMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "agent_runtime_artifact": "agentRuntimeArtifact",
        "agent_runtime_name": "agentRuntimeName",
        "authorizer_configuration": "authorizerConfiguration",
        "description": "description",
        "environment_variables": "environmentVariables",
        "lifecycle_configuration": "lifecycleConfiguration",
        "network_configuration": "networkConfiguration",
        "protocol_configuration": "protocolConfiguration",
        "request_header_configuration": "requestHeaderConfiguration",
        "role_arn": "roleArn",
        "tags": "tags",
    },
)
class CfnRuntimeMixinProps:
    def __init__(
        self,
        *,
        agent_runtime_artifact: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRuntimePropsMixin.AgentRuntimeArtifactProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        agent_runtime_name: typing.Optional[builtins.str] = None,
        authorizer_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRuntimePropsMixin.AuthorizerConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        environment_variables: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        lifecycle_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRuntimePropsMixin.LifecycleConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        network_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRuntimePropsMixin.NetworkConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        protocol_configuration: typing.Optional[builtins.str] = None,
        request_header_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRuntimePropsMixin.RequestHeaderConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnRuntimePropsMixin.

        :param agent_runtime_artifact: The artifact of the agent.
        :param agent_runtime_name: The name of the AgentCore Runtime endpoint.
        :param authorizer_configuration: Represents inbound authorization configuration options used to authenticate incoming requests.
        :param description: The agent runtime description.
        :param environment_variables: The environment variables for the agent.
        :param lifecycle_configuration: Configuration for managing the lifecycle of runtime sessions and resources.
        :param network_configuration: The network configuration.
        :param protocol_configuration: The protocol configuration for an agent runtime. This structure defines how the agent runtime communicates with clients.
        :param request_header_configuration: Configuration for HTTP request headers.
        :param role_arn: The Amazon Resource Name (ARN) for for the role.
        :param tags: The tags for the agent.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-runtime.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
            
            cfn_runtime_mixin_props = bedrockagentcore_mixins.CfnRuntimeMixinProps(
                agent_runtime_artifact=bedrockagentcore_mixins.CfnRuntimePropsMixin.AgentRuntimeArtifactProperty(
                    code_configuration=bedrockagentcore_mixins.CfnRuntimePropsMixin.CodeConfigurationProperty(
                        code=bedrockagentcore_mixins.CfnRuntimePropsMixin.CodeProperty(
                            s3=bedrockagentcore_mixins.CfnRuntimePropsMixin.S3LocationProperty(
                                bucket="bucket",
                                prefix="prefix",
                                version_id="versionId"
                            )
                        ),
                        entry_point=["entryPoint"],
                        runtime="runtime"
                    ),
                    container_configuration=bedrockagentcore_mixins.CfnRuntimePropsMixin.ContainerConfigurationProperty(
                        container_uri="containerUri"
                    )
                ),
                agent_runtime_name="agentRuntimeName",
                authorizer_configuration=bedrockagentcore_mixins.CfnRuntimePropsMixin.AuthorizerConfigurationProperty(
                    custom_jwt_authorizer=bedrockagentcore_mixins.CfnRuntimePropsMixin.CustomJWTAuthorizerConfigurationProperty(
                        allowed_audience=["allowedAudience"],
                        allowed_clients=["allowedClients"],
                        discovery_url="discoveryUrl"
                    )
                ),
                description="description",
                environment_variables={
                    "environment_variables_key": "environmentVariables"
                },
                lifecycle_configuration=bedrockagentcore_mixins.CfnRuntimePropsMixin.LifecycleConfigurationProperty(
                    idle_runtime_session_timeout=123,
                    max_lifetime=123
                ),
                network_configuration=bedrockagentcore_mixins.CfnRuntimePropsMixin.NetworkConfigurationProperty(
                    network_mode="networkMode",
                    network_mode_config=bedrockagentcore_mixins.CfnRuntimePropsMixin.VpcConfigProperty(
                        security_groups=["securityGroups"],
                        subnets=["subnets"]
                    )
                ),
                protocol_configuration="protocolConfiguration",
                request_header_configuration=bedrockagentcore_mixins.CfnRuntimePropsMixin.RequestHeaderConfigurationProperty(
                    request_header_allowlist=["requestHeaderAllowlist"]
                ),
                role_arn="roleArn",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01715e1fcca00084a57ca2aa5a3dfd01a87a0e2223cdc56fe01d6971c2f360cd)
            check_type(argname="argument agent_runtime_artifact", value=agent_runtime_artifact, expected_type=type_hints["agent_runtime_artifact"])
            check_type(argname="argument agent_runtime_name", value=agent_runtime_name, expected_type=type_hints["agent_runtime_name"])
            check_type(argname="argument authorizer_configuration", value=authorizer_configuration, expected_type=type_hints["authorizer_configuration"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
            check_type(argname="argument lifecycle_configuration", value=lifecycle_configuration, expected_type=type_hints["lifecycle_configuration"])
            check_type(argname="argument network_configuration", value=network_configuration, expected_type=type_hints["network_configuration"])
            check_type(argname="argument protocol_configuration", value=protocol_configuration, expected_type=type_hints["protocol_configuration"])
            check_type(argname="argument request_header_configuration", value=request_header_configuration, expected_type=type_hints["request_header_configuration"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if agent_runtime_artifact is not None:
            self._values["agent_runtime_artifact"] = agent_runtime_artifact
        if agent_runtime_name is not None:
            self._values["agent_runtime_name"] = agent_runtime_name
        if authorizer_configuration is not None:
            self._values["authorizer_configuration"] = authorizer_configuration
        if description is not None:
            self._values["description"] = description
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if lifecycle_configuration is not None:
            self._values["lifecycle_configuration"] = lifecycle_configuration
        if network_configuration is not None:
            self._values["network_configuration"] = network_configuration
        if protocol_configuration is not None:
            self._values["protocol_configuration"] = protocol_configuration
        if request_header_configuration is not None:
            self._values["request_header_configuration"] = request_header_configuration
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def agent_runtime_artifact(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuntimePropsMixin.AgentRuntimeArtifactProperty"]]:
        '''The artifact of the agent.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-runtime.html#cfn-bedrockagentcore-runtime-agentruntimeartifact
        '''
        result = self._values.get("agent_runtime_artifact")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuntimePropsMixin.AgentRuntimeArtifactProperty"]], result)

    @builtins.property
    def agent_runtime_name(self) -> typing.Optional[builtins.str]:
        '''The name of the AgentCore Runtime endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-runtime.html#cfn-bedrockagentcore-runtime-agentruntimename
        '''
        result = self._values.get("agent_runtime_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authorizer_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuntimePropsMixin.AuthorizerConfigurationProperty"]]:
        '''Represents inbound authorization configuration options used to authenticate incoming requests.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-runtime.html#cfn-bedrockagentcore-runtime-authorizerconfiguration
        '''
        result = self._values.get("authorizer_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuntimePropsMixin.AuthorizerConfigurationProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The agent runtime description.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-runtime.html#cfn-bedrockagentcore-runtime-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
        '''The environment variables for the agent.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-runtime.html#cfn-bedrockagentcore-runtime-environmentvariables
        '''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def lifecycle_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuntimePropsMixin.LifecycleConfigurationProperty"]]:
        '''Configuration for managing the lifecycle of runtime sessions and resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-runtime.html#cfn-bedrockagentcore-runtime-lifecycleconfiguration
        '''
        result = self._values.get("lifecycle_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuntimePropsMixin.LifecycleConfigurationProperty"]], result)

    @builtins.property
    def network_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuntimePropsMixin.NetworkConfigurationProperty"]]:
        '''The network configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-runtime.html#cfn-bedrockagentcore-runtime-networkconfiguration
        '''
        result = self._values.get("network_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuntimePropsMixin.NetworkConfigurationProperty"]], result)

    @builtins.property
    def protocol_configuration(self) -> typing.Optional[builtins.str]:
        '''The protocol configuration for an agent runtime.

        This structure defines how the agent runtime communicates with clients.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-runtime.html#cfn-bedrockagentcore-runtime-protocolconfiguration
        '''
        result = self._values.get("protocol_configuration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_header_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuntimePropsMixin.RequestHeaderConfigurationProperty"]]:
        '''Configuration for HTTP request headers.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-runtime.html#cfn-bedrockagentcore-runtime-requestheaderconfiguration
        '''
        result = self._values.get("request_header_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuntimePropsMixin.RequestHeaderConfigurationProperty"]], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) for for the role.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-runtime.html#cfn-bedrockagentcore-runtime-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The tags for the agent.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-runtime.html#cfn-bedrockagentcore-runtime-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRuntimeMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnRuntimePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnRuntimePropsMixin",
):
    '''Contains information about an agent runtime. An agent runtime is the execution environment for a Amazon Bedrock Agent.

    AgentCore Runtime is a secure, serverless runtime purpose-built for deploying and scaling dynamic AI agents and tools using any open-source framework including LangGraph, CrewAI, and Strands Agents, any protocol, and any model.

    For more information about using agent runtime in Amazon Bedrock AgentCore, see `Host agent or tools with Amazon Bedrock AgentCore Runtime <https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html>`_ .

    See the *Properties* section below for descriptions of both the required and optional properties.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-runtime.html
    :cloudformationResource: AWS::BedrockAgentCore::Runtime
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
        
        cfn_runtime_props_mixin = bedrockagentcore_mixins.CfnRuntimePropsMixin(bedrockagentcore_mixins.CfnRuntimeMixinProps(
            agent_runtime_artifact=bedrockagentcore_mixins.CfnRuntimePropsMixin.AgentRuntimeArtifactProperty(
                code_configuration=bedrockagentcore_mixins.CfnRuntimePropsMixin.CodeConfigurationProperty(
                    code=bedrockagentcore_mixins.CfnRuntimePropsMixin.CodeProperty(
                        s3=bedrockagentcore_mixins.CfnRuntimePropsMixin.S3LocationProperty(
                            bucket="bucket",
                            prefix="prefix",
                            version_id="versionId"
                        )
                    ),
                    entry_point=["entryPoint"],
                    runtime="runtime"
                ),
                container_configuration=bedrockagentcore_mixins.CfnRuntimePropsMixin.ContainerConfigurationProperty(
                    container_uri="containerUri"
                )
            ),
            agent_runtime_name="agentRuntimeName",
            authorizer_configuration=bedrockagentcore_mixins.CfnRuntimePropsMixin.AuthorizerConfigurationProperty(
                custom_jwt_authorizer=bedrockagentcore_mixins.CfnRuntimePropsMixin.CustomJWTAuthorizerConfigurationProperty(
                    allowed_audience=["allowedAudience"],
                    allowed_clients=["allowedClients"],
                    discovery_url="discoveryUrl"
                )
            ),
            description="description",
            environment_variables={
                "environment_variables_key": "environmentVariables"
            },
            lifecycle_configuration=bedrockagentcore_mixins.CfnRuntimePropsMixin.LifecycleConfigurationProperty(
                idle_runtime_session_timeout=123,
                max_lifetime=123
            ),
            network_configuration=bedrockagentcore_mixins.CfnRuntimePropsMixin.NetworkConfigurationProperty(
                network_mode="networkMode",
                network_mode_config=bedrockagentcore_mixins.CfnRuntimePropsMixin.VpcConfigProperty(
                    security_groups=["securityGroups"],
                    subnets=["subnets"]
                )
            ),
            protocol_configuration="protocolConfiguration",
            request_header_configuration=bedrockagentcore_mixins.CfnRuntimePropsMixin.RequestHeaderConfigurationProperty(
                request_header_allowlist=["requestHeaderAllowlist"]
            ),
            role_arn="roleArn",
            tags={
                "tags_key": "tags"
            }
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnRuntimeMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::BedrockAgentCore::Runtime``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64276faab950ce6dbaec26763aaba5dd965d13ca2f60c7ac0255651c08720e94)
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
            type_hints = typing.get_type_hints(_typecheckingstub__62ecccb04216f1309a237051d362e5003ef93e2c3a1e028e80ba19b88fb84de5)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b20506c7cbd0470cfda483fa37267236d504760db8074f7a84492811612200e6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnRuntimeMixinProps:
        return typing.cast(CfnRuntimeMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnRuntimePropsMixin.AgentRuntimeArtifactProperty",
        jsii_struct_bases=[],
        name_mapping={
            "code_configuration": "codeConfiguration",
            "container_configuration": "containerConfiguration",
        },
    )
    class AgentRuntimeArtifactProperty:
        def __init__(
            self,
            *,
            code_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRuntimePropsMixin.CodeConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            container_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRuntimePropsMixin.ContainerConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The artifact of the agent.

            :param code_configuration: Representation of a code configuration.
            :param container_configuration: Representation of a container configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-runtime-agentruntimeartifact.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                agent_runtime_artifact_property = bedrockagentcore_mixins.CfnRuntimePropsMixin.AgentRuntimeArtifactProperty(
                    code_configuration=bedrockagentcore_mixins.CfnRuntimePropsMixin.CodeConfigurationProperty(
                        code=bedrockagentcore_mixins.CfnRuntimePropsMixin.CodeProperty(
                            s3=bedrockagentcore_mixins.CfnRuntimePropsMixin.S3LocationProperty(
                                bucket="bucket",
                                prefix="prefix",
                                version_id="versionId"
                            )
                        ),
                        entry_point=["entryPoint"],
                        runtime="runtime"
                    ),
                    container_configuration=bedrockagentcore_mixins.CfnRuntimePropsMixin.ContainerConfigurationProperty(
                        container_uri="containerUri"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__86adfb7a7d7818c5ef49b0900cf85ab97a96df842d7b443a33bc85850b32fc29)
                check_type(argname="argument code_configuration", value=code_configuration, expected_type=type_hints["code_configuration"])
                check_type(argname="argument container_configuration", value=container_configuration, expected_type=type_hints["container_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if code_configuration is not None:
                self._values["code_configuration"] = code_configuration
            if container_configuration is not None:
                self._values["container_configuration"] = container_configuration

        @builtins.property
        def code_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuntimePropsMixin.CodeConfigurationProperty"]]:
            '''Representation of a code configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-runtime-agentruntimeartifact.html#cfn-bedrockagentcore-runtime-agentruntimeartifact-codeconfiguration
            '''
            result = self._values.get("code_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuntimePropsMixin.CodeConfigurationProperty"]], result)

        @builtins.property
        def container_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuntimePropsMixin.ContainerConfigurationProperty"]]:
            '''Representation of a container configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-runtime-agentruntimeartifact.html#cfn-bedrockagentcore-runtime-agentruntimeartifact-containerconfiguration
            '''
            result = self._values.get("container_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuntimePropsMixin.ContainerConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AgentRuntimeArtifactProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnRuntimePropsMixin.AuthorizerConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"custom_jwt_authorizer": "customJwtAuthorizer"},
    )
    class AuthorizerConfigurationProperty:
        def __init__(
            self,
            *,
            custom_jwt_authorizer: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRuntimePropsMixin.CustomJWTAuthorizerConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The authorizer configuration.

            :param custom_jwt_authorizer: Represents inbound authorization configuration options used to authenticate incoming requests.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-runtime-authorizerconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                authorizer_configuration_property = bedrockagentcore_mixins.CfnRuntimePropsMixin.AuthorizerConfigurationProperty(
                    custom_jwt_authorizer=bedrockagentcore_mixins.CfnRuntimePropsMixin.CustomJWTAuthorizerConfigurationProperty(
                        allowed_audience=["allowedAudience"],
                        allowed_clients=["allowedClients"],
                        discovery_url="discoveryUrl"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__506d6f552f2c5f5d6c905940a0140795362061ed024c266b3efdbdf6d5b971d0)
                check_type(argname="argument custom_jwt_authorizer", value=custom_jwt_authorizer, expected_type=type_hints["custom_jwt_authorizer"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if custom_jwt_authorizer is not None:
                self._values["custom_jwt_authorizer"] = custom_jwt_authorizer

        @builtins.property
        def custom_jwt_authorizer(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuntimePropsMixin.CustomJWTAuthorizerConfigurationProperty"]]:
            '''Represents inbound authorization configuration options used to authenticate incoming requests.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-runtime-authorizerconfiguration.html#cfn-bedrockagentcore-runtime-authorizerconfiguration-customjwtauthorizer
            '''
            result = self._values.get("custom_jwt_authorizer")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuntimePropsMixin.CustomJWTAuthorizerConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthorizerConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnRuntimePropsMixin.CodeConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "code": "code",
            "entry_point": "entryPoint",
            "runtime": "runtime",
        },
    )
    class CodeConfigurationProperty:
        def __init__(
            self,
            *,
            code: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRuntimePropsMixin.CodeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            entry_point: typing.Optional[typing.Sequence[builtins.str]] = None,
            runtime: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Representation of a code configuration.

            :param code: Object represents source code from zip file.
            :param entry_point: List of entry points.
            :param runtime: Managed runtime types.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-runtime-codeconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                code_configuration_property = bedrockagentcore_mixins.CfnRuntimePropsMixin.CodeConfigurationProperty(
                    code=bedrockagentcore_mixins.CfnRuntimePropsMixin.CodeProperty(
                        s3=bedrockagentcore_mixins.CfnRuntimePropsMixin.S3LocationProperty(
                            bucket="bucket",
                            prefix="prefix",
                            version_id="versionId"
                        )
                    ),
                    entry_point=["entryPoint"],
                    runtime="runtime"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__afcda0cc08b4e2c0242fa9ff198c5882d4aa8b0e41bea4027fca9afcbae39646)
                check_type(argname="argument code", value=code, expected_type=type_hints["code"])
                check_type(argname="argument entry_point", value=entry_point, expected_type=type_hints["entry_point"])
                check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if code is not None:
                self._values["code"] = code
            if entry_point is not None:
                self._values["entry_point"] = entry_point
            if runtime is not None:
                self._values["runtime"] = runtime

        @builtins.property
        def code(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuntimePropsMixin.CodeProperty"]]:
            '''Object represents source code from zip file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-runtime-codeconfiguration.html#cfn-bedrockagentcore-runtime-codeconfiguration-code
            '''
            result = self._values.get("code")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuntimePropsMixin.CodeProperty"]], result)

        @builtins.property
        def entry_point(self) -> typing.Optional[typing.List[builtins.str]]:
            '''List of entry points.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-runtime-codeconfiguration.html#cfn-bedrockagentcore-runtime-codeconfiguration-entrypoint
            '''
            result = self._values.get("entry_point")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def runtime(self) -> typing.Optional[builtins.str]:
            '''Managed runtime types.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-runtime-codeconfiguration.html#cfn-bedrockagentcore-runtime-codeconfiguration-runtime
            '''
            result = self._values.get("runtime")
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
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnRuntimePropsMixin.CodeProperty",
        jsii_struct_bases=[],
        name_mapping={"s3": "s3"},
    )
    class CodeProperty:
        def __init__(
            self,
            *,
            s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRuntimePropsMixin.S3LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Object represents source code from zip file.

            :param s3: S3 Location Configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-runtime-code.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                code_property = bedrockagentcore_mixins.CfnRuntimePropsMixin.CodeProperty(
                    s3=bedrockagentcore_mixins.CfnRuntimePropsMixin.S3LocationProperty(
                        bucket="bucket",
                        prefix="prefix",
                        version_id="versionId"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9d9f24754c32e75093a37d60272870c0913eeaeab986337864f8e3900a80d270)
                check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3 is not None:
                self._values["s3"] = s3

        @builtins.property
        def s3(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuntimePropsMixin.S3LocationProperty"]]:
            '''S3 Location Configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-runtime-code.html#cfn-bedrockagentcore-runtime-code-s3
            '''
            result = self._values.get("s3")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuntimePropsMixin.S3LocationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CodeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnRuntimePropsMixin.ContainerConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"container_uri": "containerUri"},
    )
    class ContainerConfigurationProperty:
        def __init__(
            self,
            *,
            container_uri: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The container configuration.

            :param container_uri: The container Uri.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-runtime-containerconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                container_configuration_property = bedrockagentcore_mixins.CfnRuntimePropsMixin.ContainerConfigurationProperty(
                    container_uri="containerUri"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3a214acb52f9cd96d2ad5b32d7536d2f5f329286ab0ee3eac0fe7392435e0e4e)
                check_type(argname="argument container_uri", value=container_uri, expected_type=type_hints["container_uri"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if container_uri is not None:
                self._values["container_uri"] = container_uri

        @builtins.property
        def container_uri(self) -> typing.Optional[builtins.str]:
            '''The container Uri.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-runtime-containerconfiguration.html#cfn-bedrockagentcore-runtime-containerconfiguration-containeruri
            '''
            result = self._values.get("container_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ContainerConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnRuntimePropsMixin.CustomJWTAuthorizerConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allowed_audience": "allowedAudience",
            "allowed_clients": "allowedClients",
            "discovery_url": "discoveryUrl",
        },
    )
    class CustomJWTAuthorizerConfigurationProperty:
        def __init__(
            self,
            *,
            allowed_audience: typing.Optional[typing.Sequence[builtins.str]] = None,
            allowed_clients: typing.Optional[typing.Sequence[builtins.str]] = None,
            discovery_url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration for custom JWT authorizer.

            :param allowed_audience: Represents inbound authorization configuration options used to authenticate incoming requests.
            :param allowed_clients: Represents individual client IDs that are validated in the incoming JWT token validation process.
            :param discovery_url: The configuration authorization.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-runtime-customjwtauthorizerconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                custom_jWTAuthorizer_configuration_property = bedrockagentcore_mixins.CfnRuntimePropsMixin.CustomJWTAuthorizerConfigurationProperty(
                    allowed_audience=["allowedAudience"],
                    allowed_clients=["allowedClients"],
                    discovery_url="discoveryUrl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6a15fa6aae378e79f8a8f39db95900697caee5840f3ea82417e27499a493613c)
                check_type(argname="argument allowed_audience", value=allowed_audience, expected_type=type_hints["allowed_audience"])
                check_type(argname="argument allowed_clients", value=allowed_clients, expected_type=type_hints["allowed_clients"])
                check_type(argname="argument discovery_url", value=discovery_url, expected_type=type_hints["discovery_url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allowed_audience is not None:
                self._values["allowed_audience"] = allowed_audience
            if allowed_clients is not None:
                self._values["allowed_clients"] = allowed_clients
            if discovery_url is not None:
                self._values["discovery_url"] = discovery_url

        @builtins.property
        def allowed_audience(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Represents inbound authorization configuration options used to authenticate incoming requests.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-runtime-customjwtauthorizerconfiguration.html#cfn-bedrockagentcore-runtime-customjwtauthorizerconfiguration-allowedaudience
            '''
            result = self._values.get("allowed_audience")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def allowed_clients(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Represents individual client IDs that are validated in the incoming JWT token validation process.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-runtime-customjwtauthorizerconfiguration.html#cfn-bedrockagentcore-runtime-customjwtauthorizerconfiguration-allowedclients
            '''
            result = self._values.get("allowed_clients")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def discovery_url(self) -> typing.Optional[builtins.str]:
            '''The configuration authorization.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-runtime-customjwtauthorizerconfiguration.html#cfn-bedrockagentcore-runtime-customjwtauthorizerconfiguration-discoveryurl
            '''
            result = self._values.get("discovery_url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomJWTAuthorizerConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnRuntimePropsMixin.LifecycleConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "idle_runtime_session_timeout": "idleRuntimeSessionTimeout",
            "max_lifetime": "maxLifetime",
        },
    )
    class LifecycleConfigurationProperty:
        def __init__(
            self,
            *,
            idle_runtime_session_timeout: typing.Optional[jsii.Number] = None,
            max_lifetime: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Configuration for managing the lifecycle of runtime sessions and resources.

            :param idle_runtime_session_timeout: Timeout in seconds for idle runtime sessions.
            :param max_lifetime: Maximum lifetime in seconds for runtime sessions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-runtime-lifecycleconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                lifecycle_configuration_property = bedrockagentcore_mixins.CfnRuntimePropsMixin.LifecycleConfigurationProperty(
                    idle_runtime_session_timeout=123,
                    max_lifetime=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2674bdbe2f43b95380860af9d07286ec0ed037e5e490922ed56b2786453b7e40)
                check_type(argname="argument idle_runtime_session_timeout", value=idle_runtime_session_timeout, expected_type=type_hints["idle_runtime_session_timeout"])
                check_type(argname="argument max_lifetime", value=max_lifetime, expected_type=type_hints["max_lifetime"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if idle_runtime_session_timeout is not None:
                self._values["idle_runtime_session_timeout"] = idle_runtime_session_timeout
            if max_lifetime is not None:
                self._values["max_lifetime"] = max_lifetime

        @builtins.property
        def idle_runtime_session_timeout(self) -> typing.Optional[jsii.Number]:
            '''Timeout in seconds for idle runtime sessions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-runtime-lifecycleconfiguration.html#cfn-bedrockagentcore-runtime-lifecycleconfiguration-idleruntimesessiontimeout
            '''
            result = self._values.get("idle_runtime_session_timeout")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_lifetime(self) -> typing.Optional[jsii.Number]:
            '''Maximum lifetime in seconds for runtime sessions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-runtime-lifecycleconfiguration.html#cfn-bedrockagentcore-runtime-lifecycleconfiguration-maxlifetime
            '''
            result = self._values.get("max_lifetime")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LifecycleConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnRuntimePropsMixin.NetworkConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "network_mode": "networkMode",
            "network_mode_config": "networkModeConfig",
        },
    )
    class NetworkConfigurationProperty:
        def __init__(
            self,
            *,
            network_mode: typing.Optional[builtins.str] = None,
            network_mode_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRuntimePropsMixin.VpcConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The network configuration for the agent.

            :param network_mode: The network mode.
            :param network_mode_config: Network mode configuration for VPC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-runtime-networkconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                network_configuration_property = bedrockagentcore_mixins.CfnRuntimePropsMixin.NetworkConfigurationProperty(
                    network_mode="networkMode",
                    network_mode_config=bedrockagentcore_mixins.CfnRuntimePropsMixin.VpcConfigProperty(
                        security_groups=["securityGroups"],
                        subnets=["subnets"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c4d2df4a09ed1dc31eed989d539b7fd97c052591f9ea427bad52dea599e43730)
                check_type(argname="argument network_mode", value=network_mode, expected_type=type_hints["network_mode"])
                check_type(argname="argument network_mode_config", value=network_mode_config, expected_type=type_hints["network_mode_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if network_mode is not None:
                self._values["network_mode"] = network_mode
            if network_mode_config is not None:
                self._values["network_mode_config"] = network_mode_config

        @builtins.property
        def network_mode(self) -> typing.Optional[builtins.str]:
            '''The network mode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-runtime-networkconfiguration.html#cfn-bedrockagentcore-runtime-networkconfiguration-networkmode
            '''
            result = self._values.get("network_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def network_mode_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuntimePropsMixin.VpcConfigProperty"]]:
            '''Network mode configuration for VPC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-runtime-networkconfiguration.html#cfn-bedrockagentcore-runtime-networkconfiguration-networkmodeconfig
            '''
            result = self._values.get("network_mode_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuntimePropsMixin.VpcConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NetworkConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnRuntimePropsMixin.RequestHeaderConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"request_header_allowlist": "requestHeaderAllowlist"},
    )
    class RequestHeaderConfigurationProperty:
        def __init__(
            self,
            *,
            request_header_allowlist: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Configuration for HTTP request headers.

            :param request_header_allowlist: List of allowed HTTP headers for agent runtime requests.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-runtime-requestheaderconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                request_header_configuration_property = bedrockagentcore_mixins.CfnRuntimePropsMixin.RequestHeaderConfigurationProperty(
                    request_header_allowlist=["requestHeaderAllowlist"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__147f18a9cfa93687d5e38d02cf3c5b2f300959bed445fbad3efbad8c4442f4bb)
                check_type(argname="argument request_header_allowlist", value=request_header_allowlist, expected_type=type_hints["request_header_allowlist"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if request_header_allowlist is not None:
                self._values["request_header_allowlist"] = request_header_allowlist

        @builtins.property
        def request_header_allowlist(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''List of allowed HTTP headers for agent runtime requests.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-runtime-requestheaderconfiguration.html#cfn-bedrockagentcore-runtime-requestheaderconfiguration-requestheaderallowlist
            '''
            result = self._values.get("request_header_allowlist")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RequestHeaderConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnRuntimePropsMixin.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket": "bucket",
            "prefix": "prefix",
            "version_id": "versionId",
        },
    )
    class S3LocationProperty:
        def __init__(
            self,
            *,
            bucket: typing.Optional[builtins.str] = None,
            prefix: typing.Optional[builtins.str] = None,
            version_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''S3 Location Configuration.

            :param bucket: S3 bucket name.
            :param prefix: S3 object key prefix.
            :param version_id: S3 object version ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-runtime-s3location.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                s3_location_property = bedrockagentcore_mixins.CfnRuntimePropsMixin.S3LocationProperty(
                    bucket="bucket",
                    prefix="prefix",
                    version_id="versionId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9013961fdcf91ac32d13121234a4db53102fe8fb6e86a17b17020d10c2a3e34f)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
                check_type(argname="argument version_id", value=version_id, expected_type=type_hints["version_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket is not None:
                self._values["bucket"] = bucket
            if prefix is not None:
                self._values["prefix"] = prefix
            if version_id is not None:
                self._values["version_id"] = version_id

        @builtins.property
        def bucket(self) -> typing.Optional[builtins.str]:
            '''S3 bucket name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-runtime-s3location.html#cfn-bedrockagentcore-runtime-s3location-bucket
            '''
            result = self._values.get("bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''S3 object key prefix.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-runtime-s3location.html#cfn-bedrockagentcore-runtime-s3location-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version_id(self) -> typing.Optional[builtins.str]:
            '''S3 object version ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-runtime-s3location.html#cfn-bedrockagentcore-runtime-s3location-versionid
            '''
            result = self._values.get("version_id")
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
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnRuntimePropsMixin.VpcConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"security_groups": "securityGroups", "subnets": "subnets"},
    )
    class VpcConfigProperty:
        def __init__(
            self,
            *,
            security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Network mode configuration for VPC.

            :param security_groups: Security groups for VPC.
            :param subnets: Subnets for VPC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-runtime-vpcconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                vpc_config_property = bedrockagentcore_mixins.CfnRuntimePropsMixin.VpcConfigProperty(
                    security_groups=["securityGroups"],
                    subnets=["subnets"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b9c0a2debf066313e43615d66b3937e12b0c296c710ad8415049513bc2a42c49)
                check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
                check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if security_groups is not None:
                self._values["security_groups"] = security_groups
            if subnets is not None:
                self._values["subnets"] = subnets

        @builtins.property
        def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Security groups for VPC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-runtime-vpcconfig.html#cfn-bedrockagentcore-runtime-vpcconfig-securitygroups
            '''
            result = self._values.get("security_groups")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnets(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Subnets for VPC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-runtime-vpcconfig.html#cfn-bedrockagentcore-runtime-vpcconfig-subnets
            '''
            result = self._values.get("subnets")
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
        jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnRuntimePropsMixin.WorkloadIdentityDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={"workload_identity_arn": "workloadIdentityArn"},
    )
    class WorkloadIdentityDetailsProperty:
        def __init__(
            self,
            *,
            workload_identity_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The workload identity details for the agent.

            :param workload_identity_arn: The Amazon Resource Name (ARN) for the workload identity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-runtime-workloadidentitydetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
                
                workload_identity_details_property = bedrockagentcore_mixins.CfnRuntimePropsMixin.WorkloadIdentityDetailsProperty(
                    workload_identity_arn="workloadIdentityArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fbec5cca2900853683c64e083ea7b787422a53ddee1d9166e1b0595e804a2f47)
                check_type(argname="argument workload_identity_arn", value=workload_identity_arn, expected_type=type_hints["workload_identity_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if workload_identity_arn is not None:
                self._values["workload_identity_arn"] = workload_identity_arn

        @builtins.property
        def workload_identity_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) for the workload identity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrockagentcore-runtime-workloadidentitydetails.html#cfn-bedrockagentcore-runtime-workloadidentitydetails-workloadidentityarn
            '''
            result = self._values.get("workload_identity_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WorkloadIdentityDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


class CfnRuntimeTraces(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnRuntimeTraces",
):
    '''Builder for CfnRuntimeLogsMixin to generate TRACES for CfnRuntime.

    :cloudformationResource: AWS::BedrockAgentCore::Runtime
    :logType: TRACES
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
        
        cfn_runtime_traces = bedrockagentcore_mixins.CfnRuntimeTraces()
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toXRay")
    def to_x_ray(self) -> CfnRuntimeLogsMixin:
        '''Send traces to X-Ray.'''
        return typing.cast(CfnRuntimeLogsMixin, jsii.invoke(self, "toXRay", []))


class CfnRuntimeUsageLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnRuntimeUsageLogs",
):
    '''Builder for CfnRuntimeLogsMixin to generate USAGE_LOGS for CfnRuntime.

    :cloudformationResource: AWS::BedrockAgentCore::Runtime
    :logType: USAGE_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
        
        cfn_runtime_usage_logs = bedrockagentcore_mixins.CfnRuntimeUsageLogs()
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toFirehose")
    def to_firehose(
        self,
        delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
    ) -> CfnRuntimeLogsMixin:
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f9772f153313ef784be338509999f9847a5e74a14a547e600eefb3d8f05c508)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast(CfnRuntimeLogsMixin, jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> CfnRuntimeLogsMixin:
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ff06af738be9bad685e555eff2b1b2e5f3e0eb1c9d6d41b2567ba7313c4a57c)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast(CfnRuntimeLogsMixin, jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> CfnRuntimeLogsMixin:
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67485711a24f84880f1990d9936820beddf311a8e4376ddabb3a5fdc7b41ca88)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast(CfnRuntimeLogsMixin, jsii.invoke(self, "toS3", [bucket]))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnWorkloadIdentityMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_resource_oauth2_return_urls": "allowedResourceOauth2ReturnUrls",
        "name": "name",
        "tags": "tags",
    },
)
class CfnWorkloadIdentityMixinProps:
    def __init__(
        self,
        *,
        allowed_resource_oauth2_return_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnWorkloadIdentityPropsMixin.

        :param allowed_resource_oauth2_return_urls: The list of allowed OAuth2 return URLs for resources associated with this workload identity.
        :param name: The name of the workload identity. The name must be unique within your account.
        :param tags: The tags for the workload identity.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-workloadidentity.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
            
            cfn_workload_identity_mixin_props = bedrockagentcore_mixins.CfnWorkloadIdentityMixinProps(
                allowed_resource_oauth2_return_urls=["allowedResourceOauth2ReturnUrls"],
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3918274f0d04cb4a03100b1c17198cf2700034d4ecbd2908f5435ffb8342304)
            check_type(argname="argument allowed_resource_oauth2_return_urls", value=allowed_resource_oauth2_return_urls, expected_type=type_hints["allowed_resource_oauth2_return_urls"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_resource_oauth2_return_urls is not None:
            self._values["allowed_resource_oauth2_return_urls"] = allowed_resource_oauth2_return_urls
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def allowed_resource_oauth2_return_urls(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of allowed OAuth2 return URLs for resources associated with this workload identity.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-workloadidentity.html#cfn-bedrockagentcore-workloadidentity-allowedresourceoauth2returnurls
        '''
        result = self._values.get("allowed_resource_oauth2_return_urls")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the workload identity.

        The name must be unique within your account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-workloadidentity.html#cfn-bedrockagentcore-workloadidentity-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags for the workload identity.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-workloadidentity.html#cfn-bedrockagentcore-workloadidentity-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWorkloadIdentityMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnWorkloadIdentityPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_bedrockagentcore.mixins.CfnWorkloadIdentityPropsMixin",
):
    '''Creates a workload identity for Amazon Bedrock AgentCore.

    A workload identity provides OAuth2-based authentication for resources associated with agent runtimes.

    For more information about using workload identities in Amazon Bedrock AgentCore, see `Managing workload identities <https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/workload-identity.html>`_ .

    See the *Properties* section below for descriptions of both the required and optional properties.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrockagentcore-workloadidentity.html
    :cloudformationResource: AWS::BedrockAgentCore::WorkloadIdentity
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_bedrockagentcore import mixins as bedrockagentcore_mixins
        
        cfn_workload_identity_props_mixin = bedrockagentcore_mixins.CfnWorkloadIdentityPropsMixin(bedrockagentcore_mixins.CfnWorkloadIdentityMixinProps(
            allowed_resource_oauth2_return_urls=["allowedResourceOauth2ReturnUrls"],
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
        props: typing.Union[CfnWorkloadIdentityMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::BedrockAgentCore::WorkloadIdentity``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78162d574d853b199c220c7a899559ee8621af37fd050c0bfe0aac997243c285)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5cd1ea9a23bb99bfbc6f7968f1b99aef6d389b8824405c3110feffb2f475131)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ec0d712bbc8d514b45609ea91c09a078e45992fe01c6a2564cbd37618eaac8d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnWorkloadIdentityMixinProps:
        return typing.cast(CfnWorkloadIdentityMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnBrowserCustomMixinProps",
    "CfnBrowserCustomPropsMixin",
    "CfnCodeInterpreterCustomMixinProps",
    "CfnCodeInterpreterCustomPropsMixin",
    "CfnGatewayApplicationLogs",
    "CfnGatewayLogsMixin",
    "CfnGatewayMixinProps",
    "CfnGatewayPropsMixin",
    "CfnGatewayTargetMixinProps",
    "CfnGatewayTargetPropsMixin",
    "CfnGatewayTraces",
    "CfnMemoryApplicationLogs",
    "CfnMemoryLogsMixin",
    "CfnMemoryMixinProps",
    "CfnMemoryPropsMixin",
    "CfnMemoryTraces",
    "CfnRuntimeApplicationLogs",
    "CfnRuntimeEndpointMixinProps",
    "CfnRuntimeEndpointPropsMixin",
    "CfnRuntimeLogsMixin",
    "CfnRuntimeMixinProps",
    "CfnRuntimePropsMixin",
    "CfnRuntimeTraces",
    "CfnRuntimeUsageLogs",
    "CfnWorkloadIdentityMixinProps",
    "CfnWorkloadIdentityPropsMixin",
]

publication.publish()

def _typecheckingstub__6b9b70b48124be49e254582f50a9aa1538acbefb906dd3217ac665c28bd940a2(
    *,
    browser_signing: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBrowserCustomPropsMixin.BrowserSigningProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    execution_role_arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    network_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBrowserCustomPropsMixin.BrowserNetworkConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    recording_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBrowserCustomPropsMixin.RecordingConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06558b710350f8e759531238d023a2fe14ee09c31f10db6b01a09a80094616f4(
    props: typing.Union[CfnBrowserCustomMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1698a0066840ace9b4aad0b05ebfce60e613215a4247e9928d29e8c65f9d132c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47200bb4582982b3460352e94cc98060cff750aa87f7f52cecdd2525333d9dde(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2723057ca2673184bfdfd04832a8499b356a8eca736330ae8e5c0160a6c177d(
    *,
    network_mode: typing.Optional[builtins.str] = None,
    vpc_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBrowserCustomPropsMixin.VpcConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53fbac5adc34bd7cf963db5456825e03933e8f7d344bd405f58bbf40357eab2c(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea2e3bf6ad31939ca40e9596a477ce81b59011ec4781ec32288eb919ef931a7e(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    s3_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBrowserCustomPropsMixin.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6db87d1e02e7aba9656052fdff62f48f2c2d112df1100d2b275b3f76db1b6bc9(
    *,
    bucket: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce09060669c510a96e651e22fbcd3f5c26d7ef68d9c1aba262608f5c55d30908(
    *,
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83b01cb25c7f75ec0c8c3a154c2882b6f4b58e0491056f259d2acb1e13ba982d(
    *,
    description: typing.Optional[builtins.str] = None,
    execution_role_arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    network_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCodeInterpreterCustomPropsMixin.CodeInterpreterNetworkConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3d40d4e9d5fa5eda6edd1151d8204fa8cba20cb9e98fd9821a55717c9b3180d(
    props: typing.Union[CfnCodeInterpreterCustomMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d913ae291a1dfefb89ad8db64d0523ad2f869fc58f92538420dd3b9241dd5fc(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d58ed371a2d11e8be90118e7839588aae50d62a64cc6c6ac561ad9c53f49a88e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd5462e15ceaaffb0e972705f51b156d382f2ad97d671ab9a2a51bc51161a098(
    *,
    network_mode: typing.Optional[builtins.str] = None,
    vpc_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCodeInterpreterCustomPropsMixin.VpcConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__098266e1c1ad82cfca97755bd93f405d511a848aab5e9e5f60cc0f0ef4a23fec(
    *,
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39848dbcff7bcfc40d1a54882028de18bd79f07358d575e2f766474c41432799(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a344d11427e4c8db554328e8e359728d32dff227185be0c431f0e06c8092f457(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__333af1943f4d576fe2f6f5471c064f69666be8e6d9f2a424aa8e4bbf0a6e6c26(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4bd5d58e42dde39c0c9f95fa42cce3112291750c9c136a8a9cf2c91b01184db(
    log_type: builtins.str,
    log_delivery: _ILogsDelivery_0d3c9e29,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8707bee110c27b8a30232ab12f1dd6fa82318218289552523e2bef7e7d1124d5(
    resource: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76cbea6936abcad9bd64780ec1b6cdaa37c3096acf1d0e0c8bb75ea40b400a88(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__560caa1f1eac070f9f9b5bc7d741a20666086f7f9cf4d5f6895d04ca519f2a6c(
    *,
    authorizer_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayPropsMixin.AuthorizerConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    authorizer_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    exception_level: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    protocol_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayPropsMixin.GatewayProtocolConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    protocol_type: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba3abd0219f9cebfb7aa16a400c731b3501a36ebc908f6f0bbc9c42af6ee25d2(
    props: typing.Union[CfnGatewayMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59c9507f233816216586022d2b682026d0c7b8ca4fb996890981947f2e798721(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d87466fb0ae037c6a9530a298ec294e3a6ba3ca2756eb53949950725893bda2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7780b5f278fbfa5dd7b19275cc49e773b3f769274712a5be92dd8a5805bb5068(
    *,
    custom_jwt_authorizer: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayPropsMixin.CustomJWTAuthorizerConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09d306a8dade079a9b37559f6cc8fc453da9f07af16ad8de7b2fe3941913faad(
    *,
    allowed_audience: typing.Optional[typing.Sequence[builtins.str]] = None,
    allowed_clients: typing.Optional[typing.Sequence[builtins.str]] = None,
    discovery_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2fa668753da52653a0818828285e7cecac19ca8a4b2a3792f38db7df43ffa69(
    *,
    mcp: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayPropsMixin.MCPGatewayConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03cc6dbf06d50f73aba296edc1a25298b46b34493386d3d157b280a61838f917(
    *,
    instructions: typing.Optional[builtins.str] = None,
    search_type: typing.Optional[builtins.str] = None,
    supported_versions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23fdb6c28327da2b10984c6b33f68cae77f1f92d611c594e46d86aca08cc5315(
    *,
    workload_identity_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19556b18f1f5cc739a0b467612594132917bcd7359c0c6cac83759803e3ac22a(
    *,
    credential_provider_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayTargetPropsMixin.CredentialProviderConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    gateway_identifier: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    target_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayTargetPropsMixin.TargetConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2ba80982a2a8945b00e3d59a8ecfc612aeb6e2cdce5212b16fcf10f9511c9c6(
    props: typing.Union[CfnGatewayTargetMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1500ade9b8a56b6041d403a141734dc27fdfae69423a391a044b933d679f0e2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07b78f3fa6f648b515e6867c55713eac6761ba88e466a95b55160f74101047a1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d6e78004d554f96bb5d69de161cbbc5cf3be027e3f39714b79c71b21208e7a7(
    *,
    credential_location: typing.Optional[builtins.str] = None,
    credential_parameter_name: typing.Optional[builtins.str] = None,
    credential_prefix: typing.Optional[builtins.str] = None,
    provider_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec0b2b1fccc4d0c00228dc8c1b9e28a5838b14ee418ed961fd608551f407321f(
    *,
    inline_payload: typing.Optional[builtins.str] = None,
    s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayTargetPropsMixin.S3ConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82aa1cdeb6038e3bb7e8b5ecb70ef1f6ae37bf0cefe5a522b2e79525a51e2309(
    *,
    credential_provider: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayTargetPropsMixin.CredentialProviderProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    credential_provider_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40f1df35e2b3ba63956b57d7e40a354571c1912ec13aeaf360c472669bb5a9a4(
    *,
    api_key_credential_provider: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayTargetPropsMixin.ApiKeyCredentialProviderProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    oauth_credential_provider: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayTargetPropsMixin.OAuthCredentialProviderProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea6b6e539afb296fe5821099c77a2f79217939d36a87a996842d39469298f848(
    *,
    lambda_arn: typing.Optional[builtins.str] = None,
    tool_schema: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayTargetPropsMixin.ToolSchemaProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f346fb508244d33d369be50d367d2a83b9b1a4956d25d91d33276637fe24465(
    *,
    endpoint: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__419e954162a5c3cfb94aecf0d79ec2f8c07e746de6ce5752a57d2392001029a1(
    *,
    lambda_: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayTargetPropsMixin.McpLambdaTargetConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    mcp_server: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayTargetPropsMixin.McpServerTargetConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    open_api_schema: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayTargetPropsMixin.ApiSchemaConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    smithy_model: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayTargetPropsMixin.ApiSchemaConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72d4b7360437986df141ba04c58398cb3ec01211102469f73d58b351e6dfec3c(
    *,
    custom_parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    provider_arn: typing.Optional[builtins.str] = None,
    scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc24e04e603b6b463649742164a309f5f6a95f3834add9fcd491900eaa0127be(
    *,
    bucket_owner_account_id: typing.Optional[builtins.str] = None,
    uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b22363fe5c38adb2c65bce1301b554933a2f0ffeb4564940fb20fd7c004d4533(
    *,
    description: typing.Optional[builtins.str] = None,
    items: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayTargetPropsMixin.SchemaDefinitionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayTargetPropsMixin.SchemaDefinitionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    required: typing.Optional[typing.Sequence[builtins.str]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca9b5efd2793f333b24c25666cfd4085fe90845f9c6c460c2b9089956e8625d2(
    *,
    mcp: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayTargetPropsMixin.McpTargetConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e7466617717d2a857adab5cde5aeef03c3bd567b818132e47eb0b05706bc211(
    *,
    description: typing.Optional[builtins.str] = None,
    input_schema: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayTargetPropsMixin.SchemaDefinitionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    output_schema: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayTargetPropsMixin.SchemaDefinitionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a3778d95b2b60099f86dfa32eb96663901bd2abb24c042bafdf6f24f8fc5824(
    *,
    inline_payload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayTargetPropsMixin.ToolDefinitionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayTargetPropsMixin.S3ConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__533a3d66a676933e8c35334e4a0fe72487242446cd039c1e22c95749f0aff244(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d97379a3829ca32dd7989e0c3e7bf095ac6da663e9085d43b47ebfd720d90674(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb93e3d5eba71dee2742932d989deb728d771b8572a33bd3b7ec42e99158f2e1(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ba1ef598af5d274cde246f021cccd97f3f9bacd72ca55bd4a2a655c256ffc02(
    log_type: builtins.str,
    log_delivery: _ILogsDelivery_0d3c9e29,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__346aafd94719a39bcd1b7e03f2d1d1c815b572bfa39b9a1b179e7c078ed109d1(
    resource: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaa046b4cb4a127be4c06542eeae1311c588dd8afeba3af29448f52bdd1c24f3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e22348ed1151811aee5c79cc9680ed4f85736851bc7dd5d08c24d8f8d06405c3(
    *,
    description: typing.Optional[builtins.str] = None,
    encryption_key_arn: typing.Optional[builtins.str] = None,
    event_expiry_duration: typing.Optional[jsii.Number] = None,
    memory_execution_role_arn: typing.Optional[builtins.str] = None,
    memory_strategies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMemoryPropsMixin.MemoryStrategyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3caaba0b37caf2f688269c0c0d1d483b8f701dfef20e3d18c5525458ee74a15b(
    props: typing.Union[CfnMemoryMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4d97507cbfb28b7c260cb5d4006a33d804cc16335bf3144d89a1503118eca5d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3e4c90a594f7890d51fde0a39714f10ec02b31ae63a09e1a3b7a0642342c545(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24b2d17307064123f93ac0ef040fdfb7e640b1dcfdefa2835a79b6584752bc8c(
    *,
    self_managed_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMemoryPropsMixin.SelfManagedConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    semantic_override: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMemoryPropsMixin.SemanticOverrideProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    summary_override: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMemoryPropsMixin.SummaryOverrideProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    user_preference_override: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMemoryPropsMixin.UserPreferenceOverrideProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1feb21d4011acfa1b5ef0427e95a8fac7dc541f8fc03dbf2ab7479f19180fe2(
    *,
    configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMemoryPropsMixin.CustomConfigurationInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    created_at: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[builtins.str] = None,
    strategy_id: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    updated_at: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__def0b4707baa8a1bb7decbe3b8b23454627a194206645117c63573d610b82658(
    *,
    payload_delivery_bucket_name: typing.Optional[builtins.str] = None,
    topic_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cfb716082b9dea2bf08f0664531cdff7d856f3b3ac17830566d4910fe48b81d(
    *,
    custom_memory_strategy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMemoryPropsMixin.CustomMemoryStrategyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    semantic_memory_strategy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMemoryPropsMixin.SemanticMemoryStrategyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    summary_memory_strategy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMemoryPropsMixin.SummaryMemoryStrategyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    user_preference_memory_strategy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMemoryPropsMixin.UserPreferenceMemoryStrategyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89bfddd3fe52dc0106411219d5a801fe3e8abaaf67f30d1a75ae6674b5495138(
    *,
    message_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2b92eacf901902387b61891ce0d3c9e9cb3632858166c9f05952f9f4cdee5e4(
    *,
    historical_context_window_size: typing.Optional[jsii.Number] = None,
    invocation_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMemoryPropsMixin.InvocationConfigurationInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    trigger_conditions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMemoryPropsMixin.TriggerConditionInputProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__958370f575a589413fad6b2f89ca0578f3074bede0d607223001545982fddfa2(
    *,
    created_at: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[builtins.str] = None,
    strategy_id: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    updated_at: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfee486b174cdb0ce3512caa083e969317d58b7915a45ba724a5c5c8196bf9bc(
    *,
    append_to_prompt: typing.Optional[builtins.str] = None,
    model_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bb9a25a8649486d7b10f2873fd62b296535f402b8273f4dcbff0aabe625a787(
    *,
    append_to_prompt: typing.Optional[builtins.str] = None,
    model_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d54203915ced368c5786dacbf41efee31c1b1ee99a1f83bfd8e36c455d6dc7c(
    *,
    consolidation: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMemoryPropsMixin.SemanticOverrideConsolidationConfigurationInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    extraction: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMemoryPropsMixin.SemanticOverrideExtractionConfigurationInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee76910e6915808a5a40e6c89a2f9052a20080effa45f504138a111fc0af229d(
    *,
    created_at: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[builtins.str] = None,
    strategy_id: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    updated_at: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4030e8c8159cd5bff567fd5d0fae6fcbf437fe0a829eab29ce8d21c518335b5(
    *,
    append_to_prompt: typing.Optional[builtins.str] = None,
    model_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dabf19b9b2f375aa6b70ddbd1a91f6280aefd8a2d4712fee71052c08921bdbd(
    *,
    consolidation: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMemoryPropsMixin.SummaryOverrideConsolidationConfigurationInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b50f80e3bce99c8272b80749996e8b2d013f674d46c0ac8cde566cb6c87fac3e(
    *,
    idle_session_timeout: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab3ab521f197380bb08749252596df1c0d2962b66d994bc0664a6028853402d1(
    *,
    token_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce9436814e9b2eb58e4c0a300580feae4d8fe8851be77e2d57fc40c4586a0d95(
    *,
    message_based_trigger: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMemoryPropsMixin.MessageBasedTriggerInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    time_based_trigger: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMemoryPropsMixin.TimeBasedTriggerInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    token_based_trigger: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMemoryPropsMixin.TokenBasedTriggerInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd938f1e1addc552b187c98501c5928d67daf3b4522aed4fa3d277aaf4b08f58(
    *,
    created_at: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[builtins.str] = None,
    strategy_id: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    updated_at: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3e7891ae977481d98b022c6fa981d06929da2731a1d393cffb6a07dcff87065(
    *,
    append_to_prompt: typing.Optional[builtins.str] = None,
    model_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f33a823344068e5781b7ae9fb9946525b289c962ed37f9c9a189863ead97445(
    *,
    append_to_prompt: typing.Optional[builtins.str] = None,
    model_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__970d9a40e86f10a8effddfad4bca4832e6abbcaa713551d2989289ca6e9d7ca0(
    *,
    consolidation: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMemoryPropsMixin.UserPreferenceOverrideConsolidationConfigurationInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    extraction: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMemoryPropsMixin.UserPreferenceOverrideExtractionConfigurationInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e26d0a37462ec4cab91d61182b516d7706c94f20b05770494a7bf34f1f340405(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baf26c8e9d08f77c0c132cfa2f9be98b4ced10acf2a9b28a07fd5fe2fdfda041(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45fb75951d996e803562ee5390a56b8736cdafd348f8d8ff221fe415d7f18306(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fca95be55db0e91c922cb6bbc9845f34ea0a6a4a7f80978df1afa5b408a56fa(
    *,
    agent_runtime_id: typing.Optional[builtins.str] = None,
    agent_runtime_version: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ee874d3104bef85b43ee825d40d603eaafbf54f8dc61fc2907d8ade76ca52cc(
    props: typing.Union[CfnRuntimeEndpointMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16d86028542760e13c15b65ad68cf023c729af4c5df5d68f8a0d6b9cb0fdfb3a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4773465d21d7c8508bcc6963db2993d7474d2845fcff819ca39155aab58d4806(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c929ee957c38ecb0579f34f4b66f6b56ef3ba96be84b3225d26fa2d3e7e422dd(
    log_type: builtins.str,
    log_delivery: _ILogsDelivery_0d3c9e29,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82afd6c4585e501a1f1696467983696efc0e5d38c4e491ede9ec6c24ec33b354(
    resource: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffb1490e81fb92d5e598d8ba05358a0857f0478d107764d976388f3f5905d0d9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01715e1fcca00084a57ca2aa5a3dfd01a87a0e2223cdc56fe01d6971c2f360cd(
    *,
    agent_runtime_artifact: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRuntimePropsMixin.AgentRuntimeArtifactProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    agent_runtime_name: typing.Optional[builtins.str] = None,
    authorizer_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRuntimePropsMixin.AuthorizerConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    environment_variables: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    lifecycle_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRuntimePropsMixin.LifecycleConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    network_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRuntimePropsMixin.NetworkConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    protocol_configuration: typing.Optional[builtins.str] = None,
    request_header_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRuntimePropsMixin.RequestHeaderConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64276faab950ce6dbaec26763aaba5dd965d13ca2f60c7ac0255651c08720e94(
    props: typing.Union[CfnRuntimeMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62ecccb04216f1309a237051d362e5003ef93e2c3a1e028e80ba19b88fb84de5(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b20506c7cbd0470cfda483fa37267236d504760db8074f7a84492811612200e6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86adfb7a7d7818c5ef49b0900cf85ab97a96df842d7b443a33bc85850b32fc29(
    *,
    code_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRuntimePropsMixin.CodeConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    container_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRuntimePropsMixin.ContainerConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__506d6f552f2c5f5d6c905940a0140795362061ed024c266b3efdbdf6d5b971d0(
    *,
    custom_jwt_authorizer: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRuntimePropsMixin.CustomJWTAuthorizerConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afcda0cc08b4e2c0242fa9ff198c5882d4aa8b0e41bea4027fca9afcbae39646(
    *,
    code: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRuntimePropsMixin.CodeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    entry_point: typing.Optional[typing.Sequence[builtins.str]] = None,
    runtime: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d9f24754c32e75093a37d60272870c0913eeaeab986337864f8e3900a80d270(
    *,
    s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRuntimePropsMixin.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a214acb52f9cd96d2ad5b32d7536d2f5f329286ab0ee3eac0fe7392435e0e4e(
    *,
    container_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a15fa6aae378e79f8a8f39db95900697caee5840f3ea82417e27499a493613c(
    *,
    allowed_audience: typing.Optional[typing.Sequence[builtins.str]] = None,
    allowed_clients: typing.Optional[typing.Sequence[builtins.str]] = None,
    discovery_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2674bdbe2f43b95380860af9d07286ec0ed037e5e490922ed56b2786453b7e40(
    *,
    idle_runtime_session_timeout: typing.Optional[jsii.Number] = None,
    max_lifetime: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4d2df4a09ed1dc31eed989d539b7fd97c052591f9ea427bad52dea599e43730(
    *,
    network_mode: typing.Optional[builtins.str] = None,
    network_mode_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRuntimePropsMixin.VpcConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__147f18a9cfa93687d5e38d02cf3c5b2f300959bed445fbad3efbad8c4442f4bb(
    *,
    request_header_allowlist: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9013961fdcf91ac32d13121234a4db53102fe8fb6e86a17b17020d10c2a3e34f(
    *,
    bucket: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
    version_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9c0a2debf066313e43615d66b3937e12b0c296c710ad8415049513bc2a42c49(
    *,
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbec5cca2900853683c64e083ea7b787422a53ddee1d9166e1b0595e804a2f47(
    *,
    workload_identity_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f9772f153313ef784be338509999f9847a5e74a14a547e600eefb3d8f05c508(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ff06af738be9bad685e555eff2b1b2e5f3e0eb1c9d6d41b2567ba7313c4a57c(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67485711a24f84880f1990d9936820beddf311a8e4376ddabb3a5fdc7b41ca88(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3918274f0d04cb4a03100b1c17198cf2700034d4ecbd2908f5435ffb8342304(
    *,
    allowed_resource_oauth2_return_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78162d574d853b199c220c7a899559ee8621af37fd050c0bfe0aac997243c285(
    props: typing.Union[CfnWorkloadIdentityMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5cd1ea9a23bb99bfbc6f7968f1b99aef6d389b8824405c3110feffb2f475131(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ec0d712bbc8d514b45609ea91c09a078e45992fe01c6a2564cbd37618eaac8d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
