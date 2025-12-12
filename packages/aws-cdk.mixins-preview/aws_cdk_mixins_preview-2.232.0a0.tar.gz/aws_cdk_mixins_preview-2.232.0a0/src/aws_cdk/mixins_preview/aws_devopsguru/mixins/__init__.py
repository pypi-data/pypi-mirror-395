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
    jsii_type="@aws-cdk/mixins-preview.aws_devopsguru.mixins.CfnLogAnomalyDetectionIntegrationMixinProps",
    jsii_struct_bases=[],
    name_mapping={},
)
class CfnLogAnomalyDetectionIntegrationMixinProps:
    def __init__(self) -> None:
        '''Properties for CfnLogAnomalyDetectionIntegrationPropsMixin.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsguru-loganomalydetectionintegration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_devopsguru import mixins as devopsguru_mixins
            
            cfn_log_anomaly_detection_integration_mixin_props = devopsguru_mixins.CfnLogAnomalyDetectionIntegrationMixinProps()
        '''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLogAnomalyDetectionIntegrationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLogAnomalyDetectionIntegrationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_devopsguru.mixins.CfnLogAnomalyDetectionIntegrationPropsMixin",
):
    '''Information about the integration of DevOps Guru with CloudWatch log groups for log anomaly detection.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsguru-loganomalydetectionintegration.html
    :cloudformationResource: AWS::DevOpsGuru::LogAnomalyDetectionIntegration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_devopsguru import mixins as devopsguru_mixins
        
        cfn_log_anomaly_detection_integration_props_mixin = devopsguru_mixins.CfnLogAnomalyDetectionIntegrationPropsMixin(devopsguru_mixins.CfnLogAnomalyDetectionIntegrationMixinProps(),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnLogAnomalyDetectionIntegrationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DevOpsGuru::LogAnomalyDetectionIntegration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e964c23c5414bff0882612ef31b81f3475fb4f99c2187b9579f1a11d2b649c2c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a4b577eb946948a8163817ab210c4290083c8d870cf3874925f131a9949bbba)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc1d2f503c8b58dbd2c77a2b20d6cb5172525161d7de60d44872aa519126dee6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLogAnomalyDetectionIntegrationMixinProps:
        return typing.cast(CfnLogAnomalyDetectionIntegrationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_devopsguru.mixins.CfnNotificationChannelMixinProps",
    jsii_struct_bases=[],
    name_mapping={"config": "config"},
)
class CfnNotificationChannelMixinProps:
    def __init__(
        self,
        *,
        config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnNotificationChannelPropsMixin.NotificationChannelConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnNotificationChannelPropsMixin.

        :param config: A ``NotificationChannelConfig`` object that contains information about configured notification channels.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsguru-notificationchannel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_devopsguru import mixins as devopsguru_mixins
            
            cfn_notification_channel_mixin_props = devopsguru_mixins.CfnNotificationChannelMixinProps(
                config=devopsguru_mixins.CfnNotificationChannelPropsMixin.NotificationChannelConfigProperty(
                    filters=devopsguru_mixins.CfnNotificationChannelPropsMixin.NotificationFilterConfigProperty(
                        message_types=["messageTypes"],
                        severities=["severities"]
                    ),
                    sns=devopsguru_mixins.CfnNotificationChannelPropsMixin.SnsChannelConfigProperty(
                        topic_arn="topicArn"
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aef658f7cfd33894078eb845dffa33b34cc001d8184f61da241aaf2d89828c01)
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if config is not None:
            self._values["config"] = config

    @builtins.property
    def config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnNotificationChannelPropsMixin.NotificationChannelConfigProperty"]]:
        '''A ``NotificationChannelConfig`` object that contains information about configured notification channels.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsguru-notificationchannel.html#cfn-devopsguru-notificationchannel-config
        '''
        result = self._values.get("config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnNotificationChannelPropsMixin.NotificationChannelConfigProperty"]], result)

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
    jsii_type="@aws-cdk/mixins-preview.aws_devopsguru.mixins.CfnNotificationChannelPropsMixin",
):
    '''Adds a notification channel to DevOps Guru.

    A notification channel is used to notify you about important DevOps Guru events, such as when an insight is generated.

    If you use an Amazon SNS topic in another account, you must attach a policy to it that grants DevOps Guru permission to send it notifications. DevOps Guru adds the required policy on your behalf to send notifications using Amazon SNS in your account. DevOps Guru only supports standard SNS topics. For more information, see `Permissions for Amazon SNS topics <https://docs.aws.amazon.com/devops-guru/latest/userguide/sns-required-permissions.html>`_ .

    If you use an Amazon SNS topic that is encrypted by an AWS Key Management Service customer-managed key (CMK), then you must add permissions to the CMK. For more information, see `Permissions for AWS KMS–encrypted Amazon SNS topics <https://docs.aws.amazon.com/devops-guru/latest/userguide/sns-kms-permissions.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsguru-notificationchannel.html
    :cloudformationResource: AWS::DevOpsGuru::NotificationChannel
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_devopsguru import mixins as devopsguru_mixins
        
        cfn_notification_channel_props_mixin = devopsguru_mixins.CfnNotificationChannelPropsMixin(devopsguru_mixins.CfnNotificationChannelMixinProps(
            config=devopsguru_mixins.CfnNotificationChannelPropsMixin.NotificationChannelConfigProperty(
                filters=devopsguru_mixins.CfnNotificationChannelPropsMixin.NotificationFilterConfigProperty(
                    message_types=["messageTypes"],
                    severities=["severities"]
                ),
                sns=devopsguru_mixins.CfnNotificationChannelPropsMixin.SnsChannelConfigProperty(
                    topic_arn="topicArn"
                )
            )
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
        '''Create a mixin to apply properties to ``AWS::DevOpsGuru::NotificationChannel``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc0d11f87a1600a66f452dfbb15fa8063249ef0d02f68ea3bb1ad1ed27dd34b2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8f87abbf61e077349d262e4fa5ee3e96de5cd772c09f6949aa47a042bd5223c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1500ce363461d79f9c0cd5c0ea60aaadfcb2112b16e977f11f851a84d7c7dfd0)
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
        jsii_type="@aws-cdk/mixins-preview.aws_devopsguru.mixins.CfnNotificationChannelPropsMixin.NotificationChannelConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"filters": "filters", "sns": "sns"},
    )
    class NotificationChannelConfigProperty:
        def __init__(
            self,
            *,
            filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnNotificationChannelPropsMixin.NotificationFilterConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnNotificationChannelPropsMixin.SnsChannelConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Information about notification channels you have configured with DevOps Guru.

            The one supported notification channel is Amazon Simple Notification Service (Amazon SNS).

            :param filters: The filter configurations for the Amazon SNS notification topic you use with DevOps Guru. If you do not provide filter configurations, the default configurations are to receive notifications for all message types of ``High`` or ``Medium`` severity.
            :param sns: Information about a notification channel configured in DevOps Guru to send notifications when insights are created. If you use an Amazon SNS topic in another account, you must attach a policy to it that grants DevOps Guru permission to send it notifications. DevOps Guru adds the required policy on your behalf to send notifications using Amazon SNS in your account. DevOps Guru only supports standard SNS topics. For more information, see `Permissions for Amazon SNS topics <https://docs.aws.amazon.com/devops-guru/latest/userguide/sns-required-permissions.html>`_ . If you use an Amazon SNS topic that is encrypted by an AWS Key Management Service customer-managed key (CMK), then you must add permissions to the CMK. For more information, see `Permissions for AWS KMS–encrypted Amazon SNS topics <https://docs.aws.amazon.com/devops-guru/latest/userguide/sns-kms-permissions.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsguru-notificationchannel-notificationchannelconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_devopsguru import mixins as devopsguru_mixins
                
                notification_channel_config_property = devopsguru_mixins.CfnNotificationChannelPropsMixin.NotificationChannelConfigProperty(
                    filters=devopsguru_mixins.CfnNotificationChannelPropsMixin.NotificationFilterConfigProperty(
                        message_types=["messageTypes"],
                        severities=["severities"]
                    ),
                    sns=devopsguru_mixins.CfnNotificationChannelPropsMixin.SnsChannelConfigProperty(
                        topic_arn="topicArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d32e1d8a23059736b1de7eb4fff6cb94f742656403b2bd728d4f436cc513c595)
                check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
                check_type(argname="argument sns", value=sns, expected_type=type_hints["sns"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if filters is not None:
                self._values["filters"] = filters
            if sns is not None:
                self._values["sns"] = sns

        @builtins.property
        def filters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnNotificationChannelPropsMixin.NotificationFilterConfigProperty"]]:
            '''The filter configurations for the Amazon SNS notification topic you use with DevOps Guru.

            If you do not provide filter configurations, the default configurations are to receive notifications for all message types of ``High`` or ``Medium`` severity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsguru-notificationchannel-notificationchannelconfig.html#cfn-devopsguru-notificationchannel-notificationchannelconfig-filters
            '''
            result = self._values.get("filters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnNotificationChannelPropsMixin.NotificationFilterConfigProperty"]], result)

        @builtins.property
        def sns(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnNotificationChannelPropsMixin.SnsChannelConfigProperty"]]:
            '''Information about a notification channel configured in DevOps Guru to send notifications when insights are created.

            If you use an Amazon SNS topic in another account, you must attach a policy to it that grants DevOps Guru permission to send it notifications. DevOps Guru adds the required policy on your behalf to send notifications using Amazon SNS in your account. DevOps Guru only supports standard SNS topics. For more information, see `Permissions for Amazon SNS topics <https://docs.aws.amazon.com/devops-guru/latest/userguide/sns-required-permissions.html>`_ .

            If you use an Amazon SNS topic that is encrypted by an AWS Key Management Service customer-managed key (CMK), then you must add permissions to the CMK. For more information, see `Permissions for AWS KMS–encrypted Amazon SNS topics <https://docs.aws.amazon.com/devops-guru/latest/userguide/sns-kms-permissions.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsguru-notificationchannel-notificationchannelconfig.html#cfn-devopsguru-notificationchannel-notificationchannelconfig-sns
            '''
            result = self._values.get("sns")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnNotificationChannelPropsMixin.SnsChannelConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NotificationChannelConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_devopsguru.mixins.CfnNotificationChannelPropsMixin.NotificationFilterConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"message_types": "messageTypes", "severities": "severities"},
    )
    class NotificationFilterConfigProperty:
        def __init__(
            self,
            *,
            message_types: typing.Optional[typing.Sequence[builtins.str]] = None,
            severities: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The filter configurations for the Amazon SNS notification topic you use with DevOps Guru.

            You can choose to specify which events or message types to receive notifications for. You can also choose to specify which severity levels to receive notifications for.

            :param message_types: The events that you want to receive notifications for. For example, you can choose to receive notifications only when the severity level is upgraded or a new insight is created.
            :param severities: The severity levels that you want to receive notifications for. For example, you can choose to receive notifications only for insights with ``HIGH`` and ``MEDIUM`` severity levels. For more information, see `Understanding insight severities <https://docs.aws.amazon.com/devops-guru/latest/userguide/working-with-insights.html#understanding-insights-severities>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsguru-notificationchannel-notificationfilterconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_devopsguru import mixins as devopsguru_mixins
                
                notification_filter_config_property = devopsguru_mixins.CfnNotificationChannelPropsMixin.NotificationFilterConfigProperty(
                    message_types=["messageTypes"],
                    severities=["severities"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e56e639f48dcecb2b1682daaf0fa61934dd1392216a4129fd596264758e2f879)
                check_type(argname="argument message_types", value=message_types, expected_type=type_hints["message_types"])
                check_type(argname="argument severities", value=severities, expected_type=type_hints["severities"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if message_types is not None:
                self._values["message_types"] = message_types
            if severities is not None:
                self._values["severities"] = severities

        @builtins.property
        def message_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The events that you want to receive notifications for.

            For example, you can choose to receive notifications only when the severity level is upgraded or a new insight is created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsguru-notificationchannel-notificationfilterconfig.html#cfn-devopsguru-notificationchannel-notificationfilterconfig-messagetypes
            '''
            result = self._values.get("message_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def severities(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The severity levels that you want to receive notifications for.

            For example, you can choose to receive notifications only for insights with ``HIGH`` and ``MEDIUM`` severity levels. For more information, see `Understanding insight severities <https://docs.aws.amazon.com/devops-guru/latest/userguide/working-with-insights.html#understanding-insights-severities>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsguru-notificationchannel-notificationfilterconfig.html#cfn-devopsguru-notificationchannel-notificationfilterconfig-severities
            '''
            result = self._values.get("severities")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NotificationFilterConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_devopsguru.mixins.CfnNotificationChannelPropsMixin.SnsChannelConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"topic_arn": "topicArn"},
    )
    class SnsChannelConfigProperty:
        def __init__(self, *, topic_arn: typing.Optional[builtins.str] = None) -> None:
            '''Contains the Amazon Resource Name (ARN) of an Amazon Simple Notification Service topic.

            If you use an Amazon SNS topic in another account, you must attach a policy to it that grants DevOps Guru permission to send it notifications. DevOps Guru adds the required policy on your behalf to send notifications using Amazon SNS in your account. DevOps Guru only supports standard SNS topics. For more information, see `Permissions for Amazon SNS topics <https://docs.aws.amazon.com/devops-guru/latest/userguide/sns-required-permissions.html>`_ .

            If you use an Amazon SNS topic that is encrypted by an AWS Key Management Service customer-managed key (CMK), then you must add permissions to the CMK. For more information, see `Permissions for AWS KMS–encrypted Amazon SNS topics <https://docs.aws.amazon.com/devops-guru/latest/userguide/sns-kms-permissions.html>`_ .

            :param topic_arn: The Amazon Resource Name (ARN) of an Amazon Simple Notification Service topic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsguru-notificationchannel-snschannelconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_devopsguru import mixins as devopsguru_mixins
                
                sns_channel_config_property = devopsguru_mixins.CfnNotificationChannelPropsMixin.SnsChannelConfigProperty(
                    topic_arn="topicArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b55cef444b45823822c7a7feeef377b76d134177b0cd27783c9c37afb356f92f)
                check_type(argname="argument topic_arn", value=topic_arn, expected_type=type_hints["topic_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if topic_arn is not None:
                self._values["topic_arn"] = topic_arn

        @builtins.property
        def topic_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of an Amazon Simple Notification Service topic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsguru-notificationchannel-snschannelconfig.html#cfn-devopsguru-notificationchannel-snschannelconfig-topicarn
            '''
            result = self._values.get("topic_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SnsChannelConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_devopsguru.mixins.CfnResourceCollectionMixinProps",
    jsii_struct_bases=[],
    name_mapping={"resource_collection_filter": "resourceCollectionFilter"},
)
class CfnResourceCollectionMixinProps:
    def __init__(
        self,
        *,
        resource_collection_filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResourceCollectionPropsMixin.ResourceCollectionFilterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnResourceCollectionPropsMixin.

        :param resource_collection_filter: Information about a filter used to specify which AWS resources are analyzed for anomalous behavior by DevOps Guru.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsguru-resourcecollection.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_devopsguru import mixins as devopsguru_mixins
            
            cfn_resource_collection_mixin_props = devopsguru_mixins.CfnResourceCollectionMixinProps(
                resource_collection_filter=devopsguru_mixins.CfnResourceCollectionPropsMixin.ResourceCollectionFilterProperty(
                    cloud_formation=devopsguru_mixins.CfnResourceCollectionPropsMixin.CloudFormationCollectionFilterProperty(
                        stack_names=["stackNames"]
                    ),
                    tags=[devopsguru_mixins.CfnResourceCollectionPropsMixin.TagCollectionProperty(
                        app_boundary_key="appBoundaryKey",
                        tag_values=["tagValues"]
                    )]
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c4e928eaea573cf635c02f5e48e4ae9303a55bd43be9429dab70f3fa5393e52)
            check_type(argname="argument resource_collection_filter", value=resource_collection_filter, expected_type=type_hints["resource_collection_filter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if resource_collection_filter is not None:
            self._values["resource_collection_filter"] = resource_collection_filter

    @builtins.property
    def resource_collection_filter(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceCollectionPropsMixin.ResourceCollectionFilterProperty"]]:
        '''Information about a filter used to specify which AWS resources are analyzed for anomalous behavior by DevOps Guru.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsguru-resourcecollection.html#cfn-devopsguru-resourcecollection-resourcecollectionfilter
        '''
        result = self._values.get("resource_collection_filter")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceCollectionPropsMixin.ResourceCollectionFilterProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourceCollectionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnResourceCollectionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_devopsguru.mixins.CfnResourceCollectionPropsMixin",
):
    '''A collection of AWS resources supported by DevOps Guru.

    The one type of AWS resource collection supported is AWS CloudFormation stacks. DevOps Guru can be configured to analyze only the AWS resources that are defined in the stacks.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsguru-resourcecollection.html
    :cloudformationResource: AWS::DevOpsGuru::ResourceCollection
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_devopsguru import mixins as devopsguru_mixins
        
        cfn_resource_collection_props_mixin = devopsguru_mixins.CfnResourceCollectionPropsMixin(devopsguru_mixins.CfnResourceCollectionMixinProps(
            resource_collection_filter=devopsguru_mixins.CfnResourceCollectionPropsMixin.ResourceCollectionFilterProperty(
                cloud_formation=devopsguru_mixins.CfnResourceCollectionPropsMixin.CloudFormationCollectionFilterProperty(
                    stack_names=["stackNames"]
                ),
                tags=[devopsguru_mixins.CfnResourceCollectionPropsMixin.TagCollectionProperty(
                    app_boundary_key="appBoundaryKey",
                    tag_values=["tagValues"]
                )]
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnResourceCollectionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DevOpsGuru::ResourceCollection``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2444b9642afaa87281695cab852049acf6b0312b6341c900444bcf55ad812577)
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
            type_hints = typing.get_type_hints(_typecheckingstub__51bd2834e38fcebb15d9c955b5419defe1332335f66019e1bfd23f59f49d9053)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aedc01ef9a0ac7b6984c0c247a0f7679fafbc5e1dc29e0305d577144d2e75b4c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnResourceCollectionMixinProps:
        return typing.cast(CfnResourceCollectionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_devopsguru.mixins.CfnResourceCollectionPropsMixin.CloudFormationCollectionFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"stack_names": "stackNames"},
    )
    class CloudFormationCollectionFilterProperty:
        def __init__(
            self,
            *,
            stack_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Information about AWS CloudFormation stacks.

            You can use up to 1000 stacks to specify which AWS resources in your account to analyze. For more information, see `Stacks <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacks.html>`_ in the *AWS CloudFormation User Guide* .

            :param stack_names: An array of CloudFormation stack names.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsguru-resourcecollection-cloudformationcollectionfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_devopsguru import mixins as devopsguru_mixins
                
                cloud_formation_collection_filter_property = devopsguru_mixins.CfnResourceCollectionPropsMixin.CloudFormationCollectionFilterProperty(
                    stack_names=["stackNames"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__11565f5386e1a824f0b59017d431f7535f8b36ab0b5c1f9646ceaa2ede1ddd95)
                check_type(argname="argument stack_names", value=stack_names, expected_type=type_hints["stack_names"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if stack_names is not None:
                self._values["stack_names"] = stack_names

        @builtins.property
        def stack_names(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An array of CloudFormation stack names.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsguru-resourcecollection-cloudformationcollectionfilter.html#cfn-devopsguru-resourcecollection-cloudformationcollectionfilter-stacknames
            '''
            result = self._values.get("stack_names")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudFormationCollectionFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_devopsguru.mixins.CfnResourceCollectionPropsMixin.ResourceCollectionFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"cloud_formation": "cloudFormation", "tags": "tags"},
    )
    class ResourceCollectionFilterProperty:
        def __init__(
            self,
            *,
            cloud_formation: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResourceCollectionPropsMixin.CloudFormationCollectionFilterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            tags: typing.Optional[typing.Sequence[typing.Union["CfnResourceCollectionPropsMixin.TagCollectionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Information about a filter used to specify which AWS resources are analyzed for anomalous behavior by DevOps Guru.

            :param cloud_formation: Information about AWS CloudFormation stacks. You can use up to 1000 stacks to specify which AWS resources in your account to analyze. For more information, see `Stacks <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacks.html>`_ in the *AWS CloudFormation User Guide* .
            :param tags: The AWS tags used to filter the resources in the resource collection. Tags help you identify and organize your AWS resources. Many AWS services support tagging, so you can assign the same tag to resources from different services to indicate that the resources are related. For example, you can assign the same tag to an Amazon DynamoDB table resource that you assign to an AWS Lambda function. For more information about using tags, see the `Tagging best practices <https://docs.aws.amazon.com/whitepapers/latest/tagging-best-practices/tagging-best-practices.html>`_ whitepaper. Each AWS tag has two parts. - A tag *key* (for example, ``CostCenter`` , ``Environment`` , ``Project`` , or ``Secret`` ). Tag *keys* are case-sensitive. - A field known as a tag *value* (for example, ``111122223333`` , ``Production`` , or a team name). Omitting the tag *value* is the same as using an empty string. Like tag *keys* , tag *values* are case-sensitive. The tag value is a required property when AppBoundaryKey is specified. Together these are known as *key* - *value* pairs. .. epigraph:: The string used for a *key* in a tag that you use to define your resource coverage must begin with the prefix ``Devops-guru-`` . The tag *key* might be ``DevOps-Guru-deployment-application`` or ``devops-guru-rds-application`` . When you create a *key* , the case of characters in the *key* can be whatever you choose. After you create a *key* , it is case-sensitive. For example, DevOps Guru works with a *key* named ``devops-guru-rds`` and a *key* named ``DevOps-Guru-RDS`` , and these act as two different *keys* . Possible *key* / *value* pairs in your application might be ``Devops-Guru-production-application/RDS`` or ``Devops-Guru-production-application/containers`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsguru-resourcecollection-resourcecollectionfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_devopsguru import mixins as devopsguru_mixins
                
                resource_collection_filter_property = devopsguru_mixins.CfnResourceCollectionPropsMixin.ResourceCollectionFilterProperty(
                    cloud_formation=devopsguru_mixins.CfnResourceCollectionPropsMixin.CloudFormationCollectionFilterProperty(
                        stack_names=["stackNames"]
                    ),
                    tags=[devopsguru_mixins.CfnResourceCollectionPropsMixin.TagCollectionProperty(
                        app_boundary_key="appBoundaryKey",
                        tag_values=["tagValues"]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d3080db04b51edf9d74dddc11469d539997ab81193c560b47e64f1fe14bf070b)
                check_type(argname="argument cloud_formation", value=cloud_formation, expected_type=type_hints["cloud_formation"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloud_formation is not None:
                self._values["cloud_formation"] = cloud_formation
            if tags is not None:
                self._values["tags"] = tags

        @builtins.property
        def cloud_formation(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceCollectionPropsMixin.CloudFormationCollectionFilterProperty"]]:
            '''Information about AWS CloudFormation stacks.

            You can use up to 1000 stacks to specify which AWS resources in your account to analyze. For more information, see `Stacks <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacks.html>`_ in the *AWS CloudFormation User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsguru-resourcecollection-resourcecollectionfilter.html#cfn-devopsguru-resourcecollection-resourcecollectionfilter-cloudformation
            '''
            result = self._values.get("cloud_formation")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceCollectionPropsMixin.CloudFormationCollectionFilterProperty"]], result)

        @builtins.property
        def tags(
            self,
        ) -> typing.Optional[typing.List["CfnResourceCollectionPropsMixin.TagCollectionProperty"]]:
            '''The AWS tags used to filter the resources in the resource collection.

            Tags help you identify and organize your AWS resources. Many AWS services support tagging, so you can assign the same tag to resources from different services to indicate that the resources are related. For example, you can assign the same tag to an Amazon DynamoDB table resource that you assign to an AWS Lambda function. For more information about using tags, see the `Tagging best practices <https://docs.aws.amazon.com/whitepapers/latest/tagging-best-practices/tagging-best-practices.html>`_ whitepaper.

            Each AWS tag has two parts.

            - A tag *key* (for example, ``CostCenter`` , ``Environment`` , ``Project`` , or ``Secret`` ). Tag *keys* are case-sensitive.
            - A field known as a tag *value* (for example, ``111122223333`` , ``Production`` , or a team name). Omitting the tag *value* is the same as using an empty string. Like tag *keys* , tag *values* are case-sensitive. The tag value is a required property when AppBoundaryKey is specified.

            Together these are known as *key* - *value* pairs.
            .. epigraph::

               The string used for a *key* in a tag that you use to define your resource coverage must begin with the prefix ``Devops-guru-`` . The tag *key* might be ``DevOps-Guru-deployment-application`` or ``devops-guru-rds-application`` . When you create a *key* , the case of characters in the *key* can be whatever you choose. After you create a *key* , it is case-sensitive. For example, DevOps Guru works with a *key* named ``devops-guru-rds`` and a *key* named ``DevOps-Guru-RDS`` , and these act as two different *keys* . Possible *key* / *value* pairs in your application might be ``Devops-Guru-production-application/RDS`` or ``Devops-Guru-production-application/containers`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsguru-resourcecollection-resourcecollectionfilter.html#cfn-devopsguru-resourcecollection-resourcecollectionfilter-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List["CfnResourceCollectionPropsMixin.TagCollectionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceCollectionFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_devopsguru.mixins.CfnResourceCollectionPropsMixin.TagCollectionProperty",
        jsii_struct_bases=[],
        name_mapping={"app_boundary_key": "appBoundaryKey", "tag_values": "tagValues"},
    )
    class TagCollectionProperty:
        def __init__(
            self,
            *,
            app_boundary_key: typing.Optional[builtins.str] = None,
            tag_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''A collection of AWS tags.

            Tags help you identify and organize your AWS resources. Many AWS services support tagging, so you can assign the same tag to resources from different services to indicate that the resources are related. For example, you can assign the same tag to an Amazon DynamoDB table resource that you assign to an AWS Lambda function. For more information about using tags, see the `Tagging best practices <https://docs.aws.amazon.com/whitepapers/latest/tagging-best-practices/tagging-best-practices.html>`_ whitepaper.

            Each AWS tag has two parts.

            - A tag *key* (for example, ``CostCenter`` , ``Environment`` , ``Project`` , or ``Secret`` ). Tag *keys* are case-sensitive.
            - A field known as a tag *value* (for example, ``111122223333`` , ``Production`` , or a team name). Omitting the tag *value* is the same as using an empty string. Like tag *keys* , tag *values* are case-sensitive. The tag value is a required property when *AppBoundaryKey* is specified.

            Together these are known as *key* - *value* pairs.
            .. epigraph::

               The string used for a *key* in a tag that you use to define your resource coverage must begin with the prefix ``Devops-guru-`` . The tag *key* might be ``DevOps-Guru-deployment-application`` or ``devops-guru-rds-application`` . When you create a *key* , the case of characters in the *key* can be whatever you choose. After you create a *key* , it is case-sensitive. For example, DevOps Guru works with a *key* named ``devops-guru-rds`` and a *key* named ``DevOps-Guru-RDS`` , and these act as two different *keys* . Possible *key* / *value* pairs in your application might be ``Devops-Guru-production-application/RDS`` or ``Devops-Guru-production-application/containers`` .

            :param app_boundary_key: An AWS tag *key* that is used to identify the AWS resources that DevOps Guru analyzes. All AWS resources in your account and Region tagged with this *key* make up your DevOps Guru application and analysis boundary. .. epigraph:: When you create a *key* , the case of characters in the *key* can be whatever you choose. After you create a *key* , it is case-sensitive. For example, DevOps Guru works with a *key* named ``devops-guru-rds`` and a *key* named ``DevOps-Guru-RDS`` , and these act as two different *keys* . Possible *key* / *value* pairs in your application might be ``Devops-Guru-production-application/RDS`` or ``Devops-Guru-production-application/containers`` .
            :param tag_values: The values in an AWS tag collection. The tag's *value* is a field used to associate a string with the tag *key* (for example, ``111122223333`` , ``Production`` , or a team name). The *key* and *value* are the tag's *key* pair. Omitting the tag *value* is the same as using an empty string. Like tag *keys* , tag *values* are case-sensitive. You can specify a maximum of 256 characters for a tag value. The tag value is a required property when *AppBoundaryKey* is specified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsguru-resourcecollection-tagcollection.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_devopsguru import mixins as devopsguru_mixins
                
                tag_collection_property = devopsguru_mixins.CfnResourceCollectionPropsMixin.TagCollectionProperty(
                    app_boundary_key="appBoundaryKey",
                    tag_values=["tagValues"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__27e527a945baaf9f75fc3585d820163406e6a3a0d4d7096d6dc3581c7734be3a)
                check_type(argname="argument app_boundary_key", value=app_boundary_key, expected_type=type_hints["app_boundary_key"])
                check_type(argname="argument tag_values", value=tag_values, expected_type=type_hints["tag_values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if app_boundary_key is not None:
                self._values["app_boundary_key"] = app_boundary_key
            if tag_values is not None:
                self._values["tag_values"] = tag_values

        @builtins.property
        def app_boundary_key(self) -> typing.Optional[builtins.str]:
            '''An AWS tag *key* that is used to identify the AWS resources that DevOps Guru analyzes.

            All AWS resources in your account and Region tagged with this *key* make up your DevOps Guru application and analysis boundary.
            .. epigraph::

               When you create a *key* , the case of characters in the *key* can be whatever you choose. After you create a *key* , it is case-sensitive. For example, DevOps Guru works with a *key* named ``devops-guru-rds`` and a *key* named ``DevOps-Guru-RDS`` , and these act as two different *keys* . Possible *key* / *value* pairs in your application might be ``Devops-Guru-production-application/RDS`` or ``Devops-Guru-production-application/containers`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsguru-resourcecollection-tagcollection.html#cfn-devopsguru-resourcecollection-tagcollection-appboundarykey
            '''
            result = self._values.get("app_boundary_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tag_values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The values in an AWS tag collection.

            The tag's *value* is a field used to associate a string with the tag *key* (for example, ``111122223333`` , ``Production`` , or a team name). The *key* and *value* are the tag's *key* pair. Omitting the tag *value* is the same as using an empty string. Like tag *keys* , tag *values* are case-sensitive. You can specify a maximum of 256 characters for a tag value. The tag value is a required property when *AppBoundaryKey* is specified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsguru-resourcecollection-tagcollection.html#cfn-devopsguru-resourcecollection-tagcollection-tagvalues
            '''
            result = self._values.get("tag_values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagCollectionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnLogAnomalyDetectionIntegrationMixinProps",
    "CfnLogAnomalyDetectionIntegrationPropsMixin",
    "CfnNotificationChannelMixinProps",
    "CfnNotificationChannelPropsMixin",
    "CfnResourceCollectionMixinProps",
    "CfnResourceCollectionPropsMixin",
]

publication.publish()

def _typecheckingstub__e964c23c5414bff0882612ef31b81f3475fb4f99c2187b9579f1a11d2b649c2c(
    props: typing.Union[CfnLogAnomalyDetectionIntegrationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a4b577eb946948a8163817ab210c4290083c8d870cf3874925f131a9949bbba(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc1d2f503c8b58dbd2c77a2b20d6cb5172525161d7de60d44872aa519126dee6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aef658f7cfd33894078eb845dffa33b34cc001d8184f61da241aaf2d89828c01(
    *,
    config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnNotificationChannelPropsMixin.NotificationChannelConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc0d11f87a1600a66f452dfbb15fa8063249ef0d02f68ea3bb1ad1ed27dd34b2(
    props: typing.Union[CfnNotificationChannelMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8f87abbf61e077349d262e4fa5ee3e96de5cd772c09f6949aa47a042bd5223c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1500ce363461d79f9c0cd5c0ea60aaadfcb2112b16e977f11f851a84d7c7dfd0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d32e1d8a23059736b1de7eb4fff6cb94f742656403b2bd728d4f436cc513c595(
    *,
    filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnNotificationChannelPropsMixin.NotificationFilterConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnNotificationChannelPropsMixin.SnsChannelConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e56e639f48dcecb2b1682daaf0fa61934dd1392216a4129fd596264758e2f879(
    *,
    message_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    severities: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b55cef444b45823822c7a7feeef377b76d134177b0cd27783c9c37afb356f92f(
    *,
    topic_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c4e928eaea573cf635c02f5e48e4ae9303a55bd43be9429dab70f3fa5393e52(
    *,
    resource_collection_filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResourceCollectionPropsMixin.ResourceCollectionFilterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2444b9642afaa87281695cab852049acf6b0312b6341c900444bcf55ad812577(
    props: typing.Union[CfnResourceCollectionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51bd2834e38fcebb15d9c955b5419defe1332335f66019e1bfd23f59f49d9053(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aedc01ef9a0ac7b6984c0c247a0f7679fafbc5e1dc29e0305d577144d2e75b4c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11565f5386e1a824f0b59017d431f7535f8b36ab0b5c1f9646ceaa2ede1ddd95(
    *,
    stack_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3080db04b51edf9d74dddc11469d539997ab81193c560b47e64f1fe14bf070b(
    *,
    cloud_formation: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResourceCollectionPropsMixin.CloudFormationCollectionFilterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnResourceCollectionPropsMixin.TagCollectionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27e527a945baaf9f75fc3585d820163406e6a3a0d4d7096d6dc3581c7734be3a(
    *,
    app_boundary_key: typing.Optional[builtins.str] = None,
    tag_values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
