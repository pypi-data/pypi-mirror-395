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
    jsii_type="@aws-cdk/mixins-preview.aws_ssmincidents.mixins.CfnReplicationSetMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "deletion_protected": "deletionProtected",
        "regions": "regions",
        "tags": "tags",
    },
)
class CfnReplicationSetMixinProps:
    def __init__(
        self,
        *,
        deletion_protected: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        regions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnReplicationSetPropsMixin.ReplicationRegionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnReplicationSetPropsMixin.

        :param deletion_protected: Determines if the replication set deletion protection is enabled or not. If deletion protection is enabled, you can't delete the last Region in the replication set.
        :param regions: Specifies the Regions of the replication set.
        :param tags: A list of tags to add to the replication set.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmincidents-replicationset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ssmincidents import mixins as ssmincidents_mixins
            
            cfn_replication_set_mixin_props = ssmincidents_mixins.CfnReplicationSetMixinProps(
                deletion_protected=False,
                regions=[ssmincidents_mixins.CfnReplicationSetPropsMixin.ReplicationRegionProperty(
                    region_configuration=ssmincidents_mixins.CfnReplicationSetPropsMixin.RegionConfigurationProperty(
                        sse_kms_key_id="sseKmsKeyId"
                    ),
                    region_name="regionName"
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5697467a060c7f31a46a37a5e0662acfe314fb3c9923ce30fc8f1274a31a17e)
            check_type(argname="argument deletion_protected", value=deletion_protected, expected_type=type_hints["deletion_protected"])
            check_type(argname="argument regions", value=regions, expected_type=type_hints["regions"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if deletion_protected is not None:
            self._values["deletion_protected"] = deletion_protected
        if regions is not None:
            self._values["regions"] = regions
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def deletion_protected(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Determines if the replication set deletion protection is enabled or not.

        If deletion protection is enabled, you can't delete the last Region in the replication set.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmincidents-replicationset.html#cfn-ssmincidents-replicationset-deletionprotected
        '''
        result = self._values.get("deletion_protected")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def regions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReplicationSetPropsMixin.ReplicationRegionProperty"]]]]:
        '''Specifies the Regions of the replication set.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmincidents-replicationset.html#cfn-ssmincidents-replicationset-regions
        '''
        result = self._values.get("regions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReplicationSetPropsMixin.ReplicationRegionProperty"]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of tags to add to the replication set.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmincidents-replicationset.html#cfn-ssmincidents-replicationset-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnReplicationSetMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnReplicationSetPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ssmincidents.mixins.CfnReplicationSetPropsMixin",
):
    '''The ``AWS::SSMIncidents::ReplicationSet`` resource specifies a set of AWS Regions that Incident Manager data is replicated to and the AWS Key Management Service ( AWS  key used to encrypt the data.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmincidents-replicationset.html
    :cloudformationResource: AWS::SSMIncidents::ReplicationSet
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ssmincidents import mixins as ssmincidents_mixins
        
        cfn_replication_set_props_mixin = ssmincidents_mixins.CfnReplicationSetPropsMixin(ssmincidents_mixins.CfnReplicationSetMixinProps(
            deletion_protected=False,
            regions=[ssmincidents_mixins.CfnReplicationSetPropsMixin.ReplicationRegionProperty(
                region_configuration=ssmincidents_mixins.CfnReplicationSetPropsMixin.RegionConfigurationProperty(
                    sse_kms_key_id="sseKmsKeyId"
                ),
                region_name="regionName"
            )],
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
        props: typing.Union[CfnReplicationSetMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SSMIncidents::ReplicationSet``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f12a451b47ea0de6aa68afce84a52e11d27d7496716fcbf23797dee9301dc8a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0b758deea13c99748eaf5e372ecf4a30446b595c0d3e03ca016692fdb6863d2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ccefc30ae6d4cdb3a682e0e1c7b8bfacaa9284a88666e47faa689ee0e12d03b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnReplicationSetMixinProps:
        return typing.cast(CfnReplicationSetMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssmincidents.mixins.CfnReplicationSetPropsMixin.RegionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"sse_kms_key_id": "sseKmsKeyId"},
    )
    class RegionConfigurationProperty:
        def __init__(
            self,
            *,
            sse_kms_key_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``RegionConfiguration`` property specifies the Region and AWS Key Management Service key to add to the replication set.

            :param sse_kms_key_id: The AWS Key Management Service key ID to use to encrypt your replication set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmincidents-replicationset-regionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssmincidents import mixins as ssmincidents_mixins
                
                region_configuration_property = ssmincidents_mixins.CfnReplicationSetPropsMixin.RegionConfigurationProperty(
                    sse_kms_key_id="sseKmsKeyId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1f0f5d24643127530ba9b75d52a1ca62e5bba90b385e845cd2a4526d5d8dee5c)
                check_type(argname="argument sse_kms_key_id", value=sse_kms_key_id, expected_type=type_hints["sse_kms_key_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if sse_kms_key_id is not None:
                self._values["sse_kms_key_id"] = sse_kms_key_id

        @builtins.property
        def sse_kms_key_id(self) -> typing.Optional[builtins.str]:
            '''The AWS Key Management Service key ID to use to encrypt your replication set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmincidents-replicationset-regionconfiguration.html#cfn-ssmincidents-replicationset-regionconfiguration-ssekmskeyid
            '''
            result = self._values.get("sse_kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RegionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssmincidents.mixins.CfnReplicationSetPropsMixin.ReplicationRegionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "region_configuration": "regionConfiguration",
            "region_name": "regionName",
        },
    )
    class ReplicationRegionProperty:
        def __init__(
            self,
            *,
            region_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnReplicationSetPropsMixin.RegionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            region_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``ReplicationRegion`` property type specifies the Region and AWS Key Management Service key to add to the replication set.

            :param region_configuration: Specifies the Region configuration.
            :param region_name: Specifies the region name to add to the replication set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmincidents-replicationset-replicationregion.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssmincidents import mixins as ssmincidents_mixins
                
                replication_region_property = ssmincidents_mixins.CfnReplicationSetPropsMixin.ReplicationRegionProperty(
                    region_configuration=ssmincidents_mixins.CfnReplicationSetPropsMixin.RegionConfigurationProperty(
                        sse_kms_key_id="sseKmsKeyId"
                    ),
                    region_name="regionName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__48c0ad5a250b5e5fece5475d7bfd753ec26ff28ab7eeebe4ba90e615b739b5bc)
                check_type(argname="argument region_configuration", value=region_configuration, expected_type=type_hints["region_configuration"])
                check_type(argname="argument region_name", value=region_name, expected_type=type_hints["region_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if region_configuration is not None:
                self._values["region_configuration"] = region_configuration
            if region_name is not None:
                self._values["region_name"] = region_name

        @builtins.property
        def region_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReplicationSetPropsMixin.RegionConfigurationProperty"]]:
            '''Specifies the Region configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmincidents-replicationset-replicationregion.html#cfn-ssmincidents-replicationset-replicationregion-regionconfiguration
            '''
            result = self._values.get("region_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReplicationSetPropsMixin.RegionConfigurationProperty"]], result)

        @builtins.property
        def region_name(self) -> typing.Optional[builtins.str]:
            '''Specifies the region name to add to the replication set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmincidents-replicationset-replicationregion.html#cfn-ssmincidents-replicationset-replicationregion-regionname
            '''
            result = self._values.get("region_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReplicationRegionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ssmincidents.mixins.CfnResponsePlanMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "actions": "actions",
        "chat_channel": "chatChannel",
        "display_name": "displayName",
        "engagements": "engagements",
        "incident_template": "incidentTemplate",
        "integrations": "integrations",
        "name": "name",
        "tags": "tags",
    },
)
class CfnResponsePlanMixinProps:
    def __init__(
        self,
        *,
        actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResponsePlanPropsMixin.ActionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        chat_channel: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResponsePlanPropsMixin.ChatChannelProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        display_name: typing.Optional[builtins.str] = None,
        engagements: typing.Optional[typing.Sequence[builtins.str]] = None,
        incident_template: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResponsePlanPropsMixin.IncidentTemplateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        integrations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResponsePlanPropsMixin.IntegrationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnResponsePlanPropsMixin.

        :param actions: The actions that the response plan starts at the beginning of an incident.
        :param chat_channel: The chat channel used for collaboration during an incident.
        :param display_name: The human readable name of the response plan.
        :param engagements: The Amazon Resource Name (ARN) for the contacts and escalation plans that the response plan engages during an incident.
        :param incident_template: Details used to create an incident when using this response plan.
        :param integrations: Information about third-party services integrated into the response plan.
        :param name: The name of the response plan.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmincidents-responseplan.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ssmincidents import mixins as ssmincidents_mixins
            
            cfn_response_plan_mixin_props = ssmincidents_mixins.CfnResponsePlanMixinProps(
                actions=[ssmincidents_mixins.CfnResponsePlanPropsMixin.ActionProperty(
                    ssm_automation=ssmincidents_mixins.CfnResponsePlanPropsMixin.SsmAutomationProperty(
                        document_name="documentName",
                        document_version="documentVersion",
                        dynamic_parameters=[ssmincidents_mixins.CfnResponsePlanPropsMixin.DynamicSsmParameterProperty(
                            key="key",
                            value=ssmincidents_mixins.CfnResponsePlanPropsMixin.DynamicSsmParameterValueProperty(
                                variable="variable"
                            )
                        )],
                        parameters=[ssmincidents_mixins.CfnResponsePlanPropsMixin.SsmParameterProperty(
                            key="key",
                            values=["values"]
                        )],
                        role_arn="roleArn",
                        target_account="targetAccount"
                    )
                )],
                chat_channel=ssmincidents_mixins.CfnResponsePlanPropsMixin.ChatChannelProperty(
                    chatbot_sns=["chatbotSns"]
                ),
                display_name="displayName",
                engagements=["engagements"],
                incident_template=ssmincidents_mixins.CfnResponsePlanPropsMixin.IncidentTemplateProperty(
                    dedupe_string="dedupeString",
                    impact=123,
                    incident_tags=[CfnTag(
                        key="key",
                        value="value"
                    )],
                    notification_targets=[ssmincidents_mixins.CfnResponsePlanPropsMixin.NotificationTargetItemProperty(
                        sns_topic_arn="snsTopicArn"
                    )],
                    summary="summary",
                    title="title"
                ),
                integrations=[ssmincidents_mixins.CfnResponsePlanPropsMixin.IntegrationProperty(
                    pager_duty_configuration=ssmincidents_mixins.CfnResponsePlanPropsMixin.PagerDutyConfigurationProperty(
                        name="name",
                        pager_duty_incident_configuration=ssmincidents_mixins.CfnResponsePlanPropsMixin.PagerDutyIncidentConfigurationProperty(
                            service_id="serviceId"
                        ),
                        secret_id="secretId"
                    )
                )],
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1309279f7d6cbd4a05544d7f41a69177627fd0e98d0e206441d4571977876f5c)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument chat_channel", value=chat_channel, expected_type=type_hints["chat_channel"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument engagements", value=engagements, expected_type=type_hints["engagements"])
            check_type(argname="argument incident_template", value=incident_template, expected_type=type_hints["incident_template"])
            check_type(argname="argument integrations", value=integrations, expected_type=type_hints["integrations"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if actions is not None:
            self._values["actions"] = actions
        if chat_channel is not None:
            self._values["chat_channel"] = chat_channel
        if display_name is not None:
            self._values["display_name"] = display_name
        if engagements is not None:
            self._values["engagements"] = engagements
        if incident_template is not None:
            self._values["incident_template"] = incident_template
        if integrations is not None:
            self._values["integrations"] = integrations
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def actions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResponsePlanPropsMixin.ActionProperty"]]]]:
        '''The actions that the response plan starts at the beginning of an incident.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmincidents-responseplan.html#cfn-ssmincidents-responseplan-actions
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResponsePlanPropsMixin.ActionProperty"]]]], result)

    @builtins.property
    def chat_channel(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResponsePlanPropsMixin.ChatChannelProperty"]]:
        '''The  chat channel used for collaboration during an incident.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmincidents-responseplan.html#cfn-ssmincidents-responseplan-chatchannel
        '''
        result = self._values.get("chat_channel")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResponsePlanPropsMixin.ChatChannelProperty"]], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The human readable name of the response plan.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmincidents-responseplan.html#cfn-ssmincidents-responseplan-displayname
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def engagements(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Amazon Resource Name (ARN) for the contacts and escalation plans that the response plan engages during an incident.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmincidents-responseplan.html#cfn-ssmincidents-responseplan-engagements
        '''
        result = self._values.get("engagements")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def incident_template(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResponsePlanPropsMixin.IncidentTemplateProperty"]]:
        '''Details used to create an incident when using this response plan.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmincidents-responseplan.html#cfn-ssmincidents-responseplan-incidenttemplate
        '''
        result = self._values.get("incident_template")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResponsePlanPropsMixin.IncidentTemplateProperty"]], result)

    @builtins.property
    def integrations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResponsePlanPropsMixin.IntegrationProperty"]]]]:
        '''Information about third-party services integrated into the response plan.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmincidents-responseplan.html#cfn-ssmincidents-responseplan-integrations
        '''
        result = self._values.get("integrations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResponsePlanPropsMixin.IntegrationProperty"]]]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the response plan.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmincidents-responseplan.html#cfn-ssmincidents-responseplan-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmincidents-responseplan.html#cfn-ssmincidents-responseplan-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResponsePlanMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnResponsePlanPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ssmincidents.mixins.CfnResponsePlanPropsMixin",
):
    '''The ``AWS::SSMIncidents::ResponsePlan`` resource specifies the details of the response plan that are used when creating an incident.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmincidents-responseplan.html
    :cloudformationResource: AWS::SSMIncidents::ResponsePlan
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ssmincidents import mixins as ssmincidents_mixins
        
        cfn_response_plan_props_mixin = ssmincidents_mixins.CfnResponsePlanPropsMixin(ssmincidents_mixins.CfnResponsePlanMixinProps(
            actions=[ssmincidents_mixins.CfnResponsePlanPropsMixin.ActionProperty(
                ssm_automation=ssmincidents_mixins.CfnResponsePlanPropsMixin.SsmAutomationProperty(
                    document_name="documentName",
                    document_version="documentVersion",
                    dynamic_parameters=[ssmincidents_mixins.CfnResponsePlanPropsMixin.DynamicSsmParameterProperty(
                        key="key",
                        value=ssmincidents_mixins.CfnResponsePlanPropsMixin.DynamicSsmParameterValueProperty(
                            variable="variable"
                        )
                    )],
                    parameters=[ssmincidents_mixins.CfnResponsePlanPropsMixin.SsmParameterProperty(
                        key="key",
                        values=["values"]
                    )],
                    role_arn="roleArn",
                    target_account="targetAccount"
                )
            )],
            chat_channel=ssmincidents_mixins.CfnResponsePlanPropsMixin.ChatChannelProperty(
                chatbot_sns=["chatbotSns"]
            ),
            display_name="displayName",
            engagements=["engagements"],
            incident_template=ssmincidents_mixins.CfnResponsePlanPropsMixin.IncidentTemplateProperty(
                dedupe_string="dedupeString",
                impact=123,
                incident_tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                notification_targets=[ssmincidents_mixins.CfnResponsePlanPropsMixin.NotificationTargetItemProperty(
                    sns_topic_arn="snsTopicArn"
                )],
                summary="summary",
                title="title"
            ),
            integrations=[ssmincidents_mixins.CfnResponsePlanPropsMixin.IntegrationProperty(
                pager_duty_configuration=ssmincidents_mixins.CfnResponsePlanPropsMixin.PagerDutyConfigurationProperty(
                    name="name",
                    pager_duty_incident_configuration=ssmincidents_mixins.CfnResponsePlanPropsMixin.PagerDutyIncidentConfigurationProperty(
                        service_id="serviceId"
                    ),
                    secret_id="secretId"
                )
            )],
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
        props: typing.Union[CfnResponsePlanMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SSMIncidents::ResponsePlan``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f85c9d24ba21ac86105459a7b386a0a459cab9906554a2135b0ff60b94da2da4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bdeda4e5bb4174c49ecb5591c76ea82001473b06b5a9cda8bdb16e42af1d9502)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0082e2e471a2b3e13dedfc58e7762c1936a9e874fd6bb22543fd6ad02892c94c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnResponsePlanMixinProps:
        return typing.cast(CfnResponsePlanMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssmincidents.mixins.CfnResponsePlanPropsMixin.ActionProperty",
        jsii_struct_bases=[],
        name_mapping={"ssm_automation": "ssmAutomation"},
    )
    class ActionProperty:
        def __init__(
            self,
            *,
            ssm_automation: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResponsePlanPropsMixin.SsmAutomationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The ``Action`` property type specifies the configuration to launch.

            :param ssm_automation: Details about the Systems Manager automation document that will be used as a runbook during an incident.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmincidents-responseplan-action.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssmincidents import mixins as ssmincidents_mixins
                
                action_property = ssmincidents_mixins.CfnResponsePlanPropsMixin.ActionProperty(
                    ssm_automation=ssmincidents_mixins.CfnResponsePlanPropsMixin.SsmAutomationProperty(
                        document_name="documentName",
                        document_version="documentVersion",
                        dynamic_parameters=[ssmincidents_mixins.CfnResponsePlanPropsMixin.DynamicSsmParameterProperty(
                            key="key",
                            value=ssmincidents_mixins.CfnResponsePlanPropsMixin.DynamicSsmParameterValueProperty(
                                variable="variable"
                            )
                        )],
                        parameters=[ssmincidents_mixins.CfnResponsePlanPropsMixin.SsmParameterProperty(
                            key="key",
                            values=["values"]
                        )],
                        role_arn="roleArn",
                        target_account="targetAccount"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__23f7bcff5c4430f8608a9e82a4f0bbf2e393e809eda18b97f394a8806d292ef0)
                check_type(argname="argument ssm_automation", value=ssm_automation, expected_type=type_hints["ssm_automation"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ssm_automation is not None:
                self._values["ssm_automation"] = ssm_automation

        @builtins.property
        def ssm_automation(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResponsePlanPropsMixin.SsmAutomationProperty"]]:
            '''Details about the Systems Manager automation document that will be used as a runbook during an incident.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmincidents-responseplan-action.html#cfn-ssmincidents-responseplan-action-ssmautomation
            '''
            result = self._values.get("ssm_automation")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResponsePlanPropsMixin.SsmAutomationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssmincidents.mixins.CfnResponsePlanPropsMixin.ChatChannelProperty",
        jsii_struct_bases=[],
        name_mapping={"chatbot_sns": "chatbotSns"},
    )
    class ChatChannelProperty:
        def __init__(
            self,
            *,
            chatbot_sns: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The  chat channel used for collaboration during an incident.

            :param chatbot_sns: The Amazon targets that uses to notify the chat channel of updates to an incident. You can also make updates to the incident through the chat channel by using the Amazon topics

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmincidents-responseplan-chatchannel.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssmincidents import mixins as ssmincidents_mixins
                
                chat_channel_property = ssmincidents_mixins.CfnResponsePlanPropsMixin.ChatChannelProperty(
                    chatbot_sns=["chatbotSns"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__072fda2916f037f1d58c5aa41362591a1641e0df58621d2839ea9cf61f27c96a)
                check_type(argname="argument chatbot_sns", value=chatbot_sns, expected_type=type_hints["chatbot_sns"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if chatbot_sns is not None:
                self._values["chatbot_sns"] = chatbot_sns

        @builtins.property
        def chatbot_sns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The Amazon  targets that  uses to notify the chat channel of updates to an incident.

            You can also make updates to the incident through the chat channel by using the Amazon  topics

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmincidents-responseplan-chatchannel.html#cfn-ssmincidents-responseplan-chatchannel-chatbotsns
            '''
            result = self._values.get("chatbot_sns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ChatChannelProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssmincidents.mixins.CfnResponsePlanPropsMixin.DynamicSsmParameterProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class DynamicSsmParameterProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResponsePlanPropsMixin.DynamicSsmParameterValueProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''When you add a runbook to a response plan, you can specify the parameters for the runbook to use at runtime.

            Response plans support parameters with both static and dynamic values. For static values, you enter the value when you define the parameter in the response plan. For dynamic values, the system determines the correct parameter value by collecting information from the incident. Incident Manager supports the following dynamic parameters:

            *Incident ARN*

            When Incident Manager creates an incident, the system captures the Amazon Resource Name (ARN) of the corresponding incident record and enters it for this parameter in the runbook.
            .. epigraph::

               This value can only be assigned to parameters of type ``String`` . If assigned to a parameter of any other type, the runbook fails to run.

            *Involved resources*

            When Incident Manager creates an incident, the system captures the ARNs of the resources involved in the incident. These resource ARNs are then assigned to this parameter in the runbook.
            .. epigraph::

               This value can only be assigned to parameters of type ``StringList`` . If assigned to a parameter of any other type, the runbook fails to run.

            :param key: The key parameter to use when running the Systems Manager Automation runbook.
            :param value: The dynamic parameter value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmincidents-responseplan-dynamicssmparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssmincidents import mixins as ssmincidents_mixins
                
                dynamic_ssm_parameter_property = ssmincidents_mixins.CfnResponsePlanPropsMixin.DynamicSsmParameterProperty(
                    key="key",
                    value=ssmincidents_mixins.CfnResponsePlanPropsMixin.DynamicSsmParameterValueProperty(
                        variable="variable"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fccf333cdb0bac6b052f927ec126bec8b8f3b8f0c82a888a8024128d5a327b48)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The key parameter to use when running the Systems Manager Automation runbook.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmincidents-responseplan-dynamicssmparameter.html#cfn-ssmincidents-responseplan-dynamicssmparameter-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResponsePlanPropsMixin.DynamicSsmParameterValueProperty"]]:
            '''The dynamic parameter value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmincidents-responseplan-dynamicssmparameter.html#cfn-ssmincidents-responseplan-dynamicssmparameter-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResponsePlanPropsMixin.DynamicSsmParameterValueProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DynamicSsmParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssmincidents.mixins.CfnResponsePlanPropsMixin.DynamicSsmParameterValueProperty",
        jsii_struct_bases=[],
        name_mapping={"variable": "variable"},
    )
    class DynamicSsmParameterValueProperty:
        def __init__(self, *, variable: typing.Optional[builtins.str] = None) -> None:
            '''The dynamic parameter value.

            :param variable: Variable dynamic parameters. A parameter value is determined when an incident is created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmincidents-responseplan-dynamicssmparametervalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssmincidents import mixins as ssmincidents_mixins
                
                dynamic_ssm_parameter_value_property = ssmincidents_mixins.CfnResponsePlanPropsMixin.DynamicSsmParameterValueProperty(
                    variable="variable"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bc41e3ff5267b06eb5c36cf6227afedc937357858a78781ed8cde10ecbe5ff9f)
                check_type(argname="argument variable", value=variable, expected_type=type_hints["variable"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if variable is not None:
                self._values["variable"] = variable

        @builtins.property
        def variable(self) -> typing.Optional[builtins.str]:
            '''Variable dynamic parameters.

            A parameter value is determined when an incident is created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmincidents-responseplan-dynamicssmparametervalue.html#cfn-ssmincidents-responseplan-dynamicssmparametervalue-variable
            '''
            result = self._values.get("variable")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DynamicSsmParameterValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssmincidents.mixins.CfnResponsePlanPropsMixin.IncidentTemplateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dedupe_string": "dedupeString",
            "impact": "impact",
            "incident_tags": "incidentTags",
            "notification_targets": "notificationTargets",
            "summary": "summary",
            "title": "title",
        },
    )
    class IncidentTemplateProperty:
        def __init__(
            self,
            *,
            dedupe_string: typing.Optional[builtins.str] = None,
            impact: typing.Optional[jsii.Number] = None,
            incident_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]]]] = None,
            notification_targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResponsePlanPropsMixin.NotificationTargetItemProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            summary: typing.Optional[builtins.str] = None,
            title: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``IncidentTemplate`` property type specifies details used to create an incident when using this response plan.

            :param dedupe_string: Used to create only one incident record for an incident.
            :param impact: Defines the impact to the customers. Providing an impact overwrites the impact provided by a response plan. **Possible impacts:** - ``1`` - Critical impact, this typically relates to full application failure that impacts many to all customers. - ``2`` - High impact, partial application failure with impact to many customers. - ``3`` - Medium impact, the application is providing reduced service to customers. - ``4`` - Low impact, customer might aren't impacted by the problem yet. - ``5`` - No impact, customers aren't currently impacted but urgent action is needed to avoid impact.
            :param incident_tags: Tags to assign to the template. When the ``StartIncident`` API action is called, Incident Manager assigns the tags specified in the template to the incident.
            :param notification_targets: The Amazon Simple Notification Service ( Amazon ) targets that uses to notify the chat channel of updates to an incident. You can also make updates to the incident through the chat channel using the Amazon topics.
            :param summary: The summary describes what has happened during the incident.
            :param title: The title of the incident is a brief and easily recognizable.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmincidents-responseplan-incidenttemplate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssmincidents import mixins as ssmincidents_mixins
                
                incident_template_property = ssmincidents_mixins.CfnResponsePlanPropsMixin.IncidentTemplateProperty(
                    dedupe_string="dedupeString",
                    impact=123,
                    incident_tags=[CfnTag(
                        key="key",
                        value="value"
                    )],
                    notification_targets=[ssmincidents_mixins.CfnResponsePlanPropsMixin.NotificationTargetItemProperty(
                        sns_topic_arn="snsTopicArn"
                    )],
                    summary="summary",
                    title="title"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__53e724318f0a137e5808bfd8fe9959031888abc8802254b3805f0f4a7893156b)
                check_type(argname="argument dedupe_string", value=dedupe_string, expected_type=type_hints["dedupe_string"])
                check_type(argname="argument impact", value=impact, expected_type=type_hints["impact"])
                check_type(argname="argument incident_tags", value=incident_tags, expected_type=type_hints["incident_tags"])
                check_type(argname="argument notification_targets", value=notification_targets, expected_type=type_hints["notification_targets"])
                check_type(argname="argument summary", value=summary, expected_type=type_hints["summary"])
                check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dedupe_string is not None:
                self._values["dedupe_string"] = dedupe_string
            if impact is not None:
                self._values["impact"] = impact
            if incident_tags is not None:
                self._values["incident_tags"] = incident_tags
            if notification_targets is not None:
                self._values["notification_targets"] = notification_targets
            if summary is not None:
                self._values["summary"] = summary
            if title is not None:
                self._values["title"] = title

        @builtins.property
        def dedupe_string(self) -> typing.Optional[builtins.str]:
            '''Used to create only one incident record for an incident.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmincidents-responseplan-incidenttemplate.html#cfn-ssmincidents-responseplan-incidenttemplate-dedupestring
            '''
            result = self._values.get("dedupe_string")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def impact(self) -> typing.Optional[jsii.Number]:
            '''Defines the impact to the customers. Providing an impact overwrites the impact provided by a response plan.

            **Possible impacts:** - ``1`` - Critical impact, this typically relates to full application failure that impacts many to all customers.

            - ``2`` - High impact, partial application failure with impact to many customers.
            - ``3`` - Medium impact, the application is providing reduced service to customers.
            - ``4`` - Low impact, customer might aren't impacted by the problem yet.
            - ``5`` - No impact, customers aren't currently impacted but urgent action is needed to avoid impact.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmincidents-responseplan-incidenttemplate.html#cfn-ssmincidents-responseplan-incidenttemplate-impact
            '''
            result = self._values.get("impact")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def incident_tags(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_ceddda9d.CfnTag]]]]:
            '''Tags to assign to the template.

            When the ``StartIncident`` API action is called, Incident Manager assigns the tags specified in the template to the incident.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmincidents-responseplan-incidenttemplate.html#cfn-ssmincidents-responseplan-incidenttemplate-incidenttags
            '''
            result = self._values.get("incident_tags")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_ceddda9d.CfnTag]]]], result)

        @builtins.property
        def notification_targets(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResponsePlanPropsMixin.NotificationTargetItemProperty"]]]]:
            '''The Amazon Simple Notification Service ( Amazon  ) targets that  uses to notify the chat channel of updates to an incident.

            You can also make updates to the incident through the chat channel using the Amazon  topics.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmincidents-responseplan-incidenttemplate.html#cfn-ssmincidents-responseplan-incidenttemplate-notificationtargets
            '''
            result = self._values.get("notification_targets")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResponsePlanPropsMixin.NotificationTargetItemProperty"]]]], result)

        @builtins.property
        def summary(self) -> typing.Optional[builtins.str]:
            '''The summary describes what has happened during the incident.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmincidents-responseplan-incidenttemplate.html#cfn-ssmincidents-responseplan-incidenttemplate-summary
            '''
            result = self._values.get("summary")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def title(self) -> typing.Optional[builtins.str]:
            '''The title of the incident is a brief and easily recognizable.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmincidents-responseplan-incidenttemplate.html#cfn-ssmincidents-responseplan-incidenttemplate-title
            '''
            result = self._values.get("title")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IncidentTemplateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssmincidents.mixins.CfnResponsePlanPropsMixin.IntegrationProperty",
        jsii_struct_bases=[],
        name_mapping={"pager_duty_configuration": "pagerDutyConfiguration"},
    )
    class IntegrationProperty:
        def __init__(
            self,
            *,
            pager_duty_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResponsePlanPropsMixin.PagerDutyConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Information about third-party services integrated into a response plan.

            :param pager_duty_configuration: Information about the PagerDuty service where the response plan creates an incident.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmincidents-responseplan-integration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssmincidents import mixins as ssmincidents_mixins
                
                integration_property = ssmincidents_mixins.CfnResponsePlanPropsMixin.IntegrationProperty(
                    pager_duty_configuration=ssmincidents_mixins.CfnResponsePlanPropsMixin.PagerDutyConfigurationProperty(
                        name="name",
                        pager_duty_incident_configuration=ssmincidents_mixins.CfnResponsePlanPropsMixin.PagerDutyIncidentConfigurationProperty(
                            service_id="serviceId"
                        ),
                        secret_id="secretId"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0f13dbc58f979c2ac6c6819bcc42e07f0c407e6ceaf5e366142433786017e0dc)
                check_type(argname="argument pager_duty_configuration", value=pager_duty_configuration, expected_type=type_hints["pager_duty_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if pager_duty_configuration is not None:
                self._values["pager_duty_configuration"] = pager_duty_configuration

        @builtins.property
        def pager_duty_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResponsePlanPropsMixin.PagerDutyConfigurationProperty"]]:
            '''Information about the PagerDuty service where the response plan creates an incident.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmincidents-responseplan-integration.html#cfn-ssmincidents-responseplan-integration-pagerdutyconfiguration
            '''
            result = self._values.get("pager_duty_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResponsePlanPropsMixin.PagerDutyConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IntegrationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssmincidents.mixins.CfnResponsePlanPropsMixin.NotificationTargetItemProperty",
        jsii_struct_bases=[],
        name_mapping={"sns_topic_arn": "snsTopicArn"},
    )
    class NotificationTargetItemProperty:
        def __init__(
            self,
            *,
            sns_topic_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The Amazon  topic that's used by  to notify the incidents chat channel.

            :param sns_topic_arn: The Amazon Resource Name (ARN) of the Amazon topic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmincidents-responseplan-notificationtargetitem.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssmincidents import mixins as ssmincidents_mixins
                
                notification_target_item_property = ssmincidents_mixins.CfnResponsePlanPropsMixin.NotificationTargetItemProperty(
                    sns_topic_arn="snsTopicArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__09bb3a9c0ebc5cb6871c67f733ef1adf0ae7a7ec03662e318ae8651862028b5d)
                check_type(argname="argument sns_topic_arn", value=sns_topic_arn, expected_type=type_hints["sns_topic_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if sns_topic_arn is not None:
                self._values["sns_topic_arn"] = sns_topic_arn

        @builtins.property
        def sns_topic_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Amazon  topic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmincidents-responseplan-notificationtargetitem.html#cfn-ssmincidents-responseplan-notificationtargetitem-snstopicarn
            '''
            result = self._values.get("sns_topic_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NotificationTargetItemProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssmincidents.mixins.CfnResponsePlanPropsMixin.PagerDutyConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "name": "name",
            "pager_duty_incident_configuration": "pagerDutyIncidentConfiguration",
            "secret_id": "secretId",
        },
    )
    class PagerDutyConfigurationProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            pager_duty_incident_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResponsePlanPropsMixin.PagerDutyIncidentConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            secret_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Details about the PagerDuty configuration for a response plan.

            :param name: The name of the PagerDuty configuration.
            :param pager_duty_incident_configuration: Details about the PagerDuty service associated with the configuration.
            :param secret_id: The ID of the AWS Secrets Manager secret that stores your PagerDuty key, either a General Access REST API Key or User Token REST API Key, and other user credentials.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmincidents-responseplan-pagerdutyconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssmincidents import mixins as ssmincidents_mixins
                
                pager_duty_configuration_property = ssmincidents_mixins.CfnResponsePlanPropsMixin.PagerDutyConfigurationProperty(
                    name="name",
                    pager_duty_incident_configuration=ssmincidents_mixins.CfnResponsePlanPropsMixin.PagerDutyIncidentConfigurationProperty(
                        service_id="serviceId"
                    ),
                    secret_id="secretId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3a7610cd1042fe666194d872ee69e0b64f4c67d14a4340d57e8d42d75f46c9fe)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument pager_duty_incident_configuration", value=pager_duty_incident_configuration, expected_type=type_hints["pager_duty_incident_configuration"])
                check_type(argname="argument secret_id", value=secret_id, expected_type=type_hints["secret_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if pager_duty_incident_configuration is not None:
                self._values["pager_duty_incident_configuration"] = pager_duty_incident_configuration
            if secret_id is not None:
                self._values["secret_id"] = secret_id

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the PagerDuty configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmincidents-responseplan-pagerdutyconfiguration.html#cfn-ssmincidents-responseplan-pagerdutyconfiguration-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def pager_duty_incident_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResponsePlanPropsMixin.PagerDutyIncidentConfigurationProperty"]]:
            '''Details about the PagerDuty service associated with the configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmincidents-responseplan-pagerdutyconfiguration.html#cfn-ssmincidents-responseplan-pagerdutyconfiguration-pagerdutyincidentconfiguration
            '''
            result = self._values.get("pager_duty_incident_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResponsePlanPropsMixin.PagerDutyIncidentConfigurationProperty"]], result)

        @builtins.property
        def secret_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the AWS Secrets Manager secret that stores your PagerDuty key, either a General Access REST API Key or User Token REST API Key, and other user credentials.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmincidents-responseplan-pagerdutyconfiguration.html#cfn-ssmincidents-responseplan-pagerdutyconfiguration-secretid
            '''
            result = self._values.get("secret_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PagerDutyConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssmincidents.mixins.CfnResponsePlanPropsMixin.PagerDutyIncidentConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"service_id": "serviceId"},
    )
    class PagerDutyIncidentConfigurationProperty:
        def __init__(self, *, service_id: typing.Optional[builtins.str] = None) -> None:
            '''Details about the PagerDuty service where the response plan creates an incident.

            :param service_id: The ID of the PagerDuty service that the response plan associates with an incident when it launches.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmincidents-responseplan-pagerdutyincidentconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssmincidents import mixins as ssmincidents_mixins
                
                pager_duty_incident_configuration_property = ssmincidents_mixins.CfnResponsePlanPropsMixin.PagerDutyIncidentConfigurationProperty(
                    service_id="serviceId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ea780fc4f6dc15e16a7ce7d3db1ead32f7effa7e25a11ada983d72dde0459890)
                check_type(argname="argument service_id", value=service_id, expected_type=type_hints["service_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if service_id is not None:
                self._values["service_id"] = service_id

        @builtins.property
        def service_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the PagerDuty service that the response plan associates with an incident when it launches.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmincidents-responseplan-pagerdutyincidentconfiguration.html#cfn-ssmincidents-responseplan-pagerdutyincidentconfiguration-serviceid
            '''
            result = self._values.get("service_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PagerDutyIncidentConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssmincidents.mixins.CfnResponsePlanPropsMixin.SsmAutomationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "document_name": "documentName",
            "document_version": "documentVersion",
            "dynamic_parameters": "dynamicParameters",
            "parameters": "parameters",
            "role_arn": "roleArn",
            "target_account": "targetAccount",
        },
    )
    class SsmAutomationProperty:
        def __init__(
            self,
            *,
            document_name: typing.Optional[builtins.str] = None,
            document_version: typing.Optional[builtins.str] = None,
            dynamic_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResponsePlanPropsMixin.DynamicSsmParameterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResponsePlanPropsMixin.SsmParameterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            role_arn: typing.Optional[builtins.str] = None,
            target_account: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``SsmAutomation`` property type specifies details about the Systems Manager Automation runbook that will be used as the runbook during an incident.

            :param document_name: The automation document's name.
            :param document_version: The version of the runbook to use when running.
            :param dynamic_parameters: The key-value pairs to resolve dynamic parameter values when processing a Systems Manager Automation runbook.
            :param parameters: The key-value pair parameters to use when running the runbook.
            :param role_arn: The Amazon Resource Name (ARN) of the role that the automation document will assume when running commands.
            :param target_account: The account that the automation document will be run in. This can be in either the management account or an application account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmincidents-responseplan-ssmautomation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssmincidents import mixins as ssmincidents_mixins
                
                ssm_automation_property = ssmincidents_mixins.CfnResponsePlanPropsMixin.SsmAutomationProperty(
                    document_name="documentName",
                    document_version="documentVersion",
                    dynamic_parameters=[ssmincidents_mixins.CfnResponsePlanPropsMixin.DynamicSsmParameterProperty(
                        key="key",
                        value=ssmincidents_mixins.CfnResponsePlanPropsMixin.DynamicSsmParameterValueProperty(
                            variable="variable"
                        )
                    )],
                    parameters=[ssmincidents_mixins.CfnResponsePlanPropsMixin.SsmParameterProperty(
                        key="key",
                        values=["values"]
                    )],
                    role_arn="roleArn",
                    target_account="targetAccount"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5a94a53facfd948550d8e197c96380adc471d12774505a11e07a96b980874bf5)
                check_type(argname="argument document_name", value=document_name, expected_type=type_hints["document_name"])
                check_type(argname="argument document_version", value=document_version, expected_type=type_hints["document_version"])
                check_type(argname="argument dynamic_parameters", value=dynamic_parameters, expected_type=type_hints["dynamic_parameters"])
                check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument target_account", value=target_account, expected_type=type_hints["target_account"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if document_name is not None:
                self._values["document_name"] = document_name
            if document_version is not None:
                self._values["document_version"] = document_version
            if dynamic_parameters is not None:
                self._values["dynamic_parameters"] = dynamic_parameters
            if parameters is not None:
                self._values["parameters"] = parameters
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if target_account is not None:
                self._values["target_account"] = target_account

        @builtins.property
        def document_name(self) -> typing.Optional[builtins.str]:
            '''The automation document's name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmincidents-responseplan-ssmautomation.html#cfn-ssmincidents-responseplan-ssmautomation-documentname
            '''
            result = self._values.get("document_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def document_version(self) -> typing.Optional[builtins.str]:
            '''The version of the runbook to use when running.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmincidents-responseplan-ssmautomation.html#cfn-ssmincidents-responseplan-ssmautomation-documentversion
            '''
            result = self._values.get("document_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def dynamic_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResponsePlanPropsMixin.DynamicSsmParameterProperty"]]]]:
            '''The key-value pairs to resolve dynamic parameter values when processing a Systems Manager Automation runbook.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmincidents-responseplan-ssmautomation.html#cfn-ssmincidents-responseplan-ssmautomation-dynamicparameters
            '''
            result = self._values.get("dynamic_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResponsePlanPropsMixin.DynamicSsmParameterProperty"]]]], result)

        @builtins.property
        def parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResponsePlanPropsMixin.SsmParameterProperty"]]]]:
            '''The key-value pair parameters to use when running the runbook.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmincidents-responseplan-ssmautomation.html#cfn-ssmincidents-responseplan-ssmautomation-parameters
            '''
            result = self._values.get("parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResponsePlanPropsMixin.SsmParameterProperty"]]]], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the role that the automation document will assume when running commands.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmincidents-responseplan-ssmautomation.html#cfn-ssmincidents-responseplan-ssmautomation-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_account(self) -> typing.Optional[builtins.str]:
            '''The account that the automation document will be run in.

            This can be in either the management account or an application account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmincidents-responseplan-ssmautomation.html#cfn-ssmincidents-responseplan-ssmautomation-targetaccount
            '''
            result = self._values.get("target_account")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SsmAutomationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssmincidents.mixins.CfnResponsePlanPropsMixin.SsmParameterProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "values": "values"},
    )
    class SsmParameterProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The key-value pair parameters to use when running the Automation runbook.

            :param key: The key parameter to use when running the Automation runbook.
            :param values: The value parameter to use when running the Automation runbook.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmincidents-responseplan-ssmparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssmincidents import mixins as ssmincidents_mixins
                
                ssm_parameter_property = ssmincidents_mixins.CfnResponsePlanPropsMixin.SsmParameterProperty(
                    key="key",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bcde8a09747b2ff4290d05ec73e35319336f7d8b812b36dfa93bb918d48af6b1)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The key parameter to use when running the Automation runbook.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmincidents-responseplan-ssmparameter.html#cfn-ssmincidents-responseplan-ssmparameter-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The value parameter to use when running the Automation runbook.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmincidents-responseplan-ssmparameter.html#cfn-ssmincidents-responseplan-ssmparameter-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SsmParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnReplicationSetMixinProps",
    "CfnReplicationSetPropsMixin",
    "CfnResponsePlanMixinProps",
    "CfnResponsePlanPropsMixin",
]

