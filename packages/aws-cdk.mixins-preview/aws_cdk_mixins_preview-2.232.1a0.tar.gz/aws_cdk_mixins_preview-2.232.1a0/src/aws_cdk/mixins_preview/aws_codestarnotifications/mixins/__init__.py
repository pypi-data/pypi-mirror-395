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
    jsii_type="@aws-cdk/mixins-preview.aws_codestarnotifications.mixins.CfnNotificationRuleMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "created_by": "createdBy",
        "detail_type": "detailType",
        "event_type_id": "eventTypeId",
        "event_type_ids": "eventTypeIds",
        "name": "name",
        "resource": "resource",
        "status": "status",
        "tags": "tags",
        "target_address": "targetAddress",
        "targets": "targets",
    },
)
class CfnNotificationRuleMixinProps:
    def __init__(
        self,
        *,
        created_by: typing.Optional[builtins.str] = None,
        detail_type: typing.Optional[builtins.str] = None,
        event_type_id: typing.Optional[builtins.str] = None,
        event_type_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        resource: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        target_address: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnNotificationRulePropsMixin.TargetProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnNotificationRulePropsMixin.

        :param created_by: The name or email alias of the person who created the notification rule.
        :param detail_type: The level of detail to include in the notifications for this resource. ``BASIC`` will include only the contents of the event as it would appear in Amazon CloudWatch. ``FULL`` will include any supplemental information provided by AWS CodeStar Notifications and/or the service for the resource for which the notification is created.
        :param event_type_id: The event type associated with this notification rule. For a complete list of event types and IDs, see `Notification concepts <https://docs.aws.amazon.com/dtconsole/latest/userguide/concepts.html#concepts-api>`_ in the *Developer Tools Console User Guide* .
        :param event_type_ids: A list of event types associated with this notification rule. For a complete list of event types and IDs, see `Notification concepts <https://docs.aws.amazon.com/dtconsole/latest/userguide/concepts.html#concepts-api>`_ in the *Developer Tools Console User Guide* .
        :param name: The name for the notification rule. Notification rule names must be unique in your AWS account .
        :param resource: The Amazon Resource Name (ARN) of the resource to associate with the notification rule. Supported resources include pipelines in AWS CodePipeline , repositories in AWS CodeCommit , and build projects in AWS CodeBuild .
        :param status: The status of the notification rule. The default value is ``ENABLED`` . If the status is set to ``DISABLED`` , notifications aren't sent for the notification rule.
        :param tags: A list of tags to apply to this notification rule. Key names cannot start with " ``aws`` ".
        :param target_address: The Amazon Resource Name (ARN) of the Amazon topic or client.
        :param targets: A list of Amazon Resource Names (ARNs) of Amazon topics and clients to associate with the notification rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_codestarnotifications import mixins as codestarnotifications_mixins
            
            cfn_notification_rule_mixin_props = codestarnotifications_mixins.CfnNotificationRuleMixinProps(
                created_by="createdBy",
                detail_type="detailType",
                event_type_id="eventTypeId",
                event_type_ids=["eventTypeIds"],
                name="name",
                resource="resource",
                status="status",
                tags={
                    "tags_key": "tags"
                },
                target_address="targetAddress",
                targets=[codestarnotifications_mixins.CfnNotificationRulePropsMixin.TargetProperty(
                    target_address="targetAddress",
                    target_type="targetType"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c93b9c2d3b0fdb70498955b3571f7934bdf50fc5e245f31c55f1a56c5db3e583)
            check_type(argname="argument created_by", value=created_by, expected_type=type_hints["created_by"])
            check_type(argname="argument detail_type", value=detail_type, expected_type=type_hints["detail_type"])
            check_type(argname="argument event_type_id", value=event_type_id, expected_type=type_hints["event_type_id"])
            check_type(argname="argument event_type_ids", value=event_type_ids, expected_type=type_hints["event_type_ids"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument target_address", value=target_address, expected_type=type_hints["target_address"])
            check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if created_by is not None:
            self._values["created_by"] = created_by
        if detail_type is not None:
            self._values["detail_type"] = detail_type
        if event_type_id is not None:
            self._values["event_type_id"] = event_type_id
        if event_type_ids is not None:
            self._values["event_type_ids"] = event_type_ids
        if name is not None:
            self._values["name"] = name
        if resource is not None:
            self._values["resource"] = resource
        if status is not None:
            self._values["status"] = status
        if tags is not None:
            self._values["tags"] = tags
        if target_address is not None:
            self._values["target_address"] = target_address
        if targets is not None:
            self._values["targets"] = targets

    @builtins.property
    def created_by(self) -> typing.Optional[builtins.str]:
        '''The name or email alias of the person who created the notification rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-createdby
        '''
        result = self._values.get("created_by")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def detail_type(self) -> typing.Optional[builtins.str]:
        '''The level of detail to include in the notifications for this resource.

        ``BASIC`` will include only the contents of the event as it would appear in Amazon CloudWatch. ``FULL`` will include any supplemental information provided by AWS CodeStar Notifications and/or the service for the resource for which the notification is created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-detailtype
        '''
        result = self._values.get("detail_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_type_id(self) -> typing.Optional[builtins.str]:
        '''The event type associated with this notification rule.

        For a complete list of event types and IDs, see `Notification concepts <https://docs.aws.amazon.com/dtconsole/latest/userguide/concepts.html#concepts-api>`_ in the *Developer Tools Console User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-eventtypeid
        '''
        result = self._values.get("event_type_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_type_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of event types associated with this notification rule.

        For a complete list of event types and IDs, see `Notification concepts <https://docs.aws.amazon.com/dtconsole/latest/userguide/concepts.html#concepts-api>`_ in the *Developer Tools Console User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-eventtypeids
        '''
        result = self._values.get("event_type_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name for the notification rule.

        Notification rule names must be unique in your AWS account .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the resource to associate with the notification rule.

        Supported resources include pipelines in AWS CodePipeline , repositories in AWS CodeCommit , and build projects in AWS CodeBuild .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-resource
        '''
        result = self._values.get("resource")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''The status of the notification rule.

        The default value is ``ENABLED`` . If the status is set to ``DISABLED`` , notifications aren't sent for the notification rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-status
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A list of tags to apply to this notification rule.

        Key names cannot start with " ``aws`` ".

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def target_address(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the Amazon  topic or  client.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-targetaddress
        '''
        result = self._values.get("target_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def targets(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnNotificationRulePropsMixin.TargetProperty"]]]]:
        '''A list of Amazon Resource Names (ARNs) of Amazon  topics and  clients to associate with the notification rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-targets
        '''
        result = self._values.get("targets")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnNotificationRulePropsMixin.TargetProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnNotificationRuleMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnNotificationRulePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_codestarnotifications.mixins.CfnNotificationRulePropsMixin",
):
    '''Creates a notification rule for a resource.

    The rule specifies the events you want notifications about and the targets (such as Amazon Simple Notification Service topics or  clients configured for Slack) where you want to receive them.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html
    :cloudformationResource: AWS::CodeStarNotifications::NotificationRule
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_codestarnotifications import mixins as codestarnotifications_mixins
        
        cfn_notification_rule_props_mixin = codestarnotifications_mixins.CfnNotificationRulePropsMixin(codestarnotifications_mixins.CfnNotificationRuleMixinProps(
            created_by="createdBy",
            detail_type="detailType",
            event_type_id="eventTypeId",
            event_type_ids=["eventTypeIds"],
            name="name",
            resource="resource",
            status="status",
            tags={
                "tags_key": "tags"
            },
            target_address="targetAddress",
            targets=[codestarnotifications_mixins.CfnNotificationRulePropsMixin.TargetProperty(
                target_address="targetAddress",
                target_type="targetType"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnNotificationRuleMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CodeStarNotifications::NotificationRule``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72c042149b37b653fe24bf122d214c1e0431170ca85da073e869eb4b4212c92d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd8374dd9748acc728d0637c2e23adfadc2f46fda6fbeec1a1371a82dc224a87)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41100091cbe86d6aa91151d77350714f760beab3f1c03f1b227d53056a694470)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnNotificationRuleMixinProps:
        return typing.cast(CfnNotificationRuleMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codestarnotifications.mixins.CfnNotificationRulePropsMixin.TargetProperty",
        jsii_struct_bases=[],
        name_mapping={"target_address": "targetAddress", "target_type": "targetType"},
    )
    class TargetProperty:
        def __init__(
            self,
            *,
            target_address: typing.Optional[builtins.str] = None,
            target_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about the  topics or  clients associated with a notification rule.

            :param target_address: The Amazon Resource Name (ARN) of the topic or client.
            :param target_type: The target type. Can be an Amazon Simple Notification Service topic or client. - Amazon Simple Notification Service topics are specified as ``SNS`` . - clients are specified as ``AWSChatbotSlack`` . - clients for Microsoft Teams are specified as ``AWSChatbotMicrosoftTeams`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codestarnotifications-notificationrule-target.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codestarnotifications import mixins as codestarnotifications_mixins
                
                target_property = codestarnotifications_mixins.CfnNotificationRulePropsMixin.TargetProperty(
                    target_address="targetAddress",
                    target_type="targetType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__25ed0e01c828cdaee2b044adf5c77fa82c1e01fa3ed7f8063d6faaac153432f1)
                check_type(argname="argument target_address", value=target_address, expected_type=type_hints["target_address"])
                check_type(argname="argument target_type", value=target_type, expected_type=type_hints["target_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if target_address is not None:
                self._values["target_address"] = target_address
            if target_type is not None:
                self._values["target_type"] = target_type

        @builtins.property
        def target_address(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the  topic or  client.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codestarnotifications-notificationrule-target.html#cfn-codestarnotifications-notificationrule-target-targetaddress
            '''
            result = self._values.get("target_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_type(self) -> typing.Optional[builtins.str]:
            '''The target type. Can be an Amazon Simple Notification Service topic or  client.

            - Amazon Simple Notification Service topics are specified as ``SNS`` .
            - clients are specified as ``AWSChatbotSlack`` .
            - clients for Microsoft Teams are specified as ``AWSChatbotMicrosoftTeams`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codestarnotifications-notificationrule-target.html#cfn-codestarnotifications-notificationrule-target-targettype
            '''
            result = self._values.get("target_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnNotificationRuleMixinProps",
    "CfnNotificationRulePropsMixin",
]

publication.publish()

def _typecheckingstub__c93b9c2d3b0fdb70498955b3571f7934bdf50fc5e245f31c55f1a56c5db3e583(
    *,
    created_by: typing.Optional[builtins.str] = None,
    detail_type: typing.Optional[builtins.str] = None,
    event_type_id: typing.Optional[builtins.str] = None,
    event_type_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    resource: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    target_address: typing.Optional[builtins.str] = None,
    targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnNotificationRulePropsMixin.TargetProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72c042149b37b653fe24bf122d214c1e0431170ca85da073e869eb4b4212c92d(
    props: typing.Union[CfnNotificationRuleMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd8374dd9748acc728d0637c2e23adfadc2f46fda6fbeec1a1371a82dc224a87(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41100091cbe86d6aa91151d77350714f760beab3f1c03f1b227d53056a694470(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25ed0e01c828cdaee2b044adf5c77fa82c1e01fa3ed7f8063d6faaac153432f1(
    *,
    target_address: typing.Optional[builtins.str] = None,
    target_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
