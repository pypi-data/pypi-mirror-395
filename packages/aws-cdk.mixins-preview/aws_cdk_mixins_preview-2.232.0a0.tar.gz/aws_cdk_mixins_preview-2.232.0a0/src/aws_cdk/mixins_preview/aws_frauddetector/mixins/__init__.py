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
    jsii_type="@aws-cdk/mixins-preview.aws_frauddetector.mixins.CfnDetectorMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "associated_models": "associatedModels",
        "description": "description",
        "detector_id": "detectorId",
        "detector_version_status": "detectorVersionStatus",
        "event_type": "eventType",
        "rule_execution_mode": "ruleExecutionMode",
        "rules": "rules",
        "tags": "tags",
    },
)
class CfnDetectorMixinProps:
    def __init__(
        self,
        *,
        associated_models: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorPropsMixin.ModelProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        detector_id: typing.Optional[builtins.str] = None,
        detector_version_status: typing.Optional[builtins.str] = None,
        event_type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorPropsMixin.EventTypeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        rule_execution_mode: typing.Optional[builtins.str] = None,
        rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorPropsMixin.RuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDetectorPropsMixin.

        :param associated_models: The models to associate with this detector. You must provide the ARNs of all the models you want to associate.
        :param description: The detector description.
        :param detector_id: The name of the detector.
        :param detector_version_status: The status of the detector version. If a value is not provided for this property, AWS CloudFormation assumes ``DRAFT`` status. Valid values: ``ACTIVE | DRAFT``
        :param event_type: The event type associated with this detector.
        :param rule_execution_mode: The rule execution mode for the rules included in the detector version. Valid values: ``FIRST_MATCHED | ALL_MATCHED`` Default value: ``FIRST_MATCHED`` You can define and edit the rule mode at the detector version level, when it is in draft status. If you specify ``FIRST_MATCHED`` , Amazon Fraud Detector evaluates rules sequentially, first to last, stopping at the first matched rule. Amazon Fraud dectector then provides the outcomes for that single rule. If you specifiy ``ALL_MATCHED`` , Amazon Fraud Detector evaluates all rules and returns the outcomes for all matched rules.
        :param rules: The rules to include in the detector version.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-detector.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_frauddetector import mixins as frauddetector_mixins
            
            cfn_detector_mixin_props = frauddetector_mixins.CfnDetectorMixinProps(
                associated_models=[frauddetector_mixins.CfnDetectorPropsMixin.ModelProperty(
                    arn="arn"
                )],
                description="description",
                detector_id="detectorId",
                detector_version_status="detectorVersionStatus",
                event_type=frauddetector_mixins.CfnDetectorPropsMixin.EventTypeProperty(
                    arn="arn",
                    created_time="createdTime",
                    description="description",
                    entity_types=[frauddetector_mixins.CfnDetectorPropsMixin.EntityTypeProperty(
                        arn="arn",
                        created_time="createdTime",
                        description="description",
                        inline=False,
                        last_updated_time="lastUpdatedTime",
                        name="name",
                        tags=[CfnTag(
                            key="key",
                            value="value"
                        )]
                    )],
                    event_variables=[frauddetector_mixins.CfnDetectorPropsMixin.EventVariableProperty(
                        arn="arn",
                        created_time="createdTime",
                        data_source="dataSource",
                        data_type="dataType",
                        default_value="defaultValue",
                        description="description",
                        inline=False,
                        last_updated_time="lastUpdatedTime",
                        name="name",
                        tags=[CfnTag(
                            key="key",
                            value="value"
                        )],
                        variable_type="variableType"
                    )],
                    inline=False,
                    labels=[frauddetector_mixins.CfnDetectorPropsMixin.LabelProperty(
                        arn="arn",
                        created_time="createdTime",
                        description="description",
                        inline=False,
                        last_updated_time="lastUpdatedTime",
                        name="name",
                        tags=[CfnTag(
                            key="key",
                            value="value"
                        )]
                    )],
                    last_updated_time="lastUpdatedTime",
                    name="name",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                ),
                rule_execution_mode="ruleExecutionMode",
                rules=[frauddetector_mixins.CfnDetectorPropsMixin.RuleProperty(
                    arn="arn",
                    created_time="createdTime",
                    description="description",
                    detector_id="detectorId",
                    expression="expression",
                    language="language",
                    last_updated_time="lastUpdatedTime",
                    outcomes=[frauddetector_mixins.CfnDetectorPropsMixin.OutcomeProperty(
                        arn="arn",
                        created_time="createdTime",
                        description="description",
                        inline=False,
                        last_updated_time="lastUpdatedTime",
                        name="name",
                        tags=[CfnTag(
                            key="key",
                            value="value"
                        )]
                    )],
                    rule_id="ruleId",
                    rule_version="ruleVersion",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dbc330817d424a8711de180d276e7af85d8ce7db7c9ce4774f16ebdb2bf1c3e)
            check_type(argname="argument associated_models", value=associated_models, expected_type=type_hints["associated_models"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument detector_id", value=detector_id, expected_type=type_hints["detector_id"])
            check_type(argname="argument detector_version_status", value=detector_version_status, expected_type=type_hints["detector_version_status"])
            check_type(argname="argument event_type", value=event_type, expected_type=type_hints["event_type"])
            check_type(argname="argument rule_execution_mode", value=rule_execution_mode, expected_type=type_hints["rule_execution_mode"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if associated_models is not None:
            self._values["associated_models"] = associated_models
        if description is not None:
            self._values["description"] = description
        if detector_id is not None:
            self._values["detector_id"] = detector_id
        if detector_version_status is not None:
            self._values["detector_version_status"] = detector_version_status
        if event_type is not None:
            self._values["event_type"] = event_type
        if rule_execution_mode is not None:
            self._values["rule_execution_mode"] = rule_execution_mode
        if rules is not None:
            self._values["rules"] = rules
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def associated_models(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorPropsMixin.ModelProperty"]]]]:
        '''The models to associate with this detector.

        You must provide the ARNs of all the models you want to associate.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-detector.html#cfn-frauddetector-detector-associatedmodels
        '''
        result = self._values.get("associated_models")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorPropsMixin.ModelProperty"]]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The detector description.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-detector.html#cfn-frauddetector-detector-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def detector_id(self) -> typing.Optional[builtins.str]:
        '''The name of the detector.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-detector.html#cfn-frauddetector-detector-detectorid
        '''
        result = self._values.get("detector_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def detector_version_status(self) -> typing.Optional[builtins.str]:
        '''The status of the detector version.

        If a value is not provided for this property, AWS CloudFormation assumes ``DRAFT`` status.

        Valid values: ``ACTIVE | DRAFT``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-detector.html#cfn-frauddetector-detector-detectorversionstatus
        '''
        result = self._values.get("detector_version_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_type(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorPropsMixin.EventTypeProperty"]]:
        '''The event type associated with this detector.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-detector.html#cfn-frauddetector-detector-eventtype
        '''
        result = self._values.get("event_type")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorPropsMixin.EventTypeProperty"]], result)

    @builtins.property
    def rule_execution_mode(self) -> typing.Optional[builtins.str]:
        '''The rule execution mode for the rules included in the detector version.

        Valid values: ``FIRST_MATCHED | ALL_MATCHED`` Default value: ``FIRST_MATCHED``

        You can define and edit the rule mode at the detector version level, when it is in draft status.

        If you specify ``FIRST_MATCHED`` , Amazon Fraud Detector evaluates rules sequentially, first to last, stopping at the first matched rule. Amazon Fraud dectector then provides the outcomes for that single rule.

        If you specifiy ``ALL_MATCHED`` , Amazon Fraud Detector evaluates all rules and returns the outcomes for all matched rules.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-detector.html#cfn-frauddetector-detector-ruleexecutionmode
        '''
        result = self._values.get("rule_execution_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rules(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorPropsMixin.RuleProperty"]]]]:
        '''The rules to include in the detector version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-detector.html#cfn-frauddetector-detector-rules
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorPropsMixin.RuleProperty"]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-detector.html#cfn-frauddetector-detector-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

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
    jsii_type="@aws-cdk/mixins-preview.aws_frauddetector.mixins.CfnDetectorPropsMixin",
):
    '''Manages a detector and associated detector versions.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-detector.html
    :cloudformationResource: AWS::FraudDetector::Detector
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_frauddetector import mixins as frauddetector_mixins
        
        cfn_detector_props_mixin = frauddetector_mixins.CfnDetectorPropsMixin(frauddetector_mixins.CfnDetectorMixinProps(
            associated_models=[frauddetector_mixins.CfnDetectorPropsMixin.ModelProperty(
                arn="arn"
            )],
            description="description",
            detector_id="detectorId",
            detector_version_status="detectorVersionStatus",
            event_type=frauddetector_mixins.CfnDetectorPropsMixin.EventTypeProperty(
                arn="arn",
                created_time="createdTime",
                description="description",
                entity_types=[frauddetector_mixins.CfnDetectorPropsMixin.EntityTypeProperty(
                    arn="arn",
                    created_time="createdTime",
                    description="description",
                    inline=False,
                    last_updated_time="lastUpdatedTime",
                    name="name",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )],
                event_variables=[frauddetector_mixins.CfnDetectorPropsMixin.EventVariableProperty(
                    arn="arn",
                    created_time="createdTime",
                    data_source="dataSource",
                    data_type="dataType",
                    default_value="defaultValue",
                    description="description",
                    inline=False,
                    last_updated_time="lastUpdatedTime",
                    name="name",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )],
                    variable_type="variableType"
                )],
                inline=False,
                labels=[frauddetector_mixins.CfnDetectorPropsMixin.LabelProperty(
                    arn="arn",
                    created_time="createdTime",
                    description="description",
                    inline=False,
                    last_updated_time="lastUpdatedTime",
                    name="name",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )],
                last_updated_time="lastUpdatedTime",
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            ),
            rule_execution_mode="ruleExecutionMode",
            rules=[frauddetector_mixins.CfnDetectorPropsMixin.RuleProperty(
                arn="arn",
                created_time="createdTime",
                description="description",
                detector_id="detectorId",
                expression="expression",
                language="language",
                last_updated_time="lastUpdatedTime",
                outcomes=[frauddetector_mixins.CfnDetectorPropsMixin.OutcomeProperty(
                    arn="arn",
                    created_time="createdTime",
                    description="description",
                    inline=False,
                    last_updated_time="lastUpdatedTime",
                    name="name",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )],
                rule_id="ruleId",
                rule_version="ruleVersion",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
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
        props: typing.Union[CfnDetectorMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::FraudDetector::Detector``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__827f634a3f1cf909024d15cb5a36a14661f5ce89f33b61b84c23ad4b02a27076)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6ec9f14ecc1219370644e1b7a537ba84994757462603dcc281394e7eeb81d8c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4134b1016e17b80a5079e6cd46f487cce3b62e2f097949b58817b6bbe9cdd2f)
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
        jsii_type="@aws-cdk/mixins-preview.aws_frauddetector.mixins.CfnDetectorPropsMixin.EntityTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "arn": "arn",
            "created_time": "createdTime",
            "description": "description",
            "inline": "inline",
            "last_updated_time": "lastUpdatedTime",
            "name": "name",
            "tags": "tags",
        },
    )
    class EntityTypeProperty:
        def __init__(
            self,
            *,
            arn: typing.Optional[builtins.str] = None,
            created_time: typing.Optional[builtins.str] = None,
            description: typing.Optional[builtins.str] = None,
            inline: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            last_updated_time: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The entity type details.

            :param arn: The entity type ARN.
            :param created_time: Timestamp of when the entity type was created.
            :param description: The entity type description.
            :param inline: Indicates whether the resource is defined within this CloudFormation template and impacts the create, update, and delete behavior of the stack. If the value is ``true`` , CloudFormation will create/update/delete the resource when creating/updating/deleting the stack. If the value is ``false`` , CloudFormation will validate that the object exists and then use it within the resource without making changes to the object. For example, when creating ``AWS::FraudDetector::Detector`` you must define at least two variables. You can set ``Inline=true`` for these Variables and CloudFormation will create/update/delete the variables as part of stack operations. However, if you set ``Inline=false`` , CloudFormation will associate the variables to your detector but not execute any changes to the variables.
            :param last_updated_time: Timestamp of when the entity type was last updated.
            :param name: The entity type name.
            :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-entitytype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_frauddetector import mixins as frauddetector_mixins
                
                entity_type_property = frauddetector_mixins.CfnDetectorPropsMixin.EntityTypeProperty(
                    arn="arn",
                    created_time="createdTime",
                    description="description",
                    inline=False,
                    last_updated_time="lastUpdatedTime",
                    name="name",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__10c4f2c60d4fe661e3fb8accc47ef2bebb0bc783de117aea7c821808fe14044b)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                check_type(argname="argument created_time", value=created_time, expected_type=type_hints["created_time"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument inline", value=inline, expected_type=type_hints["inline"])
                check_type(argname="argument last_updated_time", value=last_updated_time, expected_type=type_hints["last_updated_time"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn
            if created_time is not None:
                self._values["created_time"] = created_time
            if description is not None:
                self._values["description"] = description
            if inline is not None:
                self._values["inline"] = inline
            if last_updated_time is not None:
                self._values["last_updated_time"] = last_updated_time
            if name is not None:
                self._values["name"] = name
            if tags is not None:
                self._values["tags"] = tags

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The entity type ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-entitytype.html#cfn-frauddetector-detector-entitytype-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def created_time(self) -> typing.Optional[builtins.str]:
            '''Timestamp of when the entity type was created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-entitytype.html#cfn-frauddetector-detector-entitytype-createdtime
            '''
            result = self._values.get("created_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The entity type description.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-entitytype.html#cfn-frauddetector-detector-entitytype-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def inline(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether the resource is defined within this CloudFormation template and impacts the create, update, and delete behavior of the stack.

            If the value is ``true`` , CloudFormation will create/update/delete the resource when creating/updating/deleting the stack. If the value is ``false`` , CloudFormation will validate that the object exists and then use it within the resource without making changes to the object.

            For example, when creating ``AWS::FraudDetector::Detector`` you must define at least two variables. You can set ``Inline=true`` for these Variables and CloudFormation will create/update/delete the variables as part of stack operations. However, if you set ``Inline=false`` , CloudFormation will associate the variables to your detector but not execute any changes to the variables.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-entitytype.html#cfn-frauddetector-detector-entitytype-inline
            '''
            result = self._values.get("inline")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def last_updated_time(self) -> typing.Optional[builtins.str]:
            '''Timestamp of when the entity type was last updated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-entitytype.html#cfn-frauddetector-detector-entitytype-lastupdatedtime
            '''
            result = self._values.get("last_updated_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The entity type name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-entitytype.html#cfn-frauddetector-detector-entitytype-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
            '''An array of key-value pairs to apply to this resource.

            For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-entitytype.html#cfn-frauddetector-detector-entitytype-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EntityTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_frauddetector.mixins.CfnDetectorPropsMixin.EventTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "arn": "arn",
            "created_time": "createdTime",
            "description": "description",
            "entity_types": "entityTypes",
            "event_variables": "eventVariables",
            "inline": "inline",
            "labels": "labels",
            "last_updated_time": "lastUpdatedTime",
            "name": "name",
            "tags": "tags",
        },
    )
    class EventTypeProperty:
        def __init__(
            self,
            *,
            arn: typing.Optional[builtins.str] = None,
            created_time: typing.Optional[builtins.str] = None,
            description: typing.Optional[builtins.str] = None,
            entity_types: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorPropsMixin.EntityTypeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            event_variables: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorPropsMixin.EventVariableProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            inline: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            labels: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorPropsMixin.LabelProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            last_updated_time: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The event type details.

            :param arn: The entity type ARN.
            :param created_time: Timestamp of when the event type was created.
            :param description: The event type description.
            :param entity_types: The event type entity types.
            :param event_variables: The event type event variables.
            :param inline: Indicates whether the resource is defined within this CloudFormation template and impacts the create, update, and delete behavior of the stack. If the value is ``true`` , CloudFormation will create/update/delete the resource when creating/updating/deleting the stack. If the value is ``false`` , CloudFormation will validate that the object exists and then use it within the resource without making changes to the object. For example, when creating ``AWS::FraudDetector::Detector`` you must define at least two variables. You can set ``Inline=true`` for these variables and CloudFormation will create/update/delete the Variables as part of stack operations. However, if you set ``Inline=false`` , CloudFormation will associate the variables to your detector but not execute any changes to the variables.
            :param labels: The event type labels.
            :param last_updated_time: Timestamp of when the event type was last updated.
            :param name: The event type name.
            :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-eventtype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_frauddetector import mixins as frauddetector_mixins
                
                event_type_property = frauddetector_mixins.CfnDetectorPropsMixin.EventTypeProperty(
                    arn="arn",
                    created_time="createdTime",
                    description="description",
                    entity_types=[frauddetector_mixins.CfnDetectorPropsMixin.EntityTypeProperty(
                        arn="arn",
                        created_time="createdTime",
                        description="description",
                        inline=False,
                        last_updated_time="lastUpdatedTime",
                        name="name",
                        tags=[CfnTag(
                            key="key",
                            value="value"
                        )]
                    )],
                    event_variables=[frauddetector_mixins.CfnDetectorPropsMixin.EventVariableProperty(
                        arn="arn",
                        created_time="createdTime",
                        data_source="dataSource",
                        data_type="dataType",
                        default_value="defaultValue",
                        description="description",
                        inline=False,
                        last_updated_time="lastUpdatedTime",
                        name="name",
                        tags=[CfnTag(
                            key="key",
                            value="value"
                        )],
                        variable_type="variableType"
                    )],
                    inline=False,
                    labels=[frauddetector_mixins.CfnDetectorPropsMixin.LabelProperty(
                        arn="arn",
                        created_time="createdTime",
                        description="description",
                        inline=False,
                        last_updated_time="lastUpdatedTime",
                        name="name",
                        tags=[CfnTag(
                            key="key",
                            value="value"
                        )]
                    )],
                    last_updated_time="lastUpdatedTime",
                    name="name",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d0b59af5b64a98f09a9950332041c5126deb0d5251c77c26b370e213d5bd0bcb)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                check_type(argname="argument created_time", value=created_time, expected_type=type_hints["created_time"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument entity_types", value=entity_types, expected_type=type_hints["entity_types"])
                check_type(argname="argument event_variables", value=event_variables, expected_type=type_hints["event_variables"])
                check_type(argname="argument inline", value=inline, expected_type=type_hints["inline"])
                check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
                check_type(argname="argument last_updated_time", value=last_updated_time, expected_type=type_hints["last_updated_time"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn
            if created_time is not None:
                self._values["created_time"] = created_time
            if description is not None:
                self._values["description"] = description
            if entity_types is not None:
                self._values["entity_types"] = entity_types
            if event_variables is not None:
                self._values["event_variables"] = event_variables
            if inline is not None:
                self._values["inline"] = inline
            if labels is not None:
                self._values["labels"] = labels
            if last_updated_time is not None:
                self._values["last_updated_time"] = last_updated_time
            if name is not None:
                self._values["name"] = name
            if tags is not None:
                self._values["tags"] = tags

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The entity type ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-eventtype.html#cfn-frauddetector-detector-eventtype-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def created_time(self) -> typing.Optional[builtins.str]:
            '''Timestamp of when the event type was created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-eventtype.html#cfn-frauddetector-detector-eventtype-createdtime
            '''
            result = self._values.get("created_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The event type description.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-eventtype.html#cfn-frauddetector-detector-eventtype-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def entity_types(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorPropsMixin.EntityTypeProperty"]]]]:
            '''The event type entity types.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-eventtype.html#cfn-frauddetector-detector-eventtype-entitytypes
            '''
            result = self._values.get("entity_types")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorPropsMixin.EntityTypeProperty"]]]], result)

        @builtins.property
        def event_variables(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorPropsMixin.EventVariableProperty"]]]]:
            '''The event type event variables.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-eventtype.html#cfn-frauddetector-detector-eventtype-eventvariables
            '''
            result = self._values.get("event_variables")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorPropsMixin.EventVariableProperty"]]]], result)

        @builtins.property
        def inline(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether the resource is defined within this CloudFormation template and impacts the create, update, and delete behavior of the stack.

            If the value is ``true`` , CloudFormation will create/update/delete the resource when creating/updating/deleting the stack. If the value is ``false`` , CloudFormation will validate that the object exists and then use it within the resource without making changes to the object.

            For example, when creating ``AWS::FraudDetector::Detector`` you must define at least two variables. You can set ``Inline=true`` for these variables and CloudFormation will create/update/delete the Variables as part of stack operations. However, if you set ``Inline=false`` , CloudFormation will associate the variables to your detector but not execute any changes to the variables.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-eventtype.html#cfn-frauddetector-detector-eventtype-inline
            '''
            result = self._values.get("inline")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def labels(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorPropsMixin.LabelProperty"]]]]:
            '''The event type labels.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-eventtype.html#cfn-frauddetector-detector-eventtype-labels
            '''
            result = self._values.get("labels")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorPropsMixin.LabelProperty"]]]], result)

        @builtins.property
        def last_updated_time(self) -> typing.Optional[builtins.str]:
            '''Timestamp of when the event type was last updated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-eventtype.html#cfn-frauddetector-detector-eventtype-lastupdatedtime
            '''
            result = self._values.get("last_updated_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The event type name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-eventtype.html#cfn-frauddetector-detector-eventtype-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
            '''An array of key-value pairs to apply to this resource.

            For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-eventtype.html#cfn-frauddetector-detector-eventtype-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_frauddetector.mixins.CfnDetectorPropsMixin.EventVariableProperty",
        jsii_struct_bases=[],
        name_mapping={
            "arn": "arn",
            "created_time": "createdTime",
            "data_source": "dataSource",
            "data_type": "dataType",
            "default_value": "defaultValue",
            "description": "description",
            "inline": "inline",
            "last_updated_time": "lastUpdatedTime",
            "name": "name",
            "tags": "tags",
            "variable_type": "variableType",
        },
    )
    class EventVariableProperty:
        def __init__(
            self,
            *,
            arn: typing.Optional[builtins.str] = None,
            created_time: typing.Optional[builtins.str] = None,
            data_source: typing.Optional[builtins.str] = None,
            data_type: typing.Optional[builtins.str] = None,
            default_value: typing.Optional[builtins.str] = None,
            description: typing.Optional[builtins.str] = None,
            inline: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            last_updated_time: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
            variable_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The event type variable for the detector.

            :param arn: The event variable ARN.
            :param created_time: Timestamp for when the event variable was created.
            :param data_source: The data source of the event variable. Valid values: ``EVENT | EXTERNAL_MODEL_SCORE`` When defining a variable within a detector, you can only use the ``EVENT`` value for DataSource when the *Inline* property is set to true. If the *Inline* property is set false, you can use either ``EVENT`` or ``MODEL_SCORE`` for DataSource.
            :param data_type: The data type of the event variable. Valid values: ``STRING | INTEGER | BOOLEAN | FLOAT``
            :param default_value: The default value of the event variable. This is required if you are providing the details of your variables instead of the ARN.
            :param description: The description of the event variable.
            :param inline: Indicates whether the resource is defined within this CloudFormation template and impacts the create, update, and delete behavior of the stack. If the value is ``true`` , CloudFormation will create/update/delete the resource when creating/updating/deleting the stack. If the value is ``false`` , CloudFormation will validate that the object exists and then use it within the resource without making changes to the object. For example, when creating ``AWS::FraudDetector::Detector`` you must define at least two variables. You can set ``Inline=true`` for these variables and CloudFormation will create/update/delete the variables as part of stack operations. However, if you set ``Inline=false`` , CloudFormation will associate the variables to your detector but not execute any changes to the variables.
            :param last_updated_time: Timestamp for when the event variable was last updated.
            :param name: The name of the event variable.
            :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
            :param variable_type: The type of event variable. For more information, see `Variable types <https://docs.aws.amazon.com/frauddetector/latest/ug/create-a-variable.html#variable-types>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-eventvariable.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_frauddetector import mixins as frauddetector_mixins
                
                event_variable_property = frauddetector_mixins.CfnDetectorPropsMixin.EventVariableProperty(
                    arn="arn",
                    created_time="createdTime",
                    data_source="dataSource",
                    data_type="dataType",
                    default_value="defaultValue",
                    description="description",
                    inline=False,
                    last_updated_time="lastUpdatedTime",
                    name="name",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )],
                    variable_type="variableType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__517684892c045645fb24b140f18a7239cca883dfec541f5442643ed8ee9b12ef)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                check_type(argname="argument created_time", value=created_time, expected_type=type_hints["created_time"])
                check_type(argname="argument data_source", value=data_source, expected_type=type_hints["data_source"])
                check_type(argname="argument data_type", value=data_type, expected_type=type_hints["data_type"])
                check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument inline", value=inline, expected_type=type_hints["inline"])
                check_type(argname="argument last_updated_time", value=last_updated_time, expected_type=type_hints["last_updated_time"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
                check_type(argname="argument variable_type", value=variable_type, expected_type=type_hints["variable_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn
            if created_time is not None:
                self._values["created_time"] = created_time
            if data_source is not None:
                self._values["data_source"] = data_source
            if data_type is not None:
                self._values["data_type"] = data_type
            if default_value is not None:
                self._values["default_value"] = default_value
            if description is not None:
                self._values["description"] = description
            if inline is not None:
                self._values["inline"] = inline
            if last_updated_time is not None:
                self._values["last_updated_time"] = last_updated_time
            if name is not None:
                self._values["name"] = name
            if tags is not None:
                self._values["tags"] = tags
            if variable_type is not None:
                self._values["variable_type"] = variable_type

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The event variable ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-eventvariable.html#cfn-frauddetector-detector-eventvariable-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def created_time(self) -> typing.Optional[builtins.str]:
            '''Timestamp for when the event variable was created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-eventvariable.html#cfn-frauddetector-detector-eventvariable-createdtime
            '''
            result = self._values.get("created_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def data_source(self) -> typing.Optional[builtins.str]:
            '''The data source of the event variable.

            Valid values: ``EVENT | EXTERNAL_MODEL_SCORE``

            When defining a variable within a detector, you can only use the ``EVENT`` value for DataSource when the *Inline* property is set to true. If the *Inline* property is set false, you can use either ``EVENT`` or ``MODEL_SCORE`` for DataSource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-eventvariable.html#cfn-frauddetector-detector-eventvariable-datasource
            '''
            result = self._values.get("data_source")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def data_type(self) -> typing.Optional[builtins.str]:
            '''The data type of the event variable.

            Valid values: ``STRING | INTEGER | BOOLEAN | FLOAT``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-eventvariable.html#cfn-frauddetector-detector-eventvariable-datatype
            '''
            result = self._values.get("data_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def default_value(self) -> typing.Optional[builtins.str]:
            '''The default value of the event variable.

            This is required if you are providing the details of your variables instead of the ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-eventvariable.html#cfn-frauddetector-detector-eventvariable-defaultvalue
            '''
            result = self._values.get("default_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The description of the event variable.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-eventvariable.html#cfn-frauddetector-detector-eventvariable-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def inline(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether the resource is defined within this CloudFormation template and impacts the create, update, and delete behavior of the stack.

            If the value is ``true`` , CloudFormation will create/update/delete the resource when creating/updating/deleting the stack. If the value is ``false`` , CloudFormation will validate that the object exists and then use it within the resource without making changes to the object.

            For example, when creating ``AWS::FraudDetector::Detector`` you must define at least two variables. You can set ``Inline=true`` for these variables and CloudFormation will create/update/delete the variables as part of stack operations. However, if you set ``Inline=false`` , CloudFormation will associate the variables to your detector but not execute any changes to the variables.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-eventvariable.html#cfn-frauddetector-detector-eventvariable-inline
            '''
            result = self._values.get("inline")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def last_updated_time(self) -> typing.Optional[builtins.str]:
            '''Timestamp for when the event variable was last updated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-eventvariable.html#cfn-frauddetector-detector-eventvariable-lastupdatedtime
            '''
            result = self._values.get("last_updated_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the event variable.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-eventvariable.html#cfn-frauddetector-detector-eventvariable-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
            '''An array of key-value pairs to apply to this resource.

            For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-eventvariable.html#cfn-frauddetector-detector-eventvariable-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

        @builtins.property
        def variable_type(self) -> typing.Optional[builtins.str]:
            '''The type of event variable.

            For more information, see `Variable types <https://docs.aws.amazon.com/frauddetector/latest/ug/create-a-variable.html#variable-types>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-eventvariable.html#cfn-frauddetector-detector-eventvariable-variabletype
            '''
            result = self._values.get("variable_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventVariableProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_frauddetector.mixins.CfnDetectorPropsMixin.LabelProperty",
        jsii_struct_bases=[],
        name_mapping={
            "arn": "arn",
            "created_time": "createdTime",
            "description": "description",
            "inline": "inline",
            "last_updated_time": "lastUpdatedTime",
            "name": "name",
            "tags": "tags",
        },
    )
    class LabelProperty:
        def __init__(
            self,
            *,
            arn: typing.Optional[builtins.str] = None,
            created_time: typing.Optional[builtins.str] = None,
            description: typing.Optional[builtins.str] = None,
            inline: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            last_updated_time: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The label details.

            :param arn: The label ARN.
            :param created_time: Timestamp of when the event type was created.
            :param description: The label description.
            :param inline: Indicates whether the resource is defined within this CloudFormation template and impacts the create, update, and delete behavior of the stack. If the value is ``true`` , CloudFormation will create/update/delete the resource when creating/updating/deleting the stack. If the value is ``false`` , CloudFormation will validate that the object exists and then use it within the resource without making changes to the object. For example, when creating ``AWS::FraudDetector::Detector`` you must define at least two variables. You can set ``Inline=true`` for these variables and CloudFormation will create/update/delete the variables as part of stack operations. However, if you set ``Inline=false`` , CloudFormation will associate the variables to your detector but not execute any changes to the variables.
            :param last_updated_time: Timestamp of when the label was last updated.
            :param name: The label name.
            :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-label.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_frauddetector import mixins as frauddetector_mixins
                
                label_property = frauddetector_mixins.CfnDetectorPropsMixin.LabelProperty(
                    arn="arn",
                    created_time="createdTime",
                    description="description",
                    inline=False,
                    last_updated_time="lastUpdatedTime",
                    name="name",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0f9a38e9735ca460faf12b27e09581eba0a87f277bb36c9aa51176c40aa48752)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                check_type(argname="argument created_time", value=created_time, expected_type=type_hints["created_time"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument inline", value=inline, expected_type=type_hints["inline"])
                check_type(argname="argument last_updated_time", value=last_updated_time, expected_type=type_hints["last_updated_time"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn
            if created_time is not None:
                self._values["created_time"] = created_time
            if description is not None:
                self._values["description"] = description
            if inline is not None:
                self._values["inline"] = inline
            if last_updated_time is not None:
                self._values["last_updated_time"] = last_updated_time
            if name is not None:
                self._values["name"] = name
            if tags is not None:
                self._values["tags"] = tags

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The label ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-label.html#cfn-frauddetector-detector-label-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def created_time(self) -> typing.Optional[builtins.str]:
            '''Timestamp of when the event type was created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-label.html#cfn-frauddetector-detector-label-createdtime
            '''
            result = self._values.get("created_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The label description.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-label.html#cfn-frauddetector-detector-label-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def inline(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether the resource is defined within this CloudFormation template and impacts the create, update, and delete behavior of the stack.

            If the value is ``true`` , CloudFormation will create/update/delete the resource when creating/updating/deleting the stack. If the value is ``false`` , CloudFormation will validate that the object exists and then use it within the resource without making changes to the object.

            For example, when creating ``AWS::FraudDetector::Detector`` you must define at least two variables. You can set ``Inline=true`` for these variables and CloudFormation will create/update/delete the variables as part of stack operations. However, if you set ``Inline=false`` , CloudFormation will associate the variables to your detector but not execute any changes to the variables.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-label.html#cfn-frauddetector-detector-label-inline
            '''
            result = self._values.get("inline")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def last_updated_time(self) -> typing.Optional[builtins.str]:
            '''Timestamp of when the label was last updated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-label.html#cfn-frauddetector-detector-label-lastupdatedtime
            '''
            result = self._values.get("last_updated_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The label name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-label.html#cfn-frauddetector-detector-label-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
            '''An array of key-value pairs to apply to this resource.

            For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-label.html#cfn-frauddetector-detector-label-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LabelProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_frauddetector.mixins.CfnDetectorPropsMixin.ModelProperty",
        jsii_struct_bases=[],
        name_mapping={"arn": "arn"},
    )
    class ModelProperty:
        def __init__(self, *, arn: typing.Optional[builtins.str] = None) -> None:
            '''The model.

            :param arn: The ARN of the model.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-model.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_frauddetector import mixins as frauddetector_mixins
                
                model_property = frauddetector_mixins.CfnDetectorPropsMixin.ModelProperty(
                    arn="arn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8fcc08a5dfb36eaff86e201ee42d06a0b5b758ac980aa65d7802b92441e6bd3f)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the model.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-model.html#cfn-frauddetector-detector-model-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ModelProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_frauddetector.mixins.CfnDetectorPropsMixin.OutcomeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "arn": "arn",
            "created_time": "createdTime",
            "description": "description",
            "inline": "inline",
            "last_updated_time": "lastUpdatedTime",
            "name": "name",
            "tags": "tags",
        },
    )
    class OutcomeProperty:
        def __init__(
            self,
            *,
            arn: typing.Optional[builtins.str] = None,
            created_time: typing.Optional[builtins.str] = None,
            description: typing.Optional[builtins.str] = None,
            inline: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            last_updated_time: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The outcome.

            :param arn: The outcome ARN.
            :param created_time: The timestamp when the outcome was created.
            :param description: The outcome description.
            :param inline: Indicates whether the resource is defined within this CloudFormation template and impacts the create, update, and delete behavior of the stack. If the value is ``true`` , CloudFormation will create/update/delete the resource when creating/updating/deleting the stack. If the value is ``false`` , CloudFormation will validate that the object exists and then use it within the resource without making changes to the object. For example, when creating ``AWS::FraudDetector::Detector`` you must define at least two variables. You can set ``Inline=true`` for these variables and CloudFormation will create/update/delete the variables as part of stack operations. However, if you set ``Inline=false`` , CloudFormation will associate the variables to your detector but not execute any changes to the variables.
            :param last_updated_time: The timestamp when the outcome was last updated.
            :param name: The outcome name.
            :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-outcome.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_frauddetector import mixins as frauddetector_mixins
                
                outcome_property = frauddetector_mixins.CfnDetectorPropsMixin.OutcomeProperty(
                    arn="arn",
                    created_time="createdTime",
                    description="description",
                    inline=False,
                    last_updated_time="lastUpdatedTime",
                    name="name",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6b66115ca64e92bfb78d4e8e1d64f5db2110b557b3f14012e9134e343228548c)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                check_type(argname="argument created_time", value=created_time, expected_type=type_hints["created_time"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument inline", value=inline, expected_type=type_hints["inline"])
                check_type(argname="argument last_updated_time", value=last_updated_time, expected_type=type_hints["last_updated_time"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn
            if created_time is not None:
                self._values["created_time"] = created_time
            if description is not None:
                self._values["description"] = description
            if inline is not None:
                self._values["inline"] = inline
            if last_updated_time is not None:
                self._values["last_updated_time"] = last_updated_time
            if name is not None:
                self._values["name"] = name
            if tags is not None:
                self._values["tags"] = tags

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The outcome ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-outcome.html#cfn-frauddetector-detector-outcome-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def created_time(self) -> typing.Optional[builtins.str]:
            '''The timestamp when the outcome was created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-outcome.html#cfn-frauddetector-detector-outcome-createdtime
            '''
            result = self._values.get("created_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The outcome description.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-outcome.html#cfn-frauddetector-detector-outcome-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def inline(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether the resource is defined within this CloudFormation template and impacts the create, update, and delete behavior of the stack.

            If the value is ``true`` , CloudFormation will create/update/delete the resource when creating/updating/deleting the stack. If the value is ``false`` , CloudFormation will validate that the object exists and then use it within the resource without making changes to the object.

            For example, when creating ``AWS::FraudDetector::Detector`` you must define at least two variables. You can set ``Inline=true`` for these variables and CloudFormation will create/update/delete the variables as part of stack operations. However, if you set ``Inline=false`` , CloudFormation will associate the variables to your detector but not execute any changes to the variables.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-outcome.html#cfn-frauddetector-detector-outcome-inline
            '''
            result = self._values.get("inline")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def last_updated_time(self) -> typing.Optional[builtins.str]:
            '''The timestamp when the outcome was last updated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-outcome.html#cfn-frauddetector-detector-outcome-lastupdatedtime
            '''
            result = self._values.get("last_updated_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The outcome name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-outcome.html#cfn-frauddetector-detector-outcome-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
            '''An array of key-value pairs to apply to this resource.

            For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-outcome.html#cfn-frauddetector-detector-outcome-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OutcomeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_frauddetector.mixins.CfnDetectorPropsMixin.RuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "arn": "arn",
            "created_time": "createdTime",
            "description": "description",
            "detector_id": "detectorId",
            "expression": "expression",
            "language": "language",
            "last_updated_time": "lastUpdatedTime",
            "outcomes": "outcomes",
            "rule_id": "ruleId",
            "rule_version": "ruleVersion",
            "tags": "tags",
        },
    )
    class RuleProperty:
        def __init__(
            self,
            *,
            arn: typing.Optional[builtins.str] = None,
            created_time: typing.Optional[builtins.str] = None,
            description: typing.Optional[builtins.str] = None,
            detector_id: typing.Optional[builtins.str] = None,
            expression: typing.Optional[builtins.str] = None,
            language: typing.Optional[builtins.str] = None,
            last_updated_time: typing.Optional[builtins.str] = None,
            outcomes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorPropsMixin.OutcomeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            rule_id: typing.Optional[builtins.str] = None,
            rule_version: typing.Optional[builtins.str] = None,
            tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A rule.

            :param arn: The rule ARN.
            :param created_time: Timestamp for when the rule was created.
            :param description: The rule description.
            :param detector_id: The detector for which the rule is associated.
            :param expression: The rule expression. A rule expression captures the business logic. For more information, see `Rule language reference <https://docs.aws.amazon.com/frauddetector/latest/ug/rule-language-reference.html>`_ .
            :param language: The rule language. Valid Value: DETECTORPL
            :param last_updated_time: Timestamp for when the rule was last updated.
            :param outcomes: The rule outcome.
            :param rule_id: The rule ID.
            :param rule_version: The rule version.
            :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-rule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_frauddetector import mixins as frauddetector_mixins
                
                rule_property = frauddetector_mixins.CfnDetectorPropsMixin.RuleProperty(
                    arn="arn",
                    created_time="createdTime",
                    description="description",
                    detector_id="detectorId",
                    expression="expression",
                    language="language",
                    last_updated_time="lastUpdatedTime",
                    outcomes=[frauddetector_mixins.CfnDetectorPropsMixin.OutcomeProperty(
                        arn="arn",
                        created_time="createdTime",
                        description="description",
                        inline=False,
                        last_updated_time="lastUpdatedTime",
                        name="name",
                        tags=[CfnTag(
                            key="key",
                            value="value"
                        )]
                    )],
                    rule_id="ruleId",
                    rule_version="ruleVersion",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a0fb3b3d195cd01a588713ddb7109f432d8053d64676bf571be6a93883c4889c)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                check_type(argname="argument created_time", value=created_time, expected_type=type_hints["created_time"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument detector_id", value=detector_id, expected_type=type_hints["detector_id"])
                check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
                check_type(argname="argument language", value=language, expected_type=type_hints["language"])
                check_type(argname="argument last_updated_time", value=last_updated_time, expected_type=type_hints["last_updated_time"])
                check_type(argname="argument outcomes", value=outcomes, expected_type=type_hints["outcomes"])
                check_type(argname="argument rule_id", value=rule_id, expected_type=type_hints["rule_id"])
                check_type(argname="argument rule_version", value=rule_version, expected_type=type_hints["rule_version"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn
            if created_time is not None:
                self._values["created_time"] = created_time
            if description is not None:
                self._values["description"] = description
            if detector_id is not None:
                self._values["detector_id"] = detector_id
            if expression is not None:
                self._values["expression"] = expression
            if language is not None:
                self._values["language"] = language
            if last_updated_time is not None:
                self._values["last_updated_time"] = last_updated_time
            if outcomes is not None:
                self._values["outcomes"] = outcomes
            if rule_id is not None:
                self._values["rule_id"] = rule_id
            if rule_version is not None:
                self._values["rule_version"] = rule_version
            if tags is not None:
                self._values["tags"] = tags

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The rule ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-rule.html#cfn-frauddetector-detector-rule-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def created_time(self) -> typing.Optional[builtins.str]:
            '''Timestamp for when the rule was created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-rule.html#cfn-frauddetector-detector-rule-createdtime
            '''
            result = self._values.get("created_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The rule description.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-rule.html#cfn-frauddetector-detector-rule-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def detector_id(self) -> typing.Optional[builtins.str]:
            '''The detector for which the rule is associated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-rule.html#cfn-frauddetector-detector-rule-detectorid
            '''
            result = self._values.get("detector_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def expression(self) -> typing.Optional[builtins.str]:
            '''The rule expression.

            A rule expression captures the business logic. For more information, see `Rule language reference <https://docs.aws.amazon.com/frauddetector/latest/ug/rule-language-reference.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-rule.html#cfn-frauddetector-detector-rule-expression
            '''
            result = self._values.get("expression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def language(self) -> typing.Optional[builtins.str]:
            '''The rule language.

            Valid Value: DETECTORPL

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-rule.html#cfn-frauddetector-detector-rule-language
            '''
            result = self._values.get("language")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def last_updated_time(self) -> typing.Optional[builtins.str]:
            '''Timestamp for when the rule was last updated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-rule.html#cfn-frauddetector-detector-rule-lastupdatedtime
            '''
            result = self._values.get("last_updated_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def outcomes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorPropsMixin.OutcomeProperty"]]]]:
            '''The rule outcome.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-rule.html#cfn-frauddetector-detector-rule-outcomes
            '''
            result = self._values.get("outcomes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorPropsMixin.OutcomeProperty"]]]], result)

        @builtins.property
        def rule_id(self) -> typing.Optional[builtins.str]:
            '''The rule ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-rule.html#cfn-frauddetector-detector-rule-ruleid
            '''
            result = self._values.get("rule_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def rule_version(self) -> typing.Optional[builtins.str]:
            '''The rule version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-rule.html#cfn-frauddetector-detector-rule-ruleversion
            '''
            result = self._values.get("rule_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
            '''An array of key-value pairs to apply to this resource.

            For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-rule.html#cfn-frauddetector-detector-rule-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_frauddetector.mixins.CfnEntityTypeMixinProps",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "name": "name", "tags": "tags"},
)
class CfnEntityTypeMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnEntityTypePropsMixin.

        :param description: The entity type description.
        :param name: The entity type name. Pattern: ``^[0-9a-z_-]+$``
        :param tags: A key and value pair.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-entitytype.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_frauddetector import mixins as frauddetector_mixins
            
            cfn_entity_type_mixin_props = frauddetector_mixins.CfnEntityTypeMixinProps(
                description="description",
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__223839986e699de6254ef33edce8ae574b7475e21a5c51e1da7b561d20ec82a6)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The entity type description.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-entitytype.html#cfn-frauddetector-entitytype-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The entity type name.

        Pattern: ``^[0-9a-z_-]+$``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-entitytype.html#cfn-frauddetector-entitytype-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A key and value pair.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-entitytype.html#cfn-frauddetector-entitytype-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEntityTypeMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnEntityTypePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_frauddetector.mixins.CfnEntityTypePropsMixin",
):
    '''Manages an entity type.

    An entity represents who is performing the event. As part of a fraud prediction, you pass the entity ID to indicate the specific entity who performed the event. An entity type classifies the entity. Example classifications include customer, merchant, or account.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-entitytype.html
    :cloudformationResource: AWS::FraudDetector::EntityType
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_frauddetector import mixins as frauddetector_mixins
        
        cfn_entity_type_props_mixin = frauddetector_mixins.CfnEntityTypePropsMixin(frauddetector_mixins.CfnEntityTypeMixinProps(
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
        props: typing.Union[CfnEntityTypeMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::FraudDetector::EntityType``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__397a19262f23e5025bf97a53e1d3585bc5bfd69a687d8049354964d49d14791e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f38f974d2ceaddc6fbda864caa42e2ec4815f72cfb5bc7fc1ec7a379c8923b6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__186abe63f76a7e30bd91e0152b08272947c176f61c407e76e7f1dc2b73c61f41)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnEntityTypeMixinProps:
        return typing.cast(CfnEntityTypeMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_frauddetector.mixins.CfnEventTypeMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "entity_types": "entityTypes",
        "event_variables": "eventVariables",
        "labels": "labels",
        "name": "name",
        "tags": "tags",
    },
)
class CfnEventTypeMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        entity_types: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEventTypePropsMixin.EntityTypeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        event_variables: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEventTypePropsMixin.EventVariableProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        labels: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEventTypePropsMixin.LabelProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnEventTypePropsMixin.

        :param description: The event type description.
        :param entity_types: The event type entity types.
        :param event_variables: The event type event variables.
        :param labels: The event type labels.
        :param name: The event type name. Pattern : ``^[0-9a-z_-]+$``
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-eventtype.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_frauddetector import mixins as frauddetector_mixins
            
            cfn_event_type_mixin_props = frauddetector_mixins.CfnEventTypeMixinProps(
                description="description",
                entity_types=[frauddetector_mixins.CfnEventTypePropsMixin.EntityTypeProperty(
                    arn="arn",
                    created_time="createdTime",
                    description="description",
                    inline=False,
                    last_updated_time="lastUpdatedTime",
                    name="name",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )],
                event_variables=[frauddetector_mixins.CfnEventTypePropsMixin.EventVariableProperty(
                    arn="arn",
                    created_time="createdTime",
                    data_source="dataSource",
                    data_type="dataType",
                    default_value="defaultValue",
                    description="description",
                    inline=False,
                    last_updated_time="lastUpdatedTime",
                    name="name",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )],
                    variable_type="variableType"
                )],
                labels=[frauddetector_mixins.CfnEventTypePropsMixin.LabelProperty(
                    arn="arn",
                    created_time="createdTime",
                    description="description",
                    inline=False,
                    last_updated_time="lastUpdatedTime",
                    name="name",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )],
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1620305ad6010082b83a33040b46f0c31106c55022ad76c587c837407784add)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument entity_types", value=entity_types, expected_type=type_hints["entity_types"])
            check_type(argname="argument event_variables", value=event_variables, expected_type=type_hints["event_variables"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if entity_types is not None:
            self._values["entity_types"] = entity_types
        if event_variables is not None:
            self._values["event_variables"] = event_variables
        if labels is not None:
            self._values["labels"] = labels
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The event type description.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-eventtype.html#cfn-frauddetector-eventtype-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def entity_types(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventTypePropsMixin.EntityTypeProperty"]]]]:
        '''The event type entity types.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-eventtype.html#cfn-frauddetector-eventtype-entitytypes
        '''
        result = self._values.get("entity_types")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventTypePropsMixin.EntityTypeProperty"]]]], result)

    @builtins.property
    def event_variables(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventTypePropsMixin.EventVariableProperty"]]]]:
        '''The event type event variables.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-eventtype.html#cfn-frauddetector-eventtype-eventvariables
        '''
        result = self._values.get("event_variables")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventTypePropsMixin.EventVariableProperty"]]]], result)

    @builtins.property
    def labels(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventTypePropsMixin.LabelProperty"]]]]:
        '''The event type labels.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-eventtype.html#cfn-frauddetector-eventtype-labels
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventTypePropsMixin.LabelProperty"]]]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The event type name.

        Pattern : ``^[0-9a-z_-]+$``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-eventtype.html#cfn-frauddetector-eventtype-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-eventtype.html#cfn-frauddetector-eventtype-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEventTypeMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnEventTypePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_frauddetector.mixins.CfnEventTypePropsMixin",
):
    '''Manages an event type.

    An event is a business activity that is evaluated for fraud risk. With Amazon Fraud Detector, you generate fraud predictions for events. An event type defines the structure for an event sent to Amazon Fraud Detector. This includes the variables sent as part of the event, the entity performing the event (such as a customer), and the labels that classify the event. Example event types include online payment transactions, account registrations, and authentications.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-eventtype.html
    :cloudformationResource: AWS::FraudDetector::EventType
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_frauddetector import mixins as frauddetector_mixins
        
        cfn_event_type_props_mixin = frauddetector_mixins.CfnEventTypePropsMixin(frauddetector_mixins.CfnEventTypeMixinProps(
            description="description",
            entity_types=[frauddetector_mixins.CfnEventTypePropsMixin.EntityTypeProperty(
                arn="arn",
                created_time="createdTime",
                description="description",
                inline=False,
                last_updated_time="lastUpdatedTime",
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )],
            event_variables=[frauddetector_mixins.CfnEventTypePropsMixin.EventVariableProperty(
                arn="arn",
                created_time="createdTime",
                data_source="dataSource",
                data_type="dataType",
                default_value="defaultValue",
                description="description",
                inline=False,
                last_updated_time="lastUpdatedTime",
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                variable_type="variableType"
            )],
            labels=[frauddetector_mixins.CfnEventTypePropsMixin.LabelProperty(
                arn="arn",
                created_time="createdTime",
                description="description",
                inline=False,
                last_updated_time="lastUpdatedTime",
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
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
        props: typing.Union[CfnEventTypeMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::FraudDetector::EventType``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__954ed765d734efa5529fe30b538f3cea69bca0410700a1498de17514baae1edd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0e65237d0dd33526f35a4269fb957d978cd8c045e5158fa0e08357b60c1f894)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4de4827f71166518bcef2b4da254334befd864e654795641a6c023f49de506a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnEventTypeMixinProps:
        return typing.cast(CfnEventTypeMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_frauddetector.mixins.CfnEventTypePropsMixin.EntityTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "arn": "arn",
            "created_time": "createdTime",
            "description": "description",
            "inline": "inline",
            "last_updated_time": "lastUpdatedTime",
            "name": "name",
            "tags": "tags",
        },
    )
    class EntityTypeProperty:
        def __init__(
            self,
            *,
            arn: typing.Optional[builtins.str] = None,
            created_time: typing.Optional[builtins.str] = None,
            description: typing.Optional[builtins.str] = None,
            inline: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            last_updated_time: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The entity type details.

            :param arn: The entity type ARN.
            :param created_time: Timestamp of when the entity type was created.
            :param description: The entity type description.
            :param inline: Indicates whether the resource is defined within this CloudFormation template and impacts the create, update, and delete behavior of the stack. If the value is ``true`` , CloudFormation will create/update/delete the resource when creating/updating/deleting the stack. If the value is ``false`` , CloudFormation will validate that the object exists and then use it within the resource without making changes to the object. For example, when creating ``AWS::FraudDetector::EventType`` you must define at least two variables. You can set ``Inline=true`` for these variables and CloudFormation will create/update/delete the variables as part of stack operations. However, if you set ``Inline=false`` , CloudFormation will associate the variables to your event type but not execute any changes to the variables.
            :param last_updated_time: Timestamp of when the entity type was last updated.
            :param name: The entity type name. ``^[0-9a-z_-]+$``
            :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-entitytype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_frauddetector import mixins as frauddetector_mixins
                
                entity_type_property = frauddetector_mixins.CfnEventTypePropsMixin.EntityTypeProperty(
                    arn="arn",
                    created_time="createdTime",
                    description="description",
                    inline=False,
                    last_updated_time="lastUpdatedTime",
                    name="name",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__83c6cd0ee7fe15b632518c1e935a931093ee91781b076080d2b09400fdde9791)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                check_type(argname="argument created_time", value=created_time, expected_type=type_hints["created_time"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument inline", value=inline, expected_type=type_hints["inline"])
                check_type(argname="argument last_updated_time", value=last_updated_time, expected_type=type_hints["last_updated_time"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn
            if created_time is not None:
                self._values["created_time"] = created_time
            if description is not None:
                self._values["description"] = description
            if inline is not None:
                self._values["inline"] = inline
            if last_updated_time is not None:
                self._values["last_updated_time"] = last_updated_time
            if name is not None:
                self._values["name"] = name
            if tags is not None:
                self._values["tags"] = tags

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The entity type ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-entitytype.html#cfn-frauddetector-eventtype-entitytype-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def created_time(self) -> typing.Optional[builtins.str]:
            '''Timestamp of when the entity type was created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-entitytype.html#cfn-frauddetector-eventtype-entitytype-createdtime
            '''
            result = self._values.get("created_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The entity type description.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-entitytype.html#cfn-frauddetector-eventtype-entitytype-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def inline(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether the resource is defined within this CloudFormation template and impacts the create, update, and delete behavior of the stack.

            If the value is ``true`` , CloudFormation will create/update/delete the resource when creating/updating/deleting the stack. If the value is ``false`` , CloudFormation will validate that the object exists and then use it within the resource without making changes to the object.

            For example, when creating ``AWS::FraudDetector::EventType`` you must define at least two variables. You can set ``Inline=true`` for these variables and CloudFormation will create/update/delete the variables as part of stack operations. However, if you set ``Inline=false`` , CloudFormation will associate the variables to your event type but not execute any changes to the variables.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-entitytype.html#cfn-frauddetector-eventtype-entitytype-inline
            '''
            result = self._values.get("inline")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def last_updated_time(self) -> typing.Optional[builtins.str]:
            '''Timestamp of when the entity type was last updated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-entitytype.html#cfn-frauddetector-eventtype-entitytype-lastupdatedtime
            '''
            result = self._values.get("last_updated_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The entity type name.

            ``^[0-9a-z_-]+$``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-entitytype.html#cfn-frauddetector-eventtype-entitytype-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
            '''An array of key-value pairs to apply to this resource.

            For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-entitytype.html#cfn-frauddetector-eventtype-entitytype-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EntityTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_frauddetector.mixins.CfnEventTypePropsMixin.EventVariableProperty",
        jsii_struct_bases=[],
        name_mapping={
            "arn": "arn",
            "created_time": "createdTime",
            "data_source": "dataSource",
            "data_type": "dataType",
            "default_value": "defaultValue",
            "description": "description",
            "inline": "inline",
            "last_updated_time": "lastUpdatedTime",
            "name": "name",
            "tags": "tags",
            "variable_type": "variableType",
        },
    )
    class EventVariableProperty:
        def __init__(
            self,
            *,
            arn: typing.Optional[builtins.str] = None,
            created_time: typing.Optional[builtins.str] = None,
            data_source: typing.Optional[builtins.str] = None,
            data_type: typing.Optional[builtins.str] = None,
            default_value: typing.Optional[builtins.str] = None,
            description: typing.Optional[builtins.str] = None,
            inline: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            last_updated_time: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
            variable_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The variables associated with this event type.

            :param arn: The event variable ARN.
            :param created_time: Timestamp for when event variable was created.
            :param data_source: The source of the event variable. Valid values: ``EVENT | EXTERNAL_MODEL_SCORE`` When defining a variable within a event type, you can only use the ``EVENT`` value for DataSource when the *Inline* property is set to true. If the *Inline* property is set false, you can use either ``EVENT`` or ``MODEL_SCORE`` for DataSource.
            :param data_type: The data type of the event variable. For more information, see `Data types <https://docs.aws.amazon.com/frauddetector/latest/ug/variables.html#data-types>`_ .
            :param default_value: The default value of the event variable.
            :param description: The event variable description.
            :param inline: Indicates whether the resource is defined within this CloudFormation template and impacts the create, update, and delete behavior of the stack. If the value is ``true`` , CloudFormation will create/update/delete the resource when creating/updating/deleting the stack. If the value is ``false`` , CloudFormation will validate that the object exists and then use it within the resource without making changes to the object. For example, when creating ``AWS::FraudDetector::EventType`` you must define at least two variables. You can set ``Inline=true`` for these variables and CloudFormation will create/update/delete the Variables as part of stack operations. However, if you set ``Inline=false`` , CloudFormation will associate the variables to your event type but not execute any changes to the variables.
            :param last_updated_time: Timestamp for when the event variable was last updated.
            :param name: The name of the event variable.
            :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
            :param variable_type: The type of event variable. For more information, see `Variable types <https://docs.aws.amazon.com/frauddetector/latest/ug/variables.html#variable-types>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-eventvariable.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_frauddetector import mixins as frauddetector_mixins
                
                event_variable_property = frauddetector_mixins.CfnEventTypePropsMixin.EventVariableProperty(
                    arn="arn",
                    created_time="createdTime",
                    data_source="dataSource",
                    data_type="dataType",
                    default_value="defaultValue",
                    description="description",
                    inline=False,
                    last_updated_time="lastUpdatedTime",
                    name="name",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )],
                    variable_type="variableType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f1179c169a7d8e97913c414ad79477b55a51724a9629bac0a2293ed91fd6140d)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                check_type(argname="argument created_time", value=created_time, expected_type=type_hints["created_time"])
                check_type(argname="argument data_source", value=data_source, expected_type=type_hints["data_source"])
                check_type(argname="argument data_type", value=data_type, expected_type=type_hints["data_type"])
                check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument inline", value=inline, expected_type=type_hints["inline"])
                check_type(argname="argument last_updated_time", value=last_updated_time, expected_type=type_hints["last_updated_time"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
                check_type(argname="argument variable_type", value=variable_type, expected_type=type_hints["variable_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn
            if created_time is not None:
                self._values["created_time"] = created_time
            if data_source is not None:
                self._values["data_source"] = data_source
            if data_type is not None:
                self._values["data_type"] = data_type
            if default_value is not None:
                self._values["default_value"] = default_value
            if description is not None:
                self._values["description"] = description
            if inline is not None:
                self._values["inline"] = inline
            if last_updated_time is not None:
                self._values["last_updated_time"] = last_updated_time
            if name is not None:
                self._values["name"] = name
            if tags is not None:
                self._values["tags"] = tags
            if variable_type is not None:
                self._values["variable_type"] = variable_type

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The event variable ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-eventvariable.html#cfn-frauddetector-eventtype-eventvariable-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def created_time(self) -> typing.Optional[builtins.str]:
            '''Timestamp for when event variable was created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-eventvariable.html#cfn-frauddetector-eventtype-eventvariable-createdtime
            '''
            result = self._values.get("created_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def data_source(self) -> typing.Optional[builtins.str]:
            '''The source of the event variable.

            Valid values: ``EVENT | EXTERNAL_MODEL_SCORE``

            When defining a variable within a event type, you can only use the ``EVENT`` value for DataSource when the *Inline* property is set to true. If the *Inline* property is set false, you can use either ``EVENT`` or ``MODEL_SCORE`` for DataSource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-eventvariable.html#cfn-frauddetector-eventtype-eventvariable-datasource
            '''
            result = self._values.get("data_source")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def data_type(self) -> typing.Optional[builtins.str]:
            '''The data type of the event variable.

            For more information, see `Data types <https://docs.aws.amazon.com/frauddetector/latest/ug/variables.html#data-types>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-eventvariable.html#cfn-frauddetector-eventtype-eventvariable-datatype
            '''
            result = self._values.get("data_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def default_value(self) -> typing.Optional[builtins.str]:
            '''The default value of the event variable.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-eventvariable.html#cfn-frauddetector-eventtype-eventvariable-defaultvalue
            '''
            result = self._values.get("default_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The event variable description.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-eventvariable.html#cfn-frauddetector-eventtype-eventvariable-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def inline(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether the resource is defined within this CloudFormation template and impacts the create, update, and delete behavior of the stack.

            If the value is ``true`` , CloudFormation will create/update/delete the resource when creating/updating/deleting the stack. If the value is ``false`` , CloudFormation will validate that the object exists and then use it within the resource without making changes to the object.

            For example, when creating ``AWS::FraudDetector::EventType`` you must define at least two variables. You can set ``Inline=true`` for these variables and CloudFormation will create/update/delete the Variables as part of stack operations. However, if you set ``Inline=false`` , CloudFormation will associate the variables to your event type but not execute any changes to the variables.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-eventvariable.html#cfn-frauddetector-eventtype-eventvariable-inline
            '''
            result = self._values.get("inline")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def last_updated_time(self) -> typing.Optional[builtins.str]:
            '''Timestamp for when the event variable was last updated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-eventvariable.html#cfn-frauddetector-eventtype-eventvariable-lastupdatedtime
            '''
            result = self._values.get("last_updated_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the event variable.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-eventvariable.html#cfn-frauddetector-eventtype-eventvariable-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
            '''An array of key-value pairs to apply to this resource.

            For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-eventvariable.html#cfn-frauddetector-eventtype-eventvariable-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

        @builtins.property
        def variable_type(self) -> typing.Optional[builtins.str]:
            '''The type of event variable.

            For more information, see `Variable types <https://docs.aws.amazon.com/frauddetector/latest/ug/variables.html#variable-types>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-eventvariable.html#cfn-frauddetector-eventtype-eventvariable-variabletype
            '''
            result = self._values.get("variable_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventVariableProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_frauddetector.mixins.CfnEventTypePropsMixin.LabelProperty",
        jsii_struct_bases=[],
        name_mapping={
            "arn": "arn",
            "created_time": "createdTime",
            "description": "description",
            "inline": "inline",
            "last_updated_time": "lastUpdatedTime",
            "name": "name",
            "tags": "tags",
        },
    )
    class LabelProperty:
        def __init__(
            self,
            *,
            arn: typing.Optional[builtins.str] = None,
            created_time: typing.Optional[builtins.str] = None,
            description: typing.Optional[builtins.str] = None,
            inline: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            last_updated_time: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The label associated with the event type.

            :param arn: The label ARN.
            :param created_time: Timestamp of when the event type was created.
            :param description: The label description.
            :param inline: Indicates whether the resource is defined within this CloudFormation template and impacts the create, update, and delete behavior of the stack. If the value is ``true`` , CloudFormation will create/update/delete the resource when creating/updating/deleting the stack. If the value is ``false`` , CloudFormation will validate that the object exists and then use it within the resource without making changes to the object. For example, when creating ``AWS::FraudDetector::EventType`` you must define at least two variables. You can set ``Inline=true`` for these variables and CloudFormation will create/update/delete the variables as part of stack operations. However, if you set ``Inline=false`` , CloudFormation will associate the variables to your EventType but not execute any changes to the variables.
            :param last_updated_time: Timestamp of when the label was last updated.
            :param name: The label name.
            :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-label.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_frauddetector import mixins as frauddetector_mixins
                
                label_property = frauddetector_mixins.CfnEventTypePropsMixin.LabelProperty(
                    arn="arn",
                    created_time="createdTime",
                    description="description",
                    inline=False,
                    last_updated_time="lastUpdatedTime",
                    name="name",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ea61eded696ea786d4bfb17af1de79a5c469cde96af69a2985b3336439dd68c0)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                check_type(argname="argument created_time", value=created_time, expected_type=type_hints["created_time"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument inline", value=inline, expected_type=type_hints["inline"])
                check_type(argname="argument last_updated_time", value=last_updated_time, expected_type=type_hints["last_updated_time"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn
            if created_time is not None:
                self._values["created_time"] = created_time
            if description is not None:
                self._values["description"] = description
            if inline is not None:
                self._values["inline"] = inline
            if last_updated_time is not None:
                self._values["last_updated_time"] = last_updated_time
            if name is not None:
                self._values["name"] = name
            if tags is not None:
                self._values["tags"] = tags

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The label ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-label.html#cfn-frauddetector-eventtype-label-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def created_time(self) -> typing.Optional[builtins.str]:
            '''Timestamp of when the event type was created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-label.html#cfn-frauddetector-eventtype-label-createdtime
            '''
            result = self._values.get("created_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The label description.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-label.html#cfn-frauddetector-eventtype-label-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def inline(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether the resource is defined within this CloudFormation template and impacts the create, update, and delete behavior of the stack.

            If the value is ``true`` , CloudFormation will create/update/delete the resource when creating/updating/deleting the stack. If the value is ``false`` , CloudFormation will validate that the object exists and then use it within the resource without making changes to the object.

            For example, when creating ``AWS::FraudDetector::EventType`` you must define at least two variables. You can set ``Inline=true`` for these variables and CloudFormation will create/update/delete the variables as part of stack operations. However, if you set ``Inline=false`` , CloudFormation will associate the variables to your EventType but not execute any changes to the variables.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-label.html#cfn-frauddetector-eventtype-label-inline
            '''
            result = self._values.get("inline")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def last_updated_time(self) -> typing.Optional[builtins.str]:
            '''Timestamp of when the label was last updated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-label.html#cfn-frauddetector-eventtype-label-lastupdatedtime
            '''
            result = self._values.get("last_updated_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The label name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-label.html#cfn-frauddetector-eventtype-label-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
            '''An array of key-value pairs to apply to this resource.

            For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-label.html#cfn-frauddetector-eventtype-label-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LabelProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_frauddetector.mixins.CfnLabelMixinProps",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "name": "name", "tags": "tags"},
)
class CfnLabelMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnLabelPropsMixin.

        :param description: The label description.
        :param name: The label name. Pattern: ``^[0-9a-z_-]+$``
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-label.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_frauddetector import mixins as frauddetector_mixins
            
            cfn_label_mixin_props = frauddetector_mixins.CfnLabelMixinProps(
                description="description",
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c1f3327c1e889b48eafa79a5f58b0832aeaeea3da774c5cfeb8545538ecc21f)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The label description.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-label.html#cfn-frauddetector-label-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The label name.

        Pattern: ``^[0-9a-z_-]+$``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-label.html#cfn-frauddetector-label-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-label.html#cfn-frauddetector-label-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLabelMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLabelPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_frauddetector.mixins.CfnLabelPropsMixin",
):
    '''Creates or updates label.

    A label classifies an event as fraudulent or legitimate. Labels are associated with event types and used to train supervised machine learning models in Amazon Fraud Detector.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-label.html
    :cloudformationResource: AWS::FraudDetector::Label
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_frauddetector import mixins as frauddetector_mixins
        
        cfn_label_props_mixin = frauddetector_mixins.CfnLabelPropsMixin(frauddetector_mixins.CfnLabelMixinProps(
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
        props: typing.Union[CfnLabelMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::FraudDetector::Label``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c498398211649bf0e210baab2ba36d7fde0ba5715ab614c2948b25ea40154af)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2968e4d01191a1819467c2d040417ff88a92e9b96fdb33acae4a7dc442da08af)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c12e7f7fc61f554eb39ff28a82a0f38893d30992365f4c2b64b79e0d92b61d0a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLabelMixinProps:
        return typing.cast(CfnLabelMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_frauddetector.mixins.CfnListMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "elements": "elements",
        "name": "name",
        "tags": "tags",
        "variable_type": "variableType",
    },
)
class CfnListMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        elements: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        variable_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnListPropsMixin.

        :param description: The description of the list.
        :param elements: The elements in the list.
        :param name: The name of the list.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param variable_type: The variable type of the list. For more information, see `Variable types <https://docs.aws.amazon.com/frauddetector/latest/ug/variables.html#variable-types>`_

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-list.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_frauddetector import mixins as frauddetector_mixins
            
            cfn_list_mixin_props = frauddetector_mixins.CfnListMixinProps(
                description="description",
                elements=["elements"],
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                variable_type="variableType"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd008fa0f23141cc9acc62dcac8c7a9f6f985d51cacaf8cc0f5e0ced997fe51b)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument elements", value=elements, expected_type=type_hints["elements"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument variable_type", value=variable_type, expected_type=type_hints["variable_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if elements is not None:
            self._values["elements"] = elements
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags
        if variable_type is not None:
            self._values["variable_type"] = variable_type

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the list.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-list.html#cfn-frauddetector-list-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def elements(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The elements in the list.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-list.html#cfn-frauddetector-list-elements
        '''
        result = self._values.get("elements")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the list.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-list.html#cfn-frauddetector-list-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-list.html#cfn-frauddetector-list-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def variable_type(self) -> typing.Optional[builtins.str]:
        '''The variable type of the list.

        For more information, see `Variable types <https://docs.aws.amazon.com/frauddetector/latest/ug/variables.html#variable-types>`_

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-list.html#cfn-frauddetector-list-variabletype
        '''
        result = self._values.get("variable_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnListMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnListPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_frauddetector.mixins.CfnListPropsMixin",
):
    '''Creates a list.

    List is a set of input data for a variable in your event dataset. You use the input data in a rule that's associated with your detector. For more information, see `Lists <https://docs.aws.amazon.com//frauddetector/latest/ug/lists.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-list.html
    :cloudformationResource: AWS::FraudDetector::List
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_frauddetector import mixins as frauddetector_mixins
        
        cfn_list_props_mixin = frauddetector_mixins.CfnListPropsMixin(frauddetector_mixins.CfnListMixinProps(
            description="description",
            elements=["elements"],
            name="name",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            variable_type="variableType"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnListMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::FraudDetector::List``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07278220a4e2387b1f82e709a10ee46ddcb63aef030d635296d9055e1962f31d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0353119c5735dfe15b67a11f5f81f9dd5987a20b64192a4c45cfc3706a9a75be)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1af014c19a2e3e7675f974c6df1b06f3b89c1799d0759e0f1e08ae27f9109dbe)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnListMixinProps:
        return typing.cast(CfnListMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_frauddetector.mixins.CfnOutcomeMixinProps",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "name": "name", "tags": "tags"},
)
class CfnOutcomeMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnOutcomePropsMixin.

        :param description: The outcome description.
        :param name: The outcome name.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-outcome.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_frauddetector import mixins as frauddetector_mixins
            
            cfn_outcome_mixin_props = frauddetector_mixins.CfnOutcomeMixinProps(
                description="description",
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50603029460deb422e4541ab82802672091fdb679fcd49478a8b693d85beb1c6)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The outcome description.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-outcome.html#cfn-frauddetector-outcome-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The outcome name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-outcome.html#cfn-frauddetector-outcome-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-outcome.html#cfn-frauddetector-outcome-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnOutcomeMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnOutcomePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_frauddetector.mixins.CfnOutcomePropsMixin",
):
    '''Creates or updates an outcome.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-outcome.html
    :cloudformationResource: AWS::FraudDetector::Outcome
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_frauddetector import mixins as frauddetector_mixins
        
        cfn_outcome_props_mixin = frauddetector_mixins.CfnOutcomePropsMixin(frauddetector_mixins.CfnOutcomeMixinProps(
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
        props: typing.Union[CfnOutcomeMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::FraudDetector::Outcome``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a0a39c58f3a2e401eb8b9db18cc9e3ad9f1a691e62f57058cd9f396d5f51913)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9fdb7807b40e9fa9351f228e0b32ffacaad6f207339cb5dfc1f34c9255a32eb)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fa87fd48341a373d1923710d3fdedae9480473bc740b0227260f7a255bd9302)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnOutcomeMixinProps:
        return typing.cast(CfnOutcomeMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_frauddetector.mixins.CfnVariableMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "data_source": "dataSource",
        "data_type": "dataType",
        "default_value": "defaultValue",
        "description": "description",
        "name": "name",
        "tags": "tags",
        "variable_type": "variableType",
    },
)
class CfnVariableMixinProps:
    def __init__(
        self,
        *,
        data_source: typing.Optional[builtins.str] = None,
        data_type: typing.Optional[builtins.str] = None,
        default_value: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        variable_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnVariablePropsMixin.

        :param data_source: The data source of the variable. Valid values: ``EVENT | EXTERNAL_MODEL_SCORE`` When defining a variable within a detector, you can only use the ``EVENT`` value for DataSource when the *Inline* property is set to true. If the *Inline* property is set false, you can use either ``EVENT`` or ``MODEL_SCORE`` for DataSource.
        :param data_type: The data type of the variable. Valid data types: ``STRING | INTEGER | BOOLEAN | FLOAT``
        :param default_value: The default value of the variable.
        :param description: The description of the variable.
        :param name: The name of the variable. Pattern: ``^[0-9a-z_-]+$``
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param variable_type: The type of the variable. For more information see `Variable types <https://docs.aws.amazon.com/frauddetector/latest/ug/create-a-variable.html#variable-types>`_ . Valid Values: ``AUTH_CODE | AVS | BILLING_ADDRESS_L1 | BILLING_ADDRESS_L2 | BILLING_CITY | BILLING_COUNTRY | BILLING_NAME | BILLING_PHONE | BILLING_STATE | BILLING_ZIP | CARD_BIN | CATEGORICAL | CURRENCY_CODE | EMAIL_ADDRESS | FINGERPRINT | FRAUD_LABEL | FREE_FORM_TEXT | IP_ADDRESS | NUMERIC | ORDER_ID | PAYMENT_TYPE | PHONE_NUMBER | PRICE | PRODUCT_CATEGORY | SHIPPING_ADDRESS_L1 | SHIPPING_ADDRESS_L2 | SHIPPING_CITY | SHIPPING_COUNTRY | SHIPPING_NAME | SHIPPING_PHONE | SHIPPING_STATE | SHIPPING_ZIP | USERAGENT``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-variable.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_frauddetector import mixins as frauddetector_mixins
            
            cfn_variable_mixin_props = frauddetector_mixins.CfnVariableMixinProps(
                data_source="dataSource",
                data_type="dataType",
                default_value="defaultValue",
                description="description",
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                variable_type="variableType"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5f28faf95aba9437f5a3deeafad0c0fd97fc84de2ee5ac248c1a77b0e37587c)
            check_type(argname="argument data_source", value=data_source, expected_type=type_hints["data_source"])
            check_type(argname="argument data_type", value=data_type, expected_type=type_hints["data_type"])
            check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument variable_type", value=variable_type, expected_type=type_hints["variable_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data_source is not None:
            self._values["data_source"] = data_source
        if data_type is not None:
            self._values["data_type"] = data_type
        if default_value is not None:
            self._values["default_value"] = default_value
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags
        if variable_type is not None:
            self._values["variable_type"] = variable_type

    @builtins.property
    def data_source(self) -> typing.Optional[builtins.str]:
        '''The data source of the variable.

        Valid values: ``EVENT | EXTERNAL_MODEL_SCORE``

        When defining a variable within a detector, you can only use the ``EVENT`` value for DataSource when the *Inline* property is set to true. If the *Inline* property is set false, you can use either ``EVENT`` or ``MODEL_SCORE`` for DataSource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-variable.html#cfn-frauddetector-variable-datasource
        '''
        result = self._values.get("data_source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_type(self) -> typing.Optional[builtins.str]:
        '''The data type of the variable.

        Valid data types: ``STRING | INTEGER | BOOLEAN | FLOAT``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-variable.html#cfn-frauddetector-variable-datatype
        '''
        result = self._values.get("data_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_value(self) -> typing.Optional[builtins.str]:
        '''The default value of the variable.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-variable.html#cfn-frauddetector-variable-defaultvalue
        '''
        result = self._values.get("default_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the variable.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-variable.html#cfn-frauddetector-variable-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the variable.

        Pattern: ``^[0-9a-z_-]+$``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-variable.html#cfn-frauddetector-variable-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-variable.html#cfn-frauddetector-variable-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def variable_type(self) -> typing.Optional[builtins.str]:
        '''The type of the variable. For more information see `Variable types <https://docs.aws.amazon.com/frauddetector/latest/ug/create-a-variable.html#variable-types>`_ .

        Valid Values: ``AUTH_CODE | AVS | BILLING_ADDRESS_L1 | BILLING_ADDRESS_L2 | BILLING_CITY | BILLING_COUNTRY | BILLING_NAME | BILLING_PHONE | BILLING_STATE | BILLING_ZIP | CARD_BIN | CATEGORICAL | CURRENCY_CODE | EMAIL_ADDRESS | FINGERPRINT | FRAUD_LABEL | FREE_FORM_TEXT | IP_ADDRESS | NUMERIC | ORDER_ID | PAYMENT_TYPE | PHONE_NUMBER | PRICE | PRODUCT_CATEGORY | SHIPPING_ADDRESS_L1 | SHIPPING_ADDRESS_L2 | SHIPPING_CITY | SHIPPING_COUNTRY | SHIPPING_NAME | SHIPPING_PHONE | SHIPPING_STATE | SHIPPING_ZIP | USERAGENT``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-variable.html#cfn-frauddetector-variable-variabletype
        '''
        result = self._values.get("variable_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVariableMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnVariablePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_frauddetector.mixins.CfnVariablePropsMixin",
):
    '''Manages a variable.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-variable.html
    :cloudformationResource: AWS::FraudDetector::Variable
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_frauddetector import mixins as frauddetector_mixins
        
        cfn_variable_props_mixin = frauddetector_mixins.CfnVariablePropsMixin(frauddetector_mixins.CfnVariableMixinProps(
            data_source="dataSource",
            data_type="dataType",
            default_value="defaultValue",
            description="description",
            name="name",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            variable_type="variableType"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnVariableMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::FraudDetector::Variable``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae073919d4f3ba9952abebe302dd47f53c8a692984ef3faad6a349abd827132d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__71e0b35ca487c7720de96a1a703715a5d2ea874f40a015622974423e8cbc69ce)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__633bf09878b861f489a4426d5f2c7b7480124f0263ff890f0ce77231baa88e94)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnVariableMixinProps:
        return typing.cast(CfnVariableMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnDetectorMixinProps",
    "CfnDetectorPropsMixin",
    "CfnEntityTypeMixinProps",
    "CfnEntityTypePropsMixin",
    "CfnEventTypeMixinProps",
    "CfnEventTypePropsMixin",
    "CfnLabelMixinProps",
    "CfnLabelPropsMixin",
    "CfnListMixinProps",
    "CfnListPropsMixin",
    "CfnOutcomeMixinProps",
    "CfnOutcomePropsMixin",
    "CfnVariableMixinProps",
    "CfnVariablePropsMixin",
]

publication.publish()

def _typecheckingstub__9dbc330817d424a8711de180d276e7af85d8ce7db7c9ce4774f16ebdb2bf1c3e(
    *,
    associated_models: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorPropsMixin.ModelProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    detector_id: typing.Optional[builtins.str] = None,
    detector_version_status: typing.Optional[builtins.str] = None,
    event_type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorPropsMixin.EventTypeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    rule_execution_mode: typing.Optional[builtins.str] = None,
    rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorPropsMixin.RuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__827f634a3f1cf909024d15cb5a36a14661f5ce89f33b61b84c23ad4b02a27076(
    props: typing.Union[CfnDetectorMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6ec9f14ecc1219370644e1b7a537ba84994757462603dcc281394e7eeb81d8c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4134b1016e17b80a5079e6cd46f487cce3b62e2f097949b58817b6bbe9cdd2f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10c4f2c60d4fe661e3fb8accc47ef2bebb0bc783de117aea7c821808fe14044b(
    *,
    arn: typing.Optional[builtins.str] = None,
    created_time: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    inline: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    last_updated_time: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0b59af5b64a98f09a9950332041c5126deb0d5251c77c26b370e213d5bd0bcb(
    *,
    arn: typing.Optional[builtins.str] = None,
    created_time: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    entity_types: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorPropsMixin.EntityTypeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    event_variables: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorPropsMixin.EventVariableProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    inline: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    labels: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorPropsMixin.LabelProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    last_updated_time: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__517684892c045645fb24b140f18a7239cca883dfec541f5442643ed8ee9b12ef(
    *,
    arn: typing.Optional[builtins.str] = None,
    created_time: typing.Optional[builtins.str] = None,
    data_source: typing.Optional[builtins.str] = None,
    data_type: typing.Optional[builtins.str] = None,
    default_value: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    inline: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    last_updated_time: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    variable_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f9a38e9735ca460faf12b27e09581eba0a87f277bb36c9aa51176c40aa48752(
    *,
    arn: typing.Optional[builtins.str] = None,
    created_time: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    inline: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    last_updated_time: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fcc08a5dfb36eaff86e201ee42d06a0b5b758ac980aa65d7802b92441e6bd3f(
    *,
    arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b66115ca64e92bfb78d4e8e1d64f5db2110b557b3f14012e9134e343228548c(
    *,
    arn: typing.Optional[builtins.str] = None,
    created_time: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    inline: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    last_updated_time: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0fb3b3d195cd01a588713ddb7109f432d8053d64676bf571be6a93883c4889c(
    *,
    arn: typing.Optional[builtins.str] = None,
    created_time: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    detector_id: typing.Optional[builtins.str] = None,
    expression: typing.Optional[builtins.str] = None,
    language: typing.Optional[builtins.str] = None,
    last_updated_time: typing.Optional[builtins.str] = None,
    outcomes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorPropsMixin.OutcomeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    rule_id: typing.Optional[builtins.str] = None,
    rule_version: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__223839986e699de6254ef33edce8ae574b7475e21a5c51e1da7b561d20ec82a6(
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__397a19262f23e5025bf97a53e1d3585bc5bfd69a687d8049354964d49d14791e(
    props: typing.Union[CfnEntityTypeMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f38f974d2ceaddc6fbda864caa42e2ec4815f72cfb5bc7fc1ec7a379c8923b6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__186abe63f76a7e30bd91e0152b08272947c176f61c407e76e7f1dc2b73c61f41(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1620305ad6010082b83a33040b46f0c31106c55022ad76c587c837407784add(
    *,
    description: typing.Optional[builtins.str] = None,
    entity_types: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEventTypePropsMixin.EntityTypeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    event_variables: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEventTypePropsMixin.EventVariableProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    labels: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEventTypePropsMixin.LabelProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__954ed765d734efa5529fe30b538f3cea69bca0410700a1498de17514baae1edd(
    props: typing.Union[CfnEventTypeMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0e65237d0dd33526f35a4269fb957d978cd8c045e5158fa0e08357b60c1f894(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4de4827f71166518bcef2b4da254334befd864e654795641a6c023f49de506a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83c6cd0ee7fe15b632518c1e935a931093ee91781b076080d2b09400fdde9791(
    *,
    arn: typing.Optional[builtins.str] = None,
    created_time: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    inline: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    last_updated_time: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1179c169a7d8e97913c414ad79477b55a51724a9629bac0a2293ed91fd6140d(
    *,
    arn: typing.Optional[builtins.str] = None,
    created_time: typing.Optional[builtins.str] = None,
    data_source: typing.Optional[builtins.str] = None,
    data_type: typing.Optional[builtins.str] = None,
    default_value: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    inline: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    last_updated_time: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    variable_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea61eded696ea786d4bfb17af1de79a5c469cde96af69a2985b3336439dd68c0(
    *,
    arn: typing.Optional[builtins.str] = None,
    created_time: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    inline: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    last_updated_time: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c1f3327c1e889b48eafa79a5f58b0832aeaeea3da774c5cfeb8545538ecc21f(
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c498398211649bf0e210baab2ba36d7fde0ba5715ab614c2948b25ea40154af(
    props: typing.Union[CfnLabelMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2968e4d01191a1819467c2d040417ff88a92e9b96fdb33acae4a7dc442da08af(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c12e7f7fc61f554eb39ff28a82a0f38893d30992365f4c2b64b79e0d92b61d0a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd008fa0f23141cc9acc62dcac8c7a9f6f985d51cacaf8cc0f5e0ced997fe51b(
    *,
    description: typing.Optional[builtins.str] = None,
    elements: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    variable_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07278220a4e2387b1f82e709a10ee46ddcb63aef030d635296d9055e1962f31d(
    props: typing.Union[CfnListMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0353119c5735dfe15b67a11f5f81f9dd5987a20b64192a4c45cfc3706a9a75be(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1af014c19a2e3e7675f974c6df1b06f3b89c1799d0759e0f1e08ae27f9109dbe(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50603029460deb422e4541ab82802672091fdb679fcd49478a8b693d85beb1c6(
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a0a39c58f3a2e401eb8b9db18cc9e3ad9f1a691e62f57058cd9f396d5f51913(
    props: typing.Union[CfnOutcomeMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9fdb7807b40e9fa9351f228e0b32ffacaad6f207339cb5dfc1f34c9255a32eb(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fa87fd48341a373d1923710d3fdedae9480473bc740b0227260f7a255bd9302(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5f28faf95aba9437f5a3deeafad0c0fd97fc84de2ee5ac248c1a77b0e37587c(
    *,
    data_source: typing.Optional[builtins.str] = None,
    data_type: typing.Optional[builtins.str] = None,
    default_value: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    variable_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae073919d4f3ba9952abebe302dd47f53c8a692984ef3faad6a349abd827132d(
    props: typing.Union[CfnVariableMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71e0b35ca487c7720de96a1a703715a5d2ea874f40a015622974423e8cbc69ce(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__633bf09878b861f489a4426d5f2c7b7480124f0263ff890f0ce77231baa88e94(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
