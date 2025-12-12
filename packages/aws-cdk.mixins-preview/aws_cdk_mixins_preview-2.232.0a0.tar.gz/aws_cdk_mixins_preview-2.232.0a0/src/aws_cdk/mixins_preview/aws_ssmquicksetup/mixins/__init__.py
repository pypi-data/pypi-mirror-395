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
    jsii_type="@aws-cdk/mixins-preview.aws_ssmquicksetup.mixins.CfnConfigurationManagerMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "configuration_definitions": "configurationDefinitions",
        "description": "description",
        "name": "name",
        "tags": "tags",
    },
)
class CfnConfigurationManagerMixinProps:
    def __init__(
        self,
        *,
        configuration_definitions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigurationManagerPropsMixin.ConfigurationDefinitionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnConfigurationManagerPropsMixin.

        :param configuration_definitions: The definition of the Quick Setup configuration that the configuration manager deploys.
        :param description: The description of the configuration.
        :param name: The name of the configuration.
        :param tags: Key-value pairs of metadata to assign to the configuration manager.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmquicksetup-configurationmanager.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ssmquicksetup import mixins as ssmquicksetup_mixins
            
            cfn_configuration_manager_mixin_props = ssmquicksetup_mixins.CfnConfigurationManagerMixinProps(
                configuration_definitions=[ssmquicksetup_mixins.CfnConfigurationManagerPropsMixin.ConfigurationDefinitionProperty(
                    id="id",
                    local_deployment_administration_role_arn="localDeploymentAdministrationRoleArn",
                    local_deployment_execution_role_name="localDeploymentExecutionRoleName",
                    parameters={
                        "parameters_key": "parameters"
                    },
                    type="type",
                    type_version="typeVersion"
                )],
                description="description",
                name="name",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__610519f526f32e68da04716740177ea47206ed3e14f6dfb63041af44d99b2cdb)
            check_type(argname="argument configuration_definitions", value=configuration_definitions, expected_type=type_hints["configuration_definitions"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if configuration_definitions is not None:
            self._values["configuration_definitions"] = configuration_definitions
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def configuration_definitions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationManagerPropsMixin.ConfigurationDefinitionProperty"]]]]:
        '''The definition of the Quick Setup configuration that the configuration manager deploys.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmquicksetup-configurationmanager.html#cfn-ssmquicksetup-configurationmanager-configurationdefinitions
        '''
        result = self._values.get("configuration_definitions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationManagerPropsMixin.ConfigurationDefinitionProperty"]]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmquicksetup-configurationmanager.html#cfn-ssmquicksetup-configurationmanager-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmquicksetup-configurationmanager.html#cfn-ssmquicksetup-configurationmanager-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Key-value pairs of metadata to assign to the configuration manager.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmquicksetup-configurationmanager.html#cfn-ssmquicksetup-configurationmanager-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConfigurationManagerMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnConfigurationManagerPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ssmquicksetup.mixins.CfnConfigurationManagerPropsMixin",
):
    '''Creates a Quick Setup configuration manager resource.

    This object is a collection of desired state configurations for multiple configuration definitions and summaries describing the deployments of those definitions.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmquicksetup-configurationmanager.html
    :cloudformationResource: AWS::SSMQuickSetup::ConfigurationManager
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ssmquicksetup import mixins as ssmquicksetup_mixins
        
        cfn_configuration_manager_props_mixin = ssmquicksetup_mixins.CfnConfigurationManagerPropsMixin(ssmquicksetup_mixins.CfnConfigurationManagerMixinProps(
            configuration_definitions=[ssmquicksetup_mixins.CfnConfigurationManagerPropsMixin.ConfigurationDefinitionProperty(
                id="id",
                local_deployment_administration_role_arn="localDeploymentAdministrationRoleArn",
                local_deployment_execution_role_name="localDeploymentExecutionRoleName",
                parameters={
                    "parameters_key": "parameters"
                },
                type="type",
                type_version="typeVersion"
            )],
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
        props: typing.Union[CfnConfigurationManagerMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SSMQuickSetup::ConfigurationManager``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ba44d332bb66ec9dd73acbe9346f885891b17741839cd5f3d804d11453d7fbb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__db581a82f24cc025f04bdc05347783b47ae75201ed1bb8c895ef01664d15f60e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee5db2e97cd8b3623a65e5c5ebdecb6086fa1e113328c140fab7c601113d4edf)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnConfigurationManagerMixinProps:
        return typing.cast(CfnConfigurationManagerMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssmquicksetup.mixins.CfnConfigurationManagerPropsMixin.ConfigurationDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "id": "id",
            "local_deployment_administration_role_arn": "localDeploymentAdministrationRoleArn",
            "local_deployment_execution_role_name": "localDeploymentExecutionRoleName",
            "parameters": "parameters",
            "type": "type",
            "type_version": "typeVersion",
        },
    )
    class ConfigurationDefinitionProperty:
        def __init__(
            self,
            *,
            id: typing.Optional[builtins.str] = None,
            local_deployment_administration_role_arn: typing.Optional[builtins.str] = None,
            local_deployment_execution_role_name: typing.Optional[builtins.str] = None,
            parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            type: typing.Optional[builtins.str] = None,
            type_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The definition of a Quick Setup configuration.

            :param id: The ID of the configuration definition.
            :param local_deployment_administration_role_arn: The ARN of the IAM role used to administrate local configuration deployments. .. epigraph:: Although this element is listed as "Required: No", a value can be omitted only for organizational deployments of types other than ``AWSQuickSetupType-PatchPolicy`` . A value must be provided when you are running an organizational deployment for a patch policy or running any type of deployment for a single account.
            :param local_deployment_execution_role_name: The name of the IAM role used to deploy local configurations. .. epigraph:: Although this element is listed as "Required: No", a value can be omitted only for organizational deployments of types other than ``AWSQuickSetupType-PatchPolicy`` . A value must be provided when you are running an organizational deployment for a patch policy or running any type of deployment for a single account.
            :param parameters: The parameters for the configuration definition type. Parameters for configuration definitions vary based the configuration type. The following lists outline the parameters for each configuration type. - **AWS Config Recording (Type: AWS QuickSetupType-CFGRecording)** - - ``RecordAllResources`` - Description: (Optional) A boolean value that determines whether all supported resources are recorded. The default value is " ``true`` ". - ``ResourceTypesToRecord`` - Description: (Optional) A comma separated list of resource types you want to record. - ``RecordGlobalResourceTypes`` - Description: (Optional) A boolean value that determines whether global resources are recorded with all resource configurations. The default value is " ``false`` ". - ``GlobalResourceTypesRegion`` - Description: (Optional) Determines the AWS Region where global resources are recorded. - ``UseCustomBucket`` - Description: (Optional) A boolean value that determines whether a custom Amazon S3 bucket is used for delivery. The default value is " ``false`` ". - ``DeliveryBucketName`` - Description: (Optional) The name of the Amazon S3 bucket you want AWS Config to deliver configuration snapshots and configuration history files to. - ``DeliveryBucketPrefix`` - Description: (Optional) The key prefix you want to use in the custom Amazon S3 bucket. - ``NotificationOptions`` - Description: (Optional) Determines the notification configuration for the recorder. The valid values are ``NoStreaming`` , ``UseExistingTopic`` , and ``CreateTopic`` . The default value is ``NoStreaming`` . - ``CustomDeliveryTopicAccountId`` - Description: (Optional) The ID of the AWS account where the Amazon SNS topic you want to use for notifications resides. You must specify a value for this parameter if you use the ``UseExistingTopic`` notification option. - ``CustomDeliveryTopicName`` - Description: (Optional) The name of the Amazon SNS topic you want to use for notifications. You must specify a value for this parameter if you use the ``UseExistingTopic`` notification option. - ``RemediationSchedule`` - Description: (Optional) A rate expression that defines the schedule for drift remediation. The valid values are ``rate(30 days)`` , ``rate(7 days)`` , ``rate(1 days)`` , and ``none`` . The default value is " ``none`` ". - ``TargetAccounts`` - Description: (Optional) The ID of the AWS account initiating the configuration deployment. You only need to provide a value for this parameter if you want to deploy the configuration locally. A value must be provided for either ``TargetAccounts`` or ``TargetOrganizationalUnits`` . - ``TargetOrganizationalUnits`` - Description: (Optional) The ID of the root of your Organization. This configuration type doesn't currently support choosing specific OUs. The configuration will be deployed to all the OUs in the Organization. - ``TargetRegions`` - Description: (Required) A comma separated list of AWS Regions you want to deploy the configuration to. - **Change Manager (Type: AWS QuickSetupType-SSMChangeMgr)** - - ``DelegatedAccountId`` - Description: (Required) The ID of the delegated administrator account. - ``JobFunction`` - Description: (Required) The name for the Change Manager job function. - ``PermissionType`` - Description: (Optional) Specifies whether you want to use default administrator permissions for the job function role, or provide a custom IAM policy. The valid values are ``CustomPermissions`` and ``AdminPermissions`` . The default value for the parameter is ``CustomerPermissions`` . - ``CustomPermissions`` - Description: (Optional) A JSON string containing the IAM policy you want your job function to use. You must provide a value for this parameter if you specify ``CustomPermissions`` for the ``PermissionType`` parameter. - ``TargetOrganizationalUnits`` - Description: (Required) A comma separated list of organizational units (OUs) you want to deploy the configuration to. - ``TargetRegions`` - Description: (Required) A comma separated list of AWS Regions you want to deploy the configuration to. - **Conformance Packs (Type: AWS QuickSetupType-CFGCPacks)** - - ``DelegatedAccountId`` - Description: (Optional) The ID of the delegated administrator account. This parameter is required for Organization deployments. - ``RemediationSchedule`` - Description: (Optional) A rate expression that defines the schedule for drift remediation. The valid values are ``rate(30 days)`` , ``rate(14 days)`` , ``rate(2 days)`` , and ``none`` . The default value is " ``none`` ". - ``CPackNames`` - Description: (Required) A comma separated list of AWS Config conformance packs. - ``TargetAccounts`` - Description: (Optional) The ID of the AWS account initiating the configuration deployment. You only need to provide a value for this parameter if you want to deploy the configuration locally. A value must be provided for either ``TargetAccounts`` or ``TargetOrganizationalUnits`` . - ``TargetOrganizationalUnits`` - Description: (Optional) The ID of the root of your Organization. This configuration type doesn't currently support choosing specific OUs. The configuration will be deployed to all the OUs in the Organization. - ``TargetRegions`` - Description: (Required) A comma separated list of AWS Regions you want to deploy the configuration to. - **Default Host Management Configuration (Type: AWS QuickSetupType-DHMC)** - - ``UpdateSsmAgent`` - Description: (Optional) A boolean value that determines whether the SSM Agent is updated on the target instances every 2 weeks. The default value is " ``true`` ". - ``TargetOrganizationalUnits`` - Description: (Required) A comma separated list of organizational units (OUs) you want to deploy the configuration to. - ``TargetRegions`` - Description: (Required) A comma separated list of AWS Regions you want to deploy the configuration to. - **DevOps Guru (Type: AWS QuickSetupType-DevOpsGuru)** - - ``AnalyseAllResources`` - Description: (Optional) A boolean value that determines whether DevOps Guru analyzes all CloudFormation stacks in the account. The default value is " ``false`` ". - ``EnableSnsNotifications`` - Description: (Optional) A boolean value that determines whether DevOps Guru sends notifications when an insight is created. The default value is " ``true`` ". - ``EnableSsmOpsItems`` - Description: (Optional) A boolean value that determines whether DevOps Guru creates an OpsCenter OpsItem when an insight is created. The default value is " ``true`` ". - ``EnableDriftRemediation`` - Description: (Optional) A boolean value that determines whether a drift remediation schedule is used. The default value is " ``false`` ". - ``RemediationSchedule`` - Description: (Optional) A rate expression that defines the schedule for drift remediation. The valid values are ``rate(30 days)`` , ``rate(14 days)`` , ``rate(1 days)`` , and ``none`` . The default value is " ``none`` ". - ``TargetAccounts`` - Description: (Optional) The ID of the AWS account initiating the configuration deployment. You only need to provide a value for this parameter if you want to deploy the configuration locally. A value must be provided for either ``TargetAccounts`` or ``TargetOrganizationalUnits`` . - ``TargetOrganizationalUnits`` - Description: (Optional) A comma separated list of organizational units (OUs) you want to deploy the configuration to. - ``TargetRegions`` - Description: (Required) A comma separated list of AWS Regions you want to deploy the configuration to. - **Distributor (Type: AWS QuickSetupType-Distributor)** - - ``PackagesToInstall`` - Description: (Required) A comma separated list of packages you want to install on the target instances. The valid values are ``AWSEFSTools`` , ``AWSCWAgent`` , and ``AWSEC2LaunchAgent`` . - ``RemediationSchedule`` - Description: (Optional) A rate expression that defines the schedule for drift remediation. The valid values are ``rate(30 days)`` , ``rate(14 days)`` , ``rate(2 days)`` , and ``none`` . The default value is " ``rate(30 days)`` ". - ``IsPolicyAttachAllowed`` - Description: (Optional) A boolean value that determines whether Quick Setup attaches policies to instances profiles already associated with the target instances. The default value is " ``false`` ". - ``TargetType`` - Description: (Optional) Determines how instances are targeted for local account deployments. Don't specify a value for this parameter if you're deploying to OUs. The valid values are ``*`` , ``InstanceIds`` , ``ResourceGroups`` , and ``Tags`` . Use ``*`` to target all instances in the account. - ``TargetInstances`` - Description: (Optional) A comma separated list of instance IDs. You must provide a value for this parameter if you specify ``InstanceIds`` for the ``TargetType`` parameter. - ``TargetTagKey`` - Description: (Required) The tag key assigned to the instances you want to target. You must provide a value for this parameter if you specify ``Tags`` for the ``TargetType`` parameter. - ``TargetTagValue`` - Description: (Required) The value of the tag key assigned to the instances you want to target. You must provide a value for this parameter if you specify ``Tags`` for the ``TargetType`` parameter. - ``ResourceGroupName`` - Description: (Required) The name of the resource group associated with the instances you want to target. You must provide a value for this parameter if you specify ``ResourceGroups`` for the ``TargetType`` parameter. - ``TargetAccounts`` - Description: (Optional) The ID of the AWS account initiating the configuration deployment. You only need to provide a value for this parameter if you want to deploy the configuration locally. A value must be provided for either ``TargetAccounts`` or ``TargetOrganizationalUnits`` . - ``TargetOrganizationalUnits`` - Description: (Optional) A comma separated list of organizational units (OUs) you want to deploy the configuration to. - ``TargetRegions`` - Description: (Required) A comma separated list of AWS Regions you want to deploy the configuration to. - **Host Management (Type: AWS QuickSetupType-SSMHostMgmt)** - - ``UpdateSsmAgent`` - Description: (Optional) A boolean value that determines whether the SSM Agent is updated on the target instances every 2 weeks. The default value is " ``true`` ". - ``UpdateEc2LaunchAgent`` - Description: (Optional) A boolean value that determines whether the EC2 Launch agent is updated on the target instances every month. The default value is " ``false`` ". - ``CollectInventory`` - Description: (Optional) A boolean value that determines whether instance metadata is collected on the target instances every 30 minutes. The default value is " ``true`` ". - ``ScanInstances`` - Description: (Optional) A boolean value that determines whether the target instances are scanned daily for available patches. The default value is " ``true`` ". - ``InstallCloudWatchAgent`` - Description: (Optional) A boolean value that determines whether the Amazon CloudWatch agent is installed on the target instances. The default value is " ``false`` ". - ``UpdateCloudWatchAgent`` - Description: (Optional) A boolean value that determines whether the Amazon CloudWatch agent is updated on the target instances every month. The default value is " ``false`` ". - ``IsPolicyAttachAllowed`` - Description: (Optional) A boolean value that determines whether Quick Setup attaches policies to instances profiles already associated with the target instances. The default value is " ``false`` ". - ``TargetType`` - Description: (Optional) Determines how instances are targeted for local account deployments. Don't specify a value for this parameter if you're deploying to OUs. The valid values are ``*`` , ``InstanceIds`` , ``ResourceGroups`` , and ``Tags`` . Use ``*`` to target all instances in the account. - ``TargetInstances`` - Description: (Optional) A comma separated list of instance IDs. You must provide a value for this parameter if you specify ``InstanceIds`` for the ``TargetType`` parameter. - ``TargetTagKey`` - Description: (Optional) The tag key assigned to the instances you want to target. You must provide a value for this parameter if you specify ``Tags`` for the ``TargetType`` parameter. - ``TargetTagValue`` - Description: (Optional) The value of the tag key assigned to the instances you want to target. You must provide a value for this parameter if you specify ``Tags`` for the ``TargetType`` parameter. - ``ResourceGroupName`` - Description: (Optional) The name of the resource group associated with the instances you want to target. You must provide a value for this parameter if you specify ``ResourceGroups`` for the ``TargetType`` parameter. - ``TargetAccounts`` - Description: (Optional) The ID of the AWS account initiating the configuration deployment. You only need to provide a value for this parameter if you want to deploy the configuration locally. A value must be provided for either ``TargetAccounts`` or ``TargetOrganizationalUnits`` . - ``TargetOrganizationalUnits`` - Description: (Optional) A comma separated list of organizational units (OUs) you want to deploy the configuration to. - ``TargetRegions`` - Description: (Required) A comma separated list of AWS Regions you want to deploy the configuration to. - **OpsCenter (Type: AWS QuickSetupType-SSMOpsCenter)** - - ``DelegatedAccountId`` - Description: (Required) The ID of the delegated administrator account. - ``TargetOrganizationalUnits`` - Description: (Required) A comma separated list of organizational units (OUs) you want to deploy the configuration to. - ``TargetRegions`` - Description: (Required) A comma separated list of AWS Regions you want to deploy the configuration to. - **Patch Policy (Type: AWS QuickSetupType-PatchPolicy)** - - ``PatchPolicyName`` - Description: (Required) A name for the patch policy. The value you provide is applied to target Amazon EC2 instances as a tag. - ``SelectedPatchBaselines`` - Description: (Required) An array of JSON objects containing the information for the patch baselines to include in your patch policy. - ``PatchBaselineUseDefault`` - Description: (Optional) A value that determines whether the selected patch baselines are all AWS provided. Supported values are ``default`` and ``custom`` . - ``PatchBaselineRegion`` - Description: (Required) The AWS Region where the patch baseline exist. - ``ConfigurationOptionsPatchOperation`` - Description: (Optional) Determines whether target instances scan for available patches, or scan and install available patches. The valid values are ``Scan`` and ``ScanAndInstall`` . The default value for the parameter is ``Scan`` . - ``ConfigurationOptionsScanValue`` - Description: (Optional) A cron expression that is used as the schedule for when instances scan for available patches. - ``ConfigurationOptionsInstallValue`` - Description: (Optional) A cron expression that is used as the schedule for when instances install available patches. - ``ConfigurationOptionsScanNextInterval`` - Description: (Optional) A boolean value that determines whether instances should scan for available patches at the next cron interval. The default value is " ``false`` ". - ``ConfigurationOptionsInstallNextInterval`` - Description: (Optional) A boolean value that determines whether instances should scan for available patches at the next cron interval. The default value is " ``false`` ". - ``RebootOption`` - Description: (Optional) Determines whether instances are rebooted after patches are installed. Valid values are ``RebootIfNeeded`` and ``NoReboot`` . - ``IsPolicyAttachAllowed`` - Description: (Optional) A boolean value that determines whether Quick Setup attaches policies to instances profiles already associated with the target instances. The default value is " ``false`` ". - ``OutputLogEnableS3`` - Description: (Optional) A boolean value that determines whether command output logs are sent to Amazon S3. - ``OutputS3Location`` - Description: (Optional) Information about the Amazon S3 bucket where you want to store the output details of the request. - ``OutputBucketRegion`` - Description: (Optional) The AWS Region where the Amazon S3 bucket you want to deliver command output to is located. - ``OutputS3BucketName`` - Description: (Optional) The name of the Amazon S3 bucket you want to deliver command output to. - ``OutputS3KeyPrefix`` - Description: (Optional) The key prefix you want to use in the custom Amazon S3 bucket. - ``TargetType`` - Description: (Optional) Determines how instances are targeted for local account deployments. Don't specify a value for this parameter if you're deploying to OUs. The valid values are ``*`` , ``InstanceIds`` , ``ResourceGroups`` , and ``Tags`` . Use ``*`` to target all instances in the account. - ``TargetInstances`` - Description: (Optional) A comma separated list of instance IDs. You must provide a value for this parameter if you specify ``InstanceIds`` for the ``TargetType`` parameter. - ``TargetTagKey`` - Description: (Required) The tag key assigned to the instances you want to target. You must provide a value for this parameter if you specify ``Tags`` for the ``TargetType`` parameter. - ``TargetTagValue`` - Description: (Required) The value of the tag key assigned to the instances you want to target. You must provide a value for this parameter if you specify ``Tags`` for the ``TargetType`` parameter. - ``ResourceGroupName`` - Description: (Required) The name of the resource group associated with the instances you want to target. You must provide a value for this parameter if you specify ``ResourceGroups`` for the ``TargetType`` parameter. - ``TargetAccounts`` - Description: (Optional) The ID of the AWS account initiating the configuration deployment. You only need to provide a value for this parameter if you want to deploy the configuration locally. A value must be provided for either ``TargetAccounts`` or ``TargetOrganizationalUnits`` . - ``TargetOrganizationalUnits`` - Description: (Optional) A comma separated list of organizational units (OUs) you want to deploy the configuration to. - ``TargetRegions`` - Description: (Required) A comma separated list of AWS Regions you want to deploy the configuration to. - **Resource Explorer (Type: AWS QuickSetupType-ResourceExplorer)** - - ``SelectedAggregatorRegion`` - Description: (Required) The AWS Region where you want to create the aggregator index. - ``ReplaceExistingAggregator`` - Description: (Required) A boolean value that determines whether to demote an existing aggregator if it is in a Region that differs from the value you specify for the ``SelectedAggregatorRegion`` . - ``TargetOrganizationalUnits`` - Description: (Required) A comma separated list of organizational units (OUs) you want to deploy the configuration to. - ``TargetRegions`` - Description: (Required) A comma separated list of AWS Regions you want to deploy the configuration to. - **Resource Scheduler (Type: AWS QuickSetupType-Scheduler)** - - ``TargetTagKey`` - Description: (Required) The tag key assigned to the instances you want to target. - ``TargetTagValue`` - Description: (Required) The value of the tag key assigned to the instances you want to target. - ``ICalendarString`` - Description: (Required) An iCalendar formatted string containing the schedule you want Change Manager to use. - ``TargetAccounts`` - Description: (Optional) The ID of the AWS account initiating the configuration deployment. You only need to provide a value for this parameter if you want to deploy the configuration locally. A value must be provided for either ``TargetAccounts`` or ``TargetOrganizationalUnits`` . - ``TargetOrganizationalUnits`` - Description: (Optional) A comma separated list of organizational units (OUs) you want to deploy the configuration to. - ``TargetRegions`` - Description: (Required) A comma separated list of AWS Regions you want to deploy the configuration to.
            :param type: The type of the Quick Setup configuration.
            :param type_version: The version of the Quick Setup type used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmquicksetup-configurationmanager-configurationdefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssmquicksetup import mixins as ssmquicksetup_mixins
                
                configuration_definition_property = ssmquicksetup_mixins.CfnConfigurationManagerPropsMixin.ConfigurationDefinitionProperty(
                    id="id",
                    local_deployment_administration_role_arn="localDeploymentAdministrationRoleArn",
                    local_deployment_execution_role_name="localDeploymentExecutionRoleName",
                    parameters={
                        "parameters_key": "parameters"
                    },
                    type="type",
                    type_version="typeVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__539f96cbcceb0afadac5b932c6bdcf0d5fe99e46faae059387fca3910dc2a6f9)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument local_deployment_administration_role_arn", value=local_deployment_administration_role_arn, expected_type=type_hints["local_deployment_administration_role_arn"])
                check_type(argname="argument local_deployment_execution_role_name", value=local_deployment_execution_role_name, expected_type=type_hints["local_deployment_execution_role_name"])
                check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument type_version", value=type_version, expected_type=type_hints["type_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if id is not None:
                self._values["id"] = id
            if local_deployment_administration_role_arn is not None:
                self._values["local_deployment_administration_role_arn"] = local_deployment_administration_role_arn
            if local_deployment_execution_role_name is not None:
                self._values["local_deployment_execution_role_name"] = local_deployment_execution_role_name
            if parameters is not None:
                self._values["parameters"] = parameters
            if type is not None:
                self._values["type"] = type
            if type_version is not None:
                self._values["type_version"] = type_version

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''The ID of the configuration definition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmquicksetup-configurationmanager-configurationdefinition.html#cfn-ssmquicksetup-configurationmanager-configurationdefinition-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def local_deployment_administration_role_arn(
            self,
        ) -> typing.Optional[builtins.str]:
            '''The ARN of the IAM role used to administrate local configuration deployments.

            .. epigraph::

               Although this element is listed as "Required: No", a value can be omitted only for organizational deployments of types other than ``AWSQuickSetupType-PatchPolicy`` . A value must be provided when you are running an organizational deployment for a patch policy or running any type of deployment for a single account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmquicksetup-configurationmanager-configurationdefinition.html#cfn-ssmquicksetup-configurationmanager-configurationdefinition-localdeploymentadministrationrolearn
            '''
            result = self._values.get("local_deployment_administration_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def local_deployment_execution_role_name(self) -> typing.Optional[builtins.str]:
            '''The name of the IAM role used to deploy local configurations.

            .. epigraph::

               Although this element is listed as "Required: No", a value can be omitted only for organizational deployments of types other than ``AWSQuickSetupType-PatchPolicy`` . A value must be provided when you are running an organizational deployment for a patch policy or running any type of deployment for a single account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmquicksetup-configurationmanager-configurationdefinition.html#cfn-ssmquicksetup-configurationmanager-configurationdefinition-localdeploymentexecutionrolename
            '''
            result = self._values.get("local_deployment_execution_role_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def parameters(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''The parameters for the configuration definition type.

            Parameters for configuration definitions vary based the configuration type. The following lists outline the parameters for each configuration type.

            - **AWS Config Recording (Type: AWS QuickSetupType-CFGRecording)** - - ``RecordAllResources``
            - Description: (Optional) A boolean value that determines whether all supported resources are recorded. The default value is " ``true`` ".
            - ``ResourceTypesToRecord``
            - Description: (Optional) A comma separated list of resource types you want to record.
            - ``RecordGlobalResourceTypes``
            - Description: (Optional) A boolean value that determines whether global resources are recorded with all resource configurations. The default value is " ``false`` ".
            - ``GlobalResourceTypesRegion``
            - Description: (Optional) Determines the AWS Region where global resources are recorded.
            - ``UseCustomBucket``
            - Description: (Optional) A boolean value that determines whether a custom Amazon S3 bucket is used for delivery. The default value is " ``false`` ".
            - ``DeliveryBucketName``
            - Description: (Optional) The name of the Amazon S3 bucket you want AWS Config to deliver configuration snapshots and configuration history files to.
            - ``DeliveryBucketPrefix``
            - Description: (Optional) The key prefix you want to use in the custom Amazon S3 bucket.
            - ``NotificationOptions``
            - Description: (Optional) Determines the notification configuration for the recorder. The valid values are ``NoStreaming`` , ``UseExistingTopic`` , and ``CreateTopic`` . The default value is ``NoStreaming`` .
            - ``CustomDeliveryTopicAccountId``
            - Description: (Optional) The ID of the AWS account where the Amazon SNS topic you want to use for notifications resides. You must specify a value for this parameter if you use the ``UseExistingTopic`` notification option.
            - ``CustomDeliveryTopicName``
            - Description: (Optional) The name of the Amazon SNS topic you want to use for notifications. You must specify a value for this parameter if you use the ``UseExistingTopic`` notification option.
            - ``RemediationSchedule``
            - Description: (Optional) A rate expression that defines the schedule for drift remediation. The valid values are ``rate(30 days)`` , ``rate(7 days)`` , ``rate(1 days)`` , and ``none`` . The default value is " ``none`` ".
            - ``TargetAccounts``
            - Description: (Optional) The ID of the AWS account initiating the configuration deployment. You only need to provide a value for this parameter if you want to deploy the configuration locally. A value must be provided for either ``TargetAccounts`` or ``TargetOrganizationalUnits`` .
            - ``TargetOrganizationalUnits``
            - Description: (Optional) The ID of the root of your Organization. This configuration type doesn't currently support choosing specific OUs. The configuration will be deployed to all the OUs in the Organization.
            - ``TargetRegions``
            - Description: (Required) A comma separated list of AWS Regions you want to deploy the configuration to.
            - **Change Manager (Type: AWS QuickSetupType-SSMChangeMgr)** - - ``DelegatedAccountId``
            - Description: (Required) The ID of the delegated administrator account.
            - ``JobFunction``
            - Description: (Required) The name for the Change Manager job function.
            - ``PermissionType``
            - Description: (Optional) Specifies whether you want to use default administrator permissions for the job function role, or provide a custom IAM policy. The valid values are ``CustomPermissions`` and ``AdminPermissions`` . The default value for the parameter is ``CustomerPermissions`` .
            - ``CustomPermissions``
            - Description: (Optional) A JSON string containing the IAM policy you want your job function to use. You must provide a value for this parameter if you specify ``CustomPermissions`` for the ``PermissionType`` parameter.
            - ``TargetOrganizationalUnits``
            - Description: (Required) A comma separated list of organizational units (OUs) you want to deploy the configuration to.
            - ``TargetRegions``
            - Description: (Required) A comma separated list of AWS Regions you want to deploy the configuration to.
            - **Conformance Packs (Type: AWS QuickSetupType-CFGCPacks)** - - ``DelegatedAccountId``
            - Description: (Optional) The ID of the delegated administrator account. This parameter is required for Organization deployments.
            - ``RemediationSchedule``
            - Description: (Optional) A rate expression that defines the schedule for drift remediation. The valid values are ``rate(30 days)`` , ``rate(14 days)`` , ``rate(2 days)`` , and ``none`` . The default value is " ``none`` ".
            - ``CPackNames``
            - Description: (Required) A comma separated list of AWS Config conformance packs.
            - ``TargetAccounts``
            - Description: (Optional) The ID of the AWS account initiating the configuration deployment. You only need to provide a value for this parameter if you want to deploy the configuration locally. A value must be provided for either ``TargetAccounts`` or ``TargetOrganizationalUnits`` .
            - ``TargetOrganizationalUnits``
            - Description: (Optional) The ID of the root of your Organization. This configuration type doesn't currently support choosing specific OUs. The configuration will be deployed to all the OUs in the Organization.
            - ``TargetRegions``
            - Description: (Required) A comma separated list of AWS Regions you want to deploy the configuration to.
            - **Default Host Management Configuration (Type: AWS QuickSetupType-DHMC)** - - ``UpdateSsmAgent``
            - Description: (Optional) A boolean value that determines whether the SSM Agent is updated on the target instances every 2 weeks. The default value is " ``true`` ".
            - ``TargetOrganizationalUnits``
            - Description: (Required) A comma separated list of organizational units (OUs) you want to deploy the configuration to.
            - ``TargetRegions``
            - Description: (Required) A comma separated list of AWS Regions you want to deploy the configuration to.
            - **DevOps Guru (Type: AWS QuickSetupType-DevOpsGuru)** - - ``AnalyseAllResources``
            - Description: (Optional) A boolean value that determines whether DevOps Guru analyzes all CloudFormation stacks in the account. The default value is " ``false`` ".
            - ``EnableSnsNotifications``
            - Description: (Optional) A boolean value that determines whether DevOps Guru sends notifications when an insight is created. The default value is " ``true`` ".
            - ``EnableSsmOpsItems``
            - Description: (Optional) A boolean value that determines whether DevOps Guru creates an OpsCenter OpsItem when an insight is created. The default value is " ``true`` ".
            - ``EnableDriftRemediation``
            - Description: (Optional) A boolean value that determines whether a drift remediation schedule is used. The default value is " ``false`` ".
            - ``RemediationSchedule``
            - Description: (Optional) A rate expression that defines the schedule for drift remediation. The valid values are ``rate(30 days)`` , ``rate(14 days)`` , ``rate(1 days)`` , and ``none`` . The default value is " ``none`` ".
            - ``TargetAccounts``
            - Description: (Optional) The ID of the AWS account initiating the configuration deployment. You only need to provide a value for this parameter if you want to deploy the configuration locally. A value must be provided for either ``TargetAccounts`` or ``TargetOrganizationalUnits`` .
            - ``TargetOrganizationalUnits``
            - Description: (Optional) A comma separated list of organizational units (OUs) you want to deploy the configuration to.
            - ``TargetRegions``
            - Description: (Required) A comma separated list of AWS Regions you want to deploy the configuration to.
            - **Distributor (Type: AWS QuickSetupType-Distributor)** - - ``PackagesToInstall``
            - Description: (Required) A comma separated list of packages you want to install on the target instances. The valid values are ``AWSEFSTools`` , ``AWSCWAgent`` , and ``AWSEC2LaunchAgent`` .
            - ``RemediationSchedule``
            - Description: (Optional) A rate expression that defines the schedule for drift remediation. The valid values are ``rate(30 days)`` , ``rate(14 days)`` , ``rate(2 days)`` , and ``none`` . The default value is " ``rate(30 days)`` ".
            - ``IsPolicyAttachAllowed``
            - Description: (Optional) A boolean value that determines whether Quick Setup attaches policies to instances profiles already associated with the target instances. The default value is " ``false`` ".
            - ``TargetType``
            - Description: (Optional) Determines how instances are targeted for local account deployments. Don't specify a value for this parameter if you're deploying to OUs. The valid values are ``*`` , ``InstanceIds`` , ``ResourceGroups`` , and ``Tags`` . Use ``*`` to target all instances in the account.
            - ``TargetInstances``
            - Description: (Optional) A comma separated list of instance IDs. You must provide a value for this parameter if you specify ``InstanceIds`` for the ``TargetType`` parameter.
            - ``TargetTagKey``
            - Description: (Required) The tag key assigned to the instances you want to target. You must provide a value for this parameter if you specify ``Tags`` for the ``TargetType`` parameter.
            - ``TargetTagValue``
            - Description: (Required) The value of the tag key assigned to the instances you want to target. You must provide a value for this parameter if you specify ``Tags`` for the ``TargetType`` parameter.
            - ``ResourceGroupName``
            - Description: (Required) The name of the resource group associated with the instances you want to target. You must provide a value for this parameter if you specify ``ResourceGroups`` for the ``TargetType`` parameter.
            - ``TargetAccounts``
            - Description: (Optional) The ID of the AWS account initiating the configuration deployment. You only need to provide a value for this parameter if you want to deploy the configuration locally. A value must be provided for either ``TargetAccounts`` or ``TargetOrganizationalUnits`` .
            - ``TargetOrganizationalUnits``
            - Description: (Optional) A comma separated list of organizational units (OUs) you want to deploy the configuration to.
            - ``TargetRegions``
            - Description: (Required) A comma separated list of AWS Regions you want to deploy the configuration to.
            - **Host Management (Type: AWS QuickSetupType-SSMHostMgmt)** - - ``UpdateSsmAgent``
            - Description: (Optional) A boolean value that determines whether the SSM Agent is updated on the target instances every 2 weeks. The default value is " ``true`` ".
            - ``UpdateEc2LaunchAgent``
            - Description: (Optional) A boolean value that determines whether the EC2 Launch agent is updated on the target instances every month. The default value is " ``false`` ".
            - ``CollectInventory``
            - Description: (Optional) A boolean value that determines whether instance metadata is collected on the target instances every 30 minutes. The default value is " ``true`` ".
            - ``ScanInstances``
            - Description: (Optional) A boolean value that determines whether the target instances are scanned daily for available patches. The default value is " ``true`` ".
            - ``InstallCloudWatchAgent``
            - Description: (Optional) A boolean value that determines whether the Amazon CloudWatch agent is installed on the target instances. The default value is " ``false`` ".
            - ``UpdateCloudWatchAgent``
            - Description: (Optional) A boolean value that determines whether the Amazon CloudWatch agent is updated on the target instances every month. The default value is " ``false`` ".
            - ``IsPolicyAttachAllowed``
            - Description: (Optional) A boolean value that determines whether Quick Setup attaches policies to instances profiles already associated with the target instances. The default value is " ``false`` ".
            - ``TargetType``
            - Description: (Optional) Determines how instances are targeted for local account deployments. Don't specify a value for this parameter if you're deploying to OUs. The valid values are ``*`` , ``InstanceIds`` , ``ResourceGroups`` , and ``Tags`` . Use ``*`` to target all instances in the account.
            - ``TargetInstances``
            - Description: (Optional) A comma separated list of instance IDs. You must provide a value for this parameter if you specify ``InstanceIds`` for the ``TargetType`` parameter.
            - ``TargetTagKey``
            - Description: (Optional) The tag key assigned to the instances you want to target. You must provide a value for this parameter if you specify ``Tags`` for the ``TargetType`` parameter.
            - ``TargetTagValue``
            - Description: (Optional) The value of the tag key assigned to the instances you want to target. You must provide a value for this parameter if you specify ``Tags`` for the ``TargetType`` parameter.
            - ``ResourceGroupName``
            - Description: (Optional) The name of the resource group associated with the instances you want to target. You must provide a value for this parameter if you specify ``ResourceGroups`` for the ``TargetType`` parameter.
            - ``TargetAccounts``
            - Description: (Optional) The ID of the AWS account initiating the configuration deployment. You only need to provide a value for this parameter if you want to deploy the configuration locally. A value must be provided for either ``TargetAccounts`` or ``TargetOrganizationalUnits`` .
            - ``TargetOrganizationalUnits``
            - Description: (Optional) A comma separated list of organizational units (OUs) you want to deploy the configuration to.
            - ``TargetRegions``
            - Description: (Required) A comma separated list of AWS Regions you want to deploy the configuration to.
            - **OpsCenter (Type: AWS QuickSetupType-SSMOpsCenter)** - - ``DelegatedAccountId``
            - Description: (Required) The ID of the delegated administrator account.
            - ``TargetOrganizationalUnits``
            - Description: (Required) A comma separated list of organizational units (OUs) you want to deploy the configuration to.
            - ``TargetRegions``
            - Description: (Required) A comma separated list of AWS Regions you want to deploy the configuration to.
            - **Patch Policy (Type: AWS QuickSetupType-PatchPolicy)** - - ``PatchPolicyName``
            - Description: (Required) A name for the patch policy. The value you provide is applied to target Amazon EC2 instances as a tag.
            - ``SelectedPatchBaselines``
            - Description: (Required) An array of JSON objects containing the information for the patch baselines to include in your patch policy.
            - ``PatchBaselineUseDefault``
            - Description: (Optional) A value that determines whether the selected patch baselines are all AWS provided. Supported values are ``default`` and ``custom`` .
            - ``PatchBaselineRegion``
            - Description: (Required) The AWS Region where the patch baseline exist.
            - ``ConfigurationOptionsPatchOperation``
            - Description: (Optional) Determines whether target instances scan for available patches, or scan and install available patches. The valid values are ``Scan`` and ``ScanAndInstall`` . The default value for the parameter is ``Scan`` .
            - ``ConfigurationOptionsScanValue``
            - Description: (Optional) A cron expression that is used as the schedule for when instances scan for available patches.
            - ``ConfigurationOptionsInstallValue``
            - Description: (Optional) A cron expression that is used as the schedule for when instances install available patches.
            - ``ConfigurationOptionsScanNextInterval``
            - Description: (Optional) A boolean value that determines whether instances should scan for available patches at the next cron interval. The default value is " ``false`` ".
            - ``ConfigurationOptionsInstallNextInterval``
            - Description: (Optional) A boolean value that determines whether instances should scan for available patches at the next cron interval. The default value is " ``false`` ".
            - ``RebootOption``
            - Description: (Optional) Determines whether instances are rebooted after patches are installed. Valid values are ``RebootIfNeeded`` and ``NoReboot`` .
            - ``IsPolicyAttachAllowed``
            - Description: (Optional) A boolean value that determines whether Quick Setup attaches policies to instances profiles already associated with the target instances. The default value is " ``false`` ".
            - ``OutputLogEnableS3``
            - Description: (Optional) A boolean value that determines whether command output logs are sent to Amazon S3.
            - ``OutputS3Location``
            - Description: (Optional) Information about the Amazon S3 bucket where you want to store the output details of the request.
            - ``OutputBucketRegion``
            - Description: (Optional) The AWS Region where the Amazon S3 bucket you want to deliver command output to is located.
            - ``OutputS3BucketName``
            - Description: (Optional) The name of the Amazon S3 bucket you want to deliver command output to.
            - ``OutputS3KeyPrefix``
            - Description: (Optional) The key prefix you want to use in the custom Amazon S3 bucket.
            - ``TargetType``
            - Description: (Optional) Determines how instances are targeted for local account deployments. Don't specify a value for this parameter if you're deploying to OUs. The valid values are ``*`` , ``InstanceIds`` , ``ResourceGroups`` , and ``Tags`` . Use ``*`` to target all instances in the account.
            - ``TargetInstances``
            - Description: (Optional) A comma separated list of instance IDs. You must provide a value for this parameter if you specify ``InstanceIds`` for the ``TargetType`` parameter.
            - ``TargetTagKey``
            - Description: (Required) The tag key assigned to the instances you want to target. You must provide a value for this parameter if you specify ``Tags`` for the ``TargetType`` parameter.
            - ``TargetTagValue``
            - Description: (Required) The value of the tag key assigned to the instances you want to target. You must provide a value for this parameter if you specify ``Tags`` for the ``TargetType`` parameter.
            - ``ResourceGroupName``
            - Description: (Required) The name of the resource group associated with the instances you want to target. You must provide a value for this parameter if you specify ``ResourceGroups`` for the ``TargetType`` parameter.
            - ``TargetAccounts``
            - Description: (Optional) The ID of the AWS account initiating the configuration deployment. You only need to provide a value for this parameter if you want to deploy the configuration locally. A value must be provided for either ``TargetAccounts`` or ``TargetOrganizationalUnits`` .
            - ``TargetOrganizationalUnits``
            - Description: (Optional) A comma separated list of organizational units (OUs) you want to deploy the configuration to.
            - ``TargetRegions``
            - Description: (Required) A comma separated list of AWS Regions you want to deploy the configuration to.
            - **Resource Explorer (Type: AWS QuickSetupType-ResourceExplorer)** - - ``SelectedAggregatorRegion``
            - Description: (Required) The AWS Region where you want to create the aggregator index.
            - ``ReplaceExistingAggregator``
            - Description: (Required) A boolean value that determines whether to demote an existing aggregator if it is in a Region that differs from the value you specify for the ``SelectedAggregatorRegion`` .
            - ``TargetOrganizationalUnits``
            - Description: (Required) A comma separated list of organizational units (OUs) you want to deploy the configuration to.
            - ``TargetRegions``
            - Description: (Required) A comma separated list of AWS Regions you want to deploy the configuration to.
            - **Resource Scheduler (Type: AWS QuickSetupType-Scheduler)** - - ``TargetTagKey``
            - Description: (Required) The tag key assigned to the instances you want to target.
            - ``TargetTagValue``
            - Description: (Required) The value of the tag key assigned to the instances you want to target.
            - ``ICalendarString``
            - Description: (Required) An iCalendar formatted string containing the schedule you want Change Manager to use.
            - ``TargetAccounts``
            - Description: (Optional) The ID of the AWS account initiating the configuration deployment. You only need to provide a value for this parameter if you want to deploy the configuration locally. A value must be provided for either ``TargetAccounts`` or ``TargetOrganizationalUnits`` .
            - ``TargetOrganizationalUnits``
            - Description: (Optional) A comma separated list of organizational units (OUs) you want to deploy the configuration to.
            - ``TargetRegions``
            - Description: (Required) A comma separated list of AWS Regions you want to deploy the configuration to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmquicksetup-configurationmanager-configurationdefinition.html#cfn-ssmquicksetup-configurationmanager-configurationdefinition-parameters
            '''
            result = self._values.get("parameters")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of the Quick Setup configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmquicksetup-configurationmanager-configurationdefinition.html#cfn-ssmquicksetup-configurationmanager-configurationdefinition-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type_version(self) -> typing.Optional[builtins.str]:
            '''The version of the Quick Setup type used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmquicksetup-configurationmanager-configurationdefinition.html#cfn-ssmquicksetup-configurationmanager-configurationdefinition-typeversion
            '''
            result = self._values.get("type_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfigurationDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssmquicksetup.mixins.CfnConfigurationManagerPropsMixin.StatusSummaryProperty",
        jsii_struct_bases=[],
        name_mapping={
            "last_updated_at": "lastUpdatedAt",
            "status": "status",
            "status_details": "statusDetails",
            "status_message": "statusMessage",
            "status_type": "statusType",
        },
    )
    class StatusSummaryProperty:
        def __init__(
            self,
            *,
            last_updated_at: typing.Optional[builtins.str] = None,
            status: typing.Optional[builtins.str] = None,
            status_details: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            status_message: typing.Optional[builtins.str] = None,
            status_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A summarized description of the status.

            :param last_updated_at: The datetime stamp when the status was last updated.
            :param status: The current status.
            :param status_details: Details about the status.
            :param status_message: When applicable, returns an informational message relevant to the current status and status type of the status summary object. We don't recommend implementing parsing logic around this value since the messages returned can vary in format.
            :param status_type: The type of a status summary.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmquicksetup-configurationmanager-statussummary.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssmquicksetup import mixins as ssmquicksetup_mixins
                
                status_summary_property = ssmquicksetup_mixins.CfnConfigurationManagerPropsMixin.StatusSummaryProperty(
                    last_updated_at="lastUpdatedAt",
                    status="status",
                    status_details={
                        "status_details_key": "statusDetails"
                    },
                    status_message="statusMessage",
                    status_type="statusType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b498ba0212c623e3915e44f76c73acee97e71f4c771e6793e7a76fe2e1ad3bc4)
                check_type(argname="argument last_updated_at", value=last_updated_at, expected_type=type_hints["last_updated_at"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                check_type(argname="argument status_details", value=status_details, expected_type=type_hints["status_details"])
                check_type(argname="argument status_message", value=status_message, expected_type=type_hints["status_message"])
                check_type(argname="argument status_type", value=status_type, expected_type=type_hints["status_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if last_updated_at is not None:
                self._values["last_updated_at"] = last_updated_at
            if status is not None:
                self._values["status"] = status
            if status_details is not None:
                self._values["status_details"] = status_details
            if status_message is not None:
                self._values["status_message"] = status_message
            if status_type is not None:
                self._values["status_type"] = status_type

        @builtins.property
        def last_updated_at(self) -> typing.Optional[builtins.str]:
            '''The datetime stamp when the status was last updated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmquicksetup-configurationmanager-statussummary.html#cfn-ssmquicksetup-configurationmanager-statussummary-lastupdatedat
            '''
            result = self._values.get("last_updated_at")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''The current status.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmquicksetup-configurationmanager-statussummary.html#cfn-ssmquicksetup-configurationmanager-statussummary-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def status_details(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''Details about the status.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmquicksetup-configurationmanager-statussummary.html#cfn-ssmquicksetup-configurationmanager-statussummary-statusdetails
            '''
            result = self._values.get("status_details")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def status_message(self) -> typing.Optional[builtins.str]:
            '''When applicable, returns an informational message relevant to the current status and status type of the status summary object.

            We don't recommend implementing parsing logic around this value since the messages returned can vary in format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmquicksetup-configurationmanager-statussummary.html#cfn-ssmquicksetup-configurationmanager-statussummary-statusmessage
            '''
            result = self._values.get("status_message")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def status_type(self) -> typing.Optional[builtins.str]:
            '''The type of a status summary.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmquicksetup-configurationmanager-statussummary.html#cfn-ssmquicksetup-configurationmanager-statussummary-statustype
            '''
            result = self._values.get("status_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StatusSummaryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ssmquicksetup.mixins.CfnLifecycleAutomationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "automation_document": "automationDocument",
        "automation_parameters": "automationParameters",
        "resource_key": "resourceKey",
        "tags": "tags",
    },
)
class CfnLifecycleAutomationMixinProps:
    def __init__(
        self,
        *,
        automation_document: typing.Optional[builtins.str] = None,
        automation_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Sequence[builtins.str]]]] = None,
        resource_key: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnLifecycleAutomationPropsMixin.

        :param automation_document: The name of the SSM Automation document to execute in response to CloudFormation lifecycle events (CREATE, UPDATE, DELETE).
        :param automation_parameters: A map of key-value parameters passed to the Automation document during execution. Each parameter name maps to a list of values, even for single values. Parameters can include configuration-specific values for your automation workflow.
        :param resource_key: A unique identifier used for generating the SSM Association name. This ensures uniqueness when multiple lifecycle automation resources exist in the same stack.
        :param tags: Tags applied to the underlying SSM Association created by this resource. Tags help identify and organize automation executions.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmquicksetup-lifecycleautomation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ssmquicksetup import mixins as ssmquicksetup_mixins
            
            cfn_lifecycle_automation_mixin_props = ssmquicksetup_mixins.CfnLifecycleAutomationMixinProps(
                automation_document="automationDocument",
                automation_parameters={
                    "automation_parameters_key": ["automationParameters"]
                },
                resource_key="resourceKey",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17af6da6eda55935124b428465010ea2fb3530cadec6068ed0141ee1cef0a1ba)
            check_type(argname="argument automation_document", value=automation_document, expected_type=type_hints["automation_document"])
            check_type(argname="argument automation_parameters", value=automation_parameters, expected_type=type_hints["automation_parameters"])
            check_type(argname="argument resource_key", value=resource_key, expected_type=type_hints["resource_key"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if automation_document is not None:
            self._values["automation_document"] = automation_document
        if automation_parameters is not None:
            self._values["automation_parameters"] = automation_parameters
        if resource_key is not None:
            self._values["resource_key"] = resource_key
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def automation_document(self) -> typing.Optional[builtins.str]:
        '''The name of the SSM Automation document to execute in response to CloudFormation lifecycle events (CREATE, UPDATE, DELETE).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmquicksetup-lifecycleautomation.html#cfn-ssmquicksetup-lifecycleautomation-automationdocument
        '''
        result = self._values.get("automation_document")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def automation_parameters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.List[builtins.str]]]]:
        '''A map of key-value parameters passed to the Automation document during execution.

        Each parameter name maps to a list of values, even for single values. Parameters can include configuration-specific values for your automation workflow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmquicksetup-lifecycleautomation.html#cfn-ssmquicksetup-lifecycleautomation-automationparameters
        '''
        result = self._values.get("automation_parameters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.List[builtins.str]]]], result)

    @builtins.property
    def resource_key(self) -> typing.Optional[builtins.str]:
        '''A unique identifier used for generating the SSM Association name.

        This ensures uniqueness when multiple lifecycle automation resources exist in the same stack.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmquicksetup-lifecycleautomation.html#cfn-ssmquicksetup-lifecycleautomation-resourcekey
        '''
        result = self._values.get("resource_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Tags applied to the underlying SSM Association created by this resource.

        Tags help identify and organize automation executions.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmquicksetup-lifecycleautomation.html#cfn-ssmquicksetup-lifecycleautomation-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLifecycleAutomationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLifecycleAutomationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ssmquicksetup.mixins.CfnLifecycleAutomationPropsMixin",
):
    '''Creates a lifecycle automation resource that executes SSM Automation documents during CloudFormation stack operations.

    This resource replaces inline AWS Lambda custom resources and provides a managed way to handle lifecycle events in Quick Setup configurations.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmquicksetup-lifecycleautomation.html
    :cloudformationResource: AWS::SSMQuickSetup::LifecycleAutomation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ssmquicksetup import mixins as ssmquicksetup_mixins
        
        cfn_lifecycle_automation_props_mixin = ssmquicksetup_mixins.CfnLifecycleAutomationPropsMixin(ssmquicksetup_mixins.CfnLifecycleAutomationMixinProps(
            automation_document="automationDocument",
            automation_parameters={
                "automation_parameters_key": ["automationParameters"]
            },
            resource_key="resourceKey",
            tags={
                "tags_key": "tags"
            }
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnLifecycleAutomationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SSMQuickSetup::LifecycleAutomation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edfa8e457045a8f9b5e12a03dad9ca9642c1bbd53b0b35b8ec6fd18529f2fe62)
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
            type_hints = typing.get_type_hints(_typecheckingstub__43ed7899e6978cd6ee1d8d835cd98f412fe5f8e79cf64e48b2e074e1e87ca4ba)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2836aa2e73c9efafbd7fc9df84fa22c64495dc8beefe3db7220d36dea5a13d9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLifecycleAutomationMixinProps:
        return typing.cast(CfnLifecycleAutomationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnConfigurationManagerMixinProps",
    "CfnConfigurationManagerPropsMixin",
    "CfnLifecycleAutomationMixinProps",
    "CfnLifecycleAutomationPropsMixin",
]

publication.publish()

def _typecheckingstub__610519f526f32e68da04716740177ea47206ed3e14f6dfb63041af44d99b2cdb(
    *,
    configuration_definitions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigurationManagerPropsMixin.ConfigurationDefinitionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ba44d332bb66ec9dd73acbe9346f885891b17741839cd5f3d804d11453d7fbb(
    props: typing.Union[CfnConfigurationManagerMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db581a82f24cc025f04bdc05347783b47ae75201ed1bb8c895ef01664d15f60e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee5db2e97cd8b3623a65e5c5ebdecb6086fa1e113328c140fab7c601113d4edf(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__539f96cbcceb0afadac5b932c6bdcf0d5fe99e46faae059387fca3910dc2a6f9(
    *,
    id: typing.Optional[builtins.str] = None,
    local_deployment_administration_role_arn: typing.Optional[builtins.str] = None,
    local_deployment_execution_role_name: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    type: typing.Optional[builtins.str] = None,
    type_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b498ba0212c623e3915e44f76c73acee97e71f4c771e6793e7a76fe2e1ad3bc4(
    *,
    last_updated_at: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    status_details: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    status_message: typing.Optional[builtins.str] = None,
    status_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17af6da6eda55935124b428465010ea2fb3530cadec6068ed0141ee1cef0a1ba(
    *,
    automation_document: typing.Optional[builtins.str] = None,
    automation_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Sequence[builtins.str]]]] = None,
    resource_key: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edfa8e457045a8f9b5e12a03dad9ca9642c1bbd53b0b35b8ec6fd18529f2fe62(
    props: typing.Union[CfnLifecycleAutomationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43ed7899e6978cd6ee1d8d835cd98f412fe5f8e79cf64e48b2e074e1e87ca4ba(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2836aa2e73c9efafbd7fc9df84fa22c64495dc8beefe3db7220d36dea5a13d9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
