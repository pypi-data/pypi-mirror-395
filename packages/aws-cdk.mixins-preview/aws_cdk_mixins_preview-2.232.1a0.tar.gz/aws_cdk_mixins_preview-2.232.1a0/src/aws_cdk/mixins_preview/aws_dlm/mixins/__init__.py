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
    jsii_type="@aws-cdk/mixins-preview.aws_dlm.mixins.CfnLifecyclePolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "copy_tags": "copyTags",
        "create_interval": "createInterval",
        "cross_region_copy_targets": "crossRegionCopyTargets",
        "default_policy": "defaultPolicy",
        "description": "description",
        "exclusions": "exclusions",
        "execution_role_arn": "executionRoleArn",
        "extend_deletion": "extendDeletion",
        "policy_details": "policyDetails",
        "retain_interval": "retainInterval",
        "state": "state",
        "tags": "tags",
    },
)
class CfnLifecyclePolicyMixinProps:
    def __init__(
        self,
        *,
        copy_tags: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        create_interval: typing.Optional[jsii.Number] = None,
        cross_region_copy_targets: typing.Any = None,
        default_policy: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        exclusions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLifecyclePolicyPropsMixin.ExclusionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        execution_role_arn: typing.Optional[builtins.str] = None,
        extend_deletion: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        policy_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLifecyclePolicyPropsMixin.PolicyDetailsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        retain_interval: typing.Optional[jsii.Number] = None,
        state: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnLifecyclePolicyPropsMixin.

        :param copy_tags: *[Default policies only]* Indicates whether the policy should copy tags from the source resource to the snapshot or AMI. If you do not specify a value, the default is ``false`` . Default: false
        :param create_interval: *[Default policies only]* Specifies how often the policy should run and create snapshots or AMIs. The creation frequency can range from 1 to 7 days. If you do not specify a value, the default is 1. Default: 1
        :param cross_region_copy_targets: *[Default policies only]* Specifies destination Regions for snapshot or AMI copies. You can specify up to 3 destination Regions. If you do not want to create cross-Region copies, omit this parameter.
        :param default_policy: *[Default policies only]* Specify the type of default policy to create. - To create a default policy for EBS snapshots, that creates snapshots of all volumes in the Region that do not have recent backups, specify ``VOLUME`` . - To create a default policy for EBS-backed AMIs, that creates EBS-backed AMIs from all instances in the Region that do not have recent backups, specify ``INSTANCE`` .
        :param description: A description of the lifecycle policy. The characters ^[0-9A-Za-z _-]+$ are supported.
        :param exclusions: *[Default policies only]* Specifies exclusion parameters for volumes or instances for which you do not want to create snapshots or AMIs. The policy will not create snapshots or AMIs for target resources that match any of the specified exclusion parameters.
        :param execution_role_arn: The Amazon Resource Name (ARN) of the IAM role used to run the operations specified by the lifecycle policy.
        :param extend_deletion: *[Default policies only]* Defines the snapshot or AMI retention behavior for the policy if the source volume or instance is deleted, or if the policy enters the error, disabled, or deleted state. By default ( *ExtendDeletion=false* ): - If a source resource is deleted, Amazon Data Lifecycle Manager will continue to delete previously created snapshots or AMIs, up to but not including the last one, based on the specified retention period. If you want Amazon Data Lifecycle Manager to delete all snapshots or AMIs, including the last one, specify ``true`` . - If a policy enters the error, disabled, or deleted state, Amazon Data Lifecycle Manager stops deleting snapshots and AMIs. If you want Amazon Data Lifecycle Manager to continue deleting snapshots or AMIs, including the last one, if the policy enters one of these states, specify ``true`` . If you enable extended deletion ( *ExtendDeletion=true* ), you override both default behaviors simultaneously. If you do not specify a value, the default is ``false`` . Default: false
        :param policy_details: The configuration details of the lifecycle policy. .. epigraph:: If you create a default policy, you can specify the request parameters either in the request body, or in the PolicyDetails request structure, but not both.
        :param retain_interval: *[Default policies only]* Specifies how long the policy should retain snapshots or AMIs before deleting them. The retention period can range from 2 to 14 days, but it must be greater than the creation frequency to ensure that the policy retains at least 1 snapshot or AMI at any given time. If you do not specify a value, the default is 7. Default: 7
        :param state: The activation state of the lifecycle policy.
        :param tags: The tags to apply to the lifecycle policy during creation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dlm-lifecyclepolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_dlm import mixins as dlm_mixins
            
            # cross_region_copy_targets: Any
            # exclude_tags: Any
            # exclude_volume_types: Any
            
            cfn_lifecycle_policy_mixin_props = dlm_mixins.CfnLifecyclePolicyMixinProps(
                copy_tags=False,
                create_interval=123,
                cross_region_copy_targets=cross_region_copy_targets,
                default_policy="defaultPolicy",
                description="description",
                exclusions=dlm_mixins.CfnLifecyclePolicyPropsMixin.ExclusionsProperty(
                    exclude_boot_volumes=False,
                    exclude_tags=exclude_tags,
                    exclude_volume_types=exclude_volume_types
                ),
                execution_role_arn="executionRoleArn",
                extend_deletion=False,
                policy_details=dlm_mixins.CfnLifecyclePolicyPropsMixin.PolicyDetailsProperty(
                    actions=[dlm_mixins.CfnLifecyclePolicyPropsMixin.ActionProperty(
                        cross_region_copy=[dlm_mixins.CfnLifecyclePolicyPropsMixin.CrossRegionCopyActionProperty(
                            encryption_configuration=dlm_mixins.CfnLifecyclePolicyPropsMixin.EncryptionConfigurationProperty(
                                cmk_arn="cmkArn",
                                encrypted=False
                            ),
                            retain_rule=dlm_mixins.CfnLifecyclePolicyPropsMixin.CrossRegionCopyRetainRuleProperty(
                                interval=123,
                                interval_unit="intervalUnit"
                            ),
                            target="target"
                        )],
                        name="name"
                    )],
                    copy_tags=False,
                    create_interval=123,
                    cross_region_copy_targets=cross_region_copy_targets,
                    event_source=dlm_mixins.CfnLifecyclePolicyPropsMixin.EventSourceProperty(
                        parameters=dlm_mixins.CfnLifecyclePolicyPropsMixin.EventParametersProperty(
                            description_regex="descriptionRegex",
                            event_type="eventType",
                            snapshot_owner=["snapshotOwner"]
                        ),
                        type="type"
                    ),
                    exclusions=dlm_mixins.CfnLifecyclePolicyPropsMixin.ExclusionsProperty(
                        exclude_boot_volumes=False,
                        exclude_tags=exclude_tags,
                        exclude_volume_types=exclude_volume_types
                    ),
                    extend_deletion=False,
                    parameters=dlm_mixins.CfnLifecyclePolicyPropsMixin.ParametersProperty(
                        exclude_boot_volume=False,
                        exclude_data_volume_tags=[CfnTag(
                            key="key",
                            value="value"
                        )],
                        no_reboot=False
                    ),
                    policy_language="policyLanguage",
                    policy_type="policyType",
                    resource_locations=["resourceLocations"],
                    resource_type="resourceType",
                    resource_types=["resourceTypes"],
                    retain_interval=123,
                    schedules=[dlm_mixins.CfnLifecyclePolicyPropsMixin.ScheduleProperty(
                        archive_rule=dlm_mixins.CfnLifecyclePolicyPropsMixin.ArchiveRuleProperty(
                            retain_rule=dlm_mixins.CfnLifecyclePolicyPropsMixin.ArchiveRetainRuleProperty(
                                retention_archive_tier=dlm_mixins.CfnLifecyclePolicyPropsMixin.RetentionArchiveTierProperty(
                                    count=123,
                                    interval=123,
                                    interval_unit="intervalUnit"
                                )
                            )
                        ),
                        copy_tags=False,
                        create_rule=dlm_mixins.CfnLifecyclePolicyPropsMixin.CreateRuleProperty(
                            cron_expression="cronExpression",
                            interval=123,
                            interval_unit="intervalUnit",
                            location="location",
                            scripts=[dlm_mixins.CfnLifecyclePolicyPropsMixin.ScriptProperty(
                                execute_operation_on_script_failure=False,
                                execution_handler="executionHandler",
                                execution_handler_service="executionHandlerService",
                                execution_timeout=123,
                                maximum_retry_count=123,
                                stages=["stages"]
                            )],
                            times=["times"]
                        ),
                        cross_region_copy_rules=[dlm_mixins.CfnLifecyclePolicyPropsMixin.CrossRegionCopyRuleProperty(
                            cmk_arn="cmkArn",
                            copy_tags=False,
                            deprecate_rule=dlm_mixins.CfnLifecyclePolicyPropsMixin.CrossRegionCopyDeprecateRuleProperty(
                                interval=123,
                                interval_unit="intervalUnit"
                            ),
                            encrypted=False,
                            retain_rule=dlm_mixins.CfnLifecyclePolicyPropsMixin.CrossRegionCopyRetainRuleProperty(
                                interval=123,
                                interval_unit="intervalUnit"
                            ),
                            target="target",
                            target_region="targetRegion"
                        )],
                        deprecate_rule=dlm_mixins.CfnLifecyclePolicyPropsMixin.DeprecateRuleProperty(
                            count=123,
                            interval=123,
                            interval_unit="intervalUnit"
                        ),
                        fast_restore_rule=dlm_mixins.CfnLifecyclePolicyPropsMixin.FastRestoreRuleProperty(
                            availability_zones=["availabilityZones"],
                            count=123,
                            interval=123,
                            interval_unit="intervalUnit"
                        ),
                        name="name",
                        retain_rule=dlm_mixins.CfnLifecyclePolicyPropsMixin.RetainRuleProperty(
                            count=123,
                            interval=123,
                            interval_unit="intervalUnit"
                        ),
                        share_rules=[dlm_mixins.CfnLifecyclePolicyPropsMixin.ShareRuleProperty(
                            target_accounts=["targetAccounts"],
                            unshare_interval=123,
                            unshare_interval_unit="unshareIntervalUnit"
                        )],
                        tags_to_add=[CfnTag(
                            key="key",
                            value="value"
                        )],
                        variable_tags=[CfnTag(
                            key="key",
                            value="value"
                        )]
                    )],
                    target_tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                ),
                retain_interval=123,
                state="state",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__594a4f5b67bd7681312e80236a3f67277618dd68ffe3e49f22c366f9cd7504b4)
            check_type(argname="argument copy_tags", value=copy_tags, expected_type=type_hints["copy_tags"])
            check_type(argname="argument create_interval", value=create_interval, expected_type=type_hints["create_interval"])
            check_type(argname="argument cross_region_copy_targets", value=cross_region_copy_targets, expected_type=type_hints["cross_region_copy_targets"])
            check_type(argname="argument default_policy", value=default_policy, expected_type=type_hints["default_policy"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument exclusions", value=exclusions, expected_type=type_hints["exclusions"])
            check_type(argname="argument execution_role_arn", value=execution_role_arn, expected_type=type_hints["execution_role_arn"])
            check_type(argname="argument extend_deletion", value=extend_deletion, expected_type=type_hints["extend_deletion"])
            check_type(argname="argument policy_details", value=policy_details, expected_type=type_hints["policy_details"])
            check_type(argname="argument retain_interval", value=retain_interval, expected_type=type_hints["retain_interval"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if copy_tags is not None:
            self._values["copy_tags"] = copy_tags
        if create_interval is not None:
            self._values["create_interval"] = create_interval
        if cross_region_copy_targets is not None:
            self._values["cross_region_copy_targets"] = cross_region_copy_targets
        if default_policy is not None:
            self._values["default_policy"] = default_policy
        if description is not None:
            self._values["description"] = description
        if exclusions is not None:
            self._values["exclusions"] = exclusions
        if execution_role_arn is not None:
            self._values["execution_role_arn"] = execution_role_arn
        if extend_deletion is not None:
            self._values["extend_deletion"] = extend_deletion
        if policy_details is not None:
            self._values["policy_details"] = policy_details
        if retain_interval is not None:
            self._values["retain_interval"] = retain_interval
        if state is not None:
            self._values["state"] = state
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def copy_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''*[Default policies only]* Indicates whether the policy should copy tags from the source resource to the snapshot or AMI.

        If you do not specify a value, the default is ``false`` .

        Default: false

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dlm-lifecyclepolicy.html#cfn-dlm-lifecyclepolicy-copytags
        '''
        result = self._values.get("copy_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def create_interval(self) -> typing.Optional[jsii.Number]:
        '''*[Default policies only]* Specifies how often the policy should run and create snapshots or AMIs.

        The creation frequency can range from 1 to 7 days. If you do not specify a value, the default is 1.

        Default: 1

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dlm-lifecyclepolicy.html#cfn-dlm-lifecyclepolicy-createinterval
        '''
        result = self._values.get("create_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cross_region_copy_targets(self) -> typing.Any:
        '''*[Default policies only]* Specifies destination Regions for snapshot or AMI copies.

        You can specify up to 3 destination Regions. If you do not want to create cross-Region copies, omit this parameter.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dlm-lifecyclepolicy.html#cfn-dlm-lifecyclepolicy-crossregioncopytargets
        '''
        result = self._values.get("cross_region_copy_targets")
        return typing.cast(typing.Any, result)

    @builtins.property
    def default_policy(self) -> typing.Optional[builtins.str]:
        '''*[Default policies only]* Specify the type of default policy to create.

        - To create a default policy for EBS snapshots, that creates snapshots of all volumes in the Region that do not have recent backups, specify ``VOLUME`` .
        - To create a default policy for EBS-backed AMIs, that creates EBS-backed AMIs from all instances in the Region that do not have recent backups, specify ``INSTANCE`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dlm-lifecyclepolicy.html#cfn-dlm-lifecyclepolicy-defaultpolicy
        '''
        result = self._values.get("default_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the lifecycle policy.

        The characters ^[0-9A-Za-z _-]+$ are supported.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dlm-lifecyclepolicy.html#cfn-dlm-lifecyclepolicy-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exclusions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.ExclusionsProperty"]]:
        '''*[Default policies only]* Specifies exclusion parameters for volumes or instances for which you do not want to create snapshots or AMIs.

        The policy will not create snapshots or AMIs for target resources that match any of the specified exclusion parameters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dlm-lifecyclepolicy.html#cfn-dlm-lifecyclepolicy-exclusions
        '''
        result = self._values.get("exclusions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.ExclusionsProperty"]], result)

    @builtins.property
    def execution_role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the IAM role used to run the operations specified by the lifecycle policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dlm-lifecyclepolicy.html#cfn-dlm-lifecyclepolicy-executionrolearn
        '''
        result = self._values.get("execution_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extend_deletion(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''*[Default policies only]* Defines the snapshot or AMI retention behavior for the policy if the source volume or instance is deleted, or if the policy enters the error, disabled, or deleted state.

        By default ( *ExtendDeletion=false* ):

        - If a source resource is deleted, Amazon Data Lifecycle Manager will continue to delete previously created snapshots or AMIs, up to but not including the last one, based on the specified retention period. If you want Amazon Data Lifecycle Manager to delete all snapshots or AMIs, including the last one, specify ``true`` .
        - If a policy enters the error, disabled, or deleted state, Amazon Data Lifecycle Manager stops deleting snapshots and AMIs. If you want Amazon Data Lifecycle Manager to continue deleting snapshots or AMIs, including the last one, if the policy enters one of these states, specify ``true`` .

        If you enable extended deletion ( *ExtendDeletion=true* ), you override both default behaviors simultaneously.

        If you do not specify a value, the default is ``false`` .

        Default: false

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dlm-lifecyclepolicy.html#cfn-dlm-lifecyclepolicy-extenddeletion
        '''
        result = self._values.get("extend_deletion")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def policy_details(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.PolicyDetailsProperty"]]:
        '''The configuration details of the lifecycle policy.

        .. epigraph::

           If you create a default policy, you can specify the request parameters either in the request body, or in the PolicyDetails request structure, but not both.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dlm-lifecyclepolicy.html#cfn-dlm-lifecyclepolicy-policydetails
        '''
        result = self._values.get("policy_details")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.PolicyDetailsProperty"]], result)

    @builtins.property
    def retain_interval(self) -> typing.Optional[jsii.Number]:
        '''*[Default policies only]* Specifies how long the policy should retain snapshots or AMIs before deleting them.

        The retention period can range from 2 to 14 days, but it must be greater than the creation frequency to ensure that the policy retains at least 1 snapshot or AMI at any given time. If you do not specify a value, the default is 7.

        Default: 7

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dlm-lifecyclepolicy.html#cfn-dlm-lifecyclepolicy-retaininterval
        '''
        result = self._values.get("retain_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''The activation state of the lifecycle policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dlm-lifecyclepolicy.html#cfn-dlm-lifecyclepolicy-state
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags to apply to the lifecycle policy during creation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dlm-lifecyclepolicy.html#cfn-dlm-lifecyclepolicy-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLifecyclePolicyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLifecyclePolicyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_dlm.mixins.CfnLifecyclePolicyPropsMixin",
):
    '''Specifies a lifecycle policy, which is used to automate operations on Amazon EBS resources.

    The properties are required when you add a lifecycle policy and optional when you update a lifecycle policy.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dlm-lifecyclepolicy.html
    :cloudformationResource: AWS::DLM::LifecyclePolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_dlm import mixins as dlm_mixins
        
        # cross_region_copy_targets: Any
        # exclude_tags: Any
        # exclude_volume_types: Any
        
        cfn_lifecycle_policy_props_mixin = dlm_mixins.CfnLifecyclePolicyPropsMixin(dlm_mixins.CfnLifecyclePolicyMixinProps(
            copy_tags=False,
            create_interval=123,
            cross_region_copy_targets=cross_region_copy_targets,
            default_policy="defaultPolicy",
            description="description",
            exclusions=dlm_mixins.CfnLifecyclePolicyPropsMixin.ExclusionsProperty(
                exclude_boot_volumes=False,
                exclude_tags=exclude_tags,
                exclude_volume_types=exclude_volume_types
            ),
            execution_role_arn="executionRoleArn",
            extend_deletion=False,
            policy_details=dlm_mixins.CfnLifecyclePolicyPropsMixin.PolicyDetailsProperty(
                actions=[dlm_mixins.CfnLifecyclePolicyPropsMixin.ActionProperty(
                    cross_region_copy=[dlm_mixins.CfnLifecyclePolicyPropsMixin.CrossRegionCopyActionProperty(
                        encryption_configuration=dlm_mixins.CfnLifecyclePolicyPropsMixin.EncryptionConfigurationProperty(
                            cmk_arn="cmkArn",
                            encrypted=False
                        ),
                        retain_rule=dlm_mixins.CfnLifecyclePolicyPropsMixin.CrossRegionCopyRetainRuleProperty(
                            interval=123,
                            interval_unit="intervalUnit"
                        ),
                        target="target"
                    )],
                    name="name"
                )],
                copy_tags=False,
                create_interval=123,
                cross_region_copy_targets=cross_region_copy_targets,
                event_source=dlm_mixins.CfnLifecyclePolicyPropsMixin.EventSourceProperty(
                    parameters=dlm_mixins.CfnLifecyclePolicyPropsMixin.EventParametersProperty(
                        description_regex="descriptionRegex",
                        event_type="eventType",
                        snapshot_owner=["snapshotOwner"]
                    ),
                    type="type"
                ),
                exclusions=dlm_mixins.CfnLifecyclePolicyPropsMixin.ExclusionsProperty(
                    exclude_boot_volumes=False,
                    exclude_tags=exclude_tags,
                    exclude_volume_types=exclude_volume_types
                ),
                extend_deletion=False,
                parameters=dlm_mixins.CfnLifecyclePolicyPropsMixin.ParametersProperty(
                    exclude_boot_volume=False,
                    exclude_data_volume_tags=[CfnTag(
                        key="key",
                        value="value"
                    )],
                    no_reboot=False
                ),
                policy_language="policyLanguage",
                policy_type="policyType",
                resource_locations=["resourceLocations"],
                resource_type="resourceType",
                resource_types=["resourceTypes"],
                retain_interval=123,
                schedules=[dlm_mixins.CfnLifecyclePolicyPropsMixin.ScheduleProperty(
                    archive_rule=dlm_mixins.CfnLifecyclePolicyPropsMixin.ArchiveRuleProperty(
                        retain_rule=dlm_mixins.CfnLifecyclePolicyPropsMixin.ArchiveRetainRuleProperty(
                            retention_archive_tier=dlm_mixins.CfnLifecyclePolicyPropsMixin.RetentionArchiveTierProperty(
                                count=123,
                                interval=123,
                                interval_unit="intervalUnit"
                            )
                        )
                    ),
                    copy_tags=False,
                    create_rule=dlm_mixins.CfnLifecyclePolicyPropsMixin.CreateRuleProperty(
                        cron_expression="cronExpression",
                        interval=123,
                        interval_unit="intervalUnit",
                        location="location",
                        scripts=[dlm_mixins.CfnLifecyclePolicyPropsMixin.ScriptProperty(
                            execute_operation_on_script_failure=False,
                            execution_handler="executionHandler",
                            execution_handler_service="executionHandlerService",
                            execution_timeout=123,
                            maximum_retry_count=123,
                            stages=["stages"]
                        )],
                        times=["times"]
                    ),
                    cross_region_copy_rules=[dlm_mixins.CfnLifecyclePolicyPropsMixin.CrossRegionCopyRuleProperty(
                        cmk_arn="cmkArn",
                        copy_tags=False,
                        deprecate_rule=dlm_mixins.CfnLifecyclePolicyPropsMixin.CrossRegionCopyDeprecateRuleProperty(
                            interval=123,
                            interval_unit="intervalUnit"
                        ),
                        encrypted=False,
                        retain_rule=dlm_mixins.CfnLifecyclePolicyPropsMixin.CrossRegionCopyRetainRuleProperty(
                            interval=123,
                            interval_unit="intervalUnit"
                        ),
                        target="target",
                        target_region="targetRegion"
                    )],
                    deprecate_rule=dlm_mixins.CfnLifecyclePolicyPropsMixin.DeprecateRuleProperty(
                        count=123,
                        interval=123,
                        interval_unit="intervalUnit"
                    ),
                    fast_restore_rule=dlm_mixins.CfnLifecyclePolicyPropsMixin.FastRestoreRuleProperty(
                        availability_zones=["availabilityZones"],
                        count=123,
                        interval=123,
                        interval_unit="intervalUnit"
                    ),
                    name="name",
                    retain_rule=dlm_mixins.CfnLifecyclePolicyPropsMixin.RetainRuleProperty(
                        count=123,
                        interval=123,
                        interval_unit="intervalUnit"
                    ),
                    share_rules=[dlm_mixins.CfnLifecyclePolicyPropsMixin.ShareRuleProperty(
                        target_accounts=["targetAccounts"],
                        unshare_interval=123,
                        unshare_interval_unit="unshareIntervalUnit"
                    )],
                    tags_to_add=[CfnTag(
                        key="key",
                        value="value"
                    )],
                    variable_tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )],
                target_tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            ),
            retain_interval=123,
            state="state",
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
        props: typing.Union[CfnLifecyclePolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DLM::LifecyclePolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec0016e3e7dcb7c70221b6736bc2a43d40f941b4b114fda40eb7c5700e523286)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f447347aacf21e85636e7f62ece6ea23343db5dfcc8b73969a9f89910bbb4775)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6629158138525fe696cc6fefa8f62e6c2e3e4fdf9d15d91e3d534c0f12ae2259)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLifecyclePolicyMixinProps:
        return typing.cast(CfnLifecyclePolicyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dlm.mixins.CfnLifecyclePolicyPropsMixin.ActionProperty",
        jsii_struct_bases=[],
        name_mapping={"cross_region_copy": "crossRegionCopy", "name": "name"},
    )
    class ActionProperty:
        def __init__(
            self,
            *,
            cross_region_copy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLifecyclePolicyPropsMixin.CrossRegionCopyActionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''*[Event-based policies only]* Specifies an action for an event-based policy.

            :param cross_region_copy: The rule for copying shared snapshots across Regions.
            :param name: A descriptive name for the action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-action.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dlm import mixins as dlm_mixins
                
                action_property = dlm_mixins.CfnLifecyclePolicyPropsMixin.ActionProperty(
                    cross_region_copy=[dlm_mixins.CfnLifecyclePolicyPropsMixin.CrossRegionCopyActionProperty(
                        encryption_configuration=dlm_mixins.CfnLifecyclePolicyPropsMixin.EncryptionConfigurationProperty(
                            cmk_arn="cmkArn",
                            encrypted=False
                        ),
                        retain_rule=dlm_mixins.CfnLifecyclePolicyPropsMixin.CrossRegionCopyRetainRuleProperty(
                            interval=123,
                            interval_unit="intervalUnit"
                        ),
                        target="target"
                    )],
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__84f6bf4e688675063644f0b741606b39354d36d28f91d6ae18d5cd7f671aeb72)
                check_type(argname="argument cross_region_copy", value=cross_region_copy, expected_type=type_hints["cross_region_copy"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cross_region_copy is not None:
                self._values["cross_region_copy"] = cross_region_copy
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def cross_region_copy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.CrossRegionCopyActionProperty"]]]]:
            '''The rule for copying shared snapshots across Regions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-action.html#cfn-dlm-lifecyclepolicy-action-crossregioncopy
            '''
            result = self._values.get("cross_region_copy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.CrossRegionCopyActionProperty"]]]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''A descriptive name for the action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-action.html#cfn-dlm-lifecyclepolicy-action-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dlm.mixins.CfnLifecyclePolicyPropsMixin.ArchiveRetainRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"retention_archive_tier": "retentionArchiveTier"},
    )
    class ArchiveRetainRuleProperty:
        def __init__(
            self,
            *,
            retention_archive_tier: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLifecyclePolicyPropsMixin.RetentionArchiveTierProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''*[Custom snapshot policies only]* Specifies information about the archive storage tier retention period.

            :param retention_archive_tier: Information about retention period in the Amazon EBS Snapshots Archive. For more information, see `Archive Amazon EBS snapshots <https://docs.aws.amazon.com/AWSEC2/latest/WindowsGuide/snapshot-archive.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-archiveretainrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dlm import mixins as dlm_mixins
                
                archive_retain_rule_property = dlm_mixins.CfnLifecyclePolicyPropsMixin.ArchiveRetainRuleProperty(
                    retention_archive_tier=dlm_mixins.CfnLifecyclePolicyPropsMixin.RetentionArchiveTierProperty(
                        count=123,
                        interval=123,
                        interval_unit="intervalUnit"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__967e320d9798eb6435113099ad7b5d3d91d5ad5fbd011852000f16f640afe5ad)
                check_type(argname="argument retention_archive_tier", value=retention_archive_tier, expected_type=type_hints["retention_archive_tier"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if retention_archive_tier is not None:
                self._values["retention_archive_tier"] = retention_archive_tier

        @builtins.property
        def retention_archive_tier(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.RetentionArchiveTierProperty"]]:
            '''Information about retention period in the Amazon EBS Snapshots Archive.

            For more information, see `Archive Amazon EBS snapshots <https://docs.aws.amazon.com/AWSEC2/latest/WindowsGuide/snapshot-archive.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-archiveretainrule.html#cfn-dlm-lifecyclepolicy-archiveretainrule-retentionarchivetier
            '''
            result = self._values.get("retention_archive_tier")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.RetentionArchiveTierProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ArchiveRetainRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dlm.mixins.CfnLifecyclePolicyPropsMixin.ArchiveRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"retain_rule": "retainRule"},
    )
    class ArchiveRuleProperty:
        def __init__(
            self,
            *,
            retain_rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLifecyclePolicyPropsMixin.ArchiveRetainRuleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''*[Custom snapshot policies only]* Specifies a snapshot archiving rule for a schedule.

            :param retain_rule: Information about the retention period for the snapshot archiving rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-archiverule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dlm import mixins as dlm_mixins
                
                archive_rule_property = dlm_mixins.CfnLifecyclePolicyPropsMixin.ArchiveRuleProperty(
                    retain_rule=dlm_mixins.CfnLifecyclePolicyPropsMixin.ArchiveRetainRuleProperty(
                        retention_archive_tier=dlm_mixins.CfnLifecyclePolicyPropsMixin.RetentionArchiveTierProperty(
                            count=123,
                            interval=123,
                            interval_unit="intervalUnit"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__99c38907e01e31af5e3401a57efcf6f07b3cff8305ae3ec571fe3e5e063c3a97)
                check_type(argname="argument retain_rule", value=retain_rule, expected_type=type_hints["retain_rule"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if retain_rule is not None:
                self._values["retain_rule"] = retain_rule

        @builtins.property
        def retain_rule(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.ArchiveRetainRuleProperty"]]:
            '''Information about the retention period for the snapshot archiving rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-archiverule.html#cfn-dlm-lifecyclepolicy-archiverule-retainrule
            '''
            result = self._values.get("retain_rule")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.ArchiveRetainRuleProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ArchiveRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dlm.mixins.CfnLifecyclePolicyPropsMixin.CreateRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cron_expression": "cronExpression",
            "interval": "interval",
            "interval_unit": "intervalUnit",
            "location": "location",
            "scripts": "scripts",
            "times": "times",
        },
    )
    class CreateRuleProperty:
        def __init__(
            self,
            *,
            cron_expression: typing.Optional[builtins.str] = None,
            interval: typing.Optional[jsii.Number] = None,
            interval_unit: typing.Optional[builtins.str] = None,
            location: typing.Optional[builtins.str] = None,
            scripts: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLifecyclePolicyPropsMixin.ScriptProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            times: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''*[Custom snapshot and AMI policies only]* Specifies when the policy should create snapshots or AMIs.

            .. epigraph::

               - You must specify either *CronExpression* , or *Interval* , *IntervalUnit* , and *Times* .
               - If you need to specify an `ArchiveRule <https://docs.aws.amazon.com/dlm/latest/APIReference/API_ArchiveRule.html>`_ for the schedule, then you must specify a creation frequency of at least 28 days.

            :param cron_expression: The schedule, as a Cron expression. The schedule interval must be between 1 hour and 1 year. For more information, see the `Cron and rate expressions <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-scheduled-rule-pattern.html>`_ in the *Amazon EventBridge User Guide* .
            :param interval: The interval between snapshots. The supported values are 1, 2, 3, 4, 6, 8, 12, and 24.
            :param interval_unit: The interval unit.
            :param location: *[Custom snapshot policies only]* Specifies the destination for snapshots created by the policy. The allowed destinations depend on the location of the targeted resources. - If the policy targets resources in a Region, then you must create snapshots in the same Region as the source resource. - If the policy targets resources in a Local Zone, you can create snapshots in the same Local Zone or in its parent Region. - If the policy targets resources on an Outpost, then you can create snapshots on the same Outpost or in its parent Region. Specify one of the following values: - To create snapshots in the same Region as the source resource, specify ``CLOUD`` . - To create snapshots in the same Local Zone as the source resource, specify ``LOCAL_ZONE`` . - To create snapshots on the same Outpost as the source resource, specify ``OUTPOST_LOCAL`` . Default: ``CLOUD``
            :param scripts: *[Custom snapshot policies that target instances only]* Specifies pre and/or post scripts for a snapshot lifecycle policy that targets instances. This is useful for creating application-consistent snapshots, or for performing specific administrative tasks before or after Amazon Data Lifecycle Manager initiates snapshot creation. For more information, see `Automating application-consistent snapshots with pre and post scripts <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/automate-app-consistent-backups.html>`_ .
            :param times: The time, in UTC, to start the operation. The supported format is hh:mm. The operation occurs within a one-hour window following the specified time. If you do not specify a time, Amazon Data Lifecycle Manager selects a time within the next 24 hours.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-createrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dlm import mixins as dlm_mixins
                
                create_rule_property = dlm_mixins.CfnLifecyclePolicyPropsMixin.CreateRuleProperty(
                    cron_expression="cronExpression",
                    interval=123,
                    interval_unit="intervalUnit",
                    location="location",
                    scripts=[dlm_mixins.CfnLifecyclePolicyPropsMixin.ScriptProperty(
                        execute_operation_on_script_failure=False,
                        execution_handler="executionHandler",
                        execution_handler_service="executionHandlerService",
                        execution_timeout=123,
                        maximum_retry_count=123,
                        stages=["stages"]
                    )],
                    times=["times"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__312df5c95a3a2cf55cc15001b899995040b705c8659cece9de1b7ebc2c91e9f2)
                check_type(argname="argument cron_expression", value=cron_expression, expected_type=type_hints["cron_expression"])
                check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
                check_type(argname="argument interval_unit", value=interval_unit, expected_type=type_hints["interval_unit"])
                check_type(argname="argument location", value=location, expected_type=type_hints["location"])
                check_type(argname="argument scripts", value=scripts, expected_type=type_hints["scripts"])
                check_type(argname="argument times", value=times, expected_type=type_hints["times"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cron_expression is not None:
                self._values["cron_expression"] = cron_expression
            if interval is not None:
                self._values["interval"] = interval
            if interval_unit is not None:
                self._values["interval_unit"] = interval_unit
            if location is not None:
                self._values["location"] = location
            if scripts is not None:
                self._values["scripts"] = scripts
            if times is not None:
                self._values["times"] = times

        @builtins.property
        def cron_expression(self) -> typing.Optional[builtins.str]:
            '''The schedule, as a Cron expression.

            The schedule interval must be between 1 hour and 1 year. For more information, see the `Cron and rate expressions <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-scheduled-rule-pattern.html>`_ in the *Amazon EventBridge User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-createrule.html#cfn-dlm-lifecyclepolicy-createrule-cronexpression
            '''
            result = self._values.get("cron_expression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def interval(self) -> typing.Optional[jsii.Number]:
            '''The interval between snapshots.

            The supported values are 1, 2, 3, 4, 6, 8, 12, and 24.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-createrule.html#cfn-dlm-lifecyclepolicy-createrule-interval
            '''
            result = self._values.get("interval")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def interval_unit(self) -> typing.Optional[builtins.str]:
            '''The interval unit.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-createrule.html#cfn-dlm-lifecyclepolicy-createrule-intervalunit
            '''
            result = self._values.get("interval_unit")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def location(self) -> typing.Optional[builtins.str]:
            '''*[Custom snapshot policies only]* Specifies the destination for snapshots created by the policy.

            The allowed destinations depend on the location of the targeted resources.

            - If the policy targets resources in a Region, then you must create snapshots in the same Region as the source resource.
            - If the policy targets resources in a Local Zone, you can create snapshots in the same Local Zone or in its parent Region.
            - If the policy targets resources on an Outpost, then you can create snapshots on the same Outpost or in its parent Region.

            Specify one of the following values:

            - To create snapshots in the same Region as the source resource, specify ``CLOUD`` .
            - To create snapshots in the same Local Zone as the source resource, specify ``LOCAL_ZONE`` .
            - To create snapshots on the same Outpost as the source resource, specify ``OUTPOST_LOCAL`` .

            Default: ``CLOUD``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-createrule.html#cfn-dlm-lifecyclepolicy-createrule-location
            '''
            result = self._values.get("location")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def scripts(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.ScriptProperty"]]]]:
            '''*[Custom snapshot policies that target instances only]* Specifies pre and/or post scripts for a snapshot lifecycle policy that targets instances.

            This is useful for creating application-consistent snapshots, or for performing specific administrative tasks before or after Amazon Data Lifecycle Manager initiates snapshot creation.

            For more information, see `Automating application-consistent snapshots with pre and post scripts <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/automate-app-consistent-backups.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-createrule.html#cfn-dlm-lifecyclepolicy-createrule-scripts
            '''
            result = self._values.get("scripts")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.ScriptProperty"]]]], result)

        @builtins.property
        def times(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The time, in UTC, to start the operation. The supported format is hh:mm.

            The operation occurs within a one-hour window following the specified time. If you do not specify a time, Amazon Data Lifecycle Manager selects a time within the next 24 hours.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-createrule.html#cfn-dlm-lifecyclepolicy-createrule-times
            '''
            result = self._values.get("times")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CreateRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dlm.mixins.CfnLifecyclePolicyPropsMixin.CrossRegionCopyActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "encryption_configuration": "encryptionConfiguration",
            "retain_rule": "retainRule",
            "target": "target",
        },
    )
    class CrossRegionCopyActionProperty:
        def __init__(
            self,
            *,
            encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLifecyclePolicyPropsMixin.EncryptionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            retain_rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLifecyclePolicyPropsMixin.CrossRegionCopyRetainRuleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            target: typing.Optional[builtins.str] = None,
        ) -> None:
            '''*[Event-based policies only]* Specifies a cross-Region copy action for event-based policies.

            .. epigraph::

               To specify a cross-Region copy rule for snapshot and AMI policies, use `CrossRegionCopyRule <https://docs.aws.amazon.com/dlm/latest/APIReference/API_CrossRegionCopyRule.html>`_ .

            :param encryption_configuration: The encryption settings for the copied snapshot.
            :param retain_rule: Specifies a retention rule for cross-Region snapshot copies created by snapshot or event-based policies, or cross-Region AMI copies created by AMI policies. After the retention period expires, the cross-Region copy is deleted.
            :param target: The target Region.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dlm import mixins as dlm_mixins
                
                cross_region_copy_action_property = dlm_mixins.CfnLifecyclePolicyPropsMixin.CrossRegionCopyActionProperty(
                    encryption_configuration=dlm_mixins.CfnLifecyclePolicyPropsMixin.EncryptionConfigurationProperty(
                        cmk_arn="cmkArn",
                        encrypted=False
                    ),
                    retain_rule=dlm_mixins.CfnLifecyclePolicyPropsMixin.CrossRegionCopyRetainRuleProperty(
                        interval=123,
                        interval_unit="intervalUnit"
                    ),
                    target="target"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__58967213fd0902ebd1bef8b86f4ffc0c26ac3451ee9bf72c3ca944bcb2122ead)
                check_type(argname="argument encryption_configuration", value=encryption_configuration, expected_type=type_hints["encryption_configuration"])
                check_type(argname="argument retain_rule", value=retain_rule, expected_type=type_hints["retain_rule"])
                check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encryption_configuration is not None:
                self._values["encryption_configuration"] = encryption_configuration
            if retain_rule is not None:
                self._values["retain_rule"] = retain_rule
            if target is not None:
                self._values["target"] = target

        @builtins.property
        def encryption_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.EncryptionConfigurationProperty"]]:
            '''The encryption settings for the copied snapshot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyaction.html#cfn-dlm-lifecyclepolicy-crossregioncopyaction-encryptionconfiguration
            '''
            result = self._values.get("encryption_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.EncryptionConfigurationProperty"]], result)

        @builtins.property
        def retain_rule(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.CrossRegionCopyRetainRuleProperty"]]:
            '''Specifies a retention rule for cross-Region snapshot copies created by snapshot or event-based policies, or cross-Region AMI copies created by AMI policies.

            After the retention period expires, the cross-Region copy is deleted.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyaction.html#cfn-dlm-lifecyclepolicy-crossregioncopyaction-retainrule
            '''
            result = self._values.get("retain_rule")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.CrossRegionCopyRetainRuleProperty"]], result)

        @builtins.property
        def target(self) -> typing.Optional[builtins.str]:
            '''The target Region.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyaction.html#cfn-dlm-lifecyclepolicy-crossregioncopyaction-target
            '''
            result = self._values.get("target")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CrossRegionCopyActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dlm.mixins.CfnLifecyclePolicyPropsMixin.CrossRegionCopyDeprecateRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"interval": "interval", "interval_unit": "intervalUnit"},
    )
    class CrossRegionCopyDeprecateRuleProperty:
        def __init__(
            self,
            *,
            interval: typing.Optional[jsii.Number] = None,
            interval_unit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''*[Custom AMI policies only]* Specifies an AMI deprecation rule for cross-Region AMI copies created by an AMI policy.

            :param interval: The period after which to deprecate the cross-Region AMI copies. The period must be less than or equal to the cross-Region AMI copy retention period, and it can't be greater than 10 years. This is equivalent to 120 months, 520 weeks, or 3650 days.
            :param interval_unit: The unit of time in which to measure the *Interval* . For example, to deprecate a cross-Region AMI copy after 3 months, specify ``Interval=3`` and ``IntervalUnit=MONTHS`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopydeprecaterule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dlm import mixins as dlm_mixins
                
                cross_region_copy_deprecate_rule_property = dlm_mixins.CfnLifecyclePolicyPropsMixin.CrossRegionCopyDeprecateRuleProperty(
                    interval=123,
                    interval_unit="intervalUnit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__aafe9afdeaba0bd22bb4867788da095803b4c25781ed8e8e3b550ddd1dc469e7)
                check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
                check_type(argname="argument interval_unit", value=interval_unit, expected_type=type_hints["interval_unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if interval is not None:
                self._values["interval"] = interval
            if interval_unit is not None:
                self._values["interval_unit"] = interval_unit

        @builtins.property
        def interval(self) -> typing.Optional[jsii.Number]:
            '''The period after which to deprecate the cross-Region AMI copies.

            The period must be less than or equal to the cross-Region AMI copy retention period, and it can't be greater than 10 years. This is equivalent to 120 months, 520 weeks, or 3650 days.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopydeprecaterule.html#cfn-dlm-lifecyclepolicy-crossregioncopydeprecaterule-interval
            '''
            result = self._values.get("interval")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def interval_unit(self) -> typing.Optional[builtins.str]:
            '''The unit of time in which to measure the *Interval* .

            For example, to deprecate a cross-Region AMI copy after 3 months, specify ``Interval=3`` and ``IntervalUnit=MONTHS`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopydeprecaterule.html#cfn-dlm-lifecyclepolicy-crossregioncopydeprecaterule-intervalunit
            '''
            result = self._values.get("interval_unit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CrossRegionCopyDeprecateRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dlm.mixins.CfnLifecyclePolicyPropsMixin.CrossRegionCopyRetainRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"interval": "interval", "interval_unit": "intervalUnit"},
    )
    class CrossRegionCopyRetainRuleProperty:
        def __init__(
            self,
            *,
            interval: typing.Optional[jsii.Number] = None,
            interval_unit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies a retention rule for cross-Region snapshot copies created by snapshot or event-based policies, or cross-Region AMI copies created by AMI policies.

            After the retention period expires, the cross-Region copy is deleted.

            :param interval: The amount of time to retain a cross-Region snapshot or AMI copy. The maximum is 100 years. This is equivalent to 1200 months, 5200 weeks, or 36500 days.
            :param interval_unit: The unit of time for time-based retention. For example, to retain a cross-Region copy for 3 months, specify ``Interval=3`` and ``IntervalUnit=MONTHS`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyretainrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dlm import mixins as dlm_mixins
                
                cross_region_copy_retain_rule_property = dlm_mixins.CfnLifecyclePolicyPropsMixin.CrossRegionCopyRetainRuleProperty(
                    interval=123,
                    interval_unit="intervalUnit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d145963db3cba4654e05f7e140ecffffa6b7105cd93332de94844116901ac9f4)
                check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
                check_type(argname="argument interval_unit", value=interval_unit, expected_type=type_hints["interval_unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if interval is not None:
                self._values["interval"] = interval
            if interval_unit is not None:
                self._values["interval_unit"] = interval_unit

        @builtins.property
        def interval(self) -> typing.Optional[jsii.Number]:
            '''The amount of time to retain a cross-Region snapshot or AMI copy.

            The maximum is 100 years. This is equivalent to 1200 months, 5200 weeks, or 36500 days.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyretainrule.html#cfn-dlm-lifecyclepolicy-crossregioncopyretainrule-interval
            '''
            result = self._values.get("interval")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def interval_unit(self) -> typing.Optional[builtins.str]:
            '''The unit of time for time-based retention.

            For example, to retain a cross-Region copy for 3 months, specify ``Interval=3`` and ``IntervalUnit=MONTHS`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyretainrule.html#cfn-dlm-lifecyclepolicy-crossregioncopyretainrule-intervalunit
            '''
            result = self._values.get("interval_unit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CrossRegionCopyRetainRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dlm.mixins.CfnLifecyclePolicyPropsMixin.CrossRegionCopyRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cmk_arn": "cmkArn",
            "copy_tags": "copyTags",
            "deprecate_rule": "deprecateRule",
            "encrypted": "encrypted",
            "retain_rule": "retainRule",
            "target": "target",
            "target_region": "targetRegion",
        },
    )
    class CrossRegionCopyRuleProperty:
        def __init__(
            self,
            *,
            cmk_arn: typing.Optional[builtins.str] = None,
            copy_tags: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            deprecate_rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLifecyclePolicyPropsMixin.CrossRegionCopyDeprecateRuleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            encrypted: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            retain_rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLifecyclePolicyPropsMixin.CrossRegionCopyRetainRuleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            target: typing.Optional[builtins.str] = None,
            target_region: typing.Optional[builtins.str] = None,
        ) -> None:
            '''*[Custom snapshot and AMI policies only]* Specifies a cross-Region copy rule for a snapshot and AMI policies.

            .. epigraph::

               To specify a cross-Region copy action for event-based polices, use `CrossRegionCopyAction <https://docs.aws.amazon.com/dlm/latest/APIReference/API_CrossRegionCopyAction.html>`_ .

            :param cmk_arn: The Amazon Resource Name (ARN) of the AWS KMS key to use for EBS encryption. If this parameter is not specified, the default KMS key for the account is used.
            :param copy_tags: Indicates whether to copy all user-defined tags from the source snapshot or AMI to the cross-Region copy.
            :param deprecate_rule: *[Custom AMI policies only]* The AMI deprecation rule for cross-Region AMI copies created by the rule.
            :param encrypted: To encrypt a copy of an unencrypted snapshot if encryption by default is not enabled, enable encryption using this parameter. Copies of encrypted snapshots are encrypted, even if this parameter is false or if encryption by default is not enabled.
            :param retain_rule: The retention rule that indicates how long the cross-Region snapshot or AMI copies are to be retained in the destination Region.
            :param target: .. epigraph:: Use this parameter for snapshot policies only. For AMI policies, use *TargetRegion* instead. *[Custom snapshot policies only]* The target Region or the Amazon Resource Name (ARN) of the target Outpost for the snapshot copies.
            :param target_region: .. epigraph:: Use this parameter for AMI policies only. For snapshot policies, use *Target* instead. For snapshot policies created before the *Target* parameter was introduced, this parameter indicates the target Region for snapshot copies. *[Custom AMI policies only]* The target Region or the Amazon Resource Name (ARN) of the target Outpost for the snapshot copies.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dlm import mixins as dlm_mixins
                
                cross_region_copy_rule_property = dlm_mixins.CfnLifecyclePolicyPropsMixin.CrossRegionCopyRuleProperty(
                    cmk_arn="cmkArn",
                    copy_tags=False,
                    deprecate_rule=dlm_mixins.CfnLifecyclePolicyPropsMixin.CrossRegionCopyDeprecateRuleProperty(
                        interval=123,
                        interval_unit="intervalUnit"
                    ),
                    encrypted=False,
                    retain_rule=dlm_mixins.CfnLifecyclePolicyPropsMixin.CrossRegionCopyRetainRuleProperty(
                        interval=123,
                        interval_unit="intervalUnit"
                    ),
                    target="target",
                    target_region="targetRegion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bcaef2c51d663343e01848195a4e3b3297842098ea2e7b24fed51876b4c9095d)
                check_type(argname="argument cmk_arn", value=cmk_arn, expected_type=type_hints["cmk_arn"])
                check_type(argname="argument copy_tags", value=copy_tags, expected_type=type_hints["copy_tags"])
                check_type(argname="argument deprecate_rule", value=deprecate_rule, expected_type=type_hints["deprecate_rule"])
                check_type(argname="argument encrypted", value=encrypted, expected_type=type_hints["encrypted"])
                check_type(argname="argument retain_rule", value=retain_rule, expected_type=type_hints["retain_rule"])
                check_type(argname="argument target", value=target, expected_type=type_hints["target"])
                check_type(argname="argument target_region", value=target_region, expected_type=type_hints["target_region"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cmk_arn is not None:
                self._values["cmk_arn"] = cmk_arn
            if copy_tags is not None:
                self._values["copy_tags"] = copy_tags
            if deprecate_rule is not None:
                self._values["deprecate_rule"] = deprecate_rule
            if encrypted is not None:
                self._values["encrypted"] = encrypted
            if retain_rule is not None:
                self._values["retain_rule"] = retain_rule
            if target is not None:
                self._values["target"] = target
            if target_region is not None:
                self._values["target_region"] = target_region

        @builtins.property
        def cmk_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the AWS KMS key to use for EBS encryption.

            If this parameter is not specified, the default KMS key for the account is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyrule.html#cfn-dlm-lifecyclepolicy-crossregioncopyrule-cmkarn
            '''
            result = self._values.get("cmk_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def copy_tags(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether to copy all user-defined tags from the source snapshot or AMI to the cross-Region copy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyrule.html#cfn-dlm-lifecyclepolicy-crossregioncopyrule-copytags
            '''
            result = self._values.get("copy_tags")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def deprecate_rule(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.CrossRegionCopyDeprecateRuleProperty"]]:
            '''*[Custom AMI policies only]* The AMI deprecation rule for cross-Region AMI copies created by the rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyrule.html#cfn-dlm-lifecyclepolicy-crossregioncopyrule-deprecaterule
            '''
            result = self._values.get("deprecate_rule")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.CrossRegionCopyDeprecateRuleProperty"]], result)

        @builtins.property
        def encrypted(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''To encrypt a copy of an unencrypted snapshot if encryption by default is not enabled, enable encryption using this parameter.

            Copies of encrypted snapshots are encrypted, even if this parameter is false or if encryption by default is not enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyrule.html#cfn-dlm-lifecyclepolicy-crossregioncopyrule-encrypted
            '''
            result = self._values.get("encrypted")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def retain_rule(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.CrossRegionCopyRetainRuleProperty"]]:
            '''The retention rule that indicates how long the cross-Region snapshot or AMI copies are to be retained in the destination Region.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyrule.html#cfn-dlm-lifecyclepolicy-crossregioncopyrule-retainrule
            '''
            result = self._values.get("retain_rule")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.CrossRegionCopyRetainRuleProperty"]], result)

        @builtins.property
        def target(self) -> typing.Optional[builtins.str]:
            '''.. epigraph::

   Use this parameter for snapshot policies only. For AMI policies, use *TargetRegion* instead.

            *[Custom snapshot policies only]* The target Region or the Amazon Resource Name (ARN) of the target Outpost for the snapshot copies.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyrule.html#cfn-dlm-lifecyclepolicy-crossregioncopyrule-target
            '''
            result = self._values.get("target")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_region(self) -> typing.Optional[builtins.str]:
            '''.. epigraph::

   Use this parameter for AMI policies only.

            For snapshot policies, use *Target* instead. For snapshot policies created before the *Target* parameter was introduced, this parameter indicates the target Region for snapshot copies.

            *[Custom AMI policies only]* The target Region or the Amazon Resource Name (ARN) of the target Outpost for the snapshot copies.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyrule.html#cfn-dlm-lifecyclepolicy-crossregioncopyrule-targetregion
            '''
            result = self._values.get("target_region")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CrossRegionCopyRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dlm.mixins.CfnLifecyclePolicyPropsMixin.DeprecateRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "count": "count",
            "interval": "interval",
            "interval_unit": "intervalUnit",
        },
    )
    class DeprecateRuleProperty:
        def __init__(
            self,
            *,
            count: typing.Optional[jsii.Number] = None,
            interval: typing.Optional[jsii.Number] = None,
            interval_unit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''*[Custom AMI policies only]* Specifies an AMI deprecation rule for AMIs created by an AMI lifecycle policy.

            For age-based schedules, you must specify *Interval* and *IntervalUnit* . For count-based schedules, you must specify *Count* .

            :param count: If the schedule has a count-based retention rule, this parameter specifies the number of oldest AMIs to deprecate. The count must be less than or equal to the schedule's retention count, and it can't be greater than 1000.
            :param interval: If the schedule has an age-based retention rule, this parameter specifies the period after which to deprecate AMIs created by the schedule. The period must be less than or equal to the schedule's retention period, and it can't be greater than 10 years. This is equivalent to 120 months, 520 weeks, or 3650 days.
            :param interval_unit: The unit of time in which to measure the *Interval* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-deprecaterule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dlm import mixins as dlm_mixins
                
                deprecate_rule_property = dlm_mixins.CfnLifecyclePolicyPropsMixin.DeprecateRuleProperty(
                    count=123,
                    interval=123,
                    interval_unit="intervalUnit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3a61c37ccc633279754f9da8bb9f5f73dd8832c557e01d216af18f742dcb2be2)
                check_type(argname="argument count", value=count, expected_type=type_hints["count"])
                check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
                check_type(argname="argument interval_unit", value=interval_unit, expected_type=type_hints["interval_unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if count is not None:
                self._values["count"] = count
            if interval is not None:
                self._values["interval"] = interval
            if interval_unit is not None:
                self._values["interval_unit"] = interval_unit

        @builtins.property
        def count(self) -> typing.Optional[jsii.Number]:
            '''If the schedule has a count-based retention rule, this parameter specifies the number of oldest AMIs to deprecate.

            The count must be less than or equal to the schedule's retention count, and it can't be greater than 1000.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-deprecaterule.html#cfn-dlm-lifecyclepolicy-deprecaterule-count
            '''
            result = self._values.get("count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def interval(self) -> typing.Optional[jsii.Number]:
            '''If the schedule has an age-based retention rule, this parameter specifies the period after which to deprecate AMIs created by the schedule.

            The period must be less than or equal to the schedule's retention period, and it can't be greater than 10 years. This is equivalent to 120 months, 520 weeks, or 3650 days.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-deprecaterule.html#cfn-dlm-lifecyclepolicy-deprecaterule-interval
            '''
            result = self._values.get("interval")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def interval_unit(self) -> typing.Optional[builtins.str]:
            '''The unit of time in which to measure the *Interval* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-deprecaterule.html#cfn-dlm-lifecyclepolicy-deprecaterule-intervalunit
            '''
            result = self._values.get("interval_unit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeprecateRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dlm.mixins.CfnLifecyclePolicyPropsMixin.EncryptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"cmk_arn": "cmkArn", "encrypted": "encrypted"},
    )
    class EncryptionConfigurationProperty:
        def __init__(
            self,
            *,
            cmk_arn: typing.Optional[builtins.str] = None,
            encrypted: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''*[Event-based policies only]* Specifies the encryption settings for cross-Region snapshot copies created by event-based policies.

            :param cmk_arn: The Amazon Resource Name (ARN) of the AWS KMS key to use for EBS encryption. If this parameter is not specified, the default KMS key for the account is used.
            :param encrypted: To encrypt a copy of an unencrypted snapshot when encryption by default is not enabled, enable encryption using this parameter. Copies of encrypted snapshots are encrypted, even if this parameter is false or when encryption by default is not enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-encryptionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dlm import mixins as dlm_mixins
                
                encryption_configuration_property = dlm_mixins.CfnLifecyclePolicyPropsMixin.EncryptionConfigurationProperty(
                    cmk_arn="cmkArn",
                    encrypted=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e652eb6e0bcd5578b45adb8be0cf6f4639d458162b05a218b5af7570c60cf516)
                check_type(argname="argument cmk_arn", value=cmk_arn, expected_type=type_hints["cmk_arn"])
                check_type(argname="argument encrypted", value=encrypted, expected_type=type_hints["encrypted"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cmk_arn is not None:
                self._values["cmk_arn"] = cmk_arn
            if encrypted is not None:
                self._values["encrypted"] = encrypted

        @builtins.property
        def cmk_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the AWS KMS key to use for EBS encryption.

            If this parameter is not specified, the default KMS key for the account is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-encryptionconfiguration.html#cfn-dlm-lifecyclepolicy-encryptionconfiguration-cmkarn
            '''
            result = self._values.get("cmk_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def encrypted(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''To encrypt a copy of an unencrypted snapshot when encryption by default is not enabled, enable encryption using this parameter.

            Copies of encrypted snapshots are encrypted, even if this parameter is false or when encryption by default is not enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-encryptionconfiguration.html#cfn-dlm-lifecyclepolicy-encryptionconfiguration-encrypted
            '''
            result = self._values.get("encrypted")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dlm.mixins.CfnLifecyclePolicyPropsMixin.EventParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "description_regex": "descriptionRegex",
            "event_type": "eventType",
            "snapshot_owner": "snapshotOwner",
        },
    )
    class EventParametersProperty:
        def __init__(
            self,
            *,
            description_regex: typing.Optional[builtins.str] = None,
            event_type: typing.Optional[builtins.str] = None,
            snapshot_owner: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''*[Event-based policies only]* Specifies an event that activates an event-based policy.

            :param description_regex: The snapshot description that can trigger the policy. The description pattern is specified using a regular expression. The policy runs only if a snapshot with a description that matches the specified pattern is shared with your account. For example, specifying ``^.*Created for policy: policy-1234567890abcdef0.*$`` configures the policy to run only if snapshots created by policy ``policy-1234567890abcdef0`` are shared with your account.
            :param event_type: The type of event. Currently, only snapshot sharing events are supported.
            :param snapshot_owner: The IDs of the AWS accounts that can trigger policy by sharing snapshots with your account. The policy only runs if one of the specified AWS accounts shares a snapshot with your account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-eventparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dlm import mixins as dlm_mixins
                
                event_parameters_property = dlm_mixins.CfnLifecyclePolicyPropsMixin.EventParametersProperty(
                    description_regex="descriptionRegex",
                    event_type="eventType",
                    snapshot_owner=["snapshotOwner"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5d63c18260b31de3e747e98da88240c928e40d28d25bfc8cd046cb7911ceb8a1)
                check_type(argname="argument description_regex", value=description_regex, expected_type=type_hints["description_regex"])
                check_type(argname="argument event_type", value=event_type, expected_type=type_hints["event_type"])
                check_type(argname="argument snapshot_owner", value=snapshot_owner, expected_type=type_hints["snapshot_owner"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if description_regex is not None:
                self._values["description_regex"] = description_regex
            if event_type is not None:
                self._values["event_type"] = event_type
            if snapshot_owner is not None:
                self._values["snapshot_owner"] = snapshot_owner

        @builtins.property
        def description_regex(self) -> typing.Optional[builtins.str]:
            '''The snapshot description that can trigger the policy.

            The description pattern is specified using a regular expression. The policy runs only if a snapshot with a description that matches the specified pattern is shared with your account.

            For example, specifying ``^.*Created for policy: policy-1234567890abcdef0.*$`` configures the policy to run only if snapshots created by policy ``policy-1234567890abcdef0`` are shared with your account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-eventparameters.html#cfn-dlm-lifecyclepolicy-eventparameters-descriptionregex
            '''
            result = self._values.get("description_regex")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def event_type(self) -> typing.Optional[builtins.str]:
            '''The type of event.

            Currently, only snapshot sharing events are supported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-eventparameters.html#cfn-dlm-lifecyclepolicy-eventparameters-eventtype
            '''
            result = self._values.get("event_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def snapshot_owner(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The IDs of the AWS accounts that can trigger policy by sharing snapshots with your account.

            The policy only runs if one of the specified AWS accounts shares a snapshot with your account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-eventparameters.html#cfn-dlm-lifecyclepolicy-eventparameters-snapshotowner
            '''
            result = self._values.get("snapshot_owner")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dlm.mixins.CfnLifecyclePolicyPropsMixin.EventSourceProperty",
        jsii_struct_bases=[],
        name_mapping={"parameters": "parameters", "type": "type"},
    )
    class EventSourceProperty:
        def __init__(
            self,
            *,
            parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLifecyclePolicyPropsMixin.EventParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''*[Event-based policies only]* Specifies an event that activates an event-based policy.

            :param parameters: Information about the event.
            :param type: The source of the event. Currently only managed Amazon EventBridge (formerly known as Amazon CloudWatch) events are supported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-eventsource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dlm import mixins as dlm_mixins
                
                event_source_property = dlm_mixins.CfnLifecyclePolicyPropsMixin.EventSourceProperty(
                    parameters=dlm_mixins.CfnLifecyclePolicyPropsMixin.EventParametersProperty(
                        description_regex="descriptionRegex",
                        event_type="eventType",
                        snapshot_owner=["snapshotOwner"]
                    ),
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4efda3053919600c975d42ef09e1abd2774e6c0949e64c4fa9ada495d2eb31df)
                check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if parameters is not None:
                self._values["parameters"] = parameters
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.EventParametersProperty"]]:
            '''Information about the event.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-eventsource.html#cfn-dlm-lifecyclepolicy-eventsource-parameters
            '''
            result = self._values.get("parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.EventParametersProperty"]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The source of the event.

            Currently only managed Amazon EventBridge (formerly known as Amazon CloudWatch) events are supported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-eventsource.html#cfn-dlm-lifecyclepolicy-eventsource-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dlm.mixins.CfnLifecyclePolicyPropsMixin.ExclusionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "exclude_boot_volumes": "excludeBootVolumes",
            "exclude_tags": "excludeTags",
            "exclude_volume_types": "excludeVolumeTypes",
        },
    )
    class ExclusionsProperty:
        def __init__(
            self,
            *,
            exclude_boot_volumes: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            exclude_tags: typing.Any = None,
            exclude_volume_types: typing.Any = None,
        ) -> None:
            '''*[Default policies only]* Specifies exclusion parameters for volumes or instances for which you do not want to create snapshots or AMIs.

            The policy will not create snapshots or AMIs for target resources that match any of the specified exclusion parameters.

            :param exclude_boot_volumes: *[Default policies for EBS snapshots only]* Indicates whether to exclude volumes that are attached to instances as the boot volume. If you exclude boot volumes, only volumes attached as data (non-boot) volumes will be backed up by the policy. To exclude boot volumes, specify ``true`` .
            :param exclude_tags: *[Default policies for EBS-backed AMIs only]* Specifies whether to exclude volumes that have specific tags.
            :param exclude_volume_types: *[Default policies for EBS snapshots only]* Specifies the volume types to exclude. Volumes of the specified types will not be targeted by the policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-exclusions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dlm import mixins as dlm_mixins
                
                # exclude_tags: Any
                # exclude_volume_types: Any
                
                exclusions_property = dlm_mixins.CfnLifecyclePolicyPropsMixin.ExclusionsProperty(
                    exclude_boot_volumes=False,
                    exclude_tags=exclude_tags,
                    exclude_volume_types=exclude_volume_types
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c89f42aa9fe37a9fd6514ab0f060a9438f247d2f649aa6e880e142d2cd53e76a)
                check_type(argname="argument exclude_boot_volumes", value=exclude_boot_volumes, expected_type=type_hints["exclude_boot_volumes"])
                check_type(argname="argument exclude_tags", value=exclude_tags, expected_type=type_hints["exclude_tags"])
                check_type(argname="argument exclude_volume_types", value=exclude_volume_types, expected_type=type_hints["exclude_volume_types"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if exclude_boot_volumes is not None:
                self._values["exclude_boot_volumes"] = exclude_boot_volumes
            if exclude_tags is not None:
                self._values["exclude_tags"] = exclude_tags
            if exclude_volume_types is not None:
                self._values["exclude_volume_types"] = exclude_volume_types

        @builtins.property
        def exclude_boot_volumes(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''*[Default policies for EBS snapshots only]* Indicates whether to exclude volumes that are attached to instances as the boot volume.

            If you exclude boot volumes, only volumes attached as data (non-boot) volumes will be backed up by the policy. To exclude boot volumes, specify ``true`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-exclusions.html#cfn-dlm-lifecyclepolicy-exclusions-excludebootvolumes
            '''
            result = self._values.get("exclude_boot_volumes")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def exclude_tags(self) -> typing.Any:
            '''*[Default policies for EBS-backed AMIs only]* Specifies whether to exclude volumes that have specific tags.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-exclusions.html#cfn-dlm-lifecyclepolicy-exclusions-excludetags
            '''
            result = self._values.get("exclude_tags")
            return typing.cast(typing.Any, result)

        @builtins.property
        def exclude_volume_types(self) -> typing.Any:
            '''*[Default policies for EBS snapshots only]* Specifies the volume types to exclude.

            Volumes of the specified types will not be targeted by the policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-exclusions.html#cfn-dlm-lifecyclepolicy-exclusions-excludevolumetypes
            '''
            result = self._values.get("exclude_volume_types")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExclusionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dlm.mixins.CfnLifecyclePolicyPropsMixin.FastRestoreRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "availability_zones": "availabilityZones",
            "count": "count",
            "interval": "interval",
            "interval_unit": "intervalUnit",
        },
    )
    class FastRestoreRuleProperty:
        def __init__(
            self,
            *,
            availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
            count: typing.Optional[jsii.Number] = None,
            interval: typing.Optional[jsii.Number] = None,
            interval_unit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''*[Custom snapshot policies only]* Specifies a rule for enabling fast snapshot restore for snapshots created by snapshot policies.

            You can enable fast snapshot restore based on either a count or a time interval.

            :param availability_zones: The Availability Zones in which to enable fast snapshot restore.
            :param count: The number of snapshots to be enabled with fast snapshot restore.
            :param interval: The amount of time to enable fast snapshot restore. The maximum is 100 years. This is equivalent to 1200 months, 5200 weeks, or 36500 days.
            :param interval_unit: The unit of time for enabling fast snapshot restore.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-fastrestorerule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dlm import mixins as dlm_mixins
                
                fast_restore_rule_property = dlm_mixins.CfnLifecyclePolicyPropsMixin.FastRestoreRuleProperty(
                    availability_zones=["availabilityZones"],
                    count=123,
                    interval=123,
                    interval_unit="intervalUnit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3fe3649473a118edccb0f56529256d9542d066c3f62933624cb674543ce2c5f7)
                check_type(argname="argument availability_zones", value=availability_zones, expected_type=type_hints["availability_zones"])
                check_type(argname="argument count", value=count, expected_type=type_hints["count"])
                check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
                check_type(argname="argument interval_unit", value=interval_unit, expected_type=type_hints["interval_unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if availability_zones is not None:
                self._values["availability_zones"] = availability_zones
            if count is not None:
                self._values["count"] = count
            if interval is not None:
                self._values["interval"] = interval
            if interval_unit is not None:
                self._values["interval_unit"] = interval_unit

        @builtins.property
        def availability_zones(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The Availability Zones in which to enable fast snapshot restore.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-fastrestorerule.html#cfn-dlm-lifecyclepolicy-fastrestorerule-availabilityzones
            '''
            result = self._values.get("availability_zones")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def count(self) -> typing.Optional[jsii.Number]:
            '''The number of snapshots to be enabled with fast snapshot restore.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-fastrestorerule.html#cfn-dlm-lifecyclepolicy-fastrestorerule-count
            '''
            result = self._values.get("count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def interval(self) -> typing.Optional[jsii.Number]:
            '''The amount of time to enable fast snapshot restore.

            The maximum is 100 years. This is equivalent to 1200 months, 5200 weeks, or 36500 days.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-fastrestorerule.html#cfn-dlm-lifecyclepolicy-fastrestorerule-interval
            '''
            result = self._values.get("interval")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def interval_unit(self) -> typing.Optional[builtins.str]:
            '''The unit of time for enabling fast snapshot restore.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-fastrestorerule.html#cfn-dlm-lifecyclepolicy-fastrestorerule-intervalunit
            '''
            result = self._values.get("interval_unit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FastRestoreRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dlm.mixins.CfnLifecyclePolicyPropsMixin.ParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "exclude_boot_volume": "excludeBootVolume",
            "exclude_data_volume_tags": "excludeDataVolumeTags",
            "no_reboot": "noReboot",
        },
    )
    class ParametersProperty:
        def __init__(
            self,
            *,
            exclude_boot_volume: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            exclude_data_volume_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]]]] = None,
            no_reboot: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''*[Custom snapshot and AMI policies only]* Specifies optional parameters for snapshot and AMI policies.

            The set of valid parameters depends on the combination of policy type and target resource type.

            If you choose to exclude boot volumes and you specify tags that consequently exclude all of the additional data volumes attached to an instance, then Amazon Data Lifecycle Manager will not create any snapshots for the affected instance, and it will emit a ``SnapshotsCreateFailed`` Amazon CloudWatch metric. For more information, see `Monitor your policies using Amazon CloudWatch <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/monitor-dlm-cw-metrics.html>`_ .

            :param exclude_boot_volume: *[Custom snapshot policies that target instances only]* Indicates whether to exclude the root volume from multi-volume snapshot sets. The default is ``false`` . If you specify ``true`` , then the root volumes attached to targeted instances will be excluded from the multi-volume snapshot sets created by the policy.
            :param exclude_data_volume_tags: *[Custom snapshot policies that target instances only]* The tags used to identify data (non-root) volumes to exclude from multi-volume snapshot sets. If you create a snapshot lifecycle policy that targets instances and you specify tags for this parameter, then data volumes with the specified tags that are attached to targeted instances will be excluded from the multi-volume snapshot sets created by the policy.
            :param no_reboot: *[Custom AMI policies only]* Indicates whether targeted instances are rebooted when the lifecycle policy runs. ``true`` indicates that targeted instances are not rebooted when the policy runs. ``false`` indicates that target instances are rebooted when the policy runs. The default is ``true`` (instances are not rebooted).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-parameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dlm import mixins as dlm_mixins
                
                parameters_property = dlm_mixins.CfnLifecyclePolicyPropsMixin.ParametersProperty(
                    exclude_boot_volume=False,
                    exclude_data_volume_tags=[CfnTag(
                        key="key",
                        value="value"
                    )],
                    no_reboot=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7bf5f0e7af4ad072eb7ae59579339631435dd74c77fb1fd6f883556eb7a17c6b)
                check_type(argname="argument exclude_boot_volume", value=exclude_boot_volume, expected_type=type_hints["exclude_boot_volume"])
                check_type(argname="argument exclude_data_volume_tags", value=exclude_data_volume_tags, expected_type=type_hints["exclude_data_volume_tags"])
                check_type(argname="argument no_reboot", value=no_reboot, expected_type=type_hints["no_reboot"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if exclude_boot_volume is not None:
                self._values["exclude_boot_volume"] = exclude_boot_volume
            if exclude_data_volume_tags is not None:
                self._values["exclude_data_volume_tags"] = exclude_data_volume_tags
            if no_reboot is not None:
                self._values["no_reboot"] = no_reboot

        @builtins.property
        def exclude_boot_volume(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''*[Custom snapshot policies that target instances only]* Indicates whether to exclude the root volume from multi-volume snapshot sets.

            The default is ``false`` . If you specify ``true`` , then the root volumes attached to targeted instances will be excluded from the multi-volume snapshot sets created by the policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-parameters.html#cfn-dlm-lifecyclepolicy-parameters-excludebootvolume
            '''
            result = self._values.get("exclude_boot_volume")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def exclude_data_volume_tags(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_ceddda9d.CfnTag]]]]:
            '''*[Custom snapshot policies that target instances only]* The tags used to identify data (non-root) volumes to exclude from multi-volume snapshot sets.

            If you create a snapshot lifecycle policy that targets instances and you specify tags for this parameter, then data volumes with the specified tags that are attached to targeted instances will be excluded from the multi-volume snapshot sets created by the policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-parameters.html#cfn-dlm-lifecyclepolicy-parameters-excludedatavolumetags
            '''
            result = self._values.get("exclude_data_volume_tags")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_ceddda9d.CfnTag]]]], result)

        @builtins.property
        def no_reboot(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''*[Custom AMI policies only]* Indicates whether targeted instances are rebooted when the lifecycle policy runs.

            ``true`` indicates that targeted instances are not rebooted when the policy runs. ``false`` indicates that target instances are rebooted when the policy runs. The default is ``true`` (instances are not rebooted).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-parameters.html#cfn-dlm-lifecyclepolicy-parameters-noreboot
            '''
            result = self._values.get("no_reboot")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dlm.mixins.CfnLifecyclePolicyPropsMixin.PolicyDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "actions": "actions",
            "copy_tags": "copyTags",
            "create_interval": "createInterval",
            "cross_region_copy_targets": "crossRegionCopyTargets",
            "event_source": "eventSource",
            "exclusions": "exclusions",
            "extend_deletion": "extendDeletion",
            "parameters": "parameters",
            "policy_language": "policyLanguage",
            "policy_type": "policyType",
            "resource_locations": "resourceLocations",
            "resource_type": "resourceType",
            "resource_types": "resourceTypes",
            "retain_interval": "retainInterval",
            "schedules": "schedules",
            "target_tags": "targetTags",
        },
    )
    class PolicyDetailsProperty:
        def __init__(
            self,
            *,
            actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLifecyclePolicyPropsMixin.ActionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            copy_tags: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            create_interval: typing.Optional[jsii.Number] = None,
            cross_region_copy_targets: typing.Any = None,
            event_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLifecyclePolicyPropsMixin.EventSourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            exclusions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLifecyclePolicyPropsMixin.ExclusionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            extend_deletion: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLifecyclePolicyPropsMixin.ParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            policy_language: typing.Optional[builtins.str] = None,
            policy_type: typing.Optional[builtins.str] = None,
            resource_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
            resource_type: typing.Optional[builtins.str] = None,
            resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
            retain_interval: typing.Optional[jsii.Number] = None,
            schedules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLifecyclePolicyPropsMixin.ScheduleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            target_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Specifies the configuration of a lifecycle policy.

            :param actions: *[Event-based policies only]* The actions to be performed when the event-based policy is activated. You can specify only one action per policy.
            :param copy_tags: *[Default policies only]* Indicates whether the policy should copy tags from the source resource to the snapshot or AMI. If you do not specify a value, the default is ``false`` . Default: false
            :param create_interval: *[Default policies only]* Specifies how often the policy should run and create snapshots or AMIs. The creation frequency can range from 1 to 7 days. If you do not specify a value, the default is 1. Default: 1
            :param cross_region_copy_targets: *[Default policies only]* Specifies destination Regions for snapshot or AMI copies. You can specify up to 3 destination Regions. If you do not want to create cross-Region copies, omit this parameter.
            :param event_source: *[Event-based policies only]* The event that activates the event-based policy.
            :param exclusions: *[Default policies only]* Specifies exclusion parameters for volumes or instances for which you do not want to create snapshots or AMIs. The policy will not create snapshots or AMIs for target resources that match any of the specified exclusion parameters.
            :param extend_deletion: *[Default policies only]* Defines the snapshot or AMI retention behavior for the policy if the source volume or instance is deleted, or if the policy enters the error, disabled, or deleted state. By default ( *ExtendDeletion=false* ): - If a source resource is deleted, Amazon Data Lifecycle Manager will continue to delete previously created snapshots or AMIs, up to but not including the last one, based on the specified retention period. If you want Amazon Data Lifecycle Manager to delete all snapshots or AMIs, including the last one, specify ``true`` . - If a policy enters the error, disabled, or deleted state, Amazon Data Lifecycle Manager stops deleting snapshots and AMIs. If you want Amazon Data Lifecycle Manager to continue deleting snapshots or AMIs, including the last one, if the policy enters one of these states, specify ``true`` . If you enable extended deletion ( *ExtendDeletion=true* ), you override both default behaviors simultaneously. If you do not specify a value, the default is ``false`` . Default: false
            :param parameters: *[Custom snapshot and AMI policies only]* A set of optional parameters for snapshot and AMI lifecycle policies. .. epigraph:: If you are modifying a policy that was created or previously modified using the Amazon Data Lifecycle Manager console, then you must include this parameter and specify either the default values or the new values that you require. You can't omit this parameter or set its values to null.
            :param policy_language: The type of policy to create. Specify one of the following:. - ``SIMPLIFIED`` To create a default policy. - ``STANDARD`` To create a custom policy.
            :param policy_type: The type of policy. Specify ``EBS_SNAPSHOT_MANAGEMENT`` to create a lifecycle policy that manages the lifecycle of Amazon EBS snapshots. Specify ``IMAGE_MANAGEMENT`` to create a lifecycle policy that manages the lifecycle of EBS-backed AMIs. Specify ``EVENT_BASED_POLICY`` to create an event-based policy that performs specific actions when a defined event occurs in your AWS account . The default is ``EBS_SNAPSHOT_MANAGEMENT`` .
            :param resource_locations: *[Custom snapshot and AMI policies only]* The location of the resources to backup. - If the source resources are located in a Region, specify ``CLOUD`` . In this case, the policy targets all resources of the specified type with matching target tags across all Availability Zones in the Region. - *[Custom snapshot policies only]* If the source resources are located in a Local Zone, specify ``LOCAL_ZONE`` . In this case, the policy targets all resources of the specified type with matching target tags across all Local Zones in the Region. - If the source resources are located on an Outpost in your account, specify ``OUTPOST`` . In this case, the policy targets all resources of the specified type with matching target tags across all of the Outposts in your account.
            :param resource_type: *[Default policies only]* Specify the type of default policy to create. - To create a default policy for EBS snapshots, that creates snapshots of all volumes in the Region that do not have recent backups, specify ``VOLUME`` . - To create a default policy for EBS-backed AMIs, that creates EBS-backed AMIs from all instances in the Region that do not have recent backups, specify ``INSTANCE`` .
            :param resource_types: *[Custom snapshot policies only]* The target resource type for snapshot and AMI lifecycle policies. Use ``VOLUME`` to create snapshots of individual volumes or use ``INSTANCE`` to create multi-volume snapshots from the volumes for an instance.
            :param retain_interval: *[Default policies only]* Specifies how long the policy should retain snapshots or AMIs before deleting them. The retention period can range from 2 to 14 days, but it must be greater than the creation frequency to ensure that the policy retains at least 1 snapshot or AMI at any given time. If you do not specify a value, the default is 7. Default: 7
            :param schedules: *[Custom snapshot and AMI policies only]* The schedules of policy-defined actions for snapshot and AMI lifecycle policies. A policy can have up to four schedules—one mandatory schedule and up to three optional schedules.
            :param target_tags: *[Custom snapshot and AMI policies only]* The single tag that identifies targeted resources for this policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-policydetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dlm import mixins as dlm_mixins
                
                # cross_region_copy_targets: Any
                # exclude_tags: Any
                # exclude_volume_types: Any
                
                policy_details_property = dlm_mixins.CfnLifecyclePolicyPropsMixin.PolicyDetailsProperty(
                    actions=[dlm_mixins.CfnLifecyclePolicyPropsMixin.ActionProperty(
                        cross_region_copy=[dlm_mixins.CfnLifecyclePolicyPropsMixin.CrossRegionCopyActionProperty(
                            encryption_configuration=dlm_mixins.CfnLifecyclePolicyPropsMixin.EncryptionConfigurationProperty(
                                cmk_arn="cmkArn",
                                encrypted=False
                            ),
                            retain_rule=dlm_mixins.CfnLifecyclePolicyPropsMixin.CrossRegionCopyRetainRuleProperty(
                                interval=123,
                                interval_unit="intervalUnit"
                            ),
                            target="target"
                        )],
                        name="name"
                    )],
                    copy_tags=False,
                    create_interval=123,
                    cross_region_copy_targets=cross_region_copy_targets,
                    event_source=dlm_mixins.CfnLifecyclePolicyPropsMixin.EventSourceProperty(
                        parameters=dlm_mixins.CfnLifecyclePolicyPropsMixin.EventParametersProperty(
                            description_regex="descriptionRegex",
                            event_type="eventType",
                            snapshot_owner=["snapshotOwner"]
                        ),
                        type="type"
                    ),
                    exclusions=dlm_mixins.CfnLifecyclePolicyPropsMixin.ExclusionsProperty(
                        exclude_boot_volumes=False,
                        exclude_tags=exclude_tags,
                        exclude_volume_types=exclude_volume_types
                    ),
                    extend_deletion=False,
                    parameters=dlm_mixins.CfnLifecyclePolicyPropsMixin.ParametersProperty(
                        exclude_boot_volume=False,
                        exclude_data_volume_tags=[CfnTag(
                            key="key",
                            value="value"
                        )],
                        no_reboot=False
                    ),
                    policy_language="policyLanguage",
                    policy_type="policyType",
                    resource_locations=["resourceLocations"],
                    resource_type="resourceType",
                    resource_types=["resourceTypes"],
                    retain_interval=123,
                    schedules=[dlm_mixins.CfnLifecyclePolicyPropsMixin.ScheduleProperty(
                        archive_rule=dlm_mixins.CfnLifecyclePolicyPropsMixin.ArchiveRuleProperty(
                            retain_rule=dlm_mixins.CfnLifecyclePolicyPropsMixin.ArchiveRetainRuleProperty(
                                retention_archive_tier=dlm_mixins.CfnLifecyclePolicyPropsMixin.RetentionArchiveTierProperty(
                                    count=123,
                                    interval=123,
                                    interval_unit="intervalUnit"
                                )
                            )
                        ),
                        copy_tags=False,
                        create_rule=dlm_mixins.CfnLifecyclePolicyPropsMixin.CreateRuleProperty(
                            cron_expression="cronExpression",
                            interval=123,
                            interval_unit="intervalUnit",
                            location="location",
                            scripts=[dlm_mixins.CfnLifecyclePolicyPropsMixin.ScriptProperty(
                                execute_operation_on_script_failure=False,
                                execution_handler="executionHandler",
                                execution_handler_service="executionHandlerService",
                                execution_timeout=123,
                                maximum_retry_count=123,
                                stages=["stages"]
                            )],
                            times=["times"]
                        ),
                        cross_region_copy_rules=[dlm_mixins.CfnLifecyclePolicyPropsMixin.CrossRegionCopyRuleProperty(
                            cmk_arn="cmkArn",
                            copy_tags=False,
                            deprecate_rule=dlm_mixins.CfnLifecyclePolicyPropsMixin.CrossRegionCopyDeprecateRuleProperty(
                                interval=123,
                                interval_unit="intervalUnit"
                            ),
                            encrypted=False,
                            retain_rule=dlm_mixins.CfnLifecyclePolicyPropsMixin.CrossRegionCopyRetainRuleProperty(
                                interval=123,
                                interval_unit="intervalUnit"
                            ),
                            target="target",
                            target_region="targetRegion"
                        )],
                        deprecate_rule=dlm_mixins.CfnLifecyclePolicyPropsMixin.DeprecateRuleProperty(
                            count=123,
                            interval=123,
                            interval_unit="intervalUnit"
                        ),
                        fast_restore_rule=dlm_mixins.CfnLifecyclePolicyPropsMixin.FastRestoreRuleProperty(
                            availability_zones=["availabilityZones"],
                            count=123,
                            interval=123,
                            interval_unit="intervalUnit"
                        ),
                        name="name",
                        retain_rule=dlm_mixins.CfnLifecyclePolicyPropsMixin.RetainRuleProperty(
                            count=123,
                            interval=123,
                            interval_unit="intervalUnit"
                        ),
                        share_rules=[dlm_mixins.CfnLifecyclePolicyPropsMixin.ShareRuleProperty(
                            target_accounts=["targetAccounts"],
                            unshare_interval=123,
                            unshare_interval_unit="unshareIntervalUnit"
                        )],
                        tags_to_add=[CfnTag(
                            key="key",
                            value="value"
                        )],
                        variable_tags=[CfnTag(
                            key="key",
                            value="value"
                        )]
                    )],
                    target_tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e0b8c7895a6a2975016dc51e33470da8019a7a6fe9e3b2481e9438b94cd66d87)
                check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
                check_type(argname="argument copy_tags", value=copy_tags, expected_type=type_hints["copy_tags"])
                check_type(argname="argument create_interval", value=create_interval, expected_type=type_hints["create_interval"])
                check_type(argname="argument cross_region_copy_targets", value=cross_region_copy_targets, expected_type=type_hints["cross_region_copy_targets"])
                check_type(argname="argument event_source", value=event_source, expected_type=type_hints["event_source"])
                check_type(argname="argument exclusions", value=exclusions, expected_type=type_hints["exclusions"])
                check_type(argname="argument extend_deletion", value=extend_deletion, expected_type=type_hints["extend_deletion"])
                check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
                check_type(argname="argument policy_language", value=policy_language, expected_type=type_hints["policy_language"])
                check_type(argname="argument policy_type", value=policy_type, expected_type=type_hints["policy_type"])
                check_type(argname="argument resource_locations", value=resource_locations, expected_type=type_hints["resource_locations"])
                check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
                check_type(argname="argument resource_types", value=resource_types, expected_type=type_hints["resource_types"])
                check_type(argname="argument retain_interval", value=retain_interval, expected_type=type_hints["retain_interval"])
                check_type(argname="argument schedules", value=schedules, expected_type=type_hints["schedules"])
                check_type(argname="argument target_tags", value=target_tags, expected_type=type_hints["target_tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if actions is not None:
                self._values["actions"] = actions
            if copy_tags is not None:
                self._values["copy_tags"] = copy_tags
            if create_interval is not None:
                self._values["create_interval"] = create_interval
            if cross_region_copy_targets is not None:
                self._values["cross_region_copy_targets"] = cross_region_copy_targets
            if event_source is not None:
                self._values["event_source"] = event_source
            if exclusions is not None:
                self._values["exclusions"] = exclusions
            if extend_deletion is not None:
                self._values["extend_deletion"] = extend_deletion
            if parameters is not None:
                self._values["parameters"] = parameters
            if policy_language is not None:
                self._values["policy_language"] = policy_language
            if policy_type is not None:
                self._values["policy_type"] = policy_type
            if resource_locations is not None:
                self._values["resource_locations"] = resource_locations
            if resource_type is not None:
                self._values["resource_type"] = resource_type
            if resource_types is not None:
                self._values["resource_types"] = resource_types
            if retain_interval is not None:
                self._values["retain_interval"] = retain_interval
            if schedules is not None:
                self._values["schedules"] = schedules
            if target_tags is not None:
                self._values["target_tags"] = target_tags

        @builtins.property
        def actions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.ActionProperty"]]]]:
            '''*[Event-based policies only]* The actions to be performed when the event-based policy is activated.

            You can specify only one action per policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-policydetails.html#cfn-dlm-lifecyclepolicy-policydetails-actions
            '''
            result = self._values.get("actions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.ActionProperty"]]]], result)

        @builtins.property
        def copy_tags(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''*[Default policies only]* Indicates whether the policy should copy tags from the source resource to the snapshot or AMI.

            If you do not specify a value, the default is ``false`` .

            Default: false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-policydetails.html#cfn-dlm-lifecyclepolicy-policydetails-copytags
            '''
            result = self._values.get("copy_tags")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def create_interval(self) -> typing.Optional[jsii.Number]:
            '''*[Default policies only]* Specifies how often the policy should run and create snapshots or AMIs.

            The creation frequency can range from 1 to 7 days. If you do not specify a value, the default is 1.

            Default: 1

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-policydetails.html#cfn-dlm-lifecyclepolicy-policydetails-createinterval
            '''
            result = self._values.get("create_interval")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def cross_region_copy_targets(self) -> typing.Any:
            '''*[Default policies only]* Specifies destination Regions for snapshot or AMI copies.

            You can specify up to 3 destination Regions. If you do not want to create cross-Region copies, omit this parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-policydetails.html#cfn-dlm-lifecyclepolicy-policydetails-crossregioncopytargets
            '''
            result = self._values.get("cross_region_copy_targets")
            return typing.cast(typing.Any, result)

        @builtins.property
        def event_source(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.EventSourceProperty"]]:
            '''*[Event-based policies only]* The event that activates the event-based policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-policydetails.html#cfn-dlm-lifecyclepolicy-policydetails-eventsource
            '''
            result = self._values.get("event_source")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.EventSourceProperty"]], result)

        @builtins.property
        def exclusions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.ExclusionsProperty"]]:
            '''*[Default policies only]* Specifies exclusion parameters for volumes or instances for which you do not want to create snapshots or AMIs.

            The policy will not create snapshots or AMIs for target resources that match any of the specified exclusion parameters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-policydetails.html#cfn-dlm-lifecyclepolicy-policydetails-exclusions
            '''
            result = self._values.get("exclusions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.ExclusionsProperty"]], result)

        @builtins.property
        def extend_deletion(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''*[Default policies only]* Defines the snapshot or AMI retention behavior for the policy if the source volume or instance is deleted, or if the policy enters the error, disabled, or deleted state.

            By default ( *ExtendDeletion=false* ):

            - If a source resource is deleted, Amazon Data Lifecycle Manager will continue to delete previously created snapshots or AMIs, up to but not including the last one, based on the specified retention period. If you want Amazon Data Lifecycle Manager to delete all snapshots or AMIs, including the last one, specify ``true`` .
            - If a policy enters the error, disabled, or deleted state, Amazon Data Lifecycle Manager stops deleting snapshots and AMIs. If you want Amazon Data Lifecycle Manager to continue deleting snapshots or AMIs, including the last one, if the policy enters one of these states, specify ``true`` .

            If you enable extended deletion ( *ExtendDeletion=true* ), you override both default behaviors simultaneously.

            If you do not specify a value, the default is ``false`` .

            Default: false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-policydetails.html#cfn-dlm-lifecyclepolicy-policydetails-extenddeletion
            '''
            result = self._values.get("extend_deletion")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.ParametersProperty"]]:
            '''*[Custom snapshot and AMI policies only]* A set of optional parameters for snapshot and AMI lifecycle policies.

            .. epigraph::

               If you are modifying a policy that was created or previously modified using the Amazon Data Lifecycle Manager console, then you must include this parameter and specify either the default values or the new values that you require. You can't omit this parameter or set its values to null.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-policydetails.html#cfn-dlm-lifecyclepolicy-policydetails-parameters
            '''
            result = self._values.get("parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.ParametersProperty"]], result)

        @builtins.property
        def policy_language(self) -> typing.Optional[builtins.str]:
            '''The type of policy to create. Specify one of the following:.

            - ``SIMPLIFIED`` To create a default policy.
            - ``STANDARD`` To create a custom policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-policydetails.html#cfn-dlm-lifecyclepolicy-policydetails-policylanguage
            '''
            result = self._values.get("policy_language")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def policy_type(self) -> typing.Optional[builtins.str]:
            '''The type of policy.

            Specify ``EBS_SNAPSHOT_MANAGEMENT`` to create a lifecycle policy that manages the lifecycle of Amazon EBS snapshots. Specify ``IMAGE_MANAGEMENT`` to create a lifecycle policy that manages the lifecycle of EBS-backed AMIs. Specify ``EVENT_BASED_POLICY`` to create an event-based policy that performs specific actions when a defined event occurs in your AWS account .

            The default is ``EBS_SNAPSHOT_MANAGEMENT`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-policydetails.html#cfn-dlm-lifecyclepolicy-policydetails-policytype
            '''
            result = self._values.get("policy_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_locations(self) -> typing.Optional[typing.List[builtins.str]]:
            '''*[Custom snapshot and AMI policies only]* The location of the resources to backup.

            - If the source resources are located in a Region, specify ``CLOUD`` . In this case, the policy targets all resources of the specified type with matching target tags across all Availability Zones in the Region.
            - *[Custom snapshot policies only]* If the source resources are located in a Local Zone, specify ``LOCAL_ZONE`` . In this case, the policy targets all resources of the specified type with matching target tags across all Local Zones in the Region.
            - If the source resources are located on an Outpost in your account, specify ``OUTPOST`` . In this case, the policy targets all resources of the specified type with matching target tags across all of the Outposts in your account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-policydetails.html#cfn-dlm-lifecyclepolicy-policydetails-resourcelocations
            '''
            result = self._values.get("resource_locations")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def resource_type(self) -> typing.Optional[builtins.str]:
            '''*[Default policies only]* Specify the type of default policy to create.

            - To create a default policy for EBS snapshots, that creates snapshots of all volumes in the Region that do not have recent backups, specify ``VOLUME`` .
            - To create a default policy for EBS-backed AMIs, that creates EBS-backed AMIs from all instances in the Region that do not have recent backups, specify ``INSTANCE`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-policydetails.html#cfn-dlm-lifecyclepolicy-policydetails-resourcetype
            '''
            result = self._values.get("resource_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''*[Custom snapshot policies only]* The target resource type for snapshot and AMI lifecycle policies.

            Use ``VOLUME`` to create snapshots of individual volumes or use ``INSTANCE`` to create multi-volume snapshots from the volumes for an instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-policydetails.html#cfn-dlm-lifecyclepolicy-policydetails-resourcetypes
            '''
            result = self._values.get("resource_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def retain_interval(self) -> typing.Optional[jsii.Number]:
            '''*[Default policies only]* Specifies how long the policy should retain snapshots or AMIs before deleting them.

            The retention period can range from 2 to 14 days, but it must be greater than the creation frequency to ensure that the policy retains at least 1 snapshot or AMI at any given time. If you do not specify a value, the default is 7.

            Default: 7

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-policydetails.html#cfn-dlm-lifecyclepolicy-policydetails-retaininterval
            '''
            result = self._values.get("retain_interval")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def schedules(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.ScheduleProperty"]]]]:
            '''*[Custom snapshot and AMI policies only]* The schedules of policy-defined actions for snapshot and AMI lifecycle policies.

            A policy can have up to four schedules—one mandatory schedule and up to three optional schedules.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-policydetails.html#cfn-dlm-lifecyclepolicy-policydetails-schedules
            '''
            result = self._values.get("schedules")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.ScheduleProperty"]]]], result)

        @builtins.property
        def target_tags(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_ceddda9d.CfnTag]]]]:
            '''*[Custom snapshot and AMI policies only]* The single tag that identifies targeted resources for this policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-policydetails.html#cfn-dlm-lifecyclepolicy-policydetails-targettags
            '''
            result = self._values.get("target_tags")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_ceddda9d.CfnTag]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PolicyDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dlm.mixins.CfnLifecyclePolicyPropsMixin.RetainRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "count": "count",
            "interval": "interval",
            "interval_unit": "intervalUnit",
        },
    )
    class RetainRuleProperty:
        def __init__(
            self,
            *,
            count: typing.Optional[jsii.Number] = None,
            interval: typing.Optional[jsii.Number] = None,
            interval_unit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''*[Custom snapshot and AMI policies only]* Specifies a retention rule for snapshots created by snapshot policies, or for AMIs created by AMI policies.

            .. epigraph::

               For snapshot policies that have an `ArchiveRule <https://docs.aws.amazon.com/dlm/latest/APIReference/API_ArchiveRule.html>`_ , this retention rule applies to standard tier retention. When the retention threshold is met, snapshots are moved from the standard to the archive tier.

               For snapshot policies that do not have an *ArchiveRule* , snapshots are permanently deleted when this retention threshold is met.

            You can retain snapshots based on either a count or a time interval.

            - *Count-based retention*

            You must specify *Count* . If you specify an `ArchiveRule <https://docs.aws.amazon.com/dlm/latest/APIReference/API_ArchiveRule.html>`_ for the schedule, then you can specify a retention count of ``0`` to archive snapshots immediately after creation. If you specify a `FastRestoreRule <https://docs.aws.amazon.com/dlm/latest/APIReference/API_FastRestoreRule.html>`_ , `ShareRule <https://docs.aws.amazon.com/dlm/latest/APIReference/API_ShareRule.html>`_ , or a `CrossRegionCopyRule <https://docs.aws.amazon.com/dlm/latest/APIReference/API_CrossRegionCopyRule.html>`_ , then you must specify a retention count of ``1`` or more.

            - *Age-based retention*

            You must specify *Interval* and *IntervalUnit* . If you specify an `ArchiveRule <https://docs.aws.amazon.com/dlm/latest/APIReference/API_ArchiveRule.html>`_ for the schedule, then you can specify a retention interval of ``0`` days to archive snapshots immediately after creation. If you specify a `FastRestoreRule <https://docs.aws.amazon.com/dlm/latest/APIReference/API_FastRestoreRule.html>`_ , `ShareRule <https://docs.aws.amazon.com/dlm/latest/APIReference/API_ShareRule.html>`_ , or a `CrossRegionCopyRule <https://docs.aws.amazon.com/dlm/latest/APIReference/API_CrossRegionCopyRule.html>`_ , then you must specify a retention interval of ``1`` day or more.

            :param count: The number of snapshots to retain for each volume, up to a maximum of 1000. For example if you want to retain a maximum of three snapshots, specify ``3`` . When the fourth snapshot is created, the oldest retained snapshot is deleted, or it is moved to the archive tier if you have specified an `ArchiveRule <https://docs.aws.amazon.com/dlm/latest/APIReference/API_ArchiveRule.html>`_ .
            :param interval: The amount of time to retain each snapshot. The maximum is 100 years. This is equivalent to 1200 months, 5200 weeks, or 36500 days.
            :param interval_unit: The unit of time for time-based retention. For example, to retain snapshots for 3 months, specify ``Interval=3`` and ``IntervalUnit=MONTHS`` . Once the snapshot has been retained for 3 months, it is deleted, or it is moved to the archive tier if you have specified an `ArchiveRule <https://docs.aws.amazon.com/dlm/latest/APIReference/API_ArchiveRule.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-retainrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dlm import mixins as dlm_mixins
                
                retain_rule_property = dlm_mixins.CfnLifecyclePolicyPropsMixin.RetainRuleProperty(
                    count=123,
                    interval=123,
                    interval_unit="intervalUnit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6de2548ede68b0c29edfd57122818f6ffb3823ae99e9f68633f0c72393c36899)
                check_type(argname="argument count", value=count, expected_type=type_hints["count"])
                check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
                check_type(argname="argument interval_unit", value=interval_unit, expected_type=type_hints["interval_unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if count is not None:
                self._values["count"] = count
            if interval is not None:
                self._values["interval"] = interval
            if interval_unit is not None:
                self._values["interval_unit"] = interval_unit

        @builtins.property
        def count(self) -> typing.Optional[jsii.Number]:
            '''The number of snapshots to retain for each volume, up to a maximum of 1000.

            For example if you want to retain a maximum of three snapshots, specify ``3`` . When the fourth snapshot is created, the oldest retained snapshot is deleted, or it is moved to the archive tier if you have specified an `ArchiveRule <https://docs.aws.amazon.com/dlm/latest/APIReference/API_ArchiveRule.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-retainrule.html#cfn-dlm-lifecyclepolicy-retainrule-count
            '''
            result = self._values.get("count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def interval(self) -> typing.Optional[jsii.Number]:
            '''The amount of time to retain each snapshot.

            The maximum is 100 years. This is equivalent to 1200 months, 5200 weeks, or 36500 days.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-retainrule.html#cfn-dlm-lifecyclepolicy-retainrule-interval
            '''
            result = self._values.get("interval")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def interval_unit(self) -> typing.Optional[builtins.str]:
            '''The unit of time for time-based retention.

            For example, to retain snapshots for 3 months, specify ``Interval=3`` and ``IntervalUnit=MONTHS`` . Once the snapshot has been retained for 3 months, it is deleted, or it is moved to the archive tier if you have specified an `ArchiveRule <https://docs.aws.amazon.com/dlm/latest/APIReference/API_ArchiveRule.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-retainrule.html#cfn-dlm-lifecyclepolicy-retainrule-intervalunit
            '''
            result = self._values.get("interval_unit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RetainRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dlm.mixins.CfnLifecyclePolicyPropsMixin.RetentionArchiveTierProperty",
        jsii_struct_bases=[],
        name_mapping={
            "count": "count",
            "interval": "interval",
            "interval_unit": "intervalUnit",
        },
    )
    class RetentionArchiveTierProperty:
        def __init__(
            self,
            *,
            count: typing.Optional[jsii.Number] = None,
            interval: typing.Optional[jsii.Number] = None,
            interval_unit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''*[Custom snapshot policies only]* Describes the retention rule for archived snapshots.

            Once the archive retention threshold is met, the snapshots are permanently deleted from the archive tier.
            .. epigraph::

               The archive retention rule must retain snapshots in the archive tier for a minimum of 90 days.

            For *count-based schedules* , you must specify *Count* . For *age-based schedules* , you must specify *Interval* and *IntervalUnit* .

            For more information about using snapshot archiving, see `Considerations for snapshot lifecycle policies <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/snapshot-ami-policy.html#dlm-archive>`_ .

            :param count: The maximum number of snapshots to retain in the archive storage tier for each volume. The count must ensure that each snapshot remains in the archive tier for at least 90 days. For example, if the schedule creates snapshots every 30 days, you must specify a count of 3 or more to ensure that each snapshot is archived for at least 90 days.
            :param interval: Specifies the period of time to retain snapshots in the archive tier. After this period expires, the snapshot is permanently deleted.
            :param interval_unit: The unit of time in which to measure the *Interval* . For example, to retain a snapshots in the archive tier for 6 months, specify ``Interval=6`` and ``IntervalUnit=MONTHS`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-retentionarchivetier.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dlm import mixins as dlm_mixins
                
                retention_archive_tier_property = dlm_mixins.CfnLifecyclePolicyPropsMixin.RetentionArchiveTierProperty(
                    count=123,
                    interval=123,
                    interval_unit="intervalUnit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__154b3b018af24cfd0fb8770ce5b1a8f6f248bbb70fa9d51f19b0a3c37b402bc3)
                check_type(argname="argument count", value=count, expected_type=type_hints["count"])
                check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
                check_type(argname="argument interval_unit", value=interval_unit, expected_type=type_hints["interval_unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if count is not None:
                self._values["count"] = count
            if interval is not None:
                self._values["interval"] = interval
            if interval_unit is not None:
                self._values["interval_unit"] = interval_unit

        @builtins.property
        def count(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of snapshots to retain in the archive storage tier for each volume.

            The count must ensure that each snapshot remains in the archive tier for at least 90 days. For example, if the schedule creates snapshots every 30 days, you must specify a count of 3 or more to ensure that each snapshot is archived for at least 90 days.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-retentionarchivetier.html#cfn-dlm-lifecyclepolicy-retentionarchivetier-count
            '''
            result = self._values.get("count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def interval(self) -> typing.Optional[jsii.Number]:
            '''Specifies the period of time to retain snapshots in the archive tier.

            After this period expires, the snapshot is permanently deleted.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-retentionarchivetier.html#cfn-dlm-lifecyclepolicy-retentionarchivetier-interval
            '''
            result = self._values.get("interval")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def interval_unit(self) -> typing.Optional[builtins.str]:
            '''The unit of time in which to measure the *Interval* .

            For example, to retain a snapshots in the archive tier for 6 months, specify ``Interval=6`` and ``IntervalUnit=MONTHS`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-retentionarchivetier.html#cfn-dlm-lifecyclepolicy-retentionarchivetier-intervalunit
            '''
            result = self._values.get("interval_unit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RetentionArchiveTierProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dlm.mixins.CfnLifecyclePolicyPropsMixin.ScheduleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "archive_rule": "archiveRule",
            "copy_tags": "copyTags",
            "create_rule": "createRule",
            "cross_region_copy_rules": "crossRegionCopyRules",
            "deprecate_rule": "deprecateRule",
            "fast_restore_rule": "fastRestoreRule",
            "name": "name",
            "retain_rule": "retainRule",
            "share_rules": "shareRules",
            "tags_to_add": "tagsToAdd",
            "variable_tags": "variableTags",
        },
    )
    class ScheduleProperty:
        def __init__(
            self,
            *,
            archive_rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLifecyclePolicyPropsMixin.ArchiveRuleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            copy_tags: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            create_rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLifecyclePolicyPropsMixin.CreateRuleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            cross_region_copy_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLifecyclePolicyPropsMixin.CrossRegionCopyRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            deprecate_rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLifecyclePolicyPropsMixin.DeprecateRuleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            fast_restore_rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLifecyclePolicyPropsMixin.FastRestoreRuleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            name: typing.Optional[builtins.str] = None,
            retain_rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLifecyclePolicyPropsMixin.RetainRuleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            share_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLifecyclePolicyPropsMixin.ShareRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            tags_to_add: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]]]] = None,
            variable_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''*[Custom snapshot and AMI policies only]* Specifies a schedule for a snapshot or AMI lifecycle policy.

            :param archive_rule: *[Custom snapshot policies that target volumes only]* The snapshot archiving rule for the schedule. When you specify an archiving rule, snapshots are automatically moved from the standard tier to the archive tier once the schedule's retention threshold is met. Snapshots are then retained in the archive tier for the archive retention period that you specify. For more information about using snapshot archiving, see `Considerations for snapshot lifecycle policies <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/snapshot-ami-policy.html#dlm-archive>`_ .
            :param copy_tags: Copy all user-defined tags on a source volume to snapshots of the volume created by this policy.
            :param create_rule: The creation rule.
            :param cross_region_copy_rules: Specifies a rule for copying snapshots or AMIs across Regions. .. epigraph:: You can't specify cross-Region copy rules for policies that create snapshots on an Outpost or in a Local Zone. If the policy creates snapshots in a Region, then snapshots can be copied to up to three Regions or Outposts.
            :param deprecate_rule: *[Custom AMI policies only]* The AMI deprecation rule for the schedule.
            :param fast_restore_rule: *[Custom snapshot policies only]* The rule for enabling fast snapshot restore.
            :param name: The name of the schedule.
            :param retain_rule: The retention rule for snapshots or AMIs created by the policy.
            :param share_rules: *[Custom snapshot policies only]* The rule for sharing snapshots with other AWS accounts .
            :param tags_to_add: The tags to apply to policy-created resources. These user-defined tags are in addition to the AWS -added lifecycle tags.
            :param variable_tags: *[AMI policies and snapshot policies that target instances only]* A collection of key/value pairs with values determined dynamically when the policy is executed. Keys may be any valid Amazon EC2 tag key. Values must be in one of the two following formats: ``$(instance-id)`` or ``$(timestamp)`` . Variable tags are only valid for EBS Snapshot Management – Instance policies.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-schedule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dlm import mixins as dlm_mixins
                
                schedule_property = dlm_mixins.CfnLifecyclePolicyPropsMixin.ScheduleProperty(
                    archive_rule=dlm_mixins.CfnLifecyclePolicyPropsMixin.ArchiveRuleProperty(
                        retain_rule=dlm_mixins.CfnLifecyclePolicyPropsMixin.ArchiveRetainRuleProperty(
                            retention_archive_tier=dlm_mixins.CfnLifecyclePolicyPropsMixin.RetentionArchiveTierProperty(
                                count=123,
                                interval=123,
                                interval_unit="intervalUnit"
                            )
                        )
                    ),
                    copy_tags=False,
                    create_rule=dlm_mixins.CfnLifecyclePolicyPropsMixin.CreateRuleProperty(
                        cron_expression="cronExpression",
                        interval=123,
                        interval_unit="intervalUnit",
                        location="location",
                        scripts=[dlm_mixins.CfnLifecyclePolicyPropsMixin.ScriptProperty(
                            execute_operation_on_script_failure=False,
                            execution_handler="executionHandler",
                            execution_handler_service="executionHandlerService",
                            execution_timeout=123,
                            maximum_retry_count=123,
                            stages=["stages"]
                        )],
                        times=["times"]
                    ),
                    cross_region_copy_rules=[dlm_mixins.CfnLifecyclePolicyPropsMixin.CrossRegionCopyRuleProperty(
                        cmk_arn="cmkArn",
                        copy_tags=False,
                        deprecate_rule=dlm_mixins.CfnLifecyclePolicyPropsMixin.CrossRegionCopyDeprecateRuleProperty(
                            interval=123,
                            interval_unit="intervalUnit"
                        ),
                        encrypted=False,
                        retain_rule=dlm_mixins.CfnLifecyclePolicyPropsMixin.CrossRegionCopyRetainRuleProperty(
                            interval=123,
                            interval_unit="intervalUnit"
                        ),
                        target="target",
                        target_region="targetRegion"
                    )],
                    deprecate_rule=dlm_mixins.CfnLifecyclePolicyPropsMixin.DeprecateRuleProperty(
                        count=123,
                        interval=123,
                        interval_unit="intervalUnit"
                    ),
                    fast_restore_rule=dlm_mixins.CfnLifecyclePolicyPropsMixin.FastRestoreRuleProperty(
                        availability_zones=["availabilityZones"],
                        count=123,
                        interval=123,
                        interval_unit="intervalUnit"
                    ),
                    name="name",
                    retain_rule=dlm_mixins.CfnLifecyclePolicyPropsMixin.RetainRuleProperty(
                        count=123,
                        interval=123,
                        interval_unit="intervalUnit"
                    ),
                    share_rules=[dlm_mixins.CfnLifecyclePolicyPropsMixin.ShareRuleProperty(
                        target_accounts=["targetAccounts"],
                        unshare_interval=123,
                        unshare_interval_unit="unshareIntervalUnit"
                    )],
                    tags_to_add=[CfnTag(
                        key="key",
                        value="value"
                    )],
                    variable_tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ebd8d2d5e6cbd125eedc0e9aa0b478e90b879c4c1b29d090daa88a73aba7c18e)
                check_type(argname="argument archive_rule", value=archive_rule, expected_type=type_hints["archive_rule"])
                check_type(argname="argument copy_tags", value=copy_tags, expected_type=type_hints["copy_tags"])
                check_type(argname="argument create_rule", value=create_rule, expected_type=type_hints["create_rule"])
                check_type(argname="argument cross_region_copy_rules", value=cross_region_copy_rules, expected_type=type_hints["cross_region_copy_rules"])
                check_type(argname="argument deprecate_rule", value=deprecate_rule, expected_type=type_hints["deprecate_rule"])
                check_type(argname="argument fast_restore_rule", value=fast_restore_rule, expected_type=type_hints["fast_restore_rule"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument retain_rule", value=retain_rule, expected_type=type_hints["retain_rule"])
                check_type(argname="argument share_rules", value=share_rules, expected_type=type_hints["share_rules"])
                check_type(argname="argument tags_to_add", value=tags_to_add, expected_type=type_hints["tags_to_add"])
                check_type(argname="argument variable_tags", value=variable_tags, expected_type=type_hints["variable_tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if archive_rule is not None:
                self._values["archive_rule"] = archive_rule
            if copy_tags is not None:
                self._values["copy_tags"] = copy_tags
            if create_rule is not None:
                self._values["create_rule"] = create_rule
            if cross_region_copy_rules is not None:
                self._values["cross_region_copy_rules"] = cross_region_copy_rules
            if deprecate_rule is not None:
                self._values["deprecate_rule"] = deprecate_rule
            if fast_restore_rule is not None:
                self._values["fast_restore_rule"] = fast_restore_rule
            if name is not None:
                self._values["name"] = name
            if retain_rule is not None:
                self._values["retain_rule"] = retain_rule
            if share_rules is not None:
                self._values["share_rules"] = share_rules
            if tags_to_add is not None:
                self._values["tags_to_add"] = tags_to_add
            if variable_tags is not None:
                self._values["variable_tags"] = variable_tags

        @builtins.property
        def archive_rule(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.ArchiveRuleProperty"]]:
            '''*[Custom snapshot policies that target volumes only]* The snapshot archiving rule for the schedule.

            When you specify an archiving rule, snapshots are automatically moved from the standard tier to the archive tier once the schedule's retention threshold is met. Snapshots are then retained in the archive tier for the archive retention period that you specify.

            For more information about using snapshot archiving, see `Considerations for snapshot lifecycle policies <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/snapshot-ami-policy.html#dlm-archive>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-schedule.html#cfn-dlm-lifecyclepolicy-schedule-archiverule
            '''
            result = self._values.get("archive_rule")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.ArchiveRuleProperty"]], result)

        @builtins.property
        def copy_tags(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Copy all user-defined tags on a source volume to snapshots of the volume created by this policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-schedule.html#cfn-dlm-lifecyclepolicy-schedule-copytags
            '''
            result = self._values.get("copy_tags")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def create_rule(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.CreateRuleProperty"]]:
            '''The creation rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-schedule.html#cfn-dlm-lifecyclepolicy-schedule-createrule
            '''
            result = self._values.get("create_rule")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.CreateRuleProperty"]], result)

        @builtins.property
        def cross_region_copy_rules(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.CrossRegionCopyRuleProperty"]]]]:
            '''Specifies a rule for copying snapshots or AMIs across Regions.

            .. epigraph::

               You can't specify cross-Region copy rules for policies that create snapshots on an Outpost or in a Local Zone. If the policy creates snapshots in a Region, then snapshots can be copied to up to three Regions or Outposts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-schedule.html#cfn-dlm-lifecyclepolicy-schedule-crossregioncopyrules
            '''
            result = self._values.get("cross_region_copy_rules")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.CrossRegionCopyRuleProperty"]]]], result)

        @builtins.property
        def deprecate_rule(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.DeprecateRuleProperty"]]:
            '''*[Custom AMI policies only]* The AMI deprecation rule for the schedule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-schedule.html#cfn-dlm-lifecyclepolicy-schedule-deprecaterule
            '''
            result = self._values.get("deprecate_rule")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.DeprecateRuleProperty"]], result)

        @builtins.property
        def fast_restore_rule(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.FastRestoreRuleProperty"]]:
            '''*[Custom snapshot policies only]* The rule for enabling fast snapshot restore.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-schedule.html#cfn-dlm-lifecyclepolicy-schedule-fastrestorerule
            '''
            result = self._values.get("fast_restore_rule")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.FastRestoreRuleProperty"]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the schedule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-schedule.html#cfn-dlm-lifecyclepolicy-schedule-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def retain_rule(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.RetainRuleProperty"]]:
            '''The retention rule for snapshots or AMIs created by the policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-schedule.html#cfn-dlm-lifecyclepolicy-schedule-retainrule
            '''
            result = self._values.get("retain_rule")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.RetainRuleProperty"]], result)

        @builtins.property
        def share_rules(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.ShareRuleProperty"]]]]:
            '''*[Custom snapshot policies only]* The rule for sharing snapshots with other AWS accounts .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-schedule.html#cfn-dlm-lifecyclepolicy-schedule-sharerules
            '''
            result = self._values.get("share_rules")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.ShareRuleProperty"]]]], result)

        @builtins.property
        def tags_to_add(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_ceddda9d.CfnTag]]]]:
            '''The tags to apply to policy-created resources.

            These user-defined tags are in addition to the AWS -added lifecycle tags.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-schedule.html#cfn-dlm-lifecyclepolicy-schedule-tagstoadd
            '''
            result = self._values.get("tags_to_add")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_ceddda9d.CfnTag]]]], result)

        @builtins.property
        def variable_tags(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_ceddda9d.CfnTag]]]]:
            '''*[AMI policies and snapshot policies that target instances only]* A collection of key/value pairs with values determined dynamically when the policy is executed.

            Keys may be any valid Amazon EC2 tag key. Values must be in one of the two following formats: ``$(instance-id)`` or ``$(timestamp)`` . Variable tags are only valid for EBS Snapshot Management – Instance policies.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-schedule.html#cfn-dlm-lifecyclepolicy-schedule-variabletags
            '''
            result = self._values.get("variable_tags")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_ceddda9d.CfnTag]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScheduleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dlm.mixins.CfnLifecyclePolicyPropsMixin.ScriptProperty",
        jsii_struct_bases=[],
        name_mapping={
            "execute_operation_on_script_failure": "executeOperationOnScriptFailure",
            "execution_handler": "executionHandler",
            "execution_handler_service": "executionHandlerService",
            "execution_timeout": "executionTimeout",
            "maximum_retry_count": "maximumRetryCount",
            "stages": "stages",
        },
    )
    class ScriptProperty:
        def __init__(
            self,
            *,
            execute_operation_on_script_failure: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            execution_handler: typing.Optional[builtins.str] = None,
            execution_handler_service: typing.Optional[builtins.str] = None,
            execution_timeout: typing.Optional[jsii.Number] = None,
            maximum_retry_count: typing.Optional[jsii.Number] = None,
            stages: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''*[Custom snapshot policies that target instances only]* Information about pre and/or post scripts for a snapshot lifecycle policy that targets instances.

            For more information, see `Automating application-consistent snapshots with pre and post scripts <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/automate-app-consistent-backups.html>`_ .

            :param execute_operation_on_script_failure: Indicates whether Amazon Data Lifecycle Manager should default to crash-consistent snapshots if the pre script fails. - To default to crash consistent snapshot if the pre script fails, specify ``true`` . - To skip the instance for snapshot creation if the pre script fails, specify ``false`` . This parameter is supported only if you run a pre script. If you run a post script only, omit this parameter. Default: true
            :param execution_handler: The SSM document that includes the pre and/or post scripts to run. - If you are automating VSS backups, specify ``AWS_VSS_BACKUP`` . In this case, Amazon Data Lifecycle Manager automatically uses the ``AWSEC2-CreateVssSnapshot`` SSM document. - If you are automating application-consistent snapshots for SAP HANA workloads, specify ``AWSSystemsManagerSAP-CreateDLMSnapshotForSAPHANA`` . - If you are using a custom SSM document that you own, specify either the name or ARN of the SSM document. If you are using a custom SSM document that is shared with you, specify the ARN of the SSM document.
            :param execution_handler_service: Indicates the service used to execute the pre and/or post scripts. - If you are using custom SSM documents or automating application-consistent snapshots of SAP HANA workloads, specify ``AWS_SYSTEMS_MANAGER`` . - If you are automating VSS Backups, omit this parameter. Default: AWS_SYSTEMS_MANAGER
            :param execution_timeout: Specifies a timeout period, in seconds, after which Amazon Data Lifecycle Manager fails the script run attempt if it has not completed. If a script does not complete within its timeout period, Amazon Data Lifecycle Manager fails the attempt. The timeout period applies to the pre and post scripts individually. If you are automating VSS Backups, omit this parameter. Default: 10
            :param maximum_retry_count: Specifies the number of times Amazon Data Lifecycle Manager should retry scripts that fail. - If the pre script fails, Amazon Data Lifecycle Manager retries the entire snapshot creation process, including running the pre and post scripts. - If the post script fails, Amazon Data Lifecycle Manager retries the post script only; in this case, the pre script will have completed and the snapshot might have been created. If you do not want Amazon Data Lifecycle Manager to retry failed scripts, specify ``0`` . Default: 0
            :param stages: Indicate which scripts Amazon Data Lifecycle Manager should run on target instances. Pre scripts run before Amazon Data Lifecycle Manager initiates snapshot creation. Post scripts run after Amazon Data Lifecycle Manager initiates snapshot creation. - To run a pre script only, specify ``PRE`` . In this case, Amazon Data Lifecycle Manager calls the SSM document with the ``pre-script`` parameter before initiating snapshot creation. - To run a post script only, specify ``POST`` . In this case, Amazon Data Lifecycle Manager calls the SSM document with the ``post-script`` parameter after initiating snapshot creation. - To run both pre and post scripts, specify both ``PRE`` and ``POST`` . In this case, Amazon Data Lifecycle Manager calls the SSM document with the ``pre-script`` parameter before initiating snapshot creation, and then it calls the SSM document again with the ``post-script`` parameter after initiating snapshot creation. If you are automating VSS Backups, omit this parameter. Default: PRE and POST

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-script.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dlm import mixins as dlm_mixins
                
                script_property = dlm_mixins.CfnLifecyclePolicyPropsMixin.ScriptProperty(
                    execute_operation_on_script_failure=False,
                    execution_handler="executionHandler",
                    execution_handler_service="executionHandlerService",
                    execution_timeout=123,
                    maximum_retry_count=123,
                    stages=["stages"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9d444986b2928e39bdb3214c9d53fb8d5ca479e7cedd8c2077aac6c23c596003)
                check_type(argname="argument execute_operation_on_script_failure", value=execute_operation_on_script_failure, expected_type=type_hints["execute_operation_on_script_failure"])
                check_type(argname="argument execution_handler", value=execution_handler, expected_type=type_hints["execution_handler"])
                check_type(argname="argument execution_handler_service", value=execution_handler_service, expected_type=type_hints["execution_handler_service"])
                check_type(argname="argument execution_timeout", value=execution_timeout, expected_type=type_hints["execution_timeout"])
                check_type(argname="argument maximum_retry_count", value=maximum_retry_count, expected_type=type_hints["maximum_retry_count"])
                check_type(argname="argument stages", value=stages, expected_type=type_hints["stages"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if execute_operation_on_script_failure is not None:
                self._values["execute_operation_on_script_failure"] = execute_operation_on_script_failure
            if execution_handler is not None:
                self._values["execution_handler"] = execution_handler
            if execution_handler_service is not None:
                self._values["execution_handler_service"] = execution_handler_service
            if execution_timeout is not None:
                self._values["execution_timeout"] = execution_timeout
            if maximum_retry_count is not None:
                self._values["maximum_retry_count"] = maximum_retry_count
            if stages is not None:
                self._values["stages"] = stages

        @builtins.property
        def execute_operation_on_script_failure(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether Amazon Data Lifecycle Manager should default to crash-consistent snapshots if the pre script fails.

            - To default to crash consistent snapshot if the pre script fails, specify ``true`` .
            - To skip the instance for snapshot creation if the pre script fails, specify ``false`` .

            This parameter is supported only if you run a pre script. If you run a post script only, omit this parameter.

            Default: true

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-script.html#cfn-dlm-lifecyclepolicy-script-executeoperationonscriptfailure
            '''
            result = self._values.get("execute_operation_on_script_failure")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def execution_handler(self) -> typing.Optional[builtins.str]:
            '''The SSM document that includes the pre and/or post scripts to run.

            - If you are automating VSS backups, specify ``AWS_VSS_BACKUP`` . In this case, Amazon Data Lifecycle Manager automatically uses the ``AWSEC2-CreateVssSnapshot`` SSM document.
            - If you are automating application-consistent snapshots for SAP HANA workloads, specify ``AWSSystemsManagerSAP-CreateDLMSnapshotForSAPHANA`` .
            - If you are using a custom SSM document that you own, specify either the name or ARN of the SSM document. If you are using a custom SSM document that is shared with you, specify the ARN of the SSM document.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-script.html#cfn-dlm-lifecyclepolicy-script-executionhandler
            '''
            result = self._values.get("execution_handler")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def execution_handler_service(self) -> typing.Optional[builtins.str]:
            '''Indicates the service used to execute the pre and/or post scripts.

            - If you are using custom SSM documents or automating application-consistent snapshots of SAP HANA workloads, specify ``AWS_SYSTEMS_MANAGER`` .
            - If you are automating VSS Backups, omit this parameter.

            Default: AWS_SYSTEMS_MANAGER

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-script.html#cfn-dlm-lifecyclepolicy-script-executionhandlerservice
            '''
            result = self._values.get("execution_handler_service")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def execution_timeout(self) -> typing.Optional[jsii.Number]:
            '''Specifies a timeout period, in seconds, after which Amazon Data Lifecycle Manager fails the script run attempt if it has not completed.

            If a script does not complete within its timeout period, Amazon Data Lifecycle Manager fails the attempt. The timeout period applies to the pre and post scripts individually.

            If you are automating VSS Backups, omit this parameter.

            Default: 10

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-script.html#cfn-dlm-lifecyclepolicy-script-executiontimeout
            '''
            result = self._values.get("execution_timeout")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def maximum_retry_count(self) -> typing.Optional[jsii.Number]:
            '''Specifies the number of times Amazon Data Lifecycle Manager should retry scripts that fail.

            - If the pre script fails, Amazon Data Lifecycle Manager retries the entire snapshot creation process, including running the pre and post scripts.
            - If the post script fails, Amazon Data Lifecycle Manager retries the post script only; in this case, the pre script will have completed and the snapshot might have been created.

            If you do not want Amazon Data Lifecycle Manager to retry failed scripts, specify ``0`` .

            Default: 0

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-script.html#cfn-dlm-lifecyclepolicy-script-maximumretrycount
            '''
            result = self._values.get("maximum_retry_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def stages(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Indicate which scripts Amazon Data Lifecycle Manager should run on target instances.

            Pre scripts run before Amazon Data Lifecycle Manager initiates snapshot creation. Post scripts run after Amazon Data Lifecycle Manager initiates snapshot creation.

            - To run a pre script only, specify ``PRE`` . In this case, Amazon Data Lifecycle Manager calls the SSM document with the ``pre-script`` parameter before initiating snapshot creation.
            - To run a post script only, specify ``POST`` . In this case, Amazon Data Lifecycle Manager calls the SSM document with the ``post-script`` parameter after initiating snapshot creation.
            - To run both pre and post scripts, specify both ``PRE`` and ``POST`` . In this case, Amazon Data Lifecycle Manager calls the SSM document with the ``pre-script`` parameter before initiating snapshot creation, and then it calls the SSM document again with the ``post-script`` parameter after initiating snapshot creation.

            If you are automating VSS Backups, omit this parameter.

            Default: PRE and POST

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-script.html#cfn-dlm-lifecyclepolicy-script-stages
            '''
            result = self._values.get("stages")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScriptProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dlm.mixins.CfnLifecyclePolicyPropsMixin.ShareRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "target_accounts": "targetAccounts",
            "unshare_interval": "unshareInterval",
            "unshare_interval_unit": "unshareIntervalUnit",
        },
    )
    class ShareRuleProperty:
        def __init__(
            self,
            *,
            target_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
            unshare_interval: typing.Optional[jsii.Number] = None,
            unshare_interval_unit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''*[Custom snapshot policies only]* Specifies a rule for sharing snapshots across AWS accounts .

            :param target_accounts: The IDs of the AWS accounts with which to share the snapshots.
            :param unshare_interval: The period after which snapshots that are shared with other AWS accounts are automatically unshared.
            :param unshare_interval_unit: The unit of time for the automatic unsharing interval.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-sharerule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dlm import mixins as dlm_mixins
                
                share_rule_property = dlm_mixins.CfnLifecyclePolicyPropsMixin.ShareRuleProperty(
                    target_accounts=["targetAccounts"],
                    unshare_interval=123,
                    unshare_interval_unit="unshareIntervalUnit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a1139bcb2d4461a8f5c096ec8b2d8ecbc4af760e5af00075bf333b7722814dd1)
                check_type(argname="argument target_accounts", value=target_accounts, expected_type=type_hints["target_accounts"])
                check_type(argname="argument unshare_interval", value=unshare_interval, expected_type=type_hints["unshare_interval"])
                check_type(argname="argument unshare_interval_unit", value=unshare_interval_unit, expected_type=type_hints["unshare_interval_unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if target_accounts is not None:
                self._values["target_accounts"] = target_accounts
            if unshare_interval is not None:
                self._values["unshare_interval"] = unshare_interval
            if unshare_interval_unit is not None:
                self._values["unshare_interval_unit"] = unshare_interval_unit

        @builtins.property
        def target_accounts(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The IDs of the AWS accounts with which to share the snapshots.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-sharerule.html#cfn-dlm-lifecyclepolicy-sharerule-targetaccounts
            '''
            result = self._values.get("target_accounts")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def unshare_interval(self) -> typing.Optional[jsii.Number]:
            '''The period after which snapshots that are shared with other AWS accounts are automatically unshared.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-sharerule.html#cfn-dlm-lifecyclepolicy-sharerule-unshareinterval
            '''
            result = self._values.get("unshare_interval")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def unshare_interval_unit(self) -> typing.Optional[builtins.str]:
            '''The unit of time for the automatic unsharing interval.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-sharerule.html#cfn-dlm-lifecyclepolicy-sharerule-unshareintervalunit
            '''
            result = self._values.get("unshare_interval_unit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ShareRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnLifecyclePolicyMixinProps",
    "CfnLifecyclePolicyPropsMixin",
]

publication.publish()

def _typecheckingstub__594a4f5b67bd7681312e80236a3f67277618dd68ffe3e49f22c366f9cd7504b4(
    *,
    copy_tags: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    create_interval: typing.Optional[jsii.Number] = None,
    cross_region_copy_targets: typing.Any = None,
    default_policy: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    exclusions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLifecyclePolicyPropsMixin.ExclusionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    execution_role_arn: typing.Optional[builtins.str] = None,
    extend_deletion: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    policy_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLifecyclePolicyPropsMixin.PolicyDetailsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    retain_interval: typing.Optional[jsii.Number] = None,
    state: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec0016e3e7dcb7c70221b6736bc2a43d40f941b4b114fda40eb7c5700e523286(
    props: typing.Union[CfnLifecyclePolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f447347aacf21e85636e7f62ece6ea23343db5dfcc8b73969a9f89910bbb4775(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6629158138525fe696cc6fefa8f62e6c2e3e4fdf9d15d91e3d534c0f12ae2259(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84f6bf4e688675063644f0b741606b39354d36d28f91d6ae18d5cd7f671aeb72(
    *,
    cross_region_copy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLifecyclePolicyPropsMixin.CrossRegionCopyActionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__967e320d9798eb6435113099ad7b5d3d91d5ad5fbd011852000f16f640afe5ad(
    *,
    retention_archive_tier: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLifecyclePolicyPropsMixin.RetentionArchiveTierProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99c38907e01e31af5e3401a57efcf6f07b3cff8305ae3ec571fe3e5e063c3a97(
    *,
    retain_rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLifecyclePolicyPropsMixin.ArchiveRetainRuleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__312df5c95a3a2cf55cc15001b899995040b705c8659cece9de1b7ebc2c91e9f2(
    *,
    cron_expression: typing.Optional[builtins.str] = None,
    interval: typing.Optional[jsii.Number] = None,
    interval_unit: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    scripts: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLifecyclePolicyPropsMixin.ScriptProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    times: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58967213fd0902ebd1bef8b86f4ffc0c26ac3451ee9bf72c3ca944bcb2122ead(
    *,
    encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLifecyclePolicyPropsMixin.EncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    retain_rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLifecyclePolicyPropsMixin.CrossRegionCopyRetainRuleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    target: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aafe9afdeaba0bd22bb4867788da095803b4c25781ed8e8e3b550ddd1dc469e7(
    *,
    interval: typing.Optional[jsii.Number] = None,
    interval_unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d145963db3cba4654e05f7e140ecffffa6b7105cd93332de94844116901ac9f4(
    *,
    interval: typing.Optional[jsii.Number] = None,
    interval_unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcaef2c51d663343e01848195a4e3b3297842098ea2e7b24fed51876b4c9095d(
    *,
    cmk_arn: typing.Optional[builtins.str] = None,
    copy_tags: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    deprecate_rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLifecyclePolicyPropsMixin.CrossRegionCopyDeprecateRuleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    encrypted: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    retain_rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLifecyclePolicyPropsMixin.CrossRegionCopyRetainRuleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    target: typing.Optional[builtins.str] = None,
    target_region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a61c37ccc633279754f9da8bb9f5f73dd8832c557e01d216af18f742dcb2be2(
    *,
    count: typing.Optional[jsii.Number] = None,
    interval: typing.Optional[jsii.Number] = None,
    interval_unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e652eb6e0bcd5578b45adb8be0cf6f4639d458162b05a218b5af7570c60cf516(
    *,
    cmk_arn: typing.Optional[builtins.str] = None,
    encrypted: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d63c18260b31de3e747e98da88240c928e40d28d25bfc8cd046cb7911ceb8a1(
    *,
    description_regex: typing.Optional[builtins.str] = None,
    event_type: typing.Optional[builtins.str] = None,
    snapshot_owner: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4efda3053919600c975d42ef09e1abd2774e6c0949e64c4fa9ada495d2eb31df(
    *,
    parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLifecyclePolicyPropsMixin.EventParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c89f42aa9fe37a9fd6514ab0f060a9438f247d2f649aa6e880e142d2cd53e76a(
    *,
    exclude_boot_volumes: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    exclude_tags: typing.Any = None,
    exclude_volume_types: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fe3649473a118edccb0f56529256d9542d066c3f62933624cb674543ce2c5f7(
    *,
    availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    count: typing.Optional[jsii.Number] = None,
    interval: typing.Optional[jsii.Number] = None,
    interval_unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bf5f0e7af4ad072eb7ae59579339631435dd74c77fb1fd6f883556eb7a17c6b(
    *,
    exclude_boot_volume: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    exclude_data_volume_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    no_reboot: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0b8c7895a6a2975016dc51e33470da8019a7a6fe9e3b2481e9438b94cd66d87(
    *,
    actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLifecyclePolicyPropsMixin.ActionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    copy_tags: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    create_interval: typing.Optional[jsii.Number] = None,
    cross_region_copy_targets: typing.Any = None,
    event_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLifecyclePolicyPropsMixin.EventSourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    exclusions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLifecyclePolicyPropsMixin.ExclusionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    extend_deletion: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLifecyclePolicyPropsMixin.ParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    policy_language: typing.Optional[builtins.str] = None,
    policy_type: typing.Optional[builtins.str] = None,
    resource_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_type: typing.Optional[builtins.str] = None,
    resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    retain_interval: typing.Optional[jsii.Number] = None,
    schedules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLifecyclePolicyPropsMixin.ScheduleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    target_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6de2548ede68b0c29edfd57122818f6ffb3823ae99e9f68633f0c72393c36899(
    *,
    count: typing.Optional[jsii.Number] = None,
    interval: typing.Optional[jsii.Number] = None,
    interval_unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__154b3b018af24cfd0fb8770ce5b1a8f6f248bbb70fa9d51f19b0a3c37b402bc3(
    *,
    count: typing.Optional[jsii.Number] = None,
    interval: typing.Optional[jsii.Number] = None,
    interval_unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebd8d2d5e6cbd125eedc0e9aa0b478e90b879c4c1b29d090daa88a73aba7c18e(
    *,
    archive_rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLifecyclePolicyPropsMixin.ArchiveRuleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    copy_tags: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    create_rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLifecyclePolicyPropsMixin.CreateRuleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cross_region_copy_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLifecyclePolicyPropsMixin.CrossRegionCopyRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    deprecate_rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLifecyclePolicyPropsMixin.DeprecateRuleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    fast_restore_rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLifecyclePolicyPropsMixin.FastRestoreRuleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    retain_rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLifecyclePolicyPropsMixin.RetainRuleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    share_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLifecyclePolicyPropsMixin.ShareRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags_to_add: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    variable_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d444986b2928e39bdb3214c9d53fb8d5ca479e7cedd8c2077aac6c23c596003(
    *,
    execute_operation_on_script_failure: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    execution_handler: typing.Optional[builtins.str] = None,
    execution_handler_service: typing.Optional[builtins.str] = None,
    execution_timeout: typing.Optional[jsii.Number] = None,
    maximum_retry_count: typing.Optional[jsii.Number] = None,
    stages: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1139bcb2d4461a8f5c096ec8b2d8ecbc4af760e5af00075bf333b7722814dd1(
    *,
    target_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
    unshare_interval: typing.Optional[jsii.Number] = None,
    unshare_interval_unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
