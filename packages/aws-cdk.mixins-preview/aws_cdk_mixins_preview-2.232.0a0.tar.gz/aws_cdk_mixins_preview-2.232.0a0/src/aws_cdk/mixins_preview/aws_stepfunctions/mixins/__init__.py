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
import aws_cdk.interfaces.aws_logs as _aws_cdk_interfaces_aws_logs_ceddda9d
import constructs as _constructs_77d1e7e8
from ...aws_logs import ILogsDelivery as _ILogsDelivery_0d3c9e29
from ...core import IMixin as _IMixin_11e4b965, Mixin as _Mixin_a69446c0
from ...mixins import (
    CfnPropertyMixinOptions as _CfnPropertyMixinOptions_9cbff649,
    PropertyMergeStrategy as _PropertyMergeStrategy_49c157e8,
)


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_stepfunctions.mixins.CfnActivityMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "encryption_configuration": "encryptionConfiguration",
        "name": "name",
        "tags": "tags",
    },
)
class CfnActivityMixinProps:
    def __init__(
        self,
        *,
        encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnActivityPropsMixin.EncryptionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["CfnActivityPropsMixin.TagsEntryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnActivityPropsMixin.

        :param encryption_configuration: Encryption configuration for the activity. Activity configuration is immutable, and resource names must be unique. To set customer managed keys for encryption, you must create a *new Activity* . If you attempt to change the configuration in your CFN template for an existing activity, you will receive an ``ActivityAlreadyExists`` exception. To update your activity to include customer managed keys, set a new activity name within your CloudFormation template.
        :param name: The name of the activity. A name must *not* contain: - white space - brackets ``< > { } [ ]`` - wildcard characters ``? *`` - special characters ``" # % \\ ^ | ~ `` $ & , ; : /` - control characters ( ``U+0000-001F`` , ``U+007F-009F`` , ``U+FFFE-FFFF`` ) - surrogates ( ``U+D800-DFFF`` ) - invalid characters ( ``U+10FFFF`` ) To enable logging with CloudWatch Logs, the name should only contain 0-9, A-Z, a-z, - and _.
        :param tags: The list of tags to add to a resource. Tags may only contain Unicode letters, digits, white space, or these symbols: `_ . : / = + -

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-activity.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_stepfunctions import mixins as stepfunctions_mixins
            
            cfn_activity_mixin_props = stepfunctions_mixins.CfnActivityMixinProps(
                encryption_configuration=stepfunctions_mixins.CfnActivityPropsMixin.EncryptionConfigurationProperty(
                    kms_data_key_reuse_period_seconds=123,
                    kms_key_id="kmsKeyId",
                    type="type"
                ),
                name="name",
                tags=[stepfunctions_mixins.CfnActivityPropsMixin.TagsEntryProperty(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__819ed25a8b7de45e6eda4dd6744d7fc912e2afb427c8e3a9ab55264d259fc60f)
            check_type(argname="argument encryption_configuration", value=encryption_configuration, expected_type=type_hints["encryption_configuration"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if encryption_configuration is not None:
            self._values["encryption_configuration"] = encryption_configuration
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def encryption_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnActivityPropsMixin.EncryptionConfigurationProperty"]]:
        '''Encryption configuration for the activity.

        Activity configuration is immutable, and resource names must be unique. To set customer managed keys for encryption, you must create a *new Activity* . If you attempt to change the configuration in your CFN template for an existing activity, you will receive an ``ActivityAlreadyExists`` exception.

        To update your activity to include customer managed keys, set a new activity name within your CloudFormation template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-activity.html#cfn-stepfunctions-activity-encryptionconfiguration
        '''
        result = self._values.get("encryption_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnActivityPropsMixin.EncryptionConfigurationProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the activity.

        A name must *not* contain:

        - white space
        - brackets ``< > { } [ ]``
        - wildcard characters ``? *``
        - special characters ``" # % \\ ^ | ~ `` $ & , ; : /`
        - control characters ( ``U+0000-001F`` , ``U+007F-009F`` , ``U+FFFE-FFFF`` )
        - surrogates ( ``U+D800-DFFF`` )
        - invalid characters ( ``U+10FFFF`` )

        To enable logging with CloudWatch Logs, the name should only contain 0-9, A-Z, a-z, - and _.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-activity.html#cfn-stepfunctions-activity-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(
        self,
    ) -> typing.Optional[typing.List["CfnActivityPropsMixin.TagsEntryProperty"]]:
        '''The list of tags to add to a resource.

        Tags may only contain Unicode letters, digits, white space, or these symbols: `_ . : / = + -

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-activity.html#cfn-stepfunctions-activity-tags
        :: ` .
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["CfnActivityPropsMixin.TagsEntryProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnActivityMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnActivityPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_stepfunctions.mixins.CfnActivityPropsMixin",
):
    '''An activity is a task that you write in any programming language and host on any machine that has access to AWS Step Functions .

    Activities must poll Step Functions using the ``GetActivityTask`` API action and respond using ``SendTask*`` API actions. This function makes Step Functions aware of your activity and returns an identifier for use in a state machine and when polling from the activity.

    For information about creating an activity, see `Creating an Activity State Machine <https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-creating-activity-state-machine.html>`_ in the *AWS Step Functions Developer Guide* and `CreateActivity <https://docs.aws.amazon.com/step-functions/latest/apireference/API_CreateActivity.html>`_ in the *AWS Step Functions API Reference* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-activity.html
    :cloudformationResource: AWS::StepFunctions::Activity
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_stepfunctions import mixins as stepfunctions_mixins
        
        cfn_activity_props_mixin = stepfunctions_mixins.CfnActivityPropsMixin(stepfunctions_mixins.CfnActivityMixinProps(
            encryption_configuration=stepfunctions_mixins.CfnActivityPropsMixin.EncryptionConfigurationProperty(
                kms_data_key_reuse_period_seconds=123,
                kms_key_id="kmsKeyId",
                type="type"
            ),
            name="name",
            tags=[stepfunctions_mixins.CfnActivityPropsMixin.TagsEntryProperty(
                key="key",
                value="value"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnActivityMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::StepFunctions::Activity``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f0f4283ba9c37c36e33c5ed6f60c78cb98c17d0f6909c564310b835cf6c6271)
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
            type_hints = typing.get_type_hints(_typecheckingstub__655a11b296cd2b3fd72449398b5ec131ea10f6f9bcdb3282eb4fbd90c14f0b9c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd4d60fdb57c0b6e7d0178ec5f8af0cbc45e9448d5f8c3610789b8b2a5e746c9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnActivityMixinProps:
        return typing.cast(CfnActivityMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_stepfunctions.mixins.CfnActivityPropsMixin.EncryptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "kms_data_key_reuse_period_seconds": "kmsDataKeyReusePeriodSeconds",
            "kms_key_id": "kmsKeyId",
            "type": "type",
        },
    )
    class EncryptionConfigurationProperty:
        def __init__(
            self,
            *,
            kms_data_key_reuse_period_seconds: typing.Optional[jsii.Number] = None,
            kms_key_id: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Settings to configure server-side encryption for an activity.

            By default, Step Functions provides transparent server-side encryption. With this configuration, you can specify a customer managed AWS  key for encryption.

            :param kms_data_key_reuse_period_seconds: Maximum duration that Step Functions will reuse data keys. When the period expires, Step Functions will call ``GenerateDataKey`` . Only applies to customer managed keys.
            :param kms_key_id: An alias, alias ARN, key ID, or key ARN of a symmetric encryption AWS key to encrypt data. To specify a AWS key in a different AWS account, you must use the key ARN or alias ARN.
            :param type: Encryption option for an activity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-activity-encryptionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_stepfunctions import mixins as stepfunctions_mixins
                
                encryption_configuration_property = stepfunctions_mixins.CfnActivityPropsMixin.EncryptionConfigurationProperty(
                    kms_data_key_reuse_period_seconds=123,
                    kms_key_id="kmsKeyId",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__36b1c05ac6b10d614f6180f0a35a52acc01fb3e9ae65630da80b9296b9b957c8)
                check_type(argname="argument kms_data_key_reuse_period_seconds", value=kms_data_key_reuse_period_seconds, expected_type=type_hints["kms_data_key_reuse_period_seconds"])
                check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kms_data_key_reuse_period_seconds is not None:
                self._values["kms_data_key_reuse_period_seconds"] = kms_data_key_reuse_period_seconds
            if kms_key_id is not None:
                self._values["kms_key_id"] = kms_key_id
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def kms_data_key_reuse_period_seconds(self) -> typing.Optional[jsii.Number]:
            '''Maximum duration that Step Functions will reuse data keys.

            When the period expires, Step Functions will call ``GenerateDataKey`` . Only applies to customer managed keys.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-activity-encryptionconfiguration.html#cfn-stepfunctions-activity-encryptionconfiguration-kmsdatakeyreuseperiodseconds
            '''
            result = self._values.get("kms_data_key_reuse_period_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def kms_key_id(self) -> typing.Optional[builtins.str]:
            '''An alias, alias ARN, key ID, or key ARN of a symmetric encryption AWS  key to encrypt data.

            To specify a AWS  key in a different AWS account, you must use the key ARN or alias ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-activity-encryptionconfiguration.html#cfn-stepfunctions-activity-encryptionconfiguration-kmskeyid
            '''
            result = self._values.get("kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''Encryption option for an activity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-activity-encryptionconfiguration.html#cfn-stepfunctions-activity-encryptionconfiguration-type
            '''
            result = self._values.get("type")
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
        jsii_type="@aws-cdk/mixins-preview.aws_stepfunctions.mixins.CfnActivityPropsMixin.TagsEntryProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TagsEntryProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``TagsEntry`` property specifies *tags* to identify an activity.

            :param key: The ``key`` for a key-value pair in a tag entry.
            :param value: The ``value`` for a key-value pair in a tag entry.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-activity-tagsentry.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_stepfunctions import mixins as stepfunctions_mixins
                
                tags_entry_property = stepfunctions_mixins.CfnActivityPropsMixin.TagsEntryProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__476f58636160fd4a6a8cc1615f6704106b89a48fc1d9154280c3f2dafc2fbda4)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The ``key`` for a key-value pair in a tag entry.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-activity-tagsentry.html#cfn-stepfunctions-activity-tagsentry-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The ``value`` for a key-value pair in a tag entry.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-activity-tagsentry.html#cfn-stepfunctions-activity-tagsentry-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagsEntryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_stepfunctions.mixins.CfnStateMachineAliasMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "deployment_preference": "deploymentPreference",
        "description": "description",
        "name": "name",
        "routing_configuration": "routingConfiguration",
    },
)
class CfnStateMachineAliasMixinProps:
    def __init__(
        self,
        *,
        deployment_preference: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStateMachineAliasPropsMixin.DeploymentPreferenceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        routing_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStateMachineAliasPropsMixin.RoutingConfigurationVersionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnStateMachineAliasPropsMixin.

        :param deployment_preference: The settings that enable gradual state machine deployments. These settings include `Alarms <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachinealias-deploymentpreference.html#cfn-stepfunctions-statemachinealias-deploymentpreference-alarms>`_ , `Interval <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachinealias-deploymentpreference.html#cfn-stepfunctions-statemachinealias-deploymentpreference-interval>`_ , `Percentage <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachinealias-deploymentpreference.html#cfn-stepfunctions-statemachinealias-deploymentpreference-percentage>`_ , `StateMachineVersionArn <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachinealias-deploymentpreference.html#cfn-stepfunctions-statemachinealias-deploymentpreference-statemachineversionarn>`_ , and `Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachinealias-deploymentpreference.html#cfn-stepfunctions-statemachinealias-deploymentpreference-type>`_ . CloudFormation automatically shifts traffic from the version an alias currently points to, to a new state machine version that you specify. .. epigraph:: ``RoutingConfiguration`` and ``DeploymentPreference`` are mutually exclusive properties. You must define only one of these properties. Based on the type of deployment you want to perform, you can specify one of the following settings: - ``LINEAR`` - Shifts traffic to the new version in equal increments with an equal number of minutes between each increment. For example, if you specify the increment percent as ``20`` with an interval of ``600`` minutes, this deployment increases traffic by 20 percent every 600 minutes until the new version receives 100 percent of the traffic. This deployment immediately rolls back the new version if any Amazon CloudWatch alarms are triggered. - ``ALL_AT_ONCE`` - Shifts 100 percent of traffic to the new version immediately. CloudFormation monitors the new version and rolls it back automatically to the previous version if any CloudWatch alarms are triggered. - ``CANARY`` - Shifts traffic in two increments. In the first increment, a small percentage of traffic, for example, 10 percent is shifted to the new version. In the second increment, before a specified time interval in seconds gets over, the remaining traffic is shifted to the new version. The shift to the new version for the remaining traffic takes place only if no CloudWatch alarms are triggered during the specified time interval.
        :param description: An optional description of the state machine alias.
        :param name: The name of the state machine alias. If you don't provide a name, it uses an automatically generated name based on the logical ID.
        :param routing_configuration: The routing configuration of an alias. Routing configuration splits `StartExecution <https://docs.aws.amazon.com/step-functions/latest/apireference/API_StartExecution.html>`_ requests between one or two versions of the same state machine. Use ``RoutingConfiguration`` if you want to explicitly set the alias `weights <https://docs.aws.amazon.com/step-functions/latest/apireference/API_RoutingConfigurationListItem.html#StepFunctions-Type-RoutingConfigurationListItem-weight>`_ . Weight is the percentage of traffic you want to route to a state machine version. .. epigraph:: ``RoutingConfiguration`` and ``DeploymentPreference`` are mutually exclusive properties. You must define only one of these properties.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachinealias.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_stepfunctions import mixins as stepfunctions_mixins
            
            cfn_state_machine_alias_mixin_props = stepfunctions_mixins.CfnStateMachineAliasMixinProps(
                deployment_preference=stepfunctions_mixins.CfnStateMachineAliasPropsMixin.DeploymentPreferenceProperty(
                    alarms=["alarms"],
                    interval=123,
                    percentage=123,
                    state_machine_version_arn="stateMachineVersionArn",
                    type="type"
                ),
                description="description",
                name="name",
                routing_configuration=[stepfunctions_mixins.CfnStateMachineAliasPropsMixin.RoutingConfigurationVersionProperty(
                    state_machine_version_arn="stateMachineVersionArn",
                    weight=123
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de64f90980360154d77cab303a7e0ec9c981c1ae7b39627457747056a78217c2)
            check_type(argname="argument deployment_preference", value=deployment_preference, expected_type=type_hints["deployment_preference"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument routing_configuration", value=routing_configuration, expected_type=type_hints["routing_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if deployment_preference is not None:
            self._values["deployment_preference"] = deployment_preference
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if routing_configuration is not None:
            self._values["routing_configuration"] = routing_configuration

    @builtins.property
    def deployment_preference(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStateMachineAliasPropsMixin.DeploymentPreferenceProperty"]]:
        '''The settings that enable gradual state machine deployments.

        These settings include `Alarms <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachinealias-deploymentpreference.html#cfn-stepfunctions-statemachinealias-deploymentpreference-alarms>`_ , `Interval <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachinealias-deploymentpreference.html#cfn-stepfunctions-statemachinealias-deploymentpreference-interval>`_ , `Percentage <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachinealias-deploymentpreference.html#cfn-stepfunctions-statemachinealias-deploymentpreference-percentage>`_ , `StateMachineVersionArn <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachinealias-deploymentpreference.html#cfn-stepfunctions-statemachinealias-deploymentpreference-statemachineversionarn>`_ , and `Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachinealias-deploymentpreference.html#cfn-stepfunctions-statemachinealias-deploymentpreference-type>`_ .

        CloudFormation automatically shifts traffic from the version an alias currently points to, to a new state machine version that you specify.
        .. epigraph::

           ``RoutingConfiguration`` and ``DeploymentPreference`` are mutually exclusive properties. You must define only one of these properties.

        Based on the type of deployment you want to perform, you can specify one of the following settings:

        - ``LINEAR`` - Shifts traffic to the new version in equal increments with an equal number of minutes between each increment.

        For example, if you specify the increment percent as ``20`` with an interval of ``600`` minutes, this deployment increases traffic by 20 percent every 600 minutes until the new version receives 100 percent of the traffic. This deployment immediately rolls back the new version if any Amazon CloudWatch alarms are triggered.

        - ``ALL_AT_ONCE`` - Shifts 100 percent of traffic to the new version immediately. CloudFormation monitors the new version and rolls it back automatically to the previous version if any CloudWatch alarms are triggered.
        - ``CANARY`` - Shifts traffic in two increments.

        In the first increment, a small percentage of traffic, for example, 10 percent is shifted to the new version. In the second increment, before a specified time interval in seconds gets over, the remaining traffic is shifted to the new version. The shift to the new version for the remaining traffic takes place only if no CloudWatch alarms are triggered during the specified time interval.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachinealias.html#cfn-stepfunctions-statemachinealias-deploymentpreference
        '''
        result = self._values.get("deployment_preference")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStateMachineAliasPropsMixin.DeploymentPreferenceProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of the state machine alias.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachinealias.html#cfn-stepfunctions-statemachinealias-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the state machine alias.

        If you don't provide a name, it uses an automatically generated name based on the logical ID.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachinealias.html#cfn-stepfunctions-statemachinealias-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def routing_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStateMachineAliasPropsMixin.RoutingConfigurationVersionProperty"]]]]:
        '''The routing configuration of an alias.

        Routing configuration splits `StartExecution <https://docs.aws.amazon.com/step-functions/latest/apireference/API_StartExecution.html>`_ requests between one or two versions of the same state machine.

        Use ``RoutingConfiguration`` if you want to explicitly set the alias `weights <https://docs.aws.amazon.com/step-functions/latest/apireference/API_RoutingConfigurationListItem.html#StepFunctions-Type-RoutingConfigurationListItem-weight>`_ . Weight is the percentage of traffic you want to route to a state machine version.
        .. epigraph::

           ``RoutingConfiguration`` and ``DeploymentPreference`` are mutually exclusive properties. You must define only one of these properties.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachinealias.html#cfn-stepfunctions-statemachinealias-routingconfiguration
        '''
        result = self._values.get("routing_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStateMachineAliasPropsMixin.RoutingConfigurationVersionProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStateMachineAliasMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnStateMachineAliasPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_stepfunctions.mixins.CfnStateMachineAliasPropsMixin",
):
    '''Represents a state machine `alias <https://docs.aws.amazon.com/step-functions/latest/dg/concepts-state-machine-alias.html>`_ . An alias routes traffic to one or two versions of the same state machine.

    You can create up to 100 aliases for each state machine.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachinealias.html
    :cloudformationResource: AWS::StepFunctions::StateMachineAlias
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_stepfunctions import mixins as stepfunctions_mixins
        
        cfn_state_machine_alias_props_mixin = stepfunctions_mixins.CfnStateMachineAliasPropsMixin(stepfunctions_mixins.CfnStateMachineAliasMixinProps(
            deployment_preference=stepfunctions_mixins.CfnStateMachineAliasPropsMixin.DeploymentPreferenceProperty(
                alarms=["alarms"],
                interval=123,
                percentage=123,
                state_machine_version_arn="stateMachineVersionArn",
                type="type"
            ),
            description="description",
            name="name",
            routing_configuration=[stepfunctions_mixins.CfnStateMachineAliasPropsMixin.RoutingConfigurationVersionProperty(
                state_machine_version_arn="stateMachineVersionArn",
                weight=123
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnStateMachineAliasMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::StepFunctions::StateMachineAlias``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a74842a5c5fee0aebfe74930fc111ab9eabdd43c1db765695c352149d02ac113)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b934c04f2c519d2549e608617e079bb51b22d52b042b9e2fb9d01edde8d6fe8f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7aa8fc54ab1f13b648998ac52396362066ce3a3e2903056a0df9b0b628a5e9d3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnStateMachineAliasMixinProps:
        return typing.cast(CfnStateMachineAliasMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_stepfunctions.mixins.CfnStateMachineAliasPropsMixin.DeploymentPreferenceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "alarms": "alarms",
            "interval": "interval",
            "percentage": "percentage",
            "state_machine_version_arn": "stateMachineVersionArn",
            "type": "type",
        },
    )
    class DeploymentPreferenceProperty:
        def __init__(
            self,
            *,
            alarms: typing.Optional[typing.Sequence[builtins.str]] = None,
            interval: typing.Optional[jsii.Number] = None,
            percentage: typing.Optional[jsii.Number] = None,
            state_machine_version_arn: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Enables gradual state machine deployments.

            CloudFormation automatically shifts traffic from the version the alias currently points to, to a new state machine version that you specify.

            :param alarms: A list of Amazon CloudWatch alarm names to be monitored during the deployment. The deployment fails and rolls back if any of these alarms go into the ``ALARM`` state. .. epigraph:: Amazon CloudWatch considers nonexistent alarms to have an ``OK`` state. If you provide an invalid alarm name or provide the ARN of an alarm instead of its name, your deployment may not roll back correctly.
            :param interval: The time in minutes between each traffic shifting increment.
            :param percentage: The percentage of traffic to shift to the new version in each increment.
            :param state_machine_version_arn: The Amazon Resource Name (ARN) of the ```AWS::StepFunctions::StateMachineVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachineversion.html>`_ resource that will be the final version to which the alias points to when the traffic shifting is complete. While performing gradual deployments, you can only provide a single state machine version ARN. To explicitly set version weights in a CloudFormation template, use ``RoutingConfiguration`` instead.
            :param type: The type of deployment you want to perform. You can specify one of the following types:. - ``LINEAR`` - Shifts traffic to the new version in equal increments with an equal number of minutes between each increment. For example, if you specify the increment percent as ``20`` with an interval of ``600`` minutes, this deployment increases traffic by 20 percent every 600 minutes until the new version receives 100 percent of the traffic. This deployment immediately rolls back the new version if any CloudWatch alarms are triggered. - ``ALL_AT_ONCE`` - Shifts 100 percent of traffic to the new version immediately. CloudFormation monitors the new version and rolls it back automatically to the previous version if any CloudWatch alarms are triggered. - ``CANARY`` - Shifts traffic in two increments. In the first increment, a small percentage of traffic, for example, 10 percent is shifted to the new version. In the second increment, before a specified time interval in seconds gets over, the remaining traffic is shifted to the new version. The shift to the new version for the remaining traffic takes place only if no CloudWatch alarms are triggered during the specified time interval.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachinealias-deploymentpreference.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_stepfunctions import mixins as stepfunctions_mixins
                
                deployment_preference_property = stepfunctions_mixins.CfnStateMachineAliasPropsMixin.DeploymentPreferenceProperty(
                    alarms=["alarms"],
                    interval=123,
                    percentage=123,
                    state_machine_version_arn="stateMachineVersionArn",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__03c55a442cbadfbe37a8c0c6e2350cdd77bb36e934a6e077971ba080e0e05ddd)
                check_type(argname="argument alarms", value=alarms, expected_type=type_hints["alarms"])
                check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
                check_type(argname="argument percentage", value=percentage, expected_type=type_hints["percentage"])
                check_type(argname="argument state_machine_version_arn", value=state_machine_version_arn, expected_type=type_hints["state_machine_version_arn"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if alarms is not None:
                self._values["alarms"] = alarms
            if interval is not None:
                self._values["interval"] = interval
            if percentage is not None:
                self._values["percentage"] = percentage
            if state_machine_version_arn is not None:
                self._values["state_machine_version_arn"] = state_machine_version_arn
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def alarms(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of Amazon CloudWatch alarm names to be monitored during the deployment.

            The deployment fails and rolls back if any of these alarms go into the ``ALARM`` state.
            .. epigraph::

               Amazon CloudWatch considers nonexistent alarms to have an ``OK`` state. If you provide an invalid alarm name or provide the ARN of an alarm instead of its name, your deployment may not roll back correctly.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachinealias-deploymentpreference.html#cfn-stepfunctions-statemachinealias-deploymentpreference-alarms
            '''
            result = self._values.get("alarms")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def interval(self) -> typing.Optional[jsii.Number]:
            '''The time in minutes between each traffic shifting increment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachinealias-deploymentpreference.html#cfn-stepfunctions-statemachinealias-deploymentpreference-interval
            '''
            result = self._values.get("interval")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def percentage(self) -> typing.Optional[jsii.Number]:
            '''The percentage of traffic to shift to the new version in each increment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachinealias-deploymentpreference.html#cfn-stepfunctions-statemachinealias-deploymentpreference-percentage
            '''
            result = self._values.get("percentage")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def state_machine_version_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the ```AWS::StepFunctions::StateMachineVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachineversion.html>`_ resource that will be the final version to which the alias points to when the traffic shifting is complete.

            While performing gradual deployments, you can only provide a single state machine version ARN. To explicitly set version weights in a CloudFormation template, use ``RoutingConfiguration`` instead.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachinealias-deploymentpreference.html#cfn-stepfunctions-statemachinealias-deploymentpreference-statemachineversionarn
            '''
            result = self._values.get("state_machine_version_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of deployment you want to perform. You can specify one of the following types:.

            - ``LINEAR`` - Shifts traffic to the new version in equal increments with an equal number of minutes between each increment.

            For example, if you specify the increment percent as ``20`` with an interval of ``600`` minutes, this deployment increases traffic by 20 percent every 600 minutes until the new version receives 100 percent of the traffic. This deployment immediately rolls back the new version if any CloudWatch alarms are triggered.

            - ``ALL_AT_ONCE`` - Shifts 100 percent of traffic to the new version immediately. CloudFormation monitors the new version and rolls it back automatically to the previous version if any CloudWatch alarms are triggered.
            - ``CANARY`` - Shifts traffic in two increments.

            In the first increment, a small percentage of traffic, for example, 10 percent is shifted to the new version. In the second increment, before a specified time interval in seconds gets over, the remaining traffic is shifted to the new version. The shift to the new version for the remaining traffic takes place only if no CloudWatch alarms are triggered during the specified time interval.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachinealias-deploymentpreference.html#cfn-stepfunctions-statemachinealias-deploymentpreference-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeploymentPreferenceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_stepfunctions.mixins.CfnStateMachineAliasPropsMixin.RoutingConfigurationVersionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "state_machine_version_arn": "stateMachineVersionArn",
            "weight": "weight",
        },
    )
    class RoutingConfigurationVersionProperty:
        def __init__(
            self,
            *,
            state_machine_version_arn: typing.Optional[builtins.str] = None,
            weight: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The state machine version to which you want to route the execution traffic.

            :param state_machine_version_arn: The Amazon Resource Name (ARN) that identifies one or two state machine versions defined in the routing configuration. If you specify the ARN of a second version, it must belong to the same state machine as the first version.
            :param weight: The percentage of traffic you want to route to the state machine version. The sum of the weights in the routing configuration must be equal to 100.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachinealias-routingconfigurationversion.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_stepfunctions import mixins as stepfunctions_mixins
                
                routing_configuration_version_property = stepfunctions_mixins.CfnStateMachineAliasPropsMixin.RoutingConfigurationVersionProperty(
                    state_machine_version_arn="stateMachineVersionArn",
                    weight=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bda252c72eef87ff6379599fd98c1071dfde8ce8a15bc658b7308c3095033cc4)
                check_type(argname="argument state_machine_version_arn", value=state_machine_version_arn, expected_type=type_hints["state_machine_version_arn"])
                check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if state_machine_version_arn is not None:
                self._values["state_machine_version_arn"] = state_machine_version_arn
            if weight is not None:
                self._values["weight"] = weight

        @builtins.property
        def state_machine_version_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) that identifies one or two state machine versions defined in the routing configuration.

            If you specify the ARN of a second version, it must belong to the same state machine as the first version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachinealias-routingconfigurationversion.html#cfn-stepfunctions-statemachinealias-routingconfigurationversion-statemachineversionarn
            '''
            result = self._values.get("state_machine_version_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def weight(self) -> typing.Optional[jsii.Number]:
            '''The percentage of traffic you want to route to the state machine version.

            The sum of the weights in the routing configuration must be equal to 100.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachinealias-routingconfigurationversion.html#cfn-stepfunctions-statemachinealias-routingconfigurationversion-weight
            '''
            result = self._values.get("weight")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RoutingConfigurationVersionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


class CfnStateMachineExpressLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_stepfunctions.mixins.CfnStateMachineExpressLogs",
):
    '''Builder for CfnStateMachineLogsMixin to generate EXPRESS_LOGS for CfnStateMachine.

    :cloudformationResource: AWS::StepFunctions::StateMachine
    :logType: EXPRESS_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_stepfunctions import mixins as stepfunctions_mixins
        
        cfn_state_machine_express_logs = stepfunctions_mixins.CfnStateMachineExpressLogs()
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> "CfnStateMachineLogsMixin":
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a7c1718a2764a6832854b3071fef98f9d8e965ebd36a4f369a3cedaa953e7b0)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast("CfnStateMachineLogsMixin", jsii.invoke(self, "toLogGroup", [log_group]))


@jsii.implements(_IMixin_11e4b965)
class CfnStateMachineLogsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_stepfunctions.mixins.CfnStateMachineLogsMixin",
):
    '''Provisions a state machine.

    A state machine consists of a collection of states that can do work ( ``Task`` states), determine to which states to transition next ( ``Choice`` states), stop an execution with an error ( ``Fail`` states), and so on. State machines are specified using a JSON-based, structured language.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html
    :cloudformationResource: AWS::StepFunctions::StateMachine
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import aws_logs as logs
        from aws_cdk.mixins_preview.aws_stepfunctions import mixins as stepfunctions_mixins
        
        # logs_delivery: logs.ILogsDelivery
        
        cfn_state_machine_logs_mixin = stepfunctions_mixins.CfnStateMachineLogsMixin("logType", logs_delivery)
    '''

    def __init__(
        self,
        log_type: builtins.str,
        log_delivery: _ILogsDelivery_0d3c9e29,
    ) -> None:
        '''Create a mixin to enable vended logs for ``AWS::StepFunctions::StateMachine``.

        :param log_type: Type of logs that are getting vended.
        :param log_delivery: Object in charge of setting up the delivery destination and delivery connection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b3a34dcdb545059f78345b115ad4dfe2413a98ee45ea5393ff3cfaf2e8b513e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e37c0611dd50ea0c45d059142de43141228e4fb18815146a81b766cd20b1fade)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [resource]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct (has vendedLogs property).

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb1f5c0ad06c62110858ede307dc71574289f36b2977d7855936e4928820909e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="EXPRESS_LOGS")
    def EXPRESS_LOGS(cls) -> CfnStateMachineExpressLogs:
        return typing.cast(CfnStateMachineExpressLogs, jsii.sget(cls, "EXPRESS_LOGS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="STANDARD_LOGS")
    def STANDARD_LOGS(cls) -> "CfnStateMachineStandardLogs":
        return typing.cast("CfnStateMachineStandardLogs", jsii.sget(cls, "STANDARD_LOGS"))

    @builtins.property
    @jsii.member(jsii_name="logDelivery")
    def _log_delivery(self) -> _ILogsDelivery_0d3c9e29:
        return typing.cast(_ILogsDelivery_0d3c9e29, jsii.get(self, "logDelivery"))

    @builtins.property
    @jsii.member(jsii_name="logType")
    def _log_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logType"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_stepfunctions.mixins.CfnStateMachineMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "definition": "definition",
        "definition_s3_location": "definitionS3Location",
        "definition_string": "definitionString",
        "definition_substitutions": "definitionSubstitutions",
        "encryption_configuration": "encryptionConfiguration",
        "logging_configuration": "loggingConfiguration",
        "role_arn": "roleArn",
        "state_machine_name": "stateMachineName",
        "state_machine_type": "stateMachineType",
        "tags": "tags",
        "tracing_configuration": "tracingConfiguration",
    },
)
class CfnStateMachineMixinProps:
    def __init__(
        self,
        *,
        definition: typing.Any = None,
        definition_s3_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStateMachinePropsMixin.S3LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        definition_string: typing.Optional[builtins.str] = None,
        definition_substitutions: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStateMachinePropsMixin.EncryptionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        logging_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStateMachinePropsMixin.LoggingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        role_arn: typing.Optional[builtins.str] = None,
        state_machine_name: typing.Optional[builtins.str] = None,
        state_machine_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["CfnStateMachinePropsMixin.TagsEntryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tracing_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStateMachinePropsMixin.TracingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnStateMachinePropsMixin.

        :param definition: The Amazon States Language definition of the state machine. The state machine definition must be in JSON or YAML, and the format of the object must match the format of your CloudFormation template file. See `Amazon States Language <https://docs.aws.amazon.com/step-functions/latest/dg/concepts-amazon-states-language.html>`_ .
        :param definition_s3_location: The name of the S3 bucket where the state machine definition is stored. The state machine definition must be a JSON or YAML file.
        :param definition_string: The Amazon States Language definition of the state machine. The state machine definition must be in JSON. See `Amazon States Language <https://docs.aws.amazon.com/step-functions/latest/dg/concepts-amazon-states-language.html>`_ .
        :param definition_substitutions: A map (string to string) that specifies the mappings for placeholder variables in the state machine definition. This enables the customer to inject values obtained at runtime, for example from intrinsic functions, in the state machine definition. Variables can be template parameter names, resource logical IDs, resource attributes, or a variable in a key-value map. Substitutions must follow the syntax: ``${key_name}`` or ``${variable_1,variable_2,...}`` .
        :param encryption_configuration: Encryption configuration for the state machine.
        :param logging_configuration: Defines what execution history events are logged and where they are logged. .. epigraph:: By default, the ``level`` is set to ``OFF`` . For more information see `Log Levels <https://docs.aws.amazon.com/step-functions/latest/dg/cloudwatch-log-level.html>`_ in the AWS Step Functions User Guide.
        :param role_arn: The Amazon Resource Name (ARN) of the IAM role to use for this state machine.
        :param state_machine_name: The name of the state machine. A name must *not* contain: - white space - brackets ``< > { } [ ]`` - wildcard characters ``? *`` - special characters ``" # % \\ ^ | ~ `` $ & , ; : /` - control characters ( ``U+0000-001F`` , ``U+007F-009F`` ) .. epigraph:: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
        :param state_machine_type: Determines whether a ``STANDARD`` or ``EXPRESS`` state machine is created. The default is ``STANDARD`` . You cannot update the ``type`` of a state machine once it has been created. For more information on ``STANDARD`` and ``EXPRESS`` workflows, see `Standard Versus Express Workflows <https://docs.aws.amazon.com/step-functions/latest/dg/concepts-standard-vs-express.html>`_ in the AWS Step Functions Developer Guide.
        :param tags: The list of tags to add to a resource. Tags may only contain Unicode letters, digits, white space, or these symbols: `_ . : / = + -
        :param tracing_configuration: Selects whether or not the state machine's AWS X-Ray tracing is enabled.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_stepfunctions import mixins as stepfunctions_mixins
            
            # definition: Any
            
            cfn_state_machine_mixin_props = stepfunctions_mixins.CfnStateMachineMixinProps(
                definition=definition,
                definition_s3_location=stepfunctions_mixins.CfnStateMachinePropsMixin.S3LocationProperty(
                    bucket="bucket",
                    key="key",
                    version="version"
                ),
                definition_string="definitionString",
                definition_substitutions={
                    "definition_substitutions_key": "definitionSubstitutions"
                },
                encryption_configuration=stepfunctions_mixins.CfnStateMachinePropsMixin.EncryptionConfigurationProperty(
                    kms_data_key_reuse_period_seconds=123,
                    kms_key_id="kmsKeyId",
                    type="type"
                ),
                logging_configuration=stepfunctions_mixins.CfnStateMachinePropsMixin.LoggingConfigurationProperty(
                    destinations=[stepfunctions_mixins.CfnStateMachinePropsMixin.LogDestinationProperty(
                        cloud_watch_logs_log_group=stepfunctions_mixins.CfnStateMachinePropsMixin.CloudWatchLogsLogGroupProperty(
                            log_group_arn="logGroupArn"
                        )
                    )],
                    include_execution_data=False,
                    level="level"
                ),
                role_arn="roleArn",
                state_machine_name="stateMachineName",
                state_machine_type="stateMachineType",
                tags=[stepfunctions_mixins.CfnStateMachinePropsMixin.TagsEntryProperty(
                    key="key",
                    value="value"
                )],
                tracing_configuration=stepfunctions_mixins.CfnStateMachinePropsMixin.TracingConfigurationProperty(
                    enabled=False
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f2726973acc336ef70783184ea0ab5b637fee156377224526a2c139d8ab4abe)
            check_type(argname="argument definition", value=definition, expected_type=type_hints["definition"])
            check_type(argname="argument definition_s3_location", value=definition_s3_location, expected_type=type_hints["definition_s3_location"])
            check_type(argname="argument definition_string", value=definition_string, expected_type=type_hints["definition_string"])
            check_type(argname="argument definition_substitutions", value=definition_substitutions, expected_type=type_hints["definition_substitutions"])
            check_type(argname="argument encryption_configuration", value=encryption_configuration, expected_type=type_hints["encryption_configuration"])
            check_type(argname="argument logging_configuration", value=logging_configuration, expected_type=type_hints["logging_configuration"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument state_machine_name", value=state_machine_name, expected_type=type_hints["state_machine_name"])
            check_type(argname="argument state_machine_type", value=state_machine_type, expected_type=type_hints["state_machine_type"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tracing_configuration", value=tracing_configuration, expected_type=type_hints["tracing_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if definition is not None:
            self._values["definition"] = definition
        if definition_s3_location is not None:
            self._values["definition_s3_location"] = definition_s3_location
        if definition_string is not None:
            self._values["definition_string"] = definition_string
        if definition_substitutions is not None:
            self._values["definition_substitutions"] = definition_substitutions
        if encryption_configuration is not None:
            self._values["encryption_configuration"] = encryption_configuration
        if logging_configuration is not None:
            self._values["logging_configuration"] = logging_configuration
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if state_machine_name is not None:
            self._values["state_machine_name"] = state_machine_name
        if state_machine_type is not None:
            self._values["state_machine_type"] = state_machine_type
        if tags is not None:
            self._values["tags"] = tags
        if tracing_configuration is not None:
            self._values["tracing_configuration"] = tracing_configuration

    @builtins.property
    def definition(self) -> typing.Any:
        '''The Amazon States Language definition of the state machine.

        The state machine definition must be in JSON or YAML, and the format of the object must match the format of your CloudFormation template file. See `Amazon States Language <https://docs.aws.amazon.com/step-functions/latest/dg/concepts-amazon-states-language.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html#cfn-stepfunctions-statemachine-definition
        '''
        result = self._values.get("definition")
        return typing.cast(typing.Any, result)

    @builtins.property
    def definition_s3_location(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStateMachinePropsMixin.S3LocationProperty"]]:
        '''The name of the S3 bucket where the state machine definition is stored.

        The state machine definition must be a JSON or YAML file.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html#cfn-stepfunctions-statemachine-definitions3location
        '''
        result = self._values.get("definition_s3_location")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStateMachinePropsMixin.S3LocationProperty"]], result)

    @builtins.property
    def definition_string(self) -> typing.Optional[builtins.str]:
        '''The Amazon States Language definition of the state machine.

        The state machine definition must be in JSON. See `Amazon States Language <https://docs.aws.amazon.com/step-functions/latest/dg/concepts-amazon-states-language.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html#cfn-stepfunctions-statemachine-definitionstring
        '''
        result = self._values.get("definition_string")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def definition_substitutions(
        self,
    ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
        '''A map (string to string) that specifies the mappings for placeholder variables in the state machine definition.

        This enables the customer to inject values obtained at runtime, for example from intrinsic functions, in the state machine definition. Variables can be template parameter names, resource logical IDs, resource attributes, or a variable in a key-value map.

        Substitutions must follow the syntax: ``${key_name}`` or ``${variable_1,variable_2,...}`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html#cfn-stepfunctions-statemachine-definitionsubstitutions
        '''
        result = self._values.get("definition_substitutions")
        return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def encryption_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStateMachinePropsMixin.EncryptionConfigurationProperty"]]:
        '''Encryption configuration for the state machine.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html#cfn-stepfunctions-statemachine-encryptionconfiguration
        '''
        result = self._values.get("encryption_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStateMachinePropsMixin.EncryptionConfigurationProperty"]], result)

    @builtins.property
    def logging_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStateMachinePropsMixin.LoggingConfigurationProperty"]]:
        '''Defines what execution history events are logged and where they are logged.

        .. epigraph::

           By default, the ``level`` is set to ``OFF`` . For more information see `Log Levels <https://docs.aws.amazon.com/step-functions/latest/dg/cloudwatch-log-level.html>`_ in the AWS Step Functions User Guide.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html#cfn-stepfunctions-statemachine-loggingconfiguration
        '''
        result = self._values.get("logging_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStateMachinePropsMixin.LoggingConfigurationProperty"]], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the IAM role to use for this state machine.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html#cfn-stepfunctions-statemachine-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state_machine_name(self) -> typing.Optional[builtins.str]:
        '''The name of the state machine.

        A name must *not* contain:

        - white space
        - brackets ``< > { } [ ]``
        - wildcard characters ``? *``
        - special characters ``" # % \\ ^ | ~ `` $ & , ; : /`
        - control characters ( ``U+0000-001F`` , ``U+007F-009F`` )

        .. epigraph::

           If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html#cfn-stepfunctions-statemachine-statemachinename
        '''
        result = self._values.get("state_machine_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state_machine_type(self) -> typing.Optional[builtins.str]:
        '''Determines whether a ``STANDARD`` or ``EXPRESS`` state machine is created.

        The default is ``STANDARD`` . You cannot update the ``type`` of a state machine once it has been created. For more information on ``STANDARD`` and ``EXPRESS`` workflows, see `Standard Versus Express Workflows <https://docs.aws.amazon.com/step-functions/latest/dg/concepts-standard-vs-express.html>`_ in the AWS Step Functions Developer Guide.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html#cfn-stepfunctions-statemachine-statemachinetype
        '''
        result = self._values.get("state_machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(
        self,
    ) -> typing.Optional[typing.List["CfnStateMachinePropsMixin.TagsEntryProperty"]]:
        '''The list of tags to add to a resource.

        Tags may only contain Unicode letters, digits, white space, or these symbols: `_ . : / = + -

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html#cfn-stepfunctions-statemachine-tags
        :: ` .
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["CfnStateMachinePropsMixin.TagsEntryProperty"]], result)

    @builtins.property
    def tracing_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStateMachinePropsMixin.TracingConfigurationProperty"]]:
        '''Selects whether or not the state machine's AWS X-Ray tracing is enabled.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html#cfn-stepfunctions-statemachine-tracingconfiguration
        '''
        result = self._values.get("tracing_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStateMachinePropsMixin.TracingConfigurationProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStateMachineMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnStateMachinePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_stepfunctions.mixins.CfnStateMachinePropsMixin",
):
    '''Provisions a state machine.

    A state machine consists of a collection of states that can do work ( ``Task`` states), determine to which states to transition next ( ``Choice`` states), stop an execution with an error ( ``Fail`` states), and so on. State machines are specified using a JSON-based, structured language.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html
    :cloudformationResource: AWS::StepFunctions::StateMachine
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_stepfunctions import mixins as stepfunctions_mixins
        
        # definition: Any
        
        cfn_state_machine_props_mixin = stepfunctions_mixins.CfnStateMachinePropsMixin(stepfunctions_mixins.CfnStateMachineMixinProps(
            definition=definition,
            definition_s3_location=stepfunctions_mixins.CfnStateMachinePropsMixin.S3LocationProperty(
                bucket="bucket",
                key="key",
                version="version"
            ),
            definition_string="definitionString",
            definition_substitutions={
                "definition_substitutions_key": "definitionSubstitutions"
            },
            encryption_configuration=stepfunctions_mixins.CfnStateMachinePropsMixin.EncryptionConfigurationProperty(
                kms_data_key_reuse_period_seconds=123,
                kms_key_id="kmsKeyId",
                type="type"
            ),
            logging_configuration=stepfunctions_mixins.CfnStateMachinePropsMixin.LoggingConfigurationProperty(
                destinations=[stepfunctions_mixins.CfnStateMachinePropsMixin.LogDestinationProperty(
                    cloud_watch_logs_log_group=stepfunctions_mixins.CfnStateMachinePropsMixin.CloudWatchLogsLogGroupProperty(
                        log_group_arn="logGroupArn"
                    )
                )],
                include_execution_data=False,
                level="level"
            ),
            role_arn="roleArn",
            state_machine_name="stateMachineName",
            state_machine_type="stateMachineType",
            tags=[stepfunctions_mixins.CfnStateMachinePropsMixin.TagsEntryProperty(
                key="key",
                value="value"
            )],
            tracing_configuration=stepfunctions_mixins.CfnStateMachinePropsMixin.TracingConfigurationProperty(
                enabled=False
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnStateMachineMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::StepFunctions::StateMachine``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d83ec040c90c41c85f7e15278a9b36664e09e2b3183fe8530ceba95fc1a12acb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb479b3e00503f41317964fe20613b45da46558935fe3593d693e472d37adc84)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7401fa00790e6be4a5c5dcb1e572d18ca7f79e939370836d5fd7a41023c289f2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnStateMachineMixinProps:
        return typing.cast(CfnStateMachineMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_stepfunctions.mixins.CfnStateMachinePropsMixin.CloudWatchLogsLogGroupProperty",
        jsii_struct_bases=[],
        name_mapping={"log_group_arn": "logGroupArn"},
    )
    class CloudWatchLogsLogGroupProperty:
        def __init__(
            self,
            *,
            log_group_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines a CloudWatch log group.

            .. epigraph::

               For more information see `Standard Versus Express Workflows <https://docs.aws.amazon.com/step-functions/latest/dg/concepts-standard-vs-express.html>`_ in the AWS Step Functions Developer Guide.

            :param log_group_arn: The ARN of the the CloudWatch log group to which you want your logs emitted to. The ARN must end with ``:*``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-cloudwatchlogsloggroup.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_stepfunctions import mixins as stepfunctions_mixins
                
                cloud_watch_logs_log_group_property = stepfunctions_mixins.CfnStateMachinePropsMixin.CloudWatchLogsLogGroupProperty(
                    log_group_arn="logGroupArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ad2864fb3cb4b5646d70326805a39762694419674684486a4e7fa496245d2c5b)
                check_type(argname="argument log_group_arn", value=log_group_arn, expected_type=type_hints["log_group_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if log_group_arn is not None:
                self._values["log_group_arn"] = log_group_arn

        @builtins.property
        def log_group_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the the CloudWatch log group to which you want your logs emitted to.

            The ARN must end with ``:*``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-cloudwatchlogsloggroup.html#cfn-stepfunctions-statemachine-cloudwatchlogsloggroup-loggrouparn
            '''
            result = self._values.get("log_group_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchLogsLogGroupProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_stepfunctions.mixins.CfnStateMachinePropsMixin.EncryptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "kms_data_key_reuse_period_seconds": "kmsDataKeyReusePeriodSeconds",
            "kms_key_id": "kmsKeyId",
            "type": "type",
        },
    )
    class EncryptionConfigurationProperty:
        def __init__(
            self,
            *,
            kms_data_key_reuse_period_seconds: typing.Optional[jsii.Number] = None,
            kms_key_id: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Settings to configure server-side encryption for a state machine.

            By default, Step Functions provides transparent server-side encryption. With this configuration, you can specify a customer managed AWS  key for encryption.

            :param kms_data_key_reuse_period_seconds: Maximum duration that Step Functions will reuse data keys. When the period expires, Step Functions will call ``GenerateDataKey`` . Only applies to customer managed keys.
            :param kms_key_id: An alias, alias ARN, key ID, or key ARN of a symmetric encryption AWS key to encrypt data. To specify a AWS key in a different AWS account, you must use the key ARN or alias ARN.
            :param type: Encryption option for a state machine.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-encryptionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_stepfunctions import mixins as stepfunctions_mixins
                
                encryption_configuration_property = stepfunctions_mixins.CfnStateMachinePropsMixin.EncryptionConfigurationProperty(
                    kms_data_key_reuse_period_seconds=123,
                    kms_key_id="kmsKeyId",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6430b97ae25490781e163e2b4704cad16aec58f9b28140f358cbe257e9aa44ff)
                check_type(argname="argument kms_data_key_reuse_period_seconds", value=kms_data_key_reuse_period_seconds, expected_type=type_hints["kms_data_key_reuse_period_seconds"])
                check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kms_data_key_reuse_period_seconds is not None:
                self._values["kms_data_key_reuse_period_seconds"] = kms_data_key_reuse_period_seconds
            if kms_key_id is not None:
                self._values["kms_key_id"] = kms_key_id
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def kms_data_key_reuse_period_seconds(self) -> typing.Optional[jsii.Number]:
            '''Maximum duration that Step Functions will reuse data keys.

            When the period expires, Step Functions will call ``GenerateDataKey`` . Only applies to customer managed keys.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-encryptionconfiguration.html#cfn-stepfunctions-statemachine-encryptionconfiguration-kmsdatakeyreuseperiodseconds
            '''
            result = self._values.get("kms_data_key_reuse_period_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def kms_key_id(self) -> typing.Optional[builtins.str]:
            '''An alias, alias ARN, key ID, or key ARN of a symmetric encryption AWS  key to encrypt data.

            To specify a AWS  key in a different AWS account, you must use the key ARN or alias ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-encryptionconfiguration.html#cfn-stepfunctions-statemachine-encryptionconfiguration-kmskeyid
            '''
            result = self._values.get("kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''Encryption option for a state machine.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-encryptionconfiguration.html#cfn-stepfunctions-statemachine-encryptionconfiguration-type
            '''
            result = self._values.get("type")
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
        jsii_type="@aws-cdk/mixins-preview.aws_stepfunctions.mixins.CfnStateMachinePropsMixin.LogDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={"cloud_watch_logs_log_group": "cloudWatchLogsLogGroup"},
    )
    class LogDestinationProperty:
        def __init__(
            self,
            *,
            cloud_watch_logs_log_group: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStateMachinePropsMixin.CloudWatchLogsLogGroupProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Defines a destination for ``LoggingConfiguration`` .

            .. epigraph::

               For more information on logging with ``EXPRESS`` workflows, see `Logging Express Workflows Using CloudWatch Logs <https://docs.aws.amazon.com/step-functions/latest/dg/cw-logs.html>`_ .

            :param cloud_watch_logs_log_group: An object describing a CloudWatch log group. For more information, see `AWS::Logs::LogGroup <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html>`_ in the CloudFormation User Guide.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-logdestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_stepfunctions import mixins as stepfunctions_mixins
                
                log_destination_property = stepfunctions_mixins.CfnStateMachinePropsMixin.LogDestinationProperty(
                    cloud_watch_logs_log_group=stepfunctions_mixins.CfnStateMachinePropsMixin.CloudWatchLogsLogGroupProperty(
                        log_group_arn="logGroupArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bd9c1e01cd4575fc1102e846bef01df061ce45bae0262e46bc014dc487ef20cd)
                check_type(argname="argument cloud_watch_logs_log_group", value=cloud_watch_logs_log_group, expected_type=type_hints["cloud_watch_logs_log_group"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloud_watch_logs_log_group is not None:
                self._values["cloud_watch_logs_log_group"] = cloud_watch_logs_log_group

        @builtins.property
        def cloud_watch_logs_log_group(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStateMachinePropsMixin.CloudWatchLogsLogGroupProperty"]]:
            '''An object describing a CloudWatch log group.

            For more information, see `AWS::Logs::LogGroup <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html>`_ in the CloudFormation User Guide.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-logdestination.html#cfn-stepfunctions-statemachine-logdestination-cloudwatchlogsloggroup
            '''
            result = self._values.get("cloud_watch_logs_log_group")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStateMachinePropsMixin.CloudWatchLogsLogGroupProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_stepfunctions.mixins.CfnStateMachinePropsMixin.LoggingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destinations": "destinations",
            "include_execution_data": "includeExecutionData",
            "level": "level",
        },
    )
    class LoggingConfigurationProperty:
        def __init__(
            self,
            *,
            destinations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStateMachinePropsMixin.LogDestinationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            include_execution_data: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            level: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines what execution history events are logged and where they are logged.

            Step Functions provides the log levels — ``OFF`` , ``ALL`` , ``ERROR`` , and ``FATAL`` . No event types log when set to ``OFF`` and all event types do when set to ``ALL`` .
            .. epigraph::

               By default, the ``level`` is set to ``OFF`` . For more information see `Log Levels <https://docs.aws.amazon.com/step-functions/latest/dg/cloudwatch-log-level.html>`_ in the AWS Step Functions User Guide.

            :param destinations: An array of objects that describes where your execution history events will be logged. Limited to size 1. Required, if your log level is not set to ``OFF`` .
            :param include_execution_data: Determines whether execution data is included in your log. When set to ``false`` , data is excluded.
            :param level: Defines which category of execution history events are logged.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-loggingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_stepfunctions import mixins as stepfunctions_mixins
                
                logging_configuration_property = stepfunctions_mixins.CfnStateMachinePropsMixin.LoggingConfigurationProperty(
                    destinations=[stepfunctions_mixins.CfnStateMachinePropsMixin.LogDestinationProperty(
                        cloud_watch_logs_log_group=stepfunctions_mixins.CfnStateMachinePropsMixin.CloudWatchLogsLogGroupProperty(
                            log_group_arn="logGroupArn"
                        )
                    )],
                    include_execution_data=False,
                    level="level"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__164c79c6187a24733578e8baabcc5bf2cfe5226a6e0fe8c12981169e661c36b8)
                check_type(argname="argument destinations", value=destinations, expected_type=type_hints["destinations"])
                check_type(argname="argument include_execution_data", value=include_execution_data, expected_type=type_hints["include_execution_data"])
                check_type(argname="argument level", value=level, expected_type=type_hints["level"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destinations is not None:
                self._values["destinations"] = destinations
            if include_execution_data is not None:
                self._values["include_execution_data"] = include_execution_data
            if level is not None:
                self._values["level"] = level

        @builtins.property
        def destinations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStateMachinePropsMixin.LogDestinationProperty"]]]]:
            '''An array of objects that describes where your execution history events will be logged.

            Limited to size 1. Required, if your log level is not set to ``OFF`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-loggingconfiguration.html#cfn-stepfunctions-statemachine-loggingconfiguration-destinations
            '''
            result = self._values.get("destinations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStateMachinePropsMixin.LogDestinationProperty"]]]], result)

        @builtins.property
        def include_execution_data(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Determines whether execution data is included in your log.

            When set to ``false`` , data is excluded.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-loggingconfiguration.html#cfn-stepfunctions-statemachine-loggingconfiguration-includeexecutiondata
            '''
            result = self._values.get("include_execution_data")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def level(self) -> typing.Optional[builtins.str]:
            '''Defines which category of execution history events are logged.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-loggingconfiguration.html#cfn-stepfunctions-statemachine-loggingconfiguration-level
            '''
            result = self._values.get("level")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_stepfunctions.mixins.CfnStateMachinePropsMixin.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "key": "key", "version": "version"},
    )
    class S3LocationProperty:
        def __init__(
            self,
            *,
            bucket: typing.Optional[builtins.str] = None,
            key: typing.Optional[builtins.str] = None,
            version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines the S3 bucket location where a state machine definition is stored.

            The state machine definition must be a JSON or YAML file.

            :param bucket: The name of the S3 bucket where the state machine definition JSON or YAML file is stored.
            :param key: The name of the state machine definition file (Amazon S3 object name).
            :param version: For versioning-enabled buckets, a specific version of the state machine definition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-s3location.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_stepfunctions import mixins as stepfunctions_mixins
                
                s3_location_property = stepfunctions_mixins.CfnStateMachinePropsMixin.S3LocationProperty(
                    bucket="bucket",
                    key="key",
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__046339df25223caefff2eca3c6a1c06f224300c90d98f1a728b00ac57b8aa438)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket is not None:
                self._values["bucket"] = bucket
            if key is not None:
                self._values["key"] = key
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def bucket(self) -> typing.Optional[builtins.str]:
            '''The name of the S3 bucket where the state machine definition JSON or YAML file is stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-s3location.html#cfn-stepfunctions-statemachine-s3location-bucket
            '''
            result = self._values.get("bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The name of the state machine definition file (Amazon S3 object name).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-s3location.html#cfn-stepfunctions-statemachine-s3location-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''For versioning-enabled buckets, a specific version of the state machine definition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-s3location.html#cfn-stepfunctions-statemachine-s3location-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_stepfunctions.mixins.CfnStateMachinePropsMixin.TagsEntryProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TagsEntryProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``TagsEntry`` property specifies *tags* to identify a state machine.

            :param key: The ``key`` for a key-value pair in a tag entry.
            :param value: The ``value`` for a key-value pair in a tag entry.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-tagsentry.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_stepfunctions import mixins as stepfunctions_mixins
                
                tags_entry_property = stepfunctions_mixins.CfnStateMachinePropsMixin.TagsEntryProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e40b1b92423d0d105794286bf6481c9e458d9d0b996f64d4918bb3ea0f0e67bc)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The ``key`` for a key-value pair in a tag entry.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-tagsentry.html#cfn-stepfunctions-statemachine-tagsentry-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The ``value`` for a key-value pair in a tag entry.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-tagsentry.html#cfn-stepfunctions-statemachine-tagsentry-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagsEntryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_stepfunctions.mixins.CfnStateMachinePropsMixin.TracingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled"},
    )
    class TracingConfigurationProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Selects whether or not the state machine's AWS X-Ray tracing is enabled.

            To configure your state machine to send trace data to X-Ray, set ``Enabled`` to ``true`` .

            :param enabled: When set to ``true`` , X-Ray tracing is enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-tracingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_stepfunctions import mixins as stepfunctions_mixins
                
                tracing_configuration_property = stepfunctions_mixins.CfnStateMachinePropsMixin.TracingConfigurationProperty(
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b202bd56e278cbf4410b43c95ddb5ac0efa1dcfc4a1337effab8a687ac339ba8)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When set to ``true`` , X-Ray tracing is enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-tracingconfiguration.html#cfn-stepfunctions-statemachine-tracingconfiguration-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TracingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


class CfnStateMachineStandardLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_stepfunctions.mixins.CfnStateMachineStandardLogs",
):
    '''Builder for CfnStateMachineLogsMixin to generate STANDARD_LOGS for CfnStateMachine.

    :cloudformationResource: AWS::StepFunctions::StateMachine
    :logType: STANDARD_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_stepfunctions import mixins as stepfunctions_mixins
        
        cfn_state_machine_standard_logs = stepfunctions_mixins.CfnStateMachineStandardLogs()
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> CfnStateMachineLogsMixin:
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbca6b009d3838dabea6cbd5f7f76c1e346ade2d2a43f6858d0c46fa4d039a93)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast(CfnStateMachineLogsMixin, jsii.invoke(self, "toLogGroup", [log_group]))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_stepfunctions.mixins.CfnStateMachineVersionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "state_machine_arn": "stateMachineArn",
        "state_machine_revision_id": "stateMachineRevisionId",
    },
)
class CfnStateMachineVersionMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        state_machine_arn: typing.Optional[builtins.str] = None,
        state_machine_revision_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnStateMachineVersionPropsMixin.

        :param description: An optional description of the state machine version.
        :param state_machine_arn: The Amazon Resource Name (ARN) of the state machine.
        :param state_machine_revision_id: Identifier for a state machine revision, which is an immutable, read-only snapshot of a state machine’s definition and configuration. Only publish the state machine version if the current state machine's revision ID matches the specified ID. Use this option to avoid publishing a version if the state machine has changed since you last updated it. To specify the initial state machine revision, set the value as ``INITIAL`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachineversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_stepfunctions import mixins as stepfunctions_mixins
            
            cfn_state_machine_version_mixin_props = stepfunctions_mixins.CfnStateMachineVersionMixinProps(
                description="description",
                state_machine_arn="stateMachineArn",
                state_machine_revision_id="stateMachineRevisionId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc0c3061b58691a01bb7e22dac380d9d08a742bc38a85865a390659c40f92259)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument state_machine_arn", value=state_machine_arn, expected_type=type_hints["state_machine_arn"])
            check_type(argname="argument state_machine_revision_id", value=state_machine_revision_id, expected_type=type_hints["state_machine_revision_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if state_machine_arn is not None:
            self._values["state_machine_arn"] = state_machine_arn
        if state_machine_revision_id is not None:
            self._values["state_machine_revision_id"] = state_machine_revision_id

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of the state machine version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachineversion.html#cfn-stepfunctions-statemachineversion-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state_machine_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the state machine.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachineversion.html#cfn-stepfunctions-statemachineversion-statemachinearn
        '''
        result = self._values.get("state_machine_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state_machine_revision_id(self) -> typing.Optional[builtins.str]:
        '''Identifier for a state machine revision, which is an immutable, read-only snapshot of a state machine’s definition and configuration.

        Only publish the state machine version if the current state machine's revision ID matches the specified ID. Use this option to avoid publishing a version if the state machine has changed since you last updated it.

        To specify the initial state machine revision, set the value as ``INITIAL`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachineversion.html#cfn-stepfunctions-statemachineversion-statemachinerevisionid
        '''
        result = self._values.get("state_machine_revision_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStateMachineVersionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnStateMachineVersionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_stepfunctions.mixins.CfnStateMachineVersionPropsMixin",
):
    '''Represents a state machine `version <https://docs.aws.amazon.com/step-functions/latest/dg/concepts-state-machine-version.html>`_ . A published version uses the latest state machine `*revision* <https://docs.aws.amazon.com/step-functions/latest/dg/concepts-state-machine-version.html>`_ . A revision is an immutable, read-only snapshot of a state machine’s definition and configuration.

    You can publish up to 1000 versions for each state machine.
    .. epigraph::

       Before you delete a version, make sure that version's ARN isn't being referenced in any long-running workflows or application code outside of the stack.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachineversion.html
    :cloudformationResource: AWS::StepFunctions::StateMachineVersion
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_stepfunctions import mixins as stepfunctions_mixins
        
        cfn_state_machine_version_props_mixin = stepfunctions_mixins.CfnStateMachineVersionPropsMixin(stepfunctions_mixins.CfnStateMachineVersionMixinProps(
            description="description",
            state_machine_arn="stateMachineArn",
            state_machine_revision_id="stateMachineRevisionId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnStateMachineVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::StepFunctions::StateMachineVersion``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1123ae25fa8e247d344470c8cf0b238956352d8cfe06ffc3b74d1c4a0135c84e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f55fa612629107340df54d2eaaf278af55e0fe93920a9815d961ed3ba968003)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0b96d8135a1cc304f2104db2ae512b224f1ef9dd8189ba707ebd97f315135fa)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnStateMachineVersionMixinProps:
        return typing.cast(CfnStateMachineVersionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnActivityMixinProps",
    "CfnActivityPropsMixin",
    "CfnStateMachineAliasMixinProps",
    "CfnStateMachineAliasPropsMixin",
    "CfnStateMachineExpressLogs",
    "CfnStateMachineLogsMixin",
    "CfnStateMachineMixinProps",
    "CfnStateMachinePropsMixin",
    "CfnStateMachineStandardLogs",
    "CfnStateMachineVersionMixinProps",
    "CfnStateMachineVersionPropsMixin",
]

publication.publish()

def _typecheckingstub__819ed25a8b7de45e6eda4dd6744d7fc912e2afb427c8e3a9ab55264d259fc60f(
    *,
    encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnActivityPropsMixin.EncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnActivityPropsMixin.TagsEntryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f0f4283ba9c37c36e33c5ed6f60c78cb98c17d0f6909c564310b835cf6c6271(
    props: typing.Union[CfnActivityMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__655a11b296cd2b3fd72449398b5ec131ea10f6f9bcdb3282eb4fbd90c14f0b9c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd4d60fdb57c0b6e7d0178ec5f8af0cbc45e9448d5f8c3610789b8b2a5e746c9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36b1c05ac6b10d614f6180f0a35a52acc01fb3e9ae65630da80b9296b9b957c8(
    *,
    kms_data_key_reuse_period_seconds: typing.Optional[jsii.Number] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__476f58636160fd4a6a8cc1615f6704106b89a48fc1d9154280c3f2dafc2fbda4(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de64f90980360154d77cab303a7e0ec9c981c1ae7b39627457747056a78217c2(
    *,
    deployment_preference: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStateMachineAliasPropsMixin.DeploymentPreferenceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    routing_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStateMachineAliasPropsMixin.RoutingConfigurationVersionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a74842a5c5fee0aebfe74930fc111ab9eabdd43c1db765695c352149d02ac113(
    props: typing.Union[CfnStateMachineAliasMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b934c04f2c519d2549e608617e079bb51b22d52b042b9e2fb9d01edde8d6fe8f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aa8fc54ab1f13b648998ac52396362066ce3a3e2903056a0df9b0b628a5e9d3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03c55a442cbadfbe37a8c0c6e2350cdd77bb36e934a6e077971ba080e0e05ddd(
    *,
    alarms: typing.Optional[typing.Sequence[builtins.str]] = None,
    interval: typing.Optional[jsii.Number] = None,
    percentage: typing.Optional[jsii.Number] = None,
    state_machine_version_arn: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bda252c72eef87ff6379599fd98c1071dfde8ce8a15bc658b7308c3095033cc4(
    *,
    state_machine_version_arn: typing.Optional[builtins.str] = None,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a7c1718a2764a6832854b3071fef98f9d8e965ebd36a4f369a3cedaa953e7b0(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b3a34dcdb545059f78345b115ad4dfe2413a98ee45ea5393ff3cfaf2e8b513e(
    log_type: builtins.str,
    log_delivery: _ILogsDelivery_0d3c9e29,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e37c0611dd50ea0c45d059142de43141228e4fb18815146a81b766cd20b1fade(
    resource: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb1f5c0ad06c62110858ede307dc71574289f36b2977d7855936e4928820909e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f2726973acc336ef70783184ea0ab5b637fee156377224526a2c139d8ab4abe(
    *,
    definition: typing.Any = None,
    definition_s3_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStateMachinePropsMixin.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    definition_string: typing.Optional[builtins.str] = None,
    definition_substitutions: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStateMachinePropsMixin.EncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    logging_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStateMachinePropsMixin.LoggingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    role_arn: typing.Optional[builtins.str] = None,
    state_machine_name: typing.Optional[builtins.str] = None,
    state_machine_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnStateMachinePropsMixin.TagsEntryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tracing_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStateMachinePropsMixin.TracingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d83ec040c90c41c85f7e15278a9b36664e09e2b3183fe8530ceba95fc1a12acb(
    props: typing.Union[CfnStateMachineMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb479b3e00503f41317964fe20613b45da46558935fe3593d693e472d37adc84(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7401fa00790e6be4a5c5dcb1e572d18ca7f79e939370836d5fd7a41023c289f2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad2864fb3cb4b5646d70326805a39762694419674684486a4e7fa496245d2c5b(
    *,
    log_group_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6430b97ae25490781e163e2b4704cad16aec58f9b28140f358cbe257e9aa44ff(
    *,
    kms_data_key_reuse_period_seconds: typing.Optional[jsii.Number] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd9c1e01cd4575fc1102e846bef01df061ce45bae0262e46bc014dc487ef20cd(
    *,
    cloud_watch_logs_log_group: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStateMachinePropsMixin.CloudWatchLogsLogGroupProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__164c79c6187a24733578e8baabcc5bf2cfe5226a6e0fe8c12981169e661c36b8(
    *,
    destinations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStateMachinePropsMixin.LogDestinationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    include_execution_data: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    level: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__046339df25223caefff2eca3c6a1c06f224300c90d98f1a728b00ac57b8aa438(
    *,
    bucket: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e40b1b92423d0d105794286bf6481c9e458d9d0b996f64d4918bb3ea0f0e67bc(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b202bd56e278cbf4410b43c95ddb5ac0efa1dcfc4a1337effab8a687ac339ba8(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbca6b009d3838dabea6cbd5f7f76c1e346ade2d2a43f6858d0c46fa4d039a93(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc0c3061b58691a01bb7e22dac380d9d08a742bc38a85865a390659c40f92259(
    *,
    description: typing.Optional[builtins.str] = None,
    state_machine_arn: typing.Optional[builtins.str] = None,
    state_machine_revision_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1123ae25fa8e247d344470c8cf0b238956352d8cfe06ffc3b74d1c4a0135c84e(
    props: typing.Union[CfnStateMachineVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f55fa612629107340df54d2eaaf278af55e0fe93920a9815d961ed3ba968003(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0b96d8135a1cc304f2104db2ae512b224f1ef9dd8189ba707ebd97f315135fa(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
