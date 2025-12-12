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
    jsii_type="@aws-cdk/mixins-preview.aws_iotcoredeviceadvisor.mixins.CfnSuiteDefinitionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "suite_definition_configuration": "suiteDefinitionConfiguration",
        "tags": "tags",
    },
)
class CfnSuiteDefinitionMixinProps:
    def __init__(
        self,
        *,
        suite_definition_configuration: typing.Any = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnSuiteDefinitionPropsMixin.

        :param suite_definition_configuration: Gets the suite definition configuration.
        :param tags: Metadata that can be used to manage the the Suite Definition.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotcoredeviceadvisor-suitedefinition.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iotcoredeviceadvisor import mixins as iotcoredeviceadvisor_mixins
            
            # suite_definition_configuration: Any
            
            cfn_suite_definition_mixin_props = iotcoredeviceadvisor_mixins.CfnSuiteDefinitionMixinProps(
                suite_definition_configuration=suite_definition_configuration,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccc141b32e86a71a0d10db0930e4f6cd5a0d43fff2eda79fe0bbc11d94a7d8b3)
            check_type(argname="argument suite_definition_configuration", value=suite_definition_configuration, expected_type=type_hints["suite_definition_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if suite_definition_configuration is not None:
            self._values["suite_definition_configuration"] = suite_definition_configuration
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def suite_definition_configuration(self) -> typing.Any:
        '''Gets the suite definition configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotcoredeviceadvisor-suitedefinition.html#cfn-iotcoredeviceadvisor-suitedefinition-suitedefinitionconfiguration
        '''
        result = self._values.get("suite_definition_configuration")
        return typing.cast(typing.Any, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Metadata that can be used to manage the the Suite Definition.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotcoredeviceadvisor-suitedefinition.html#cfn-iotcoredeviceadvisor-suitedefinition-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSuiteDefinitionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSuiteDefinitionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iotcoredeviceadvisor.mixins.CfnSuiteDefinitionPropsMixin",
):
    '''Creates a Device Advisor test suite.

    Requires permission to access the `CreateSuiteDefinition <https://docs.aws.amazon.com//service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`_ action.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotcoredeviceadvisor-suitedefinition.html
    :cloudformationResource: AWS::IoTCoreDeviceAdvisor::SuiteDefinition
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iotcoredeviceadvisor import mixins as iotcoredeviceadvisor_mixins
        
        # suite_definition_configuration: Any
        
        cfn_suite_definition_props_mixin = iotcoredeviceadvisor_mixins.CfnSuiteDefinitionPropsMixin(iotcoredeviceadvisor_mixins.CfnSuiteDefinitionMixinProps(
            suite_definition_configuration=suite_definition_configuration,
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
        props: typing.Union[CfnSuiteDefinitionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IoTCoreDeviceAdvisor::SuiteDefinition``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5932b0ce3d45e2869d63b9e6b005c52ce748c86ecb0b2aec2fef8067e96acaf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__71706ec26dc90dc7f6e6869c7f0fa8a295f692749f85cef6e68246bb3d17a7f6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab23e8236977ab91fc01b34b603d5c2c5a6f3b51f9e3a92e21b22cf42d524a12)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSuiteDefinitionMixinProps:
        return typing.cast(CfnSuiteDefinitionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotcoredeviceadvisor.mixins.CfnSuiteDefinitionPropsMixin.DeviceUnderTestProperty",
        jsii_struct_bases=[],
        name_mapping={"certificate_arn": "certificateArn", "thing_arn": "thingArn"},
    )
    class DeviceUnderTestProperty:
        def __init__(
            self,
            *,
            certificate_arn: typing.Optional[builtins.str] = None,
            thing_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information of a test device.

            A thing ARN, certificate ARN or device role ARN is required.

            :param certificate_arn: Lists device's certificate ARN.
            :param thing_arn: Lists device's thing ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotcoredeviceadvisor-suitedefinition-deviceundertest.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotcoredeviceadvisor import mixins as iotcoredeviceadvisor_mixins
                
                device_under_test_property = iotcoredeviceadvisor_mixins.CfnSuiteDefinitionPropsMixin.DeviceUnderTestProperty(
                    certificate_arn="certificateArn",
                    thing_arn="thingArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__78a71bd901a7ec194c1c283c4380cd2e708ac6526364e747c273b908ec3af5ce)
                check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
                check_type(argname="argument thing_arn", value=thing_arn, expected_type=type_hints["thing_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate_arn is not None:
                self._values["certificate_arn"] = certificate_arn
            if thing_arn is not None:
                self._values["thing_arn"] = thing_arn

        @builtins.property
        def certificate_arn(self) -> typing.Optional[builtins.str]:
            '''Lists device's certificate ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotcoredeviceadvisor-suitedefinition-deviceundertest.html#cfn-iotcoredeviceadvisor-suitedefinition-deviceundertest-certificatearn
            '''
            result = self._values.get("certificate_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def thing_arn(self) -> typing.Optional[builtins.str]:
            '''Lists device's thing ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotcoredeviceadvisor-suitedefinition-deviceundertest.html#cfn-iotcoredeviceadvisor-suitedefinition-deviceundertest-thingarn
            '''
            result = self._values.get("thing_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeviceUnderTestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotcoredeviceadvisor.mixins.CfnSuiteDefinitionPropsMixin.SuiteDefinitionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "device_permission_role_arn": "devicePermissionRoleArn",
            "devices": "devices",
            "intended_for_qualification": "intendedForQualification",
            "root_group": "rootGroup",
            "suite_definition_name": "suiteDefinitionName",
        },
    )
    class SuiteDefinitionConfigurationProperty:
        def __init__(
            self,
            *,
            device_permission_role_arn: typing.Optional[builtins.str] = None,
            devices: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSuiteDefinitionPropsMixin.DeviceUnderTestProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            intended_for_qualification: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            root_group: typing.Optional[builtins.str] = None,
            suite_definition_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration of the Suite Definition. Listed below are the required elements of the ``SuiteDefinitionConfiguration`` .

            - ***devicePermissionRoleArn*** - The device permission arn.

            This is a required element.

            *Type:* String

            - ***devices*** - The list of configured devices under test. For more information on devices under test, see `DeviceUnderTest <https://docs.aws.amazon.com/iot/latest/apireference/API_iotdeviceadvisor_DeviceUnderTest.html>`_

            Not a required element.

            *Type:* List of devices under test

            - ***intendedForQualification*** - The tests intended for qualification in a suite.

            Not a required element.

            *Type:* Boolean

            - ***rootGroup*** - The test suite root group. For more information on creating and using root groups see the `Device Advisor workflow <https://docs.aws.amazon.com/iot/latest/developerguide/device-advisor-workflow.html>`_ .

            This is a required element.

            *Type:* String

            - ***suiteDefinitionName*** - The Suite Definition Configuration name.

            This is a required element.

            *Type:* String

            :param device_permission_role_arn: Gets the device permission ARN. This is a required parameter.
            :param devices: Gets the devices configured.
            :param intended_for_qualification: Gets the tests intended for qualification in a suite.
            :param root_group: Gets the test suite root group. This is a required parameter. For updating or creating the latest qualification suite, if ``intendedForQualification`` is set to true, ``rootGroup`` can be an empty string. If ``intendedForQualification`` is false, ``rootGroup`` cannot be an empty string. If ``rootGroup`` is empty, and ``intendedForQualification`` is set to true, all the qualification tests are included, and the configuration is default. For a qualification suite, the minimum length is 0, and the maximum is 2048. For a non-qualification suite, the minimum length is 1, and the maximum is 2048.
            :param suite_definition_name: Gets the suite definition name. This is a required parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotcoredeviceadvisor-suitedefinition-suitedefinitionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotcoredeviceadvisor import mixins as iotcoredeviceadvisor_mixins
                
                suite_definition_configuration_property = iotcoredeviceadvisor_mixins.CfnSuiteDefinitionPropsMixin.SuiteDefinitionConfigurationProperty(
                    device_permission_role_arn="devicePermissionRoleArn",
                    devices=[iotcoredeviceadvisor_mixins.CfnSuiteDefinitionPropsMixin.DeviceUnderTestProperty(
                        certificate_arn="certificateArn",
                        thing_arn="thingArn"
                    )],
                    intended_for_qualification=False,
                    root_group="rootGroup",
                    suite_definition_name="suiteDefinitionName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cd62ebb3dbd2f1b581f81899188b9567b7771d67db3cfd464803b8739dfed989)
                check_type(argname="argument device_permission_role_arn", value=device_permission_role_arn, expected_type=type_hints["device_permission_role_arn"])
                check_type(argname="argument devices", value=devices, expected_type=type_hints["devices"])
                check_type(argname="argument intended_for_qualification", value=intended_for_qualification, expected_type=type_hints["intended_for_qualification"])
                check_type(argname="argument root_group", value=root_group, expected_type=type_hints["root_group"])
                check_type(argname="argument suite_definition_name", value=suite_definition_name, expected_type=type_hints["suite_definition_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if device_permission_role_arn is not None:
                self._values["device_permission_role_arn"] = device_permission_role_arn
            if devices is not None:
                self._values["devices"] = devices
            if intended_for_qualification is not None:
                self._values["intended_for_qualification"] = intended_for_qualification
            if root_group is not None:
                self._values["root_group"] = root_group
            if suite_definition_name is not None:
                self._values["suite_definition_name"] = suite_definition_name

        @builtins.property
        def device_permission_role_arn(self) -> typing.Optional[builtins.str]:
            '''Gets the device permission ARN.

            This is a required parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotcoredeviceadvisor-suitedefinition-suitedefinitionconfiguration.html#cfn-iotcoredeviceadvisor-suitedefinition-suitedefinitionconfiguration-devicepermissionrolearn
            '''
            result = self._values.get("device_permission_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def devices(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSuiteDefinitionPropsMixin.DeviceUnderTestProperty"]]]]:
            '''Gets the devices configured.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotcoredeviceadvisor-suitedefinition-suitedefinitionconfiguration.html#cfn-iotcoredeviceadvisor-suitedefinition-suitedefinitionconfiguration-devices
            '''
            result = self._values.get("devices")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSuiteDefinitionPropsMixin.DeviceUnderTestProperty"]]]], result)

        @builtins.property
        def intended_for_qualification(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Gets the tests intended for qualification in a suite.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotcoredeviceadvisor-suitedefinition-suitedefinitionconfiguration.html#cfn-iotcoredeviceadvisor-suitedefinition-suitedefinitionconfiguration-intendedforqualification
            '''
            result = self._values.get("intended_for_qualification")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def root_group(self) -> typing.Optional[builtins.str]:
            '''Gets the test suite root group.

            This is a required parameter. For updating or creating the latest qualification suite, if ``intendedForQualification`` is set to true, ``rootGroup`` can be an empty string. If ``intendedForQualification`` is false, ``rootGroup`` cannot be an empty string. If ``rootGroup`` is empty, and ``intendedForQualification`` is set to true, all the qualification tests are included, and the configuration is default.

            For a qualification suite, the minimum length is 0, and the maximum is 2048. For a non-qualification suite, the minimum length is 1, and the maximum is 2048.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotcoredeviceadvisor-suitedefinition-suitedefinitionconfiguration.html#cfn-iotcoredeviceadvisor-suitedefinition-suitedefinitionconfiguration-rootgroup
            '''
            result = self._values.get("root_group")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def suite_definition_name(self) -> typing.Optional[builtins.str]:
            '''Gets the suite definition name.

            This is a required parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotcoredeviceadvisor-suitedefinition-suitedefinitionconfiguration.html#cfn-iotcoredeviceadvisor-suitedefinition-suitedefinitionconfiguration-suitedefinitionname
            '''
            result = self._values.get("suite_definition_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SuiteDefinitionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnSuiteDefinitionMixinProps",
    "CfnSuiteDefinitionPropsMixin",
]

publication.publish()

def _typecheckingstub__ccc141b32e86a71a0d10db0930e4f6cd5a0d43fff2eda79fe0bbc11d94a7d8b3(
    *,
    suite_definition_configuration: typing.Any = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5932b0ce3d45e2869d63b9e6b005c52ce748c86ecb0b2aec2fef8067e96acaf(
    props: typing.Union[CfnSuiteDefinitionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71706ec26dc90dc7f6e6869c7f0fa8a295f692749f85cef6e68246bb3d17a7f6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab23e8236977ab91fc01b34b603d5c2c5a6f3b51f9e3a92e21b22cf42d524a12(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78a71bd901a7ec194c1c283c4380cd2e708ac6526364e747c273b908ec3af5ce(
    *,
    certificate_arn: typing.Optional[builtins.str] = None,
    thing_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd62ebb3dbd2f1b581f81899188b9567b7771d67db3cfd464803b8739dfed989(
    *,
    device_permission_role_arn: typing.Optional[builtins.str] = None,
    devices: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSuiteDefinitionPropsMixin.DeviceUnderTestProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    intended_for_qualification: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    root_group: typing.Optional[builtins.str] = None,
    suite_definition_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
