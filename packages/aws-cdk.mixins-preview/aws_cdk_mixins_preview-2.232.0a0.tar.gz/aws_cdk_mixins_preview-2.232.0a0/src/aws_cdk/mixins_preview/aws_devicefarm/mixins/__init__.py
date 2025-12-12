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
    jsii_type="@aws-cdk/mixins-preview.aws_devicefarm.mixins.CfnDevicePoolMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "max_devices": "maxDevices",
        "name": "name",
        "project_arn": "projectArn",
        "rules": "rules",
        "tags": "tags",
    },
)
class CfnDevicePoolMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        max_devices: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        project_arn: typing.Optional[builtins.str] = None,
        rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDevicePoolPropsMixin.RuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDevicePoolPropsMixin.

        :param description: The device pool's description.
        :param max_devices: The number of devices that Device Farm can add to your device pool. Device Farm adds devices that are available and meet the criteria that you assign for the ``rules`` parameter. Depending on how many devices meet these constraints, your device pool might contain fewer devices than the value for this parameter. By specifying the maximum number of devices, you can control the costs that you incur by running tests.
        :param name: The device pool's name.
        :param project_arn: The ARN of the project for the device pool.
        :param rules: The device pool's rules.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ in the *guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-devicepool.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_devicefarm import mixins as devicefarm_mixins
            
            cfn_device_pool_mixin_props = devicefarm_mixins.CfnDevicePoolMixinProps(
                description="description",
                max_devices=123,
                name="name",
                project_arn="projectArn",
                rules=[devicefarm_mixins.CfnDevicePoolPropsMixin.RuleProperty(
                    attribute="attribute",
                    operator="operator",
                    value="value"
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85bfbf20cea680dbc2bd0a1b5e1807a17dcc5692fb0fbd5c1665e7e738d0f9e6)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument max_devices", value=max_devices, expected_type=type_hints["max_devices"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument project_arn", value=project_arn, expected_type=type_hints["project_arn"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if max_devices is not None:
            self._values["max_devices"] = max_devices
        if name is not None:
            self._values["name"] = name
        if project_arn is not None:
            self._values["project_arn"] = project_arn
        if rules is not None:
            self._values["rules"] = rules
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The device pool's description.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-devicepool.html#cfn-devicefarm-devicepool-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_devices(self) -> typing.Optional[jsii.Number]:
        '''The number of devices that Device Farm can add to your device pool.

        Device Farm adds devices that are available and meet the criteria that you assign for the ``rules`` parameter. Depending on how many devices meet these constraints, your device pool might contain fewer devices than the value for this parameter.

        By specifying the maximum number of devices, you can control the costs that you incur by running tests.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-devicepool.html#cfn-devicefarm-devicepool-maxdevices
        '''
        result = self._values.get("max_devices")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The device pool's name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-devicepool.html#cfn-devicefarm-devicepool-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the project for the device pool.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-devicepool.html#cfn-devicefarm-devicepool-projectarn
        '''
        result = self._values.get("project_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rules(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDevicePoolPropsMixin.RuleProperty"]]]]:
        '''The device pool's rules.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-devicepool.html#cfn-devicefarm-devicepool-rules
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDevicePoolPropsMixin.RuleProperty"]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ in the *guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-devicepool.html#cfn-devicefarm-devicepool-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDevicePoolMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDevicePoolPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_devicefarm.mixins.CfnDevicePoolPropsMixin",
):
    '''Represents a request to the create device pool operation.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-devicepool.html
    :cloudformationResource: AWS::DeviceFarm::DevicePool
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_devicefarm import mixins as devicefarm_mixins
        
        cfn_device_pool_props_mixin = devicefarm_mixins.CfnDevicePoolPropsMixin(devicefarm_mixins.CfnDevicePoolMixinProps(
            description="description",
            max_devices=123,
            name="name",
            project_arn="projectArn",
            rules=[devicefarm_mixins.CfnDevicePoolPropsMixin.RuleProperty(
                attribute="attribute",
                operator="operator",
                value="value"
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
        props: typing.Union[CfnDevicePoolMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DeviceFarm::DevicePool``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea1d1df1c7b7fbb7b675116e780553a53935b60a9cebee4f5b88bbe3c00967bf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__13f08f282119af0ada25eaa1390bd3777770c87d0a6677741e260732caeab3bb)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9041d3c2b632dde085ecca78efc2e7daacb2db92d1e52c56d0909e15c84207e6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDevicePoolMixinProps:
        return typing.cast(CfnDevicePoolMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_devicefarm.mixins.CfnDevicePoolPropsMixin.RuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attribute": "attribute",
            "operator": "operator",
            "value": "value",
        },
    )
    class RuleProperty:
        def __init__(
            self,
            *,
            attribute: typing.Optional[builtins.str] = None,
            operator: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents a condition for a device pool.

            :param attribute: The rule's stringified attribute. For example, specify the value as ``"\\"abc\\""`` . The supported operators for each attribute are provided in the following list. - **APPIUM_VERSION** - The Appium version for the test. Supported operators: ``CONTAINS`` - **ARN** - The Amazon Resource Name (ARN) of the device (for example, ``arn:aws:devicefarm:us-west-2::device:12345Example`` . Supported operators: ``EQUALS`` , ``IN`` , ``NOT_IN`` - **AVAILABILITY** - The current availability of the device. Valid values are AVAILABLE, HIGHLY_AVAILABLE, BUSY, or TEMPORARY_NOT_AVAILABLE. Supported operators: ``EQUALS`` - **FLEET_TYPE** - The fleet type. Valid values are PUBLIC or PRIVATE. Supported operators: ``EQUALS`` - **FORM_FACTOR** - The device form factor. Valid values are PHONE or TABLET. Supported operators: ``EQUALS`` , ``IN`` , ``NOT_IN`` - **INSTANCE_ARN** - The Amazon Resource Name (ARN) of the device instance. Supported operators: ``IN`` , ``NOT_IN`` - **INSTANCE_LABELS** - The label of the device instance. Supported operators: ``CONTAINS`` - **MANUFACTURER** - The device manufacturer (for example, Apple). Supported operators: ``EQUALS`` , ``IN`` , ``NOT_IN`` - **MODEL** - The device model, such as Apple iPad Air 2 or Google Pixel. Supported operators: ``CONTAINS`` , ``EQUALS`` , ``IN`` , ``NOT_IN`` - **OS_VERSION** - The operating system version (for example, 10.3.2). Supported operators: ``EQUALS`` , ``GREATER_THAN`` , ``GREATER_THAN_OR_EQUALS`` , ``IN`` , ``LESS_THAN`` , ``LESS_THAN_OR_EQUALS`` , ``NOT_IN`` - **PLATFORM** - The device platform. Valid values are ANDROID or IOS. Supported operators: ``EQUALS`` , ``IN`` , ``NOT_IN`` - **REMOTE_ACCESS_ENABLED** - Whether the device is enabled for remote access. Valid values are TRUE or FALSE. Supported operators: ``EQUALS`` - **REMOTE_DEBUG_ENABLED** - Whether the device is enabled for remote debugging. Valid values are TRUE or FALSE. Supported operators: ``EQUALS`` Because remote debugging is `no longer supported <https://docs.aws.amazon.com/devicefarm/latest/developerguide/history.html>`_ , this filter is ignored.
            :param operator: Specifies how Device Farm compares the rule's attribute to the value. For the operators that are supported by each attribute, see the attribute descriptions.
            :param value: The rule's value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devicefarm-devicepool-rule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_devicefarm import mixins as devicefarm_mixins
                
                rule_property = devicefarm_mixins.CfnDevicePoolPropsMixin.RuleProperty(
                    attribute="attribute",
                    operator="operator",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fd91f9e3c68e337ea2010ebbf1cb09360380234e87120dcde0dc42789bb6dd47)
                check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
                check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attribute is not None:
                self._values["attribute"] = attribute
            if operator is not None:
                self._values["operator"] = operator
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def attribute(self) -> typing.Optional[builtins.str]:
            '''The rule's stringified attribute. For example, specify the value as ``"\\"abc\\""`` .

            The supported operators for each attribute are provided in the following list.

            - **APPIUM_VERSION** - The Appium version for the test.

            Supported operators: ``CONTAINS``

            - **ARN** - The Amazon Resource Name (ARN) of the device (for example, ``arn:aws:devicefarm:us-west-2::device:12345Example`` .

            Supported operators: ``EQUALS`` , ``IN`` , ``NOT_IN``

            - **AVAILABILITY** - The current availability of the device. Valid values are AVAILABLE, HIGHLY_AVAILABLE, BUSY, or TEMPORARY_NOT_AVAILABLE.

            Supported operators: ``EQUALS``

            - **FLEET_TYPE** - The fleet type. Valid values are PUBLIC or PRIVATE.

            Supported operators: ``EQUALS``

            - **FORM_FACTOR** - The device form factor. Valid values are PHONE or TABLET.

            Supported operators: ``EQUALS`` , ``IN`` , ``NOT_IN``

            - **INSTANCE_ARN** - The Amazon Resource Name (ARN) of the device instance.

            Supported operators: ``IN`` , ``NOT_IN``

            - **INSTANCE_LABELS** - The label of the device instance.

            Supported operators: ``CONTAINS``

            - **MANUFACTURER** - The device manufacturer (for example, Apple).

            Supported operators: ``EQUALS`` , ``IN`` , ``NOT_IN``

            - **MODEL** - The device model, such as Apple iPad Air 2 or Google Pixel.

            Supported operators: ``CONTAINS`` , ``EQUALS`` , ``IN`` , ``NOT_IN``

            - **OS_VERSION** - The operating system version (for example, 10.3.2).

            Supported operators: ``EQUALS`` , ``GREATER_THAN`` , ``GREATER_THAN_OR_EQUALS`` , ``IN`` , ``LESS_THAN`` , ``LESS_THAN_OR_EQUALS`` , ``NOT_IN``

            - **PLATFORM** - The device platform. Valid values are ANDROID or IOS.

            Supported operators: ``EQUALS`` , ``IN`` , ``NOT_IN``

            - **REMOTE_ACCESS_ENABLED** - Whether the device is enabled for remote access. Valid values are TRUE or FALSE.

            Supported operators: ``EQUALS``

            - **REMOTE_DEBUG_ENABLED** - Whether the device is enabled for remote debugging. Valid values are TRUE or FALSE.

            Supported operators: ``EQUALS``

            Because remote debugging is `no longer supported <https://docs.aws.amazon.com/devicefarm/latest/developerguide/history.html>`_ , this filter is ignored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devicefarm-devicepool-rule.html#cfn-devicefarm-devicepool-rule-attribute
            '''
            result = self._values.get("attribute")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def operator(self) -> typing.Optional[builtins.str]:
            '''Specifies how Device Farm compares the rule's attribute to the value.

            For the operators that are supported by each attribute, see the attribute descriptions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devicefarm-devicepool-rule.html#cfn-devicefarm-devicepool-rule-operator
            '''
            result = self._values.get("operator")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The rule's value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devicefarm-devicepool-rule.html#cfn-devicefarm-devicepool-rule-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_devicefarm.mixins.CfnInstanceProfileMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "exclude_app_packages_from_cleanup": "excludeAppPackagesFromCleanup",
        "name": "name",
        "package_cleanup": "packageCleanup",
        "reboot_after_use": "rebootAfterUse",
        "tags": "tags",
    },
)
class CfnInstanceProfileMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        exclude_app_packages_from_cleanup: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        package_cleanup: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        reboot_after_use: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnInstanceProfilePropsMixin.

        :param description: The description of the instance profile.
        :param exclude_app_packages_from_cleanup: An array of strings containing the list of app packages that should not be cleaned up from the device after a test run completes. The list of packages is considered only if you set ``packageCleanup`` to ``true`` .
        :param name: The name of the instance profile.
        :param package_cleanup: When set to ``true`` , Device Farm removes app packages after a test run. The default value is ``false`` for private devices.
        :param reboot_after_use: When set to ``true`` , Device Farm reboots the instance after a test run. The default value is ``true`` .
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ in the *guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-instanceprofile.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_devicefarm import mixins as devicefarm_mixins
            
            cfn_instance_profile_mixin_props = devicefarm_mixins.CfnInstanceProfileMixinProps(
                description="description",
                exclude_app_packages_from_cleanup=["excludeAppPackagesFromCleanup"],
                name="name",
                package_cleanup=False,
                reboot_after_use=False,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__515bed5647f239f5ae46ac45103d4e696806be95a69a3297c6b4957498c48eab)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument exclude_app_packages_from_cleanup", value=exclude_app_packages_from_cleanup, expected_type=type_hints["exclude_app_packages_from_cleanup"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument package_cleanup", value=package_cleanup, expected_type=type_hints["package_cleanup"])
            check_type(argname="argument reboot_after_use", value=reboot_after_use, expected_type=type_hints["reboot_after_use"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if exclude_app_packages_from_cleanup is not None:
            self._values["exclude_app_packages_from_cleanup"] = exclude_app_packages_from_cleanup
        if name is not None:
            self._values["name"] = name
        if package_cleanup is not None:
            self._values["package_cleanup"] = package_cleanup
        if reboot_after_use is not None:
            self._values["reboot_after_use"] = reboot_after_use
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the instance profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-instanceprofile.html#cfn-devicefarm-instanceprofile-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exclude_app_packages_from_cleanup(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of strings containing the list of app packages that should not be cleaned up from the device after a test run completes.

        The list of packages is considered only if you set ``packageCleanup`` to ``true`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-instanceprofile.html#cfn-devicefarm-instanceprofile-excludeapppackagesfromcleanup
        '''
        result = self._values.get("exclude_app_packages_from_cleanup")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the instance profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-instanceprofile.html#cfn-devicefarm-instanceprofile-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def package_cleanup(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''When set to ``true`` , Device Farm removes app packages after a test run.

        The default value is ``false`` for private devices.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-instanceprofile.html#cfn-devicefarm-instanceprofile-packagecleanup
        '''
        result = self._values.get("package_cleanup")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def reboot_after_use(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''When set to ``true`` , Device Farm reboots the instance after a test run.

        The default value is ``true`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-instanceprofile.html#cfn-devicefarm-instanceprofile-rebootafteruse
        '''
        result = self._values.get("reboot_after_use")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ in the *guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-instanceprofile.html#cfn-devicefarm-instanceprofile-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnInstanceProfileMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnInstanceProfilePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_devicefarm.mixins.CfnInstanceProfilePropsMixin",
):
    '''Creates a profile that can be applied to one or more private fleet device instances.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-instanceprofile.html
    :cloudformationResource: AWS::DeviceFarm::InstanceProfile
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_devicefarm import mixins as devicefarm_mixins
        
        cfn_instance_profile_props_mixin = devicefarm_mixins.CfnInstanceProfilePropsMixin(devicefarm_mixins.CfnInstanceProfileMixinProps(
            description="description",
            exclude_app_packages_from_cleanup=["excludeAppPackagesFromCleanup"],
            name="name",
            package_cleanup=False,
            reboot_after_use=False,
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
        props: typing.Union[CfnInstanceProfileMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DeviceFarm::InstanceProfile``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ad8fb972d47a6c35a32df5ef42480e72de42a30d1af52bce61e835944fd220b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__af3b6c83dfe03f51351bccd00065523cc4b4e2931e155556d62499e30b4f9e09)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac01f52897ecd5f80a303209eaee73d000a4817ed2bcd0be4124c5b41cc36408)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnInstanceProfileMixinProps:
        return typing.cast(CfnInstanceProfileMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_devicefarm.mixins.CfnNetworkProfileMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "downlink_bandwidth_bits": "downlinkBandwidthBits",
        "downlink_delay_ms": "downlinkDelayMs",
        "downlink_jitter_ms": "downlinkJitterMs",
        "downlink_loss_percent": "downlinkLossPercent",
        "name": "name",
        "project_arn": "projectArn",
        "tags": "tags",
        "uplink_bandwidth_bits": "uplinkBandwidthBits",
        "uplink_delay_ms": "uplinkDelayMs",
        "uplink_jitter_ms": "uplinkJitterMs",
        "uplink_loss_percent": "uplinkLossPercent",
    },
)
class CfnNetworkProfileMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        downlink_bandwidth_bits: typing.Optional[jsii.Number] = None,
        downlink_delay_ms: typing.Optional[jsii.Number] = None,
        downlink_jitter_ms: typing.Optional[jsii.Number] = None,
        downlink_loss_percent: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        project_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        uplink_bandwidth_bits: typing.Optional[jsii.Number] = None,
        uplink_delay_ms: typing.Optional[jsii.Number] = None,
        uplink_jitter_ms: typing.Optional[jsii.Number] = None,
        uplink_loss_percent: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties for CfnNetworkProfilePropsMixin.

        :param description: The description of the network profile.
        :param downlink_bandwidth_bits: The data throughput rate in bits per second, as an integer from 0 to 104857600.
        :param downlink_delay_ms: Delay time for all packets to destination in milliseconds as an integer from 0 to 2000.
        :param downlink_jitter_ms: Time variation in the delay of received packets in milliseconds as an integer from 0 to 2000.
        :param downlink_loss_percent: Proportion of received packets that fail to arrive from 0 to 100 percent.
        :param name: The name of the network profile.
        :param project_arn: The Amazon Resource Name (ARN) of the specified project.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ in the *guide* .
        :param uplink_bandwidth_bits: The data throughput rate in bits per second, as an integer from 0 to 104857600.
        :param uplink_delay_ms: Delay time for all packets to destination in milliseconds as an integer from 0 to 2000.
        :param uplink_jitter_ms: Time variation in the delay of received packets in milliseconds as an integer from 0 to 2000.
        :param uplink_loss_percent: Proportion of transmitted packets that fail to arrive from 0 to 100 percent.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-networkprofile.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_devicefarm import mixins as devicefarm_mixins
            
            cfn_network_profile_mixin_props = devicefarm_mixins.CfnNetworkProfileMixinProps(
                description="description",
                downlink_bandwidth_bits=123,
                downlink_delay_ms=123,
                downlink_jitter_ms=123,
                downlink_loss_percent=123,
                name="name",
                project_arn="projectArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                uplink_bandwidth_bits=123,
                uplink_delay_ms=123,
                uplink_jitter_ms=123,
                uplink_loss_percent=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__055014c2a840471080d8a42b0f71ff3b62be9b5d5acc1eb35b80472c6954ac15)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument downlink_bandwidth_bits", value=downlink_bandwidth_bits, expected_type=type_hints["downlink_bandwidth_bits"])
            check_type(argname="argument downlink_delay_ms", value=downlink_delay_ms, expected_type=type_hints["downlink_delay_ms"])
            check_type(argname="argument downlink_jitter_ms", value=downlink_jitter_ms, expected_type=type_hints["downlink_jitter_ms"])
            check_type(argname="argument downlink_loss_percent", value=downlink_loss_percent, expected_type=type_hints["downlink_loss_percent"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument project_arn", value=project_arn, expected_type=type_hints["project_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument uplink_bandwidth_bits", value=uplink_bandwidth_bits, expected_type=type_hints["uplink_bandwidth_bits"])
            check_type(argname="argument uplink_delay_ms", value=uplink_delay_ms, expected_type=type_hints["uplink_delay_ms"])
            check_type(argname="argument uplink_jitter_ms", value=uplink_jitter_ms, expected_type=type_hints["uplink_jitter_ms"])
            check_type(argname="argument uplink_loss_percent", value=uplink_loss_percent, expected_type=type_hints["uplink_loss_percent"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if downlink_bandwidth_bits is not None:
            self._values["downlink_bandwidth_bits"] = downlink_bandwidth_bits
        if downlink_delay_ms is not None:
            self._values["downlink_delay_ms"] = downlink_delay_ms
        if downlink_jitter_ms is not None:
            self._values["downlink_jitter_ms"] = downlink_jitter_ms
        if downlink_loss_percent is not None:
            self._values["downlink_loss_percent"] = downlink_loss_percent
        if name is not None:
            self._values["name"] = name
        if project_arn is not None:
            self._values["project_arn"] = project_arn
        if tags is not None:
            self._values["tags"] = tags
        if uplink_bandwidth_bits is not None:
            self._values["uplink_bandwidth_bits"] = uplink_bandwidth_bits
        if uplink_delay_ms is not None:
            self._values["uplink_delay_ms"] = uplink_delay_ms
        if uplink_jitter_ms is not None:
            self._values["uplink_jitter_ms"] = uplink_jitter_ms
        if uplink_loss_percent is not None:
            self._values["uplink_loss_percent"] = uplink_loss_percent

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the network profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-networkprofile.html#cfn-devicefarm-networkprofile-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def downlink_bandwidth_bits(self) -> typing.Optional[jsii.Number]:
        '''The data throughput rate in bits per second, as an integer from 0 to 104857600.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-networkprofile.html#cfn-devicefarm-networkprofile-downlinkbandwidthbits
        '''
        result = self._values.get("downlink_bandwidth_bits")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def downlink_delay_ms(self) -> typing.Optional[jsii.Number]:
        '''Delay time for all packets to destination in milliseconds as an integer from 0 to 2000.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-networkprofile.html#cfn-devicefarm-networkprofile-downlinkdelayms
        '''
        result = self._values.get("downlink_delay_ms")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def downlink_jitter_ms(self) -> typing.Optional[jsii.Number]:
        '''Time variation in the delay of received packets in milliseconds as an integer from 0 to 2000.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-networkprofile.html#cfn-devicefarm-networkprofile-downlinkjitterms
        '''
        result = self._values.get("downlink_jitter_ms")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def downlink_loss_percent(self) -> typing.Optional[jsii.Number]:
        '''Proportion of received packets that fail to arrive from 0 to 100 percent.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-networkprofile.html#cfn-devicefarm-networkprofile-downlinklosspercent
        '''
        result = self._values.get("downlink_loss_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the network profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-networkprofile.html#cfn-devicefarm-networkprofile-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the specified project.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-networkprofile.html#cfn-devicefarm-networkprofile-projectarn
        '''
        result = self._values.get("project_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ in the *guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-networkprofile.html#cfn-devicefarm-networkprofile-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def uplink_bandwidth_bits(self) -> typing.Optional[jsii.Number]:
        '''The data throughput rate in bits per second, as an integer from 0 to 104857600.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-networkprofile.html#cfn-devicefarm-networkprofile-uplinkbandwidthbits
        '''
        result = self._values.get("uplink_bandwidth_bits")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def uplink_delay_ms(self) -> typing.Optional[jsii.Number]:
        '''Delay time for all packets to destination in milliseconds as an integer from 0 to 2000.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-networkprofile.html#cfn-devicefarm-networkprofile-uplinkdelayms
        '''
        result = self._values.get("uplink_delay_ms")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def uplink_jitter_ms(self) -> typing.Optional[jsii.Number]:
        '''Time variation in the delay of received packets in milliseconds as an integer from 0 to 2000.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-networkprofile.html#cfn-devicefarm-networkprofile-uplinkjitterms
        '''
        result = self._values.get("uplink_jitter_ms")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def uplink_loss_percent(self) -> typing.Optional[jsii.Number]:
        '''Proportion of transmitted packets that fail to arrive from 0 to 100 percent.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-networkprofile.html#cfn-devicefarm-networkprofile-uplinklosspercent
        '''
        result = self._values.get("uplink_loss_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnNetworkProfileMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnNetworkProfilePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_devicefarm.mixins.CfnNetworkProfilePropsMixin",
):
    '''Creates a network profile.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-networkprofile.html
    :cloudformationResource: AWS::DeviceFarm::NetworkProfile
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_devicefarm import mixins as devicefarm_mixins
        
        cfn_network_profile_props_mixin = devicefarm_mixins.CfnNetworkProfilePropsMixin(devicefarm_mixins.CfnNetworkProfileMixinProps(
            description="description",
            downlink_bandwidth_bits=123,
            downlink_delay_ms=123,
            downlink_jitter_ms=123,
            downlink_loss_percent=123,
            name="name",
            project_arn="projectArn",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            uplink_bandwidth_bits=123,
            uplink_delay_ms=123,
            uplink_jitter_ms=123,
            uplink_loss_percent=123
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnNetworkProfileMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DeviceFarm::NetworkProfile``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c86f0a00444a656a2fa173d53f6e3502767cff31637991d0133f2c52bc6052e2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1967b335619e4d742618d183030f57dc3d25c6e769874c5c2c902eeb38dc06f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f01e2463a893db931c60ccb0a9fd0854307fa916db219c2bea52d2732bd00ea)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnNetworkProfileMixinProps:
        return typing.cast(CfnNetworkProfileMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_devicefarm.mixins.CfnProjectMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "default_job_timeout_minutes": "defaultJobTimeoutMinutes",
        "name": "name",
        "tags": "tags",
        "vpc_config": "vpcConfig",
    },
)
class CfnProjectMixinProps:
    def __init__(
        self,
        *,
        default_job_timeout_minutes: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProjectPropsMixin.VpcConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnProjectPropsMixin.

        :param default_job_timeout_minutes: Sets the execution timeout value (in minutes) for a project. All test runs in this project use the specified execution timeout value unless overridden when scheduling a run.
        :param name: The project's name.
        :param tags: The tags to add to the resource. A tag is an array of key-value pairs. Tag keys can have a maximum character length of 128 characters. Tag values can have a maximum length of 256 characters.
        :param vpc_config: The VPC security groups and subnets that are attached to a project.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-project.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_devicefarm import mixins as devicefarm_mixins
            
            cfn_project_mixin_props = devicefarm_mixins.CfnProjectMixinProps(
                default_job_timeout_minutes=123,
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vpc_config=devicefarm_mixins.CfnProjectPropsMixin.VpcConfigProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"],
                    vpc_id="vpcId"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fde6c0a8d74f3e557776cd1acf460530e0ff2b9dbc19f21f7841f7dd0cdbe352)
            check_type(argname="argument default_job_timeout_minutes", value=default_job_timeout_minutes, expected_type=type_hints["default_job_timeout_minutes"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc_config", value=vpc_config, expected_type=type_hints["vpc_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default_job_timeout_minutes is not None:
            self._values["default_job_timeout_minutes"] = default_job_timeout_minutes
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags
        if vpc_config is not None:
            self._values["vpc_config"] = vpc_config

    @builtins.property
    def default_job_timeout_minutes(self) -> typing.Optional[jsii.Number]:
        '''Sets the execution timeout value (in minutes) for a project.

        All test runs in this project use the specified execution timeout value unless overridden when scheduling a run.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-project.html#cfn-devicefarm-project-defaultjobtimeoutminutes
        '''
        result = self._values.get("default_job_timeout_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The project's name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-project.html#cfn-devicefarm-project-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags to add to the resource.

        A tag is an array of key-value pairs. Tag keys can have a maximum character length of 128 characters. Tag values can have a maximum length of 256 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-project.html#cfn-devicefarm-project-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def vpc_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.VpcConfigProperty"]]:
        '''The VPC security groups and subnets that are attached to a project.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-project.html#cfn-devicefarm-project-vpcconfig
        '''
        result = self._values.get("vpc_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.VpcConfigProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnProjectMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnProjectPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_devicefarm.mixins.CfnProjectPropsMixin",
):
    '''Creates a project.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-project.html
    :cloudformationResource: AWS::DeviceFarm::Project
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_devicefarm import mixins as devicefarm_mixins
        
        cfn_project_props_mixin = devicefarm_mixins.CfnProjectPropsMixin(devicefarm_mixins.CfnProjectMixinProps(
            default_job_timeout_minutes=123,
            name="name",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            vpc_config=devicefarm_mixins.CfnProjectPropsMixin.VpcConfigProperty(
                security_group_ids=["securityGroupIds"],
                subnet_ids=["subnetIds"],
                vpc_id="vpcId"
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnProjectMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DeviceFarm::Project``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af52de51658b1b2000b6e009eae5e7668d5983ce4a09e17919686e92ff85f267)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7519d97163809f0973eb6a2ea021653ef2614d99261f609d8a1045943b934168)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b40d6f76d5be968718089fec5679b5ded8c43bbeacd0ab79d96893254804825)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnProjectMixinProps:
        return typing.cast(CfnProjectMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_devicefarm.mixins.CfnProjectPropsMixin.VpcConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
            "vpc_id": "vpcId",
        },
    )
    class VpcConfigProperty:
        def __init__(
            self,
            *,
            security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            vpc_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The VPC security groups and subnets that are attached to a project.

            :param security_group_ids: A list of VPC security group IDs. A security group allows inbound traffic from network interfaces (and their associated instances) that are assigned to the same security group. See `Security groups <https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html>`_ in the *Amazon Virtual Private Cloud user guide* .
            :param subnet_ids: A subnet is a range of IP addresses in your VPC. You can launch Amazon resources, such as EC2 instances, into a specific subnet. When you create a subnet, you specify the IPv4 CIDR block for the subnet, which is a subset of the VPC CIDR block. See `VPCs and subnets <https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html>`_ in the *Amazon Virtual Private Cloud user guide* .
            :param vpc_id: A list of VPC IDs. Each VPC is given a unique ID upon creation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devicefarm-project-vpcconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_devicefarm import mixins as devicefarm_mixins
                
                vpc_config_property = devicefarm_mixins.CfnProjectPropsMixin.VpcConfigProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"],
                    vpc_id="vpcId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__34e35903fb738d00326bef7fc9797d7a579fa49de0a7fd2ba7b75d3d395cab1a)
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
                check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
                check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnet_ids is not None:
                self._values["subnet_ids"] = subnet_ids
            if vpc_id is not None:
                self._values["vpc_id"] = vpc_id

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of VPC security group IDs.

            A security group allows inbound traffic from network interfaces (and their associated instances) that are assigned to the same security group. See `Security groups <https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html>`_ in the *Amazon Virtual Private Cloud user guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devicefarm-project-vpcconfig.html#cfn-devicefarm-project-vpcconfig-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A subnet is a range of IP addresses in your VPC.

            You can launch Amazon resources, such as EC2 instances, into a specific subnet. When you create a subnet, you specify the IPv4 CIDR block for the subnet, which is a subset of the VPC CIDR block. See `VPCs and subnets <https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html>`_ in the *Amazon Virtual Private Cloud user guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devicefarm-project-vpcconfig.html#cfn-devicefarm-project-vpcconfig-subnetids
            '''
            result = self._values.get("subnet_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def vpc_id(self) -> typing.Optional[builtins.str]:
            '''A list of VPC IDs.

            Each VPC is given a unique ID upon creation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devicefarm-project-vpcconfig.html#cfn-devicefarm-project-vpcconfig-vpcid
            '''
            result = self._values.get("vpc_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_devicefarm.mixins.CfnTestGridProjectMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "name": "name",
        "tags": "tags",
        "vpc_config": "vpcConfig",
    },
)
class CfnTestGridProjectMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTestGridProjectPropsMixin.VpcConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnTestGridProjectPropsMixin.

        :param description: A human-readable description for the project.
        :param name: A human-readable name for the project.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ in the *guide* .
        :param vpc_config: The VPC security groups and subnets that are attached to a project.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-testgridproject.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_devicefarm import mixins as devicefarm_mixins
            
            cfn_test_grid_project_mixin_props = devicefarm_mixins.CfnTestGridProjectMixinProps(
                description="description",
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vpc_config=devicefarm_mixins.CfnTestGridProjectPropsMixin.VpcConfigProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"],
                    vpc_id="vpcId"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cc7cd1513a068dfaa611a2357e7f8df0879c6c9810e992eea5862e1164ae09c)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc_config", value=vpc_config, expected_type=type_hints["vpc_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags
        if vpc_config is not None:
            self._values["vpc_config"] = vpc_config

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A human-readable description for the project.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-testgridproject.html#cfn-devicefarm-testgridproject-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A human-readable name for the project.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-testgridproject.html#cfn-devicefarm-testgridproject-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ in the *guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-testgridproject.html#cfn-devicefarm-testgridproject-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def vpc_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestGridProjectPropsMixin.VpcConfigProperty"]]:
        '''The VPC security groups and subnets that are attached to a project.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-testgridproject.html#cfn-devicefarm-testgridproject-vpcconfig
        '''
        result = self._values.get("vpc_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestGridProjectPropsMixin.VpcConfigProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTestGridProjectMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnTestGridProjectPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_devicefarm.mixins.CfnTestGridProjectPropsMixin",
):
    '''A Selenium testing project.

    Projects are used to collect and collate sessions.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-testgridproject.html
    :cloudformationResource: AWS::DeviceFarm::TestGridProject
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_devicefarm import mixins as devicefarm_mixins
        
        cfn_test_grid_project_props_mixin = devicefarm_mixins.CfnTestGridProjectPropsMixin(devicefarm_mixins.CfnTestGridProjectMixinProps(
            description="description",
            name="name",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            vpc_config=devicefarm_mixins.CfnTestGridProjectPropsMixin.VpcConfigProperty(
                security_group_ids=["securityGroupIds"],
                subnet_ids=["subnetIds"],
                vpc_id="vpcId"
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnTestGridProjectMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DeviceFarm::TestGridProject``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce8222dce3cc00570c5eca3e817d7157726c9272872def097cb9d77aa013a18f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b772561ff547c4a85281305c35f522ec66d638eb7474d338f8432821ed78402)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e86e50ea5961064d701ed9acbc02ce5786e3ef65dcb3a2588174aac6cc1c5d0f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTestGridProjectMixinProps:
        return typing.cast(CfnTestGridProjectMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_devicefarm.mixins.CfnTestGridProjectPropsMixin.VpcConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
            "vpc_id": "vpcId",
        },
    )
    class VpcConfigProperty:
        def __init__(
            self,
            *,
            security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            vpc_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The VPC security groups and subnets attached to the ``TestGrid`` project.

            :param security_group_ids: A list of VPC security group IDs. A security group allows inbound traffic from network interfaces (and their associated instances) that are assigned to the same security group. See `Security groups <https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html>`_ in the *Amazon Virtual Private Cloud user guide* .
            :param subnet_ids: A list of VPC subnet IDs. A subnet is a range of IP addresses in your VPC. You can launch Amazon resources, such as EC2 instances, into a specific subnet. When you create a subnet, you specify the IPv4 CIDR block for the subnet, which is a subset of the VPC CIDR block. See `VPCs and subnets <https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html>`_ in the *Amazon Virtual Private Cloud user guide* .
            :param vpc_id: A list of VPC IDs. Each VPC is given a unique ID upon creation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devicefarm-testgridproject-vpcconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_devicefarm import mixins as devicefarm_mixins
                
                vpc_config_property = devicefarm_mixins.CfnTestGridProjectPropsMixin.VpcConfigProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"],
                    vpc_id="vpcId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3b44e5d30ec96310f7355f35f7bb4bc5917dee3d69c91a431d47d08929aa912a)
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
                check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
                check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnet_ids is not None:
                self._values["subnet_ids"] = subnet_ids
            if vpc_id is not None:
                self._values["vpc_id"] = vpc_id

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of VPC security group IDs.

            A security group allows inbound traffic from network interfaces (and their associated instances) that are assigned to the same security group. See `Security groups <https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html>`_ in the *Amazon Virtual Private Cloud user guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devicefarm-testgridproject-vpcconfig.html#cfn-devicefarm-testgridproject-vpcconfig-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of VPC subnet IDs.

            A subnet is a range of IP addresses in your VPC. You can launch Amazon resources, such as EC2 instances, into a specific subnet. When you create a subnet, you specify the IPv4 CIDR block for the subnet, which is a subset of the VPC CIDR block. See `VPCs and subnets <https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html>`_ in the *Amazon Virtual Private Cloud user guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devicefarm-testgridproject-vpcconfig.html#cfn-devicefarm-testgridproject-vpcconfig-subnetids
            '''
            result = self._values.get("subnet_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def vpc_id(self) -> typing.Optional[builtins.str]:
            '''A list of VPC IDs.

            Each VPC is given a unique ID upon creation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devicefarm-testgridproject-vpcconfig.html#cfn-devicefarm-testgridproject-vpcconfig-vpcid
            '''
            result = self._values.get("vpc_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_devicefarm.mixins.CfnVPCEConfigurationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "service_dns_name": "serviceDnsName",
        "tags": "tags",
        "vpce_configuration_description": "vpceConfigurationDescription",
        "vpce_configuration_name": "vpceConfigurationName",
        "vpce_service_name": "vpceServiceName",
    },
)
class CfnVPCEConfigurationMixinProps:
    def __init__(
        self,
        *,
        service_dns_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpce_configuration_description: typing.Optional[builtins.str] = None,
        vpce_configuration_name: typing.Optional[builtins.str] = None,
        vpce_service_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnVPCEConfigurationPropsMixin.

        :param service_dns_name: The DNS name that Device Farm will use to map to the private service you want to access.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ in the *guide* .
        :param vpce_configuration_description: An optional description that provides details about your VPC endpoint configuration.
        :param vpce_configuration_name: The friendly name you give to your VPC endpoint configuration to manage your configurations more easily.
        :param vpce_service_name: The name of the VPC endpoint service that you want to access from Device Farm. The name follows the format ``com.amazonaws.vpce.us-west-2.vpce-svc-id`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-vpceconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_devicefarm import mixins as devicefarm_mixins
            
            cfn_vPCEConfiguration_mixin_props = devicefarm_mixins.CfnVPCEConfigurationMixinProps(
                service_dns_name="serviceDnsName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vpce_configuration_description="vpceConfigurationDescription",
                vpce_configuration_name="vpceConfigurationName",
                vpce_service_name="vpceServiceName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41c29c02a66026670a3414f497199ba01c48594daca2bafa331be358009a9e73)
            check_type(argname="argument service_dns_name", value=service_dns_name, expected_type=type_hints["service_dns_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpce_configuration_description", value=vpce_configuration_description, expected_type=type_hints["vpce_configuration_description"])
            check_type(argname="argument vpce_configuration_name", value=vpce_configuration_name, expected_type=type_hints["vpce_configuration_name"])
            check_type(argname="argument vpce_service_name", value=vpce_service_name, expected_type=type_hints["vpce_service_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if service_dns_name is not None:
            self._values["service_dns_name"] = service_dns_name
        if tags is not None:
            self._values["tags"] = tags
        if vpce_configuration_description is not None:
            self._values["vpce_configuration_description"] = vpce_configuration_description
        if vpce_configuration_name is not None:
            self._values["vpce_configuration_name"] = vpce_configuration_name
        if vpce_service_name is not None:
            self._values["vpce_service_name"] = vpce_service_name

    @builtins.property
    def service_dns_name(self) -> typing.Optional[builtins.str]:
        '''The DNS name that Device Farm will use to map to the private service you want to access.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-vpceconfiguration.html#cfn-devicefarm-vpceconfiguration-servicednsname
        '''
        result = self._values.get("service_dns_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ in the *guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-vpceconfiguration.html#cfn-devicefarm-vpceconfiguration-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def vpce_configuration_description(self) -> typing.Optional[builtins.str]:
        '''An optional description that provides details about your VPC endpoint configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-vpceconfiguration.html#cfn-devicefarm-vpceconfiguration-vpceconfigurationdescription
        '''
        result = self._values.get("vpce_configuration_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpce_configuration_name(self) -> typing.Optional[builtins.str]:
        '''The friendly name you give to your VPC endpoint configuration to manage your configurations more easily.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-vpceconfiguration.html#cfn-devicefarm-vpceconfiguration-vpceconfigurationname
        '''
        result = self._values.get("vpce_configuration_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpce_service_name(self) -> typing.Optional[builtins.str]:
        '''The name of the VPC endpoint service that you want to access from Device Farm.

        The name follows the format ``com.amazonaws.vpce.us-west-2.vpce-svc-id`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-vpceconfiguration.html#cfn-devicefarm-vpceconfiguration-vpceservicename
        '''
        result = self._values.get("vpce_service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVPCEConfigurationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnVPCEConfigurationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_devicefarm.mixins.CfnVPCEConfigurationPropsMixin",
):
    '''Creates a configuration record in Device Farm for your Amazon Virtual Private Cloud (VPC) endpoint service.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devicefarm-vpceconfiguration.html
    :cloudformationResource: AWS::DeviceFarm::VPCEConfiguration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_devicefarm import mixins as devicefarm_mixins
        
        cfn_vPCEConfiguration_props_mixin = devicefarm_mixins.CfnVPCEConfigurationPropsMixin(devicefarm_mixins.CfnVPCEConfigurationMixinProps(
            service_dns_name="serviceDnsName",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            vpce_configuration_description="vpceConfigurationDescription",
            vpce_configuration_name="vpceConfigurationName",
            vpce_service_name="vpceServiceName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnVPCEConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DeviceFarm::VPCEConfiguration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0ad67004aed1ab1cab82adb6dd99daad449fdd84c4c6609242add5e56707b3f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3c2bc36e210de930b181acac12e12f08703048f811e91b43abfa66d94b120c5)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57050f9ebfbd03d12ba1ea7bae0785e86096c9897bcd7ff9afd9ff216d1ad22e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnVPCEConfigurationMixinProps:
        return typing.cast(CfnVPCEConfigurationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnDevicePoolMixinProps",
    "CfnDevicePoolPropsMixin",
    "CfnInstanceProfileMixinProps",
    "CfnInstanceProfilePropsMixin",
    "CfnNetworkProfileMixinProps",
    "CfnNetworkProfilePropsMixin",
    "CfnProjectMixinProps",
    "CfnProjectPropsMixin",
    "CfnTestGridProjectMixinProps",
    "CfnTestGridProjectPropsMixin",
    "CfnVPCEConfigurationMixinProps",
    "CfnVPCEConfigurationPropsMixin",
]

publication.publish()

def _typecheckingstub__85bfbf20cea680dbc2bd0a1b5e1807a17dcc5692fb0fbd5c1665e7e738d0f9e6(
    *,
    description: typing.Optional[builtins.str] = None,
    max_devices: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    project_arn: typing.Optional[builtins.str] = None,
    rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDevicePoolPropsMixin.RuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea1d1df1c7b7fbb7b675116e780553a53935b60a9cebee4f5b88bbe3c00967bf(
    props: typing.Union[CfnDevicePoolMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13f08f282119af0ada25eaa1390bd3777770c87d0a6677741e260732caeab3bb(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9041d3c2b632dde085ecca78efc2e7daacb2db92d1e52c56d0909e15c84207e6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd91f9e3c68e337ea2010ebbf1cb09360380234e87120dcde0dc42789bb6dd47(
    *,
    attribute: typing.Optional[builtins.str] = None,
    operator: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__515bed5647f239f5ae46ac45103d4e696806be95a69a3297c6b4957498c48eab(
    *,
    description: typing.Optional[builtins.str] = None,
    exclude_app_packages_from_cleanup: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    package_cleanup: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    reboot_after_use: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ad8fb972d47a6c35a32df5ef42480e72de42a30d1af52bce61e835944fd220b(
    props: typing.Union[CfnInstanceProfileMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af3b6c83dfe03f51351bccd00065523cc4b4e2931e155556d62499e30b4f9e09(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac01f52897ecd5f80a303209eaee73d000a4817ed2bcd0be4124c5b41cc36408(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__055014c2a840471080d8a42b0f71ff3b62be9b5d5acc1eb35b80472c6954ac15(
    *,
    description: typing.Optional[builtins.str] = None,
    downlink_bandwidth_bits: typing.Optional[jsii.Number] = None,
    downlink_delay_ms: typing.Optional[jsii.Number] = None,
    downlink_jitter_ms: typing.Optional[jsii.Number] = None,
    downlink_loss_percent: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    project_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    uplink_bandwidth_bits: typing.Optional[jsii.Number] = None,
    uplink_delay_ms: typing.Optional[jsii.Number] = None,
    uplink_jitter_ms: typing.Optional[jsii.Number] = None,
    uplink_loss_percent: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c86f0a00444a656a2fa173d53f6e3502767cff31637991d0133f2c52bc6052e2(
    props: typing.Union[CfnNetworkProfileMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1967b335619e4d742618d183030f57dc3d25c6e769874c5c2c902eeb38dc06f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f01e2463a893db931c60ccb0a9fd0854307fa916db219c2bea52d2732bd00ea(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fde6c0a8d74f3e557776cd1acf460530e0ff2b9dbc19f21f7841f7dd0cdbe352(
    *,
    default_job_timeout_minutes: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProjectPropsMixin.VpcConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af52de51658b1b2000b6e009eae5e7668d5983ce4a09e17919686e92ff85f267(
    props: typing.Union[CfnProjectMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7519d97163809f0973eb6a2ea021653ef2614d99261f609d8a1045943b934168(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b40d6f76d5be968718089fec5679b5ded8c43bbeacd0ab79d96893254804825(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34e35903fb738d00326bef7fc9797d7a579fa49de0a7fd2ba7b75d3d395cab1a(
    *,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cc7cd1513a068dfaa611a2357e7f8df0879c6c9810e992eea5862e1164ae09c(
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTestGridProjectPropsMixin.VpcConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce8222dce3cc00570c5eca3e817d7157726c9272872def097cb9d77aa013a18f(
    props: typing.Union[CfnTestGridProjectMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b772561ff547c4a85281305c35f522ec66d638eb7474d338f8432821ed78402(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e86e50ea5961064d701ed9acbc02ce5786e3ef65dcb3a2588174aac6cc1c5d0f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b44e5d30ec96310f7355f35f7bb4bc5917dee3d69c91a431d47d08929aa912a(
    *,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41c29c02a66026670a3414f497199ba01c48594daca2bafa331be358009a9e73(
    *,
    service_dns_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpce_configuration_description: typing.Optional[builtins.str] = None,
    vpce_configuration_name: typing.Optional[builtins.str] = None,
    vpce_service_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0ad67004aed1ab1cab82adb6dd99daad449fdd84c4c6609242add5e56707b3f(
    props: typing.Union[CfnVPCEConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3c2bc36e210de930b181acac12e12f08703048f811e91b43abfa66d94b120c5(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57050f9ebfbd03d12ba1ea7bae0785e86096c9897bcd7ff9afd9ff216d1ad22e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
