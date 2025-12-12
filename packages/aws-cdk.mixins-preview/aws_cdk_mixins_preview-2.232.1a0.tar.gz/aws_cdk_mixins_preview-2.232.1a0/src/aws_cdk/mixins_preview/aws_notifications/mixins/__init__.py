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
    jsii_type="@aws-cdk/mixins-preview.aws_notifications.mixins.CfnChannelAssociationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "arn": "arn",
        "notification_configuration_arn": "notificationConfigurationArn",
    },
)
class CfnChannelAssociationMixinProps:
    def __init__(
        self,
        *,
        arn: typing.Optional[builtins.str] = None,
        notification_configuration_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnChannelAssociationPropsMixin.

        :param arn: The Amazon Resource Name (ARN) of the ``Channel`` .
        :param notification_configuration_arn: The ARN of the ``NotificationConfiguration`` associated with the ``Channel`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-notifications-channelassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_notifications import mixins as notifications_mixins
            
            cfn_channel_association_mixin_props = notifications_mixins.CfnChannelAssociationMixinProps(
                arn="arn",
                notification_configuration_arn="notificationConfigurationArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f05a7ba00a3875da8d3d796f739e71a7e0e2595986480d1d35a55dbbf8e6ab74)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            check_type(argname="argument notification_configuration_arn", value=notification_configuration_arn, expected_type=type_hints["notification_configuration_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if arn is not None:
            self._values["arn"] = arn
        if notification_configuration_arn is not None:
            self._values["notification_configuration_arn"] = notification_configuration_arn

    @builtins.property
    def arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the ``Channel`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-notifications-channelassociation.html#cfn-notifications-channelassociation-arn
        '''
        result = self._values.get("arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_configuration_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the ``NotificationConfiguration`` associated with the ``Channel`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-notifications-channelassociation.html#cfn-notifications-channelassociation-notificationconfigurationarn
        '''
        result = self._values.get("notification_configuration_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnChannelAssociationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnChannelAssociationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_notifications.mixins.CfnChannelAssociationPropsMixin",
):
    '''The ``AWS::Notifications::ChannelAssociation`` resource associates a ``Channel`` with a ``NotificationConfiguration`` for AWS User Notifications .

    For more information about AWS User Notifications , see the `AWS User Notifications User Guide <https://docs.aws.amazon.com/notifications/latest/userguide/what-is-service.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-notifications-channelassociation.html
    :cloudformationResource: AWS::Notifications::ChannelAssociation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_notifications import mixins as notifications_mixins
        
        cfn_channel_association_props_mixin = notifications_mixins.CfnChannelAssociationPropsMixin(notifications_mixins.CfnChannelAssociationMixinProps(
            arn="arn",
            notification_configuration_arn="notificationConfigurationArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnChannelAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Notifications::ChannelAssociation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__622241d91676e535367c726f228fb7aad31287aa94ec0951f71f61b43b8dac52)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1996773ea646a8f86d373d143629f97cf536fd415d893143293cc465f7ae820d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c9bdc689eb4537f71c3b7285c1332388a146cb06b79739ca8ccdebb94f8c538)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnChannelAssociationMixinProps:
        return typing.cast(CfnChannelAssociationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_notifications.mixins.CfnEventRuleMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "event_pattern": "eventPattern",
        "event_type": "eventType",
        "notification_configuration_arn": "notificationConfigurationArn",
        "regions": "regions",
        "source": "source",
    },
)
class CfnEventRuleMixinProps:
    def __init__(
        self,
        *,
        event_pattern: typing.Optional[builtins.str] = None,
        event_type: typing.Optional[builtins.str] = None,
        notification_configuration_arn: typing.Optional[builtins.str] = None,
        regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        source: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnEventRulePropsMixin.

        :param event_pattern: An additional event pattern used to further filter the events this ``EventRule`` receives. For more information, see `Amazon EventBridge event patterns <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-event-patterns.html>`_ in the *Amazon EventBridge User Guide.*
        :param event_type: The event type this rule should match with the EventBridge events. It must match with atleast one of the valid EventBridge event types. For example, Amazon EC2 Instance State change Notification and Amazon CloudWatch State Change. For more information, see `Event delivery from AWS services <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-service-event.html#eb-service-event-delivery-level>`_ in the *Amazon EventBridge User Guide* .
        :param notification_configuration_arn: The ARN for the ``NotificationConfiguration`` associated with this ``EventRule`` .
        :param regions: A list of AWS Regions that send events to this ``EventRule`` .
        :param source: The event source this rule should match with the EventBridge event sources. It must match with atleast one of the valid EventBridge event sources. Only AWS service sourced events are supported. For example, ``aws.ec2`` and ``aws.cloudwatch`` . For more information, see `Event delivery from AWS services <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-service-event.html#eb-service-event-delivery-level>`_ in the *Amazon EventBridge User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-notifications-eventrule.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_notifications import mixins as notifications_mixins
            
            cfn_event_rule_mixin_props = notifications_mixins.CfnEventRuleMixinProps(
                event_pattern="eventPattern",
                event_type="eventType",
                notification_configuration_arn="notificationConfigurationArn",
                regions=["regions"],
                source="source"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__454845c55f3f1aaf9ecd22e8c93755feb5b7430b144be8dea9edb8e2b0946cb9)
            check_type(argname="argument event_pattern", value=event_pattern, expected_type=type_hints["event_pattern"])
            check_type(argname="argument event_type", value=event_type, expected_type=type_hints["event_type"])
            check_type(argname="argument notification_configuration_arn", value=notification_configuration_arn, expected_type=type_hints["notification_configuration_arn"])
            check_type(argname="argument regions", value=regions, expected_type=type_hints["regions"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if event_pattern is not None:
            self._values["event_pattern"] = event_pattern
        if event_type is not None:
            self._values["event_type"] = event_type
        if notification_configuration_arn is not None:
            self._values["notification_configuration_arn"] = notification_configuration_arn
        if regions is not None:
            self._values["regions"] = regions
        if source is not None:
            self._values["source"] = source

    @builtins.property
    def event_pattern(self) -> typing.Optional[builtins.str]:
        '''An additional event pattern used to further filter the events this ``EventRule`` receives.

        For more information, see `Amazon EventBridge event patterns <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-event-patterns.html>`_ in the *Amazon EventBridge User Guide.*

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-notifications-eventrule.html#cfn-notifications-eventrule-eventpattern
        '''
        result = self._values.get("event_pattern")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_type(self) -> typing.Optional[builtins.str]:
        '''The event type this rule should match with the EventBridge events.

        It must match with atleast one of the valid EventBridge event types. For example, Amazon EC2 Instance State change Notification and Amazon CloudWatch State Change. For more information, see `Event delivery from AWS services <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-service-event.html#eb-service-event-delivery-level>`_ in the *Amazon EventBridge User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-notifications-eventrule.html#cfn-notifications-eventrule-eventtype
        '''
        result = self._values.get("event_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_configuration_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN for the ``NotificationConfiguration`` associated with this ``EventRule`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-notifications-eventrule.html#cfn-notifications-eventrule-notificationconfigurationarn
        '''
        result = self._values.get("notification_configuration_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of AWS Regions that send events to this ``EventRule`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-notifications-eventrule.html#cfn-notifications-eventrule-regions
        '''
        result = self._values.get("regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''The event source this rule should match with the EventBridge event sources.

        It must match with atleast one of the valid EventBridge event sources. Only AWS service sourced events are supported. For example, ``aws.ec2`` and ``aws.cloudwatch`` . For more information, see `Event delivery from AWS services <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-service-event.html#eb-service-event-delivery-level>`_ in the *Amazon EventBridge User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-notifications-eventrule.html#cfn-notifications-eventrule-source
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEventRuleMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnEventRulePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_notifications.mixins.CfnEventRulePropsMixin",
):
    '''Creates an ```EventRule`` <https://docs.aws.amazon.com/notifications/latest/userguide/glossary.html>`_ that is associated with a specified ``NotificationConfiguration`` .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-notifications-eventrule.html
    :cloudformationResource: AWS::Notifications::EventRule
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_notifications import mixins as notifications_mixins
        
        cfn_event_rule_props_mixin = notifications_mixins.CfnEventRulePropsMixin(notifications_mixins.CfnEventRuleMixinProps(
            event_pattern="eventPattern",
            event_type="eventType",
            notification_configuration_arn="notificationConfigurationArn",
            regions=["regions"],
            source="source"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnEventRuleMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Notifications::EventRule``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85fb0d8861ef80d36d1b604fc483a81d8d6e6699e2f65eeee67683875727078d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b36f866fcb61b49383eb5453078a3c5ad83654ccc877f22350761e5b65fb1a9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e68f82ff5b1637f069de54257e87fa860a986d5e3dc999373dccc33a564aa7c0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnEventRuleMixinProps:
        return typing.cast(CfnEventRuleMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_notifications.mixins.CfnEventRulePropsMixin.EventRuleStatusSummaryProperty",
        jsii_struct_bases=[],
        name_mapping={"reason": "reason", "status": "status"},
    )
    class EventRuleStatusSummaryProperty:
        def __init__(
            self,
            *,
            reason: typing.Optional[builtins.str] = None,
            status: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides additional information about the current ``EventRule`` status.

            :param reason: A human-readable reason for ``EventRuleStatus`` .
            :param status: The status of the ``EventRule`` . - Values: - ``ACTIVE`` - The ``EventRule`` can process events. - ``INACTIVE`` - The ``EventRule`` may be unable to process events. - ``CREATING`` - The ``EventRule`` is being created. Only ``GET`` and ``LIST`` calls can be run. - ``UPDATING`` - The ``EventRule`` is being updated. Only ``GET`` and ``LIST`` calls can be run. - ``DELETING`` - The ``EventRule`` is being deleted. Only ``GET`` and ``LIST`` calls can be run.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-notifications-eventrule-eventrulestatussummary.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_notifications import mixins as notifications_mixins
                
                event_rule_status_summary_property = notifications_mixins.CfnEventRulePropsMixin.EventRuleStatusSummaryProperty(
                    reason="reason",
                    status="status"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__aee0c0a1ec8d5703247ec6afcb4ea095435bb0c6e1843b246f8522e7a44539d7)
                check_type(argname="argument reason", value=reason, expected_type=type_hints["reason"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if reason is not None:
                self._values["reason"] = reason
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def reason(self) -> typing.Optional[builtins.str]:
            '''A human-readable reason for ``EventRuleStatus`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-notifications-eventrule-eventrulestatussummary.html#cfn-notifications-eventrule-eventrulestatussummary-reason
            '''
            result = self._values.get("reason")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''The status of the ``EventRule`` .

            - Values:
            - ``ACTIVE``
            - The ``EventRule`` can process events.
            - ``INACTIVE``
            - The ``EventRule`` may be unable to process events.
            - ``CREATING``
            - The ``EventRule`` is being created.

            Only ``GET`` and ``LIST`` calls can be run.

            - ``UPDATING``
            - The ``EventRule`` is being updated.

            Only ``GET`` and ``LIST`` calls can be run.

            - ``DELETING``
            - The ``EventRule`` is being deleted.

            Only ``GET`` and ``LIST`` calls can be run.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-notifications-eventrule-eventrulestatussummary.html#cfn-notifications-eventrule-eventrulestatussummary-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventRuleStatusSummaryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_notifications.mixins.CfnManagedNotificationAccountContactAssociationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "contact_identifier": "contactIdentifier",
        "managed_notification_configuration_arn": "managedNotificationConfigurationArn",
    },
)
class CfnManagedNotificationAccountContactAssociationMixinProps:
    def __init__(
        self,
        *,
        contact_identifier: typing.Optional[builtins.str] = None,
        managed_notification_configuration_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnManagedNotificationAccountContactAssociationPropsMixin.

        :param contact_identifier: The unique identifier of the notification contact associated with the AWS account. For more information about the contact types associated with an account, see the `Account Management Reference Guide <https://docs.aws.amazon.com/accounts/latest/reference/manage-acct-update-contact-alternate.html#manage-acct-update-contact-alternate-orgs>`_ .
        :param managed_notification_configuration_arn: The ARN of the ``ManagedNotificationConfiguration`` to be associated with the ``Channel`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-notifications-managednotificationaccountcontactassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_notifications import mixins as notifications_mixins
            
            cfn_managed_notification_account_contact_association_mixin_props = notifications_mixins.CfnManagedNotificationAccountContactAssociationMixinProps(
                contact_identifier="contactIdentifier",
                managed_notification_configuration_arn="managedNotificationConfigurationArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b50074bccca11e47c7c47a3e205069373075920d005865c8c64b259a3710b1e)
            check_type(argname="argument contact_identifier", value=contact_identifier, expected_type=type_hints["contact_identifier"])
            check_type(argname="argument managed_notification_configuration_arn", value=managed_notification_configuration_arn, expected_type=type_hints["managed_notification_configuration_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if contact_identifier is not None:
            self._values["contact_identifier"] = contact_identifier
        if managed_notification_configuration_arn is not None:
            self._values["managed_notification_configuration_arn"] = managed_notification_configuration_arn

    @builtins.property
    def contact_identifier(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the notification contact associated with the AWS account.

        For more information about the contact types associated with an account, see the `Account Management Reference Guide <https://docs.aws.amazon.com/accounts/latest/reference/manage-acct-update-contact-alternate.html#manage-acct-update-contact-alternate-orgs>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-notifications-managednotificationaccountcontactassociation.html#cfn-notifications-managednotificationaccountcontactassociation-contactidentifier
        '''
        result = self._values.get("contact_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managed_notification_configuration_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the ``ManagedNotificationConfiguration`` to be associated with the ``Channel`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-notifications-managednotificationaccountcontactassociation.html#cfn-notifications-managednotificationaccountcontactassociation-managednotificationconfigurationarn
        '''
        result = self._values.get("managed_notification_configuration_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnManagedNotificationAccountContactAssociationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnManagedNotificationAccountContactAssociationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_notifications.mixins.CfnManagedNotificationAccountContactAssociationPropsMixin",
):
    '''Associates an Account Management Contact with a ``ManagedNotificationConfiguration`` for AWS User Notifications .

    For more information about AWS User Notifications , see the `AWS User Notifications User Guide <https://docs.aws.amazon.com/notifications/latest/userguide/what-is-service.html>`_ . For more information about Account Management Contacts, see the `Account Management Reference Guide <https://docs.aws.amazon.com/accounts/latest/reference/API_AlternateContact.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-notifications-managednotificationaccountcontactassociation.html
    :cloudformationResource: AWS::Notifications::ManagedNotificationAccountContactAssociation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_notifications import mixins as notifications_mixins
        
        cfn_managed_notification_account_contact_association_props_mixin = notifications_mixins.CfnManagedNotificationAccountContactAssociationPropsMixin(notifications_mixins.CfnManagedNotificationAccountContactAssociationMixinProps(
            contact_identifier="contactIdentifier",
            managed_notification_configuration_arn="managedNotificationConfigurationArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnManagedNotificationAccountContactAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Notifications::ManagedNotificationAccountContactAssociation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__329835a66741ecdd3a920b4a09fe0af95f0683d1b761c65ddd83e659deb31b49)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a55933930f9e27287fc1688abfd6e17dab598ca4c3a1f9220dcee60602e8d98)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1897bb67a9a33f6a9f819b206c33a7b16726e7e5d6ae16953555137c77bc61cd)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnManagedNotificationAccountContactAssociationMixinProps:
        return typing.cast(CfnManagedNotificationAccountContactAssociationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_notifications.mixins.CfnManagedNotificationAdditionalChannelAssociationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "channel_arn": "channelArn",
        "managed_notification_configuration_arn": "managedNotificationConfigurationArn",
    },
)
class CfnManagedNotificationAdditionalChannelAssociationMixinProps:
    def __init__(
        self,
        *,
        channel_arn: typing.Optional[builtins.str] = None,
        managed_notification_configuration_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnManagedNotificationAdditionalChannelAssociationPropsMixin.

        :param channel_arn: The ARN of the ``Channel`` .
        :param managed_notification_configuration_arn: The ARN of the ``ManagedNotificationAdditionalChannelAssociation`` associated with the ``Channel`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-notifications-managednotificationadditionalchannelassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_notifications import mixins as notifications_mixins
            
            cfn_managed_notification_additional_channel_association_mixin_props = notifications_mixins.CfnManagedNotificationAdditionalChannelAssociationMixinProps(
                channel_arn="channelArn",
                managed_notification_configuration_arn="managedNotificationConfigurationArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__625f23678441146ccf27e8e8f10cda09472927f3175edc645a71c6b1e486160d)
            check_type(argname="argument channel_arn", value=channel_arn, expected_type=type_hints["channel_arn"])
            check_type(argname="argument managed_notification_configuration_arn", value=managed_notification_configuration_arn, expected_type=type_hints["managed_notification_configuration_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if channel_arn is not None:
            self._values["channel_arn"] = channel_arn
        if managed_notification_configuration_arn is not None:
            self._values["managed_notification_configuration_arn"] = managed_notification_configuration_arn

    @builtins.property
    def channel_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the ``Channel`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-notifications-managednotificationadditionalchannelassociation.html#cfn-notifications-managednotificationadditionalchannelassociation-channelarn
        '''
        result = self._values.get("channel_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managed_notification_configuration_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the ``ManagedNotificationAdditionalChannelAssociation`` associated with the ``Channel`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-notifications-managednotificationadditionalchannelassociation.html#cfn-notifications-managednotificationadditionalchannelassociation-managednotificationconfigurationarn
        '''
        result = self._values.get("managed_notification_configuration_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnManagedNotificationAdditionalChannelAssociationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnManagedNotificationAdditionalChannelAssociationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_notifications.mixins.CfnManagedNotificationAdditionalChannelAssociationPropsMixin",
):
    '''Associates a ``Channel`` with a ``ManagedNotificationAdditionalChannelAssociation`` for AWS User Notifications .

    For more information about AWS User Notifications , see the `AWS User Notifications User Guide <https://docs.aws.amazon.com/notifications/latest/userguide/what-is-service.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-notifications-managednotificationadditionalchannelassociation.html
    :cloudformationResource: AWS::Notifications::ManagedNotificationAdditionalChannelAssociation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_notifications import mixins as notifications_mixins
        
        cfn_managed_notification_additional_channel_association_props_mixin = notifications_mixins.CfnManagedNotificationAdditionalChannelAssociationPropsMixin(notifications_mixins.CfnManagedNotificationAdditionalChannelAssociationMixinProps(
            channel_arn="channelArn",
            managed_notification_configuration_arn="managedNotificationConfigurationArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnManagedNotificationAdditionalChannelAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Notifications::ManagedNotificationAdditionalChannelAssociation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59fb17bcebcb23070fcb0fa4102a5607a18fe50d179530caa747a05f8592aff0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__336f8c66a8a44696b8cbac79c482502bbc5ab34e490b565f9ba8c5c315a6cd3b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e39f1e4d17c834e7aaec8a02ac86172063768de84d7e60e7f712cc90030a6340)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnManagedNotificationAdditionalChannelAssociationMixinProps:
        return typing.cast(CfnManagedNotificationAdditionalChannelAssociationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_notifications.mixins.CfnNotificationConfigurationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "aggregation_duration": "aggregationDuration",
        "description": "description",
        "name": "name",
        "tags": "tags",
    },
)
class CfnNotificationConfigurationMixinProps:
    def __init__(
        self,
        *,
        aggregation_duration: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnNotificationConfigurationPropsMixin.

        :param aggregation_duration: The aggregation preference of the ``NotificationConfiguration`` . - Values: - ``LONG`` - Aggregate notifications for long periods of time (12 hours). - ``SHORT`` - Aggregate notifications for short periods of time (5 minutes). - ``NONE`` - Don't aggregate notifications.
        :param description: The description of the ``NotificationConfiguration`` .
        :param name: The name of the ``NotificationConfiguration`` . Supports RFC 3986's unreserved characters.
        :param tags: A map of tags assigned to a ``NotificationConfiguration`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-notifications-notificationconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_notifications import mixins as notifications_mixins
            
            cfn_notification_configuration_mixin_props = notifications_mixins.CfnNotificationConfigurationMixinProps(
                aggregation_duration="aggregationDuration",
                description="description",
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__574a34934c688eb4ae2fa17b9ad558f838bdc2fc098b2878b764c2b3f543db20)
            check_type(argname="argument aggregation_duration", value=aggregation_duration, expected_type=type_hints["aggregation_duration"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aggregation_duration is not None:
            self._values["aggregation_duration"] = aggregation_duration
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def aggregation_duration(self) -> typing.Optional[builtins.str]:
        '''The aggregation preference of the ``NotificationConfiguration`` .

        - Values:
        - ``LONG``
        - Aggregate notifications for long periods of time (12 hours).
        - ``SHORT``
        - Aggregate notifications for short periods of time (5 minutes).
        - ``NONE``
        - Don't aggregate notifications.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-notifications-notificationconfiguration.html#cfn-notifications-notificationconfiguration-aggregationduration
        '''
        result = self._values.get("aggregation_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the ``NotificationConfiguration`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-notifications-notificationconfiguration.html#cfn-notifications-notificationconfiguration-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the ``NotificationConfiguration`` .

        Supports RFC 3986's unreserved characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-notifications-notificationconfiguration.html#cfn-notifications-notificationconfiguration-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A map of tags assigned to a ``NotificationConfiguration`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-notifications-notificationconfiguration.html#cfn-notifications-notificationconfiguration-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnNotificationConfigurationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnNotificationConfigurationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_notifications.mixins.CfnNotificationConfigurationPropsMixin",
):
    '''Configures a ``NotificationConfiguration`` for AWS User Notifications .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-notifications-notificationconfiguration.html
    :cloudformationResource: AWS::Notifications::NotificationConfiguration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_notifications import mixins as notifications_mixins
        
        cfn_notification_configuration_props_mixin = notifications_mixins.CfnNotificationConfigurationPropsMixin(notifications_mixins.CfnNotificationConfigurationMixinProps(
            aggregation_duration="aggregationDuration",
            description="description",
            name="name",
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
        props: typing.Union[CfnNotificationConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Notifications::NotificationConfiguration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3167bd8d4ce0be29e9aa9e122bf19a34a175afc596e50bb964c327de277759b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4abba098f92a955bc8ce15938e9b82f708285a55d4aea07646f355c98eb5f97)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__781334621ad18fcfc604ceb4950e35ba989eb4398bdb3a8149c6c4cd85745e25)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnNotificationConfigurationMixinProps:
        return typing.cast(CfnNotificationConfigurationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_notifications.mixins.CfnNotificationHubMixinProps",
    jsii_struct_bases=[],
    name_mapping={"region": "region"},
)
class CfnNotificationHubMixinProps:
    def __init__(self, *, region: typing.Optional[builtins.str] = None) -> None:
        '''Properties for CfnNotificationHubPropsMixin.

        :param region: The ``NotificationHub`` Region.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-notifications-notificationhub.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_notifications import mixins as notifications_mixins
            
            cfn_notification_hub_mixin_props = notifications_mixins.CfnNotificationHubMixinProps(
                region="region"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0376d26f9d8ad683a1e170c16da7a0d7541115907fbe3b26b76d430664294550)
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The ``NotificationHub`` Region.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-notifications-notificationhub.html#cfn-notifications-notificationhub-region
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnNotificationHubMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnNotificationHubPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_notifications.mixins.CfnNotificationHubPropsMixin",
):
    '''Configures a ``NotificationHub`` for AWS User Notifications .

    For more information about notification hub, see the `AWS User Notifications User Guide <https://docs.aws.amazon.com/notifications/latest/userguide/notification-hubs.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-notifications-notificationhub.html
    :cloudformationResource: AWS::Notifications::NotificationHub
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_notifications import mixins as notifications_mixins
        
        cfn_notification_hub_props_mixin = notifications_mixins.CfnNotificationHubPropsMixin(notifications_mixins.CfnNotificationHubMixinProps(
            region="region"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnNotificationHubMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Notifications::NotificationHub``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce95d0d74075a0284cff037611e7e6a52e9e708078738f09a7fb0a9b104cba3a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e09e22bb8b660e001f7db80eea22adc35af45045bc8fcf6d7269b1ce62433006)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fd7f2dadf49dbd151377a132d9d4c2a8089672dabb39e2e39e5f057fc4180e0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnNotificationHubMixinProps:
        return typing.cast(CfnNotificationHubMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_notifications.mixins.CfnNotificationHubPropsMixin.NotificationHubStatusSummaryProperty",
        jsii_struct_bases=[],
        name_mapping={
            "notification_hub_status": "notificationHubStatus",
            "notification_hub_status_reason": "notificationHubStatusReason",
        },
    )
    class NotificationHubStatusSummaryProperty:
        def __init__(
            self,
            *,
            notification_hub_status: typing.Optional[builtins.str] = None,
            notification_hub_status_reason: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides additional information about the current ``NotificationHub`` status.

            :param notification_hub_status: Indicates the current status of the ``NotificationHub`` .
            :param notification_hub_status_reason: An explanation for the current status.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-notifications-notificationhub-notificationhubstatussummary.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_notifications import mixins as notifications_mixins
                
                notification_hub_status_summary_property = notifications_mixins.CfnNotificationHubPropsMixin.NotificationHubStatusSummaryProperty(
                    notification_hub_status="notificationHubStatus",
                    notification_hub_status_reason="notificationHubStatusReason"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__358581c164cfe5373ae4e7213b0ef533620e4bbacf5fa8b6632401fa7a5300e8)
                check_type(argname="argument notification_hub_status", value=notification_hub_status, expected_type=type_hints["notification_hub_status"])
                check_type(argname="argument notification_hub_status_reason", value=notification_hub_status_reason, expected_type=type_hints["notification_hub_status_reason"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if notification_hub_status is not None:
                self._values["notification_hub_status"] = notification_hub_status
            if notification_hub_status_reason is not None:
                self._values["notification_hub_status_reason"] = notification_hub_status_reason

        @builtins.property
        def notification_hub_status(self) -> typing.Optional[builtins.str]:
            '''Indicates the current status of the ``NotificationHub`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-notifications-notificationhub-notificationhubstatussummary.html#cfn-notifications-notificationhub-notificationhubstatussummary-notificationhubstatus
            '''
            result = self._values.get("notification_hub_status")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def notification_hub_status_reason(self) -> typing.Optional[builtins.str]:
            '''An explanation for the current status.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-notifications-notificationhub-notificationhubstatussummary.html#cfn-notifications-notificationhub-notificationhubstatussummary-notificationhubstatusreason
            '''
            result = self._values.get("notification_hub_status_reason")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NotificationHubStatusSummaryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_notifications.mixins.CfnOrganizationalUnitAssociationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "notification_configuration_arn": "notificationConfigurationArn",
        "organizational_unit_id": "organizationalUnitId",
    },
)
class CfnOrganizationalUnitAssociationMixinProps:
    def __init__(
        self,
        *,
        notification_configuration_arn: typing.Optional[builtins.str] = None,
        organizational_unit_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnOrganizationalUnitAssociationPropsMixin.

        :param notification_configuration_arn: ARN identifier of the NotificationConfiguration. Example: arn:aws:notifications::123456789012:configuration/a01jes88qxwkbj05xv9c967pgm1
        :param organizational_unit_id: The ID of the organizational unit.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-notifications-organizationalunitassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_notifications import mixins as notifications_mixins
            
            cfn_organizational_unit_association_mixin_props = notifications_mixins.CfnOrganizationalUnitAssociationMixinProps(
                notification_configuration_arn="notificationConfigurationArn",
                organizational_unit_id="organizationalUnitId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc503e7e995d845bd8002a8b44779e67188f62d79ddaf0582793622257c5c6b4)
            check_type(argname="argument notification_configuration_arn", value=notification_configuration_arn, expected_type=type_hints["notification_configuration_arn"])
            check_type(argname="argument organizational_unit_id", value=organizational_unit_id, expected_type=type_hints["organizational_unit_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if notification_configuration_arn is not None:
            self._values["notification_configuration_arn"] = notification_configuration_arn
        if organizational_unit_id is not None:
            self._values["organizational_unit_id"] = organizational_unit_id

    @builtins.property
    def notification_configuration_arn(self) -> typing.Optional[builtins.str]:
        '''ARN identifier of the NotificationConfiguration.

        Example: arn:aws:notifications::123456789012:configuration/a01jes88qxwkbj05xv9c967pgm1

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-notifications-organizationalunitassociation.html#cfn-notifications-organizationalunitassociation-notificationconfigurationarn
        '''
        result = self._values.get("notification_configuration_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def organizational_unit_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the organizational unit.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-notifications-organizationalunitassociation.html#cfn-notifications-organizationalunitassociation-organizationalunitid
        '''
        result = self._values.get("organizational_unit_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnOrganizationalUnitAssociationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnOrganizationalUnitAssociationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_notifications.mixins.CfnOrganizationalUnitAssociationPropsMixin",
):
    '''Resource Type definition for AWS::Notifications::OrganizationalUnitAssociation.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-notifications-organizationalunitassociation.html
    :cloudformationResource: AWS::Notifications::OrganizationalUnitAssociation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_notifications import mixins as notifications_mixins
        
        cfn_organizational_unit_association_props_mixin = notifications_mixins.CfnOrganizationalUnitAssociationPropsMixin(notifications_mixins.CfnOrganizationalUnitAssociationMixinProps(
            notification_configuration_arn="notificationConfigurationArn",
            organizational_unit_id="organizationalUnitId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnOrganizationalUnitAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Notifications::OrganizationalUnitAssociation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b30322febc19d34c4bad670d88a89f31f117eefacc29d33199c931bf8a51cc5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0634d0dc4d22512563bb639615c7c57a5c10c3322196ed5fba8d211018e0b9e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76759831410feaf9237bff864d85b5da733a119820571d72fe16a419fd06f6f4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnOrganizationalUnitAssociationMixinProps:
        return typing.cast(CfnOrganizationalUnitAssociationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnChannelAssociationMixinProps",
    "CfnChannelAssociationPropsMixin",
    "CfnEventRuleMixinProps",
    "CfnEventRulePropsMixin",
    "CfnManagedNotificationAccountContactAssociationMixinProps",
    "CfnManagedNotificationAccountContactAssociationPropsMixin",
    "CfnManagedNotificationAdditionalChannelAssociationMixinProps",
    "CfnManagedNotificationAdditionalChannelAssociationPropsMixin",
    "CfnNotificationConfigurationMixinProps",
    "CfnNotificationConfigurationPropsMixin",
    "CfnNotificationHubMixinProps",
    "CfnNotificationHubPropsMixin",
    "CfnOrganizationalUnitAssociationMixinProps",
    "CfnOrganizationalUnitAssociationPropsMixin",
]

publication.publish()

def _typecheckingstub__f05a7ba00a3875da8d3d796f739e71a7e0e2595986480d1d35a55dbbf8e6ab74(
    *,
    arn: typing.Optional[builtins.str] = None,
    notification_configuration_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__622241d91676e535367c726f228fb7aad31287aa94ec0951f71f61b43b8dac52(
    props: typing.Union[CfnChannelAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1996773ea646a8f86d373d143629f97cf536fd415d893143293cc465f7ae820d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c9bdc689eb4537f71c3b7285c1332388a146cb06b79739ca8ccdebb94f8c538(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__454845c55f3f1aaf9ecd22e8c93755feb5b7430b144be8dea9edb8e2b0946cb9(
    *,
    event_pattern: typing.Optional[builtins.str] = None,
    event_type: typing.Optional[builtins.str] = None,
    notification_configuration_arn: typing.Optional[builtins.str] = None,
    regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85fb0d8861ef80d36d1b604fc483a81d8d6e6699e2f65eeee67683875727078d(
    props: typing.Union[CfnEventRuleMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b36f866fcb61b49383eb5453078a3c5ad83654ccc877f22350761e5b65fb1a9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e68f82ff5b1637f069de54257e87fa860a986d5e3dc999373dccc33a564aa7c0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aee0c0a1ec8d5703247ec6afcb4ea095435bb0c6e1843b246f8522e7a44539d7(
    *,
    reason: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b50074bccca11e47c7c47a3e205069373075920d005865c8c64b259a3710b1e(
    *,
    contact_identifier: typing.Optional[builtins.str] = None,
    managed_notification_configuration_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__329835a66741ecdd3a920b4a09fe0af95f0683d1b761c65ddd83e659deb31b49(
    props: typing.Union[CfnManagedNotificationAccountContactAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a55933930f9e27287fc1688abfd6e17dab598ca4c3a1f9220dcee60602e8d98(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1897bb67a9a33f6a9f819b206c33a7b16726e7e5d6ae16953555137c77bc61cd(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__625f23678441146ccf27e8e8f10cda09472927f3175edc645a71c6b1e486160d(
    *,
    channel_arn: typing.Optional[builtins.str] = None,
    managed_notification_configuration_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59fb17bcebcb23070fcb0fa4102a5607a18fe50d179530caa747a05f8592aff0(
    props: typing.Union[CfnManagedNotificationAdditionalChannelAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__336f8c66a8a44696b8cbac79c482502bbc5ab34e490b565f9ba8c5c315a6cd3b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e39f1e4d17c834e7aaec8a02ac86172063768de84d7e60e7f712cc90030a6340(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__574a34934c688eb4ae2fa17b9ad558f838bdc2fc098b2878b764c2b3f543db20(
    *,
    aggregation_duration: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3167bd8d4ce0be29e9aa9e122bf19a34a175afc596e50bb964c327de277759b(
    props: typing.Union[CfnNotificationConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4abba098f92a955bc8ce15938e9b82f708285a55d4aea07646f355c98eb5f97(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__781334621ad18fcfc604ceb4950e35ba989eb4398bdb3a8149c6c4cd85745e25(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0376d26f9d8ad683a1e170c16da7a0d7541115907fbe3b26b76d430664294550(
    *,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce95d0d74075a0284cff037611e7e6a52e9e708078738f09a7fb0a9b104cba3a(
    props: typing.Union[CfnNotificationHubMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e09e22bb8b660e001f7db80eea22adc35af45045bc8fcf6d7269b1ce62433006(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fd7f2dadf49dbd151377a132d9d4c2a8089672dabb39e2e39e5f057fc4180e0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__358581c164cfe5373ae4e7213b0ef533620e4bbacf5fa8b6632401fa7a5300e8(
    *,
    notification_hub_status: typing.Optional[builtins.str] = None,
    notification_hub_status_reason: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc503e7e995d845bd8002a8b44779e67188f62d79ddaf0582793622257c5c6b4(
    *,
    notification_configuration_arn: typing.Optional[builtins.str] = None,
    organizational_unit_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b30322febc19d34c4bad670d88a89f31f117eefacc29d33199c931bf8a51cc5(
    props: typing.Union[CfnOrganizationalUnitAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0634d0dc4d22512563bb639615c7c57a5c10c3322196ed5fba8d211018e0b9e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76759831410feaf9237bff864d85b5da733a119820571d72fe16a419fd06f6f4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
