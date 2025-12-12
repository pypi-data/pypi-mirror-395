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
    jsii_type="@aws-cdk/mixins-preview.aws_shield.mixins.CfnDRTAccessMixinProps",
    jsii_struct_bases=[],
    name_mapping={"log_bucket_list": "logBucketList", "role_arn": "roleArn"},
)
class CfnDRTAccessMixinProps:
    def __init__(
        self,
        *,
        log_bucket_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnDRTAccessPropsMixin.

        :param log_bucket_list: Authorizes the Shield Response Team (SRT) to access the specified Amazon S3 bucket containing log data such as Application Load Balancer access logs, CloudFront logs, or logs from third party sources. You can associate up to 10 Amazon S3 buckets with your subscription. Use this to share information with the SRT that's not available in AWS WAF logs. To use the services of the SRT, you must be subscribed to the `Business Support plan <https://docs.aws.amazon.com/premiumsupport/business-support/>`_ or the `Enterprise Support plan <https://docs.aws.amazon.com/premiumsupport/enterprise-support/>`_ .
        :param role_arn: Authorizes the Shield Response Team (SRT) using the specified role, to access your AWS account to assist with DDoS attack mitigation during potential attacks. This enables the SRT to inspect your AWS WAF configuration and logs and to create or update AWS WAF rules and web ACLs. You can associate only one ``RoleArn`` with your subscription. If you submit this update for an account that already has an associated role, the new ``RoleArn`` will replace the existing ``RoleArn`` . This change requires the following: - You must be subscribed to the `Business Support plan <https://docs.aws.amazon.com/premiumsupport/business-support/>`_ or the `Enterprise Support plan <https://docs.aws.amazon.com/premiumsupport/enterprise-support/>`_ . - The ``AWSShieldDRTAccessPolicy`` managed policy must be attached to the role that you specify in the request. You can access this policy in the IAM console at `AWSShieldDRTAccessPolicy <https://docs.aws.amazon.com/iam/home?#/policies/arn:aws:iam::aws:policy/service-role/AWSShieldDRTAccessPolicy>`_ . For information, see `Adding and removing IAM identity permissions <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage-attach-detach.html>`_ . - The role must trust the service principal ``drt.shield.amazonaws.com`` . For information, see `IAM JSON policy elements: Principal <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_principal.html>`_ . The SRT will have access only to your AWS WAF and Shield resources. By submitting this request, you provide permissions to the SRT to inspect your AWS WAF and Shield configuration and logs, and to create and update AWS WAF rules and web ACLs on your behalf. The SRT takes these actions only if explicitly authorized by you.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-drtaccess.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_shield import mixins as shield_mixins
            
            cfn_dRTAccess_mixin_props = shield_mixins.CfnDRTAccessMixinProps(
                log_bucket_list=["logBucketList"],
                role_arn="roleArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9067699efbf295d28a953deac689da6e50be8b3d1777157123bd6c17647e6d56)
            check_type(argname="argument log_bucket_list", value=log_bucket_list, expected_type=type_hints["log_bucket_list"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if log_bucket_list is not None:
            self._values["log_bucket_list"] = log_bucket_list
        if role_arn is not None:
            self._values["role_arn"] = role_arn

    @builtins.property
    def log_bucket_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Authorizes the Shield Response Team (SRT) to access the specified Amazon S3 bucket containing log data such as Application Load Balancer access logs, CloudFront logs, or logs from third party sources.

        You can associate up to 10 Amazon S3 buckets with your subscription.

        Use this to share information with the SRT that's not available in AWS WAF logs.

        To use the services of the SRT, you must be subscribed to the `Business Support plan <https://docs.aws.amazon.com/premiumsupport/business-support/>`_ or the `Enterprise Support plan <https://docs.aws.amazon.com/premiumsupport/enterprise-support/>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-drtaccess.html#cfn-shield-drtaccess-logbucketlist
        '''
        result = self._values.get("log_bucket_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''Authorizes the Shield Response Team (SRT) using the specified role, to access your AWS account to assist with DDoS attack mitigation during potential attacks.

        This enables the SRT to inspect your AWS WAF configuration and logs and to create or update AWS WAF rules and web ACLs.

        You can associate only one ``RoleArn`` with your subscription. If you submit this update for an account that already has an associated role, the new ``RoleArn`` will replace the existing ``RoleArn`` .

        This change requires the following:

        - You must be subscribed to the `Business Support plan <https://docs.aws.amazon.com/premiumsupport/business-support/>`_ or the `Enterprise Support plan <https://docs.aws.amazon.com/premiumsupport/enterprise-support/>`_ .
        - The ``AWSShieldDRTAccessPolicy`` managed policy must be attached to the role that you specify in the request. You can access this policy in the IAM console at `AWSShieldDRTAccessPolicy <https://docs.aws.amazon.com/iam/home?#/policies/arn:aws:iam::aws:policy/service-role/AWSShieldDRTAccessPolicy>`_ . For information, see `Adding and removing IAM identity permissions <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage-attach-detach.html>`_ .
        - The role must trust the service principal ``drt.shield.amazonaws.com`` . For information, see `IAM JSON policy elements: Principal <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_principal.html>`_ .

        The SRT will have access only to your AWS WAF and Shield resources. By submitting this request, you provide permissions to the SRT to inspect your AWS WAF and Shield configuration and logs, and to create and update AWS WAF rules and web ACLs on your behalf. The SRT takes these actions only if explicitly authorized by you.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-drtaccess.html#cfn-shield-drtaccess-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDRTAccessMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDRTAccessPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_shield.mixins.CfnDRTAccessPropsMixin",
):
    '''Provides permissions for the AWS Shield Advanced Shield response team (SRT) to access your account and your resource protections, to help you mitigate potential distributed denial of service (DDoS) attacks.

    *Configure ``AWS::Shield::DRTAccess`` for one account*

    To configure this resource through CloudFormation , you must be subscribed to AWS Shield Advanced . You can subscribe through the `Shield Advanced console <https://docs.aws.amazon.com/wafv2/shieldv2#/>`_ and through the APIs. For more information, see `Subscribe to AWS Shield Advanced <https://docs.aws.amazon.com/waf/latest/developerguide/enable-ddos-prem.html>`_ .

    See example templates for Shield Advanced in CloudFormation at `aws-samples/aws-shield-advanced-examples <https://docs.aws.amazon.com/https://github.com/aws-samples/aws-shield-advanced-examples>`_ .

    *Configure Shield Advanced using AWS CloudFormation and AWS Firewall Manager*

    You might be able to use Firewall Manager with AWS CloudFormation to configure Shield Advanced across multiple accounts and protected resources. To do this, your accounts must be part of an organization in AWS Organizations . You can use Firewall Manager to configure Shield Advanced protections for any resource types except for Amazon Route 53 or AWS Global Accelerator .

    For an example of this, see the one-click configuration guidance published by the AWS technical community at `One-click deployment of Shield Advanced <https://docs.aws.amazon.com/https://youtu.be/LCA3FwMk_QE>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-drtaccess.html
    :cloudformationResource: AWS::Shield::DRTAccess
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_shield import mixins as shield_mixins
        
        cfn_dRTAccess_props_mixin = shield_mixins.CfnDRTAccessPropsMixin(shield_mixins.CfnDRTAccessMixinProps(
            log_bucket_list=["logBucketList"],
            role_arn="roleArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDRTAccessMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Shield::DRTAccess``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7b2b614654dd999d912d0c6cb140f230e4352dacdb127e960cb62135f511b9d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b115fdc0c08c6e117712e7a150415a6f6eacaa70887bc8af744a10259019edde)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a3f4857aad3db7eb916ec1444076856d44b870d05de5c7371c22ccf01847216)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDRTAccessMixinProps:
        return typing.cast(CfnDRTAccessMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_shield.mixins.CfnProactiveEngagementMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "emergency_contact_list": "emergencyContactList",
        "proactive_engagement_status": "proactiveEngagementStatus",
    },
)
class CfnProactiveEngagementMixinProps:
    def __init__(
        self,
        *,
        emergency_contact_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProactiveEngagementPropsMixin.EmergencyContactProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        proactive_engagement_status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnProactiveEngagementPropsMixin.

        :param emergency_contact_list: The list of email addresses and phone numbers that the Shield Response Team (SRT) can use to contact you for escalations to the SRT and to initiate proactive customer support, plus any relevant notes. To enable proactive engagement, the contact list must include at least one phone number. If you provide more than one contact, in the notes, indicate the circumstances under which each contact should be used. Include primary and secondary contact designations, and provide the hours of availability and time zones for each contact. Example contact notes: - This is a hotline that's staffed 24x7x365. Please work with the responding analyst and they will get the appropriate person on the call. - Please contact the secondary phone number if the hotline doesn't respond within 5 minutes.
        :param proactive_engagement_status: Specifies whether proactive engagement is enabled or disabled. Valid values: ``ENABLED`` - The Shield Response Team (SRT) will use email and phone to notify contacts about escalations to the SRT and to initiate proactive customer support. ``DISABLED`` - The SRT will not proactively notify contacts about escalations or to initiate proactive customer support.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-proactiveengagement.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_shield import mixins as shield_mixins
            
            cfn_proactive_engagement_mixin_props = shield_mixins.CfnProactiveEngagementMixinProps(
                emergency_contact_list=[shield_mixins.CfnProactiveEngagementPropsMixin.EmergencyContactProperty(
                    contact_notes="contactNotes",
                    email_address="emailAddress",
                    phone_number="phoneNumber"
                )],
                proactive_engagement_status="proactiveEngagementStatus"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__574e87d10761868d33588edef16cbac67e7eddd279c97649ec4ee14c23e2c8c9)
            check_type(argname="argument emergency_contact_list", value=emergency_contact_list, expected_type=type_hints["emergency_contact_list"])
            check_type(argname="argument proactive_engagement_status", value=proactive_engagement_status, expected_type=type_hints["proactive_engagement_status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if emergency_contact_list is not None:
            self._values["emergency_contact_list"] = emergency_contact_list
        if proactive_engagement_status is not None:
            self._values["proactive_engagement_status"] = proactive_engagement_status

    @builtins.property
    def emergency_contact_list(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProactiveEngagementPropsMixin.EmergencyContactProperty"]]]]:
        '''The list of email addresses and phone numbers that the Shield Response Team (SRT) can use to contact you for escalations to the SRT and to initiate proactive customer support, plus any relevant notes.

        To enable proactive engagement, the contact list must include at least one phone number.

        If you provide more than one contact, in the notes, indicate the circumstances under which each contact should be used. Include primary and secondary contact designations, and provide the hours of availability and time zones for each contact.

        Example contact notes:

        - This is a hotline that's staffed 24x7x365. Please work with the responding analyst and they will get the appropriate person on the call.
        - Please contact the secondary phone number if the hotline doesn't respond within 5 minutes.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-proactiveengagement.html#cfn-shield-proactiveengagement-emergencycontactlist
        '''
        result = self._values.get("emergency_contact_list")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProactiveEngagementPropsMixin.EmergencyContactProperty"]]]], result)

    @builtins.property
    def proactive_engagement_status(self) -> typing.Optional[builtins.str]:
        '''Specifies whether proactive engagement is enabled or disabled.

        Valid values:

        ``ENABLED`` - The Shield Response Team (SRT) will use email and phone to notify contacts about escalations to the SRT and to initiate proactive customer support.

        ``DISABLED`` - The SRT will not proactively notify contacts about escalations or to initiate proactive customer support.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-proactiveengagement.html#cfn-shield-proactiveengagement-proactiveengagementstatus
        '''
        result = self._values.get("proactive_engagement_status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnProactiveEngagementMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnProactiveEngagementPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_shield.mixins.CfnProactiveEngagementPropsMixin",
):
    '''Authorizes the Shield Response Team (SRT) to use email and phone to notify contacts about escalations to the SRT and to initiate proactive customer support.

    To enable proactive engagement, you must be subscribed to the `Business Support plan <https://docs.aws.amazon.com/premiumsupport/business-support/>`_ or the `Enterprise Support plan <https://docs.aws.amazon.com/premiumsupport/enterprise-support/>`_ .

    *Configure ``AWS::Shield::ProactiveEngagement`` for one account*

    To configure this resource through CloudFormation , you must be subscribed to AWS Shield Advanced . You can subscribe through the `Shield Advanced console <https://docs.aws.amazon.com/wafv2/shieldv2#/>`_ and through the APIs. For more information, see `Subscribe to AWS Shield Advanced <https://docs.aws.amazon.com/waf/latest/developerguide/enable-ddos-prem.html>`_ .

    See example templates for Shield Advanced in CloudFormation at `aws-samples/aws-shield-advanced-examples <https://docs.aws.amazon.com/https://github.com/aws-samples/aws-shield-advanced-examples>`_ .

    *Configure Shield Advanced using AWS CloudFormation and AWS Firewall Manager*

    You might be able to use Firewall Manager with AWS CloudFormation to configure Shield Advanced across multiple accounts and protected resources. To do this, your accounts must be part of an organization in AWS Organizations . You can use Firewall Manager to configure Shield Advanced protections for any resource types except for Amazon Route 53 or AWS Global Accelerator .

    For an example of this, see the one-click configuration guidance published by the AWS technical community at `One-click deployment of Shield Advanced <https://docs.aws.amazon.com/https://youtu.be/LCA3FwMk_QE>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-proactiveengagement.html
    :cloudformationResource: AWS::Shield::ProactiveEngagement
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_shield import mixins as shield_mixins
        
        cfn_proactive_engagement_props_mixin = shield_mixins.CfnProactiveEngagementPropsMixin(shield_mixins.CfnProactiveEngagementMixinProps(
            emergency_contact_list=[shield_mixins.CfnProactiveEngagementPropsMixin.EmergencyContactProperty(
                contact_notes="contactNotes",
                email_address="emailAddress",
                phone_number="phoneNumber"
            )],
            proactive_engagement_status="proactiveEngagementStatus"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnProactiveEngagementMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Shield::ProactiveEngagement``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5c4176c88b89a2d6087c74b17736a277958887802f074d043a8c92242dcd23f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8565a33b6900eefd9653d104fb295d6d0d57c4b49788159dc7013e9e2b1e6836)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3228ab8820cafdd3e30c4e0fe2abddaf2fa0269f862e2673f525f04b9fc91728)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnProactiveEngagementMixinProps:
        return typing.cast(CfnProactiveEngagementMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_shield.mixins.CfnProactiveEngagementPropsMixin.EmergencyContactProperty",
        jsii_struct_bases=[],
        name_mapping={
            "contact_notes": "contactNotes",
            "email_address": "emailAddress",
            "phone_number": "phoneNumber",
        },
    )
    class EmergencyContactProperty:
        def __init__(
            self,
            *,
            contact_notes: typing.Optional[builtins.str] = None,
            email_address: typing.Optional[builtins.str] = None,
            phone_number: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contact information that the SRT can use to contact you if you have proactive engagement enabled, for escalations to the SRT and to initiate proactive customer support.

            :param contact_notes: Additional notes regarding the contact.
            :param email_address: The email address for the contact.
            :param phone_number: The phone number for the contact.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-shield-proactiveengagement-emergencycontact.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_shield import mixins as shield_mixins
                
                emergency_contact_property = shield_mixins.CfnProactiveEngagementPropsMixin.EmergencyContactProperty(
                    contact_notes="contactNotes",
                    email_address="emailAddress",
                    phone_number="phoneNumber"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5fe3fc40cc2aecea95c88c866f22f375ffd6c78489589b7854c16d993141ee07)
                check_type(argname="argument contact_notes", value=contact_notes, expected_type=type_hints["contact_notes"])
                check_type(argname="argument email_address", value=email_address, expected_type=type_hints["email_address"])
                check_type(argname="argument phone_number", value=phone_number, expected_type=type_hints["phone_number"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if contact_notes is not None:
                self._values["contact_notes"] = contact_notes
            if email_address is not None:
                self._values["email_address"] = email_address
            if phone_number is not None:
                self._values["phone_number"] = phone_number

        @builtins.property
        def contact_notes(self) -> typing.Optional[builtins.str]:
            '''Additional notes regarding the contact.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-shield-proactiveengagement-emergencycontact.html#cfn-shield-proactiveengagement-emergencycontact-contactnotes
            '''
            result = self._values.get("contact_notes")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def email_address(self) -> typing.Optional[builtins.str]:
            '''The email address for the contact.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-shield-proactiveengagement-emergencycontact.html#cfn-shield-proactiveengagement-emergencycontact-emailaddress
            '''
            result = self._values.get("email_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def phone_number(self) -> typing.Optional[builtins.str]:
            '''The phone number for the contact.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-shield-proactiveengagement-emergencycontact.html#cfn-shield-proactiveengagement-emergencycontact-phonenumber
            '''
            result = self._values.get("phone_number")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EmergencyContactProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


class CfnProtectionFlowLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_shield.mixins.CfnProtectionFlowLogs",
):
    '''Builder for CfnProtectionLogsMixin to generate FLOW_LOGS for CfnProtection.

    :cloudformationResource: AWS::Shield::Protection
    :logType: FLOW_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_shield import mixins as shield_mixins
        
        cfn_protection_flow_logs = shield_mixins.CfnProtectionFlowLogs()
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
    ) -> "CfnProtectionLogsMixin":
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__136d81442ac67a5f9da1b9dbb70ea6c15f06a3291690f5f1186661e6f7b40a02)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast("CfnProtectionLogsMixin", jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> "CfnProtectionLogsMixin":
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8935061f26d8f172c9c7f882d4f671ca602e5547150852b5d8f035af7623aa51)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast("CfnProtectionLogsMixin", jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> "CfnProtectionLogsMixin":
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d5c168144cbe18d17705006808147b8ca024b10dcdeb900d9be370afcc0ee58)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast("CfnProtectionLogsMixin", jsii.invoke(self, "toS3", [bucket]))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_shield.mixins.CfnProtectionGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "aggregation": "aggregation",
        "members": "members",
        "pattern": "pattern",
        "protection_group_id": "protectionGroupId",
        "resource_type": "resourceType",
        "tags": "tags",
    },
)
class CfnProtectionGroupMixinProps:
    def __init__(
        self,
        *,
        aggregation: typing.Optional[builtins.str] = None,
        members: typing.Optional[typing.Sequence[builtins.str]] = None,
        pattern: typing.Optional[builtins.str] = None,
        protection_group_id: typing.Optional[builtins.str] = None,
        resource_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnProtectionGroupPropsMixin.

        :param aggregation: Defines how AWS Shield combines resource data for the group in order to detect, mitigate, and report events. - ``Sum`` - Use the total traffic across the group. This is a good choice for most cases. Examples include Elastic IP addresses for EC2 instances that scale manually or automatically. - ``Mean`` - Use the average of the traffic across the group. This is a good choice for resources that share traffic uniformly. Examples include accelerators and load balancers. - ``Max`` - Use the highest traffic from each resource. This is useful for resources that don't share traffic and for resources that share that traffic in a non-uniform way. Examples include Amazon CloudFront distributions and origin resources for CloudFront distributions.
        :param members: The ARNs (Amazon Resource Names) of the resources to include in the protection group. You must set this when you set ``Pattern`` to ``ARBITRARY`` and you must not set it for any other ``Pattern`` setting.
        :param pattern: The criteria to use to choose the protected resources for inclusion in the group. You can include all resources that have protections, provide a list of resource ARNs (Amazon Resource Names), or include all resources of a specified resource type.
        :param protection_group_id: The name of the protection group. You use this to identify the protection group in lists and to manage the protection group, for example to update, delete, or describe it.
        :param resource_type: The resource type to include in the protection group. All protected resources of this type are included in the protection group. You must set this when you set ``Pattern`` to ``BY_RESOURCE_TYPE`` and you must not set it for any other ``Pattern`` setting.
        :param tags: Key:value pairs associated with an AWS resource. The key:value pair can be anything you define. Typically, the tag key represents a category (such as "environment") and the tag value represents a specific value within that category (such as "test," "development," or "production"). You can add up to 50 tags to each AWS resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protectiongroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_shield import mixins as shield_mixins
            
            cfn_protection_group_mixin_props = shield_mixins.CfnProtectionGroupMixinProps(
                aggregation="aggregation",
                members=["members"],
                pattern="pattern",
                protection_group_id="protectionGroupId",
                resource_type="resourceType",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f18584a0f818143a26dc5de25fda068f974eca3451ffe8975cce54a406287b7)
            check_type(argname="argument aggregation", value=aggregation, expected_type=type_hints["aggregation"])
            check_type(argname="argument members", value=members, expected_type=type_hints["members"])
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
            check_type(argname="argument protection_group_id", value=protection_group_id, expected_type=type_hints["protection_group_id"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aggregation is not None:
            self._values["aggregation"] = aggregation
        if members is not None:
            self._values["members"] = members
        if pattern is not None:
            self._values["pattern"] = pattern
        if protection_group_id is not None:
            self._values["protection_group_id"] = protection_group_id
        if resource_type is not None:
            self._values["resource_type"] = resource_type
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def aggregation(self) -> typing.Optional[builtins.str]:
        '''Defines how AWS Shield combines resource data for the group in order to detect, mitigate, and report events.

        - ``Sum`` - Use the total traffic across the group. This is a good choice for most cases. Examples include Elastic IP addresses for EC2 instances that scale manually or automatically.
        - ``Mean`` - Use the average of the traffic across the group. This is a good choice for resources that share traffic uniformly. Examples include accelerators and load balancers.
        - ``Max`` - Use the highest traffic from each resource. This is useful for resources that don't share traffic and for resources that share that traffic in a non-uniform way. Examples include Amazon CloudFront distributions and origin resources for CloudFront distributions.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protectiongroup.html#cfn-shield-protectiongroup-aggregation
        '''
        result = self._values.get("aggregation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def members(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The ARNs (Amazon Resource Names) of the resources to include in the protection group.

        You must set this when you set ``Pattern`` to ``ARBITRARY`` and you must not set it for any other ``Pattern`` setting.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protectiongroup.html#cfn-shield-protectiongroup-members
        '''
        result = self._values.get("members")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def pattern(self) -> typing.Optional[builtins.str]:
        '''The criteria to use to choose the protected resources for inclusion in the group.

        You can include all resources that have protections, provide a list of resource ARNs (Amazon Resource Names), or include all resources of a specified resource type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protectiongroup.html#cfn-shield-protectiongroup-pattern
        '''
        result = self._values.get("pattern")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protection_group_id(self) -> typing.Optional[builtins.str]:
        '''The name of the protection group.

        You use this to identify the protection group in lists and to manage the protection group, for example to update, delete, or describe it.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protectiongroup.html#cfn-shield-protectiongroup-protectiongroupid
        '''
        result = self._values.get("protection_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_type(self) -> typing.Optional[builtins.str]:
        '''The resource type to include in the protection group.

        All protected resources of this type are included in the protection group. You must set this when you set ``Pattern`` to ``BY_RESOURCE_TYPE`` and you must not set it for any other ``Pattern`` setting.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protectiongroup.html#cfn-shield-protectiongroup-resourcetype
        '''
        result = self._values.get("resource_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Key:value pairs associated with an AWS resource.

        The key:value pair can be anything you define. Typically, the tag key represents a category (such as "environment") and the tag value represents a specific value within that category (such as "test," "development," or "production"). You can add up to 50 tags to each AWS resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protectiongroup.html#cfn-shield-protectiongroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnProtectionGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnProtectionGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_shield.mixins.CfnProtectionGroupPropsMixin",
):
    '''Creates a grouping of protected resources so they can be handled as a collective.

    This resource grouping improves the accuracy of detection and reduces false positives.

    To configure this resource through CloudFormation , you must be subscribed to AWS Shield Advanced . You can subscribe through the `Shield Advanced console <https://docs.aws.amazon.com/wafv2/shieldv2#/>`_ and through the APIs. For more information, see `Subscribe to AWS Shield Advanced <https://docs.aws.amazon.com/waf/latest/developerguide/enable-ddos-prem.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protectiongroup.html
    :cloudformationResource: AWS::Shield::ProtectionGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_shield import mixins as shield_mixins
        
        cfn_protection_group_props_mixin = shield_mixins.CfnProtectionGroupPropsMixin(shield_mixins.CfnProtectionGroupMixinProps(
            aggregation="aggregation",
            members=["members"],
            pattern="pattern",
            protection_group_id="protectionGroupId",
            resource_type="resourceType",
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
        props: typing.Union[CfnProtectionGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Shield::ProtectionGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0054216c20e70edaa095aedc92061c85023f6a6519af90d6187182424f9ed72)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe2d78cd59bc031c3901b730cf441107d210d1499539f0a9217cfc6337fb34be)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24553133542be71e5b745306fa9bd0ca925cd36512e19b8ac482f65ee4437995)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnProtectionGroupMixinProps:
        return typing.cast(CfnProtectionGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.implements(_IMixin_11e4b965)
class CfnProtectionLogsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_shield.mixins.CfnProtectionLogsMixin",
):
    '''Enables AWS Shield Advanced for a specific AWS resource.

    The resource can be an Amazon CloudFront distribution, Amazon Route 53 hosted zone, AWS Global Accelerator standard accelerator, Elastic IP Address, Application Load Balancer, or a Classic Load Balancer. You can protect Amazon EC2 instances and Network Load Balancers by association with protected Amazon EC2 Elastic IP addresses.

    *Configure a single ``AWS::Shield::Protection``*

    Use this protection to protect a single resource at a time.

    To configure this Shield Advanced protection through CloudFormation , you must be subscribed to Shield Advanced . You can subscribe through the `Shield Advanced console <https://docs.aws.amazon.com/wafv2/shieldv2#/>`_ and through the APIs. For more information, see `Subscribe to AWS Shield Advanced <https://docs.aws.amazon.com/waf/latest/developerguide/enable-ddos-prem.html>`_ .

    See example templates for Shield Advanced in CloudFormation at `aws-samples/aws-shield-advanced-examples <https://docs.aws.amazon.com/https://github.com/aws-samples/aws-shield-advanced-examples>`_ .

    *Configure Shield Advanced using AWS CloudFormation and AWS Firewall Manager*

    You might be able to use Firewall Manager with AWS CloudFormation to configure Shield Advanced across multiple accounts and protected resources. To do this, your accounts must be part of an organization in AWS Organizations . You can use Firewall Manager to configure Shield Advanced protections for any resource types except for Amazon Route 53 or AWS Global Accelerator .

    For an example of this, see the one-click configuration guidance published by the AWS technical community at `One-click deployment of Shield Advanced <https://docs.aws.amazon.com/https://youtu.be/LCA3FwMk_QE>`_ .

    *Configure multiple protections through the Shield Advanced console*

    You can add protection to multiple resources at once through the `Shield Advanced console <https://docs.aws.amazon.com/wafv2/shieldv2#/>`_ . For more information see `Getting Started with AWS Shield Advanced <https://docs.aws.amazon.com/waf/latest/developerguide/getting-started-ddos.html>`_ and `Managing resource protections in AWS Shield Advanced <https://docs.aws.amazon.com/waf/latest/developerguide/ddos-manage-protected-resources.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protection.html
    :cloudformationResource: AWS::Shield::Protection
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import aws_logs as logs
        from aws_cdk.mixins_preview.aws_shield import mixins as shield_mixins
        
        # logs_delivery: logs.ILogsDelivery
        
        cfn_protection_logs_mixin = shield_mixins.CfnProtectionLogsMixin("logType", logs_delivery)
    '''

    def __init__(
        self,
        log_type: builtins.str,
        log_delivery: _ILogsDelivery_0d3c9e29,
    ) -> None:
        '''Create a mixin to enable vended logs for ``AWS::Shield::Protection``.

        :param log_type: Type of logs that are getting vended.
        :param log_delivery: Object in charge of setting up the delivery destination and delivery connection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f853b84145ee8ae6c4a7164de1f2bf22b1c31bb2fea688a920cca0830d1e9b3c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4246c8bdb5fabd43df75a738f8e585355249981b359428bc5f06dee728b0bdc4)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [resource]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct (has vendedLogs property).

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88dc6e48eacd43b668d6c430163bb776930601f7ab80a68e391058191e0b8a07)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="FLOW_LOGS")
    def FLOW_LOGS(cls) -> CfnProtectionFlowLogs:
        return typing.cast(CfnProtectionFlowLogs, jsii.sget(cls, "FLOW_LOGS"))

    @builtins.property
    @jsii.member(jsii_name="logDelivery")
    def _log_delivery(self) -> _ILogsDelivery_0d3c9e29:
        return typing.cast(_ILogsDelivery_0d3c9e29, jsii.get(self, "logDelivery"))

    @builtins.property
    @jsii.member(jsii_name="logType")
    def _log_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logType"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_shield.mixins.CfnProtectionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_layer_automatic_response_configuration": "applicationLayerAutomaticResponseConfiguration",
        "health_check_arns": "healthCheckArns",
        "name": "name",
        "resource_arn": "resourceArn",
        "tags": "tags",
    },
)
class CfnProtectionMixinProps:
    def __init__(
        self,
        *,
        application_layer_automatic_response_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProtectionPropsMixin.ApplicationLayerAutomaticResponseConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        health_check_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        resource_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnProtectionPropsMixin.

        :param application_layer_automatic_response_configuration: The automatic application layer DDoS mitigation settings for the protection. This configuration determines whether Shield Advanced automatically manages rules in the web ACL in order to respond to application layer events that Shield Advanced determines to be DDoS attacks. If you use CloudFormation to manage the web ACLs that you use with Shield Advanced automatic mitigation, see the additional guidance about web ACL management in the ``AWS::WAFv2::WebACL`` resource description.
        :param health_check_arns: The ARN (Amazon Resource Name) of the health check to associate with the protection. Health-based detection provides improved responsiveness and accuracy in attack detection and mitigation. You can use this option with any resource type except for Route 53 hosted zones. For more information, see `Configuring health-based detection using health checks <https://docs.aws.amazon.com/waf/latest/developerguide/ddos-advanced-health-checks.html>`_ in the *AWS Shield Advanced Developer Guide* .
        :param name: The name of the protection. For example, ``My CloudFront distributions`` . .. epigraph:: If you change the name of an existing protection, Shield Advanced deletes the protection and replaces it with a new one. While this is happening, the protection isn't available on the AWS resource.
        :param resource_arn: The ARN (Amazon Resource Name) of the AWS resource that is protected.
        :param tags: Key:value pairs associated with an AWS resource. The key:value pair can be anything you define. Typically, the tag key represents a category (such as "environment") and the tag value represents a specific value within that category (such as "test," "development," or "production"). You can add up to 50 tags to each AWS resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protection.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_shield import mixins as shield_mixins
            
            # block: Any
            # count: Any
            
            cfn_protection_mixin_props = shield_mixins.CfnProtectionMixinProps(
                application_layer_automatic_response_configuration=shield_mixins.CfnProtectionPropsMixin.ApplicationLayerAutomaticResponseConfigurationProperty(
                    action=shield_mixins.CfnProtectionPropsMixin.ActionProperty(
                        block=block,
                        count=count
                    ),
                    status="status"
                ),
                health_check_arns=["healthCheckArns"],
                name="name",
                resource_arn="resourceArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44cffb5705700b9450e185658460afa0d7922958e84963f65c6ce438836c67d6)
            check_type(argname="argument application_layer_automatic_response_configuration", value=application_layer_automatic_response_configuration, expected_type=type_hints["application_layer_automatic_response_configuration"])
            check_type(argname="argument health_check_arns", value=health_check_arns, expected_type=type_hints["health_check_arns"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_layer_automatic_response_configuration is not None:
            self._values["application_layer_automatic_response_configuration"] = application_layer_automatic_response_configuration
        if health_check_arns is not None:
            self._values["health_check_arns"] = health_check_arns
        if name is not None:
            self._values["name"] = name
        if resource_arn is not None:
            self._values["resource_arn"] = resource_arn
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def application_layer_automatic_response_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProtectionPropsMixin.ApplicationLayerAutomaticResponseConfigurationProperty"]]:
        '''The automatic application layer DDoS mitigation settings for the protection.

        This configuration determines whether Shield Advanced automatically manages rules in the web ACL in order to respond to application layer events that Shield Advanced determines to be DDoS attacks.

        If you use CloudFormation to manage the web ACLs that you use with Shield Advanced automatic mitigation, see the additional guidance about web ACL management in the ``AWS::WAFv2::WebACL`` resource description.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protection.html#cfn-shield-protection-applicationlayerautomaticresponseconfiguration
        '''
        result = self._values.get("application_layer_automatic_response_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProtectionPropsMixin.ApplicationLayerAutomaticResponseConfigurationProperty"]], result)

    @builtins.property
    def health_check_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The ARN (Amazon Resource Name) of the health check to associate with the protection.

        Health-based detection provides improved responsiveness and accuracy in attack detection and mitigation.

        You can use this option with any resource type except for Route 53 hosted zones.

        For more information, see `Configuring health-based detection using health checks <https://docs.aws.amazon.com/waf/latest/developerguide/ddos-advanced-health-checks.html>`_ in the *AWS Shield Advanced Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protection.html#cfn-shield-protection-healthcheckarns
        '''
        result = self._values.get("health_check_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the protection. For example, ``My CloudFront distributions`` .

        .. epigraph::

           If you change the name of an existing protection, Shield Advanced deletes the protection and replaces it with a new one. While this is happening, the protection isn't available on the AWS resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protection.html#cfn-shield-protection-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN (Amazon Resource Name) of the AWS resource that is protected.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protection.html#cfn-shield-protection-resourcearn
        '''
        result = self._values.get("resource_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Key:value pairs associated with an AWS resource.

        The key:value pair can be anything you define. Typically, the tag key represents a category (such as "environment") and the tag value represents a specific value within that category (such as "test," "development," or "production"). You can add up to 50 tags to each AWS resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protection.html#cfn-shield-protection-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnProtectionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnProtectionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_shield.mixins.CfnProtectionPropsMixin",
):
    '''Enables AWS Shield Advanced for a specific AWS resource.

    The resource can be an Amazon CloudFront distribution, Amazon Route 53 hosted zone, AWS Global Accelerator standard accelerator, Elastic IP Address, Application Load Balancer, or a Classic Load Balancer. You can protect Amazon EC2 instances and Network Load Balancers by association with protected Amazon EC2 Elastic IP addresses.

    *Configure a single ``AWS::Shield::Protection``*

    Use this protection to protect a single resource at a time.

    To configure this Shield Advanced protection through CloudFormation , you must be subscribed to Shield Advanced . You can subscribe through the `Shield Advanced console <https://docs.aws.amazon.com/wafv2/shieldv2#/>`_ and through the APIs. For more information, see `Subscribe to AWS Shield Advanced <https://docs.aws.amazon.com/waf/latest/developerguide/enable-ddos-prem.html>`_ .

    See example templates for Shield Advanced in CloudFormation at `aws-samples/aws-shield-advanced-examples <https://docs.aws.amazon.com/https://github.com/aws-samples/aws-shield-advanced-examples>`_ .

    *Configure Shield Advanced using AWS CloudFormation and AWS Firewall Manager*

    You might be able to use Firewall Manager with AWS CloudFormation to configure Shield Advanced across multiple accounts and protected resources. To do this, your accounts must be part of an organization in AWS Organizations . You can use Firewall Manager to configure Shield Advanced protections for any resource types except for Amazon Route 53 or AWS Global Accelerator .

    For an example of this, see the one-click configuration guidance published by the AWS technical community at `One-click deployment of Shield Advanced <https://docs.aws.amazon.com/https://youtu.be/LCA3FwMk_QE>`_ .

    *Configure multiple protections through the Shield Advanced console*

    You can add protection to multiple resources at once through the `Shield Advanced console <https://docs.aws.amazon.com/wafv2/shieldv2#/>`_ . For more information see `Getting Started with AWS Shield Advanced <https://docs.aws.amazon.com/waf/latest/developerguide/getting-started-ddos.html>`_ and `Managing resource protections in AWS Shield Advanced <https://docs.aws.amazon.com/waf/latest/developerguide/ddos-manage-protected-resources.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protection.html
    :cloudformationResource: AWS::Shield::Protection
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_shield import mixins as shield_mixins
        
        # block: Any
        # count: Any
        
        cfn_protection_props_mixin = shield_mixins.CfnProtectionPropsMixin(shield_mixins.CfnProtectionMixinProps(
            application_layer_automatic_response_configuration=shield_mixins.CfnProtectionPropsMixin.ApplicationLayerAutomaticResponseConfigurationProperty(
                action=shield_mixins.CfnProtectionPropsMixin.ActionProperty(
                    block=block,
                    count=count
                ),
                status="status"
            ),
            health_check_arns=["healthCheckArns"],
            name="name",
            resource_arn="resourceArn",
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
        props: typing.Union[CfnProtectionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Shield::Protection``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5dc91e25617724b7c84f0223b8960ec85c5c8f42d23f6f51e35d1511654a94f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b70c0878f512df8f80896c69484a4268e7b8131b69397688fffe3f903c0ba30)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44119b0bfab7c1693b204f80de61e7a06ddc1ea7af02a0551e2616b487c368c2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnProtectionMixinProps:
        return typing.cast(CfnProtectionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_shield.mixins.CfnProtectionPropsMixin.ActionProperty",
        jsii_struct_bases=[],
        name_mapping={"block": "block", "count": "count"},
    )
    class ActionProperty:
        def __init__(
            self,
            *,
            block: typing.Any = None,
            count: typing.Any = None,
        ) -> None:
            '''Specifies the action setting that Shield Advanced should use in the AWS WAF rules that it creates on behalf of the protected resource in response to DDoS attacks.

            You specify this as part of the configuration for the automatic application layer DDoS mitigation feature, when you enable or update automatic mitigation. Shield Advanced creates the AWS WAF rules in a Shield Advanced-managed rule group, inside the web ACL that you have associated with the resource.

            :param block: Specifies that Shield Advanced should configure its AWS WAF rules with the AWS WAF ``Block`` action. You must specify exactly one action, either ``Block`` or ``Count`` . Example JSON: ``{ "Block": {} }`` Example YAML: ``Block: {}``
            :param count: Specifies that Shield Advanced should configure its AWS WAF rules with the AWS WAF ``Count`` action. You must specify exactly one action, either ``Block`` or ``Count`` . Example JSON: ``{ "Count": {} }`` Example YAML: ``Count: {}``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-shield-protection-action.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_shield import mixins as shield_mixins
                
                # block: Any
                # count: Any
                
                action_property = shield_mixins.CfnProtectionPropsMixin.ActionProperty(
                    block=block,
                    count=count
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__921a30cb62a85e3ee9eb07b54f85d03bdfae606c1185c578f78c68debdb6c7f9)
                check_type(argname="argument block", value=block, expected_type=type_hints["block"])
                check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if block is not None:
                self._values["block"] = block
            if count is not None:
                self._values["count"] = count

        @builtins.property
        def block(self) -> typing.Any:
            '''Specifies that Shield Advanced should configure its AWS WAF rules with the AWS WAF ``Block`` action.

            You must specify exactly one action, either ``Block`` or ``Count`` .

            Example JSON: ``{ "Block": {} }``

            Example YAML: ``Block: {}``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-shield-protection-action.html#cfn-shield-protection-action-block
            '''
            result = self._values.get("block")
            return typing.cast(typing.Any, result)

        @builtins.property
        def count(self) -> typing.Any:
            '''Specifies that Shield Advanced should configure its AWS WAF rules with the AWS WAF ``Count`` action.

            You must specify exactly one action, either ``Block`` or ``Count`` .

            Example JSON: ``{ "Count": {} }``

            Example YAML: ``Count: {}``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-shield-protection-action.html#cfn-shield-protection-action-count
            '''
            result = self._values.get("count")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_shield.mixins.CfnProtectionPropsMixin.ApplicationLayerAutomaticResponseConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"action": "action", "status": "status"},
    )
    class ApplicationLayerAutomaticResponseConfigurationProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProtectionPropsMixin.ActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            status: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The automatic application layer DDoS mitigation settings for a ``Protection`` .

            This configuration determines whether Shield Advanced automatically manages rules in the web ACL in order to respond to application layer events that Shield Advanced determines to be DDoS attacks.

            If you use CloudFormation to manage the web ACLs that you use with Shield Advanced automatic mitigation, see the guidance for the ``AWS::WAFv2::WebACL`` resource.

            :param action: Specifies the action setting that Shield Advanced should use in the AWS WAF rules that it creates on behalf of the protected resource in response to DDoS attacks. You specify this as part of the configuration for the automatic application layer DDoS mitigation feature, when you enable or update automatic mitigation. Shield Advanced creates the AWS WAF rules in a Shield Advanced-managed rule group, inside the web ACL that you have associated with the resource.
            :param status: Indicates whether automatic application layer DDoS mitigation is enabled for the protection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-shield-protection-applicationlayerautomaticresponseconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_shield import mixins as shield_mixins
                
                # block: Any
                # count: Any
                
                application_layer_automatic_response_configuration_property = shield_mixins.CfnProtectionPropsMixin.ApplicationLayerAutomaticResponseConfigurationProperty(
                    action=shield_mixins.CfnProtectionPropsMixin.ActionProperty(
                        block=block,
                        count=count
                    ),
                    status="status"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7196d527128b1363e96908cefe50ec80d7bdc6155f5a7734227f8d7d5bedf2f8)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProtectionPropsMixin.ActionProperty"]]:
            '''Specifies the action setting that Shield Advanced should use in the AWS WAF rules that it creates on behalf of the protected resource in response to DDoS attacks.

            You specify this as part of the configuration for the automatic application layer DDoS mitigation feature, when you enable or update automatic mitigation. Shield Advanced creates the AWS WAF rules in a Shield Advanced-managed rule group, inside the web ACL that you have associated with the resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-shield-protection-applicationlayerautomaticresponseconfiguration.html#cfn-shield-protection-applicationlayerautomaticresponseconfiguration-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProtectionPropsMixin.ActionProperty"]], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''Indicates whether automatic application layer DDoS mitigation is enabled for the protection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-shield-protection-applicationlayerautomaticresponseconfiguration.html#cfn-shield-protection-applicationlayerautomaticresponseconfiguration-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApplicationLayerAutomaticResponseConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnDRTAccessMixinProps",
    "CfnDRTAccessPropsMixin",
    "CfnProactiveEngagementMixinProps",
    "CfnProactiveEngagementPropsMixin",
    "CfnProtectionFlowLogs",
    "CfnProtectionGroupMixinProps",
    "CfnProtectionGroupPropsMixin",
    "CfnProtectionLogsMixin",
    "CfnProtectionMixinProps",
    "CfnProtectionPropsMixin",
]

publication.publish()

def _typecheckingstub__9067699efbf295d28a953deac689da6e50be8b3d1777157123bd6c17647e6d56(
    *,
    log_bucket_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7b2b614654dd999d912d0c6cb140f230e4352dacdb127e960cb62135f511b9d(
    props: typing.Union[CfnDRTAccessMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b115fdc0c08c6e117712e7a150415a6f6eacaa70887bc8af744a10259019edde(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a3f4857aad3db7eb916ec1444076856d44b870d05de5c7371c22ccf01847216(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__574e87d10761868d33588edef16cbac67e7eddd279c97649ec4ee14c23e2c8c9(
    *,
    emergency_contact_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProactiveEngagementPropsMixin.EmergencyContactProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    proactive_engagement_status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5c4176c88b89a2d6087c74b17736a277958887802f074d043a8c92242dcd23f(
    props: typing.Union[CfnProactiveEngagementMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8565a33b6900eefd9653d104fb295d6d0d57c4b49788159dc7013e9e2b1e6836(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3228ab8820cafdd3e30c4e0fe2abddaf2fa0269f862e2673f525f04b9fc91728(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fe3fc40cc2aecea95c88c866f22f375ffd6c78489589b7854c16d993141ee07(
    *,
    contact_notes: typing.Optional[builtins.str] = None,
    email_address: typing.Optional[builtins.str] = None,
    phone_number: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__136d81442ac67a5f9da1b9dbb70ea6c15f06a3291690f5f1186661e6f7b40a02(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8935061f26d8f172c9c7f882d4f671ca602e5547150852b5d8f035af7623aa51(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d5c168144cbe18d17705006808147b8ca024b10dcdeb900d9be370afcc0ee58(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f18584a0f818143a26dc5de25fda068f974eca3451ffe8975cce54a406287b7(
    *,
    aggregation: typing.Optional[builtins.str] = None,
    members: typing.Optional[typing.Sequence[builtins.str]] = None,
    pattern: typing.Optional[builtins.str] = None,
    protection_group_id: typing.Optional[builtins.str] = None,
    resource_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0054216c20e70edaa095aedc92061c85023f6a6519af90d6187182424f9ed72(
    props: typing.Union[CfnProtectionGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe2d78cd59bc031c3901b730cf441107d210d1499539f0a9217cfc6337fb34be(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24553133542be71e5b745306fa9bd0ca925cd36512e19b8ac482f65ee4437995(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f853b84145ee8ae6c4a7164de1f2bf22b1c31bb2fea688a920cca0830d1e9b3c(
    log_type: builtins.str,
    log_delivery: _ILogsDelivery_0d3c9e29,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4246c8bdb5fabd43df75a738f8e585355249981b359428bc5f06dee728b0bdc4(
    resource: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88dc6e48eacd43b668d6c430163bb776930601f7ab80a68e391058191e0b8a07(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44cffb5705700b9450e185658460afa0d7922958e84963f65c6ce438836c67d6(
    *,
    application_layer_automatic_response_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProtectionPropsMixin.ApplicationLayerAutomaticResponseConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    health_check_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    resource_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5dc91e25617724b7c84f0223b8960ec85c5c8f42d23f6f51e35d1511654a94f(
    props: typing.Union[CfnProtectionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b70c0878f512df8f80896c69484a4268e7b8131b69397688fffe3f903c0ba30(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44119b0bfab7c1693b204f80de61e7a06ddc1ea7af02a0551e2616b487c368c2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__921a30cb62a85e3ee9eb07b54f85d03bdfae606c1185c578f78c68debdb6c7f9(
    *,
    block: typing.Any = None,
    count: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7196d527128b1363e96908cefe50ec80d7bdc6155f5a7734227f8d7d5bedf2f8(
    *,
    action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProtectionPropsMixin.ActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
