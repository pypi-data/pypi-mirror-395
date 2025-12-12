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
    jsii_type="@aws-cdk/mixins-preview.aws_fms.mixins.CfnNotificationChannelMixinProps",
    jsii_struct_bases=[],
    name_mapping={"sns_role_name": "snsRoleName", "sns_topic_arn": "snsTopicArn"},
)
class CfnNotificationChannelMixinProps:
    def __init__(
        self,
        *,
        sns_role_name: typing.Optional[builtins.str] = None,
        sns_topic_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnNotificationChannelPropsMixin.

        :param sns_role_name: The Amazon Resource Name (ARN) of the IAM role that allows Amazon to record AWS Firewall Manager activity.
        :param sns_topic_arn: The Amazon Resource Name (ARN) of the SNS topic that collects notifications from AWS Firewall Manager .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-notificationchannel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_fms import mixins as fms_mixins
            
            cfn_notification_channel_mixin_props = fms_mixins.CfnNotificationChannelMixinProps(
                sns_role_name="snsRoleName",
                sns_topic_arn="snsTopicArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8adc25437ea2a35fbd61994baf429d178b007c5da9eff3ce96c4f5f326517816)
            check_type(argname="argument sns_role_name", value=sns_role_name, expected_type=type_hints["sns_role_name"])
            check_type(argname="argument sns_topic_arn", value=sns_topic_arn, expected_type=type_hints["sns_topic_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if sns_role_name is not None:
            self._values["sns_role_name"] = sns_role_name
        if sns_topic_arn is not None:
            self._values["sns_topic_arn"] = sns_topic_arn

    @builtins.property
    def sns_role_name(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the IAM role that allows Amazon  to record AWS Firewall Manager activity.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-notificationchannel.html#cfn-fms-notificationchannel-snsrolename
        '''
        result = self._values.get("sns_role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sns_topic_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the SNS topic that collects notifications from AWS Firewall Manager .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-notificationchannel.html#cfn-fms-notificationchannel-snstopicarn
        '''
        result = self._values.get("sns_topic_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnNotificationChannelMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnNotificationChannelPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_fms.mixins.CfnNotificationChannelPropsMixin",
):
    '''Designates the IAM role and Amazon Simple Notification Service (SNS) topic to use to record SNS logs.

    To perform this action outside of the console, you must configure the SNS topic to allow the role ``AWSServiceRoleForFMS`` to publish SNS logs. For more information, see `Firewall Manager required permissions for API actions <https://docs.aws.amazon.com/waf/latest/developerguide/fms-api-permissions-ref.html>`_ in the *AWS Firewall Manager Developer Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-notificationchannel.html
    :cloudformationResource: AWS::FMS::NotificationChannel
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_fms import mixins as fms_mixins
        
        cfn_notification_channel_props_mixin = fms_mixins.CfnNotificationChannelPropsMixin(fms_mixins.CfnNotificationChannelMixinProps(
            sns_role_name="snsRoleName",
            sns_topic_arn="snsTopicArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnNotificationChannelMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::FMS::NotificationChannel``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2657260abfdfd973e047458724e7e52c9b15cf6f46657d656f79a5ddfc1b9271)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d174e5c0c2c5ab6845ce2f49ddad1fec5cd59d5460006ffad80a79951c63f11a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__373940a19e5444b0cdf7803ee7a486506926be0994ee58dba172062b075b9a96)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnNotificationChannelMixinProps:
        return typing.cast(CfnNotificationChannelMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_fms.mixins.CfnPolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "delete_all_policy_resources": "deleteAllPolicyResources",
        "exclude_map": "excludeMap",
        "exclude_resource_tags": "excludeResourceTags",
        "include_map": "includeMap",
        "policy_description": "policyDescription",
        "policy_name": "policyName",
        "remediation_enabled": "remediationEnabled",
        "resources_clean_up": "resourcesCleanUp",
        "resource_set_ids": "resourceSetIds",
        "resource_tag_logical_operator": "resourceTagLogicalOperator",
        "resource_tags": "resourceTags",
        "resource_type": "resourceType",
        "resource_type_list": "resourceTypeList",
        "security_service_policy_data": "securityServicePolicyData",
        "tags": "tags",
    },
)
class CfnPolicyMixinProps:
    def __init__(
        self,
        *,
        delete_all_policy_resources: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        exclude_map: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPolicyPropsMixin.IEMapProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        exclude_resource_tags: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        include_map: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPolicyPropsMixin.IEMapProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        policy_description: typing.Optional[builtins.str] = None,
        policy_name: typing.Optional[builtins.str] = None,
        remediation_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        resources_clean_up: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        resource_set_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        resource_tag_logical_operator: typing.Optional[builtins.str] = None,
        resource_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPolicyPropsMixin.ResourceTagProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        resource_type: typing.Optional[builtins.str] = None,
        resource_type_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        security_service_policy_data: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPolicyPropsMixin.SecurityServicePolicyDataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["CfnPolicyPropsMixin.PolicyTagProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnPolicyPropsMixin.

        :param delete_all_policy_resources: Used when deleting a policy. If ``true`` , Firewall Manager performs cleanup according to the policy type. For AWS WAF and Shield Advanced policies, Firewall Manager does the following: - Deletes rule groups created by Firewall Manager - Removes web ACLs from in-scope resources - Deletes web ACLs that contain no rules or rule groups For security group policies, Firewall Manager does the following for each security group in the policy: - Disassociates the security group from in-scope resources - Deletes the security group if it was created through Firewall Manager and if it's no longer associated with any resources through another policy After the cleanup, in-scope resources are no longer protected by web ACLs in this policy. Protection of out-of-scope resources remains unchanged. Scope is determined by tags that you create and accounts that you associate with the policy. When creating the policy, if you specify that only resources in specific accounts or with specific tags are in scope of the policy, those accounts and resources are handled by the policy. All others are out of scope. If you don't specify tags or accounts, all resources are in scope.
        :param exclude_map: Specifies the AWS account IDs and AWS Organizations organizational units (OUs) to exclude from the policy. Specifying an OU is the equivalent of specifying all accounts in the OU and in any of its child OUs, including any child OUs and accounts that are added at a later time. You can specify inclusions or exclusions, but not both. If you specify an ``IncludeMap`` , AWS Firewall Manager applies the policy to all accounts specified by the ``IncludeMap`` , and does not evaluate any ``ExcludeMap`` specifications. If you do not specify an ``IncludeMap`` , then Firewall Manager applies the policy to all accounts except for those specified by the ``ExcludeMap`` . You can specify account IDs, OUs, or a combination: - Specify account IDs by setting the key to ``ACCOUNT`` . For example, the following is a valid map: ``{“ACCOUNT” : [“accountID1”, “accountID2”]}`` . - Specify OUs by setting the key to ``ORGUNIT`` . For example, the following is a valid map: ``{“ORGUNIT” : [“ouid111”, “ouid112”]}`` . - Specify accounts and OUs together in a single map, separated with a comma. For example, the following is a valid map: ``{“ACCOUNT” : [“accountID1”, “accountID2”], “ORGUNIT” : [“ouid111”, “ouid112”]}`` .
        :param exclude_resource_tags: Used only when tags are specified in the ``ResourceTags`` property. If this property is ``True`` , resources with the specified tags are not in scope of the policy. If it's ``False`` , only resources with the specified tags are in scope of the policy.
        :param include_map: Specifies the AWS account IDs and AWS Organizations organizational units (OUs) to include in the policy. Specifying an OU is the equivalent of specifying all accounts in the OU and in any of its child OUs, including any child OUs and accounts that are added at a later time. You can specify inclusions or exclusions, but not both. If you specify an ``IncludeMap`` , AWS Firewall Manager applies the policy to all accounts specified by the ``IncludeMap`` , and does not evaluate any ``ExcludeMap`` specifications. If you do not specify an ``IncludeMap`` , then Firewall Manager applies the policy to all accounts except for those specified by the ``ExcludeMap`` . You can specify account IDs, OUs, or a combination: - Specify account IDs by setting the key to ``ACCOUNT`` . For example, the following is a valid map: ``{“ACCOUNT” : [“accountID1”, “accountID2”]}`` . - Specify OUs by setting the key to ``ORGUNIT`` . For example, the following is a valid map: ``{“ORGUNIT” : [“ouid111”, “ouid112”]}`` . - Specify accounts and OUs together in a single map, separated with a comma. For example, the following is a valid map: ``{“ACCOUNT” : [“accountID1”, “accountID2”], “ORGUNIT” : [“ouid111”, “ouid112”]}`` .
        :param policy_description: Your description of the AWS Firewall Manager policy.
        :param policy_name: The name of the AWS Firewall Manager policy.
        :param remediation_enabled: Indicates if the policy should be automatically applied to new resources.
        :param resources_clean_up: Indicates whether AWS Firewall Manager should automatically remove protections from resources that leave the policy scope and clean up resources that Firewall Manager is managing for accounts when those accounts leave policy scope. For example, Firewall Manager will disassociate a Firewall Manager managed web ACL from a protected customer resource when the customer resource leaves policy scope. By default, Firewall Manager doesn't remove protections or delete Firewall Manager managed resources. This option is not available for Shield Advanced or AWS WAF Classic policies.
        :param resource_set_ids: The unique identifiers of the resource sets used by the policy.
        :param resource_tag_logical_operator: Specifies whether to combine multiple resource tags with AND, so that a resource must have all tags to be included or excluded, or OR, so that a resource must have at least one tag. Default: ``AND``
        :param resource_tags: An array of ``ResourceTag`` objects, used to explicitly include resources in the policy scope or explicitly exclude them. If this isn't set, then tags aren't used to modify policy scope. See also ``ExcludeResourceTags`` .
        :param resource_type: The type of resource protected by or in scope of the policy. This is in the format shown in the `AWS Resource Types Reference <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html>`_ . To apply this policy to multiple resource types, specify a resource type of ``ResourceTypeList`` and then specify the resource types in a ``ResourceTypeList`` . The following are valid resource types for each Firewall Manager policy type: - AWS WAF Classic - ``AWS::ApiGateway::Stage`` , ``AWS::CloudFront::Distribution`` , and ``AWS::ElasticLoadBalancingV2::LoadBalancer`` . - AWS WAF - ``AWS::ApiGateway::Stage`` , ``AWS::ElasticLoadBalancingV2::LoadBalancer`` , and ``AWS::CloudFront::Distribution`` . - Shield Advanced - ``AWS::ElasticLoadBalancingV2::LoadBalancer`` , ``AWS::ElasticLoadBalancing::LoadBalancer`` , ``AWS::EC2::EIP`` , and ``AWS::CloudFront::Distribution`` . - Network ACL - ``AWS::EC2::Subnet`` . - Security group usage audit - ``AWS::EC2::SecurityGroup`` . - Security group content audit - ``AWS::EC2::SecurityGroup`` , ``AWS::EC2::NetworkInterface`` , and ``AWS::EC2::Instance`` . - DNS Firewall, AWS Network Firewall , and third-party firewall - ``AWS::EC2::VPC`` .
        :param resource_type_list: An array of ``ResourceType`` objects. Use this only to specify multiple resource types. To specify a single resource type, use ``ResourceType`` .
        :param security_service_policy_data: Details about the security service that is being used to protect the resources. This contains the following settings: - Type - Indicates the service type that the policy uses to protect the resource. For security group policies, Firewall Manager supports one security group for each common policy and for each content audit policy. This is an adjustable limit that you can increase by contacting . Valid values: ``DNS_FIREWALL`` | ``NETWORK_FIREWALL`` | ``SECURITY_GROUPS_COMMON`` | ``SECURITY_GROUPS_CONTENT_AUDIT`` | ``SECURITY_GROUPS_USAGE_AUDIT`` | ``SHIELD_ADVANCED`` | ``THIRD_PARTY_FIREWALL`` | ``WAFV2`` | ``WAF`` - ManagedServiceData - Details about the service that are specific to the service type, in JSON format. - Example: ``DNS_FIREWALL`` ``"{\\"type\\":\\"DNS_FIREWALL\\",\\"preProcessRuleGroups\\":[{\\"ruleGroupId\\":\\"rslvr-frg-1\\",\\"priority\\":10}],\\"postProcessRuleGroups\\":[{\\"ruleGroupId\\":\\"rslvr-frg-2\\",\\"priority\\":9911}]}"`` .. epigraph:: Valid values for ``preProcessRuleGroups`` are between 1 and 99. Valid values for ``postProcessRuleGroups`` are between 9901 and 10000. - Example: ``NETWORK_FIREWALL`` - Centralized deployment model ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"awsNetworkFirewallConfig\\":{\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":true}},\\"firewallDeploymentModel\\":{\\"centralizedFirewallDeploymentModel\\":{\\"centralizedFirewallOrchestrationConfig\\":{\\"inspectionVpcIds\\":[{\\"resourceId\\":\\"vpc-1234\\",\\"accountId\\":\\"123456789011\\"}],\\"firewallCreationConfig\\":{\\"endpointLocation\\":{\\"availabilityZoneConfigList\\":[{\\"availabilityZoneId\\":null,\\"availabilityZoneName\\":\\"us-east-1a\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]}]}},\\"allowedIPV4CidrList\\":[]}}}}"`` To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` . - Example: ``NETWORK_FIREWALL`` - Distributed deployment model with automatic Availability Zone configuration ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallOrchestrationConfig\\":{\\"singleFirewallEndpointPerVPC\\":false,\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\",\\"192.168.0.0/28\\"],\\"routeManagementAction\\":\\"OFF\\"},\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":true}}"`` With automatic Availbility Zone configuration, Firewall Manager chooses which Availability Zones to create the endpoints in. To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` . - Example: ``NETWORK_FIREWALL`` - Distributed deployment model with automatic Availability Zone configuration and route management ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallOrchestrationConfig\\":{\\"singleFirewallEndpointPerVPC\\":false,\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\",\\"192.168.0.0/28\\"],\\"routeManagementAction\\":\\"MONITOR\\",\\"routeManagementTargetTypes\\":[\\"InternetGateway\\"]},\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\": \\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":true}}"`` To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` . - Example: ``NETWORK_FIREWALL`` - Distributed deployment model with custom Availability Zone configuration ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"fragmentcustomactionname\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\", \\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}},{\\"actionName\\":\\"fragmentcustomactionname\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"fragmentmetricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallOrchestrationConfig\\":{\\"firewallCreationConfig\\":{ \\"endpointLocation\\":{\\"availabilityZoneConfigList\\":[{\\"availabilityZoneName\\":\\"us-east-1a\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]},{\\"availabilityZoneName\\":\\"us-east-1b\\",\\"allowedIPV4CidrList\\":[ \\"10.0.0.0/28\\"]}]} },\\"singleFirewallEndpointPerVPC\\":false,\\"allowedIPV4CidrList\\":null,\\"routeManagementAction\\":\\"OFF\\",\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":boolean}}"`` With custom Availability Zone configuration, you define which specific Availability Zones to create endpoints in by configuring ``firewallCreationConfig`` . To configure the Availability Zones in ``firewallCreationConfig`` , specify either the ``availabilityZoneName`` or ``availabilityZoneId`` parameter, not both parameters. To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` . - Example: ``NETWORK_FIREWALL`` - Distributed deployment model with custom Availability Zone configuration and route management ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"fragmentcustomactionname\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}},{\\"actionName\\":\\"fragmentcustomactionname\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"fragmentmetricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallOrchestrationConfig\\":{\\"firewallCreationConfig\\":{\\"endpointLocation\\":{\\"availabilityZoneConfigList\\":[{\\"availabilityZoneName\\":\\"us-east-1a\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]},{\\"availabilityZoneName\\":\\"us-east-1b\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]}]}},\\"singleFirewallEndpointPerVPC\\":false,\\"allowedIPV4CidrList\\":null,\\"routeManagementAction\\":\\"MONITOR\\",\\"routeManagementTargetTypes\\":[\\"InternetGateway\\"],\\"routeManagementConfig\\":{\\"allowCrossAZTrafficIfNoEndpoint\\":true}},\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":boolean}}"`` To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` . - Example: ``THIRD_PARTY_FIREWALL`` - Palo Alto Networks Cloud Next-Generation Firewall centralized deployment model ``"{ \\"type\\":\\"THIRD_PARTY_FIREWALL\\", \\"thirdPartyFirewall\\":\\"PALO_ALTO_NETWORKS_CLOUD_NGFW\\", \\"thirdPartyFirewallConfig\\":{ \\"thirdPartyFirewallPolicyList\\":[\\"global-1\\"] },\\"firewallDeploymentModel\\":{\\"centralizedFirewallDeploymentModel\\":{\\"centralizedFirewallOrchestrationConfig\\":{\\"inspectionVpcIds\\":[{\\"resourceId\\":\\"vpc-1234\\",\\"accountId\\":\\"123456789011\\"}],\\"firewallCreationConfig\\":{\\"endpointLocation\\":{\\"availabilityZoneConfigList\\":[{\\"availabilityZoneId\\":null,\\"availabilityZoneName\\":\\"us-east-1a\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]}]}},\\"allowedIPV4CidrList\\":[]}}}}"`` To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-thirdpartyfirewallpolicy.html>`_ to ``CENTRALIZED`` . - Example: ``THIRD_PARTY_FIREWALL`` - Palo Alto Networks Cloud Next-Generation Firewall distributed deployment model ``"{\\"type\\":\\"THIRD_PARTY_FIREWALL\\",\\"thirdPartyFirewall\\":\\"PALO_ALTO_NETWORKS_CLOUD_NGFW\\",\\"thirdPartyFirewallConfig\\":{\\"thirdPartyFirewallPolicyList\\":[\\"global-1\\"] },\\"firewallDeploymentModel\\":{ \\"distributedFirewallDeploymentModel\\":{ \\"distributedFirewallOrchestrationConfig\\":{\\"firewallCreationConfig\\":{\\"endpointLocation\\":{ \\"availabilityZoneConfigList\\":[ {\\"availabilityZoneName\\":\\"${AvailabilityZone}\\" } ] } }, \\"allowedIPV4CidrList\\":[ ] } } } }"`` To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-thirdpartyfirewallpolicy.html>`_ to ``DISTRIBUTED`` . - Specification for ``SHIELD_ADVANCED`` for Amazon CloudFront distributions ``"{\\"type\\":\\"SHIELD_ADVANCED\\",\\"automaticResponseConfiguration\\": {\\"automaticResponseStatus\\":\\"ENABLED|IGNORED|DISABLED\\", \\"automaticResponseAction\\":\\"BLOCK|COUNT\\"}, \\"overrideCustomerWebaclClassic\\":true|false}"`` For example: ``"{\\"type\\":\\"SHIELD_ADVANCED\\",\\"automaticResponseConfiguration\\": {\\"automaticResponseStatus\\":\\"ENABLED\\", \\"automaticResponseAction\\":\\"COUNT\\"}}"`` The default value for ``automaticResponseStatus`` is ``IGNORED`` . The value for ``automaticResponseAction`` is only required when ``automaticResponseStatus`` is set to ``ENABLED`` . The default value for ``overrideCustomerWebaclClassic`` is ``false`` . For other resource types that you can protect with a Shield Advanced policy, this ``ManagedServiceData`` configuration is an empty string. - Example: ``WAFV2`` ``"{\\"type\\":\\"WAFV2\\",\\"preProcessRuleGroups\\":[{\\"ruleGroupArn\\":null,\\"overrideAction\\":{\\"type\\":\\"NONE\\"},\\"managedRuleGroupIdentifier\\":{\\"version\\":null,\\"vendorName\\":\\"AWS\\",\\"managedRuleGroupName\\":\\"AWSManagedRulesAmazonIpReputationList\\"},\\"ruleGroupType\\":\\"ManagedRuleGroup\\",\\"excludeRules\\":[{\\"name\\":\\"NoUserAgent_HEADER\\"}]}],\\"postProcessRuleGroups\\":[],\\"defaultAction\\":{\\"type\\":\\"ALLOW\\"},\\"overrideCustomerWebACLAssociation\\":false,\\"loggingConfiguration\\":{\\"logDestinationConfigs\\":[\\"arn:aws:firehose:us-west-2:12345678912:deliverystream/aws-waf-logs-fms-admin-destination\\"],\\"redactedFields\\":[{\\"redactedFieldType\\":\\"SingleHeader\\",\\"redactedFieldValue\\":\\"Cookies\\"},{\\"redactedFieldType\\":\\"Method\\"}]}}"`` In the ``loggingConfiguration`` , you can specify one ``logDestinationConfigs`` , you can optionally provide up to 20 ``redactedFields`` , and the ``RedactedFieldType`` must be one of ``URI`` , ``QUERY_STRING`` , ``HEADER`` , or ``METHOD`` . - Example: ``AWS WAF Classic`` ``"{\\"type\\": \\"WAF\\", \\"ruleGroups\\": [{\\"id\\":\\"12345678-1bcd-9012-efga-0987654321ab\\", \\"overrideAction\\" : {\\"type\\": \\"COUNT\\"}}], \\"defaultAction\\": {\\"type\\": \\"BLOCK\\"}}"`` - Example: ``WAFV2`` - AWS Firewall Manager support for AWS WAF managed rule group versioning ``"{\\"type\\":\\"WAFV2\\",\\"preProcessRuleGroups\\":[{\\"ruleGroupArn\\":null,\\"overrideAction\\":{\\"type\\":\\"NONE\\"},\\"managedRuleGroupIdentifier\\":{\\"versionEnabled\\":true,\\"version\\":\\"Version_2.0\\",\\"vendorName\\":\\"AWS\\",\\"managedRuleGroupName\\":\\"AWSManagedRulesCommonRuleSet\\"},\\"ruleGroupType\\":\\"ManagedRuleGroup\\",\\"excludeRules\\":[{\\"name\\":\\"NoUserAgent_HEADER\\"}]}],\\"postProcessRuleGroups\\":[],\\"defaultAction\\":{\\"type\\":\\"ALLOW\\"},\\"overrideCustomerWebACLAssociation\\":false,\\"loggingConfiguration\\":{\\"logDestinationConfigs\\":[\\"arn:aws:firehose:us-west-2:12345678912:deliverystream/aws-waf-logs-fms-admin-destination\\"],\\"redactedFields\\":[{\\"redactedFieldType\\":\\"SingleHeader\\",\\"redactedFieldValue\\":\\"Cookies\\"},{\\"redactedFieldType\\":\\"Method\\"}]}}"`` To use a specific version of a AWS WAF managed rule group in your Firewall Manager policy, you must set ``versionEnabled`` to ``true`` , and set ``version`` to the version you'd like to use. If you don't set ``versionEnabled`` to ``true`` , or if you omit ``versionEnabled`` , then Firewall Manager uses the default version of the AWS WAF managed rule group. - Example: ``SECURITY_GROUPS_COMMON`` ``"{\\"type\\":\\"SECURITY_GROUPS_COMMON\\",\\"revertManualSecurityGroupChanges\\":false,\\"exclusiveResourceSecurityGroupManagement\\":false, \\"applyToAllEC2InstanceENIs\\":false,\\"securityGroups\\":[{\\"id\\":\\" sg-000e55995d61a06bd\\"}]}"`` - Example: Shared VPCs. Apply the preceding policy to resources in shared VPCs as well as to those in VPCs that the account owns ``"{\\"type\\":\\"SECURITY_GROUPS_COMMON\\",\\"revertManualSecurityGroupChanges\\":false,\\"exclusiveResourceSecurityGroupManagement\\":false, \\"applyToAllEC2InstanceENIs\\":false,\\"includeSharedVPC\\":true,\\"securityGroups\\":[{\\"id\\":\\" sg-000e55995d61a06bd\\"}]}"`` - Example: ``SECURITY_GROUPS_CONTENT_AUDIT`` ``"{\\"type\\":\\"SECURITY_GROUPS_CONTENT_AUDIT\\",\\"securityGroups\\":[{\\"id\\":\\"sg-000e55995d61a06bd\\"}],\\"securityGroupAction\\":{\\"type\\":\\"ALLOW\\"}}"`` The security group action for content audit can be ``ALLOW`` or ``DENY`` . For ``ALLOW`` , all in-scope security group rules must be within the allowed range of the policy's security group rules. For ``DENY`` , all in-scope security group rules must not contain a value or a range that matches a rule value or range in the policy security group. - Example: ``SECURITY_GROUPS_USAGE_AUDIT`` ``"{\\"type\\":\\"SECURITY_GROUPS_USAGE_AUDIT\\",\\"deleteUnusedSecurityGroups\\":true,\\"coalesceRedundantSecurityGroups\\":true}"``
        :param tags: A collection of key:value pairs associated with an AWS resource. The key:value pair can be anything you define. Typically, the tag key represents a category (such as "environment") and the tag value represents a specific value within that category (such as "test," "development," or "production"). You can add up to 50 tags to each AWS resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_fms import mixins as fms_mixins
            
            cfn_policy_mixin_props = fms_mixins.CfnPolicyMixinProps(
                delete_all_policy_resources=False,
                exclude_map={
                    "account": ["account"],
                    "orgunit": ["orgunit"]
                },
                exclude_resource_tags=False,
                include_map={
                    "account": ["account"],
                    "orgunit": ["orgunit"]
                },
                policy_description="policyDescription",
                policy_name="policyName",
                remediation_enabled=False,
                resources_clean_up=False,
                resource_set_ids=["resourceSetIds"],
                resource_tag_logical_operator="resourceTagLogicalOperator",
                resource_tags=[fms_mixins.CfnPolicyPropsMixin.ResourceTagProperty(
                    key="key",
                    value="value"
                )],
                resource_type="resourceType",
                resource_type_list=["resourceTypeList"],
                security_service_policy_data=fms_mixins.CfnPolicyPropsMixin.SecurityServicePolicyDataProperty(
                    managed_service_data="managedServiceData",
                    policy_option=fms_mixins.CfnPolicyPropsMixin.PolicyOptionProperty(
                        network_acl_common_policy=fms_mixins.CfnPolicyPropsMixin.NetworkAclCommonPolicyProperty(
                            network_acl_entry_set=fms_mixins.CfnPolicyPropsMixin.NetworkAclEntrySetProperty(
                                first_entries=[fms_mixins.CfnPolicyPropsMixin.NetworkAclEntryProperty(
                                    cidr_block="cidrBlock",
                                    egress=False,
                                    icmp_type_code=fms_mixins.CfnPolicyPropsMixin.IcmpTypeCodeProperty(
                                        code=123,
                                        type=123
                                    ),
                                    ipv6_cidr_block="ipv6CidrBlock",
                                    port_range=fms_mixins.CfnPolicyPropsMixin.PortRangeProperty(
                                        from=123,
                                        to=123
                                    ),
                                    protocol="protocol",
                                    rule_action="ruleAction"
                                )],
                                force_remediate_for_first_entries=False,
                                force_remediate_for_last_entries=False,
                                last_entries=[fms_mixins.CfnPolicyPropsMixin.NetworkAclEntryProperty(
                                    cidr_block="cidrBlock",
                                    egress=False,
                                    icmp_type_code=fms_mixins.CfnPolicyPropsMixin.IcmpTypeCodeProperty(
                                        code=123,
                                        type=123
                                    ),
                                    ipv6_cidr_block="ipv6CidrBlock",
                                    port_range=fms_mixins.CfnPolicyPropsMixin.PortRangeProperty(
                                        from=123,
                                        to=123
                                    ),
                                    protocol="protocol",
                                    rule_action="ruleAction"
                                )]
                            )
                        ),
                        network_firewall_policy=fms_mixins.CfnPolicyPropsMixin.NetworkFirewallPolicyProperty(
                            firewall_deployment_model="firewallDeploymentModel"
                        ),
                        third_party_firewall_policy=fms_mixins.CfnPolicyPropsMixin.ThirdPartyFirewallPolicyProperty(
                            firewall_deployment_model="firewallDeploymentModel"
                        )
                    ),
                    type="type"
                ),
                tags=[fms_mixins.CfnPolicyPropsMixin.PolicyTagProperty(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d64da381ce3dece9f4cc9562b4eca4c433c1dd2ee75de9d445baa07aa9c513e)
            check_type(argname="argument delete_all_policy_resources", value=delete_all_policy_resources, expected_type=type_hints["delete_all_policy_resources"])
            check_type(argname="argument exclude_map", value=exclude_map, expected_type=type_hints["exclude_map"])
            check_type(argname="argument exclude_resource_tags", value=exclude_resource_tags, expected_type=type_hints["exclude_resource_tags"])
            check_type(argname="argument include_map", value=include_map, expected_type=type_hints["include_map"])
            check_type(argname="argument policy_description", value=policy_description, expected_type=type_hints["policy_description"])
            check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
            check_type(argname="argument remediation_enabled", value=remediation_enabled, expected_type=type_hints["remediation_enabled"])
            check_type(argname="argument resources_clean_up", value=resources_clean_up, expected_type=type_hints["resources_clean_up"])
            check_type(argname="argument resource_set_ids", value=resource_set_ids, expected_type=type_hints["resource_set_ids"])
            check_type(argname="argument resource_tag_logical_operator", value=resource_tag_logical_operator, expected_type=type_hints["resource_tag_logical_operator"])
            check_type(argname="argument resource_tags", value=resource_tags, expected_type=type_hints["resource_tags"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            check_type(argname="argument resource_type_list", value=resource_type_list, expected_type=type_hints["resource_type_list"])
            check_type(argname="argument security_service_policy_data", value=security_service_policy_data, expected_type=type_hints["security_service_policy_data"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if delete_all_policy_resources is not None:
            self._values["delete_all_policy_resources"] = delete_all_policy_resources
        if exclude_map is not None:
            self._values["exclude_map"] = exclude_map
        if exclude_resource_tags is not None:
            self._values["exclude_resource_tags"] = exclude_resource_tags
        if include_map is not None:
            self._values["include_map"] = include_map
        if policy_description is not None:
            self._values["policy_description"] = policy_description
        if policy_name is not None:
            self._values["policy_name"] = policy_name
        if remediation_enabled is not None:
            self._values["remediation_enabled"] = remediation_enabled
        if resources_clean_up is not None:
            self._values["resources_clean_up"] = resources_clean_up
        if resource_set_ids is not None:
            self._values["resource_set_ids"] = resource_set_ids
        if resource_tag_logical_operator is not None:
            self._values["resource_tag_logical_operator"] = resource_tag_logical_operator
        if resource_tags is not None:
            self._values["resource_tags"] = resource_tags
        if resource_type is not None:
            self._values["resource_type"] = resource_type
        if resource_type_list is not None:
            self._values["resource_type_list"] = resource_type_list
        if security_service_policy_data is not None:
            self._values["security_service_policy_data"] = security_service_policy_data
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def delete_all_policy_resources(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Used when deleting a policy. If ``true`` , Firewall Manager performs cleanup according to the policy type.

        For AWS WAF and Shield Advanced policies, Firewall Manager does the following:

        - Deletes rule groups created by Firewall Manager
        - Removes web ACLs from in-scope resources
        - Deletes web ACLs that contain no rules or rule groups

        For security group policies, Firewall Manager does the following for each security group in the policy:

        - Disassociates the security group from in-scope resources
        - Deletes the security group if it was created through Firewall Manager and if it's no longer associated with any resources through another policy

        After the cleanup, in-scope resources are no longer protected by web ACLs in this policy. Protection of out-of-scope resources remains unchanged. Scope is determined by tags that you create and accounts that you associate with the policy. When creating the policy, if you specify that only resources in specific accounts or with specific tags are in scope of the policy, those accounts and resources are handled by the policy. All others are out of scope. If you don't specify tags or accounts, all resources are in scope.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html#cfn-fms-policy-deleteallpolicyresources
        '''
        result = self._values.get("delete_all_policy_resources")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def exclude_map(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyPropsMixin.IEMapProperty"]]:
        '''Specifies the AWS account IDs and AWS Organizations organizational units (OUs) to exclude from the policy.

        Specifying an OU is the equivalent of specifying all accounts in the OU and in any of its child OUs, including any child OUs and accounts that are added at a later time.

        You can specify inclusions or exclusions, but not both. If you specify an ``IncludeMap`` , AWS Firewall Manager applies the policy to all accounts specified by the ``IncludeMap`` , and does not evaluate any ``ExcludeMap`` specifications. If you do not specify an ``IncludeMap`` , then Firewall Manager applies the policy to all accounts except for those specified by the ``ExcludeMap`` .

        You can specify account IDs, OUs, or a combination:

        - Specify account IDs by setting the key to ``ACCOUNT`` . For example, the following is a valid map: ``{“ACCOUNT” : [“accountID1”, “accountID2”]}`` .
        - Specify OUs by setting the key to ``ORGUNIT`` . For example, the following is a valid map: ``{“ORGUNIT” : [“ouid111”, “ouid112”]}`` .
        - Specify accounts and OUs together in a single map, separated with a comma. For example, the following is a valid map: ``{“ACCOUNT” : [“accountID1”, “accountID2”], “ORGUNIT” : [“ouid111”, “ouid112”]}`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html#cfn-fms-policy-excludemap
        '''
        result = self._values.get("exclude_map")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyPropsMixin.IEMapProperty"]], result)

    @builtins.property
    def exclude_resource_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Used only when tags are specified in the ``ResourceTags`` property.

        If this property is ``True`` , resources with the specified tags are not in scope of the policy. If it's ``False`` , only resources with the specified tags are in scope of the policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html#cfn-fms-policy-excluderesourcetags
        '''
        result = self._values.get("exclude_resource_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def include_map(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyPropsMixin.IEMapProperty"]]:
        '''Specifies the AWS account IDs and AWS Organizations organizational units (OUs) to include in the policy.

        Specifying an OU is the equivalent of specifying all accounts in the OU and in any of its child OUs, including any child OUs and accounts that are added at a later time.

        You can specify inclusions or exclusions, but not both. If you specify an ``IncludeMap`` , AWS Firewall Manager applies the policy to all accounts specified by the ``IncludeMap`` , and does not evaluate any ``ExcludeMap`` specifications. If you do not specify an ``IncludeMap`` , then Firewall Manager applies the policy to all accounts except for those specified by the ``ExcludeMap`` .

        You can specify account IDs, OUs, or a combination:

        - Specify account IDs by setting the key to ``ACCOUNT`` . For example, the following is a valid map: ``{“ACCOUNT” : [“accountID1”, “accountID2”]}`` .
        - Specify OUs by setting the key to ``ORGUNIT`` . For example, the following is a valid map: ``{“ORGUNIT” : [“ouid111”, “ouid112”]}`` .
        - Specify accounts and OUs together in a single map, separated with a comma. For example, the following is a valid map: ``{“ACCOUNT” : [“accountID1”, “accountID2”], “ORGUNIT” : [“ouid111”, “ouid112”]}`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html#cfn-fms-policy-includemap
        '''
        result = self._values.get("include_map")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyPropsMixin.IEMapProperty"]], result)

    @builtins.property
    def policy_description(self) -> typing.Optional[builtins.str]:
        '''Your description of the AWS Firewall Manager policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html#cfn-fms-policy-policydescription
        '''
        result = self._values.get("policy_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_name(self) -> typing.Optional[builtins.str]:
        '''The name of the AWS Firewall Manager policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html#cfn-fms-policy-policyname
        '''
        result = self._values.get("policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remediation_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Indicates if the policy should be automatically applied to new resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html#cfn-fms-policy-remediationenabled
        '''
        result = self._values.get("remediation_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def resources_clean_up(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Indicates whether AWS Firewall Manager should automatically remove protections from resources that leave the policy scope and clean up resources that Firewall Manager is managing for accounts when those accounts leave policy scope.

        For example, Firewall Manager will disassociate a Firewall Manager managed web ACL from a protected customer resource when the customer resource leaves policy scope.

        By default, Firewall Manager doesn't remove protections or delete Firewall Manager managed resources.

        This option is not available for Shield Advanced or AWS WAF Classic policies.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html#cfn-fms-policy-resourcescleanup
        '''
        result = self._values.get("resources_clean_up")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def resource_set_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The unique identifiers of the resource sets used by the policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html#cfn-fms-policy-resourcesetids
        '''
        result = self._values.get("resource_set_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def resource_tag_logical_operator(self) -> typing.Optional[builtins.str]:
        '''Specifies whether to combine multiple resource tags with AND, so that a resource must have all tags to be included or excluded, or OR, so that a resource must have at least one tag.

        Default: ``AND``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html#cfn-fms-policy-resourcetaglogicaloperator
        '''
        result = self._values.get("resource_tag_logical_operator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_tags(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyPropsMixin.ResourceTagProperty"]]]]:
        '''An array of ``ResourceTag`` objects, used to explicitly include resources in the policy scope or explicitly exclude them.

        If this isn't set, then tags aren't used to modify policy scope. See also ``ExcludeResourceTags`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html#cfn-fms-policy-resourcetags
        '''
        result = self._values.get("resource_tags")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyPropsMixin.ResourceTagProperty"]]]], result)

    @builtins.property
    def resource_type(self) -> typing.Optional[builtins.str]:
        '''The type of resource protected by or in scope of the policy.

        This is in the format shown in the `AWS Resource Types Reference <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html>`_ . To apply this policy to multiple resource types, specify a resource type of ``ResourceTypeList`` and then specify the resource types in a ``ResourceTypeList`` .

        The following are valid resource types for each Firewall Manager policy type:

        - AWS WAF Classic - ``AWS::ApiGateway::Stage`` , ``AWS::CloudFront::Distribution`` , and ``AWS::ElasticLoadBalancingV2::LoadBalancer`` .
        - AWS WAF - ``AWS::ApiGateway::Stage`` , ``AWS::ElasticLoadBalancingV2::LoadBalancer`` , and ``AWS::CloudFront::Distribution`` .
        - Shield Advanced - ``AWS::ElasticLoadBalancingV2::LoadBalancer`` , ``AWS::ElasticLoadBalancing::LoadBalancer`` , ``AWS::EC2::EIP`` , and ``AWS::CloudFront::Distribution`` .
        - Network ACL - ``AWS::EC2::Subnet`` .
        - Security group usage audit - ``AWS::EC2::SecurityGroup`` .
        - Security group content audit - ``AWS::EC2::SecurityGroup`` , ``AWS::EC2::NetworkInterface`` , and ``AWS::EC2::Instance`` .
        - DNS Firewall, AWS Network Firewall , and third-party firewall - ``AWS::EC2::VPC`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html#cfn-fms-policy-resourcetype
        '''
        result = self._values.get("resource_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_type_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of ``ResourceType`` objects.

        Use this only to specify multiple resource types. To specify a single resource type, use ``ResourceType`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html#cfn-fms-policy-resourcetypelist
        '''
        result = self._values.get("resource_type_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def security_service_policy_data(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyPropsMixin.SecurityServicePolicyDataProperty"]]:
        '''Details about the security service that is being used to protect the resources.

        This contains the following settings:

        - Type - Indicates the service type that the policy uses to protect the resource. For security group policies, Firewall Manager supports one security group for each common policy and for each content audit policy. This is an adjustable limit that you can increase by contacting  .

        Valid values: ``DNS_FIREWALL`` | ``NETWORK_FIREWALL`` | ``SECURITY_GROUPS_COMMON`` | ``SECURITY_GROUPS_CONTENT_AUDIT`` | ``SECURITY_GROUPS_USAGE_AUDIT`` | ``SHIELD_ADVANCED`` | ``THIRD_PARTY_FIREWALL`` | ``WAFV2`` | ``WAF``

        - ManagedServiceData - Details about the service that are specific to the service type, in JSON format.
        - Example: ``DNS_FIREWALL``

        ``"{\\"type\\":\\"DNS_FIREWALL\\",\\"preProcessRuleGroups\\":[{\\"ruleGroupId\\":\\"rslvr-frg-1\\",\\"priority\\":10}],\\"postProcessRuleGroups\\":[{\\"ruleGroupId\\":\\"rslvr-frg-2\\",\\"priority\\":9911}]}"``
        .. epigraph::

           Valid values for ``preProcessRuleGroups`` are between 1 and 99. Valid values for ``postProcessRuleGroups`` are between 9901 and 10000.

        - Example: ``NETWORK_FIREWALL`` - Centralized deployment model

        ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"awsNetworkFirewallConfig\\":{\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":true}},\\"firewallDeploymentModel\\":{\\"centralizedFirewallDeploymentModel\\":{\\"centralizedFirewallOrchestrationConfig\\":{\\"inspectionVpcIds\\":[{\\"resourceId\\":\\"vpc-1234\\",\\"accountId\\":\\"123456789011\\"}],\\"firewallCreationConfig\\":{\\"endpointLocation\\":{\\"availabilityZoneConfigList\\":[{\\"availabilityZoneId\\":null,\\"availabilityZoneName\\":\\"us-east-1a\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]}]}},\\"allowedIPV4CidrList\\":[]}}}}"``

        To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` .

        - Example: ``NETWORK_FIREWALL`` - Distributed deployment model with automatic Availability Zone configuration

        ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallOrchestrationConfig\\":{\\"singleFirewallEndpointPerVPC\\":false,\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\",\\"192.168.0.0/28\\"],\\"routeManagementAction\\":\\"OFF\\"},\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":true}}"``

        With automatic Availbility Zone configuration, Firewall Manager chooses which Availability Zones to create the endpoints in. To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` .

        - Example: ``NETWORK_FIREWALL`` - Distributed deployment model with automatic Availability Zone configuration and route management

        ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallOrchestrationConfig\\":{\\"singleFirewallEndpointPerVPC\\":false,\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\",\\"192.168.0.0/28\\"],\\"routeManagementAction\\":\\"MONITOR\\",\\"routeManagementTargetTypes\\":[\\"InternetGateway\\"]},\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\": \\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":true}}"``

        To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` .

        - Example: ``NETWORK_FIREWALL`` - Distributed deployment model with custom Availability Zone configuration

        ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"fragmentcustomactionname\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\", \\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}},{\\"actionName\\":\\"fragmentcustomactionname\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"fragmentmetricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallOrchestrationConfig\\":{\\"firewallCreationConfig\\":{ \\"endpointLocation\\":{\\"availabilityZoneConfigList\\":[{\\"availabilityZoneName\\":\\"us-east-1a\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]},{\\"availabilityZoneName\\":\\"us-east-1b\\",\\"allowedIPV4CidrList\\":[ \\"10.0.0.0/28\\"]}]} },\\"singleFirewallEndpointPerVPC\\":false,\\"allowedIPV4CidrList\\":null,\\"routeManagementAction\\":\\"OFF\\",\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":boolean}}"``

        With custom Availability Zone configuration, you define which specific Availability Zones to create endpoints in by configuring ``firewallCreationConfig`` . To configure the Availability Zones in ``firewallCreationConfig`` , specify either the ``availabilityZoneName`` or ``availabilityZoneId`` parameter, not both parameters.

        To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` .

        - Example: ``NETWORK_FIREWALL`` - Distributed deployment model with custom Availability Zone configuration and route management

        ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"fragmentcustomactionname\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}},{\\"actionName\\":\\"fragmentcustomactionname\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"fragmentmetricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallOrchestrationConfig\\":{\\"firewallCreationConfig\\":{\\"endpointLocation\\":{\\"availabilityZoneConfigList\\":[{\\"availabilityZoneName\\":\\"us-east-1a\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]},{\\"availabilityZoneName\\":\\"us-east-1b\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]}]}},\\"singleFirewallEndpointPerVPC\\":false,\\"allowedIPV4CidrList\\":null,\\"routeManagementAction\\":\\"MONITOR\\",\\"routeManagementTargetTypes\\":[\\"InternetGateway\\"],\\"routeManagementConfig\\":{\\"allowCrossAZTrafficIfNoEndpoint\\":true}},\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":boolean}}"``

        To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` .

        - Example: ``THIRD_PARTY_FIREWALL`` - Palo Alto Networks Cloud Next-Generation Firewall centralized deployment model

        ``"{ \\"type\\":\\"THIRD_PARTY_FIREWALL\\", \\"thirdPartyFirewall\\":\\"PALO_ALTO_NETWORKS_CLOUD_NGFW\\", \\"thirdPartyFirewallConfig\\":{ \\"thirdPartyFirewallPolicyList\\":[\\"global-1\\"] },\\"firewallDeploymentModel\\":{\\"centralizedFirewallDeploymentModel\\":{\\"centralizedFirewallOrchestrationConfig\\":{\\"inspectionVpcIds\\":[{\\"resourceId\\":\\"vpc-1234\\",\\"accountId\\":\\"123456789011\\"}],\\"firewallCreationConfig\\":{\\"endpointLocation\\":{\\"availabilityZoneConfigList\\":[{\\"availabilityZoneId\\":null,\\"availabilityZoneName\\":\\"us-east-1a\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]}]}},\\"allowedIPV4CidrList\\":[]}}}}"``

        To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-thirdpartyfirewallpolicy.html>`_ to ``CENTRALIZED`` .

        - Example: ``THIRD_PARTY_FIREWALL`` - Palo Alto Networks Cloud Next-Generation Firewall distributed deployment model

        ``"{\\"type\\":\\"THIRD_PARTY_FIREWALL\\",\\"thirdPartyFirewall\\":\\"PALO_ALTO_NETWORKS_CLOUD_NGFW\\",\\"thirdPartyFirewallConfig\\":{\\"thirdPartyFirewallPolicyList\\":[\\"global-1\\"] },\\"firewallDeploymentModel\\":{ \\"distributedFirewallDeploymentModel\\":{ \\"distributedFirewallOrchestrationConfig\\":{\\"firewallCreationConfig\\":{\\"endpointLocation\\":{ \\"availabilityZoneConfigList\\":[ {\\"availabilityZoneName\\":\\"${AvailabilityZone}\\" } ] } }, \\"allowedIPV4CidrList\\":[ ] } } } }"``

        To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-thirdpartyfirewallpolicy.html>`_ to ``DISTRIBUTED`` .

        - Specification for ``SHIELD_ADVANCED`` for Amazon CloudFront distributions

        ``"{\\"type\\":\\"SHIELD_ADVANCED\\",\\"automaticResponseConfiguration\\": {\\"automaticResponseStatus\\":\\"ENABLED|IGNORED|DISABLED\\", \\"automaticResponseAction\\":\\"BLOCK|COUNT\\"}, \\"overrideCustomerWebaclClassic\\":true|false}"``

        For example: ``"{\\"type\\":\\"SHIELD_ADVANCED\\",\\"automaticResponseConfiguration\\": {\\"automaticResponseStatus\\":\\"ENABLED\\", \\"automaticResponseAction\\":\\"COUNT\\"}}"``

        The default value for ``automaticResponseStatus`` is ``IGNORED`` . The value for ``automaticResponseAction`` is only required when ``automaticResponseStatus`` is set to ``ENABLED`` . The default value for ``overrideCustomerWebaclClassic`` is ``false`` .

        For other resource types that you can protect with a Shield Advanced policy, this ``ManagedServiceData`` configuration is an empty string.

        - Example: ``WAFV2``

        ``"{\\"type\\":\\"WAFV2\\",\\"preProcessRuleGroups\\":[{\\"ruleGroupArn\\":null,\\"overrideAction\\":{\\"type\\":\\"NONE\\"},\\"managedRuleGroupIdentifier\\":{\\"version\\":null,\\"vendorName\\":\\"AWS\\",\\"managedRuleGroupName\\":\\"AWSManagedRulesAmazonIpReputationList\\"},\\"ruleGroupType\\":\\"ManagedRuleGroup\\",\\"excludeRules\\":[{\\"name\\":\\"NoUserAgent_HEADER\\"}]}],\\"postProcessRuleGroups\\":[],\\"defaultAction\\":{\\"type\\":\\"ALLOW\\"},\\"overrideCustomerWebACLAssociation\\":false,\\"loggingConfiguration\\":{\\"logDestinationConfigs\\":[\\"arn:aws:firehose:us-west-2:12345678912:deliverystream/aws-waf-logs-fms-admin-destination\\"],\\"redactedFields\\":[{\\"redactedFieldType\\":\\"SingleHeader\\",\\"redactedFieldValue\\":\\"Cookies\\"},{\\"redactedFieldType\\":\\"Method\\"}]}}"``

        In the ``loggingConfiguration`` , you can specify one ``logDestinationConfigs`` , you can optionally provide up to 20 ``redactedFields`` , and the ``RedactedFieldType`` must be one of ``URI`` , ``QUERY_STRING`` , ``HEADER`` , or ``METHOD`` .

        - Example: ``AWS WAF Classic``

        ``"{\\"type\\": \\"WAF\\", \\"ruleGroups\\": [{\\"id\\":\\"12345678-1bcd-9012-efga-0987654321ab\\", \\"overrideAction\\" : {\\"type\\": \\"COUNT\\"}}], \\"defaultAction\\": {\\"type\\": \\"BLOCK\\"}}"``

        - Example: ``WAFV2`` - AWS Firewall Manager support for AWS WAF managed rule group versioning

        ``"{\\"type\\":\\"WAFV2\\",\\"preProcessRuleGroups\\":[{\\"ruleGroupArn\\":null,\\"overrideAction\\":{\\"type\\":\\"NONE\\"},\\"managedRuleGroupIdentifier\\":{\\"versionEnabled\\":true,\\"version\\":\\"Version_2.0\\",\\"vendorName\\":\\"AWS\\",\\"managedRuleGroupName\\":\\"AWSManagedRulesCommonRuleSet\\"},\\"ruleGroupType\\":\\"ManagedRuleGroup\\",\\"excludeRules\\":[{\\"name\\":\\"NoUserAgent_HEADER\\"}]}],\\"postProcessRuleGroups\\":[],\\"defaultAction\\":{\\"type\\":\\"ALLOW\\"},\\"overrideCustomerWebACLAssociation\\":false,\\"loggingConfiguration\\":{\\"logDestinationConfigs\\":[\\"arn:aws:firehose:us-west-2:12345678912:deliverystream/aws-waf-logs-fms-admin-destination\\"],\\"redactedFields\\":[{\\"redactedFieldType\\":\\"SingleHeader\\",\\"redactedFieldValue\\":\\"Cookies\\"},{\\"redactedFieldType\\":\\"Method\\"}]}}"``

        To use a specific version of a AWS WAF managed rule group in your Firewall Manager policy, you must set ``versionEnabled`` to ``true`` , and set ``version`` to the version you'd like to use. If you don't set ``versionEnabled`` to ``true`` , or if you omit ``versionEnabled`` , then Firewall Manager uses the default version of the AWS WAF managed rule group.

        - Example: ``SECURITY_GROUPS_COMMON``

        ``"{\\"type\\":\\"SECURITY_GROUPS_COMMON\\",\\"revertManualSecurityGroupChanges\\":false,\\"exclusiveResourceSecurityGroupManagement\\":false, \\"applyToAllEC2InstanceENIs\\":false,\\"securityGroups\\":[{\\"id\\":\\" sg-000e55995d61a06bd\\"}]}"``

        - Example: Shared VPCs. Apply the preceding policy to resources in shared VPCs as well as to those in VPCs that the account owns

        ``"{\\"type\\":\\"SECURITY_GROUPS_COMMON\\",\\"revertManualSecurityGroupChanges\\":false,\\"exclusiveResourceSecurityGroupManagement\\":false, \\"applyToAllEC2InstanceENIs\\":false,\\"includeSharedVPC\\":true,\\"securityGroups\\":[{\\"id\\":\\" sg-000e55995d61a06bd\\"}]}"``

        - Example: ``SECURITY_GROUPS_CONTENT_AUDIT``

        ``"{\\"type\\":\\"SECURITY_GROUPS_CONTENT_AUDIT\\",\\"securityGroups\\":[{\\"id\\":\\"sg-000e55995d61a06bd\\"}],\\"securityGroupAction\\":{\\"type\\":\\"ALLOW\\"}}"``

        The security group action for content audit can be ``ALLOW`` or ``DENY`` . For ``ALLOW`` , all in-scope security group rules must be within the allowed range of the policy's security group rules. For ``DENY`` , all in-scope security group rules must not contain a value or a range that matches a rule value or range in the policy security group.

        - Example: ``SECURITY_GROUPS_USAGE_AUDIT``

        ``"{\\"type\\":\\"SECURITY_GROUPS_USAGE_AUDIT\\",\\"deleteUnusedSecurityGroups\\":true,\\"coalesceRedundantSecurityGroups\\":true}"``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html#cfn-fms-policy-securityservicepolicydata
        '''
        result = self._values.get("security_service_policy_data")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyPropsMixin.SecurityServicePolicyDataProperty"]], result)

    @builtins.property
    def tags(
        self,
    ) -> typing.Optional[typing.List["CfnPolicyPropsMixin.PolicyTagProperty"]]:
        '''A collection of key:value pairs associated with an AWS resource.

        The key:value pair can be anything you define. Typically, the tag key represents a category (such as "environment") and the tag value represents a specific value within that category (such as "test," "development," or "production"). You can add up to 50 tags to each AWS resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html#cfn-fms-policy-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["CfnPolicyPropsMixin.PolicyTagProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPolicyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPolicyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_fms.mixins.CfnPolicyPropsMixin",
):
    '''An AWS Firewall Manager policy.

    A Firewall Manager policy is specific to the individual policy type. If you want to enforce multiple policy types across accounts, you can create multiple policies. You can create more than one policy for each type.

    If you add a new account to an organization that you created with AWS Organizations , Firewall Manager automatically applies the policy to the resources in that account that are within scope of the policy.

    Policies require some setup to use. For more information, see the sections on prerequisites and getting started under `Firewall Manager prerequisites <https://docs.aws.amazon.com/waf/latest/developerguide/fms-prereq.html>`_ .

    Firewall Manager provides the following types of policies:

    - *AWS WAF policy* - This policy applies AWS WAF web ACL protections to specified accounts and resources.
    - *Shield Advanced policy* - This policy applies Shield Advanced protection to specified accounts and resources.
    - *Security Groups policy* - This type of policy gives you control over security groups that are in use throughout your organization in AWS Organizations and lets you enforce a baseline set of rules across your organization.
    - *Network ACL policy* - This type of policy gives you control over the network ACLs that are in use throughout your organization in AWS Organizations and lets you enforce a baseline set of first and last network ACL rules across your organization.
    - *Network Firewall policy* - This policy applies Network Firewall protection to your organization's VPCs.
    - *DNS Firewall policy* - This policy applies Amazon Route 53 Resolver DNS Firewall protections to your organization's VPCs.
    - *Third-party firewall policy* - This policy applies third-party firewall protections. Third-party firewalls are available by subscription through the AWS Marketplace console at `AWS Marketplace <https://docs.aws.amazon.com/marketplace>`_ .
    - *Palo Alto Networks Cloud NGFW policy* - This policy applies Palo Alto Networks Cloud Next Generation Firewall (NGFW) protections and Palo Alto Networks Cloud NGFW rulestacks to your organization's VPCs.
    - *Fortigate CNF policy* - This policy applies Fortigate Cloud Native Firewall (CNF) protections. Fortigate CNF is a cloud-centered solution that blocks Zero-Day threats and secures cloud infrastructures with industry-leading advanced threat prevention, smart web application firewalls (WAF), and API protection.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html
    :cloudformationResource: AWS::FMS::Policy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_fms import mixins as fms_mixins
        
        cfn_policy_props_mixin = fms_mixins.CfnPolicyPropsMixin(fms_mixins.CfnPolicyMixinProps(
            delete_all_policy_resources=False,
            exclude_map={
                "account": ["account"],
                "orgunit": ["orgunit"]
            },
            exclude_resource_tags=False,
            include_map={
                "account": ["account"],
                "orgunit": ["orgunit"]
            },
            policy_description="policyDescription",
            policy_name="policyName",
            remediation_enabled=False,
            resources_clean_up=False,
            resource_set_ids=["resourceSetIds"],
            resource_tag_logical_operator="resourceTagLogicalOperator",
            resource_tags=[fms_mixins.CfnPolicyPropsMixin.ResourceTagProperty(
                key="key",
                value="value"
            )],
            resource_type="resourceType",
            resource_type_list=["resourceTypeList"],
            security_service_policy_data=fms_mixins.CfnPolicyPropsMixin.SecurityServicePolicyDataProperty(
                managed_service_data="managedServiceData",
                policy_option=fms_mixins.CfnPolicyPropsMixin.PolicyOptionProperty(
                    network_acl_common_policy=fms_mixins.CfnPolicyPropsMixin.NetworkAclCommonPolicyProperty(
                        network_acl_entry_set=fms_mixins.CfnPolicyPropsMixin.NetworkAclEntrySetProperty(
                            first_entries=[fms_mixins.CfnPolicyPropsMixin.NetworkAclEntryProperty(
                                cidr_block="cidrBlock",
                                egress=False,
                                icmp_type_code=fms_mixins.CfnPolicyPropsMixin.IcmpTypeCodeProperty(
                                    code=123,
                                    type=123
                                ),
                                ipv6_cidr_block="ipv6CidrBlock",
                                port_range=fms_mixins.CfnPolicyPropsMixin.PortRangeProperty(
                                    from=123,
                                    to=123
                                ),
                                protocol="protocol",
                                rule_action="ruleAction"
                            )],
                            force_remediate_for_first_entries=False,
                            force_remediate_for_last_entries=False,
                            last_entries=[fms_mixins.CfnPolicyPropsMixin.NetworkAclEntryProperty(
                                cidr_block="cidrBlock",
                                egress=False,
                                icmp_type_code=fms_mixins.CfnPolicyPropsMixin.IcmpTypeCodeProperty(
                                    code=123,
                                    type=123
                                ),
                                ipv6_cidr_block="ipv6CidrBlock",
                                port_range=fms_mixins.CfnPolicyPropsMixin.PortRangeProperty(
                                    from=123,
                                    to=123
                                ),
                                protocol="protocol",
                                rule_action="ruleAction"
                            )]
                        )
                    ),
                    network_firewall_policy=fms_mixins.CfnPolicyPropsMixin.NetworkFirewallPolicyProperty(
                        firewall_deployment_model="firewallDeploymentModel"
                    ),
                    third_party_firewall_policy=fms_mixins.CfnPolicyPropsMixin.ThirdPartyFirewallPolicyProperty(
                        firewall_deployment_model="firewallDeploymentModel"
                    )
                ),
                type="type"
            ),
            tags=[fms_mixins.CfnPolicyPropsMixin.PolicyTagProperty(
                key="key",
                value="value"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::FMS::Policy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f1987207e12dde62cf379bb2739f25551cef507c75f6129a5341da10bcffb75)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9dcf9cf0343a3ae68b5bac4252c7d8b6eba98a67102a05bf192ded521b04d731)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__826efa27110674dc325a352e4d5e8fe72dde51cbe246300e3395875609ac98fe)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPolicyMixinProps:
        return typing.cast(CfnPolicyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fms.mixins.CfnPolicyPropsMixin.IEMapProperty",
        jsii_struct_bases=[],
        name_mapping={"account": "account", "orgunit": "orgunit"},
    )
    class IEMapProperty:
        def __init__(
            self,
            *,
            account: typing.Optional[typing.Sequence[builtins.str]] = None,
            orgunit: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Specifies the AWS account IDs and AWS Organizations organizational units (OUs) to include in or exclude from the policy.

            Specifying an OU is the equivalent of specifying all accounts in the OU and in any of its child OUs, including any child OUs and accounts that are added at a later time.

            This is used for the policy's ``IncludeMap`` and ``ExcludeMap`` .

            You can specify account IDs, OUs, or a combination:

            - Specify account IDs by setting the key to ``ACCOUNT`` . For example, the following is a valid map: ``{“ACCOUNT” : [“accountID1”, “accountID2”]}`` .
            - Specify OUs by setting the key to ``ORGUNIT`` . For example, the following is a valid map: ``{“ORGUNIT” : [“ouid111”, “ouid112”]}`` .
            - Specify accounts and OUs together in a single map, separated with a comma. For example, the following is a valid map: ``{“ACCOUNT” : [“accountID1”, “accountID2”], “ORGUNIT” : [“ouid111”, “ouid112”]}`` .

            :param account: The account list for the map.
            :param orgunit: The organizational unit list for the map.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-iemap.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fms import mixins as fms_mixins
                
                i_eMap_property = {
                    "account": ["account"],
                    "orgunit": ["orgunit"]
                }
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9d86b0b120942b5f38e8304a1793cfd6a283aad4c81c9cf15a20a24dc33ae1ee)
                check_type(argname="argument account", value=account, expected_type=type_hints["account"])
                check_type(argname="argument orgunit", value=orgunit, expected_type=type_hints["orgunit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if account is not None:
                self._values["account"] = account
            if orgunit is not None:
                self._values["orgunit"] = orgunit

        @builtins.property
        def account(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The account list for the map.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-iemap.html#cfn-fms-policy-iemap-account
            '''
            result = self._values.get("account")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def orgunit(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The organizational unit list for the map.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-iemap.html#cfn-fms-policy-iemap-orgunit
            '''
            result = self._values.get("orgunit")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IEMapProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fms.mixins.CfnPolicyPropsMixin.IcmpTypeCodeProperty",
        jsii_struct_bases=[],
        name_mapping={"code": "code", "type": "type"},
    )
    class IcmpTypeCodeProperty:
        def __init__(
            self,
            *,
            code: typing.Optional[jsii.Number] = None,
            type: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''ICMP protocol: The ICMP type and code.

            :param code: ICMP code.
            :param type: ICMP type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-icmptypecode.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fms import mixins as fms_mixins
                
                icmp_type_code_property = fms_mixins.CfnPolicyPropsMixin.IcmpTypeCodeProperty(
                    code=123,
                    type=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ef758e1d3ae927eaaa052c2b92b1fa3a4f8a71e8996c717f10bdc7727aa82ea9)
                check_type(argname="argument code", value=code, expected_type=type_hints["code"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if code is not None:
                self._values["code"] = code
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def code(self) -> typing.Optional[jsii.Number]:
            '''ICMP code.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-icmptypecode.html#cfn-fms-policy-icmptypecode-code
            '''
            result = self._values.get("code")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def type(self) -> typing.Optional[jsii.Number]:
            '''ICMP type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-icmptypecode.html#cfn-fms-policy-icmptypecode-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IcmpTypeCodeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fms.mixins.CfnPolicyPropsMixin.NetworkAclCommonPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"network_acl_entry_set": "networkAclEntrySet"},
    )
    class NetworkAclCommonPolicyProperty:
        def __init__(
            self,
            *,
            network_acl_entry_set: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPolicyPropsMixin.NetworkAclEntrySetProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Defines a Firewall Manager network ACL policy.

            This is used in the ``PolicyOption`` of a ``SecurityServicePolicyData`` for a ``Policy`` , when the ``SecurityServicePolicyData`` type is set to ``NETWORK_ACL_COMMON`` .

            For information about network ACLs, see `Control traffic to subnets using network ACLs <https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html>`_ in the *Amazon Virtual Private Cloud User Guide* .

            :param network_acl_entry_set: The definition of the first and last rules for the network ACL policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkaclcommonpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fms import mixins as fms_mixins
                
                network_acl_common_policy_property = fms_mixins.CfnPolicyPropsMixin.NetworkAclCommonPolicyProperty(
                    network_acl_entry_set=fms_mixins.CfnPolicyPropsMixin.NetworkAclEntrySetProperty(
                        first_entries=[fms_mixins.CfnPolicyPropsMixin.NetworkAclEntryProperty(
                            cidr_block="cidrBlock",
                            egress=False,
                            icmp_type_code=fms_mixins.CfnPolicyPropsMixin.IcmpTypeCodeProperty(
                                code=123,
                                type=123
                            ),
                            ipv6_cidr_block="ipv6CidrBlock",
                            port_range=fms_mixins.CfnPolicyPropsMixin.PortRangeProperty(
                                from=123,
                                to=123
                            ),
                            protocol="protocol",
                            rule_action="ruleAction"
                        )],
                        force_remediate_for_first_entries=False,
                        force_remediate_for_last_entries=False,
                        last_entries=[fms_mixins.CfnPolicyPropsMixin.NetworkAclEntryProperty(
                            cidr_block="cidrBlock",
                            egress=False,
                            icmp_type_code=fms_mixins.CfnPolicyPropsMixin.IcmpTypeCodeProperty(
                                code=123,
                                type=123
                            ),
                            ipv6_cidr_block="ipv6CidrBlock",
                            port_range=fms_mixins.CfnPolicyPropsMixin.PortRangeProperty(
                                from=123,
                                to=123
                            ),
                            protocol="protocol",
                            rule_action="ruleAction"
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__488c4fcde080373477bb882fb5797280a201b4e08d06e2860a1e8d45f404ac1c)
                check_type(argname="argument network_acl_entry_set", value=network_acl_entry_set, expected_type=type_hints["network_acl_entry_set"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if network_acl_entry_set is not None:
                self._values["network_acl_entry_set"] = network_acl_entry_set

        @builtins.property
        def network_acl_entry_set(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyPropsMixin.NetworkAclEntrySetProperty"]]:
            '''The definition of the first and last rules for the network ACL policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkaclcommonpolicy.html#cfn-fms-policy-networkaclcommonpolicy-networkaclentryset
            '''
            result = self._values.get("network_acl_entry_set")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyPropsMixin.NetworkAclEntrySetProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NetworkAclCommonPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fms.mixins.CfnPolicyPropsMixin.NetworkAclEntryProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cidr_block": "cidrBlock",
            "egress": "egress",
            "icmp_type_code": "icmpTypeCode",
            "ipv6_cidr_block": "ipv6CidrBlock",
            "port_range": "portRange",
            "protocol": "protocol",
            "rule_action": "ruleAction",
        },
    )
    class NetworkAclEntryProperty:
        def __init__(
            self,
            *,
            cidr_block: typing.Optional[builtins.str] = None,
            egress: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            icmp_type_code: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPolicyPropsMixin.IcmpTypeCodeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ipv6_cidr_block: typing.Optional[builtins.str] = None,
            port_range: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPolicyPropsMixin.PortRangeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            protocol: typing.Optional[builtins.str] = None,
            rule_action: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes a rule in a network ACL.

            Each network ACL has a set of numbered ingress rules and a separate set of numbered egress rules. When determining
            whether a packet should be allowed in or out of a subnet associated with the network ACL, AWS processes the entries in the network ACL according to the rule numbers, in ascending order.

            When you manage an individual network ACL, you explicitly specify the rule numbers. When you specify the network ACL rules in a Firewall Manager policy, you provide the rules to run first, in the order that you want them to run, and the rules to run last, in the order that you want them to run. Firewall Manager assigns the rule numbers for you when you save the network ACL policy specification.

            :param cidr_block: The IPv4 network range to allow or deny, in CIDR notation.
            :param egress: Indicates whether the rule is an egress, or outbound, rule (applied to traffic leaving the subnet). If it's not an egress rule, then it's an ingress, or inbound, rule.
            :param icmp_type_code: ICMP protocol: The ICMP type and code.
            :param ipv6_cidr_block: The IPv6 network range to allow or deny, in CIDR notation.
            :param port_range: TCP or UDP protocols: The range of ports the rule applies to.
            :param protocol: The protocol number. A value of "-1" means all protocols.
            :param rule_action: Indicates whether to allow or deny the traffic that matches the rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkaclentry.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fms import mixins as fms_mixins
                
                network_acl_entry_property = fms_mixins.CfnPolicyPropsMixin.NetworkAclEntryProperty(
                    cidr_block="cidrBlock",
                    egress=False,
                    icmp_type_code=fms_mixins.CfnPolicyPropsMixin.IcmpTypeCodeProperty(
                        code=123,
                        type=123
                    ),
                    ipv6_cidr_block="ipv6CidrBlock",
                    port_range=fms_mixins.CfnPolicyPropsMixin.PortRangeProperty(
                        from=123,
                        to=123
                    ),
                    protocol="protocol",
                    rule_action="ruleAction"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9068816134f9e29ee46e2e892c6d323912caf352304f6249794e95254e6f453f)
                check_type(argname="argument cidr_block", value=cidr_block, expected_type=type_hints["cidr_block"])
                check_type(argname="argument egress", value=egress, expected_type=type_hints["egress"])
                check_type(argname="argument icmp_type_code", value=icmp_type_code, expected_type=type_hints["icmp_type_code"])
                check_type(argname="argument ipv6_cidr_block", value=ipv6_cidr_block, expected_type=type_hints["ipv6_cidr_block"])
                check_type(argname="argument port_range", value=port_range, expected_type=type_hints["port_range"])
                check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
                check_type(argname="argument rule_action", value=rule_action, expected_type=type_hints["rule_action"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cidr_block is not None:
                self._values["cidr_block"] = cidr_block
            if egress is not None:
                self._values["egress"] = egress
            if icmp_type_code is not None:
                self._values["icmp_type_code"] = icmp_type_code
            if ipv6_cidr_block is not None:
                self._values["ipv6_cidr_block"] = ipv6_cidr_block
            if port_range is not None:
                self._values["port_range"] = port_range
            if protocol is not None:
                self._values["protocol"] = protocol
            if rule_action is not None:
                self._values["rule_action"] = rule_action

        @builtins.property
        def cidr_block(self) -> typing.Optional[builtins.str]:
            '''The IPv4 network range to allow or deny, in CIDR notation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkaclentry.html#cfn-fms-policy-networkaclentry-cidrblock
            '''
            result = self._values.get("cidr_block")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def egress(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether the rule is an egress, or outbound, rule (applied to traffic leaving the subnet).

            If it's not an egress rule, then it's an ingress, or inbound, rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkaclentry.html#cfn-fms-policy-networkaclentry-egress
            '''
            result = self._values.get("egress")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def icmp_type_code(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyPropsMixin.IcmpTypeCodeProperty"]]:
            '''ICMP protocol: The ICMP type and code.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkaclentry.html#cfn-fms-policy-networkaclentry-icmptypecode
            '''
            result = self._values.get("icmp_type_code")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyPropsMixin.IcmpTypeCodeProperty"]], result)

        @builtins.property
        def ipv6_cidr_block(self) -> typing.Optional[builtins.str]:
            '''The IPv6 network range to allow or deny, in CIDR notation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkaclentry.html#cfn-fms-policy-networkaclentry-ipv6cidrblock
            '''
            result = self._values.get("ipv6_cidr_block")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port_range(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyPropsMixin.PortRangeProperty"]]:
            '''TCP or UDP protocols: The range of ports the rule applies to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkaclentry.html#cfn-fms-policy-networkaclentry-portrange
            '''
            result = self._values.get("port_range")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyPropsMixin.PortRangeProperty"]], result)

        @builtins.property
        def protocol(self) -> typing.Optional[builtins.str]:
            '''The protocol number.

            A value of "-1" means all protocols.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkaclentry.html#cfn-fms-policy-networkaclentry-protocol
            '''
            result = self._values.get("protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def rule_action(self) -> typing.Optional[builtins.str]:
            '''Indicates whether to allow or deny the traffic that matches the rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkaclentry.html#cfn-fms-policy-networkaclentry-ruleaction
            '''
            result = self._values.get("rule_action")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NetworkAclEntryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fms.mixins.CfnPolicyPropsMixin.NetworkAclEntrySetProperty",
        jsii_struct_bases=[],
        name_mapping={
            "first_entries": "firstEntries",
            "force_remediate_for_first_entries": "forceRemediateForFirstEntries",
            "force_remediate_for_last_entries": "forceRemediateForLastEntries",
            "last_entries": "lastEntries",
        },
    )
    class NetworkAclEntrySetProperty:
        def __init__(
            self,
            *,
            first_entries: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPolicyPropsMixin.NetworkAclEntryProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            force_remediate_for_first_entries: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            force_remediate_for_last_entries: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            last_entries: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPolicyPropsMixin.NetworkAclEntryProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The configuration of the first and last rules for the network ACL policy, and the remediation settings for each.

            :param first_entries: The rules that you want to run first in the Firewall Manager managed network ACLs. .. epigraph:: Provide these in the order in which you want them to run. Firewall Manager will assign the specific rule numbers for you, in the network ACLs that it creates. You must specify at least one first entry or one last entry in any network ACL policy.
            :param force_remediate_for_first_entries: Applies only when remediation is enabled for the policy as a whole. Firewall Manager uses this setting when it finds policy violations that involve conflicts between the custom entries and the policy entries. If forced remediation is disabled, Firewall Manager marks the network ACL as noncompliant and does not try to remediate. For more information about the remediation behavior, see `Remediation for managed network ACLs <https://docs.aws.amazon.com/waf/latest/developerguide/network-acl-policies.html#network-acls-remediation>`_ in the *AWS Firewall Manager Developer Guide* .
            :param force_remediate_for_last_entries: Applies only when remediation is enabled for the policy as a whole. Firewall Manager uses this setting when it finds policy violations that involve conflicts between the custom entries and the policy entries. If forced remediation is disabled, Firewall Manager marks the network ACL as noncompliant and does not try to remediate. For more information about the remediation behavior, see `Remediation for managed network ACLs <https://docs.aws.amazon.com/waf/latest/developerguide/network-acl-policies.html#network-acls-remediation>`_ in the *AWS Firewall Manager Developer Guide* .
            :param last_entries: The rules that you want to run last in the Firewall Manager managed network ACLs. .. epigraph:: Provide these in the order in which you want them to run. Firewall Manager will assign the specific rule numbers for you, in the network ACLs that it creates. You must specify at least one first entry or one last entry in any network ACL policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkaclentryset.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fms import mixins as fms_mixins
                
                network_acl_entry_set_property = fms_mixins.CfnPolicyPropsMixin.NetworkAclEntrySetProperty(
                    first_entries=[fms_mixins.CfnPolicyPropsMixin.NetworkAclEntryProperty(
                        cidr_block="cidrBlock",
                        egress=False,
                        icmp_type_code=fms_mixins.CfnPolicyPropsMixin.IcmpTypeCodeProperty(
                            code=123,
                            type=123
                        ),
                        ipv6_cidr_block="ipv6CidrBlock",
                        port_range=fms_mixins.CfnPolicyPropsMixin.PortRangeProperty(
                            from=123,
                            to=123
                        ),
                        protocol="protocol",
                        rule_action="ruleAction"
                    )],
                    force_remediate_for_first_entries=False,
                    force_remediate_for_last_entries=False,
                    last_entries=[fms_mixins.CfnPolicyPropsMixin.NetworkAclEntryProperty(
                        cidr_block="cidrBlock",
                        egress=False,
                        icmp_type_code=fms_mixins.CfnPolicyPropsMixin.IcmpTypeCodeProperty(
                            code=123,
                            type=123
                        ),
                        ipv6_cidr_block="ipv6CidrBlock",
                        port_range=fms_mixins.CfnPolicyPropsMixin.PortRangeProperty(
                            from=123,
                            to=123
                        ),
                        protocol="protocol",
                        rule_action="ruleAction"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c7e19c9aa716835dee3942287ed4d1862555b53107d6a465fd17677bf24c720c)
                check_type(argname="argument first_entries", value=first_entries, expected_type=type_hints["first_entries"])
                check_type(argname="argument force_remediate_for_first_entries", value=force_remediate_for_first_entries, expected_type=type_hints["force_remediate_for_first_entries"])
                check_type(argname="argument force_remediate_for_last_entries", value=force_remediate_for_last_entries, expected_type=type_hints["force_remediate_for_last_entries"])
                check_type(argname="argument last_entries", value=last_entries, expected_type=type_hints["last_entries"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if first_entries is not None:
                self._values["first_entries"] = first_entries
            if force_remediate_for_first_entries is not None:
                self._values["force_remediate_for_first_entries"] = force_remediate_for_first_entries
            if force_remediate_for_last_entries is not None:
                self._values["force_remediate_for_last_entries"] = force_remediate_for_last_entries
            if last_entries is not None:
                self._values["last_entries"] = last_entries

        @builtins.property
        def first_entries(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyPropsMixin.NetworkAclEntryProperty"]]]]:
            '''The rules that you want to run first in the Firewall Manager managed network ACLs.

            .. epigraph::

               Provide these in the order in which you want them to run. Firewall Manager will assign the specific rule numbers for you, in the network ACLs that it creates.

            You must specify at least one first entry or one last entry in any network ACL policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkaclentryset.html#cfn-fms-policy-networkaclentryset-firstentries
            '''
            result = self._values.get("first_entries")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyPropsMixin.NetworkAclEntryProperty"]]]], result)

        @builtins.property
        def force_remediate_for_first_entries(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Applies only when remediation is enabled for the policy as a whole.

            Firewall Manager uses this setting when it finds policy violations that involve conflicts between the custom entries and the policy entries.

            If forced remediation is disabled, Firewall Manager marks the network ACL as noncompliant and does not try to remediate. For more information about the remediation behavior, see `Remediation for managed network ACLs <https://docs.aws.amazon.com/waf/latest/developerguide/network-acl-policies.html#network-acls-remediation>`_ in the *AWS Firewall Manager Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkaclentryset.html#cfn-fms-policy-networkaclentryset-forceremediateforfirstentries
            '''
            result = self._values.get("force_remediate_for_first_entries")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def force_remediate_for_last_entries(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Applies only when remediation is enabled for the policy as a whole.

            Firewall Manager uses this setting when it finds policy violations that involve conflicts between the custom entries and the policy entries.

            If forced remediation is disabled, Firewall Manager marks the network ACL as noncompliant and does not try to remediate. For more information about the remediation behavior, see `Remediation for managed network ACLs <https://docs.aws.amazon.com/waf/latest/developerguide/network-acl-policies.html#network-acls-remediation>`_ in the *AWS Firewall Manager Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkaclentryset.html#cfn-fms-policy-networkaclentryset-forceremediateforlastentries
            '''
            result = self._values.get("force_remediate_for_last_entries")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def last_entries(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyPropsMixin.NetworkAclEntryProperty"]]]]:
            '''The rules that you want to run last in the Firewall Manager managed network ACLs.

            .. epigraph::

               Provide these in the order in which you want them to run. Firewall Manager will assign the specific rule numbers for you, in the network ACLs that it creates.

            You must specify at least one first entry or one last entry in any network ACL policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkaclentryset.html#cfn-fms-policy-networkaclentryset-lastentries
            '''
            result = self._values.get("last_entries")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyPropsMixin.NetworkAclEntryProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NetworkAclEntrySetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fms.mixins.CfnPolicyPropsMixin.NetworkFirewallPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"firewall_deployment_model": "firewallDeploymentModel"},
    )
    class NetworkFirewallPolicyProperty:
        def __init__(
            self,
            *,
            firewall_deployment_model: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configures the firewall policy deployment model of AWS Network Firewall .

            For information about Network Firewall deployment models, see `AWS Network Firewall example architectures with routing <https://docs.aws.amazon.com/network-firewall/latest/developerguide/architectures.html>`_ in the *Network Firewall Developer Guide* .

            :param firewall_deployment_model: Defines the deployment model to use for the firewall policy. To use a distributed model, set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-thirdpartyfirewallpolicy.html>`_ to ``DISTRIBUTED`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fms import mixins as fms_mixins
                
                network_firewall_policy_property = fms_mixins.CfnPolicyPropsMixin.NetworkFirewallPolicyProperty(
                    firewall_deployment_model="firewallDeploymentModel"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cb3a362e375b3e7f849d663507151896eead64651ca8977a4093c30aac1cdfbe)
                check_type(argname="argument firewall_deployment_model", value=firewall_deployment_model, expected_type=type_hints["firewall_deployment_model"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if firewall_deployment_model is not None:
                self._values["firewall_deployment_model"] = firewall_deployment_model

        @builtins.property
        def firewall_deployment_model(self) -> typing.Optional[builtins.str]:
            '''Defines the deployment model to use for the firewall policy.

            To use a distributed model, set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-thirdpartyfirewallpolicy.html>`_ to ``DISTRIBUTED`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html#cfn-fms-policy-networkfirewallpolicy-firewalldeploymentmodel
            '''
            result = self._values.get("firewall_deployment_model")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NetworkFirewallPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fms.mixins.CfnPolicyPropsMixin.PolicyOptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "network_acl_common_policy": "networkAclCommonPolicy",
            "network_firewall_policy": "networkFirewallPolicy",
            "third_party_firewall_policy": "thirdPartyFirewallPolicy",
        },
    )
    class PolicyOptionProperty:
        def __init__(
            self,
            *,
            network_acl_common_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPolicyPropsMixin.NetworkAclCommonPolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            network_firewall_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPolicyPropsMixin.NetworkFirewallPolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            third_party_firewall_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPolicyPropsMixin.ThirdPartyFirewallPolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains the settings to configure a network ACL policy, a AWS Network Firewall firewall policy deployment model, or a third-party firewall policy.

            :param network_acl_common_policy: Defines a Firewall Manager network ACL policy.
            :param network_firewall_policy: Defines the deployment model to use for the firewall policy.
            :param third_party_firewall_policy: Defines the policy options for a third-party firewall policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-policyoption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fms import mixins as fms_mixins
                
                policy_option_property = fms_mixins.CfnPolicyPropsMixin.PolicyOptionProperty(
                    network_acl_common_policy=fms_mixins.CfnPolicyPropsMixin.NetworkAclCommonPolicyProperty(
                        network_acl_entry_set=fms_mixins.CfnPolicyPropsMixin.NetworkAclEntrySetProperty(
                            first_entries=[fms_mixins.CfnPolicyPropsMixin.NetworkAclEntryProperty(
                                cidr_block="cidrBlock",
                                egress=False,
                                icmp_type_code=fms_mixins.CfnPolicyPropsMixin.IcmpTypeCodeProperty(
                                    code=123,
                                    type=123
                                ),
                                ipv6_cidr_block="ipv6CidrBlock",
                                port_range=fms_mixins.CfnPolicyPropsMixin.PortRangeProperty(
                                    from=123,
                                    to=123
                                ),
                                protocol="protocol",
                                rule_action="ruleAction"
                            )],
                            force_remediate_for_first_entries=False,
                            force_remediate_for_last_entries=False,
                            last_entries=[fms_mixins.CfnPolicyPropsMixin.NetworkAclEntryProperty(
                                cidr_block="cidrBlock",
                                egress=False,
                                icmp_type_code=fms_mixins.CfnPolicyPropsMixin.IcmpTypeCodeProperty(
                                    code=123,
                                    type=123
                                ),
                                ipv6_cidr_block="ipv6CidrBlock",
                                port_range=fms_mixins.CfnPolicyPropsMixin.PortRangeProperty(
                                    from=123,
                                    to=123
                                ),
                                protocol="protocol",
                                rule_action="ruleAction"
                            )]
                        )
                    ),
                    network_firewall_policy=fms_mixins.CfnPolicyPropsMixin.NetworkFirewallPolicyProperty(
                        firewall_deployment_model="firewallDeploymentModel"
                    ),
                    third_party_firewall_policy=fms_mixins.CfnPolicyPropsMixin.ThirdPartyFirewallPolicyProperty(
                        firewall_deployment_model="firewallDeploymentModel"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__adc3582121f40f618d997a0cdf177827a31c6770c76ebf57bdda1c4fcdcc1277)
                check_type(argname="argument network_acl_common_policy", value=network_acl_common_policy, expected_type=type_hints["network_acl_common_policy"])
                check_type(argname="argument network_firewall_policy", value=network_firewall_policy, expected_type=type_hints["network_firewall_policy"])
                check_type(argname="argument third_party_firewall_policy", value=third_party_firewall_policy, expected_type=type_hints["third_party_firewall_policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if network_acl_common_policy is not None:
                self._values["network_acl_common_policy"] = network_acl_common_policy
            if network_firewall_policy is not None:
                self._values["network_firewall_policy"] = network_firewall_policy
            if third_party_firewall_policy is not None:
                self._values["third_party_firewall_policy"] = third_party_firewall_policy

        @builtins.property
        def network_acl_common_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyPropsMixin.NetworkAclCommonPolicyProperty"]]:
            '''Defines a Firewall Manager network ACL policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-policyoption.html#cfn-fms-policy-policyoption-networkaclcommonpolicy
            '''
            result = self._values.get("network_acl_common_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyPropsMixin.NetworkAclCommonPolicyProperty"]], result)

        @builtins.property
        def network_firewall_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyPropsMixin.NetworkFirewallPolicyProperty"]]:
            '''Defines the deployment model to use for the firewall policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-policyoption.html#cfn-fms-policy-policyoption-networkfirewallpolicy
            '''
            result = self._values.get("network_firewall_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyPropsMixin.NetworkFirewallPolicyProperty"]], result)

        @builtins.property
        def third_party_firewall_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyPropsMixin.ThirdPartyFirewallPolicyProperty"]]:
            '''Defines the policy options for a third-party firewall policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-policyoption.html#cfn-fms-policy-policyoption-thirdpartyfirewallpolicy
            '''
            result = self._values.get("third_party_firewall_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyPropsMixin.ThirdPartyFirewallPolicyProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PolicyOptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fms.mixins.CfnPolicyPropsMixin.PolicyTagProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class PolicyTagProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A collection of key:value pairs associated with an AWS resource.

            The key:value pair can be anything you define. Typically, the tag key represents a category (such as "environment") and the tag value represents a specific value within that category (such as "test," "development," or "production"). You can add up to 50 tags to each AWS resource.

            :param key: Part of the key:value pair that defines a tag. You can use a tag key to describe a category of information, such as "customer." Tag keys are case-sensitive.
            :param value: Part of the key:value pair that defines a tag. You can use a tag value to describe a specific value within a category, such as "companyA" or "companyB." Tag values are case-sensitive.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-policytag.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fms import mixins as fms_mixins
                
                policy_tag_property = fms_mixins.CfnPolicyPropsMixin.PolicyTagProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__afa7a5585b5952aafbfefaaf6567929d1dc5114b4cfcdb2f31eca65e247d6c9e)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''Part of the key:value pair that defines a tag.

            You can use a tag key to describe a category of information, such as "customer." Tag keys are case-sensitive.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-policytag.html#cfn-fms-policy-policytag-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''Part of the key:value pair that defines a tag.

            You can use a tag value to describe a specific value within a category, such as "companyA" or "companyB." Tag values are case-sensitive.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-policytag.html#cfn-fms-policy-policytag-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PolicyTagProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fms.mixins.CfnPolicyPropsMixin.PortRangeProperty",
        jsii_struct_bases=[],
        name_mapping={"from_": "from", "to": "to"},
    )
    class PortRangeProperty:
        def __init__(
            self,
            *,
            from_: typing.Optional[jsii.Number] = None,
            to: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''TCP or UDP protocols: The range of ports the rule applies to.

            :param from_: The beginning port number of the range.
            :param to: The ending port number of the range.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-portrange.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fms import mixins as fms_mixins
                
                port_range_property = fms_mixins.CfnPolicyPropsMixin.PortRangeProperty(
                    from=123,
                    to=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ab5910ef3f4ee6308ee653c07e0ad4891dfbbd4c1b964d0982dccf7ce1e35b6d)
                check_type(argname="argument from_", value=from_, expected_type=type_hints["from_"])
                check_type(argname="argument to", value=to, expected_type=type_hints["to"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if from_ is not None:
                self._values["from_"] = from_
            if to is not None:
                self._values["to"] = to

        @builtins.property
        def from_(self) -> typing.Optional[jsii.Number]:
            '''The beginning port number of the range.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-portrange.html#cfn-fms-policy-portrange-from
            '''
            result = self._values.get("from_")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def to(self) -> typing.Optional[jsii.Number]:
            '''The ending port number of the range.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-portrange.html#cfn-fms-policy-portrange-to
            '''
            result = self._values.get("to")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PortRangeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fms.mixins.CfnPolicyPropsMixin.ResourceTagProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class ResourceTagProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The resource tags that AWS Firewall Manager uses to determine if a particular resource should be included or excluded from the AWS Firewall Manager policy.

            Tags enable you to categorize your AWS resources in different ways, for example, by purpose, owner, or environment. Each tag consists of a key and an optional value. Firewall Manager combines the tags with "AND" so that, if you add more than one tag to a policy scope, a resource must have all the specified tags to be included or excluded. For more information, see `Working with Tag Editor <https://docs.aws.amazon.com/awsconsolehelpdocs/latest/gsg/tag-editor.html>`_ .

            :param key: The resource tag key.
            :param value: The resource tag value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-resourcetag.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fms import mixins as fms_mixins
                
                resource_tag_property = fms_mixins.CfnPolicyPropsMixin.ResourceTagProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__86f85a3a863d1b83df6ab6b2808acb1eba44cca63e2ce56624618279e838599d)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The resource tag key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-resourcetag.html#cfn-fms-policy-resourcetag-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The resource tag value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-resourcetag.html#cfn-fms-policy-resourcetag-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceTagProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fms.mixins.CfnPolicyPropsMixin.SecurityServicePolicyDataProperty",
        jsii_struct_bases=[],
        name_mapping={
            "managed_service_data": "managedServiceData",
            "policy_option": "policyOption",
            "type": "type",
        },
    )
    class SecurityServicePolicyDataProperty:
        def __init__(
            self,
            *,
            managed_service_data: typing.Optional[builtins.str] = None,
            policy_option: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPolicyPropsMixin.PolicyOptionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Details about the security service that is being used to protect the resources.

            :param managed_service_data: Details about the service that are specific to the service type, in JSON format. - Example: ``DNS_FIREWALL`` ``"{\\"type\\":\\"DNS_FIREWALL\\",\\"preProcessRuleGroups\\":[{\\"ruleGroupId\\":\\"rslvr-frg-1\\",\\"priority\\":10}],\\"postProcessRuleGroups\\":[{\\"ruleGroupId\\":\\"rslvr-frg-2\\",\\"priority\\":9911}]}"`` .. epigraph:: Valid values for ``preProcessRuleGroups`` are between 1 and 99. Valid values for ``postProcessRuleGroups`` are between 9901 and 10000. - Example: ``NETWORK_FIREWALL`` - Centralized deployment model ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"awsNetworkFirewallConfig\\":{\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":true}},\\"firewallDeploymentModel\\":{\\"centralizedFirewallDeploymentModel\\":{\\"centralizedFirewallOrchestrationConfig\\":{\\"inspectionVpcIds\\":[{\\"resourceId\\":\\"vpc-1234\\",\\"accountId\\":\\"123456789011\\"}],\\"firewallCreationConfig\\":{\\"endpointLocation\\":{\\"availabilityZoneConfigList\\":[{\\"availabilityZoneId\\":null,\\"availabilityZoneName\\":\\"us-east-1a\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]}]}},\\"allowedIPV4CidrList\\":[]}}}}"`` To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` . - Example: ``NETWORK_FIREWALL`` - Distributed deployment model with automatic Availability Zone configuration ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallOrchestrationConfig\\":{\\"singleFirewallEndpointPerVPC\\":false,\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\",\\"192.168.0.0/28\\"],\\"routeManagementAction\\":\\"OFF\\"},\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":true}}"`` With automatic Availbility Zone configuration, Firewall Manager chooses which Availability Zones to create the endpoints in. To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` . - Example: ``NETWORK_FIREWALL`` - Distributed deployment model with automatic Availability Zone configuration and route management ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallOrchestrationConfig\\":{\\"singleFirewallEndpointPerVPC\\":false,\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\",\\"192.168.0.0/28\\"],\\"routeManagementAction\\":\\"MONITOR\\",\\"routeManagementTargetTypes\\":[\\"InternetGateway\\"]},\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\": \\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":true}}"`` To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` . - Example: ``NETWORK_FIREWALL`` - Distributed deployment model with custom Availability Zone configuration ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"fragmentcustomactionname\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\", \\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}},{\\"actionName\\":\\"fragmentcustomactionname\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"fragmentmetricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallOrchestrationConfig\\":{\\"firewallCreationConfig\\":{ \\"endpointLocation\\":{\\"availabilityZoneConfigList\\":[{\\"availabilityZoneName\\":\\"us-east-1a\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]},{\\"availabilityZoneName\\":\\"us-east-1b\\",\\"allowedIPV4CidrList\\":[ \\"10.0.0.0/28\\"]}]} },\\"singleFirewallEndpointPerVPC\\":false,\\"allowedIPV4CidrList\\":null,\\"routeManagementAction\\":\\"OFF\\",\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":boolean}}"`` With custom Availability Zone configuration, you define which specific Availability Zones to create endpoints in by configuring ``firewallCreationConfig`` . To configure the Availability Zones in ``firewallCreationConfig`` , specify either the ``availabilityZoneName`` or ``availabilityZoneId`` parameter, not both parameters. To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` . - Example: ``NETWORK_FIREWALL`` - Distributed deployment model with custom Availability Zone configuration and route management ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"fragmentcustomactionname\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}},{\\"actionName\\":\\"fragmentcustomactionname\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"fragmentmetricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallOrchestrationConfig\\":{\\"firewallCreationConfig\\":{\\"endpointLocation\\":{\\"availabilityZoneConfigList\\":[{\\"availabilityZoneName\\":\\"us-east-1a\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]},{\\"availabilityZoneName\\":\\"us-east-1b\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]}]}},\\"singleFirewallEndpointPerVPC\\":false,\\"allowedIPV4CidrList\\":null,\\"routeManagementAction\\":\\"MONITOR\\",\\"routeManagementTargetTypes\\":[\\"InternetGateway\\"],\\"routeManagementConfig\\":{\\"allowCrossAZTrafficIfNoEndpoint\\":true}},\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":boolean}}"`` To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` . - Example: ``THIRD_PARTY_FIREWALL`` - Palo Alto Networks Cloud Next-Generation Firewall centralized deployment model ``"{ \\"type\\":\\"THIRD_PARTY_FIREWALL\\", \\"thirdPartyFirewall\\":\\"PALO_ALTO_NETWORKS_CLOUD_NGFW\\", \\"thirdPartyFirewallConfig\\":{ \\"thirdPartyFirewallPolicyList\\":[\\"global-1\\"] },\\"firewallDeploymentModel\\":{\\"centralizedFirewallDeploymentModel\\":{\\"centralizedFirewallOrchestrationConfig\\":{\\"inspectionVpcIds\\":[{\\"resourceId\\":\\"vpc-1234\\",\\"accountId\\":\\"123456789011\\"}],\\"firewallCreationConfig\\":{\\"endpointLocation\\":{\\"availabilityZoneConfigList\\":[{\\"availabilityZoneId\\":null,\\"availabilityZoneName\\":\\"us-east-1a\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]}]}},\\"allowedIPV4CidrList\\":[]}}}}"`` To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-thirdpartyfirewallpolicy.html>`_ to ``CENTRALIZED`` . - Example: ``THIRD_PARTY_FIREWALL`` - Palo Alto Networks Cloud Next-Generation Firewall distributed deployment model ``"{\\"type\\":\\"THIRD_PARTY_FIREWALL\\",\\"thirdPartyFirewall\\":\\"PALO_ALTO_NETWORKS_CLOUD_NGFW\\",\\"thirdPartyFirewallConfig\\":{\\"thirdPartyFirewallPolicyList\\":[\\"global-1\\"] },\\"firewallDeploymentModel\\":{ \\"distributedFirewallDeploymentModel\\":{ \\"distributedFirewallOrchestrationConfig\\":{\\"firewallCreationConfig\\":{\\"endpointLocation\\":{ \\"availabilityZoneConfigList\\":[ {\\"availabilityZoneName\\":\\"${AvailabilityZone}\\" } ] } }, \\"allowedIPV4CidrList\\":[ ] } } } }"`` To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-thirdpartyfirewallpolicy.html>`_ to ``DISTRIBUTED`` . - Specification for ``SHIELD_ADVANCED`` for Amazon CloudFront distributions ``"{\\"type\\":\\"SHIELD_ADVANCED\\",\\"automaticResponseConfiguration\\": {\\"automaticResponseStatus\\":\\"ENABLED|IGNORED|DISABLED\\", \\"automaticResponseAction\\":\\"BLOCK|COUNT\\"}, \\"overrideCustomerWebaclClassic\\":true|false}"`` For example: ``"{\\"type\\":\\"SHIELD_ADVANCED\\",\\"automaticResponseConfiguration\\": {\\"automaticResponseStatus\\":\\"ENABLED\\", \\"automaticResponseAction\\":\\"COUNT\\"}}"`` The default value for ``automaticResponseStatus`` is ``IGNORED`` . The value for ``automaticResponseAction`` is only required when ``automaticResponseStatus`` is set to ``ENABLED`` . The default value for ``overrideCustomerWebaclClassic`` is ``false`` . For other resource types that you can protect with a Shield Advanced policy, this ``ManagedServiceData`` configuration is an empty string. - Example: ``WAFV2`` ``"{\\"type\\":\\"WAFV2\\",\\"preProcessRuleGroups\\":[{\\"ruleGroupArn\\":null,\\"overrideAction\\":{\\"type\\":\\"NONE\\"},\\"managedRuleGroupIdentifier\\":{\\"version\\":null,\\"vendorName\\":\\"AWS\\",\\"managedRuleGroupName\\":\\"AWSManagedRulesAmazonIpReputationList\\"},\\"ruleGroupType\\":\\"ManagedRuleGroup\\",\\"excludeRules\\":[{\\"name\\":\\"NoUserAgent_HEADER\\"}]}],\\"postProcessRuleGroups\\":[],\\"defaultAction\\":{\\"type\\":\\"ALLOW\\"},\\"overrideCustomerWebACLAssociation\\":false,\\"loggingConfiguration\\":{\\"logDestinationConfigs\\":[\\"arn:aws:firehose:us-west-2:12345678912:deliverystream/aws-waf-logs-fms-admin-destination\\"],\\"redactedFields\\":[{\\"redactedFieldType\\":\\"SingleHeader\\",\\"redactedFieldValue\\":\\"Cookies\\"},{\\"redactedFieldType\\":\\"Method\\"}]}}"`` In the ``loggingConfiguration`` , you can specify one ``logDestinationConfigs`` , you can optionally provide up to 20 ``redactedFields`` , and the ``RedactedFieldType`` must be one of ``URI`` , ``QUERY_STRING`` , ``HEADER`` , or ``METHOD`` . - Example: ``AWS WAF Classic`` ``"{\\"type\\": \\"WAF\\", \\"ruleGroups\\": [{\\"id\\":\\"12345678-1bcd-9012-efga-0987654321ab\\", \\"overrideAction\\" : {\\"type\\": \\"COUNT\\"}}], \\"defaultAction\\": {\\"type\\": \\"BLOCK\\"}}"`` - Example: ``WAFV2`` - AWS Firewall Manager support for AWS WAF managed rule group versioning ``"{\\"type\\":\\"WAFV2\\",\\"preProcessRuleGroups\\":[{\\"ruleGroupArn\\":null,\\"overrideAction\\":{\\"type\\":\\"NONE\\"},\\"managedRuleGroupIdentifier\\":{\\"versionEnabled\\":true,\\"version\\":\\"Version_2.0\\",\\"vendorName\\":\\"AWS\\",\\"managedRuleGroupName\\":\\"AWSManagedRulesCommonRuleSet\\"},\\"ruleGroupType\\":\\"ManagedRuleGroup\\",\\"excludeRules\\":[{\\"name\\":\\"NoUserAgent_HEADER\\"}]}],\\"postProcessRuleGroups\\":[],\\"defaultAction\\":{\\"type\\":\\"ALLOW\\"},\\"overrideCustomerWebACLAssociation\\":false,\\"loggingConfiguration\\":{\\"logDestinationConfigs\\":[\\"arn:aws:firehose:us-west-2:12345678912:deliverystream/aws-waf-logs-fms-admin-destination\\"],\\"redactedFields\\":[{\\"redactedFieldType\\":\\"SingleHeader\\",\\"redactedFieldValue\\":\\"Cookies\\"},{\\"redactedFieldType\\":\\"Method\\"}]}}"`` To use a specific version of a AWS WAF managed rule group in your Firewall Manager policy, you must set ``versionEnabled`` to ``true`` , and set ``version`` to the version you'd like to use. If you don't set ``versionEnabled`` to ``true`` , or if you omit ``versionEnabled`` , then Firewall Manager uses the default version of the AWS WAF managed rule group. - Example: ``SECURITY_GROUPS_COMMON`` ``"{\\"type\\":\\"SECURITY_GROUPS_COMMON\\",\\"revertManualSecurityGroupChanges\\":false,\\"exclusiveResourceSecurityGroupManagement\\":false, \\"applyToAllEC2InstanceENIs\\":false,\\"securityGroups\\":[{\\"id\\":\\" sg-000e55995d61a06bd\\"}]}"`` - Example: Shared VPCs. Apply the preceding policy to resources in shared VPCs as well as to those in VPCs that the account owns ``"{\\"type\\":\\"SECURITY_GROUPS_COMMON\\",\\"revertManualSecurityGroupChanges\\":false,\\"exclusiveResourceSecurityGroupManagement\\":false, \\"applyToAllEC2InstanceENIs\\":false,\\"includeSharedVPC\\":true,\\"securityGroups\\":[{\\"id\\":\\" sg-000e55995d61a06bd\\"}]}"`` - Example: ``SECURITY_GROUPS_CONTENT_AUDIT`` ``"{\\"type\\":\\"SECURITY_GROUPS_CONTENT_AUDIT\\",\\"securityGroups\\":[{\\"id\\":\\"sg-000e55995d61a06bd\\"}],\\"securityGroupAction\\":{\\"type\\":\\"ALLOW\\"}}"`` The security group action for content audit can be ``ALLOW`` or ``DENY`` . For ``ALLOW`` , all in-scope security group rules must be within the allowed range of the policy's security group rules. For ``DENY`` , all in-scope security group rules must not contain a value or a range that matches a rule value or range in the policy security group. - Example: ``SECURITY_GROUPS_USAGE_AUDIT`` ``"{\\"type\\":\\"SECURITY_GROUPS_USAGE_AUDIT\\",\\"deleteUnusedSecurityGroups\\":true,\\"coalesceRedundantSecurityGroups\\":true}"``
            :param policy_option: Contains the settings to configure a network ACL policy, a AWS Network Firewall firewall policy deployment model, or a third-party firewall policy.
            :param type: The service that the policy is using to protect the resources. This specifies the type of policy that is created, either an AWS WAF policy, a Shield Advanced policy, or a security group policy. For security group policies, Firewall Manager supports one security group for each common policy and for each content audit policy. This is an adjustable limit that you can increase by contacting SUPlong .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-securityservicepolicydata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fms import mixins as fms_mixins
                
                security_service_policy_data_property = fms_mixins.CfnPolicyPropsMixin.SecurityServicePolicyDataProperty(
                    managed_service_data="managedServiceData",
                    policy_option=fms_mixins.CfnPolicyPropsMixin.PolicyOptionProperty(
                        network_acl_common_policy=fms_mixins.CfnPolicyPropsMixin.NetworkAclCommonPolicyProperty(
                            network_acl_entry_set=fms_mixins.CfnPolicyPropsMixin.NetworkAclEntrySetProperty(
                                first_entries=[fms_mixins.CfnPolicyPropsMixin.NetworkAclEntryProperty(
                                    cidr_block="cidrBlock",
                                    egress=False,
                                    icmp_type_code=fms_mixins.CfnPolicyPropsMixin.IcmpTypeCodeProperty(
                                        code=123,
                                        type=123
                                    ),
                                    ipv6_cidr_block="ipv6CidrBlock",
                                    port_range=fms_mixins.CfnPolicyPropsMixin.PortRangeProperty(
                                        from=123,
                                        to=123
                                    ),
                                    protocol="protocol",
                                    rule_action="ruleAction"
                                )],
                                force_remediate_for_first_entries=False,
                                force_remediate_for_last_entries=False,
                                last_entries=[fms_mixins.CfnPolicyPropsMixin.NetworkAclEntryProperty(
                                    cidr_block="cidrBlock",
                                    egress=False,
                                    icmp_type_code=fms_mixins.CfnPolicyPropsMixin.IcmpTypeCodeProperty(
                                        code=123,
                                        type=123
                                    ),
                                    ipv6_cidr_block="ipv6CidrBlock",
                                    port_range=fms_mixins.CfnPolicyPropsMixin.PortRangeProperty(
                                        from=123,
                                        to=123
                                    ),
                                    protocol="protocol",
                                    rule_action="ruleAction"
                                )]
                            )
                        ),
                        network_firewall_policy=fms_mixins.CfnPolicyPropsMixin.NetworkFirewallPolicyProperty(
                            firewall_deployment_model="firewallDeploymentModel"
                        ),
                        third_party_firewall_policy=fms_mixins.CfnPolicyPropsMixin.ThirdPartyFirewallPolicyProperty(
                            firewall_deployment_model="firewallDeploymentModel"
                        )
                    ),
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__65a2ed89e9f554d53101c30521cc5e2c76dbac0d783e94fbe53750ea77de2be7)
                check_type(argname="argument managed_service_data", value=managed_service_data, expected_type=type_hints["managed_service_data"])
                check_type(argname="argument policy_option", value=policy_option, expected_type=type_hints["policy_option"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if managed_service_data is not None:
                self._values["managed_service_data"] = managed_service_data
            if policy_option is not None:
                self._values["policy_option"] = policy_option
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def managed_service_data(self) -> typing.Optional[builtins.str]:
            '''Details about the service that are specific to the service type, in JSON format.

            - Example: ``DNS_FIREWALL``

            ``"{\\"type\\":\\"DNS_FIREWALL\\",\\"preProcessRuleGroups\\":[{\\"ruleGroupId\\":\\"rslvr-frg-1\\",\\"priority\\":10}],\\"postProcessRuleGroups\\":[{\\"ruleGroupId\\":\\"rslvr-frg-2\\",\\"priority\\":9911}]}"``
            .. epigraph::

               Valid values for ``preProcessRuleGroups`` are between 1 and 99. Valid values for ``postProcessRuleGroups`` are between 9901 and 10000.

            - Example: ``NETWORK_FIREWALL`` - Centralized deployment model

            ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"awsNetworkFirewallConfig\\":{\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":true}},\\"firewallDeploymentModel\\":{\\"centralizedFirewallDeploymentModel\\":{\\"centralizedFirewallOrchestrationConfig\\":{\\"inspectionVpcIds\\":[{\\"resourceId\\":\\"vpc-1234\\",\\"accountId\\":\\"123456789011\\"}],\\"firewallCreationConfig\\":{\\"endpointLocation\\":{\\"availabilityZoneConfigList\\":[{\\"availabilityZoneId\\":null,\\"availabilityZoneName\\":\\"us-east-1a\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]}]}},\\"allowedIPV4CidrList\\":[]}}}}"``

            To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` .

            - Example: ``NETWORK_FIREWALL`` - Distributed deployment model with automatic Availability Zone configuration

            ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallOrchestrationConfig\\":{\\"singleFirewallEndpointPerVPC\\":false,\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\",\\"192.168.0.0/28\\"],\\"routeManagementAction\\":\\"OFF\\"},\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":true}}"``

            With automatic Availbility Zone configuration, Firewall Manager chooses which Availability Zones to create the endpoints in. To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` .

            - Example: ``NETWORK_FIREWALL`` - Distributed deployment model with automatic Availability Zone configuration and route management

            ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallOrchestrationConfig\\":{\\"singleFirewallEndpointPerVPC\\":false,\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\",\\"192.168.0.0/28\\"],\\"routeManagementAction\\":\\"MONITOR\\",\\"routeManagementTargetTypes\\":[\\"InternetGateway\\"]},\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\": \\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":true}}"``

            To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` .

            - Example: ``NETWORK_FIREWALL`` - Distributed deployment model with custom Availability Zone configuration

            ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"fragmentcustomactionname\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\", \\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}},{\\"actionName\\":\\"fragmentcustomactionname\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"fragmentmetricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallOrchestrationConfig\\":{\\"firewallCreationConfig\\":{ \\"endpointLocation\\":{\\"availabilityZoneConfigList\\":[{\\"availabilityZoneName\\":\\"us-east-1a\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]},{\\"availabilityZoneName\\":\\"us-east-1b\\",\\"allowedIPV4CidrList\\":[ \\"10.0.0.0/28\\"]}]} },\\"singleFirewallEndpointPerVPC\\":false,\\"allowedIPV4CidrList\\":null,\\"routeManagementAction\\":\\"OFF\\",\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":boolean}}"``

            With custom Availability Zone configuration, you define which specific Availability Zones to create endpoints in by configuring ``firewallCreationConfig`` . To configure the Availability Zones in ``firewallCreationConfig`` , specify either the ``availabilityZoneName`` or ``availabilityZoneId`` parameter, not both parameters.

            To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` .

            - Example: ``NETWORK_FIREWALL`` - Distributed deployment model with custom Availability Zone configuration and route management

            ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"fragmentcustomactionname\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}},{\\"actionName\\":\\"fragmentcustomactionname\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"fragmentmetricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallOrchestrationConfig\\":{\\"firewallCreationConfig\\":{\\"endpointLocation\\":{\\"availabilityZoneConfigList\\":[{\\"availabilityZoneName\\":\\"us-east-1a\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]},{\\"availabilityZoneName\\":\\"us-east-1b\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]}]}},\\"singleFirewallEndpointPerVPC\\":false,\\"allowedIPV4CidrList\\":null,\\"routeManagementAction\\":\\"MONITOR\\",\\"routeManagementTargetTypes\\":[\\"InternetGateway\\"],\\"routeManagementConfig\\":{\\"allowCrossAZTrafficIfNoEndpoint\\":true}},\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":boolean}}"``

            To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` .

            - Example: ``THIRD_PARTY_FIREWALL`` - Palo Alto Networks Cloud Next-Generation Firewall centralized deployment model

            ``"{ \\"type\\":\\"THIRD_PARTY_FIREWALL\\", \\"thirdPartyFirewall\\":\\"PALO_ALTO_NETWORKS_CLOUD_NGFW\\", \\"thirdPartyFirewallConfig\\":{ \\"thirdPartyFirewallPolicyList\\":[\\"global-1\\"] },\\"firewallDeploymentModel\\":{\\"centralizedFirewallDeploymentModel\\":{\\"centralizedFirewallOrchestrationConfig\\":{\\"inspectionVpcIds\\":[{\\"resourceId\\":\\"vpc-1234\\",\\"accountId\\":\\"123456789011\\"}],\\"firewallCreationConfig\\":{\\"endpointLocation\\":{\\"availabilityZoneConfigList\\":[{\\"availabilityZoneId\\":null,\\"availabilityZoneName\\":\\"us-east-1a\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]}]}},\\"allowedIPV4CidrList\\":[]}}}}"``

            To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-thirdpartyfirewallpolicy.html>`_ to ``CENTRALIZED`` .

            - Example: ``THIRD_PARTY_FIREWALL`` - Palo Alto Networks Cloud Next-Generation Firewall distributed deployment model

            ``"{\\"type\\":\\"THIRD_PARTY_FIREWALL\\",\\"thirdPartyFirewall\\":\\"PALO_ALTO_NETWORKS_CLOUD_NGFW\\",\\"thirdPartyFirewallConfig\\":{\\"thirdPartyFirewallPolicyList\\":[\\"global-1\\"] },\\"firewallDeploymentModel\\":{ \\"distributedFirewallDeploymentModel\\":{ \\"distributedFirewallOrchestrationConfig\\":{\\"firewallCreationConfig\\":{\\"endpointLocation\\":{ \\"availabilityZoneConfigList\\":[ {\\"availabilityZoneName\\":\\"${AvailabilityZone}\\" } ] } }, \\"allowedIPV4CidrList\\":[ ] } } } }"``

            To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-thirdpartyfirewallpolicy.html>`_ to ``DISTRIBUTED`` .

            - Specification for ``SHIELD_ADVANCED`` for Amazon CloudFront distributions

            ``"{\\"type\\":\\"SHIELD_ADVANCED\\",\\"automaticResponseConfiguration\\": {\\"automaticResponseStatus\\":\\"ENABLED|IGNORED|DISABLED\\", \\"automaticResponseAction\\":\\"BLOCK|COUNT\\"}, \\"overrideCustomerWebaclClassic\\":true|false}"``

            For example: ``"{\\"type\\":\\"SHIELD_ADVANCED\\",\\"automaticResponseConfiguration\\": {\\"automaticResponseStatus\\":\\"ENABLED\\", \\"automaticResponseAction\\":\\"COUNT\\"}}"``

            The default value for ``automaticResponseStatus`` is ``IGNORED`` . The value for ``automaticResponseAction`` is only required when ``automaticResponseStatus`` is set to ``ENABLED`` . The default value for ``overrideCustomerWebaclClassic`` is ``false`` .

            For other resource types that you can protect with a Shield Advanced policy, this ``ManagedServiceData`` configuration is an empty string.

            - Example: ``WAFV2``

            ``"{\\"type\\":\\"WAFV2\\",\\"preProcessRuleGroups\\":[{\\"ruleGroupArn\\":null,\\"overrideAction\\":{\\"type\\":\\"NONE\\"},\\"managedRuleGroupIdentifier\\":{\\"version\\":null,\\"vendorName\\":\\"AWS\\",\\"managedRuleGroupName\\":\\"AWSManagedRulesAmazonIpReputationList\\"},\\"ruleGroupType\\":\\"ManagedRuleGroup\\",\\"excludeRules\\":[{\\"name\\":\\"NoUserAgent_HEADER\\"}]}],\\"postProcessRuleGroups\\":[],\\"defaultAction\\":{\\"type\\":\\"ALLOW\\"},\\"overrideCustomerWebACLAssociation\\":false,\\"loggingConfiguration\\":{\\"logDestinationConfigs\\":[\\"arn:aws:firehose:us-west-2:12345678912:deliverystream/aws-waf-logs-fms-admin-destination\\"],\\"redactedFields\\":[{\\"redactedFieldType\\":\\"SingleHeader\\",\\"redactedFieldValue\\":\\"Cookies\\"},{\\"redactedFieldType\\":\\"Method\\"}]}}"``

            In the ``loggingConfiguration`` , you can specify one ``logDestinationConfigs`` , you can optionally provide up to 20 ``redactedFields`` , and the ``RedactedFieldType`` must be one of ``URI`` , ``QUERY_STRING`` , ``HEADER`` , or ``METHOD`` .

            - Example: ``AWS WAF Classic``

            ``"{\\"type\\": \\"WAF\\", \\"ruleGroups\\": [{\\"id\\":\\"12345678-1bcd-9012-efga-0987654321ab\\", \\"overrideAction\\" : {\\"type\\": \\"COUNT\\"}}], \\"defaultAction\\": {\\"type\\": \\"BLOCK\\"}}"``

            - Example: ``WAFV2`` - AWS Firewall Manager support for AWS WAF managed rule group versioning

            ``"{\\"type\\":\\"WAFV2\\",\\"preProcessRuleGroups\\":[{\\"ruleGroupArn\\":null,\\"overrideAction\\":{\\"type\\":\\"NONE\\"},\\"managedRuleGroupIdentifier\\":{\\"versionEnabled\\":true,\\"version\\":\\"Version_2.0\\",\\"vendorName\\":\\"AWS\\",\\"managedRuleGroupName\\":\\"AWSManagedRulesCommonRuleSet\\"},\\"ruleGroupType\\":\\"ManagedRuleGroup\\",\\"excludeRules\\":[{\\"name\\":\\"NoUserAgent_HEADER\\"}]}],\\"postProcessRuleGroups\\":[],\\"defaultAction\\":{\\"type\\":\\"ALLOW\\"},\\"overrideCustomerWebACLAssociation\\":false,\\"loggingConfiguration\\":{\\"logDestinationConfigs\\":[\\"arn:aws:firehose:us-west-2:12345678912:deliverystream/aws-waf-logs-fms-admin-destination\\"],\\"redactedFields\\":[{\\"redactedFieldType\\":\\"SingleHeader\\",\\"redactedFieldValue\\":\\"Cookies\\"},{\\"redactedFieldType\\":\\"Method\\"}]}}"``

            To use a specific version of a AWS WAF managed rule group in your Firewall Manager policy, you must set ``versionEnabled`` to ``true`` , and set ``version`` to the version you'd like to use. If you don't set ``versionEnabled`` to ``true`` , or if you omit ``versionEnabled`` , then Firewall Manager uses the default version of the AWS WAF managed rule group.

            - Example: ``SECURITY_GROUPS_COMMON``

            ``"{\\"type\\":\\"SECURITY_GROUPS_COMMON\\",\\"revertManualSecurityGroupChanges\\":false,\\"exclusiveResourceSecurityGroupManagement\\":false, \\"applyToAllEC2InstanceENIs\\":false,\\"securityGroups\\":[{\\"id\\":\\" sg-000e55995d61a06bd\\"}]}"``

            - Example: Shared VPCs. Apply the preceding policy to resources in shared VPCs as well as to those in VPCs that the account owns

            ``"{\\"type\\":\\"SECURITY_GROUPS_COMMON\\",\\"revertManualSecurityGroupChanges\\":false,\\"exclusiveResourceSecurityGroupManagement\\":false, \\"applyToAllEC2InstanceENIs\\":false,\\"includeSharedVPC\\":true,\\"securityGroups\\":[{\\"id\\":\\" sg-000e55995d61a06bd\\"}]}"``

            - Example: ``SECURITY_GROUPS_CONTENT_AUDIT``

            ``"{\\"type\\":\\"SECURITY_GROUPS_CONTENT_AUDIT\\",\\"securityGroups\\":[{\\"id\\":\\"sg-000e55995d61a06bd\\"}],\\"securityGroupAction\\":{\\"type\\":\\"ALLOW\\"}}"``

            The security group action for content audit can be ``ALLOW`` or ``DENY`` . For ``ALLOW`` , all in-scope security group rules must be within the allowed range of the policy's security group rules. For ``DENY`` , all in-scope security group rules must not contain a value or a range that matches a rule value or range in the policy security group.

            - Example: ``SECURITY_GROUPS_USAGE_AUDIT``

            ``"{\\"type\\":\\"SECURITY_GROUPS_USAGE_AUDIT\\",\\"deleteUnusedSecurityGroups\\":true,\\"coalesceRedundantSecurityGroups\\":true}"``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-securityservicepolicydata.html#cfn-fms-policy-securityservicepolicydata-managedservicedata
            '''
            result = self._values.get("managed_service_data")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def policy_option(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyPropsMixin.PolicyOptionProperty"]]:
            '''Contains the settings to configure a network ACL policy, a AWS Network Firewall firewall policy deployment model, or a third-party firewall policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-securityservicepolicydata.html#cfn-fms-policy-securityservicepolicydata-policyoption
            '''
            result = self._values.get("policy_option")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyPropsMixin.PolicyOptionProperty"]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The service that the policy is using to protect the resources.

            This specifies the type of policy that is created, either an AWS WAF policy, a Shield Advanced policy, or a security group policy. For security group policies, Firewall Manager supports one security group for each common policy and for each content audit policy. This is an adjustable limit that you can increase by contacting SUPlong .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-securityservicepolicydata.html#cfn-fms-policy-securityservicepolicydata-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SecurityServicePolicyDataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fms.mixins.CfnPolicyPropsMixin.ThirdPartyFirewallPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"firewall_deployment_model": "firewallDeploymentModel"},
    )
    class ThirdPartyFirewallPolicyProperty:
        def __init__(
            self,
            *,
            firewall_deployment_model: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configures the deployment model for the third-party firewall.

            :param firewall_deployment_model: Defines the deployment model to use for the third-party firewall policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-thirdpartyfirewallpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fms import mixins as fms_mixins
                
                third_party_firewall_policy_property = fms_mixins.CfnPolicyPropsMixin.ThirdPartyFirewallPolicyProperty(
                    firewall_deployment_model="firewallDeploymentModel"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5b9788b5d5638bc721f212013d9405d822ad9d356393ab9fd09ab880b0c80182)
                check_type(argname="argument firewall_deployment_model", value=firewall_deployment_model, expected_type=type_hints["firewall_deployment_model"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if firewall_deployment_model is not None:
                self._values["firewall_deployment_model"] = firewall_deployment_model

        @builtins.property
        def firewall_deployment_model(self) -> typing.Optional[builtins.str]:
            '''Defines the deployment model to use for the third-party firewall policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-thirdpartyfirewallpolicy.html#cfn-fms-policy-thirdpartyfirewallpolicy-firewalldeploymentmodel
            '''
            result = self._values.get("firewall_deployment_model")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ThirdPartyFirewallPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_fms.mixins.CfnResourceSetMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "name": "name",
        "resources": "resources",
        "resource_type_list": "resourceTypeList",
        "tags": "tags",
    },
)
class CfnResourceSetMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        resource_type_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnResourceSetPropsMixin.

        :param description: A description of the resource set.
        :param name: The descriptive name of the resource set. You can't change the name of a resource set after you create it.
        :param resources: 
        :param resource_type_list: Determines the resources that can be associated to the resource set. Depending on your setting for max results and the number of resource sets, a single call might not return the full list.
        :param tags: 

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-resourceset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_fms import mixins as fms_mixins
            
            cfn_resource_set_mixin_props = fms_mixins.CfnResourceSetMixinProps(
                description="description",
                name="name",
                resources=["resources"],
                resource_type_list=["resourceTypeList"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97aa6cbfae4f077a1b17cfb876ad0849ac857c101e08b59e8c74972e16e74594)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            check_type(argname="argument resource_type_list", value=resource_type_list, expected_type=type_hints["resource_type_list"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if resources is not None:
            self._values["resources"] = resources
        if resource_type_list is not None:
            self._values["resource_type_list"] = resource_type_list
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the resource set.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-resourceset.html#cfn-fms-resourceset-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The descriptive name of the resource set.

        You can't change the name of a resource set after you create it.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-resourceset.html#cfn-fms-resourceset-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-resourceset.html#cfn-fms-resourceset-resources
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def resource_type_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Determines the resources that can be associated to the resource set.

        Depending on your setting for max results and the number of resource sets, a single call might not return the full list.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-resourceset.html#cfn-fms-resourceset-resourcetypelist
        '''
        result = self._values.get("resource_type_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-resourceset.html#cfn-fms-resourceset-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourceSetMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnResourceSetPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_fms.mixins.CfnResourceSetPropsMixin",
):
    '''A set of resources to include in a policy.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-resourceset.html
    :cloudformationResource: AWS::FMS::ResourceSet
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_fms import mixins as fms_mixins
        
        cfn_resource_set_props_mixin = fms_mixins.CfnResourceSetPropsMixin(fms_mixins.CfnResourceSetMixinProps(
            description="description",
            name="name",
            resources=["resources"],
            resource_type_list=["resourceTypeList"],
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
        props: typing.Union[CfnResourceSetMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::FMS::ResourceSet``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b7f7b57c890e9d1385242ce74ff038593cf85693a32d4ff6d7a6fd74cbe0874)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9df803251d9d21d08363559d151f64e7e7c9cb3489320fc7b223287ea7140455)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dece693b1b30d2c4d59f39c41208a4bed5b7f75430336b7faf67d6cbada8bb12)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnResourceSetMixinProps:
        return typing.cast(CfnResourceSetMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnNotificationChannelMixinProps",
    "CfnNotificationChannelPropsMixin",
    "CfnPolicyMixinProps",
    "CfnPolicyPropsMixin",
    "CfnResourceSetMixinProps",
    "CfnResourceSetPropsMixin",
]

publication.publish()

def _typecheckingstub__8adc25437ea2a35fbd61994baf429d178b007c5da9eff3ce96c4f5f326517816(
    *,
    sns_role_name: typing.Optional[builtins.str] = None,
    sns_topic_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2657260abfdfd973e047458724e7e52c9b15cf6f46657d656f79a5ddfc1b9271(
    props: typing.Union[CfnNotificationChannelMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d174e5c0c2c5ab6845ce2f49ddad1fec5cd59d5460006ffad80a79951c63f11a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__373940a19e5444b0cdf7803ee7a486506926be0994ee58dba172062b075b9a96(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d64da381ce3dece9f4cc9562b4eca4c433c1dd2ee75de9d445baa07aa9c513e(
    *,
    delete_all_policy_resources: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    exclude_map: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPolicyPropsMixin.IEMapProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    exclude_resource_tags: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    include_map: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPolicyPropsMixin.IEMapProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    policy_description: typing.Optional[builtins.str] = None,
    policy_name: typing.Optional[builtins.str] = None,
    remediation_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    resources_clean_up: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    resource_set_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_tag_logical_operator: typing.Optional[builtins.str] = None,
    resource_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPolicyPropsMixin.ResourceTagProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resource_type: typing.Optional[builtins.str] = None,
    resource_type_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    security_service_policy_data: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPolicyPropsMixin.SecurityServicePolicyDataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnPolicyPropsMixin.PolicyTagProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f1987207e12dde62cf379bb2739f25551cef507c75f6129a5341da10bcffb75(
    props: typing.Union[CfnPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dcf9cf0343a3ae68b5bac4252c7d8b6eba98a67102a05bf192ded521b04d731(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__826efa27110674dc325a352e4d5e8fe72dde51cbe246300e3395875609ac98fe(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d86b0b120942b5f38e8304a1793cfd6a283aad4c81c9cf15a20a24dc33ae1ee(
    *,
    account: typing.Optional[typing.Sequence[builtins.str]] = None,
    orgunit: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef758e1d3ae927eaaa052c2b92b1fa3a4f8a71e8996c717f10bdc7727aa82ea9(
    *,
    code: typing.Optional[jsii.Number] = None,
    type: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__488c4fcde080373477bb882fb5797280a201b4e08d06e2860a1e8d45f404ac1c(
    *,
    network_acl_entry_set: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPolicyPropsMixin.NetworkAclEntrySetProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9068816134f9e29ee46e2e892c6d323912caf352304f6249794e95254e6f453f(
    *,
    cidr_block: typing.Optional[builtins.str] = None,
    egress: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    icmp_type_code: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPolicyPropsMixin.IcmpTypeCodeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ipv6_cidr_block: typing.Optional[builtins.str] = None,
    port_range: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPolicyPropsMixin.PortRangeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    protocol: typing.Optional[builtins.str] = None,
    rule_action: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7e19c9aa716835dee3942287ed4d1862555b53107d6a465fd17677bf24c720c(
    *,
    first_entries: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPolicyPropsMixin.NetworkAclEntryProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    force_remediate_for_first_entries: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    force_remediate_for_last_entries: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    last_entries: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPolicyPropsMixin.NetworkAclEntryProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb3a362e375b3e7f849d663507151896eead64651ca8977a4093c30aac1cdfbe(
    *,
    firewall_deployment_model: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adc3582121f40f618d997a0cdf177827a31c6770c76ebf57bdda1c4fcdcc1277(
    *,
    network_acl_common_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPolicyPropsMixin.NetworkAclCommonPolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    network_firewall_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPolicyPropsMixin.NetworkFirewallPolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    third_party_firewall_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPolicyPropsMixin.ThirdPartyFirewallPolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afa7a5585b5952aafbfefaaf6567929d1dc5114b4cfcdb2f31eca65e247d6c9e(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab5910ef3f4ee6308ee653c07e0ad4891dfbbd4c1b964d0982dccf7ce1e35b6d(
    *,
    from_: typing.Optional[jsii.Number] = None,
    to: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86f85a3a863d1b83df6ab6b2808acb1eba44cca63e2ce56624618279e838599d(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65a2ed89e9f554d53101c30521cc5e2c76dbac0d783e94fbe53750ea77de2be7(
    *,
    managed_service_data: typing.Optional[builtins.str] = None,
    policy_option: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPolicyPropsMixin.PolicyOptionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b9788b5d5638bc721f212013d9405d822ad9d356393ab9fd09ab880b0c80182(
    *,
    firewall_deployment_model: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97aa6cbfae4f077a1b17cfb876ad0849ac857c101e08b59e8c74972e16e74594(
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_type_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b7f7b57c890e9d1385242ce74ff038593cf85693a32d4ff6d7a6fd74cbe0874(
    props: typing.Union[CfnResourceSetMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9df803251d9d21d08363559d151f64e7e7c9cb3489320fc7b223287ea7140455(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dece693b1b30d2c4d59f39c41208a4bed5b7f75430336b7faf67d6cbada8bb12(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
