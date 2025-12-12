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


class CfnApplicationEventLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnApplicationEventLogs",
):
    '''Builder for CfnApplicationLogsMixin to generate EVENT_LOGS for CfnApplication.

    :cloudformationResource: AWS::QBusiness::Application
    :logType: EVENT_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
        
        cfn_application_event_logs = qbusiness_mixins.CfnApplicationEventLogs()
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
    ) -> "CfnApplicationLogsMixin":
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d34e31e7f28e6d9623407543aa02e24a98471b0062cc49fcc9cb33da27c54014)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast("CfnApplicationLogsMixin", jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> "CfnApplicationLogsMixin":
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a12a04f7977985f75ecb608750d79b72a20f7e5c1b93bfdb63908e7268d0f453)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast("CfnApplicationLogsMixin", jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> "CfnApplicationLogsMixin":
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c4f7d1ed69da227cb7bad96687fd5cc95437dd676e0866347acdd9d859b0081)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast("CfnApplicationLogsMixin", jsii.invoke(self, "toS3", [bucket]))


@jsii.implements(_IMixin_11e4b965)
class CfnApplicationLogsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnApplicationLogsMixin",
):
    '''Creates an Amazon Q Business application.

    .. epigraph::

       There are new tiers for Amazon Q Business. Not all features in Amazon Q Business Pro are also available in Amazon Q Business Lite. For information on what's included in Amazon Q Business Lite and what's included in Amazon Q Business Pro, see `Amazon Q Business tiers <https://docs.aws.amazon.com/amazonq/latest/qbusiness-ug/tiers.html#user-sub-tiers>`_ . You must use the Amazon Q Business console to assign subscription tiers to users.

       An Amazon Q Apps service linked role will be created if it's absent in the AWS account when ``QAppsConfiguration`` is enabled in the request. For more information, see `Using service-linked roles for Q Apps <https://docs.aws.amazon.com/amazonq/latest/qbusiness-ug/using-service-linked-roles-qapps.html>`_ .

       When you create an application, Amazon Q Business may securely transmit data for processing from your selected AWS region, but within your geography. For more information, see `Cross region inference in Amazon Q Business <https://docs.aws.amazon.com/amazonq/latest/qbusiness-ug/cross-region-inference.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-application.html
    :cloudformationResource: AWS::QBusiness::Application
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import aws_logs as logs
        from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
        
        # logs_delivery: logs.ILogsDelivery
        
        cfn_application_logs_mixin = qbusiness_mixins.CfnApplicationLogsMixin("logType", logs_delivery)
    '''

    def __init__(
        self,
        log_type: builtins.str,
        log_delivery: _ILogsDelivery_0d3c9e29,
    ) -> None:
        '''Create a mixin to enable vended logs for ``AWS::QBusiness::Application``.

        :param log_type: Type of logs that are getting vended.
        :param log_delivery: Object in charge of setting up the delivery destination and delivery connection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e84fe8d369c72562838387fdaae117e98be3cf0570e02903adb20cf2508b27f9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__62dc97b6e94872349ea0b8ac24843a120b9852800b12632288610257ed38e845)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [resource]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct (has vendedLogs property).

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1265d846673268ba93d93a93dd82e96447415ffec70165e1bf7fe6fc26c78981)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="EVENT_LOGS")
    def EVENT_LOGS(cls) -> CfnApplicationEventLogs:
        return typing.cast(CfnApplicationEventLogs, jsii.sget(cls, "EVENT_LOGS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SYNC_JOB_LOGS")
    def SYNC_JOB_LOGS(cls) -> "CfnApplicationSyncJobLogs":
        return typing.cast("CfnApplicationSyncJobLogs", jsii.sget(cls, "SYNC_JOB_LOGS"))

    @builtins.property
    @jsii.member(jsii_name="logDelivery")
    def _log_delivery(self) -> _ILogsDelivery_0d3c9e29:
        return typing.cast(_ILogsDelivery_0d3c9e29, jsii.get(self, "logDelivery"))

    @builtins.property
    @jsii.member(jsii_name="logType")
    def _log_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logType"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnApplicationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "attachments_configuration": "attachmentsConfiguration",
        "auto_subscription_configuration": "autoSubscriptionConfiguration",
        "client_ids_for_oidc": "clientIdsForOidc",
        "description": "description",
        "display_name": "displayName",
        "encryption_configuration": "encryptionConfiguration",
        "iam_identity_provider_arn": "iamIdentityProviderArn",
        "identity_center_instance_arn": "identityCenterInstanceArn",
        "identity_type": "identityType",
        "personalization_configuration": "personalizationConfiguration",
        "q_apps_configuration": "qAppsConfiguration",
        "quick_sight_configuration": "quickSightConfiguration",
        "role_arn": "roleArn",
        "tags": "tags",
    },
)
class CfnApplicationMixinProps:
    def __init__(
        self,
        *,
        attachments_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.AttachmentsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        auto_subscription_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.AutoSubscriptionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        client_ids_for_oidc: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.EncryptionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        iam_identity_provider_arn: typing.Optional[builtins.str] = None,
        identity_center_instance_arn: typing.Optional[builtins.str] = None,
        identity_type: typing.Optional[builtins.str] = None,
        personalization_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.PersonalizationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        q_apps_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.QAppsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        quick_sight_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.QuickSightConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnApplicationPropsMixin.

        :param attachments_configuration: Configuration information for the file upload during chat feature.
        :param auto_subscription_configuration: Subscription configuration information for an Amazon Q Business application using IAM identity federation for user management.
        :param client_ids_for_oidc: The OIDC client ID for a Amazon Q Business application.
        :param description: A description for the Amazon Q Business application.
        :param display_name: The name of the Amazon Q Business application.
        :param encryption_configuration: Provides the identifier of the AWS key used to encrypt data indexed by Amazon Q Business. Amazon Q Business doesn't support asymmetric keys.
        :param iam_identity_provider_arn: The Amazon Resource Name (ARN) of an identity provider being used by an Amazon Q Business application.
        :param identity_center_instance_arn: The Amazon Resource Name (ARN) of the IAM Identity Center instance you are either creating for—or connecting to—your Amazon Q Business application. *Required* : ``Yes``
        :param identity_type: The authentication type being used by a Amazon Q Business application.
        :param personalization_configuration: Configuration information about chat response personalization. For more information, see `Personalizing chat responses <https://docs.aws.amazon.com/amazonq/latest/qbusiness-ug/personalizing-chat-responses.html>`_ .
        :param q_apps_configuration: Configuration information about Amazon Q Apps.
        :param quick_sight_configuration: The Amazon Quick Suite configuration for an Amazon Q Business application that uses Quick Suite as the identity provider.
        :param role_arn: The Amazon Resource Name (ARN) of an IAM role with permissions to access your Amazon CloudWatch logs and metrics. If this property is not specified, Amazon Q Business will create a `service linked role (SLR) <https://docs.aws.amazon.com/amazonq/latest/qbusiness-ug/using-service-linked-roles.html#slr-permissions>`_ and use it as the application's role.
        :param tags: A list of key-value pairs that identify or categorize your Amazon Q Business application. You can also use tags to help control access to the application. Tag keys and values can consist of Unicode letters, digits, white space, and any of the following symbols: _ . : / = + -

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-application.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
            
            cfn_application_mixin_props = qbusiness_mixins.CfnApplicationMixinProps(
                attachments_configuration=qbusiness_mixins.CfnApplicationPropsMixin.AttachmentsConfigurationProperty(
                    attachments_control_mode="attachmentsControlMode"
                ),
                auto_subscription_configuration=qbusiness_mixins.CfnApplicationPropsMixin.AutoSubscriptionConfigurationProperty(
                    auto_subscribe="autoSubscribe",
                    default_subscription_type="defaultSubscriptionType"
                ),
                client_ids_for_oidc=["clientIdsForOidc"],
                description="description",
                display_name="displayName",
                encryption_configuration=qbusiness_mixins.CfnApplicationPropsMixin.EncryptionConfigurationProperty(
                    kms_key_id="kmsKeyId"
                ),
                iam_identity_provider_arn="iamIdentityProviderArn",
                identity_center_instance_arn="identityCenterInstanceArn",
                identity_type="identityType",
                personalization_configuration=qbusiness_mixins.CfnApplicationPropsMixin.PersonalizationConfigurationProperty(
                    personalization_control_mode="personalizationControlMode"
                ),
                q_apps_configuration=qbusiness_mixins.CfnApplicationPropsMixin.QAppsConfigurationProperty(
                    q_apps_control_mode="qAppsControlMode"
                ),
                quick_sight_configuration=qbusiness_mixins.CfnApplicationPropsMixin.QuickSightConfigurationProperty(
                    client_namespace="clientNamespace"
                ),
                role_arn="roleArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__405e06fa15fa4362c08df578fa4de610505ca8386cedcbe2103a0b952c4d502f)
            check_type(argname="argument attachments_configuration", value=attachments_configuration, expected_type=type_hints["attachments_configuration"])
            check_type(argname="argument auto_subscription_configuration", value=auto_subscription_configuration, expected_type=type_hints["auto_subscription_configuration"])
            check_type(argname="argument client_ids_for_oidc", value=client_ids_for_oidc, expected_type=type_hints["client_ids_for_oidc"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument encryption_configuration", value=encryption_configuration, expected_type=type_hints["encryption_configuration"])
            check_type(argname="argument iam_identity_provider_arn", value=iam_identity_provider_arn, expected_type=type_hints["iam_identity_provider_arn"])
            check_type(argname="argument identity_center_instance_arn", value=identity_center_instance_arn, expected_type=type_hints["identity_center_instance_arn"])
            check_type(argname="argument identity_type", value=identity_type, expected_type=type_hints["identity_type"])
            check_type(argname="argument personalization_configuration", value=personalization_configuration, expected_type=type_hints["personalization_configuration"])
            check_type(argname="argument q_apps_configuration", value=q_apps_configuration, expected_type=type_hints["q_apps_configuration"])
            check_type(argname="argument quick_sight_configuration", value=quick_sight_configuration, expected_type=type_hints["quick_sight_configuration"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if attachments_configuration is not None:
            self._values["attachments_configuration"] = attachments_configuration
        if auto_subscription_configuration is not None:
            self._values["auto_subscription_configuration"] = auto_subscription_configuration
        if client_ids_for_oidc is not None:
            self._values["client_ids_for_oidc"] = client_ids_for_oidc
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if encryption_configuration is not None:
            self._values["encryption_configuration"] = encryption_configuration
        if iam_identity_provider_arn is not None:
            self._values["iam_identity_provider_arn"] = iam_identity_provider_arn
        if identity_center_instance_arn is not None:
            self._values["identity_center_instance_arn"] = identity_center_instance_arn
        if identity_type is not None:
            self._values["identity_type"] = identity_type
        if personalization_configuration is not None:
            self._values["personalization_configuration"] = personalization_configuration
        if q_apps_configuration is not None:
            self._values["q_apps_configuration"] = q_apps_configuration
        if quick_sight_configuration is not None:
            self._values["quick_sight_configuration"] = quick_sight_configuration
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def attachments_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.AttachmentsConfigurationProperty"]]:
        '''Configuration information for the file upload during chat feature.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-application.html#cfn-qbusiness-application-attachmentsconfiguration
        '''
        result = self._values.get("attachments_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.AttachmentsConfigurationProperty"]], result)

    @builtins.property
    def auto_subscription_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.AutoSubscriptionConfigurationProperty"]]:
        '''Subscription configuration information for an Amazon Q Business application using IAM identity federation for user management.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-application.html#cfn-qbusiness-application-autosubscriptionconfiguration
        '''
        result = self._values.get("auto_subscription_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.AutoSubscriptionConfigurationProperty"]], result)

    @builtins.property
    def client_ids_for_oidc(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The OIDC client ID for a Amazon Q Business application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-application.html#cfn-qbusiness-application-clientidsforoidc
        '''
        result = self._values.get("client_ids_for_oidc")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the Amazon Q Business application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-application.html#cfn-qbusiness-application-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Amazon Q Business application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-application.html#cfn-qbusiness-application-displayname
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.EncryptionConfigurationProperty"]]:
        '''Provides the identifier of the AWS  key used to encrypt data indexed by Amazon Q Business.

        Amazon Q Business doesn't support asymmetric keys.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-application.html#cfn-qbusiness-application-encryptionconfiguration
        '''
        result = self._values.get("encryption_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.EncryptionConfigurationProperty"]], result)

    @builtins.property
    def iam_identity_provider_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of an identity provider being used by an Amazon Q Business application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-application.html#cfn-qbusiness-application-iamidentityproviderarn
        '''
        result = self._values.get("iam_identity_provider_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_center_instance_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the IAM Identity Center instance you are either creating for—or connecting to—your Amazon Q Business application.

        *Required* : ``Yes``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-application.html#cfn-qbusiness-application-identitycenterinstancearn
        '''
        result = self._values.get("identity_center_instance_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_type(self) -> typing.Optional[builtins.str]:
        '''The authentication type being used by a Amazon Q Business application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-application.html#cfn-qbusiness-application-identitytype
        '''
        result = self._values.get("identity_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def personalization_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.PersonalizationConfigurationProperty"]]:
        '''Configuration information about chat response personalization.

        For more information, see `Personalizing chat responses <https://docs.aws.amazon.com/amazonq/latest/qbusiness-ug/personalizing-chat-responses.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-application.html#cfn-qbusiness-application-personalizationconfiguration
        '''
        result = self._values.get("personalization_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.PersonalizationConfigurationProperty"]], result)

    @builtins.property
    def q_apps_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.QAppsConfigurationProperty"]]:
        '''Configuration information about Amazon Q Apps.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-application.html#cfn-qbusiness-application-qappsconfiguration
        '''
        result = self._values.get("q_apps_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.QAppsConfigurationProperty"]], result)

    @builtins.property
    def quick_sight_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.QuickSightConfigurationProperty"]]:
        '''The Amazon Quick Suite configuration for an Amazon Q Business application that uses Quick Suite as the identity provider.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-application.html#cfn-qbusiness-application-quicksightconfiguration
        '''
        result = self._values.get("quick_sight_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.QuickSightConfigurationProperty"]], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of an IAM role with permissions to access your Amazon CloudWatch logs and metrics.

        If this property is not specified, Amazon Q Business will create a `service linked role (SLR) <https://docs.aws.amazon.com/amazonq/latest/qbusiness-ug/using-service-linked-roles.html#slr-permissions>`_ and use it as the application's role.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-application.html#cfn-qbusiness-application-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of key-value pairs that identify or categorize your Amazon Q Business application.

        You can also use tags to help control access to the application. Tag keys and values can consist of Unicode letters, digits, white space, and any of the following symbols: _ . : / = + -

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-application.html#cfn-qbusiness-application-tags
        :: .
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnApplicationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnApplicationPropsMixin",
):
    '''Creates an Amazon Q Business application.

    .. epigraph::

       There are new tiers for Amazon Q Business. Not all features in Amazon Q Business Pro are also available in Amazon Q Business Lite. For information on what's included in Amazon Q Business Lite and what's included in Amazon Q Business Pro, see `Amazon Q Business tiers <https://docs.aws.amazon.com/amazonq/latest/qbusiness-ug/tiers.html#user-sub-tiers>`_ . You must use the Amazon Q Business console to assign subscription tiers to users.

       An Amazon Q Apps service linked role will be created if it's absent in the AWS account when ``QAppsConfiguration`` is enabled in the request. For more information, see `Using service-linked roles for Q Apps <https://docs.aws.amazon.com/amazonq/latest/qbusiness-ug/using-service-linked-roles-qapps.html>`_ .

       When you create an application, Amazon Q Business may securely transmit data for processing from your selected AWS region, but within your geography. For more information, see `Cross region inference in Amazon Q Business <https://docs.aws.amazon.com/amazonq/latest/qbusiness-ug/cross-region-inference.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-application.html
    :cloudformationResource: AWS::QBusiness::Application
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
        
        cfn_application_props_mixin = qbusiness_mixins.CfnApplicationPropsMixin(qbusiness_mixins.CfnApplicationMixinProps(
            attachments_configuration=qbusiness_mixins.CfnApplicationPropsMixin.AttachmentsConfigurationProperty(
                attachments_control_mode="attachmentsControlMode"
            ),
            auto_subscription_configuration=qbusiness_mixins.CfnApplicationPropsMixin.AutoSubscriptionConfigurationProperty(
                auto_subscribe="autoSubscribe",
                default_subscription_type="defaultSubscriptionType"
            ),
            client_ids_for_oidc=["clientIdsForOidc"],
            description="description",
            display_name="displayName",
            encryption_configuration=qbusiness_mixins.CfnApplicationPropsMixin.EncryptionConfigurationProperty(
                kms_key_id="kmsKeyId"
            ),
            iam_identity_provider_arn="iamIdentityProviderArn",
            identity_center_instance_arn="identityCenterInstanceArn",
            identity_type="identityType",
            personalization_configuration=qbusiness_mixins.CfnApplicationPropsMixin.PersonalizationConfigurationProperty(
                personalization_control_mode="personalizationControlMode"
            ),
            q_apps_configuration=qbusiness_mixins.CfnApplicationPropsMixin.QAppsConfigurationProperty(
                q_apps_control_mode="qAppsControlMode"
            ),
            quick_sight_configuration=qbusiness_mixins.CfnApplicationPropsMixin.QuickSightConfigurationProperty(
                client_namespace="clientNamespace"
            ),
            role_arn="roleArn",
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
        props: typing.Union[CfnApplicationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::QBusiness::Application``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a35eb1c6fadef94000cb27322ac411e04a4e13c389fa34f6855ed1c645c7379f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__85d49ed171be1cf1816b09e9f7cf1fe7ce45ffd2802657a154b40d57a3428052)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d0c5da74f1fb60550797988c1262828607d125f7194dfeae5361dd6cc32d0b7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnApplicationMixinProps:
        return typing.cast(CfnApplicationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnApplicationPropsMixin.AttachmentsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"attachments_control_mode": "attachmentsControlMode"},
    )
    class AttachmentsConfigurationProperty:
        def __init__(
            self,
            *,
            attachments_control_mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration information for the file upload during chat feature.

            :param attachments_control_mode: Status information about whether file upload functionality is activated or deactivated for your end user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-application-attachmentsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
                
                attachments_configuration_property = qbusiness_mixins.CfnApplicationPropsMixin.AttachmentsConfigurationProperty(
                    attachments_control_mode="attachmentsControlMode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5e7db48e1f3960a32e62df24d8d2b72a47a8af41af28535456be1af9f3238198)
                check_type(argname="argument attachments_control_mode", value=attachments_control_mode, expected_type=type_hints["attachments_control_mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attachments_control_mode is not None:
                self._values["attachments_control_mode"] = attachments_control_mode

        @builtins.property
        def attachments_control_mode(self) -> typing.Optional[builtins.str]:
            '''Status information about whether file upload functionality is activated or deactivated for your end user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-application-attachmentsconfiguration.html#cfn-qbusiness-application-attachmentsconfiguration-attachmentscontrolmode
            '''
            result = self._values.get("attachments_control_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AttachmentsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnApplicationPropsMixin.AutoSubscriptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "auto_subscribe": "autoSubscribe",
            "default_subscription_type": "defaultSubscriptionType",
        },
    )
    class AutoSubscriptionConfigurationProperty:
        def __init__(
            self,
            *,
            auto_subscribe: typing.Optional[builtins.str] = None,
            default_subscription_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Subscription configuration information for an Amazon Q Business application using IAM identity federation for user management.

            :param auto_subscribe: Describes whether automatic subscriptions are enabled for an Amazon Q Business application using IAM identity federation for user management.
            :param default_subscription_type: Describes the default subscription type assigned to an Amazon Q Business application using IAM identity federation for user management. If the value for ``autoSubscribe`` is set to ``ENABLED`` you must select a value for this field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-application-autosubscriptionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
                
                auto_subscription_configuration_property = qbusiness_mixins.CfnApplicationPropsMixin.AutoSubscriptionConfigurationProperty(
                    auto_subscribe="autoSubscribe",
                    default_subscription_type="defaultSubscriptionType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2a73a656b57077448cc8042722e6ce38ce33ec8001083a6147bad543a77c1080)
                check_type(argname="argument auto_subscribe", value=auto_subscribe, expected_type=type_hints["auto_subscribe"])
                check_type(argname="argument default_subscription_type", value=default_subscription_type, expected_type=type_hints["default_subscription_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auto_subscribe is not None:
                self._values["auto_subscribe"] = auto_subscribe
            if default_subscription_type is not None:
                self._values["default_subscription_type"] = default_subscription_type

        @builtins.property
        def auto_subscribe(self) -> typing.Optional[builtins.str]:
            '''Describes whether automatic subscriptions are enabled for an Amazon Q Business application using IAM identity federation for user management.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-application-autosubscriptionconfiguration.html#cfn-qbusiness-application-autosubscriptionconfiguration-autosubscribe
            '''
            result = self._values.get("auto_subscribe")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def default_subscription_type(self) -> typing.Optional[builtins.str]:
            '''Describes the default subscription type assigned to an Amazon Q Business application using IAM identity federation for user management.

            If the value for ``autoSubscribe`` is set to ``ENABLED`` you must select a value for this field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-application-autosubscriptionconfiguration.html#cfn-qbusiness-application-autosubscriptionconfiguration-defaultsubscriptiontype
            '''
            result = self._values.get("default_subscription_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AutoSubscriptionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnApplicationPropsMixin.EncryptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"kms_key_id": "kmsKeyId"},
    )
    class EncryptionConfigurationProperty:
        def __init__(self, *, kms_key_id: typing.Optional[builtins.str] = None) -> None:
            '''Provides the identifier of the AWS  key used to encrypt data indexed by Amazon Q Business.

            Amazon Q Business doesn't support asymmetric keys.

            :param kms_key_id: The identifier of the AWS key. Amazon Q Business doesn't support asymmetric keys.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-application-encryptionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
                
                encryption_configuration_property = qbusiness_mixins.CfnApplicationPropsMixin.EncryptionConfigurationProperty(
                    kms_key_id="kmsKeyId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5acf4619d8867aa4b9983b194bb4c7f5eba797613b793130f287ecc8b6579304)
                check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kms_key_id is not None:
                self._values["kms_key_id"] = kms_key_id

        @builtins.property
        def kms_key_id(self) -> typing.Optional[builtins.str]:
            '''The identifier of the AWS  key.

            Amazon Q Business doesn't support asymmetric keys.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-application-encryptionconfiguration.html#cfn-qbusiness-application-encryptionconfiguration-kmskeyid
            '''
            result = self._values.get("kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnApplicationPropsMixin.PersonalizationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"personalization_control_mode": "personalizationControlMode"},
    )
    class PersonalizationConfigurationProperty:
        def __init__(
            self,
            *,
            personalization_control_mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration information about chat response personalization.

            For more information, see `Personalizing chat responses <https://docs.aws.amazon.com/amazonq/latest/qbusiness-ug/personalizing-chat-responses.html>`_ .

            :param personalization_control_mode: An option to allow Amazon Q Business to customize chat responses using user specific metadata—specifically, location and job information—in your IAM Identity Center instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-application-personalizationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
                
                personalization_configuration_property = qbusiness_mixins.CfnApplicationPropsMixin.PersonalizationConfigurationProperty(
                    personalization_control_mode="personalizationControlMode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a46aeecd8fd69ab94e629df1df3e0025e1dec0bed8e94c5b8877c8b1610db528)
                check_type(argname="argument personalization_control_mode", value=personalization_control_mode, expected_type=type_hints["personalization_control_mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if personalization_control_mode is not None:
                self._values["personalization_control_mode"] = personalization_control_mode

        @builtins.property
        def personalization_control_mode(self) -> typing.Optional[builtins.str]:
            '''An option to allow Amazon Q Business to customize chat responses using user specific metadata—specifically, location and job information—in your IAM Identity Center instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-application-personalizationconfiguration.html#cfn-qbusiness-application-personalizationconfiguration-personalizationcontrolmode
            '''
            result = self._values.get("personalization_control_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PersonalizationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnApplicationPropsMixin.QAppsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"q_apps_control_mode": "qAppsControlMode"},
    )
    class QAppsConfigurationProperty:
        def __init__(
            self,
            *,
            q_apps_control_mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration information about Amazon Q Apps.

            :param q_apps_control_mode: Status information about whether end users can create and use Amazon Q Apps in the web experience.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-application-qappsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
                
                q_apps_configuration_property = qbusiness_mixins.CfnApplicationPropsMixin.QAppsConfigurationProperty(
                    q_apps_control_mode="qAppsControlMode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__252b2166d0ae705554ffa78ea3cf67cee03dbda04f2101239160a5dc11b34227)
                check_type(argname="argument q_apps_control_mode", value=q_apps_control_mode, expected_type=type_hints["q_apps_control_mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if q_apps_control_mode is not None:
                self._values["q_apps_control_mode"] = q_apps_control_mode

        @builtins.property
        def q_apps_control_mode(self) -> typing.Optional[builtins.str]:
            '''Status information about whether end users can create and use Amazon Q Apps in the web experience.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-application-qappsconfiguration.html#cfn-qbusiness-application-qappsconfiguration-qappscontrolmode
            '''
            result = self._values.get("q_apps_control_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QAppsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnApplicationPropsMixin.QuickSightConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"client_namespace": "clientNamespace"},
    )
    class QuickSightConfigurationProperty:
        def __init__(
            self,
            *,
            client_namespace: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The Amazon Quick Suite configuration for an Amazon Q Business application that uses Quick Suite as the identity provider.

            For more information, see `Creating an Amazon Quick Suite integrated application <https://docs.aws.amazon.com/amazonq/latest/qbusiness-ug/create-quicksight-integrated-application.html>`_ .

            :param client_namespace: The Amazon Quick Suite namespace that is used as the identity provider. For more information about Quick Suite namespaces, see `Namespace operations <https://docs.aws.amazon.com/quicksight/latest/developerguide/namespace-operations.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-application-quicksightconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
                
                quick_sight_configuration_property = qbusiness_mixins.CfnApplicationPropsMixin.QuickSightConfigurationProperty(
                    client_namespace="clientNamespace"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2400f1e6df36d8fcb39e114003e364561a84867c505daa3724eb07879d3e3cd6)
                check_type(argname="argument client_namespace", value=client_namespace, expected_type=type_hints["client_namespace"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if client_namespace is not None:
                self._values["client_namespace"] = client_namespace

        @builtins.property
        def client_namespace(self) -> typing.Optional[builtins.str]:
            '''The Amazon Quick Suite namespace that is used as the identity provider.

            For more information about Quick Suite namespaces, see `Namespace operations <https://docs.aws.amazon.com/quicksight/latest/developerguide/namespace-operations.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-application-quicksightconfiguration.html#cfn-qbusiness-application-quicksightconfiguration-clientnamespace
            '''
            result = self._values.get("client_namespace")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QuickSightConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


class CfnApplicationSyncJobLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnApplicationSyncJobLogs",
):
    '''Builder for CfnApplicationLogsMixin to generate SYNC_JOB_LOGS for CfnApplication.

    :cloudformationResource: AWS::QBusiness::Application
    :logType: SYNC_JOB_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
        
        cfn_application_sync_job_logs = qbusiness_mixins.CfnApplicationSyncJobLogs()
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
    ) -> CfnApplicationLogsMixin:
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7c853e432127afc1e5b7e60825df1729a6e13477c1049de8aa9dbf3e09b4a5c)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast(CfnApplicationLogsMixin, jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> CfnApplicationLogsMixin:
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a7988e4f14e0dbf66a558d4f53f2b1e80e6c64e86c51534a75311fb9dc1f0f2)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast(CfnApplicationLogsMixin, jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> CfnApplicationLogsMixin:
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37f3f8f9a207e71e32c156240352cd9b1b3081f399d986bb2401c056e3110caa)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast(CfnApplicationLogsMixin, jsii.invoke(self, "toS3", [bucket]))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnDataAccessorMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "action_configurations": "actionConfigurations",
        "application_id": "applicationId",
        "authentication_detail": "authenticationDetail",
        "display_name": "displayName",
        "principal": "principal",
        "tags": "tags",
    },
)
class CfnDataAccessorMixinProps:
    def __init__(
        self,
        *,
        action_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataAccessorPropsMixin.ActionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        application_id: typing.Optional[builtins.str] = None,
        authentication_detail: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataAccessorPropsMixin.DataAccessorAuthenticationDetailProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        display_name: typing.Optional[builtins.str] = None,
        principal: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDataAccessorPropsMixin.

        :param action_configurations: A list of action configurations specifying the allowed actions and any associated filters.
        :param application_id: The unique identifier of the Amazon Q Business application.
        :param authentication_detail: The authentication configuration details for the data accessor. This specifies how the ISV authenticates when accessing data through this data accessor.
        :param display_name: The friendly name of the data accessor.
        :param principal: The Amazon Resource Name (ARN) of the IAM role for the ISV associated with this data accessor.
        :param tags: The tags to associate with the data accessor.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-dataaccessor.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
            
            # attribute_filter_property_: qbusiness_mixins.CfnDataAccessorPropsMixin.AttributeFilterProperty
            
            cfn_data_accessor_mixin_props = qbusiness_mixins.CfnDataAccessorMixinProps(
                action_configurations=[qbusiness_mixins.CfnDataAccessorPropsMixin.ActionConfigurationProperty(
                    action="action",
                    filter_configuration=qbusiness_mixins.CfnDataAccessorPropsMixin.ActionFilterConfigurationProperty(
                        document_attribute_filter=qbusiness_mixins.CfnDataAccessorPropsMixin.AttributeFilterProperty(
                            and_all_filters=[attribute_filter_property_],
                            contains_all=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeProperty(
                                name="name",
                                value=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeValueProperty(
                                    date_value="dateValue",
                                    long_value=123,
                                    string_list_value=["stringListValue"],
                                    string_value="stringValue"
                                )
                            ),
                            contains_any=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeProperty(
                                name="name",
                                value=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeValueProperty(
                                    date_value="dateValue",
                                    long_value=123,
                                    string_list_value=["stringListValue"],
                                    string_value="stringValue"
                                )
                            ),
                            equals_to=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeProperty(
                                name="name",
                                value=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeValueProperty(
                                    date_value="dateValue",
                                    long_value=123,
                                    string_list_value=["stringListValue"],
                                    string_value="stringValue"
                                )
                            ),
                            greater_than=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeProperty(
                                name="name",
                                value=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeValueProperty(
                                    date_value="dateValue",
                                    long_value=123,
                                    string_list_value=["stringListValue"],
                                    string_value="stringValue"
                                )
                            ),
                            greater_than_or_equals=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeProperty(
                                name="name",
                                value=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeValueProperty(
                                    date_value="dateValue",
                                    long_value=123,
                                    string_list_value=["stringListValue"],
                                    string_value="stringValue"
                                )
                            ),
                            less_than=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeProperty(
                                name="name",
                                value=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeValueProperty(
                                    date_value="dateValue",
                                    long_value=123,
                                    string_list_value=["stringListValue"],
                                    string_value="stringValue"
                                )
                            ),
                            less_than_or_equals=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeProperty(
                                name="name",
                                value=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeValueProperty(
                                    date_value="dateValue",
                                    long_value=123,
                                    string_list_value=["stringListValue"],
                                    string_value="stringValue"
                                )
                            ),
                            not_filter=attribute_filter_property_,
                            or_all_filters=[attribute_filter_property_]
                        )
                    )
                )],
                application_id="applicationId",
                authentication_detail=qbusiness_mixins.CfnDataAccessorPropsMixin.DataAccessorAuthenticationDetailProperty(
                    authentication_configuration=qbusiness_mixins.CfnDataAccessorPropsMixin.DataAccessorAuthenticationConfigurationProperty(
                        idc_trusted_token_issuer_configuration=qbusiness_mixins.CfnDataAccessorPropsMixin.DataAccessorIdcTrustedTokenIssuerConfigurationProperty(
                            idc_trusted_token_issuer_arn="idcTrustedTokenIssuerArn"
                        )
                    ),
                    authentication_type="authenticationType",
                    external_ids=["externalIds"]
                ),
                display_name="displayName",
                principal="principal",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a09653529779915f6e67bbe15fdba5c486ede4580785cb5c5647180f4f660322)
            check_type(argname="argument action_configurations", value=action_configurations, expected_type=type_hints["action_configurations"])
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument authentication_detail", value=authentication_detail, expected_type=type_hints["authentication_detail"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action_configurations is not None:
            self._values["action_configurations"] = action_configurations
        if application_id is not None:
            self._values["application_id"] = application_id
        if authentication_detail is not None:
            self._values["authentication_detail"] = authentication_detail
        if display_name is not None:
            self._values["display_name"] = display_name
        if principal is not None:
            self._values["principal"] = principal
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def action_configurations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataAccessorPropsMixin.ActionConfigurationProperty"]]]]:
        '''A list of action configurations specifying the allowed actions and any associated filters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-dataaccessor.html#cfn-qbusiness-dataaccessor-actionconfigurations
        '''
        result = self._values.get("action_configurations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataAccessorPropsMixin.ActionConfigurationProperty"]]]], result)

    @builtins.property
    def application_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the Amazon Q Business application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-dataaccessor.html#cfn-qbusiness-dataaccessor-applicationid
        '''
        result = self._values.get("application_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authentication_detail(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataAccessorPropsMixin.DataAccessorAuthenticationDetailProperty"]]:
        '''The authentication configuration details for the data accessor.

        This specifies how the ISV authenticates when accessing data through this data accessor.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-dataaccessor.html#cfn-qbusiness-dataaccessor-authenticationdetail
        '''
        result = self._values.get("authentication_detail")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataAccessorPropsMixin.DataAccessorAuthenticationDetailProperty"]], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The friendly name of the data accessor.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-dataaccessor.html#cfn-qbusiness-dataaccessor-displayname
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def principal(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the IAM role for the ISV associated with this data accessor.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-dataaccessor.html#cfn-qbusiness-dataaccessor-principal
        '''
        result = self._values.get("principal")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags to associate with the data accessor.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-dataaccessor.html#cfn-qbusiness-dataaccessor-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDataAccessorMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDataAccessorPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnDataAccessorPropsMixin",
):
    '''Creates a new data accessor for an ISV to access data from a Amazon Q Business application.

    The data accessor is an entity that represents the ISV's access to the Amazon Q Business application's data. It includes the IAM role ARN for the ISV, a friendly name, and a set of action configurations that define the specific actions the ISV is allowed to perform and any associated data filters. When the data accessor is created, an IAM Identity Center application is also created to manage the ISV's identity and authentication for accessing the Amazon Q Business application.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-dataaccessor.html
    :cloudformationResource: AWS::QBusiness::DataAccessor
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
        
        # attribute_filter_property_: qbusiness_mixins.CfnDataAccessorPropsMixin.AttributeFilterProperty
        
        cfn_data_accessor_props_mixin = qbusiness_mixins.CfnDataAccessorPropsMixin(qbusiness_mixins.CfnDataAccessorMixinProps(
            action_configurations=[qbusiness_mixins.CfnDataAccessorPropsMixin.ActionConfigurationProperty(
                action="action",
                filter_configuration=qbusiness_mixins.CfnDataAccessorPropsMixin.ActionFilterConfigurationProperty(
                    document_attribute_filter=qbusiness_mixins.CfnDataAccessorPropsMixin.AttributeFilterProperty(
                        and_all_filters=[attribute_filter_property_],
                        contains_all=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeProperty(
                            name="name",
                            value=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeValueProperty(
                                date_value="dateValue",
                                long_value=123,
                                string_list_value=["stringListValue"],
                                string_value="stringValue"
                            )
                        ),
                        contains_any=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeProperty(
                            name="name",
                            value=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeValueProperty(
                                date_value="dateValue",
                                long_value=123,
                                string_list_value=["stringListValue"],
                                string_value="stringValue"
                            )
                        ),
                        equals_to=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeProperty(
                            name="name",
                            value=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeValueProperty(
                                date_value="dateValue",
                                long_value=123,
                                string_list_value=["stringListValue"],
                                string_value="stringValue"
                            )
                        ),
                        greater_than=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeProperty(
                            name="name",
                            value=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeValueProperty(
                                date_value="dateValue",
                                long_value=123,
                                string_list_value=["stringListValue"],
                                string_value="stringValue"
                            )
                        ),
                        greater_than_or_equals=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeProperty(
                            name="name",
                            value=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeValueProperty(
                                date_value="dateValue",
                                long_value=123,
                                string_list_value=["stringListValue"],
                                string_value="stringValue"
                            )
                        ),
                        less_than=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeProperty(
                            name="name",
                            value=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeValueProperty(
                                date_value="dateValue",
                                long_value=123,
                                string_list_value=["stringListValue"],
                                string_value="stringValue"
                            )
                        ),
                        less_than_or_equals=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeProperty(
                            name="name",
                            value=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeValueProperty(
                                date_value="dateValue",
                                long_value=123,
                                string_list_value=["stringListValue"],
                                string_value="stringValue"
                            )
                        ),
                        not_filter=attribute_filter_property_,
                        or_all_filters=[attribute_filter_property_]
                    )
                )
            )],
            application_id="applicationId",
            authentication_detail=qbusiness_mixins.CfnDataAccessorPropsMixin.DataAccessorAuthenticationDetailProperty(
                authentication_configuration=qbusiness_mixins.CfnDataAccessorPropsMixin.DataAccessorAuthenticationConfigurationProperty(
                    idc_trusted_token_issuer_configuration=qbusiness_mixins.CfnDataAccessorPropsMixin.DataAccessorIdcTrustedTokenIssuerConfigurationProperty(
                        idc_trusted_token_issuer_arn="idcTrustedTokenIssuerArn"
                    )
                ),
                authentication_type="authenticationType",
                external_ids=["externalIds"]
            ),
            display_name="displayName",
            principal="principal",
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
        props: typing.Union[CfnDataAccessorMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::QBusiness::DataAccessor``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58da3fe90207ca823347a3df6367aba9b262e992df83060e34ea693bffe5d02c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__13d4fa13814f6bc79c00168a7b8785679a90b43d1629dd52d33cc886646d546c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bcb5bfa0de17bc5b08ee8c12a8e85f83f95e5026e282671cd6330da5df11a59)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDataAccessorMixinProps:
        return typing.cast(CfnDataAccessorMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnDataAccessorPropsMixin.ActionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "filter_configuration": "filterConfiguration",
        },
    )
    class ActionConfigurationProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[builtins.str] = None,
            filter_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataAccessorPropsMixin.ActionFilterConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies an allowed action and its associated filter configuration.

            :param action: The Amazon Q Business action that is allowed.
            :param filter_configuration: The filter configuration for the action, if any.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-dataaccessor-actionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
                
                # attribute_filter_property_: qbusiness_mixins.CfnDataAccessorPropsMixin.AttributeFilterProperty
                
                action_configuration_property = qbusiness_mixins.CfnDataAccessorPropsMixin.ActionConfigurationProperty(
                    action="action",
                    filter_configuration=qbusiness_mixins.CfnDataAccessorPropsMixin.ActionFilterConfigurationProperty(
                        document_attribute_filter=qbusiness_mixins.CfnDataAccessorPropsMixin.AttributeFilterProperty(
                            and_all_filters=[attribute_filter_property_],
                            contains_all=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeProperty(
                                name="name",
                                value=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeValueProperty(
                                    date_value="dateValue",
                                    long_value=123,
                                    string_list_value=["stringListValue"],
                                    string_value="stringValue"
                                )
                            ),
                            contains_any=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeProperty(
                                name="name",
                                value=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeValueProperty(
                                    date_value="dateValue",
                                    long_value=123,
                                    string_list_value=["stringListValue"],
                                    string_value="stringValue"
                                )
                            ),
                            equals_to=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeProperty(
                                name="name",
                                value=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeValueProperty(
                                    date_value="dateValue",
                                    long_value=123,
                                    string_list_value=["stringListValue"],
                                    string_value="stringValue"
                                )
                            ),
                            greater_than=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeProperty(
                                name="name",
                                value=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeValueProperty(
                                    date_value="dateValue",
                                    long_value=123,
                                    string_list_value=["stringListValue"],
                                    string_value="stringValue"
                                )
                            ),
                            greater_than_or_equals=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeProperty(
                                name="name",
                                value=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeValueProperty(
                                    date_value="dateValue",
                                    long_value=123,
                                    string_list_value=["stringListValue"],
                                    string_value="stringValue"
                                )
                            ),
                            less_than=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeProperty(
                                name="name",
                                value=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeValueProperty(
                                    date_value="dateValue",
                                    long_value=123,
                                    string_list_value=["stringListValue"],
                                    string_value="stringValue"
                                )
                            ),
                            less_than_or_equals=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeProperty(
                                name="name",
                                value=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeValueProperty(
                                    date_value="dateValue",
                                    long_value=123,
                                    string_list_value=["stringListValue"],
                                    string_value="stringValue"
                                )
                            ),
                            not_filter=attribute_filter_property_,
                            or_all_filters=[attribute_filter_property_]
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__079392577f866c15fb7027c29e65e74a02e717973bd2a5c084ac04703e61d4e7)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument filter_configuration", value=filter_configuration, expected_type=type_hints["filter_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if filter_configuration is not None:
                self._values["filter_configuration"] = filter_configuration

        @builtins.property
        def action(self) -> typing.Optional[builtins.str]:
            '''The Amazon Q Business action that is allowed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-dataaccessor-actionconfiguration.html#cfn-qbusiness-dataaccessor-actionconfiguration-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def filter_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataAccessorPropsMixin.ActionFilterConfigurationProperty"]]:
            '''The filter configuration for the action, if any.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-dataaccessor-actionconfiguration.html#cfn-qbusiness-dataaccessor-actionconfiguration-filterconfiguration
            '''
            result = self._values.get("filter_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataAccessorPropsMixin.ActionFilterConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnDataAccessorPropsMixin.ActionFilterConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"document_attribute_filter": "documentAttributeFilter"},
    )
    class ActionFilterConfigurationProperty:
        def __init__(
            self,
            *,
            document_attribute_filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataAccessorPropsMixin.AttributeFilterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies filters to apply to an allowed action.

            :param document_attribute_filter: Enables filtering of responses based on document attributes or metadata fields.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-dataaccessor-actionfilterconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
                
                # attribute_filter_property_: qbusiness_mixins.CfnDataAccessorPropsMixin.AttributeFilterProperty
                
                action_filter_configuration_property = qbusiness_mixins.CfnDataAccessorPropsMixin.ActionFilterConfigurationProperty(
                    document_attribute_filter=qbusiness_mixins.CfnDataAccessorPropsMixin.AttributeFilterProperty(
                        and_all_filters=[attribute_filter_property_],
                        contains_all=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeProperty(
                            name="name",
                            value=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeValueProperty(
                                date_value="dateValue",
                                long_value=123,
                                string_list_value=["stringListValue"],
                                string_value="stringValue"
                            )
                        ),
                        contains_any=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeProperty(
                            name="name",
                            value=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeValueProperty(
                                date_value="dateValue",
                                long_value=123,
                                string_list_value=["stringListValue"],
                                string_value="stringValue"
                            )
                        ),
                        equals_to=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeProperty(
                            name="name",
                            value=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeValueProperty(
                                date_value="dateValue",
                                long_value=123,
                                string_list_value=["stringListValue"],
                                string_value="stringValue"
                            )
                        ),
                        greater_than=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeProperty(
                            name="name",
                            value=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeValueProperty(
                                date_value="dateValue",
                                long_value=123,
                                string_list_value=["stringListValue"],
                                string_value="stringValue"
                            )
                        ),
                        greater_than_or_equals=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeProperty(
                            name="name",
                            value=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeValueProperty(
                                date_value="dateValue",
                                long_value=123,
                                string_list_value=["stringListValue"],
                                string_value="stringValue"
                            )
                        ),
                        less_than=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeProperty(
                            name="name",
                            value=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeValueProperty(
                                date_value="dateValue",
                                long_value=123,
                                string_list_value=["stringListValue"],
                                string_value="stringValue"
                            )
                        ),
                        less_than_or_equals=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeProperty(
                            name="name",
                            value=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeValueProperty(
                                date_value="dateValue",
                                long_value=123,
                                string_list_value=["stringListValue"],
                                string_value="stringValue"
                            )
                        ),
                        not_filter=attribute_filter_property_,
                        or_all_filters=[attribute_filter_property_]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c971fab1ef7478a15d9fe4886bdffe97f92072003ccd789ad0f03ffd381a2ac2)
                check_type(argname="argument document_attribute_filter", value=document_attribute_filter, expected_type=type_hints["document_attribute_filter"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if document_attribute_filter is not None:
                self._values["document_attribute_filter"] = document_attribute_filter

        @builtins.property
        def document_attribute_filter(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataAccessorPropsMixin.AttributeFilterProperty"]]:
            '''Enables filtering of responses based on document attributes or metadata fields.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-dataaccessor-actionfilterconfiguration.html#cfn-qbusiness-dataaccessor-actionfilterconfiguration-documentattributefilter
            '''
            result = self._values.get("document_attribute_filter")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataAccessorPropsMixin.AttributeFilterProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionFilterConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnDataAccessorPropsMixin.AttributeFilterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "and_all_filters": "andAllFilters",
            "contains_all": "containsAll",
            "contains_any": "containsAny",
            "equals_to": "equalsTo",
            "greater_than": "greaterThan",
            "greater_than_or_equals": "greaterThanOrEquals",
            "less_than": "lessThan",
            "less_than_or_equals": "lessThanOrEquals",
            "not_filter": "notFilter",
            "or_all_filters": "orAllFilters",
        },
    )
    class AttributeFilterProperty:
        def __init__(
            self,
            *,
            and_all_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataAccessorPropsMixin.AttributeFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            contains_all: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataAccessorPropsMixin.DocumentAttributeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            contains_any: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataAccessorPropsMixin.DocumentAttributeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            equals_to: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataAccessorPropsMixin.DocumentAttributeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            greater_than: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataAccessorPropsMixin.DocumentAttributeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            greater_than_or_equals: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataAccessorPropsMixin.DocumentAttributeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            less_than: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataAccessorPropsMixin.DocumentAttributeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            less_than_or_equals: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataAccessorPropsMixin.DocumentAttributeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            not_filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataAccessorPropsMixin.AttributeFilterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            or_all_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataAccessorPropsMixin.AttributeFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Enables filtering of responses based on document attributes or metadata fields.

            :param and_all_filters: Performs a logical ``AND`` operation on all supplied filters.
            :param contains_all: Returns ``true`` when a document contains all the specified document attributes or metadata fields. Supported for the following `document attribute value types <https://docs.aws.amazon.com/amazonq/latest/api-reference/API_DocumentAttributeValue.html>`_ : ``stringListValue`` .
            :param contains_any: Returns ``true`` when a document contains any of the specified document attributes or metadata fields. Supported for the following `document attribute value types <https://docs.aws.amazon.com/amazonq/latest/api-reference/API_DocumentAttributeValue.html>`_ : ``stringListValue`` .
            :param equals_to: Performs an equals operation on two document attributes or metadata fields. Supported for the following `document attribute value types <https://docs.aws.amazon.com/amazonq/latest/api-reference/API_DocumentAttributeValue.html>`_ : ``dateValue`` , ``longValue`` , ``stringListValue`` and ``stringValue`` .
            :param greater_than: Performs a greater than operation on two document attributes or metadata fields. Supported for the following `document attribute value types <https://docs.aws.amazon.com/amazonq/latest/api-reference/API_DocumentAttributeValue.html>`_ : ``dateValue`` and ``longValue`` .
            :param greater_than_or_equals: Performs a greater or equals than operation on two document attributes or metadata fields. Supported for the following `document attribute value types <https://docs.aws.amazon.com/amazonq/latest/api-reference/API_DocumentAttributeValue.html>`_ : ``dateValue`` and ``longValue`` .
            :param less_than: Performs a less than operation on two document attributes or metadata fields. Supported for the following `document attribute value types <https://docs.aws.amazon.com/amazonq/latest/api-reference/API_DocumentAttributeValue.html>`_ : ``dateValue`` and ``longValue`` .
            :param less_than_or_equals: Performs a less than or equals operation on two document attributes or metadata fields.Supported for the following `document attribute value type <https://docs.aws.amazon.com/amazonq/latest/api-reference/API_DocumentAttributeValue.html>`_ : ``dateValue`` and ``longValue`` .
            :param not_filter: Performs a logical ``NOT`` operation on all supplied filters.
            :param or_all_filters: Performs a logical ``OR`` operation on all supplied filters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-dataaccessor-attributefilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
                
                # attribute_filter_property_: qbusiness_mixins.CfnDataAccessorPropsMixin.AttributeFilterProperty
                
                attribute_filter_property = qbusiness_mixins.CfnDataAccessorPropsMixin.AttributeFilterProperty(
                    and_all_filters=[attribute_filter_property_],
                    contains_all=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeProperty(
                        name="name",
                        value=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeValueProperty(
                            date_value="dateValue",
                            long_value=123,
                            string_list_value=["stringListValue"],
                            string_value="stringValue"
                        )
                    ),
                    contains_any=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeProperty(
                        name="name",
                        value=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeValueProperty(
                            date_value="dateValue",
                            long_value=123,
                            string_list_value=["stringListValue"],
                            string_value="stringValue"
                        )
                    ),
                    equals_to=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeProperty(
                        name="name",
                        value=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeValueProperty(
                            date_value="dateValue",
                            long_value=123,
                            string_list_value=["stringListValue"],
                            string_value="stringValue"
                        )
                    ),
                    greater_than=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeProperty(
                        name="name",
                        value=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeValueProperty(
                            date_value="dateValue",
                            long_value=123,
                            string_list_value=["stringListValue"],
                            string_value="stringValue"
                        )
                    ),
                    greater_than_or_equals=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeProperty(
                        name="name",
                        value=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeValueProperty(
                            date_value="dateValue",
                            long_value=123,
                            string_list_value=["stringListValue"],
                            string_value="stringValue"
                        )
                    ),
                    less_than=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeProperty(
                        name="name",
                        value=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeValueProperty(
                            date_value="dateValue",
                            long_value=123,
                            string_list_value=["stringListValue"],
                            string_value="stringValue"
                        )
                    ),
                    less_than_or_equals=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeProperty(
                        name="name",
                        value=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeValueProperty(
                            date_value="dateValue",
                            long_value=123,
                            string_list_value=["stringListValue"],
                            string_value="stringValue"
                        )
                    ),
                    not_filter=attribute_filter_property_,
                    or_all_filters=[attribute_filter_property_]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2559b99e1f72d226c78d14f2445a737be6e03347ec2827de36ba8d497b788b5a)
                check_type(argname="argument and_all_filters", value=and_all_filters, expected_type=type_hints["and_all_filters"])
                check_type(argname="argument contains_all", value=contains_all, expected_type=type_hints["contains_all"])
                check_type(argname="argument contains_any", value=contains_any, expected_type=type_hints["contains_any"])
                check_type(argname="argument equals_to", value=equals_to, expected_type=type_hints["equals_to"])
                check_type(argname="argument greater_than", value=greater_than, expected_type=type_hints["greater_than"])
                check_type(argname="argument greater_than_or_equals", value=greater_than_or_equals, expected_type=type_hints["greater_than_or_equals"])
                check_type(argname="argument less_than", value=less_than, expected_type=type_hints["less_than"])
                check_type(argname="argument less_than_or_equals", value=less_than_or_equals, expected_type=type_hints["less_than_or_equals"])
                check_type(argname="argument not_filter", value=not_filter, expected_type=type_hints["not_filter"])
                check_type(argname="argument or_all_filters", value=or_all_filters, expected_type=type_hints["or_all_filters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if and_all_filters is not None:
                self._values["and_all_filters"] = and_all_filters
            if contains_all is not None:
                self._values["contains_all"] = contains_all
            if contains_any is not None:
                self._values["contains_any"] = contains_any
            if equals_to is not None:
                self._values["equals_to"] = equals_to
            if greater_than is not None:
                self._values["greater_than"] = greater_than
            if greater_than_or_equals is not None:
                self._values["greater_than_or_equals"] = greater_than_or_equals
            if less_than is not None:
                self._values["less_than"] = less_than
            if less_than_or_equals is not None:
                self._values["less_than_or_equals"] = less_than_or_equals
            if not_filter is not None:
                self._values["not_filter"] = not_filter
            if or_all_filters is not None:
                self._values["or_all_filters"] = or_all_filters

        @builtins.property
        def and_all_filters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataAccessorPropsMixin.AttributeFilterProperty"]]]]:
            '''Performs a logical ``AND`` operation on all supplied filters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-dataaccessor-attributefilter.html#cfn-qbusiness-dataaccessor-attributefilter-andallfilters
            '''
            result = self._values.get("and_all_filters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataAccessorPropsMixin.AttributeFilterProperty"]]]], result)

        @builtins.property
        def contains_all(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataAccessorPropsMixin.DocumentAttributeProperty"]]:
            '''Returns ``true`` when a document contains all the specified document attributes or metadata fields.

            Supported for the following `document attribute value types <https://docs.aws.amazon.com/amazonq/latest/api-reference/API_DocumentAttributeValue.html>`_ : ``stringListValue`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-dataaccessor-attributefilter.html#cfn-qbusiness-dataaccessor-attributefilter-containsall
            '''
            result = self._values.get("contains_all")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataAccessorPropsMixin.DocumentAttributeProperty"]], result)

        @builtins.property
        def contains_any(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataAccessorPropsMixin.DocumentAttributeProperty"]]:
            '''Returns ``true`` when a document contains any of the specified document attributes or metadata fields.

            Supported for the following `document attribute value types <https://docs.aws.amazon.com/amazonq/latest/api-reference/API_DocumentAttributeValue.html>`_ : ``stringListValue`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-dataaccessor-attributefilter.html#cfn-qbusiness-dataaccessor-attributefilter-containsany
            '''
            result = self._values.get("contains_any")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataAccessorPropsMixin.DocumentAttributeProperty"]], result)

        @builtins.property
        def equals_to(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataAccessorPropsMixin.DocumentAttributeProperty"]]:
            '''Performs an equals operation on two document attributes or metadata fields.

            Supported for the following `document attribute value types <https://docs.aws.amazon.com/amazonq/latest/api-reference/API_DocumentAttributeValue.html>`_ : ``dateValue`` , ``longValue`` , ``stringListValue`` and ``stringValue`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-dataaccessor-attributefilter.html#cfn-qbusiness-dataaccessor-attributefilter-equalsto
            '''
            result = self._values.get("equals_to")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataAccessorPropsMixin.DocumentAttributeProperty"]], result)

        @builtins.property
        def greater_than(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataAccessorPropsMixin.DocumentAttributeProperty"]]:
            '''Performs a greater than operation on two document attributes or metadata fields.

            Supported for the following `document attribute value types <https://docs.aws.amazon.com/amazonq/latest/api-reference/API_DocumentAttributeValue.html>`_ : ``dateValue`` and ``longValue`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-dataaccessor-attributefilter.html#cfn-qbusiness-dataaccessor-attributefilter-greaterthan
            '''
            result = self._values.get("greater_than")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataAccessorPropsMixin.DocumentAttributeProperty"]], result)

        @builtins.property
        def greater_than_or_equals(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataAccessorPropsMixin.DocumentAttributeProperty"]]:
            '''Performs a greater or equals than operation on two document attributes or metadata fields.

            Supported for the following `document attribute value types <https://docs.aws.amazon.com/amazonq/latest/api-reference/API_DocumentAttributeValue.html>`_ : ``dateValue`` and ``longValue`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-dataaccessor-attributefilter.html#cfn-qbusiness-dataaccessor-attributefilter-greaterthanorequals
            '''
            result = self._values.get("greater_than_or_equals")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataAccessorPropsMixin.DocumentAttributeProperty"]], result)

        @builtins.property
        def less_than(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataAccessorPropsMixin.DocumentAttributeProperty"]]:
            '''Performs a less than operation on two document attributes or metadata fields.

            Supported for the following `document attribute value types <https://docs.aws.amazon.com/amazonq/latest/api-reference/API_DocumentAttributeValue.html>`_ : ``dateValue`` and ``longValue`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-dataaccessor-attributefilter.html#cfn-qbusiness-dataaccessor-attributefilter-lessthan
            '''
            result = self._values.get("less_than")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataAccessorPropsMixin.DocumentAttributeProperty"]], result)

        @builtins.property
        def less_than_or_equals(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataAccessorPropsMixin.DocumentAttributeProperty"]]:
            '''Performs a less than or equals operation on two document attributes or metadata fields.Supported for the following `document attribute value type <https://docs.aws.amazon.com/amazonq/latest/api-reference/API_DocumentAttributeValue.html>`_ : ``dateValue`` and ``longValue`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-dataaccessor-attributefilter.html#cfn-qbusiness-dataaccessor-attributefilter-lessthanorequals
            '''
            result = self._values.get("less_than_or_equals")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataAccessorPropsMixin.DocumentAttributeProperty"]], result)

        @builtins.property
        def not_filter(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataAccessorPropsMixin.AttributeFilterProperty"]]:
            '''Performs a logical ``NOT`` operation on all supplied filters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-dataaccessor-attributefilter.html#cfn-qbusiness-dataaccessor-attributefilter-notfilter
            '''
            result = self._values.get("not_filter")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataAccessorPropsMixin.AttributeFilterProperty"]], result)

        @builtins.property
        def or_all_filters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataAccessorPropsMixin.AttributeFilterProperty"]]]]:
            '''Performs a logical ``OR`` operation on all supplied filters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-dataaccessor-attributefilter.html#cfn-qbusiness-dataaccessor-attributefilter-orallfilters
            '''
            result = self._values.get("or_all_filters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataAccessorPropsMixin.AttributeFilterProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AttributeFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnDataAccessorPropsMixin.DataAccessorAuthenticationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "idc_trusted_token_issuer_configuration": "idcTrustedTokenIssuerConfiguration",
        },
    )
    class DataAccessorAuthenticationConfigurationProperty:
        def __init__(
            self,
            *,
            idc_trusted_token_issuer_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataAccessorPropsMixin.DataAccessorIdcTrustedTokenIssuerConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A union type that contains the specific authentication configuration based on the authentication type selected.

            :param idc_trusted_token_issuer_configuration: Configuration for IAM Identity Center Trusted Token Issuer (TTI) authentication used when the authentication type is ``AWS_IAM_IDC_TTI`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-dataaccessor-dataaccessorauthenticationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
                
                data_accessor_authentication_configuration_property = qbusiness_mixins.CfnDataAccessorPropsMixin.DataAccessorAuthenticationConfigurationProperty(
                    idc_trusted_token_issuer_configuration=qbusiness_mixins.CfnDataAccessorPropsMixin.DataAccessorIdcTrustedTokenIssuerConfigurationProperty(
                        idc_trusted_token_issuer_arn="idcTrustedTokenIssuerArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__04d0abd3fcfd7f606cb60c6b113fc7416cd74b5ef0d63b3c6a153eeddd5f2e0a)
                check_type(argname="argument idc_trusted_token_issuer_configuration", value=idc_trusted_token_issuer_configuration, expected_type=type_hints["idc_trusted_token_issuer_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if idc_trusted_token_issuer_configuration is not None:
                self._values["idc_trusted_token_issuer_configuration"] = idc_trusted_token_issuer_configuration

        @builtins.property
        def idc_trusted_token_issuer_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataAccessorPropsMixin.DataAccessorIdcTrustedTokenIssuerConfigurationProperty"]]:
            '''Configuration for IAM Identity Center Trusted Token Issuer (TTI) authentication used when the authentication type is ``AWS_IAM_IDC_TTI`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-dataaccessor-dataaccessorauthenticationconfiguration.html#cfn-qbusiness-dataaccessor-dataaccessorauthenticationconfiguration-idctrustedtokenissuerconfiguration
            '''
            result = self._values.get("idc_trusted_token_issuer_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataAccessorPropsMixin.DataAccessorIdcTrustedTokenIssuerConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataAccessorAuthenticationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnDataAccessorPropsMixin.DataAccessorAuthenticationDetailProperty",
        jsii_struct_bases=[],
        name_mapping={
            "authentication_configuration": "authenticationConfiguration",
            "authentication_type": "authenticationType",
            "external_ids": "externalIds",
        },
    )
    class DataAccessorAuthenticationDetailProperty:
        def __init__(
            self,
            *,
            authentication_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataAccessorPropsMixin.DataAccessorAuthenticationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            authentication_type: typing.Optional[builtins.str] = None,
            external_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Contains the authentication configuration details for a data accessor.

            This structure defines how the ISV authenticates when accessing data through the data accessor.

            :param authentication_configuration: The specific authentication configuration based on the authentication type.
            :param authentication_type: The type of authentication to use for the data accessor. This determines how the ISV authenticates when accessing data. You can use one of two authentication types: - ``AWS_IAM_IDC_TTI`` - Authentication using IAM Identity Center Trusted Token Issuer (TTI). This authentication type allows the ISV to use a trusted token issuer to generate tokens for accessing the data. - ``AWS_IAM_IDC_AUTH_CODE`` - Authentication using IAM Identity Center authorization code flow. This authentication type uses the standard OAuth 2.0 authorization code flow for authentication.
            :param external_ids: A list of external identifiers associated with this authentication configuration. These are used to correlate the data accessor with external systems.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-dataaccessor-dataaccessorauthenticationdetail.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
                
                data_accessor_authentication_detail_property = qbusiness_mixins.CfnDataAccessorPropsMixin.DataAccessorAuthenticationDetailProperty(
                    authentication_configuration=qbusiness_mixins.CfnDataAccessorPropsMixin.DataAccessorAuthenticationConfigurationProperty(
                        idc_trusted_token_issuer_configuration=qbusiness_mixins.CfnDataAccessorPropsMixin.DataAccessorIdcTrustedTokenIssuerConfigurationProperty(
                            idc_trusted_token_issuer_arn="idcTrustedTokenIssuerArn"
                        )
                    ),
                    authentication_type="authenticationType",
                    external_ids=["externalIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__66767ee46594ae7cb70c040a1aba5400c4e8eeb1bf0bf35567c0a2dba4ab8b45)
                check_type(argname="argument authentication_configuration", value=authentication_configuration, expected_type=type_hints["authentication_configuration"])
                check_type(argname="argument authentication_type", value=authentication_type, expected_type=type_hints["authentication_type"])
                check_type(argname="argument external_ids", value=external_ids, expected_type=type_hints["external_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if authentication_configuration is not None:
                self._values["authentication_configuration"] = authentication_configuration
            if authentication_type is not None:
                self._values["authentication_type"] = authentication_type
            if external_ids is not None:
                self._values["external_ids"] = external_ids

        @builtins.property
        def authentication_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataAccessorPropsMixin.DataAccessorAuthenticationConfigurationProperty"]]:
            '''The specific authentication configuration based on the authentication type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-dataaccessor-dataaccessorauthenticationdetail.html#cfn-qbusiness-dataaccessor-dataaccessorauthenticationdetail-authenticationconfiguration
            '''
            result = self._values.get("authentication_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataAccessorPropsMixin.DataAccessorAuthenticationConfigurationProperty"]], result)

        @builtins.property
        def authentication_type(self) -> typing.Optional[builtins.str]:
            '''The type of authentication to use for the data accessor.

            This determines how the ISV authenticates when accessing data. You can use one of two authentication types:

            - ``AWS_IAM_IDC_TTI`` - Authentication using IAM Identity Center Trusted Token Issuer (TTI). This authentication type allows the ISV to use a trusted token issuer to generate tokens for accessing the data.
            - ``AWS_IAM_IDC_AUTH_CODE`` - Authentication using IAM Identity Center authorization code flow. This authentication type uses the standard OAuth 2.0 authorization code flow for authentication.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-dataaccessor-dataaccessorauthenticationdetail.html#cfn-qbusiness-dataaccessor-dataaccessorauthenticationdetail-authenticationtype
            '''
            result = self._values.get("authentication_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def external_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of external identifiers associated with this authentication configuration.

            These are used to correlate the data accessor with external systems.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-dataaccessor-dataaccessorauthenticationdetail.html#cfn-qbusiness-dataaccessor-dataaccessorauthenticationdetail-externalids
            '''
            result = self._values.get("external_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataAccessorAuthenticationDetailProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnDataAccessorPropsMixin.DataAccessorIdcTrustedTokenIssuerConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"idc_trusted_token_issuer_arn": "idcTrustedTokenIssuerArn"},
    )
    class DataAccessorIdcTrustedTokenIssuerConfigurationProperty:
        def __init__(
            self,
            *,
            idc_trusted_token_issuer_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration details for IAM Identity Center Trusted Token Issuer (TTI) authentication.

            :param idc_trusted_token_issuer_arn: The Amazon Resource Name (ARN) of the IAM Identity Center Trusted Token Issuer that will be used for authentication.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-dataaccessor-dataaccessoridctrustedtokenissuerconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
                
                data_accessor_idc_trusted_token_issuer_configuration_property = qbusiness_mixins.CfnDataAccessorPropsMixin.DataAccessorIdcTrustedTokenIssuerConfigurationProperty(
                    idc_trusted_token_issuer_arn="idcTrustedTokenIssuerArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__797f50ec87c6133feb43b2e4bd210e53f1fb6e8d782e546955a53321d3bef4fb)
                check_type(argname="argument idc_trusted_token_issuer_arn", value=idc_trusted_token_issuer_arn, expected_type=type_hints["idc_trusted_token_issuer_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if idc_trusted_token_issuer_arn is not None:
                self._values["idc_trusted_token_issuer_arn"] = idc_trusted_token_issuer_arn

        @builtins.property
        def idc_trusted_token_issuer_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the IAM Identity Center Trusted Token Issuer that will be used for authentication.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-dataaccessor-dataaccessoridctrustedtokenissuerconfiguration.html#cfn-qbusiness-dataaccessor-dataaccessoridctrustedtokenissuerconfiguration-idctrustedtokenissuerarn
            '''
            result = self._values.get("idc_trusted_token_issuer_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataAccessorIdcTrustedTokenIssuerConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnDataAccessorPropsMixin.DocumentAttributeProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class DocumentAttributeProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataAccessorPropsMixin.DocumentAttributeValueProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A document attribute or metadata field.

            :param name: The identifier for the attribute.
            :param value: The value of the attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-dataaccessor-documentattribute.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
                
                document_attribute_property = qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeProperty(
                    name="name",
                    value=qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeValueProperty(
                        date_value="dateValue",
                        long_value=123,
                        string_list_value=["stringListValue"],
                        string_value="stringValue"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d4e82d6deeabb3672b92ab8699c15a9301d157736fd77f0a33481571be5945e3)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The identifier for the attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-dataaccessor-documentattribute.html#cfn-qbusiness-dataaccessor-documentattribute-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataAccessorPropsMixin.DocumentAttributeValueProperty"]]:
            '''The value of the attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-dataaccessor-documentattribute.html#cfn-qbusiness-dataaccessor-documentattribute-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataAccessorPropsMixin.DocumentAttributeValueProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DocumentAttributeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnDataAccessorPropsMixin.DocumentAttributeValueProperty",
        jsii_struct_bases=[],
        name_mapping={
            "date_value": "dateValue",
            "long_value": "longValue",
            "string_list_value": "stringListValue",
            "string_value": "stringValue",
        },
    )
    class DocumentAttributeValueProperty:
        def __init__(
            self,
            *,
            date_value: typing.Optional[builtins.str] = None,
            long_value: typing.Optional[jsii.Number] = None,
            string_list_value: typing.Optional[typing.Sequence[builtins.str]] = None,
            string_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The value of a document attribute.

            You can only provide one value for a document attribute.

            :param date_value: A date expressed as an ISO 8601 string. It's important for the time zone to be included in the ISO 8601 date-time format. For example, 2012-03-25T12:30:10+01:00 is the ISO 8601 date-time format for March 25th 2012 at 12:30PM (plus 10 seconds) in Central European Time.
            :param long_value: A long integer value.
            :param string_list_value: A list of strings.
            :param string_value: A string.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-dataaccessor-documentattributevalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
                
                document_attribute_value_property = qbusiness_mixins.CfnDataAccessorPropsMixin.DocumentAttributeValueProperty(
                    date_value="dateValue",
                    long_value=123,
                    string_list_value=["stringListValue"],
                    string_value="stringValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__00e5fdbcc2aaf8baa826ce27b0195afe9f465001b311406a330a07a97e5abac7)
                check_type(argname="argument date_value", value=date_value, expected_type=type_hints["date_value"])
                check_type(argname="argument long_value", value=long_value, expected_type=type_hints["long_value"])
                check_type(argname="argument string_list_value", value=string_list_value, expected_type=type_hints["string_list_value"])
                check_type(argname="argument string_value", value=string_value, expected_type=type_hints["string_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if date_value is not None:
                self._values["date_value"] = date_value
            if long_value is not None:
                self._values["long_value"] = long_value
            if string_list_value is not None:
                self._values["string_list_value"] = string_list_value
            if string_value is not None:
                self._values["string_value"] = string_value

        @builtins.property
        def date_value(self) -> typing.Optional[builtins.str]:
            '''A date expressed as an ISO 8601 string.

            It's important for the time zone to be included in the ISO 8601 date-time format. For example, 2012-03-25T12:30:10+01:00 is the ISO 8601 date-time format for March 25th 2012 at 12:30PM (plus 10 seconds) in Central European Time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-dataaccessor-documentattributevalue.html#cfn-qbusiness-dataaccessor-documentattributevalue-datevalue
            '''
            result = self._values.get("date_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def long_value(self) -> typing.Optional[jsii.Number]:
            '''A long integer value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-dataaccessor-documentattributevalue.html#cfn-qbusiness-dataaccessor-documentattributevalue-longvalue
            '''
            result = self._values.get("long_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def string_list_value(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of strings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-dataaccessor-documentattributevalue.html#cfn-qbusiness-dataaccessor-documentattributevalue-stringlistvalue
            '''
            result = self._values.get("string_list_value")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def string_value(self) -> typing.Optional[builtins.str]:
            '''A string.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-dataaccessor-documentattributevalue.html#cfn-qbusiness-dataaccessor-documentattributevalue-stringvalue
            '''
            result = self._values.get("string_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DocumentAttributeValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnDataSourceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "configuration": "configuration",
        "description": "description",
        "display_name": "displayName",
        "document_enrichment_configuration": "documentEnrichmentConfiguration",
        "index_id": "indexId",
        "media_extraction_configuration": "mediaExtractionConfiguration",
        "role_arn": "roleArn",
        "sync_schedule": "syncSchedule",
        "tags": "tags",
        "vpc_configuration": "vpcConfiguration",
    },
)
class CfnDataSourceMixinProps:
    def __init__(
        self,
        *,
        application_id: typing.Optional[builtins.str] = None,
        configuration: typing.Any = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        document_enrichment_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.DocumentEnrichmentConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        index_id: typing.Optional[builtins.str] = None,
        media_extraction_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.MediaExtractionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        role_arn: typing.Optional[builtins.str] = None,
        sync_schedule: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.DataSourceVpcConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDataSourcePropsMixin.

        :param application_id: The identifier of the Amazon Q Business application the data source will be attached to.
        :param configuration: Use this property to specify a JSON or YAML schema with configuration properties specific to your data source connector to connect your data source repository to Amazon Q Business . You must use the JSON or YAML schema provided by Amazon Q . The following links have the configuration properties and schemas for AWS CloudFormation for the following connectors: - `Amazon Simple Storage Service <https://docs.aws.amazon.com/amazonq/latest/qbusiness-ug/s3-cfn.html>`_ - `Amazon Q Web Crawler <https://docs.aws.amazon.com/amazonq/latest/qbusiness-ug/web-crawler-cfn.html>`_ Similarly, you can find configuration templates and properties for your specific data source using the following steps: - Navigate to the `Supported connectors <https://docs.aws.amazon.com/amazonq/latest/business-use-dg/connectors-list.html>`_ page in the Amazon Q Business User Guide, and select the data source connector of your choice. - Then, from that specific data source connector's page, choose the topic containing *Using CloudFormation* to find the schemas for your data source connector, including configuration parameter descriptions and examples.
        :param description: A description for the data source connector.
        :param display_name: The name of the Amazon Q Business data source.
        :param document_enrichment_configuration: Provides the configuration information for altering document metadata and content during the document ingestion process. For more information, see `Custom document enrichment <https://docs.aws.amazon.com/amazonq/latest/business-use-dg/custom-document-enrichment.html>`_ .
        :param index_id: The identifier of the index the data source is attached to.
        :param media_extraction_configuration: The configuration for extracting information from media in documents.
        :param role_arn: The Amazon Resource Name (ARN) of an IAM role with permission to access the data source and required resources. This field is required for all connector types except custom connectors, where it is optional.
        :param sync_schedule: Sets the frequency for Amazon Q Business to check the documents in your data source repository and update your index. If you don't set a schedule, Amazon Q Business won't periodically update the index. Specify a ``cron-`` format schedule string or an empty string to indicate that the index is updated on demand. You can't specify the ``Schedule`` parameter when the ``Type`` parameter is set to ``CUSTOM`` . If you do, you receive a ``ValidationException`` exception.
        :param tags: A list of key-value pairs that identify or categorize the data source connector. You can also use tags to help control access to the data source connector. Tag keys and values can consist of Unicode letters, digits, white space, and any of the following symbols: _ . : / = + -
        :param vpc_configuration: Configuration information for an Amazon VPC (Virtual Private Cloud) to connect to your data source. For more information, see `Using Amazon VPC with Amazon Q Business connectors <https://docs.aws.amazon.com/amazonq/latest/business-use-dg/connector-vpc.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-datasource.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
            
            # configuration: Any
            
            cfn_data_source_mixin_props = qbusiness_mixins.CfnDataSourceMixinProps(
                application_id="applicationId",
                configuration=configuration,
                description="description",
                display_name="displayName",
                document_enrichment_configuration=qbusiness_mixins.CfnDataSourcePropsMixin.DocumentEnrichmentConfigurationProperty(
                    inline_configurations=[qbusiness_mixins.CfnDataSourcePropsMixin.InlineDocumentEnrichmentConfigurationProperty(
                        condition=qbusiness_mixins.CfnDataSourcePropsMixin.DocumentAttributeConditionProperty(
                            key="key",
                            operator="operator",
                            value=qbusiness_mixins.CfnDataSourcePropsMixin.DocumentAttributeValueProperty(
                                date_value="dateValue",
                                long_value=123,
                                string_list_value=["stringListValue"],
                                string_value="stringValue"
                            )
                        ),
                        document_content_operator="documentContentOperator",
                        target=qbusiness_mixins.CfnDataSourcePropsMixin.DocumentAttributeTargetProperty(
                            attribute_value_operator="attributeValueOperator",
                            key="key",
                            value=qbusiness_mixins.CfnDataSourcePropsMixin.DocumentAttributeValueProperty(
                                date_value="dateValue",
                                long_value=123,
                                string_list_value=["stringListValue"],
                                string_value="stringValue"
                            )
                        )
                    )],
                    post_extraction_hook_configuration=qbusiness_mixins.CfnDataSourcePropsMixin.HookConfigurationProperty(
                        invocation_condition=qbusiness_mixins.CfnDataSourcePropsMixin.DocumentAttributeConditionProperty(
                            key="key",
                            operator="operator",
                            value=qbusiness_mixins.CfnDataSourcePropsMixin.DocumentAttributeValueProperty(
                                date_value="dateValue",
                                long_value=123,
                                string_list_value=["stringListValue"],
                                string_value="stringValue"
                            )
                        ),
                        lambda_arn="lambdaArn",
                        role_arn="roleArn",
                        s3_bucket_name="s3BucketName"
                    ),
                    pre_extraction_hook_configuration=qbusiness_mixins.CfnDataSourcePropsMixin.HookConfigurationProperty(
                        invocation_condition=qbusiness_mixins.CfnDataSourcePropsMixin.DocumentAttributeConditionProperty(
                            key="key",
                            operator="operator",
                            value=qbusiness_mixins.CfnDataSourcePropsMixin.DocumentAttributeValueProperty(
                                date_value="dateValue",
                                long_value=123,
                                string_list_value=["stringListValue"],
                                string_value="stringValue"
                            )
                        ),
                        lambda_arn="lambdaArn",
                        role_arn="roleArn",
                        s3_bucket_name="s3BucketName"
                    )
                ),
                index_id="indexId",
                media_extraction_configuration=qbusiness_mixins.CfnDataSourcePropsMixin.MediaExtractionConfigurationProperty(
                    audio_extraction_configuration=qbusiness_mixins.CfnDataSourcePropsMixin.AudioExtractionConfigurationProperty(
                        audio_extraction_status="audioExtractionStatus"
                    ),
                    image_extraction_configuration=qbusiness_mixins.CfnDataSourcePropsMixin.ImageExtractionConfigurationProperty(
                        image_extraction_status="imageExtractionStatus"
                    ),
                    video_extraction_configuration=qbusiness_mixins.CfnDataSourcePropsMixin.VideoExtractionConfigurationProperty(
                        video_extraction_status="videoExtractionStatus"
                    )
                ),
                role_arn="roleArn",
                sync_schedule="syncSchedule",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vpc_configuration=qbusiness_mixins.CfnDataSourcePropsMixin.DataSourceVpcConfigurationProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b891d365764aa6854b482ca34148482e8d94ee53a5195d7e9514e7a602308337)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument document_enrichment_configuration", value=document_enrichment_configuration, expected_type=type_hints["document_enrichment_configuration"])
            check_type(argname="argument index_id", value=index_id, expected_type=type_hints["index_id"])
            check_type(argname="argument media_extraction_configuration", value=media_extraction_configuration, expected_type=type_hints["media_extraction_configuration"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument sync_schedule", value=sync_schedule, expected_type=type_hints["sync_schedule"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc_configuration", value=vpc_configuration, expected_type=type_hints["vpc_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_id is not None:
            self._values["application_id"] = application_id
        if configuration is not None:
            self._values["configuration"] = configuration
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if document_enrichment_configuration is not None:
            self._values["document_enrichment_configuration"] = document_enrichment_configuration
        if index_id is not None:
            self._values["index_id"] = index_id
        if media_extraction_configuration is not None:
            self._values["media_extraction_configuration"] = media_extraction_configuration
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if sync_schedule is not None:
            self._values["sync_schedule"] = sync_schedule
        if tags is not None:
            self._values["tags"] = tags
        if vpc_configuration is not None:
            self._values["vpc_configuration"] = vpc_configuration

    @builtins.property
    def application_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the Amazon Q Business application the data source will be attached to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-datasource.html#cfn-qbusiness-datasource-applicationid
        '''
        result = self._values.get("application_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def configuration(self) -> typing.Any:
        '''Use this property to specify a JSON or YAML schema with configuration properties specific to your data source connector to connect your data source repository to Amazon Q Business .

        You must use the JSON or YAML schema provided by Amazon Q .

        The following links have the configuration properties and schemas for AWS CloudFormation for the following connectors:

        - `Amazon Simple Storage Service <https://docs.aws.amazon.com/amazonq/latest/qbusiness-ug/s3-cfn.html>`_
        - `Amazon Q Web Crawler <https://docs.aws.amazon.com/amazonq/latest/qbusiness-ug/web-crawler-cfn.html>`_

        Similarly, you can find configuration templates and properties for your specific data source using the following steps:

        - Navigate to the `Supported connectors <https://docs.aws.amazon.com/amazonq/latest/business-use-dg/connectors-list.html>`_ page in the Amazon Q Business User Guide, and select the data source connector of your choice.
        - Then, from that specific data source connector's page, choose the topic containing *Using CloudFormation* to find the schemas for your data source connector, including configuration parameter descriptions and examples.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-datasource.html#cfn-qbusiness-datasource-configuration
        '''
        result = self._values.get("configuration")
        return typing.cast(typing.Any, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the data source connector.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-datasource.html#cfn-qbusiness-datasource-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Amazon Q Business data source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-datasource.html#cfn-qbusiness-datasource-displayname
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def document_enrichment_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DocumentEnrichmentConfigurationProperty"]]:
        '''Provides the configuration information for altering document metadata and content during the document ingestion process.

        For more information, see `Custom document enrichment <https://docs.aws.amazon.com/amazonq/latest/business-use-dg/custom-document-enrichment.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-datasource.html#cfn-qbusiness-datasource-documentenrichmentconfiguration
        '''
        result = self._values.get("document_enrichment_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DocumentEnrichmentConfigurationProperty"]], result)

    @builtins.property
    def index_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the index the data source is attached to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-datasource.html#cfn-qbusiness-datasource-indexid
        '''
        result = self._values.get("index_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def media_extraction_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.MediaExtractionConfigurationProperty"]]:
        '''The configuration for extracting information from media in documents.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-datasource.html#cfn-qbusiness-datasource-mediaextractionconfiguration
        '''
        result = self._values.get("media_extraction_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.MediaExtractionConfigurationProperty"]], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of an IAM role with permission to access the data source and required resources.

        This field is required for all connector types except custom connectors, where it is optional.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-datasource.html#cfn-qbusiness-datasource-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_schedule(self) -> typing.Optional[builtins.str]:
        '''Sets the frequency for Amazon Q Business to check the documents in your data source repository and update your index.

        If you don't set a schedule, Amazon Q Business won't periodically update the index.

        Specify a ``cron-`` format schedule string or an empty string to indicate that the index is updated on demand. You can't specify the ``Schedule`` parameter when the ``Type`` parameter is set to ``CUSTOM`` . If you do, you receive a ``ValidationException`` exception.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-datasource.html#cfn-qbusiness-datasource-syncschedule
        '''
        result = self._values.get("sync_schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of key-value pairs that identify or categorize the data source connector.

        You can also use tags to help control access to the data source connector. Tag keys and values can consist of Unicode letters, digits, white space, and any of the following symbols: _ . : / = + -

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-datasource.html#cfn-qbusiness-datasource-tags
        :: .
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def vpc_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DataSourceVpcConfigurationProperty"]]:
        '''Configuration information for an Amazon VPC (Virtual Private Cloud) to connect to your data source.

        For more information, see `Using Amazon VPC with Amazon Q Business connectors <https://docs.aws.amazon.com/amazonq/latest/business-use-dg/connector-vpc.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-datasource.html#cfn-qbusiness-datasource-vpcconfiguration
        '''
        result = self._values.get("vpc_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DataSourceVpcConfigurationProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDataSourceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDataSourcePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnDataSourcePropsMixin",
):
    '''Creates a data source connector for an Amazon Q Business application.

    ``CreateDataSource`` is a synchronous operation. The operation returns 200 if the data source was successfully created. Otherwise, an exception is raised.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-datasource.html
    :cloudformationResource: AWS::QBusiness::DataSource
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
        
        # configuration: Any
        
        cfn_data_source_props_mixin = qbusiness_mixins.CfnDataSourcePropsMixin(qbusiness_mixins.CfnDataSourceMixinProps(
            application_id="applicationId",
            configuration=configuration,
            description="description",
            display_name="displayName",
            document_enrichment_configuration=qbusiness_mixins.CfnDataSourcePropsMixin.DocumentEnrichmentConfigurationProperty(
                inline_configurations=[qbusiness_mixins.CfnDataSourcePropsMixin.InlineDocumentEnrichmentConfigurationProperty(
                    condition=qbusiness_mixins.CfnDataSourcePropsMixin.DocumentAttributeConditionProperty(
                        key="key",
                        operator="operator",
                        value=qbusiness_mixins.CfnDataSourcePropsMixin.DocumentAttributeValueProperty(
                            date_value="dateValue",
                            long_value=123,
                            string_list_value=["stringListValue"],
                            string_value="stringValue"
                        )
                    ),
                    document_content_operator="documentContentOperator",
                    target=qbusiness_mixins.CfnDataSourcePropsMixin.DocumentAttributeTargetProperty(
                        attribute_value_operator="attributeValueOperator",
                        key="key",
                        value=qbusiness_mixins.CfnDataSourcePropsMixin.DocumentAttributeValueProperty(
                            date_value="dateValue",
                            long_value=123,
                            string_list_value=["stringListValue"],
                            string_value="stringValue"
                        )
                    )
                )],
                post_extraction_hook_configuration=qbusiness_mixins.CfnDataSourcePropsMixin.HookConfigurationProperty(
                    invocation_condition=qbusiness_mixins.CfnDataSourcePropsMixin.DocumentAttributeConditionProperty(
                        key="key",
                        operator="operator",
                        value=qbusiness_mixins.CfnDataSourcePropsMixin.DocumentAttributeValueProperty(
                            date_value="dateValue",
                            long_value=123,
                            string_list_value=["stringListValue"],
                            string_value="stringValue"
                        )
                    ),
                    lambda_arn="lambdaArn",
                    role_arn="roleArn",
                    s3_bucket_name="s3BucketName"
                ),
                pre_extraction_hook_configuration=qbusiness_mixins.CfnDataSourcePropsMixin.HookConfigurationProperty(
                    invocation_condition=qbusiness_mixins.CfnDataSourcePropsMixin.DocumentAttributeConditionProperty(
                        key="key",
                        operator="operator",
                        value=qbusiness_mixins.CfnDataSourcePropsMixin.DocumentAttributeValueProperty(
                            date_value="dateValue",
                            long_value=123,
                            string_list_value=["stringListValue"],
                            string_value="stringValue"
                        )
                    ),
                    lambda_arn="lambdaArn",
                    role_arn="roleArn",
                    s3_bucket_name="s3BucketName"
                )
            ),
            index_id="indexId",
            media_extraction_configuration=qbusiness_mixins.CfnDataSourcePropsMixin.MediaExtractionConfigurationProperty(
                audio_extraction_configuration=qbusiness_mixins.CfnDataSourcePropsMixin.AudioExtractionConfigurationProperty(
                    audio_extraction_status="audioExtractionStatus"
                ),
                image_extraction_configuration=qbusiness_mixins.CfnDataSourcePropsMixin.ImageExtractionConfigurationProperty(
                    image_extraction_status="imageExtractionStatus"
                ),
                video_extraction_configuration=qbusiness_mixins.CfnDataSourcePropsMixin.VideoExtractionConfigurationProperty(
                    video_extraction_status="videoExtractionStatus"
                )
            ),
            role_arn="roleArn",
            sync_schedule="syncSchedule",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            vpc_configuration=qbusiness_mixins.CfnDataSourcePropsMixin.DataSourceVpcConfigurationProperty(
                security_group_ids=["securityGroupIds"],
                subnet_ids=["subnetIds"]
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDataSourceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::QBusiness::DataSource``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38528ca7532aaf871b7e9516e6d3b3de3eaf34a5115256c060664cef579ffd55)
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
            type_hints = typing.get_type_hints(_typecheckingstub__640a5a9e974c1b32b990ba74fee211f91a7a3e575d9c50b0202df64cee7cf597)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b29087c22ca13716c896ad70fa0a6448f41e577096bf02b5ff04e5b9e70b545)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDataSourceMixinProps:
        return typing.cast(CfnDataSourceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnDataSourcePropsMixin.AudioExtractionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"audio_extraction_status": "audioExtractionStatus"},
    )
    class AudioExtractionConfigurationProperty:
        def __init__(
            self,
            *,
            audio_extraction_status: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration settings for audio content extraction and processing.

            :param audio_extraction_status: The status of audio extraction (ENABLED or DISABLED) for processing audio content from files.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-datasource-audioextractionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
                
                audio_extraction_configuration_property = qbusiness_mixins.CfnDataSourcePropsMixin.AudioExtractionConfigurationProperty(
                    audio_extraction_status="audioExtractionStatus"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0cbc958e7ac6d268bba872abbe7f76f04e68ae7a59c961bc2b5c3614aae3c19d)
                check_type(argname="argument audio_extraction_status", value=audio_extraction_status, expected_type=type_hints["audio_extraction_status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if audio_extraction_status is not None:
                self._values["audio_extraction_status"] = audio_extraction_status

        @builtins.property
        def audio_extraction_status(self) -> typing.Optional[builtins.str]:
            '''The status of audio extraction (ENABLED or DISABLED) for processing audio content from files.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-datasource-audioextractionconfiguration.html#cfn-qbusiness-datasource-audioextractionconfiguration-audioextractionstatus
            '''
            result = self._values.get("audio_extraction_status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AudioExtractionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnDataSourcePropsMixin.DataSourceVpcConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
        },
    )
    class DataSourceVpcConfigurationProperty:
        def __init__(
            self,
            *,
            security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Provides configuration information needed to connect to an Amazon VPC (Virtual Private Cloud).

            :param security_group_ids: A list of identifiers of security groups within your Amazon VPC. The security groups should enable Amazon Q Business to connect to the data source.
            :param subnet_ids: A list of identifiers for subnets within your Amazon VPC. The subnets should be able to connect to each other in the VPC, and they should have outgoing access to the Internet through a NAT device.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-datasource-datasourcevpcconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
                
                data_source_vpc_configuration_property = qbusiness_mixins.CfnDataSourcePropsMixin.DataSourceVpcConfigurationProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9bdc2659728932c3487742fd50d2412915adb4286c6a8f2f4fe99df27789218b)
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
                check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnet_ids is not None:
                self._values["subnet_ids"] = subnet_ids

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of identifiers of security groups within your Amazon VPC.

            The security groups should enable Amazon Q Business to connect to the data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-datasource-datasourcevpcconfiguration.html#cfn-qbusiness-datasource-datasourcevpcconfiguration-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of identifiers for subnets within your Amazon VPC.

            The subnets should be able to connect to each other in the VPC, and they should have outgoing access to the Internet through a NAT device.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-datasource-datasourcevpcconfiguration.html#cfn-qbusiness-datasource-datasourcevpcconfiguration-subnetids
            '''
            result = self._values.get("subnet_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataSourceVpcConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnDataSourcePropsMixin.DocumentAttributeConditionProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "operator": "operator", "value": "value"},
    )
    class DocumentAttributeConditionProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            operator: typing.Optional[builtins.str] = None,
            value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.DocumentAttributeValueProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The condition used for the target document attribute or metadata field when ingesting documents into Amazon Q Business.

            You use this with ```DocumentAttributeTarget`` <https://docs.aws.amazon.com/amazonq/latest/api-reference/API_DocumentAttributeTarget.html>`_ to apply the condition.

            For example, you can create the 'Department' target field and have it prefill department names associated with the documents based on information in the 'Source_URI' field. Set the condition that if the 'Source_URI' field contains 'financial' in its URI value, then prefill the target field 'Department' with the target value 'Finance' for the document.

            Amazon Q Business can't create a target field if it has not already been created as an index field. After you create your index field, you can create a document metadata field using ``DocumentAttributeTarget`` . Amazon Q Business then will map your newly created metadata field to your index field.

            :param key: The identifier of the document attribute used for the condition. For example, 'Source_URI' could be an identifier for the attribute or metadata field that contains source URIs associated with the documents. Amazon Q Business currently doesn't support ``_document_body`` as an attribute key used for the condition.
            :param operator: The identifier of the document attribute used for the condition. For example, 'Source_URI' could be an identifier for the attribute or metadata field that contains source URIs associated with the documents. Amazon Q Business currently does not support ``_document_body`` as an attribute key used for the condition.
            :param value: The value of a document attribute. You can only provide one value for a document attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-datasource-documentattributecondition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
                
                document_attribute_condition_property = qbusiness_mixins.CfnDataSourcePropsMixin.DocumentAttributeConditionProperty(
                    key="key",
                    operator="operator",
                    value=qbusiness_mixins.CfnDataSourcePropsMixin.DocumentAttributeValueProperty(
                        date_value="dateValue",
                        long_value=123,
                        string_list_value=["stringListValue"],
                        string_value="stringValue"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a2e379efb79afebc0d361d7f2bc1cc756e8668175f3fd3314acdbd0cd5b87306)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if operator is not None:
                self._values["operator"] = operator
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The identifier of the document attribute used for the condition.

            For example, 'Source_URI' could be an identifier for the attribute or metadata field that contains source URIs associated with the documents.

            Amazon Q Business currently doesn't support ``_document_body`` as an attribute key used for the condition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-datasource-documentattributecondition.html#cfn-qbusiness-datasource-documentattributecondition-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def operator(self) -> typing.Optional[builtins.str]:
            '''The identifier of the document attribute used for the condition.

            For example, 'Source_URI' could be an identifier for the attribute or metadata field that contains source URIs associated with the documents.

            Amazon Q Business currently does not support ``_document_body`` as an attribute key used for the condition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-datasource-documentattributecondition.html#cfn-qbusiness-datasource-documentattributecondition-operator
            '''
            result = self._values.get("operator")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DocumentAttributeValueProperty"]]:
            '''The value of a document attribute.

            You can only provide one value for a document attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-datasource-documentattributecondition.html#cfn-qbusiness-datasource-documentattributecondition-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DocumentAttributeValueProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DocumentAttributeConditionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnDataSourcePropsMixin.DocumentAttributeTargetProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attribute_value_operator": "attributeValueOperator",
            "key": "key",
            "value": "value",
        },
    )
    class DocumentAttributeTargetProperty:
        def __init__(
            self,
            *,
            attribute_value_operator: typing.Optional[builtins.str] = None,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.DocumentAttributeValueProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The target document attribute or metadata field you want to alter when ingesting documents into Amazon Q Business.

            For example, you can delete all customer identification numbers associated with the documents, stored in the document metadata field called 'Customer_ID' by setting the target key as 'Customer_ID' and the deletion flag to ``TRUE`` . This removes all customer ID values in the field 'Customer_ID'. This would scrub personally identifiable information from each document's metadata.

            Amazon Q Business can't create a target field if it has not already been created as an index field. After you create your index field, you can create a document metadata field using ```DocumentAttributeTarget`` <https://docs.aws.amazon.com/amazonq/latest/api-reference/API_DocumentAttributeTarget.html>`_ . Amazon Q Business will then map your newly created document attribute to your index field.

            You can also use this with ```DocumentAttributeCondition`` <https://docs.aws.amazon.com/amazonq/latest/api-reference/API_DocumentAttributeCondition.html>`_ .

            :param attribute_value_operator: ``TRUE`` to delete the existing target value for your specified target attribute key. You cannot create a target value and set this to ``TRUE`` .
            :param key: The identifier of the target document attribute or metadata field. For example, 'Department' could be an identifier for the target attribute or metadata field that includes the department names associated with the documents.
            :param value: The value of a document attribute. You can only provide one value for a document attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-datasource-documentattributetarget.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
                
                document_attribute_target_property = qbusiness_mixins.CfnDataSourcePropsMixin.DocumentAttributeTargetProperty(
                    attribute_value_operator="attributeValueOperator",
                    key="key",
                    value=qbusiness_mixins.CfnDataSourcePropsMixin.DocumentAttributeValueProperty(
                        date_value="dateValue",
                        long_value=123,
                        string_list_value=["stringListValue"],
                        string_value="stringValue"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1ea2e3529e8719e5d18efc7b63b7a5ff2bc8522ee21a0ad8761fadc617cbb94e)
                check_type(argname="argument attribute_value_operator", value=attribute_value_operator, expected_type=type_hints["attribute_value_operator"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attribute_value_operator is not None:
                self._values["attribute_value_operator"] = attribute_value_operator
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def attribute_value_operator(self) -> typing.Optional[builtins.str]:
            '''``TRUE`` to delete the existing target value for your specified target attribute key.

            You cannot create a target value and set this to ``TRUE`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-datasource-documentattributetarget.html#cfn-qbusiness-datasource-documentattributetarget-attributevalueoperator
            '''
            result = self._values.get("attribute_value_operator")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The identifier of the target document attribute or metadata field.

            For example, 'Department' could be an identifier for the target attribute or metadata field that includes the department names associated with the documents.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-datasource-documentattributetarget.html#cfn-qbusiness-datasource-documentattributetarget-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DocumentAttributeValueProperty"]]:
            '''The value of a document attribute.

            You can only provide one value for a document attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-datasource-documentattributetarget.html#cfn-qbusiness-datasource-documentattributetarget-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DocumentAttributeValueProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DocumentAttributeTargetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnDataSourcePropsMixin.DocumentAttributeValueProperty",
        jsii_struct_bases=[],
        name_mapping={
            "date_value": "dateValue",
            "long_value": "longValue",
            "string_list_value": "stringListValue",
            "string_value": "stringValue",
        },
    )
    class DocumentAttributeValueProperty:
        def __init__(
            self,
            *,
            date_value: typing.Optional[builtins.str] = None,
            long_value: typing.Optional[jsii.Number] = None,
            string_list_value: typing.Optional[typing.Sequence[builtins.str]] = None,
            string_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The value of a document attribute.

            You can only provide one value for a document attribute.

            :param date_value: A date expressed as an ISO 8601 string. It's important for the time zone to be included in the ISO 8601 date-time format. For example, 2012-03-25T12:30:10+01:00 is the ISO 8601 date-time format for March 25th 2012 at 12:30PM (plus 10 seconds) in Central European Time.
            :param long_value: A long integer value.
            :param string_list_value: A list of strings.
            :param string_value: A string.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-datasource-documentattributevalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
                
                document_attribute_value_property = qbusiness_mixins.CfnDataSourcePropsMixin.DocumentAttributeValueProperty(
                    date_value="dateValue",
                    long_value=123,
                    string_list_value=["stringListValue"],
                    string_value="stringValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c684b4e243e409a4a2ea82719ddcdc667897c49830b86cd2f209c653b9af8625)
                check_type(argname="argument date_value", value=date_value, expected_type=type_hints["date_value"])
                check_type(argname="argument long_value", value=long_value, expected_type=type_hints["long_value"])
                check_type(argname="argument string_list_value", value=string_list_value, expected_type=type_hints["string_list_value"])
                check_type(argname="argument string_value", value=string_value, expected_type=type_hints["string_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if date_value is not None:
                self._values["date_value"] = date_value
            if long_value is not None:
                self._values["long_value"] = long_value
            if string_list_value is not None:
                self._values["string_list_value"] = string_list_value
            if string_value is not None:
                self._values["string_value"] = string_value

        @builtins.property
        def date_value(self) -> typing.Optional[builtins.str]:
            '''A date expressed as an ISO 8601 string.

            It's important for the time zone to be included in the ISO 8601 date-time format. For example, 2012-03-25T12:30:10+01:00 is the ISO 8601 date-time format for March 25th 2012 at 12:30PM (plus 10 seconds) in Central European Time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-datasource-documentattributevalue.html#cfn-qbusiness-datasource-documentattributevalue-datevalue
            '''
            result = self._values.get("date_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def long_value(self) -> typing.Optional[jsii.Number]:
            '''A long integer value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-datasource-documentattributevalue.html#cfn-qbusiness-datasource-documentattributevalue-longvalue
            '''
            result = self._values.get("long_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def string_list_value(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of strings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-datasource-documentattributevalue.html#cfn-qbusiness-datasource-documentattributevalue-stringlistvalue
            '''
            result = self._values.get("string_list_value")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def string_value(self) -> typing.Optional[builtins.str]:
            '''A string.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-datasource-documentattributevalue.html#cfn-qbusiness-datasource-documentattributevalue-stringvalue
            '''
            result = self._values.get("string_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DocumentAttributeValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnDataSourcePropsMixin.DocumentEnrichmentConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "inline_configurations": "inlineConfigurations",
            "post_extraction_hook_configuration": "postExtractionHookConfiguration",
            "pre_extraction_hook_configuration": "preExtractionHookConfiguration",
        },
    )
    class DocumentEnrichmentConfigurationProperty:
        def __init__(
            self,
            *,
            inline_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.InlineDocumentEnrichmentConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            post_extraction_hook_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.HookConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            pre_extraction_hook_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.HookConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Provides the configuration information for altering document metadata and content during the document ingestion process.

            For more information, see `Custom document enrichment <https://docs.aws.amazon.com/amazonq/latest/business-use-dg/custom-document-enrichment.html>`_ .

            :param inline_configurations: Configuration information to alter document attributes or metadata fields and content when ingesting documents into Amazon Q Business.
            :param post_extraction_hook_configuration: Configuration information for invoking a Lambda function in AWS Lambda on the structured documents with their metadata and text extracted. You can use a Lambda function to apply advanced logic for creating, modifying, or deleting document metadata and content. For more information, see `Using Lambda functions <https://docs.aws.amazon.com/amazonq/latest/business-use-dg/cde-lambda-operations.html>`_ .
            :param pre_extraction_hook_configuration: Configuration information for invoking a Lambda function in AWS Lambda on the original or raw documents before extracting their metadata and text. You can use a Lambda function to apply advanced logic for creating, modifying, or deleting document metadata and content. For more information, see `Using Lambda functions <https://docs.aws.amazon.com/amazonq/latest/business-use-dg/cde-lambda-operations.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-datasource-documentenrichmentconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
                
                document_enrichment_configuration_property = qbusiness_mixins.CfnDataSourcePropsMixin.DocumentEnrichmentConfigurationProperty(
                    inline_configurations=[qbusiness_mixins.CfnDataSourcePropsMixin.InlineDocumentEnrichmentConfigurationProperty(
                        condition=qbusiness_mixins.CfnDataSourcePropsMixin.DocumentAttributeConditionProperty(
                            key="key",
                            operator="operator",
                            value=qbusiness_mixins.CfnDataSourcePropsMixin.DocumentAttributeValueProperty(
                                date_value="dateValue",
                                long_value=123,
                                string_list_value=["stringListValue"],
                                string_value="stringValue"
                            )
                        ),
                        document_content_operator="documentContentOperator",
                        target=qbusiness_mixins.CfnDataSourcePropsMixin.DocumentAttributeTargetProperty(
                            attribute_value_operator="attributeValueOperator",
                            key="key",
                            value=qbusiness_mixins.CfnDataSourcePropsMixin.DocumentAttributeValueProperty(
                                date_value="dateValue",
                                long_value=123,
                                string_list_value=["stringListValue"],
                                string_value="stringValue"
                            )
                        )
                    )],
                    post_extraction_hook_configuration=qbusiness_mixins.CfnDataSourcePropsMixin.HookConfigurationProperty(
                        invocation_condition=qbusiness_mixins.CfnDataSourcePropsMixin.DocumentAttributeConditionProperty(
                            key="key",
                            operator="operator",
                            value=qbusiness_mixins.CfnDataSourcePropsMixin.DocumentAttributeValueProperty(
                                date_value="dateValue",
                                long_value=123,
                                string_list_value=["stringListValue"],
                                string_value="stringValue"
                            )
                        ),
                        lambda_arn="lambdaArn",
                        role_arn="roleArn",
                        s3_bucket_name="s3BucketName"
                    ),
                    pre_extraction_hook_configuration=qbusiness_mixins.CfnDataSourcePropsMixin.HookConfigurationProperty(
                        invocation_condition=qbusiness_mixins.CfnDataSourcePropsMixin.DocumentAttributeConditionProperty(
                            key="key",
                            operator="operator",
                            value=qbusiness_mixins.CfnDataSourcePropsMixin.DocumentAttributeValueProperty(
                                date_value="dateValue",
                                long_value=123,
                                string_list_value=["stringListValue"],
                                string_value="stringValue"
                            )
                        ),
                        lambda_arn="lambdaArn",
                        role_arn="roleArn",
                        s3_bucket_name="s3BucketName"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f775c3879a3ad8e4e6463d81a4e860abc09aedcee8f24bc0c2cd02856d22eb93)
                check_type(argname="argument inline_configurations", value=inline_configurations, expected_type=type_hints["inline_configurations"])
                check_type(argname="argument post_extraction_hook_configuration", value=post_extraction_hook_configuration, expected_type=type_hints["post_extraction_hook_configuration"])
                check_type(argname="argument pre_extraction_hook_configuration", value=pre_extraction_hook_configuration, expected_type=type_hints["pre_extraction_hook_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if inline_configurations is not None:
                self._values["inline_configurations"] = inline_configurations
            if post_extraction_hook_configuration is not None:
                self._values["post_extraction_hook_configuration"] = post_extraction_hook_configuration
            if pre_extraction_hook_configuration is not None:
                self._values["pre_extraction_hook_configuration"] = pre_extraction_hook_configuration

        @builtins.property
        def inline_configurations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.InlineDocumentEnrichmentConfigurationProperty"]]]]:
            '''Configuration information to alter document attributes or metadata fields and content when ingesting documents into Amazon Q Business.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-datasource-documentenrichmentconfiguration.html#cfn-qbusiness-datasource-documentenrichmentconfiguration-inlineconfigurations
            '''
            result = self._values.get("inline_configurations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.InlineDocumentEnrichmentConfigurationProperty"]]]], result)

        @builtins.property
        def post_extraction_hook_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.HookConfigurationProperty"]]:
            '''Configuration information for invoking a Lambda function in AWS Lambda on the structured documents with their metadata and text extracted.

            You can use a Lambda function to apply advanced logic for creating, modifying, or deleting document metadata and content. For more information, see `Using Lambda functions <https://docs.aws.amazon.com/amazonq/latest/business-use-dg/cde-lambda-operations.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-datasource-documentenrichmentconfiguration.html#cfn-qbusiness-datasource-documentenrichmentconfiguration-postextractionhookconfiguration
            '''
            result = self._values.get("post_extraction_hook_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.HookConfigurationProperty"]], result)

        @builtins.property
        def pre_extraction_hook_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.HookConfigurationProperty"]]:
            '''Configuration information for invoking a Lambda function in AWS Lambda on the original or raw documents before extracting their metadata and text.

            You can use a Lambda function to apply advanced logic for creating, modifying, or deleting document metadata and content. For more information, see `Using Lambda functions <https://docs.aws.amazon.com/amazonq/latest/business-use-dg/cde-lambda-operations.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-datasource-documentenrichmentconfiguration.html#cfn-qbusiness-datasource-documentenrichmentconfiguration-preextractionhookconfiguration
            '''
            result = self._values.get("pre_extraction_hook_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.HookConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DocumentEnrichmentConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnDataSourcePropsMixin.HookConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "invocation_condition": "invocationCondition",
            "lambda_arn": "lambdaArn",
            "role_arn": "roleArn",
            "s3_bucket_name": "s3BucketName",
        },
    )
    class HookConfigurationProperty:
        def __init__(
            self,
            *,
            invocation_condition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.DocumentAttributeConditionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            lambda_arn: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
            s3_bucket_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides the configuration information for invoking a Lambda function in AWS Lambda to alter document metadata and content when ingesting documents into Amazon Q Business.

            You can configure your Lambda function using the ``PreExtractionHookConfiguration`` parameter if you want to apply advanced alterations on the original or raw documents.

            If you want to apply advanced alterations on the Amazon Q Business structured documents, you must configure your Lambda function using ``PostExtractionHookConfiguration`` .

            You can only invoke one Lambda function. However, this function can invoke other functions it requires.

            For more information, see `Custom document enrichment <https://docs.aws.amazon.com/amazonq/latest/business-use-dg/custom-document-enrichment.html>`_ .

            :param invocation_condition: The condition used for when a Lambda function should be invoked. For example, you can specify a condition that if there are empty date-time values, then Amazon Q Business should invoke a function that inserts the current date-time.
            :param lambda_arn: The Amazon Resource Name (ARN) of the Lambda function during ingestion. For more information, see `Using Lambda functions for Amazon Q Business document enrichment <https://docs.aws.amazon.com/amazonq/latest/qbusiness-ug/cde-lambda-operations.html>`_ .
            :param role_arn: The Amazon Resource Name (ARN) of a role with permission to run ``PreExtractionHookConfiguration`` and ``PostExtractionHookConfiguration`` for altering document metadata and content during the document ingestion process.
            :param s3_bucket_name: Stores the original, raw documents or the structured, parsed documents before and after altering them. For more information, see `Data contracts for Lambda functions <https://docs.aws.amazon.com/amazonq/latest/business-use-dg/cde-lambda-operations.html#cde-lambda-operations-data-contracts>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-datasource-hookconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
                
                hook_configuration_property = qbusiness_mixins.CfnDataSourcePropsMixin.HookConfigurationProperty(
                    invocation_condition=qbusiness_mixins.CfnDataSourcePropsMixin.DocumentAttributeConditionProperty(
                        key="key",
                        operator="operator",
                        value=qbusiness_mixins.CfnDataSourcePropsMixin.DocumentAttributeValueProperty(
                            date_value="dateValue",
                            long_value=123,
                            string_list_value=["stringListValue"],
                            string_value="stringValue"
                        )
                    ),
                    lambda_arn="lambdaArn",
                    role_arn="roleArn",
                    s3_bucket_name="s3BucketName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9d9c1a478132d58acc8b13ae8dc88e8dfd523dd6fbbb0a13ecdd609d5defe048)
                check_type(argname="argument invocation_condition", value=invocation_condition, expected_type=type_hints["invocation_condition"])
                check_type(argname="argument lambda_arn", value=lambda_arn, expected_type=type_hints["lambda_arn"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument s3_bucket_name", value=s3_bucket_name, expected_type=type_hints["s3_bucket_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if invocation_condition is not None:
                self._values["invocation_condition"] = invocation_condition
            if lambda_arn is not None:
                self._values["lambda_arn"] = lambda_arn
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if s3_bucket_name is not None:
                self._values["s3_bucket_name"] = s3_bucket_name

        @builtins.property
        def invocation_condition(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DocumentAttributeConditionProperty"]]:
            '''The condition used for when a Lambda function should be invoked.

            For example, you can specify a condition that if there are empty date-time values, then Amazon Q Business should invoke a function that inserts the current date-time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-datasource-hookconfiguration.html#cfn-qbusiness-datasource-hookconfiguration-invocationcondition
            '''
            result = self._values.get("invocation_condition")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DocumentAttributeConditionProperty"]], result)

        @builtins.property
        def lambda_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Lambda function during ingestion.

            For more information, see `Using Lambda functions for Amazon Q Business document enrichment <https://docs.aws.amazon.com/amazonq/latest/qbusiness-ug/cde-lambda-operations.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-datasource-hookconfiguration.html#cfn-qbusiness-datasource-hookconfiguration-lambdaarn
            '''
            result = self._values.get("lambda_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of a role with permission to run ``PreExtractionHookConfiguration`` and ``PostExtractionHookConfiguration`` for altering document metadata and content during the document ingestion process.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-datasource-hookconfiguration.html#cfn-qbusiness-datasource-hookconfiguration-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_bucket_name(self) -> typing.Optional[builtins.str]:
            '''Stores the original, raw documents or the structured, parsed documents before and after altering them.

            For more information, see `Data contracts for Lambda functions <https://docs.aws.amazon.com/amazonq/latest/business-use-dg/cde-lambda-operations.html#cde-lambda-operations-data-contracts>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-datasource-hookconfiguration.html#cfn-qbusiness-datasource-hookconfiguration-s3bucketname
            '''
            result = self._values.get("s3_bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HookConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnDataSourcePropsMixin.ImageExtractionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"image_extraction_status": "imageExtractionStatus"},
    )
    class ImageExtractionConfigurationProperty:
        def __init__(
            self,
            *,
            image_extraction_status: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration for extracting semantic meaning from images in documents.

            For more information, see `Extracting semantic meaning from images and visuals <https://docs.aws.amazon.com/amazonq/latest/qbusiness-ug/extracting-meaning-from-images.html>`_ .

            :param image_extraction_status: Specify whether to extract semantic meaning from images and visuals from documents.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-datasource-imageextractionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
                
                image_extraction_configuration_property = qbusiness_mixins.CfnDataSourcePropsMixin.ImageExtractionConfigurationProperty(
                    image_extraction_status="imageExtractionStatus"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7c31dd7214a114351a9f158c827e8895c5bf076eb82f5028c9d1b5db5765e0a1)
                check_type(argname="argument image_extraction_status", value=image_extraction_status, expected_type=type_hints["image_extraction_status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if image_extraction_status is not None:
                self._values["image_extraction_status"] = image_extraction_status

        @builtins.property
        def image_extraction_status(self) -> typing.Optional[builtins.str]:
            '''Specify whether to extract semantic meaning from images and visuals from documents.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-datasource-imageextractionconfiguration.html#cfn-qbusiness-datasource-imageextractionconfiguration-imageextractionstatus
            '''
            result = self._values.get("image_extraction_status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ImageExtractionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnDataSourcePropsMixin.InlineDocumentEnrichmentConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "condition": "condition",
            "document_content_operator": "documentContentOperator",
            "target": "target",
        },
    )
    class InlineDocumentEnrichmentConfigurationProperty:
        def __init__(
            self,
            *,
            condition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.DocumentAttributeConditionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            document_content_operator: typing.Optional[builtins.str] = None,
            target: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.DocumentAttributeTargetProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Provides the configuration information for applying basic logic to alter document metadata and content when ingesting documents into Amazon Q Business.

            To apply advanced logic, to go beyond what you can do with basic logic, see ```HookConfiguration`` <https://docs.aws.amazon.com/amazonq/latest/api-reference/API_HookConfiguration.html>`_ .

            For more information, see `Custom document enrichment <https://docs.aws.amazon.com/amazonq/latest/business-use-dg/custom-document-enrichment.html>`_ .

            :param condition: Configuration of the condition used for the target document attribute or metadata field when ingesting documents into Amazon Q Business .
            :param document_content_operator: ``TRUE`` to delete content if the condition used for the target attribute is met.
            :param target: Configuration of the target document attribute or metadata field when ingesting documents into Amazon Q Business . You can also include a value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-datasource-inlinedocumentenrichmentconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
                
                inline_document_enrichment_configuration_property = qbusiness_mixins.CfnDataSourcePropsMixin.InlineDocumentEnrichmentConfigurationProperty(
                    condition=qbusiness_mixins.CfnDataSourcePropsMixin.DocumentAttributeConditionProperty(
                        key="key",
                        operator="operator",
                        value=qbusiness_mixins.CfnDataSourcePropsMixin.DocumentAttributeValueProperty(
                            date_value="dateValue",
                            long_value=123,
                            string_list_value=["stringListValue"],
                            string_value="stringValue"
                        )
                    ),
                    document_content_operator="documentContentOperator",
                    target=qbusiness_mixins.CfnDataSourcePropsMixin.DocumentAttributeTargetProperty(
                        attribute_value_operator="attributeValueOperator",
                        key="key",
                        value=qbusiness_mixins.CfnDataSourcePropsMixin.DocumentAttributeValueProperty(
                            date_value="dateValue",
                            long_value=123,
                            string_list_value=["stringListValue"],
                            string_value="stringValue"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9eb79e48f90d83a23f715048411959312e0331b9a4c05e1352bac0fb219e5bed)
                check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
                check_type(argname="argument document_content_operator", value=document_content_operator, expected_type=type_hints["document_content_operator"])
                check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if condition is not None:
                self._values["condition"] = condition
            if document_content_operator is not None:
                self._values["document_content_operator"] = document_content_operator
            if target is not None:
                self._values["target"] = target

        @builtins.property
        def condition(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DocumentAttributeConditionProperty"]]:
            '''Configuration of the condition used for the target document attribute or metadata field when ingesting documents into Amazon Q Business .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-datasource-inlinedocumentenrichmentconfiguration.html#cfn-qbusiness-datasource-inlinedocumentenrichmentconfiguration-condition
            '''
            result = self._values.get("condition")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DocumentAttributeConditionProperty"]], result)

        @builtins.property
        def document_content_operator(self) -> typing.Optional[builtins.str]:
            '''``TRUE`` to delete content if the condition used for the target attribute is met.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-datasource-inlinedocumentenrichmentconfiguration.html#cfn-qbusiness-datasource-inlinedocumentenrichmentconfiguration-documentcontentoperator
            '''
            result = self._values.get("document_content_operator")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DocumentAttributeTargetProperty"]]:
            '''Configuration of the target document attribute or metadata field when ingesting documents into Amazon Q Business .

            You can also include a value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-datasource-inlinedocumentenrichmentconfiguration.html#cfn-qbusiness-datasource-inlinedocumentenrichmentconfiguration-target
            '''
            result = self._values.get("target")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DocumentAttributeTargetProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InlineDocumentEnrichmentConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnDataSourcePropsMixin.MediaExtractionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "audio_extraction_configuration": "audioExtractionConfiguration",
            "image_extraction_configuration": "imageExtractionConfiguration",
            "video_extraction_configuration": "videoExtractionConfiguration",
        },
    )
    class MediaExtractionConfigurationProperty:
        def __init__(
            self,
            *,
            audio_extraction_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.AudioExtractionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            image_extraction_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.ImageExtractionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            video_extraction_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.VideoExtractionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The configuration for extracting information from media in documents.

            :param audio_extraction_configuration: Configuration settings for extracting and processing audio content from media files.
            :param image_extraction_configuration: The configuration for extracting semantic meaning from images in documents. For more information, see `Extracting semantic meaning from images and visuals <https://docs.aws.amazon.com/amazonq/latest/qbusiness-ug/extracting-meaning-from-images.html>`_ .
            :param video_extraction_configuration: Configuration settings for extracting and processing video content from media files.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-datasource-mediaextractionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
                
                media_extraction_configuration_property = qbusiness_mixins.CfnDataSourcePropsMixin.MediaExtractionConfigurationProperty(
                    audio_extraction_configuration=qbusiness_mixins.CfnDataSourcePropsMixin.AudioExtractionConfigurationProperty(
                        audio_extraction_status="audioExtractionStatus"
                    ),
                    image_extraction_configuration=qbusiness_mixins.CfnDataSourcePropsMixin.ImageExtractionConfigurationProperty(
                        image_extraction_status="imageExtractionStatus"
                    ),
                    video_extraction_configuration=qbusiness_mixins.CfnDataSourcePropsMixin.VideoExtractionConfigurationProperty(
                        video_extraction_status="videoExtractionStatus"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e0117d8505fbcf3ae483ba98b7c6f58ef9b679cc654132953eb6e835550a4460)
                check_type(argname="argument audio_extraction_configuration", value=audio_extraction_configuration, expected_type=type_hints["audio_extraction_configuration"])
                check_type(argname="argument image_extraction_configuration", value=image_extraction_configuration, expected_type=type_hints["image_extraction_configuration"])
                check_type(argname="argument video_extraction_configuration", value=video_extraction_configuration, expected_type=type_hints["video_extraction_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if audio_extraction_configuration is not None:
                self._values["audio_extraction_configuration"] = audio_extraction_configuration
            if image_extraction_configuration is not None:
                self._values["image_extraction_configuration"] = image_extraction_configuration
            if video_extraction_configuration is not None:
                self._values["video_extraction_configuration"] = video_extraction_configuration

        @builtins.property
        def audio_extraction_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.AudioExtractionConfigurationProperty"]]:
            '''Configuration settings for extracting and processing audio content from media files.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-datasource-mediaextractionconfiguration.html#cfn-qbusiness-datasource-mediaextractionconfiguration-audioextractionconfiguration
            '''
            result = self._values.get("audio_extraction_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.AudioExtractionConfigurationProperty"]], result)

        @builtins.property
        def image_extraction_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.ImageExtractionConfigurationProperty"]]:
            '''The configuration for extracting semantic meaning from images in documents.

            For more information, see `Extracting semantic meaning from images and visuals <https://docs.aws.amazon.com/amazonq/latest/qbusiness-ug/extracting-meaning-from-images.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-datasource-mediaextractionconfiguration.html#cfn-qbusiness-datasource-mediaextractionconfiguration-imageextractionconfiguration
            '''
            result = self._values.get("image_extraction_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.ImageExtractionConfigurationProperty"]], result)

        @builtins.property
        def video_extraction_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.VideoExtractionConfigurationProperty"]]:
            '''Configuration settings for extracting and processing video content from media files.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-datasource-mediaextractionconfiguration.html#cfn-qbusiness-datasource-mediaextractionconfiguration-videoextractionconfiguration
            '''
            result = self._values.get("video_extraction_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.VideoExtractionConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MediaExtractionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnDataSourcePropsMixin.VideoExtractionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"video_extraction_status": "videoExtractionStatus"},
    )
    class VideoExtractionConfigurationProperty:
        def __init__(
            self,
            *,
            video_extraction_status: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration settings for video content extraction and processing.

            :param video_extraction_status: The status of video extraction (ENABLED or DISABLED) for processing video content from files.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-datasource-videoextractionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
                
                video_extraction_configuration_property = qbusiness_mixins.CfnDataSourcePropsMixin.VideoExtractionConfigurationProperty(
                    video_extraction_status="videoExtractionStatus"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__38295be14311d23bcd66e3be24ea7dd3d403ebb7c4052b34238545ba89f7d884)
                check_type(argname="argument video_extraction_status", value=video_extraction_status, expected_type=type_hints["video_extraction_status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if video_extraction_status is not None:
                self._values["video_extraction_status"] = video_extraction_status

        @builtins.property
        def video_extraction_status(self) -> typing.Optional[builtins.str]:
            '''The status of video extraction (ENABLED or DISABLED) for processing video content from files.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-datasource-videoextractionconfiguration.html#cfn-qbusiness-datasource-videoextractionconfiguration-videoextractionstatus
            '''
            result = self._values.get("video_extraction_status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VideoExtractionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnIndexMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "capacity_configuration": "capacityConfiguration",
        "description": "description",
        "display_name": "displayName",
        "document_attribute_configurations": "documentAttributeConfigurations",
        "tags": "tags",
        "type": "type",
    },
)
class CfnIndexMixinProps:
    def __init__(
        self,
        *,
        application_id: typing.Optional[builtins.str] = None,
        capacity_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIndexPropsMixin.IndexCapacityConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        document_attribute_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIndexPropsMixin.DocumentAttributeConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnIndexPropsMixin.

        :param application_id: The identifier of the Amazon Q Business application using the index.
        :param capacity_configuration: The capacity units you want to provision for your index. You can add and remove capacity to fit your usage needs.
        :param description: A description for the Amazon Q Business index.
        :param display_name: The name of the index.
        :param document_attribute_configurations: Configuration information for document attributes. Document attributes are metadata or fields associated with your documents. For example, the company department name associated with each document. For more information, see `Understanding document attributes <https://docs.aws.amazon.com/amazonq/latest/business-use-dg/doc-attributes.html>`_ .
        :param tags: A list of key-value pairs that identify or categorize the index. You can also use tags to help control access to the index. Tag keys and values can consist of Unicode letters, digits, white space, and any of the following symbols: _ . : / = + -
        :param type: The index type that's suitable for your needs. For more information on what's included in each type of index, see `Amazon Q Business tiers <https://docs.aws.amazon.com/amazonq/latest/qbusiness-ug/tiers.html#index-tiers>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-index.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
            
            cfn_index_mixin_props = qbusiness_mixins.CfnIndexMixinProps(
                application_id="applicationId",
                capacity_configuration=qbusiness_mixins.CfnIndexPropsMixin.IndexCapacityConfigurationProperty(
                    units=123
                ),
                description="description",
                display_name="displayName",
                document_attribute_configurations=[qbusiness_mixins.CfnIndexPropsMixin.DocumentAttributeConfigurationProperty(
                    name="name",
                    search="search",
                    type="type"
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53554ff588af07028f8f1755b4fa0abaf072523a5a21afea1825f6876267c1c2)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument capacity_configuration", value=capacity_configuration, expected_type=type_hints["capacity_configuration"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument document_attribute_configurations", value=document_attribute_configurations, expected_type=type_hints["document_attribute_configurations"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_id is not None:
            self._values["application_id"] = application_id
        if capacity_configuration is not None:
            self._values["capacity_configuration"] = capacity_configuration
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if document_attribute_configurations is not None:
            self._values["document_attribute_configurations"] = document_attribute_configurations
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def application_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the Amazon Q Business application using the index.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-index.html#cfn-qbusiness-index-applicationid
        '''
        result = self._values.get("application_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def capacity_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIndexPropsMixin.IndexCapacityConfigurationProperty"]]:
        '''The capacity units you want to provision for your index.

        You can add and remove capacity to fit your usage needs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-index.html#cfn-qbusiness-index-capacityconfiguration
        '''
        result = self._values.get("capacity_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIndexPropsMixin.IndexCapacityConfigurationProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the Amazon Q Business index.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-index.html#cfn-qbusiness-index-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The name of the index.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-index.html#cfn-qbusiness-index-displayname
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def document_attribute_configurations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIndexPropsMixin.DocumentAttributeConfigurationProperty"]]]]:
        '''Configuration information for document attributes.

        Document attributes are metadata or fields associated with your documents. For example, the company department name associated with each document.

        For more information, see `Understanding document attributes <https://docs.aws.amazon.com/amazonq/latest/business-use-dg/doc-attributes.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-index.html#cfn-qbusiness-index-documentattributeconfigurations
        '''
        result = self._values.get("document_attribute_configurations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIndexPropsMixin.DocumentAttributeConfigurationProperty"]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of key-value pairs that identify or categorize the index.

        You can also use tags to help control access to the index. Tag keys and values can consist of Unicode letters, digits, white space, and any of the following symbols: _ . : / = + -

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-index.html#cfn-qbusiness-index-tags
        :: .
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The index type that's suitable for your needs.

        For more information on what's included in each type of index, see `Amazon Q Business tiers <https://docs.aws.amazon.com/amazonq/latest/qbusiness-ug/tiers.html#index-tiers>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-index.html#cfn-qbusiness-index-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIndexMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnIndexPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnIndexPropsMixin",
):
    '''Creates an Amazon Q Business index.

    To determine if index creation has completed, check the ``Status`` field returned from a call to ``DescribeIndex`` . The ``Status`` field is set to ``ACTIVE`` when the index is ready to use.

    Once the index is active, you can index your documents using the ```BatchPutDocument`` <https://docs.aws.amazon.com/amazonq/latest/api-reference/API_BatchPutDocument.html>`_ API or the ```CreateDataSource`` <https://docs.aws.amazon.com/amazonq/latest/api-reference/API_CreateDataSource.html>`_ API.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-index.html
    :cloudformationResource: AWS::QBusiness::Index
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
        
        cfn_index_props_mixin = qbusiness_mixins.CfnIndexPropsMixin(qbusiness_mixins.CfnIndexMixinProps(
            application_id="applicationId",
            capacity_configuration=qbusiness_mixins.CfnIndexPropsMixin.IndexCapacityConfigurationProperty(
                units=123
            ),
            description="description",
            display_name="displayName",
            document_attribute_configurations=[qbusiness_mixins.CfnIndexPropsMixin.DocumentAttributeConfigurationProperty(
                name="name",
                search="search",
                type="type"
            )],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            type="type"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnIndexMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::QBusiness::Index``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcef6a15e3c6c159f0074fd7193bb18e0ffbbb633959bfe2e033fdcca4a5f3ed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc050d4e5d0ac12b59572a92e733a521c78766e1d87ce9f16b3a3da1c8fcf29c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__153c1648a993600a8195b338fb5685f172a0d1de0aa3c0ac855b4254642c5fd8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnIndexMixinProps:
        return typing.cast(CfnIndexMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnIndexPropsMixin.DocumentAttributeConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "search": "search", "type": "type"},
    )
    class DocumentAttributeConfigurationProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            search: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration information for document attributes.

            Document attributes are metadata or fields associated with your documents. For example, the company department name associated with each document.

            For more information, see `Understanding document attributes <https://docs.aws.amazon.com/amazonq/latest/business-use-dg/doc-attributes.html>`_ .

            :param name: The name of the document attribute.
            :param search: Information about whether the document attribute can be used by an end user to search for information on their web experience.
            :param type: The type of document attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-index-documentattributeconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
                
                document_attribute_configuration_property = qbusiness_mixins.CfnIndexPropsMixin.DocumentAttributeConfigurationProperty(
                    name="name",
                    search="search",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6540f9293221a5ea244e5dd288c052027ee75d0e45b34e2ec0d8651d8c0f215a)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument search", value=search, expected_type=type_hints["search"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if search is not None:
                self._values["search"] = search
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the document attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-index-documentattributeconfiguration.html#cfn-qbusiness-index-documentattributeconfiguration-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def search(self) -> typing.Optional[builtins.str]:
            '''Information about whether the document attribute can be used by an end user to search for information on their web experience.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-index-documentattributeconfiguration.html#cfn-qbusiness-index-documentattributeconfiguration-search
            '''
            result = self._values.get("search")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of document attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-index-documentattributeconfiguration.html#cfn-qbusiness-index-documentattributeconfiguration-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DocumentAttributeConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnIndexPropsMixin.IndexCapacityConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"units": "units"},
    )
    class IndexCapacityConfigurationProperty:
        def __init__(self, *, units: typing.Optional[jsii.Number] = None) -> None:
            '''Provides information about index capacity configuration.

            :param units: The number of storage units configured for an Amazon Q Business index.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-index-indexcapacityconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
                
                index_capacity_configuration_property = qbusiness_mixins.CfnIndexPropsMixin.IndexCapacityConfigurationProperty(
                    units=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c039394c6b9d12ab7c38c90173785029a062b30cf8c29289a723f41763d365f5)
                check_type(argname="argument units", value=units, expected_type=type_hints["units"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if units is not None:
                self._values["units"] = units

        @builtins.property
        def units(self) -> typing.Optional[jsii.Number]:
            '''The number of storage units configured for an Amazon Q Business index.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-index-indexcapacityconfiguration.html#cfn-qbusiness-index-indexcapacityconfiguration-units
            '''
            result = self._values.get("units")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IndexCapacityConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnIndexPropsMixin.IndexStatisticsProperty",
        jsii_struct_bases=[],
        name_mapping={"text_document_statistics": "textDocumentStatistics"},
    )
    class IndexStatisticsProperty:
        def __init__(
            self,
            *,
            text_document_statistics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIndexPropsMixin.TextDocumentStatisticsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Provides information about the number of documents in an index.

            :param text_document_statistics: The number of documents indexed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-index-indexstatistics.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
                
                index_statistics_property = qbusiness_mixins.CfnIndexPropsMixin.IndexStatisticsProperty(
                    text_document_statistics=qbusiness_mixins.CfnIndexPropsMixin.TextDocumentStatisticsProperty(
                        indexed_text_bytes=123,
                        indexed_text_document_count=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__22f20ff2d96d1191dad912b8598e6edbaad0c80820df3471ffd03438f1fda87a)
                check_type(argname="argument text_document_statistics", value=text_document_statistics, expected_type=type_hints["text_document_statistics"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if text_document_statistics is not None:
                self._values["text_document_statistics"] = text_document_statistics

        @builtins.property
        def text_document_statistics(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIndexPropsMixin.TextDocumentStatisticsProperty"]]:
            '''The number of documents indexed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-index-indexstatistics.html#cfn-qbusiness-index-indexstatistics-textdocumentstatistics
            '''
            result = self._values.get("text_document_statistics")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIndexPropsMixin.TextDocumentStatisticsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IndexStatisticsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnIndexPropsMixin.TextDocumentStatisticsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "indexed_text_bytes": "indexedTextBytes",
            "indexed_text_document_count": "indexedTextDocumentCount",
        },
    )
    class TextDocumentStatisticsProperty:
        def __init__(
            self,
            *,
            indexed_text_bytes: typing.Optional[jsii.Number] = None,
            indexed_text_document_count: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Provides information about text documents in an index.

            :param indexed_text_bytes: The total size, in bytes, of the indexed documents.
            :param indexed_text_document_count: The number of text documents indexed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-index-textdocumentstatistics.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
                
                text_document_statistics_property = qbusiness_mixins.CfnIndexPropsMixin.TextDocumentStatisticsProperty(
                    indexed_text_bytes=123,
                    indexed_text_document_count=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4dc1b1951c6658ad7f8105ed69eca043f737170dad0a367e0a98f8ada886705a)
                check_type(argname="argument indexed_text_bytes", value=indexed_text_bytes, expected_type=type_hints["indexed_text_bytes"])
                check_type(argname="argument indexed_text_document_count", value=indexed_text_document_count, expected_type=type_hints["indexed_text_document_count"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if indexed_text_bytes is not None:
                self._values["indexed_text_bytes"] = indexed_text_bytes
            if indexed_text_document_count is not None:
                self._values["indexed_text_document_count"] = indexed_text_document_count

        @builtins.property
        def indexed_text_bytes(self) -> typing.Optional[jsii.Number]:
            '''The total size, in bytes, of the indexed documents.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-index-textdocumentstatistics.html#cfn-qbusiness-index-textdocumentstatistics-indexedtextbytes
            '''
            result = self._values.get("indexed_text_bytes")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def indexed_text_document_count(self) -> typing.Optional[jsii.Number]:
            '''The number of text documents indexed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-index-textdocumentstatistics.html#cfn-qbusiness-index-textdocumentstatistics-indexedtextdocumentcount
            '''
            result = self._values.get("indexed_text_document_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TextDocumentStatisticsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnPermissionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "actions": "actions",
        "application_id": "applicationId",
        "conditions": "conditions",
        "principal": "principal",
        "statement_id": "statementId",
    },
)
class CfnPermissionMixinProps:
    def __init__(
        self,
        *,
        actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        application_id: typing.Optional[builtins.str] = None,
        conditions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPermissionPropsMixin.ConditionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        principal: typing.Optional[builtins.str] = None,
        statement_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnPermissionPropsMixin.

        :param actions: The list of Amazon Q Business actions that the ISV is allowed to perform.
        :param application_id: The unique identifier of the Amazon Q Business application.
        :param conditions: 
        :param principal: Provides user and group information used for filtering documents to use for generating Amazon Q Business conversation responses.
        :param statement_id: A unique identifier for the policy statement.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-permission.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
            
            cfn_permission_mixin_props = qbusiness_mixins.CfnPermissionMixinProps(
                actions=["actions"],
                application_id="applicationId",
                conditions=[qbusiness_mixins.CfnPermissionPropsMixin.ConditionProperty(
                    condition_key="conditionKey",
                    condition_operator="conditionOperator",
                    condition_values=["conditionValues"]
                )],
                principal="principal",
                statement_id="statementId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c86da2da938978223d99601fe2837cf2c1c97f78e8a75d6c5ab7219124bda65b)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
            check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
            check_type(argname="argument statement_id", value=statement_id, expected_type=type_hints["statement_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if actions is not None:
            self._values["actions"] = actions
        if application_id is not None:
            self._values["application_id"] = application_id
        if conditions is not None:
            self._values["conditions"] = conditions
        if principal is not None:
            self._values["principal"] = principal
        if statement_id is not None:
            self._values["statement_id"] = statement_id

    @builtins.property
    def actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of Amazon Q Business actions that the ISV is allowed to perform.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-permission.html#cfn-qbusiness-permission-actions
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def application_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the Amazon Q Business application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-permission.html#cfn-qbusiness-permission-applicationid
        '''
        result = self._values.get("application_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def conditions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPermissionPropsMixin.ConditionProperty"]]]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-permission.html#cfn-qbusiness-permission-conditions
        '''
        result = self._values.get("conditions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPermissionPropsMixin.ConditionProperty"]]]], result)

    @builtins.property
    def principal(self) -> typing.Optional[builtins.str]:
        '''Provides user and group information used for filtering documents to use for generating Amazon Q Business conversation responses.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-permission.html#cfn-qbusiness-permission-principal
        '''
        result = self._values.get("principal")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def statement_id(self) -> typing.Optional[builtins.str]:
        '''A unique identifier for the policy statement.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-permission.html#cfn-qbusiness-permission-statementid
        '''
        result = self._values.get("statement_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPermissionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPermissionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnPermissionPropsMixin",
):
    '''Adds or updates a permission policy for a Amazon Q Business application, allowing cross-account access for an ISV.

    This operation creates a new policy statement for the specified Amazon Q Business application. The policy statement defines the IAM actions that the ISV is allowed to perform on the Amazon Q Business application's resources.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-permission.html
    :cloudformationResource: AWS::QBusiness::Permission
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
        
        cfn_permission_props_mixin = qbusiness_mixins.CfnPermissionPropsMixin(qbusiness_mixins.CfnPermissionMixinProps(
            actions=["actions"],
            application_id="applicationId",
            conditions=[qbusiness_mixins.CfnPermissionPropsMixin.ConditionProperty(
                condition_key="conditionKey",
                condition_operator="conditionOperator",
                condition_values=["conditionValues"]
            )],
            principal="principal",
            statement_id="statementId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnPermissionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::QBusiness::Permission``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba4f7f747671dde747450e52a446a9ddcfcdfbb58c1c8cc75c423002e6cb8b85)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c2dbeb37071cc96ab48a40394b55e11b0061efe52a62a39296ffb3f7d898bbb)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab38a6f5215c74810c54d8a2c480497521dcb2bdcfeae4d1a0eab3109a3ec79a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPermissionMixinProps:
        return typing.cast(CfnPermissionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnPermissionPropsMixin.ConditionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "condition_key": "conditionKey",
            "condition_operator": "conditionOperator",
            "condition_values": "conditionValues",
        },
    )
    class ConditionProperty:
        def __init__(
            self,
            *,
            condition_key: typing.Optional[builtins.str] = None,
            condition_operator: typing.Optional[builtins.str] = None,
            condition_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''
            :param condition_key: 
            :param condition_operator: 
            :param condition_values: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-permission-condition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
                
                condition_property = qbusiness_mixins.CfnPermissionPropsMixin.ConditionProperty(
                    condition_key="conditionKey",
                    condition_operator="conditionOperator",
                    condition_values=["conditionValues"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__055ce9b6472cc34499f662d0b16baafb97f1ed480c1dcb1a6af31e6ceddc0a13)
                check_type(argname="argument condition_key", value=condition_key, expected_type=type_hints["condition_key"])
                check_type(argname="argument condition_operator", value=condition_operator, expected_type=type_hints["condition_operator"])
                check_type(argname="argument condition_values", value=condition_values, expected_type=type_hints["condition_values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if condition_key is not None:
                self._values["condition_key"] = condition_key
            if condition_operator is not None:
                self._values["condition_operator"] = condition_operator
            if condition_values is not None:
                self._values["condition_values"] = condition_values

        @builtins.property
        def condition_key(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-permission-condition.html#cfn-qbusiness-permission-condition-conditionkey
            '''
            result = self._values.get("condition_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def condition_operator(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-permission-condition.html#cfn-qbusiness-permission-condition-conditionoperator
            '''
            result = self._values.get("condition_operator")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def condition_values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-permission-condition.html#cfn-qbusiness-permission-condition-conditionvalues
            '''
            result = self._values.get("condition_values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConditionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnPluginMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "auth_configuration": "authConfiguration",
        "custom_plugin_configuration": "customPluginConfiguration",
        "display_name": "displayName",
        "server_url": "serverUrl",
        "state": "state",
        "tags": "tags",
        "type": "type",
    },
)
class CfnPluginMixinProps:
    def __init__(
        self,
        *,
        application_id: typing.Optional[builtins.str] = None,
        auth_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPluginPropsMixin.PluginAuthConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        custom_plugin_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPluginPropsMixin.CustomPluginConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        display_name: typing.Optional[builtins.str] = None,
        server_url: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnPluginPropsMixin.

        :param application_id: The identifier of the application that will contain the plugin.
        :param auth_configuration: Authentication configuration information for an Amazon Q Business plugin.
        :param custom_plugin_configuration: Configuration information required to create a custom plugin.
        :param display_name: The name of the plugin.
        :param server_url: The plugin server URL used for configuration.
        :param state: The current status of the plugin.
        :param tags: A list of key-value pairs that identify or categorize the data source connector. You can also use tags to help control access to the data source connector. Tag keys and values can consist of Unicode letters, digits, white space, and any of the following symbols: _ . : / = + -
        :param type: The type of the plugin.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-plugin.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
            
            # no_auth_configuration: Any
            
            cfn_plugin_mixin_props = qbusiness_mixins.CfnPluginMixinProps(
                application_id="applicationId",
                auth_configuration=qbusiness_mixins.CfnPluginPropsMixin.PluginAuthConfigurationProperty(
                    basic_auth_configuration=qbusiness_mixins.CfnPluginPropsMixin.BasicAuthConfigurationProperty(
                        role_arn="roleArn",
                        secret_arn="secretArn"
                    ),
                    no_auth_configuration=no_auth_configuration,
                    o_auth2_client_credential_configuration=qbusiness_mixins.CfnPluginPropsMixin.OAuth2ClientCredentialConfigurationProperty(
                        authorization_url="authorizationUrl",
                        role_arn="roleArn",
                        secret_arn="secretArn",
                        token_url="tokenUrl"
                    )
                ),
                custom_plugin_configuration=qbusiness_mixins.CfnPluginPropsMixin.CustomPluginConfigurationProperty(
                    api_schema=qbusiness_mixins.CfnPluginPropsMixin.APISchemaProperty(
                        payload="payload",
                        s3=qbusiness_mixins.CfnPluginPropsMixin.S3Property(
                            bucket="bucket",
                            key="key"
                        )
                    ),
                    api_schema_type="apiSchemaType",
                    description="description"
                ),
                display_name="displayName",
                server_url="serverUrl",
                state="state",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34f690c39af0ef12a05631e2c7a6386ac67cd9f5bd9ec31f738257ba025dca1a)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument auth_configuration", value=auth_configuration, expected_type=type_hints["auth_configuration"])
            check_type(argname="argument custom_plugin_configuration", value=custom_plugin_configuration, expected_type=type_hints["custom_plugin_configuration"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument server_url", value=server_url, expected_type=type_hints["server_url"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_id is not None:
            self._values["application_id"] = application_id
        if auth_configuration is not None:
            self._values["auth_configuration"] = auth_configuration
        if custom_plugin_configuration is not None:
            self._values["custom_plugin_configuration"] = custom_plugin_configuration
        if display_name is not None:
            self._values["display_name"] = display_name
        if server_url is not None:
            self._values["server_url"] = server_url
        if state is not None:
            self._values["state"] = state
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def application_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the application that will contain the plugin.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-plugin.html#cfn-qbusiness-plugin-applicationid
        '''
        result = self._values.get("application_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auth_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPluginPropsMixin.PluginAuthConfigurationProperty"]]:
        '''Authentication configuration information for an Amazon Q Business plugin.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-plugin.html#cfn-qbusiness-plugin-authconfiguration
        '''
        result = self._values.get("auth_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPluginPropsMixin.PluginAuthConfigurationProperty"]], result)

    @builtins.property
    def custom_plugin_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPluginPropsMixin.CustomPluginConfigurationProperty"]]:
        '''Configuration information required to create a custom plugin.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-plugin.html#cfn-qbusiness-plugin-custompluginconfiguration
        '''
        result = self._values.get("custom_plugin_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPluginPropsMixin.CustomPluginConfigurationProperty"]], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The name of the plugin.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-plugin.html#cfn-qbusiness-plugin-displayname
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_url(self) -> typing.Optional[builtins.str]:
        '''The plugin server URL used for configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-plugin.html#cfn-qbusiness-plugin-serverurl
        '''
        result = self._values.get("server_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''The current status of the plugin.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-plugin.html#cfn-qbusiness-plugin-state
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of key-value pairs that identify or categorize the data source connector.

        You can also use tags to help control access to the data source connector. Tag keys and values can consist of Unicode letters, digits, white space, and any of the following symbols: _ . : / = + -

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-plugin.html#cfn-qbusiness-plugin-tags
        :: .
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of the plugin.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-plugin.html#cfn-qbusiness-plugin-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPluginMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPluginPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnPluginPropsMixin",
):
    '''Information about an Amazon Q Business plugin and its configuration.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-plugin.html
    :cloudformationResource: AWS::QBusiness::Plugin
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
        
        # no_auth_configuration: Any
        
        cfn_plugin_props_mixin = qbusiness_mixins.CfnPluginPropsMixin(qbusiness_mixins.CfnPluginMixinProps(
            application_id="applicationId",
            auth_configuration=qbusiness_mixins.CfnPluginPropsMixin.PluginAuthConfigurationProperty(
                basic_auth_configuration=qbusiness_mixins.CfnPluginPropsMixin.BasicAuthConfigurationProperty(
                    role_arn="roleArn",
                    secret_arn="secretArn"
                ),
                no_auth_configuration=no_auth_configuration,
                o_auth2_client_credential_configuration=qbusiness_mixins.CfnPluginPropsMixin.OAuth2ClientCredentialConfigurationProperty(
                    authorization_url="authorizationUrl",
                    role_arn="roleArn",
                    secret_arn="secretArn",
                    token_url="tokenUrl"
                )
            ),
            custom_plugin_configuration=qbusiness_mixins.CfnPluginPropsMixin.CustomPluginConfigurationProperty(
                api_schema=qbusiness_mixins.CfnPluginPropsMixin.APISchemaProperty(
                    payload="payload",
                    s3=qbusiness_mixins.CfnPluginPropsMixin.S3Property(
                        bucket="bucket",
                        key="key"
                    )
                ),
                api_schema_type="apiSchemaType",
                description="description"
            ),
            display_name="displayName",
            server_url="serverUrl",
            state="state",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            type="type"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnPluginMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::QBusiness::Plugin``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b9fd4966aae59f2d65e5bdc645692fb20f2d2639d7694dacd2367379a113e4b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__900715ffcacaeca4015718dbb6c7d5287dcaf5812151aa980193a13fe18ffbd5)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fc3337cfa999b69d186d22cd5450d925ce0e48085e3295755b4afc021b7ba9d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPluginMixinProps:
        return typing.cast(CfnPluginMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnPluginPropsMixin.APISchemaProperty",
        jsii_struct_bases=[],
        name_mapping={"payload": "payload", "s3": "s3"},
    )
    class APISchemaProperty:
        def __init__(
            self,
            *,
            payload: typing.Optional[builtins.str] = None,
            s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPluginPropsMixin.S3Property", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains details about the OpenAPI schema for a custom plugin.

            For more information, see `custom plugin OpenAPI schemas <https://docs.aws.amazon.com/amazonq/latest/qbusiness-ug/custom-plugin.html#plugins-api-schema>`_ . You can either include the schema directly in the payload field or you can upload it to an S3 bucket and specify the S3 bucket location in the ``s3`` field.

            :param payload: The JSON or YAML-formatted payload defining the OpenAPI schema for a custom plugin.
            :param s3: Contains details about the S3 object containing the OpenAPI schema for a custom plugin. The schema could be in either JSON or YAML format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-plugin-apischema.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
                
                a_pISchema_property = qbusiness_mixins.CfnPluginPropsMixin.APISchemaProperty(
                    payload="payload",
                    s3=qbusiness_mixins.CfnPluginPropsMixin.S3Property(
                        bucket="bucket",
                        key="key"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__baa4f41339b887ecb75f681121e05353ed3ee484c9ba3043c9bffe125c89ac96)
                check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
                check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if payload is not None:
                self._values["payload"] = payload
            if s3 is not None:
                self._values["s3"] = s3

        @builtins.property
        def payload(self) -> typing.Optional[builtins.str]:
            '''The JSON or YAML-formatted payload defining the OpenAPI schema for a custom plugin.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-plugin-apischema.html#cfn-qbusiness-plugin-apischema-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPluginPropsMixin.S3Property"]]:
            '''Contains details about the S3 object containing the OpenAPI schema for a custom plugin.

            The schema could be in either JSON or YAML format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-plugin-apischema.html#cfn-qbusiness-plugin-apischema-s3
            '''
            result = self._values.get("s3")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPluginPropsMixin.S3Property"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "APISchemaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnPluginPropsMixin.BasicAuthConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"role_arn": "roleArn", "secret_arn": "secretArn"},
    )
    class BasicAuthConfigurationProperty:
        def __init__(
            self,
            *,
            role_arn: typing.Optional[builtins.str] = None,
            secret_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about the basic authentication credentials used to configure a plugin.

            :param role_arn: The ARN of an IAM role used by Amazon Q Business to access the basic authentication credentials stored in a Secrets Manager secret.
            :param secret_arn: The ARN of the Secrets Manager secret that stores the basic authentication credentials used for plugin configuration..

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-plugin-basicauthconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
                
                basic_auth_configuration_property = qbusiness_mixins.CfnPluginPropsMixin.BasicAuthConfigurationProperty(
                    role_arn="roleArn",
                    secret_arn="secretArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3472a50e64be444e96e6c05249afdcfade38150163d364ea279160a1b05fc0f1)
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if secret_arn is not None:
                self._values["secret_arn"] = secret_arn

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of an IAM role used by Amazon Q Business to access the basic authentication credentials stored in a Secrets Manager secret.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-plugin-basicauthconfiguration.html#cfn-qbusiness-plugin-basicauthconfiguration-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secret_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the Secrets Manager secret that stores the basic authentication credentials used for plugin configuration..

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-plugin-basicauthconfiguration.html#cfn-qbusiness-plugin-basicauthconfiguration-secretarn
            '''
            result = self._values.get("secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BasicAuthConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnPluginPropsMixin.CustomPluginConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "api_schema": "apiSchema",
            "api_schema_type": "apiSchemaType",
            "description": "description",
        },
    )
    class CustomPluginConfigurationProperty:
        def __init__(
            self,
            *,
            api_schema: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPluginPropsMixin.APISchemaProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            api_schema_type: typing.Optional[builtins.str] = None,
            description: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration information required to create a custom plugin.

            :param api_schema: Contains either details about the S3 object containing the OpenAPI schema for the action group or the JSON or YAML-formatted payload defining the schema.
            :param api_schema_type: The type of OpenAPI schema to use.
            :param description: A description for your custom plugin configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-plugin-custompluginconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
                
                custom_plugin_configuration_property = qbusiness_mixins.CfnPluginPropsMixin.CustomPluginConfigurationProperty(
                    api_schema=qbusiness_mixins.CfnPluginPropsMixin.APISchemaProperty(
                        payload="payload",
                        s3=qbusiness_mixins.CfnPluginPropsMixin.S3Property(
                            bucket="bucket",
                            key="key"
                        )
                    ),
                    api_schema_type="apiSchemaType",
                    description="description"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b4bf971e3152958a9beb006a6380a4eb87bbdbf13032c26f522f63973b20d8b0)
                check_type(argname="argument api_schema", value=api_schema, expected_type=type_hints["api_schema"])
                check_type(argname="argument api_schema_type", value=api_schema_type, expected_type=type_hints["api_schema_type"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if api_schema is not None:
                self._values["api_schema"] = api_schema
            if api_schema_type is not None:
                self._values["api_schema_type"] = api_schema_type
            if description is not None:
                self._values["description"] = description

        @builtins.property
        def api_schema(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPluginPropsMixin.APISchemaProperty"]]:
            '''Contains either details about the S3 object containing the OpenAPI schema for the action group or the JSON or YAML-formatted payload defining the schema.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-plugin-custompluginconfiguration.html#cfn-qbusiness-plugin-custompluginconfiguration-apischema
            '''
            result = self._values.get("api_schema")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPluginPropsMixin.APISchemaProperty"]], result)

        @builtins.property
        def api_schema_type(self) -> typing.Optional[builtins.str]:
            '''The type of OpenAPI schema to use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-plugin-custompluginconfiguration.html#cfn-qbusiness-plugin-custompluginconfiguration-apischematype
            '''
            result = self._values.get("api_schema_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''A description for your custom plugin configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-plugin-custompluginconfiguration.html#cfn-qbusiness-plugin-custompluginconfiguration-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomPluginConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnPluginPropsMixin.OAuth2ClientCredentialConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "authorization_url": "authorizationUrl",
            "role_arn": "roleArn",
            "secret_arn": "secretArn",
            "token_url": "tokenUrl",
        },
    )
    class OAuth2ClientCredentialConfigurationProperty:
        def __init__(
            self,
            *,
            authorization_url: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
            secret_arn: typing.Optional[builtins.str] = None,
            token_url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about the OAuth 2.0 authentication credential/token used to configure a plugin.

            :param authorization_url: The redirect URL required by the OAuth 2.0 protocol for Amazon Q Business to authenticate a plugin user through a third party authentication server.
            :param role_arn: The ARN of an IAM role used by Amazon Q Business to access the OAuth 2.0 authentication credentials stored in a Secrets Manager secret.
            :param secret_arn: The ARN of the Secrets Manager secret that stores the OAuth 2.0 credentials/token used for plugin configuration.
            :param token_url: The URL required by the OAuth 2.0 protocol to exchange an end user authorization code for an access token.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-plugin-oauth2clientcredentialconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
                
                o_auth2_client_credential_configuration_property = qbusiness_mixins.CfnPluginPropsMixin.OAuth2ClientCredentialConfigurationProperty(
                    authorization_url="authorizationUrl",
                    role_arn="roleArn",
                    secret_arn="secretArn",
                    token_url="tokenUrl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__567bfc234c019a7e23c4fe3c393f8e60d23537043ffccb404790878128ffd94e)
                check_type(argname="argument authorization_url", value=authorization_url, expected_type=type_hints["authorization_url"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
                check_type(argname="argument token_url", value=token_url, expected_type=type_hints["token_url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if authorization_url is not None:
                self._values["authorization_url"] = authorization_url
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if secret_arn is not None:
                self._values["secret_arn"] = secret_arn
            if token_url is not None:
                self._values["token_url"] = token_url

        @builtins.property
        def authorization_url(self) -> typing.Optional[builtins.str]:
            '''The redirect URL required by the OAuth 2.0 protocol for Amazon Q Business to authenticate a plugin user through a third party authentication server.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-plugin-oauth2clientcredentialconfiguration.html#cfn-qbusiness-plugin-oauth2clientcredentialconfiguration-authorizationurl
            '''
            result = self._values.get("authorization_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of an IAM role used by Amazon Q Business to access the OAuth 2.0 authentication credentials stored in a Secrets Manager secret.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-plugin-oauth2clientcredentialconfiguration.html#cfn-qbusiness-plugin-oauth2clientcredentialconfiguration-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secret_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the Secrets Manager secret that stores the OAuth 2.0 credentials/token used for plugin configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-plugin-oauth2clientcredentialconfiguration.html#cfn-qbusiness-plugin-oauth2clientcredentialconfiguration-secretarn
            '''
            result = self._values.get("secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def token_url(self) -> typing.Optional[builtins.str]:
            '''The URL required by the OAuth 2.0 protocol to exchange an end user authorization code for an access token.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-plugin-oauth2clientcredentialconfiguration.html#cfn-qbusiness-plugin-oauth2clientcredentialconfiguration-tokenurl
            '''
            result = self._values.get("token_url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OAuth2ClientCredentialConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnPluginPropsMixin.PluginAuthConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "basic_auth_configuration": "basicAuthConfiguration",
            "no_auth_configuration": "noAuthConfiguration",
            "o_auth2_client_credential_configuration": "oAuth2ClientCredentialConfiguration",
        },
    )
    class PluginAuthConfigurationProperty:
        def __init__(
            self,
            *,
            basic_auth_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPluginPropsMixin.BasicAuthConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            no_auth_configuration: typing.Any = None,
            o_auth2_client_credential_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPluginPropsMixin.OAuth2ClientCredentialConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Authentication configuration information for an Amazon Q Business plugin.

            :param basic_auth_configuration: Information about the basic authentication credentials used to configure a plugin.
            :param no_auth_configuration: Information about invoking a custom plugin without any authentication.
            :param o_auth2_client_credential_configuration: Information about the OAuth 2.0 authentication credential/token used to configure a plugin.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-plugin-pluginauthconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
                
                # no_auth_configuration: Any
                
                plugin_auth_configuration_property = qbusiness_mixins.CfnPluginPropsMixin.PluginAuthConfigurationProperty(
                    basic_auth_configuration=qbusiness_mixins.CfnPluginPropsMixin.BasicAuthConfigurationProperty(
                        role_arn="roleArn",
                        secret_arn="secretArn"
                    ),
                    no_auth_configuration=no_auth_configuration,
                    o_auth2_client_credential_configuration=qbusiness_mixins.CfnPluginPropsMixin.OAuth2ClientCredentialConfigurationProperty(
                        authorization_url="authorizationUrl",
                        role_arn="roleArn",
                        secret_arn="secretArn",
                        token_url="tokenUrl"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bee46e23e5ad71281db51cde9fffd2beb666f51f4e16efbaaf0ed66491695eee)
                check_type(argname="argument basic_auth_configuration", value=basic_auth_configuration, expected_type=type_hints["basic_auth_configuration"])
                check_type(argname="argument no_auth_configuration", value=no_auth_configuration, expected_type=type_hints["no_auth_configuration"])
                check_type(argname="argument o_auth2_client_credential_configuration", value=o_auth2_client_credential_configuration, expected_type=type_hints["o_auth2_client_credential_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if basic_auth_configuration is not None:
                self._values["basic_auth_configuration"] = basic_auth_configuration
            if no_auth_configuration is not None:
                self._values["no_auth_configuration"] = no_auth_configuration
            if o_auth2_client_credential_configuration is not None:
                self._values["o_auth2_client_credential_configuration"] = o_auth2_client_credential_configuration

        @builtins.property
        def basic_auth_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPluginPropsMixin.BasicAuthConfigurationProperty"]]:
            '''Information about the basic authentication credentials used to configure a plugin.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-plugin-pluginauthconfiguration.html#cfn-qbusiness-plugin-pluginauthconfiguration-basicauthconfiguration
            '''
            result = self._values.get("basic_auth_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPluginPropsMixin.BasicAuthConfigurationProperty"]], result)

        @builtins.property
        def no_auth_configuration(self) -> typing.Any:
            '''Information about invoking a custom plugin without any authentication.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-plugin-pluginauthconfiguration.html#cfn-qbusiness-plugin-pluginauthconfiguration-noauthconfiguration
            '''
            result = self._values.get("no_auth_configuration")
            return typing.cast(typing.Any, result)

        @builtins.property
        def o_auth2_client_credential_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPluginPropsMixin.OAuth2ClientCredentialConfigurationProperty"]]:
            '''Information about the OAuth 2.0 authentication credential/token used to configure a plugin.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-plugin-pluginauthconfiguration.html#cfn-qbusiness-plugin-pluginauthconfiguration-oauth2clientcredentialconfiguration
            '''
            result = self._values.get("o_auth2_client_credential_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPluginPropsMixin.OAuth2ClientCredentialConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PluginAuthConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnPluginPropsMixin.S3Property",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "key": "key"},
    )
    class S3Property:
        def __init__(
            self,
            *,
            bucket: typing.Optional[builtins.str] = None,
            key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information required for Amazon Q Business to find a specific file in an Amazon S3 bucket.

            :param bucket: The name of the S3 bucket that contains the file.
            :param key: The name of the file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-plugin-s3.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
                
                s3_property = qbusiness_mixins.CfnPluginPropsMixin.S3Property(
                    bucket="bucket",
                    key="key"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2a565d061d5a08fb3aeded624e0213366e45f3fb2988da629947fcf6d433af3a)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket is not None:
                self._values["bucket"] = bucket
            if key is not None:
                self._values["key"] = key

        @builtins.property
        def bucket(self) -> typing.Optional[builtins.str]:
            '''The name of the S3 bucket that contains the file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-plugin-s3.html#cfn-qbusiness-plugin-s3-bucket
            '''
            result = self._values.get("bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The name of the file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-plugin-s3.html#cfn-qbusiness-plugin-s3-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnRetrieverMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "configuration": "configuration",
        "display_name": "displayName",
        "role_arn": "roleArn",
        "tags": "tags",
        "type": "type",
    },
)
class CfnRetrieverMixinProps:
    def __init__(
        self,
        *,
        application_id: typing.Optional[builtins.str] = None,
        configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRetrieverPropsMixin.RetrieverConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        display_name: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnRetrieverPropsMixin.

        :param application_id: The identifier of the Amazon Q Business application using the retriever.
        :param configuration: Provides information on how the retriever used for your Amazon Q Business application is configured.
        :param display_name: The name of your retriever.
        :param role_arn: The ARN of an IAM role used by Amazon Q Business to access the basic authentication credentials stored in a Secrets Manager secret.
        :param tags: A list of key-value pairs that identify or categorize the retriever. You can also use tags to help control access to the retriever. Tag keys and values can consist of Unicode letters, digits, white space, and any of the following symbols: _ . : / = + -
        :param type: The type of your retriever.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-retriever.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
            
            cfn_retriever_mixin_props = qbusiness_mixins.CfnRetrieverMixinProps(
                application_id="applicationId",
                configuration=qbusiness_mixins.CfnRetrieverPropsMixin.RetrieverConfigurationProperty(
                    kendra_index_configuration=qbusiness_mixins.CfnRetrieverPropsMixin.KendraIndexConfigurationProperty(
                        index_id="indexId"
                    ),
                    native_index_configuration=qbusiness_mixins.CfnRetrieverPropsMixin.NativeIndexConfigurationProperty(
                        index_id="indexId"
                    )
                ),
                display_name="displayName",
                role_arn="roleArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83b0fa260c1158e721d7411a56d3647f49b62e3c55a1162a988dc823ac81b414)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_id is not None:
            self._values["application_id"] = application_id
        if configuration is not None:
            self._values["configuration"] = configuration
        if display_name is not None:
            self._values["display_name"] = display_name
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def application_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the Amazon Q Business application using the retriever.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-retriever.html#cfn-qbusiness-retriever-applicationid
        '''
        result = self._values.get("application_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRetrieverPropsMixin.RetrieverConfigurationProperty"]]:
        '''Provides information on how the retriever used for your Amazon Q Business application is configured.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-retriever.html#cfn-qbusiness-retriever-configuration
        '''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRetrieverPropsMixin.RetrieverConfigurationProperty"]], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The name of your retriever.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-retriever.html#cfn-qbusiness-retriever-displayname
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of an IAM role used by Amazon Q Business to access the basic authentication credentials stored in a Secrets Manager secret.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-retriever.html#cfn-qbusiness-retriever-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of key-value pairs that identify or categorize the retriever.

        You can also use tags to help control access to the retriever. Tag keys and values can consist of Unicode letters, digits, white space, and any of the following symbols: _ . : / = + -

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-retriever.html#cfn-qbusiness-retriever-tags
        :: .
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of your retriever.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-retriever.html#cfn-qbusiness-retriever-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRetrieverMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnRetrieverPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnRetrieverPropsMixin",
):
    '''Adds a retriever to your Amazon Q Business application.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-retriever.html
    :cloudformationResource: AWS::QBusiness::Retriever
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
        
        cfn_retriever_props_mixin = qbusiness_mixins.CfnRetrieverPropsMixin(qbusiness_mixins.CfnRetrieverMixinProps(
            application_id="applicationId",
            configuration=qbusiness_mixins.CfnRetrieverPropsMixin.RetrieverConfigurationProperty(
                kendra_index_configuration=qbusiness_mixins.CfnRetrieverPropsMixin.KendraIndexConfigurationProperty(
                    index_id="indexId"
                ),
                native_index_configuration=qbusiness_mixins.CfnRetrieverPropsMixin.NativeIndexConfigurationProperty(
                    index_id="indexId"
                )
            ),
            display_name="displayName",
            role_arn="roleArn",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            type="type"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnRetrieverMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::QBusiness::Retriever``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a9aa58a6435b7623c66b0ab48ff481b3d1ecb3b9baa8486a185a4e171d0db3f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__14a05691bc76f71042311627a3b3b4532b892c30213aee77ef731995f0b59798)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4123022e86c05d4409b4a86c1211340542defd1301381cb01d8d47ed07c4881)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnRetrieverMixinProps:
        return typing.cast(CfnRetrieverMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnRetrieverPropsMixin.KendraIndexConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"index_id": "indexId"},
    )
    class KendraIndexConfigurationProperty:
        def __init__(self, *, index_id: typing.Optional[builtins.str] = None) -> None:
            '''Stores an Amazon Kendra index as a retriever.

            :param index_id: The identifier of the Amazon Kendra index.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-retriever-kendraindexconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
                
                kendra_index_configuration_property = qbusiness_mixins.CfnRetrieverPropsMixin.KendraIndexConfigurationProperty(
                    index_id="indexId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__242cc13e90371ff4552607488c9582355454d936dabf353ca82af90a73c37439)
                check_type(argname="argument index_id", value=index_id, expected_type=type_hints["index_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if index_id is not None:
                self._values["index_id"] = index_id

        @builtins.property
        def index_id(self) -> typing.Optional[builtins.str]:
            '''The identifier of the Amazon Kendra index.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-retriever-kendraindexconfiguration.html#cfn-qbusiness-retriever-kendraindexconfiguration-indexid
            '''
            result = self._values.get("index_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KendraIndexConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnRetrieverPropsMixin.NativeIndexConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"index_id": "indexId"},
    )
    class NativeIndexConfigurationProperty:
        def __init__(self, *, index_id: typing.Optional[builtins.str] = None) -> None:
            '''Configuration information for an Amazon Q Business index.

            :param index_id: The identifier for the Amazon Q Business index.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-retriever-nativeindexconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
                
                native_index_configuration_property = qbusiness_mixins.CfnRetrieverPropsMixin.NativeIndexConfigurationProperty(
                    index_id="indexId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b36f26245402072ff4c67038aef2c999809087396bbe32747db74fb92b41d5b9)
                check_type(argname="argument index_id", value=index_id, expected_type=type_hints["index_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if index_id is not None:
                self._values["index_id"] = index_id

        @builtins.property
        def index_id(self) -> typing.Optional[builtins.str]:
            '''The identifier for the Amazon Q Business index.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-retriever-nativeindexconfiguration.html#cfn-qbusiness-retriever-nativeindexconfiguration-indexid
            '''
            result = self._values.get("index_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NativeIndexConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnRetrieverPropsMixin.RetrieverConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "kendra_index_configuration": "kendraIndexConfiguration",
            "native_index_configuration": "nativeIndexConfiguration",
        },
    )
    class RetrieverConfigurationProperty:
        def __init__(
            self,
            *,
            kendra_index_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRetrieverPropsMixin.KendraIndexConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            native_index_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRetrieverPropsMixin.NativeIndexConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Provides information on how the retriever used for your Amazon Q Business application is configured.

            :param kendra_index_configuration: Provides information on how the Amazon Kendra index used as a retriever for your Amazon Q Business application is configured.
            :param native_index_configuration: Provides information on how a Amazon Q Business index used as a retriever for your Amazon Q Business application is configured.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-retriever-retrieverconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
                
                retriever_configuration_property = qbusiness_mixins.CfnRetrieverPropsMixin.RetrieverConfigurationProperty(
                    kendra_index_configuration=qbusiness_mixins.CfnRetrieverPropsMixin.KendraIndexConfigurationProperty(
                        index_id="indexId"
                    ),
                    native_index_configuration=qbusiness_mixins.CfnRetrieverPropsMixin.NativeIndexConfigurationProperty(
                        index_id="indexId"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bcb31f2ed09a33221b0c3caa708bae3eff49e8b6878671f4645a4fa86686c4f4)
                check_type(argname="argument kendra_index_configuration", value=kendra_index_configuration, expected_type=type_hints["kendra_index_configuration"])
                check_type(argname="argument native_index_configuration", value=native_index_configuration, expected_type=type_hints["native_index_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kendra_index_configuration is not None:
                self._values["kendra_index_configuration"] = kendra_index_configuration
            if native_index_configuration is not None:
                self._values["native_index_configuration"] = native_index_configuration

        @builtins.property
        def kendra_index_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRetrieverPropsMixin.KendraIndexConfigurationProperty"]]:
            '''Provides information on how the Amazon Kendra index used as a retriever for your Amazon Q Business application is configured.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-retriever-retrieverconfiguration.html#cfn-qbusiness-retriever-retrieverconfiguration-kendraindexconfiguration
            '''
            result = self._values.get("kendra_index_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRetrieverPropsMixin.KendraIndexConfigurationProperty"]], result)

        @builtins.property
        def native_index_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRetrieverPropsMixin.NativeIndexConfigurationProperty"]]:
            '''Provides information on how a Amazon Q Business index used as a retriever for your Amazon Q Business application is configured.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-retriever-retrieverconfiguration.html#cfn-qbusiness-retriever-retrieverconfiguration-nativeindexconfiguration
            '''
            result = self._values.get("native_index_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRetrieverPropsMixin.NativeIndexConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RetrieverConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnWebExperienceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "browser_extension_configuration": "browserExtensionConfiguration",
        "customization_configuration": "customizationConfiguration",
        "identity_provider_configuration": "identityProviderConfiguration",
        "origins": "origins",
        "role_arn": "roleArn",
        "sample_prompts_control_mode": "samplePromptsControlMode",
        "subtitle": "subtitle",
        "tags": "tags",
        "title": "title",
        "welcome_message": "welcomeMessage",
    },
)
class CfnWebExperienceMixinProps:
    def __init__(
        self,
        *,
        application_id: typing.Optional[builtins.str] = None,
        browser_extension_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWebExperiencePropsMixin.BrowserExtensionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        customization_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWebExperiencePropsMixin.CustomizationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        identity_provider_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWebExperiencePropsMixin.IdentityProviderConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        origins: typing.Optional[typing.Sequence[builtins.str]] = None,
        role_arn: typing.Optional[builtins.str] = None,
        sample_prompts_control_mode: typing.Optional[builtins.str] = None,
        subtitle: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        title: typing.Optional[builtins.str] = None,
        welcome_message: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnWebExperiencePropsMixin.

        :param application_id: The identifier of the Amazon Q Business web experience.
        :param browser_extension_configuration: The container for browser extension configuration for an Amazon Q Business web experience.
        :param customization_configuration: Contains the configuration information to customize the logo, font, and color of an Amazon Q Business web experience with individual files for each property or a CSS file for them all.
        :param identity_provider_configuration: Provides information about the identity provider (IdP) used to authenticate end users of an Amazon Q Business web experience.
        :param origins: Sets the website domain origins that are allowed to embed the Amazon Q Business web experience. The *domain origin* refers to the base URL for accessing a website including the protocol ( ``http/https`` ), the domain name, and the port number (if specified). .. epigraph:: You must only submit a *base URL* and not a full path. For example, ``https://docs.aws.amazon.com`` .
        :param role_arn: The Amazon Resource Name (ARN) of the service role attached to your web experience. .. epigraph:: The ``roleArn`` parameter is required when your Amazon Q Business application is created with IAM Identity Center. It is not required for SAML-based applications.
        :param sample_prompts_control_mode: Determines whether sample prompts are enabled in the web experience for an end user.
        :param subtitle: A subtitle to personalize your Amazon Q Business web experience.
        :param tags: A list of key-value pairs that identify or categorize your Amazon Q Business web experience. You can also use tags to help control access to the web experience. Tag keys and values can consist of Unicode letters, digits, white space, and any of the following symbols: _ . : / = + -
        :param title: The title for your Amazon Q Business web experience.
        :param welcome_message: A message in an Amazon Q Business web experience.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-webexperience.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
            
            cfn_web_experience_mixin_props = qbusiness_mixins.CfnWebExperienceMixinProps(
                application_id="applicationId",
                browser_extension_configuration=qbusiness_mixins.CfnWebExperiencePropsMixin.BrowserExtensionConfigurationProperty(
                    enabled_browser_extensions=["enabledBrowserExtensions"]
                ),
                customization_configuration=qbusiness_mixins.CfnWebExperiencePropsMixin.CustomizationConfigurationProperty(
                    custom_css_url="customCssUrl",
                    favicon_url="faviconUrl",
                    font_url="fontUrl",
                    logo_url="logoUrl"
                ),
                identity_provider_configuration=qbusiness_mixins.CfnWebExperiencePropsMixin.IdentityProviderConfigurationProperty(
                    open_id_connect_configuration=qbusiness_mixins.CfnWebExperiencePropsMixin.OpenIDConnectProviderConfigurationProperty(
                        secrets_arn="secretsArn",
                        secrets_role="secretsRole"
                    ),
                    saml_configuration=qbusiness_mixins.CfnWebExperiencePropsMixin.SamlProviderConfigurationProperty(
                        authentication_url="authenticationUrl"
                    )
                ),
                origins=["origins"],
                role_arn="roleArn",
                sample_prompts_control_mode="samplePromptsControlMode",
                subtitle="subtitle",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                title="title",
                welcome_message="welcomeMessage"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88e5f9a204a377ae7fbc169df9f901268c5aae8a2b098e35db92a0397ea9d632)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument browser_extension_configuration", value=browser_extension_configuration, expected_type=type_hints["browser_extension_configuration"])
            check_type(argname="argument customization_configuration", value=customization_configuration, expected_type=type_hints["customization_configuration"])
            check_type(argname="argument identity_provider_configuration", value=identity_provider_configuration, expected_type=type_hints["identity_provider_configuration"])
            check_type(argname="argument origins", value=origins, expected_type=type_hints["origins"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument sample_prompts_control_mode", value=sample_prompts_control_mode, expected_type=type_hints["sample_prompts_control_mode"])
            check_type(argname="argument subtitle", value=subtitle, expected_type=type_hints["subtitle"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument welcome_message", value=welcome_message, expected_type=type_hints["welcome_message"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_id is not None:
            self._values["application_id"] = application_id
        if browser_extension_configuration is not None:
            self._values["browser_extension_configuration"] = browser_extension_configuration
        if customization_configuration is not None:
            self._values["customization_configuration"] = customization_configuration
        if identity_provider_configuration is not None:
            self._values["identity_provider_configuration"] = identity_provider_configuration
        if origins is not None:
            self._values["origins"] = origins
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if sample_prompts_control_mode is not None:
            self._values["sample_prompts_control_mode"] = sample_prompts_control_mode
        if subtitle is not None:
            self._values["subtitle"] = subtitle
        if tags is not None:
            self._values["tags"] = tags
        if title is not None:
            self._values["title"] = title
        if welcome_message is not None:
            self._values["welcome_message"] = welcome_message

    @builtins.property
    def application_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the Amazon Q Business web experience.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-webexperience.html#cfn-qbusiness-webexperience-applicationid
        '''
        result = self._values.get("application_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def browser_extension_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWebExperiencePropsMixin.BrowserExtensionConfigurationProperty"]]:
        '''The container for browser extension configuration for an Amazon Q Business web experience.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-webexperience.html#cfn-qbusiness-webexperience-browserextensionconfiguration
        '''
        result = self._values.get("browser_extension_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWebExperiencePropsMixin.BrowserExtensionConfigurationProperty"]], result)

    @builtins.property
    def customization_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWebExperiencePropsMixin.CustomizationConfigurationProperty"]]:
        '''Contains the configuration information to customize the logo, font, and color of an Amazon Q Business web experience with individual files for each property or a CSS file for them all.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-webexperience.html#cfn-qbusiness-webexperience-customizationconfiguration
        '''
        result = self._values.get("customization_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWebExperiencePropsMixin.CustomizationConfigurationProperty"]], result)

    @builtins.property
    def identity_provider_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWebExperiencePropsMixin.IdentityProviderConfigurationProperty"]]:
        '''Provides information about the identity provider (IdP) used to authenticate end users of an Amazon Q Business web experience.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-webexperience.html#cfn-qbusiness-webexperience-identityproviderconfiguration
        '''
        result = self._values.get("identity_provider_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWebExperiencePropsMixin.IdentityProviderConfigurationProperty"]], result)

    @builtins.property
    def origins(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Sets the website domain origins that are allowed to embed the Amazon Q Business web experience.

        The *domain origin* refers to the base URL for accessing a website including the protocol ( ``http/https`` ), the domain name, and the port number (if specified).
        .. epigraph::

           You must only submit a *base URL* and not a full path. For example, ``https://docs.aws.amazon.com`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-webexperience.html#cfn-qbusiness-webexperience-origins
        '''
        result = self._values.get("origins")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the service role attached to your web experience.

        .. epigraph::

           The ``roleArn`` parameter is required when your Amazon Q Business application is created with IAM Identity Center. It is not required for SAML-based applications.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-webexperience.html#cfn-qbusiness-webexperience-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sample_prompts_control_mode(self) -> typing.Optional[builtins.str]:
        '''Determines whether sample prompts are enabled in the web experience for an end user.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-webexperience.html#cfn-qbusiness-webexperience-samplepromptscontrolmode
        '''
        result = self._values.get("sample_prompts_control_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subtitle(self) -> typing.Optional[builtins.str]:
        '''A subtitle to personalize your Amazon Q Business web experience.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-webexperience.html#cfn-qbusiness-webexperience-subtitle
        '''
        result = self._values.get("subtitle")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of key-value pairs that identify or categorize your Amazon Q Business web experience.

        You can also use tags to help control access to the web experience. Tag keys and values can consist of Unicode letters, digits, white space, and any of the following symbols: _ . : / = + -

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-webexperience.html#cfn-qbusiness-webexperience-tags
        :: .
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''The title for your Amazon Q Business web experience.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-webexperience.html#cfn-qbusiness-webexperience-title
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def welcome_message(self) -> typing.Optional[builtins.str]:
        '''A message in an Amazon Q Business web experience.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-webexperience.html#cfn-qbusiness-webexperience-welcomemessage
        '''
        result = self._values.get("welcome_message")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWebExperienceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnWebExperiencePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnWebExperiencePropsMixin",
):
    '''Creates an Amazon Q Business web experience.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qbusiness-webexperience.html
    :cloudformationResource: AWS::QBusiness::WebExperience
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
        
        cfn_web_experience_props_mixin = qbusiness_mixins.CfnWebExperiencePropsMixin(qbusiness_mixins.CfnWebExperienceMixinProps(
            application_id="applicationId",
            browser_extension_configuration=qbusiness_mixins.CfnWebExperiencePropsMixin.BrowserExtensionConfigurationProperty(
                enabled_browser_extensions=["enabledBrowserExtensions"]
            ),
            customization_configuration=qbusiness_mixins.CfnWebExperiencePropsMixin.CustomizationConfigurationProperty(
                custom_css_url="customCssUrl",
                favicon_url="faviconUrl",
                font_url="fontUrl",
                logo_url="logoUrl"
            ),
            identity_provider_configuration=qbusiness_mixins.CfnWebExperiencePropsMixin.IdentityProviderConfigurationProperty(
                open_id_connect_configuration=qbusiness_mixins.CfnWebExperiencePropsMixin.OpenIDConnectProviderConfigurationProperty(
                    secrets_arn="secretsArn",
                    secrets_role="secretsRole"
                ),
                saml_configuration=qbusiness_mixins.CfnWebExperiencePropsMixin.SamlProviderConfigurationProperty(
                    authentication_url="authenticationUrl"
                )
            ),
            origins=["origins"],
            role_arn="roleArn",
            sample_prompts_control_mode="samplePromptsControlMode",
            subtitle="subtitle",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            title="title",
            welcome_message="welcomeMessage"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnWebExperienceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::QBusiness::WebExperience``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91ceb5eadb9531cc9c190acfd83269024dda958d1bc70294297fa237de32428d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d71b18f411915b38326405c0f39f75733cffd5269dc93da51adc360bdec5b94)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4df9326e9ae8fc37c1908a933e650728e583ef9f9b749ed9b8c5efd16f5086e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnWebExperienceMixinProps:
        return typing.cast(CfnWebExperienceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnWebExperiencePropsMixin.BrowserExtensionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled_browser_extensions": "enabledBrowserExtensions"},
    )
    class BrowserExtensionConfigurationProperty:
        def __init__(
            self,
            *,
            enabled_browser_extensions: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The container for browser extension configuration for an Amazon Q Business web experience.

            :param enabled_browser_extensions: Specify the browser extensions allowed for your Amazon Q web experience. - ``CHROME`` — Enables the extension for Chromium-based browsers (Google Chrome, Microsoft Edge, Opera, etc.). - ``FIREFOX`` — Enables the extension for Mozilla Firefox. - ``CHROME`` and ``FIREFOX`` — Enable the extension for Chromium-based browsers and Mozilla Firefox.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-webexperience-browserextensionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
                
                browser_extension_configuration_property = qbusiness_mixins.CfnWebExperiencePropsMixin.BrowserExtensionConfigurationProperty(
                    enabled_browser_extensions=["enabledBrowserExtensions"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1c21272394cad47df52d5f8ae5076f4a7221aac2327e972360c16507a97e9f71)
                check_type(argname="argument enabled_browser_extensions", value=enabled_browser_extensions, expected_type=type_hints["enabled_browser_extensions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled_browser_extensions is not None:
                self._values["enabled_browser_extensions"] = enabled_browser_extensions

        @builtins.property
        def enabled_browser_extensions(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''Specify the browser extensions allowed for your Amazon Q web experience.

            - ``CHROME`` — Enables the extension for Chromium-based browsers (Google Chrome, Microsoft Edge, Opera, etc.).
            - ``FIREFOX`` — Enables the extension for Mozilla Firefox.
            - ``CHROME`` and ``FIREFOX`` — Enable the extension for Chromium-based browsers and Mozilla Firefox.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-webexperience-browserextensionconfiguration.html#cfn-qbusiness-webexperience-browserextensionconfiguration-enabledbrowserextensions
            '''
            result = self._values.get("enabled_browser_extensions")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BrowserExtensionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnWebExperiencePropsMixin.CustomizationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "custom_css_url": "customCssUrl",
            "favicon_url": "faviconUrl",
            "font_url": "fontUrl",
            "logo_url": "logoUrl",
        },
    )
    class CustomizationConfigurationProperty:
        def __init__(
            self,
            *,
            custom_css_url: typing.Optional[builtins.str] = None,
            favicon_url: typing.Optional[builtins.str] = None,
            font_url: typing.Optional[builtins.str] = None,
            logo_url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains the configuration information to customize the logo, font, and color of an Amazon Q Business web experience with individual files for each property or a CSS file for them all.

            :param custom_css_url: Provides the URL where the custom CSS file is hosted for an Amazon Q web experience.
            :param favicon_url: Provides the URL where the custom favicon file is hosted for an Amazon Q web experience.
            :param font_url: Provides the URL where the custom font file is hosted for an Amazon Q web experience.
            :param logo_url: Provides the URL where the custom logo file is hosted for an Amazon Q web experience.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-webexperience-customizationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
                
                customization_configuration_property = qbusiness_mixins.CfnWebExperiencePropsMixin.CustomizationConfigurationProperty(
                    custom_css_url="customCssUrl",
                    favicon_url="faviconUrl",
                    font_url="fontUrl",
                    logo_url="logoUrl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b989e52069a4b0acce66f78e5f07a93032a3eed02499bc5ac10041e734445da9)
                check_type(argname="argument custom_css_url", value=custom_css_url, expected_type=type_hints["custom_css_url"])
                check_type(argname="argument favicon_url", value=favicon_url, expected_type=type_hints["favicon_url"])
                check_type(argname="argument font_url", value=font_url, expected_type=type_hints["font_url"])
                check_type(argname="argument logo_url", value=logo_url, expected_type=type_hints["logo_url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if custom_css_url is not None:
                self._values["custom_css_url"] = custom_css_url
            if favicon_url is not None:
                self._values["favicon_url"] = favicon_url
            if font_url is not None:
                self._values["font_url"] = font_url
            if logo_url is not None:
                self._values["logo_url"] = logo_url

        @builtins.property
        def custom_css_url(self) -> typing.Optional[builtins.str]:
            '''Provides the URL where the custom CSS file is hosted for an Amazon Q web experience.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-webexperience-customizationconfiguration.html#cfn-qbusiness-webexperience-customizationconfiguration-customcssurl
            '''
            result = self._values.get("custom_css_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def favicon_url(self) -> typing.Optional[builtins.str]:
            '''Provides the URL where the custom favicon file is hosted for an Amazon Q web experience.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-webexperience-customizationconfiguration.html#cfn-qbusiness-webexperience-customizationconfiguration-faviconurl
            '''
            result = self._values.get("favicon_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def font_url(self) -> typing.Optional[builtins.str]:
            '''Provides the URL where the custom font file is hosted for an Amazon Q web experience.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-webexperience-customizationconfiguration.html#cfn-qbusiness-webexperience-customizationconfiguration-fonturl
            '''
            result = self._values.get("font_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def logo_url(self) -> typing.Optional[builtins.str]:
            '''Provides the URL where the custom logo file is hosted for an Amazon Q web experience.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-webexperience-customizationconfiguration.html#cfn-qbusiness-webexperience-customizationconfiguration-logourl
            '''
            result = self._values.get("logo_url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomizationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnWebExperiencePropsMixin.IdentityProviderConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "open_id_connect_configuration": "openIdConnectConfiguration",
            "saml_configuration": "samlConfiguration",
        },
    )
    class IdentityProviderConfigurationProperty:
        def __init__(
            self,
            *,
            open_id_connect_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWebExperiencePropsMixin.OpenIDConnectProviderConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            saml_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWebExperiencePropsMixin.SamlProviderConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Provides information about the identity provider (IdP) used to authenticate end users of an Amazon Q Business web experience.

            :param open_id_connect_configuration: The OIDC-compliant identity provider (IdP) used to authenticate end users of an Amazon Q Business web experience.
            :param saml_configuration: The SAML 2.0-compliant identity provider (IdP) used to authenticate end users of an Amazon Q Business web experience.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-webexperience-identityproviderconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
                
                identity_provider_configuration_property = qbusiness_mixins.CfnWebExperiencePropsMixin.IdentityProviderConfigurationProperty(
                    open_id_connect_configuration=qbusiness_mixins.CfnWebExperiencePropsMixin.OpenIDConnectProviderConfigurationProperty(
                        secrets_arn="secretsArn",
                        secrets_role="secretsRole"
                    ),
                    saml_configuration=qbusiness_mixins.CfnWebExperiencePropsMixin.SamlProviderConfigurationProperty(
                        authentication_url="authenticationUrl"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6eccae75a3a388e945a6dd677c3626431a868cfb3e5e361232c71403100643d5)
                check_type(argname="argument open_id_connect_configuration", value=open_id_connect_configuration, expected_type=type_hints["open_id_connect_configuration"])
                check_type(argname="argument saml_configuration", value=saml_configuration, expected_type=type_hints["saml_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if open_id_connect_configuration is not None:
                self._values["open_id_connect_configuration"] = open_id_connect_configuration
            if saml_configuration is not None:
                self._values["saml_configuration"] = saml_configuration

        @builtins.property
        def open_id_connect_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWebExperiencePropsMixin.OpenIDConnectProviderConfigurationProperty"]]:
            '''The OIDC-compliant identity provider (IdP) used to authenticate end users of an Amazon Q Business web experience.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-webexperience-identityproviderconfiguration.html#cfn-qbusiness-webexperience-identityproviderconfiguration-openidconnectconfiguration
            '''
            result = self._values.get("open_id_connect_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWebExperiencePropsMixin.OpenIDConnectProviderConfigurationProperty"]], result)

        @builtins.property
        def saml_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWebExperiencePropsMixin.SamlProviderConfigurationProperty"]]:
            '''The SAML 2.0-compliant identity provider (IdP) used to authenticate end users of an Amazon Q Business web experience.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-webexperience-identityproviderconfiguration.html#cfn-qbusiness-webexperience-identityproviderconfiguration-samlconfiguration
            '''
            result = self._values.get("saml_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWebExperiencePropsMixin.SamlProviderConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IdentityProviderConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnWebExperiencePropsMixin.OpenIDConnectProviderConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"secrets_arn": "secretsArn", "secrets_role": "secretsRole"},
    )
    class OpenIDConnectProviderConfigurationProperty:
        def __init__(
            self,
            *,
            secrets_arn: typing.Optional[builtins.str] = None,
            secrets_role: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about the OIDC-compliant identity provider (IdP) used to authenticate end users of an Amazon Q Business web experience.

            :param secrets_arn: The Amazon Resource Name (ARN) of a Secrets Manager secret containing the OIDC client secret.
            :param secrets_role: An IAM role with permissions to access AWS to decrypt the Secrets Manager secret containing your OIDC client secret.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-webexperience-openidconnectproviderconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
                
                open_iDConnect_provider_configuration_property = qbusiness_mixins.CfnWebExperiencePropsMixin.OpenIDConnectProviderConfigurationProperty(
                    secrets_arn="secretsArn",
                    secrets_role="secretsRole"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__12a89897aff44c4f8a3cbe36f3dbd7003054fe1e3ba050f7c670ba53a1e91027)
                check_type(argname="argument secrets_arn", value=secrets_arn, expected_type=type_hints["secrets_arn"])
                check_type(argname="argument secrets_role", value=secrets_role, expected_type=type_hints["secrets_role"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if secrets_arn is not None:
                self._values["secrets_arn"] = secrets_arn
            if secrets_role is not None:
                self._values["secrets_role"] = secrets_role

        @builtins.property
        def secrets_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of a Secrets Manager secret containing the OIDC client secret.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-webexperience-openidconnectproviderconfiguration.html#cfn-qbusiness-webexperience-openidconnectproviderconfiguration-secretsarn
            '''
            result = self._values.get("secrets_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secrets_role(self) -> typing.Optional[builtins.str]:
            '''An IAM role with permissions to access AWS  to decrypt the Secrets Manager secret containing your OIDC client secret.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-webexperience-openidconnectproviderconfiguration.html#cfn-qbusiness-webexperience-openidconnectproviderconfiguration-secretsrole
            '''
            result = self._values.get("secrets_role")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OpenIDConnectProviderConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_qbusiness.mixins.CfnWebExperiencePropsMixin.SamlProviderConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"authentication_url": "authenticationUrl"},
    )
    class SamlProviderConfigurationProperty:
        def __init__(
            self,
            *,
            authentication_url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about the SAML 2.0-compliant identity provider (IdP) used to authenticate end users of an Amazon Q Business web experience.

            :param authentication_url: The URL where Amazon Q Business end users will be redirected for authentication.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-webexperience-samlproviderconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_qbusiness import mixins as qbusiness_mixins
                
                saml_provider_configuration_property = qbusiness_mixins.CfnWebExperiencePropsMixin.SamlProviderConfigurationProperty(
                    authentication_url="authenticationUrl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__88b675d662a741fc13e93b1273fc9b01d6854c14b493bbeeb3bf360e58f36643)
                check_type(argname="argument authentication_url", value=authentication_url, expected_type=type_hints["authentication_url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if authentication_url is not None:
                self._values["authentication_url"] = authentication_url

        @builtins.property
        def authentication_url(self) -> typing.Optional[builtins.str]:
            '''The URL where Amazon Q Business end users will be redirected for authentication.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qbusiness-webexperience-samlproviderconfiguration.html#cfn-qbusiness-webexperience-samlproviderconfiguration-authenticationurl
            '''
            result = self._values.get("authentication_url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SamlProviderConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnApplicationEventLogs",
    "CfnApplicationLogsMixin",
    "CfnApplicationMixinProps",
    "CfnApplicationPropsMixin",
    "CfnApplicationSyncJobLogs",
    "CfnDataAccessorMixinProps",
    "CfnDataAccessorPropsMixin",
    "CfnDataSourceMixinProps",
    "CfnDataSourcePropsMixin",
    "CfnIndexMixinProps",
    "CfnIndexPropsMixin",
    "CfnPermissionMixinProps",
    "CfnPermissionPropsMixin",
    "CfnPluginMixinProps",
    "CfnPluginPropsMixin",
    "CfnRetrieverMixinProps",
    "CfnRetrieverPropsMixin",
    "CfnWebExperienceMixinProps",
    "CfnWebExperiencePropsMixin",
]

publication.publish()

def _typecheckingstub__d34e31e7f28e6d9623407543aa02e24a98471b0062cc49fcc9cb33da27c54014(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a12a04f7977985f75ecb608750d79b72a20f7e5c1b93bfdb63908e7268d0f453(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c4f7d1ed69da227cb7bad96687fd5cc95437dd676e0866347acdd9d859b0081(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e84fe8d369c72562838387fdaae117e98be3cf0570e02903adb20cf2508b27f9(
    log_type: builtins.str,
    log_delivery: _ILogsDelivery_0d3c9e29,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62dc97b6e94872349ea0b8ac24843a120b9852800b12632288610257ed38e845(
    resource: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1265d846673268ba93d93a93dd82e96447415ffec70165e1bf7fe6fc26c78981(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__405e06fa15fa4362c08df578fa4de610505ca8386cedcbe2103a0b952c4d502f(
    *,
    attachments_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.AttachmentsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    auto_subscription_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.AutoSubscriptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    client_ids_for_oidc: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.EncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    iam_identity_provider_arn: typing.Optional[builtins.str] = None,
    identity_center_instance_arn: typing.Optional[builtins.str] = None,
    identity_type: typing.Optional[builtins.str] = None,
    personalization_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.PersonalizationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    q_apps_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.QAppsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    quick_sight_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.QuickSightConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a35eb1c6fadef94000cb27322ac411e04a4e13c389fa34f6855ed1c645c7379f(
    props: typing.Union[CfnApplicationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85d49ed171be1cf1816b09e9f7cf1fe7ce45ffd2802657a154b40d57a3428052(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d0c5da74f1fb60550797988c1262828607d125f7194dfeae5361dd6cc32d0b7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e7db48e1f3960a32e62df24d8d2b72a47a8af41af28535456be1af9f3238198(
    *,
    attachments_control_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a73a656b57077448cc8042722e6ce38ce33ec8001083a6147bad543a77c1080(
    *,
    auto_subscribe: typing.Optional[builtins.str] = None,
    default_subscription_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5acf4619d8867aa4b9983b194bb4c7f5eba797613b793130f287ecc8b6579304(
    *,
    kms_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a46aeecd8fd69ab94e629df1df3e0025e1dec0bed8e94c5b8877c8b1610db528(
    *,
    personalization_control_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__252b2166d0ae705554ffa78ea3cf67cee03dbda04f2101239160a5dc11b34227(
    *,
    q_apps_control_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2400f1e6df36d8fcb39e114003e364561a84867c505daa3724eb07879d3e3cd6(
    *,
    client_namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7c853e432127afc1e5b7e60825df1729a6e13477c1049de8aa9dbf3e09b4a5c(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a7988e4f14e0dbf66a558d4f53f2b1e80e6c64e86c51534a75311fb9dc1f0f2(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37f3f8f9a207e71e32c156240352cd9b1b3081f399d986bb2401c056e3110caa(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a09653529779915f6e67bbe15fdba5c486ede4580785cb5c5647180f4f660322(
    *,
    action_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataAccessorPropsMixin.ActionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    application_id: typing.Optional[builtins.str] = None,
    authentication_detail: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataAccessorPropsMixin.DataAccessorAuthenticationDetailProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    display_name: typing.Optional[builtins.str] = None,
    principal: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58da3fe90207ca823347a3df6367aba9b262e992df83060e34ea693bffe5d02c(
    props: typing.Union[CfnDataAccessorMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13d4fa13814f6bc79c00168a7b8785679a90b43d1629dd52d33cc886646d546c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bcb5bfa0de17bc5b08ee8c12a8e85f83f95e5026e282671cd6330da5df11a59(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__079392577f866c15fb7027c29e65e74a02e717973bd2a5c084ac04703e61d4e7(
    *,
    action: typing.Optional[builtins.str] = None,
    filter_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataAccessorPropsMixin.ActionFilterConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c971fab1ef7478a15d9fe4886bdffe97f92072003ccd789ad0f03ffd381a2ac2(
    *,
    document_attribute_filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataAccessorPropsMixin.AttributeFilterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2559b99e1f72d226c78d14f2445a737be6e03347ec2827de36ba8d497b788b5a(
    *,
    and_all_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataAccessorPropsMixin.AttributeFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    contains_all: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataAccessorPropsMixin.DocumentAttributeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    contains_any: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataAccessorPropsMixin.DocumentAttributeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    equals_to: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataAccessorPropsMixin.DocumentAttributeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    greater_than: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataAccessorPropsMixin.DocumentAttributeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    greater_than_or_equals: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataAccessorPropsMixin.DocumentAttributeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    less_than: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataAccessorPropsMixin.DocumentAttributeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    less_than_or_equals: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataAccessorPropsMixin.DocumentAttributeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    not_filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataAccessorPropsMixin.AttributeFilterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    or_all_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataAccessorPropsMixin.AttributeFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04d0abd3fcfd7f606cb60c6b113fc7416cd74b5ef0d63b3c6a153eeddd5f2e0a(
    *,
    idc_trusted_token_issuer_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataAccessorPropsMixin.DataAccessorIdcTrustedTokenIssuerConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66767ee46594ae7cb70c040a1aba5400c4e8eeb1bf0bf35567c0a2dba4ab8b45(
    *,
    authentication_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataAccessorPropsMixin.DataAccessorAuthenticationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    authentication_type: typing.Optional[builtins.str] = None,
    external_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__797f50ec87c6133feb43b2e4bd210e53f1fb6e8d782e546955a53321d3bef4fb(
    *,
    idc_trusted_token_issuer_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4e82d6deeabb3672b92ab8699c15a9301d157736fd77f0a33481571be5945e3(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataAccessorPropsMixin.DocumentAttributeValueProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00e5fdbcc2aaf8baa826ce27b0195afe9f465001b311406a330a07a97e5abac7(
    *,
    date_value: typing.Optional[builtins.str] = None,
    long_value: typing.Optional[jsii.Number] = None,
    string_list_value: typing.Optional[typing.Sequence[builtins.str]] = None,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b891d365764aa6854b482ca34148482e8d94ee53a5195d7e9514e7a602308337(
    *,
    application_id: typing.Optional[builtins.str] = None,
    configuration: typing.Any = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    document_enrichment_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.DocumentEnrichmentConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    index_id: typing.Optional[builtins.str] = None,
    media_extraction_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.MediaExtractionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    role_arn: typing.Optional[builtins.str] = None,
    sync_schedule: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.DataSourceVpcConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38528ca7532aaf871b7e9516e6d3b3de3eaf34a5115256c060664cef579ffd55(
    props: typing.Union[CfnDataSourceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__640a5a9e974c1b32b990ba74fee211f91a7a3e575d9c50b0202df64cee7cf597(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b29087c22ca13716c896ad70fa0a6448f41e577096bf02b5ff04e5b9e70b545(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cbc958e7ac6d268bba872abbe7f76f04e68ae7a59c961bc2b5c3614aae3c19d(
    *,
    audio_extraction_status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bdc2659728932c3487742fd50d2412915adb4286c6a8f2f4fe99df27789218b(
    *,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2e379efb79afebc0d361d7f2bc1cc756e8668175f3fd3314acdbd0cd5b87306(
    *,
    key: typing.Optional[builtins.str] = None,
    operator: typing.Optional[builtins.str] = None,
    value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.DocumentAttributeValueProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ea2e3529e8719e5d18efc7b63b7a5ff2bc8522ee21a0ad8761fadc617cbb94e(
    *,
    attribute_value_operator: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.DocumentAttributeValueProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c684b4e243e409a4a2ea82719ddcdc667897c49830b86cd2f209c653b9af8625(
    *,
    date_value: typing.Optional[builtins.str] = None,
    long_value: typing.Optional[jsii.Number] = None,
    string_list_value: typing.Optional[typing.Sequence[builtins.str]] = None,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f775c3879a3ad8e4e6463d81a4e860abc09aedcee8f24bc0c2cd02856d22eb93(
    *,
    inline_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.InlineDocumentEnrichmentConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    post_extraction_hook_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.HookConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    pre_extraction_hook_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.HookConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d9c1a478132d58acc8b13ae8dc88e8dfd523dd6fbbb0a13ecdd609d5defe048(
    *,
    invocation_condition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.DocumentAttributeConditionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    lambda_arn: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    s3_bucket_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c31dd7214a114351a9f158c827e8895c5bf076eb82f5028c9d1b5db5765e0a1(
    *,
    image_extraction_status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eb79e48f90d83a23f715048411959312e0331b9a4c05e1352bac0fb219e5bed(
    *,
    condition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.DocumentAttributeConditionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    document_content_operator: typing.Optional[builtins.str] = None,
    target: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.DocumentAttributeTargetProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0117d8505fbcf3ae483ba98b7c6f58ef9b679cc654132953eb6e835550a4460(
    *,
    audio_extraction_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.AudioExtractionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    image_extraction_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.ImageExtractionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    video_extraction_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.VideoExtractionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38295be14311d23bcd66e3be24ea7dd3d403ebb7c4052b34238545ba89f7d884(
    *,
    video_extraction_status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53554ff588af07028f8f1755b4fa0abaf072523a5a21afea1825f6876267c1c2(
    *,
    application_id: typing.Optional[builtins.str] = None,
    capacity_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIndexPropsMixin.IndexCapacityConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    document_attribute_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIndexPropsMixin.DocumentAttributeConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcef6a15e3c6c159f0074fd7193bb18e0ffbbb633959bfe2e033fdcca4a5f3ed(
    props: typing.Union[CfnIndexMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc050d4e5d0ac12b59572a92e733a521c78766e1d87ce9f16b3a3da1c8fcf29c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__153c1648a993600a8195b338fb5685f172a0d1de0aa3c0ac855b4254642c5fd8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6540f9293221a5ea244e5dd288c052027ee75d0e45b34e2ec0d8651d8c0f215a(
    *,
    name: typing.Optional[builtins.str] = None,
    search: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c039394c6b9d12ab7c38c90173785029a062b30cf8c29289a723f41763d365f5(
    *,
    units: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22f20ff2d96d1191dad912b8598e6edbaad0c80820df3471ffd03438f1fda87a(
    *,
    text_document_statistics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIndexPropsMixin.TextDocumentStatisticsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dc1b1951c6658ad7f8105ed69eca043f737170dad0a367e0a98f8ada886705a(
    *,
    indexed_text_bytes: typing.Optional[jsii.Number] = None,
    indexed_text_document_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c86da2da938978223d99601fe2837cf2c1c97f78e8a75d6c5ab7219124bda65b(
    *,
    actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    application_id: typing.Optional[builtins.str] = None,
    conditions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPermissionPropsMixin.ConditionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    principal: typing.Optional[builtins.str] = None,
    statement_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba4f7f747671dde747450e52a446a9ddcfcdfbb58c1c8cc75c423002e6cb8b85(
    props: typing.Union[CfnPermissionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c2dbeb37071cc96ab48a40394b55e11b0061efe52a62a39296ffb3f7d898bbb(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab38a6f5215c74810c54d8a2c480497521dcb2bdcfeae4d1a0eab3109a3ec79a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__055ce9b6472cc34499f662d0b16baafb97f1ed480c1dcb1a6af31e6ceddc0a13(
    *,
    condition_key: typing.Optional[builtins.str] = None,
    condition_operator: typing.Optional[builtins.str] = None,
    condition_values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34f690c39af0ef12a05631e2c7a6386ac67cd9f5bd9ec31f738257ba025dca1a(
    *,
    application_id: typing.Optional[builtins.str] = None,
    auth_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPluginPropsMixin.PluginAuthConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    custom_plugin_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPluginPropsMixin.CustomPluginConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    display_name: typing.Optional[builtins.str] = None,
    server_url: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b9fd4966aae59f2d65e5bdc645692fb20f2d2639d7694dacd2367379a113e4b(
    props: typing.Union[CfnPluginMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__900715ffcacaeca4015718dbb6c7d5287dcaf5812151aa980193a13fe18ffbd5(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fc3337cfa999b69d186d22cd5450d925ce0e48085e3295755b4afc021b7ba9d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baa4f41339b887ecb75f681121e05353ed3ee484c9ba3043c9bffe125c89ac96(
    *,
    payload: typing.Optional[builtins.str] = None,
    s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPluginPropsMixin.S3Property, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3472a50e64be444e96e6c05249afdcfade38150163d364ea279160a1b05fc0f1(
    *,
    role_arn: typing.Optional[builtins.str] = None,
    secret_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4bf971e3152958a9beb006a6380a4eb87bbdbf13032c26f522f63973b20d8b0(
    *,
    api_schema: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPluginPropsMixin.APISchemaProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    api_schema_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__567bfc234c019a7e23c4fe3c393f8e60d23537043ffccb404790878128ffd94e(
    *,
    authorization_url: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    secret_arn: typing.Optional[builtins.str] = None,
    token_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bee46e23e5ad71281db51cde9fffd2beb666f51f4e16efbaaf0ed66491695eee(
    *,
    basic_auth_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPluginPropsMixin.BasicAuthConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    no_auth_configuration: typing.Any = None,
    o_auth2_client_credential_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPluginPropsMixin.OAuth2ClientCredentialConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a565d061d5a08fb3aeded624e0213366e45f3fb2988da629947fcf6d433af3a(
    *,
    bucket: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83b0fa260c1158e721d7411a56d3647f49b62e3c55a1162a988dc823ac81b414(
    *,
    application_id: typing.Optional[builtins.str] = None,
    configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRetrieverPropsMixin.RetrieverConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    display_name: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a9aa58a6435b7623c66b0ab48ff481b3d1ecb3b9baa8486a185a4e171d0db3f(
    props: typing.Union[CfnRetrieverMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14a05691bc76f71042311627a3b3b4532b892c30213aee77ef731995f0b59798(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4123022e86c05d4409b4a86c1211340542defd1301381cb01d8d47ed07c4881(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__242cc13e90371ff4552607488c9582355454d936dabf353ca82af90a73c37439(
    *,
    index_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b36f26245402072ff4c67038aef2c999809087396bbe32747db74fb92b41d5b9(
    *,
    index_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcb31f2ed09a33221b0c3caa708bae3eff49e8b6878671f4645a4fa86686c4f4(
    *,
    kendra_index_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRetrieverPropsMixin.KendraIndexConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    native_index_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRetrieverPropsMixin.NativeIndexConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88e5f9a204a377ae7fbc169df9f901268c5aae8a2b098e35db92a0397ea9d632(
    *,
    application_id: typing.Optional[builtins.str] = None,
    browser_extension_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWebExperiencePropsMixin.BrowserExtensionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    customization_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWebExperiencePropsMixin.CustomizationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    identity_provider_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWebExperiencePropsMixin.IdentityProviderConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    origins: typing.Optional[typing.Sequence[builtins.str]] = None,
    role_arn: typing.Optional[builtins.str] = None,
    sample_prompts_control_mode: typing.Optional[builtins.str] = None,
    subtitle: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    title: typing.Optional[builtins.str] = None,
    welcome_message: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91ceb5eadb9531cc9c190acfd83269024dda958d1bc70294297fa237de32428d(
    props: typing.Union[CfnWebExperienceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d71b18f411915b38326405c0f39f75733cffd5269dc93da51adc360bdec5b94(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4df9326e9ae8fc37c1908a933e650728e583ef9f9b749ed9b8c5efd16f5086e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c21272394cad47df52d5f8ae5076f4a7221aac2327e972360c16507a97e9f71(
    *,
    enabled_browser_extensions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b989e52069a4b0acce66f78e5f07a93032a3eed02499bc5ac10041e734445da9(
    *,
    custom_css_url: typing.Optional[builtins.str] = None,
    favicon_url: typing.Optional[builtins.str] = None,
    font_url: typing.Optional[builtins.str] = None,
    logo_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eccae75a3a388e945a6dd677c3626431a868cfb3e5e361232c71403100643d5(
    *,
    open_id_connect_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWebExperiencePropsMixin.OpenIDConnectProviderConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    saml_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWebExperiencePropsMixin.SamlProviderConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12a89897aff44c4f8a3cbe36f3dbd7003054fe1e3ba050f7c670ba53a1e91027(
    *,
    secrets_arn: typing.Optional[builtins.str] = None,
    secrets_role: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88b675d662a741fc13e93b1273fc9b01d6854c14b493bbeeb3bf360e58f36643(
    *,
    authentication_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
