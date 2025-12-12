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
    jsii_type="@aws-cdk/mixins-preview.aws_accessanalyzer.mixins.CfnAnalyzerMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "analyzer_configuration": "analyzerConfiguration",
        "analyzer_name": "analyzerName",
        "archive_rules": "archiveRules",
        "tags": "tags",
        "type": "type",
    },
)
class CfnAnalyzerMixinProps:
    def __init__(
        self,
        *,
        analyzer_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnalyzerPropsMixin.AnalyzerConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        analyzer_name: typing.Optional[builtins.str] = None,
        archive_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnalyzerPropsMixin.ArchiveRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnAnalyzerPropsMixin.

        :param analyzer_configuration: Contains information about the configuration of an analyzer for an AWS organization or account.
        :param analyzer_name: The name of the analyzer.
        :param archive_rules: Specifies the archive rules to add for the analyzer. Archive rules automatically archive findings that meet the criteria you define for the rule.
        :param tags: An array of key-value pairs to apply to the analyzer. You can use the set of Unicode letters, digits, whitespace, ``_`` , ``.`` , ``/`` , ``=`` , ``+`` , and ``-`` . For the tag key, you can specify a value that is 1 to 128 characters in length and cannot be prefixed with ``aws:`` . For the tag value, you can specify a value that is 0 to 256 characters in length.
        :param type: The type represents the zone of trust for the analyzer. *Allowed Values* : ACCOUNT | ORGANIZATION | ACCOUNT_UNUSED_ACCESS | ACCOUNT_INTERNAL_ACCESS | ORGANIZATION_INTERNAL_ACCESS | ORGANIZATION_UNUSED_ACCESS

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-accessanalyzer-analyzer.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_accessanalyzer import mixins as accessanalyzer_mixins
            
            cfn_analyzer_mixin_props = accessanalyzer_mixins.CfnAnalyzerMixinProps(
                analyzer_configuration=accessanalyzer_mixins.CfnAnalyzerPropsMixin.AnalyzerConfigurationProperty(
                    internal_access_configuration=accessanalyzer_mixins.CfnAnalyzerPropsMixin.InternalAccessConfigurationProperty(
                        internal_access_analysis_rule=accessanalyzer_mixins.CfnAnalyzerPropsMixin.InternalAccessAnalysisRuleProperty(
                            inclusions=[accessanalyzer_mixins.CfnAnalyzerPropsMixin.InternalAccessAnalysisRuleCriteriaProperty(
                                account_ids=["accountIds"],
                                resource_arns=["resourceArns"],
                                resource_types=["resourceTypes"]
                            )]
                        )
                    ),
                    unused_access_configuration=accessanalyzer_mixins.CfnAnalyzerPropsMixin.UnusedAccessConfigurationProperty(
                        analysis_rule=accessanalyzer_mixins.CfnAnalyzerPropsMixin.AnalysisRuleProperty(
                            exclusions=[accessanalyzer_mixins.CfnAnalyzerPropsMixin.AnalysisRuleCriteriaProperty(
                                account_ids=["accountIds"],
                                resource_tags=[[CfnTag(
                                    key="key",
                                    value="value"
                                )]]
                            )]
                        ),
                        unused_access_age=123
                    )
                ),
                analyzer_name="analyzerName",
                archive_rules=[accessanalyzer_mixins.CfnAnalyzerPropsMixin.ArchiveRuleProperty(
                    filter=[accessanalyzer_mixins.CfnAnalyzerPropsMixin.FilterProperty(
                        contains=["contains"],
                        eq=["eq"],
                        exists=False,
                        neq=["neq"],
                        property="property"
                    )],
                    rule_name="ruleName"
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69fe1cc1bbe2826083f4ee05e71a9fc2303244fb87cee4549b48d13c0b6235c8)
            check_type(argname="argument analyzer_configuration", value=analyzer_configuration, expected_type=type_hints["analyzer_configuration"])
            check_type(argname="argument analyzer_name", value=analyzer_name, expected_type=type_hints["analyzer_name"])
            check_type(argname="argument archive_rules", value=archive_rules, expected_type=type_hints["archive_rules"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if analyzer_configuration is not None:
            self._values["analyzer_configuration"] = analyzer_configuration
        if analyzer_name is not None:
            self._values["analyzer_name"] = analyzer_name
        if archive_rules is not None:
            self._values["archive_rules"] = archive_rules
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def analyzer_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnalyzerPropsMixin.AnalyzerConfigurationProperty"]]:
        '''Contains information about the configuration of an analyzer for an AWS organization or account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-accessanalyzer-analyzer.html#cfn-accessanalyzer-analyzer-analyzerconfiguration
        '''
        result = self._values.get("analyzer_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnalyzerPropsMixin.AnalyzerConfigurationProperty"]], result)

    @builtins.property
    def analyzer_name(self) -> typing.Optional[builtins.str]:
        '''The name of the analyzer.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-accessanalyzer-analyzer.html#cfn-accessanalyzer-analyzer-analyzername
        '''
        result = self._values.get("analyzer_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def archive_rules(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnalyzerPropsMixin.ArchiveRuleProperty"]]]]:
        '''Specifies the archive rules to add for the analyzer.

        Archive rules automatically archive findings that meet the criteria you define for the rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-accessanalyzer-analyzer.html#cfn-accessanalyzer-analyzer-archiverules
        '''
        result = self._values.get("archive_rules")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnalyzerPropsMixin.ArchiveRuleProperty"]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to the analyzer.

        You can use the set of Unicode letters, digits, whitespace, ``_`` , ``.`` , ``/`` , ``=`` , ``+`` , and ``-`` .

        For the tag key, you can specify a value that is 1 to 128 characters in length and cannot be prefixed with ``aws:`` .

        For the tag value, you can specify a value that is 0 to 256 characters in length.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-accessanalyzer-analyzer.html#cfn-accessanalyzer-analyzer-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type represents the zone of trust for the analyzer.

        *Allowed Values* : ACCOUNT | ORGANIZATION | ACCOUNT_UNUSED_ACCESS | ACCOUNT_INTERNAL_ACCESS | ORGANIZATION_INTERNAL_ACCESS | ORGANIZATION_UNUSED_ACCESS

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-accessanalyzer-analyzer.html#cfn-accessanalyzer-analyzer-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAnalyzerMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAnalyzerPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_accessanalyzer.mixins.CfnAnalyzerPropsMixin",
):
    '''The ``AWS::AccessAnalyzer::Analyzer`` resource specifies a new analyzer.

    The analyzer is an object that represents the IAM Access Analyzer feature. An analyzer is required for Access Analyzer to become operational.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-accessanalyzer-analyzer.html
    :cloudformationResource: AWS::AccessAnalyzer::Analyzer
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_accessanalyzer import mixins as accessanalyzer_mixins
        
        cfn_analyzer_props_mixin = accessanalyzer_mixins.CfnAnalyzerPropsMixin(accessanalyzer_mixins.CfnAnalyzerMixinProps(
            analyzer_configuration=accessanalyzer_mixins.CfnAnalyzerPropsMixin.AnalyzerConfigurationProperty(
                internal_access_configuration=accessanalyzer_mixins.CfnAnalyzerPropsMixin.InternalAccessConfigurationProperty(
                    internal_access_analysis_rule=accessanalyzer_mixins.CfnAnalyzerPropsMixin.InternalAccessAnalysisRuleProperty(
                        inclusions=[accessanalyzer_mixins.CfnAnalyzerPropsMixin.InternalAccessAnalysisRuleCriteriaProperty(
                            account_ids=["accountIds"],
                            resource_arns=["resourceArns"],
                            resource_types=["resourceTypes"]
                        )]
                    )
                ),
                unused_access_configuration=accessanalyzer_mixins.CfnAnalyzerPropsMixin.UnusedAccessConfigurationProperty(
                    analysis_rule=accessanalyzer_mixins.CfnAnalyzerPropsMixin.AnalysisRuleProperty(
                        exclusions=[accessanalyzer_mixins.CfnAnalyzerPropsMixin.AnalysisRuleCriteriaProperty(
                            account_ids=["accountIds"],
                            resource_tags=[[CfnTag(
                                key="key",
                                value="value"
                            )]]
                        )]
                    ),
                    unused_access_age=123
                )
            ),
            analyzer_name="analyzerName",
            archive_rules=[accessanalyzer_mixins.CfnAnalyzerPropsMixin.ArchiveRuleProperty(
                filter=[accessanalyzer_mixins.CfnAnalyzerPropsMixin.FilterProperty(
                    contains=["contains"],
                    eq=["eq"],
                    exists=False,
                    neq=["neq"],
                    property="property"
                )],
                rule_name="ruleName"
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
        props: typing.Union[CfnAnalyzerMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AccessAnalyzer::Analyzer``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c954668bed59f02d0ad7a4f0cce23933f30f54c8a2277a899fd301bf10fb72a5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__de7ff3894a64c3aef10f8ae4471c5f5a07e421a98588e81226f0772315d77d5c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aad9a902683682e41db2008f65d2bea9839fd3e4b60983c60cba6c02232e6f8b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAnalyzerMixinProps:
        return typing.cast(CfnAnalyzerMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_accessanalyzer.mixins.CfnAnalyzerPropsMixin.AnalysisRuleCriteriaProperty",
        jsii_struct_bases=[],
        name_mapping={"account_ids": "accountIds", "resource_tags": "resourceTags"},
    )
    class AnalysisRuleCriteriaProperty:
        def __init__(
            self,
            *,
            account_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            resource_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]]]]]] = None,
        ) -> None:
            '''The criteria for an analysis rule for an analyzer.

            The criteria determine which entities will generate findings.

            :param account_ids: A list of AWS account IDs to apply to the analysis rule criteria. The accounts cannot include the organization analyzer owner account. Account IDs can only be applied to the analysis rule criteria for organization-level analyzers. The list cannot include more than 2,000 account IDs.
            :param resource_tags: An array of key-value pairs to match for your resources. You can use the set of Unicode letters, digits, whitespace, ``_`` , ``.`` , ``/`` , ``=`` , ``+`` , and ``-`` . For the tag key, you can specify a value that is 1 to 128 characters in length and cannot be prefixed with ``aws:`` . For the tag value, you can specify a value that is 0 to 256 characters in length. If the specified tag value is 0 characters, the rule is applied to all principals with the specified tag key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-accessanalyzer-analyzer-analysisrulecriteria.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_accessanalyzer import mixins as accessanalyzer_mixins
                
                analysis_rule_criteria_property = accessanalyzer_mixins.CfnAnalyzerPropsMixin.AnalysisRuleCriteriaProperty(
                    account_ids=["accountIds"],
                    resource_tags=[[CfnTag(
                        key="key",
                        value="value"
                    )]]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2a680f076761a0597e3aaddcc7166caf3caec05a619e1195d2dceba8551ecd12)
                check_type(argname="argument account_ids", value=account_ids, expected_type=type_hints["account_ids"])
                check_type(argname="argument resource_tags", value=resource_tags, expected_type=type_hints["resource_tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if account_ids is not None:
                self._values["account_ids"] = account_ids
            if resource_tags is not None:
                self._values["resource_tags"] = resource_tags

        @builtins.property
        def account_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of AWS account IDs to apply to the analysis rule criteria.

            The accounts cannot include the organization analyzer owner account. Account IDs can only be applied to the analysis rule criteria for organization-level analyzers. The list cannot include more than 2,000 account IDs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-accessanalyzer-analyzer-analysisrulecriteria.html#cfn-accessanalyzer-analyzer-analysisrulecriteria-accountids
            '''
            result = self._values.get("account_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def resource_tags(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_ceddda9d.CfnTag]]]]]]:
            '''An array of key-value pairs to match for your resources.

            You can use the set of Unicode letters, digits, whitespace, ``_`` , ``.`` , ``/`` , ``=`` , ``+`` , and ``-`` .

            For the tag key, you can specify a value that is 1 to 128 characters in length and cannot be prefixed with ``aws:`` .

            For the tag value, you can specify a value that is 0 to 256 characters in length. If the specified tag value is 0 characters, the rule is applied to all principals with the specified tag key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-accessanalyzer-analyzer-analysisrulecriteria.html#cfn-accessanalyzer-analyzer-analysisrulecriteria-resourcetags
            '''
            result = self._values.get("resource_tags")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_ceddda9d.CfnTag]]]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AnalysisRuleCriteriaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_accessanalyzer.mixins.CfnAnalyzerPropsMixin.AnalysisRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"exclusions": "exclusions"},
    )
    class AnalysisRuleProperty:
        def __init__(
            self,
            *,
            exclusions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnalyzerPropsMixin.AnalysisRuleCriteriaProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Contains information about analysis rules for the analyzer.

            Analysis rules determine which entities will generate findings based on the criteria you define when you create the rule.

            :param exclusions: A list of rules for the analyzer containing criteria to exclude from analysis. Entities that meet the rule criteria will not generate findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-accessanalyzer-analyzer-analysisrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_accessanalyzer import mixins as accessanalyzer_mixins
                
                analysis_rule_property = accessanalyzer_mixins.CfnAnalyzerPropsMixin.AnalysisRuleProperty(
                    exclusions=[accessanalyzer_mixins.CfnAnalyzerPropsMixin.AnalysisRuleCriteriaProperty(
                        account_ids=["accountIds"],
                        resource_tags=[[CfnTag(
                            key="key",
                            value="value"
                        )]]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__16d2d9b6c92c88259edbcc34ed666d0f0a5ff14ab379a87467d3cb260395b67a)
                check_type(argname="argument exclusions", value=exclusions, expected_type=type_hints["exclusions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if exclusions is not None:
                self._values["exclusions"] = exclusions

        @builtins.property
        def exclusions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnalyzerPropsMixin.AnalysisRuleCriteriaProperty"]]]]:
            '''A list of rules for the analyzer containing criteria to exclude from analysis.

            Entities that meet the rule criteria will not generate findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-accessanalyzer-analyzer-analysisrule.html#cfn-accessanalyzer-analyzer-analysisrule-exclusions
            '''
            result = self._values.get("exclusions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnalyzerPropsMixin.AnalysisRuleCriteriaProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AnalysisRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_accessanalyzer.mixins.CfnAnalyzerPropsMixin.AnalyzerConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "internal_access_configuration": "internalAccessConfiguration",
            "unused_access_configuration": "unusedAccessConfiguration",
        },
    )
    class AnalyzerConfigurationProperty:
        def __init__(
            self,
            *,
            internal_access_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnalyzerPropsMixin.InternalAccessConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            unused_access_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnalyzerPropsMixin.UnusedAccessConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains information about the configuration of an analyzer for an AWS organization or account.

            :param internal_access_configuration: Specifies the configuration of an internal access analyzer for an AWS organization or account. This configuration determines how the analyzer evaluates access within your AWS environment.
            :param unused_access_configuration: Specifies the configuration of an unused access analyzer for an AWS organization or account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-accessanalyzer-analyzer-analyzerconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_accessanalyzer import mixins as accessanalyzer_mixins
                
                analyzer_configuration_property = accessanalyzer_mixins.CfnAnalyzerPropsMixin.AnalyzerConfigurationProperty(
                    internal_access_configuration=accessanalyzer_mixins.CfnAnalyzerPropsMixin.InternalAccessConfigurationProperty(
                        internal_access_analysis_rule=accessanalyzer_mixins.CfnAnalyzerPropsMixin.InternalAccessAnalysisRuleProperty(
                            inclusions=[accessanalyzer_mixins.CfnAnalyzerPropsMixin.InternalAccessAnalysisRuleCriteriaProperty(
                                account_ids=["accountIds"],
                                resource_arns=["resourceArns"],
                                resource_types=["resourceTypes"]
                            )]
                        )
                    ),
                    unused_access_configuration=accessanalyzer_mixins.CfnAnalyzerPropsMixin.UnusedAccessConfigurationProperty(
                        analysis_rule=accessanalyzer_mixins.CfnAnalyzerPropsMixin.AnalysisRuleProperty(
                            exclusions=[accessanalyzer_mixins.CfnAnalyzerPropsMixin.AnalysisRuleCriteriaProperty(
                                account_ids=["accountIds"],
                                resource_tags=[[CfnTag(
                                    key="key",
                                    value="value"
                                )]]
                            )]
                        ),
                        unused_access_age=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8b07bd627a1c24a0750233c2e89396c510ac157b0dc9ddcf581a741e967c4284)
                check_type(argname="argument internal_access_configuration", value=internal_access_configuration, expected_type=type_hints["internal_access_configuration"])
                check_type(argname="argument unused_access_configuration", value=unused_access_configuration, expected_type=type_hints["unused_access_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if internal_access_configuration is not None:
                self._values["internal_access_configuration"] = internal_access_configuration
            if unused_access_configuration is not None:
                self._values["unused_access_configuration"] = unused_access_configuration

        @builtins.property
        def internal_access_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnalyzerPropsMixin.InternalAccessConfigurationProperty"]]:
            '''Specifies the configuration of an internal access analyzer for an AWS organization or account.

            This configuration determines how the analyzer evaluates access within your AWS environment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-accessanalyzer-analyzer-analyzerconfiguration.html#cfn-accessanalyzer-analyzer-analyzerconfiguration-internalaccessconfiguration
            '''
            result = self._values.get("internal_access_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnalyzerPropsMixin.InternalAccessConfigurationProperty"]], result)

        @builtins.property
        def unused_access_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnalyzerPropsMixin.UnusedAccessConfigurationProperty"]]:
            '''Specifies the configuration of an unused access analyzer for an AWS organization or account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-accessanalyzer-analyzer-analyzerconfiguration.html#cfn-accessanalyzer-analyzer-analyzerconfiguration-unusedaccessconfiguration
            '''
            result = self._values.get("unused_access_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnalyzerPropsMixin.UnusedAccessConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AnalyzerConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_accessanalyzer.mixins.CfnAnalyzerPropsMixin.ArchiveRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"filter": "filter", "rule_name": "ruleName"},
    )
    class ArchiveRuleProperty:
        def __init__(
            self,
            *,
            filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnalyzerPropsMixin.FilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            rule_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about an archive rule.

            Archive rules automatically archive new findings that meet the criteria you define when you create the rule.

            :param filter: The criteria for the rule.
            :param rule_name: The name of the rule to create.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-accessanalyzer-analyzer-archiverule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_accessanalyzer import mixins as accessanalyzer_mixins
                
                archive_rule_property = accessanalyzer_mixins.CfnAnalyzerPropsMixin.ArchiveRuleProperty(
                    filter=[accessanalyzer_mixins.CfnAnalyzerPropsMixin.FilterProperty(
                        contains=["contains"],
                        eq=["eq"],
                        exists=False,
                        neq=["neq"],
                        property="property"
                    )],
                    rule_name="ruleName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__272719439db4cbd7291b417ed0ad293655accb73a00dd9a564f341752ff515bf)
                check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
                check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if filter is not None:
                self._values["filter"] = filter
            if rule_name is not None:
                self._values["rule_name"] = rule_name

        @builtins.property
        def filter(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnalyzerPropsMixin.FilterProperty"]]]]:
            '''The criteria for the rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-accessanalyzer-analyzer-archiverule.html#cfn-accessanalyzer-analyzer-archiverule-filter
            '''
            result = self._values.get("filter")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnalyzerPropsMixin.FilterProperty"]]]], result)

        @builtins.property
        def rule_name(self) -> typing.Optional[builtins.str]:
            '''The name of the rule to create.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-accessanalyzer-analyzer-archiverule.html#cfn-accessanalyzer-analyzer-archiverule-rulename
            '''
            result = self._values.get("rule_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ArchiveRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_accessanalyzer.mixins.CfnAnalyzerPropsMixin.FilterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "contains": "contains",
            "eq": "eq",
            "exists": "exists",
            "neq": "neq",
            "property": "property",
        },
    )
    class FilterProperty:
        def __init__(
            self,
            *,
            contains: typing.Optional[typing.Sequence[builtins.str]] = None,
            eq: typing.Optional[typing.Sequence[builtins.str]] = None,
            exists: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            neq: typing.Optional[typing.Sequence[builtins.str]] = None,
            property: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The criteria that defines the archive rule.

            To learn about filter keys that you can use to create an archive rule, see `filter keys <https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-reference-filter-keys.html>`_ in the *User Guide* .

            :param contains: A "contains" condition to match for the rule.
            :param eq: An "equals" condition to match for the rule.
            :param exists: An "exists" condition to match for the rule.
            :param neq: A "not equal" condition to match for the rule.
            :param property: The property used to define the criteria in the filter for the rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-accessanalyzer-analyzer-filter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_accessanalyzer import mixins as accessanalyzer_mixins
                
                filter_property = accessanalyzer_mixins.CfnAnalyzerPropsMixin.FilterProperty(
                    contains=["contains"],
                    eq=["eq"],
                    exists=False,
                    neq=["neq"],
                    property="property"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a185b96fc89197b05a8a3c2eee316a77d7cedf2686c4f60d796bd6818316ba85)
                check_type(argname="argument contains", value=contains, expected_type=type_hints["contains"])
                check_type(argname="argument eq", value=eq, expected_type=type_hints["eq"])
                check_type(argname="argument exists", value=exists, expected_type=type_hints["exists"])
                check_type(argname="argument neq", value=neq, expected_type=type_hints["neq"])
                check_type(argname="argument property", value=property, expected_type=type_hints["property"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if contains is not None:
                self._values["contains"] = contains
            if eq is not None:
                self._values["eq"] = eq
            if exists is not None:
                self._values["exists"] = exists
            if neq is not None:
                self._values["neq"] = neq
            if property is not None:
                self._values["property"] = property

        @builtins.property
        def contains(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A "contains" condition to match for the rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-accessanalyzer-analyzer-filter.html#cfn-accessanalyzer-analyzer-filter-contains
            '''
            result = self._values.get("contains")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def eq(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An "equals" condition to match for the rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-accessanalyzer-analyzer-filter.html#cfn-accessanalyzer-analyzer-filter-eq
            '''
            result = self._values.get("eq")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def exists(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''An "exists" condition to match for the rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-accessanalyzer-analyzer-filter.html#cfn-accessanalyzer-analyzer-filter-exists
            '''
            result = self._values.get("exists")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def neq(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A "not equal" condition to match for the rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-accessanalyzer-analyzer-filter.html#cfn-accessanalyzer-analyzer-filter-neq
            '''
            result = self._values.get("neq")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def property(self) -> typing.Optional[builtins.str]:
            '''The property used to define the criteria in the filter for the rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-accessanalyzer-analyzer-filter.html#cfn-accessanalyzer-analyzer-filter-property
            '''
            result = self._values.get("property")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_accessanalyzer.mixins.CfnAnalyzerPropsMixin.InternalAccessAnalysisRuleCriteriaProperty",
        jsii_struct_bases=[],
        name_mapping={
            "account_ids": "accountIds",
            "resource_arns": "resourceArns",
            "resource_types": "resourceTypes",
        },
    )
    class InternalAccessAnalysisRuleCriteriaProperty:
        def __init__(
            self,
            *,
            account_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            resource_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
            resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The criteria for an analysis rule for an internal access analyzer.

            :param account_ids: A list of AWS account IDs to apply to the internal access analysis rule criteria. Account IDs can only be applied to the analysis rule criteria for organization-level analyzers.
            :param resource_arns: A list of resource ARNs to apply to the internal access analysis rule criteria. The analyzer will only generate findings for resources that match these ARNs.
            :param resource_types: A list of resource types to apply to the internal access analysis rule criteria. The analyzer will only generate findings for resources of these types. These resource types are currently supported for internal access analyzers: - ``AWS::S3::Bucket`` - ``AWS::RDS::DBSnapshot`` - ``AWS::RDS::DBClusterSnapshot`` - ``AWS::S3Express::DirectoryBucket`` - ``AWS::DynamoDB::Table`` - ``AWS::DynamoDB::Stream``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-accessanalyzer-analyzer-internalaccessanalysisrulecriteria.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_accessanalyzer import mixins as accessanalyzer_mixins
                
                internal_access_analysis_rule_criteria_property = accessanalyzer_mixins.CfnAnalyzerPropsMixin.InternalAccessAnalysisRuleCriteriaProperty(
                    account_ids=["accountIds"],
                    resource_arns=["resourceArns"],
                    resource_types=["resourceTypes"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ae1f64c3f69ed6b67655be091919b5e466e4ab60aad5998c44186b78c29ac7d3)
                check_type(argname="argument account_ids", value=account_ids, expected_type=type_hints["account_ids"])
                check_type(argname="argument resource_arns", value=resource_arns, expected_type=type_hints["resource_arns"])
                check_type(argname="argument resource_types", value=resource_types, expected_type=type_hints["resource_types"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if account_ids is not None:
                self._values["account_ids"] = account_ids
            if resource_arns is not None:
                self._values["resource_arns"] = resource_arns
            if resource_types is not None:
                self._values["resource_types"] = resource_types

        @builtins.property
        def account_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of AWS account IDs to apply to the internal access analysis rule criteria.

            Account IDs can only be applied to the analysis rule criteria for organization-level analyzers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-accessanalyzer-analyzer-internalaccessanalysisrulecriteria.html#cfn-accessanalyzer-analyzer-internalaccessanalysisrulecriteria-accountids
            '''
            result = self._values.get("account_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def resource_arns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of resource ARNs to apply to the internal access analysis rule criteria.

            The analyzer will only generate findings for resources that match these ARNs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-accessanalyzer-analyzer-internalaccessanalysisrulecriteria.html#cfn-accessanalyzer-analyzer-internalaccessanalysisrulecriteria-resourcearns
            '''
            result = self._values.get("resource_arns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def resource_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of resource types to apply to the internal access analysis rule criteria.

            The analyzer will only generate findings for resources of these types. These resource types are currently supported for internal access analyzers:

            - ``AWS::S3::Bucket``
            - ``AWS::RDS::DBSnapshot``
            - ``AWS::RDS::DBClusterSnapshot``
            - ``AWS::S3Express::DirectoryBucket``
            - ``AWS::DynamoDB::Table``
            - ``AWS::DynamoDB::Stream``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-accessanalyzer-analyzer-internalaccessanalysisrulecriteria.html#cfn-accessanalyzer-analyzer-internalaccessanalysisrulecriteria-resourcetypes
            '''
            result = self._values.get("resource_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InternalAccessAnalysisRuleCriteriaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_accessanalyzer.mixins.CfnAnalyzerPropsMixin.InternalAccessAnalysisRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"inclusions": "inclusions"},
    )
    class InternalAccessAnalysisRuleProperty:
        def __init__(
            self,
            *,
            inclusions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnalyzerPropsMixin.InternalAccessAnalysisRuleCriteriaProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Contains information about analysis rules for the internal access analyzer.

            Analysis rules determine which entities will generate findings based on the criteria you define when you create the rule.

            :param inclusions: A list of rules for the internal access analyzer containing criteria to include in analysis. Only resources that meet the rule criteria will generate findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-accessanalyzer-analyzer-internalaccessanalysisrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_accessanalyzer import mixins as accessanalyzer_mixins
                
                internal_access_analysis_rule_property = accessanalyzer_mixins.CfnAnalyzerPropsMixin.InternalAccessAnalysisRuleProperty(
                    inclusions=[accessanalyzer_mixins.CfnAnalyzerPropsMixin.InternalAccessAnalysisRuleCriteriaProperty(
                        account_ids=["accountIds"],
                        resource_arns=["resourceArns"],
                        resource_types=["resourceTypes"]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5080dec50c510d1f00f43d5ada29136552cc05561b525c6ec5961c0aa0f7df30)
                check_type(argname="argument inclusions", value=inclusions, expected_type=type_hints["inclusions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if inclusions is not None:
                self._values["inclusions"] = inclusions

        @builtins.property
        def inclusions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnalyzerPropsMixin.InternalAccessAnalysisRuleCriteriaProperty"]]]]:
            '''A list of rules for the internal access analyzer containing criteria to include in analysis.

            Only resources that meet the rule criteria will generate findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-accessanalyzer-analyzer-internalaccessanalysisrule.html#cfn-accessanalyzer-analyzer-internalaccessanalysisrule-inclusions
            '''
            result = self._values.get("inclusions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnalyzerPropsMixin.InternalAccessAnalysisRuleCriteriaProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InternalAccessAnalysisRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_accessanalyzer.mixins.CfnAnalyzerPropsMixin.InternalAccessConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"internal_access_analysis_rule": "internalAccessAnalysisRule"},
    )
    class InternalAccessConfigurationProperty:
        def __init__(
            self,
            *,
            internal_access_analysis_rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnalyzerPropsMixin.InternalAccessAnalysisRuleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the configuration of an internal access analyzer for an AWS organization or account.

            This configuration determines how the analyzer evaluates internal access within your AWS environment.

            :param internal_access_analysis_rule: Contains information about analysis rules for the internal access analyzer. These rules determine which resources and access patterns will be analyzed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-accessanalyzer-analyzer-internalaccessconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_accessanalyzer import mixins as accessanalyzer_mixins
                
                internal_access_configuration_property = accessanalyzer_mixins.CfnAnalyzerPropsMixin.InternalAccessConfigurationProperty(
                    internal_access_analysis_rule=accessanalyzer_mixins.CfnAnalyzerPropsMixin.InternalAccessAnalysisRuleProperty(
                        inclusions=[accessanalyzer_mixins.CfnAnalyzerPropsMixin.InternalAccessAnalysisRuleCriteriaProperty(
                            account_ids=["accountIds"],
                            resource_arns=["resourceArns"],
                            resource_types=["resourceTypes"]
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f25d461ddf3d2bf0431f9cf2861cb46e2ce9cc03357928ec0a83ec31cd54faeb)
                check_type(argname="argument internal_access_analysis_rule", value=internal_access_analysis_rule, expected_type=type_hints["internal_access_analysis_rule"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if internal_access_analysis_rule is not None:
                self._values["internal_access_analysis_rule"] = internal_access_analysis_rule

        @builtins.property
        def internal_access_analysis_rule(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnalyzerPropsMixin.InternalAccessAnalysisRuleProperty"]]:
            '''Contains information about analysis rules for the internal access analyzer.

            These rules determine which resources and access patterns will be analyzed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-accessanalyzer-analyzer-internalaccessconfiguration.html#cfn-accessanalyzer-analyzer-internalaccessconfiguration-internalaccessanalysisrule
            '''
            result = self._values.get("internal_access_analysis_rule")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnalyzerPropsMixin.InternalAccessAnalysisRuleProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InternalAccessConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_accessanalyzer.mixins.CfnAnalyzerPropsMixin.UnusedAccessConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "analysis_rule": "analysisRule",
            "unused_access_age": "unusedAccessAge",
        },
    )
    class UnusedAccessConfigurationProperty:
        def __init__(
            self,
            *,
            analysis_rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnalyzerPropsMixin.AnalysisRuleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            unused_access_age: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Contains information about an unused access analyzer.

            :param analysis_rule: Contains information about analysis rules for the analyzer. Analysis rules determine which entities will generate findings based on the criteria you define when you create the rule.
            :param unused_access_age: The specified access age in days for which to generate findings for unused access. For example, if you specify 90 days, the analyzer will generate findings for IAM entities within the accounts of the selected organization for any access that hasn't been used in 90 or more days since the analyzer's last scan. You can choose a value between 1 and 365 days.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-accessanalyzer-analyzer-unusedaccessconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_accessanalyzer import mixins as accessanalyzer_mixins
                
                unused_access_configuration_property = accessanalyzer_mixins.CfnAnalyzerPropsMixin.UnusedAccessConfigurationProperty(
                    analysis_rule=accessanalyzer_mixins.CfnAnalyzerPropsMixin.AnalysisRuleProperty(
                        exclusions=[accessanalyzer_mixins.CfnAnalyzerPropsMixin.AnalysisRuleCriteriaProperty(
                            account_ids=["accountIds"],
                            resource_tags=[[CfnTag(
                                key="key",
                                value="value"
                            )]]
                        )]
                    ),
                    unused_access_age=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__09a6c9bbd13e303d59381f198968cc80980df6fcece450f7205c3ff9f3966d10)
                check_type(argname="argument analysis_rule", value=analysis_rule, expected_type=type_hints["analysis_rule"])
                check_type(argname="argument unused_access_age", value=unused_access_age, expected_type=type_hints["unused_access_age"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if analysis_rule is not None:
                self._values["analysis_rule"] = analysis_rule
            if unused_access_age is not None:
                self._values["unused_access_age"] = unused_access_age

        @builtins.property
        def analysis_rule(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnalyzerPropsMixin.AnalysisRuleProperty"]]:
            '''Contains information about analysis rules for the analyzer.

            Analysis rules determine which entities will generate findings based on the criteria you define when you create the rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-accessanalyzer-analyzer-unusedaccessconfiguration.html#cfn-accessanalyzer-analyzer-unusedaccessconfiguration-analysisrule
            '''
            result = self._values.get("analysis_rule")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnalyzerPropsMixin.AnalysisRuleProperty"]], result)

        @builtins.property
        def unused_access_age(self) -> typing.Optional[jsii.Number]:
            '''The specified access age in days for which to generate findings for unused access.

            For example, if you specify 90 days, the analyzer will generate findings for IAM entities within the accounts of the selected organization for any access that hasn't been used in 90 or more days since the analyzer's last scan. You can choose a value between 1 and 365 days.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-accessanalyzer-analyzer-unusedaccessconfiguration.html#cfn-accessanalyzer-analyzer-unusedaccessconfiguration-unusedaccessage
            '''
            result = self._values.get("unused_access_age")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UnusedAccessConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnAnalyzerMixinProps",
    "CfnAnalyzerPropsMixin",
]

publication.publish()

def _typecheckingstub__69fe1cc1bbe2826083f4ee05e71a9fc2303244fb87cee4549b48d13c0b6235c8(
    *,
    analyzer_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnalyzerPropsMixin.AnalyzerConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    analyzer_name: typing.Optional[builtins.str] = None,
    archive_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnalyzerPropsMixin.ArchiveRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c954668bed59f02d0ad7a4f0cce23933f30f54c8a2277a899fd301bf10fb72a5(
    props: typing.Union[CfnAnalyzerMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de7ff3894a64c3aef10f8ae4471c5f5a07e421a98588e81226f0772315d77d5c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aad9a902683682e41db2008f65d2bea9839fd3e4b60983c60cba6c02232e6f8b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a680f076761a0597e3aaddcc7166caf3caec05a619e1195d2dceba8551ecd12(
    *,
    account_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16d2d9b6c92c88259edbcc34ed666d0f0a5ff14ab379a87467d3cb260395b67a(
    *,
    exclusions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnalyzerPropsMixin.AnalysisRuleCriteriaProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b07bd627a1c24a0750233c2e89396c510ac157b0dc9ddcf581a741e967c4284(
    *,
    internal_access_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnalyzerPropsMixin.InternalAccessConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    unused_access_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnalyzerPropsMixin.UnusedAccessConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__272719439db4cbd7291b417ed0ad293655accb73a00dd9a564f341752ff515bf(
    *,
    filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnalyzerPropsMixin.FilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a185b96fc89197b05a8a3c2eee316a77d7cedf2686c4f60d796bd6818316ba85(
    *,
    contains: typing.Optional[typing.Sequence[builtins.str]] = None,
    eq: typing.Optional[typing.Sequence[builtins.str]] = None,
    exists: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    neq: typing.Optional[typing.Sequence[builtins.str]] = None,
    property: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae1f64c3f69ed6b67655be091919b5e466e4ab60aad5998c44186b78c29ac7d3(
    *,
    account_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5080dec50c510d1f00f43d5ada29136552cc05561b525c6ec5961c0aa0f7df30(
    *,
    inclusions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnalyzerPropsMixin.InternalAccessAnalysisRuleCriteriaProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f25d461ddf3d2bf0431f9cf2861cb46e2ce9cc03357928ec0a83ec31cd54faeb(
    *,
    internal_access_analysis_rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnalyzerPropsMixin.InternalAccessAnalysisRuleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09a6c9bbd13e303d59381f198968cc80980df6fcece450f7205c3ff9f3966d10(
    *,
    analysis_rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnalyzerPropsMixin.AnalysisRuleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    unused_access_age: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