publication.publish()

def _typecheckingstub__d5697467a060c7f31a46a37a5e0662acfe314fb3c9923ce30fc8f1274a31a17e(
    *,
    deletion_protected: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    regions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnReplicationSetPropsMixin.ReplicationRegionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f12a451b47ea0de6aa68afce84a52e11d27d7496716fcbf23797dee9301dc8a(
    props: typing.Union[CfnReplicationSetMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0b758deea13c99748eaf5e372ecf4a30446b595c0d3e03ca016692fdb6863d2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ccefc30ae6d4cdb3a682e0e1c7b8bfacaa9284a88666e47faa689ee0e12d03b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f0f5d24643127530ba9b75d52a1ca62e5bba90b385e845cd2a4526d5d8dee5c(
    *,
    sse_kms_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48c0ad5a250b5e5fece5475d7bfd753ec26ff28ab7eeebe4ba90e615b739b5bc(
    *,
    region_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnReplicationSetPropsMixin.RegionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    region_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1309279f7d6cbd4a05544d7f41a69177627fd0e98d0e206441d4571977876f5c(
    *,
    actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResponsePlanPropsMixin.ActionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    chat_channel: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResponsePlanPropsMixin.ChatChannelProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    display_name: typing.Optional[builtins.str] = None,
    engagements: typing.Optional[typing.Sequence[builtins.str]] = None,
    incident_template: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResponsePlanPropsMixin.IncidentTemplateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    integrations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResponsePlanPropsMixin.IntegrationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f85c9d24ba21ac86105459a7b386a0a459cab9906554a2135b0ff60b94da2da4(
    props: typing.Union[CfnResponsePlanMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdeda4e5bb4174c49ecb5591c76ea82001473b06b5a9cda8bdb16e42af1d9502(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0082e2e471a2b3e13dedfc58e7762c1936a9e874fd6bb22543fd6ad02892c94c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23f7bcff5c4430f8608a9e82a4f0bbf2e393e809eda18b97f394a8806d292ef0(
    *,
    ssm_automation: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResponsePlanPropsMixin.SsmAutomationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__072fda2916f037f1d58c5aa41362591a1641e0df58621d2839ea9cf61f27c96a(
    *,
    chatbot_sns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fccf333cdb0bac6b052f927ec126bec8b8f3b8f0c82a888a8024128d5a327b48(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResponsePlanPropsMixin.DynamicSsmParameterValueProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc41e3ff5267b06eb5c36cf6227afedc937357858a78781ed8cde10ecbe5ff9f(
    *,
    variable: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53e724318f0a137e5808bfd8fe9959031888abc8802254b3805f0f4a7893156b(
    *,
    dedupe_string: typing.Optional[builtins.str] = None,
    impact: typing.Optional[jsii.Number] = None,
    incident_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    notification_targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResponsePlanPropsMixin.NotificationTargetItemProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    summary: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f13dbc58f979c2ac6c6819bcc42e07f0c407e6ceaf5e366142433786017e0dc(
    *,
    pager_duty_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResponsePlanPropsMixin.PagerDutyConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09bb3a9c0ebc5cb6871c67f733ef1adf0ae7a7ec03662e318ae8651862028b5d(
    *,
    sns_topic_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a7610cd1042fe666194d872ee69e0b64f4c67d14a4340d57e8d42d75f46c9fe(
    *,
    name: typing.Optional[builtins.str] = None,
    pager_duty_incident_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResponsePlanPropsMixin.PagerDutyIncidentConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    secret_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea780fc4f6dc15e16a7ce7d3db1ead32f7effa7e25a11ada983d72dde0459890(
    *,
    service_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a94a53facfd948550d8e197c96380adc471d12774505a11e07a96b980874bf5(
    *,
    document_name: typing.Optional[builtins.str] = None,
    document_version: typing.Optional[builtins.str] = None,
    dynamic_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResponsePlanPropsMixin.DynamicSsmParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResponsePlanPropsMixin.SsmParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    role_arn: typing.Optional[builtins.str] = None,
    target_account: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcde8a09747b2ff4290d05ec73e35319336f7d8b812b36dfa93bb918d48af6b1(
    *,
    key: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
