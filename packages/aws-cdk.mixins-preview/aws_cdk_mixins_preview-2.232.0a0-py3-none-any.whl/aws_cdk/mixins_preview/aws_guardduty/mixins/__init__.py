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
    jsii_type="@aws-cdk/mixins-preview.aws_guardduty.mixins.CfnDetectorMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "data_sources": "dataSources",
        "enable": "enable",
        "features": "features",
        "finding_publishing_frequency": "findingPublishingFrequency",
        "tags": "tags",
    },
)
class CfnDetectorMixinProps:
    def __init__(
        self,
        *,
        data_sources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorPropsMixin.CFNDataSourceConfigurationsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        enable: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        features: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorPropsMixin.CFNFeatureConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        finding_publishing_frequency: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["CfnDetectorPropsMixin.TagItemProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDetectorPropsMixin.

        :param data_sources: Describes which data sources will be enabled for the detector.
        :param enable: Specifies whether the detector is to be enabled on creation.
        :param features: A list of features that will be configured for the detector.
        :param finding_publishing_frequency: Specifies how frequently updated findings are exported.
        :param tags: Specifies tags added to a new detector resource. Each tag consists of a key and an optional value, both of which you define. Currently, support is available only for creating and deleting a tag. No support exists for updating the tags. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-detector.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_guardduty import mixins as guardduty_mixins
            
            cfn_detector_mixin_props = guardduty_mixins.CfnDetectorMixinProps(
                data_sources=guardduty_mixins.CfnDetectorPropsMixin.CFNDataSourceConfigurationsProperty(
                    kubernetes=guardduty_mixins.CfnDetectorPropsMixin.CFNKubernetesConfigurationProperty(
                        audit_logs=guardduty_mixins.CfnDetectorPropsMixin.CFNKubernetesAuditLogsConfigurationProperty(
                            enable=False
                        )
                    ),
                    malware_protection=guardduty_mixins.CfnDetectorPropsMixin.CFNMalwareProtectionConfigurationProperty(
                        scan_ec2_instance_with_findings=guardduty_mixins.CfnDetectorPropsMixin.CFNScanEc2InstanceWithFindingsConfigurationProperty(
                            ebs_volumes=False
                        )
                    ),
                    s3_logs=guardduty_mixins.CfnDetectorPropsMixin.CFNS3LogsConfigurationProperty(
                        enable=False
                    )
                ),
                enable=False,
                features=[guardduty_mixins.CfnDetectorPropsMixin.CFNFeatureConfigurationProperty(
                    additional_configuration=[guardduty_mixins.CfnDetectorPropsMixin.CFNFeatureAdditionalConfigurationProperty(
                        name="name",
                        status="status"
                    )],
                    name="name",
                    status="status"
                )],
                finding_publishing_frequency="findingPublishingFrequency",
                tags=[guardduty_mixins.CfnDetectorPropsMixin.TagItemProperty(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__883a81dafcde9c0df87748169824f5a372f2c64055971e3969497cb73f7536c5)
            check_type(argname="argument data_sources", value=data_sources, expected_type=type_hints["data_sources"])
            check_type(argname="argument enable", value=enable, expected_type=type_hints["enable"])
            check_type(argname="argument features", value=features, expected_type=type_hints["features"])
            check_type(argname="argument finding_publishing_frequency", value=finding_publishing_frequency, expected_type=type_hints["finding_publishing_frequency"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data_sources is not None:
            self._values["data_sources"] = data_sources
        if enable is not None:
            self._values["enable"] = enable
        if features is not None:
            self._values["features"] = features
        if finding_publishing_frequency is not None:
            self._values["finding_publishing_frequency"] = finding_publishing_frequency
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def data_sources(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorPropsMixin.CFNDataSourceConfigurationsProperty"]]:
        '''Describes which data sources will be enabled for the detector.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-detector.html#cfn-guardduty-detector-datasources
        '''
        result = self._values.get("data_sources")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorPropsMixin.CFNDataSourceConfigurationsProperty"]], result)

    @builtins.property
    def enable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether the detector is to be enabled on creation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-detector.html#cfn-guardduty-detector-enable
        '''
        result = self._values.get("enable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def features(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorPropsMixin.CFNFeatureConfigurationProperty"]]]]:
        '''A list of features that will be configured for the detector.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-detector.html#cfn-guardduty-detector-features
        '''
        result = self._values.get("features")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorPropsMixin.CFNFeatureConfigurationProperty"]]]], result)

    @builtins.property
    def finding_publishing_frequency(self) -> typing.Optional[builtins.str]:
        '''Specifies how frequently updated findings are exported.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-detector.html#cfn-guardduty-detector-findingpublishingfrequency
        '''
        result = self._values.get("finding_publishing_frequency")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(
        self,
    ) -> typing.Optional[typing.List["CfnDetectorPropsMixin.TagItemProperty"]]:
        '''Specifies tags added to a new detector resource.

        Each tag consists of a key and an optional value, both of which you define.

        Currently, support is available only for creating and deleting a tag. No support exists for updating the tags.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-detector.html#cfn-guardduty-detector-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["CfnDetectorPropsMixin.TagItemProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDetectorMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDetectorPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_guardduty.mixins.CfnDetectorPropsMixin",
):
    '''The ``AWS::GuardDuty::Detector`` resource specifies a new GuardDuty detector.

    A detector is an object that represents the GuardDuty service. A detector is required for GuardDuty to become operational.

    Make sure you use either ``DataSources`` or ``Features`` in a one request, and not both.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-detector.html
    :cloudformationResource: AWS::GuardDuty::Detector
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_guardduty import mixins as guardduty_mixins
        
        cfn_detector_props_mixin = guardduty_mixins.CfnDetectorPropsMixin(guardduty_mixins.CfnDetectorMixinProps(
            data_sources=guardduty_mixins.CfnDetectorPropsMixin.CFNDataSourceConfigurationsProperty(
                kubernetes=guardduty_mixins.CfnDetectorPropsMixin.CFNKubernetesConfigurationProperty(
                    audit_logs=guardduty_mixins.CfnDetectorPropsMixin.CFNKubernetesAuditLogsConfigurationProperty(
                        enable=False
                    )
                ),
                malware_protection=guardduty_mixins.CfnDetectorPropsMixin.CFNMalwareProtectionConfigurationProperty(
                    scan_ec2_instance_with_findings=guardduty_mixins.CfnDetectorPropsMixin.CFNScanEc2InstanceWithFindingsConfigurationProperty(
                        ebs_volumes=False
                    )
                ),
                s3_logs=guardduty_mixins.CfnDetectorPropsMixin.CFNS3LogsConfigurationProperty(
                    enable=False
                )
            ),
            enable=False,
            features=[guardduty_mixins.CfnDetectorPropsMixin.CFNFeatureConfigurationProperty(
                additional_configuration=[guardduty_mixins.CfnDetectorPropsMixin.CFNFeatureAdditionalConfigurationProperty(
                    name="name",
                    status="status"
                )],
                name="name",
                status="status"
            )],
            finding_publishing_frequency="findingPublishingFrequency",
            tags=[guardduty_mixins.CfnDetectorPropsMixin.TagItemProperty(
                key="key",
                value="value"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDetectorMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::GuardDuty::Detector``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e641b1bb9ee99d91ab515c406437f8d04952f6280c85a1ffb30272c76330e1cf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4591c02ade0b3d68bc05f2f350460ca2f3b1b9e4c909cb285e27cb5c4e4b2f7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__474f74b1a1bac845e9cec0456f64075ff8ab23d679218bdd5a0cffa6eb053d61)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDetectorMixinProps:
        return typing.cast(CfnDetectorMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_guardduty.mixins.CfnDetectorPropsMixin.CFNDataSourceConfigurationsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "kubernetes": "kubernetes",
            "malware_protection": "malwareProtection",
            "s3_logs": "s3Logs",
        },
    )
    class CFNDataSourceConfigurationsProperty:
        def __init__(
            self,
            *,
            kubernetes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorPropsMixin.CFNKubernetesConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            malware_protection: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorPropsMixin.CFNMalwareProtectionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3_logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorPropsMixin.CFNS3LogsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes whether S3 data event logs, Kubernetes audit logs, or Malware Protection will be enabled as a data source when the detector is created.

            :param kubernetes: Describes which Kubernetes data sources are enabled for a detector.
            :param malware_protection: Describes whether Malware Protection will be enabled as a data source.
            :param s3_logs: Describes whether S3 data event logs are enabled as a data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-detector-cfndatasourceconfigurations.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_guardduty import mixins as guardduty_mixins
                
                c_fNData_source_configurations_property = guardduty_mixins.CfnDetectorPropsMixin.CFNDataSourceConfigurationsProperty(
                    kubernetes=guardduty_mixins.CfnDetectorPropsMixin.CFNKubernetesConfigurationProperty(
                        audit_logs=guardduty_mixins.CfnDetectorPropsMixin.CFNKubernetesAuditLogsConfigurationProperty(
                            enable=False
                        )
                    ),
                    malware_protection=guardduty_mixins.CfnDetectorPropsMixin.CFNMalwareProtectionConfigurationProperty(
                        scan_ec2_instance_with_findings=guardduty_mixins.CfnDetectorPropsMixin.CFNScanEc2InstanceWithFindingsConfigurationProperty(
                            ebs_volumes=False
                        )
                    ),
                    s3_logs=guardduty_mixins.CfnDetectorPropsMixin.CFNS3LogsConfigurationProperty(
                        enable=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4ebed8bbda351905c6308ac86e49fa325502088a6a87674326026a9beebdb1d0)
                check_type(argname="argument kubernetes", value=kubernetes, expected_type=type_hints["kubernetes"])
                check_type(argname="argument malware_protection", value=malware_protection, expected_type=type_hints["malware_protection"])
                check_type(argname="argument s3_logs", value=s3_logs, expected_type=type_hints["s3_logs"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kubernetes is not None:
                self._values["kubernetes"] = kubernetes
            if malware_protection is not None:
                self._values["malware_protection"] = malware_protection
            if s3_logs is not None:
                self._values["s3_logs"] = s3_logs

        @builtins.property
        def kubernetes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorPropsMixin.CFNKubernetesConfigurationProperty"]]:
            '''Describes which Kubernetes data sources are enabled for a detector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-detector-cfndatasourceconfigurations.html#cfn-guardduty-detector-cfndatasourceconfigurations-kubernetes
            '''
            result = self._values.get("kubernetes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorPropsMixin.CFNKubernetesConfigurationProperty"]], result)

        @builtins.property
        def malware_protection(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorPropsMixin.CFNMalwareProtectionConfigurationProperty"]]:
            '''Describes whether Malware Protection will be enabled as a data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-detector-cfndatasourceconfigurations.html#cfn-guardduty-detector-cfndatasourceconfigurations-malwareprotection
            '''
            result = self._values.get("malware_protection")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorPropsMixin.CFNMalwareProtectionConfigurationProperty"]], result)

        @builtins.property
        def s3_logs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorPropsMixin.CFNS3LogsConfigurationProperty"]]:
            '''Describes whether S3 data event logs are enabled as a data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-detector-cfndatasourceconfigurations.html#cfn-guardduty-detector-cfndatasourceconfigurations-s3logs
            '''
            result = self._values.get("s3_logs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorPropsMixin.CFNS3LogsConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CFNDataSourceConfigurationsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_guardduty.mixins.CfnDetectorPropsMixin.CFNFeatureAdditionalConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "status": "status"},
    )
    class CFNFeatureAdditionalConfigurationProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            status: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about the additional configuration of a feature in your account.

            :param name: Name of the additional configuration.
            :param status: Status of the additional configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-detector-cfnfeatureadditionalconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_guardduty import mixins as guardduty_mixins
                
                c_fNFeature_additional_configuration_property = guardduty_mixins.CfnDetectorPropsMixin.CFNFeatureAdditionalConfigurationProperty(
                    name="name",
                    status="status"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e2fa0f3322dda3edcf62b73ef7b47a1a1bb13236ce13981c0ef955da6716609c)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''Name of the additional configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-detector-cfnfeatureadditionalconfiguration.html#cfn-guardduty-detector-cfnfeatureadditionalconfiguration-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''Status of the additional configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-detector-cfnfeatureadditionalconfiguration.html#cfn-guardduty-detector-cfnfeatureadditionalconfiguration-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CFNFeatureAdditionalConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_guardduty.mixins.CfnDetectorPropsMixin.CFNFeatureConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "additional_configuration": "additionalConfiguration",
            "name": "name",
            "status": "status",
        },
    )
    class CFNFeatureConfigurationProperty:
        def __init__(
            self,
            *,
            additional_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorPropsMixin.CFNFeatureAdditionalConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            name: typing.Optional[builtins.str] = None,
            status: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about the configuration of a feature in your account.

            :param additional_configuration: Information about the additional configuration of a feature in your account.
            :param name: Name of the feature. For a list of allowed values, see `DetectorFeatureConfiguration <https://docs.aws.amazon.com/guardduty/latest/APIReference/API_DetectorFeatureConfiguration.html#guardduty-Type-DetectorFeatureConfiguration-name>`_ in the *GuardDuty API Reference* .
            :param status: Status of the feature configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-detector-cfnfeatureconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_guardduty import mixins as guardduty_mixins
                
                c_fNFeature_configuration_property = guardduty_mixins.CfnDetectorPropsMixin.CFNFeatureConfigurationProperty(
                    additional_configuration=[guardduty_mixins.CfnDetectorPropsMixin.CFNFeatureAdditionalConfigurationProperty(
                        name="name",
                        status="status"
                    )],
                    name="name",
                    status="status"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4d616d1cb7fa440b8d453f6d7739b4904c87a97d4a37cdd2c66c89236f15ecba)
                check_type(argname="argument additional_configuration", value=additional_configuration, expected_type=type_hints["additional_configuration"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if additional_configuration is not None:
                self._values["additional_configuration"] = additional_configuration
            if name is not None:
                self._values["name"] = name
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def additional_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorPropsMixin.CFNFeatureAdditionalConfigurationProperty"]]]]:
            '''Information about the additional configuration of a feature in your account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-detector-cfnfeatureconfiguration.html#cfn-guardduty-detector-cfnfeatureconfiguration-additionalconfiguration
            '''
            result = self._values.get("additional_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorPropsMixin.CFNFeatureAdditionalConfigurationProperty"]]]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''Name of the feature.

            For a list of allowed values, see `DetectorFeatureConfiguration <https://docs.aws.amazon.com/guardduty/latest/APIReference/API_DetectorFeatureConfiguration.html#guardduty-Type-DetectorFeatureConfiguration-name>`_ in the *GuardDuty API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-detector-cfnfeatureconfiguration.html#cfn-guardduty-detector-cfnfeatureconfiguration-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''Status of the feature configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-detector-cfnfeatureconfiguration.html#cfn-guardduty-detector-cfnfeatureconfiguration-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CFNFeatureConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_guardduty.mixins.CfnDetectorPropsMixin.CFNKubernetesAuditLogsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"enable": "enable"},
    )
    class CFNKubernetesAuditLogsConfigurationProperty:
        def __init__(
            self,
            *,
            enable: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Describes which optional data sources are enabled for a detector.

            :param enable: Describes whether Kubernetes audit logs are enabled as a data source for the detector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-detector-cfnkubernetesauditlogsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_guardduty import mixins as guardduty_mixins
                
                c_fNKubernetes_audit_logs_configuration_property = guardduty_mixins.CfnDetectorPropsMixin.CFNKubernetesAuditLogsConfigurationProperty(
                    enable=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__95ff04533e66480f5035ba8148238dc8712c42f344f9ceccf9de72f89ece9713)
                check_type(argname="argument enable", value=enable, expected_type=type_hints["enable"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enable is not None:
                self._values["enable"] = enable

        @builtins.property
        def enable(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Describes whether Kubernetes audit logs are enabled as a data source for the detector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-detector-cfnkubernetesauditlogsconfiguration.html#cfn-guardduty-detector-cfnkubernetesauditlogsconfiguration-enable
            '''
            result = self._values.get("enable")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CFNKubernetesAuditLogsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_guardduty.mixins.CfnDetectorPropsMixin.CFNKubernetesConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"audit_logs": "auditLogs"},
    )
    class CFNKubernetesConfigurationProperty:
        def __init__(
            self,
            *,
            audit_logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorPropsMixin.CFNKubernetesAuditLogsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes which Kubernetes protection data sources are enabled for the detector.

            :param audit_logs: Describes whether Kubernetes audit logs are enabled as a data source for the detector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-detector-cfnkubernetesconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_guardduty import mixins as guardduty_mixins
                
                c_fNKubernetes_configuration_property = guardduty_mixins.CfnDetectorPropsMixin.CFNKubernetesConfigurationProperty(
                    audit_logs=guardduty_mixins.CfnDetectorPropsMixin.CFNKubernetesAuditLogsConfigurationProperty(
                        enable=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e632566480af702f64343b47a487909e4e98891488b4cd186cf14827b9dd0424)
                check_type(argname="argument audit_logs", value=audit_logs, expected_type=type_hints["audit_logs"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if audit_logs is not None:
                self._values["audit_logs"] = audit_logs

        @builtins.property
        def audit_logs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorPropsMixin.CFNKubernetesAuditLogsConfigurationProperty"]]:
            '''Describes whether Kubernetes audit logs are enabled as a data source for the detector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-detector-cfnkubernetesconfiguration.html#cfn-guardduty-detector-cfnkubernetesconfiguration-auditlogs
            '''
            result = self._values.get("audit_logs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorPropsMixin.CFNKubernetesAuditLogsConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CFNKubernetesConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_guardduty.mixins.CfnDetectorPropsMixin.CFNMalwareProtectionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "scan_ec2_instance_with_findings": "scanEc2InstanceWithFindings",
        },
    )
    class CFNMalwareProtectionConfigurationProperty:
        def __init__(
            self,
            *,
            scan_ec2_instance_with_findings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorPropsMixin.CFNScanEc2InstanceWithFindingsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes whether Malware Protection will be enabled as a data source.

            :param scan_ec2_instance_with_findings: Describes the configuration of Malware Protection for EC2 instances with findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-detector-cfnmalwareprotectionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_guardduty import mixins as guardduty_mixins
                
                c_fNMalware_protection_configuration_property = guardduty_mixins.CfnDetectorPropsMixin.CFNMalwareProtectionConfigurationProperty(
                    scan_ec2_instance_with_findings=guardduty_mixins.CfnDetectorPropsMixin.CFNScanEc2InstanceWithFindingsConfigurationProperty(
                        ebs_volumes=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e2a2f6a537ab08c20166671c5df08a2c27900200abae4b70f03f890f607850b4)
                check_type(argname="argument scan_ec2_instance_with_findings", value=scan_ec2_instance_with_findings, expected_type=type_hints["scan_ec2_instance_with_findings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if scan_ec2_instance_with_findings is not None:
                self._values["scan_ec2_instance_with_findings"] = scan_ec2_instance_with_findings

        @builtins.property
        def scan_ec2_instance_with_findings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorPropsMixin.CFNScanEc2InstanceWithFindingsConfigurationProperty"]]:
            '''Describes the configuration of Malware Protection for EC2 instances with findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-detector-cfnmalwareprotectionconfiguration.html#cfn-guardduty-detector-cfnmalwareprotectionconfiguration-scanec2instancewithfindings
            '''
            result = self._values.get("scan_ec2_instance_with_findings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorPropsMixin.CFNScanEc2InstanceWithFindingsConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CFNMalwareProtectionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_guardduty.mixins.CfnDetectorPropsMixin.CFNS3LogsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"enable": "enable"},
    )
    class CFNS3LogsConfigurationProperty:
        def __init__(
            self,
            *,
            enable: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Describes whether S3 data event logs will be enabled as a data source when the detector is created.

            :param enable: The status of S3 data event logs as a data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-detector-cfns3logsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_guardduty import mixins as guardduty_mixins
                
                c_fNS3_logs_configuration_property = guardduty_mixins.CfnDetectorPropsMixin.CFNS3LogsConfigurationProperty(
                    enable=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7f3797b3ffcb5cfc99ece164da8daa052159ec8977c923b8ff4f683c09dbf9a9)
                check_type(argname="argument enable", value=enable, expected_type=type_hints["enable"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enable is not None:
                self._values["enable"] = enable

        @builtins.property
        def enable(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''The status of S3 data event logs as a data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-detector-cfns3logsconfiguration.html#cfn-guardduty-detector-cfns3logsconfiguration-enable
            '''
            result = self._values.get("enable")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CFNS3LogsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_guardduty.mixins.CfnDetectorPropsMixin.CFNScanEc2InstanceWithFindingsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"ebs_volumes": "ebsVolumes"},
    )
    class CFNScanEc2InstanceWithFindingsConfigurationProperty:
        def __init__(
            self,
            *,
            ebs_volumes: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Describes whether Malware Protection for EC2 instances with findings will be enabled as a data source.

            :param ebs_volumes: Describes the configuration for scanning EBS volumes as data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-detector-cfnscanec2instancewithfindingsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_guardduty import mixins as guardduty_mixins
                
                c_fNScan_ec2_instance_with_findings_configuration_property = guardduty_mixins.CfnDetectorPropsMixin.CFNScanEc2InstanceWithFindingsConfigurationProperty(
                    ebs_volumes=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2d0e3c9488519266dbc05874572f219eb1c737d6a893c0904f7ef16f1aa72b7b)
                check_type(argname="argument ebs_volumes", value=ebs_volumes, expected_type=type_hints["ebs_volumes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ebs_volumes is not None:
                self._values["ebs_volumes"] = ebs_volumes

        @builtins.property
        def ebs_volumes(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Describes the configuration for scanning EBS volumes as data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-detector-cfnscanec2instancewithfindingsconfiguration.html#cfn-guardduty-detector-cfnscanec2instancewithfindingsconfiguration-ebsvolumes
            '''
            result = self._values.get("ebs_volumes")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CFNScanEc2InstanceWithFindingsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_guardduty.mixins.CfnDetectorPropsMixin.TagItemProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TagItemProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes a tag.

            :param key: The tag key.
            :param value: The tag value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-detector-tagitem.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_guardduty import mixins as guardduty_mixins
                
                tag_item_property = guardduty_mixins.CfnDetectorPropsMixin.TagItemProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8a506433312af4b47d43e1d5d45eef146484d84624a1ccefd6473e4503a5e96c)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The tag key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-detector-tagitem.html#cfn-guardduty-detector-tagitem-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The tag value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-detector-tagitem.html#cfn-guardduty-detector-tagitem-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagItemProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_guardduty.mixins.CfnFilterMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "description": "description",
        "detector_id": "detectorId",
        "finding_criteria": "findingCriteria",
        "name": "name",
        "rank": "rank",
        "tags": "tags",
    },
)
class CfnFilterMixinProps:
    def __init__(
        self,
        *,
        action: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        detector_id: typing.Optional[builtins.str] = None,
        finding_criteria: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.FindingCriteriaProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        rank: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnFilterPropsMixin.

        :param action: Specifies the action that is to be applied to the findings that match the filter.
        :param description: The description of the filter. Valid characters include alphanumeric characters, and special characters such as hyphen, period, colon, underscore, parentheses ( ``{ }`` , ``[ ]`` , and ``( )`` ), forward slash, horizontal tab, vertical tab, newline, form feed, return, and whitespace.
        :param detector_id: The detector ID associated with the GuardDuty account for which you want to create a filter. To find the ``detectorId`` in the current Region, see the Settings page in the GuardDuty console, or run the `ListDetectors <https://docs.aws.amazon.com/guardduty/latest/APIReference/API_ListDetectors.html>`_ API.
        :param finding_criteria: Represents the criteria to be used in the filter for querying findings.
        :param name: The name of the filter. Valid characters include period (.), underscore (_), dash (-), and alphanumeric characters. A whitespace is considered to be an invalid character.
        :param rank: Specifies the position of the filter in the list of current filters. Also specifies the order in which this filter is applied to the findings. The minimum value for this property is 1 and the maximum is 100. By default, filters may not be created in the same order as they are ranked. To ensure that the filters are created in the expected order, you can use an optional attribute, `DependsOn <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html>`_ , with the following syntax: ``"DependsOn":[ "ObjectName" ]`` .
        :param tags: The tags to be added to a new filter resource. Each tag consists of a key and an optional value, both of which you define. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-filter.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_guardduty import mixins as guardduty_mixins
            
            # criterion: Any
            
            cfn_filter_mixin_props = guardduty_mixins.CfnFilterMixinProps(
                action="action",
                description="description",
                detector_id="detectorId",
                finding_criteria=guardduty_mixins.CfnFilterPropsMixin.FindingCriteriaProperty(
                    criterion=criterion,
                    item_type=guardduty_mixins.CfnFilterPropsMixin.ConditionProperty(
                        eq=["eq"],
                        equal_to=["equalTo"],
                        greater_than=123,
                        greater_than_or_equal=123,
                        gt=123,
                        gte=123,
                        less_than=123,
                        less_than_or_equal=123,
                        lt=123,
                        lte=123,
                        neq=["neq"],
                        not_equals=["notEquals"]
                    )
                ),
                name="name",
                rank=123,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7945b40d785a0cf11bbe2d3ee3b2b0c249e8182e1718a3b79b3af54ae5b33ed5)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument detector_id", value=detector_id, expected_type=type_hints["detector_id"])
            check_type(argname="argument finding_criteria", value=finding_criteria, expected_type=type_hints["finding_criteria"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument rank", value=rank, expected_type=type_hints["rank"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action is not None:
            self._values["action"] = action
        if description is not None:
            self._values["description"] = description
        if detector_id is not None:
            self._values["detector_id"] = detector_id
        if finding_criteria is not None:
            self._values["finding_criteria"] = finding_criteria
        if name is not None:
            self._values["name"] = name
        if rank is not None:
            self._values["rank"] = rank
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def action(self) -> typing.Optional[builtins.str]:
        '''Specifies the action that is to be applied to the findings that match the filter.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-filter.html#cfn-guardduty-filter-action
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the filter.

        Valid characters include alphanumeric characters, and special characters such as hyphen, period, colon, underscore, parentheses ( ``{ }`` , ``[ ]`` , and ``( )`` ), forward slash, horizontal tab, vertical tab, newline, form feed, return, and whitespace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-filter.html#cfn-guardduty-filter-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def detector_id(self) -> typing.Optional[builtins.str]:
        '''The detector ID associated with the GuardDuty account for which you want to create a filter.

        To find the ``detectorId`` in the current Region, see the
        Settings page in the GuardDuty console, or run the `ListDetectors <https://docs.aws.amazon.com/guardduty/latest/APIReference/API_ListDetectors.html>`_ API.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-filter.html#cfn-guardduty-filter-detectorid
        '''
        result = self._values.get("detector_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def finding_criteria(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.FindingCriteriaProperty"]]:
        '''Represents the criteria to be used in the filter for querying findings.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-filter.html#cfn-guardduty-filter-findingcriteria
        '''
        result = self._values.get("finding_criteria")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.FindingCriteriaProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the filter.

        Valid characters include period (.), underscore (_), dash (-), and alphanumeric characters. A whitespace is considered to be an invalid character.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-filter.html#cfn-guardduty-filter-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rank(self) -> typing.Optional[jsii.Number]:
        '''Specifies the position of the filter in the list of current filters.

        Also specifies the order in which this filter is applied to the findings. The minimum value for this property is 1 and the maximum is 100.

        By default, filters may not be created in the same order as they are ranked. To ensure that the filters are created in the expected order, you can use an optional attribute, `DependsOn <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html>`_ , with the following syntax: ``"DependsOn":[ "ObjectName" ]`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-filter.html#cfn-guardduty-filter-rank
        '''
        result = self._values.get("rank")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags to be added to a new filter resource.

        Each tag consists of a key and an optional value, both of which you define.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-filter.html#cfn-guardduty-filter-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFilterMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnFilterPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_guardduty.mixins.CfnFilterPropsMixin",
):
    '''The ``AWS::GuardDuty::Filter`` resource specifies a new filter defined by the provided ``findingCriteria`` .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-filter.html
    :cloudformationResource: AWS::GuardDuty::Filter
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_guardduty import mixins as guardduty_mixins
        
        # criterion: Any
        
        cfn_filter_props_mixin = guardduty_mixins.CfnFilterPropsMixin(guardduty_mixins.CfnFilterMixinProps(
            action="action",
            description="description",
            detector_id="detectorId",
            finding_criteria=guardduty_mixins.CfnFilterPropsMixin.FindingCriteriaProperty(
                criterion=criterion,
                item_type=guardduty_mixins.CfnFilterPropsMixin.ConditionProperty(
                    eq=["eq"],
                    equal_to=["equalTo"],
                    greater_than=123,
                    greater_than_or_equal=123,
                    gt=123,
                    gte=123,
                    less_than=123,
                    less_than_or_equal=123,
                    lt=123,
                    lte=123,
                    neq=["neq"],
                    not_equals=["notEquals"]
                )
            ),
            name="name",
            rank=123,
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
        props: typing.Union[CfnFilterMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::GuardDuty::Filter``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d53390215220d0bb24e5d5a000d54a98dc37b22827453ce3dcae59d293b5511)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7ba28f15e9760f66d37ed2f3ebbb3d8f71b1a6380826bde7d2452c119304c8e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f047a8bb6a932936ae560b57a4018c431ed763d1b23121c682ec23ebb59b79ec)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnFilterMixinProps:
        return typing.cast(CfnFilterMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_guardduty.mixins.CfnFilterPropsMixin.ConditionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "eq": "eq",
            "equal_to": "equalTo",
            "greater_than": "greaterThan",
            "greater_than_or_equal": "greaterThanOrEqual",
            "gt": "gt",
            "gte": "gte",
            "less_than": "lessThan",
            "less_than_or_equal": "lessThanOrEqual",
            "lt": "lt",
            "lte": "lte",
            "neq": "neq",
            "not_equals": "notEquals",
        },
    )
    class ConditionProperty:
        def __init__(
            self,
            *,
            eq: typing.Optional[typing.Sequence[builtins.str]] = None,
            equal_to: typing.Optional[typing.Sequence[builtins.str]] = None,
            greater_than: typing.Optional[jsii.Number] = None,
            greater_than_or_equal: typing.Optional[jsii.Number] = None,
            gt: typing.Optional[jsii.Number] = None,
            gte: typing.Optional[jsii.Number] = None,
            less_than: typing.Optional[jsii.Number] = None,
            less_than_or_equal: typing.Optional[jsii.Number] = None,
            lt: typing.Optional[jsii.Number] = None,
            lte: typing.Optional[jsii.Number] = None,
            neq: typing.Optional[typing.Sequence[builtins.str]] = None,
            not_equals: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Specifies the condition to apply to a single field when filtering through GuardDuty findings.

            :param eq: Represents the equal condition to apply to a single field when querying for findings.
            :param equal_to: Represents an *equal* ** condition to be applied to a single field when querying for findings.
            :param greater_than: Represents a *greater than* condition to be applied to a single field when querying for findings.
            :param greater_than_or_equal: Represents a *greater than or equal* condition to be applied to a single field when querying for findings.
            :param gt: Represents a *greater than* condition to be applied to a single field when querying for findings.
            :param gte: Represents the greater than or equal condition to apply to a single field when querying for findings.
            :param less_than: Represents a *less than* condition to be applied to a single field when querying for findings.
            :param less_than_or_equal: Represents a *less than or equal* condition to be applied to a single field when querying for findings.
            :param lt: Represents the less than condition to apply to a single field when querying for findings.
            :param lte: Represents the less than or equal condition to apply to a single field when querying for findings.
            :param neq: Represents the not equal condition to apply to a single field when querying for findings.
            :param not_equals: Represents a *not equal* ** condition to be applied to a single field when querying for findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-filter-condition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_guardduty import mixins as guardduty_mixins
                
                condition_property = guardduty_mixins.CfnFilterPropsMixin.ConditionProperty(
                    eq=["eq"],
                    equal_to=["equalTo"],
                    greater_than=123,
                    greater_than_or_equal=123,
                    gt=123,
                    gte=123,
                    less_than=123,
                    less_than_or_equal=123,
                    lt=123,
                    lte=123,
                    neq=["neq"],
                    not_equals=["notEquals"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0e376dbe045f0f43c5a64c2282b80d4355bb09dae69d8bf5b1c49ef5f2181a89)
                check_type(argname="argument eq", value=eq, expected_type=type_hints["eq"])
                check_type(argname="argument equal_to", value=equal_to, expected_type=type_hints["equal_to"])
                check_type(argname="argument greater_than", value=greater_than, expected_type=type_hints["greater_than"])
                check_type(argname="argument greater_than_or_equal", value=greater_than_or_equal, expected_type=type_hints["greater_than_or_equal"])
                check_type(argname="argument gt", value=gt, expected_type=type_hints["gt"])
                check_type(argname="argument gte", value=gte, expected_type=type_hints["gte"])
                check_type(argname="argument less_than", value=less_than, expected_type=type_hints["less_than"])
                check_type(argname="argument less_than_or_equal", value=less_than_or_equal, expected_type=type_hints["less_than_or_equal"])
                check_type(argname="argument lt", value=lt, expected_type=type_hints["lt"])
                check_type(argname="argument lte", value=lte, expected_type=type_hints["lte"])
                check_type(argname="argument neq", value=neq, expected_type=type_hints["neq"])
                check_type(argname="argument not_equals", value=not_equals, expected_type=type_hints["not_equals"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if eq is not None:
                self._values["eq"] = eq
            if equal_to is not None:
                self._values["equal_to"] = equal_to
            if greater_than is not None:
                self._values["greater_than"] = greater_than
            if greater_than_or_equal is not None:
                self._values["greater_than_or_equal"] = greater_than_or_equal
            if gt is not None:
                self._values["gt"] = gt
            if gte is not None:
                self._values["gte"] = gte
            if less_than is not None:
                self._values["less_than"] = less_than
            if less_than_or_equal is not None:
                self._values["less_than_or_equal"] = less_than_or_equal
            if lt is not None:
                self._values["lt"] = lt
            if lte is not None:
                self._values["lte"] = lte
            if neq is not None:
                self._values["neq"] = neq
            if not_equals is not None:
                self._values["not_equals"] = not_equals

        @builtins.property
        def eq(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Represents the equal condition to apply to a single field when querying for findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-filter-condition.html#cfn-guardduty-filter-condition-eq
            '''
            result = self._values.get("eq")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def equal_to(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Represents an *equal* ** condition to be applied to a single field when querying for findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-filter-condition.html#cfn-guardduty-filter-condition-equals
            '''
            result = self._values.get("equal_to")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def greater_than(self) -> typing.Optional[jsii.Number]:
            '''Represents a *greater than* condition to be applied to a single field when querying for findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-filter-condition.html#cfn-guardduty-filter-condition-greaterthan
            '''
            result = self._values.get("greater_than")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def greater_than_or_equal(self) -> typing.Optional[jsii.Number]:
            '''Represents a *greater than or equal* condition to be applied to a single field when querying for findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-filter-condition.html#cfn-guardduty-filter-condition-greaterthanorequal
            '''
            result = self._values.get("greater_than_or_equal")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def gt(self) -> typing.Optional[jsii.Number]:
            '''Represents a *greater than* condition to be applied to a single field when querying for findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-filter-condition.html#cfn-guardduty-filter-condition-gt
            '''
            result = self._values.get("gt")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def gte(self) -> typing.Optional[jsii.Number]:
            '''Represents the greater than or equal condition to apply to a single field when querying for findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-filter-condition.html#cfn-guardduty-filter-condition-gte
            '''
            result = self._values.get("gte")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def less_than(self) -> typing.Optional[jsii.Number]:
            '''Represents a *less than* condition to be applied to a single field when querying for findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-filter-condition.html#cfn-guardduty-filter-condition-lessthan
            '''
            result = self._values.get("less_than")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def less_than_or_equal(self) -> typing.Optional[jsii.Number]:
            '''Represents a *less than or equal* condition to be applied to a single field when querying for findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-filter-condition.html#cfn-guardduty-filter-condition-lessthanorequal
            '''
            result = self._values.get("less_than_or_equal")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def lt(self) -> typing.Optional[jsii.Number]:
            '''Represents the less than condition to apply to a single field when querying for findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-filter-condition.html#cfn-guardduty-filter-condition-lt
            '''
            result = self._values.get("lt")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def lte(self) -> typing.Optional[jsii.Number]:
            '''Represents the less than or equal condition to apply to a single field when querying for findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-filter-condition.html#cfn-guardduty-filter-condition-lte
            '''
            result = self._values.get("lte")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def neq(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Represents the not equal condition to apply to a single field when querying for findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-filter-condition.html#cfn-guardduty-filter-condition-neq
            '''
            result = self._values.get("neq")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def not_equals(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Represents a *not equal* ** condition to be applied to a single field when querying for findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-filter-condition.html#cfn-guardduty-filter-condition-notequals
            '''
            result = self._values.get("not_equals")
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
        jsii_type="@aws-cdk/mixins-preview.aws_guardduty.mixins.CfnFilterPropsMixin.FindingCriteriaProperty",
        jsii_struct_bases=[],
        name_mapping={"criterion": "criterion", "item_type": "itemType"},
    )
    class FindingCriteriaProperty:
        def __init__(
            self,
            *,
            criterion: typing.Any = None,
            item_type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.ConditionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Represents a map of finding properties that match specified conditions and values when querying findings.

            :param criterion: Represents a map of finding properties that match specified conditions and values when querying findings. For information about JSON criterion mapping to their console equivalent, see `Finding criteria <https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_filter-findings.html#filter_criteria>`_ . The following are the available criterion: - accountId - id - region - severity To filter on the basis of severity, the API and AWS CLI use the following input list for the ``FindingCriteria`` condition: - *Low* : ``["1", "2", "3"]`` - *Medium* : ``["4", "5", "6"]`` - *High* : ``["7", "8", "9"]`` For more information, see `Severity levels for GuardDuty findings <https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_findings.html#guardduty_findings-severity>`_ in the *Amazon GuardDuty User Guide* . - type - updatedAt Type: ISO 8601 string format: ``YYYY-MM-DDTHH:MM:SS.SSSZ`` or ``YYYY-MM-DDTHH:MM:SSZ`` depending on whether the value contains milliseconds. - resource.accessKeyDetails.accessKeyId - resource.accessKeyDetails.principalId - resource.accessKeyDetails.userName - resource.accessKeyDetails.userType - resource.instanceDetails.iamInstanceProfile.id - resource.instanceDetails.imageId - resource.instanceDetails.instanceId - resource.instanceDetails.tags.key - resource.instanceDetails.tags.value - resource.instanceDetails.networkInterfaces.ipv6Addresses - resource.instanceDetails.networkInterfaces.privateIpAddresses.privateIpAddress - resource.instanceDetails.networkInterfaces.publicDnsName - resource.instanceDetails.networkInterfaces.publicIp - resource.instanceDetails.networkInterfaces.securityGroups.groupId - resource.instanceDetails.networkInterfaces.securityGroups.groupName - resource.instanceDetails.networkInterfaces.subnetId - resource.instanceDetails.networkInterfaces.vpcId - resource.instanceDetails.outpostArn - resource.resourceType - resource.s3BucketDetails.publicAccess.effectivePermissions - resource.s3BucketDetails.name - resource.s3BucketDetails.tags.key - resource.s3BucketDetails.tags.value - resource.s3BucketDetails.type - service.action.actionType - service.action.awsApiCallAction.api - service.action.awsApiCallAction.callerType - service.action.awsApiCallAction.errorCode - service.action.awsApiCallAction.remoteIpDetails.city.cityName - service.action.awsApiCallAction.remoteIpDetails.country.countryName - service.action.awsApiCallAction.remoteIpDetails.ipAddressV4 - service.action.awsApiCallAction.remoteIpDetails.ipAddressV6 - service.action.awsApiCallAction.remoteIpDetails.organization.asn - service.action.awsApiCallAction.remoteIpDetails.organization.asnOrg - service.action.awsApiCallAction.serviceName - service.action.dnsRequestAction.domain - service.action.dnsRequestAction.domainWithSuffix - service.action.networkConnectionAction.blocked - service.action.networkConnectionAction.connectionDirection - service.action.networkConnectionAction.localPortDetails.port - service.action.networkConnectionAction.protocol - service.action.networkConnectionAction.remoteIpDetails.city.cityName - service.action.networkConnectionAction.remoteIpDetails.country.countryName - service.action.networkConnectionAction.remoteIpDetails.ipAddressV4 - service.action.networkConnectionAction.remoteIpDetails.ipAddressV6 - service.action.networkConnectionAction.remoteIpDetails.organization.asn - service.action.networkConnectionAction.remoteIpDetails.organization.asnOrg - service.action.networkConnectionAction.remotePortDetails.port - service.action.awsApiCallAction.remoteAccountDetails.affiliated - service.action.kubernetesApiCallAction.remoteIpDetails.ipAddressV4 - service.action.kubernetesApiCallAction.remoteIpDetails.ipAddressV6 - service.action.kubernetesApiCallAction.namespace - service.action.kubernetesApiCallAction.remoteIpDetails.organization.asn - service.action.kubernetesApiCallAction.requestUri - service.action.kubernetesApiCallAction.statusCode - service.action.networkConnectionAction.localIpDetails.ipAddressV4 - service.action.networkConnectionAction.localIpDetails.ipAddressV6 - service.action.networkConnectionAction.protocol - service.action.awsApiCallAction.serviceName - service.action.awsApiCallAction.remoteAccountDetails.accountId - service.additionalInfo.threatListName - service.resourceRole - resource.eksClusterDetails.name - resource.kubernetesDetails.kubernetesWorkloadDetails.name - resource.kubernetesDetails.kubernetesWorkloadDetails.namespace - resource.kubernetesDetails.kubernetesUserDetails.username - resource.kubernetesDetails.kubernetesWorkloadDetails.containers.image - resource.kubernetesDetails.kubernetesWorkloadDetails.containers.imagePrefix - service.ebsVolumeScanDetails.scanId - service.ebsVolumeScanDetails.scanDetections.threatDetectedByName.threatNames.name - service.ebsVolumeScanDetails.scanDetections.threatDetectedByName.threatNames.severity - service.ebsVolumeScanDetails.scanDetections.threatDetectedByName.threatNames.filePaths.hash - service.malwareScanDetails.threats.name - resource.ecsClusterDetails.name - resource.ecsClusterDetails.taskDetails.containers.image - resource.ecsClusterDetails.taskDetails.definitionArn - resource.containerDetails.image - resource.rdsDbInstanceDetails.dbInstanceIdentifier - resource.rdsDbInstanceDetails.dbClusterIdentifier - resource.rdsDbInstanceDetails.engine - resource.rdsDbUserDetails.user - resource.rdsDbInstanceDetails.tags.key - resource.rdsDbInstanceDetails.tags.value - service.runtimeDetails.process.executableSha256 - service.runtimeDetails.process.name - service.runtimeDetails.process.name - resource.lambdaDetails.functionName - resource.lambdaDetails.functionArn - resource.lambdaDetails.tags.key - resource.lambdaDetails.tags.value
            :param item_type: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-filter-findingcriteria.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_guardduty import mixins as guardduty_mixins
                
                # criterion: Any
                
                finding_criteria_property = guardduty_mixins.CfnFilterPropsMixin.FindingCriteriaProperty(
                    criterion=criterion,
                    item_type=guardduty_mixins.CfnFilterPropsMixin.ConditionProperty(
                        eq=["eq"],
                        equal_to=["equalTo"],
                        greater_than=123,
                        greater_than_or_equal=123,
                        gt=123,
                        gte=123,
                        less_than=123,
                        less_than_or_equal=123,
                        lt=123,
                        lte=123,
                        neq=["neq"],
                        not_equals=["notEquals"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__106802f46c9c141d4f3d013be3fe7492c389e46a8e6ef5702796e2c9e186ffae)
                check_type(argname="argument criterion", value=criterion, expected_type=type_hints["criterion"])
                check_type(argname="argument item_type", value=item_type, expected_type=type_hints["item_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if criterion is not None:
                self._values["criterion"] = criterion
            if item_type is not None:
                self._values["item_type"] = item_type

        @builtins.property
        def criterion(self) -> typing.Any:
            '''Represents a map of finding properties that match specified conditions and values when querying findings.

            For information about JSON criterion mapping to their console equivalent, see `Finding criteria <https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_filter-findings.html#filter_criteria>`_ . The following are the available criterion:

            - accountId
            - id
            - region
            - severity

            To filter on the basis of severity, the API and AWS CLI use the following input list for the ``FindingCriteria`` condition:

            - *Low* : ``["1", "2", "3"]``
            - *Medium* : ``["4", "5", "6"]``
            - *High* : ``["7", "8", "9"]``

            For more information, see `Severity levels for GuardDuty findings <https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_findings.html#guardduty_findings-severity>`_ in the *Amazon GuardDuty User Guide* .

            - type
            - updatedAt

            Type: ISO 8601 string format: ``YYYY-MM-DDTHH:MM:SS.SSSZ`` or ``YYYY-MM-DDTHH:MM:SSZ`` depending on whether the value contains milliseconds.

            - resource.accessKeyDetails.accessKeyId
            - resource.accessKeyDetails.principalId
            - resource.accessKeyDetails.userName
            - resource.accessKeyDetails.userType
            - resource.instanceDetails.iamInstanceProfile.id
            - resource.instanceDetails.imageId
            - resource.instanceDetails.instanceId
            - resource.instanceDetails.tags.key
            - resource.instanceDetails.tags.value
            - resource.instanceDetails.networkInterfaces.ipv6Addresses
            - resource.instanceDetails.networkInterfaces.privateIpAddresses.privateIpAddress
            - resource.instanceDetails.networkInterfaces.publicDnsName
            - resource.instanceDetails.networkInterfaces.publicIp
            - resource.instanceDetails.networkInterfaces.securityGroups.groupId
            - resource.instanceDetails.networkInterfaces.securityGroups.groupName
            - resource.instanceDetails.networkInterfaces.subnetId
            - resource.instanceDetails.networkInterfaces.vpcId
            - resource.instanceDetails.outpostArn
            - resource.resourceType
            - resource.s3BucketDetails.publicAccess.effectivePermissions
            - resource.s3BucketDetails.name
            - resource.s3BucketDetails.tags.key
            - resource.s3BucketDetails.tags.value
            - resource.s3BucketDetails.type
            - service.action.actionType
            - service.action.awsApiCallAction.api
            - service.action.awsApiCallAction.callerType
            - service.action.awsApiCallAction.errorCode
            - service.action.awsApiCallAction.remoteIpDetails.city.cityName
            - service.action.awsApiCallAction.remoteIpDetails.country.countryName
            - service.action.awsApiCallAction.remoteIpDetails.ipAddressV4
            - service.action.awsApiCallAction.remoteIpDetails.ipAddressV6
            - service.action.awsApiCallAction.remoteIpDetails.organization.asn
            - service.action.awsApiCallAction.remoteIpDetails.organization.asnOrg
            - service.action.awsApiCallAction.serviceName
            - service.action.dnsRequestAction.domain
            - service.action.dnsRequestAction.domainWithSuffix
            - service.action.networkConnectionAction.blocked
            - service.action.networkConnectionAction.connectionDirection
            - service.action.networkConnectionAction.localPortDetails.port
            - service.action.networkConnectionAction.protocol
            - service.action.networkConnectionAction.remoteIpDetails.city.cityName
            - service.action.networkConnectionAction.remoteIpDetails.country.countryName
            - service.action.networkConnectionAction.remoteIpDetails.ipAddressV4
            - service.action.networkConnectionAction.remoteIpDetails.ipAddressV6
            - service.action.networkConnectionAction.remoteIpDetails.organization.asn
            - service.action.networkConnectionAction.remoteIpDetails.organization.asnOrg
            - service.action.networkConnectionAction.remotePortDetails.port
            - service.action.awsApiCallAction.remoteAccountDetails.affiliated
            - service.action.kubernetesApiCallAction.remoteIpDetails.ipAddressV4
            - service.action.kubernetesApiCallAction.remoteIpDetails.ipAddressV6
            - service.action.kubernetesApiCallAction.namespace
            - service.action.kubernetesApiCallAction.remoteIpDetails.organization.asn
            - service.action.kubernetesApiCallAction.requestUri
            - service.action.kubernetesApiCallAction.statusCode
            - service.action.networkConnectionAction.localIpDetails.ipAddressV4
            - service.action.networkConnectionAction.localIpDetails.ipAddressV6
            - service.action.networkConnectionAction.protocol
            - service.action.awsApiCallAction.serviceName
            - service.action.awsApiCallAction.remoteAccountDetails.accountId
            - service.additionalInfo.threatListName
            - service.resourceRole
            - resource.eksClusterDetails.name
            - resource.kubernetesDetails.kubernetesWorkloadDetails.name
            - resource.kubernetesDetails.kubernetesWorkloadDetails.namespace
            - resource.kubernetesDetails.kubernetesUserDetails.username
            - resource.kubernetesDetails.kubernetesWorkloadDetails.containers.image
            - resource.kubernetesDetails.kubernetesWorkloadDetails.containers.imagePrefix
            - service.ebsVolumeScanDetails.scanId
            - service.ebsVolumeScanDetails.scanDetections.threatDetectedByName.threatNames.name
            - service.ebsVolumeScanDetails.scanDetections.threatDetectedByName.threatNames.severity
            - service.ebsVolumeScanDetails.scanDetections.threatDetectedByName.threatNames.filePaths.hash
            - service.malwareScanDetails.threats.name
            - resource.ecsClusterDetails.name
            - resource.ecsClusterDetails.taskDetails.containers.image
            - resource.ecsClusterDetails.taskDetails.definitionArn
            - resource.containerDetails.image
            - resource.rdsDbInstanceDetails.dbInstanceIdentifier
            - resource.rdsDbInstanceDetails.dbClusterIdentifier
            - resource.rdsDbInstanceDetails.engine
            - resource.rdsDbUserDetails.user
            - resource.rdsDbInstanceDetails.tags.key
            - resource.rdsDbInstanceDetails.tags.value
            - service.runtimeDetails.process.executableSha256
            - service.runtimeDetails.process.name
            - service.runtimeDetails.process.name
            - resource.lambdaDetails.functionName
            - resource.lambdaDetails.functionArn
            - resource.lambdaDetails.tags.key
            - resource.lambdaDetails.tags.value

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-filter-findingcriteria.html#cfn-guardduty-filter-findingcriteria-criterion
            '''
            result = self._values.get("criterion")
            return typing.cast(typing.Any, result)

        @builtins.property
        def item_type(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.ConditionProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-filter-findingcriteria.html#cfn-guardduty-filter-findingcriteria-itemtype
            '''
            result = self._values.get("item_type")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.ConditionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FindingCriteriaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_guardduty.mixins.CfnIPSetMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "activate": "activate",
        "detector_id": "detectorId",
        "expected_bucket_owner": "expectedBucketOwner",
        "format": "format",
        "location": "location",
        "name": "name",
        "tags": "tags",
    },
)
class CfnIPSetMixinProps:
    def __init__(
        self,
        *,
        activate: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        detector_id: typing.Optional[builtins.str] = None,
        expected_bucket_owner: typing.Optional[builtins.str] = None,
        format: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnIPSetPropsMixin.

        :param activate: A boolean value that determines if GuardDuty can start using this list for custom threat detection. For GuardDuty to prevent generating findings based on an activity associated with these entries, this list must be active.
        :param detector_id: The unique ID of the detector of the GuardDuty account for which you want to create an IPSet. To find the ``detectorId`` in the current Region, see the Settings page in the GuardDuty console, or run the `ListDetectors <https://docs.aws.amazon.com/guardduty/latest/APIReference/API_ListDetectors.html>`_ API.
        :param expected_bucket_owner: The AWS account ID that owns the Amazon S3 bucket specified in the *Location* field. When you provide this account ID, GuardDuty will validate that the S3 bucket belongs to this account. If you don't specify an account ID owner, GuardDuty doesn't perform any validation.
        :param format: The format of the file that contains the IPSet. For information about supported formats, see `List formats <https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_upload-lists.html#prepare_list>`_ in the *Amazon GuardDuty User Guide* .
        :param location: The URI of the file that contains the IPSet.
        :param name: The user-friendly name to identify the IPSet. The name of your list must be unique within an AWS account and Region. Valid characters are alphanumeric, whitespace, dash (-), and underscores (_).
        :param tags: The tags to be added to a new threat entity set resource. Each tag consists of a key and an optional value, both of which you define. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-ipset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_guardduty import mixins as guardduty_mixins
            
            cfn_iPSet_mixin_props = guardduty_mixins.CfnIPSetMixinProps(
                activate=False,
                detector_id="detectorId",
                expected_bucket_owner="expectedBucketOwner",
                format="format",
                location="location",
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1279eed9969f44d105998a8286ffff89cc1d7e59db31775d6cf1d803e9d12f5c)
            check_type(argname="argument activate", value=activate, expected_type=type_hints["activate"])
            check_type(argname="argument detector_id", value=detector_id, expected_type=type_hints["detector_id"])
            check_type(argname="argument expected_bucket_owner", value=expected_bucket_owner, expected_type=type_hints["expected_bucket_owner"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if activate is not None:
            self._values["activate"] = activate
        if detector_id is not None:
            self._values["detector_id"] = detector_id
        if expected_bucket_owner is not None:
            self._values["expected_bucket_owner"] = expected_bucket_owner
        if format is not None:
            self._values["format"] = format
        if location is not None:
            self._values["location"] = location
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def activate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A boolean value that determines if GuardDuty can start using this list for custom threat detection.

        For GuardDuty to prevent generating findings based on an activity associated with these entries, this list must be active.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-ipset.html#cfn-guardduty-ipset-activate
        '''
        result = self._values.get("activate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def detector_id(self) -> typing.Optional[builtins.str]:
        '''The unique ID of the detector of the GuardDuty account for which you want to create an IPSet.

        To find the ``detectorId`` in the current Region, see the
        Settings page in the GuardDuty console, or run the `ListDetectors <https://docs.aws.amazon.com/guardduty/latest/APIReference/API_ListDetectors.html>`_ API.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-ipset.html#cfn-guardduty-ipset-detectorid
        '''
        result = self._values.get("detector_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expected_bucket_owner(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID that owns the Amazon S3 bucket specified in the *Location* field.

        When you provide this account ID, GuardDuty will validate that the S3 bucket belongs to this account. If you don't specify an account ID owner, GuardDuty doesn't perform any validation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-ipset.html#cfn-guardduty-ipset-expectedbucketowner
        '''
        result = self._values.get("expected_bucket_owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def format(self) -> typing.Optional[builtins.str]:
        '''The format of the file that contains the IPSet.

        For information about supported formats, see `List formats <https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_upload-lists.html#prepare_list>`_ in the *Amazon GuardDuty User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-ipset.html#cfn-guardduty-ipset-format
        '''
        result = self._values.get("format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The URI of the file that contains the IPSet.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-ipset.html#cfn-guardduty-ipset-location
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The user-friendly name to identify the IPSet.

        The name of your list must be unique within an AWS account and Region. Valid characters are alphanumeric, whitespace, dash (-), and underscores (_).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-ipset.html#cfn-guardduty-ipset-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags to be added to a new threat entity set resource.

        Each tag consists of a key and an optional value, both of which you define.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-ipset.html#cfn-guardduty-ipset-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIPSetMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnIPSetPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_guardduty.mixins.CfnIPSetPropsMixin",
):
    '''The ``AWS::GuardDuty::IPSet`` resource helps you create a list of trusted IP addresses that you can use for secure communication with AWS infrastructure and applications.

    Once you activate this list, GuardDuty will not generate findings when there is an activity associated with these safe IP addresses.

    Only the users of the GuardDuty administrator account can manage this list. These settings are also applied to the member accounts.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-ipset.html
    :cloudformationResource: AWS::GuardDuty::IPSet
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_guardduty import mixins as guardduty_mixins
        
        cfn_iPSet_props_mixin = guardduty_mixins.CfnIPSetPropsMixin(guardduty_mixins.CfnIPSetMixinProps(
            activate=False,
            detector_id="detectorId",
            expected_bucket_owner="expectedBucketOwner",
            format="format",
            location="location",
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
        props: typing.Union[CfnIPSetMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::GuardDuty::IPSet``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3443eb64cbfd4cf39765b42ea1a3cf0b8bf7a211c593745d5ada8d498329d15d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cae0f827c561420d6236228c792b2797ae157e9414363ef5e97638d25c1499ea)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a424ddc49b4635d9f65f382d7917a13bf339d666d8b1b4573f93f1f7473818cd)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnIPSetMixinProps:
        return typing.cast(CfnIPSetMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_guardduty.mixins.CfnMalwareProtectionPlanMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "actions": "actions",
        "protected_resource": "protectedResource",
        "role": "role",
        "tags": "tags",
    },
)
class CfnMalwareProtectionPlanMixinProps:
    def __init__(
        self,
        *,
        actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMalwareProtectionPlanPropsMixin.CFNActionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        protected_resource: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMalwareProtectionPlanPropsMixin.CFNProtectedResourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        role: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["CfnMalwareProtectionPlanPropsMixin.TagItemProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnMalwareProtectionPlanPropsMixin.

        :param actions: Specifies the action that is to be applied to the Malware Protection plan resource.
        :param protected_resource: Information about the protected resource. Presently, ``S3Bucket`` is the only supported protected resource.
        :param role: Amazon Resource Name (ARN) of the IAM role that includes the permissions required to scan and (optionally) add tags to the associated protected resource. To find the ARN of your IAM role, go to the IAM console, and select the role name for details.
        :param tags: The tags to be added to the created Malware Protection plan resource. Each tag consists of a key and an optional value, both of which you need to specify.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-malwareprotectionplan.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_guardduty import mixins as guardduty_mixins
            
            cfn_malware_protection_plan_mixin_props = guardduty_mixins.CfnMalwareProtectionPlanMixinProps(
                actions=guardduty_mixins.CfnMalwareProtectionPlanPropsMixin.CFNActionsProperty(
                    tagging=guardduty_mixins.CfnMalwareProtectionPlanPropsMixin.CFNTaggingProperty(
                        status="status"
                    )
                ),
                protected_resource=guardduty_mixins.CfnMalwareProtectionPlanPropsMixin.CFNProtectedResourceProperty(
                    s3_bucket=guardduty_mixins.CfnMalwareProtectionPlanPropsMixin.S3BucketProperty(
                        bucket_name="bucketName",
                        object_prefixes=["objectPrefixes"]
                    )
                ),
                role="role",
                tags=[guardduty_mixins.CfnMalwareProtectionPlanPropsMixin.TagItemProperty(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c61be3ecb724212b92586e1a10b7d76d35ca2815f4382422c4d0c3c81fb7a33d)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument protected_resource", value=protected_resource, expected_type=type_hints["protected_resource"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if actions is not None:
            self._values["actions"] = actions
        if protected_resource is not None:
            self._values["protected_resource"] = protected_resource
        if role is not None:
            self._values["role"] = role
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def actions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMalwareProtectionPlanPropsMixin.CFNActionsProperty"]]:
        '''Specifies the action that is to be applied to the Malware Protection plan resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-malwareprotectionplan.html#cfn-guardduty-malwareprotectionplan-actions
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMalwareProtectionPlanPropsMixin.CFNActionsProperty"]], result)

    @builtins.property
    def protected_resource(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMalwareProtectionPlanPropsMixin.CFNProtectedResourceProperty"]]:
        '''Information about the protected resource.

        Presently, ``S3Bucket`` is the only supported protected resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-malwareprotectionplan.html#cfn-guardduty-malwareprotectionplan-protectedresource
        '''
        result = self._values.get("protected_resource")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMalwareProtectionPlanPropsMixin.CFNProtectedResourceProperty"]], result)

    @builtins.property
    def role(self) -> typing.Optional[builtins.str]:
        '''Amazon Resource Name (ARN) of the IAM role that includes the permissions required to scan and (optionally) add tags to the associated protected resource.

        To find the ARN of your IAM role, go to the IAM console, and select the role name for details.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-malwareprotectionplan.html#cfn-guardduty-malwareprotectionplan-role
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(
        self,
    ) -> typing.Optional[typing.List["CfnMalwareProtectionPlanPropsMixin.TagItemProperty"]]:
        '''The tags to be added to the created Malware Protection plan resource.

        Each tag consists of a key and an optional value, both of which you need to specify.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-malwareprotectionplan.html#cfn-guardduty-malwareprotectionplan-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["CfnMalwareProtectionPlanPropsMixin.TagItemProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMalwareProtectionPlanMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnMalwareProtectionPlanPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_guardduty.mixins.CfnMalwareProtectionPlanPropsMixin",
):
    '''Creates a new Malware Protection plan for the protected resource.

    When you create a Malware Protection plan, the `AWS service terms for GuardDuty Malware Protection <https://docs.aws.amazon.com/service-terms/#87._Amazon_GuardDuty>`_ will apply.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-malwareprotectionplan.html
    :cloudformationResource: AWS::GuardDuty::MalwareProtectionPlan
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_guardduty import mixins as guardduty_mixins
        
        cfn_malware_protection_plan_props_mixin = guardduty_mixins.CfnMalwareProtectionPlanPropsMixin(guardduty_mixins.CfnMalwareProtectionPlanMixinProps(
            actions=guardduty_mixins.CfnMalwareProtectionPlanPropsMixin.CFNActionsProperty(
                tagging=guardduty_mixins.CfnMalwareProtectionPlanPropsMixin.CFNTaggingProperty(
                    status="status"
                )
            ),
            protected_resource=guardduty_mixins.CfnMalwareProtectionPlanPropsMixin.CFNProtectedResourceProperty(
                s3_bucket=guardduty_mixins.CfnMalwareProtectionPlanPropsMixin.S3BucketProperty(
                    bucket_name="bucketName",
                    object_prefixes=["objectPrefixes"]
                )
            ),
            role="role",
            tags=[guardduty_mixins.CfnMalwareProtectionPlanPropsMixin.TagItemProperty(
                key="key",
                value="value"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnMalwareProtectionPlanMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::GuardDuty::MalwareProtectionPlan``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77f6f8097171b51155d769a546f6f0e5bc951114fe583011b339494d847ea88b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__32c211c4717648311b4d6df0ab46ab0a468516c5d2cbdd4981d7b45031e9dded)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4032aa219e5988af3d631ca978e574d416701d61fc8f77a5878a05113f99f7ab)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnMalwareProtectionPlanMixinProps:
        return typing.cast(CfnMalwareProtectionPlanMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_guardduty.mixins.CfnMalwareProtectionPlanPropsMixin.CFNActionsProperty",
        jsii_struct_bases=[],
        name_mapping={"tagging": "tagging"},
    )
    class CFNActionsProperty:
        def __init__(
            self,
            *,
            tagging: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMalwareProtectionPlanPropsMixin.CFNTaggingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the action that is to be applied to the Malware Protection plan resource.

            :param tagging: Contains information about tagging status of the Malware Protection plan resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-malwareprotectionplan-cfnactions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_guardduty import mixins as guardduty_mixins
                
                c_fNActions_property = guardduty_mixins.CfnMalwareProtectionPlanPropsMixin.CFNActionsProperty(
                    tagging=guardduty_mixins.CfnMalwareProtectionPlanPropsMixin.CFNTaggingProperty(
                        status="status"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f83f90edbbc057c95834313577ebbb49af8146f48ec3ebf124af4bd398a51aca)
                check_type(argname="argument tagging", value=tagging, expected_type=type_hints["tagging"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if tagging is not None:
                self._values["tagging"] = tagging

        @builtins.property
        def tagging(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMalwareProtectionPlanPropsMixin.CFNTaggingProperty"]]:
            '''Contains information about tagging status of the Malware Protection plan resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-malwareprotectionplan-cfnactions.html#cfn-guardduty-malwareprotectionplan-cfnactions-tagging
            '''
            result = self._values.get("tagging")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMalwareProtectionPlanPropsMixin.CFNTaggingProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CFNActionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_guardduty.mixins.CfnMalwareProtectionPlanPropsMixin.CFNProtectedResourceProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_bucket": "s3Bucket"},
    )
    class CFNProtectedResourceProperty:
        def __init__(
            self,
            *,
            s3_bucket: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMalwareProtectionPlanPropsMixin.S3BucketProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Information about the protected resource.

            Presently, ``S3Bucket`` is the only supported protected resource.

            :param s3_bucket: Information about the protected S3 bucket resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-malwareprotectionplan-cfnprotectedresource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_guardduty import mixins as guardduty_mixins
                
                c_fNProtected_resource_property = guardduty_mixins.CfnMalwareProtectionPlanPropsMixin.CFNProtectedResourceProperty(
                    s3_bucket=guardduty_mixins.CfnMalwareProtectionPlanPropsMixin.S3BucketProperty(
                        bucket_name="bucketName",
                        object_prefixes=["objectPrefixes"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c5596035c1b2372196f4df6e4e23b78ff2dbbe1bc539188b796393d924f72531)
                check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3_bucket is not None:
                self._values["s3_bucket"] = s3_bucket

        @builtins.property
        def s3_bucket(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMalwareProtectionPlanPropsMixin.S3BucketProperty"]]:
            '''Information about the protected S3 bucket resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-malwareprotectionplan-cfnprotectedresource.html#cfn-guardduty-malwareprotectionplan-cfnprotectedresource-s3bucket
            '''
            result = self._values.get("s3_bucket")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMalwareProtectionPlanPropsMixin.S3BucketProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CFNProtectedResourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_guardduty.mixins.CfnMalwareProtectionPlanPropsMixin.CFNStatusReasonsProperty",
        jsii_struct_bases=[],
        name_mapping={"code": "code", "message": "message"},
    )
    class CFNStatusReasonsProperty:
        def __init__(
            self,
            *,
            code: typing.Optional[builtins.str] = None,
            message: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about the status code and status details associated with the status of the Malware Protection plan.

            :param code: The status code of the Malware Protection plan. For more information, see `Malware Protection plan resource status <https://docs.aws.amazon.com/guardduty/latest/ug/malware-protection-s3-bucket-status-gdu.html>`_ in the *GuardDuty User Guide* .
            :param message: Issue message that specifies the reason. For information about potential troubleshooting steps, see `Troubleshooting Malware Protection for S3 status issues <https://docs.aws.amazon.com/guardduty/latest/ug/troubleshoot-s3-malware-protection-status-errors.html>`_ in the *Amazon GuardDuty User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-malwareprotectionplan-cfnstatusreasons.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_guardduty import mixins as guardduty_mixins
                
                c_fNStatus_reasons_property = guardduty_mixins.CfnMalwareProtectionPlanPropsMixin.CFNStatusReasonsProperty(
                    code="code",
                    message="message"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b30c76a39ff18ff6929665ca5179e8ff20895e231c1937ac4ab6c2926620b29a)
                check_type(argname="argument code", value=code, expected_type=type_hints["code"])
                check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if code is not None:
                self._values["code"] = code
            if message is not None:
                self._values["message"] = message

        @builtins.property
        def code(self) -> typing.Optional[builtins.str]:
            '''The status code of the Malware Protection plan.

            For more information, see `Malware Protection plan resource status <https://docs.aws.amazon.com/guardduty/latest/ug/malware-protection-s3-bucket-status-gdu.html>`_ in the *GuardDuty User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-malwareprotectionplan-cfnstatusreasons.html#cfn-guardduty-malwareprotectionplan-cfnstatusreasons-code
            '''
            result = self._values.get("code")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def message(self) -> typing.Optional[builtins.str]:
            '''Issue message that specifies the reason.

            For information about potential troubleshooting steps, see `Troubleshooting Malware Protection for S3 status issues <https://docs.aws.amazon.com/guardduty/latest/ug/troubleshoot-s3-malware-protection-status-errors.html>`_ in the *Amazon GuardDuty User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-malwareprotectionplan-cfnstatusreasons.html#cfn-guardduty-malwareprotectionplan-cfnstatusreasons-message
            '''
            result = self._values.get("message")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CFNStatusReasonsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_guardduty.mixins.CfnMalwareProtectionPlanPropsMixin.CFNTaggingProperty",
        jsii_struct_bases=[],
        name_mapping={"status": "status"},
    )
    class CFNTaggingProperty:
        def __init__(self, *, status: typing.Optional[builtins.str] = None) -> None:
            '''Contains information about tagging status of the Malware Protection plan resource.

            :param status: Indicates whether or not you chose GuardDuty to add a predefined tag to the scanned S3 object. Potential values include ``ENABLED`` and ``DISABLED`` . These values are case-sensitive.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-malwareprotectionplan-cfntagging.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_guardduty import mixins as guardduty_mixins
                
                c_fNTagging_property = guardduty_mixins.CfnMalwareProtectionPlanPropsMixin.CFNTaggingProperty(
                    status="status"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cc94c33f01b397d84a20e7f5749b4d2328da914d4bff2a0ab6c0ae557b196214)
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''Indicates whether or not you chose GuardDuty to add a predefined tag to the scanned S3 object.

            Potential values include ``ENABLED`` and ``DISABLED`` . These values are case-sensitive.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-malwareprotectionplan-cfntagging.html#cfn-guardduty-malwareprotectionplan-cfntagging-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CFNTaggingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_guardduty.mixins.CfnMalwareProtectionPlanPropsMixin.S3BucketProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_name": "bucketName",
            "object_prefixes": "objectPrefixes",
        },
    )
    class S3BucketProperty:
        def __init__(
            self,
            *,
            bucket_name: typing.Optional[builtins.str] = None,
            object_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Information about the protected S3 bucket resource.

            :param bucket_name: Name of the S3 bucket.
            :param object_prefixes: Information about the specified object prefixes. An S3 object will be scanned only if it belongs to any of the specified object prefixes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-malwareprotectionplan-s3bucket.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_guardduty import mixins as guardduty_mixins
                
                s3_bucket_property = guardduty_mixins.CfnMalwareProtectionPlanPropsMixin.S3BucketProperty(
                    bucket_name="bucketName",
                    object_prefixes=["objectPrefixes"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__76737cfe5b89f0461f4859fe8378793056f5443edf17267af3857fa89140e5f2)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument object_prefixes", value=object_prefixes, expected_type=type_hints["object_prefixes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_name is not None:
                self._values["bucket_name"] = bucket_name
            if object_prefixes is not None:
                self._values["object_prefixes"] = object_prefixes

        @builtins.property
        def bucket_name(self) -> typing.Optional[builtins.str]:
            '''Name of the S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-malwareprotectionplan-s3bucket.html#cfn-guardduty-malwareprotectionplan-s3bucket-bucketname
            '''
            result = self._values.get("bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def object_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Information about the specified object prefixes.

            An S3 object will be scanned only if it belongs to any of the specified object prefixes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-malwareprotectionplan-s3bucket.html#cfn-guardduty-malwareprotectionplan-s3bucket-objectprefixes
            '''
            result = self._values.get("object_prefixes")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3BucketProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_guardduty.mixins.CfnMalwareProtectionPlanPropsMixin.TagItemProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TagItemProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes a tag.

            :param key: The tag key.
            :param value: The tag value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-malwareprotectionplan-tagitem.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_guardduty import mixins as guardduty_mixins
                
                tag_item_property = guardduty_mixins.CfnMalwareProtectionPlanPropsMixin.TagItemProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4c85686deb189451e52f191224741467d2c9b4198716d73afc36e71ec77fd0b8)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The tag key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-malwareprotectionplan-tagitem.html#cfn-guardduty-malwareprotectionplan-tagitem-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The tag value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-malwareprotectionplan-tagitem.html#cfn-guardduty-malwareprotectionplan-tagitem-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagItemProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_guardduty.mixins.CfnMasterMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "detector_id": "detectorId",
        "invitation_id": "invitationId",
        "master_id": "masterId",
    },
)
class CfnMasterMixinProps:
    def __init__(
        self,
        *,
        detector_id: typing.Optional[builtins.str] = None,
        invitation_id: typing.Optional[builtins.str] = None,
        master_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnMasterPropsMixin.

        :param detector_id: The unique ID of the detector of the GuardDuty member account. To find the ``detectorId`` in the current Region, see the Settings page in the GuardDuty console, or run the `ListDetectors <https://docs.aws.amazon.com/guardduty/latest/APIReference/API_ListDetectors.html>`_ API.
        :param invitation_id: The ID of the invitation that is sent to the account designated as a member account. You can find the invitation ID by running the `ListInvitations <https://docs.aws.amazon.com/guardduty/latest/APIReference/API_ListInvitations.html>`_ in the *GuardDuty API Reference* .
        :param master_id: The AWS account ID of the account designated as the GuardDuty administrator account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-master.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_guardduty import mixins as guardduty_mixins
            
            cfn_master_mixin_props = guardduty_mixins.CfnMasterMixinProps(
                detector_id="detectorId",
                invitation_id="invitationId",
                master_id="masterId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83fa1871aa734d50251056365ca201bbe1c3645a5678ebd0f6ba445ce8715b5f)
            check_type(argname="argument detector_id", value=detector_id, expected_type=type_hints["detector_id"])
            check_type(argname="argument invitation_id", value=invitation_id, expected_type=type_hints["invitation_id"])
            check_type(argname="argument master_id", value=master_id, expected_type=type_hints["master_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if detector_id is not None:
            self._values["detector_id"] = detector_id
        if invitation_id is not None:
            self._values["invitation_id"] = invitation_id
        if master_id is not None:
            self._values["master_id"] = master_id

    @builtins.property
    def detector_id(self) -> typing.Optional[builtins.str]:
        '''The unique ID of the detector of the GuardDuty member account.

        To find the ``detectorId`` in the current Region, see the
        Settings page in the GuardDuty console, or run the `ListDetectors <https://docs.aws.amazon.com/guardduty/latest/APIReference/API_ListDetectors.html>`_ API.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-master.html#cfn-guardduty-master-detectorid
        '''
        result = self._values.get("detector_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def invitation_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the invitation that is sent to the account designated as a member account.

        You can find the invitation ID by running the `ListInvitations <https://docs.aws.amazon.com/guardduty/latest/APIReference/API_ListInvitations.html>`_ in the *GuardDuty API Reference* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-master.html#cfn-guardduty-master-invitationid
        '''
        result = self._values.get("invitation_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def master_id(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID of the account designated as the GuardDuty administrator account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-master.html#cfn-guardduty-master-masterid
        '''
        result = self._values.get("master_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMasterMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnMasterPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_guardduty.mixins.CfnMasterPropsMixin",
):
    '''You can use the ``AWS::GuardDuty::Master`` resource in a GuardDuty member account to accept an invitation from a GuardDuty administrator account.

    The invitation to the member account must be sent prior to using the ``AWS::GuardDuty::Master`` resource to accept the administrator account's invitation. You can invite a member account by using the ``InviteMembers`` operation of the GuardDuty API, or by creating an ``AWS::GuardDuty::Member`` resource.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-master.html
    :cloudformationResource: AWS::GuardDuty::Master
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_guardduty import mixins as guardduty_mixins
        
        cfn_master_props_mixin = guardduty_mixins.CfnMasterPropsMixin(guardduty_mixins.CfnMasterMixinProps(
            detector_id="detectorId",
            invitation_id="invitationId",
            master_id="masterId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnMasterMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::GuardDuty::Master``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31f089ecc4d0d34781c99b0937267abce5777f311c1008a1c26dd1717d5b49ef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aecf520d9b9b519bce136e337c17381ff4d18e526d35ae05948505b456fdb969)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d1f1851e9730df784a2ccb1dee7b53124c905706f0dfb4dce5f8f3022730bb1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnMasterMixinProps:
        return typing.cast(CfnMasterMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_guardduty.mixins.CfnMemberMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "detector_id": "detectorId",
        "disable_email_notification": "disableEmailNotification",
        "email": "email",
        "member_id": "memberId",
        "message": "message",
        "status": "status",
    },
)
class CfnMemberMixinProps:
    def __init__(
        self,
        *,
        detector_id: typing.Optional[builtins.str] = None,
        disable_email_notification: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        email: typing.Optional[builtins.str] = None,
        member_id: typing.Optional[builtins.str] = None,
        message: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnMemberPropsMixin.

        :param detector_id: The ID of the detector associated with the GuardDuty service to add the member to.
        :param disable_email_notification: Specifies whether or not to disable email notification for the member account that you invite.
        :param email: The email address associated with the member account.
        :param member_id: The AWS account ID of the account to designate as a member.
        :param message: The invitation message that you want to send to the accounts that you're inviting to GuardDuty as members.
        :param status: You can use the ``Status`` property to update the status of the relationship between the member account and its administrator account. Valid values are ``Created`` and ``Invited`` when using an ``AWS::GuardDuty::Member`` resource. If the value for this property is not provided or set to ``Created`` , a member account is created but not invited. If the value of this property is set to ``Invited`` , a member account is created and invited.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-member.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_guardduty import mixins as guardduty_mixins
            
            cfn_member_mixin_props = guardduty_mixins.CfnMemberMixinProps(
                detector_id="detectorId",
                disable_email_notification=False,
                email="email",
                member_id="memberId",
                message="message",
                status="status"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f6f9d6afdb37fa56d79f6bc46f61cac57a8959125387810113f4444abbeabbd)
            check_type(argname="argument detector_id", value=detector_id, expected_type=type_hints["detector_id"])
            check_type(argname="argument disable_email_notification", value=disable_email_notification, expected_type=type_hints["disable_email_notification"])
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument member_id", value=member_id, expected_type=type_hints["member_id"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if detector_id is not None:
            self._values["detector_id"] = detector_id
        if disable_email_notification is not None:
            self._values["disable_email_notification"] = disable_email_notification
        if email is not None:
            self._values["email"] = email
        if member_id is not None:
            self._values["member_id"] = member_id
        if message is not None:
            self._values["message"] = message
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def detector_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the detector associated with the GuardDuty service to add the member to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-member.html#cfn-guardduty-member-detectorid
        '''
        result = self._values.get("detector_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_email_notification(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether or not to disable email notification for the member account that you invite.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-member.html#cfn-guardduty-member-disableemailnotification
        '''
        result = self._values.get("disable_email_notification")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def email(self) -> typing.Optional[builtins.str]:
        '''The email address associated with the member account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-member.html#cfn-guardduty-member-email
        '''
        result = self._values.get("email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def member_id(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID of the account to designate as a member.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-member.html#cfn-guardduty-member-memberid
        '''
        result = self._values.get("member_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def message(self) -> typing.Optional[builtins.str]:
        '''The invitation message that you want to send to the accounts that you're inviting to GuardDuty as members.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-member.html#cfn-guardduty-member-message
        '''
        result = self._values.get("message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''You can use the ``Status`` property to update the status of the relationship between the member account and its administrator account.

        Valid values are ``Created`` and ``Invited`` when using an ``AWS::GuardDuty::Member`` resource. If the value for this property is not provided or set to ``Created`` , a member account is created but not invited. If the value of this property is set to ``Invited`` , a member account is created and invited.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-member.html#cfn-guardduty-member-status
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMemberMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnMemberPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_guardduty.mixins.CfnMemberPropsMixin",
):
    '''You can use the ``AWS::GuardDuty::Member`` resource to add an AWS account as a GuardDuty member account to the current GuardDuty administrator account.

    If the value of the ``Status`` property is not provided or is set to ``Created`` , a member account is created but not invited. If the value of the ``Status`` property is set to ``Invited`` , a member account is created and invited. An ``AWS::GuardDuty::Member`` resource must be created with the ``Status`` property set to ``Invited`` before the ``AWS::GuardDuty::Master`` resource can be created in a GuardDuty member account.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-member.html
    :cloudformationResource: AWS::GuardDuty::Member
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_guardduty import mixins as guardduty_mixins
        
        cfn_member_props_mixin = guardduty_mixins.CfnMemberPropsMixin(guardduty_mixins.CfnMemberMixinProps(
            detector_id="detectorId",
            disable_email_notification=False,
            email="email",
            member_id="memberId",
            message="message",
            status="status"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnMemberMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::GuardDuty::Member``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__392807d794f05267d95a9d01cc401f953c47d8957faa258ed58147840a41e513)
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
            type_hints = typing.get_type_hints(_typecheckingstub__64da5ece26e87f07a19c2dc5c60134950338a3bccfedd611454d73d2a981810a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e102b2c8dee2de8fea9b2e4c50c3556479e308c88a6cc6b88bba7f0830ca06a5)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnMemberMixinProps:
        return typing.cast(CfnMemberMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_guardduty.mixins.CfnPublishingDestinationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "destination_properties": "destinationProperties",
        "destination_type": "destinationType",
        "detector_id": "detectorId",
        "tags": "tags",
    },
)
class CfnPublishingDestinationMixinProps:
    def __init__(
        self,
        *,
        destination_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPublishingDestinationPropsMixin.CFNDestinationPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        destination_type: typing.Optional[builtins.str] = None,
        detector_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["CfnPublishingDestinationPropsMixin.TagItemProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnPublishingDestinationPropsMixin.

        :param destination_properties: Contains the Amazon Resource Name (ARN) of the resource to publish to, such as an S3 bucket, and the ARN of the KMS key to use to encrypt published findings.
        :param destination_type: The type of publishing destination. GuardDuty supports Amazon S3 buckets as a publishing destination.
        :param detector_id: The ID of the GuardDuty detector where the publishing destination exists.
        :param tags: Describes a tag.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-publishingdestination.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_guardduty import mixins as guardduty_mixins
            
            cfn_publishing_destination_mixin_props = guardduty_mixins.CfnPublishingDestinationMixinProps(
                destination_properties=guardduty_mixins.CfnPublishingDestinationPropsMixin.CFNDestinationPropertiesProperty(
                    destination_arn="destinationArn",
                    kms_key_arn="kmsKeyArn"
                ),
                destination_type="destinationType",
                detector_id="detectorId",
                tags=[guardduty_mixins.CfnPublishingDestinationPropsMixin.TagItemProperty(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f66cb101923801014da5bd7595bb040bd164f190537c782c4df380ff86b76278)
            check_type(argname="argument destination_properties", value=destination_properties, expected_type=type_hints["destination_properties"])
            check_type(argname="argument destination_type", value=destination_type, expected_type=type_hints["destination_type"])
            check_type(argname="argument detector_id", value=detector_id, expected_type=type_hints["detector_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if destination_properties is not None:
            self._values["destination_properties"] = destination_properties
        if destination_type is not None:
            self._values["destination_type"] = destination_type
        if detector_id is not None:
            self._values["detector_id"] = detector_id
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def destination_properties(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPublishingDestinationPropsMixin.CFNDestinationPropertiesProperty"]]:
        '''Contains the Amazon Resource Name (ARN) of the resource to publish to, such as an S3 bucket, and the ARN of the KMS key to use to encrypt published findings.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-publishingdestination.html#cfn-guardduty-publishingdestination-destinationproperties
        '''
        result = self._values.get("destination_properties")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPublishingDestinationPropsMixin.CFNDestinationPropertiesProperty"]], result)

    @builtins.property
    def destination_type(self) -> typing.Optional[builtins.str]:
        '''The type of publishing destination.

        GuardDuty supports Amazon S3 buckets as a publishing destination.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-publishingdestination.html#cfn-guardduty-publishingdestination-destinationtype
        '''
        result = self._values.get("destination_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def detector_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the GuardDuty detector where the publishing destination exists.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-publishingdestination.html#cfn-guardduty-publishingdestination-detectorid
        '''
        result = self._values.get("detector_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(
        self,
    ) -> typing.Optional[typing.List["CfnPublishingDestinationPropsMixin.TagItemProperty"]]:
        '''Describes a tag.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-publishingdestination.html#cfn-guardduty-publishingdestination-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["CfnPublishingDestinationPropsMixin.TagItemProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPublishingDestinationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPublishingDestinationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_guardduty.mixins.CfnPublishingDestinationPropsMixin",
):
    '''Creates a publishing destination where you can export your GuardDuty findings.

    Before you start exporting the findings, the destination resource must exist.

    For more information about considerations and permissions, see `Exporting GuardDuty findings to Amazon S3 buckets <https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_exportfindings.html>`_ in the *Amazon GuardDuty User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-publishingdestination.html
    :cloudformationResource: AWS::GuardDuty::PublishingDestination
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_guardduty import mixins as guardduty_mixins
        
        cfn_publishing_destination_props_mixin = guardduty_mixins.CfnPublishingDestinationPropsMixin(guardduty_mixins.CfnPublishingDestinationMixinProps(
            destination_properties=guardduty_mixins.CfnPublishingDestinationPropsMixin.CFNDestinationPropertiesProperty(
                destination_arn="destinationArn",
                kms_key_arn="kmsKeyArn"
            ),
            destination_type="destinationType",
            detector_id="detectorId",
            tags=[guardduty_mixins.CfnPublishingDestinationPropsMixin.TagItemProperty(
                key="key",
                value="value"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnPublishingDestinationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::GuardDuty::PublishingDestination``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ba0f8dad44e13844cd9444de66fad4a3330e75228c20c7e1cff15b89206c20f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f9cdcb37d616ec702e2fbfd8e0ba2664030b8cdbf44fdd08671e404bbd66452)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca05821294bf0f5520ccb953f827e38b892ff5e3561dc51943c7f7678ef72d30)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPublishingDestinationMixinProps:
        return typing.cast(CfnPublishingDestinationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_guardduty.mixins.CfnPublishingDestinationPropsMixin.CFNDestinationPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"destination_arn": "destinationArn", "kms_key_arn": "kmsKeyArn"},
    )
    class CFNDestinationPropertiesProperty:
        def __init__(
            self,
            *,
            destination_arn: typing.Optional[builtins.str] = None,
            kms_key_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains the Amazon Resource Name (ARN) of the resource that receives the published findings, such as an S3 bucket, and the ARN of the KMS key that is used to encrypt these published findings.

            :param destination_arn: The ARN of the resource where the findings are published.
            :param kms_key_arn: The ARN of the KMS key to use for encryption.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-publishingdestination-cfndestinationproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_guardduty import mixins as guardduty_mixins
                
                c_fNDestination_properties_property = guardduty_mixins.CfnPublishingDestinationPropsMixin.CFNDestinationPropertiesProperty(
                    destination_arn="destinationArn",
                    kms_key_arn="kmsKeyArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__eb7c59164a86cc546687c7bc558823e45483c6479f4fedca6a0299ac5391cfd5)
                check_type(argname="argument destination_arn", value=destination_arn, expected_type=type_hints["destination_arn"])
                check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination_arn is not None:
                self._values["destination_arn"] = destination_arn
            if kms_key_arn is not None:
                self._values["kms_key_arn"] = kms_key_arn

        @builtins.property
        def destination_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the resource where the findings are published.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-publishingdestination-cfndestinationproperties.html#cfn-guardduty-publishingdestination-cfndestinationproperties-destinationarn
            '''
            result = self._values.get("destination_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def kms_key_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the KMS key to use for encryption.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-publishingdestination-cfndestinationproperties.html#cfn-guardduty-publishingdestination-cfndestinationproperties-kmskeyarn
            '''
            result = self._values.get("kms_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CFNDestinationPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_guardduty.mixins.CfnPublishingDestinationPropsMixin.TagItemProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TagItemProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes a tag.

            :param key: The tag key.
            :param value: The tag value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-publishingdestination-tagitem.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_guardduty import mixins as guardduty_mixins
                
                tag_item_property = guardduty_mixins.CfnPublishingDestinationPropsMixin.TagItemProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a8e62b62b8328a348441b1f93842f1317775a6fc3d44395dee1df9f380eb138f)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The tag key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-publishingdestination-tagitem.html#cfn-guardduty-publishingdestination-tagitem-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The tag value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-publishingdestination-tagitem.html#cfn-guardduty-publishingdestination-tagitem-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagItemProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_guardduty.mixins.CfnThreatEntitySetMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "activate": "activate",
        "detector_id": "detectorId",
        "expected_bucket_owner": "expectedBucketOwner",
        "format": "format",
        "location": "location",
        "name": "name",
        "tags": "tags",
    },
)
class CfnThreatEntitySetMixinProps:
    def __init__(
        self,
        *,
        activate: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        detector_id: typing.Optional[builtins.str] = None,
        expected_bucket_owner: typing.Optional[builtins.str] = None,
        format: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["CfnThreatEntitySetPropsMixin.TagItemProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnThreatEntitySetPropsMixin.

        :param activate: A boolean value that determines if GuardDuty can start using this list for custom threat detection. For GuardDuty to consider the entries in this list and generate findings based on associated activity, this list must be active.
        :param detector_id: The unique regional detector ID of the GuardDuty account for which you want to create a threat entity set. To find the ``detectorId`` in the current Region, see the Settings page in the GuardDuty console, or run the `ListDetectors <https://docs.aws.amazon.com/guardduty/latest/APIReference/API_ListDetectors.html>`_ API.
        :param expected_bucket_owner: The AWS account ID that owns the Amazon S3 bucket specified in the *Location* field. Whether or not you provide the account ID for this optional field, GuardDuty validates that the account ID associated with the ``DetectorId`` owns the S3 bucket in the ``Location`` field. If GuardDuty finds that this S3 bucket doesn't belong to the specified account ID, you will get an error at the time of activating this list.
        :param format: The format of the file that contains the threat entity set. For information about supported formats, see `List formats <https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_upload-lists.html#prepare_list>`_ in the *Amazon GuardDuty User Guide* .
        :param location: The URI of the file that contains the threat entity set.
        :param name: The user-friendly name to identify the threat entity set. Valid characters are alphanumeric, whitespace, dash (-), and underscores (_).
        :param tags: The tags to be added to a new threat entity set resource. Each tag consists of a key and an optional value, both of which you define. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-threatentityset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_guardduty import mixins as guardduty_mixins
            
            cfn_threat_entity_set_mixin_props = guardduty_mixins.CfnThreatEntitySetMixinProps(
                activate=False,
                detector_id="detectorId",
                expected_bucket_owner="expectedBucketOwner",
                format="format",
                location="location",
                name="name",
                tags=[guardduty_mixins.CfnThreatEntitySetPropsMixin.TagItemProperty(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39a3a353b0cea5cdb09bdfb91019597550cb207c6ddc4dcbf7ae929662f8bfb8)
            check_type(argname="argument activate", value=activate, expected_type=type_hints["activate"])
            check_type(argname="argument detector_id", value=detector_id, expected_type=type_hints["detector_id"])
            check_type(argname="argument expected_bucket_owner", value=expected_bucket_owner, expected_type=type_hints["expected_bucket_owner"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if activate is not None:
            self._values["activate"] = activate
        if detector_id is not None:
            self._values["detector_id"] = detector_id
        if expected_bucket_owner is not None:
            self._values["expected_bucket_owner"] = expected_bucket_owner
        if format is not None:
            self._values["format"] = format
        if location is not None:
            self._values["location"] = location
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def activate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A boolean value that determines if GuardDuty can start using this list for custom threat detection.

        For GuardDuty to consider the entries in this list and generate findings based on associated activity, this list must be active.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-threatentityset.html#cfn-guardduty-threatentityset-activate
        '''
        result = self._values.get("activate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def detector_id(self) -> typing.Optional[builtins.str]:
        '''The unique regional detector ID of the GuardDuty account for which you want to create a threat entity set.

        To find the ``detectorId`` in the current Region, see the Settings page in the GuardDuty console, or run the `ListDetectors <https://docs.aws.amazon.com/guardduty/latest/APIReference/API_ListDetectors.html>`_ API.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-threatentityset.html#cfn-guardduty-threatentityset-detectorid
        '''
        result = self._values.get("detector_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expected_bucket_owner(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID that owns the Amazon S3 bucket specified in the *Location* field.

        Whether or not you provide the account ID for this optional field, GuardDuty validates that the account ID associated with the ``DetectorId`` owns the S3 bucket in the ``Location`` field. If GuardDuty finds that this S3 bucket doesn't belong to the specified account ID, you will get an error at the time of activating this list.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-threatentityset.html#cfn-guardduty-threatentityset-expectedbucketowner
        '''
        result = self._values.get("expected_bucket_owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def format(self) -> typing.Optional[builtins.str]:
        '''The format of the file that contains the threat entity set.

        For information about supported formats, see `List formats <https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_upload-lists.html#prepare_list>`_ in the *Amazon GuardDuty User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-threatentityset.html#cfn-guardduty-threatentityset-format
        '''
        result = self._values.get("format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The URI of the file that contains the threat entity set.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-threatentityset.html#cfn-guardduty-threatentityset-location
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The user-friendly name to identify the threat entity set.

        Valid characters are alphanumeric, whitespace, dash (-), and underscores (_).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-threatentityset.html#cfn-guardduty-threatentityset-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(
        self,
    ) -> typing.Optional[typing.List["CfnThreatEntitySetPropsMixin.TagItemProperty"]]:
        '''The tags to be added to a new threat entity set resource.

        Each tag consists of a key and an optional value, both of which you define.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-threatentityset.html#cfn-guardduty-threatentityset-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["CfnThreatEntitySetPropsMixin.TagItemProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnThreatEntitySetMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnThreatEntitySetPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_guardduty.mixins.CfnThreatEntitySetPropsMixin",
):
    '''The ``AWS::GuardDuty::ThreatEntitySet`` resource helps you create a list of known malicious IP addresses and domain names in your AWS environment.

    Once you activate this list, GuardDuty will use the entries in this list as an additional source of threat detection and generate findings when there is an activity associated with these known malicious IP addresses and domain names. GuardDuty continues to monitor independently of this custom threat entity set.

    Only the users of the GuardDuty administrator account can manage this list. These settings automatically apply to the member accounts.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-threatentityset.html
    :cloudformationResource: AWS::GuardDuty::ThreatEntitySet
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_guardduty import mixins as guardduty_mixins
        
        cfn_threat_entity_set_props_mixin = guardduty_mixins.CfnThreatEntitySetPropsMixin(guardduty_mixins.CfnThreatEntitySetMixinProps(
            activate=False,
            detector_id="detectorId",
            expected_bucket_owner="expectedBucketOwner",
            format="format",
            location="location",
            name="name",
            tags=[guardduty_mixins.CfnThreatEntitySetPropsMixin.TagItemProperty(
                key="key",
                value="value"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnThreatEntitySetMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::GuardDuty::ThreatEntitySet``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f9ca7441561e1f1a181dd2c6c3855dfa4e793ee963244344c0a5568f50afaae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ff516b3c5fb6305e980cb189f273cc773b3dfef05e049691da70a386d4806a8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5ecab8be1bd228b1bc9b35367e7755b2af72dbc5c1c8fd88660e4ea373a1c15)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnThreatEntitySetMixinProps:
        return typing.cast(CfnThreatEntitySetMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_guardduty.mixins.CfnThreatEntitySetPropsMixin.TagItemProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TagItemProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes a tag.

            For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

            :param key: The tag key.
            :param value: The tag value. This is optional.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-threatentityset-tagitem.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_guardduty import mixins as guardduty_mixins
                
                tag_item_property = guardduty_mixins.CfnThreatEntitySetPropsMixin.TagItemProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f7becf9ade2f0635b74650ce5c32ca5e01d54b5a1ecbd43a8f9e57203d54cc92)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The tag key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-threatentityset-tagitem.html#cfn-guardduty-threatentityset-tagitem-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The tag value.

            This is optional.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-threatentityset-tagitem.html#cfn-guardduty-threatentityset-tagitem-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagItemProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_guardduty.mixins.CfnThreatIntelSetMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "activate": "activate",
        "detector_id": "detectorId",
        "expected_bucket_owner": "expectedBucketOwner",
        "format": "format",
        "location": "location",
        "name": "name",
        "tags": "tags",
    },
)
class CfnThreatIntelSetMixinProps:
    def __init__(
        self,
        *,
        activate: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        detector_id: typing.Optional[builtins.str] = None,
        expected_bucket_owner: typing.Optional[builtins.str] = None,
        format: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnThreatIntelSetPropsMixin.

        :param activate: A boolean value that determines if GuardDuty can start using this list for custom threat detection. For GuardDuty to be able to generate findings based on an activity associated with these entries, this list must be active.
        :param detector_id: The unique ID of the detector of the GuardDuty account for which you want to create a ``threatIntelSet`` . To find the ``detectorId`` in the current Region, see the Settings page in the GuardDuty console, or run the `ListDetectors <https://docs.aws.amazon.com/guardduty/latest/APIReference/API_ListDetectors.html>`_ API.
        :param expected_bucket_owner: The AWS account ID that owns the Amazon S3 bucket specified in the *Location* field. When you provide this account ID, GuardDuty will validate that the S3 bucket belongs to this account. If you don't specify an account ID owner, GuardDuty doesn't perform any validation.
        :param format: The format of the file that contains the ``ThreatIntelSet`` . For information about supported formats, see `List formats <https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_upload-lists.html#prepare_list>`_ in the *Amazon GuardDuty User Guide* .
        :param location: The URI of the file that contains the ThreatIntelSet.
        :param name: The user-friendly name to identify the ThreatIntelSet. The name of your list must be unique within an AWS account and Region. Valid characters are alphanumeric, whitespace, dash (-), and underscores (_).
        :param tags: The tags to be added to a new threat entity set resource. Each tag consists of a key and an optional value, both of which you define. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-threatintelset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_guardduty import mixins as guardduty_mixins
            
            cfn_threat_intel_set_mixin_props = guardduty_mixins.CfnThreatIntelSetMixinProps(
                activate=False,
                detector_id="detectorId",
                expected_bucket_owner="expectedBucketOwner",
                format="format",
                location="location",
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__350503e05fc2192a357c195ee8de774f8aac84762eb5c8ac3bf7aaf82b6cc27d)
            check_type(argname="argument activate", value=activate, expected_type=type_hints["activate"])
            check_type(argname="argument detector_id", value=detector_id, expected_type=type_hints["detector_id"])
            check_type(argname="argument expected_bucket_owner", value=expected_bucket_owner, expected_type=type_hints["expected_bucket_owner"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if activate is not None:
            self._values["activate"] = activate
        if detector_id is not None:
            self._values["detector_id"] = detector_id
        if expected_bucket_owner is not None:
            self._values["expected_bucket_owner"] = expected_bucket_owner
        if format is not None:
            self._values["format"] = format
        if location is not None:
            self._values["location"] = location
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def activate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A boolean value that determines if GuardDuty can start using this list for custom threat detection.

        For GuardDuty to be able to generate findings based on an activity associated with these entries, this list must be active.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-threatintelset.html#cfn-guardduty-threatintelset-activate
        '''
        result = self._values.get("activate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def detector_id(self) -> typing.Optional[builtins.str]:
        '''The unique ID of the detector of the GuardDuty account for which you want to create a ``threatIntelSet`` .

        To find the ``detectorId`` in the current Region, see the
        Settings page in the GuardDuty console, or run the `ListDetectors <https://docs.aws.amazon.com/guardduty/latest/APIReference/API_ListDetectors.html>`_ API.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-threatintelset.html#cfn-guardduty-threatintelset-detectorid
        '''
        result = self._values.get("detector_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expected_bucket_owner(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID that owns the Amazon S3 bucket specified in the *Location* field.

        When you provide this account ID, GuardDuty will validate that the S3 bucket belongs to this account. If you don't specify an account ID owner, GuardDuty doesn't perform any validation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-threatintelset.html#cfn-guardduty-threatintelset-expectedbucketowner
        '''
        result = self._values.get("expected_bucket_owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def format(self) -> typing.Optional[builtins.str]:
        '''The format of the file that contains the ``ThreatIntelSet`` .

        For information about supported formats, see `List formats <https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_upload-lists.html#prepare_list>`_ in the *Amazon GuardDuty User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-threatintelset.html#cfn-guardduty-threatintelset-format
        '''
        result = self._values.get("format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The URI of the file that contains the ThreatIntelSet.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-threatintelset.html#cfn-guardduty-threatintelset-location
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The user-friendly name to identify the ThreatIntelSet.

        The name of your list must be unique within an AWS account and Region. Valid characters are alphanumeric, whitespace, dash (-), and underscores (_).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-threatintelset.html#cfn-guardduty-threatintelset-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags to be added to a new threat entity set resource.

        Each tag consists of a key and an optional value, both of which you define.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-threatintelset.html#cfn-guardduty-threatintelset-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnThreatIntelSetMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnThreatIntelSetPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_guardduty.mixins.CfnThreatIntelSetPropsMixin",
):
    '''The ``AWS::GuardDuty::ThreatIntelSet`` resource helps you create a list of known malicious IP addresses in your AWS environment.

    Once you activate this list, GuardDuty will use list the entries in this list as an additional source for threat detection and generate findings when there is an activity associated with these known malicious IP addresses. GuardDuty continues to monitor independently of this custom threat intelligence set.

    Only the users of the GuardDuty administrator account can manage this list. These settings automatically apply to the member accounts.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-threatintelset.html
    :cloudformationResource: AWS::GuardDuty::ThreatIntelSet
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_guardduty import mixins as guardduty_mixins
        
        cfn_threat_intel_set_props_mixin = guardduty_mixins.CfnThreatIntelSetPropsMixin(guardduty_mixins.CfnThreatIntelSetMixinProps(
            activate=False,
            detector_id="detectorId",
            expected_bucket_owner="expectedBucketOwner",
            format="format",
            location="location",
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
        props: typing.Union[CfnThreatIntelSetMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::GuardDuty::ThreatIntelSet``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5beb8c2058cefe1e272325538c5ded164253969740d56f48b5affbe68580ff6f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__21ef18946e04af9ac68ba8a43f8538eb8f8b723dbb2c2a378f4271d404392cc6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9875a1cc195284b2f0bba305c793167a9f0bbfc4b00d41ada6a602cb87d982b0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnThreatIntelSetMixinProps:
        return typing.cast(CfnThreatIntelSetMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_guardduty.mixins.CfnTrustedEntitySetMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "activate": "activate",
        "detector_id": "detectorId",
        "expected_bucket_owner": "expectedBucketOwner",
        "format": "format",
        "location": "location",
        "name": "name",
        "tags": "tags",
    },
)
class CfnTrustedEntitySetMixinProps:
    def __init__(
        self,
        *,
        activate: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        detector_id: typing.Optional[builtins.str] = None,
        expected_bucket_owner: typing.Optional[builtins.str] = None,
        format: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["CfnTrustedEntitySetPropsMixin.TagItemProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnTrustedEntitySetPropsMixin.

        :param activate: A boolean value that determines if GuardDuty can start using this list for custom threat detection. For GuardDuty to prevent generating findings based on an activity associated with these entries, this list must be active.
        :param detector_id: The unique regional detector ID of the GuardDuty account for which you want to create a trusted entity set. To find the ``detectorId`` in the current Region, see the Settings page in the GuardDuty console, or run the `ListDetectors <https://docs.aws.amazon.com/guardduty/latest/APIReference/API_ListDetectors.html>`_ API.
        :param expected_bucket_owner: The AWS account ID that owns the Amazon S3 bucket specified in the *Location* field. Whether or not you provide the account ID for this optional field, GuardDuty validates that the account ID associated with the ``DetectorId`` value owns the S3 bucket in the ``Location`` field. If GuardDuty finds that this S3 bucket doesn't belong to the specified account ID, you will get an error at the time of activating this list.
        :param format: The format of the file that contains the trusted entity set. For information about supported formats, see `List formats <https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_upload-lists.html#prepare_list>`_ in the *Amazon GuardDuty User Guide* .
        :param location: The URI of the file that contains the trusted entity set.
        :param name: A user-friendly name to identify the trusted entity set. Valid characters include lowercase letters, uppercase letters, numbers, dash(-), and underscore (_).
        :param tags: The tags to be added to a new trusted entity set resource. Each tag consists of a key and an optional value, both of which you define. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-trustedentityset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_guardduty import mixins as guardduty_mixins
            
            cfn_trusted_entity_set_mixin_props = guardduty_mixins.CfnTrustedEntitySetMixinProps(
                activate=False,
                detector_id="detectorId",
                expected_bucket_owner="expectedBucketOwner",
                format="format",
                location="location",
                name="name",
                tags=[guardduty_mixins.CfnTrustedEntitySetPropsMixin.TagItemProperty(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a61047fa48edf280f9777cf779fe1218d9367612abc5d0c1c9fb01c88254cbe9)
            check_type(argname="argument activate", value=activate, expected_type=type_hints["activate"])
            check_type(argname="argument detector_id", value=detector_id, expected_type=type_hints["detector_id"])
            check_type(argname="argument expected_bucket_owner", value=expected_bucket_owner, expected_type=type_hints["expected_bucket_owner"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if activate is not None:
            self._values["activate"] = activate
        if detector_id is not None:
            self._values["detector_id"] = detector_id
        if expected_bucket_owner is not None:
            self._values["expected_bucket_owner"] = expected_bucket_owner
        if format is not None:
            self._values["format"] = format
        if location is not None:
            self._values["location"] = location
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def activate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A boolean value that determines if GuardDuty can start using this list for custom threat detection.

        For GuardDuty to prevent generating findings based on an activity associated with these entries, this list must be active.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-trustedentityset.html#cfn-guardduty-trustedentityset-activate
        '''
        result = self._values.get("activate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def detector_id(self) -> typing.Optional[builtins.str]:
        '''The unique regional detector ID of the GuardDuty account for which you want to create a trusted entity set.

        To find the ``detectorId`` in the current Region, see the Settings page in the GuardDuty console, or run the `ListDetectors <https://docs.aws.amazon.com/guardduty/latest/APIReference/API_ListDetectors.html>`_ API.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-trustedentityset.html#cfn-guardduty-trustedentityset-detectorid
        '''
        result = self._values.get("detector_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expected_bucket_owner(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID that owns the Amazon S3 bucket specified in the *Location* field.

        Whether or not you provide the account ID for this optional field, GuardDuty validates that the account ID associated with the ``DetectorId`` value owns the S3 bucket in the ``Location`` field. If GuardDuty finds that this S3 bucket doesn't belong to the specified account ID, you will get an error at the time of activating this list.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-trustedentityset.html#cfn-guardduty-trustedentityset-expectedbucketowner
        '''
        result = self._values.get("expected_bucket_owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def format(self) -> typing.Optional[builtins.str]:
        '''The format of the file that contains the trusted entity set.

        For information about supported formats, see `List formats <https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_upload-lists.html#prepare_list>`_ in the *Amazon GuardDuty User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-trustedentityset.html#cfn-guardduty-trustedentityset-format
        '''
        result = self._values.get("format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The URI of the file that contains the trusted entity set.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-trustedentityset.html#cfn-guardduty-trustedentityset-location
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A user-friendly name to identify the trusted entity set.

        Valid characters include lowercase letters, uppercase letters, numbers, dash(-), and underscore (_).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-trustedentityset.html#cfn-guardduty-trustedentityset-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(
        self,
    ) -> typing.Optional[typing.List["CfnTrustedEntitySetPropsMixin.TagItemProperty"]]:
        '''The tags to be added to a new trusted entity set resource.

        Each tag consists of a key and an optional value, both of which you define.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-trustedentityset.html#cfn-guardduty-trustedentityset-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["CfnTrustedEntitySetPropsMixin.TagItemProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTrustedEntitySetMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnTrustedEntitySetPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_guardduty.mixins.CfnTrustedEntitySetPropsMixin",
):
    '''Creates a new trusted entity set.

    In the trusted entity set, you can provide IP addresses and domains that you believe are secure for communication in your AWS environment. GuardDuty will not generate findings for the entries that are specified in a trusted entity set. At any given time, you can have only one trusted entity set.

    Only users of the administrator account can manage the entity sets, which automatically apply to member accounts.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-trustedentityset.html
    :cloudformationResource: AWS::GuardDuty::TrustedEntitySet
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_guardduty import mixins as guardduty_mixins
        
        cfn_trusted_entity_set_props_mixin = guardduty_mixins.CfnTrustedEntitySetPropsMixin(guardduty_mixins.CfnTrustedEntitySetMixinProps(
            activate=False,
            detector_id="detectorId",
            expected_bucket_owner="expectedBucketOwner",
            format="format",
            location="location",
            name="name",
            tags=[guardduty_mixins.CfnTrustedEntitySetPropsMixin.TagItemProperty(
                key="key",
                value="value"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnTrustedEntitySetMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::GuardDuty::TrustedEntitySet``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ff8dc988549c8f9930e3707d0fa0ebb618204c1c86264b79ba25de28d937570)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bcba341dafaaa4ae42d9332743534654547fb0e01bf74a38d629506cba1d5198)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2d36e9d35d5ae8aa1c431b613093a4582704c42016852bc764b93205adf11e6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTrustedEntitySetMixinProps:
        return typing.cast(CfnTrustedEntitySetMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_guardduty.mixins.CfnTrustedEntitySetPropsMixin.TagItemProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TagItemProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes a tag.

            For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

            :param key: The tag key.
            :param value: The tag value. This is optional.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-trustedentityset-tagitem.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_guardduty import mixins as guardduty_mixins
                
                tag_item_property = guardduty_mixins.CfnTrustedEntitySetPropsMixin.TagItemProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__41c2cb820550f454863b7b27a4d2ba7238a125dbdd799b286ef78045b12e5f87)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The tag key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-trustedentityset-tagitem.html#cfn-guardduty-trustedentityset-tagitem-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The tag value.

            This is optional.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-trustedentityset-tagitem.html#cfn-guardduty-trustedentityset-tagitem-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagItemProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnDetectorMixinProps",
    "CfnDetectorPropsMixin",
    "CfnFilterMixinProps",
    "CfnFilterPropsMixin",
    "CfnIPSetMixinProps",
    "CfnIPSetPropsMixin",
    "CfnMalwareProtectionPlanMixinProps",
    "CfnMalwareProtectionPlanPropsMixin",
    "CfnMasterMixinProps",
    "CfnMasterPropsMixin",
    "CfnMemberMixinProps",
    "CfnMemberPropsMixin",
    "CfnPublishingDestinationMixinProps",
    "CfnPublishingDestinationPropsMixin",
    "CfnThreatEntitySetMixinProps",
    "CfnThreatEntitySetPropsMixin",
    "CfnThreatIntelSetMixinProps",
    "CfnThreatIntelSetPropsMixin",
    "CfnTrustedEntitySetMixinProps",
    "CfnTrustedEntitySetPropsMixin",
]

publication.publish()

def _typecheckingstub__883a81dafcde9c0df87748169824f5a372f2c64055971e3969497cb73f7536c5(
    *,
    data_sources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorPropsMixin.CFNDataSourceConfigurationsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    enable: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    features: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorPropsMixin.CFNFeatureConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    finding_publishing_frequency: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnDetectorPropsMixin.TagItemProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e641b1bb9ee99d91ab515c406437f8d04952f6280c85a1ffb30272c76330e1cf(
    props: typing.Union[CfnDetectorMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4591c02ade0b3d68bc05f2f350460ca2f3b1b9e4c909cb285e27cb5c4e4b2f7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__474f74b1a1bac845e9cec0456f64075ff8ab23d679218bdd5a0cffa6eb053d61(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ebed8bbda351905c6308ac86e49fa325502088a6a87674326026a9beebdb1d0(
    *,
    kubernetes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorPropsMixin.CFNKubernetesConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    malware_protection: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorPropsMixin.CFNMalwareProtectionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorPropsMixin.CFNS3LogsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2fa0f3322dda3edcf62b73ef7b47a1a1bb13236ce13981c0ef955da6716609c(
    *,
    name: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d616d1cb7fa440b8d453f6d7739b4904c87a97d4a37cdd2c66c89236f15ecba(
    *,
    additional_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorPropsMixin.CFNFeatureAdditionalConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    name: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95ff04533e66480f5035ba8148238dc8712c42f344f9ceccf9de72f89ece9713(
    *,
    enable: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e632566480af702f64343b47a487909e4e98891488b4cd186cf14827b9dd0424(
    *,
    audit_logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorPropsMixin.CFNKubernetesAuditLogsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2a2f6a537ab08c20166671c5df08a2c27900200abae4b70f03f890f607850b4(
    *,
    scan_ec2_instance_with_findings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorPropsMixin.CFNScanEc2InstanceWithFindingsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f3797b3ffcb5cfc99ece164da8daa052159ec8977c923b8ff4f683c09dbf9a9(
    *,
    enable: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d0e3c9488519266dbc05874572f219eb1c737d6a893c0904f7ef16f1aa72b7b(
    *,
    ebs_volumes: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a506433312af4b47d43e1d5d45eef146484d84624a1ccefd6473e4503a5e96c(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7945b40d785a0cf11bbe2d3ee3b2b0c249e8182e1718a3b79b3af54ae5b33ed5(
    *,
    action: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    detector_id: typing.Optional[builtins.str] = None,
    finding_criteria: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.FindingCriteriaProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    rank: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d53390215220d0bb24e5d5a000d54a98dc37b22827453ce3dcae59d293b5511(
    props: typing.Union[CfnFilterMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7ba28f15e9760f66d37ed2f3ebbb3d8f71b1a6380826bde7d2452c119304c8e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f047a8bb6a932936ae560b57a4018c431ed763d1b23121c682ec23ebb59b79ec(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e376dbe045f0f43c5a64c2282b80d4355bb09dae69d8bf5b1c49ef5f2181a89(
    *,
    eq: typing.Optional[typing.Sequence[builtins.str]] = None,
    equal_to: typing.Optional[typing.Sequence[builtins.str]] = None,
    greater_than: typing.Optional[jsii.Number] = None,
    greater_than_or_equal: typing.Optional[jsii.Number] = None,
    gt: typing.Optional[jsii.Number] = None,
    gte: typing.Optional[jsii.Number] = None,
    less_than: typing.Optional[jsii.Number] = None,
    less_than_or_equal: typing.Optional[jsii.Number] = None,
    lt: typing.Optional[jsii.Number] = None,
    lte: typing.Optional[jsii.Number] = None,
    neq: typing.Optional[typing.Sequence[builtins.str]] = None,
    not_equals: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__106802f46c9c141d4f3d013be3fe7492c389e46a8e6ef5702796e2c9e186ffae(
    *,
    criterion: typing.Any = None,
    item_type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.ConditionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1279eed9969f44d105998a8286ffff89cc1d7e59db31775d6cf1d803e9d12f5c(
    *,
    activate: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    detector_id: typing.Optional[builtins.str] = None,
    expected_bucket_owner: typing.Optional[builtins.str] = None,
    format: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3443eb64cbfd4cf39765b42ea1a3cf0b8bf7a211c593745d5ada8d498329d15d(
    props: typing.Union[CfnIPSetMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cae0f827c561420d6236228c792b2797ae157e9414363ef5e97638d25c1499ea(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a424ddc49b4635d9f65f382d7917a13bf339d666d8b1b4573f93f1f7473818cd(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c61be3ecb724212b92586e1a10b7d76d35ca2815f4382422c4d0c3c81fb7a33d(
    *,
    actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMalwareProtectionPlanPropsMixin.CFNActionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    protected_resource: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMalwareProtectionPlanPropsMixin.CFNProtectedResourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    role: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnMalwareProtectionPlanPropsMixin.TagItemProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77f6f8097171b51155d769a546f6f0e5bc951114fe583011b339494d847ea88b(
    props: typing.Union[CfnMalwareProtectionPlanMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32c211c4717648311b4d6df0ab46ab0a468516c5d2cbdd4981d7b45031e9dded(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4032aa219e5988af3d631ca978e574d416701d61fc8f77a5878a05113f99f7ab(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f83f90edbbc057c95834313577ebbb49af8146f48ec3ebf124af4bd398a51aca(
    *,
    tagging: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMalwareProtectionPlanPropsMixin.CFNTaggingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5596035c1b2372196f4df6e4e23b78ff2dbbe1bc539188b796393d924f72531(
    *,
    s3_bucket: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMalwareProtectionPlanPropsMixin.S3BucketProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b30c76a39ff18ff6929665ca5179e8ff20895e231c1937ac4ab6c2926620b29a(
    *,
    code: typing.Optional[builtins.str] = None,
    message: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc94c33f01b397d84a20e7f5749b4d2328da914d4bff2a0ab6c0ae557b196214(
    *,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76737cfe5b89f0461f4859fe8378793056f5443edf17267af3857fa89140e5f2(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    object_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c85686deb189451e52f191224741467d2c9b4198716d73afc36e71ec77fd0b8(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83fa1871aa734d50251056365ca201bbe1c3645a5678ebd0f6ba445ce8715b5f(
    *,
    detector_id: typing.Optional[builtins.str] = None,
    invitation_id: typing.Optional[builtins.str] = None,
    master_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31f089ecc4d0d34781c99b0937267abce5777f311c1008a1c26dd1717d5b49ef(
    props: typing.Union[CfnMasterMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aecf520d9b9b519bce136e337c17381ff4d18e526d35ae05948505b456fdb969(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d1f1851e9730df784a2ccb1dee7b53124c905706f0dfb4dce5f8f3022730bb1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f6f9d6afdb37fa56d79f6bc46f61cac57a8959125387810113f4444abbeabbd(
    *,
    detector_id: typing.Optional[builtins.str] = None,
    disable_email_notification: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    email: typing.Optional[builtins.str] = None,
    member_id: typing.Optional[builtins.str] = None,
    message: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__392807d794f05267d95a9d01cc401f953c47d8957faa258ed58147840a41e513(
    props: typing.Union[CfnMemberMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64da5ece26e87f07a19c2dc5c60134950338a3bccfedd611454d73d2a981810a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e102b2c8dee2de8fea9b2e4c50c3556479e308c88a6cc6b88bba7f0830ca06a5(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f66cb101923801014da5bd7595bb040bd164f190537c782c4df380ff86b76278(
    *,
    destination_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPublishingDestinationPropsMixin.CFNDestinationPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    destination_type: typing.Optional[builtins.str] = None,
    detector_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnPublishingDestinationPropsMixin.TagItemProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ba0f8dad44e13844cd9444de66fad4a3330e75228c20c7e1cff15b89206c20f(
    props: typing.Union[CfnPublishingDestinationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f9cdcb37d616ec702e2fbfd8e0ba2664030b8cdbf44fdd08671e404bbd66452(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca05821294bf0f5520ccb953f827e38b892ff5e3561dc51943c7f7678ef72d30(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb7c59164a86cc546687c7bc558823e45483c6479f4fedca6a0299ac5391cfd5(
    *,
    destination_arn: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8e62b62b8328a348441b1f93842f1317775a6fc3d44395dee1df9f380eb138f(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39a3a353b0cea5cdb09bdfb91019597550cb207c6ddc4dcbf7ae929662f8bfb8(
    *,
    activate: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    detector_id: typing.Optional[builtins.str] = None,
    expected_bucket_owner: typing.Optional[builtins.str] = None,
    format: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnThreatEntitySetPropsMixin.TagItemProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f9ca7441561e1f1a181dd2c6c3855dfa4e793ee963244344c0a5568f50afaae(
    props: typing.Union[CfnThreatEntitySetMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ff516b3c5fb6305e980cb189f273cc773b3dfef05e049691da70a386d4806a8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5ecab8be1bd228b1bc9b35367e7755b2af72dbc5c1c8fd88660e4ea373a1c15(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7becf9ade2f0635b74650ce5c32ca5e01d54b5a1ecbd43a8f9e57203d54cc92(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__350503e05fc2192a357c195ee8de774f8aac84762eb5c8ac3bf7aaf82b6cc27d(
    *,
    activate: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    detector_id: typing.Optional[builtins.str] = None,
    expected_bucket_owner: typing.Optional[builtins.str] = None,
    format: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5beb8c2058cefe1e272325538c5ded164253969740d56f48b5affbe68580ff6f(
    props: typing.Union[CfnThreatIntelSetMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21ef18946e04af9ac68ba8a43f8538eb8f8b723dbb2c2a378f4271d404392cc6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9875a1cc195284b2f0bba305c793167a9f0bbfc4b00d41ada6a602cb87d982b0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a61047fa48edf280f9777cf779fe1218d9367612abc5d0c1c9fb01c88254cbe9(
    *,
    activate: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    detector_id: typing.Optional[builtins.str] = None,
    expected_bucket_owner: typing.Optional[builtins.str] = None,
    format: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnTrustedEntitySetPropsMixin.TagItemProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ff8dc988549c8f9930e3707d0fa0ebb618204c1c86264b79ba25de28d937570(
    props: typing.Union[CfnTrustedEntitySetMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcba341dafaaa4ae42d9332743534654547fb0e01bf74a38d629506cba1d5198(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2d36e9d35d5ae8aa1c431b613093a4582704c42016852bc764b93205adf11e6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41c2cb820550f454863b7b27a4d2ba7238a125dbdd799b286ef78045b12e5f87(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
