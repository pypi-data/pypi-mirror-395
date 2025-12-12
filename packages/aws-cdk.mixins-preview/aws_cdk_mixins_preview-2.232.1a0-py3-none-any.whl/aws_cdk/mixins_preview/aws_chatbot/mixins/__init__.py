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
    jsii_type="@aws-cdk/mixins-preview.aws_chatbot.mixins.CfnCustomActionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "action_name": "actionName",
        "alias_name": "aliasName",
        "attachments": "attachments",
        "definition": "definition",
        "tags": "tags",
    },
)
class CfnCustomActionMixinProps:
    def __init__(
        self,
        *,
        action_name: typing.Optional[builtins.str] = None,
        alias_name: typing.Optional[builtins.str] = None,
        attachments: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCustomActionPropsMixin.CustomActionAttachmentProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        definition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCustomActionPropsMixin.CustomActionDefinitionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnCustomActionPropsMixin.

        :param action_name: The name of the custom action. This name is included in the Amazon Resource Name (ARN).
        :param alias_name: The name used to invoke this action in a chat channel. For example, ``@Amazon Q run my-alias`` .
        :param attachments: Defines when this custom action button should be attached to a notification.
        :param definition: The definition of the command to run when invoked as an alias or as an action button.
        :param tags: The tags to add to the configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-customaction.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_chatbot import mixins as chatbot_mixins
            
            cfn_custom_action_mixin_props = chatbot_mixins.CfnCustomActionMixinProps(
                action_name="actionName",
                alias_name="aliasName",
                attachments=[chatbot_mixins.CfnCustomActionPropsMixin.CustomActionAttachmentProperty(
                    button_text="buttonText",
                    criteria=[chatbot_mixins.CfnCustomActionPropsMixin.CustomActionAttachmentCriteriaProperty(
                        operator="operator",
                        value="value",
                        variable_name="variableName"
                    )],
                    notification_type="notificationType",
                    variables={
                        "variables_key": "variables"
                    }
                )],
                definition=chatbot_mixins.CfnCustomActionPropsMixin.CustomActionDefinitionProperty(
                    command_text="commandText"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94089542dd44ae5108337e861ea3ad42df6842a467488ff46edd9acb3c16b8f9)
            check_type(argname="argument action_name", value=action_name, expected_type=type_hints["action_name"])
            check_type(argname="argument alias_name", value=alias_name, expected_type=type_hints["alias_name"])
            check_type(argname="argument attachments", value=attachments, expected_type=type_hints["attachments"])
            check_type(argname="argument definition", value=definition, expected_type=type_hints["definition"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action_name is not None:
            self._values["action_name"] = action_name
        if alias_name is not None:
            self._values["alias_name"] = alias_name
        if attachments is not None:
            self._values["attachments"] = attachments
        if definition is not None:
            self._values["definition"] = definition
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def action_name(self) -> typing.Optional[builtins.str]:
        '''The name of the custom action.

        This name is included in the Amazon Resource Name (ARN).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-customaction.html#cfn-chatbot-customaction-actionname
        '''
        result = self._values.get("action_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alias_name(self) -> typing.Optional[builtins.str]:
        '''The name used to invoke this action in a chat channel.

        For example, ``@Amazon Q run my-alias`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-customaction.html#cfn-chatbot-customaction-aliasname
        '''
        result = self._values.get("alias_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def attachments(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCustomActionPropsMixin.CustomActionAttachmentProperty"]]]]:
        '''Defines when this custom action button should be attached to a notification.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-customaction.html#cfn-chatbot-customaction-attachments
        '''
        result = self._values.get("attachments")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCustomActionPropsMixin.CustomActionAttachmentProperty"]]]], result)

    @builtins.property
    def definition(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCustomActionPropsMixin.CustomActionDefinitionProperty"]]:
        '''The definition of the command to run when invoked as an alias or as an action button.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-customaction.html#cfn-chatbot-customaction-definition
        '''
        result = self._values.get("definition")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCustomActionPropsMixin.CustomActionDefinitionProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags to add to the configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-customaction.html#cfn-chatbot-customaction-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCustomActionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnCustomActionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_chatbot.mixins.CfnCustomActionPropsMixin",
):
    '''.. epigraph::

   AWS Chatbot is now  .

    `Learn more <https://docs.aws.amazon.com//chatbot/latest/adminguide/service-rename.html>`_
    .. epigraph::

       ``Type`` attribute values remain unchanged.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-customaction.html
    :cloudformationResource: AWS::Chatbot::CustomAction
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_chatbot import mixins as chatbot_mixins
        
        cfn_custom_action_props_mixin = chatbot_mixins.CfnCustomActionPropsMixin(chatbot_mixins.CfnCustomActionMixinProps(
            action_name="actionName",
            alias_name="aliasName",
            attachments=[chatbot_mixins.CfnCustomActionPropsMixin.CustomActionAttachmentProperty(
                button_text="buttonText",
                criteria=[chatbot_mixins.CfnCustomActionPropsMixin.CustomActionAttachmentCriteriaProperty(
                    operator="operator",
                    value="value",
                    variable_name="variableName"
                )],
                notification_type="notificationType",
                variables={
                    "variables_key": "variables"
                }
            )],
            definition=chatbot_mixins.CfnCustomActionPropsMixin.CustomActionDefinitionProperty(
                command_text="commandText"
            ),
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
        props: typing.Union[CfnCustomActionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Chatbot::CustomAction``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b655f23a21db6c37e5f1e30a8c73677a1b72706fd134b0687de45744e251e061)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e005835297a92f5f0c27fb43aa1098eb4c82aeb0bba208e99eae2c25149f562)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ac6ccb32fbaefd319841ef7892335bdbcefa5c37ae6f848831149d0e61d677b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnCustomActionMixinProps:
        return typing.cast(CfnCustomActionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_chatbot.mixins.CfnCustomActionPropsMixin.CustomActionAttachmentCriteriaProperty",
        jsii_struct_bases=[],
        name_mapping={
            "operator": "operator",
            "value": "value",
            "variable_name": "variableName",
        },
    )
    class CustomActionAttachmentCriteriaProperty:
        def __init__(
            self,
            *,
            operator: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
            variable_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''.. epigraph::

   AWS Chatbot is now  . `Learn more <https://docs.aws.amazon.com//chatbot/latest/adminguide/service-rename.html>`_ >  > ``Type`` attribute values remain unchanged.

            A criteria for when a button should be shown based on values in the notification.

            :param operator: The operation to perform on the named variable.
            :param value: A value that is compared with the actual value of the variable based on the behavior of the operator.
            :param variable_name: The name of the variable to operate on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-chatbot-customaction-customactionattachmentcriteria.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_chatbot import mixins as chatbot_mixins
                
                custom_action_attachment_criteria_property = chatbot_mixins.CfnCustomActionPropsMixin.CustomActionAttachmentCriteriaProperty(
                    operator="operator",
                    value="value",
                    variable_name="variableName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__05a9833c8e2a0001a4e1de9ef53287aa69c394662ffec02e1894c79d09dbf1ab)
                check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
                check_type(argname="argument variable_name", value=variable_name, expected_type=type_hints["variable_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if operator is not None:
                self._values["operator"] = operator
            if value is not None:
                self._values["value"] = value
            if variable_name is not None:
                self._values["variable_name"] = variable_name

        @builtins.property
        def operator(self) -> typing.Optional[builtins.str]:
            '''The operation to perform on the named variable.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-chatbot-customaction-customactionattachmentcriteria.html#cfn-chatbot-customaction-customactionattachmentcriteria-operator
            '''
            result = self._values.get("operator")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''A value that is compared with the actual value of the variable based on the behavior of the operator.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-chatbot-customaction-customactionattachmentcriteria.html#cfn-chatbot-customaction-customactionattachmentcriteria-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def variable_name(self) -> typing.Optional[builtins.str]:
            '''The name of the variable to operate on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-chatbot-customaction-customactionattachmentcriteria.html#cfn-chatbot-customaction-customactionattachmentcriteria-variablename
            '''
            result = self._values.get("variable_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomActionAttachmentCriteriaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_chatbot.mixins.CfnCustomActionPropsMixin.CustomActionAttachmentProperty",
        jsii_struct_bases=[],
        name_mapping={
            "button_text": "buttonText",
            "criteria": "criteria",
            "notification_type": "notificationType",
            "variables": "variables",
        },
    )
    class CustomActionAttachmentProperty:
        def __init__(
            self,
            *,
            button_text: typing.Optional[builtins.str] = None,
            criteria: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCustomActionPropsMixin.CustomActionAttachmentCriteriaProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            notification_type: typing.Optional[builtins.str] = None,
            variables: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''.. epigraph::

   AWS Chatbot is now  . `Learn more <https://docs.aws.amazon.com//chatbot/latest/adminguide/service-rename.html>`_ >  > ``Type`` attribute values remain unchanged.

            Defines when a custom action button should be attached to a notification.

            :param button_text: The text of the button that appears on the notification.
            :param criteria: The criteria for when a button should be shown based on values in the notification.
            :param notification_type: The type of notification that the custom action should be attached to.
            :param variables: The variables to extract from the notification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-chatbot-customaction-customactionattachment.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_chatbot import mixins as chatbot_mixins
                
                custom_action_attachment_property = chatbot_mixins.CfnCustomActionPropsMixin.CustomActionAttachmentProperty(
                    button_text="buttonText",
                    criteria=[chatbot_mixins.CfnCustomActionPropsMixin.CustomActionAttachmentCriteriaProperty(
                        operator="operator",
                        value="value",
                        variable_name="variableName"
                    )],
                    notification_type="notificationType",
                    variables={
                        "variables_key": "variables"
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4442eeb685a4ad1dc0ad0dc57afbba6266deedb269360c0380bf08029e916f26)
                check_type(argname="argument button_text", value=button_text, expected_type=type_hints["button_text"])
                check_type(argname="argument criteria", value=criteria, expected_type=type_hints["criteria"])
                check_type(argname="argument notification_type", value=notification_type, expected_type=type_hints["notification_type"])
                check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if button_text is not None:
                self._values["button_text"] = button_text
            if criteria is not None:
                self._values["criteria"] = criteria
            if notification_type is not None:
                self._values["notification_type"] = notification_type
            if variables is not None:
                self._values["variables"] = variables

        @builtins.property
        def button_text(self) -> typing.Optional[builtins.str]:
            '''The text of the button that appears on the notification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-chatbot-customaction-customactionattachment.html#cfn-chatbot-customaction-customactionattachment-buttontext
            '''
            result = self._values.get("button_text")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def criteria(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCustomActionPropsMixin.CustomActionAttachmentCriteriaProperty"]]]]:
            '''The criteria for when a button should be shown based on values in the notification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-chatbot-customaction-customactionattachment.html#cfn-chatbot-customaction-customactionattachment-criteria
            '''
            result = self._values.get("criteria")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCustomActionPropsMixin.CustomActionAttachmentCriteriaProperty"]]]], result)

        @builtins.property
        def notification_type(self) -> typing.Optional[builtins.str]:
            '''The type of notification that the custom action should be attached to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-chatbot-customaction-customactionattachment.html#cfn-chatbot-customaction-customactionattachment-notificationtype
            '''
            result = self._values.get("notification_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def variables(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''The variables to extract from the notification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-chatbot-customaction-customactionattachment.html#cfn-chatbot-customaction-customactionattachment-variables
            '''
            result = self._values.get("variables")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomActionAttachmentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_chatbot.mixins.CfnCustomActionPropsMixin.CustomActionDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={"command_text": "commandText"},
    )
    class CustomActionDefinitionProperty:
        def __init__(
            self,
            *,
            command_text: typing.Optional[builtins.str] = None,
        ) -> None:
            '''.. epigraph::

   AWS Chatbot is now  . `Learn more <https://docs.aws.amazon.com//chatbot/latest/adminguide/service-rename.html>`_ >  > ``Type`` attribute values remain unchanged.

            The definition of the command to run when invoked as an alias or as an action button.

            :param command_text: The command string to run which may include variables by prefixing with a dollar sign ($).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-chatbot-customaction-customactiondefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_chatbot import mixins as chatbot_mixins
                
                custom_action_definition_property = chatbot_mixins.CfnCustomActionPropsMixin.CustomActionDefinitionProperty(
                    command_text="commandText"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__77da1385d4f7f49a809850dd72a1c7aad4cbf01bf303c3a3d99a5cb4320c0cb4)
                check_type(argname="argument command_text", value=command_text, expected_type=type_hints["command_text"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if command_text is not None:
                self._values["command_text"] = command_text

        @builtins.property
        def command_text(self) -> typing.Optional[builtins.str]:
            '''The command string to run which may include variables by prefixing with a dollar sign ($).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-chatbot-customaction-customactiondefinition.html#cfn-chatbot-customaction-customactiondefinition-commandtext
            '''
            result = self._values.get("command_text")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomActionDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_chatbot.mixins.CfnMicrosoftTeamsChannelConfigurationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "configuration_name": "configurationName",
        "customization_resource_arns": "customizationResourceArns",
        "guardrail_policies": "guardrailPolicies",
        "iam_role_arn": "iamRoleArn",
        "logging_level": "loggingLevel",
        "sns_topic_arns": "snsTopicArns",
        "tags": "tags",
        "team_id": "teamId",
        "teams_channel_id": "teamsChannelId",
        "teams_channel_name": "teamsChannelName",
        "teams_tenant_id": "teamsTenantId",
        "user_role_required": "userRoleRequired",
    },
)
class CfnMicrosoftTeamsChannelConfigurationMixinProps:
    def __init__(
        self,
        *,
        configuration_name: typing.Optional[builtins.str] = None,
        customization_resource_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        guardrail_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
        iam_role_arn: typing.Optional[builtins.str] = None,
        logging_level: typing.Optional[builtins.str] = None,
        sns_topic_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        team_id: typing.Optional[builtins.str] = None,
        teams_channel_id: typing.Optional[builtins.str] = None,
        teams_channel_name: typing.Optional[builtins.str] = None,
        teams_tenant_id: typing.Optional[builtins.str] = None,
        user_role_required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    ) -> None:
        '''Properties for CfnMicrosoftTeamsChannelConfigurationPropsMixin.

        :param configuration_name: The name of the configuration.
        :param customization_resource_arns: Links a list of resource ARNs (for example, custom action ARNs) to a Microsoft Teams channel configuration for .
        :param guardrail_policies: The list of IAM policy ARNs that are applied as channel guardrails. The AWS managed 'AdministratorAccess' policy is applied as a default if this is not set.
        :param iam_role_arn: The ARN of the IAM role that defines the permissions for . This is a user-defined role that will assume. This is not the service-linked role. For more information, see `IAM Policies for in chat applications <https://docs.aws.amazon.com/chatbot/latest/adminguide/chatbot-iam-policies.html>`_ .
        :param logging_level: Specifies the logging level for this configuration. This property affects the log entries pushed to Amazon CloudWatch Logs. Logging levels include ``ERROR`` , ``INFO`` , or ``NONE`` . Default: - "NONE"
        :param sns_topic_arns: The ARNs of the SNS topics that deliver notifications to .
        :param tags: The tags to add to the configuration.
        :param team_id: The ID of the Microsoft Team authorized with . To get the team ID, you must perform the initial authorization flow with Microsoft Teams in the in chat applications console. Then you can copy and paste the team ID from the console. For more details, see steps 1-3 in `Tutorial: Get started with Microsoft Teams <https://docs.aws.amazon.com/chatbot/latest/adminguide/teams-setup.html>`_ in the *in chat applications Administrator Guide* .
        :param teams_channel_id: The ID of the Microsoft Teams channel. To get the channel ID, open Microsoft Teams, right click on the channel name in the left pane, then choose *Copy* . An example of the channel ID syntax is: ``19%3ab6ef35dc342d56ba5654e6fc6d25a071%40thread.tacv2`` .
        :param teams_channel_name: The name of the Microsoft Teams channel.
        :param teams_tenant_id: The ID of the Microsoft Teams tenant. To get the tenant ID, you must perform the initial authorization flow with Microsoft Teams in the in chat applications console. Then you can copy and paste the tenant ID from the console. For more details, see steps 1-3 in `Tutorial: Get started with Microsoft Teams <https://docs.aws.amazon.com/chatbot/latest/adminguide/teams-setup.html>`_ in the *in chat applications Administrator Guide* .
        :param user_role_required: Enables use of a user role requirement in your chat configuration. Default: - false

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-microsoftteamschannelconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_chatbot import mixins as chatbot_mixins
            
            cfn_microsoft_teams_channel_configuration_mixin_props = chatbot_mixins.CfnMicrosoftTeamsChannelConfigurationMixinProps(
                configuration_name="configurationName",
                customization_resource_arns=["customizationResourceArns"],
                guardrail_policies=["guardrailPolicies"],
                iam_role_arn="iamRoleArn",
                logging_level="loggingLevel",
                sns_topic_arns=["snsTopicArns"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                team_id="teamId",
                teams_channel_id="teamsChannelId",
                teams_channel_name="teamsChannelName",
                teams_tenant_id="teamsTenantId",
                user_role_required=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd397887e26a05eb089e6c881edfc4ac5e095b2b8795901d32786253d31b2685)
            check_type(argname="argument configuration_name", value=configuration_name, expected_type=type_hints["configuration_name"])
            check_type(argname="argument customization_resource_arns", value=customization_resource_arns, expected_type=type_hints["customization_resource_arns"])
            check_type(argname="argument guardrail_policies", value=guardrail_policies, expected_type=type_hints["guardrail_policies"])
            check_type(argname="argument iam_role_arn", value=iam_role_arn, expected_type=type_hints["iam_role_arn"])
            check_type(argname="argument logging_level", value=logging_level, expected_type=type_hints["logging_level"])
            check_type(argname="argument sns_topic_arns", value=sns_topic_arns, expected_type=type_hints["sns_topic_arns"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument team_id", value=team_id, expected_type=type_hints["team_id"])
            check_type(argname="argument teams_channel_id", value=teams_channel_id, expected_type=type_hints["teams_channel_id"])
            check_type(argname="argument teams_channel_name", value=teams_channel_name, expected_type=type_hints["teams_channel_name"])
            check_type(argname="argument teams_tenant_id", value=teams_tenant_id, expected_type=type_hints["teams_tenant_id"])
            check_type(argname="argument user_role_required", value=user_role_required, expected_type=type_hints["user_role_required"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if configuration_name is not None:
            self._values["configuration_name"] = configuration_name
        if customization_resource_arns is not None:
            self._values["customization_resource_arns"] = customization_resource_arns
        if guardrail_policies is not None:
            self._values["guardrail_policies"] = guardrail_policies
        if iam_role_arn is not None:
            self._values["iam_role_arn"] = iam_role_arn
        if logging_level is not None:
            self._values["logging_level"] = logging_level
        if sns_topic_arns is not None:
            self._values["sns_topic_arns"] = sns_topic_arns
        if tags is not None:
            self._values["tags"] = tags
        if team_id is not None:
            self._values["team_id"] = team_id
        if teams_channel_id is not None:
            self._values["teams_channel_id"] = teams_channel_id
        if teams_channel_name is not None:
            self._values["teams_channel_name"] = teams_channel_name
        if teams_tenant_id is not None:
            self._values["teams_tenant_id"] = teams_tenant_id
        if user_role_required is not None:
            self._values["user_role_required"] = user_role_required

    @builtins.property
    def configuration_name(self) -> typing.Optional[builtins.str]:
        '''The name of the configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-microsoftteamschannelconfiguration.html#cfn-chatbot-microsoftteamschannelconfiguration-configurationname
        '''
        result = self._values.get("configuration_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def customization_resource_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Links a list of resource ARNs (for example, custom action ARNs) to a Microsoft Teams channel configuration for  .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-microsoftteamschannelconfiguration.html#cfn-chatbot-microsoftteamschannelconfiguration-customizationresourcearns
        '''
        result = self._values.get("customization_resource_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def guardrail_policies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of IAM policy ARNs that are applied as channel guardrails.

        The AWS managed 'AdministratorAccess' policy is applied as a default if this is not set.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-microsoftteamschannelconfiguration.html#cfn-chatbot-microsoftteamschannelconfiguration-guardrailpolicies
        '''
        result = self._values.get("guardrail_policies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def iam_role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the IAM role that defines the permissions for  .

        This is a user-defined role that  will assume. This is not the service-linked role. For more information, see `IAM Policies for  in chat applications <https://docs.aws.amazon.com/chatbot/latest/adminguide/chatbot-iam-policies.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-microsoftteamschannelconfiguration.html#cfn-chatbot-microsoftteamschannelconfiguration-iamrolearn
        '''
        result = self._values.get("iam_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_level(self) -> typing.Optional[builtins.str]:
        '''Specifies the logging level for this configuration. This property affects the log entries pushed to Amazon CloudWatch Logs.

        Logging levels include ``ERROR`` , ``INFO`` , or ``NONE`` .

        :default: - "NONE"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-microsoftteamschannelconfiguration.html#cfn-chatbot-microsoftteamschannelconfiguration-logginglevel
        '''
        result = self._values.get("logging_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sns_topic_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The ARNs of the SNS topics that deliver notifications to  .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-microsoftteamschannelconfiguration.html#cfn-chatbot-microsoftteamschannelconfiguration-snstopicarns
        '''
        result = self._values.get("sns_topic_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags to add to the configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-microsoftteamschannelconfiguration.html#cfn-chatbot-microsoftteamschannelconfiguration-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def team_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the Microsoft Team authorized with  .

        To get the team ID, you must perform the initial authorization flow with Microsoft Teams in the  in chat applications console. Then you can copy and paste the team ID from the console. For more details, see steps 1-3 in `Tutorial: Get started with Microsoft Teams <https://docs.aws.amazon.com/chatbot/latest/adminguide/teams-setup.html>`_ in the *in chat applications Administrator Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-microsoftteamschannelconfiguration.html#cfn-chatbot-microsoftteamschannelconfiguration-teamid
        '''
        result = self._values.get("team_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def teams_channel_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the Microsoft Teams channel.

        To get the channel ID, open Microsoft Teams, right click on the channel name in the left pane, then choose *Copy* . An example of the channel ID syntax is: ``19%3ab6ef35dc342d56ba5654e6fc6d25a071%40thread.tacv2`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-microsoftteamschannelconfiguration.html#cfn-chatbot-microsoftteamschannelconfiguration-teamschannelid
        '''
        result = self._values.get("teams_channel_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def teams_channel_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Microsoft Teams channel.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-microsoftteamschannelconfiguration.html#cfn-chatbot-microsoftteamschannelconfiguration-teamschannelname
        '''
        result = self._values.get("teams_channel_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def teams_tenant_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the Microsoft Teams tenant.

        To get the tenant ID, you must perform the initial authorization flow with Microsoft Teams in the  in chat applications console. Then you can copy and paste the tenant ID from the console. For more details, see steps 1-3 in `Tutorial: Get started with Microsoft Teams <https://docs.aws.amazon.com/chatbot/latest/adminguide/teams-setup.html>`_ in the *in chat applications Administrator Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-microsoftteamschannelconfiguration.html#cfn-chatbot-microsoftteamschannelconfiguration-teamstenantid
        '''
        result = self._values.get("teams_tenant_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_role_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Enables use of a user role requirement in your chat configuration.

        :default: - false

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-microsoftteamschannelconfiguration.html#cfn-chatbot-microsoftteamschannelconfiguration-userrolerequired
        '''
        result = self._values.get("user_role_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMicrosoftTeamsChannelConfigurationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnMicrosoftTeamsChannelConfigurationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_chatbot.mixins.CfnMicrosoftTeamsChannelConfigurationPropsMixin",
):
    '''.. epigraph::

   AWS Chatbot is now  . `Learn more <https://docs.aws.amazon.com//chatbot/latest/adminguide/service-rename.html>`_ >  > ``Type`` attribute values remain unchanged.

    The ``AWS::Chatbot::MicrosoftTeamsChannelConfiguration`` resource configures a Microsoft Teams channel to allow users to use  with CloudFormation templates.

    This resource requires some setup to be done in the  in chat applications console. To provide the required Microsoft Teams team and tenant IDs, you must perform the initial authorization flow with Microsoft Teams in the  in chat applications console, then copy and paste the IDs from the console. For more details, see steps 1-3 in `Get started with Microsoft Teams <https://docs.aws.amazon.com/chatbot/latest/adminguide/teams-setup.html#teams-client-setup>`_ in the *in chat applications Administrator Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-microsoftteamschannelconfiguration.html
    :cloudformationResource: AWS::Chatbot::MicrosoftTeamsChannelConfiguration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_chatbot import mixins as chatbot_mixins
        
        cfn_microsoft_teams_channel_configuration_props_mixin = chatbot_mixins.CfnMicrosoftTeamsChannelConfigurationPropsMixin(chatbot_mixins.CfnMicrosoftTeamsChannelConfigurationMixinProps(
            configuration_name="configurationName",
            customization_resource_arns=["customizationResourceArns"],
            guardrail_policies=["guardrailPolicies"],
            iam_role_arn="iamRoleArn",
            logging_level="loggingLevel",
            sns_topic_arns=["snsTopicArns"],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            team_id="teamId",
            teams_channel_id="teamsChannelId",
            teams_channel_name="teamsChannelName",
            teams_tenant_id="teamsTenantId",
            user_role_required=False
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnMicrosoftTeamsChannelConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Chatbot::MicrosoftTeamsChannelConfiguration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95cd3eecf32bb85ccff41ab80c56297031c1d57a9b8479bf23cc8d0879dc464a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd26c5de1a4e4a88abbe5494e643a244e46318d26985eb24ce6d830c78c4c003)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f88aab6640074ec0917314b05f522b2bb8ec09b24b05e3e8f3d65d8afa1c224)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnMicrosoftTeamsChannelConfigurationMixinProps:
        return typing.cast(CfnMicrosoftTeamsChannelConfigurationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_chatbot.mixins.CfnSlackChannelConfigurationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "configuration_name": "configurationName",
        "customization_resource_arns": "customizationResourceArns",
        "guardrail_policies": "guardrailPolicies",
        "iam_role_arn": "iamRoleArn",
        "logging_level": "loggingLevel",
        "slack_channel_id": "slackChannelId",
        "slack_workspace_id": "slackWorkspaceId",
        "sns_topic_arns": "snsTopicArns",
        "tags": "tags",
        "user_role_required": "userRoleRequired",
    },
)
class CfnSlackChannelConfigurationMixinProps:
    def __init__(
        self,
        *,
        configuration_name: typing.Optional[builtins.str] = None,
        customization_resource_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        guardrail_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
        iam_role_arn: typing.Optional[builtins.str] = None,
        logging_level: typing.Optional[builtins.str] = None,
        slack_channel_id: typing.Optional[builtins.str] = None,
        slack_workspace_id: typing.Optional[builtins.str] = None,
        sns_topic_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        user_role_required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    ) -> None:
        '''Properties for CfnSlackChannelConfigurationPropsMixin.

        :param configuration_name: The name of the configuration.
        :param customization_resource_arns: Links a list of resource ARNs (for example, custom action ARNs) to a Slack channel configuration for .
        :param guardrail_policies: The list of IAM policy ARNs that are applied as channel guardrails. The AWS managed 'AdministratorAccess' policy is applied as a default if this is not set.
        :param iam_role_arn: The ARN of the IAM role that defines the permissions for . This is a user-defined role that will assume. This is not the service-linked role. For more information, see `IAM Policies for in chat applications <https://docs.aws.amazon.com/chatbot/latest/adminguide/chatbot-iam-policies.html>`_ .
        :param logging_level: Specifies the logging level for this configuration. This property affects the log entries pushed to Amazon CloudWatch Logs. Logging levels include ``ERROR`` , ``INFO`` , or ``NONE`` . Default: - "NONE"
        :param slack_channel_id: The ID of the Slack channel. To get the ID, open Slack, right click on the channel name in the left pane, then choose Copy Link. The channel ID is the character string at the end of the URL. For example, ``ABCBBLZZZ`` .
        :param slack_workspace_id: The ID of the Slack workspace authorized with . To get the workspace ID, you must perform the initial authorization flow with Slack in the in chat applications console. Then you can copy and paste the workspace ID from the console. For more details, see steps 1-3 in `Tutorial: Get started with Slack <https://docs.aws.amazon.com/chatbot/latest/adminguide/slack-setup.html#slack-client-setup>`_ in the *in chat applications User Guide* .
        :param sns_topic_arns: The ARNs of the SNS topics that deliver notifications to .
        :param tags: The tags to add to the configuration.
        :param user_role_required: Enables use of a user role requirement in your chat configuration. Default: - false

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_chatbot import mixins as chatbot_mixins
            
            cfn_slack_channel_configuration_mixin_props = chatbot_mixins.CfnSlackChannelConfigurationMixinProps(
                configuration_name="configurationName",
                customization_resource_arns=["customizationResourceArns"],
                guardrail_policies=["guardrailPolicies"],
                iam_role_arn="iamRoleArn",
                logging_level="loggingLevel",
                slack_channel_id="slackChannelId",
                slack_workspace_id="slackWorkspaceId",
                sns_topic_arns=["snsTopicArns"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                user_role_required=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b56407e23397623cd43ae3adb8da84a15e3a3d7b42297f24e4ca4e549eeba647)
            check_type(argname="argument configuration_name", value=configuration_name, expected_type=type_hints["configuration_name"])
            check_type(argname="argument customization_resource_arns", value=customization_resource_arns, expected_type=type_hints["customization_resource_arns"])
            check_type(argname="argument guardrail_policies", value=guardrail_policies, expected_type=type_hints["guardrail_policies"])
            check_type(argname="argument iam_role_arn", value=iam_role_arn, expected_type=type_hints["iam_role_arn"])
            check_type(argname="argument logging_level", value=logging_level, expected_type=type_hints["logging_level"])
            check_type(argname="argument slack_channel_id", value=slack_channel_id, expected_type=type_hints["slack_channel_id"])
            check_type(argname="argument slack_workspace_id", value=slack_workspace_id, expected_type=type_hints["slack_workspace_id"])
            check_type(argname="argument sns_topic_arns", value=sns_topic_arns, expected_type=type_hints["sns_topic_arns"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument user_role_required", value=user_role_required, expected_type=type_hints["user_role_required"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if configuration_name is not None:
            self._values["configuration_name"] = configuration_name
        if customization_resource_arns is not None:
            self._values["customization_resource_arns"] = customization_resource_arns
        if guardrail_policies is not None:
            self._values["guardrail_policies"] = guardrail_policies
        if iam_role_arn is not None:
            self._values["iam_role_arn"] = iam_role_arn
        if logging_level is not None:
            self._values["logging_level"] = logging_level
        if slack_channel_id is not None:
            self._values["slack_channel_id"] = slack_channel_id
        if slack_workspace_id is not None:
            self._values["slack_workspace_id"] = slack_workspace_id
        if sns_topic_arns is not None:
            self._values["sns_topic_arns"] = sns_topic_arns
        if tags is not None:
            self._values["tags"] = tags
        if user_role_required is not None:
            self._values["user_role_required"] = user_role_required

    @builtins.property
    def configuration_name(self) -> typing.Optional[builtins.str]:
        '''The name of the configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-configurationname
        '''
        result = self._values.get("configuration_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def customization_resource_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Links a list of resource ARNs (for example, custom action ARNs) to a Slack channel configuration for  .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-customizationresourcearns
        '''
        result = self._values.get("customization_resource_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def guardrail_policies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of IAM policy ARNs that are applied as channel guardrails.

        The AWS managed 'AdministratorAccess' policy is applied as a default if this is not set.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-guardrailpolicies
        '''
        result = self._values.get("guardrail_policies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def iam_role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the IAM role that defines the permissions for  .

        This is a user-defined role that  will assume. This is not the service-linked role. For more information, see `IAM Policies for  in chat applications <https://docs.aws.amazon.com/chatbot/latest/adminguide/chatbot-iam-policies.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-iamrolearn
        '''
        result = self._values.get("iam_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_level(self) -> typing.Optional[builtins.str]:
        '''Specifies the logging level for this configuration. This property affects the log entries pushed to Amazon CloudWatch Logs.

        Logging levels include ``ERROR`` , ``INFO`` , or ``NONE`` .

        :default: - "NONE"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-logginglevel
        '''
        result = self._values.get("logging_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def slack_channel_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the Slack channel.

        To get the ID, open Slack, right click on the channel name in the left pane, then choose Copy Link. The channel ID is the character string at the end of the URL. For example, ``ABCBBLZZZ`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-slackchannelid
        '''
        result = self._values.get("slack_channel_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def slack_workspace_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the Slack workspace authorized with  .

        To get the workspace ID, you must perform the initial authorization flow with Slack in the  in chat applications console. Then you can copy and paste the workspace ID from the console. For more details, see steps 1-3 in `Tutorial: Get started with Slack <https://docs.aws.amazon.com/chatbot/latest/adminguide/slack-setup.html#slack-client-setup>`_ in the *in chat applications User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-slackworkspaceid
        '''
        result = self._values.get("slack_workspace_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sns_topic_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The ARNs of the SNS topics that deliver notifications to  .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-snstopicarns
        '''
        result = self._values.get("sns_topic_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags to add to the configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def user_role_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Enables use of a user role requirement in your chat configuration.

        :default: - false

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-userrolerequired
        '''
        result = self._values.get("user_role_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSlackChannelConfigurationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSlackChannelConfigurationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_chatbot.mixins.CfnSlackChannelConfigurationPropsMixin",
):
    '''.. epigraph::

   AWS Chatbot is now  . `Learn more <https://docs.aws.amazon.com//chatbot/latest/adminguide/service-rename.html>`_ >  > ``Type`` attribute values remain unchanged.

    The ``AWS::Chatbot::SlackChannelConfiguration`` resource configures a Slack channel to allow users to use  with CloudFormation templates.

    This resource requires some setup to be done in the  in chat applications console. To provide the required Slack workspace ID, you must perform the initial authorization flow with Slack in the  in chat applications console, then copy and paste the workspace ID from the console. For more details, see steps 1-3 in `Tutorial: Get started with Slack <https://docs.aws.amazon.com/chatbot/latest/adminguide/slack-setup.html#slack-client-setup>`_ in the *in chat applications User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html
    :cloudformationResource: AWS::Chatbot::SlackChannelConfiguration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_chatbot import mixins as chatbot_mixins
        
        cfn_slack_channel_configuration_props_mixin = chatbot_mixins.CfnSlackChannelConfigurationPropsMixin(chatbot_mixins.CfnSlackChannelConfigurationMixinProps(
            configuration_name="configurationName",
            customization_resource_arns=["customizationResourceArns"],
            guardrail_policies=["guardrailPolicies"],
            iam_role_arn="iamRoleArn",
            logging_level="loggingLevel",
            slack_channel_id="slackChannelId",
            slack_workspace_id="slackWorkspaceId",
            sns_topic_arns=["snsTopicArns"],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            user_role_required=False
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnSlackChannelConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Chatbot::SlackChannelConfiguration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0db3e0a0db7df306541c2f0ad9db303a9caf273d97ea1ccc8b9c781a4e754cfe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd56f4ec7f54da6a12e5ff8e56fd64a30f733b6c60e8ece8b026e506fba01a6d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e37ac84b376d72fc2d123abf4563ff60d4fd7a6902d3d885734982697e16c3bb)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSlackChannelConfigurationMixinProps:
        return typing.cast(CfnSlackChannelConfigurationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnCustomActionMixinProps",
    "CfnCustomActionPropsMixin",
    "CfnMicrosoftTeamsChannelConfigurationMixinProps",
    "CfnMicrosoftTeamsChannelConfigurationPropsMixin",
    "CfnSlackChannelConfigurationMixinProps",
    "CfnSlackChannelConfigurationPropsMixin",
]

publication.publish()

def _typecheckingstub__94089542dd44ae5108337e861ea3ad42df6842a467488ff46edd9acb3c16b8f9(
    *,
    action_name: typing.Optional[builtins.str] = None,
    alias_name: typing.Optional[builtins.str] = None,
    attachments: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCustomActionPropsMixin.CustomActionAttachmentProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    definition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCustomActionPropsMixin.CustomActionDefinitionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b655f23a21db6c37e5f1e30a8c73677a1b72706fd134b0687de45744e251e061(
    props: typing.Union[CfnCustomActionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e005835297a92f5f0c27fb43aa1098eb4c82aeb0bba208e99eae2c25149f562(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ac6ccb32fbaefd319841ef7892335bdbcefa5c37ae6f848831149d0e61d677b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05a9833c8e2a0001a4e1de9ef53287aa69c394662ffec02e1894c79d09dbf1ab(
    *,
    operator: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
    variable_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4442eeb685a4ad1dc0ad0dc57afbba6266deedb269360c0380bf08029e916f26(
    *,
    button_text: typing.Optional[builtins.str] = None,
    criteria: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCustomActionPropsMixin.CustomActionAttachmentCriteriaProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    notification_type: typing.Optional[builtins.str] = None,
    variables: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77da1385d4f7f49a809850dd72a1c7aad4cbf01bf303c3a3d99a5cb4320c0cb4(
    *,
    command_text: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd397887e26a05eb089e6c881edfc4ac5e095b2b8795901d32786253d31b2685(
    *,
    configuration_name: typing.Optional[builtins.str] = None,
    customization_resource_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    guardrail_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
    iam_role_arn: typing.Optional[builtins.str] = None,
    logging_level: typing.Optional[builtins.str] = None,
    sns_topic_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    team_id: typing.Optional[builtins.str] = None,
    teams_channel_id: typing.Optional[builtins.str] = None,
    teams_channel_name: typing.Optional[builtins.str] = None,
    teams_tenant_id: typing.Optional[builtins.str] = None,
    user_role_required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95cd3eecf32bb85ccff41ab80c56297031c1d57a9b8479bf23cc8d0879dc464a(
    props: typing.Union[CfnMicrosoftTeamsChannelConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd26c5de1a4e4a88abbe5494e643a244e46318d26985eb24ce6d830c78c4c003(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f88aab6640074ec0917314b05f522b2bb8ec09b24b05e3e8f3d65d8afa1c224(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b56407e23397623cd43ae3adb8da84a15e3a3d7b42297f24e4ca4e549eeba647(
    *,
    configuration_name: typing.Optional[builtins.str] = None,
    customization_resource_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    guardrail_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
    iam_role_arn: typing.Optional[builtins.str] = None,
    logging_level: typing.Optional[builtins.str] = None,
    slack_channel_id: typing.Optional[builtins.str] = None,
    slack_workspace_id: typing.Optional[builtins.str] = None,
    sns_topic_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    user_role_required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0db3e0a0db7df306541c2f0ad9db303a9caf273d97ea1ccc8b9c781a4e754cfe(
    props: typing.Union[CfnSlackChannelConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd56f4ec7f54da6a12e5ff8e56fd64a30f733b6c60e8ece8b026e506fba01a6d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e37ac84b376d72fc2d123abf4563ff60d4fd7a6902d3d885734982697e16c3bb(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
