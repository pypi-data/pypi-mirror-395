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
    jsii_type="@aws-cdk/mixins-preview.aws_observabilityadmin.mixins.CfnOrganizationCentralizationRuleMixinProps",
    jsii_struct_bases=[],
    name_mapping={"rule": "rule", "rule_name": "ruleName", "tags": "tags"},
)
class CfnOrganizationCentralizationRuleMixinProps:
    def __init__(
        self,
        *,
        rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOrganizationCentralizationRulePropsMixin.CentralizationRuleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnOrganizationCentralizationRulePropsMixin.

        :param rule: 
        :param rule_name: The name of the organization centralization rule.
        :param tags: A key-value pair to filter resources based on tags associated with the resource. For more information about tags, see `What are tags? <https://docs.aws.amazon.com/whitepapers/latest/tagging-best-practices/what-are-tags.html>`_

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-observabilityadmin-organizationcentralizationrule.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_observabilityadmin import mixins as observabilityadmin_mixins
            
            cfn_organization_centralization_rule_mixin_props = observabilityadmin_mixins.CfnOrganizationCentralizationRuleMixinProps(
                rule=observabilityadmin_mixins.CfnOrganizationCentralizationRulePropsMixin.CentralizationRuleProperty(
                    destination=observabilityadmin_mixins.CfnOrganizationCentralizationRulePropsMixin.CentralizationRuleDestinationProperty(
                        account="account",
                        destination_logs_configuration=observabilityadmin_mixins.CfnOrganizationCentralizationRulePropsMixin.DestinationLogsConfigurationProperty(
                            backup_configuration=observabilityadmin_mixins.CfnOrganizationCentralizationRulePropsMixin.LogsBackupConfigurationProperty(
                                kms_key_arn="kmsKeyArn",
                                region="region"
                            ),
                            logs_encryption_configuration=observabilityadmin_mixins.CfnOrganizationCentralizationRulePropsMixin.LogsEncryptionConfigurationProperty(
                                encryption_conflict_resolution_strategy="encryptionConflictResolutionStrategy",
                                encryption_strategy="encryptionStrategy",
                                kms_key_arn="kmsKeyArn"
                            )
                        ),
                        region="region"
                    ),
                    source=observabilityadmin_mixins.CfnOrganizationCentralizationRulePropsMixin.CentralizationRuleSourceProperty(
                        regions=["regions"],
                        scope="scope",
                        source_logs_configuration=observabilityadmin_mixins.CfnOrganizationCentralizationRulePropsMixin.SourceLogsConfigurationProperty(
                            encrypted_log_group_strategy="encryptedLogGroupStrategy",
                            log_group_selection_criteria="logGroupSelectionCriteria"
                        )
                    )
                ),
                rule_name="ruleName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__310ec6a679061eb83926d8ae3b39173eb5ab3332834bcd390f2b95654cb0a988)
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
            check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if rule is not None:
            self._values["rule"] = rule
        if rule_name is not None:
            self._values["rule_name"] = rule_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def rule(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOrganizationCentralizationRulePropsMixin.CentralizationRuleProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-observabilityadmin-organizationcentralizationrule.html#cfn-observabilityadmin-organizationcentralizationrule-rule
        '''
        result = self._values.get("rule")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOrganizationCentralizationRulePropsMixin.CentralizationRuleProperty"]], result)

    @builtins.property
    def rule_name(self) -> typing.Optional[builtins.str]:
        '''The name of the organization centralization rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-observabilityadmin-organizationcentralizationrule.html#cfn-observabilityadmin-organizationcentralizationrule-rulename
        '''
        result = self._values.get("rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A key-value pair to filter resources based on tags associated with the resource.

        For more information about tags, see `What are tags? <https://docs.aws.amazon.com/whitepapers/latest/tagging-best-practices/what-are-tags.html>`_

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-observabilityadmin-organizationcentralizationrule.html#cfn-observabilityadmin-organizationcentralizationrule-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnOrganizationCentralizationRuleMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnOrganizationCentralizationRulePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_observabilityadmin.mixins.CfnOrganizationCentralizationRulePropsMixin",
):
    '''Defines how telemetry data should be centralized across an AWS Organization, including source and destination configurations.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-observabilityadmin-organizationcentralizationrule.html
    :cloudformationResource: AWS::ObservabilityAdmin::OrganizationCentralizationRule
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_observabilityadmin import mixins as observabilityadmin_mixins
        
        cfn_organization_centralization_rule_props_mixin = observabilityadmin_mixins.CfnOrganizationCentralizationRulePropsMixin(observabilityadmin_mixins.CfnOrganizationCentralizationRuleMixinProps(
            rule=observabilityadmin_mixins.CfnOrganizationCentralizationRulePropsMixin.CentralizationRuleProperty(
                destination=observabilityadmin_mixins.CfnOrganizationCentralizationRulePropsMixin.CentralizationRuleDestinationProperty(
                    account="account",
                    destination_logs_configuration=observabilityadmin_mixins.CfnOrganizationCentralizationRulePropsMixin.DestinationLogsConfigurationProperty(
                        backup_configuration=observabilityadmin_mixins.CfnOrganizationCentralizationRulePropsMixin.LogsBackupConfigurationProperty(
                            kms_key_arn="kmsKeyArn",
                            region="region"
                        ),
                        logs_encryption_configuration=observabilityadmin_mixins.CfnOrganizationCentralizationRulePropsMixin.LogsEncryptionConfigurationProperty(
                            encryption_conflict_resolution_strategy="encryptionConflictResolutionStrategy",
                            encryption_strategy="encryptionStrategy",
                            kms_key_arn="kmsKeyArn"
                        )
                    ),
                    region="region"
                ),
                source=observabilityadmin_mixins.CfnOrganizationCentralizationRulePropsMixin.CentralizationRuleSourceProperty(
                    regions=["regions"],
                    scope="scope",
                    source_logs_configuration=observabilityadmin_mixins.CfnOrganizationCentralizationRulePropsMixin.SourceLogsConfigurationProperty(
                        encrypted_log_group_strategy="encryptedLogGroupStrategy",
                        log_group_selection_criteria="logGroupSelectionCriteria"
                    )
                )
            ),
            rule_name="ruleName",
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
        props: typing.Union[CfnOrganizationCentralizationRuleMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ObservabilityAdmin::OrganizationCentralizationRule``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b92a09ea5de36bca1624cdcd88855863a8f25907b5e61b62b7133dd3d649072a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a090de4b65435c87ee9ab9d01f183e4b6a7d4b839d3d3ee55716dbb86843eff)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dee77b4f08a81761096aeb80a178d25ea4a782637b6bc9c71b6573905e47038f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnOrganizationCentralizationRuleMixinProps:
        return typing.cast(CfnOrganizationCentralizationRuleMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_observabilityadmin.mixins.CfnOrganizationCentralizationRulePropsMixin.CentralizationRuleDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "account": "account",
            "destination_logs_configuration": "destinationLogsConfiguration",
            "region": "region",
        },
    )
    class CentralizationRuleDestinationProperty:
        def __init__(
            self,
            *,
            account: typing.Optional[builtins.str] = None,
            destination_logs_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOrganizationCentralizationRulePropsMixin.DestinationLogsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            region: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration specifying the primary destination for centralized telemetry data.

            :param account: The destination account (within the organization) to which the telemetry data should be centralized.
            :param destination_logs_configuration: Log specific configuration for centralization destination log groups.
            :param region: The primary destination region to which telemetry data should be centralized.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-organizationcentralizationrule-centralizationruledestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_observabilityadmin import mixins as observabilityadmin_mixins
                
                centralization_rule_destination_property = observabilityadmin_mixins.CfnOrganizationCentralizationRulePropsMixin.CentralizationRuleDestinationProperty(
                    account="account",
                    destination_logs_configuration=observabilityadmin_mixins.CfnOrganizationCentralizationRulePropsMixin.DestinationLogsConfigurationProperty(
                        backup_configuration=observabilityadmin_mixins.CfnOrganizationCentralizationRulePropsMixin.LogsBackupConfigurationProperty(
                            kms_key_arn="kmsKeyArn",
                            region="region"
                        ),
                        logs_encryption_configuration=observabilityadmin_mixins.CfnOrganizationCentralizationRulePropsMixin.LogsEncryptionConfigurationProperty(
                            encryption_conflict_resolution_strategy="encryptionConflictResolutionStrategy",
                            encryption_strategy="encryptionStrategy",
                            kms_key_arn="kmsKeyArn"
                        )
                    ),
                    region="region"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d1fc4a314714a6ee9b9c5401241d44806f07d9b0144aab9bf41228542fbef316)
                check_type(argname="argument account", value=account, expected_type=type_hints["account"])
                check_type(argname="argument destination_logs_configuration", value=destination_logs_configuration, expected_type=type_hints["destination_logs_configuration"])
                check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if account is not None:
                self._values["account"] = account
            if destination_logs_configuration is not None:
                self._values["destination_logs_configuration"] = destination_logs_configuration
            if region is not None:
                self._values["region"] = region

        @builtins.property
        def account(self) -> typing.Optional[builtins.str]:
            '''The destination account (within the organization) to which the telemetry data should be centralized.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-organizationcentralizationrule-centralizationruledestination.html#cfn-observabilityadmin-organizationcentralizationrule-centralizationruledestination-account
            '''
            result = self._values.get("account")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def destination_logs_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOrganizationCentralizationRulePropsMixin.DestinationLogsConfigurationProperty"]]:
            '''Log specific configuration for centralization destination log groups.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-organizationcentralizationrule-centralizationruledestination.html#cfn-observabilityadmin-organizationcentralizationrule-centralizationruledestination-destinationlogsconfiguration
            '''
            result = self._values.get("destination_logs_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOrganizationCentralizationRulePropsMixin.DestinationLogsConfigurationProperty"]], result)

        @builtins.property
        def region(self) -> typing.Optional[builtins.str]:
            '''The primary destination region to which telemetry data should be centralized.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-organizationcentralizationrule-centralizationruledestination.html#cfn-observabilityadmin-organizationcentralizationrule-centralizationruledestination-region
            '''
            result = self._values.get("region")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CentralizationRuleDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_observabilityadmin.mixins.CfnOrganizationCentralizationRulePropsMixin.CentralizationRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"destination": "destination", "source": "source"},
    )
    class CentralizationRuleProperty:
        def __init__(
            self,
            *,
            destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOrganizationCentralizationRulePropsMixin.CentralizationRuleDestinationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOrganizationCentralizationRulePropsMixin.CentralizationRuleSourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Defines how telemetry data should be centralized across an AWS Organization, including source and destination configurations.

            :param destination: Configuration determining where the telemetry data should be centralized, backed up, as well as encryption configuration for the primary and backup destinations.
            :param source: Configuration determining the source of the telemetry data to be centralized.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-organizationcentralizationrule-centralizationrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_observabilityadmin import mixins as observabilityadmin_mixins
                
                centralization_rule_property = observabilityadmin_mixins.CfnOrganizationCentralizationRulePropsMixin.CentralizationRuleProperty(
                    destination=observabilityadmin_mixins.CfnOrganizationCentralizationRulePropsMixin.CentralizationRuleDestinationProperty(
                        account="account",
                        destination_logs_configuration=observabilityadmin_mixins.CfnOrganizationCentralizationRulePropsMixin.DestinationLogsConfigurationProperty(
                            backup_configuration=observabilityadmin_mixins.CfnOrganizationCentralizationRulePropsMixin.LogsBackupConfigurationProperty(
                                kms_key_arn="kmsKeyArn",
                                region="region"
                            ),
                            logs_encryption_configuration=observabilityadmin_mixins.CfnOrganizationCentralizationRulePropsMixin.LogsEncryptionConfigurationProperty(
                                encryption_conflict_resolution_strategy="encryptionConflictResolutionStrategy",
                                encryption_strategy="encryptionStrategy",
                                kms_key_arn="kmsKeyArn"
                            )
                        ),
                        region="region"
                    ),
                    source=observabilityadmin_mixins.CfnOrganizationCentralizationRulePropsMixin.CentralizationRuleSourceProperty(
                        regions=["regions"],
                        scope="scope",
                        source_logs_configuration=observabilityadmin_mixins.CfnOrganizationCentralizationRulePropsMixin.SourceLogsConfigurationProperty(
                            encrypted_log_group_strategy="encryptedLogGroupStrategy",
                            log_group_selection_criteria="logGroupSelectionCriteria"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__aeb025381c67cbd8d6fbeb2bf419a2922b2c6960d2ff942c49ffdb25ed4532bb)
                check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
                check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination is not None:
                self._values["destination"] = destination
            if source is not None:
                self._values["source"] = source

        @builtins.property
        def destination(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOrganizationCentralizationRulePropsMixin.CentralizationRuleDestinationProperty"]]:
            '''Configuration determining where the telemetry data should be centralized, backed up, as well as encryption configuration for the primary and backup destinations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-organizationcentralizationrule-centralizationrule.html#cfn-observabilityadmin-organizationcentralizationrule-centralizationrule-destination
            '''
            result = self._values.get("destination")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOrganizationCentralizationRulePropsMixin.CentralizationRuleDestinationProperty"]], result)

        @builtins.property
        def source(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOrganizationCentralizationRulePropsMixin.CentralizationRuleSourceProperty"]]:
            '''Configuration determining the source of the telemetry data to be centralized.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-organizationcentralizationrule-centralizationrule.html#cfn-observabilityadmin-organizationcentralizationrule-centralizationrule-source
            '''
            result = self._values.get("source")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOrganizationCentralizationRulePropsMixin.CentralizationRuleSourceProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CentralizationRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_observabilityadmin.mixins.CfnOrganizationCentralizationRulePropsMixin.CentralizationRuleSourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "regions": "regions",
            "scope": "scope",
            "source_logs_configuration": "sourceLogsConfiguration",
        },
    )
    class CentralizationRuleSourceProperty:
        def __init__(
            self,
            *,
            regions: typing.Optional[typing.Sequence[builtins.str]] = None,
            scope: typing.Optional[builtins.str] = None,
            source_logs_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOrganizationCentralizationRulePropsMixin.SourceLogsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Configuration specifying the source of telemetry data to be centralized.

            :param regions: The list of source regions from which telemetry data should be centralized.
            :param scope: The organizational scope from which telemetry data should be centralized, specified using organization id, accounts or organizational unit ids.
            :param source_logs_configuration: Log specific configuration for centralization source log groups.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-organizationcentralizationrule-centralizationrulesource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_observabilityadmin import mixins as observabilityadmin_mixins
                
                centralization_rule_source_property = observabilityadmin_mixins.CfnOrganizationCentralizationRulePropsMixin.CentralizationRuleSourceProperty(
                    regions=["regions"],
                    scope="scope",
                    source_logs_configuration=observabilityadmin_mixins.CfnOrganizationCentralizationRulePropsMixin.SourceLogsConfigurationProperty(
                        encrypted_log_group_strategy="encryptedLogGroupStrategy",
                        log_group_selection_criteria="logGroupSelectionCriteria"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__efe48945816c679e788eeaba1d740a2273e1e1c659b1fe3737dc05fd07e0f356)
                check_type(argname="argument regions", value=regions, expected_type=type_hints["regions"])
                check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
                check_type(argname="argument source_logs_configuration", value=source_logs_configuration, expected_type=type_hints["source_logs_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if regions is not None:
                self._values["regions"] = regions
            if scope is not None:
                self._values["scope"] = scope
            if source_logs_configuration is not None:
                self._values["source_logs_configuration"] = source_logs_configuration

        @builtins.property
        def regions(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of source regions from which telemetry data should be centralized.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-organizationcentralizationrule-centralizationrulesource.html#cfn-observabilityadmin-organizationcentralizationrule-centralizationrulesource-regions
            '''
            result = self._values.get("regions")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def scope(self) -> typing.Optional[builtins.str]:
            '''The organizational scope from which telemetry data should be centralized, specified using organization id, accounts or organizational unit ids.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-organizationcentralizationrule-centralizationrulesource.html#cfn-observabilityadmin-organizationcentralizationrule-centralizationrulesource-scope
            '''
            result = self._values.get("scope")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_logs_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOrganizationCentralizationRulePropsMixin.SourceLogsConfigurationProperty"]]:
            '''Log specific configuration for centralization source log groups.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-organizationcentralizationrule-centralizationrulesource.html#cfn-observabilityadmin-organizationcentralizationrule-centralizationrulesource-sourcelogsconfiguration
            '''
            result = self._values.get("source_logs_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOrganizationCentralizationRulePropsMixin.SourceLogsConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CentralizationRuleSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_observabilityadmin.mixins.CfnOrganizationCentralizationRulePropsMixin.DestinationLogsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "backup_configuration": "backupConfiguration",
            "logs_encryption_configuration": "logsEncryptionConfiguration",
        },
    )
    class DestinationLogsConfigurationProperty:
        def __init__(
            self,
            *,
            backup_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOrganizationCentralizationRulePropsMixin.LogsBackupConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            logs_encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOrganizationCentralizationRulePropsMixin.LogsEncryptionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Configuration for centralization destination log groups, including encryption and backup settings.

            :param backup_configuration: Configuration defining the backup region and an optional KMS key for the backup destination.
            :param logs_encryption_configuration: The encryption configuration for centralization destination log groups.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-organizationcentralizationrule-destinationlogsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_observabilityadmin import mixins as observabilityadmin_mixins
                
                destination_logs_configuration_property = observabilityadmin_mixins.CfnOrganizationCentralizationRulePropsMixin.DestinationLogsConfigurationProperty(
                    backup_configuration=observabilityadmin_mixins.CfnOrganizationCentralizationRulePropsMixin.LogsBackupConfigurationProperty(
                        kms_key_arn="kmsKeyArn",
                        region="region"
                    ),
                    logs_encryption_configuration=observabilityadmin_mixins.CfnOrganizationCentralizationRulePropsMixin.LogsEncryptionConfigurationProperty(
                        encryption_conflict_resolution_strategy="encryptionConflictResolutionStrategy",
                        encryption_strategy="encryptionStrategy",
                        kms_key_arn="kmsKeyArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__62c5ba476b7b03a0e2dd22bca8f2c17a33e42db3e21d261e03bd3755258abbb7)
                check_type(argname="argument backup_configuration", value=backup_configuration, expected_type=type_hints["backup_configuration"])
                check_type(argname="argument logs_encryption_configuration", value=logs_encryption_configuration, expected_type=type_hints["logs_encryption_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if backup_configuration is not None:
                self._values["backup_configuration"] = backup_configuration
            if logs_encryption_configuration is not None:
                self._values["logs_encryption_configuration"] = logs_encryption_configuration

        @builtins.property
        def backup_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOrganizationCentralizationRulePropsMixin.LogsBackupConfigurationProperty"]]:
            '''Configuration defining the backup region and an optional KMS key for the backup destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-organizationcentralizationrule-destinationlogsconfiguration.html#cfn-observabilityadmin-organizationcentralizationrule-destinationlogsconfiguration-backupconfiguration
            '''
            result = self._values.get("backup_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOrganizationCentralizationRulePropsMixin.LogsBackupConfigurationProperty"]], result)

        @builtins.property
        def logs_encryption_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOrganizationCentralizationRulePropsMixin.LogsEncryptionConfigurationProperty"]]:
            '''The encryption configuration for centralization destination log groups.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-organizationcentralizationrule-destinationlogsconfiguration.html#cfn-observabilityadmin-organizationcentralizationrule-destinationlogsconfiguration-logsencryptionconfiguration
            '''
            result = self._values.get("logs_encryption_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOrganizationCentralizationRulePropsMixin.LogsEncryptionConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DestinationLogsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_observabilityadmin.mixins.CfnOrganizationCentralizationRulePropsMixin.LogsBackupConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"kms_key_arn": "kmsKeyArn", "region": "region"},
    )
    class LogsBackupConfigurationProperty:
        def __init__(
            self,
            *,
            kms_key_arn: typing.Optional[builtins.str] = None,
            region: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration for backing up centralized log data to a secondary region.

            :param kms_key_arn: KMS Key ARN belonging to the primary destination account and backup region, to encrypt newly created central log groups in the backup destination.
            :param region: Logs specific backup destination region within the primary destination account to which log data should be centralized.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-organizationcentralizationrule-logsbackupconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_observabilityadmin import mixins as observabilityadmin_mixins
                
                logs_backup_configuration_property = observabilityadmin_mixins.CfnOrganizationCentralizationRulePropsMixin.LogsBackupConfigurationProperty(
                    kms_key_arn="kmsKeyArn",
                    region="region"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__48f392ca61db0ece40aedc750490cec67420f62313bb4db5194b426c3affc678)
                check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
                check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kms_key_arn is not None:
                self._values["kms_key_arn"] = kms_key_arn
            if region is not None:
                self._values["region"] = region

        @builtins.property
        def kms_key_arn(self) -> typing.Optional[builtins.str]:
            '''KMS Key ARN belonging to the primary destination account and backup region, to encrypt newly created central log groups in the backup destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-organizationcentralizationrule-logsbackupconfiguration.html#cfn-observabilityadmin-organizationcentralizationrule-logsbackupconfiguration-kmskeyarn
            '''
            result = self._values.get("kms_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def region(self) -> typing.Optional[builtins.str]:
            '''Logs specific backup destination region within the primary destination account to which log data should be centralized.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-organizationcentralizationrule-logsbackupconfiguration.html#cfn-observabilityadmin-organizationcentralizationrule-logsbackupconfiguration-region
            '''
            result = self._values.get("region")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogsBackupConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_observabilityadmin.mixins.CfnOrganizationCentralizationRulePropsMixin.LogsEncryptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "encryption_conflict_resolution_strategy": "encryptionConflictResolutionStrategy",
            "encryption_strategy": "encryptionStrategy",
            "kms_key_arn": "kmsKeyArn",
        },
    )
    class LogsEncryptionConfigurationProperty:
        def __init__(
            self,
            *,
            encryption_conflict_resolution_strategy: typing.Optional[builtins.str] = None,
            encryption_strategy: typing.Optional[builtins.str] = None,
            kms_key_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration for encrypting centralized log groups.

            This configuration is only applied to destination log groups for which the corresponding source log groups are encrypted using Customer Managed KMS Keys.

            :param encryption_conflict_resolution_strategy: Conflict resolution strategy for centralization if the encryption strategy is set to CUSTOMER_MANAGED and the destination log group is encrypted with an AWS_OWNED KMS Key. ALLOW lets centralization go through while SKIP prevents centralization into the destination log group.
            :param encryption_strategy: Configuration that determines the encryption strategy of the destination log groups. CUSTOMER_MANAGED uses the configured KmsKeyArn to encrypt newly created destination log groups.
            :param kms_key_arn: KMS Key ARN belonging to the primary destination account and region, to encrypt newly created central log groups in the primary destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-organizationcentralizationrule-logsencryptionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_observabilityadmin import mixins as observabilityadmin_mixins
                
                logs_encryption_configuration_property = observabilityadmin_mixins.CfnOrganizationCentralizationRulePropsMixin.LogsEncryptionConfigurationProperty(
                    encryption_conflict_resolution_strategy="encryptionConflictResolutionStrategy",
                    encryption_strategy="encryptionStrategy",
                    kms_key_arn="kmsKeyArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4af2121f84a79b891422c6ca4148fa507b8c9739f568532bc7676bbcd1a1e2fe)
                check_type(argname="argument encryption_conflict_resolution_strategy", value=encryption_conflict_resolution_strategy, expected_type=type_hints["encryption_conflict_resolution_strategy"])
                check_type(argname="argument encryption_strategy", value=encryption_strategy, expected_type=type_hints["encryption_strategy"])
                check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encryption_conflict_resolution_strategy is not None:
                self._values["encryption_conflict_resolution_strategy"] = encryption_conflict_resolution_strategy
            if encryption_strategy is not None:
                self._values["encryption_strategy"] = encryption_strategy
            if kms_key_arn is not None:
                self._values["kms_key_arn"] = kms_key_arn

        @builtins.property
        def encryption_conflict_resolution_strategy(
            self,
        ) -> typing.Optional[builtins.str]:
            '''Conflict resolution strategy for centralization if the encryption strategy is set to CUSTOMER_MANAGED and the destination log group is encrypted with an AWS_OWNED KMS Key.

            ALLOW lets centralization go through while SKIP prevents centralization into the destination log group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-organizationcentralizationrule-logsencryptionconfiguration.html#cfn-observabilityadmin-organizationcentralizationrule-logsencryptionconfiguration-encryptionconflictresolutionstrategy
            '''
            result = self._values.get("encryption_conflict_resolution_strategy")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def encryption_strategy(self) -> typing.Optional[builtins.str]:
            '''Configuration that determines the encryption strategy of the destination log groups.

            CUSTOMER_MANAGED uses the configured KmsKeyArn to encrypt newly created destination log groups.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-organizationcentralizationrule-logsencryptionconfiguration.html#cfn-observabilityadmin-organizationcentralizationrule-logsencryptionconfiguration-encryptionstrategy
            '''
            result = self._values.get("encryption_strategy")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def kms_key_arn(self) -> typing.Optional[builtins.str]:
            '''KMS Key ARN belonging to the primary destination account and region, to encrypt newly created central log groups in the primary destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-organizationcentralizationrule-logsencryptionconfiguration.html#cfn-observabilityadmin-organizationcentralizationrule-logsencryptionconfiguration-kmskeyarn
            '''
            result = self._values.get("kms_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogsEncryptionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_observabilityadmin.mixins.CfnOrganizationCentralizationRulePropsMixin.SourceLogsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "encrypted_log_group_strategy": "encryptedLogGroupStrategy",
            "log_group_selection_criteria": "logGroupSelectionCriteria",
        },
    )
    class SourceLogsConfigurationProperty:
        def __init__(
            self,
            *,
            encrypted_log_group_strategy: typing.Optional[builtins.str] = None,
            log_group_selection_criteria: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration for selecting and handling source log groups for centralization.

            :param encrypted_log_group_strategy: A strategy determining whether to centralize source log groups that are encrypted with customer managed KMS keys (CMK). ALLOW will consider CMK encrypted source log groups for centralization while SKIP will skip CMK encrypted source log groups from centralization.
            :param log_group_selection_criteria: The selection criteria that specifies which source log groups to centralize. The selection criteria uses the same format as OAM link filters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-organizationcentralizationrule-sourcelogsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_observabilityadmin import mixins as observabilityadmin_mixins
                
                source_logs_configuration_property = observabilityadmin_mixins.CfnOrganizationCentralizationRulePropsMixin.SourceLogsConfigurationProperty(
                    encrypted_log_group_strategy="encryptedLogGroupStrategy",
                    log_group_selection_criteria="logGroupSelectionCriteria"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2189fab5fc6f36ac4898822304ae1b38fa0852872791d45876a1c3bfd2b550e8)
                check_type(argname="argument encrypted_log_group_strategy", value=encrypted_log_group_strategy, expected_type=type_hints["encrypted_log_group_strategy"])
                check_type(argname="argument log_group_selection_criteria", value=log_group_selection_criteria, expected_type=type_hints["log_group_selection_criteria"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encrypted_log_group_strategy is not None:
                self._values["encrypted_log_group_strategy"] = encrypted_log_group_strategy
            if log_group_selection_criteria is not None:
                self._values["log_group_selection_criteria"] = log_group_selection_criteria

        @builtins.property
        def encrypted_log_group_strategy(self) -> typing.Optional[builtins.str]:
            '''A strategy determining whether to centralize source log groups that are encrypted with customer managed KMS keys (CMK).

            ALLOW will consider CMK encrypted source log groups for centralization while SKIP will skip CMK encrypted source log groups from centralization.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-organizationcentralizationrule-sourcelogsconfiguration.html#cfn-observabilityadmin-organizationcentralizationrule-sourcelogsconfiguration-encryptedloggroupstrategy
            '''
            result = self._values.get("encrypted_log_group_strategy")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_group_selection_criteria(self) -> typing.Optional[builtins.str]:
            '''The selection criteria that specifies which source log groups to centralize.

            The selection criteria uses the same format as OAM link filters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-organizationcentralizationrule-sourcelogsconfiguration.html#cfn-observabilityadmin-organizationcentralizationrule-sourcelogsconfiguration-loggroupselectioncriteria
            '''
            result = self._values.get("log_group_selection_criteria")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceLogsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_observabilityadmin.mixins.CfnOrganizationTelemetryRuleMixinProps",
    jsii_struct_bases=[],
    name_mapping={"rule": "rule", "rule_name": "ruleName", "tags": "tags"},
)
class CfnOrganizationTelemetryRuleMixinProps:
    def __init__(
        self,
        *,
        rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOrganizationTelemetryRulePropsMixin.TelemetryRuleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnOrganizationTelemetryRulePropsMixin.

        :param rule: The name of the organization telemetry rule.
        :param rule_name: The name of the organization centralization rule.
        :param tags: Lists all tags attached to the specified telemetry rule resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-observabilityadmin-organizationtelemetryrule.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_observabilityadmin import mixins as observabilityadmin_mixins
            
            cfn_organization_telemetry_rule_mixin_props = observabilityadmin_mixins.CfnOrganizationTelemetryRuleMixinProps(
                rule=observabilityadmin_mixins.CfnOrganizationTelemetryRulePropsMixin.TelemetryRuleProperty(
                    destination_configuration=observabilityadmin_mixins.CfnOrganizationTelemetryRulePropsMixin.TelemetryDestinationConfigurationProperty(
                        destination_pattern="destinationPattern",
                        destination_type="destinationType",
                        retention_in_days=123,
                        vpc_flow_log_parameters=observabilityadmin_mixins.CfnOrganizationTelemetryRulePropsMixin.VPCFlowLogParametersProperty(
                            log_format="logFormat",
                            max_aggregation_interval=123,
                            traffic_type="trafficType"
                        )
                    ),
                    resource_type="resourceType",
                    scope="scope",
                    selection_criteria="selectionCriteria",
                    telemetry_type="telemetryType"
                ),
                rule_name="ruleName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a1acec9dba368ed19d2bcc8bcabdaa2d58c2298bc6a5af321537e2778ad29c8)
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
            check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if rule is not None:
            self._values["rule"] = rule
        if rule_name is not None:
            self._values["rule_name"] = rule_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def rule(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOrganizationTelemetryRulePropsMixin.TelemetryRuleProperty"]]:
        '''The name of the organization telemetry rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-observabilityadmin-organizationtelemetryrule.html#cfn-observabilityadmin-organizationtelemetryrule-rule
        '''
        result = self._values.get("rule")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOrganizationTelemetryRulePropsMixin.TelemetryRuleProperty"]], result)

    @builtins.property
    def rule_name(self) -> typing.Optional[builtins.str]:
        '''The name of the organization centralization rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-observabilityadmin-organizationtelemetryrule.html#cfn-observabilityadmin-organizationtelemetryrule-rulename
        '''
        result = self._values.get("rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Lists all tags attached to the specified telemetry rule resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-observabilityadmin-organizationtelemetryrule.html#cfn-observabilityadmin-organizationtelemetryrule-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnOrganizationTelemetryRuleMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnOrganizationTelemetryRulePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_observabilityadmin.mixins.CfnOrganizationTelemetryRulePropsMixin",
):
    '''Retrieves the details of a specific organization centralization rule.

    This operation can only be called by the organization's management account or a delegated administrator account.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-observabilityadmin-organizationtelemetryrule.html
    :cloudformationResource: AWS::ObservabilityAdmin::OrganizationTelemetryRule
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_observabilityadmin import mixins as observabilityadmin_mixins
        
        cfn_organization_telemetry_rule_props_mixin = observabilityadmin_mixins.CfnOrganizationTelemetryRulePropsMixin(observabilityadmin_mixins.CfnOrganizationTelemetryRuleMixinProps(
            rule=observabilityadmin_mixins.CfnOrganizationTelemetryRulePropsMixin.TelemetryRuleProperty(
                destination_configuration=observabilityadmin_mixins.CfnOrganizationTelemetryRulePropsMixin.TelemetryDestinationConfigurationProperty(
                    destination_pattern="destinationPattern",
                    destination_type="destinationType",
                    retention_in_days=123,
                    vpc_flow_log_parameters=observabilityadmin_mixins.CfnOrganizationTelemetryRulePropsMixin.VPCFlowLogParametersProperty(
                        log_format="logFormat",
                        max_aggregation_interval=123,
                        traffic_type="trafficType"
                    )
                ),
                resource_type="resourceType",
                scope="scope",
                selection_criteria="selectionCriteria",
                telemetry_type="telemetryType"
            ),
            rule_name="ruleName",
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
        props: typing.Union[CfnOrganizationTelemetryRuleMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ObservabilityAdmin::OrganizationTelemetryRule``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55ed612c92f8c36eb825f453891f36c8e15a55233b53c73df248ec685ad0590a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f59046f5a873bc5970849188c64584c0d42e2ecb442ec727e5e8cb65f656a20)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afa44fc6e808f884af9d1bbf40f5eda0e6c734dca626e41f8d89ac3dba9018e6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnOrganizationTelemetryRuleMixinProps:
        return typing.cast(CfnOrganizationTelemetryRuleMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_observabilityadmin.mixins.CfnOrganizationTelemetryRulePropsMixin.TelemetryDestinationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_pattern": "destinationPattern",
            "destination_type": "destinationType",
            "retention_in_days": "retentionInDays",
            "vpc_flow_log_parameters": "vpcFlowLogParameters",
        },
    )
    class TelemetryDestinationConfigurationProperty:
        def __init__(
            self,
            *,
            destination_pattern: typing.Optional[builtins.str] = None,
            destination_type: typing.Optional[builtins.str] = None,
            retention_in_days: typing.Optional[jsii.Number] = None,
            vpc_flow_log_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOrganizationTelemetryRulePropsMixin.VPCFlowLogParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Configuration specifying where and how telemetry data should be delivered for AWS resources.

            :param destination_pattern: The pattern used to generate the destination path or name, supporting macros like and .
            :param destination_type: The type of destination for the telemetry data (e.g., "Amazon CloudWatch Logs", "S3").
            :param retention_in_days: The number of days to retain the telemetry data in the destination.
            :param vpc_flow_log_parameters: Configuration parameters specific to VPC Flow Logs when VPC is the resource type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-organizationtelemetryrule-telemetrydestinationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_observabilityadmin import mixins as observabilityadmin_mixins
                
                telemetry_destination_configuration_property = observabilityadmin_mixins.CfnOrganizationTelemetryRulePropsMixin.TelemetryDestinationConfigurationProperty(
                    destination_pattern="destinationPattern",
                    destination_type="destinationType",
                    retention_in_days=123,
                    vpc_flow_log_parameters=observabilityadmin_mixins.CfnOrganizationTelemetryRulePropsMixin.VPCFlowLogParametersProperty(
                        log_format="logFormat",
                        max_aggregation_interval=123,
                        traffic_type="trafficType"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0aad96fd4765150ac739ae57bb0a5f2fc0da8b91213df52eaa07bc558b32dec3)
                check_type(argname="argument destination_pattern", value=destination_pattern, expected_type=type_hints["destination_pattern"])
                check_type(argname="argument destination_type", value=destination_type, expected_type=type_hints["destination_type"])
                check_type(argname="argument retention_in_days", value=retention_in_days, expected_type=type_hints["retention_in_days"])
                check_type(argname="argument vpc_flow_log_parameters", value=vpc_flow_log_parameters, expected_type=type_hints["vpc_flow_log_parameters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination_pattern is not None:
                self._values["destination_pattern"] = destination_pattern
            if destination_type is not None:
                self._values["destination_type"] = destination_type
            if retention_in_days is not None:
                self._values["retention_in_days"] = retention_in_days
            if vpc_flow_log_parameters is not None:
                self._values["vpc_flow_log_parameters"] = vpc_flow_log_parameters

        @builtins.property
        def destination_pattern(self) -> typing.Optional[builtins.str]:
            '''The pattern used to generate the destination path or name, supporting macros like  and .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-organizationtelemetryrule-telemetrydestinationconfiguration.html#cfn-observabilityadmin-organizationtelemetryrule-telemetrydestinationconfiguration-destinationpattern
            '''
            result = self._values.get("destination_pattern")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def destination_type(self) -> typing.Optional[builtins.str]:
            '''The type of destination for the telemetry data (e.g., "Amazon CloudWatch Logs", "S3").

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-organizationtelemetryrule-telemetrydestinationconfiguration.html#cfn-observabilityadmin-organizationtelemetryrule-telemetrydestinationconfiguration-destinationtype
            '''
            result = self._values.get("destination_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def retention_in_days(self) -> typing.Optional[jsii.Number]:
            '''The number of days to retain the telemetry data in the destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-organizationtelemetryrule-telemetrydestinationconfiguration.html#cfn-observabilityadmin-organizationtelemetryrule-telemetrydestinationconfiguration-retentionindays
            '''
            result = self._values.get("retention_in_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def vpc_flow_log_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOrganizationTelemetryRulePropsMixin.VPCFlowLogParametersProperty"]]:
            '''Configuration parameters specific to VPC Flow Logs when VPC is the resource type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-organizationtelemetryrule-telemetrydestinationconfiguration.html#cfn-observabilityadmin-organizationtelemetryrule-telemetrydestinationconfiguration-vpcflowlogparameters
            '''
            result = self._values.get("vpc_flow_log_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOrganizationTelemetryRulePropsMixin.VPCFlowLogParametersProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TelemetryDestinationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_observabilityadmin.mixins.CfnOrganizationTelemetryRulePropsMixin.TelemetryRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_configuration": "destinationConfiguration",
            "resource_type": "resourceType",
            "scope": "scope",
            "selection_criteria": "selectionCriteria",
            "telemetry_type": "telemetryType",
        },
    )
    class TelemetryRuleProperty:
        def __init__(
            self,
            *,
            destination_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOrganizationTelemetryRulePropsMixin.TelemetryDestinationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            resource_type: typing.Optional[builtins.str] = None,
            scope: typing.Optional[builtins.str] = None,
            selection_criteria: typing.Optional[builtins.str] = None,
            telemetry_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines how telemetry should be configured for specific AWS resources.

            :param destination_configuration: Configuration specifying where and how the telemetry data should be delivered.
            :param resource_type: The type of AWS resource to configure telemetry for (e.g., "AWS::EC2::VPC").
            :param scope: The organizational scope to which the rule applies, specified using accounts or organizational units.
            :param selection_criteria: Criteria for selecting which resources the rule applies to, such as resource tags.
            :param telemetry_type: The type of telemetry to collect (Logs, Metrics, or Traces).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-organizationtelemetryrule-telemetryrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_observabilityadmin import mixins as observabilityadmin_mixins
                
                telemetry_rule_property = observabilityadmin_mixins.CfnOrganizationTelemetryRulePropsMixin.TelemetryRuleProperty(
                    destination_configuration=observabilityadmin_mixins.CfnOrganizationTelemetryRulePropsMixin.TelemetryDestinationConfigurationProperty(
                        destination_pattern="destinationPattern",
                        destination_type="destinationType",
                        retention_in_days=123,
                        vpc_flow_log_parameters=observabilityadmin_mixins.CfnOrganizationTelemetryRulePropsMixin.VPCFlowLogParametersProperty(
                            log_format="logFormat",
                            max_aggregation_interval=123,
                            traffic_type="trafficType"
                        )
                    ),
                    resource_type="resourceType",
                    scope="scope",
                    selection_criteria="selectionCriteria",
                    telemetry_type="telemetryType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d963398c2186e5f1789c1583caf09b321373e83e19a74bfd3683c30f2ec6a35a)
                check_type(argname="argument destination_configuration", value=destination_configuration, expected_type=type_hints["destination_configuration"])
                check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
                check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
                check_type(argname="argument selection_criteria", value=selection_criteria, expected_type=type_hints["selection_criteria"])
                check_type(argname="argument telemetry_type", value=telemetry_type, expected_type=type_hints["telemetry_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination_configuration is not None:
                self._values["destination_configuration"] = destination_configuration
            if resource_type is not None:
                self._values["resource_type"] = resource_type
            if scope is not None:
                self._values["scope"] = scope
            if selection_criteria is not None:
                self._values["selection_criteria"] = selection_criteria
            if telemetry_type is not None:
                self._values["telemetry_type"] = telemetry_type

        @builtins.property
        def destination_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOrganizationTelemetryRulePropsMixin.TelemetryDestinationConfigurationProperty"]]:
            '''Configuration specifying where and how the telemetry data should be delivered.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-organizationtelemetryrule-telemetryrule.html#cfn-observabilityadmin-organizationtelemetryrule-telemetryrule-destinationconfiguration
            '''
            result = self._values.get("destination_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOrganizationTelemetryRulePropsMixin.TelemetryDestinationConfigurationProperty"]], result)

        @builtins.property
        def resource_type(self) -> typing.Optional[builtins.str]:
            '''The type of AWS resource to configure telemetry for (e.g., "AWS::EC2::VPC").

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-organizationtelemetryrule-telemetryrule.html#cfn-observabilityadmin-organizationtelemetryrule-telemetryrule-resourcetype
            '''
            result = self._values.get("resource_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def scope(self) -> typing.Optional[builtins.str]:
            '''The organizational scope to which the rule applies, specified using accounts or organizational units.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-organizationtelemetryrule-telemetryrule.html#cfn-observabilityadmin-organizationtelemetryrule-telemetryrule-scope
            '''
            result = self._values.get("scope")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def selection_criteria(self) -> typing.Optional[builtins.str]:
            '''Criteria for selecting which resources the rule applies to, such as resource tags.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-organizationtelemetryrule-telemetryrule.html#cfn-observabilityadmin-organizationtelemetryrule-telemetryrule-selectioncriteria
            '''
            result = self._values.get("selection_criteria")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def telemetry_type(self) -> typing.Optional[builtins.str]:
            '''The type of telemetry to collect (Logs, Metrics, or Traces).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-organizationtelemetryrule-telemetryrule.html#cfn-observabilityadmin-organizationtelemetryrule-telemetryrule-telemetrytype
            '''
            result = self._values.get("telemetry_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TelemetryRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_observabilityadmin.mixins.CfnOrganizationTelemetryRulePropsMixin.VPCFlowLogParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "log_format": "logFormat",
            "max_aggregation_interval": "maxAggregationInterval",
            "traffic_type": "trafficType",
        },
    )
    class VPCFlowLogParametersProperty:
        def __init__(
            self,
            *,
            log_format: typing.Optional[builtins.str] = None,
            max_aggregation_interval: typing.Optional[jsii.Number] = None,
            traffic_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration parameters specific to VPC Flow Logs.

            :param log_format: The format in which VPC Flow Log entries should be logged.
            :param max_aggregation_interval: The maximum interval in seconds between the capture of flow log records.
            :param traffic_type: The type of traffic to log (ACCEPT, REJECT, or ALL).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-organizationtelemetryrule-vpcflowlogparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_observabilityadmin import mixins as observabilityadmin_mixins
                
                v_pCFlow_log_parameters_property = observabilityadmin_mixins.CfnOrganizationTelemetryRulePropsMixin.VPCFlowLogParametersProperty(
                    log_format="logFormat",
                    max_aggregation_interval=123,
                    traffic_type="trafficType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__800d32ba27dda96915b16198d35c7226c11dded78a8a76197a149d6f37c3097c)
                check_type(argname="argument log_format", value=log_format, expected_type=type_hints["log_format"])
                check_type(argname="argument max_aggregation_interval", value=max_aggregation_interval, expected_type=type_hints["max_aggregation_interval"])
                check_type(argname="argument traffic_type", value=traffic_type, expected_type=type_hints["traffic_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if log_format is not None:
                self._values["log_format"] = log_format
            if max_aggregation_interval is not None:
                self._values["max_aggregation_interval"] = max_aggregation_interval
            if traffic_type is not None:
                self._values["traffic_type"] = traffic_type

        @builtins.property
        def log_format(self) -> typing.Optional[builtins.str]:
            '''The format in which VPC Flow Log entries should be logged.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-organizationtelemetryrule-vpcflowlogparameters.html#cfn-observabilityadmin-organizationtelemetryrule-vpcflowlogparameters-logformat
            '''
            result = self._values.get("log_format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def max_aggregation_interval(self) -> typing.Optional[jsii.Number]:
            '''The maximum interval in seconds between the capture of flow log records.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-organizationtelemetryrule-vpcflowlogparameters.html#cfn-observabilityadmin-organizationtelemetryrule-vpcflowlogparameters-maxaggregationinterval
            '''
            result = self._values.get("max_aggregation_interval")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def traffic_type(self) -> typing.Optional[builtins.str]:
            '''The type of traffic to log (ACCEPT, REJECT, or ALL).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-organizationtelemetryrule-vpcflowlogparameters.html#cfn-observabilityadmin-organizationtelemetryrule-vpcflowlogparameters-traffictype
            '''
            result = self._values.get("traffic_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VPCFlowLogParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_observabilityadmin.mixins.CfnS3TableIntegrationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "encryption": "encryption",
        "log_sources": "logSources",
        "role_arn": "roleArn",
        "tags": "tags",
    },
)
class CfnS3TableIntegrationMixinProps:
    def __init__(
        self,
        *,
        encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnS3TableIntegrationPropsMixin.EncryptionConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        log_sources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnS3TableIntegrationPropsMixin.LogSourceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnS3TableIntegrationPropsMixin.

        :param encryption: Encryption configuration for the S3 Table Integration.
        :param log_sources: The CloudWatch Logs data sources to associate with the S3 Table Integration.
        :param role_arn: The ARN of the role used to access the S3 Table Integration.
        :param tags: An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-observabilityadmin-s3tableintegration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_observabilityadmin import mixins as observabilityadmin_mixins
            
            cfn_s3_table_integration_mixin_props = observabilityadmin_mixins.CfnS3TableIntegrationMixinProps(
                encryption=observabilityadmin_mixins.CfnS3TableIntegrationPropsMixin.EncryptionConfigProperty(
                    kms_key_arn="kmsKeyArn",
                    sse_algorithm="sseAlgorithm"
                ),
                log_sources=[observabilityadmin_mixins.CfnS3TableIntegrationPropsMixin.LogSourceProperty(
                    identifier="identifier",
                    name="name",
                    type="type"
                )],
                role_arn="roleArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89f0602bcddda493541aa5c50f1dca52fca6b6b1db0d092329afe2e25abf932f)
            check_type(argname="argument encryption", value=encryption, expected_type=type_hints["encryption"])
            check_type(argname="argument log_sources", value=log_sources, expected_type=type_hints["log_sources"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if encryption is not None:
            self._values["encryption"] = encryption
        if log_sources is not None:
            self._values["log_sources"] = log_sources
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def encryption(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnS3TableIntegrationPropsMixin.EncryptionConfigProperty"]]:
        '''Encryption configuration for the S3 Table Integration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-observabilityadmin-s3tableintegration.html#cfn-observabilityadmin-s3tableintegration-encryption
        '''
        result = self._values.get("encryption")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnS3TableIntegrationPropsMixin.EncryptionConfigProperty"]], result)

    @builtins.property
    def log_sources(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnS3TableIntegrationPropsMixin.LogSourceProperty"]]]]:
        '''The CloudWatch Logs data sources to associate with the S3 Table Integration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-observabilityadmin-s3tableintegration.html#cfn-observabilityadmin-s3tableintegration-logsources
        '''
        result = self._values.get("log_sources")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnS3TableIntegrationPropsMixin.LogSourceProperty"]]]], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the role used to access the S3 Table Integration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-observabilityadmin-s3tableintegration.html#cfn-observabilityadmin-s3tableintegration-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-observabilityadmin-s3tableintegration.html#cfn-observabilityadmin-s3tableintegration-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnS3TableIntegrationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnS3TableIntegrationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_observabilityadmin.mixins.CfnS3TableIntegrationPropsMixin",
):
    '''Resource Type definition for a CloudWatch Observability Admin S3 Table Integration.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-observabilityadmin-s3tableintegration.html
    :cloudformationResource: AWS::ObservabilityAdmin::S3TableIntegration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_observabilityadmin import mixins as observabilityadmin_mixins
        
        cfn_s3_table_integration_props_mixin = observabilityadmin_mixins.CfnS3TableIntegrationPropsMixin(observabilityadmin_mixins.CfnS3TableIntegrationMixinProps(
            encryption=observabilityadmin_mixins.CfnS3TableIntegrationPropsMixin.EncryptionConfigProperty(
                kms_key_arn="kmsKeyArn",
                sse_algorithm="sseAlgorithm"
            ),
            log_sources=[observabilityadmin_mixins.CfnS3TableIntegrationPropsMixin.LogSourceProperty(
                identifier="identifier",
                name="name",
                type="type"
            )],
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
        props: typing.Union[CfnS3TableIntegrationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ObservabilityAdmin::S3TableIntegration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ecefc94a5d14d6f82bd29573934ddd9402892663a6628b5f5c9f6b93ce165c3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__590b3dc3305d44cd252dbe2d17502f17f3902a7463be507e9fc4efe68ab48d99)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f6614d16b6ac1ca40575a26878a09fc7fdd8e9f0a9e59a0ec3dc3b234862562)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnS3TableIntegrationMixinProps:
        return typing.cast(CfnS3TableIntegrationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_observabilityadmin.mixins.CfnS3TableIntegrationPropsMixin.EncryptionConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"kms_key_arn": "kmsKeyArn", "sse_algorithm": "sseAlgorithm"},
    )
    class EncryptionConfigProperty:
        def __init__(
            self,
            *,
            kms_key_arn: typing.Optional[builtins.str] = None,
            sse_algorithm: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Encryption configuration for the S3 Table Integration.

            :param kms_key_arn: The ARN of the KMS key used to encrypt the S3 Table Integration.
            :param sse_algorithm: The server-side encryption algorithm used to encrypt the S3 Table(s) data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-s3tableintegration-encryptionconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_observabilityadmin import mixins as observabilityadmin_mixins
                
                encryption_config_property = observabilityadmin_mixins.CfnS3TableIntegrationPropsMixin.EncryptionConfigProperty(
                    kms_key_arn="kmsKeyArn",
                    sse_algorithm="sseAlgorithm"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5c224dda3e14b265c3d0033c46e331e7c3e0784f4c72e9a57901495a35d6fd73)
                check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
                check_type(argname="argument sse_algorithm", value=sse_algorithm, expected_type=type_hints["sse_algorithm"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kms_key_arn is not None:
                self._values["kms_key_arn"] = kms_key_arn
            if sse_algorithm is not None:
                self._values["sse_algorithm"] = sse_algorithm

        @builtins.property
        def kms_key_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the KMS key used to encrypt the S3 Table Integration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-s3tableintegration-encryptionconfig.html#cfn-observabilityadmin-s3tableintegration-encryptionconfig-kmskeyarn
            '''
            result = self._values.get("kms_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sse_algorithm(self) -> typing.Optional[builtins.str]:
            '''The server-side encryption algorithm used to encrypt the S3 Table(s) data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-s3tableintegration-encryptionconfig.html#cfn-observabilityadmin-s3tableintegration-encryptionconfig-ssealgorithm
            '''
            result = self._values.get("sse_algorithm")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_observabilityadmin.mixins.CfnS3TableIntegrationPropsMixin.LogSourceProperty",
        jsii_struct_bases=[],
        name_mapping={"identifier": "identifier", "name": "name", "type": "type"},
    )
    class LogSourceProperty:
        def __init__(
            self,
            *,
            identifier: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''CloudWatch Logs data source to associate with the S3 Table Integration.

            :param identifier: The ID of the CloudWatch Logs data source association.
            :param name: The name of the CloudWatch Logs data source.
            :param type: The type of the CloudWatch Logs data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-s3tableintegration-logsource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_observabilityadmin import mixins as observabilityadmin_mixins
                
                log_source_property = observabilityadmin_mixins.CfnS3TableIntegrationPropsMixin.LogSourceProperty(
                    identifier="identifier",
                    name="name",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__55a1b8dc81413f99d4f97d385779f9ee673c49fade884c18f97de11adf123b86)
                check_type(argname="argument identifier", value=identifier, expected_type=type_hints["identifier"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if identifier is not None:
                self._values["identifier"] = identifier
            if name is not None:
                self._values["name"] = name
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def identifier(self) -> typing.Optional[builtins.str]:
            '''The ID of the CloudWatch Logs data source association.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-s3tableintegration-logsource.html#cfn-observabilityadmin-s3tableintegration-logsource-identifier
            '''
            result = self._values.get("identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the CloudWatch Logs data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-s3tableintegration-logsource.html#cfn-observabilityadmin-s3tableintegration-logsource-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of the CloudWatch Logs data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-s3tableintegration-logsource.html#cfn-observabilityadmin-s3tableintegration-logsource-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_observabilityadmin.mixins.CfnTelemetryPipelinesMixinProps",
    jsii_struct_bases=[],
    name_mapping={"configuration": "configuration", "name": "name", "tags": "tags"},
)
class CfnTelemetryPipelinesMixinProps:
    def __init__(
        self,
        *,
        configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTelemetryPipelinesPropsMixin.TelemetryPipelineConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnTelemetryPipelinesPropsMixin.

        :param configuration: 
        :param name: 
        :param tags: An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-observabilityadmin-telemetrypipelines.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_observabilityadmin import mixins as observabilityadmin_mixins
            
            cfn_telemetry_pipelines_mixin_props = observabilityadmin_mixins.CfnTelemetryPipelinesMixinProps(
                configuration=observabilityadmin_mixins.CfnTelemetryPipelinesPropsMixin.TelemetryPipelineConfigurationProperty(
                    body="body"
                ),
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e57e930d90900d811e8510de229c3cf9635373026652d762a7053411ae50b4ee)
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if configuration is not None:
            self._values["configuration"] = configuration
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTelemetryPipelinesPropsMixin.TelemetryPipelineConfigurationProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-observabilityadmin-telemetrypipelines.html#cfn-observabilityadmin-telemetrypipelines-configuration
        '''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTelemetryPipelinesPropsMixin.TelemetryPipelineConfigurationProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-observabilityadmin-telemetrypipelines.html#cfn-observabilityadmin-telemetrypipelines-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-observabilityadmin-telemetrypipelines.html#cfn-observabilityadmin-telemetrypipelines-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTelemetryPipelinesMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnTelemetryPipelinesPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_observabilityadmin.mixins.CfnTelemetryPipelinesPropsMixin",
):
    '''Resource Type definition for AWS::ObservabilityAdmin::TelemetryPipelines.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-observabilityadmin-telemetrypipelines.html
    :cloudformationResource: AWS::ObservabilityAdmin::TelemetryPipelines
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_observabilityadmin import mixins as observabilityadmin_mixins
        
        cfn_telemetry_pipelines_props_mixin = observabilityadmin_mixins.CfnTelemetryPipelinesPropsMixin(observabilityadmin_mixins.CfnTelemetryPipelinesMixinProps(
            configuration=observabilityadmin_mixins.CfnTelemetryPipelinesPropsMixin.TelemetryPipelineConfigurationProperty(
                body="body"
            ),
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
        props: typing.Union[CfnTelemetryPipelinesMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ObservabilityAdmin::TelemetryPipelines``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90597d794795765813e020b415e8d167f4495b35d274efec2aeacdbc04f458be)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4dee45317d853c4c0cf9a53dfe0f82037b2221791c55604d9902563d83c4d4dc)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaac31a163b9df7c4a7924a9d5ffa358c99cc220f8594921b86633a1a2f6046f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTelemetryPipelinesMixinProps:
        return typing.cast(CfnTelemetryPipelinesMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_observabilityadmin.mixins.CfnTelemetryPipelinesPropsMixin.TelemetryPipelineConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"body": "body"},
    )
    class TelemetryPipelineConfigurationProperty:
        def __init__(self, *, body: typing.Optional[builtins.str] = None) -> None:
            '''
            :param body: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-telemetrypipelines-telemetrypipelineconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_observabilityadmin import mixins as observabilityadmin_mixins
                
                telemetry_pipeline_configuration_property = observabilityadmin_mixins.CfnTelemetryPipelinesPropsMixin.TelemetryPipelineConfigurationProperty(
                    body="body"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4a563a720c1f6f5e49098b737e2c1f6182a1919592f63854fc5ae80358d4eb23)
                check_type(argname="argument body", value=body, expected_type=type_hints["body"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if body is not None:
                self._values["body"] = body

        @builtins.property
        def body(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-telemetrypipelines-telemetrypipelineconfiguration.html#cfn-observabilityadmin-telemetrypipelines-telemetrypipelineconfiguration-body
            '''
            result = self._values.get("body")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TelemetryPipelineConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_observabilityadmin.mixins.CfnTelemetryPipelinesPropsMixin.TelemetryPipelineProperty",
        jsii_struct_bases=[],
        name_mapping={
            "arn": "arn",
            "configuration": "configuration",
            "created_time_stamp": "createdTimeStamp",
            "last_update_time_stamp": "lastUpdateTimeStamp",
            "name": "name",
            "status": "status",
            "status_reason": "statusReason",
            "tags": "tags",
        },
    )
    class TelemetryPipelineProperty:
        def __init__(
            self,
            *,
            arn: typing.Optional[builtins.str] = None,
            configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTelemetryPipelinesPropsMixin.TelemetryPipelineConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            created_time_stamp: typing.Optional[jsii.Number] = None,
            last_update_time_stamp: typing.Optional[jsii.Number] = None,
            name: typing.Optional[builtins.str] = None,
            status: typing.Optional[builtins.str] = None,
            status_reason: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTelemetryPipelinesPropsMixin.TelemetryPipelineStatusReasonProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param arn: 
            :param configuration: 
            :param created_time_stamp: 
            :param last_update_time_stamp: 
            :param name: 
            :param status: 
            :param status_reason: 
            :param tags: An array of key-value pairs to apply to this resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-telemetrypipelines-telemetrypipeline.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_observabilityadmin import mixins as observabilityadmin_mixins
                
                telemetry_pipeline_property = observabilityadmin_mixins.CfnTelemetryPipelinesPropsMixin.TelemetryPipelineProperty(
                    arn="arn",
                    configuration=observabilityadmin_mixins.CfnTelemetryPipelinesPropsMixin.TelemetryPipelineConfigurationProperty(
                        body="body"
                    ),
                    created_time_stamp=123,
                    last_update_time_stamp=123,
                    name="name",
                    status="status",
                    status_reason=observabilityadmin_mixins.CfnTelemetryPipelinesPropsMixin.TelemetryPipelineStatusReasonProperty(
                        description="description"
                    ),
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bd72d7748ca2dbbfb4974e7471f57d1761c27026fda054887b106e4113c2616f)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
                check_type(argname="argument created_time_stamp", value=created_time_stamp, expected_type=type_hints["created_time_stamp"])
                check_type(argname="argument last_update_time_stamp", value=last_update_time_stamp, expected_type=type_hints["last_update_time_stamp"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                check_type(argname="argument status_reason", value=status_reason, expected_type=type_hints["status_reason"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn
            if configuration is not None:
                self._values["configuration"] = configuration
            if created_time_stamp is not None:
                self._values["created_time_stamp"] = created_time_stamp
            if last_update_time_stamp is not None:
                self._values["last_update_time_stamp"] = last_update_time_stamp
            if name is not None:
                self._values["name"] = name
            if status is not None:
                self._values["status"] = status
            if status_reason is not None:
                self._values["status_reason"] = status_reason
            if tags is not None:
                self._values["tags"] = tags

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-telemetrypipelines-telemetrypipeline.html#cfn-observabilityadmin-telemetrypipelines-telemetrypipeline-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTelemetryPipelinesPropsMixin.TelemetryPipelineConfigurationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-telemetrypipelines-telemetrypipeline.html#cfn-observabilityadmin-telemetrypipelines-telemetrypipeline-configuration
            '''
            result = self._values.get("configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTelemetryPipelinesPropsMixin.TelemetryPipelineConfigurationProperty"]], result)

        @builtins.property
        def created_time_stamp(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-telemetrypipelines-telemetrypipeline.html#cfn-observabilityadmin-telemetrypipelines-telemetrypipeline-createdtimestamp
            '''
            result = self._values.get("created_time_stamp")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def last_update_time_stamp(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-telemetrypipelines-telemetrypipeline.html#cfn-observabilityadmin-telemetrypipelines-telemetrypipeline-lastupdatetimestamp
            '''
            result = self._values.get("last_update_time_stamp")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-telemetrypipelines-telemetrypipeline.html#cfn-observabilityadmin-telemetrypipelines-telemetrypipeline-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-telemetrypipelines-telemetrypipeline.html#cfn-observabilityadmin-telemetrypipelines-telemetrypipeline-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def status_reason(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTelemetryPipelinesPropsMixin.TelemetryPipelineStatusReasonProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-telemetrypipelines-telemetrypipeline.html#cfn-observabilityadmin-telemetrypipelines-telemetrypipeline-statusreason
            '''
            result = self._values.get("status_reason")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTelemetryPipelinesPropsMixin.TelemetryPipelineStatusReasonProperty"]], result)

        @builtins.property
        def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
            '''An array of key-value pairs to apply to this resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-telemetrypipelines-telemetrypipeline.html#cfn-observabilityadmin-telemetrypipelines-telemetrypipeline-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TelemetryPipelineProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_observabilityadmin.mixins.CfnTelemetryPipelinesPropsMixin.TelemetryPipelineStatusReasonProperty",
        jsii_struct_bases=[],
        name_mapping={"description": "description"},
    )
    class TelemetryPipelineStatusReasonProperty:
        def __init__(
            self,
            *,
            description: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param description: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-telemetrypipelines-telemetrypipelinestatusreason.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_observabilityadmin import mixins as observabilityadmin_mixins
                
                telemetry_pipeline_status_reason_property = observabilityadmin_mixins.CfnTelemetryPipelinesPropsMixin.TelemetryPipelineStatusReasonProperty(
                    description="description"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__93da8fa05341fff8c03c1461086d0010dd5a2ce0d708d449e4066cc49b309eab)
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if description is not None:
                self._values["description"] = description

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-telemetrypipelines-telemetrypipelinestatusreason.html#cfn-observabilityadmin-telemetrypipelines-telemetrypipelinestatusreason-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TelemetryPipelineStatusReasonProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_observabilityadmin.mixins.CfnTelemetryRuleMixinProps",
    jsii_struct_bases=[],
    name_mapping={"rule": "rule", "rule_name": "ruleName", "tags": "tags"},
)
class CfnTelemetryRuleMixinProps:
    def __init__(
        self,
        *,
        rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTelemetryRulePropsMixin.TelemetryRuleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnTelemetryRulePropsMixin.

        :param rule: Retrieves the details of a specific telemetry rule in your account.
        :param rule_name: The name of the telemetry rule.
        :param tags: Lists all tags attached to the specified telemetry rule resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-observabilityadmin-telemetryrule.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_observabilityadmin import mixins as observabilityadmin_mixins
            
            cfn_telemetry_rule_mixin_props = observabilityadmin_mixins.CfnTelemetryRuleMixinProps(
                rule=observabilityadmin_mixins.CfnTelemetryRulePropsMixin.TelemetryRuleProperty(
                    destination_configuration=observabilityadmin_mixins.CfnTelemetryRulePropsMixin.TelemetryDestinationConfigurationProperty(
                        destination_pattern="destinationPattern",
                        destination_type="destinationType",
                        retention_in_days=123,
                        vpc_flow_log_parameters=observabilityadmin_mixins.CfnTelemetryRulePropsMixin.VPCFlowLogParametersProperty(
                            log_format="logFormat",
                            max_aggregation_interval=123,
                            traffic_type="trafficType"
                        )
                    ),
                    resource_type="resourceType",
                    selection_criteria="selectionCriteria",
                    telemetry_type="telemetryType"
                ),
                rule_name="ruleName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f106b09656ea9269cc1711a5a9f08475640536bd9c554025d19f3dd58e3f6d7)
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
            check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if rule is not None:
            self._values["rule"] = rule
        if rule_name is not None:
            self._values["rule_name"] = rule_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def rule(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTelemetryRulePropsMixin.TelemetryRuleProperty"]]:
        '''Retrieves the details of a specific telemetry rule in your account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-observabilityadmin-telemetryrule.html#cfn-observabilityadmin-telemetryrule-rule
        '''
        result = self._values.get("rule")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTelemetryRulePropsMixin.TelemetryRuleProperty"]], result)

    @builtins.property
    def rule_name(self) -> typing.Optional[builtins.str]:
        '''The name of the telemetry rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-observabilityadmin-telemetryrule.html#cfn-observabilityadmin-telemetryrule-rulename
        '''
        result = self._values.get("rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Lists all tags attached to the specified telemetry rule resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-observabilityadmin-telemetryrule.html#cfn-observabilityadmin-telemetryrule-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTelemetryRuleMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnTelemetryRulePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_observabilityadmin.mixins.CfnTelemetryRulePropsMixin",
):
    '''Creates a telemetry rule that defines how telemetry should be configured for AWS resources in your account.

    The rule specifies which resources should have telemetry enabled and how that telemetry data should be collected based on resource type, telemetry type, and selection criteria.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-observabilityadmin-telemetryrule.html
    :cloudformationResource: AWS::ObservabilityAdmin::TelemetryRule
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_observabilityadmin import mixins as observabilityadmin_mixins
        
        cfn_telemetry_rule_props_mixin = observabilityadmin_mixins.CfnTelemetryRulePropsMixin(observabilityadmin_mixins.CfnTelemetryRuleMixinProps(
            rule=observabilityadmin_mixins.CfnTelemetryRulePropsMixin.TelemetryRuleProperty(
                destination_configuration=observabilityadmin_mixins.CfnTelemetryRulePropsMixin.TelemetryDestinationConfigurationProperty(
                    destination_pattern="destinationPattern",
                    destination_type="destinationType",
                    retention_in_days=123,
                    vpc_flow_log_parameters=observabilityadmin_mixins.CfnTelemetryRulePropsMixin.VPCFlowLogParametersProperty(
                        log_format="logFormat",
                        max_aggregation_interval=123,
                        traffic_type="trafficType"
                    )
                ),
                resource_type="resourceType",
                selection_criteria="selectionCriteria",
                telemetry_type="telemetryType"
            ),
            rule_name="ruleName",
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
        props: typing.Union[CfnTelemetryRuleMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ObservabilityAdmin::TelemetryRule``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77057f3c384f54dce35c5153e8066e4aeb4b704caeec57789b0009db5583f28c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__16f1483e302f12ce770367f29f5975e83b1bb48ed1f565417ad4c8506c555750)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f441ffc6e2caf60f690ce4950c1b886e8719529f76a4e8acbb8e999de4c018c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTelemetryRuleMixinProps:
        return typing.cast(CfnTelemetryRuleMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_observabilityadmin.mixins.CfnTelemetryRulePropsMixin.TelemetryDestinationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_pattern": "destinationPattern",
            "destination_type": "destinationType",
            "retention_in_days": "retentionInDays",
            "vpc_flow_log_parameters": "vpcFlowLogParameters",
        },
    )
    class TelemetryDestinationConfigurationProperty:
        def __init__(
            self,
            *,
            destination_pattern: typing.Optional[builtins.str] = None,
            destination_type: typing.Optional[builtins.str] = None,
            retention_in_days: typing.Optional[jsii.Number] = None,
            vpc_flow_log_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTelemetryRulePropsMixin.VPCFlowLogParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Configuration specifying where and how telemetry data should be delivered for AWS resources.

            :param destination_pattern: The pattern used to generate the destination path or name, supporting macros like and .
            :param destination_type: The type of destination for the telemetry data (e.g., "Amazon CloudWatch Logs", "S3").
            :param retention_in_days: The number of days to retain the telemetry data in the destination.
            :param vpc_flow_log_parameters: Configuration parameters specific to VPC Flow Logs when VPC is the resource type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-telemetryrule-telemetrydestinationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_observabilityadmin import mixins as observabilityadmin_mixins
                
                telemetry_destination_configuration_property = observabilityadmin_mixins.CfnTelemetryRulePropsMixin.TelemetryDestinationConfigurationProperty(
                    destination_pattern="destinationPattern",
                    destination_type="destinationType",
                    retention_in_days=123,
                    vpc_flow_log_parameters=observabilityadmin_mixins.CfnTelemetryRulePropsMixin.VPCFlowLogParametersProperty(
                        log_format="logFormat",
                        max_aggregation_interval=123,
                        traffic_type="trafficType"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__28501549e29342901adb712557c8c6e60a55f52969fa24acf562e782e8f0aef4)
                check_type(argname="argument destination_pattern", value=destination_pattern, expected_type=type_hints["destination_pattern"])
                check_type(argname="argument destination_type", value=destination_type, expected_type=type_hints["destination_type"])
                check_type(argname="argument retention_in_days", value=retention_in_days, expected_type=type_hints["retention_in_days"])
                check_type(argname="argument vpc_flow_log_parameters", value=vpc_flow_log_parameters, expected_type=type_hints["vpc_flow_log_parameters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination_pattern is not None:
                self._values["destination_pattern"] = destination_pattern
            if destination_type is not None:
                self._values["destination_type"] = destination_type
            if retention_in_days is not None:
                self._values["retention_in_days"] = retention_in_days
            if vpc_flow_log_parameters is not None:
                self._values["vpc_flow_log_parameters"] = vpc_flow_log_parameters

        @builtins.property
        def destination_pattern(self) -> typing.Optional[builtins.str]:
            '''The pattern used to generate the destination path or name, supporting macros like  and .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-telemetryrule-telemetrydestinationconfiguration.html#cfn-observabilityadmin-telemetryrule-telemetrydestinationconfiguration-destinationpattern
            '''
            result = self._values.get("destination_pattern")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def destination_type(self) -> typing.Optional[builtins.str]:
            '''The type of destination for the telemetry data (e.g., "Amazon CloudWatch Logs", "S3").

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-telemetryrule-telemetrydestinationconfiguration.html#cfn-observabilityadmin-telemetryrule-telemetrydestinationconfiguration-destinationtype
            '''
            result = self._values.get("destination_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def retention_in_days(self) -> typing.Optional[jsii.Number]:
            '''The number of days to retain the telemetry data in the destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-telemetryrule-telemetrydestinationconfiguration.html#cfn-observabilityadmin-telemetryrule-telemetrydestinationconfiguration-retentionindays
            '''
            result = self._values.get("retention_in_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def vpc_flow_log_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTelemetryRulePropsMixin.VPCFlowLogParametersProperty"]]:
            '''Configuration parameters specific to VPC Flow Logs when VPC is the resource type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-telemetryrule-telemetrydestinationconfiguration.html#cfn-observabilityadmin-telemetryrule-telemetrydestinationconfiguration-vpcflowlogparameters
            '''
            result = self._values.get("vpc_flow_log_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTelemetryRulePropsMixin.VPCFlowLogParametersProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TelemetryDestinationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_observabilityadmin.mixins.CfnTelemetryRulePropsMixin.TelemetryRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_configuration": "destinationConfiguration",
            "resource_type": "resourceType",
            "selection_criteria": "selectionCriteria",
            "telemetry_type": "telemetryType",
        },
    )
    class TelemetryRuleProperty:
        def __init__(
            self,
            *,
            destination_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTelemetryRulePropsMixin.TelemetryDestinationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            resource_type: typing.Optional[builtins.str] = None,
            selection_criteria: typing.Optional[builtins.str] = None,
            telemetry_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines how telemetry should be configured for specific AWS resources.

            :param destination_configuration: Configuration specifying where and how the telemetry data should be delivered.
            :param resource_type: The type of AWS resource to configure telemetry for (e.g., "AWS::EC2::VPC").
            :param selection_criteria: Criteria for selecting which resources the rule applies to, such as resource tags.
            :param telemetry_type: The type of telemetry to collect (Logs, Metrics, or Traces).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-telemetryrule-telemetryrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_observabilityadmin import mixins as observabilityadmin_mixins
                
                telemetry_rule_property = observabilityadmin_mixins.CfnTelemetryRulePropsMixin.TelemetryRuleProperty(
                    destination_configuration=observabilityadmin_mixins.CfnTelemetryRulePropsMixin.TelemetryDestinationConfigurationProperty(
                        destination_pattern="destinationPattern",
                        destination_type="destinationType",
                        retention_in_days=123,
                        vpc_flow_log_parameters=observabilityadmin_mixins.CfnTelemetryRulePropsMixin.VPCFlowLogParametersProperty(
                            log_format="logFormat",
                            max_aggregation_interval=123,
                            traffic_type="trafficType"
                        )
                    ),
                    resource_type="resourceType",
                    selection_criteria="selectionCriteria",
                    telemetry_type="telemetryType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8fe0de6e2112ec49c0ef50100d16747fc0268f739c08c0cbb018d1ea90b36418)
                check_type(argname="argument destination_configuration", value=destination_configuration, expected_type=type_hints["destination_configuration"])
                check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
                check_type(argname="argument selection_criteria", value=selection_criteria, expected_type=type_hints["selection_criteria"])
                check_type(argname="argument telemetry_type", value=telemetry_type, expected_type=type_hints["telemetry_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination_configuration is not None:
                self._values["destination_configuration"] = destination_configuration
            if resource_type is not None:
                self._values["resource_type"] = resource_type
            if selection_criteria is not None:
                self._values["selection_criteria"] = selection_criteria
            if telemetry_type is not None:
                self._values["telemetry_type"] = telemetry_type

        @builtins.property
        def destination_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTelemetryRulePropsMixin.TelemetryDestinationConfigurationProperty"]]:
            '''Configuration specifying where and how the telemetry data should be delivered.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-telemetryrule-telemetryrule.html#cfn-observabilityadmin-telemetryrule-telemetryrule-destinationconfiguration
            '''
            result = self._values.get("destination_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTelemetryRulePropsMixin.TelemetryDestinationConfigurationProperty"]], result)

        @builtins.property
        def resource_type(self) -> typing.Optional[builtins.str]:
            '''The type of AWS resource to configure telemetry for (e.g., "AWS::EC2::VPC").

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-telemetryrule-telemetryrule.html#cfn-observabilityadmin-telemetryrule-telemetryrule-resourcetype
            '''
            result = self._values.get("resource_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def selection_criteria(self) -> typing.Optional[builtins.str]:
            '''Criteria for selecting which resources the rule applies to, such as resource tags.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-telemetryrule-telemetryrule.html#cfn-observabilityadmin-telemetryrule-telemetryrule-selectioncriteria
            '''
            result = self._values.get("selection_criteria")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def telemetry_type(self) -> typing.Optional[builtins.str]:
            '''The type of telemetry to collect (Logs, Metrics, or Traces).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-telemetryrule-telemetryrule.html#cfn-observabilityadmin-telemetryrule-telemetryrule-telemetrytype
            '''
            result = self._values.get("telemetry_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TelemetryRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_observabilityadmin.mixins.CfnTelemetryRulePropsMixin.VPCFlowLogParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "log_format": "logFormat",
            "max_aggregation_interval": "maxAggregationInterval",
            "traffic_type": "trafficType",
        },
    )
    class VPCFlowLogParametersProperty:
        def __init__(
            self,
            *,
            log_format: typing.Optional[builtins.str] = None,
            max_aggregation_interval: typing.Optional[jsii.Number] = None,
            traffic_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration parameters specific to VPC Flow Logs.

            :param log_format: The format in which VPC Flow Log entries should be logged.
            :param max_aggregation_interval: The maximum interval in seconds between the capture of flow log records.
            :param traffic_type: The type of traffic to log (ACCEPT, REJECT, or ALL).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-telemetryrule-vpcflowlogparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_observabilityadmin import mixins as observabilityadmin_mixins
                
                v_pCFlow_log_parameters_property = observabilityadmin_mixins.CfnTelemetryRulePropsMixin.VPCFlowLogParametersProperty(
                    log_format="logFormat",
                    max_aggregation_interval=123,
                    traffic_type="trafficType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7df388d0e9198af0dfb5b2fbc8fda02f18c1034c511694a21f9df79d6b8472df)
                check_type(argname="argument log_format", value=log_format, expected_type=type_hints["log_format"])
                check_type(argname="argument max_aggregation_interval", value=max_aggregation_interval, expected_type=type_hints["max_aggregation_interval"])
                check_type(argname="argument traffic_type", value=traffic_type, expected_type=type_hints["traffic_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if log_format is not None:
                self._values["log_format"] = log_format
            if max_aggregation_interval is not None:
                self._values["max_aggregation_interval"] = max_aggregation_interval
            if traffic_type is not None:
                self._values["traffic_type"] = traffic_type

        @builtins.property
        def log_format(self) -> typing.Optional[builtins.str]:
            '''The format in which VPC Flow Log entries should be logged.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-telemetryrule-vpcflowlogparameters.html#cfn-observabilityadmin-telemetryrule-vpcflowlogparameters-logformat
            '''
            result = self._values.get("log_format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def max_aggregation_interval(self) -> typing.Optional[jsii.Number]:
            '''The maximum interval in seconds between the capture of flow log records.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-telemetryrule-vpcflowlogparameters.html#cfn-observabilityadmin-telemetryrule-vpcflowlogparameters-maxaggregationinterval
            '''
            result = self._values.get("max_aggregation_interval")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def traffic_type(self) -> typing.Optional[builtins.str]:
            '''The type of traffic to log (ACCEPT, REJECT, or ALL).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-observabilityadmin-telemetryrule-vpcflowlogparameters.html#cfn-observabilityadmin-telemetryrule-vpcflowlogparameters-traffictype
            '''
            result = self._values.get("traffic_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VPCFlowLogParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnOrganizationCentralizationRuleMixinProps",
    "CfnOrganizationCentralizationRulePropsMixin",
    "CfnOrganizationTelemetryRuleMixinProps",
    "CfnOrganizationTelemetryRulePropsMixin",
    "CfnS3TableIntegrationMixinProps",
    "CfnS3TableIntegrationPropsMixin",
    "CfnTelemetryPipelinesMixinProps",
    "CfnTelemetryPipelinesPropsMixin",
    "CfnTelemetryRuleMixinProps",
    "CfnTelemetryRulePropsMixin",
]

publication.publish()

def _typecheckingstub__310ec6a679061eb83926d8ae3b39173eb5ab3332834bcd390f2b95654cb0a988(
    *,
    rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOrganizationCentralizationRulePropsMixin.CentralizationRuleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b92a09ea5de36bca1624cdcd88855863a8f25907b5e61b62b7133dd3d649072a(
    props: typing.Union[CfnOrganizationCentralizationRuleMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a090de4b65435c87ee9ab9d01f183e4b6a7d4b839d3d3ee55716dbb86843eff(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dee77b4f08a81761096aeb80a178d25ea4a782637b6bc9c71b6573905e47038f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1fc4a314714a6ee9b9c5401241d44806f07d9b0144aab9bf41228542fbef316(
    *,
    account: typing.Optional[builtins.str] = None,
    destination_logs_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOrganizationCentralizationRulePropsMixin.DestinationLogsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeb025381c67cbd8d6fbeb2bf419a2922b2c6960d2ff942c49ffdb25ed4532bb(
    *,
    destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOrganizationCentralizationRulePropsMixin.CentralizationRuleDestinationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOrganizationCentralizationRulePropsMixin.CentralizationRuleSourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efe48945816c679e788eeaba1d740a2273e1e1c659b1fe3737dc05fd07e0f356(
    *,
    regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    scope: typing.Optional[builtins.str] = None,
    source_logs_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOrganizationCentralizationRulePropsMixin.SourceLogsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62c5ba476b7b03a0e2dd22bca8f2c17a33e42db3e21d261e03bd3755258abbb7(
    *,
    backup_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOrganizationCentralizationRulePropsMixin.LogsBackupConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    logs_encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOrganizationCentralizationRulePropsMixin.LogsEncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48f392ca61db0ece40aedc750490cec67420f62313bb4db5194b426c3affc678(
    *,
    kms_key_arn: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4af2121f84a79b891422c6ca4148fa507b8c9739f568532bc7676bbcd1a1e2fe(
    *,
    encryption_conflict_resolution_strategy: typing.Optional[builtins.str] = None,
    encryption_strategy: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2189fab5fc6f36ac4898822304ae1b38fa0852872791d45876a1c3bfd2b550e8(
    *,
    encrypted_log_group_strategy: typing.Optional[builtins.str] = None,
    log_group_selection_criteria: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a1acec9dba368ed19d2bcc8bcabdaa2d58c2298bc6a5af321537e2778ad29c8(
    *,
    rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOrganizationTelemetryRulePropsMixin.TelemetryRuleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55ed612c92f8c36eb825f453891f36c8e15a55233b53c73df248ec685ad0590a(
    props: typing.Union[CfnOrganizationTelemetryRuleMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f59046f5a873bc5970849188c64584c0d42e2ecb442ec727e5e8cb65f656a20(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afa44fc6e808f884af9d1bbf40f5eda0e6c734dca626e41f8d89ac3dba9018e6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aad96fd4765150ac739ae57bb0a5f2fc0da8b91213df52eaa07bc558b32dec3(
    *,
    destination_pattern: typing.Optional[builtins.str] = None,
    destination_type: typing.Optional[builtins.str] = None,
    retention_in_days: typing.Optional[jsii.Number] = None,
    vpc_flow_log_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOrganizationTelemetryRulePropsMixin.VPCFlowLogParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d963398c2186e5f1789c1583caf09b321373e83e19a74bfd3683c30f2ec6a35a(
    *,
    destination_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOrganizationTelemetryRulePropsMixin.TelemetryDestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    resource_type: typing.Optional[builtins.str] = None,
    scope: typing.Optional[builtins.str] = None,
    selection_criteria: typing.Optional[builtins.str] = None,
    telemetry_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__800d32ba27dda96915b16198d35c7226c11dded78a8a76197a149d6f37c3097c(
    *,
    log_format: typing.Optional[builtins.str] = None,
    max_aggregation_interval: typing.Optional[jsii.Number] = None,
    traffic_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89f0602bcddda493541aa5c50f1dca52fca6b6b1db0d092329afe2e25abf932f(
    *,
    encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnS3TableIntegrationPropsMixin.EncryptionConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    log_sources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnS3TableIntegrationPropsMixin.LogSourceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ecefc94a5d14d6f82bd29573934ddd9402892663a6628b5f5c9f6b93ce165c3(
    props: typing.Union[CfnS3TableIntegrationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__590b3dc3305d44cd252dbe2d17502f17f3902a7463be507e9fc4efe68ab48d99(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f6614d16b6ac1ca40575a26878a09fc7fdd8e9f0a9e59a0ec3dc3b234862562(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c224dda3e14b265c3d0033c46e331e7c3e0784f4c72e9a57901495a35d6fd73(
    *,
    kms_key_arn: typing.Optional[builtins.str] = None,
    sse_algorithm: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55a1b8dc81413f99d4f97d385779f9ee673c49fade884c18f97de11adf123b86(
    *,
    identifier: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e57e930d90900d811e8510de229c3cf9635373026652d762a7053411ae50b4ee(
    *,
    configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTelemetryPipelinesPropsMixin.TelemetryPipelineConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90597d794795765813e020b415e8d167f4495b35d274efec2aeacdbc04f458be(
    props: typing.Union[CfnTelemetryPipelinesMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dee45317d853c4c0cf9a53dfe0f82037b2221791c55604d9902563d83c4d4dc(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaac31a163b9df7c4a7924a9d5ffa358c99cc220f8594921b86633a1a2f6046f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a563a720c1f6f5e49098b737e2c1f6182a1919592f63854fc5ae80358d4eb23(
    *,
    body: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd72d7748ca2dbbfb4974e7471f57d1761c27026fda054887b106e4113c2616f(
    *,
    arn: typing.Optional[builtins.str] = None,
    configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTelemetryPipelinesPropsMixin.TelemetryPipelineConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    created_time_stamp: typing.Optional[jsii.Number] = None,
    last_update_time_stamp: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    status_reason: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTelemetryPipelinesPropsMixin.TelemetryPipelineStatusReasonProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93da8fa05341fff8c03c1461086d0010dd5a2ce0d708d449e4066cc49b309eab(
    *,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f106b09656ea9269cc1711a5a9f08475640536bd9c554025d19f3dd58e3f6d7(
    *,
    rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTelemetryRulePropsMixin.TelemetryRuleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77057f3c384f54dce35c5153e8066e4aeb4b704caeec57789b0009db5583f28c(
    props: typing.Union[CfnTelemetryRuleMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16f1483e302f12ce770367f29f5975e83b1bb48ed1f565417ad4c8506c555750(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f441ffc6e2caf60f690ce4950c1b886e8719529f76a4e8acbb8e999de4c018c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28501549e29342901adb712557c8c6e60a55f52969fa24acf562e782e8f0aef4(
    *,
    destination_pattern: typing.Optional[builtins.str] = None,
    destination_type: typing.Optional[builtins.str] = None,
    retention_in_days: typing.Optional[jsii.Number] = None,
    vpc_flow_log_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTelemetryRulePropsMixin.VPCFlowLogParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fe0de6e2112ec49c0ef50100d16747fc0268f739c08c0cbb018d1ea90b36418(
    *,
    destination_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTelemetryRulePropsMixin.TelemetryDestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    resource_type: typing.Optional[builtins.str] = None,
    selection_criteria: typing.Optional[builtins.str] = None,
    telemetry_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7df388d0e9198af0dfb5b2fbc8fda02f18c1034c511694a21f9df79d6b8472df(
    *,
    log_format: typing.Optional[builtins.str] = None,
    max_aggregation_interval: typing.Optional[jsii.Number] = None,
    traffic_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
