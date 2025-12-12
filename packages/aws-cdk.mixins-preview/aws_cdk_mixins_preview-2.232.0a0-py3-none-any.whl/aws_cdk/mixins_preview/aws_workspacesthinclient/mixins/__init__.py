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
    jsii_type="@aws-cdk/mixins-preview.aws_workspacesthinclient.mixins.CfnEnvironmentMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "desired_software_set_id": "desiredSoftwareSetId",
        "desktop_arn": "desktopArn",
        "desktop_endpoint": "desktopEndpoint",
        "device_creation_tags": "deviceCreationTags",
        "kms_key_arn": "kmsKeyArn",
        "maintenance_window": "maintenanceWindow",
        "name": "name",
        "software_set_update_mode": "softwareSetUpdateMode",
        "software_set_update_schedule": "softwareSetUpdateSchedule",
        "tags": "tags",
    },
)
class CfnEnvironmentMixinProps:
    def __init__(
        self,
        *,
        desired_software_set_id: typing.Optional[builtins.str] = None,
        desktop_arn: typing.Optional[builtins.str] = None,
        desktop_endpoint: typing.Optional[builtins.str] = None,
        device_creation_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        maintenance_window: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEnvironmentPropsMixin.MaintenanceWindowProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        software_set_update_mode: typing.Optional[builtins.str] = None,
        software_set_update_schedule: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnEnvironmentPropsMixin.

        :param desired_software_set_id: The ID of the software set to apply.
        :param desktop_arn: The Amazon Resource Name (ARN) of the desktop to stream from Amazon WorkSpaces, WorkSpaces Secure Browser, or WorkSpaces Applications.
        :param desktop_endpoint: The URL for the identity provider login (only for environments that use WorkSpaces Applications).
        :param device_creation_tags: An array of key-value pairs to apply to the newly created devices for this environment.
        :param kms_key_arn: The Amazon Resource Name (ARN) of the AWS Key Management Service key used to encrypt the environment.
        :param maintenance_window: A specification for a time window to apply software updates.
        :param name: The name of the environment.
        :param software_set_update_mode: An option to define which software updates to apply.
        :param software_set_update_schedule: An option to define if software updates should be applied within a maintenance window.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesthinclient-environment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_workspacesthinclient import mixins as workspacesthinclient_mixins
            
            cfn_environment_mixin_props = workspacesthinclient_mixins.CfnEnvironmentMixinProps(
                desired_software_set_id="desiredSoftwareSetId",
                desktop_arn="desktopArn",
                desktop_endpoint="desktopEndpoint",
                device_creation_tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                kms_key_arn="kmsKeyArn",
                maintenance_window=workspacesthinclient_mixins.CfnEnvironmentPropsMixin.MaintenanceWindowProperty(
                    apply_time_of="applyTimeOf",
                    days_of_the_week=["daysOfTheWeek"],
                    end_time_hour=123,
                    end_time_minute=123,
                    start_time_hour=123,
                    start_time_minute=123,
                    type="type"
                ),
                name="name",
                software_set_update_mode="softwareSetUpdateMode",
                software_set_update_schedule="softwareSetUpdateSchedule",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d95a64baee29422e32ee43e6ede31fd4c018aff8c103133fc31ea377eb44dea8)
            check_type(argname="argument desired_software_set_id", value=desired_software_set_id, expected_type=type_hints["desired_software_set_id"])
            check_type(argname="argument desktop_arn", value=desktop_arn, expected_type=type_hints["desktop_arn"])
            check_type(argname="argument desktop_endpoint", value=desktop_endpoint, expected_type=type_hints["desktop_endpoint"])
            check_type(argname="argument device_creation_tags", value=device_creation_tags, expected_type=type_hints["device_creation_tags"])
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            check_type(argname="argument maintenance_window", value=maintenance_window, expected_type=type_hints["maintenance_window"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument software_set_update_mode", value=software_set_update_mode, expected_type=type_hints["software_set_update_mode"])
            check_type(argname="argument software_set_update_schedule", value=software_set_update_schedule, expected_type=type_hints["software_set_update_schedule"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if desired_software_set_id is not None:
            self._values["desired_software_set_id"] = desired_software_set_id
        if desktop_arn is not None:
            self._values["desktop_arn"] = desktop_arn
        if desktop_endpoint is not None:
            self._values["desktop_endpoint"] = desktop_endpoint
        if device_creation_tags is not None:
            self._values["device_creation_tags"] = device_creation_tags
        if kms_key_arn is not None:
            self._values["kms_key_arn"] = kms_key_arn
        if maintenance_window is not None:
            self._values["maintenance_window"] = maintenance_window
        if name is not None:
            self._values["name"] = name
        if software_set_update_mode is not None:
            self._values["software_set_update_mode"] = software_set_update_mode
        if software_set_update_schedule is not None:
            self._values["software_set_update_schedule"] = software_set_update_schedule
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def desired_software_set_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the software set to apply.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesthinclient-environment.html#cfn-workspacesthinclient-environment-desiredsoftwaresetid
        '''
        result = self._values.get("desired_software_set_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def desktop_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the desktop to stream from Amazon WorkSpaces, WorkSpaces Secure Browser, or WorkSpaces Applications.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesthinclient-environment.html#cfn-workspacesthinclient-environment-desktoparn
        '''
        result = self._values.get("desktop_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def desktop_endpoint(self) -> typing.Optional[builtins.str]:
        '''The URL for the identity provider login (only for environments that use WorkSpaces Applications).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesthinclient-environment.html#cfn-workspacesthinclient-environment-desktopendpoint
        '''
        result = self._values.get("desktop_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def device_creation_tags(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_ceddda9d.CfnTag]]]]:
        '''An array of key-value pairs to apply to the newly created devices for this environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesthinclient-environment.html#cfn-workspacesthinclient-environment-devicecreationtags
        '''
        result = self._values.get("device_creation_tags")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_ceddda9d.CfnTag]]]], result)

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the AWS Key Management Service key used to encrypt the environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesthinclient-environment.html#cfn-workspacesthinclient-environment-kmskeyarn
        '''
        result = self._values.get("kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maintenance_window(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.MaintenanceWindowProperty"]]:
        '''A specification for a time window to apply software updates.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesthinclient-environment.html#cfn-workspacesthinclient-environment-maintenancewindow
        '''
        result = self._values.get("maintenance_window")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.MaintenanceWindowProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesthinclient-environment.html#cfn-workspacesthinclient-environment-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def software_set_update_mode(self) -> typing.Optional[builtins.str]:
        '''An option to define which software updates to apply.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesthinclient-environment.html#cfn-workspacesthinclient-environment-softwaresetupdatemode
        '''
        result = self._values.get("software_set_update_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def software_set_update_schedule(self) -> typing.Optional[builtins.str]:
        '''An option to define if software updates should be applied within a maintenance window.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesthinclient-environment.html#cfn-workspacesthinclient-environment-softwaresetupdateschedule
        '''
        result = self._values.get("software_set_update_schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesthinclient-environment.html#cfn-workspacesthinclient-environment-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEnvironmentMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnEnvironmentPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_workspacesthinclient.mixins.CfnEnvironmentPropsMixin",
):
    '''Describes an environment.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesthinclient-environment.html
    :cloudformationResource: AWS::WorkSpacesThinClient::Environment
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_workspacesthinclient import mixins as workspacesthinclient_mixins
        
        cfn_environment_props_mixin = workspacesthinclient_mixins.CfnEnvironmentPropsMixin(workspacesthinclient_mixins.CfnEnvironmentMixinProps(
            desired_software_set_id="desiredSoftwareSetId",
            desktop_arn="desktopArn",
            desktop_endpoint="desktopEndpoint",
            device_creation_tags=[CfnTag(
                key="key",
                value="value"
            )],
            kms_key_arn="kmsKeyArn",
            maintenance_window=workspacesthinclient_mixins.CfnEnvironmentPropsMixin.MaintenanceWindowProperty(
                apply_time_of="applyTimeOf",
                days_of_the_week=["daysOfTheWeek"],
                end_time_hour=123,
                end_time_minute=123,
                start_time_hour=123,
                start_time_minute=123,
                type="type"
            ),
            name="name",
            software_set_update_mode="softwareSetUpdateMode",
            software_set_update_schedule="softwareSetUpdateSchedule",
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
        props: typing.Union[CfnEnvironmentMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::WorkSpacesThinClient::Environment``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69925f20143e5da2d25c1eb7a404d5a642a5bd5992c1e86f5c3b43cceb58f70d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d19089b3ca31f7830bb4400cc5aef7c283e0a61bcf368ac112b4a17daa6a0ffc)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe9777e9bc44684d805879ab2a946cf4424f17067dbc58216a5216f39af2e8a3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnEnvironmentMixinProps:
        return typing.cast(CfnEnvironmentMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_workspacesthinclient.mixins.CfnEnvironmentPropsMixin.MaintenanceWindowProperty",
        jsii_struct_bases=[],
        name_mapping={
            "apply_time_of": "applyTimeOf",
            "days_of_the_week": "daysOfTheWeek",
            "end_time_hour": "endTimeHour",
            "end_time_minute": "endTimeMinute",
            "start_time_hour": "startTimeHour",
            "start_time_minute": "startTimeMinute",
            "type": "type",
        },
    )
    class MaintenanceWindowProperty:
        def __init__(
            self,
            *,
            apply_time_of: typing.Optional[builtins.str] = None,
            days_of_the_week: typing.Optional[typing.Sequence[builtins.str]] = None,
            end_time_hour: typing.Optional[jsii.Number] = None,
            end_time_minute: typing.Optional[jsii.Number] = None,
            start_time_hour: typing.Optional[jsii.Number] = None,
            start_time_minute: typing.Optional[jsii.Number] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the maintenance window for a thin client device.

            :param apply_time_of: The option to set the maintenance window during the device local time or Universal Coordinated Time (UTC).
            :param days_of_the_week: The days of the week during which the maintenance window is open.
            :param end_time_hour: The hour for the maintenance window end ( ``00`` - ``23`` ).
            :param end_time_minute: The minutes for the maintenance window end ( ``00`` - ``59`` ).
            :param start_time_hour: The hour for the maintenance window start ( ``00`` - ``23`` ).
            :param start_time_minute: The minutes past the hour for the maintenance window start ( ``00`` - ``59`` ).
            :param type: An option to select the default or custom maintenance window.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesthinclient-environment-maintenancewindow.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_workspacesthinclient import mixins as workspacesthinclient_mixins
                
                maintenance_window_property = workspacesthinclient_mixins.CfnEnvironmentPropsMixin.MaintenanceWindowProperty(
                    apply_time_of="applyTimeOf",
                    days_of_the_week=["daysOfTheWeek"],
                    end_time_hour=123,
                    end_time_minute=123,
                    start_time_hour=123,
                    start_time_minute=123,
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e39388ac2b174e8a328f1fef4ca8fe28b3510ca91356cda9daa4f2639ba74495)
                check_type(argname="argument apply_time_of", value=apply_time_of, expected_type=type_hints["apply_time_of"])
                check_type(argname="argument days_of_the_week", value=days_of_the_week, expected_type=type_hints["days_of_the_week"])
                check_type(argname="argument end_time_hour", value=end_time_hour, expected_type=type_hints["end_time_hour"])
                check_type(argname="argument end_time_minute", value=end_time_minute, expected_type=type_hints["end_time_minute"])
                check_type(argname="argument start_time_hour", value=start_time_hour, expected_type=type_hints["start_time_hour"])
                check_type(argname="argument start_time_minute", value=start_time_minute, expected_type=type_hints["start_time_minute"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if apply_time_of is not None:
                self._values["apply_time_of"] = apply_time_of
            if days_of_the_week is not None:
                self._values["days_of_the_week"] = days_of_the_week
            if end_time_hour is not None:
                self._values["end_time_hour"] = end_time_hour
            if end_time_minute is not None:
                self._values["end_time_minute"] = end_time_minute
            if start_time_hour is not None:
                self._values["start_time_hour"] = start_time_hour
            if start_time_minute is not None:
                self._values["start_time_minute"] = start_time_minute
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def apply_time_of(self) -> typing.Optional[builtins.str]:
            '''The option to set the maintenance window during the device local time or Universal Coordinated Time (UTC).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesthinclient-environment-maintenancewindow.html#cfn-workspacesthinclient-environment-maintenancewindow-applytimeof
            '''
            result = self._values.get("apply_time_of")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def days_of_the_week(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The days of the week during which the maintenance window is open.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesthinclient-environment-maintenancewindow.html#cfn-workspacesthinclient-environment-maintenancewindow-daysoftheweek
            '''
            result = self._values.get("days_of_the_week")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def end_time_hour(self) -> typing.Optional[jsii.Number]:
            '''The hour for the maintenance window end ( ``00`` - ``23`` ).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesthinclient-environment-maintenancewindow.html#cfn-workspacesthinclient-environment-maintenancewindow-endtimehour
            '''
            result = self._values.get("end_time_hour")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def end_time_minute(self) -> typing.Optional[jsii.Number]:
            '''The minutes for the maintenance window end ( ``00`` - ``59`` ).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesthinclient-environment-maintenancewindow.html#cfn-workspacesthinclient-environment-maintenancewindow-endtimeminute
            '''
            result = self._values.get("end_time_minute")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def start_time_hour(self) -> typing.Optional[jsii.Number]:
            '''The hour for the maintenance window start ( ``00`` - ``23`` ).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesthinclient-environment-maintenancewindow.html#cfn-workspacesthinclient-environment-maintenancewindow-starttimehour
            '''
            result = self._values.get("start_time_hour")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def start_time_minute(self) -> typing.Optional[jsii.Number]:
            '''The minutes past the hour for the maintenance window start ( ``00`` - ``59`` ).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesthinclient-environment-maintenancewindow.html#cfn-workspacesthinclient-environment-maintenancewindow-starttimeminute
            '''
            result = self._values.get("start_time_minute")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''An option to select the default or custom maintenance window.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesthinclient-environment-maintenancewindow.html#cfn-workspacesthinclient-environment-maintenancewindow-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MaintenanceWindowProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnEnvironmentMixinProps",
    "CfnEnvironmentPropsMixin",
]

publication.publish()

def _typecheckingstub__d95a64baee29422e32ee43e6ede31fd4c018aff8c103133fc31ea377eb44dea8(
    *,
    desired_software_set_id: typing.Optional[builtins.str] = None,
    desktop_arn: typing.Optional[builtins.str] = None,
    desktop_endpoint: typing.Optional[builtins.str] = None,
    device_creation_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    maintenance_window: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEnvironmentPropsMixin.MaintenanceWindowProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    software_set_update_mode: typing.Optional[builtins.str] = None,
    software_set_update_schedule: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69925f20143e5da2d25c1eb7a404d5a642a5bd5992c1e86f5c3b43cceb58f70d(
    props: typing.Union[CfnEnvironmentMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d19089b3ca31f7830bb4400cc5aef7c283e0a61bcf368ac112b4a17daa6a0ffc(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe9777e9bc44684d805879ab2a946cf4424f17067dbc58216a5216f39af2e8a3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e39388ac2b174e8a328f1fef4ca8fe28b3510ca91356cda9daa4f2639ba74495(
    *,
    apply_time_of: typing.Optional[builtins.str] = None,
    days_of_the_week: typing.Optional[typing.Sequence[builtins.str]] = None,
    end_time_hour: typing.Optional[jsii.Number] = None,
    end_time_minute: typing.Optional[jsii.Number] = None,
    start_time_hour: typing.Optional[jsii.Number] = None,
    start_time_minute: typing.Optional[jsii.Number] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
