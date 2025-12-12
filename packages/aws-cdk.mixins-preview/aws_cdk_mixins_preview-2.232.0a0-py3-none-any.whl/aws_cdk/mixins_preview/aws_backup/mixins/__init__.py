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
    jsii_type="@aws-cdk/mixins-preview.aws_backup.mixins.CfnBackupPlanMixinProps",
    jsii_struct_bases=[],
    name_mapping={"backup_plan": "backupPlan", "backup_plan_tags": "backupPlanTags"},
)
class CfnBackupPlanMixinProps:
    def __init__(
        self,
        *,
        backup_plan: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBackupPlanPropsMixin.BackupPlanResourceTypeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        backup_plan_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnBackupPlanPropsMixin.

        :param backup_plan: Uniquely identifies the backup plan to be associated with the selection of resources.
        :param backup_plan_tags: The tags to assign to the backup plan.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupplan.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_backup import mixins as backup_mixins
            
            # backup_options: Any
            
            cfn_backup_plan_mixin_props = backup_mixins.CfnBackupPlanMixinProps(
                backup_plan=backup_mixins.CfnBackupPlanPropsMixin.BackupPlanResourceTypeProperty(
                    advanced_backup_settings=[backup_mixins.CfnBackupPlanPropsMixin.AdvancedBackupSettingResourceTypeProperty(
                        backup_options=backup_options,
                        resource_type="resourceType"
                    )],
                    backup_plan_name="backupPlanName",
                    backup_plan_rule=[backup_mixins.CfnBackupPlanPropsMixin.BackupRuleResourceTypeProperty(
                        completion_window_minutes=123,
                        copy_actions=[backup_mixins.CfnBackupPlanPropsMixin.CopyActionResourceTypeProperty(
                            destination_backup_vault_arn="destinationBackupVaultArn",
                            lifecycle=backup_mixins.CfnBackupPlanPropsMixin.LifecycleResourceTypeProperty(
                                delete_after_days=123,
                                move_to_cold_storage_after_days=123,
                                opt_in_to_archive_for_supported_resources=False
                            )
                        )],
                        enable_continuous_backup=False,
                        index_actions=[backup_mixins.CfnBackupPlanPropsMixin.IndexActionsResourceTypeProperty(
                            resource_types=["resourceTypes"]
                        )],
                        lifecycle=backup_mixins.CfnBackupPlanPropsMixin.LifecycleResourceTypeProperty(
                            delete_after_days=123,
                            move_to_cold_storage_after_days=123,
                            opt_in_to_archive_for_supported_resources=False
                        ),
                        recovery_point_tags={
                            "recovery_point_tags_key": "recoveryPointTags"
                        },
                        rule_name="ruleName",
                        schedule_expression="scheduleExpression",
                        schedule_expression_timezone="scheduleExpressionTimezone",
                        start_window_minutes=123,
                        target_backup_vault="targetBackupVault",
                        target_logically_air_gapped_backup_vault_arn="targetLogicallyAirGappedBackupVaultArn"
                    )]
                ),
                backup_plan_tags={
                    "backup_plan_tags_key": "backupPlanTags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c52c3ba5518a4eddf653790cfcc9253bcbcda34e798ed1e347336649f2cedbf7)
            check_type(argname="argument backup_plan", value=backup_plan, expected_type=type_hints["backup_plan"])
            check_type(argname="argument backup_plan_tags", value=backup_plan_tags, expected_type=type_hints["backup_plan_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if backup_plan is not None:
            self._values["backup_plan"] = backup_plan
        if backup_plan_tags is not None:
            self._values["backup_plan_tags"] = backup_plan_tags

    @builtins.property
    def backup_plan(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBackupPlanPropsMixin.BackupPlanResourceTypeProperty"]]:
        '''Uniquely identifies the backup plan to be associated with the selection of resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupplan.html#cfn-backup-backupplan-backupplan
        '''
        result = self._values.get("backup_plan")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBackupPlanPropsMixin.BackupPlanResourceTypeProperty"]], result)

    @builtins.property
    def backup_plan_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The tags to assign to the backup plan.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupplan.html#cfn-backup-backupplan-backupplantags
        '''
        result = self._values.get("backup_plan_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBackupPlanMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnBackupPlanPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_backup.mixins.CfnBackupPlanPropsMixin",
):
    '''Contains an optional backup plan display name and an array of ``BackupRule`` objects, each of which specifies a backup rule.

    Each rule in a backup plan is a separate scheduled task and can back up a different selection of AWS resources.

    For a sample CloudFormation template, see the `AWS Backup Developer Guide <https://docs.aws.amazon.com/aws-backup/latest/devguide/assigning-resources.html#assigning-resources-cfn>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupplan.html
    :cloudformationResource: AWS::Backup::BackupPlan
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_backup import mixins as backup_mixins
        
        # backup_options: Any
        
        cfn_backup_plan_props_mixin = backup_mixins.CfnBackupPlanPropsMixin(backup_mixins.CfnBackupPlanMixinProps(
            backup_plan=backup_mixins.CfnBackupPlanPropsMixin.BackupPlanResourceTypeProperty(
                advanced_backup_settings=[backup_mixins.CfnBackupPlanPropsMixin.AdvancedBackupSettingResourceTypeProperty(
                    backup_options=backup_options,
                    resource_type="resourceType"
                )],
                backup_plan_name="backupPlanName",
                backup_plan_rule=[backup_mixins.CfnBackupPlanPropsMixin.BackupRuleResourceTypeProperty(
                    completion_window_minutes=123,
                    copy_actions=[backup_mixins.CfnBackupPlanPropsMixin.CopyActionResourceTypeProperty(
                        destination_backup_vault_arn="destinationBackupVaultArn",
                        lifecycle=backup_mixins.CfnBackupPlanPropsMixin.LifecycleResourceTypeProperty(
                            delete_after_days=123,
                            move_to_cold_storage_after_days=123,
                            opt_in_to_archive_for_supported_resources=False
                        )
                    )],
                    enable_continuous_backup=False,
                    index_actions=[backup_mixins.CfnBackupPlanPropsMixin.IndexActionsResourceTypeProperty(
                        resource_types=["resourceTypes"]
                    )],
                    lifecycle=backup_mixins.CfnBackupPlanPropsMixin.LifecycleResourceTypeProperty(
                        delete_after_days=123,
                        move_to_cold_storage_after_days=123,
                        opt_in_to_archive_for_supported_resources=False
                    ),
                    recovery_point_tags={
                        "recovery_point_tags_key": "recoveryPointTags"
                    },
                    rule_name="ruleName",
                    schedule_expression="scheduleExpression",
                    schedule_expression_timezone="scheduleExpressionTimezone",
                    start_window_minutes=123,
                    target_backup_vault="targetBackupVault",
                    target_logically_air_gapped_backup_vault_arn="targetLogicallyAirGappedBackupVaultArn"
                )]
            ),
            backup_plan_tags={
                "backup_plan_tags_key": "backupPlanTags"
            }
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnBackupPlanMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Backup::BackupPlan``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa1fb7fd3baec625155ea0022560ceb0289f5ee02e77a7b7852a07edc73239a6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f7255e14502397e518347471c7aeaa4ee6ed8f1fb9aa7f192189a186243fc15)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d33c9b99526c39919a02d46f942083c45301e82b31f24c00f61a32551deb8cb9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnBackupPlanMixinProps:
        return typing.cast(CfnBackupPlanMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_backup.mixins.CfnBackupPlanPropsMixin.AdvancedBackupSettingResourceTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "backup_options": "backupOptions",
            "resource_type": "resourceType",
        },
    )
    class AdvancedBackupSettingResourceTypeProperty:
        def __init__(
            self,
            *,
            backup_options: typing.Any = None,
            resource_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies an object containing resource type and backup options.

            This is only supported for Windows VSS backups.

            :param backup_options: The backup option for the resource. Each option is a key-value pair. This option is only available for Windows VSS backup jobs. Valid values: Set to ``"WindowsVSS":"enabled"`` to enable the ``WindowsVSS`` backup option and create a Windows VSS backup. Set to ``"WindowsVSS":"disabled"`` to create a regular backup. The ``WindowsVSS`` option is not enabled by default. If you specify an invalid option, you get an ``InvalidParameterValueException`` exception. For more information about Windows VSS backups, see `Creating a VSS-Enabled Windows Backup <https://docs.aws.amazon.com/aws-backup/latest/devguide/windows-backups.html>`_ .
            :param resource_type: The name of a resource type. The only supported resource type is EC2.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-advancedbackupsettingresourcetype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_backup import mixins as backup_mixins
                
                # backup_options: Any
                
                advanced_backup_setting_resource_type_property = backup_mixins.CfnBackupPlanPropsMixin.AdvancedBackupSettingResourceTypeProperty(
                    backup_options=backup_options,
                    resource_type="resourceType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__461955aaf03e4b77445644bde0b4c762ad052ded1e115b150888942af8a8196f)
                check_type(argname="argument backup_options", value=backup_options, expected_type=type_hints["backup_options"])
                check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if backup_options is not None:
                self._values["backup_options"] = backup_options
            if resource_type is not None:
                self._values["resource_type"] = resource_type

        @builtins.property
        def backup_options(self) -> typing.Any:
            '''The backup option for the resource.

            Each option is a key-value pair. This option is only available for Windows VSS backup jobs.

            Valid values:

            Set to ``"WindowsVSS":"enabled"`` to enable the ``WindowsVSS`` backup option and create a Windows VSS backup.

            Set to ``"WindowsVSS":"disabled"`` to create a regular backup. The ``WindowsVSS`` option is not enabled by default.

            If you specify an invalid option, you get an ``InvalidParameterValueException`` exception.

            For more information about Windows VSS backups, see `Creating a VSS-Enabled Windows Backup <https://docs.aws.amazon.com/aws-backup/latest/devguide/windows-backups.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-advancedbackupsettingresourcetype.html#cfn-backup-backupplan-advancedbackupsettingresourcetype-backupoptions
            '''
            result = self._values.get("backup_options")
            return typing.cast(typing.Any, result)

        @builtins.property
        def resource_type(self) -> typing.Optional[builtins.str]:
            '''The name of a resource type.

            The only supported resource type is EC2.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-advancedbackupsettingresourcetype.html#cfn-backup-backupplan-advancedbackupsettingresourcetype-resourcetype
            '''
            result = self._values.get("resource_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AdvancedBackupSettingResourceTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_backup.mixins.CfnBackupPlanPropsMixin.BackupPlanResourceTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "advanced_backup_settings": "advancedBackupSettings",
            "backup_plan_name": "backupPlanName",
            "backup_plan_rule": "backupPlanRule",
        },
    )
    class BackupPlanResourceTypeProperty:
        def __init__(
            self,
            *,
            advanced_backup_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBackupPlanPropsMixin.AdvancedBackupSettingResourceTypeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            backup_plan_name: typing.Optional[builtins.str] = None,
            backup_plan_rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBackupPlanPropsMixin.BackupRuleResourceTypeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Specifies an object containing properties used to create a backup plan.

            :param advanced_backup_settings: A list of backup options for each resource type.
            :param backup_plan_name: The display name of a backup plan.
            :param backup_plan_rule: An array of ``BackupRule`` objects, each of which specifies a scheduled task that is used to back up a selection of resources.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-backupplanresourcetype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_backup import mixins as backup_mixins
                
                # backup_options: Any
                
                backup_plan_resource_type_property = backup_mixins.CfnBackupPlanPropsMixin.BackupPlanResourceTypeProperty(
                    advanced_backup_settings=[backup_mixins.CfnBackupPlanPropsMixin.AdvancedBackupSettingResourceTypeProperty(
                        backup_options=backup_options,
                        resource_type="resourceType"
                    )],
                    backup_plan_name="backupPlanName",
                    backup_plan_rule=[backup_mixins.CfnBackupPlanPropsMixin.BackupRuleResourceTypeProperty(
                        completion_window_minutes=123,
                        copy_actions=[backup_mixins.CfnBackupPlanPropsMixin.CopyActionResourceTypeProperty(
                            destination_backup_vault_arn="destinationBackupVaultArn",
                            lifecycle=backup_mixins.CfnBackupPlanPropsMixin.LifecycleResourceTypeProperty(
                                delete_after_days=123,
                                move_to_cold_storage_after_days=123,
                                opt_in_to_archive_for_supported_resources=False
                            )
                        )],
                        enable_continuous_backup=False,
                        index_actions=[backup_mixins.CfnBackupPlanPropsMixin.IndexActionsResourceTypeProperty(
                            resource_types=["resourceTypes"]
                        )],
                        lifecycle=backup_mixins.CfnBackupPlanPropsMixin.LifecycleResourceTypeProperty(
                            delete_after_days=123,
                            move_to_cold_storage_after_days=123,
                            opt_in_to_archive_for_supported_resources=False
                        ),
                        recovery_point_tags={
                            "recovery_point_tags_key": "recoveryPointTags"
                        },
                        rule_name="ruleName",
                        schedule_expression="scheduleExpression",
                        schedule_expression_timezone="scheduleExpressionTimezone",
                        start_window_minutes=123,
                        target_backup_vault="targetBackupVault",
                        target_logically_air_gapped_backup_vault_arn="targetLogicallyAirGappedBackupVaultArn"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__15c9250612b8f408f2b07b56b91b7dac9c891af8a4af727b2ca9485ff633f9ce)
                check_type(argname="argument advanced_backup_settings", value=advanced_backup_settings, expected_type=type_hints["advanced_backup_settings"])
                check_type(argname="argument backup_plan_name", value=backup_plan_name, expected_type=type_hints["backup_plan_name"])
                check_type(argname="argument backup_plan_rule", value=backup_plan_rule, expected_type=type_hints["backup_plan_rule"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if advanced_backup_settings is not None:
                self._values["advanced_backup_settings"] = advanced_backup_settings
            if backup_plan_name is not None:
                self._values["backup_plan_name"] = backup_plan_name
            if backup_plan_rule is not None:
                self._values["backup_plan_rule"] = backup_plan_rule

        @builtins.property
        def advanced_backup_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBackupPlanPropsMixin.AdvancedBackupSettingResourceTypeProperty"]]]]:
            '''A list of backup options for each resource type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-backupplanresourcetype.html#cfn-backup-backupplan-backupplanresourcetype-advancedbackupsettings
            '''
            result = self._values.get("advanced_backup_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBackupPlanPropsMixin.AdvancedBackupSettingResourceTypeProperty"]]]], result)

        @builtins.property
        def backup_plan_name(self) -> typing.Optional[builtins.str]:
            '''The display name of a backup plan.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-backupplanresourcetype.html#cfn-backup-backupplan-backupplanresourcetype-backupplanname
            '''
            result = self._values.get("backup_plan_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def backup_plan_rule(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBackupPlanPropsMixin.BackupRuleResourceTypeProperty"]]]]:
            '''An array of ``BackupRule`` objects, each of which specifies a scheduled task that is used to back up a selection of resources.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-backupplanresourcetype.html#cfn-backup-backupplan-backupplanresourcetype-backupplanrule
            '''
            result = self._values.get("backup_plan_rule")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBackupPlanPropsMixin.BackupRuleResourceTypeProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BackupPlanResourceTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_backup.mixins.CfnBackupPlanPropsMixin.BackupRuleResourceTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "completion_window_minutes": "completionWindowMinutes",
            "copy_actions": "copyActions",
            "enable_continuous_backup": "enableContinuousBackup",
            "index_actions": "indexActions",
            "lifecycle": "lifecycle",
            "recovery_point_tags": "recoveryPointTags",
            "rule_name": "ruleName",
            "schedule_expression": "scheduleExpression",
            "schedule_expression_timezone": "scheduleExpressionTimezone",
            "start_window_minutes": "startWindowMinutes",
            "target_backup_vault": "targetBackupVault",
            "target_logically_air_gapped_backup_vault_arn": "targetLogicallyAirGappedBackupVaultArn",
        },
    )
    class BackupRuleResourceTypeProperty:
        def __init__(
            self,
            *,
            completion_window_minutes: typing.Optional[jsii.Number] = None,
            copy_actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBackupPlanPropsMixin.CopyActionResourceTypeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            enable_continuous_backup: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            index_actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBackupPlanPropsMixin.IndexActionsResourceTypeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            lifecycle: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBackupPlanPropsMixin.LifecycleResourceTypeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            recovery_point_tags: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            rule_name: typing.Optional[builtins.str] = None,
            schedule_expression: typing.Optional[builtins.str] = None,
            schedule_expression_timezone: typing.Optional[builtins.str] = None,
            start_window_minutes: typing.Optional[jsii.Number] = None,
            target_backup_vault: typing.Optional[builtins.str] = None,
            target_logically_air_gapped_backup_vault_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies an object containing properties used to schedule a task to back up a selection of resources.

            :param completion_window_minutes: A value in minutes after a backup job is successfully started before it must be completed or it is canceled by AWS Backup .
            :param copy_actions: An array of CopyAction objects, which contains the details of the copy operation.
            :param enable_continuous_backup: Enables continuous backup and point-in-time restores (PITR).
            :param index_actions: There can up to one IndexAction in each BackupRule, as each backup can have 0 or 1 backup index associated with it. Within the array is ResourceTypes. Only 1 resource type will be accepted for each BackupRule. Valid values: - ``EBS`` for Amazon Elastic Block Store - ``S3`` for Amazon Simple Storage Service (Amazon S3)
            :param lifecycle: The lifecycle defines when a protected resource is transitioned to cold storage and when it expires. AWS Backup transitions and expires backups automatically according to the lifecycle that you define.
            :param recovery_point_tags: The tags to assign to the resources.
            :param rule_name: A display name for a backup rule.
            :param schedule_expression: A CRON expression specifying when AWS Backup initiates a backup job.
            :param schedule_expression_timezone: This is the timezone in which the schedule expression is set. By default, ScheduleExpressions are in UTC. You can modify this to a specified timezone.
            :param start_window_minutes: An optional value that specifies a period of time in minutes after a backup is scheduled before a job is canceled if it doesn't start successfully. If this value is included, it must be at least 60 minutes to avoid errors.
            :param target_backup_vault: The name of a logical container where backups are stored. Backup vaults are identified by names that are unique to the account used to create them and the AWS Region where they are created. They consist of letters, numbers, and hyphens.
            :param target_logically_air_gapped_backup_vault_arn: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-backupruleresourcetype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_backup import mixins as backup_mixins
                
                backup_rule_resource_type_property = backup_mixins.CfnBackupPlanPropsMixin.BackupRuleResourceTypeProperty(
                    completion_window_minutes=123,
                    copy_actions=[backup_mixins.CfnBackupPlanPropsMixin.CopyActionResourceTypeProperty(
                        destination_backup_vault_arn="destinationBackupVaultArn",
                        lifecycle=backup_mixins.CfnBackupPlanPropsMixin.LifecycleResourceTypeProperty(
                            delete_after_days=123,
                            move_to_cold_storage_after_days=123,
                            opt_in_to_archive_for_supported_resources=False
                        )
                    )],
                    enable_continuous_backup=False,
                    index_actions=[backup_mixins.CfnBackupPlanPropsMixin.IndexActionsResourceTypeProperty(
                        resource_types=["resourceTypes"]
                    )],
                    lifecycle=backup_mixins.CfnBackupPlanPropsMixin.LifecycleResourceTypeProperty(
                        delete_after_days=123,
                        move_to_cold_storage_after_days=123,
                        opt_in_to_archive_for_supported_resources=False
                    ),
                    recovery_point_tags={
                        "recovery_point_tags_key": "recoveryPointTags"
                    },
                    rule_name="ruleName",
                    schedule_expression="scheduleExpression",
                    schedule_expression_timezone="scheduleExpressionTimezone",
                    start_window_minutes=123,
                    target_backup_vault="targetBackupVault",
                    target_logically_air_gapped_backup_vault_arn="targetLogicallyAirGappedBackupVaultArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8ea571f90248cad05290a3f2b70ae8d80d8ade58a97b0838fa2e9d0188a32e19)
                check_type(argname="argument completion_window_minutes", value=completion_window_minutes, expected_type=type_hints["completion_window_minutes"])
                check_type(argname="argument copy_actions", value=copy_actions, expected_type=type_hints["copy_actions"])
                check_type(argname="argument enable_continuous_backup", value=enable_continuous_backup, expected_type=type_hints["enable_continuous_backup"])
                check_type(argname="argument index_actions", value=index_actions, expected_type=type_hints["index_actions"])
                check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
                check_type(argname="argument recovery_point_tags", value=recovery_point_tags, expected_type=type_hints["recovery_point_tags"])
                check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
                check_type(argname="argument schedule_expression", value=schedule_expression, expected_type=type_hints["schedule_expression"])
                check_type(argname="argument schedule_expression_timezone", value=schedule_expression_timezone, expected_type=type_hints["schedule_expression_timezone"])
                check_type(argname="argument start_window_minutes", value=start_window_minutes, expected_type=type_hints["start_window_minutes"])
                check_type(argname="argument target_backup_vault", value=target_backup_vault, expected_type=type_hints["target_backup_vault"])
                check_type(argname="argument target_logically_air_gapped_backup_vault_arn", value=target_logically_air_gapped_backup_vault_arn, expected_type=type_hints["target_logically_air_gapped_backup_vault_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if completion_window_minutes is not None:
                self._values["completion_window_minutes"] = completion_window_minutes
            if copy_actions is not None:
                self._values["copy_actions"] = copy_actions
            if enable_continuous_backup is not None:
                self._values["enable_continuous_backup"] = enable_continuous_backup
            if index_actions is not None:
                self._values["index_actions"] = index_actions
            if lifecycle is not None:
                self._values["lifecycle"] = lifecycle
            if recovery_point_tags is not None:
                self._values["recovery_point_tags"] = recovery_point_tags
            if rule_name is not None:
                self._values["rule_name"] = rule_name
            if schedule_expression is not None:
                self._values["schedule_expression"] = schedule_expression
            if schedule_expression_timezone is not None:
                self._values["schedule_expression_timezone"] = schedule_expression_timezone
            if start_window_minutes is not None:
                self._values["start_window_minutes"] = start_window_minutes
            if target_backup_vault is not None:
                self._values["target_backup_vault"] = target_backup_vault
            if target_logically_air_gapped_backup_vault_arn is not None:
                self._values["target_logically_air_gapped_backup_vault_arn"] = target_logically_air_gapped_backup_vault_arn

        @builtins.property
        def completion_window_minutes(self) -> typing.Optional[jsii.Number]:
            '''A value in minutes after a backup job is successfully started before it must be completed or it is canceled by AWS Backup .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-backupruleresourcetype.html#cfn-backup-backupplan-backupruleresourcetype-completionwindowminutes
            '''
            result = self._values.get("completion_window_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def copy_actions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBackupPlanPropsMixin.CopyActionResourceTypeProperty"]]]]:
            '''An array of CopyAction objects, which contains the details of the copy operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-backupruleresourcetype.html#cfn-backup-backupplan-backupruleresourcetype-copyactions
            '''
            result = self._values.get("copy_actions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBackupPlanPropsMixin.CopyActionResourceTypeProperty"]]]], result)

        @builtins.property
        def enable_continuous_backup(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Enables continuous backup and point-in-time restores (PITR).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-backupruleresourcetype.html#cfn-backup-backupplan-backupruleresourcetype-enablecontinuousbackup
            '''
            result = self._values.get("enable_continuous_backup")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def index_actions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBackupPlanPropsMixin.IndexActionsResourceTypeProperty"]]]]:
            '''There can up to one IndexAction in each BackupRule, as each backup can have 0 or 1 backup index associated with it.

            Within the array is ResourceTypes. Only 1 resource type will be accepted for each BackupRule. Valid values:

            - ``EBS`` for Amazon Elastic Block Store
            - ``S3`` for Amazon Simple Storage Service (Amazon S3)

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-backupruleresourcetype.html#cfn-backup-backupplan-backupruleresourcetype-indexactions
            '''
            result = self._values.get("index_actions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBackupPlanPropsMixin.IndexActionsResourceTypeProperty"]]]], result)

        @builtins.property
        def lifecycle(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBackupPlanPropsMixin.LifecycleResourceTypeProperty"]]:
            '''The lifecycle defines when a protected resource is transitioned to cold storage and when it expires.

            AWS Backup transitions and expires backups automatically according to the lifecycle that you define.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-backupruleresourcetype.html#cfn-backup-backupplan-backupruleresourcetype-lifecycle
            '''
            result = self._values.get("lifecycle")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBackupPlanPropsMixin.LifecycleResourceTypeProperty"]], result)

        @builtins.property
        def recovery_point_tags(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''The tags to assign to the resources.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-backupruleresourcetype.html#cfn-backup-backupplan-backupruleresourcetype-recoverypointtags
            '''
            result = self._values.get("recovery_point_tags")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def rule_name(self) -> typing.Optional[builtins.str]:
            '''A display name for a backup rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-backupruleresourcetype.html#cfn-backup-backupplan-backupruleresourcetype-rulename
            '''
            result = self._values.get("rule_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def schedule_expression(self) -> typing.Optional[builtins.str]:
            '''A CRON expression specifying when AWS Backup initiates a backup job.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-backupruleresourcetype.html#cfn-backup-backupplan-backupruleresourcetype-scheduleexpression
            '''
            result = self._values.get("schedule_expression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def schedule_expression_timezone(self) -> typing.Optional[builtins.str]:
            '''This is the timezone in which the schedule expression is set.

            By default, ScheduleExpressions are in UTC. You can modify this to a specified timezone.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-backupruleresourcetype.html#cfn-backup-backupplan-backupruleresourcetype-scheduleexpressiontimezone
            '''
            result = self._values.get("schedule_expression_timezone")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def start_window_minutes(self) -> typing.Optional[jsii.Number]:
            '''An optional value that specifies a period of time in minutes after a backup is scheduled before a job is canceled if it doesn't start successfully.

            If this value is included, it must be at least 60 minutes to avoid errors.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-backupruleresourcetype.html#cfn-backup-backupplan-backupruleresourcetype-startwindowminutes
            '''
            result = self._values.get("start_window_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def target_backup_vault(self) -> typing.Optional[builtins.str]:
            '''The name of a logical container where backups are stored.

            Backup vaults are identified by names that are unique to the account used to create them and the AWS Region where they are created. They consist of letters, numbers, and hyphens.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-backupruleresourcetype.html#cfn-backup-backupplan-backupruleresourcetype-targetbackupvault
            '''
            result = self._values.get("target_backup_vault")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_logically_air_gapped_backup_vault_arn(
            self,
        ) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-backupruleresourcetype.html#cfn-backup-backupplan-backupruleresourcetype-targetlogicallyairgappedbackupvaultarn
            '''
            result = self._values.get("target_logically_air_gapped_backup_vault_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BackupRuleResourceTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_backup.mixins.CfnBackupPlanPropsMixin.CopyActionResourceTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_backup_vault_arn": "destinationBackupVaultArn",
            "lifecycle": "lifecycle",
        },
    )
    class CopyActionResourceTypeProperty:
        def __init__(
            self,
            *,
            destination_backup_vault_arn: typing.Optional[builtins.str] = None,
            lifecycle: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBackupPlanPropsMixin.LifecycleResourceTypeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Copies backups created by a backup rule to another vault.

            :param destination_backup_vault_arn: An Amazon Resource Name (ARN) that uniquely identifies the destination backup vault for the copied backup. For example, ``arn:aws:backup:us-east-1:123456789012:vault:aBackupVault.``
            :param lifecycle: Defines when a protected resource is transitioned to cold storage and when it expires. AWS Backup transitions and expires backups automatically according to the lifecycle that you define. If you do not specify a lifecycle, AWS Backup applies the lifecycle policy of the source backup to the destination backup. Backups transitioned to cold storage must be stored in cold storage for a minimum of 90 days.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-copyactionresourcetype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_backup import mixins as backup_mixins
                
                copy_action_resource_type_property = backup_mixins.CfnBackupPlanPropsMixin.CopyActionResourceTypeProperty(
                    destination_backup_vault_arn="destinationBackupVaultArn",
                    lifecycle=backup_mixins.CfnBackupPlanPropsMixin.LifecycleResourceTypeProperty(
                        delete_after_days=123,
                        move_to_cold_storage_after_days=123,
                        opt_in_to_archive_for_supported_resources=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f5c58b9d2d5a4321a8189b50d8d7b950929b947271c008bff06c10f6598d8e84)
                check_type(argname="argument destination_backup_vault_arn", value=destination_backup_vault_arn, expected_type=type_hints["destination_backup_vault_arn"])
                check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination_backup_vault_arn is not None:
                self._values["destination_backup_vault_arn"] = destination_backup_vault_arn
            if lifecycle is not None:
                self._values["lifecycle"] = lifecycle

        @builtins.property
        def destination_backup_vault_arn(self) -> typing.Optional[builtins.str]:
            '''An Amazon Resource Name (ARN) that uniquely identifies the destination backup vault for the copied backup.

            For example, ``arn:aws:backup:us-east-1:123456789012:vault:aBackupVault.``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-copyactionresourcetype.html#cfn-backup-backupplan-copyactionresourcetype-destinationbackupvaultarn
            '''
            result = self._values.get("destination_backup_vault_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def lifecycle(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBackupPlanPropsMixin.LifecycleResourceTypeProperty"]]:
            '''Defines when a protected resource is transitioned to cold storage and when it expires.

            AWS Backup transitions and expires backups automatically according to the lifecycle that you define. If you do not specify a lifecycle, AWS Backup applies the lifecycle policy of the source backup to the destination backup.

            Backups transitioned to cold storage must be stored in cold storage for a minimum of 90 days.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-copyactionresourcetype.html#cfn-backup-backupplan-copyactionresourcetype-lifecycle
            '''
            result = self._values.get("lifecycle")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBackupPlanPropsMixin.LifecycleResourceTypeProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CopyActionResourceTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_backup.mixins.CfnBackupPlanPropsMixin.IndexActionsResourceTypeProperty",
        jsii_struct_bases=[],
        name_mapping={"resource_types": "resourceTypes"},
    )
    class IndexActionsResourceTypeProperty:
        def __init__(
            self,
            *,
            resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Specifies index actions.

            :param resource_types: 0 or 1 index action will be accepted for each BackupRule. Valid values: - ``EBS`` for Amazon Elastic Block Store - ``S3`` for Amazon Simple Storage Service (Amazon S3)

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-indexactionsresourcetype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_backup import mixins as backup_mixins
                
                index_actions_resource_type_property = backup_mixins.CfnBackupPlanPropsMixin.IndexActionsResourceTypeProperty(
                    resource_types=["resourceTypes"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9ec78af3ad88b132b7dcc80fe1e930ecfb06c641ca343736be1bdbac6007a007)
                check_type(argname="argument resource_types", value=resource_types, expected_type=type_hints["resource_types"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if resource_types is not None:
                self._values["resource_types"] = resource_types

        @builtins.property
        def resource_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''0 or 1 index action will be accepted for each BackupRule.

            Valid values:

            - ``EBS`` for Amazon Elastic Block Store
            - ``S3`` for Amazon Simple Storage Service (Amazon S3)

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-indexactionsresourcetype.html#cfn-backup-backupplan-indexactionsresourcetype-resourcetypes
            '''
            result = self._values.get("resource_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IndexActionsResourceTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_backup.mixins.CfnBackupPlanPropsMixin.LifecycleResourceTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "delete_after_days": "deleteAfterDays",
            "move_to_cold_storage_after_days": "moveToColdStorageAfterDays",
            "opt_in_to_archive_for_supported_resources": "optInToArchiveForSupportedResources",
        },
    )
    class LifecycleResourceTypeProperty:
        def __init__(
            self,
            *,
            delete_after_days: typing.Optional[jsii.Number] = None,
            move_to_cold_storage_after_days: typing.Optional[jsii.Number] = None,
            opt_in_to_archive_for_supported_resources: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Specifies an object containing an array of ``Transition`` objects that determine how long in days before a recovery point transitions to cold storage or is deleted.

            :param delete_after_days: The number of days after creation that a recovery point is deleted. This value must be at least 90 days after the number of days specified in ``MoveToColdStorageAfterDays`` .
            :param move_to_cold_storage_after_days: The number of days after creation that a recovery point is moved to cold storage.
            :param opt_in_to_archive_for_supported_resources: If the value is true, your backup plan transitions supported resources to archive (cold) storage tier in accordance with your lifecycle settings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-lifecycleresourcetype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_backup import mixins as backup_mixins
                
                lifecycle_resource_type_property = backup_mixins.CfnBackupPlanPropsMixin.LifecycleResourceTypeProperty(
                    delete_after_days=123,
                    move_to_cold_storage_after_days=123,
                    opt_in_to_archive_for_supported_resources=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fec90a2f0249924188094f68d3c8b1a094444ec5d9496801005ff8b9b635e597)
                check_type(argname="argument delete_after_days", value=delete_after_days, expected_type=type_hints["delete_after_days"])
                check_type(argname="argument move_to_cold_storage_after_days", value=move_to_cold_storage_after_days, expected_type=type_hints["move_to_cold_storage_after_days"])
                check_type(argname="argument opt_in_to_archive_for_supported_resources", value=opt_in_to_archive_for_supported_resources, expected_type=type_hints["opt_in_to_archive_for_supported_resources"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if delete_after_days is not None:
                self._values["delete_after_days"] = delete_after_days
            if move_to_cold_storage_after_days is not None:
                self._values["move_to_cold_storage_after_days"] = move_to_cold_storage_after_days
            if opt_in_to_archive_for_supported_resources is not None:
                self._values["opt_in_to_archive_for_supported_resources"] = opt_in_to_archive_for_supported_resources

        @builtins.property
        def delete_after_days(self) -> typing.Optional[jsii.Number]:
            '''The number of days after creation that a recovery point is deleted.

            This value must be at least 90 days after the number of days specified in ``MoveToColdStorageAfterDays`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-lifecycleresourcetype.html#cfn-backup-backupplan-lifecycleresourcetype-deleteafterdays
            '''
            result = self._values.get("delete_after_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def move_to_cold_storage_after_days(self) -> typing.Optional[jsii.Number]:
            '''The number of days after creation that a recovery point is moved to cold storage.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-lifecycleresourcetype.html#cfn-backup-backupplan-lifecycleresourcetype-movetocoldstorageafterdays
            '''
            result = self._values.get("move_to_cold_storage_after_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def opt_in_to_archive_for_supported_resources(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If the value is true, your backup plan transitions supported resources to archive (cold) storage tier in accordance with your lifecycle settings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-lifecycleresourcetype.html#cfn-backup-backupplan-lifecycleresourcetype-optintoarchiveforsupportedresources
            '''
            result = self._values.get("opt_in_to_archive_for_supported_resources")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LifecycleResourceTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_backup.mixins.CfnBackupSelectionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "backup_plan_id": "backupPlanId",
        "backup_selection": "backupSelection",
    },
)
class CfnBackupSelectionMixinProps:
    def __init__(
        self,
        *,
        backup_plan_id: typing.Optional[builtins.str] = None,
        backup_selection: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBackupSelectionPropsMixin.BackupSelectionResourceTypeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnBackupSelectionPropsMixin.

        :param backup_plan_id: Uniquely identifies a backup plan.
        :param backup_selection: Specifies the body of a request to assign a set of resources to a backup plan. It includes an array of resources, an optional array of patterns to exclude resources, an optional role to provide access to the AWS service the resource belongs to, and an optional array of tags used to identify a set of resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupselection.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_backup import mixins as backup_mixins
            
            # conditions: Any
            
            cfn_backup_selection_mixin_props = backup_mixins.CfnBackupSelectionMixinProps(
                backup_plan_id="backupPlanId",
                backup_selection=backup_mixins.CfnBackupSelectionPropsMixin.BackupSelectionResourceTypeProperty(
                    conditions=conditions,
                    iam_role_arn="iamRoleArn",
                    list_of_tags=[backup_mixins.CfnBackupSelectionPropsMixin.ConditionResourceTypeProperty(
                        condition_key="conditionKey",
                        condition_type="conditionType",
                        condition_value="conditionValue"
                    )],
                    not_resources=["notResources"],
                    resources=["resources"],
                    selection_name="selectionName"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e66fe88d24bd9cba4a1cf23894b412f1c0a62ac484f972b0ce53538f26659b4f)
            check_type(argname="argument backup_plan_id", value=backup_plan_id, expected_type=type_hints["backup_plan_id"])
            check_type(argname="argument backup_selection", value=backup_selection, expected_type=type_hints["backup_selection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if backup_plan_id is not None:
            self._values["backup_plan_id"] = backup_plan_id
        if backup_selection is not None:
            self._values["backup_selection"] = backup_selection

    @builtins.property
    def backup_plan_id(self) -> typing.Optional[builtins.str]:
        '''Uniquely identifies a backup plan.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupselection.html#cfn-backup-backupselection-backupplanid
        '''
        result = self._values.get("backup_plan_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def backup_selection(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBackupSelectionPropsMixin.BackupSelectionResourceTypeProperty"]]:
        '''Specifies the body of a request to assign a set of resources to a backup plan.

        It includes an array of resources, an optional array of patterns to exclude resources, an optional role to provide access to the AWS service the resource belongs to, and an optional array of tags used to identify a set of resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupselection.html#cfn-backup-backupselection-backupselection
        '''
        result = self._values.get("backup_selection")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBackupSelectionPropsMixin.BackupSelectionResourceTypeProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBackupSelectionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnBackupSelectionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_backup.mixins.CfnBackupSelectionPropsMixin",
):
    '''Specifies a set of resources to assign to a backup plan.

    For a sample CloudFormation template, see the `AWS Backup Developer Guide <https://docs.aws.amazon.com/aws-backup/latest/devguide/assigning-resources.html#assigning-resources-cfn>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupselection.html
    :cloudformationResource: AWS::Backup::BackupSelection
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_backup import mixins as backup_mixins
        
        # conditions: Any
        
        cfn_backup_selection_props_mixin = backup_mixins.CfnBackupSelectionPropsMixin(backup_mixins.CfnBackupSelectionMixinProps(
            backup_plan_id="backupPlanId",
            backup_selection=backup_mixins.CfnBackupSelectionPropsMixin.BackupSelectionResourceTypeProperty(
                conditions=conditions,
                iam_role_arn="iamRoleArn",
                list_of_tags=[backup_mixins.CfnBackupSelectionPropsMixin.ConditionResourceTypeProperty(
                    condition_key="conditionKey",
                    condition_type="conditionType",
                    condition_value="conditionValue"
                )],
                not_resources=["notResources"],
                resources=["resources"],
                selection_name="selectionName"
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnBackupSelectionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Backup::BackupSelection``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d16f7a5ce8e77eab8341119bc680e7449b46efaf45281093bb41e5e5b944d74)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d630695d14edec806f033e6c22077d7ca0bb572dc2cf27a36a6a94b55ecda1ea)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb31847e2bfb8c4c15b051200526df6fe5f4e5dcc1774baeb2faf5c7dbbb657b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnBackupSelectionMixinProps:
        return typing.cast(CfnBackupSelectionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_backup.mixins.CfnBackupSelectionPropsMixin.BackupSelectionResourceTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "conditions": "conditions",
            "iam_role_arn": "iamRoleArn",
            "list_of_tags": "listOfTags",
            "not_resources": "notResources",
            "resources": "resources",
            "selection_name": "selectionName",
        },
    )
    class BackupSelectionResourceTypeProperty:
        def __init__(
            self,
            *,
            conditions: typing.Any = None,
            iam_role_arn: typing.Optional[builtins.str] = None,
            list_of_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBackupSelectionPropsMixin.ConditionResourceTypeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            not_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
            resources: typing.Optional[typing.Sequence[builtins.str]] = None,
            selection_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies an object containing properties used to assign a set of resources to a backup plan.

            :param conditions: A list of conditions that you define to assign resources to your backup plans using tags. For example, ``"StringEquals": { "ConditionKey": "aws:ResourceTag/CreatedByCryo", "ConditionValue": "true" },`` . Condition operators are case sensitive. ``Conditions`` differs from ``ListOfTags`` as follows: - When you specify more than one condition, you only assign the resources that match ALL conditions (using AND logic). - ``Conditions`` supports ``StringEquals`` , ``StringLike`` , ``StringNotEquals`` , and ``StringNotLike`` . ``ListOfTags`` only supports ``StringEquals`` .
            :param iam_role_arn: The ARN of the IAM role that AWS Backup uses to authenticate when backing up the target resource; for example, ``arn:aws:iam::123456789012:role/S3Access`` .
            :param list_of_tags: A list of conditions that you define to assign resources to your backup plans using tags. For example, ``"StringEquals": { "ConditionKey": "aws:ResourceTag/CreatedByCryo", "ConditionValue": "true" },`` . Condition operators are case sensitive. ``ListOfTags`` differs from ``Conditions`` as follows: - When you specify more than one condition, you assign all resources that match AT LEAST ONE condition (using OR logic). - ``ListOfTags`` only supports ``StringEquals`` . ``Conditions`` supports ``StringEquals`` , ``StringLike`` , ``StringNotEquals`` , and ``StringNotLike`` .
            :param not_resources: A list of Amazon Resource Names (ARNs) to exclude from a backup plan. The maximum number of ARNs is 500 without wildcards, or 30 ARNs with wildcards. If you need to exclude many resources from a backup plan, consider a different resource selection strategy, such as assigning only one or a few resource types or refining your resource selection using tags.
            :param resources: An array of strings that contain Amazon Resource Names (ARNs) of resources to assign to a backup plan.
            :param selection_name: The display name of a resource selection document.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupselection-backupselectionresourcetype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_backup import mixins as backup_mixins
                
                # conditions: Any
                
                backup_selection_resource_type_property = backup_mixins.CfnBackupSelectionPropsMixin.BackupSelectionResourceTypeProperty(
                    conditions=conditions,
                    iam_role_arn="iamRoleArn",
                    list_of_tags=[backup_mixins.CfnBackupSelectionPropsMixin.ConditionResourceTypeProperty(
                        condition_key="conditionKey",
                        condition_type="conditionType",
                        condition_value="conditionValue"
                    )],
                    not_resources=["notResources"],
                    resources=["resources"],
                    selection_name="selectionName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5445957c477620010ea3aa0ebf94f59a7aceff6213ba5202eb96fb089af993a8)
                check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
                check_type(argname="argument iam_role_arn", value=iam_role_arn, expected_type=type_hints["iam_role_arn"])
                check_type(argname="argument list_of_tags", value=list_of_tags, expected_type=type_hints["list_of_tags"])
                check_type(argname="argument not_resources", value=not_resources, expected_type=type_hints["not_resources"])
                check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
                check_type(argname="argument selection_name", value=selection_name, expected_type=type_hints["selection_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if conditions is not None:
                self._values["conditions"] = conditions
            if iam_role_arn is not None:
                self._values["iam_role_arn"] = iam_role_arn
            if list_of_tags is not None:
                self._values["list_of_tags"] = list_of_tags
            if not_resources is not None:
                self._values["not_resources"] = not_resources
            if resources is not None:
                self._values["resources"] = resources
            if selection_name is not None:
                self._values["selection_name"] = selection_name

        @builtins.property
        def conditions(self) -> typing.Any:
            '''A list of conditions that you define to assign resources to your backup plans using tags.

            For example, ``"StringEquals": { "ConditionKey": "aws:ResourceTag/CreatedByCryo", "ConditionValue": "true" },`` . Condition operators are case sensitive.

            ``Conditions`` differs from ``ListOfTags`` as follows:

            - When you specify more than one condition, you only assign the resources that match ALL conditions (using AND logic).
            - ``Conditions`` supports ``StringEquals`` , ``StringLike`` , ``StringNotEquals`` , and ``StringNotLike`` . ``ListOfTags`` only supports ``StringEquals`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupselection-backupselectionresourcetype.html#cfn-backup-backupselection-backupselectionresourcetype-conditions
            '''
            result = self._values.get("conditions")
            return typing.cast(typing.Any, result)

        @builtins.property
        def iam_role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the IAM role that AWS Backup uses to authenticate when backing up the target resource;

            for example, ``arn:aws:iam::123456789012:role/S3Access`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupselection-backupselectionresourcetype.html#cfn-backup-backupselection-backupselectionresourcetype-iamrolearn
            '''
            result = self._values.get("iam_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def list_of_tags(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBackupSelectionPropsMixin.ConditionResourceTypeProperty"]]]]:
            '''A list of conditions that you define to assign resources to your backup plans using tags.

            For example, ``"StringEquals": { "ConditionKey": "aws:ResourceTag/CreatedByCryo", "ConditionValue": "true" },`` . Condition operators are case sensitive.

            ``ListOfTags`` differs from ``Conditions`` as follows:

            - When you specify more than one condition, you assign all resources that match AT LEAST ONE condition (using OR logic).
            - ``ListOfTags`` only supports ``StringEquals`` . ``Conditions`` supports ``StringEquals`` , ``StringLike`` , ``StringNotEquals`` , and ``StringNotLike`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupselection-backupselectionresourcetype.html#cfn-backup-backupselection-backupselectionresourcetype-listoftags
            '''
            result = self._values.get("list_of_tags")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBackupSelectionPropsMixin.ConditionResourceTypeProperty"]]]], result)

        @builtins.property
        def not_resources(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of Amazon Resource Names (ARNs) to exclude from a backup plan.

            The maximum number of ARNs is 500 without wildcards, or 30 ARNs with wildcards.

            If you need to exclude many resources from a backup plan, consider a different resource selection strategy, such as assigning only one or a few resource types or refining your resource selection using tags.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupselection-backupselectionresourcetype.html#cfn-backup-backupselection-backupselectionresourcetype-notresources
            '''
            result = self._values.get("not_resources")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def resources(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An array of strings that contain Amazon Resource Names (ARNs) of resources to assign to a backup plan.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupselection-backupselectionresourcetype.html#cfn-backup-backupselection-backupselectionresourcetype-resources
            '''
            result = self._values.get("resources")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def selection_name(self) -> typing.Optional[builtins.str]:
            '''The display name of a resource selection document.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupselection-backupselectionresourcetype.html#cfn-backup-backupselection-backupselectionresourcetype-selectionname
            '''
            result = self._values.get("selection_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BackupSelectionResourceTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_backup.mixins.CfnBackupSelectionPropsMixin.ConditionResourceTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "condition_key": "conditionKey",
            "condition_type": "conditionType",
            "condition_value": "conditionValue",
        },
    )
    class ConditionResourceTypeProperty:
        def __init__(
            self,
            *,
            condition_key: typing.Optional[builtins.str] = None,
            condition_type: typing.Optional[builtins.str] = None,
            condition_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies an object that contains an array of triplets made up of a condition type (such as ``STRINGEQUALS`` ), a key, and a value.

            Conditions are used to filter resources in a selection that is assigned to a backup plan.

            :param condition_key: The key in a key-value pair. For example, in ``"Department": "accounting"`` , ``"Department"`` is the key.
            :param condition_type: An operation, such as ``STRINGEQUALS`` , that is applied to a key-value pair used to filter resources in a selection.
            :param condition_value: The value in a key-value pair. For example, in ``"Department": "accounting"`` , ``"accounting"`` is the value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupselection-conditionresourcetype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_backup import mixins as backup_mixins
                
                condition_resource_type_property = backup_mixins.CfnBackupSelectionPropsMixin.ConditionResourceTypeProperty(
                    condition_key="conditionKey",
                    condition_type="conditionType",
                    condition_value="conditionValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__94d3ae6a933028793e9c703f8aca3cdf1bd0e280a2ed752b344c30a4d77cf6ac)
                check_type(argname="argument condition_key", value=condition_key, expected_type=type_hints["condition_key"])
                check_type(argname="argument condition_type", value=condition_type, expected_type=type_hints["condition_type"])
                check_type(argname="argument condition_value", value=condition_value, expected_type=type_hints["condition_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if condition_key is not None:
                self._values["condition_key"] = condition_key
            if condition_type is not None:
                self._values["condition_type"] = condition_type
            if condition_value is not None:
                self._values["condition_value"] = condition_value

        @builtins.property
        def condition_key(self) -> typing.Optional[builtins.str]:
            '''The key in a key-value pair.

            For example, in ``"Department": "accounting"`` , ``"Department"`` is the key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupselection-conditionresourcetype.html#cfn-backup-backupselection-conditionresourcetype-conditionkey
            '''
            result = self._values.get("condition_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def condition_type(self) -> typing.Optional[builtins.str]:
            '''An operation, such as ``STRINGEQUALS`` , that is applied to a key-value pair used to filter resources in a selection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupselection-conditionresourcetype.html#cfn-backup-backupselection-conditionresourcetype-conditiontype
            '''
            result = self._values.get("condition_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def condition_value(self) -> typing.Optional[builtins.str]:
            '''The value in a key-value pair.

            For example, in ``"Department": "accounting"`` , ``"accounting"`` is the value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupselection-conditionresourcetype.html#cfn-backup-backupselection-conditionresourcetype-conditionvalue
            '''
            result = self._values.get("condition_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConditionResourceTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_backup.mixins.CfnBackupVaultMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_policy": "accessPolicy",
        "backup_vault_name": "backupVaultName",
        "backup_vault_tags": "backupVaultTags",
        "encryption_key_arn": "encryptionKeyArn",
        "lock_configuration": "lockConfiguration",
        "notifications": "notifications",
    },
)
class CfnBackupVaultMixinProps:
    def __init__(
        self,
        *,
        access_policy: typing.Any = None,
        backup_vault_name: typing.Optional[builtins.str] = None,
        backup_vault_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        encryption_key_arn: typing.Optional[builtins.str] = None,
        lock_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBackupVaultPropsMixin.LockConfigurationTypeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        notifications: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBackupVaultPropsMixin.NotificationObjectTypeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnBackupVaultPropsMixin.

        :param access_policy: A resource-based policy that is used to manage access permissions on the target backup vault.
        :param backup_vault_name: The name of a logical container where backups are stored. Backup vaults are identified by names that are unique to the account used to create them and the AWS Region where they are created.
        :param backup_vault_tags: The tags to assign to the backup vault.
        :param encryption_key_arn: A server-side encryption key you can specify to encrypt your backups from services that support full AWS Backup management; for example, ``arn:aws:kms:us-west-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab`` . If you specify a key, you must specify its ARN, not its alias. If you do not specify a key, AWS Backup creates a KMS key for you by default. To learn which AWS Backup services support full AWS Backup management and how AWS Backup handles encryption for backups from services that do not yet support full AWS Backup , see `Encryption for backups in AWS Backup <https://docs.aws.amazon.com/aws-backup/latest/devguide/encryption.html>`_
        :param lock_configuration: Configuration for `AWS Backup Vault Lock <https://docs.aws.amazon.com/aws-backup/latest/devguide/vault-lock.html>`_ .
        :param notifications: The SNS event notifications for the specified backup vault.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupvault.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_backup import mixins as backup_mixins
            
            # access_policy: Any
            
            cfn_backup_vault_mixin_props = backup_mixins.CfnBackupVaultMixinProps(
                access_policy=access_policy,
                backup_vault_name="backupVaultName",
                backup_vault_tags={
                    "backup_vault_tags_key": "backupVaultTags"
                },
                encryption_key_arn="encryptionKeyArn",
                lock_configuration=backup_mixins.CfnBackupVaultPropsMixin.LockConfigurationTypeProperty(
                    changeable_for_days=123,
                    max_retention_days=123,
                    min_retention_days=123
                ),
                notifications=backup_mixins.CfnBackupVaultPropsMixin.NotificationObjectTypeProperty(
                    backup_vault_events=["backupVaultEvents"],
                    sns_topic_arn="snsTopicArn"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dae6b99048b55ef079d526d8d6ed9e5f3c1d3fd4245a74cbf8519c620f9ba5ab)
            check_type(argname="argument access_policy", value=access_policy, expected_type=type_hints["access_policy"])
            check_type(argname="argument backup_vault_name", value=backup_vault_name, expected_type=type_hints["backup_vault_name"])
            check_type(argname="argument backup_vault_tags", value=backup_vault_tags, expected_type=type_hints["backup_vault_tags"])
            check_type(argname="argument encryption_key_arn", value=encryption_key_arn, expected_type=type_hints["encryption_key_arn"])
            check_type(argname="argument lock_configuration", value=lock_configuration, expected_type=type_hints["lock_configuration"])
            check_type(argname="argument notifications", value=notifications, expected_type=type_hints["notifications"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_policy is not None:
            self._values["access_policy"] = access_policy
        if backup_vault_name is not None:
            self._values["backup_vault_name"] = backup_vault_name
        if backup_vault_tags is not None:
            self._values["backup_vault_tags"] = backup_vault_tags
        if encryption_key_arn is not None:
            self._values["encryption_key_arn"] = encryption_key_arn
        if lock_configuration is not None:
            self._values["lock_configuration"] = lock_configuration
        if notifications is not None:
            self._values["notifications"] = notifications

    @builtins.property
    def access_policy(self) -> typing.Any:
        '''A resource-based policy that is used to manage access permissions on the target backup vault.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupvault.html#cfn-backup-backupvault-accesspolicy
        '''
        result = self._values.get("access_policy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def backup_vault_name(self) -> typing.Optional[builtins.str]:
        '''The name of a logical container where backups are stored.

        Backup vaults are identified by names that are unique to the account used to create them and the AWS Region where they are created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupvault.html#cfn-backup-backupvault-backupvaultname
        '''
        result = self._values.get("backup_vault_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def backup_vault_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The tags to assign to the backup vault.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupvault.html#cfn-backup-backupvault-backupvaulttags
        '''
        result = self._values.get("backup_vault_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def encryption_key_arn(self) -> typing.Optional[builtins.str]:
        '''A server-side encryption key you can specify to encrypt your backups from services that support full AWS Backup management;

        for example, ``arn:aws:kms:us-west-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab`` . If you specify a key, you must specify its ARN, not its alias. If you do not specify a key, AWS Backup creates a KMS key for you by default.

        To learn which AWS Backup services support full AWS Backup management and how AWS Backup handles encryption for backups from services that do not yet support full AWS Backup , see `Encryption for backups in AWS Backup <https://docs.aws.amazon.com/aws-backup/latest/devguide/encryption.html>`_

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupvault.html#cfn-backup-backupvault-encryptionkeyarn
        '''
        result = self._values.get("encryption_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lock_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBackupVaultPropsMixin.LockConfigurationTypeProperty"]]:
        '''Configuration for `AWS Backup Vault Lock <https://docs.aws.amazon.com/aws-backup/latest/devguide/vault-lock.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupvault.html#cfn-backup-backupvault-lockconfiguration
        '''
        result = self._values.get("lock_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBackupVaultPropsMixin.LockConfigurationTypeProperty"]], result)

    @builtins.property
    def notifications(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBackupVaultPropsMixin.NotificationObjectTypeProperty"]]:
        '''The SNS event notifications for the specified backup vault.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupvault.html#cfn-backup-backupvault-notifications
        '''
        result = self._values.get("notifications")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBackupVaultPropsMixin.NotificationObjectTypeProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBackupVaultMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnBackupVaultPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_backup.mixins.CfnBackupVaultPropsMixin",
):
    '''Creates a logical container where backups are stored.

    A ``CreateBackupVault`` request includes a name, optionally one or more resource tags, an encryption key, and a request ID.

    Do not include sensitive data, such as passport numbers, in the name of a backup vault.

    For a sample CloudFormation template, see the `AWS Backup Developer Guide <https://docs.aws.amazon.com/aws-backup/latest/devguide/assigning-resources.html#assigning-resources-cfn>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupvault.html
    :cloudformationResource: AWS::Backup::BackupVault
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_backup import mixins as backup_mixins
        
        # access_policy: Any
        
        cfn_backup_vault_props_mixin = backup_mixins.CfnBackupVaultPropsMixin(backup_mixins.CfnBackupVaultMixinProps(
            access_policy=access_policy,
            backup_vault_name="backupVaultName",
            backup_vault_tags={
                "backup_vault_tags_key": "backupVaultTags"
            },
            encryption_key_arn="encryptionKeyArn",
            lock_configuration=backup_mixins.CfnBackupVaultPropsMixin.LockConfigurationTypeProperty(
                changeable_for_days=123,
                max_retention_days=123,
                min_retention_days=123
            ),
            notifications=backup_mixins.CfnBackupVaultPropsMixin.NotificationObjectTypeProperty(
                backup_vault_events=["backupVaultEvents"],
                sns_topic_arn="snsTopicArn"
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnBackupVaultMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Backup::BackupVault``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__427786b5415a8501d76140d99d3a7505d2372b792b3a798d0cda6804db1b24f8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1887d96ce0cc9927afa93dc01d3f2a7a4479b8f283af45c6e4a66b35aa2e4e7a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__298d887174a9ca2dccf0d7af332cbade9f3f36b252478797a2df6747f34979e0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnBackupVaultMixinProps:
        return typing.cast(CfnBackupVaultMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_backup.mixins.CfnBackupVaultPropsMixin.LockConfigurationTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "changeable_for_days": "changeableForDays",
            "max_retention_days": "maxRetentionDays",
            "min_retention_days": "minRetentionDays",
        },
    )
    class LockConfigurationTypeProperty:
        def __init__(
            self,
            *,
            changeable_for_days: typing.Optional[jsii.Number] = None,
            max_retention_days: typing.Optional[jsii.Number] = None,
            min_retention_days: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The ``LockConfigurationType`` property type specifies configuration for `AWS Backup Vault Lock <https://docs.aws.amazon.com/aws-backup/latest/devguide/vault-lock.html>`_ .

            :param changeable_for_days: The AWS Backup Vault Lock configuration that specifies the number of days before the lock date. For example, setting ``ChangeableForDays`` to 30 on Jan. 1, 2022 at 8pm UTC will set the lock date to Jan. 31, 2022 at 8pm UTC. AWS Backup enforces a 72-hour cooling-off period before Vault Lock takes effect and becomes immutable. Therefore, you must set ``ChangeableForDays`` to 3 or greater. Before the lock date, you can delete Vault Lock from the vault using ``DeleteBackupVaultLockConfiguration`` or change the Vault Lock configuration using ``PutBackupVaultLockConfiguration`` . On and after the lock date, the Vault Lock becomes immutable and cannot be changed or deleted. If this parameter is not specified, you can delete Vault Lock from the vault using ``DeleteBackupVaultLockConfiguration`` or change the Vault Lock configuration using ``PutBackupVaultLockConfiguration`` at any time.
            :param max_retention_days: The AWS Backup Vault Lock configuration that specifies the maximum retention period that the vault retains its recovery points. This setting can be useful if, for example, your organization's policies require you to destroy certain data after retaining it for four years (1460 days). If this parameter is not included, Vault Lock does not enforce a maximum retention period on the recovery points in the vault. If this parameter is included without a value, Vault Lock will not enforce a maximum retention period. If this parameter is specified, any backup or copy job to the vault must have a lifecycle policy with a retention period equal to or shorter than the maximum retention period. If the job's retention period is longer than that maximum retention period, then the vault fails the backup or copy job, and you should either modify your lifecycle settings or use a different vault. Recovery points already saved in the vault prior to Vault Lock are not affected.
            :param min_retention_days: The AWS Backup Vault Lock configuration that specifies the minimum retention period that the vault retains its recovery points. This setting can be useful if, for example, your organization's policies require you to retain certain data for at least seven years (2555 days). If this parameter is not specified, Vault Lock will not enforce a minimum retention period. If this parameter is specified, any backup or copy job to the vault must have a lifecycle policy with a retention period equal to or longer than the minimum retention period. If the job's retention period is shorter than that minimum retention period, then the vault fails that backup or copy job, and you should either modify your lifecycle settings or use a different vault. Recovery points already saved in the vault prior to Vault Lock are not affected.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupvault-lockconfigurationtype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_backup import mixins as backup_mixins
                
                lock_configuration_type_property = backup_mixins.CfnBackupVaultPropsMixin.LockConfigurationTypeProperty(
                    changeable_for_days=123,
                    max_retention_days=123,
                    min_retention_days=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a2e9c992d1044bda2fbc3b7d316c2cce8727569b1e31807dd50984f832adabe9)
                check_type(argname="argument changeable_for_days", value=changeable_for_days, expected_type=type_hints["changeable_for_days"])
                check_type(argname="argument max_retention_days", value=max_retention_days, expected_type=type_hints["max_retention_days"])
                check_type(argname="argument min_retention_days", value=min_retention_days, expected_type=type_hints["min_retention_days"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if changeable_for_days is not None:
                self._values["changeable_for_days"] = changeable_for_days
            if max_retention_days is not None:
                self._values["max_retention_days"] = max_retention_days
            if min_retention_days is not None:
                self._values["min_retention_days"] = min_retention_days

        @builtins.property
        def changeable_for_days(self) -> typing.Optional[jsii.Number]:
            '''The AWS Backup Vault Lock configuration that specifies the number of days before the lock date.

            For example, setting ``ChangeableForDays`` to 30 on Jan. 1, 2022 at 8pm UTC will set the lock date to Jan. 31, 2022 at 8pm UTC.

            AWS Backup enforces a 72-hour cooling-off period before Vault Lock takes effect and becomes immutable. Therefore, you must set ``ChangeableForDays`` to 3 or greater.

            Before the lock date, you can delete Vault Lock from the vault using ``DeleteBackupVaultLockConfiguration`` or change the Vault Lock configuration using ``PutBackupVaultLockConfiguration`` . On and after the lock date, the Vault Lock becomes immutable and cannot be changed or deleted.

            If this parameter is not specified, you can delete Vault Lock from the vault using ``DeleteBackupVaultLockConfiguration`` or change the Vault Lock configuration using ``PutBackupVaultLockConfiguration`` at any time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupvault-lockconfigurationtype.html#cfn-backup-backupvault-lockconfigurationtype-changeablefordays
            '''
            result = self._values.get("changeable_for_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_retention_days(self) -> typing.Optional[jsii.Number]:
            '''The AWS Backup Vault Lock configuration that specifies the maximum retention period that the vault retains its recovery points.

            This setting can be useful if, for example, your organization's policies require you to destroy certain data after retaining it for four years (1460 days).

            If this parameter is not included, Vault Lock does not enforce a maximum retention period on the recovery points in the vault. If this parameter is included without a value, Vault Lock will not enforce a maximum retention period.

            If this parameter is specified, any backup or copy job to the vault must have a lifecycle policy with a retention period equal to or shorter than the maximum retention period. If the job's retention period is longer than that maximum retention period, then the vault fails the backup or copy job, and you should either modify your lifecycle settings or use a different vault. Recovery points already saved in the vault prior to Vault Lock are not affected.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupvault-lockconfigurationtype.html#cfn-backup-backupvault-lockconfigurationtype-maxretentiondays
            '''
            result = self._values.get("max_retention_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min_retention_days(self) -> typing.Optional[jsii.Number]:
            '''The AWS Backup Vault Lock configuration that specifies the minimum retention period that the vault retains its recovery points.

            This setting can be useful if, for example, your organization's policies require you to retain certain data for at least seven years (2555 days).

            If this parameter is not specified, Vault Lock will not enforce a minimum retention period.

            If this parameter is specified, any backup or copy job to the vault must have a lifecycle policy with a retention period equal to or longer than the minimum retention period. If the job's retention period is shorter than that minimum retention period, then the vault fails that backup or copy job, and you should either modify your lifecycle settings or use a different vault. Recovery points already saved in the vault prior to Vault Lock are not affected.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupvault-lockconfigurationtype.html#cfn-backup-backupvault-lockconfigurationtype-minretentiondays
            '''
            result = self._values.get("min_retention_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LockConfigurationTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_backup.mixins.CfnBackupVaultPropsMixin.NotificationObjectTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "backup_vault_events": "backupVaultEvents",
            "sns_topic_arn": "snsTopicArn",
        },
    )
    class NotificationObjectTypeProperty:
        def __init__(
            self,
            *,
            backup_vault_events: typing.Optional[typing.Sequence[builtins.str]] = None,
            sns_topic_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies an object containing SNS event notification properties for the target backup vault.

            :param backup_vault_events: An array of events that indicate the status of jobs to back up resources to the backup vault. For valid events, see `BackupVaultEvents <https://docs.aws.amazon.com/aws-backup/latest/devguide/API_PutBackupVaultNotifications.html#API_PutBackupVaultNotifications_RequestSyntax>`_ in the *AWS Backup API Guide* .
            :param sns_topic_arn: An ARN that uniquely identifies an Amazon Simple Notification Service (Amazon SNS) topic; for example, ``arn:aws:sns:us-west-2:111122223333:MyTopic`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupvault-notificationobjecttype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_backup import mixins as backup_mixins
                
                notification_object_type_property = backup_mixins.CfnBackupVaultPropsMixin.NotificationObjectTypeProperty(
                    backup_vault_events=["backupVaultEvents"],
                    sns_topic_arn="snsTopicArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__aa0f487b6836a98326372782594ba4c7e54cdecbfb04df36526d47843c7ef595)
                check_type(argname="argument backup_vault_events", value=backup_vault_events, expected_type=type_hints["backup_vault_events"])
                check_type(argname="argument sns_topic_arn", value=sns_topic_arn, expected_type=type_hints["sns_topic_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if backup_vault_events is not None:
                self._values["backup_vault_events"] = backup_vault_events
            if sns_topic_arn is not None:
                self._values["sns_topic_arn"] = sns_topic_arn

        @builtins.property
        def backup_vault_events(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An array of events that indicate the status of jobs to back up resources to the backup vault.

            For valid events, see `BackupVaultEvents <https://docs.aws.amazon.com/aws-backup/latest/devguide/API_PutBackupVaultNotifications.html#API_PutBackupVaultNotifications_RequestSyntax>`_ in the *AWS Backup API Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupvault-notificationobjecttype.html#cfn-backup-backupvault-notificationobjecttype-backupvaultevents
            '''
            result = self._values.get("backup_vault_events")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def sns_topic_arn(self) -> typing.Optional[builtins.str]:
            '''An ARN that uniquely identifies an Amazon Simple Notification Service (Amazon SNS) topic;

            for example, ``arn:aws:sns:us-west-2:111122223333:MyTopic`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupvault-notificationobjecttype.html#cfn-backup-backupvault-notificationobjecttype-snstopicarn
            '''
            result = self._values.get("sns_topic_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NotificationObjectTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_backup.mixins.CfnFrameworkMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "framework_controls": "frameworkControls",
        "framework_description": "frameworkDescription",
        "framework_name": "frameworkName",
        "framework_tags": "frameworkTags",
    },
)
class CfnFrameworkMixinProps:
    def __init__(
        self,
        *,
        framework_controls: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFrameworkPropsMixin.FrameworkControlProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        framework_description: typing.Optional[builtins.str] = None,
        framework_name: typing.Optional[builtins.str] = None,
        framework_tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnFrameworkPropsMixin.

        :param framework_controls: Contains detailed information about all of the controls of a framework. Each framework must contain at least one control.
        :param framework_description: An optional description of the framework with a maximum 1,024 characters.
        :param framework_name: The unique name of a framework. This name is between 1 and 256 characters, starting with a letter, and consisting of letters (a-z, A-Z), numbers (0-9), and underscores (_).
        :param framework_tags: The tags to assign to your framework.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-framework.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_backup import mixins as backup_mixins
            
            # control_scope: Any
            
            cfn_framework_mixin_props = backup_mixins.CfnFrameworkMixinProps(
                framework_controls=[backup_mixins.CfnFrameworkPropsMixin.FrameworkControlProperty(
                    control_input_parameters=[backup_mixins.CfnFrameworkPropsMixin.ControlInputParameterProperty(
                        parameter_name="parameterName",
                        parameter_value="parameterValue"
                    )],
                    control_name="controlName",
                    control_scope=control_scope
                )],
                framework_description="frameworkDescription",
                framework_name="frameworkName",
                framework_tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64afb43307664ba019223293fc2c53b56c619db24827386c4a44b75e588a7c62)
            check_type(argname="argument framework_controls", value=framework_controls, expected_type=type_hints["framework_controls"])
            check_type(argname="argument framework_description", value=framework_description, expected_type=type_hints["framework_description"])
            check_type(argname="argument framework_name", value=framework_name, expected_type=type_hints["framework_name"])
            check_type(argname="argument framework_tags", value=framework_tags, expected_type=type_hints["framework_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if framework_controls is not None:
            self._values["framework_controls"] = framework_controls
        if framework_description is not None:
            self._values["framework_description"] = framework_description
        if framework_name is not None:
            self._values["framework_name"] = framework_name
        if framework_tags is not None:
            self._values["framework_tags"] = framework_tags

    @builtins.property
    def framework_controls(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFrameworkPropsMixin.FrameworkControlProperty"]]]]:
        '''Contains detailed information about all of the controls of a framework.

        Each framework must contain at least one control.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-framework.html#cfn-backup-framework-frameworkcontrols
        '''
        result = self._values.get("framework_controls")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFrameworkPropsMixin.FrameworkControlProperty"]]]], result)

    @builtins.property
    def framework_description(self) -> typing.Optional[builtins.str]:
        '''An optional description of the framework with a maximum 1,024 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-framework.html#cfn-backup-framework-frameworkdescription
        '''
        result = self._values.get("framework_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def framework_name(self) -> typing.Optional[builtins.str]:
        '''The unique name of a framework.

        This name is between 1 and 256 characters, starting with a letter, and consisting of letters (a-z, A-Z), numbers (0-9), and underscores (_).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-framework.html#cfn-backup-framework-frameworkname
        '''
        result = self._values.get("framework_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def framework_tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags to assign to your framework.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-framework.html#cfn-backup-framework-frameworktags
        '''
        result = self._values.get("framework_tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFrameworkMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnFrameworkPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_backup.mixins.CfnFrameworkPropsMixin",
):
    '''Creates a framework with one or more controls.

    A framework is a collection of controls that you can use to evaluate your backup practices. By using pre-built customizable controls to define your policies, you can evaluate whether your backup practices comply with your policies and which resources are not yet in compliance.

    For a sample CloudFormation template, see the `AWS Backup Developer Guide <https://docs.aws.amazon.com/aws-backup/latest/devguide/bam-cfn-integration.html#bam-cfn-frameworks-template>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-framework.html
    :cloudformationResource: AWS::Backup::Framework
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_backup import mixins as backup_mixins
        
        # control_scope: Any
        
        cfn_framework_props_mixin = backup_mixins.CfnFrameworkPropsMixin(backup_mixins.CfnFrameworkMixinProps(
            framework_controls=[backup_mixins.CfnFrameworkPropsMixin.FrameworkControlProperty(
                control_input_parameters=[backup_mixins.CfnFrameworkPropsMixin.ControlInputParameterProperty(
                    parameter_name="parameterName",
                    parameter_value="parameterValue"
                )],
                control_name="controlName",
                control_scope=control_scope
            )],
            framework_description="frameworkDescription",
            framework_name="frameworkName",
            framework_tags=[CfnTag(
                key="key",
                value="value"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnFrameworkMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Backup::Framework``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c281e43247da2422c011bcd54900c8ff8e5acd11e3f9de6e0b3ed9ac0c09040)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0eb723e29c1039bc5ec07fc302fbdec28b178061c0e03c5032d22efd2a29bf1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2a6735206fe0575c856f8ba3edbd0db289756584faa684737433229862d19f2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnFrameworkMixinProps:
        return typing.cast(CfnFrameworkMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_backup.mixins.CfnFrameworkPropsMixin.ControlInputParameterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "parameter_name": "parameterName",
            "parameter_value": "parameterValue",
        },
    )
    class ControlInputParameterProperty:
        def __init__(
            self,
            *,
            parameter_name: typing.Optional[builtins.str] = None,
            parameter_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The parameters for a control.

            A control can have zero, one, or more than one parameter. An example of a control with two parameters is: "backup plan frequency is at least ``daily`` and the retention period is at least ``1 year`` ". The first parameter is ``daily`` . The second parameter is ``1 year`` .

            :param parameter_name: The name of a parameter, for example, ``BackupPlanFrequency`` .
            :param parameter_value: The value of parameter, for example, ``hourly`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-framework-controlinputparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_backup import mixins as backup_mixins
                
                control_input_parameter_property = backup_mixins.CfnFrameworkPropsMixin.ControlInputParameterProperty(
                    parameter_name="parameterName",
                    parameter_value="parameterValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__73e2c34fffd8bca3db301cd9225e5f957748c31af12e340668559ede3c9a870f)
                check_type(argname="argument parameter_name", value=parameter_name, expected_type=type_hints["parameter_name"])
                check_type(argname="argument parameter_value", value=parameter_value, expected_type=type_hints["parameter_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if parameter_name is not None:
                self._values["parameter_name"] = parameter_name
            if parameter_value is not None:
                self._values["parameter_value"] = parameter_value

        @builtins.property
        def parameter_name(self) -> typing.Optional[builtins.str]:
            '''The name of a parameter, for example, ``BackupPlanFrequency`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-framework-controlinputparameter.html#cfn-backup-framework-controlinputparameter-parametername
            '''
            result = self._values.get("parameter_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def parameter_value(self) -> typing.Optional[builtins.str]:
            '''The value of parameter, for example, ``hourly`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-framework-controlinputparameter.html#cfn-backup-framework-controlinputparameter-parametervalue
            '''
            result = self._values.get("parameter_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ControlInputParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_backup.mixins.CfnFrameworkPropsMixin.FrameworkControlProperty",
        jsii_struct_bases=[],
        name_mapping={
            "control_input_parameters": "controlInputParameters",
            "control_name": "controlName",
            "control_scope": "controlScope",
        },
    )
    class FrameworkControlProperty:
        def __init__(
            self,
            *,
            control_input_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFrameworkPropsMixin.ControlInputParameterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            control_name: typing.Optional[builtins.str] = None,
            control_scope: typing.Any = None,
        ) -> None:
            '''Contains detailed information about all of the controls of a framework.

            Each framework must contain at least one control.

            :param control_input_parameters: The name/value pairs.
            :param control_name: The name of a control. This name is between 1 and 256 characters.
            :param control_scope: The scope of a control. The control scope defines what the control will evaluate. Three examples of control scopes are: a specific backup plan, all backup plans with a specific tag, or all backup plans. For more information, see ```ControlScope`` . <https://docs.aws.amazon.com/aws-backup/latest/devguide/API_ControlScope.html>`_

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-framework-frameworkcontrol.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_backup import mixins as backup_mixins
                
                # control_scope: Any
                
                framework_control_property = backup_mixins.CfnFrameworkPropsMixin.FrameworkControlProperty(
                    control_input_parameters=[backup_mixins.CfnFrameworkPropsMixin.ControlInputParameterProperty(
                        parameter_name="parameterName",
                        parameter_value="parameterValue"
                    )],
                    control_name="controlName",
                    control_scope=control_scope
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__edb50c6a1e59c9f4f26a8249fd1982d7f273b7ad0b2207a9e302da139bc98535)
                check_type(argname="argument control_input_parameters", value=control_input_parameters, expected_type=type_hints["control_input_parameters"])
                check_type(argname="argument control_name", value=control_name, expected_type=type_hints["control_name"])
                check_type(argname="argument control_scope", value=control_scope, expected_type=type_hints["control_scope"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if control_input_parameters is not None:
                self._values["control_input_parameters"] = control_input_parameters
            if control_name is not None:
                self._values["control_name"] = control_name
            if control_scope is not None:
                self._values["control_scope"] = control_scope

        @builtins.property
        def control_input_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFrameworkPropsMixin.ControlInputParameterProperty"]]]]:
            '''The name/value pairs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-framework-frameworkcontrol.html#cfn-backup-framework-frameworkcontrol-controlinputparameters
            '''
            result = self._values.get("control_input_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFrameworkPropsMixin.ControlInputParameterProperty"]]]], result)

        @builtins.property
        def control_name(self) -> typing.Optional[builtins.str]:
            '''The name of a control.

            This name is between 1 and 256 characters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-framework-frameworkcontrol.html#cfn-backup-framework-frameworkcontrol-controlname
            '''
            result = self._values.get("control_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def control_scope(self) -> typing.Any:
            '''The scope of a control.

            The control scope defines what the control will evaluate. Three examples of control scopes are: a specific backup plan, all backup plans with a specific tag, or all backup plans.

            For more information, see ```ControlScope`` . <https://docs.aws.amazon.com/aws-backup/latest/devguide/API_ControlScope.html>`_

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-framework-frameworkcontrol.html#cfn-backup-framework-frameworkcontrol-controlscope
            '''
            result = self._values.get("control_scope")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FrameworkControlProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_backup.mixins.CfnLogicallyAirGappedBackupVaultMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_policy": "accessPolicy",
        "backup_vault_name": "backupVaultName",
        "backup_vault_tags": "backupVaultTags",
        "encryption_key_arn": "encryptionKeyArn",
        "max_retention_days": "maxRetentionDays",
        "min_retention_days": "minRetentionDays",
        "mpa_approval_team_arn": "mpaApprovalTeamArn",
        "notifications": "notifications",
    },
)
class CfnLogicallyAirGappedBackupVaultMixinProps:
    def __init__(
        self,
        *,
        access_policy: typing.Any = None,
        backup_vault_name: typing.Optional[builtins.str] = None,
        backup_vault_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        encryption_key_arn: typing.Optional[builtins.str] = None,
        max_retention_days: typing.Optional[jsii.Number] = None,
        min_retention_days: typing.Optional[jsii.Number] = None,
        mpa_approval_team_arn: typing.Optional[builtins.str] = None,
        notifications: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLogicallyAirGappedBackupVaultPropsMixin.NotificationObjectTypeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnLogicallyAirGappedBackupVaultPropsMixin.

        :param access_policy: The backup vault access policy document in JSON format.
        :param backup_vault_name: The name of a logical container where backups are stored. Logically air-gapped backup vaults are identified by names that are unique to the account used to create them and the Region where they are created.
        :param backup_vault_tags: The tags to assign to the vault.
        :param encryption_key_arn: The server-side encryption key that is used to protect your backups; for example, ``arn:aws:kms:us-west-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab`` .
        :param max_retention_days: The maximum retention period that the vault retains its recovery points.
        :param min_retention_days: This setting specifies the minimum retention period that the vault retains its recovery points. The minimum value accepted is 7 days.
        :param mpa_approval_team_arn: 
        :param notifications: Returns event notifications for the specified backup vault.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-logicallyairgappedbackupvault.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_backup import mixins as backup_mixins
            
            # access_policy: Any
            
            cfn_logically_air_gapped_backup_vault_mixin_props = backup_mixins.CfnLogicallyAirGappedBackupVaultMixinProps(
                access_policy=access_policy,
                backup_vault_name="backupVaultName",
                backup_vault_tags={
                    "backup_vault_tags_key": "backupVaultTags"
                },
                encryption_key_arn="encryptionKeyArn",
                max_retention_days=123,
                min_retention_days=123,
                mpa_approval_team_arn="mpaApprovalTeamArn",
                notifications=backup_mixins.CfnLogicallyAirGappedBackupVaultPropsMixin.NotificationObjectTypeProperty(
                    backup_vault_events=["backupVaultEvents"],
                    sns_topic_arn="snsTopicArn"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0a89d891ba9c98b8da62805bcb1f9059e77b326370f48b4bac19e5507c248f9)
            check_type(argname="argument access_policy", value=access_policy, expected_type=type_hints["access_policy"])
            check_type(argname="argument backup_vault_name", value=backup_vault_name, expected_type=type_hints["backup_vault_name"])
            check_type(argname="argument backup_vault_tags", value=backup_vault_tags, expected_type=type_hints["backup_vault_tags"])
            check_type(argname="argument encryption_key_arn", value=encryption_key_arn, expected_type=type_hints["encryption_key_arn"])
            check_type(argname="argument max_retention_days", value=max_retention_days, expected_type=type_hints["max_retention_days"])
            check_type(argname="argument min_retention_days", value=min_retention_days, expected_type=type_hints["min_retention_days"])
            check_type(argname="argument mpa_approval_team_arn", value=mpa_approval_team_arn, expected_type=type_hints["mpa_approval_team_arn"])
            check_type(argname="argument notifications", value=notifications, expected_type=type_hints["notifications"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_policy is not None:
            self._values["access_policy"] = access_policy
        if backup_vault_name is not None:
            self._values["backup_vault_name"] = backup_vault_name
        if backup_vault_tags is not None:
            self._values["backup_vault_tags"] = backup_vault_tags
        if encryption_key_arn is not None:
            self._values["encryption_key_arn"] = encryption_key_arn
        if max_retention_days is not None:
            self._values["max_retention_days"] = max_retention_days
        if min_retention_days is not None:
            self._values["min_retention_days"] = min_retention_days
        if mpa_approval_team_arn is not None:
            self._values["mpa_approval_team_arn"] = mpa_approval_team_arn
        if notifications is not None:
            self._values["notifications"] = notifications

    @builtins.property
    def access_policy(self) -> typing.Any:
        '''The backup vault access policy document in JSON format.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-logicallyairgappedbackupvault.html#cfn-backup-logicallyairgappedbackupvault-accesspolicy
        '''
        result = self._values.get("access_policy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def backup_vault_name(self) -> typing.Optional[builtins.str]:
        '''The name of a logical container where backups are stored.

        Logically air-gapped backup vaults are identified by names that are unique to the account used to create them and the Region where they are created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-logicallyairgappedbackupvault.html#cfn-backup-logicallyairgappedbackupvault-backupvaultname
        '''
        result = self._values.get("backup_vault_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def backup_vault_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The tags to assign to the vault.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-logicallyairgappedbackupvault.html#cfn-backup-logicallyairgappedbackupvault-backupvaulttags
        '''
        result = self._values.get("backup_vault_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def encryption_key_arn(self) -> typing.Optional[builtins.str]:
        '''The server-side encryption key that is used to protect your backups;

        for example, ``arn:aws:kms:us-west-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-logicallyairgappedbackupvault.html#cfn-backup-logicallyairgappedbackupvault-encryptionkeyarn
        '''
        result = self._values.get("encryption_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_retention_days(self) -> typing.Optional[jsii.Number]:
        '''The maximum retention period that the vault retains its recovery points.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-logicallyairgappedbackupvault.html#cfn-backup-logicallyairgappedbackupvault-maxretentiondays
        '''
        result = self._values.get("max_retention_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_retention_days(self) -> typing.Optional[jsii.Number]:
        '''This setting specifies the minimum retention period that the vault retains its recovery points.

        The minimum value accepted is 7 days.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-logicallyairgappedbackupvault.html#cfn-backup-logicallyairgappedbackupvault-minretentiondays
        '''
        result = self._values.get("min_retention_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def mpa_approval_team_arn(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-logicallyairgappedbackupvault.html#cfn-backup-logicallyairgappedbackupvault-mpaapprovalteamarn
        '''
        result = self._values.get("mpa_approval_team_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notifications(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLogicallyAirGappedBackupVaultPropsMixin.NotificationObjectTypeProperty"]]:
        '''Returns event notifications for the specified backup vault.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-logicallyairgappedbackupvault.html#cfn-backup-logicallyairgappedbackupvault-notifications
        '''
        result = self._values.get("notifications")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLogicallyAirGappedBackupVaultPropsMixin.NotificationObjectTypeProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLogicallyAirGappedBackupVaultMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLogicallyAirGappedBackupVaultPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_backup.mixins.CfnLogicallyAirGappedBackupVaultPropsMixin",
):
    '''Creates a logical container to where backups may be copied.

    This request includes a name, the Region, the maximum number of retention days, the minimum number of retention days, and optionally can include tags and a creator request ID.
    .. epigraph::

       Do not include sensitive data, such as passport numbers, in the name of a backup vault.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-logicallyairgappedbackupvault.html
    :cloudformationResource: AWS::Backup::LogicallyAirGappedBackupVault
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_backup import mixins as backup_mixins
        
        # access_policy: Any
        
        cfn_logically_air_gapped_backup_vault_props_mixin = backup_mixins.CfnLogicallyAirGappedBackupVaultPropsMixin(backup_mixins.CfnLogicallyAirGappedBackupVaultMixinProps(
            access_policy=access_policy,
            backup_vault_name="backupVaultName",
            backup_vault_tags={
                "backup_vault_tags_key": "backupVaultTags"
            },
            encryption_key_arn="encryptionKeyArn",
            max_retention_days=123,
            min_retention_days=123,
            mpa_approval_team_arn="mpaApprovalTeamArn",
            notifications=backup_mixins.CfnLogicallyAirGappedBackupVaultPropsMixin.NotificationObjectTypeProperty(
                backup_vault_events=["backupVaultEvents"],
                sns_topic_arn="snsTopicArn"
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnLogicallyAirGappedBackupVaultMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Backup::LogicallyAirGappedBackupVault``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c480369cdde00896e4ebab5026f4f9a973accd1e672113e71dbda5960c2f9ce)
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
            type_hints = typing.get_type_hints(_typecheckingstub__de6e043262cde5253ac48d4d8ee23b292501d40251efcbaa82009fdd58679836)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26e83a04ff3c2b9d94fd5c1b6673d1d1f52e1a825b24accf759918c981e2d666)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLogicallyAirGappedBackupVaultMixinProps:
        return typing.cast(CfnLogicallyAirGappedBackupVaultMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_backup.mixins.CfnLogicallyAirGappedBackupVaultPropsMixin.NotificationObjectTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "backup_vault_events": "backupVaultEvents",
            "sns_topic_arn": "snsTopicArn",
        },
    )
    class NotificationObjectTypeProperty:
        def __init__(
            self,
            *,
            backup_vault_events: typing.Optional[typing.Sequence[builtins.str]] = None,
            sns_topic_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param backup_vault_events: An array of events that indicate the status of jobs to back up resources to the backup vault.
            :param sns_topic_arn: The Amazon Resource Name (ARN) that specifies the topic for a backup vault’s events; for example, ``arn:aws:sns:us-west-2:111122223333:MyVaultTopic`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-logicallyairgappedbackupvault-notificationobjecttype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_backup import mixins as backup_mixins
                
                notification_object_type_property = backup_mixins.CfnLogicallyAirGappedBackupVaultPropsMixin.NotificationObjectTypeProperty(
                    backup_vault_events=["backupVaultEvents"],
                    sns_topic_arn="snsTopicArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__51da8e513a32f33acd3f441f25fa1e6103c4343c9c8120ab91bed1596c02660c)
                check_type(argname="argument backup_vault_events", value=backup_vault_events, expected_type=type_hints["backup_vault_events"])
                check_type(argname="argument sns_topic_arn", value=sns_topic_arn, expected_type=type_hints["sns_topic_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if backup_vault_events is not None:
                self._values["backup_vault_events"] = backup_vault_events
            if sns_topic_arn is not None:
                self._values["sns_topic_arn"] = sns_topic_arn

        @builtins.property
        def backup_vault_events(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An array of events that indicate the status of jobs to back up resources to the backup vault.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-logicallyairgappedbackupvault-notificationobjecttype.html#cfn-backup-logicallyairgappedbackupvault-notificationobjecttype-backupvaultevents
            '''
            result = self._values.get("backup_vault_events")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def sns_topic_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) that specifies the topic for a backup vault’s events;

            for example, ``arn:aws:sns:us-west-2:111122223333:MyVaultTopic`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-logicallyairgappedbackupvault-notificationobjecttype.html#cfn-backup-logicallyairgappedbackupvault-notificationobjecttype-snstopicarn
            '''
            result = self._values.get("sns_topic_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NotificationObjectTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_backup.mixins.CfnReportPlanMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "report_delivery_channel": "reportDeliveryChannel",
        "report_plan_description": "reportPlanDescription",
        "report_plan_name": "reportPlanName",
        "report_plan_tags": "reportPlanTags",
        "report_setting": "reportSetting",
    },
)
class CfnReportPlanMixinProps:
    def __init__(
        self,
        *,
        report_delivery_channel: typing.Any = None,
        report_plan_description: typing.Optional[builtins.str] = None,
        report_plan_name: typing.Optional[builtins.str] = None,
        report_plan_tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        report_setting: typing.Any = None,
    ) -> None:
        '''Properties for CfnReportPlanPropsMixin.

        :param report_delivery_channel: Contains information about where and how to deliver your reports, specifically your Amazon S3 bucket name, S3 key prefix, and the formats of your reports.
        :param report_plan_description: An optional description of the report plan with a maximum 1,024 characters.
        :param report_plan_name: The unique name of the report plan. This name is between 1 and 256 characters starting with a letter, and consisting of letters (a-z, A-Z), numbers (0-9), and underscores (_).
        :param report_plan_tags: The tags to assign to your report plan.
        :param report_setting: Identifies the report template for the report. Reports are built using a report template. The report templates are:. ``RESOURCE_COMPLIANCE_REPORT | CONTROL_COMPLIANCE_REPORT | BACKUP_JOB_REPORT | COPY_JOB_REPORT | RESTORE_JOB_REPORT`` If the report template is ``RESOURCE_COMPLIANCE_REPORT`` or ``CONTROL_COMPLIANCE_REPORT`` , this API resource also describes the report coverage by AWS Regions and frameworks.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-reportplan.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_backup import mixins as backup_mixins
            
            # report_delivery_channel: Any
            # report_setting: Any
            
            cfn_report_plan_mixin_props = backup_mixins.CfnReportPlanMixinProps(
                report_delivery_channel=report_delivery_channel,
                report_plan_description="reportPlanDescription",
                report_plan_name="reportPlanName",
                report_plan_tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                report_setting=report_setting
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c293bad169d8d720bae5c3bceaf74305f1ae6a82bf784df267e10f4d76a3ba2f)
            check_type(argname="argument report_delivery_channel", value=report_delivery_channel, expected_type=type_hints["report_delivery_channel"])
            check_type(argname="argument report_plan_description", value=report_plan_description, expected_type=type_hints["report_plan_description"])
            check_type(argname="argument report_plan_name", value=report_plan_name, expected_type=type_hints["report_plan_name"])
            check_type(argname="argument report_plan_tags", value=report_plan_tags, expected_type=type_hints["report_plan_tags"])
            check_type(argname="argument report_setting", value=report_setting, expected_type=type_hints["report_setting"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if report_delivery_channel is not None:
            self._values["report_delivery_channel"] = report_delivery_channel
        if report_plan_description is not None:
            self._values["report_plan_description"] = report_plan_description
        if report_plan_name is not None:
            self._values["report_plan_name"] = report_plan_name
        if report_plan_tags is not None:
            self._values["report_plan_tags"] = report_plan_tags
        if report_setting is not None:
            self._values["report_setting"] = report_setting

    @builtins.property
    def report_delivery_channel(self) -> typing.Any:
        '''Contains information about where and how to deliver your reports, specifically your Amazon S3 bucket name, S3 key prefix, and the formats of your reports.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-reportplan.html#cfn-backup-reportplan-reportdeliverychannel
        '''
        result = self._values.get("report_delivery_channel")
        return typing.cast(typing.Any, result)

    @builtins.property
    def report_plan_description(self) -> typing.Optional[builtins.str]:
        '''An optional description of the report plan with a maximum 1,024 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-reportplan.html#cfn-backup-reportplan-reportplandescription
        '''
        result = self._values.get("report_plan_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def report_plan_name(self) -> typing.Optional[builtins.str]:
        '''The unique name of the report plan.

        This name is between 1 and 256 characters starting with a letter, and consisting of letters (a-z, A-Z), numbers (0-9), and underscores (_).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-reportplan.html#cfn-backup-reportplan-reportplanname
        '''
        result = self._values.get("report_plan_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def report_plan_tags(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags to assign to your report plan.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-reportplan.html#cfn-backup-reportplan-reportplantags
        '''
        result = self._values.get("report_plan_tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def report_setting(self) -> typing.Any:
        '''Identifies the report template for the report. Reports are built using a report template. The report templates are:.

        ``RESOURCE_COMPLIANCE_REPORT | CONTROL_COMPLIANCE_REPORT | BACKUP_JOB_REPORT | COPY_JOB_REPORT | RESTORE_JOB_REPORT``

        If the report template is ``RESOURCE_COMPLIANCE_REPORT`` or ``CONTROL_COMPLIANCE_REPORT`` , this API resource also describes the report coverage by AWS Regions and frameworks.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-reportplan.html#cfn-backup-reportplan-reportsetting
        '''
        result = self._values.get("report_setting")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnReportPlanMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnReportPlanPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_backup.mixins.CfnReportPlanPropsMixin",
):
    '''Creates a report plan.

    A report plan is a document that contains information about the contents of the report and where AWS Backup will deliver it.

    If you call ``CreateReportPlan`` with a plan that already exists, you receive an ``AlreadyExistsException`` exception.

    For a sample CloudFormation template, see the `AWS Backup Developer Guide <https://docs.aws.amazon.com/aws-backup/latest/devguide/assigning-resources.html#assigning-resources-cfn>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-reportplan.html
    :cloudformationResource: AWS::Backup::ReportPlan
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_backup import mixins as backup_mixins
        
        # report_delivery_channel: Any
        # report_setting: Any
        
        cfn_report_plan_props_mixin = backup_mixins.CfnReportPlanPropsMixin(backup_mixins.CfnReportPlanMixinProps(
            report_delivery_channel=report_delivery_channel,
            report_plan_description="reportPlanDescription",
            report_plan_name="reportPlanName",
            report_plan_tags=[CfnTag(
                key="key",
                value="value"
            )],
            report_setting=report_setting
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnReportPlanMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Backup::ReportPlan``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa2e1b23d15adeee4b6c3f426cfff83adcd82f792cb02c293a2a3541455f5cf8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e0e4d2d3d9bfd17d933aad7c8818e8a7407499730f3b3b3fe9559331882dae6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cea986c9ddcc043aae45fe357bdc385650f8aead47104332ab327aacd107678a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnReportPlanMixinProps:
        return typing.cast(CfnReportPlanMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_backup.mixins.CfnReportPlanPropsMixin.ReportDeliveryChannelProperty",
        jsii_struct_bases=[],
        name_mapping={
            "formats": "formats",
            "s3_bucket_name": "s3BucketName",
            "s3_key_prefix": "s3KeyPrefix",
        },
    )
    class ReportDeliveryChannelProperty:
        def __init__(
            self,
            *,
            formats: typing.Optional[typing.Sequence[builtins.str]] = None,
            s3_bucket_name: typing.Optional[builtins.str] = None,
            s3_key_prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information from your report plan about where to deliver your reports, specifically your Amazon S3 bucket name, S3 key prefix, and the formats of your reports.

            :param formats: The format of your reports: ``CSV`` , ``JSON`` , or both. If not specified, the default format is ``CSV`` .
            :param s3_bucket_name: The unique name of the S3 bucket that receives your reports.
            :param s3_key_prefix: The prefix for where AWS Backup Audit Manager delivers your reports to Amazon S3. The prefix is this part of the following path: s3://your-bucket-name/ ``prefix`` /Backup/us-west-2/year/month/day/report-name. If not specified, there is no prefix.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-reportplan-reportdeliverychannel.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_backup import mixins as backup_mixins
                
                report_delivery_channel_property = backup_mixins.CfnReportPlanPropsMixin.ReportDeliveryChannelProperty(
                    formats=["formats"],
                    s3_bucket_name="s3BucketName",
                    s3_key_prefix="s3KeyPrefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2c7fcf3920b70cba059812d37416686328721ea4e26500e42115f767fc99ca4f)
                check_type(argname="argument formats", value=formats, expected_type=type_hints["formats"])
                check_type(argname="argument s3_bucket_name", value=s3_bucket_name, expected_type=type_hints["s3_bucket_name"])
                check_type(argname="argument s3_key_prefix", value=s3_key_prefix, expected_type=type_hints["s3_key_prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if formats is not None:
                self._values["formats"] = formats
            if s3_bucket_name is not None:
                self._values["s3_bucket_name"] = s3_bucket_name
            if s3_key_prefix is not None:
                self._values["s3_key_prefix"] = s3_key_prefix

        @builtins.property
        def formats(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The format of your reports: ``CSV`` , ``JSON`` , or both.

            If not specified, the default format is ``CSV`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-reportplan-reportdeliverychannel.html#cfn-backup-reportplan-reportdeliverychannel-formats
            '''
            result = self._values.get("formats")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def s3_bucket_name(self) -> typing.Optional[builtins.str]:
            '''The unique name of the S3 bucket that receives your reports.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-reportplan-reportdeliverychannel.html#cfn-backup-reportplan-reportdeliverychannel-s3bucketname
            '''
            result = self._values.get("s3_bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_key_prefix(self) -> typing.Optional[builtins.str]:
            '''The prefix for where AWS Backup Audit Manager delivers your reports to Amazon S3.

            The prefix is this part of the following path: s3://your-bucket-name/ ``prefix`` /Backup/us-west-2/year/month/day/report-name. If not specified, there is no prefix.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-reportplan-reportdeliverychannel.html#cfn-backup-reportplan-reportdeliverychannel-s3keyprefix
            '''
            result = self._values.get("s3_key_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReportDeliveryChannelProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_backup.mixins.CfnReportPlanPropsMixin.ReportSettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "accounts": "accounts",
            "framework_arns": "frameworkArns",
            "organization_units": "organizationUnits",
            "regions": "regions",
            "report_template": "reportTemplate",
        },
    )
    class ReportSettingProperty:
        def __init__(
            self,
            *,
            accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
            framework_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
            organization_units: typing.Optional[typing.Sequence[builtins.str]] = None,
            regions: typing.Optional[typing.Sequence[builtins.str]] = None,
            report_template: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains detailed information about a report setting.

            :param accounts: These are the accounts to be included in the report. Use string value of ``ROOT`` to include all organizational units.
            :param framework_arns: The Amazon Resource Names (ARNs) of the frameworks a report covers.
            :param organization_units: These are the Organizational Units to be included in the report.
            :param regions: These are the Regions to be included in the report. Use the wildcard as the string value to include all Regions.
            :param report_template: Identifies the report template for the report. Reports are built using a report template. The report templates are:. ``RESOURCE_COMPLIANCE_REPORT | CONTROL_COMPLIANCE_REPORT | BACKUP_JOB_REPORT | COPY_JOB_REPORT | RESTORE_JOB_REPORT | SCAN_JOB_REPORT``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-reportplan-reportsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_backup import mixins as backup_mixins
                
                report_setting_property = backup_mixins.CfnReportPlanPropsMixin.ReportSettingProperty(
                    accounts=["accounts"],
                    framework_arns=["frameworkArns"],
                    organization_units=["organizationUnits"],
                    regions=["regions"],
                    report_template="reportTemplate"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a265c9fb3afe50f573a7ac01096c931e2fae7505cee5e1f1657c2b4da7b40f89)
                check_type(argname="argument accounts", value=accounts, expected_type=type_hints["accounts"])
                check_type(argname="argument framework_arns", value=framework_arns, expected_type=type_hints["framework_arns"])
                check_type(argname="argument organization_units", value=organization_units, expected_type=type_hints["organization_units"])
                check_type(argname="argument regions", value=regions, expected_type=type_hints["regions"])
                check_type(argname="argument report_template", value=report_template, expected_type=type_hints["report_template"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if accounts is not None:
                self._values["accounts"] = accounts
            if framework_arns is not None:
                self._values["framework_arns"] = framework_arns
            if organization_units is not None:
                self._values["organization_units"] = organization_units
            if regions is not None:
                self._values["regions"] = regions
            if report_template is not None:
                self._values["report_template"] = report_template

        @builtins.property
        def accounts(self) -> typing.Optional[typing.List[builtins.str]]:
            '''These are the accounts to be included in the report.

            Use string value of ``ROOT`` to include all organizational units.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-reportplan-reportsetting.html#cfn-backup-reportplan-reportsetting-accounts
            '''
            result = self._values.get("accounts")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def framework_arns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The Amazon Resource Names (ARNs) of the frameworks a report covers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-reportplan-reportsetting.html#cfn-backup-reportplan-reportsetting-frameworkarns
            '''
            result = self._values.get("framework_arns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def organization_units(self) -> typing.Optional[typing.List[builtins.str]]:
            '''These are the Organizational Units to be included in the report.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-reportplan-reportsetting.html#cfn-backup-reportplan-reportsetting-organizationunits
            '''
            result = self._values.get("organization_units")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def regions(self) -> typing.Optional[typing.List[builtins.str]]:
            '''These are the Regions to be included in the report.

            Use the wildcard as the string value to include all Regions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-reportplan-reportsetting.html#cfn-backup-reportplan-reportsetting-regions
            '''
            result = self._values.get("regions")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def report_template(self) -> typing.Optional[builtins.str]:
            '''Identifies the report template for the report. Reports are built using a report template. The report templates are:.

            ``RESOURCE_COMPLIANCE_REPORT | CONTROL_COMPLIANCE_REPORT | BACKUP_JOB_REPORT | COPY_JOB_REPORT | RESTORE_JOB_REPORT | SCAN_JOB_REPORT``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-reportplan-reportsetting.html#cfn-backup-reportplan-reportsetting-reporttemplate
            '''
            result = self._values.get("report_template")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReportSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_backup.mixins.CfnRestoreTestingPlanMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "recovery_point_selection": "recoveryPointSelection",
        "restore_testing_plan_name": "restoreTestingPlanName",
        "schedule_expression": "scheduleExpression",
        "schedule_expression_timezone": "scheduleExpressionTimezone",
        "start_window_hours": "startWindowHours",
        "tags": "tags",
    },
)
class CfnRestoreTestingPlanMixinProps:
    def __init__(
        self,
        *,
        recovery_point_selection: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRestoreTestingPlanPropsMixin.RestoreTestingRecoveryPointSelectionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        restore_testing_plan_name: typing.Optional[builtins.str] = None,
        schedule_expression: typing.Optional[builtins.str] = None,
        schedule_expression_timezone: typing.Optional[builtins.str] = None,
        start_window_hours: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnRestoreTestingPlanPropsMixin.

        :param recovery_point_selection: The specified criteria to assign a set of resources, such as recovery point types or backup vaults.
        :param restore_testing_plan_name: The RestoreTestingPlanName is a unique string that is the name of the restore testing plan. This cannot be changed after creation, and it must consist of only alphanumeric characters and underscores.
        :param schedule_expression: A CRON expression in specified timezone when a restore testing plan is executed. When no CRON expression is provided, AWS Backup will use the default expression ``cron(0 5 ? * * *)`` .
        :param schedule_expression_timezone: Optional. This is the timezone in which the schedule expression is set. By default, ScheduleExpressions are in UTC. You can modify this to a specified timezone.
        :param start_window_hours: Defaults to 24 hours. A value in hours after a restore test is scheduled before a job will be canceled if it doesn't start successfully. This value is optional. If this value is included, this parameter has a maximum value of 168 hours (one week).
        :param tags: Optional tags to include. A tag is a key-value pair you can use to manage, filter, and search for your resources. Allowed characters include UTF-8 letters,numbers, spaces, and the following characters: ``+ - = . _ : /.``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-restoretestingplan.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_backup import mixins as backup_mixins
            
            cfn_restore_testing_plan_mixin_props = backup_mixins.CfnRestoreTestingPlanMixinProps(
                recovery_point_selection=backup_mixins.CfnRestoreTestingPlanPropsMixin.RestoreTestingRecoveryPointSelectionProperty(
                    algorithm="algorithm",
                    exclude_vaults=["excludeVaults"],
                    include_vaults=["includeVaults"],
                    recovery_point_types=["recoveryPointTypes"],
                    selection_window_days=123
                ),
                restore_testing_plan_name="restoreTestingPlanName",
                schedule_expression="scheduleExpression",
                schedule_expression_timezone="scheduleExpressionTimezone",
                start_window_hours=123,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1c9d019e568e3fcfbad25fab5d9d716c651470a08864736e376fa9c26e54a57)
            check_type(argname="argument recovery_point_selection", value=recovery_point_selection, expected_type=type_hints["recovery_point_selection"])
            check_type(argname="argument restore_testing_plan_name", value=restore_testing_plan_name, expected_type=type_hints["restore_testing_plan_name"])
            check_type(argname="argument schedule_expression", value=schedule_expression, expected_type=type_hints["schedule_expression"])
            check_type(argname="argument schedule_expression_timezone", value=schedule_expression_timezone, expected_type=type_hints["schedule_expression_timezone"])
            check_type(argname="argument start_window_hours", value=start_window_hours, expected_type=type_hints["start_window_hours"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if recovery_point_selection is not None:
            self._values["recovery_point_selection"] = recovery_point_selection
        if restore_testing_plan_name is not None:
            self._values["restore_testing_plan_name"] = restore_testing_plan_name
        if schedule_expression is not None:
            self._values["schedule_expression"] = schedule_expression
        if schedule_expression_timezone is not None:
            self._values["schedule_expression_timezone"] = schedule_expression_timezone
        if start_window_hours is not None:
            self._values["start_window_hours"] = start_window_hours
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def recovery_point_selection(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRestoreTestingPlanPropsMixin.RestoreTestingRecoveryPointSelectionProperty"]]:
        '''The specified criteria to assign a set of resources, such as recovery point types or backup vaults.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-restoretestingplan.html#cfn-backup-restoretestingplan-recoverypointselection
        '''
        result = self._values.get("recovery_point_selection")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRestoreTestingPlanPropsMixin.RestoreTestingRecoveryPointSelectionProperty"]], result)

    @builtins.property
    def restore_testing_plan_name(self) -> typing.Optional[builtins.str]:
        '''The RestoreTestingPlanName is a unique string that is the name of the restore testing plan.

        This cannot be changed after creation, and it must consist of only alphanumeric characters and underscores.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-restoretestingplan.html#cfn-backup-restoretestingplan-restoretestingplanname
        '''
        result = self._values.get("restore_testing_plan_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule_expression(self) -> typing.Optional[builtins.str]:
        '''A CRON expression in specified timezone when a restore testing plan is executed.

        When no CRON expression is provided, AWS Backup will use the default expression ``cron(0 5 ? * * *)`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-restoretestingplan.html#cfn-backup-restoretestingplan-scheduleexpression
        '''
        result = self._values.get("schedule_expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule_expression_timezone(self) -> typing.Optional[builtins.str]:
        '''Optional.

        This is the timezone in which the schedule expression is set. By default, ScheduleExpressions are in UTC. You can modify this to a specified timezone.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-restoretestingplan.html#cfn-backup-restoretestingplan-scheduleexpressiontimezone
        '''
        result = self._values.get("schedule_expression_timezone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_window_hours(self) -> typing.Optional[jsii.Number]:
        '''Defaults to 24 hours.

        A value in hours after a restore test is scheduled before a job will be canceled if it doesn't start successfully. This value is optional. If this value is included, this parameter has a maximum value of 168 hours (one week).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-restoretestingplan.html#cfn-backup-restoretestingplan-startwindowhours
        '''
        result = self._values.get("start_window_hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Optional tags to include.

        A tag is a key-value pair you can use to manage, filter, and search for your resources. Allowed characters include UTF-8 letters,numbers, spaces, and the following characters: ``+ - = . _ : /.``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-restoretestingplan.html#cfn-backup-restoretestingplan-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRestoreTestingPlanMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnRestoreTestingPlanPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_backup.mixins.CfnRestoreTestingPlanPropsMixin",
):
    '''Creates a restore testing plan.

    The first of two steps to create a restore testing plan. After this request is successful, finish the procedure using CreateRestoreTestingSelection.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-restoretestingplan.html
    :cloudformationResource: AWS::Backup::RestoreTestingPlan
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_backup import mixins as backup_mixins
        
        cfn_restore_testing_plan_props_mixin = backup_mixins.CfnRestoreTestingPlanPropsMixin(backup_mixins.CfnRestoreTestingPlanMixinProps(
            recovery_point_selection=backup_mixins.CfnRestoreTestingPlanPropsMixin.RestoreTestingRecoveryPointSelectionProperty(
                algorithm="algorithm",
                exclude_vaults=["excludeVaults"],
                include_vaults=["includeVaults"],
                recovery_point_types=["recoveryPointTypes"],
                selection_window_days=123
            ),
            restore_testing_plan_name="restoreTestingPlanName",
            schedule_expression="scheduleExpression",
            schedule_expression_timezone="scheduleExpressionTimezone",
            start_window_hours=123,
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
        props: typing.Union[CfnRestoreTestingPlanMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Backup::RestoreTestingPlan``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d58346e7976909cab3c1ff52f1b7e7342654ef2ace75d5408b49a8266fcaba04)
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
            type_hints = typing.get_type_hints(_typecheckingstub__10d05ee1c5d11e222a0c4c879e2cee2f25983ae6cabe7678114983f24e356694)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4138f05abd72584f4563a2a2dd1be99ec37376f5508d618c15fb193c267232eb)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnRestoreTestingPlanMixinProps:
        return typing.cast(CfnRestoreTestingPlanMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_backup.mixins.CfnRestoreTestingPlanPropsMixin.RestoreTestingRecoveryPointSelectionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "algorithm": "algorithm",
            "exclude_vaults": "excludeVaults",
            "include_vaults": "includeVaults",
            "recovery_point_types": "recoveryPointTypes",
            "selection_window_days": "selectionWindowDays",
        },
    )
    class RestoreTestingRecoveryPointSelectionProperty:
        def __init__(
            self,
            *,
            algorithm: typing.Optional[builtins.str] = None,
            exclude_vaults: typing.Optional[typing.Sequence[builtins.str]] = None,
            include_vaults: typing.Optional[typing.Sequence[builtins.str]] = None,
            recovery_point_types: typing.Optional[typing.Sequence[builtins.str]] = None,
            selection_window_days: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''``RecoveryPointSelection`` has five parameters (three required and two optional).

            The values you specify determine which recovery point is included in the restore test. You must indicate with ``Algorithm`` if you want the latest recovery point within your ``SelectionWindowDays`` or if you want a random recovery point, and you must indicate through ``IncludeVaults`` from which vaults the recovery points can be chosen.

            ``Algorithm`` ( *required* ) Valid values: " ``LATEST_WITHIN_WINDOW`` " or " ``RANDOM_WITHIN_WINDOW`` ".

            ``Recovery point types`` ( *required* ) Valid values: " ``SNAPSHOT`` " and/or " ``CONTINUOUS`` ". Include ``SNAPSHOT`` to restore only snapshot recovery points; include ``CONTINUOUS`` to restore continuous recovery points (point in time restore / PITR); use both to restore either a snapshot or a continuous recovery point. The recovery point will be determined by the value for ``Algorithm`` .

            ``IncludeVaults`` ( *required* ). You must include one or more backup vaults. Use the wildcard ["*"] or specific ARNs.

            ``SelectionWindowDays`` ( *optional* ) Value must be an integer (in days) from 1 to 365. If not included, the value defaults to ``30`` .

            ``ExcludeVaults`` ( *optional* ). You can choose to input one or more specific backup vault ARNs to exclude those vaults' contents from restore eligibility. Or, you can include a list of selectors. If this parameter and its value are not included, it defaults to empty list.

            :param algorithm: Acceptable values include "LATEST_WITHIN_WINDOW" or "RANDOM_WITHIN_WINDOW".
            :param exclude_vaults: Accepted values include specific ARNs or list of selectors. Defaults to empty list if not listed.
            :param include_vaults: Accepted values include wildcard ["*"] or by specific ARNs or ARN wilcard replacement ["arn:aws:backup:us-west-2:123456789012:backup-vault:asdf", ...] ["arn:aws:backup:*:*:backup-vault:asdf-*", ...].
            :param recovery_point_types: These are the types of recovery points. Include ``SNAPSHOT`` to restore only snapshot recovery points; include ``CONTINUOUS`` to restore continuous recovery points (point in time restore / PITR); use both to restore either a snapshot or a continuous recovery point. The recovery point will be determined by the value for ``Algorithm`` .
            :param selection_window_days: Accepted values are integers from 1 to 365.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-restoretestingplan-restoretestingrecoverypointselection.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_backup import mixins as backup_mixins
                
                restore_testing_recovery_point_selection_property = backup_mixins.CfnRestoreTestingPlanPropsMixin.RestoreTestingRecoveryPointSelectionProperty(
                    algorithm="algorithm",
                    exclude_vaults=["excludeVaults"],
                    include_vaults=["includeVaults"],
                    recovery_point_types=["recoveryPointTypes"],
                    selection_window_days=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b0d1a68f81af2ead9a0c51ca626c061e2aca432d752e052072fd80fb2611fca1)
                check_type(argname="argument algorithm", value=algorithm, expected_type=type_hints["algorithm"])
                check_type(argname="argument exclude_vaults", value=exclude_vaults, expected_type=type_hints["exclude_vaults"])
                check_type(argname="argument include_vaults", value=include_vaults, expected_type=type_hints["include_vaults"])
                check_type(argname="argument recovery_point_types", value=recovery_point_types, expected_type=type_hints["recovery_point_types"])
                check_type(argname="argument selection_window_days", value=selection_window_days, expected_type=type_hints["selection_window_days"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if algorithm is not None:
                self._values["algorithm"] = algorithm
            if exclude_vaults is not None:
                self._values["exclude_vaults"] = exclude_vaults
            if include_vaults is not None:
                self._values["include_vaults"] = include_vaults
            if recovery_point_types is not None:
                self._values["recovery_point_types"] = recovery_point_types
            if selection_window_days is not None:
                self._values["selection_window_days"] = selection_window_days

        @builtins.property
        def algorithm(self) -> typing.Optional[builtins.str]:
            '''Acceptable values include "LATEST_WITHIN_WINDOW" or "RANDOM_WITHIN_WINDOW".

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-restoretestingplan-restoretestingrecoverypointselection.html#cfn-backup-restoretestingplan-restoretestingrecoverypointselection-algorithm
            '''
            result = self._values.get("algorithm")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def exclude_vaults(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Accepted values include specific ARNs or list of selectors.

            Defaults to empty list if not listed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-restoretestingplan-restoretestingrecoverypointselection.html#cfn-backup-restoretestingplan-restoretestingrecoverypointselection-excludevaults
            '''
            result = self._values.get("exclude_vaults")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def include_vaults(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Accepted values include wildcard ["*"] or by specific ARNs or ARN wilcard replacement ["arn:aws:backup:us-west-2:123456789012:backup-vault:asdf", ...] ["arn:aws:backup:*:*:backup-vault:asdf-*", ...].

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-restoretestingplan-restoretestingrecoverypointselection.html#cfn-backup-restoretestingplan-restoretestingrecoverypointselection-includevaults
            '''
            result = self._values.get("include_vaults")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def recovery_point_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''These are the types of recovery points.

            Include ``SNAPSHOT`` to restore only snapshot recovery points; include ``CONTINUOUS`` to restore continuous recovery points (point in time restore / PITR); use both to restore either a snapshot or a continuous recovery point. The recovery point will be determined by the value for ``Algorithm`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-restoretestingplan-restoretestingrecoverypointselection.html#cfn-backup-restoretestingplan-restoretestingrecoverypointselection-recoverypointtypes
            '''
            result = self._values.get("recovery_point_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def selection_window_days(self) -> typing.Optional[jsii.Number]:
            '''Accepted values are integers from 1 to 365.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-restoretestingplan-restoretestingrecoverypointselection.html#cfn-backup-restoretestingplan-restoretestingrecoverypointselection-selectionwindowdays
            '''
            result = self._values.get("selection_window_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RestoreTestingRecoveryPointSelectionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_backup.mixins.CfnRestoreTestingSelectionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "iam_role_arn": "iamRoleArn",
        "protected_resource_arns": "protectedResourceArns",
        "protected_resource_conditions": "protectedResourceConditions",
        "protected_resource_type": "protectedResourceType",
        "restore_metadata_overrides": "restoreMetadataOverrides",
        "restore_testing_plan_name": "restoreTestingPlanName",
        "restore_testing_selection_name": "restoreTestingSelectionName",
        "validation_window_hours": "validationWindowHours",
    },
)
class CfnRestoreTestingSelectionMixinProps:
    def __init__(
        self,
        *,
        iam_role_arn: typing.Optional[builtins.str] = None,
        protected_resource_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        protected_resource_conditions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRestoreTestingSelectionPropsMixin.ProtectedResourceConditionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        protected_resource_type: typing.Optional[builtins.str] = None,
        restore_metadata_overrides: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        restore_testing_plan_name: typing.Optional[builtins.str] = None,
        restore_testing_selection_name: typing.Optional[builtins.str] = None,
        validation_window_hours: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties for CfnRestoreTestingSelectionPropsMixin.

        :param iam_role_arn: The Amazon Resource Name (ARN) of the IAM role that AWS Backup uses to create the target resource; for example: ``arn:aws:iam::123456789012:role/S3Access`` .
        :param protected_resource_arns: You can include specific ARNs, such as ``ProtectedResourceArns: ["arn:aws:...", "arn:aws:..."]`` or you can include a wildcard: ``ProtectedResourceArns: ["*"]`` , but not both.
        :param protected_resource_conditions: In a resource testing selection, this parameter filters by specific conditions such as ``StringEquals`` or ``StringNotEquals`` .
        :param protected_resource_type: The type of AWS resource included in a resource testing selection; for example, an Amazon EBS volume or an Amazon RDS database.
        :param restore_metadata_overrides: You can override certain restore metadata keys by including the parameter ``RestoreMetadataOverrides`` in the body of ``RestoreTestingSelection`` . Key values are not case sensitive. See the complete list of `restore testing inferred metadata <https://docs.aws.amazon.com/aws-backup/latest/devguide/restore-testing-inferred-metadata.html>`_ .
        :param restore_testing_plan_name: Unique string that is the name of the restore testing plan. The name cannot be changed after creation. The name must consist of only alphanumeric characters and underscores. Maximum length is 50.
        :param restore_testing_selection_name: The unique name of the restore testing selection that belongs to the related restore testing plan. The name consists of only alphanumeric characters and underscores. Maximum length is 50.
        :param validation_window_hours: This is amount of hours (1 to 168) available to run a validation script on the data. The data will be deleted upon the completion of the validation script or the end of the specified retention period, whichever comes first.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-restoretestingselection.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_backup import mixins as backup_mixins
            
            cfn_restore_testing_selection_mixin_props = backup_mixins.CfnRestoreTestingSelectionMixinProps(
                iam_role_arn="iamRoleArn",
                protected_resource_arns=["protectedResourceArns"],
                protected_resource_conditions=backup_mixins.CfnRestoreTestingSelectionPropsMixin.ProtectedResourceConditionsProperty(
                    string_equals=[backup_mixins.CfnRestoreTestingSelectionPropsMixin.KeyValueProperty(
                        key="key",
                        value="value"
                    )],
                    string_not_equals=[backup_mixins.CfnRestoreTestingSelectionPropsMixin.KeyValueProperty(
                        key="key",
                        value="value"
                    )]
                ),
                protected_resource_type="protectedResourceType",
                restore_metadata_overrides={
                    "restore_metadata_overrides_key": "restoreMetadataOverrides"
                },
                restore_testing_plan_name="restoreTestingPlanName",
                restore_testing_selection_name="restoreTestingSelectionName",
                validation_window_hours=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c37768d11f47ebe24237b830579a26cebb0f43e35e9d9796c8fd1ce5691c2a8b)
            check_type(argname="argument iam_role_arn", value=iam_role_arn, expected_type=type_hints["iam_role_arn"])
            check_type(argname="argument protected_resource_arns", value=protected_resource_arns, expected_type=type_hints["protected_resource_arns"])
            check_type(argname="argument protected_resource_conditions", value=protected_resource_conditions, expected_type=type_hints["protected_resource_conditions"])
            check_type(argname="argument protected_resource_type", value=protected_resource_type, expected_type=type_hints["protected_resource_type"])
            check_type(argname="argument restore_metadata_overrides", value=restore_metadata_overrides, expected_type=type_hints["restore_metadata_overrides"])
            check_type(argname="argument restore_testing_plan_name", value=restore_testing_plan_name, expected_type=type_hints["restore_testing_plan_name"])
            check_type(argname="argument restore_testing_selection_name", value=restore_testing_selection_name, expected_type=type_hints["restore_testing_selection_name"])
            check_type(argname="argument validation_window_hours", value=validation_window_hours, expected_type=type_hints["validation_window_hours"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if iam_role_arn is not None:
            self._values["iam_role_arn"] = iam_role_arn
        if protected_resource_arns is not None:
            self._values["protected_resource_arns"] = protected_resource_arns
        if protected_resource_conditions is not None:
            self._values["protected_resource_conditions"] = protected_resource_conditions
        if protected_resource_type is not None:
            self._values["protected_resource_type"] = protected_resource_type
        if restore_metadata_overrides is not None:
            self._values["restore_metadata_overrides"] = restore_metadata_overrides
        if restore_testing_plan_name is not None:
            self._values["restore_testing_plan_name"] = restore_testing_plan_name
        if restore_testing_selection_name is not None:
            self._values["restore_testing_selection_name"] = restore_testing_selection_name
        if validation_window_hours is not None:
            self._values["validation_window_hours"] = validation_window_hours

    @builtins.property
    def iam_role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the IAM role that AWS Backup uses to create the target resource;

        for example: ``arn:aws:iam::123456789012:role/S3Access`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-restoretestingselection.html#cfn-backup-restoretestingselection-iamrolearn
        '''
        result = self._values.get("iam_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protected_resource_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''You can include specific ARNs, such as ``ProtectedResourceArns: ["arn:aws:...", "arn:aws:..."]`` or you can include a wildcard: ``ProtectedResourceArns: ["*"]`` , but not both.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-restoretestingselection.html#cfn-backup-restoretestingselection-protectedresourcearns
        '''
        result = self._values.get("protected_resource_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def protected_resource_conditions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRestoreTestingSelectionPropsMixin.ProtectedResourceConditionsProperty"]]:
        '''In a resource testing selection, this parameter filters by specific conditions such as ``StringEquals`` or ``StringNotEquals`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-restoretestingselection.html#cfn-backup-restoretestingselection-protectedresourceconditions
        '''
        result = self._values.get("protected_resource_conditions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRestoreTestingSelectionPropsMixin.ProtectedResourceConditionsProperty"]], result)

    @builtins.property
    def protected_resource_type(self) -> typing.Optional[builtins.str]:
        '''The type of AWS resource included in a resource testing selection;

        for example, an Amazon EBS volume or an Amazon RDS database.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-restoretestingselection.html#cfn-backup-restoretestingselection-protectedresourcetype
        '''
        result = self._values.get("protected_resource_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def restore_metadata_overrides(
        self,
    ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
        '''You can override certain restore metadata keys by including the parameter ``RestoreMetadataOverrides`` in the body of ``RestoreTestingSelection`` .

        Key values are not case sensitive.

        See the complete list of `restore testing inferred metadata <https://docs.aws.amazon.com/aws-backup/latest/devguide/restore-testing-inferred-metadata.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-restoretestingselection.html#cfn-backup-restoretestingselection-restoremetadataoverrides
        '''
        result = self._values.get("restore_metadata_overrides")
        return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def restore_testing_plan_name(self) -> typing.Optional[builtins.str]:
        '''Unique string that is the name of the restore testing plan.

        The name cannot be changed after creation. The name must consist of only alphanumeric characters and underscores. Maximum length is 50.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-restoretestingselection.html#cfn-backup-restoretestingselection-restoretestingplanname
        '''
        result = self._values.get("restore_testing_plan_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def restore_testing_selection_name(self) -> typing.Optional[builtins.str]:
        '''The unique name of the restore testing selection that belongs to the related restore testing plan.

        The name consists of only alphanumeric characters and underscores. Maximum length is 50.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-restoretestingselection.html#cfn-backup-restoretestingselection-restoretestingselectionname
        '''
        result = self._values.get("restore_testing_selection_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def validation_window_hours(self) -> typing.Optional[jsii.Number]:
        '''This is amount of hours (1 to 168) available to run a validation script on the data.

        The data will be deleted upon the completion of the validation script or the end of the specified retention period, whichever comes first.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-restoretestingselection.html#cfn-backup-restoretestingselection-validationwindowhours
        '''
        result = self._values.get("validation_window_hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRestoreTestingSelectionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnRestoreTestingSelectionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_backup.mixins.CfnRestoreTestingSelectionPropsMixin",
):
    '''This request can be sent after CreateRestoreTestingPlan request returns successfully.

    This is the second part of creating a resource testing plan, and it must be completed sequentially.

    This consists of ``RestoreTestingSelectionName`` , ``ProtectedResourceType`` , and one of the following:

    - ``ProtectedResourceArns``
    - ``ProtectedResourceConditions``

    Each protected resource type can have one single value.

    A restore testing selection can include a wildcard value ("*") for ``ProtectedResourceArns`` along with ``ProtectedResourceConditions`` . Alternatively, you can include up to 30 specific protected resource ARNs in ``ProtectedResourceArns`` .

    Cannot select by both protected resource types AND specific ARNs. Request will fail if both are included.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-restoretestingselection.html
    :cloudformationResource: AWS::Backup::RestoreTestingSelection
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_backup import mixins as backup_mixins
        
        cfn_restore_testing_selection_props_mixin = backup_mixins.CfnRestoreTestingSelectionPropsMixin(backup_mixins.CfnRestoreTestingSelectionMixinProps(
            iam_role_arn="iamRoleArn",
            protected_resource_arns=["protectedResourceArns"],
            protected_resource_conditions=backup_mixins.CfnRestoreTestingSelectionPropsMixin.ProtectedResourceConditionsProperty(
                string_equals=[backup_mixins.CfnRestoreTestingSelectionPropsMixin.KeyValueProperty(
                    key="key",
                    value="value"
                )],
                string_not_equals=[backup_mixins.CfnRestoreTestingSelectionPropsMixin.KeyValueProperty(
                    key="key",
                    value="value"
                )]
            ),
            protected_resource_type="protectedResourceType",
            restore_metadata_overrides={
                "restore_metadata_overrides_key": "restoreMetadataOverrides"
            },
            restore_testing_plan_name="restoreTestingPlanName",
            restore_testing_selection_name="restoreTestingSelectionName",
            validation_window_hours=123
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnRestoreTestingSelectionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Backup::RestoreTestingSelection``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3e7f9dfcc90eec6cc7d015dd880828356ee9959f339bb4ec9e8a70f0a29cddf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b562b0b8391b3e5779898f7859f9b7f6f49319d3dbf15c4f407c75c4d9276b25)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00eda2ddffdeaeb06597833e9ff3e2e893b44dede0f8d4c99796ed5b9aff64df)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnRestoreTestingSelectionMixinProps:
        return typing.cast(CfnRestoreTestingSelectionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_backup.mixins.CfnRestoreTestingSelectionPropsMixin.KeyValueProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class KeyValueProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Pair of two related strings.

            Allowed characters are letters, white space, and numbers that can be represented in UTF-8 and the following characters: ``+ - = . _ : /``

            :param key: The tag key.
            :param value: The tag value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-restoretestingselection-keyvalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_backup import mixins as backup_mixins
                
                key_value_property = backup_mixins.CfnRestoreTestingSelectionPropsMixin.KeyValueProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f87f26731f219727bd1a546db67acfa1cdbeca7828674e130a35fb65f0f06384)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The tag key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-restoretestingselection-keyvalue.html#cfn-backup-restoretestingselection-keyvalue-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The tag value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-restoretestingselection-keyvalue.html#cfn-backup-restoretestingselection-keyvalue-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KeyValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_backup.mixins.CfnRestoreTestingSelectionPropsMixin.ProtectedResourceConditionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "string_equals": "stringEquals",
            "string_not_equals": "stringNotEquals",
        },
    )
    class ProtectedResourceConditionsProperty:
        def __init__(
            self,
            *,
            string_equals: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRestoreTestingSelectionPropsMixin.KeyValueProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            string_not_equals: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRestoreTestingSelectionPropsMixin.KeyValueProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The conditions that you define for resources in your restore testing plan using tags.

            :param string_equals: Filters the values of your tagged resources for only those resources that you tagged with the same value. Also called "exact matching."
            :param string_not_equals: Filters the values of your tagged resources for only those resources that you tagged that do not have the same value. Also called "negated matching."

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-restoretestingselection-protectedresourceconditions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_backup import mixins as backup_mixins
                
                protected_resource_conditions_property = backup_mixins.CfnRestoreTestingSelectionPropsMixin.ProtectedResourceConditionsProperty(
                    string_equals=[backup_mixins.CfnRestoreTestingSelectionPropsMixin.KeyValueProperty(
                        key="key",
                        value="value"
                    )],
                    string_not_equals=[backup_mixins.CfnRestoreTestingSelectionPropsMixin.KeyValueProperty(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__79320e1994dcc842867ac4ecf15fb15d7233745304b884a13a82335a4cb5b3cf)
                check_type(argname="argument string_equals", value=string_equals, expected_type=type_hints["string_equals"])
                check_type(argname="argument string_not_equals", value=string_not_equals, expected_type=type_hints["string_not_equals"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if string_equals is not None:
                self._values["string_equals"] = string_equals
            if string_not_equals is not None:
                self._values["string_not_equals"] = string_not_equals

        @builtins.property
        def string_equals(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRestoreTestingSelectionPropsMixin.KeyValueProperty"]]]]:
            '''Filters the values of your tagged resources for only those resources that you tagged with the same value.

            Also called "exact matching."

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-restoretestingselection-protectedresourceconditions.html#cfn-backup-restoretestingselection-protectedresourceconditions-stringequals
            '''
            result = self._values.get("string_equals")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRestoreTestingSelectionPropsMixin.KeyValueProperty"]]]], result)

        @builtins.property
        def string_not_equals(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRestoreTestingSelectionPropsMixin.KeyValueProperty"]]]]:
            '''Filters the values of your tagged resources for only those resources that you tagged that do not have the same value.

            Also called "negated matching."

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-restoretestingselection-protectedresourceconditions.html#cfn-backup-restoretestingselection-protectedresourceconditions-stringnotequals
            '''
            result = self._values.get("string_not_equals")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRestoreTestingSelectionPropsMixin.KeyValueProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProtectedResourceConditionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnBackupPlanMixinProps",
    "CfnBackupPlanPropsMixin",
    "CfnBackupSelectionMixinProps",
    "CfnBackupSelectionPropsMixin",
    "CfnBackupVaultMixinProps",
    "CfnBackupVaultPropsMixin",
    "CfnFrameworkMixinProps",
    "CfnFrameworkPropsMixin",
    "CfnLogicallyAirGappedBackupVaultMixinProps",
    "CfnLogicallyAirGappedBackupVaultPropsMixin",
    "CfnReportPlanMixinProps",
    "CfnReportPlanPropsMixin",
    "CfnRestoreTestingPlanMixinProps",
    "CfnRestoreTestingPlanPropsMixin",
    "CfnRestoreTestingSelectionMixinProps",
    "CfnRestoreTestingSelectionPropsMixin",
]

publication.publish()

def _typecheckingstub__c52c3ba5518a4eddf653790cfcc9253bcbcda34e798ed1e347336649f2cedbf7(
    *,
    backup_plan: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBackupPlanPropsMixin.BackupPlanResourceTypeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    backup_plan_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa1fb7fd3baec625155ea0022560ceb0289f5ee02e77a7b7852a07edc73239a6(
    props: typing.Union[CfnBackupPlanMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f7255e14502397e518347471c7aeaa4ee6ed8f1fb9aa7f192189a186243fc15(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d33c9b99526c39919a02d46f942083c45301e82b31f24c00f61a32551deb8cb9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__461955aaf03e4b77445644bde0b4c762ad052ded1e115b150888942af8a8196f(
    *,
    backup_options: typing.Any = None,
    resource_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15c9250612b8f408f2b07b56b91b7dac9c891af8a4af727b2ca9485ff633f9ce(
    *,
    advanced_backup_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBackupPlanPropsMixin.AdvancedBackupSettingResourceTypeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    backup_plan_name: typing.Optional[builtins.str] = None,
    backup_plan_rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBackupPlanPropsMixin.BackupRuleResourceTypeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ea571f90248cad05290a3f2b70ae8d80d8ade58a97b0838fa2e9d0188a32e19(
    *,
    completion_window_minutes: typing.Optional[jsii.Number] = None,
    copy_actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBackupPlanPropsMixin.CopyActionResourceTypeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    enable_continuous_backup: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    index_actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBackupPlanPropsMixin.IndexActionsResourceTypeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    lifecycle: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBackupPlanPropsMixin.LifecycleResourceTypeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    recovery_point_tags: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    rule_name: typing.Optional[builtins.str] = None,
    schedule_expression: typing.Optional[builtins.str] = None,
    schedule_expression_timezone: typing.Optional[builtins.str] = None,
    start_window_minutes: typing.Optional[jsii.Number] = None,
    target_backup_vault: typing.Optional[builtins.str] = None,
    target_logically_air_gapped_backup_vault_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5c58b9d2d5a4321a8189b50d8d7b950929b947271c008bff06c10f6598d8e84(
    *,
    destination_backup_vault_arn: typing.Optional[builtins.str] = None,
    lifecycle: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBackupPlanPropsMixin.LifecycleResourceTypeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ec78af3ad88b132b7dcc80fe1e930ecfb06c641ca343736be1bdbac6007a007(
    *,
    resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fec90a2f0249924188094f68d3c8b1a094444ec5d9496801005ff8b9b635e597(
    *,
    delete_after_days: typing.Optional[jsii.Number] = None,
    move_to_cold_storage_after_days: typing.Optional[jsii.Number] = None,
    opt_in_to_archive_for_supported_resources: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e66fe88d24bd9cba4a1cf23894b412f1c0a62ac484f972b0ce53538f26659b4f(
    *,
    backup_plan_id: typing.Optional[builtins.str] = None,
    backup_selection: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBackupSelectionPropsMixin.BackupSelectionResourceTypeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d16f7a5ce8e77eab8341119bc680e7449b46efaf45281093bb41e5e5b944d74(
    props: typing.Union[CfnBackupSelectionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d630695d14edec806f033e6c22077d7ca0bb572dc2cf27a36a6a94b55ecda1ea(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb31847e2bfb8c4c15b051200526df6fe5f4e5dcc1774baeb2faf5c7dbbb657b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5445957c477620010ea3aa0ebf94f59a7aceff6213ba5202eb96fb089af993a8(
    *,
    conditions: typing.Any = None,
    iam_role_arn: typing.Optional[builtins.str] = None,
    list_of_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBackupSelectionPropsMixin.ConditionResourceTypeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    not_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    selection_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94d3ae6a933028793e9c703f8aca3cdf1bd0e280a2ed752b344c30a4d77cf6ac(
    *,
    condition_key: typing.Optional[builtins.str] = None,
    condition_type: typing.Optional[builtins.str] = None,
    condition_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dae6b99048b55ef079d526d8d6ed9e5f3c1d3fd4245a74cbf8519c620f9ba5ab(
    *,
    access_policy: typing.Any = None,
    backup_vault_name: typing.Optional[builtins.str] = None,
    backup_vault_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    encryption_key_arn: typing.Optional[builtins.str] = None,
    lock_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBackupVaultPropsMixin.LockConfigurationTypeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    notifications: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBackupVaultPropsMixin.NotificationObjectTypeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__427786b5415a8501d76140d99d3a7505d2372b792b3a798d0cda6804db1b24f8(
    props: typing.Union[CfnBackupVaultMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1887d96ce0cc9927afa93dc01d3f2a7a4479b8f283af45c6e4a66b35aa2e4e7a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__298d887174a9ca2dccf0d7af332cbade9f3f36b252478797a2df6747f34979e0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2e9c992d1044bda2fbc3b7d316c2cce8727569b1e31807dd50984f832adabe9(
    *,
    changeable_for_days: typing.Optional[jsii.Number] = None,
    max_retention_days: typing.Optional[jsii.Number] = None,
    min_retention_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa0f487b6836a98326372782594ba4c7e54cdecbfb04df36526d47843c7ef595(
    *,
    backup_vault_events: typing.Optional[typing.Sequence[builtins.str]] = None,
    sns_topic_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64afb43307664ba019223293fc2c53b56c619db24827386c4a44b75e588a7c62(
    *,
    framework_controls: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFrameworkPropsMixin.FrameworkControlProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    framework_description: typing.Optional[builtins.str] = None,
    framework_name: typing.Optional[builtins.str] = None,
    framework_tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c281e43247da2422c011bcd54900c8ff8e5acd11e3f9de6e0b3ed9ac0c09040(
    props: typing.Union[CfnFrameworkMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0eb723e29c1039bc5ec07fc302fbdec28b178061c0e03c5032d22efd2a29bf1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2a6735206fe0575c856f8ba3edbd0db289756584faa684737433229862d19f2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73e2c34fffd8bca3db301cd9225e5f957748c31af12e340668559ede3c9a870f(
    *,
    parameter_name: typing.Optional[builtins.str] = None,
    parameter_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edb50c6a1e59c9f4f26a8249fd1982d7f273b7ad0b2207a9e302da139bc98535(
    *,
    control_input_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFrameworkPropsMixin.ControlInputParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    control_name: typing.Optional[builtins.str] = None,
    control_scope: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0a89d891ba9c98b8da62805bcb1f9059e77b326370f48b4bac19e5507c248f9(
    *,
    access_policy: typing.Any = None,
    backup_vault_name: typing.Optional[builtins.str] = None,
    backup_vault_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    encryption_key_arn: typing.Optional[builtins.str] = None,
    max_retention_days: typing.Optional[jsii.Number] = None,
    min_retention_days: typing.Optional[jsii.Number] = None,
    mpa_approval_team_arn: typing.Optional[builtins.str] = None,
    notifications: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLogicallyAirGappedBackupVaultPropsMixin.NotificationObjectTypeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c480369cdde00896e4ebab5026f4f9a973accd1e672113e71dbda5960c2f9ce(
    props: typing.Union[CfnLogicallyAirGappedBackupVaultMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de6e043262cde5253ac48d4d8ee23b292501d40251efcbaa82009fdd58679836(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26e83a04ff3c2b9d94fd5c1b6673d1d1f52e1a825b24accf759918c981e2d666(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51da8e513a32f33acd3f441f25fa1e6103c4343c9c8120ab91bed1596c02660c(
    *,
    backup_vault_events: typing.Optional[typing.Sequence[builtins.str]] = None,
    sns_topic_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c293bad169d8d720bae5c3bceaf74305f1ae6a82bf784df267e10f4d76a3ba2f(
    *,
    report_delivery_channel: typing.Any = None,
    report_plan_description: typing.Optional[builtins.str] = None,
    report_plan_name: typing.Optional[builtins.str] = None,
    report_plan_tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    report_setting: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa2e1b23d15adeee4b6c3f426cfff83adcd82f792cb02c293a2a3541455f5cf8(
    props: typing.Union[CfnReportPlanMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e0e4d2d3d9bfd17d933aad7c8818e8a7407499730f3b3b3fe9559331882dae6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cea986c9ddcc043aae45fe357bdc385650f8aead47104332ab327aacd107678a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c7fcf3920b70cba059812d37416686328721ea4e26500e42115f767fc99ca4f(
    *,
    formats: typing.Optional[typing.Sequence[builtins.str]] = None,
    s3_bucket_name: typing.Optional[builtins.str] = None,
    s3_key_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a265c9fb3afe50f573a7ac01096c931e2fae7505cee5e1f1657c2b4da7b40f89(
    *,
    accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
    framework_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    organization_units: typing.Optional[typing.Sequence[builtins.str]] = None,
    regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    report_template: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1c9d019e568e3fcfbad25fab5d9d716c651470a08864736e376fa9c26e54a57(
    *,
    recovery_point_selection: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRestoreTestingPlanPropsMixin.RestoreTestingRecoveryPointSelectionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    restore_testing_plan_name: typing.Optional[builtins.str] = None,
    schedule_expression: typing.Optional[builtins.str] = None,
    schedule_expression_timezone: typing.Optional[builtins.str] = None,
    start_window_hours: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d58346e7976909cab3c1ff52f1b7e7342654ef2ace75d5408b49a8266fcaba04(
    props: typing.Union[CfnRestoreTestingPlanMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10d05ee1c5d11e222a0c4c879e2cee2f25983ae6cabe7678114983f24e356694(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4138f05abd72584f4563a2a2dd1be99ec37376f5508d618c15fb193c267232eb(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0d1a68f81af2ead9a0c51ca626c061e2aca432d752e052072fd80fb2611fca1(
    *,
    algorithm: typing.Optional[builtins.str] = None,
    exclude_vaults: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_vaults: typing.Optional[typing.Sequence[builtins.str]] = None,
    recovery_point_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    selection_window_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c37768d11f47ebe24237b830579a26cebb0f43e35e9d9796c8fd1ce5691c2a8b(
    *,
    iam_role_arn: typing.Optional[builtins.str] = None,
    protected_resource_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    protected_resource_conditions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRestoreTestingSelectionPropsMixin.ProtectedResourceConditionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    protected_resource_type: typing.Optional[builtins.str] = None,
    restore_metadata_overrides: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    restore_testing_plan_name: typing.Optional[builtins.str] = None,
    restore_testing_selection_name: typing.Optional[builtins.str] = None,
    validation_window_hours: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3e7f9dfcc90eec6cc7d015dd880828356ee9959f339bb4ec9e8a70f0a29cddf(
    props: typing.Union[CfnRestoreTestingSelectionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b562b0b8391b3e5779898f7859f9b7f6f49319d3dbf15c4f407c75c4d9276b25(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00eda2ddffdeaeb06597833e9ff3e2e893b44dede0f8d4c99796ed5b9aff64df(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f87f26731f219727bd1a546db67acfa1cdbeca7828674e130a35fb65f0f06384(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79320e1994dcc842867ac4ecf15fb15d7233745304b884a13a82335a4cb5b3cf(
    *,
    string_equals: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRestoreTestingSelectionPropsMixin.KeyValueProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    string_not_equals: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRestoreTestingSelectionPropsMixin.KeyValueProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
