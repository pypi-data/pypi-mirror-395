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
    jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnConnectorDefinitionMixinProps",
    jsii_struct_bases=[],
    name_mapping={"initial_version": "initialVersion", "name": "name", "tags": "tags"},
)
class CfnConnectorDefinitionMixinProps:
    def __init__(
        self,
        *,
        initial_version: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorDefinitionPropsMixin.ConnectorDefinitionVersionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Properties for CfnConnectorDefinitionPropsMixin.

        :param initial_version: The connector definition version to include when the connector definition is created. A connector definition version contains a list of ```connector`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-connectordefinition-connector.html>`_ property types. .. epigraph:: To associate a connector definition version after the connector definition is created, create an ```AWS::Greengrass::ConnectorDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-connectordefinitionversion.html>`_ resource and specify the ID of this connector definition.
        :param name: The name of the connector definition.
        :param tags: Application-specific metadata to attach to the connector definition. You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/v1/developerguide/tagging.html>`_ in the *Developer Guide* . This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in CloudFormation templates:: "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value" }

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-connectordefinition.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
            
            # parameters: Any
            # tags: Any
            
            cfn_connector_definition_mixin_props = greengrass_mixins.CfnConnectorDefinitionMixinProps(
                initial_version=greengrass_mixins.CfnConnectorDefinitionPropsMixin.ConnectorDefinitionVersionProperty(
                    connectors=[greengrass_mixins.CfnConnectorDefinitionPropsMixin.ConnectorProperty(
                        connector_arn="connectorArn",
                        id="id",
                        parameters=parameters
                    )]
                ),
                name="name",
                tags=tags
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57b0a4755acd51781d2f9f84eec1a2790e5f5c5725d638a6758ba57c0558bbf3)
            check_type(argname="argument initial_version", value=initial_version, expected_type=type_hints["initial_version"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if initial_version is not None:
            self._values["initial_version"] = initial_version
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def initial_version(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorDefinitionPropsMixin.ConnectorDefinitionVersionProperty"]]:
        '''The connector definition version to include when the connector definition is created.

        A connector definition version contains a list of ```connector`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-connectordefinition-connector.html>`_ property types.
        .. epigraph::

           To associate a connector definition version after the connector definition is created, create an ```AWS::Greengrass::ConnectorDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-connectordefinitionversion.html>`_ resource and specify the ID of this connector definition.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-connectordefinition.html#cfn-greengrass-connectordefinition-initialversion
        '''
        result = self._values.get("initial_version")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorDefinitionPropsMixin.ConnectorDefinitionVersionProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the connector definition.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-connectordefinition.html#cfn-greengrass-connectordefinition-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''Application-specific metadata to attach to the connector definition.

        You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/v1/developerguide/tagging.html>`_ in the *Developer Guide* .

        This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in CloudFormation templates::

           "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value"
           }

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-connectordefinition.html#cfn-greengrass-connectordefinition-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConnectorDefinitionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnConnectorDefinitionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnConnectorDefinitionPropsMixin",
):
    '''The ``AWS::Greengrass::ConnectorDefinition`` resource represents a connector definition for AWS IoT Greengrass .

    Connector definitions are used to organize your connector definition versions.

    Connector definitions can reference multiple connector definition versions. All connector definition versions must be associated with a connector definition. Each connector definition version can contain one or more connectors.
    .. epigraph::

       When you create a connector definition, you can optionally include an initial connector definition version. To associate a connector definition version later, create an ```AWS::Greengrass::ConnectorDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-connectordefinitionversion.html>`_ resource and specify the ID of this connector definition.

       After you create the connector definition version that contains the connectors you want to deploy, you must add it to your group version. For more information, see ```AWS::Greengrass::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-connectordefinition.html
    :cloudformationResource: AWS::Greengrass::ConnectorDefinition
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
        
        # parameters: Any
        # tags: Any
        
        cfn_connector_definition_props_mixin = greengrass_mixins.CfnConnectorDefinitionPropsMixin(greengrass_mixins.CfnConnectorDefinitionMixinProps(
            initial_version=greengrass_mixins.CfnConnectorDefinitionPropsMixin.ConnectorDefinitionVersionProperty(
                connectors=[greengrass_mixins.CfnConnectorDefinitionPropsMixin.ConnectorProperty(
                    connector_arn="connectorArn",
                    id="id",
                    parameters=parameters
                )]
            ),
            name="name",
            tags=tags
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnConnectorDefinitionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Greengrass::ConnectorDefinition``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d05b6b5845542c620a3fd58b27061f6babe75645d1e498b6370568d33d363569)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6af34f38b541dc02f89aa688fd31207fd075863315e41e94e21df98001c052d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b236ca7b34307777a7c8616b8cca6d84e8816a5bfa3c235a618d71f1d29094d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnConnectorDefinitionMixinProps:
        return typing.cast(CfnConnectorDefinitionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnConnectorDefinitionPropsMixin.ConnectorDefinitionVersionProperty",
        jsii_struct_bases=[],
        name_mapping={"connectors": "connectors"},
    )
    class ConnectorDefinitionVersionProperty:
        def __init__(
            self,
            *,
            connectors: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorDefinitionPropsMixin.ConnectorProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''A connector definition version contains a list of connectors.

            .. epigraph::

               After you create a connector definition version that contains the connectors you want to deploy, you must add it to your group version. For more information, see ```AWS::Greengrass::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html>`_ .

            In an CloudFormation template, ``ConnectorDefinitionVersion`` is the property type of the ``InitialVersion`` property in the ```AWS::Greengrass::ConnectorDefinition`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-connectordefinition.html>`_ resource.

            :param connectors: The connectors in this version. Only one instance of a given connector can be added to a connector definition version at a time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-connectordefinition-connectordefinitionversion.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                # parameters: Any
                
                connector_definition_version_property = greengrass_mixins.CfnConnectorDefinitionPropsMixin.ConnectorDefinitionVersionProperty(
                    connectors=[greengrass_mixins.CfnConnectorDefinitionPropsMixin.ConnectorProperty(
                        connector_arn="connectorArn",
                        id="id",
                        parameters=parameters
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4931b0d72c72845a5d58d7b3306c33797814d1c231e0ed482d907421f500af73)
                check_type(argname="argument connectors", value=connectors, expected_type=type_hints["connectors"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if connectors is not None:
                self._values["connectors"] = connectors

        @builtins.property
        def connectors(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorDefinitionPropsMixin.ConnectorProperty"]]]]:
            '''The connectors in this version.

            Only one instance of a given connector can be added to a connector definition version at a time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-connectordefinition-connectordefinitionversion.html#cfn-greengrass-connectordefinition-connectordefinitionversion-connectors
            '''
            result = self._values.get("connectors")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorDefinitionPropsMixin.ConnectorProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectorDefinitionVersionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnConnectorDefinitionPropsMixin.ConnectorProperty",
        jsii_struct_bases=[],
        name_mapping={
            "connector_arn": "connectorArn",
            "id": "id",
            "parameters": "parameters",
        },
    )
    class ConnectorProperty:
        def __init__(
            self,
            *,
            connector_arn: typing.Optional[builtins.str] = None,
            id: typing.Optional[builtins.str] = None,
            parameters: typing.Any = None,
        ) -> None:
            '''Connectors are modules that provide built-in integration with local infrastructure, device protocols, AWS , and other cloud services.

            For more information, see `Integrate with Services and Protocols Using Greengrass Connectors <https://docs.aws.amazon.com/greengrass/v1/developerguide/connectors.html>`_ in the *Developer Guide* .

            In an CloudFormation template, the ``Connectors`` property of the ```ConnectorDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-connectordefinition-connectordefinitionversion.html>`_ property type contains a list of ``Connector`` property types.

            :param connector_arn: The Amazon Resource Name (ARN) of the connector. For more information about connectors provided by AWS , see `Greengrass Connectors Provided by AWS <https://docs.aws.amazon.com/greengrass/v1/developerguide/connectors-list.html>`_ .
            :param id: A descriptive or arbitrary ID for the connector. This value must be unique within the connector definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .
            :param parameters: The parameters or configuration used by the connector. For more information about connectors provided by AWS , see `Greengrass Connectors Provided by AWS <https://docs.aws.amazon.com/greengrass/v1/developerguide/connectors-list.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-connectordefinition-connector.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                # parameters: Any
                
                connector_property = greengrass_mixins.CfnConnectorDefinitionPropsMixin.ConnectorProperty(
                    connector_arn="connectorArn",
                    id="id",
                    parameters=parameters
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6a3ea25d71d4e05d2954225f69ce30d85b3afc2375690c762e48c4e1043447a5)
                check_type(argname="argument connector_arn", value=connector_arn, expected_type=type_hints["connector_arn"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if connector_arn is not None:
                self._values["connector_arn"] = connector_arn
            if id is not None:
                self._values["id"] = id
            if parameters is not None:
                self._values["parameters"] = parameters

        @builtins.property
        def connector_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the connector.

            For more information about connectors provided by AWS , see `Greengrass Connectors Provided by AWS <https://docs.aws.amazon.com/greengrass/v1/developerguide/connectors-list.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-connectordefinition-connector.html#cfn-greengrass-connectordefinition-connector-connectorarn
            '''
            result = self._values.get("connector_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''A descriptive or arbitrary ID for the connector.

            This value must be unique within the connector definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-connectordefinition-connector.html#cfn-greengrass-connectordefinition-connector-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def parameters(self) -> typing.Any:
            '''The parameters or configuration used by the connector.

            For more information about connectors provided by AWS , see `Greengrass Connectors Provided by AWS <https://docs.aws.amazon.com/greengrass/v1/developerguide/connectors-list.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-connectordefinition-connector.html#cfn-greengrass-connectordefinition-connector-parameters
            '''
            result = self._values.get("parameters")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnConnectorDefinitionVersionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "connector_definition_id": "connectorDefinitionId",
        "connectors": "connectors",
    },
)
class CfnConnectorDefinitionVersionMixinProps:
    def __init__(
        self,
        *,
        connector_definition_id: typing.Optional[builtins.str] = None,
        connectors: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorDefinitionVersionPropsMixin.ConnectorProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnConnectorDefinitionVersionPropsMixin.

        :param connector_definition_id: The ID of the connector definition associated with this version. This value is a GUID.
        :param connectors: The connectors in this version. Only one instance of a given connector can be added to the connector definition version at a time.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-connectordefinitionversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
            
            # parameters: Any
            
            cfn_connector_definition_version_mixin_props = greengrass_mixins.CfnConnectorDefinitionVersionMixinProps(
                connector_definition_id="connectorDefinitionId",
                connectors=[greengrass_mixins.CfnConnectorDefinitionVersionPropsMixin.ConnectorProperty(
                    connector_arn="connectorArn",
                    id="id",
                    parameters=parameters
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e51fd100eaf9684a050144252e8f39ff4505dfe2c1aede84c481a2872bfc1539)
            check_type(argname="argument connector_definition_id", value=connector_definition_id, expected_type=type_hints["connector_definition_id"])
            check_type(argname="argument connectors", value=connectors, expected_type=type_hints["connectors"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connector_definition_id is not None:
            self._values["connector_definition_id"] = connector_definition_id
        if connectors is not None:
            self._values["connectors"] = connectors

    @builtins.property
    def connector_definition_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the connector definition associated with this version.

        This value is a GUID.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-connectordefinitionversion.html#cfn-greengrass-connectordefinitionversion-connectordefinitionid
        '''
        result = self._values.get("connector_definition_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connectors(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorDefinitionVersionPropsMixin.ConnectorProperty"]]]]:
        '''The connectors in this version.

        Only one instance of a given connector can be added to the connector definition version at a time.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-connectordefinitionversion.html#cfn-greengrass-connectordefinitionversion-connectors
        '''
        result = self._values.get("connectors")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorDefinitionVersionPropsMixin.ConnectorProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConnectorDefinitionVersionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnConnectorDefinitionVersionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnConnectorDefinitionVersionPropsMixin",
):
    '''The ``AWS::Greengrass::ConnectorDefinitionVersion`` resource represents a connector definition version for AWS IoT Greengrass .

    A connector definition version contains a list of connectors.
    .. epigraph::

       To create a connector definition version, you must specify the ID of the connector definition that you want to associate with the version. For information about creating a connector definition, see ```AWS::Greengrass::ConnectorDefinition`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-connectordefinition.html>`_ .

       After you create a connector definition version that contains the connectors you want to deploy, you must add it to your group version. For more information, see ```AWS::Greengrass::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-connectordefinitionversion.html
    :cloudformationResource: AWS::Greengrass::ConnectorDefinitionVersion
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
        
        # parameters: Any
        
        cfn_connector_definition_version_props_mixin = greengrass_mixins.CfnConnectorDefinitionVersionPropsMixin(greengrass_mixins.CfnConnectorDefinitionVersionMixinProps(
            connector_definition_id="connectorDefinitionId",
            connectors=[greengrass_mixins.CfnConnectorDefinitionVersionPropsMixin.ConnectorProperty(
                connector_arn="connectorArn",
                id="id",
                parameters=parameters
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnConnectorDefinitionVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Greengrass::ConnectorDefinitionVersion``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42459fc68d474770bf7b84fdb6bc0039dc9dbcdcb6ecc9f9b14d939d103d7adb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d87930949e5cf54fb4262b7cf4ec885ab2f64eae6edd08d7f7841000eb55951)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f0f9699e20fde20c0ea31bea15dbd2c045892c96ccad19d1a145250f6b4d8c3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnConnectorDefinitionVersionMixinProps:
        return typing.cast(CfnConnectorDefinitionVersionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnConnectorDefinitionVersionPropsMixin.ConnectorProperty",
        jsii_struct_bases=[],
        name_mapping={
            "connector_arn": "connectorArn",
            "id": "id",
            "parameters": "parameters",
        },
    )
    class ConnectorProperty:
        def __init__(
            self,
            *,
            connector_arn: typing.Optional[builtins.str] = None,
            id: typing.Optional[builtins.str] = None,
            parameters: typing.Any = None,
        ) -> None:
            '''Connectors are modules that provide built-in integration with local infrastructure, device protocols, AWS , and other cloud services.

            For more information, see `Integrate with Services and Protocols Using Greengrass Connectors <https://docs.aws.amazon.com/greengrass/v1/developerguide/connectors.html>`_ in the *Developer Guide* .

            In an CloudFormation template, the ``Connectors`` property of the ```AWS::Greengrass::ConnectorDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-connectordefinitionversion.html>`_ resource contains a list of ``Connector`` property types.

            :param connector_arn: The Amazon Resource Name (ARN) of the connector. For more information about connectors provided by AWS , see `Greengrass Connectors Provided by AWS <https://docs.aws.amazon.com/greengrass/v1/developerguide/connectors-list.html>`_ .
            :param id: A descriptive or arbitrary ID for the connector. This value must be unique within the connector definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .
            :param parameters: The parameters or configuration that the connector uses. For more information about connectors provided by AWS , see `Greengrass Connectors Provided by AWS <https://docs.aws.amazon.com/greengrass/v1/developerguide/connectors-list.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-connectordefinitionversion-connector.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                # parameters: Any
                
                connector_property = greengrass_mixins.CfnConnectorDefinitionVersionPropsMixin.ConnectorProperty(
                    connector_arn="connectorArn",
                    id="id",
                    parameters=parameters
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dfd558649511aa07d06e2f6bbcd3b84047b24134ad3e3e25ca862124a9fced72)
                check_type(argname="argument connector_arn", value=connector_arn, expected_type=type_hints["connector_arn"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if connector_arn is not None:
                self._values["connector_arn"] = connector_arn
            if id is not None:
                self._values["id"] = id
            if parameters is not None:
                self._values["parameters"] = parameters

        @builtins.property
        def connector_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the connector.

            For more information about connectors provided by AWS , see `Greengrass Connectors Provided by AWS <https://docs.aws.amazon.com/greengrass/v1/developerguide/connectors-list.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-connectordefinitionversion-connector.html#cfn-greengrass-connectordefinitionversion-connector-connectorarn
            '''
            result = self._values.get("connector_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''A descriptive or arbitrary ID for the connector.

            This value must be unique within the connector definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-connectordefinitionversion-connector.html#cfn-greengrass-connectordefinitionversion-connector-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def parameters(self) -> typing.Any:
            '''The parameters or configuration that the connector uses.

            For more information about connectors provided by AWS , see `Greengrass Connectors Provided by AWS <https://docs.aws.amazon.com/greengrass/v1/developerguide/connectors-list.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-connectordefinitionversion-connector.html#cfn-greengrass-connectordefinitionversion-connector-parameters
            '''
            result = self._values.get("parameters")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnCoreDefinitionMixinProps",
    jsii_struct_bases=[],
    name_mapping={"initial_version": "initialVersion", "name": "name", "tags": "tags"},
)
class CfnCoreDefinitionMixinProps:
    def __init__(
        self,
        *,
        initial_version: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCoreDefinitionPropsMixin.CoreDefinitionVersionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Properties for CfnCoreDefinitionPropsMixin.

        :param initial_version: The core definition version to include when the core definition is created. Currently, a core definition version can contain only one ```core`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-coredefinition-core.html>`_ . .. epigraph:: To associate a core definition version after the core definition is created, create an ```AWS::Greengrass::CoreDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-coredefinitionversion.html>`_ resource and specify the ID of this core definition.
        :param name: The name of the core definition.
        :param tags: Application-specific metadata to attach to the core definition. You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/v1/developerguide/tagging.html>`_ in the *Developer Guide* . This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in CloudFormation templates:: "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value" }

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-coredefinition.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
            
            # tags: Any
            
            cfn_core_definition_mixin_props = greengrass_mixins.CfnCoreDefinitionMixinProps(
                initial_version=greengrass_mixins.CfnCoreDefinitionPropsMixin.CoreDefinitionVersionProperty(
                    cores=[greengrass_mixins.CfnCoreDefinitionPropsMixin.CoreProperty(
                        certificate_arn="certificateArn",
                        id="id",
                        sync_shadow=False,
                        thing_arn="thingArn"
                    )]
                ),
                name="name",
                tags=tags
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95131d35a1833efb1cd1bed4b5d00ad13f68b49e4cda134dc6f14fbf78fbf412)
            check_type(argname="argument initial_version", value=initial_version, expected_type=type_hints["initial_version"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if initial_version is not None:
            self._values["initial_version"] = initial_version
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def initial_version(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCoreDefinitionPropsMixin.CoreDefinitionVersionProperty"]]:
        '''The core definition version to include when the core definition is created.

        Currently, a core definition version can contain only one ```core`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-coredefinition-core.html>`_ .
        .. epigraph::

           To associate a core definition version after the core definition is created, create an ```AWS::Greengrass::CoreDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-coredefinitionversion.html>`_ resource and specify the ID of this core definition.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-coredefinition.html#cfn-greengrass-coredefinition-initialversion
        '''
        result = self._values.get("initial_version")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCoreDefinitionPropsMixin.CoreDefinitionVersionProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the core definition.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-coredefinition.html#cfn-greengrass-coredefinition-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''Application-specific metadata to attach to the core definition.

        You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/v1/developerguide/tagging.html>`_ in the *Developer Guide* .

        This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in CloudFormation templates::

           "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value"
           }

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-coredefinition.html#cfn-greengrass-coredefinition-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCoreDefinitionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnCoreDefinitionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnCoreDefinitionPropsMixin",
):
    '''The ``AWS::Greengrass::CoreDefinition`` resource represents a core definition for AWS IoT Greengrass .

    Core definitions are used to organize your core definition versions.

    Core definitions can reference multiple core definition versions. All core definition versions must be associated with a core definition. Each core definition version can contain one Greengrass core.
    .. epigraph::

       When you create a core definition, you can optionally include an initial core definition version. To associate a core definition version later, create an ```AWS::Greengrass::CoreDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-coredefinitionversion.html>`_ resource and specify the ID of this core definition.

       After you create the core definition version that contains the core you want to deploy, you must add it to your group version. For more information, see ```AWS::Greengrass::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-coredefinition.html
    :cloudformationResource: AWS::Greengrass::CoreDefinition
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
        
        # tags: Any
        
        cfn_core_definition_props_mixin = greengrass_mixins.CfnCoreDefinitionPropsMixin(greengrass_mixins.CfnCoreDefinitionMixinProps(
            initial_version=greengrass_mixins.CfnCoreDefinitionPropsMixin.CoreDefinitionVersionProperty(
                cores=[greengrass_mixins.CfnCoreDefinitionPropsMixin.CoreProperty(
                    certificate_arn="certificateArn",
                    id="id",
                    sync_shadow=False,
                    thing_arn="thingArn"
                )]
            ),
            name="name",
            tags=tags
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnCoreDefinitionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Greengrass::CoreDefinition``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__101d3d5ebefd9192d680191fcd06b8e654c9f2001e2fdcc00d74697257c4be7b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ed56372505ef9536d61e6c261b887c83259d6d8a804fea0cb1c45d6d1f06d42)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcab1b2943fcc8f7063e32d5aac4d4688a334e16dd1dd0084bb2af91f16fff0f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnCoreDefinitionMixinProps:
        return typing.cast(CfnCoreDefinitionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnCoreDefinitionPropsMixin.CoreDefinitionVersionProperty",
        jsii_struct_bases=[],
        name_mapping={"cores": "cores"},
    )
    class CoreDefinitionVersionProperty:
        def __init__(
            self,
            *,
            cores: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCoreDefinitionPropsMixin.CoreProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''A core definition version contains a Greengrass `core <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-coredefinition-core.html>`_ .

            .. epigraph::

               After you create a core definition version that contains the core you want to deploy, you must add it to your group version. For more information, see ```AWS::Greengrass::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html>`_ .

            In an CloudFormation template, ``CoreDefinitionVersion`` is the property type of the ``InitialVersion`` property in the ```AWS::Greengrass::CoreDefinition`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-coredefinition.html>`_ resource.

            :param cores: The Greengrass core in this version. Currently, the ``Cores`` property for a core definition version can contain only one core.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-coredefinition-coredefinitionversion.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                core_definition_version_property = greengrass_mixins.CfnCoreDefinitionPropsMixin.CoreDefinitionVersionProperty(
                    cores=[greengrass_mixins.CfnCoreDefinitionPropsMixin.CoreProperty(
                        certificate_arn="certificateArn",
                        id="id",
                        sync_shadow=False,
                        thing_arn="thingArn"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__86d1abafb9deb3dc9a8b6b301d5926082e500107e153275a85de34828683a206)
                check_type(argname="argument cores", value=cores, expected_type=type_hints["cores"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cores is not None:
                self._values["cores"] = cores

        @builtins.property
        def cores(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCoreDefinitionPropsMixin.CoreProperty"]]]]:
            '''The Greengrass core in this version.

            Currently, the ``Cores`` property for a core definition version can contain only one core.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-coredefinition-coredefinitionversion.html#cfn-greengrass-coredefinition-coredefinitionversion-cores
            '''
            result = self._values.get("cores")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCoreDefinitionPropsMixin.CoreProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CoreDefinitionVersionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnCoreDefinitionPropsMixin.CoreProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate_arn": "certificateArn",
            "id": "id",
            "sync_shadow": "syncShadow",
            "thing_arn": "thingArn",
        },
    )
    class CoreProperty:
        def __init__(
            self,
            *,
            certificate_arn: typing.Optional[builtins.str] = None,
            id: typing.Optional[builtins.str] = None,
            sync_shadow: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            thing_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A core is an AWS IoT device that runs the AWS IoT Greengrass core software and manages local processes for a Greengrass group.

            For more information, see `What Is AWS IoT Greengrass ? <https://docs.aws.amazon.com/greengrass/v1/developerguide/what-is-gg.html>`_ in the *Developer Guide* .

            In an CloudFormation template, the ``Cores`` property of the ```CoreDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-coredefinition-coredefinitionversion.html>`_ property type contains a list of ``Core`` property types. Currently, the list can contain only one core.

            :param certificate_arn: The Amazon Resource Name (ARN) of the device certificate for the core. This X.509 certificate is used to authenticate the core with AWS IoT and AWS IoT Greengrass services.
            :param id: A descriptive or arbitrary ID for the core. This value must be unique within the core definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .
            :param sync_shadow: Indicates whether the core's local shadow is synced with the cloud automatically. The default is false.
            :param thing_arn: The ARN of the core, which is an AWS IoT device (thing).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-coredefinition-core.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                core_property = greengrass_mixins.CfnCoreDefinitionPropsMixin.CoreProperty(
                    certificate_arn="certificateArn",
                    id="id",
                    sync_shadow=False,
                    thing_arn="thingArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6d20f9a84bf47ad684a4ffe818b1a45c7cc087230a584e2a1fb8c4e7bb840261)
                check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument sync_shadow", value=sync_shadow, expected_type=type_hints["sync_shadow"])
                check_type(argname="argument thing_arn", value=thing_arn, expected_type=type_hints["thing_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate_arn is not None:
                self._values["certificate_arn"] = certificate_arn
            if id is not None:
                self._values["id"] = id
            if sync_shadow is not None:
                self._values["sync_shadow"] = sync_shadow
            if thing_arn is not None:
                self._values["thing_arn"] = thing_arn

        @builtins.property
        def certificate_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the device certificate for the core.

            This X.509 certificate is used to authenticate the core with AWS IoT and AWS IoT Greengrass services.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-coredefinition-core.html#cfn-greengrass-coredefinition-core-certificatearn
            '''
            result = self._values.get("certificate_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''A descriptive or arbitrary ID for the core.

            This value must be unique within the core definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-coredefinition-core.html#cfn-greengrass-coredefinition-core-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sync_shadow(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether the core's local shadow is synced with the cloud automatically.

            The default is false.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-coredefinition-core.html#cfn-greengrass-coredefinition-core-syncshadow
            '''
            result = self._values.get("sync_shadow")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def thing_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the core, which is an AWS IoT device (thing).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-coredefinition-core.html#cfn-greengrass-coredefinition-core-thingarn
            '''
            result = self._values.get("thing_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CoreProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnCoreDefinitionVersionMixinProps",
    jsii_struct_bases=[],
    name_mapping={"core_definition_id": "coreDefinitionId", "cores": "cores"},
)
class CfnCoreDefinitionVersionMixinProps:
    def __init__(
        self,
        *,
        core_definition_id: typing.Optional[builtins.str] = None,
        cores: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCoreDefinitionVersionPropsMixin.CoreProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnCoreDefinitionVersionPropsMixin.

        :param core_definition_id: The ID of the core definition associated with this version. This value is a GUID.
        :param cores: The Greengrass core in this version. Currently, the ``Cores`` property for a core definition version can contain only one core.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-coredefinitionversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
            
            cfn_core_definition_version_mixin_props = greengrass_mixins.CfnCoreDefinitionVersionMixinProps(
                core_definition_id="coreDefinitionId",
                cores=[greengrass_mixins.CfnCoreDefinitionVersionPropsMixin.CoreProperty(
                    certificate_arn="certificateArn",
                    id="id",
                    sync_shadow=False,
                    thing_arn="thingArn"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a1eae3da3babded8ac784e4ccd67ae22eb8ef0d411e0c6caae46deb48b181bd)
            check_type(argname="argument core_definition_id", value=core_definition_id, expected_type=type_hints["core_definition_id"])
            check_type(argname="argument cores", value=cores, expected_type=type_hints["cores"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if core_definition_id is not None:
            self._values["core_definition_id"] = core_definition_id
        if cores is not None:
            self._values["cores"] = cores

    @builtins.property
    def core_definition_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the core definition associated with this version.

        This value is a GUID.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-coredefinitionversion.html#cfn-greengrass-coredefinitionversion-coredefinitionid
        '''
        result = self._values.get("core_definition_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cores(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCoreDefinitionVersionPropsMixin.CoreProperty"]]]]:
        '''The Greengrass core in this version.

        Currently, the ``Cores`` property for a core definition version can contain only one core.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-coredefinitionversion.html#cfn-greengrass-coredefinitionversion-cores
        '''
        result = self._values.get("cores")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCoreDefinitionVersionPropsMixin.CoreProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCoreDefinitionVersionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnCoreDefinitionVersionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnCoreDefinitionVersionPropsMixin",
):
    '''The ``AWS::Greengrass::CoreDefinitionVersion`` resource represents a core definition version for AWS IoT Greengrass .

    A core definition version contains a Greengrass core.
    .. epigraph::

       To create a core definition version, you must specify the ID of the core definition that you want to associate with the version. For information about creating a core definition, see ```AWS::Greengrass::CoreDefinition`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-coredefinition.html>`_ .

       After you create a core definition version that contains the core you want to deploy, you must add it to your group version. For more information, see ```AWS::Greengrass::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-coredefinitionversion.html
    :cloudformationResource: AWS::Greengrass::CoreDefinitionVersion
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
        
        cfn_core_definition_version_props_mixin = greengrass_mixins.CfnCoreDefinitionVersionPropsMixin(greengrass_mixins.CfnCoreDefinitionVersionMixinProps(
            core_definition_id="coreDefinitionId",
            cores=[greengrass_mixins.CfnCoreDefinitionVersionPropsMixin.CoreProperty(
                certificate_arn="certificateArn",
                id="id",
                sync_shadow=False,
                thing_arn="thingArn"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnCoreDefinitionVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Greengrass::CoreDefinitionVersion``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7140cb6af6123d37d747e0ba23913f963a96699c049b8b3106d01bcc4e922cf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__37a992e942f3582ab97784b0dd29bf4f08c7c06279801cc2ad7648ef31eff38f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1df06d798f4ab9fa481a3c6e5d63107bbdaa98bc2333ef5eb78b31f145d05bbe)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnCoreDefinitionVersionMixinProps:
        return typing.cast(CfnCoreDefinitionVersionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnCoreDefinitionVersionPropsMixin.CoreProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate_arn": "certificateArn",
            "id": "id",
            "sync_shadow": "syncShadow",
            "thing_arn": "thingArn",
        },
    )
    class CoreProperty:
        def __init__(
            self,
            *,
            certificate_arn: typing.Optional[builtins.str] = None,
            id: typing.Optional[builtins.str] = None,
            sync_shadow: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            thing_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A core is an AWS IoT device that runs the AWS IoT Greengrass core software and manages local processes for a Greengrass group.

            For more information, see `What Is AWS IoT Greengrass ? <https://docs.aws.amazon.com/greengrass/v1/developerguide/what-is-gg.html>`_ in the *Developer Guide* .

            In an CloudFormation template, the ``Cores`` property of the ```AWS::Greengrass::CoreDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-coredefinitionversion.html>`_ resource contains a list of ``Core`` property types. Currently, the list can contain only one core.

            :param certificate_arn: The ARN of the device certificate for the core. This X.509 certificate is used to authenticate the core with AWS IoT and AWS IoT Greengrass services.
            :param id: A descriptive or arbitrary ID for the core. This value must be unique within the core definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .
            :param sync_shadow: Indicates whether the core's local shadow is synced with the cloud automatically. The default is false.
            :param thing_arn: The Amazon Resource Name (ARN) of the core, which is an AWS IoT device (thing).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-coredefinitionversion-core.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                core_property = greengrass_mixins.CfnCoreDefinitionVersionPropsMixin.CoreProperty(
                    certificate_arn="certificateArn",
                    id="id",
                    sync_shadow=False,
                    thing_arn="thingArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d6cce34d8f08e949f96d6474026ef34913f128610a0dfc8dfe7aae7e67f77f9b)
                check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument sync_shadow", value=sync_shadow, expected_type=type_hints["sync_shadow"])
                check_type(argname="argument thing_arn", value=thing_arn, expected_type=type_hints["thing_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate_arn is not None:
                self._values["certificate_arn"] = certificate_arn
            if id is not None:
                self._values["id"] = id
            if sync_shadow is not None:
                self._values["sync_shadow"] = sync_shadow
            if thing_arn is not None:
                self._values["thing_arn"] = thing_arn

        @builtins.property
        def certificate_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the device certificate for the core.

            This X.509 certificate is used to authenticate the core with AWS IoT and AWS IoT Greengrass services.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-coredefinitionversion-core.html#cfn-greengrass-coredefinitionversion-core-certificatearn
            '''
            result = self._values.get("certificate_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''A descriptive or arbitrary ID for the core.

            This value must be unique within the core definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-coredefinitionversion-core.html#cfn-greengrass-coredefinitionversion-core-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sync_shadow(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether the core's local shadow is synced with the cloud automatically.

            The default is false.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-coredefinitionversion-core.html#cfn-greengrass-coredefinitionversion-core-syncshadow
            '''
            result = self._values.get("sync_shadow")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def thing_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the core, which is an AWS IoT device (thing).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-coredefinitionversion-core.html#cfn-greengrass-coredefinitionversion-core-thingarn
            '''
            result = self._values.get("thing_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CoreProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnDeviceDefinitionMixinProps",
    jsii_struct_bases=[],
    name_mapping={"initial_version": "initialVersion", "name": "name", "tags": "tags"},
)
class CfnDeviceDefinitionMixinProps:
    def __init__(
        self,
        *,
        initial_version: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeviceDefinitionPropsMixin.DeviceDefinitionVersionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Properties for CfnDeviceDefinitionPropsMixin.

        :param initial_version: The device definition version to include when the device definition is created. A device definition version contains a list of ```device`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-devicedefinition-device.html>`_ property types. .. epigraph:: To associate a device definition version after the device definition is created, create an ```AWS::Greengrass::DeviceDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-devicedefinitionversion.html>`_ resource and specify the ID of this device definition.
        :param name: The name of the device definition.
        :param tags: Application-specific metadata to attach to the device definition. You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/v1/developerguide/tagging.html>`_ in the *Developer Guide* . This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in CloudFormation templates:: "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value" }

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-devicedefinition.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
            
            # tags: Any
            
            cfn_device_definition_mixin_props = greengrass_mixins.CfnDeviceDefinitionMixinProps(
                initial_version=greengrass_mixins.CfnDeviceDefinitionPropsMixin.DeviceDefinitionVersionProperty(
                    devices=[greengrass_mixins.CfnDeviceDefinitionPropsMixin.DeviceProperty(
                        certificate_arn="certificateArn",
                        id="id",
                        sync_shadow=False,
                        thing_arn="thingArn"
                    )]
                ),
                name="name",
                tags=tags
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beb51de996764ae0259401f9f2259c09b0cd57fe89f76bcdf2c8963ddcd87335)
            check_type(argname="argument initial_version", value=initial_version, expected_type=type_hints["initial_version"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if initial_version is not None:
            self._values["initial_version"] = initial_version
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def initial_version(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeviceDefinitionPropsMixin.DeviceDefinitionVersionProperty"]]:
        '''The device definition version to include when the device definition is created.

        A device definition version contains a list of ```device`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-devicedefinition-device.html>`_ property types.
        .. epigraph::

           To associate a device definition version after the device definition is created, create an ```AWS::Greengrass::DeviceDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-devicedefinitionversion.html>`_ resource and specify the ID of this device definition.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-devicedefinition.html#cfn-greengrass-devicedefinition-initialversion
        '''
        result = self._values.get("initial_version")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeviceDefinitionPropsMixin.DeviceDefinitionVersionProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the device definition.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-devicedefinition.html#cfn-greengrass-devicedefinition-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''Application-specific metadata to attach to the device definition.

        You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/v1/developerguide/tagging.html>`_ in the *Developer Guide* .

        This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in CloudFormation templates::

           "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value"
           }

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-devicedefinition.html#cfn-greengrass-devicedefinition-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeviceDefinitionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDeviceDefinitionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnDeviceDefinitionPropsMixin",
):
    '''The ``AWS::Greengrass::DeviceDefinition`` resource represents a device definition for AWS IoT Greengrass .

    Device definitions are used to organize your device definition versions.

    Device definitions can reference multiple device definition versions. All device definition versions must be associated with a device definition. Each device definition version can contain one or more devices.
    .. epigraph::

       When you create a device definition, you can optionally include an initial device definition version. To associate a device definition version later, create an ```AWS::Greengrass::DeviceDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-devicedefinitionversion.html>`_ resource and specify the ID of this device definition.

       After you create the device definition version that contains the devices you want to deploy, you must add it to your group version. For more information, see ```AWS::Greengrass::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-devicedefinition.html
    :cloudformationResource: AWS::Greengrass::DeviceDefinition
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
        
        # tags: Any
        
        cfn_device_definition_props_mixin = greengrass_mixins.CfnDeviceDefinitionPropsMixin(greengrass_mixins.CfnDeviceDefinitionMixinProps(
            initial_version=greengrass_mixins.CfnDeviceDefinitionPropsMixin.DeviceDefinitionVersionProperty(
                devices=[greengrass_mixins.CfnDeviceDefinitionPropsMixin.DeviceProperty(
                    certificate_arn="certificateArn",
                    id="id",
                    sync_shadow=False,
                    thing_arn="thingArn"
                )]
            ),
            name="name",
            tags=tags
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDeviceDefinitionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Greengrass::DeviceDefinition``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b22dedd2758ff7883d497172c7b7fce6275ea0bbe94093b970383958585d1a4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__453e8704d38e818d0cbb9d3d5d14fe6e1b0e93d3f0b07141d0a7b6c76f300918)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aab2dc8bdb0867789d43c7a2358c5562d1663c9c0de915a99975a060ab083b8d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDeviceDefinitionMixinProps:
        return typing.cast(CfnDeviceDefinitionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnDeviceDefinitionPropsMixin.DeviceDefinitionVersionProperty",
        jsii_struct_bases=[],
        name_mapping={"devices": "devices"},
    )
    class DeviceDefinitionVersionProperty:
        def __init__(
            self,
            *,
            devices: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeviceDefinitionPropsMixin.DeviceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''A device definition version contains a list of `devices <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-devicedefinition-device.html>`_ .

            .. epigraph::

               After you create a device definition version that contains the devices you want to deploy, you must add it to your group version. For more information, see ```AWS::Greengrass::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html>`_ .

            In an CloudFormation template, ``DeviceDefinitionVersion`` is the property type of the ``InitialVersion`` property in the ```AWS::Greengrass::DeviceDefinition`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-devicedefinition.html>`_ resource.

            :param devices: The devices in this version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-devicedefinition-devicedefinitionversion.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                device_definition_version_property = greengrass_mixins.CfnDeviceDefinitionPropsMixin.DeviceDefinitionVersionProperty(
                    devices=[greengrass_mixins.CfnDeviceDefinitionPropsMixin.DeviceProperty(
                        certificate_arn="certificateArn",
                        id="id",
                        sync_shadow=False,
                        thing_arn="thingArn"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__18dfac721607b8042734c3b7a9f768487012bf34e90cc34cf123254fecb16ff7)
                check_type(argname="argument devices", value=devices, expected_type=type_hints["devices"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if devices is not None:
                self._values["devices"] = devices

        @builtins.property
        def devices(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeviceDefinitionPropsMixin.DeviceProperty"]]]]:
            '''The devices in this version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-devicedefinition-devicedefinitionversion.html#cfn-greengrass-devicedefinition-devicedefinitionversion-devices
            '''
            result = self._values.get("devices")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeviceDefinitionPropsMixin.DeviceProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeviceDefinitionVersionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnDeviceDefinitionPropsMixin.DeviceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate_arn": "certificateArn",
            "id": "id",
            "sync_shadow": "syncShadow",
            "thing_arn": "thingArn",
        },
    )
    class DeviceProperty:
        def __init__(
            self,
            *,
            certificate_arn: typing.Optional[builtins.str] = None,
            id: typing.Optional[builtins.str] = None,
            sync_shadow: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            thing_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A device is an AWS IoT device (thing) that's added to a Greengrass group.

            Greengrass devices can communicate with the Greengrass core in the same group. For more information, see `What Is AWS IoT Greengrass ? <https://docs.aws.amazon.com/greengrass/v1/developerguide/what-is-gg.html>`_ in the *Developer Guide* .

            In an CloudFormation template, the ``Devices`` property of the ```DeviceDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-devicedefinition-devicedefinitionversion.html>`_ property type contains a list of ``Device`` property types.

            :param certificate_arn: The Amazon Resource Name (ARN) of the device certificate for the device. This X.509 certificate is used to authenticate the device with AWS IoT and AWS IoT Greengrass services.
            :param id: A descriptive or arbitrary ID for the device. This value must be unique within the device definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .
            :param sync_shadow: Indicates whether the device's local shadow is synced with the cloud automatically.
            :param thing_arn: The ARN of the device, which is an AWS IoT device (thing).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-devicedefinition-device.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                device_property = greengrass_mixins.CfnDeviceDefinitionPropsMixin.DeviceProperty(
                    certificate_arn="certificateArn",
                    id="id",
                    sync_shadow=False,
                    thing_arn="thingArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__06511ab24a1f53381ce0a089fb07dd67f852f14d10c0a546f9818be911f30d79)
                check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument sync_shadow", value=sync_shadow, expected_type=type_hints["sync_shadow"])
                check_type(argname="argument thing_arn", value=thing_arn, expected_type=type_hints["thing_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate_arn is not None:
                self._values["certificate_arn"] = certificate_arn
            if id is not None:
                self._values["id"] = id
            if sync_shadow is not None:
                self._values["sync_shadow"] = sync_shadow
            if thing_arn is not None:
                self._values["thing_arn"] = thing_arn

        @builtins.property
        def certificate_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the device certificate for the device.

            This X.509 certificate is used to authenticate the device with AWS IoT and AWS IoT Greengrass services.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-devicedefinition-device.html#cfn-greengrass-devicedefinition-device-certificatearn
            '''
            result = self._values.get("certificate_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''A descriptive or arbitrary ID for the device.

            This value must be unique within the device definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-devicedefinition-device.html#cfn-greengrass-devicedefinition-device-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sync_shadow(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether the device's local shadow is synced with the cloud automatically.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-devicedefinition-device.html#cfn-greengrass-devicedefinition-device-syncshadow
            '''
            result = self._values.get("sync_shadow")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def thing_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the device, which is an AWS IoT device (thing).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-devicedefinition-device.html#cfn-greengrass-devicedefinition-device-thingarn
            '''
            result = self._values.get("thing_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeviceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnDeviceDefinitionVersionMixinProps",
    jsii_struct_bases=[],
    name_mapping={"device_definition_id": "deviceDefinitionId", "devices": "devices"},
)
class CfnDeviceDefinitionVersionMixinProps:
    def __init__(
        self,
        *,
        device_definition_id: typing.Optional[builtins.str] = None,
        devices: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeviceDefinitionVersionPropsMixin.DeviceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnDeviceDefinitionVersionPropsMixin.

        :param device_definition_id: The ID of the device definition associated with this version. This value is a GUID.
        :param devices: The devices in this version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-devicedefinitionversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
            
            cfn_device_definition_version_mixin_props = greengrass_mixins.CfnDeviceDefinitionVersionMixinProps(
                device_definition_id="deviceDefinitionId",
                devices=[greengrass_mixins.CfnDeviceDefinitionVersionPropsMixin.DeviceProperty(
                    certificate_arn="certificateArn",
                    id="id",
                    sync_shadow=False,
                    thing_arn="thingArn"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12006b6d7314ac3787bbdef126579715eaebabb2da2223abbf59980378375b96)
            check_type(argname="argument device_definition_id", value=device_definition_id, expected_type=type_hints["device_definition_id"])
            check_type(argname="argument devices", value=devices, expected_type=type_hints["devices"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if device_definition_id is not None:
            self._values["device_definition_id"] = device_definition_id
        if devices is not None:
            self._values["devices"] = devices

    @builtins.property
    def device_definition_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the device definition associated with this version.

        This value is a GUID.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-devicedefinitionversion.html#cfn-greengrass-devicedefinitionversion-devicedefinitionid
        '''
        result = self._values.get("device_definition_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def devices(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeviceDefinitionVersionPropsMixin.DeviceProperty"]]]]:
        '''The devices in this version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-devicedefinitionversion.html#cfn-greengrass-devicedefinitionversion-devices
        '''
        result = self._values.get("devices")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeviceDefinitionVersionPropsMixin.DeviceProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeviceDefinitionVersionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDeviceDefinitionVersionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnDeviceDefinitionVersionPropsMixin",
):
    '''The ``AWS::Greengrass::DeviceDefinitionVersion`` resource represents a device definition version for AWS IoT Greengrass .

    A device definition version contains a list of devices.
    .. epigraph::

       To create a device definition version, you must specify the ID of the device definition that you want to associate with the version. For information about creating a device definition, see ```AWS::Greengrass::DeviceDefinition`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-devicedefinition.html>`_ .

       After you create a device definition version that contains the devices you want to deploy, you must add it to your group version. For more information, see ```AWS::Greengrass::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-devicedefinitionversion.html
    :cloudformationResource: AWS::Greengrass::DeviceDefinitionVersion
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
        
        cfn_device_definition_version_props_mixin = greengrass_mixins.CfnDeviceDefinitionVersionPropsMixin(greengrass_mixins.CfnDeviceDefinitionVersionMixinProps(
            device_definition_id="deviceDefinitionId",
            devices=[greengrass_mixins.CfnDeviceDefinitionVersionPropsMixin.DeviceProperty(
                certificate_arn="certificateArn",
                id="id",
                sync_shadow=False,
                thing_arn="thingArn"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDeviceDefinitionVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Greengrass::DeviceDefinitionVersion``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bf4f2b3963c9821ae4051f1cca1c1f32db2ff8a09aae19ec5ec7c1ade2a902d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__048dac45aa803c49295100d20c6134e6e5cd4fe5cfaf725f2f87e7c0955e3723)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab8eeb9cf5809e32975425bb421bcbfc2459288ec121905910ab2eb4baad8946)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDeviceDefinitionVersionMixinProps:
        return typing.cast(CfnDeviceDefinitionVersionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnDeviceDefinitionVersionPropsMixin.DeviceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate_arn": "certificateArn",
            "id": "id",
            "sync_shadow": "syncShadow",
            "thing_arn": "thingArn",
        },
    )
    class DeviceProperty:
        def __init__(
            self,
            *,
            certificate_arn: typing.Optional[builtins.str] = None,
            id: typing.Optional[builtins.str] = None,
            sync_shadow: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            thing_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A device is an AWS IoT device (thing) that's added to a Greengrass group.

            Greengrass devices can communicate with the Greengrass core in the same group. For more information, see `What Is AWS IoT Greengrass ? <https://docs.aws.amazon.com/greengrass/v1/developerguide/what-is-gg.html>`_ in the *Developer Guide* .

            In an CloudFormation template, the ``Devices`` property of the ```AWS::Greengrass::DeviceDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-devicedefinitionversion.html>`_ resource contains a list of ``Device`` property types.

            :param certificate_arn: The ARN of the device certificate for the device. This X.509 certificate is used to authenticate the device with AWS IoT and AWS IoT Greengrass services.
            :param id: A descriptive or arbitrary ID for the device. This value must be unique within the device definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .
            :param sync_shadow: Indicates whether the device's local shadow is synced with the cloud automatically.
            :param thing_arn: The Amazon Resource Name (ARN) of the device, which is an AWS IoT device (thing).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-devicedefinitionversion-device.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                device_property = greengrass_mixins.CfnDeviceDefinitionVersionPropsMixin.DeviceProperty(
                    certificate_arn="certificateArn",
                    id="id",
                    sync_shadow=False,
                    thing_arn="thingArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e9833da919e59111af3d750c2d19725705748806013721c3a5e3ded085f7f59c)
                check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument sync_shadow", value=sync_shadow, expected_type=type_hints["sync_shadow"])
                check_type(argname="argument thing_arn", value=thing_arn, expected_type=type_hints["thing_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate_arn is not None:
                self._values["certificate_arn"] = certificate_arn
            if id is not None:
                self._values["id"] = id
            if sync_shadow is not None:
                self._values["sync_shadow"] = sync_shadow
            if thing_arn is not None:
                self._values["thing_arn"] = thing_arn

        @builtins.property
        def certificate_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the device certificate for the device.

            This X.509 certificate is used to authenticate the device with AWS IoT and AWS IoT Greengrass services.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-devicedefinitionversion-device.html#cfn-greengrass-devicedefinitionversion-device-certificatearn
            '''
            result = self._values.get("certificate_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''A descriptive or arbitrary ID for the device.

            This value must be unique within the device definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-devicedefinitionversion-device.html#cfn-greengrass-devicedefinitionversion-device-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sync_shadow(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether the device's local shadow is synced with the cloud automatically.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-devicedefinitionversion-device.html#cfn-greengrass-devicedefinitionversion-device-syncshadow
            '''
            result = self._values.get("sync_shadow")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def thing_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the device, which is an AWS IoT device (thing).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-devicedefinitionversion-device.html#cfn-greengrass-devicedefinitionversion-device-thingarn
            '''
            result = self._values.get("thing_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeviceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnFunctionDefinitionMixinProps",
    jsii_struct_bases=[],
    name_mapping={"initial_version": "initialVersion", "name": "name", "tags": "tags"},
)
class CfnFunctionDefinitionMixinProps:
    def __init__(
        self,
        *,
        initial_version: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionDefinitionPropsMixin.FunctionDefinitionVersionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Properties for CfnFunctionDefinitionPropsMixin.

        :param initial_version: The function definition version to include when the function definition is created. A function definition version contains a list of ```function`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-function.html>`_ property types. .. epigraph:: To associate a function definition version after the function definition is created, create an ```AWS::Greengrass::FunctionDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-functiondefinitionversion.html>`_ resource and specify the ID of this function definition.
        :param name: The name of the function definition.
        :param tags: Application-specific metadata to attach to the function definition. You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/v1/developerguide/tagging.html>`_ in the *Developer Guide* . This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in CloudFormation templates:: "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value" }

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-functiondefinition.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
            
            # tags: Any
            # variables: Any
            
            cfn_function_definition_mixin_props = greengrass_mixins.CfnFunctionDefinitionMixinProps(
                initial_version=greengrass_mixins.CfnFunctionDefinitionPropsMixin.FunctionDefinitionVersionProperty(
                    default_config=greengrass_mixins.CfnFunctionDefinitionPropsMixin.DefaultConfigProperty(
                        execution=greengrass_mixins.CfnFunctionDefinitionPropsMixin.ExecutionProperty(
                            isolation_mode="isolationMode",
                            run_as=greengrass_mixins.CfnFunctionDefinitionPropsMixin.RunAsProperty(
                                gid=123,
                                uid=123
                            )
                        )
                    ),
                    functions=[greengrass_mixins.CfnFunctionDefinitionPropsMixin.FunctionProperty(
                        function_arn="functionArn",
                        function_configuration=greengrass_mixins.CfnFunctionDefinitionPropsMixin.FunctionConfigurationProperty(
                            encoding_type="encodingType",
                            environment=greengrass_mixins.CfnFunctionDefinitionPropsMixin.EnvironmentProperty(
                                access_sysfs=False,
                                execution=greengrass_mixins.CfnFunctionDefinitionPropsMixin.ExecutionProperty(
                                    isolation_mode="isolationMode",
                                    run_as=greengrass_mixins.CfnFunctionDefinitionPropsMixin.RunAsProperty(
                                        gid=123,
                                        uid=123
                                    )
                                ),
                                resource_access_policies=[greengrass_mixins.CfnFunctionDefinitionPropsMixin.ResourceAccessPolicyProperty(
                                    permission="permission",
                                    resource_id="resourceId"
                                )],
                                variables=variables
                            ),
                            exec_args="execArgs",
                            executable="executable",
                            memory_size=123,
                            pinned=False,
                            timeout=123
                        ),
                        id="id"
                    )]
                ),
                name="name",
                tags=tags
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53f1a6d1f5345effb5ff39a7ca481f90ebc6e66ae92cbddcb37c1d32f6444173)
            check_type(argname="argument initial_version", value=initial_version, expected_type=type_hints["initial_version"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if initial_version is not None:
            self._values["initial_version"] = initial_version
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def initial_version(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionDefinitionPropsMixin.FunctionDefinitionVersionProperty"]]:
        '''The function definition version to include when the function definition is created.

        A function definition version contains a list of ```function`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-function.html>`_ property types.
        .. epigraph::

           To associate a function definition version after the function definition is created, create an ```AWS::Greengrass::FunctionDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-functiondefinitionversion.html>`_ resource and specify the ID of this function definition.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-functiondefinition.html#cfn-greengrass-functiondefinition-initialversion
        '''
        result = self._values.get("initial_version")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionDefinitionPropsMixin.FunctionDefinitionVersionProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the function definition.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-functiondefinition.html#cfn-greengrass-functiondefinition-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''Application-specific metadata to attach to the function definition.

        You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/v1/developerguide/tagging.html>`_ in the *Developer Guide* .

        This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in CloudFormation templates::

           "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value"
           }

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-functiondefinition.html#cfn-greengrass-functiondefinition-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFunctionDefinitionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnFunctionDefinitionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnFunctionDefinitionPropsMixin",
):
    '''The ``AWS::Greengrass::FunctionDefinition`` resource represents a function definition for AWS IoT Greengrass .

    Function definitions are used to organize your function definition versions.

    Function definitions can reference multiple function definition versions. All function definition versions must be associated with a function definition. Each function definition version can contain one or more functions.
    .. epigraph::

       When you create a function definition, you can optionally include an initial function definition version. To associate a function definition version later, create an ```AWS::Greengrass::FunctionDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-functiondefinitionversion.html>`_ resource and specify the ID of this function definition.

       After you create the function definition version that contains the functions you want to deploy, you must add it to your group version. For more information, see ```AWS::Greengrass::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-functiondefinition.html
    :cloudformationResource: AWS::Greengrass::FunctionDefinition
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
        
        # tags: Any
        # variables: Any
        
        cfn_function_definition_props_mixin = greengrass_mixins.CfnFunctionDefinitionPropsMixin(greengrass_mixins.CfnFunctionDefinitionMixinProps(
            initial_version=greengrass_mixins.CfnFunctionDefinitionPropsMixin.FunctionDefinitionVersionProperty(
                default_config=greengrass_mixins.CfnFunctionDefinitionPropsMixin.DefaultConfigProperty(
                    execution=greengrass_mixins.CfnFunctionDefinitionPropsMixin.ExecutionProperty(
                        isolation_mode="isolationMode",
                        run_as=greengrass_mixins.CfnFunctionDefinitionPropsMixin.RunAsProperty(
                            gid=123,
                            uid=123
                        )
                    )
                ),
                functions=[greengrass_mixins.CfnFunctionDefinitionPropsMixin.FunctionProperty(
                    function_arn="functionArn",
                    function_configuration=greengrass_mixins.CfnFunctionDefinitionPropsMixin.FunctionConfigurationProperty(
                        encoding_type="encodingType",
                        environment=greengrass_mixins.CfnFunctionDefinitionPropsMixin.EnvironmentProperty(
                            access_sysfs=False,
                            execution=greengrass_mixins.CfnFunctionDefinitionPropsMixin.ExecutionProperty(
                                isolation_mode="isolationMode",
                                run_as=greengrass_mixins.CfnFunctionDefinitionPropsMixin.RunAsProperty(
                                    gid=123,
                                    uid=123
                                )
                            ),
                            resource_access_policies=[greengrass_mixins.CfnFunctionDefinitionPropsMixin.ResourceAccessPolicyProperty(
                                permission="permission",
                                resource_id="resourceId"
                            )],
                            variables=variables
                        ),
                        exec_args="execArgs",
                        executable="executable",
                        memory_size=123,
                        pinned=False,
                        timeout=123
                    ),
                    id="id"
                )]
            ),
            name="name",
            tags=tags
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnFunctionDefinitionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Greengrass::FunctionDefinition``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3db7bcaaec4757d82ea19ea1a553a6550563efc4819087ed57a7a5c0309454f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bea7ac6933b5fff22b6d765a312660e505f9e9e238dda961ab9e97a9dfb09268)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b3a42a15446032ebc4808c5190ef14ef7ea22f6ec0fcdb8b82219ac8f0f25fd)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnFunctionDefinitionMixinProps:
        return typing.cast(CfnFunctionDefinitionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnFunctionDefinitionPropsMixin.DefaultConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"execution": "execution"},
    )
    class DefaultConfigProperty:
        def __init__(
            self,
            *,
            execution: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionDefinitionPropsMixin.ExecutionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The default configuration that applies to all Lambda functions in the function definition version.

            Individual Lambda functions can override these settings.

            In an CloudFormation template, ``DefaultConfig`` is a property of the ```FunctionDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-functiondefinitionversion.html>`_ property type.

            :param execution: Configuration settings for the Lambda execution environment on the AWS IoT Greengrass core.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-defaultconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                default_config_property = greengrass_mixins.CfnFunctionDefinitionPropsMixin.DefaultConfigProperty(
                    execution=greengrass_mixins.CfnFunctionDefinitionPropsMixin.ExecutionProperty(
                        isolation_mode="isolationMode",
                        run_as=greengrass_mixins.CfnFunctionDefinitionPropsMixin.RunAsProperty(
                            gid=123,
                            uid=123
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c9b25291096e3aeb0bae7d6068fa798989528fce1a35363084deab4d19e0a434)
                check_type(argname="argument execution", value=execution, expected_type=type_hints["execution"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if execution is not None:
                self._values["execution"] = execution

        @builtins.property
        def execution(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionDefinitionPropsMixin.ExecutionProperty"]]:
            '''Configuration settings for the Lambda execution environment on the AWS IoT Greengrass core.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-defaultconfig.html#cfn-greengrass-functiondefinition-defaultconfig-execution
            '''
            result = self._values.get("execution")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionDefinitionPropsMixin.ExecutionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DefaultConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnFunctionDefinitionPropsMixin.EnvironmentProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_sysfs": "accessSysfs",
            "execution": "execution",
            "resource_access_policies": "resourceAccessPolicies",
            "variables": "variables",
        },
    )
    class EnvironmentProperty:
        def __init__(
            self,
            *,
            access_sysfs: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            execution: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionDefinitionPropsMixin.ExecutionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            resource_access_policies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionDefinitionPropsMixin.ResourceAccessPolicyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            variables: typing.Any = None,
        ) -> None:
            '''The environment configuration for a Lambda function on the AWS IoT Greengrass core.

            In an CloudFormation template, ``Environment`` is a property of the ```FunctionConfiguration`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-functionconfiguration.html>`_ property type.

            :param access_sysfs: Indicates whether the function is allowed to access the ``/sys`` directory on the core device, which allows the read device information from ``/sys`` . .. epigraph:: This property applies only to Lambda functions that run in a Greengrass container.
            :param execution: Settings for the Lambda execution environment in AWS IoT Greengrass .
            :param resource_access_policies: A list of the `resources <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourceinstance.html>`_ in the group that the function can access, with the corresponding read-only or read-write permissions. The maximum is 10 resources. .. epigraph:: This property applies only for Lambda functions that run in a Greengrass container.
            :param variables: Environment variables for the Lambda function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-environment.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                # variables: Any
                
                environment_property = greengrass_mixins.CfnFunctionDefinitionPropsMixin.EnvironmentProperty(
                    access_sysfs=False,
                    execution=greengrass_mixins.CfnFunctionDefinitionPropsMixin.ExecutionProperty(
                        isolation_mode="isolationMode",
                        run_as=greengrass_mixins.CfnFunctionDefinitionPropsMixin.RunAsProperty(
                            gid=123,
                            uid=123
                        )
                    ),
                    resource_access_policies=[greengrass_mixins.CfnFunctionDefinitionPropsMixin.ResourceAccessPolicyProperty(
                        permission="permission",
                        resource_id="resourceId"
                    )],
                    variables=variables
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d45f3ed05959bcd38ea39663723975acf4d25359b0a9cbdb5e3aab10f54a9361)
                check_type(argname="argument access_sysfs", value=access_sysfs, expected_type=type_hints["access_sysfs"])
                check_type(argname="argument execution", value=execution, expected_type=type_hints["execution"])
                check_type(argname="argument resource_access_policies", value=resource_access_policies, expected_type=type_hints["resource_access_policies"])
                check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_sysfs is not None:
                self._values["access_sysfs"] = access_sysfs
            if execution is not None:
                self._values["execution"] = execution
            if resource_access_policies is not None:
                self._values["resource_access_policies"] = resource_access_policies
            if variables is not None:
                self._values["variables"] = variables

        @builtins.property
        def access_sysfs(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether the function is allowed to access the ``/sys`` directory on the core device, which allows the read device information from ``/sys`` .

            .. epigraph::

               This property applies only to Lambda functions that run in a Greengrass container.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-environment.html#cfn-greengrass-functiondefinition-environment-accesssysfs
            '''
            result = self._values.get("access_sysfs")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def execution(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionDefinitionPropsMixin.ExecutionProperty"]]:
            '''Settings for the Lambda execution environment in AWS IoT Greengrass .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-environment.html#cfn-greengrass-functiondefinition-environment-execution
            '''
            result = self._values.get("execution")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionDefinitionPropsMixin.ExecutionProperty"]], result)

        @builtins.property
        def resource_access_policies(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionDefinitionPropsMixin.ResourceAccessPolicyProperty"]]]]:
            '''A list of the `resources <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourceinstance.html>`_ in the group that the function can access, with the corresponding read-only or read-write permissions. The maximum is 10 resources.

            .. epigraph::

               This property applies only for Lambda functions that run in a Greengrass container.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-environment.html#cfn-greengrass-functiondefinition-environment-resourceaccesspolicies
            '''
            result = self._values.get("resource_access_policies")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionDefinitionPropsMixin.ResourceAccessPolicyProperty"]]]], result)

        @builtins.property
        def variables(self) -> typing.Any:
            '''Environment variables for the Lambda function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-environment.html#cfn-greengrass-functiondefinition-environment-variables
            '''
            result = self._values.get("variables")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EnvironmentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnFunctionDefinitionPropsMixin.ExecutionProperty",
        jsii_struct_bases=[],
        name_mapping={"isolation_mode": "isolationMode", "run_as": "runAs"},
    )
    class ExecutionProperty:
        def __init__(
            self,
            *,
            isolation_mode: typing.Optional[builtins.str] = None,
            run_as: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionDefinitionPropsMixin.RunAsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Configuration settings for the Lambda execution environment on the AWS IoT Greengrass core.

            In an CloudFormation template, ``Execution`` is a property of the ```DefaultConfig`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-defaultconfig.html>`_ property type for a function definition version and the ```Environment`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-environment.html>`_ property type for a function.

            :param isolation_mode: The containerization that the Lambda function runs in. Valid values are ``GreengrassContainer`` or ``NoContainer`` . Typically, this is ``GreengrassContainer`` . For more information, see `Containerization <https://docs.aws.amazon.com/greengrass/v1/developerguide/lambda-group-config.html#lambda-function-containerization>`_ in the *Developer Guide* . - When set on the ```DefaultConfig`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-defaultconfig.html>`_ property of a function definition version, this setting is used as the default containerization for all Lambda functions in the function definition version. - When set on the ```Environment`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-environment.html>`_ property of a function, this setting applies to the individual function and overrides the default. Omit this value to run the function with the default containerization. .. epigraph:: We recommend that you run in a Greengrass container unless your business case requires that you run without containerization.
            :param run_as: The user and group permissions used to run the Lambda function. Typically, this is the ggc_user and ggc_group. For more information, see `Run as <https://docs.aws.amazon.com/greengrass/v1/developerguide/lambda-group-config.html#lambda-access-identity.html>`_ in the *Developer Guide* . - When set on the ```DefaultConfig`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-defaultconfig.html>`_ property of a function definition version, this setting is used as the default access identity for all Lambda functions in the function definition version. - When set on the ```Environment`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-environment.html>`_ property of a function, this setting applies to the individual function and overrides the default. You can override the user, group, or both. Omit this value to run the function with the default permissions. .. epigraph:: Running as the root user increases risks to your data and device. Do not run as root (UID/GID=0) unless your business case requires it. For more information and requirements, see `Running a Lambda Function as Root <https://docs.aws.amazon.com/greengrass/v1/developerguide/lambda-group-config.html#lambda-running-as-root>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-execution.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                execution_property = greengrass_mixins.CfnFunctionDefinitionPropsMixin.ExecutionProperty(
                    isolation_mode="isolationMode",
                    run_as=greengrass_mixins.CfnFunctionDefinitionPropsMixin.RunAsProperty(
                        gid=123,
                        uid=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9054d318b6b0e0fb3af5a1d95cced6ea85cb8978c841296916fad4ecd5b0f5b2)
                check_type(argname="argument isolation_mode", value=isolation_mode, expected_type=type_hints["isolation_mode"])
                check_type(argname="argument run_as", value=run_as, expected_type=type_hints["run_as"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if isolation_mode is not None:
                self._values["isolation_mode"] = isolation_mode
            if run_as is not None:
                self._values["run_as"] = run_as

        @builtins.property
        def isolation_mode(self) -> typing.Optional[builtins.str]:
            '''The containerization that the Lambda function runs in.

            Valid values are ``GreengrassContainer`` or ``NoContainer`` . Typically, this is ``GreengrassContainer`` . For more information, see `Containerization <https://docs.aws.amazon.com/greengrass/v1/developerguide/lambda-group-config.html#lambda-function-containerization>`_ in the *Developer Guide* .

            - When set on the ```DefaultConfig`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-defaultconfig.html>`_ property of a function definition version, this setting is used as the default containerization for all Lambda functions in the function definition version.
            - When set on the ```Environment`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-environment.html>`_ property of a function, this setting applies to the individual function and overrides the default. Omit this value to run the function with the default containerization.

            .. epigraph::

               We recommend that you run in a Greengrass container unless your business case requires that you run without containerization.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-execution.html#cfn-greengrass-functiondefinition-execution-isolationmode
            '''
            result = self._values.get("isolation_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def run_as(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionDefinitionPropsMixin.RunAsProperty"]]:
            '''The user and group permissions used to run the Lambda function.

            Typically, this is the ggc_user and ggc_group. For more information, see `Run as <https://docs.aws.amazon.com/greengrass/v1/developerguide/lambda-group-config.html#lambda-access-identity.html>`_ in the *Developer Guide* .

            - When set on the ```DefaultConfig`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-defaultconfig.html>`_ property of a function definition version, this setting is used as the default access identity for all Lambda functions in the function definition version.
            - When set on the ```Environment`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-environment.html>`_ property of a function, this setting applies to the individual function and overrides the default. You can override the user, group, or both. Omit this value to run the function with the default permissions.

            .. epigraph::

               Running as the root user increases risks to your data and device. Do not run as root (UID/GID=0) unless your business case requires it. For more information and requirements, see `Running a Lambda Function as Root <https://docs.aws.amazon.com/greengrass/v1/developerguide/lambda-group-config.html#lambda-running-as-root>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-execution.html#cfn-greengrass-functiondefinition-execution-runas
            '''
            result = self._values.get("run_as")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionDefinitionPropsMixin.RunAsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExecutionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnFunctionDefinitionPropsMixin.FunctionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "encoding_type": "encodingType",
            "environment": "environment",
            "exec_args": "execArgs",
            "executable": "executable",
            "memory_size": "memorySize",
            "pinned": "pinned",
            "timeout": "timeout",
        },
    )
    class FunctionConfigurationProperty:
        def __init__(
            self,
            *,
            encoding_type: typing.Optional[builtins.str] = None,
            environment: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionDefinitionPropsMixin.EnvironmentProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            exec_args: typing.Optional[builtins.str] = None,
            executable: typing.Optional[builtins.str] = None,
            memory_size: typing.Optional[jsii.Number] = None,
            pinned: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            timeout: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The group-specific configuration settings for a Lambda function.

            These settings configure the function's behavior in the Greengrass group. For more information, see `Controlling Execution of Greengrass Lambda Functions by Using Group-Specific Configuration <https://docs.aws.amazon.com/greengrass/v1/developerguide/lambda-group-config.html>`_ in the *Developer Guide* .

            In an CloudFormation template, ``FunctionConfiguration`` is a property of the ```Function`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-function.html>`_ property type.

            :param encoding_type: The expected encoding type of the input payload for the function. Valid values are ``json`` (default) and ``binary`` .
            :param environment: The environment configuration of the function.
            :param exec_args: The execution arguments.
            :param executable: The name of the function executable.
            :param memory_size: The memory size (in KB) required by the function. .. epigraph:: This property applies only to Lambda functions that run in a Greengrass container.
            :param pinned: Indicates whether the function is pinned (or *long-lived* ). Pinned functions start when the core starts and process all requests in the same container. The default value is false.
            :param timeout: The allowed execution time (in seconds) after which the function should terminate. For pinned functions, this timeout applies for each request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-functionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                # variables: Any
                
                function_configuration_property = greengrass_mixins.CfnFunctionDefinitionPropsMixin.FunctionConfigurationProperty(
                    encoding_type="encodingType",
                    environment=greengrass_mixins.CfnFunctionDefinitionPropsMixin.EnvironmentProperty(
                        access_sysfs=False,
                        execution=greengrass_mixins.CfnFunctionDefinitionPropsMixin.ExecutionProperty(
                            isolation_mode="isolationMode",
                            run_as=greengrass_mixins.CfnFunctionDefinitionPropsMixin.RunAsProperty(
                                gid=123,
                                uid=123
                            )
                        ),
                        resource_access_policies=[greengrass_mixins.CfnFunctionDefinitionPropsMixin.ResourceAccessPolicyProperty(
                            permission="permission",
                            resource_id="resourceId"
                        )],
                        variables=variables
                    ),
                    exec_args="execArgs",
                    executable="executable",
                    memory_size=123,
                    pinned=False,
                    timeout=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__56afe81deb77f187f00a0efe5c0fe13febeed01db0c2c4f991ab4322d38a3a19)
                check_type(argname="argument encoding_type", value=encoding_type, expected_type=type_hints["encoding_type"])
                check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
                check_type(argname="argument exec_args", value=exec_args, expected_type=type_hints["exec_args"])
                check_type(argname="argument executable", value=executable, expected_type=type_hints["executable"])
                check_type(argname="argument memory_size", value=memory_size, expected_type=type_hints["memory_size"])
                check_type(argname="argument pinned", value=pinned, expected_type=type_hints["pinned"])
                check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encoding_type is not None:
                self._values["encoding_type"] = encoding_type
            if environment is not None:
                self._values["environment"] = environment
            if exec_args is not None:
                self._values["exec_args"] = exec_args
            if executable is not None:
                self._values["executable"] = executable
            if memory_size is not None:
                self._values["memory_size"] = memory_size
            if pinned is not None:
                self._values["pinned"] = pinned
            if timeout is not None:
                self._values["timeout"] = timeout

        @builtins.property
        def encoding_type(self) -> typing.Optional[builtins.str]:
            '''The expected encoding type of the input payload for the function.

            Valid values are ``json`` (default) and ``binary`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-functionconfiguration.html#cfn-greengrass-functiondefinition-functionconfiguration-encodingtype
            '''
            result = self._values.get("encoding_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def environment(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionDefinitionPropsMixin.EnvironmentProperty"]]:
            '''The environment configuration of the function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-functionconfiguration.html#cfn-greengrass-functiondefinition-functionconfiguration-environment
            '''
            result = self._values.get("environment")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionDefinitionPropsMixin.EnvironmentProperty"]], result)

        @builtins.property
        def exec_args(self) -> typing.Optional[builtins.str]:
            '''The execution arguments.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-functionconfiguration.html#cfn-greengrass-functiondefinition-functionconfiguration-execargs
            '''
            result = self._values.get("exec_args")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def executable(self) -> typing.Optional[builtins.str]:
            '''The name of the function executable.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-functionconfiguration.html#cfn-greengrass-functiondefinition-functionconfiguration-executable
            '''
            result = self._values.get("executable")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def memory_size(self) -> typing.Optional[jsii.Number]:
            '''The memory size (in KB) required by the function.

            .. epigraph::

               This property applies only to Lambda functions that run in a Greengrass container.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-functionconfiguration.html#cfn-greengrass-functiondefinition-functionconfiguration-memorysize
            '''
            result = self._values.get("memory_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def pinned(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether the function is pinned (or *long-lived* ).

            Pinned functions start when the core starts and process all requests in the same container. The default value is false.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-functionconfiguration.html#cfn-greengrass-functiondefinition-functionconfiguration-pinned
            '''
            result = self._values.get("pinned")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def timeout(self) -> typing.Optional[jsii.Number]:
            '''The allowed execution time (in seconds) after which the function should terminate.

            For pinned functions, this timeout applies for each request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-functionconfiguration.html#cfn-greengrass-functiondefinition-functionconfiguration-timeout
            '''
            result = self._values.get("timeout")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FunctionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnFunctionDefinitionPropsMixin.FunctionDefinitionVersionProperty",
        jsii_struct_bases=[],
        name_mapping={"default_config": "defaultConfig", "functions": "functions"},
    )
    class FunctionDefinitionVersionProperty:
        def __init__(
            self,
            *,
            default_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionDefinitionPropsMixin.DefaultConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            functions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionDefinitionPropsMixin.FunctionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''A function definition version contains a list of functions.

            .. epigraph::

               After you create a function definition version that contains the functions you want to deploy, you must add it to your group version. For more information, see ```AWS::Greengrass::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html>`_ .

            In an CloudFormation template, ``FunctionDefinitionVersion`` is the property type of the ``InitialVersion`` property in the ```AWS::Greengrass::FunctionDefinition`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-functiondefinition.html>`_ resource.

            :param default_config: The default configuration that applies to all Lambda functions in the group. Individual Lambda functions can override these settings.
            :param functions: The functions in this version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-functiondefinitionversion.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                # variables: Any
                
                function_definition_version_property = greengrass_mixins.CfnFunctionDefinitionPropsMixin.FunctionDefinitionVersionProperty(
                    default_config=greengrass_mixins.CfnFunctionDefinitionPropsMixin.DefaultConfigProperty(
                        execution=greengrass_mixins.CfnFunctionDefinitionPropsMixin.ExecutionProperty(
                            isolation_mode="isolationMode",
                            run_as=greengrass_mixins.CfnFunctionDefinitionPropsMixin.RunAsProperty(
                                gid=123,
                                uid=123
                            )
                        )
                    ),
                    functions=[greengrass_mixins.CfnFunctionDefinitionPropsMixin.FunctionProperty(
                        function_arn="functionArn",
                        function_configuration=greengrass_mixins.CfnFunctionDefinitionPropsMixin.FunctionConfigurationProperty(
                            encoding_type="encodingType",
                            environment=greengrass_mixins.CfnFunctionDefinitionPropsMixin.EnvironmentProperty(
                                access_sysfs=False,
                                execution=greengrass_mixins.CfnFunctionDefinitionPropsMixin.ExecutionProperty(
                                    isolation_mode="isolationMode",
                                    run_as=greengrass_mixins.CfnFunctionDefinitionPropsMixin.RunAsProperty(
                                        gid=123,
                                        uid=123
                                    )
                                ),
                                resource_access_policies=[greengrass_mixins.CfnFunctionDefinitionPropsMixin.ResourceAccessPolicyProperty(
                                    permission="permission",
                                    resource_id="resourceId"
                                )],
                                variables=variables
                            ),
                            exec_args="execArgs",
                            executable="executable",
                            memory_size=123,
                            pinned=False,
                            timeout=123
                        ),
                        id="id"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1cb7be51cbd722ee899144c963c7328c7295c39dd8bc365601412af901ee54ec)
                check_type(argname="argument default_config", value=default_config, expected_type=type_hints["default_config"])
                check_type(argname="argument functions", value=functions, expected_type=type_hints["functions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if default_config is not None:
                self._values["default_config"] = default_config
            if functions is not None:
                self._values["functions"] = functions

        @builtins.property
        def default_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionDefinitionPropsMixin.DefaultConfigProperty"]]:
            '''The default configuration that applies to all Lambda functions in the group.

            Individual Lambda functions can override these settings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-functiondefinitionversion.html#cfn-greengrass-functiondefinition-functiondefinitionversion-defaultconfig
            '''
            result = self._values.get("default_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionDefinitionPropsMixin.DefaultConfigProperty"]], result)

        @builtins.property
        def functions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionDefinitionPropsMixin.FunctionProperty"]]]]:
            '''The functions in this version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-functiondefinitionversion.html#cfn-greengrass-functiondefinition-functiondefinitionversion-functions
            '''
            result = self._values.get("functions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionDefinitionPropsMixin.FunctionProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FunctionDefinitionVersionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnFunctionDefinitionPropsMixin.FunctionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "function_arn": "functionArn",
            "function_configuration": "functionConfiguration",
            "id": "id",
        },
    )
    class FunctionProperty:
        def __init__(
            self,
            *,
            function_arn: typing.Optional[builtins.str] = None,
            function_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionDefinitionPropsMixin.FunctionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A function is a Lambda function that's referenced from an AWS IoT Greengrass group.

            The function is deployed to a Greengrass core where it runs locally. For more information, see `Run Lambda Functions on the AWS IoT Greengrass Core <https://docs.aws.amazon.com/greengrass/v1/developerguide/lambda-functions.html>`_ in the *Developer Guide* .

            In an CloudFormation template, the ``Functions`` property of the ```FunctionDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-functiondefinitionversion.html>`_ property type contains a list of ``Function`` property types.

            :param function_arn: The Amazon Resource Name (ARN) of the alias (recommended) or version of the referenced Lambda function.
            :param function_configuration: The group-specific settings of the Lambda function. These settings configure the function's behavior in the Greengrass group.
            :param id: A descriptive or arbitrary ID for the function. This value must be unique within the function definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-function.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                # variables: Any
                
                function_property = greengrass_mixins.CfnFunctionDefinitionPropsMixin.FunctionProperty(
                    function_arn="functionArn",
                    function_configuration=greengrass_mixins.CfnFunctionDefinitionPropsMixin.FunctionConfigurationProperty(
                        encoding_type="encodingType",
                        environment=greengrass_mixins.CfnFunctionDefinitionPropsMixin.EnvironmentProperty(
                            access_sysfs=False,
                            execution=greengrass_mixins.CfnFunctionDefinitionPropsMixin.ExecutionProperty(
                                isolation_mode="isolationMode",
                                run_as=greengrass_mixins.CfnFunctionDefinitionPropsMixin.RunAsProperty(
                                    gid=123,
                                    uid=123
                                )
                            ),
                            resource_access_policies=[greengrass_mixins.CfnFunctionDefinitionPropsMixin.ResourceAccessPolicyProperty(
                                permission="permission",
                                resource_id="resourceId"
                            )],
                            variables=variables
                        ),
                        exec_args="execArgs",
                        executable="executable",
                        memory_size=123,
                        pinned=False,
                        timeout=123
                    ),
                    id="id"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__deaa419483dc0ce7d7f542d404c94d81af0680e1c74fb46d8a83bedf450fd03f)
                check_type(argname="argument function_arn", value=function_arn, expected_type=type_hints["function_arn"])
                check_type(argname="argument function_configuration", value=function_configuration, expected_type=type_hints["function_configuration"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if function_arn is not None:
                self._values["function_arn"] = function_arn
            if function_configuration is not None:
                self._values["function_configuration"] = function_configuration
            if id is not None:
                self._values["id"] = id

        @builtins.property
        def function_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the alias (recommended) or version of the referenced Lambda function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-function.html#cfn-greengrass-functiondefinition-function-functionarn
            '''
            result = self._values.get("function_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def function_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionDefinitionPropsMixin.FunctionConfigurationProperty"]]:
            '''The group-specific settings of the Lambda function.

            These settings configure the function's behavior in the Greengrass group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-function.html#cfn-greengrass-functiondefinition-function-functionconfiguration
            '''
            result = self._values.get("function_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionDefinitionPropsMixin.FunctionConfigurationProperty"]], result)

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''A descriptive or arbitrary ID for the function.

            This value must be unique within the function definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-function.html#cfn-greengrass-functiondefinition-function-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FunctionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnFunctionDefinitionPropsMixin.ResourceAccessPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"permission": "permission", "resource_id": "resourceId"},
    )
    class ResourceAccessPolicyProperty:
        def __init__(
            self,
            *,
            permission: typing.Optional[builtins.str] = None,
            resource_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A list of the `resources <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourceinstance.html>`_ in the group that the function can access, with the corresponding read-only or read-write permissions. The maximum is 10 resources.

            .. epigraph::

               This property applies only to Lambda functions that run in a Greengrass container.

            In an CloudFormation template, ``ResourceAccessPolicy`` is a property of the ```Environment`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-environment.html>`_ property type.

            :param permission: The read-only or read-write access that the Lambda function has to the resource. Valid values are ``ro`` or ``rw`` .
            :param resource_id: The ID of the resource. This ID is assigned to the resource when you create the resource definition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-resourceaccesspolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                resource_access_policy_property = greengrass_mixins.CfnFunctionDefinitionPropsMixin.ResourceAccessPolicyProperty(
                    permission="permission",
                    resource_id="resourceId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__54736471e1fd9485c2b5be546915791c0bab7f35f24a2c594fcb46a6e2097a95)
                check_type(argname="argument permission", value=permission, expected_type=type_hints["permission"])
                check_type(argname="argument resource_id", value=resource_id, expected_type=type_hints["resource_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if permission is not None:
                self._values["permission"] = permission
            if resource_id is not None:
                self._values["resource_id"] = resource_id

        @builtins.property
        def permission(self) -> typing.Optional[builtins.str]:
            '''The read-only or read-write access that the Lambda function has to the resource.

            Valid values are ``ro`` or ``rw`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-resourceaccesspolicy.html#cfn-greengrass-functiondefinition-resourceaccesspolicy-permission
            '''
            result = self._values.get("permission")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the resource.

            This ID is assigned to the resource when you create the resource definition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-resourceaccesspolicy.html#cfn-greengrass-functiondefinition-resourceaccesspolicy-resourceid
            '''
            result = self._values.get("resource_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceAccessPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnFunctionDefinitionPropsMixin.RunAsProperty",
        jsii_struct_bases=[],
        name_mapping={"gid": "gid", "uid": "uid"},
    )
    class RunAsProperty:
        def __init__(
            self,
            *,
            gid: typing.Optional[jsii.Number] = None,
            uid: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The access identity whose permissions are used to run the Lambda function.

            This setting overrides the default access identity that's specified for the group (by default, ggc_user and ggc_group). You can override the user, group, or both. For more information, see `Run as <https://docs.aws.amazon.com/greengrass/v1/developerguide/lambda-group-config.html#lambda-access-identity.html>`_ in the *Developer Guide* .
            .. epigraph::

               Running as the root user increases risks to your data and device. Do not run as root (UID/GID=0) unless your business case requires it. For more information and requirements, see `Running a Lambda Function as Root <https://docs.aws.amazon.com/greengrass/v1/developerguide/lambda-group-config.html#lambda-running-as-root>`_ .

            In an CloudFormation template, ``RunAs`` is a property of the ```Execution`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-execution.html>`_ property type.

            :param gid: The group ID whose permissions are used to run the Lambda function. You can use the ``getent group`` command on your core device to look up the group ID.
            :param uid: The user ID whose permissions are used to run the Lambda function. You can use the ``getent passwd`` command on your core device to look up the user ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-runas.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                run_as_property = greengrass_mixins.CfnFunctionDefinitionPropsMixin.RunAsProperty(
                    gid=123,
                    uid=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6d177fd4caed497b9c4bc5deafc1de7872ba74e4f879dd40c917431c270981ad)
                check_type(argname="argument gid", value=gid, expected_type=type_hints["gid"])
                check_type(argname="argument uid", value=uid, expected_type=type_hints["uid"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if gid is not None:
                self._values["gid"] = gid
            if uid is not None:
                self._values["uid"] = uid

        @builtins.property
        def gid(self) -> typing.Optional[jsii.Number]:
            '''The group ID whose permissions are used to run the Lambda function.

            You can use the ``getent group`` command on your core device to look up the group ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-runas.html#cfn-greengrass-functiondefinition-runas-gid
            '''
            result = self._values.get("gid")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def uid(self) -> typing.Optional[jsii.Number]:
            '''The user ID whose permissions are used to run the Lambda function.

            You can use the ``getent passwd`` command on your core device to look up the user ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-runas.html#cfn-greengrass-functiondefinition-runas-uid
            '''
            result = self._values.get("uid")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RunAsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnFunctionDefinitionVersionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "default_config": "defaultConfig",
        "function_definition_id": "functionDefinitionId",
        "functions": "functions",
    },
)
class CfnFunctionDefinitionVersionMixinProps:
    def __init__(
        self,
        *,
        default_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionDefinitionVersionPropsMixin.DefaultConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        function_definition_id: typing.Optional[builtins.str] = None,
        functions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionDefinitionVersionPropsMixin.FunctionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnFunctionDefinitionVersionPropsMixin.

        :param default_config: The default configuration that applies to all Lambda functions in the group. Individual Lambda functions can override these settings.
        :param function_definition_id: The ID of the function definition associated with this version. This value is a GUID.
        :param functions: The functions in this version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-functiondefinitionversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
            
            # variables: Any
            
            cfn_function_definition_version_mixin_props = greengrass_mixins.CfnFunctionDefinitionVersionMixinProps(
                default_config=greengrass_mixins.CfnFunctionDefinitionVersionPropsMixin.DefaultConfigProperty(
                    execution=greengrass_mixins.CfnFunctionDefinitionVersionPropsMixin.ExecutionProperty(
                        isolation_mode="isolationMode",
                        run_as=greengrass_mixins.CfnFunctionDefinitionVersionPropsMixin.RunAsProperty(
                            gid=123,
                            uid=123
                        )
                    )
                ),
                function_definition_id="functionDefinitionId",
                functions=[greengrass_mixins.CfnFunctionDefinitionVersionPropsMixin.FunctionProperty(
                    function_arn="functionArn",
                    function_configuration=greengrass_mixins.CfnFunctionDefinitionVersionPropsMixin.FunctionConfigurationProperty(
                        encoding_type="encodingType",
                        environment=greengrass_mixins.CfnFunctionDefinitionVersionPropsMixin.EnvironmentProperty(
                            access_sysfs=False,
                            execution=greengrass_mixins.CfnFunctionDefinitionVersionPropsMixin.ExecutionProperty(
                                isolation_mode="isolationMode",
                                run_as=greengrass_mixins.CfnFunctionDefinitionVersionPropsMixin.RunAsProperty(
                                    gid=123,
                                    uid=123
                                )
                            ),
                            resource_access_policies=[greengrass_mixins.CfnFunctionDefinitionVersionPropsMixin.ResourceAccessPolicyProperty(
                                permission="permission",
                                resource_id="resourceId"
                            )],
                            variables=variables
                        ),
                        exec_args="execArgs",
                        executable="executable",
                        memory_size=123,
                        pinned=False,
                        timeout=123
                    ),
                    id="id"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d811cf337e0b6ebcf06d55ad5167305d47778dc675a0ae8539863345f807e03b)
            check_type(argname="argument default_config", value=default_config, expected_type=type_hints["default_config"])
            check_type(argname="argument function_definition_id", value=function_definition_id, expected_type=type_hints["function_definition_id"])
            check_type(argname="argument functions", value=functions, expected_type=type_hints["functions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default_config is not None:
            self._values["default_config"] = default_config
        if function_definition_id is not None:
            self._values["function_definition_id"] = function_definition_id
        if functions is not None:
            self._values["functions"] = functions

    @builtins.property
    def default_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionDefinitionVersionPropsMixin.DefaultConfigProperty"]]:
        '''The default configuration that applies to all Lambda functions in the group.

        Individual Lambda functions can override these settings.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-functiondefinitionversion.html#cfn-greengrass-functiondefinitionversion-defaultconfig
        '''
        result = self._values.get("default_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionDefinitionVersionPropsMixin.DefaultConfigProperty"]], result)

    @builtins.property
    def function_definition_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the function definition associated with this version.

        This value is a GUID.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-functiondefinitionversion.html#cfn-greengrass-functiondefinitionversion-functiondefinitionid
        '''
        result = self._values.get("function_definition_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def functions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionDefinitionVersionPropsMixin.FunctionProperty"]]]]:
        '''The functions in this version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-functiondefinitionversion.html#cfn-greengrass-functiondefinitionversion-functions
        '''
        result = self._values.get("functions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionDefinitionVersionPropsMixin.FunctionProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFunctionDefinitionVersionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnFunctionDefinitionVersionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnFunctionDefinitionVersionPropsMixin",
):
    '''The ``AWS::Greengrass::FunctionDefinitionVersion`` resource represents a function definition version for AWS IoT Greengrass .

    A function definition version contains contain a list of functions.
    .. epigraph::

       To create a function definition version, you must specify the ID of the function definition that you want to associate with the version. For information about creating a function definition, see ```AWS::Greengrass::FunctionDefinition`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-functiondefinition.html>`_ .

       After you create a function definition version that contains the functions you want to deploy, you must add it to your group version. For more information, see ```AWS::Greengrass::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-functiondefinitionversion.html
    :cloudformationResource: AWS::Greengrass::FunctionDefinitionVersion
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
        
        # variables: Any
        
        cfn_function_definition_version_props_mixin = greengrass_mixins.CfnFunctionDefinitionVersionPropsMixin(greengrass_mixins.CfnFunctionDefinitionVersionMixinProps(
            default_config=greengrass_mixins.CfnFunctionDefinitionVersionPropsMixin.DefaultConfigProperty(
                execution=greengrass_mixins.CfnFunctionDefinitionVersionPropsMixin.ExecutionProperty(
                    isolation_mode="isolationMode",
                    run_as=greengrass_mixins.CfnFunctionDefinitionVersionPropsMixin.RunAsProperty(
                        gid=123,
                        uid=123
                    )
                )
            ),
            function_definition_id="functionDefinitionId",
            functions=[greengrass_mixins.CfnFunctionDefinitionVersionPropsMixin.FunctionProperty(
                function_arn="functionArn",
                function_configuration=greengrass_mixins.CfnFunctionDefinitionVersionPropsMixin.FunctionConfigurationProperty(
                    encoding_type="encodingType",
                    environment=greengrass_mixins.CfnFunctionDefinitionVersionPropsMixin.EnvironmentProperty(
                        access_sysfs=False,
                        execution=greengrass_mixins.CfnFunctionDefinitionVersionPropsMixin.ExecutionProperty(
                            isolation_mode="isolationMode",
                            run_as=greengrass_mixins.CfnFunctionDefinitionVersionPropsMixin.RunAsProperty(
                                gid=123,
                                uid=123
                            )
                        ),
                        resource_access_policies=[greengrass_mixins.CfnFunctionDefinitionVersionPropsMixin.ResourceAccessPolicyProperty(
                            permission="permission",
                            resource_id="resourceId"
                        )],
                        variables=variables
                    ),
                    exec_args="execArgs",
                    executable="executable",
                    memory_size=123,
                    pinned=False,
                    timeout=123
                ),
                id="id"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnFunctionDefinitionVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Greengrass::FunctionDefinitionVersion``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a039f77f3a430812fc8e4af444955baac95da91ffc6dfd8246555e14c3cf42a4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__91c92725d22fa4ae957b06a610fcbf1c4aca71633f5cf3e5333c52156af1e5f0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29de5e90428ecc574a3311208ef10e47ca62a5ef248ad9716383958e73e5c329)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnFunctionDefinitionVersionMixinProps:
        return typing.cast(CfnFunctionDefinitionVersionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnFunctionDefinitionVersionPropsMixin.DefaultConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"execution": "execution"},
    )
    class DefaultConfigProperty:
        def __init__(
            self,
            *,
            execution: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionDefinitionVersionPropsMixin.ExecutionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The default configuration that applies to all Lambda functions in the function definition version.

            Individual Lambda functions can override these settings.

            In an CloudFormation template, ``DefaultConfig`` is a property of the ```AWS::Greengrass::FunctionDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-functiondefinitionversion.html>`_ resource.

            :param execution: Configuration settings for the Lambda execution environment on the AWS IoT Greengrass core.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-defaultconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                default_config_property = greengrass_mixins.CfnFunctionDefinitionVersionPropsMixin.DefaultConfigProperty(
                    execution=greengrass_mixins.CfnFunctionDefinitionVersionPropsMixin.ExecutionProperty(
                        isolation_mode="isolationMode",
                        run_as=greengrass_mixins.CfnFunctionDefinitionVersionPropsMixin.RunAsProperty(
                            gid=123,
                            uid=123
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cc793b2556a3f488869f1c5ca9f394e85ff8be9d464adadc91fe88c81e01a9ea)
                check_type(argname="argument execution", value=execution, expected_type=type_hints["execution"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if execution is not None:
                self._values["execution"] = execution

        @builtins.property
        def execution(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionDefinitionVersionPropsMixin.ExecutionProperty"]]:
            '''Configuration settings for the Lambda execution environment on the AWS IoT Greengrass core.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-defaultconfig.html#cfn-greengrass-functiondefinitionversion-defaultconfig-execution
            '''
            result = self._values.get("execution")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionDefinitionVersionPropsMixin.ExecutionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DefaultConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnFunctionDefinitionVersionPropsMixin.EnvironmentProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_sysfs": "accessSysfs",
            "execution": "execution",
            "resource_access_policies": "resourceAccessPolicies",
            "variables": "variables",
        },
    )
    class EnvironmentProperty:
        def __init__(
            self,
            *,
            access_sysfs: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            execution: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionDefinitionVersionPropsMixin.ExecutionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            resource_access_policies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionDefinitionVersionPropsMixin.ResourceAccessPolicyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            variables: typing.Any = None,
        ) -> None:
            '''The environment configuration for a Lambda function on the AWS IoT Greengrass core.

            In an CloudFormation template, ``Environment`` is a property of the ```FunctionConfiguration`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-functionconfiguration.html>`_ property type.

            :param access_sysfs: Indicates whether the function is allowed to access the ``/sys`` directory on the core device, which allows the read device information from ``/sys`` . .. epigraph:: This property applies only to Lambda functions that run in a Greengrass container.
            :param execution: Settings for the Lambda execution environment in AWS IoT Greengrass .
            :param resource_access_policies: A list of the `resources <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourceinstance.html>`_ in the group that the function can access, with the corresponding read-only or read-write permissions. The maximum is 10 resources. .. epigraph:: This property applies only to Lambda functions that run in a Greengrass container.
            :param variables: Environment variables for the Lambda function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-environment.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                # variables: Any
                
                environment_property = greengrass_mixins.CfnFunctionDefinitionVersionPropsMixin.EnvironmentProperty(
                    access_sysfs=False,
                    execution=greengrass_mixins.CfnFunctionDefinitionVersionPropsMixin.ExecutionProperty(
                        isolation_mode="isolationMode",
                        run_as=greengrass_mixins.CfnFunctionDefinitionVersionPropsMixin.RunAsProperty(
                            gid=123,
                            uid=123
                        )
                    ),
                    resource_access_policies=[greengrass_mixins.CfnFunctionDefinitionVersionPropsMixin.ResourceAccessPolicyProperty(
                        permission="permission",
                        resource_id="resourceId"
                    )],
                    variables=variables
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__189a691d38edbdad466d8da7a8541a0f832bd04938ced99f567194298f7c76c0)
                check_type(argname="argument access_sysfs", value=access_sysfs, expected_type=type_hints["access_sysfs"])
                check_type(argname="argument execution", value=execution, expected_type=type_hints["execution"])
                check_type(argname="argument resource_access_policies", value=resource_access_policies, expected_type=type_hints["resource_access_policies"])
                check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_sysfs is not None:
                self._values["access_sysfs"] = access_sysfs
            if execution is not None:
                self._values["execution"] = execution
            if resource_access_policies is not None:
                self._values["resource_access_policies"] = resource_access_policies
            if variables is not None:
                self._values["variables"] = variables

        @builtins.property
        def access_sysfs(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether the function is allowed to access the ``/sys`` directory on the core device, which allows the read device information from ``/sys`` .

            .. epigraph::

               This property applies only to Lambda functions that run in a Greengrass container.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-environment.html#cfn-greengrass-functiondefinitionversion-environment-accesssysfs
            '''
            result = self._values.get("access_sysfs")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def execution(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionDefinitionVersionPropsMixin.ExecutionProperty"]]:
            '''Settings for the Lambda execution environment in AWS IoT Greengrass .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-environment.html#cfn-greengrass-functiondefinitionversion-environment-execution
            '''
            result = self._values.get("execution")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionDefinitionVersionPropsMixin.ExecutionProperty"]], result)

        @builtins.property
        def resource_access_policies(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionDefinitionVersionPropsMixin.ResourceAccessPolicyProperty"]]]]:
            '''A list of the `resources <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourceinstance.html>`_ in the group that the function can access, with the corresponding read-only or read-write permissions. The maximum is 10 resources.

            .. epigraph::

               This property applies only to Lambda functions that run in a Greengrass container.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-environment.html#cfn-greengrass-functiondefinitionversion-environment-resourceaccesspolicies
            '''
            result = self._values.get("resource_access_policies")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionDefinitionVersionPropsMixin.ResourceAccessPolicyProperty"]]]], result)

        @builtins.property
        def variables(self) -> typing.Any:
            '''Environment variables for the Lambda function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-environment.html#cfn-greengrass-functiondefinitionversion-environment-variables
            '''
            result = self._values.get("variables")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EnvironmentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnFunctionDefinitionVersionPropsMixin.ExecutionProperty",
        jsii_struct_bases=[],
        name_mapping={"isolation_mode": "isolationMode", "run_as": "runAs"},
    )
    class ExecutionProperty:
        def __init__(
            self,
            *,
            isolation_mode: typing.Optional[builtins.str] = None,
            run_as: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionDefinitionVersionPropsMixin.RunAsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Configuration settings for the Lambda execution environment on the AWS IoT Greengrass core.

            In an CloudFormation template, ``Execution`` is a property of the ```DefaultConfig`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-defaultconfig.html>`_ property type for a function definition version and the ```Environment`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-environment.html>`_ property type for a function.

            :param isolation_mode: The containerization that the Lambda function runs in. Valid values are ``GreengrassContainer`` or ``NoContainer`` . Typically, this is ``GreengrassContainer`` . For more information, see `Containerization <https://docs.aws.amazon.com/greengrass/v1/developerguide/lambda-group-config.html#lambda-function-containerization>`_ in the *Developer Guide* . - When set on the ```DefaultConfig`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-defaultconfig.html>`_ property of a function definition version, this setting is used as the default containerization for all Lambda functions in the function definition version. - When set on the ```Environment`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-environment.html>`_ property of a function, this setting applies to the individual function and overrides the default. Omit this value to run the function with the default containerization. .. epigraph:: We recommend that you run in a Greengrass container unless your business case requires that you run without containerization.
            :param run_as: The user and group permissions used to run the Lambda function. Typically, this is the ggc_user and ggc_group. For more information, see `Run as <https://docs.aws.amazon.com/greengrass/v1/developerguide/lambda-group-config.html#lambda-access-identity.html>`_ in the *Developer Guide* . - When set on the ```DefaultConfig`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-defaultconfig.html>`_ property of a function definition version, this setting is used as the default access identity for all Lambda functions in the function definition version. - When set on the ```Environment`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-environment.html>`_ property of a function, this setting applies to the individual function and overrides the default. You can override the user, group, or both. Omit this value to run the function with the default permissions. .. epigraph:: Running as the root user increases risks to your data and device. Do not run as root (UID/GID=0) unless your business case requires it. For more information and requirements, see `Running a Lambda Function as Root <https://docs.aws.amazon.com/greengrass/v1/developerguide/lambda-group-config.html#lambda-running-as-root>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-execution.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                execution_property = greengrass_mixins.CfnFunctionDefinitionVersionPropsMixin.ExecutionProperty(
                    isolation_mode="isolationMode",
                    run_as=greengrass_mixins.CfnFunctionDefinitionVersionPropsMixin.RunAsProperty(
                        gid=123,
                        uid=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e7cfdf69518effd74ab056c5e588c6e02927404315ddd856539884e49b1eafcb)
                check_type(argname="argument isolation_mode", value=isolation_mode, expected_type=type_hints["isolation_mode"])
                check_type(argname="argument run_as", value=run_as, expected_type=type_hints["run_as"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if isolation_mode is not None:
                self._values["isolation_mode"] = isolation_mode
            if run_as is not None:
                self._values["run_as"] = run_as

        @builtins.property
        def isolation_mode(self) -> typing.Optional[builtins.str]:
            '''The containerization that the Lambda function runs in.

            Valid values are ``GreengrassContainer`` or ``NoContainer`` . Typically, this is ``GreengrassContainer`` . For more information, see `Containerization <https://docs.aws.amazon.com/greengrass/v1/developerguide/lambda-group-config.html#lambda-function-containerization>`_ in the *Developer Guide* .

            - When set on the ```DefaultConfig`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-defaultconfig.html>`_ property of a function definition version, this setting is used as the default containerization for all Lambda functions in the function definition version.
            - When set on the ```Environment`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-environment.html>`_ property of a function, this setting applies to the individual function and overrides the default. Omit this value to run the function with the default containerization.

            .. epigraph::

               We recommend that you run in a Greengrass container unless your business case requires that you run without containerization.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-execution.html#cfn-greengrass-functiondefinitionversion-execution-isolationmode
            '''
            result = self._values.get("isolation_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def run_as(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionDefinitionVersionPropsMixin.RunAsProperty"]]:
            '''The user and group permissions used to run the Lambda function.

            Typically, this is the ggc_user and ggc_group. For more information, see `Run as <https://docs.aws.amazon.com/greengrass/v1/developerguide/lambda-group-config.html#lambda-access-identity.html>`_ in the *Developer Guide* .

            - When set on the ```DefaultConfig`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-defaultconfig.html>`_ property of a function definition version, this setting is used as the default access identity for all Lambda functions in the function definition version.
            - When set on the ```Environment`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-environment.html>`_ property of a function, this setting applies to the individual function and overrides the default. You can override the user, group, or both. Omit this value to run the function with the default permissions.

            .. epigraph::

               Running as the root user increases risks to your data and device. Do not run as root (UID/GID=0) unless your business case requires it. For more information and requirements, see `Running a Lambda Function as Root <https://docs.aws.amazon.com/greengrass/v1/developerguide/lambda-group-config.html#lambda-running-as-root>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-execution.html#cfn-greengrass-functiondefinitionversion-execution-runas
            '''
            result = self._values.get("run_as")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionDefinitionVersionPropsMixin.RunAsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExecutionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnFunctionDefinitionVersionPropsMixin.FunctionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "encoding_type": "encodingType",
            "environment": "environment",
            "exec_args": "execArgs",
            "executable": "executable",
            "memory_size": "memorySize",
            "pinned": "pinned",
            "timeout": "timeout",
        },
    )
    class FunctionConfigurationProperty:
        def __init__(
            self,
            *,
            encoding_type: typing.Optional[builtins.str] = None,
            environment: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionDefinitionVersionPropsMixin.EnvironmentProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            exec_args: typing.Optional[builtins.str] = None,
            executable: typing.Optional[builtins.str] = None,
            memory_size: typing.Optional[jsii.Number] = None,
            pinned: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            timeout: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The group-specific configuration settings for a Lambda function.

            These settings configure the function's behavior in the Greengrass group. For more information, see `Controlling Execution of Greengrass Lambda Functions by Using Group-Specific Configuration <https://docs.aws.amazon.com/greengrass/v1/developerguide/lambda-group-config.html>`_ in the *Developer Guide* .

            In an CloudFormation template, ``FunctionConfiguration`` is a property of the ```Function`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-function.html>`_ property type.

            :param encoding_type: The expected encoding type of the input payload for the function. Valid values are ``json`` (default) and ``binary`` .
            :param environment: The environment configuration of the function.
            :param exec_args: The execution arguments.
            :param executable: The name of the function executable.
            :param memory_size: The memory size (in KB) required by the function. .. epigraph:: This property applies only to Lambda functions that run in a Greengrass container.
            :param pinned: Indicates whether the function is pinned (or *long-lived* ). Pinned functions start when the core starts and process all requests in the same container. The default value is false.
            :param timeout: The allowed execution time (in seconds) after which the function should terminate. For pinned functions, this timeout applies for each request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-functionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                # variables: Any
                
                function_configuration_property = greengrass_mixins.CfnFunctionDefinitionVersionPropsMixin.FunctionConfigurationProperty(
                    encoding_type="encodingType",
                    environment=greengrass_mixins.CfnFunctionDefinitionVersionPropsMixin.EnvironmentProperty(
                        access_sysfs=False,
                        execution=greengrass_mixins.CfnFunctionDefinitionVersionPropsMixin.ExecutionProperty(
                            isolation_mode="isolationMode",
                            run_as=greengrass_mixins.CfnFunctionDefinitionVersionPropsMixin.RunAsProperty(
                                gid=123,
                                uid=123
                            )
                        ),
                        resource_access_policies=[greengrass_mixins.CfnFunctionDefinitionVersionPropsMixin.ResourceAccessPolicyProperty(
                            permission="permission",
                            resource_id="resourceId"
                        )],
                        variables=variables
                    ),
                    exec_args="execArgs",
                    executable="executable",
                    memory_size=123,
                    pinned=False,
                    timeout=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__62356aa46ccb51619743fa732427bfcad665114c63941b941a10e86f2abc22c0)
                check_type(argname="argument encoding_type", value=encoding_type, expected_type=type_hints["encoding_type"])
                check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
                check_type(argname="argument exec_args", value=exec_args, expected_type=type_hints["exec_args"])
                check_type(argname="argument executable", value=executable, expected_type=type_hints["executable"])
                check_type(argname="argument memory_size", value=memory_size, expected_type=type_hints["memory_size"])
                check_type(argname="argument pinned", value=pinned, expected_type=type_hints["pinned"])
                check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encoding_type is not None:
                self._values["encoding_type"] = encoding_type
            if environment is not None:
                self._values["environment"] = environment
            if exec_args is not None:
                self._values["exec_args"] = exec_args
            if executable is not None:
                self._values["executable"] = executable
            if memory_size is not None:
                self._values["memory_size"] = memory_size
            if pinned is not None:
                self._values["pinned"] = pinned
            if timeout is not None:
                self._values["timeout"] = timeout

        @builtins.property
        def encoding_type(self) -> typing.Optional[builtins.str]:
            '''The expected encoding type of the input payload for the function.

            Valid values are ``json`` (default) and ``binary`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-functionconfiguration.html#cfn-greengrass-functiondefinitionversion-functionconfiguration-encodingtype
            '''
            result = self._values.get("encoding_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def environment(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionDefinitionVersionPropsMixin.EnvironmentProperty"]]:
            '''The environment configuration of the function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-functionconfiguration.html#cfn-greengrass-functiondefinitionversion-functionconfiguration-environment
            '''
            result = self._values.get("environment")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionDefinitionVersionPropsMixin.EnvironmentProperty"]], result)

        @builtins.property
        def exec_args(self) -> typing.Optional[builtins.str]:
            '''The execution arguments.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-functionconfiguration.html#cfn-greengrass-functiondefinitionversion-functionconfiguration-execargs
            '''
            result = self._values.get("exec_args")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def executable(self) -> typing.Optional[builtins.str]:
            '''The name of the function executable.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-functionconfiguration.html#cfn-greengrass-functiondefinitionversion-functionconfiguration-executable
            '''
            result = self._values.get("executable")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def memory_size(self) -> typing.Optional[jsii.Number]:
            '''The memory size (in KB) required by the function.

            .. epigraph::

               This property applies only to Lambda functions that run in a Greengrass container.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-functionconfiguration.html#cfn-greengrass-functiondefinitionversion-functionconfiguration-memorysize
            '''
            result = self._values.get("memory_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def pinned(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether the function is pinned (or *long-lived* ).

            Pinned functions start when the core starts and process all requests in the same container. The default value is false.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-functionconfiguration.html#cfn-greengrass-functiondefinitionversion-functionconfiguration-pinned
            '''
            result = self._values.get("pinned")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def timeout(self) -> typing.Optional[jsii.Number]:
            '''The allowed execution time (in seconds) after which the function should terminate.

            For pinned functions, this timeout applies for each request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-functionconfiguration.html#cfn-greengrass-functiondefinitionversion-functionconfiguration-timeout
            '''
            result = self._values.get("timeout")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FunctionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnFunctionDefinitionVersionPropsMixin.FunctionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "function_arn": "functionArn",
            "function_configuration": "functionConfiguration",
            "id": "id",
        },
    )
    class FunctionProperty:
        def __init__(
            self,
            *,
            function_arn: typing.Optional[builtins.str] = None,
            function_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionDefinitionVersionPropsMixin.FunctionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A function is a Lambda function that's referenced from an AWS IoT Greengrass group.

            The function is deployed to a Greengrass core where it runs locally. For more information, see `Run Lambda Functions on the AWS IoT Greengrass Core <https://docs.aws.amazon.com/greengrass/v1/developerguide/lambda-functions.html>`_ in the *Developer Guide* .

            In an CloudFormation template, the ``Functions`` property of the ```AWS::Greengrass::FunctionDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-functiondefinitionversion.html>`_ resource contains a list of ``Function`` property types.

            :param function_arn: The Amazon Resource Name (ARN) of the alias (recommended) or version of the referenced Lambda function.
            :param function_configuration: The group-specific settings of the Lambda function. These settings configure the function's behavior in the Greengrass group.
            :param id: A descriptive or arbitrary ID for the function. This value must be unique within the function definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-function.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                # variables: Any
                
                function_property = greengrass_mixins.CfnFunctionDefinitionVersionPropsMixin.FunctionProperty(
                    function_arn="functionArn",
                    function_configuration=greengrass_mixins.CfnFunctionDefinitionVersionPropsMixin.FunctionConfigurationProperty(
                        encoding_type="encodingType",
                        environment=greengrass_mixins.CfnFunctionDefinitionVersionPropsMixin.EnvironmentProperty(
                            access_sysfs=False,
                            execution=greengrass_mixins.CfnFunctionDefinitionVersionPropsMixin.ExecutionProperty(
                                isolation_mode="isolationMode",
                                run_as=greengrass_mixins.CfnFunctionDefinitionVersionPropsMixin.RunAsProperty(
                                    gid=123,
                                    uid=123
                                )
                            ),
                            resource_access_policies=[greengrass_mixins.CfnFunctionDefinitionVersionPropsMixin.ResourceAccessPolicyProperty(
                                permission="permission",
                                resource_id="resourceId"
                            )],
                            variables=variables
                        ),
                        exec_args="execArgs",
                        executable="executable",
                        memory_size=123,
                        pinned=False,
                        timeout=123
                    ),
                    id="id"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bd8b1bcb4bdef10f4eb8cf98898ebb4ac0c276a61158abdc11eb0f6fc6cafc8a)
                check_type(argname="argument function_arn", value=function_arn, expected_type=type_hints["function_arn"])
                check_type(argname="argument function_configuration", value=function_configuration, expected_type=type_hints["function_configuration"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if function_arn is not None:
                self._values["function_arn"] = function_arn
            if function_configuration is not None:
                self._values["function_configuration"] = function_configuration
            if id is not None:
                self._values["id"] = id

        @builtins.property
        def function_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the alias (recommended) or version of the referenced Lambda function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-function.html#cfn-greengrass-functiondefinitionversion-function-functionarn
            '''
            result = self._values.get("function_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def function_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionDefinitionVersionPropsMixin.FunctionConfigurationProperty"]]:
            '''The group-specific settings of the Lambda function.

            These settings configure the function's behavior in the Greengrass group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-function.html#cfn-greengrass-functiondefinitionversion-function-functionconfiguration
            '''
            result = self._values.get("function_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionDefinitionVersionPropsMixin.FunctionConfigurationProperty"]], result)

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''A descriptive or arbitrary ID for the function.

            This value must be unique within the function definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-function.html#cfn-greengrass-functiondefinitionversion-function-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FunctionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnFunctionDefinitionVersionPropsMixin.ResourceAccessPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"permission": "permission", "resource_id": "resourceId"},
    )
    class ResourceAccessPolicyProperty:
        def __init__(
            self,
            *,
            permission: typing.Optional[builtins.str] = None,
            resource_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A list of the `resources <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourceinstance.html>`_ in the group that the function can access, with the corresponding read-only or read-write permissions. The maximum is 10 resources.

            .. epigraph::

               This property applies only to Lambda functions that run in a Greengrass container.

            In an CloudFormation template, ``ResourceAccessPolicy`` is a property of the ```Environment`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-environment.html>`_ property type.

            :param permission: The read-only or read-write access that the Lambda function has to the resource. Valid values are ``ro`` or ``rw`` .
            :param resource_id: The ID of the resource. This ID is assigned to the resource when you create the resource definition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-resourceaccesspolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                resource_access_policy_property = greengrass_mixins.CfnFunctionDefinitionVersionPropsMixin.ResourceAccessPolicyProperty(
                    permission="permission",
                    resource_id="resourceId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1d3ec3c1504e9708d8df881573ffdd2eafc285970cb6c220f1a94aff857048bd)
                check_type(argname="argument permission", value=permission, expected_type=type_hints["permission"])
                check_type(argname="argument resource_id", value=resource_id, expected_type=type_hints["resource_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if permission is not None:
                self._values["permission"] = permission
            if resource_id is not None:
                self._values["resource_id"] = resource_id

        @builtins.property
        def permission(self) -> typing.Optional[builtins.str]:
            '''The read-only or read-write access that the Lambda function has to the resource.

            Valid values are ``ro`` or ``rw`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-resourceaccesspolicy.html#cfn-greengrass-functiondefinitionversion-resourceaccesspolicy-permission
            '''
            result = self._values.get("permission")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the resource.

            This ID is assigned to the resource when you create the resource definition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-resourceaccesspolicy.html#cfn-greengrass-functiondefinitionversion-resourceaccesspolicy-resourceid
            '''
            result = self._values.get("resource_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceAccessPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnFunctionDefinitionVersionPropsMixin.RunAsProperty",
        jsii_struct_bases=[],
        name_mapping={"gid": "gid", "uid": "uid"},
    )
    class RunAsProperty:
        def __init__(
            self,
            *,
            gid: typing.Optional[jsii.Number] = None,
            uid: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The user and group permissions used to run the Lambda function.

            This setting overrides the default access identity that's specified for the group (by default, ggc_user and ggc_group). You can override the user, group, or both. For more information, see `Run as <https://docs.aws.amazon.com/greengrass/v1/developerguide/lambda-group-config.html#lambda-access-identity.html>`_ in the *Developer Guide* .
            .. epigraph::

               Running as the root user increases risks to your data and device. Do not run as root (UID/GID=0) unless your business case requires it. For more information and requirements, see `Running a Lambda Function as Root <https://docs.aws.amazon.com/greengrass/v1/developerguide/lambda-group-config.html#lambda-running-as-root>`_ .

            In an CloudFormation template, ``RunAs`` is a property of the ```Execution`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-execution.html>`_ property type.

            :param gid: The group ID whose permissions are used to run the Lambda function. You can use the ``getent group`` command on your core device to look up the group ID.
            :param uid: The user ID whose permissions are used to run the Lambda function. You can use the ``getent passwd`` command on your core device to look up the user ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-runas.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                run_as_property = greengrass_mixins.CfnFunctionDefinitionVersionPropsMixin.RunAsProperty(
                    gid=123,
                    uid=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__55e9aad960236054930d6d8c620c5c54b971f3cff021a823f70b7f39dc32d4d5)
                check_type(argname="argument gid", value=gid, expected_type=type_hints["gid"])
                check_type(argname="argument uid", value=uid, expected_type=type_hints["uid"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if gid is not None:
                self._values["gid"] = gid
            if uid is not None:
                self._values["uid"] = uid

        @builtins.property
        def gid(self) -> typing.Optional[jsii.Number]:
            '''The group ID whose permissions are used to run the Lambda function.

            You can use the ``getent group`` command on your core device to look up the group ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-runas.html#cfn-greengrass-functiondefinitionversion-runas-gid
            '''
            result = self._values.get("gid")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def uid(self) -> typing.Optional[jsii.Number]:
            '''The user ID whose permissions are used to run the Lambda function.

            You can use the ``getent passwd`` command on your core device to look up the user ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-runas.html#cfn-greengrass-functiondefinitionversion-runas-uid
            '''
            result = self._values.get("uid")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RunAsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "initial_version": "initialVersion",
        "name": "name",
        "role_arn": "roleArn",
        "tags": "tags",
    },
)
class CfnGroupMixinProps:
    def __init__(
        self,
        *,
        initial_version: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGroupPropsMixin.GroupVersionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Properties for CfnGroupPropsMixin.

        :param initial_version: The group version to include when the group is created. A group version references the Amazon Resource Name (ARN) of a core definition version, device definition version, subscription definition version, and other version types. The group version must reference a core definition version that contains one core. Other version types are optionally included, depending on your business need. .. epigraph:: To associate a group version after the group is created, create an ```AWS::Greengrass::GroupVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-groupversion.html>`_ resource and specify the ID of this group.
        :param name: The name of the group.
        :param role_arn: The Amazon Resource Name (ARN) of the IAM role attached to the group. This role contains the permissions that Lambda functions and connectors use to interact with other AWS services.
        :param tags: Application-specific metadata to attach to the group. You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/v1/developerguide/tagging.html>`_ in the *Developer Guide* . This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in CloudFormation templates:: "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value" }

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
            
            # tags: Any
            
            cfn_group_mixin_props = greengrass_mixins.CfnGroupMixinProps(
                initial_version=greengrass_mixins.CfnGroupPropsMixin.GroupVersionProperty(
                    connector_definition_version_arn="connectorDefinitionVersionArn",
                    core_definition_version_arn="coreDefinitionVersionArn",
                    device_definition_version_arn="deviceDefinitionVersionArn",
                    function_definition_version_arn="functionDefinitionVersionArn",
                    logger_definition_version_arn="loggerDefinitionVersionArn",
                    resource_definition_version_arn="resourceDefinitionVersionArn",
                    subscription_definition_version_arn="subscriptionDefinitionVersionArn"
                ),
                name="name",
                role_arn="roleArn",
                tags=tags
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab5af4731743d4248c39bfbb7132b4d007051d4e042149cb6bb5ce5cc618c604)
            check_type(argname="argument initial_version", value=initial_version, expected_type=type_hints["initial_version"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if initial_version is not None:
            self._values["initial_version"] = initial_version
        if name is not None:
            self._values["name"] = name
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def initial_version(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGroupPropsMixin.GroupVersionProperty"]]:
        '''The group version to include when the group is created.

        A group version references the Amazon Resource Name (ARN) of a core definition version, device definition version, subscription definition version, and other version types. The group version must reference a core definition version that contains one core. Other version types are optionally included, depending on your business need.
        .. epigraph::

           To associate a group version after the group is created, create an ```AWS::Greengrass::GroupVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-groupversion.html>`_ resource and specify the ID of this group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html#cfn-greengrass-group-initialversion
        '''
        result = self._values.get("initial_version")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGroupPropsMixin.GroupVersionProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html#cfn-greengrass-group-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the IAM role attached to the group.

        This role contains the permissions that Lambda functions and connectors use to interact with other AWS services.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html#cfn-greengrass-group-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''Application-specific metadata to attach to the group.

        You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/v1/developerguide/tagging.html>`_ in the *Developer Guide* .

        This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in CloudFormation templates::

           "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value"
           }

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html#cfn-greengrass-group-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnGroupPropsMixin",
):
    '''AWS IoT Greengrass seamlessly extends AWS to edge devices so they can act locally on the data they generate, while still using the cloud for management, analytics, and durable storage.

    With AWS IoT Greengrass , connected devices can run AWS Lambda functions, execute predictions based on machine learning models, keep device data in sync, and communicate with other devices securely – even when not connected to the internet. For more information, see the `Developer Guide <https://docs.aws.amazon.com/greengrass/v1/developerguide/what-is-gg.html>`_ .
    .. epigraph::

       For AWS Region support, see `CloudFormation Support for AWS IoT Greengrass <https://docs.aws.amazon.com/greengrass/v1/developerguide/cloudformation-support.html>`_ in the *Developer Guide* .

    The ``AWS::Greengrass::Group`` resource represents a group in AWS IoT Greengrass . In the AWS IoT Greengrass API, groups are used to organize your group versions.

    Groups can reference multiple group versions. All group versions must be associated with a group. A group version references a device definition version, subscription definition version, and other version types that contain the components you want to deploy to a Greengrass core device.

    To deploy a group version, the group version must reference a core definition version that contains one core. Other version types are optionally included, depending on your business need.
    .. epigraph::

       When you create a group, you can optionally include an initial group version. To associate a group version later, create a ```AWS::Greengrass::GroupVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-groupversion.html>`_ resource and specify the ID of this group.

       To change group components (such as devices, subscriptions, or functions), you must create new versions. This is because versions are immutable. For example, to add a function, you create a function definition version that contains the new function (and all other functions that you want to deploy). Then you create a group version that references the new function definition version (and all other version types that you want to deploy).

    *Deploying a Group Version*

    After you create the group version in your CloudFormation template, you can deploy it using the ```aws greengrass create-deployment`` <https://docs.aws.amazon.com/greengrass/v1/apireference/createdeployment-post.html>`_ command in the AWS CLI or from the *Greengrass* node in the AWS IoT console. To deploy a group version, you must have a Greengrass service role associated with your AWS account . For more information, see `CloudFormation Support for AWS IoT Greengrass <https://docs.aws.amazon.com/greengrass/v1/developerguide/cloudformation-support.html>`_ in the *Developer Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html
    :cloudformationResource: AWS::Greengrass::Group
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
        
        # tags: Any
        
        cfn_group_props_mixin = greengrass_mixins.CfnGroupPropsMixin(greengrass_mixins.CfnGroupMixinProps(
            initial_version=greengrass_mixins.CfnGroupPropsMixin.GroupVersionProperty(
                connector_definition_version_arn="connectorDefinitionVersionArn",
                core_definition_version_arn="coreDefinitionVersionArn",
                device_definition_version_arn="deviceDefinitionVersionArn",
                function_definition_version_arn="functionDefinitionVersionArn",
                logger_definition_version_arn="loggerDefinitionVersionArn",
                resource_definition_version_arn="resourceDefinitionVersionArn",
                subscription_definition_version_arn="subscriptionDefinitionVersionArn"
            ),
            name="name",
            role_arn="roleArn",
            tags=tags
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Greengrass::Group``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37b5fbb33e6b77d6af05adb6de78e4475f7c2e26574880af7314386f57db8fe8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ea6dc2a679645b98ac17da0ca5210702c7b1a25c83098496c02a10a95f8921e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03e0f96b6f1df38d662191f7edd44268f5a9f0cc54651cbad15904799baef719)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnGroupMixinProps:
        return typing.cast(CfnGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnGroupPropsMixin.GroupVersionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "connector_definition_version_arn": "connectorDefinitionVersionArn",
            "core_definition_version_arn": "coreDefinitionVersionArn",
            "device_definition_version_arn": "deviceDefinitionVersionArn",
            "function_definition_version_arn": "functionDefinitionVersionArn",
            "logger_definition_version_arn": "loggerDefinitionVersionArn",
            "resource_definition_version_arn": "resourceDefinitionVersionArn",
            "subscription_definition_version_arn": "subscriptionDefinitionVersionArn",
        },
    )
    class GroupVersionProperty:
        def __init__(
            self,
            *,
            connector_definition_version_arn: typing.Optional[builtins.str] = None,
            core_definition_version_arn: typing.Optional[builtins.str] = None,
            device_definition_version_arn: typing.Optional[builtins.str] = None,
            function_definition_version_arn: typing.Optional[builtins.str] = None,
            logger_definition_version_arn: typing.Optional[builtins.str] = None,
            resource_definition_version_arn: typing.Optional[builtins.str] = None,
            subscription_definition_version_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A group version in AWS IoT Greengrass , which references of a core definition version, device definition version, subscription definition version, and other version types that contain the components you want to deploy to a Greengrass core device.

            The group version must reference a core definition version that contains one core. Other version types are optionally included, depending on your business need.

            In an CloudFormation template, ``GroupVersion`` is the property type of the ``InitialVersion`` property in the ```AWS::Greengrass::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html>`_ resource.

            :param connector_definition_version_arn: The Amazon Resource Name (ARN) of the connector definition version that contains the connectors you want to deploy with the group version.
            :param core_definition_version_arn: The ARN of the core definition version that contains the core you want to deploy with the group version. Currently, the core definition version can contain only one core.
            :param device_definition_version_arn: The ARN of the device definition version that contains the devices you want to deploy with the group version.
            :param function_definition_version_arn: The ARN of the function definition version that contains the functions you want to deploy with the group version.
            :param logger_definition_version_arn: The ARN of the logger definition version that contains the loggers you want to deploy with the group version.
            :param resource_definition_version_arn: The ARN of the resource definition version that contains the resources you want to deploy with the group version.
            :param subscription_definition_version_arn: The ARN of the subscription definition version that contains the subscriptions you want to deploy with the group version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-group-groupversion.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                group_version_property = greengrass_mixins.CfnGroupPropsMixin.GroupVersionProperty(
                    connector_definition_version_arn="connectorDefinitionVersionArn",
                    core_definition_version_arn="coreDefinitionVersionArn",
                    device_definition_version_arn="deviceDefinitionVersionArn",
                    function_definition_version_arn="functionDefinitionVersionArn",
                    logger_definition_version_arn="loggerDefinitionVersionArn",
                    resource_definition_version_arn="resourceDefinitionVersionArn",
                    subscription_definition_version_arn="subscriptionDefinitionVersionArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__06dc1246ebe173fb8ad4730bbde12b4595f1c1067740d1b5acd3955fa4b7cf7d)
                check_type(argname="argument connector_definition_version_arn", value=connector_definition_version_arn, expected_type=type_hints["connector_definition_version_arn"])
                check_type(argname="argument core_definition_version_arn", value=core_definition_version_arn, expected_type=type_hints["core_definition_version_arn"])
                check_type(argname="argument device_definition_version_arn", value=device_definition_version_arn, expected_type=type_hints["device_definition_version_arn"])
                check_type(argname="argument function_definition_version_arn", value=function_definition_version_arn, expected_type=type_hints["function_definition_version_arn"])
                check_type(argname="argument logger_definition_version_arn", value=logger_definition_version_arn, expected_type=type_hints["logger_definition_version_arn"])
                check_type(argname="argument resource_definition_version_arn", value=resource_definition_version_arn, expected_type=type_hints["resource_definition_version_arn"])
                check_type(argname="argument subscription_definition_version_arn", value=subscription_definition_version_arn, expected_type=type_hints["subscription_definition_version_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if connector_definition_version_arn is not None:
                self._values["connector_definition_version_arn"] = connector_definition_version_arn
            if core_definition_version_arn is not None:
                self._values["core_definition_version_arn"] = core_definition_version_arn
            if device_definition_version_arn is not None:
                self._values["device_definition_version_arn"] = device_definition_version_arn
            if function_definition_version_arn is not None:
                self._values["function_definition_version_arn"] = function_definition_version_arn
            if logger_definition_version_arn is not None:
                self._values["logger_definition_version_arn"] = logger_definition_version_arn
            if resource_definition_version_arn is not None:
                self._values["resource_definition_version_arn"] = resource_definition_version_arn
            if subscription_definition_version_arn is not None:
                self._values["subscription_definition_version_arn"] = subscription_definition_version_arn

        @builtins.property
        def connector_definition_version_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the connector definition version that contains the connectors you want to deploy with the group version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-group-groupversion.html#cfn-greengrass-group-groupversion-connectordefinitionversionarn
            '''
            result = self._values.get("connector_definition_version_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def core_definition_version_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the core definition version that contains the core you want to deploy with the group version.

            Currently, the core definition version can contain only one core.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-group-groupversion.html#cfn-greengrass-group-groupversion-coredefinitionversionarn
            '''
            result = self._values.get("core_definition_version_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def device_definition_version_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the device definition version that contains the devices you want to deploy with the group version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-group-groupversion.html#cfn-greengrass-group-groupversion-devicedefinitionversionarn
            '''
            result = self._values.get("device_definition_version_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def function_definition_version_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the function definition version that contains the functions you want to deploy with the group version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-group-groupversion.html#cfn-greengrass-group-groupversion-functiondefinitionversionarn
            '''
            result = self._values.get("function_definition_version_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def logger_definition_version_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the logger definition version that contains the loggers you want to deploy with the group version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-group-groupversion.html#cfn-greengrass-group-groupversion-loggerdefinitionversionarn
            '''
            result = self._values.get("logger_definition_version_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_definition_version_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the resource definition version that contains the resources you want to deploy with the group version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-group-groupversion.html#cfn-greengrass-group-groupversion-resourcedefinitionversionarn
            '''
            result = self._values.get("resource_definition_version_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def subscription_definition_version_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the subscription definition version that contains the subscriptions you want to deploy with the group version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-group-groupversion.html#cfn-greengrass-group-groupversion-subscriptiondefinitionversionarn
            '''
            result = self._values.get("subscription_definition_version_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GroupVersionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnGroupVersionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "connector_definition_version_arn": "connectorDefinitionVersionArn",
        "core_definition_version_arn": "coreDefinitionVersionArn",
        "device_definition_version_arn": "deviceDefinitionVersionArn",
        "function_definition_version_arn": "functionDefinitionVersionArn",
        "group_id": "groupId",
        "logger_definition_version_arn": "loggerDefinitionVersionArn",
        "resource_definition_version_arn": "resourceDefinitionVersionArn",
        "subscription_definition_version_arn": "subscriptionDefinitionVersionArn",
    },
)
class CfnGroupVersionMixinProps:
    def __init__(
        self,
        *,
        connector_definition_version_arn: typing.Optional[builtins.str] = None,
        core_definition_version_arn: typing.Optional[builtins.str] = None,
        device_definition_version_arn: typing.Optional[builtins.str] = None,
        function_definition_version_arn: typing.Optional[builtins.str] = None,
        group_id: typing.Optional[builtins.str] = None,
        logger_definition_version_arn: typing.Optional[builtins.str] = None,
        resource_definition_version_arn: typing.Optional[builtins.str] = None,
        subscription_definition_version_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnGroupVersionPropsMixin.

        :param connector_definition_version_arn: The Amazon Resource Name (ARN) of the connector definition version that contains the connectors you want to deploy with the group version.
        :param core_definition_version_arn: The ARN of the core definition version that contains the core you want to deploy with the group version. Currently, the core definition version can contain only one core.
        :param device_definition_version_arn: The ARN of the device definition version that contains the devices you want to deploy with the group version.
        :param function_definition_version_arn: The ARN of the function definition version that contains the functions you want to deploy with the group version.
        :param group_id: The ID of the group associated with this version. This value is a GUID.
        :param logger_definition_version_arn: The ARN of the logger definition version that contains the loggers you want to deploy with the group version.
        :param resource_definition_version_arn: The ARN of the resource definition version that contains the resources you want to deploy with the group version.
        :param subscription_definition_version_arn: The ARN of the subscription definition version that contains the subscriptions you want to deploy with the group version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-groupversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
            
            cfn_group_version_mixin_props = greengrass_mixins.CfnGroupVersionMixinProps(
                connector_definition_version_arn="connectorDefinitionVersionArn",
                core_definition_version_arn="coreDefinitionVersionArn",
                device_definition_version_arn="deviceDefinitionVersionArn",
                function_definition_version_arn="functionDefinitionVersionArn",
                group_id="groupId",
                logger_definition_version_arn="loggerDefinitionVersionArn",
                resource_definition_version_arn="resourceDefinitionVersionArn",
                subscription_definition_version_arn="subscriptionDefinitionVersionArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f35dc189118a6d54675250cf9990576f5e6caaf57a288864c8599c36f491a41)
            check_type(argname="argument connector_definition_version_arn", value=connector_definition_version_arn, expected_type=type_hints["connector_definition_version_arn"])
            check_type(argname="argument core_definition_version_arn", value=core_definition_version_arn, expected_type=type_hints["core_definition_version_arn"])
            check_type(argname="argument device_definition_version_arn", value=device_definition_version_arn, expected_type=type_hints["device_definition_version_arn"])
            check_type(argname="argument function_definition_version_arn", value=function_definition_version_arn, expected_type=type_hints["function_definition_version_arn"])
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
            check_type(argname="argument logger_definition_version_arn", value=logger_definition_version_arn, expected_type=type_hints["logger_definition_version_arn"])
            check_type(argname="argument resource_definition_version_arn", value=resource_definition_version_arn, expected_type=type_hints["resource_definition_version_arn"])
            check_type(argname="argument subscription_definition_version_arn", value=subscription_definition_version_arn, expected_type=type_hints["subscription_definition_version_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connector_definition_version_arn is not None:
            self._values["connector_definition_version_arn"] = connector_definition_version_arn
        if core_definition_version_arn is not None:
            self._values["core_definition_version_arn"] = core_definition_version_arn
        if device_definition_version_arn is not None:
            self._values["device_definition_version_arn"] = device_definition_version_arn
        if function_definition_version_arn is not None:
            self._values["function_definition_version_arn"] = function_definition_version_arn
        if group_id is not None:
            self._values["group_id"] = group_id
        if logger_definition_version_arn is not None:
            self._values["logger_definition_version_arn"] = logger_definition_version_arn
        if resource_definition_version_arn is not None:
            self._values["resource_definition_version_arn"] = resource_definition_version_arn
        if subscription_definition_version_arn is not None:
            self._values["subscription_definition_version_arn"] = subscription_definition_version_arn

    @builtins.property
    def connector_definition_version_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the connector definition version that contains the connectors you want to deploy with the group version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-groupversion.html#cfn-greengrass-groupversion-connectordefinitionversionarn
        '''
        result = self._values.get("connector_definition_version_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def core_definition_version_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the core definition version that contains the core you want to deploy with the group version.

        Currently, the core definition version can contain only one core.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-groupversion.html#cfn-greengrass-groupversion-coredefinitionversionarn
        '''
        result = self._values.get("core_definition_version_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def device_definition_version_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the device definition version that contains the devices you want to deploy with the group version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-groupversion.html#cfn-greengrass-groupversion-devicedefinitionversionarn
        '''
        result = self._values.get("device_definition_version_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def function_definition_version_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the function definition version that contains the functions you want to deploy with the group version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-groupversion.html#cfn-greengrass-groupversion-functiondefinitionversionarn
        '''
        result = self._values.get("function_definition_version_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def group_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the group associated with this version.

        This value is a GUID.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-groupversion.html#cfn-greengrass-groupversion-groupid
        '''
        result = self._values.get("group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logger_definition_version_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the logger definition version that contains the loggers you want to deploy with the group version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-groupversion.html#cfn-greengrass-groupversion-loggerdefinitionversionarn
        '''
        result = self._values.get("logger_definition_version_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_definition_version_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the resource definition version that contains the resources you want to deploy with the group version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-groupversion.html#cfn-greengrass-groupversion-resourcedefinitionversionarn
        '''
        result = self._values.get("resource_definition_version_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subscription_definition_version_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the subscription definition version that contains the subscriptions you want to deploy with the group version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-groupversion.html#cfn-greengrass-groupversion-subscriptiondefinitionversionarn
        '''
        result = self._values.get("subscription_definition_version_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupVersionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnGroupVersionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnGroupVersionPropsMixin",
):
    '''The ``AWS::Greengrass::GroupVersion`` resource represents a group version in AWS IoT Greengrass .

    A group version references a core definition version, device definition version, subscription definition version, and other version types that contain the components you want to deploy to a Greengrass core device. The group version must reference a core definition version that contains one core. Other version types are optionally included, depending on your business need.
    .. epigraph::

       To create a group version, you must specify the ID of the group that you want to associate with the version. For information about creating a group, see ```AWS::Greengrass::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-groupversion.html
    :cloudformationResource: AWS::Greengrass::GroupVersion
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
        
        cfn_group_version_props_mixin = greengrass_mixins.CfnGroupVersionPropsMixin(greengrass_mixins.CfnGroupVersionMixinProps(
            connector_definition_version_arn="connectorDefinitionVersionArn",
            core_definition_version_arn="coreDefinitionVersionArn",
            device_definition_version_arn="deviceDefinitionVersionArn",
            function_definition_version_arn="functionDefinitionVersionArn",
            group_id="groupId",
            logger_definition_version_arn="loggerDefinitionVersionArn",
            resource_definition_version_arn="resourceDefinitionVersionArn",
            subscription_definition_version_arn="subscriptionDefinitionVersionArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnGroupVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Greengrass::GroupVersion``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1116238c1d62e7d91cb9e43d666267890e5200cb9c8daa9037f92d8e50382d9b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8857dba89a5a73721d6b6b72c912056659750459f64e3d89446ad9b68b253ac)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a70a07a7db5527469a3273525f537f9b5db67081e3a32a31645a6be05de069d1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnGroupVersionMixinProps:
        return typing.cast(CfnGroupVersionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnLoggerDefinitionMixinProps",
    jsii_struct_bases=[],
    name_mapping={"initial_version": "initialVersion", "name": "name", "tags": "tags"},
)
class CfnLoggerDefinitionMixinProps:
    def __init__(
        self,
        *,
        initial_version: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLoggerDefinitionPropsMixin.LoggerDefinitionVersionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Properties for CfnLoggerDefinitionPropsMixin.

        :param initial_version: The logger definition version to include when the logger definition is created. A logger definition version contains a list of ```logger`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-loggerdefinition-logger.html>`_ property types. .. epigraph:: To associate a logger definition version after the logger definition is created, create an ```AWS::Greengrass::LoggerDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-loggerdefinitionversion.html>`_ resource and specify the ID of this logger definition.
        :param name: The name of the logger definition.
        :param tags: Application-specific metadata to attach to the logger definition. You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/v1/developerguide/tagging.html>`_ in the *Developer Guide* . This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in CloudFormation templates:: "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value" }

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-loggerdefinition.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
            
            # tags: Any
            
            cfn_logger_definition_mixin_props = greengrass_mixins.CfnLoggerDefinitionMixinProps(
                initial_version=greengrass_mixins.CfnLoggerDefinitionPropsMixin.LoggerDefinitionVersionProperty(
                    loggers=[greengrass_mixins.CfnLoggerDefinitionPropsMixin.LoggerProperty(
                        component="component",
                        id="id",
                        level="level",
                        space=123,
                        type="type"
                    )]
                ),
                name="name",
                tags=tags
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11488f1d2da72411620f6dd98a1e5b6ebdc91c2e33fc636b51b3a2feb408a7b7)
            check_type(argname="argument initial_version", value=initial_version, expected_type=type_hints["initial_version"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if initial_version is not None:
            self._values["initial_version"] = initial_version
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def initial_version(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLoggerDefinitionPropsMixin.LoggerDefinitionVersionProperty"]]:
        '''The logger definition version to include when the logger definition is created.

        A logger definition version contains a list of ```logger`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-loggerdefinition-logger.html>`_ property types.
        .. epigraph::

           To associate a logger definition version after the logger definition is created, create an ```AWS::Greengrass::LoggerDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-loggerdefinitionversion.html>`_ resource and specify the ID of this logger definition.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-loggerdefinition.html#cfn-greengrass-loggerdefinition-initialversion
        '''
        result = self._values.get("initial_version")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLoggerDefinitionPropsMixin.LoggerDefinitionVersionProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the logger definition.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-loggerdefinition.html#cfn-greengrass-loggerdefinition-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''Application-specific metadata to attach to the logger definition.

        You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/v1/developerguide/tagging.html>`_ in the *Developer Guide* .

        This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in CloudFormation templates::

           "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value"
           }

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-loggerdefinition.html#cfn-greengrass-loggerdefinition-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLoggerDefinitionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLoggerDefinitionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnLoggerDefinitionPropsMixin",
):
    '''The ``AWS::Greengrass::LoggerDefinition`` resource represents a logger definition for AWS IoT Greengrass .

    Logger definitions are used to organize your logger definition versions.

    Logger definitions can reference multiple logger definition versions. All logger definition versions must be associated with a logger definition. Each logger definition version can contain one or more loggers.
    .. epigraph::

       When you create a logger definition, you can optionally include an initial logger definition version. To associate a logger definition version later, create an ```AWS::Greengrass::LoggerDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-loggerdefinitionversion.html>`_ resource and specify the ID of this logger definition.

       After you create the logger definition version that contains the loggers you want to deploy, you must add it to your group version. For more information, see ```AWS::Greengrass::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-loggerdefinition.html
    :cloudformationResource: AWS::Greengrass::LoggerDefinition
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
        
        # tags: Any
        
        cfn_logger_definition_props_mixin = greengrass_mixins.CfnLoggerDefinitionPropsMixin(greengrass_mixins.CfnLoggerDefinitionMixinProps(
            initial_version=greengrass_mixins.CfnLoggerDefinitionPropsMixin.LoggerDefinitionVersionProperty(
                loggers=[greengrass_mixins.CfnLoggerDefinitionPropsMixin.LoggerProperty(
                    component="component",
                    id="id",
                    level="level",
                    space=123,
                    type="type"
                )]
            ),
            name="name",
            tags=tags
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnLoggerDefinitionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Greengrass::LoggerDefinition``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c373c68d89549c1574942186d772752254520688cb98b22fb5cf9c96871f8bca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__89cde0b938f6946a7e1c9b016e08f247080702b3d81b7059b70cc5461b3e0daf)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0645ca1531ae7861fd8bd4d669730d0f1b8bca118114320cf8b768723a3cf16)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLoggerDefinitionMixinProps:
        return typing.cast(CfnLoggerDefinitionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnLoggerDefinitionPropsMixin.LoggerDefinitionVersionProperty",
        jsii_struct_bases=[],
        name_mapping={"loggers": "loggers"},
    )
    class LoggerDefinitionVersionProperty:
        def __init__(
            self,
            *,
            loggers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLoggerDefinitionPropsMixin.LoggerProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''A logger definition version contains a list of `loggers <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-loggerdefinition-logger.html>`_ .

            .. epigraph::

               After you create a logger definition version that contains the loggers you want to deploy, you must add it to your group version. For more information, see ```AWS::Greengrass::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html>`_ .

            In an CloudFormation template, ``LoggerDefinitionVersion`` is the property type of the ``InitialVersion`` property in the ```AWS::Greengrass::LoggerDefinition`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-loggerdefinition.html>`_ resource.

            :param loggers: The loggers in this version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-loggerdefinition-loggerdefinitionversion.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                logger_definition_version_property = greengrass_mixins.CfnLoggerDefinitionPropsMixin.LoggerDefinitionVersionProperty(
                    loggers=[greengrass_mixins.CfnLoggerDefinitionPropsMixin.LoggerProperty(
                        component="component",
                        id="id",
                        level="level",
                        space=123,
                        type="type"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d685a0b144be1b6473264f71dc12bcc6688812685e51f6e5dff03f8c03dab377)
                check_type(argname="argument loggers", value=loggers, expected_type=type_hints["loggers"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if loggers is not None:
                self._values["loggers"] = loggers

        @builtins.property
        def loggers(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLoggerDefinitionPropsMixin.LoggerProperty"]]]]:
            '''The loggers in this version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-loggerdefinition-loggerdefinitionversion.html#cfn-greengrass-loggerdefinition-loggerdefinitionversion-loggers
            '''
            result = self._values.get("loggers")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLoggerDefinitionPropsMixin.LoggerProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggerDefinitionVersionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnLoggerDefinitionPropsMixin.LoggerProperty",
        jsii_struct_bases=[],
        name_mapping={
            "component": "component",
            "id": "id",
            "level": "level",
            "space": "space",
            "type": "type",
        },
    )
    class LoggerProperty:
        def __init__(
            self,
            *,
            component: typing.Optional[builtins.str] = None,
            id: typing.Optional[builtins.str] = None,
            level: typing.Optional[builtins.str] = None,
            space: typing.Optional[jsii.Number] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A logger represents logging settings for the AWS IoT Greengrass group, which can be stored in CloudWatch and the local file system of your core device.

            All log entries include a timestamp, log level, and information about the event. For more information, see `Monitoring with AWS IoT Greengrass Logs <https://docs.aws.amazon.com/greengrass/v1/developerguide/greengrass-logs-overview.html>`_ in the *Developer Guide* .

            In an CloudFormation template, the ``Loggers`` property of the ```LoggerDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-loggerdefinition-loggerdefinitionversion.html>`_ property type contains a list of ``Logger`` property types.

            :param component: The source of the log event. Valid values are ``GreengrassSystem`` or ``Lambda`` . When ``GreengrassSystem`` is used, events from Greengrass system components are logged. When ``Lambda`` is used, events from user-defined Lambda functions are logged.
            :param id: A descriptive or arbitrary ID for the logger. This value must be unique within the logger definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .
            :param level: The log-level threshold. Log events below this threshold are filtered out and aren't stored. Valid values are ``DEBUG`` , ``INFO`` (recommended), ``WARN`` , ``ERROR`` , or ``FATAL`` .
            :param space: The amount of file space (in KB) to use when writing logs to the local file system. This property does not apply for CloudWatch Logs .
            :param type: The storage mechanism for log events. Valid values are ``FileSystem`` or ``AWSCloudWatch`` . When ``AWSCloudWatch`` is used, log events are sent to CloudWatch Logs . When ``FileSystem`` is used, log events are stored on the local file system.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-loggerdefinition-logger.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                logger_property = greengrass_mixins.CfnLoggerDefinitionPropsMixin.LoggerProperty(
                    component="component",
                    id="id",
                    level="level",
                    space=123,
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3b64f857839660b799d536dde6360b80e9d67f5272fad5b5e863c64c5bc8e7dd)
                check_type(argname="argument component", value=component, expected_type=type_hints["component"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument level", value=level, expected_type=type_hints["level"])
                check_type(argname="argument space", value=space, expected_type=type_hints["space"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if component is not None:
                self._values["component"] = component
            if id is not None:
                self._values["id"] = id
            if level is not None:
                self._values["level"] = level
            if space is not None:
                self._values["space"] = space
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def component(self) -> typing.Optional[builtins.str]:
            '''The source of the log event.

            Valid values are ``GreengrassSystem`` or ``Lambda`` . When ``GreengrassSystem`` is used, events from Greengrass system components are logged. When ``Lambda`` is used, events from user-defined Lambda functions are logged.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-loggerdefinition-logger.html#cfn-greengrass-loggerdefinition-logger-component
            '''
            result = self._values.get("component")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''A descriptive or arbitrary ID for the logger.

            This value must be unique within the logger definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-loggerdefinition-logger.html#cfn-greengrass-loggerdefinition-logger-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def level(self) -> typing.Optional[builtins.str]:
            '''The log-level threshold.

            Log events below this threshold are filtered out and aren't stored. Valid values are ``DEBUG`` , ``INFO`` (recommended), ``WARN`` , ``ERROR`` , or ``FATAL`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-loggerdefinition-logger.html#cfn-greengrass-loggerdefinition-logger-level
            '''
            result = self._values.get("level")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def space(self) -> typing.Optional[jsii.Number]:
            '''The amount of file space (in KB) to use when writing logs to the local file system.

            This property does not apply for CloudWatch Logs .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-loggerdefinition-logger.html#cfn-greengrass-loggerdefinition-logger-space
            '''
            result = self._values.get("space")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The storage mechanism for log events.

            Valid values are ``FileSystem`` or ``AWSCloudWatch`` . When ``AWSCloudWatch`` is used, log events are sent to CloudWatch Logs . When ``FileSystem`` is used, log events are stored on the local file system.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-loggerdefinition-logger.html#cfn-greengrass-loggerdefinition-logger-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggerProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnLoggerDefinitionVersionMixinProps",
    jsii_struct_bases=[],
    name_mapping={"logger_definition_id": "loggerDefinitionId", "loggers": "loggers"},
)
class CfnLoggerDefinitionVersionMixinProps:
    def __init__(
        self,
        *,
        logger_definition_id: typing.Optional[builtins.str] = None,
        loggers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLoggerDefinitionVersionPropsMixin.LoggerProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnLoggerDefinitionVersionPropsMixin.

        :param logger_definition_id: The ID of the logger definition associated with this version. This value is a GUID.
        :param loggers: The loggers in this version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-loggerdefinitionversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
            
            cfn_logger_definition_version_mixin_props = greengrass_mixins.CfnLoggerDefinitionVersionMixinProps(
                logger_definition_id="loggerDefinitionId",
                loggers=[greengrass_mixins.CfnLoggerDefinitionVersionPropsMixin.LoggerProperty(
                    component="component",
                    id="id",
                    level="level",
                    space=123,
                    type="type"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5390edfbeefa03bf2aad0f5218bb18620c121f71b9da7b41d35569ec6dd4c0bb)
            check_type(argname="argument logger_definition_id", value=logger_definition_id, expected_type=type_hints["logger_definition_id"])
            check_type(argname="argument loggers", value=loggers, expected_type=type_hints["loggers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if logger_definition_id is not None:
            self._values["logger_definition_id"] = logger_definition_id
        if loggers is not None:
            self._values["loggers"] = loggers

    @builtins.property
    def logger_definition_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the logger definition associated with this version.

        This value is a GUID.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-loggerdefinitionversion.html#cfn-greengrass-loggerdefinitionversion-loggerdefinitionid
        '''
        result = self._values.get("logger_definition_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def loggers(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLoggerDefinitionVersionPropsMixin.LoggerProperty"]]]]:
        '''The loggers in this version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-loggerdefinitionversion.html#cfn-greengrass-loggerdefinitionversion-loggers
        '''
        result = self._values.get("loggers")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLoggerDefinitionVersionPropsMixin.LoggerProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLoggerDefinitionVersionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLoggerDefinitionVersionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnLoggerDefinitionVersionPropsMixin",
):
    '''The ``AWS::Greengrass::LoggerDefinitionVersion`` resource represents a logger definition version for AWS IoT Greengrass .

    A logger definition version contains a list of loggers.
    .. epigraph::

       To create a logger definition version, you must specify the ID of the logger definition that you want to associate with the version. For information about creating a logger definition, see ```AWS::Greengrass::LoggerDefinition`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-loggerdefinition.html>`_ .

       After you create a logger definition version that contains the loggers you want to deploy, you must add it to your group version. For more information, see ```AWS::Greengrass::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-loggerdefinitionversion.html
    :cloudformationResource: AWS::Greengrass::LoggerDefinitionVersion
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
        
        cfn_logger_definition_version_props_mixin = greengrass_mixins.CfnLoggerDefinitionVersionPropsMixin(greengrass_mixins.CfnLoggerDefinitionVersionMixinProps(
            logger_definition_id="loggerDefinitionId",
            loggers=[greengrass_mixins.CfnLoggerDefinitionVersionPropsMixin.LoggerProperty(
                component="component",
                id="id",
                level="level",
                space=123,
                type="type"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnLoggerDefinitionVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Greengrass::LoggerDefinitionVersion``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9aa8d6b3cc549cb0ee09ae09d60acb4d99258d13d5422ea62566cc738cbbfd2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__052f4d7c5fb10415b4a52ab7cbdbaa0b8d6ed2d217fd6e09661c13ea11a434b0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__964ad1c4fa1186099e65cc4da6200f56961b5c9ae67b7ac86b9bb9840e4f3f33)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLoggerDefinitionVersionMixinProps:
        return typing.cast(CfnLoggerDefinitionVersionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnLoggerDefinitionVersionPropsMixin.LoggerProperty",
        jsii_struct_bases=[],
        name_mapping={
            "component": "component",
            "id": "id",
            "level": "level",
            "space": "space",
            "type": "type",
        },
    )
    class LoggerProperty:
        def __init__(
            self,
            *,
            component: typing.Optional[builtins.str] = None,
            id: typing.Optional[builtins.str] = None,
            level: typing.Optional[builtins.str] = None,
            space: typing.Optional[jsii.Number] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A logger represents logging settings for the AWS IoT Greengrass group, which can be stored in CloudWatch and the local file system of your core device.

            All log entries include a timestamp, log level, and information about the event. For more information, see `Monitoring with AWS IoT Greengrass Logs <https://docs.aws.amazon.com/greengrass/v1/developerguide/greengrass-logs-overview.html>`_ in the *Developer Guide* .

            In an CloudFormation template, the ``Loggers`` property of the ```AWS::Greengrass::LoggerDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-loggerdefinitionversion.html>`_ resource contains a list of ``Logger`` property types.

            :param component: The source of the log event. Valid values are ``GreengrassSystem`` or ``Lambda`` . When ``GreengrassSystem`` is used, events from Greengrass system components are logged. When ``Lambda`` is used, events from user-defined Lambda functions are logged.
            :param id: A descriptive or arbitrary ID for the logger. This value must be unique within the logger definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .
            :param level: The log-level threshold. Log events below this threshold are filtered out and aren't stored. Valid values are ``DEBUG`` , ``INFO`` (recommended), ``WARN`` , ``ERROR`` , or ``FATAL`` .
            :param space: The amount of file space (in KB) to use when writing logs to the local file system. This property does not apply for CloudWatch Logs .
            :param type: The storage mechanism for log events. Valid values are ``FileSystem`` or ``AWSCloudWatch`` . When ``AWSCloudWatch`` is used, log events are sent to CloudWatch Logs . When ``FileSystem`` is used, log events are stored on the local file system.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-loggerdefinitionversion-logger.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                logger_property = greengrass_mixins.CfnLoggerDefinitionVersionPropsMixin.LoggerProperty(
                    component="component",
                    id="id",
                    level="level",
                    space=123,
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cacdaa86e346686ae3c1e112658ce8ef33deafa29ce4fcaf668a37aa43750aba)
                check_type(argname="argument component", value=component, expected_type=type_hints["component"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument level", value=level, expected_type=type_hints["level"])
                check_type(argname="argument space", value=space, expected_type=type_hints["space"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if component is not None:
                self._values["component"] = component
            if id is not None:
                self._values["id"] = id
            if level is not None:
                self._values["level"] = level
            if space is not None:
                self._values["space"] = space
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def component(self) -> typing.Optional[builtins.str]:
            '''The source of the log event.

            Valid values are ``GreengrassSystem`` or ``Lambda`` . When ``GreengrassSystem`` is used, events from Greengrass system components are logged. When ``Lambda`` is used, events from user-defined Lambda functions are logged.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-loggerdefinitionversion-logger.html#cfn-greengrass-loggerdefinitionversion-logger-component
            '''
            result = self._values.get("component")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''A descriptive or arbitrary ID for the logger.

            This value must be unique within the logger definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-loggerdefinitionversion-logger.html#cfn-greengrass-loggerdefinitionversion-logger-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def level(self) -> typing.Optional[builtins.str]:
            '''The log-level threshold.

            Log events below this threshold are filtered out and aren't stored. Valid values are ``DEBUG`` , ``INFO`` (recommended), ``WARN`` , ``ERROR`` , or ``FATAL`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-loggerdefinitionversion-logger.html#cfn-greengrass-loggerdefinitionversion-logger-level
            '''
            result = self._values.get("level")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def space(self) -> typing.Optional[jsii.Number]:
            '''The amount of file space (in KB) to use when writing logs to the local file system.

            This property does not apply for CloudWatch Logs .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-loggerdefinitionversion-logger.html#cfn-greengrass-loggerdefinitionversion-logger-space
            '''
            result = self._values.get("space")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The storage mechanism for log events.

            Valid values are ``FileSystem`` or ``AWSCloudWatch`` . When ``AWSCloudWatch`` is used, log events are sent to CloudWatch Logs . When ``FileSystem`` is used, log events are stored on the local file system.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-loggerdefinitionversion-logger.html#cfn-greengrass-loggerdefinitionversion-logger-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggerProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnResourceDefinitionMixinProps",
    jsii_struct_bases=[],
    name_mapping={"initial_version": "initialVersion", "name": "name", "tags": "tags"},
)
class CfnResourceDefinitionMixinProps:
    def __init__(
        self,
        *,
        initial_version: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResourceDefinitionPropsMixin.ResourceDefinitionVersionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Properties for CfnResourceDefinitionPropsMixin.

        :param initial_version: The resource definition version to include when the resource definition is created. A resource definition version contains a list of ```resource instance`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourceinstance.html>`_ property types. .. epigraph:: To associate a resource definition version after the resource definition is created, create an ```AWS::Greengrass::ResourceDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-resourcedefinitionversion.html>`_ resource and specify the ID of this resource definition.
        :param name: The name of the resource definition.
        :param tags: Application-specific metadata to attach to the resource definition. You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/v1/developerguide/tagging.html>`_ in the *Developer Guide* . This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in CloudFormation templates:: "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value" }

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-resourcedefinition.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
            
            # tags: Any
            
            cfn_resource_definition_mixin_props = greengrass_mixins.CfnResourceDefinitionMixinProps(
                initial_version=greengrass_mixins.CfnResourceDefinitionPropsMixin.ResourceDefinitionVersionProperty(
                    resources=[greengrass_mixins.CfnResourceDefinitionPropsMixin.ResourceInstanceProperty(
                        id="id",
                        name="name",
                        resource_data_container=greengrass_mixins.CfnResourceDefinitionPropsMixin.ResourceDataContainerProperty(
                            local_device_resource_data=greengrass_mixins.CfnResourceDefinitionPropsMixin.LocalDeviceResourceDataProperty(
                                group_owner_setting=greengrass_mixins.CfnResourceDefinitionPropsMixin.GroupOwnerSettingProperty(
                                    auto_add_group_owner=False,
                                    group_owner="groupOwner"
                                ),
                                source_path="sourcePath"
                            ),
                            local_volume_resource_data=greengrass_mixins.CfnResourceDefinitionPropsMixin.LocalVolumeResourceDataProperty(
                                destination_path="destinationPath",
                                group_owner_setting=greengrass_mixins.CfnResourceDefinitionPropsMixin.GroupOwnerSettingProperty(
                                    auto_add_group_owner=False,
                                    group_owner="groupOwner"
                                ),
                                source_path="sourcePath"
                            ),
                            s3_machine_learning_model_resource_data=greengrass_mixins.CfnResourceDefinitionPropsMixin.S3MachineLearningModelResourceDataProperty(
                                destination_path="destinationPath",
                                owner_setting=greengrass_mixins.CfnResourceDefinitionPropsMixin.ResourceDownloadOwnerSettingProperty(
                                    group_owner="groupOwner",
                                    group_permission="groupPermission"
                                ),
                                s3_uri="s3Uri"
                            ),
                            sage_maker_machine_learning_model_resource_data=greengrass_mixins.CfnResourceDefinitionPropsMixin.SageMakerMachineLearningModelResourceDataProperty(
                                destination_path="destinationPath",
                                owner_setting=greengrass_mixins.CfnResourceDefinitionPropsMixin.ResourceDownloadOwnerSettingProperty(
                                    group_owner="groupOwner",
                                    group_permission="groupPermission"
                                ),
                                sage_maker_job_arn="sageMakerJobArn"
                            ),
                            secrets_manager_secret_resource_data=greengrass_mixins.CfnResourceDefinitionPropsMixin.SecretsManagerSecretResourceDataProperty(
                                additional_staging_labels_to_download=["additionalStagingLabelsToDownload"],
                                arn="arn"
                            )
                        )
                    )]
                ),
                name="name",
                tags=tags
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daec316b12d26e47c8dac50bc0b8e3fdf7d4b2217e32751e895025b145fea4f8)
            check_type(argname="argument initial_version", value=initial_version, expected_type=type_hints["initial_version"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if initial_version is not None:
            self._values["initial_version"] = initial_version
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def initial_version(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDefinitionPropsMixin.ResourceDefinitionVersionProperty"]]:
        '''The resource definition version to include when the resource definition is created.

        A resource definition version contains a list of ```resource instance`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourceinstance.html>`_ property types.
        .. epigraph::

           To associate a resource definition version after the resource definition is created, create an ```AWS::Greengrass::ResourceDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-resourcedefinitionversion.html>`_ resource and specify the ID of this resource definition.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-resourcedefinition.html#cfn-greengrass-resourcedefinition-initialversion
        '''
        result = self._values.get("initial_version")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDefinitionPropsMixin.ResourceDefinitionVersionProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the resource definition.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-resourcedefinition.html#cfn-greengrass-resourcedefinition-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''Application-specific metadata to attach to the resource definition.

        You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/v1/developerguide/tagging.html>`_ in the *Developer Guide* .

        This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in CloudFormation templates::

           "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value"
           }

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-resourcedefinition.html#cfn-greengrass-resourcedefinition-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourceDefinitionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnResourceDefinitionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnResourceDefinitionPropsMixin",
):
    '''The ``AWS::Greengrass::ResourceDefinition`` resource represents a resource definition for AWS IoT Greengrass .

    Resource definitions are used to organize your resource definition versions.

    Resource definitions can reference multiple resource definition versions. All resource definition versions must be associated with a resource definition. Each resource definition version can contain one or more resources. (In CloudFormation , resources are named *resource instances* .)
    .. epigraph::

       When you create a resource definition, you can optionally include an initial resource definition version. To associate a resource definition version later, create an ```AWS::Greengrass::ResourceDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-resourcedefinitionversion.html>`_ resource and specify the ID of this resource definition.

       After you create the resource definition version that contains the resources you want to deploy, you must add it to your group version. For more information, see ```AWS::Greengrass::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-resourcedefinition.html
    :cloudformationResource: AWS::Greengrass::ResourceDefinition
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
        
        # tags: Any
        
        cfn_resource_definition_props_mixin = greengrass_mixins.CfnResourceDefinitionPropsMixin(greengrass_mixins.CfnResourceDefinitionMixinProps(
            initial_version=greengrass_mixins.CfnResourceDefinitionPropsMixin.ResourceDefinitionVersionProperty(
                resources=[greengrass_mixins.CfnResourceDefinitionPropsMixin.ResourceInstanceProperty(
                    id="id",
                    name="name",
                    resource_data_container=greengrass_mixins.CfnResourceDefinitionPropsMixin.ResourceDataContainerProperty(
                        local_device_resource_data=greengrass_mixins.CfnResourceDefinitionPropsMixin.LocalDeviceResourceDataProperty(
                            group_owner_setting=greengrass_mixins.CfnResourceDefinitionPropsMixin.GroupOwnerSettingProperty(
                                auto_add_group_owner=False,
                                group_owner="groupOwner"
                            ),
                            source_path="sourcePath"
                        ),
                        local_volume_resource_data=greengrass_mixins.CfnResourceDefinitionPropsMixin.LocalVolumeResourceDataProperty(
                            destination_path="destinationPath",
                            group_owner_setting=greengrass_mixins.CfnResourceDefinitionPropsMixin.GroupOwnerSettingProperty(
                                auto_add_group_owner=False,
                                group_owner="groupOwner"
                            ),
                            source_path="sourcePath"
                        ),
                        s3_machine_learning_model_resource_data=greengrass_mixins.CfnResourceDefinitionPropsMixin.S3MachineLearningModelResourceDataProperty(
                            destination_path="destinationPath",
                            owner_setting=greengrass_mixins.CfnResourceDefinitionPropsMixin.ResourceDownloadOwnerSettingProperty(
                                group_owner="groupOwner",
                                group_permission="groupPermission"
                            ),
                            s3_uri="s3Uri"
                        ),
                        sage_maker_machine_learning_model_resource_data=greengrass_mixins.CfnResourceDefinitionPropsMixin.SageMakerMachineLearningModelResourceDataProperty(
                            destination_path="destinationPath",
                            owner_setting=greengrass_mixins.CfnResourceDefinitionPropsMixin.ResourceDownloadOwnerSettingProperty(
                                group_owner="groupOwner",
                                group_permission="groupPermission"
                            ),
                            sage_maker_job_arn="sageMakerJobArn"
                        ),
                        secrets_manager_secret_resource_data=greengrass_mixins.CfnResourceDefinitionPropsMixin.SecretsManagerSecretResourceDataProperty(
                            additional_staging_labels_to_download=["additionalStagingLabelsToDownload"],
                            arn="arn"
                        )
                    )
                )]
            ),
            name="name",
            tags=tags
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnResourceDefinitionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Greengrass::ResourceDefinition``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4e5d46e0b579098d4d6516c14fb858636b3544f39d6d45754a4c6826ecbd6e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__291f087829390f873bd080fc16bc4c0d5d61620457587afda4f4704989eeb1b8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3c6fb32ecc6199ff434b5b811bf6ea266f6da5141de8b69236bf4639eb7d580)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnResourceDefinitionMixinProps:
        return typing.cast(CfnResourceDefinitionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnResourceDefinitionPropsMixin.GroupOwnerSettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "auto_add_group_owner": "autoAddGroupOwner",
            "group_owner": "groupOwner",
        },
    )
    class GroupOwnerSettingProperty:
        def __init__(
            self,
            *,
            auto_add_group_owner: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            group_owner: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Settings that define additional Linux OS group permissions to give to the Lambda function process.

            You can give the permissions of the Linux group that owns the resource or choose another Linux group. These permissions are in addition to the function's ``RunAs`` permissions.

            In an CloudFormation template, ``GroupOwnerSetting`` is a property of the ```LocalDeviceResourceData`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-localdeviceresourcedata.html>`_ and ```LocalVolumeResourceData`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-localvolumeresourcedata.html>`_ property types.

            :param auto_add_group_owner: Indicates whether to give the privileges of the Linux group that owns the resource to the Lambda process. This gives the Lambda process the file access permissions of the Linux group.
            :param group_owner: The name of the Linux group whose privileges you want to add to the Lambda process. This value is ignored if ``AutoAddGroupOwner`` is true.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-groupownersetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                group_owner_setting_property = greengrass_mixins.CfnResourceDefinitionPropsMixin.GroupOwnerSettingProperty(
                    auto_add_group_owner=False,
                    group_owner="groupOwner"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4d3f000210f1dc195a347e848b3fb22a2172648705124b2dd915ad9717d991c4)
                check_type(argname="argument auto_add_group_owner", value=auto_add_group_owner, expected_type=type_hints["auto_add_group_owner"])
                check_type(argname="argument group_owner", value=group_owner, expected_type=type_hints["group_owner"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auto_add_group_owner is not None:
                self._values["auto_add_group_owner"] = auto_add_group_owner
            if group_owner is not None:
                self._values["group_owner"] = group_owner

        @builtins.property
        def auto_add_group_owner(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether to give the privileges of the Linux group that owns the resource to the Lambda process.

            This gives the Lambda process the file access permissions of the Linux group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-groupownersetting.html#cfn-greengrass-resourcedefinition-groupownersetting-autoaddgroupowner
            '''
            result = self._values.get("auto_add_group_owner")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def group_owner(self) -> typing.Optional[builtins.str]:
            '''The name of the Linux group whose privileges you want to add to the Lambda process.

            This value is ignored if ``AutoAddGroupOwner`` is true.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-groupownersetting.html#cfn-greengrass-resourcedefinition-groupownersetting-groupowner
            '''
            result = self._values.get("group_owner")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GroupOwnerSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnResourceDefinitionPropsMixin.LocalDeviceResourceDataProperty",
        jsii_struct_bases=[],
        name_mapping={
            "group_owner_setting": "groupOwnerSetting",
            "source_path": "sourcePath",
        },
    )
    class LocalDeviceResourceDataProperty:
        def __init__(
            self,
            *,
            group_owner_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResourceDefinitionPropsMixin.GroupOwnerSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            source_path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Settings for a local device resource, which represents a file under ``/dev`` .

            For more information, see `Access Local Resources with Lambda Functions <https://docs.aws.amazon.com/greengrass/v1/developerguide/access-local-resources.html>`_ in the *Developer Guide* .

            In an CloudFormation template, ``LocalDeviceResourceData`` can be used in the ```ResourceDataContainer`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourcedatacontainer.html>`_ property type.

            :param group_owner_setting: Settings that define additional Linux OS group permissions to give to the Lambda function process.
            :param source_path: The local absolute path of the device resource. The source path for a device resource can refer only to a character device or block device under ``/dev`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-localdeviceresourcedata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                local_device_resource_data_property = greengrass_mixins.CfnResourceDefinitionPropsMixin.LocalDeviceResourceDataProperty(
                    group_owner_setting=greengrass_mixins.CfnResourceDefinitionPropsMixin.GroupOwnerSettingProperty(
                        auto_add_group_owner=False,
                        group_owner="groupOwner"
                    ),
                    source_path="sourcePath"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__076cb180e78bb2959e8dc327fd2901a0ec5ddf69eea8737e417814012fb17390)
                check_type(argname="argument group_owner_setting", value=group_owner_setting, expected_type=type_hints["group_owner_setting"])
                check_type(argname="argument source_path", value=source_path, expected_type=type_hints["source_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if group_owner_setting is not None:
                self._values["group_owner_setting"] = group_owner_setting
            if source_path is not None:
                self._values["source_path"] = source_path

        @builtins.property
        def group_owner_setting(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDefinitionPropsMixin.GroupOwnerSettingProperty"]]:
            '''Settings that define additional Linux OS group permissions to give to the Lambda function process.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-localdeviceresourcedata.html#cfn-greengrass-resourcedefinition-localdeviceresourcedata-groupownersetting
            '''
            result = self._values.get("group_owner_setting")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDefinitionPropsMixin.GroupOwnerSettingProperty"]], result)

        @builtins.property
        def source_path(self) -> typing.Optional[builtins.str]:
            '''The local absolute path of the device resource.

            The source path for a device resource can refer only to a character device or block device under ``/dev`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-localdeviceresourcedata.html#cfn-greengrass-resourcedefinition-localdeviceresourcedata-sourcepath
            '''
            result = self._values.get("source_path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LocalDeviceResourceDataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnResourceDefinitionPropsMixin.LocalVolumeResourceDataProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_path": "destinationPath",
            "group_owner_setting": "groupOwnerSetting",
            "source_path": "sourcePath",
        },
    )
    class LocalVolumeResourceDataProperty:
        def __init__(
            self,
            *,
            destination_path: typing.Optional[builtins.str] = None,
            group_owner_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResourceDefinitionPropsMixin.GroupOwnerSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            source_path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Settings for a local volume resource, which represents a file or directory on the root file system.

            For more information, see `Access Local Resources with Lambda Functions <https://docs.aws.amazon.com/greengrass/v1/developerguide/access-local-resources.html>`_ in the *Developer Guide* .

            In an CloudFormation template, ``LocalVolumeResourceData`` can be used in the ```ResourceDataContainer`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourcedatacontainer.html>`_ property type.

            :param destination_path: The absolute local path of the resource in the Lambda environment.
            :param group_owner_setting: Settings that define additional Linux OS group permissions to give to the Lambda function process.
            :param source_path: The local absolute path of the volume resource on the host. The source path for a volume resource type cannot start with ``/sys`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-localvolumeresourcedata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                local_volume_resource_data_property = greengrass_mixins.CfnResourceDefinitionPropsMixin.LocalVolumeResourceDataProperty(
                    destination_path="destinationPath",
                    group_owner_setting=greengrass_mixins.CfnResourceDefinitionPropsMixin.GroupOwnerSettingProperty(
                        auto_add_group_owner=False,
                        group_owner="groupOwner"
                    ),
                    source_path="sourcePath"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__905fc9d4c49b27aec236f0178dd769db292b78362d44983e5583fb687da623e2)
                check_type(argname="argument destination_path", value=destination_path, expected_type=type_hints["destination_path"])
                check_type(argname="argument group_owner_setting", value=group_owner_setting, expected_type=type_hints["group_owner_setting"])
                check_type(argname="argument source_path", value=source_path, expected_type=type_hints["source_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination_path is not None:
                self._values["destination_path"] = destination_path
            if group_owner_setting is not None:
                self._values["group_owner_setting"] = group_owner_setting
            if source_path is not None:
                self._values["source_path"] = source_path

        @builtins.property
        def destination_path(self) -> typing.Optional[builtins.str]:
            '''The absolute local path of the resource in the Lambda environment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-localvolumeresourcedata.html#cfn-greengrass-resourcedefinition-localvolumeresourcedata-destinationpath
            '''
            result = self._values.get("destination_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def group_owner_setting(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDefinitionPropsMixin.GroupOwnerSettingProperty"]]:
            '''Settings that define additional Linux OS group permissions to give to the Lambda function process.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-localvolumeresourcedata.html#cfn-greengrass-resourcedefinition-localvolumeresourcedata-groupownersetting
            '''
            result = self._values.get("group_owner_setting")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDefinitionPropsMixin.GroupOwnerSettingProperty"]], result)

        @builtins.property
        def source_path(self) -> typing.Optional[builtins.str]:
            '''The local absolute path of the volume resource on the host.

            The source path for a volume resource type cannot start with ``/sys`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-localvolumeresourcedata.html#cfn-greengrass-resourcedefinition-localvolumeresourcedata-sourcepath
            '''
            result = self._values.get("source_path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LocalVolumeResourceDataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnResourceDefinitionPropsMixin.ResourceDataContainerProperty",
        jsii_struct_bases=[],
        name_mapping={
            "local_device_resource_data": "localDeviceResourceData",
            "local_volume_resource_data": "localVolumeResourceData",
            "s3_machine_learning_model_resource_data": "s3MachineLearningModelResourceData",
            "sage_maker_machine_learning_model_resource_data": "sageMakerMachineLearningModelResourceData",
            "secrets_manager_secret_resource_data": "secretsManagerSecretResourceData",
        },
    )
    class ResourceDataContainerProperty:
        def __init__(
            self,
            *,
            local_device_resource_data: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResourceDefinitionPropsMixin.LocalDeviceResourceDataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            local_volume_resource_data: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResourceDefinitionPropsMixin.LocalVolumeResourceDataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3_machine_learning_model_resource_data: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResourceDefinitionPropsMixin.S3MachineLearningModelResourceDataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sage_maker_machine_learning_model_resource_data: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResourceDefinitionPropsMixin.SageMakerMachineLearningModelResourceDataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            secrets_manager_secret_resource_data: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResourceDefinitionPropsMixin.SecretsManagerSecretResourceDataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A container for resource data, which defines the resource type.

            The container takes only one of the following supported resource data types: ``LocalDeviceResourceData`` , ``LocalVolumeResourceData`` , ``SageMakerMachineLearningModelResourceData`` , ``S3MachineLearningModelResourceData`` , or ``SecretsManagerSecretResourceData`` .
            .. epigraph::

               Only one resource type can be defined for a ``ResourceDataContainer`` instance.

            In an CloudFormation template, ``ResourceDataContainer`` is a property of the ```ResourceInstance`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourceinstance.html>`_ property type.

            :param local_device_resource_data: Settings for a local device resource.
            :param local_volume_resource_data: Settings for a local volume resource.
            :param s3_machine_learning_model_resource_data: Settings for a machine learning resource stored in Amazon S3 .
            :param sage_maker_machine_learning_model_resource_data: Settings for a machine learning resource saved as an SageMaker AI training job.
            :param secrets_manager_secret_resource_data: Settings for a secret resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourcedatacontainer.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                resource_data_container_property = greengrass_mixins.CfnResourceDefinitionPropsMixin.ResourceDataContainerProperty(
                    local_device_resource_data=greengrass_mixins.CfnResourceDefinitionPropsMixin.LocalDeviceResourceDataProperty(
                        group_owner_setting=greengrass_mixins.CfnResourceDefinitionPropsMixin.GroupOwnerSettingProperty(
                            auto_add_group_owner=False,
                            group_owner="groupOwner"
                        ),
                        source_path="sourcePath"
                    ),
                    local_volume_resource_data=greengrass_mixins.CfnResourceDefinitionPropsMixin.LocalVolumeResourceDataProperty(
                        destination_path="destinationPath",
                        group_owner_setting=greengrass_mixins.CfnResourceDefinitionPropsMixin.GroupOwnerSettingProperty(
                            auto_add_group_owner=False,
                            group_owner="groupOwner"
                        ),
                        source_path="sourcePath"
                    ),
                    s3_machine_learning_model_resource_data=greengrass_mixins.CfnResourceDefinitionPropsMixin.S3MachineLearningModelResourceDataProperty(
                        destination_path="destinationPath",
                        owner_setting=greengrass_mixins.CfnResourceDefinitionPropsMixin.ResourceDownloadOwnerSettingProperty(
                            group_owner="groupOwner",
                            group_permission="groupPermission"
                        ),
                        s3_uri="s3Uri"
                    ),
                    sage_maker_machine_learning_model_resource_data=greengrass_mixins.CfnResourceDefinitionPropsMixin.SageMakerMachineLearningModelResourceDataProperty(
                        destination_path="destinationPath",
                        owner_setting=greengrass_mixins.CfnResourceDefinitionPropsMixin.ResourceDownloadOwnerSettingProperty(
                            group_owner="groupOwner",
                            group_permission="groupPermission"
                        ),
                        sage_maker_job_arn="sageMakerJobArn"
                    ),
                    secrets_manager_secret_resource_data=greengrass_mixins.CfnResourceDefinitionPropsMixin.SecretsManagerSecretResourceDataProperty(
                        additional_staging_labels_to_download=["additionalStagingLabelsToDownload"],
                        arn="arn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0ee2633e07d5e0ee9f7ef319c08be058431ce90c7dc172cb4afb65048d4e65ad)
                check_type(argname="argument local_device_resource_data", value=local_device_resource_data, expected_type=type_hints["local_device_resource_data"])
                check_type(argname="argument local_volume_resource_data", value=local_volume_resource_data, expected_type=type_hints["local_volume_resource_data"])
                check_type(argname="argument s3_machine_learning_model_resource_data", value=s3_machine_learning_model_resource_data, expected_type=type_hints["s3_machine_learning_model_resource_data"])
                check_type(argname="argument sage_maker_machine_learning_model_resource_data", value=sage_maker_machine_learning_model_resource_data, expected_type=type_hints["sage_maker_machine_learning_model_resource_data"])
                check_type(argname="argument secrets_manager_secret_resource_data", value=secrets_manager_secret_resource_data, expected_type=type_hints["secrets_manager_secret_resource_data"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if local_device_resource_data is not None:
                self._values["local_device_resource_data"] = local_device_resource_data
            if local_volume_resource_data is not None:
                self._values["local_volume_resource_data"] = local_volume_resource_data
            if s3_machine_learning_model_resource_data is not None:
                self._values["s3_machine_learning_model_resource_data"] = s3_machine_learning_model_resource_data
            if sage_maker_machine_learning_model_resource_data is not None:
                self._values["sage_maker_machine_learning_model_resource_data"] = sage_maker_machine_learning_model_resource_data
            if secrets_manager_secret_resource_data is not None:
                self._values["secrets_manager_secret_resource_data"] = secrets_manager_secret_resource_data

        @builtins.property
        def local_device_resource_data(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDefinitionPropsMixin.LocalDeviceResourceDataProperty"]]:
            '''Settings for a local device resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourcedatacontainer.html#cfn-greengrass-resourcedefinition-resourcedatacontainer-localdeviceresourcedata
            '''
            result = self._values.get("local_device_resource_data")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDefinitionPropsMixin.LocalDeviceResourceDataProperty"]], result)

        @builtins.property
        def local_volume_resource_data(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDefinitionPropsMixin.LocalVolumeResourceDataProperty"]]:
            '''Settings for a local volume resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourcedatacontainer.html#cfn-greengrass-resourcedefinition-resourcedatacontainer-localvolumeresourcedata
            '''
            result = self._values.get("local_volume_resource_data")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDefinitionPropsMixin.LocalVolumeResourceDataProperty"]], result)

        @builtins.property
        def s3_machine_learning_model_resource_data(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDefinitionPropsMixin.S3MachineLearningModelResourceDataProperty"]]:
            '''Settings for a machine learning resource stored in Amazon S3 .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourcedatacontainer.html#cfn-greengrass-resourcedefinition-resourcedatacontainer-s3machinelearningmodelresourcedata
            '''
            result = self._values.get("s3_machine_learning_model_resource_data")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDefinitionPropsMixin.S3MachineLearningModelResourceDataProperty"]], result)

        @builtins.property
        def sage_maker_machine_learning_model_resource_data(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDefinitionPropsMixin.SageMakerMachineLearningModelResourceDataProperty"]]:
            '''Settings for a machine learning resource saved as an SageMaker AI training job.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourcedatacontainer.html#cfn-greengrass-resourcedefinition-resourcedatacontainer-sagemakermachinelearningmodelresourcedata
            '''
            result = self._values.get("sage_maker_machine_learning_model_resource_data")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDefinitionPropsMixin.SageMakerMachineLearningModelResourceDataProperty"]], result)

        @builtins.property
        def secrets_manager_secret_resource_data(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDefinitionPropsMixin.SecretsManagerSecretResourceDataProperty"]]:
            '''Settings for a secret resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourcedatacontainer.html#cfn-greengrass-resourcedefinition-resourcedatacontainer-secretsmanagersecretresourcedata
            '''
            result = self._values.get("secrets_manager_secret_resource_data")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDefinitionPropsMixin.SecretsManagerSecretResourceDataProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceDataContainerProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnResourceDefinitionPropsMixin.ResourceDefinitionVersionProperty",
        jsii_struct_bases=[],
        name_mapping={"resources": "resources"},
    )
    class ResourceDefinitionVersionProperty:
        def __init__(
            self,
            *,
            resources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResourceDefinitionPropsMixin.ResourceInstanceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''A resource definition version contains a list of resources. (In CloudFormation , resources are named *resource instances* .).

            .. epigraph::

               After you create a resource definition version that contains the resources you want to deploy, you must add it to your group version. For more information, see ```AWS::Greengrass::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html>`_ .

            In an CloudFormation template, ``ResourceDefinitionVersion`` is the property type of the ``InitialVersion`` property in the ```AWS::Greengrass::ResourceDefinition`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-resourcedefinition.html>`_ resource.

            :param resources: The resources in this version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourcedefinitionversion.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                resource_definition_version_property = greengrass_mixins.CfnResourceDefinitionPropsMixin.ResourceDefinitionVersionProperty(
                    resources=[greengrass_mixins.CfnResourceDefinitionPropsMixin.ResourceInstanceProperty(
                        id="id",
                        name="name",
                        resource_data_container=greengrass_mixins.CfnResourceDefinitionPropsMixin.ResourceDataContainerProperty(
                            local_device_resource_data=greengrass_mixins.CfnResourceDefinitionPropsMixin.LocalDeviceResourceDataProperty(
                                group_owner_setting=greengrass_mixins.CfnResourceDefinitionPropsMixin.GroupOwnerSettingProperty(
                                    auto_add_group_owner=False,
                                    group_owner="groupOwner"
                                ),
                                source_path="sourcePath"
                            ),
                            local_volume_resource_data=greengrass_mixins.CfnResourceDefinitionPropsMixin.LocalVolumeResourceDataProperty(
                                destination_path="destinationPath",
                                group_owner_setting=greengrass_mixins.CfnResourceDefinitionPropsMixin.GroupOwnerSettingProperty(
                                    auto_add_group_owner=False,
                                    group_owner="groupOwner"
                                ),
                                source_path="sourcePath"
                            ),
                            s3_machine_learning_model_resource_data=greengrass_mixins.CfnResourceDefinitionPropsMixin.S3MachineLearningModelResourceDataProperty(
                                destination_path="destinationPath",
                                owner_setting=greengrass_mixins.CfnResourceDefinitionPropsMixin.ResourceDownloadOwnerSettingProperty(
                                    group_owner="groupOwner",
                                    group_permission="groupPermission"
                                ),
                                s3_uri="s3Uri"
                            ),
                            sage_maker_machine_learning_model_resource_data=greengrass_mixins.CfnResourceDefinitionPropsMixin.SageMakerMachineLearningModelResourceDataProperty(
                                destination_path="destinationPath",
                                owner_setting=greengrass_mixins.CfnResourceDefinitionPropsMixin.ResourceDownloadOwnerSettingProperty(
                                    group_owner="groupOwner",
                                    group_permission="groupPermission"
                                ),
                                sage_maker_job_arn="sageMakerJobArn"
                            ),
                            secrets_manager_secret_resource_data=greengrass_mixins.CfnResourceDefinitionPropsMixin.SecretsManagerSecretResourceDataProperty(
                                additional_staging_labels_to_download=["additionalStagingLabelsToDownload"],
                                arn="arn"
                            )
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ace4a1020dc67c92704d8bd2058ee04e2465c5c813824ab3ba9b10be2b6430a5)
                check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if resources is not None:
                self._values["resources"] = resources

        @builtins.property
        def resources(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDefinitionPropsMixin.ResourceInstanceProperty"]]]]:
            '''The resources in this version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourcedefinitionversion.html#cfn-greengrass-resourcedefinition-resourcedefinitionversion-resources
            '''
            result = self._values.get("resources")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDefinitionPropsMixin.ResourceInstanceProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceDefinitionVersionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnResourceDefinitionPropsMixin.ResourceDownloadOwnerSettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "group_owner": "groupOwner",
            "group_permission": "groupPermission",
        },
    )
    class ResourceDownloadOwnerSettingProperty:
        def __init__(
            self,
            *,
            group_owner: typing.Optional[builtins.str] = None,
            group_permission: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The owner setting for a downloaded machine learning resource.

            For more information, see `Access Machine Learning Resources from Lambda Functions <https://docs.aws.amazon.com/greengrass/v1/developerguide/access-ml-resources.html>`_ in the *Developer Guide* .

            In an CloudFormation template, ``ResourceDownloadOwnerSetting`` is the property type of the ``OwnerSetting`` property for the ```S3MachineLearningModelResourceData`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-s3machinelearningmodelresourcedata.html>`_ and ```SageMakerMachineLearningModelResourceData`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-sagemakermachinelearningmodelresourcedata.html>`_ property types.

            :param group_owner: The group owner of the machine learning resource. This is the group ID (GID) of an existing Linux OS group on the system. The group's permissions are added to the Lambda process.
            :param group_permission: The permissions that the group owner has to the machine learning resource. Valid values are ``rw`` (read-write) or ``ro`` (read-only).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourcedownloadownersetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                resource_download_owner_setting_property = greengrass_mixins.CfnResourceDefinitionPropsMixin.ResourceDownloadOwnerSettingProperty(
                    group_owner="groupOwner",
                    group_permission="groupPermission"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7a44afeb1dbca52baee179ecbe3563ed14d1720bb7eb2859671986aa767582a2)
                check_type(argname="argument group_owner", value=group_owner, expected_type=type_hints["group_owner"])
                check_type(argname="argument group_permission", value=group_permission, expected_type=type_hints["group_permission"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if group_owner is not None:
                self._values["group_owner"] = group_owner
            if group_permission is not None:
                self._values["group_permission"] = group_permission

        @builtins.property
        def group_owner(self) -> typing.Optional[builtins.str]:
            '''The group owner of the machine learning resource.

            This is the group ID (GID) of an existing Linux OS group on the system. The group's permissions are added to the Lambda process.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourcedownloadownersetting.html#cfn-greengrass-resourcedefinition-resourcedownloadownersetting-groupowner
            '''
            result = self._values.get("group_owner")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def group_permission(self) -> typing.Optional[builtins.str]:
            '''The permissions that the group owner has to the machine learning resource.

            Valid values are ``rw`` (read-write) or ``ro`` (read-only).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourcedownloadownersetting.html#cfn-greengrass-resourcedefinition-resourcedownloadownersetting-grouppermission
            '''
            result = self._values.get("group_permission")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceDownloadOwnerSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnResourceDefinitionPropsMixin.ResourceInstanceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "id": "id",
            "name": "name",
            "resource_data_container": "resourceDataContainer",
        },
    )
    class ResourceInstanceProperty:
        def __init__(
            self,
            *,
            id: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            resource_data_container: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResourceDefinitionPropsMixin.ResourceDataContainerProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A local resource, machine learning resource, or secret resource.

            For more information, see `Access Local Resources with Lambda Functions <https://docs.aws.amazon.com/greengrass/v1/developerguide/access-local-resources.html>`_ , `Perform Machine Learning Inference <https://docs.aws.amazon.com/greengrass/v1/developerguide/ml-inference.html>`_ , and `Deploy Secrets to the AWS IoT Greengrass Core <https://docs.aws.amazon.com/greengrass/v1/developerguide/secrets.html>`_ in the *Developer Guide* .

            In an CloudFormation template, the ``Resources`` property of the ```AWS::Greengrass::ResourceDefinition`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-resourcedefinition.html>`_ resource contains a list of ``ResourceInstance`` property types.

            :param id: A descriptive or arbitrary ID for the resource. This value must be unique within the resource definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .
            :param name: The descriptive resource name, which is displayed on the AWS IoT Greengrass console. Maximum length 128 characters with pattern [a-zA-Z0-9:_-]+. This must be unique within a Greengrass group.
            :param resource_data_container: A container for resource data. The container takes only one of the following supported resource data types: ``LocalDeviceResourceData`` , ``LocalVolumeResourceData`` , ``SageMakerMachineLearningModelResourceData`` , ``S3MachineLearningModelResourceData`` , or ``SecretsManagerSecretResourceData`` . .. epigraph:: Only one resource type can be defined for a ``ResourceDataContainer`` instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourceinstance.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                resource_instance_property = greengrass_mixins.CfnResourceDefinitionPropsMixin.ResourceInstanceProperty(
                    id="id",
                    name="name",
                    resource_data_container=greengrass_mixins.CfnResourceDefinitionPropsMixin.ResourceDataContainerProperty(
                        local_device_resource_data=greengrass_mixins.CfnResourceDefinitionPropsMixin.LocalDeviceResourceDataProperty(
                            group_owner_setting=greengrass_mixins.CfnResourceDefinitionPropsMixin.GroupOwnerSettingProperty(
                                auto_add_group_owner=False,
                                group_owner="groupOwner"
                            ),
                            source_path="sourcePath"
                        ),
                        local_volume_resource_data=greengrass_mixins.CfnResourceDefinitionPropsMixin.LocalVolumeResourceDataProperty(
                            destination_path="destinationPath",
                            group_owner_setting=greengrass_mixins.CfnResourceDefinitionPropsMixin.GroupOwnerSettingProperty(
                                auto_add_group_owner=False,
                                group_owner="groupOwner"
                            ),
                            source_path="sourcePath"
                        ),
                        s3_machine_learning_model_resource_data=greengrass_mixins.CfnResourceDefinitionPropsMixin.S3MachineLearningModelResourceDataProperty(
                            destination_path="destinationPath",
                            owner_setting=greengrass_mixins.CfnResourceDefinitionPropsMixin.ResourceDownloadOwnerSettingProperty(
                                group_owner="groupOwner",
                                group_permission="groupPermission"
                            ),
                            s3_uri="s3Uri"
                        ),
                        sage_maker_machine_learning_model_resource_data=greengrass_mixins.CfnResourceDefinitionPropsMixin.SageMakerMachineLearningModelResourceDataProperty(
                            destination_path="destinationPath",
                            owner_setting=greengrass_mixins.CfnResourceDefinitionPropsMixin.ResourceDownloadOwnerSettingProperty(
                                group_owner="groupOwner",
                                group_permission="groupPermission"
                            ),
                            sage_maker_job_arn="sageMakerJobArn"
                        ),
                        secrets_manager_secret_resource_data=greengrass_mixins.CfnResourceDefinitionPropsMixin.SecretsManagerSecretResourceDataProperty(
                            additional_staging_labels_to_download=["additionalStagingLabelsToDownload"],
                            arn="arn"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__89e2ca09d217847aa8aca952e0f8707f84a3b48430c8eb0d55788ea75681eff7)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument resource_data_container", value=resource_data_container, expected_type=type_hints["resource_data_container"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if id is not None:
                self._values["id"] = id
            if name is not None:
                self._values["name"] = name
            if resource_data_container is not None:
                self._values["resource_data_container"] = resource_data_container

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''A descriptive or arbitrary ID for the resource.

            This value must be unique within the resource definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourceinstance.html#cfn-greengrass-resourcedefinition-resourceinstance-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The descriptive resource name, which is displayed on the AWS IoT Greengrass console.

            Maximum length 128 characters with pattern [a-zA-Z0-9:_-]+. This must be unique within a Greengrass group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourceinstance.html#cfn-greengrass-resourcedefinition-resourceinstance-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_data_container(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDefinitionPropsMixin.ResourceDataContainerProperty"]]:
            '''A container for resource data.

            The container takes only one of the following supported resource data types: ``LocalDeviceResourceData`` , ``LocalVolumeResourceData`` , ``SageMakerMachineLearningModelResourceData`` , ``S3MachineLearningModelResourceData`` , or ``SecretsManagerSecretResourceData`` .
            .. epigraph::

               Only one resource type can be defined for a ``ResourceDataContainer`` instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourceinstance.html#cfn-greengrass-resourcedefinition-resourceinstance-resourcedatacontainer
            '''
            result = self._values.get("resource_data_container")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDefinitionPropsMixin.ResourceDataContainerProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceInstanceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnResourceDefinitionPropsMixin.S3MachineLearningModelResourceDataProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_path": "destinationPath",
            "owner_setting": "ownerSetting",
            "s3_uri": "s3Uri",
        },
    )
    class S3MachineLearningModelResourceDataProperty:
        def __init__(
            self,
            *,
            destination_path: typing.Optional[builtins.str] = None,
            owner_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResourceDefinitionPropsMixin.ResourceDownloadOwnerSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3_uri: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Settings for an Amazon S3 machine learning resource.

            For more information, see `Perform Machine Learning Inference <https://docs.aws.amazon.com/greengrass/v1/developerguide/ml-inference.html>`_ in the *Developer Guide* .

            In an CloudFormation template, ``S3MachineLearningModelResourceData`` can be used in the ```ResourceDataContainer`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourcedatacontainer.html>`_ property type.

            :param destination_path: The absolute local path of the resource inside the Lambda environment.
            :param owner_setting: The owner setting for the downloaded machine learning resource. For more information, see `Access Machine Learning Resources from Lambda Functions <https://docs.aws.amazon.com/greengrass/v1/developerguide/access-ml-resources.html>`_ in the *Developer Guide* .
            :param s3_uri: The URI of the source model in an Amazon S3 bucket. The model package must be in ``tar.gz`` or ``.zip`` format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-s3machinelearningmodelresourcedata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                s3_machine_learning_model_resource_data_property = greengrass_mixins.CfnResourceDefinitionPropsMixin.S3MachineLearningModelResourceDataProperty(
                    destination_path="destinationPath",
                    owner_setting=greengrass_mixins.CfnResourceDefinitionPropsMixin.ResourceDownloadOwnerSettingProperty(
                        group_owner="groupOwner",
                        group_permission="groupPermission"
                    ),
                    s3_uri="s3Uri"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1757c8a3d80cae85eaf3a35c62cd360edc3d2700ad468a5d14d85c37851d7b11)
                check_type(argname="argument destination_path", value=destination_path, expected_type=type_hints["destination_path"])
                check_type(argname="argument owner_setting", value=owner_setting, expected_type=type_hints["owner_setting"])
                check_type(argname="argument s3_uri", value=s3_uri, expected_type=type_hints["s3_uri"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination_path is not None:
                self._values["destination_path"] = destination_path
            if owner_setting is not None:
                self._values["owner_setting"] = owner_setting
            if s3_uri is not None:
                self._values["s3_uri"] = s3_uri

        @builtins.property
        def destination_path(self) -> typing.Optional[builtins.str]:
            '''The absolute local path of the resource inside the Lambda environment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-s3machinelearningmodelresourcedata.html#cfn-greengrass-resourcedefinition-s3machinelearningmodelresourcedata-destinationpath
            '''
            result = self._values.get("destination_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def owner_setting(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDefinitionPropsMixin.ResourceDownloadOwnerSettingProperty"]]:
            '''The owner setting for the downloaded machine learning resource.

            For more information, see `Access Machine Learning Resources from Lambda Functions <https://docs.aws.amazon.com/greengrass/v1/developerguide/access-ml-resources.html>`_ in the *Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-s3machinelearningmodelresourcedata.html#cfn-greengrass-resourcedefinition-s3machinelearningmodelresourcedata-ownersetting
            '''
            result = self._values.get("owner_setting")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDefinitionPropsMixin.ResourceDownloadOwnerSettingProperty"]], result)

        @builtins.property
        def s3_uri(self) -> typing.Optional[builtins.str]:
            '''The URI of the source model in an Amazon S3 bucket.

            The model package must be in ``tar.gz`` or ``.zip`` format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-s3machinelearningmodelresourcedata.html#cfn-greengrass-resourcedefinition-s3machinelearningmodelresourcedata-s3uri
            '''
            result = self._values.get("s3_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3MachineLearningModelResourceDataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnResourceDefinitionPropsMixin.SageMakerMachineLearningModelResourceDataProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_path": "destinationPath",
            "owner_setting": "ownerSetting",
            "sage_maker_job_arn": "sageMakerJobArn",
        },
    )
    class SageMakerMachineLearningModelResourceDataProperty:
        def __init__(
            self,
            *,
            destination_path: typing.Optional[builtins.str] = None,
            owner_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResourceDefinitionPropsMixin.ResourceDownloadOwnerSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sage_maker_job_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Settings for an Secrets Manager machine learning resource.

            For more information, see `Perform Machine Learning Inference <https://docs.aws.amazon.com/greengrass/v1/developerguide/ml-inference.html>`_ in the *Developer Guide* .

            In an CloudFormation template, ``SageMakerMachineLearningModelResourceData`` can be used in the ```ResourceDataContainer`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourcedatacontainer.html>`_ property type.

            :param destination_path: The absolute local path of the resource inside the Lambda environment.
            :param owner_setting: The owner setting for the downloaded machine learning resource. For more information, see `Access Machine Learning Resources from Lambda Functions <https://docs.aws.amazon.com/greengrass/v1/developerguide/access-ml-resources.html>`_ in the *Developer Guide* .
            :param sage_maker_job_arn: The Amazon Resource Name (ARN) of the Amazon SageMaker AI training job that represents the source model.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-sagemakermachinelearningmodelresourcedata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                sage_maker_machine_learning_model_resource_data_property = greengrass_mixins.CfnResourceDefinitionPropsMixin.SageMakerMachineLearningModelResourceDataProperty(
                    destination_path="destinationPath",
                    owner_setting=greengrass_mixins.CfnResourceDefinitionPropsMixin.ResourceDownloadOwnerSettingProperty(
                        group_owner="groupOwner",
                        group_permission="groupPermission"
                    ),
                    sage_maker_job_arn="sageMakerJobArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__abdb831801448da68595ed60f8754d61126f819c5ec63c11b8e167c9f193dbf9)
                check_type(argname="argument destination_path", value=destination_path, expected_type=type_hints["destination_path"])
                check_type(argname="argument owner_setting", value=owner_setting, expected_type=type_hints["owner_setting"])
                check_type(argname="argument sage_maker_job_arn", value=sage_maker_job_arn, expected_type=type_hints["sage_maker_job_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination_path is not None:
                self._values["destination_path"] = destination_path
            if owner_setting is not None:
                self._values["owner_setting"] = owner_setting
            if sage_maker_job_arn is not None:
                self._values["sage_maker_job_arn"] = sage_maker_job_arn

        @builtins.property
        def destination_path(self) -> typing.Optional[builtins.str]:
            '''The absolute local path of the resource inside the Lambda environment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-sagemakermachinelearningmodelresourcedata.html#cfn-greengrass-resourcedefinition-sagemakermachinelearningmodelresourcedata-destinationpath
            '''
            result = self._values.get("destination_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def owner_setting(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDefinitionPropsMixin.ResourceDownloadOwnerSettingProperty"]]:
            '''The owner setting for the downloaded machine learning resource.

            For more information, see `Access Machine Learning Resources from Lambda Functions <https://docs.aws.amazon.com/greengrass/v1/developerguide/access-ml-resources.html>`_ in the *Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-sagemakermachinelearningmodelresourcedata.html#cfn-greengrass-resourcedefinition-sagemakermachinelearningmodelresourcedata-ownersetting
            '''
            result = self._values.get("owner_setting")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDefinitionPropsMixin.ResourceDownloadOwnerSettingProperty"]], result)

        @builtins.property
        def sage_maker_job_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Amazon SageMaker AI training job that represents the source model.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-sagemakermachinelearningmodelresourcedata.html#cfn-greengrass-resourcedefinition-sagemakermachinelearningmodelresourcedata-sagemakerjobarn
            '''
            result = self._values.get("sage_maker_job_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SageMakerMachineLearningModelResourceDataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnResourceDefinitionPropsMixin.SecretsManagerSecretResourceDataProperty",
        jsii_struct_bases=[],
        name_mapping={
            "additional_staging_labels_to_download": "additionalStagingLabelsToDownload",
            "arn": "arn",
        },
    )
    class SecretsManagerSecretResourceDataProperty:
        def __init__(
            self,
            *,
            additional_staging_labels_to_download: typing.Optional[typing.Sequence[builtins.str]] = None,
            arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Settings for a secret resource, which references a secret from AWS Secrets Manager .

            AWS IoT Greengrass stores a local, encrypted copy of the secret on the Greengrass core, where it can be securely accessed by connectors and Lambda functions. For more information, see `Deploy Secrets to the AWS IoT Greengrass Core <https://docs.aws.amazon.com/greengrass/v1/developerguide/secrets.html>`_ in the *Developer Guide* .

            In an CloudFormation template, ``SecretsManagerSecretResourceData`` can be used in the ```ResourceDataContainer`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourcedatacontainer.html>`_ property type.

            :param additional_staging_labels_to_download: The staging labels whose values you want to make available on the core, in addition to ``AWSCURRENT`` .
            :param arn: The Amazon Resource Name (ARN) of the Secrets Manager secret to make available on the core. The value of the secret's latest version (represented by the ``AWSCURRENT`` staging label) is included by default.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-secretsmanagersecretresourcedata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                secrets_manager_secret_resource_data_property = greengrass_mixins.CfnResourceDefinitionPropsMixin.SecretsManagerSecretResourceDataProperty(
                    additional_staging_labels_to_download=["additionalStagingLabelsToDownload"],
                    arn="arn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__726e4235d2c6af532b336c4fa97b43b044df064e8dd80698740e3e7f01706dc1)
                check_type(argname="argument additional_staging_labels_to_download", value=additional_staging_labels_to_download, expected_type=type_hints["additional_staging_labels_to_download"])
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if additional_staging_labels_to_download is not None:
                self._values["additional_staging_labels_to_download"] = additional_staging_labels_to_download
            if arn is not None:
                self._values["arn"] = arn

        @builtins.property
        def additional_staging_labels_to_download(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''The staging labels whose values you want to make available on the core, in addition to ``AWSCURRENT`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-secretsmanagersecretresourcedata.html#cfn-greengrass-resourcedefinition-secretsmanagersecretresourcedata-additionalstaginglabelstodownload
            '''
            result = self._values.get("additional_staging_labels_to_download")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Secrets Manager secret to make available on the core.

            The value of the secret's latest version (represented by the ``AWSCURRENT`` staging label) is included by default.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-secretsmanagersecretresourcedata.html#cfn-greengrass-resourcedefinition-secretsmanagersecretresourcedata-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SecretsManagerSecretResourceDataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnResourceDefinitionVersionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "resource_definition_id": "resourceDefinitionId",
        "resources": "resources",
    },
)
class CfnResourceDefinitionVersionMixinProps:
    def __init__(
        self,
        *,
        resource_definition_id: typing.Optional[builtins.str] = None,
        resources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResourceDefinitionVersionPropsMixin.ResourceInstanceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnResourceDefinitionVersionPropsMixin.

        :param resource_definition_id: The ID of the resource definition associated with this version. This value is a GUID.
        :param resources: The resources in this version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-resourcedefinitionversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
            
            cfn_resource_definition_version_mixin_props = greengrass_mixins.CfnResourceDefinitionVersionMixinProps(
                resource_definition_id="resourceDefinitionId",
                resources=[greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.ResourceInstanceProperty(
                    id="id",
                    name="name",
                    resource_data_container=greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.ResourceDataContainerProperty(
                        local_device_resource_data=greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.LocalDeviceResourceDataProperty(
                            group_owner_setting=greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.GroupOwnerSettingProperty(
                                auto_add_group_owner=False,
                                group_owner="groupOwner"
                            ),
                            source_path="sourcePath"
                        ),
                        local_volume_resource_data=greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.LocalVolumeResourceDataProperty(
                            destination_path="destinationPath",
                            group_owner_setting=greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.GroupOwnerSettingProperty(
                                auto_add_group_owner=False,
                                group_owner="groupOwner"
                            ),
                            source_path="sourcePath"
                        ),
                        s3_machine_learning_model_resource_data=greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.S3MachineLearningModelResourceDataProperty(
                            destination_path="destinationPath",
                            owner_setting=greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.ResourceDownloadOwnerSettingProperty(
                                group_owner="groupOwner",
                                group_permission="groupPermission"
                            ),
                            s3_uri="s3Uri"
                        ),
                        sage_maker_machine_learning_model_resource_data=greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.SageMakerMachineLearningModelResourceDataProperty(
                            destination_path="destinationPath",
                            owner_setting=greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.ResourceDownloadOwnerSettingProperty(
                                group_owner="groupOwner",
                                group_permission="groupPermission"
                            ),
                            sage_maker_job_arn="sageMakerJobArn"
                        ),
                        secrets_manager_secret_resource_data=greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.SecretsManagerSecretResourceDataProperty(
                            additional_staging_labels_to_download=["additionalStagingLabelsToDownload"],
                            arn="arn"
                        )
                    )
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f9a7b0846b4c13bd74f9ec5ac53048e65db6e3a8e3e870e47a5e196bdb2999c)
            check_type(argname="argument resource_definition_id", value=resource_definition_id, expected_type=type_hints["resource_definition_id"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if resource_definition_id is not None:
            self._values["resource_definition_id"] = resource_definition_id
        if resources is not None:
            self._values["resources"] = resources

    @builtins.property
    def resource_definition_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the resource definition associated with this version.

        This value is a GUID.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-resourcedefinitionversion.html#cfn-greengrass-resourcedefinitionversion-resourcedefinitionid
        '''
        result = self._values.get("resource_definition_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resources(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDefinitionVersionPropsMixin.ResourceInstanceProperty"]]]]:
        '''The resources in this version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-resourcedefinitionversion.html#cfn-greengrass-resourcedefinitionversion-resources
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDefinitionVersionPropsMixin.ResourceInstanceProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourceDefinitionVersionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnResourceDefinitionVersionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnResourceDefinitionVersionPropsMixin",
):
    '''The ``AWS::Greengrass::ResourceDefinitionVersion`` resource represents a resource definition version for AWS IoT Greengrass .

    A resource definition version contains a list of resources. (In CloudFormation , resources are named *resource instances* .)
    .. epigraph::

       To create a resource definition version, you must specify the ID of the resource definition that you want to associate with the version. For information about creating a resource definition, see ```AWS::Greengrass::ResourceDefinition`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-resourcedefinition.html>`_ .

       After you create a resource definition version that contains the resources you want to deploy, you must add it to your group version. For more information, see ```AWS::Greengrass::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-resourcedefinitionversion.html
    :cloudformationResource: AWS::Greengrass::ResourceDefinitionVersion
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
        
        cfn_resource_definition_version_props_mixin = greengrass_mixins.CfnResourceDefinitionVersionPropsMixin(greengrass_mixins.CfnResourceDefinitionVersionMixinProps(
            resource_definition_id="resourceDefinitionId",
            resources=[greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.ResourceInstanceProperty(
                id="id",
                name="name",
                resource_data_container=greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.ResourceDataContainerProperty(
                    local_device_resource_data=greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.LocalDeviceResourceDataProperty(
                        group_owner_setting=greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.GroupOwnerSettingProperty(
                            auto_add_group_owner=False,
                            group_owner="groupOwner"
                        ),
                        source_path="sourcePath"
                    ),
                    local_volume_resource_data=greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.LocalVolumeResourceDataProperty(
                        destination_path="destinationPath",
                        group_owner_setting=greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.GroupOwnerSettingProperty(
                            auto_add_group_owner=False,
                            group_owner="groupOwner"
                        ),
                        source_path="sourcePath"
                    ),
                    s3_machine_learning_model_resource_data=greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.S3MachineLearningModelResourceDataProperty(
                        destination_path="destinationPath",
                        owner_setting=greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.ResourceDownloadOwnerSettingProperty(
                            group_owner="groupOwner",
                            group_permission="groupPermission"
                        ),
                        s3_uri="s3Uri"
                    ),
                    sage_maker_machine_learning_model_resource_data=greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.SageMakerMachineLearningModelResourceDataProperty(
                        destination_path="destinationPath",
                        owner_setting=greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.ResourceDownloadOwnerSettingProperty(
                            group_owner="groupOwner",
                            group_permission="groupPermission"
                        ),
                        sage_maker_job_arn="sageMakerJobArn"
                    ),
                    secrets_manager_secret_resource_data=greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.SecretsManagerSecretResourceDataProperty(
                        additional_staging_labels_to_download=["additionalStagingLabelsToDownload"],
                        arn="arn"
                    )
                )
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnResourceDefinitionVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Greengrass::ResourceDefinitionVersion``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f028c34c2b3dd5fa2cb084a81e2c6cf9a36622c275ff749e1835dc303e51e8b5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__de0746b20847abf6ee330378fa518616d6dc17b2fd05e429485e16fe1cf62ef5)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25315b24341d185f256cafab933501168b49d9d4949a2cc26858ed1b60e90e7e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnResourceDefinitionVersionMixinProps:
        return typing.cast(CfnResourceDefinitionVersionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnResourceDefinitionVersionPropsMixin.GroupOwnerSettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "auto_add_group_owner": "autoAddGroupOwner",
            "group_owner": "groupOwner",
        },
    )
    class GroupOwnerSettingProperty:
        def __init__(
            self,
            *,
            auto_add_group_owner: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            group_owner: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Settings that define additional Linux OS group permissions to give to the Lambda function process.

            You can give the permissions of the Linux group that owns the resource or choose another Linux group. These permissions are in addition to the function's ``RunAs`` permissions.

            In an CloudFormation template, ``GroupOwnerSetting`` is a property of the ```LocalDeviceResourceData`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-localdeviceresourcedata.html>`_ and ```LocalVolumeResourceData`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-localvolumeresourcedata.html>`_ property types.

            :param auto_add_group_owner: Indicates whether to give the privileges of the Linux group that owns the resource to the Lambda process. This gives the Lambda process the file access permissions of the Linux group.
            :param group_owner: The name of the Linux group whose privileges you want to add to the Lambda process. This value is ignored if ``AutoAddGroupOwner`` is true.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-groupownersetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                group_owner_setting_property = greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.GroupOwnerSettingProperty(
                    auto_add_group_owner=False,
                    group_owner="groupOwner"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d60725ac803ffba779c0de5ca65f82c90080628c77d04af6cdc5fa1e02c5bd58)
                check_type(argname="argument auto_add_group_owner", value=auto_add_group_owner, expected_type=type_hints["auto_add_group_owner"])
                check_type(argname="argument group_owner", value=group_owner, expected_type=type_hints["group_owner"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auto_add_group_owner is not None:
                self._values["auto_add_group_owner"] = auto_add_group_owner
            if group_owner is not None:
                self._values["group_owner"] = group_owner

        @builtins.property
        def auto_add_group_owner(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether to give the privileges of the Linux group that owns the resource to the Lambda process.

            This gives the Lambda process the file access permissions of the Linux group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-groupownersetting.html#cfn-greengrass-resourcedefinitionversion-groupownersetting-autoaddgroupowner
            '''
            result = self._values.get("auto_add_group_owner")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def group_owner(self) -> typing.Optional[builtins.str]:
            '''The name of the Linux group whose privileges you want to add to the Lambda process.

            This value is ignored if ``AutoAddGroupOwner`` is true.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-groupownersetting.html#cfn-greengrass-resourcedefinitionversion-groupownersetting-groupowner
            '''
            result = self._values.get("group_owner")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GroupOwnerSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnResourceDefinitionVersionPropsMixin.LocalDeviceResourceDataProperty",
        jsii_struct_bases=[],
        name_mapping={
            "group_owner_setting": "groupOwnerSetting",
            "source_path": "sourcePath",
        },
    )
    class LocalDeviceResourceDataProperty:
        def __init__(
            self,
            *,
            group_owner_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResourceDefinitionVersionPropsMixin.GroupOwnerSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            source_path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Settings for a local device resource, which represents a file under ``/dev`` .

            For more information, see `Access Local Resources with Lambda Functions <https://docs.aws.amazon.com/greengrass/v1/developerguide/access-local-resources.html>`_ in the *Developer Guide* .

            In an CloudFormation template, ``LocalDeviceResourceData`` can be used in the ```ResourceDataContainer`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourcedatacontainer.html>`_ property type.

            :param group_owner_setting: Settings that define additional Linux OS group permissions to give to the Lambda function process.
            :param source_path: The local absolute path of the device resource. The source path for a device resource can refer only to a character device or block device under ``/dev`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-localdeviceresourcedata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                local_device_resource_data_property = greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.LocalDeviceResourceDataProperty(
                    group_owner_setting=greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.GroupOwnerSettingProperty(
                        auto_add_group_owner=False,
                        group_owner="groupOwner"
                    ),
                    source_path="sourcePath"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7c0441d9b1560a13ba031a6f00970cb38777f71fd59a6e7fb009ffe41cd973c4)
                check_type(argname="argument group_owner_setting", value=group_owner_setting, expected_type=type_hints["group_owner_setting"])
                check_type(argname="argument source_path", value=source_path, expected_type=type_hints["source_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if group_owner_setting is not None:
                self._values["group_owner_setting"] = group_owner_setting
            if source_path is not None:
                self._values["source_path"] = source_path

        @builtins.property
        def group_owner_setting(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDefinitionVersionPropsMixin.GroupOwnerSettingProperty"]]:
            '''Settings that define additional Linux OS group permissions to give to the Lambda function process.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-localdeviceresourcedata.html#cfn-greengrass-resourcedefinitionversion-localdeviceresourcedata-groupownersetting
            '''
            result = self._values.get("group_owner_setting")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDefinitionVersionPropsMixin.GroupOwnerSettingProperty"]], result)

        @builtins.property
        def source_path(self) -> typing.Optional[builtins.str]:
            '''The local absolute path of the device resource.

            The source path for a device resource can refer only to a character device or block device under ``/dev`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-localdeviceresourcedata.html#cfn-greengrass-resourcedefinitionversion-localdeviceresourcedata-sourcepath
            '''
            result = self._values.get("source_path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LocalDeviceResourceDataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnResourceDefinitionVersionPropsMixin.LocalVolumeResourceDataProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_path": "destinationPath",
            "group_owner_setting": "groupOwnerSetting",
            "source_path": "sourcePath",
        },
    )
    class LocalVolumeResourceDataProperty:
        def __init__(
            self,
            *,
            destination_path: typing.Optional[builtins.str] = None,
            group_owner_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResourceDefinitionVersionPropsMixin.GroupOwnerSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            source_path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Settings for a local volume resource, which represents a file or directory on the root file system.

            For more information, see `Access Local Resources with Lambda Functions <https://docs.aws.amazon.com/greengrass/v1/developerguide/access-local-resources.html>`_ in the *Developer Guide* .

            In an CloudFormation template, ``LocalVolumeResourceData`` can be used in the ```ResourceDataContainer`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourcedatacontainer.html>`_ property type.

            :param destination_path: The absolute local path of the resource in the Lambda environment.
            :param group_owner_setting: Settings that define additional Linux OS group permissions to give to the Lambda function process.
            :param source_path: The local absolute path of the volume resource on the host. The source path for a volume resource type cannot start with ``/sys`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-localvolumeresourcedata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                local_volume_resource_data_property = greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.LocalVolumeResourceDataProperty(
                    destination_path="destinationPath",
                    group_owner_setting=greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.GroupOwnerSettingProperty(
                        auto_add_group_owner=False,
                        group_owner="groupOwner"
                    ),
                    source_path="sourcePath"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c9accb2d0ddbe8a720d68b2a33b19d7cb3c9237b114a20e4b85fbe1e003053fd)
                check_type(argname="argument destination_path", value=destination_path, expected_type=type_hints["destination_path"])
                check_type(argname="argument group_owner_setting", value=group_owner_setting, expected_type=type_hints["group_owner_setting"])
                check_type(argname="argument source_path", value=source_path, expected_type=type_hints["source_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination_path is not None:
                self._values["destination_path"] = destination_path
            if group_owner_setting is not None:
                self._values["group_owner_setting"] = group_owner_setting
            if source_path is not None:
                self._values["source_path"] = source_path

        @builtins.property
        def destination_path(self) -> typing.Optional[builtins.str]:
            '''The absolute local path of the resource in the Lambda environment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-localvolumeresourcedata.html#cfn-greengrass-resourcedefinitionversion-localvolumeresourcedata-destinationpath
            '''
            result = self._values.get("destination_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def group_owner_setting(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDefinitionVersionPropsMixin.GroupOwnerSettingProperty"]]:
            '''Settings that define additional Linux OS group permissions to give to the Lambda function process.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-localvolumeresourcedata.html#cfn-greengrass-resourcedefinitionversion-localvolumeresourcedata-groupownersetting
            '''
            result = self._values.get("group_owner_setting")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDefinitionVersionPropsMixin.GroupOwnerSettingProperty"]], result)

        @builtins.property
        def source_path(self) -> typing.Optional[builtins.str]:
            '''The local absolute path of the volume resource on the host.

            The source path for a volume resource type cannot start with ``/sys`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-localvolumeresourcedata.html#cfn-greengrass-resourcedefinitionversion-localvolumeresourcedata-sourcepath
            '''
            result = self._values.get("source_path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LocalVolumeResourceDataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnResourceDefinitionVersionPropsMixin.ResourceDataContainerProperty",
        jsii_struct_bases=[],
        name_mapping={
            "local_device_resource_data": "localDeviceResourceData",
            "local_volume_resource_data": "localVolumeResourceData",
            "s3_machine_learning_model_resource_data": "s3MachineLearningModelResourceData",
            "sage_maker_machine_learning_model_resource_data": "sageMakerMachineLearningModelResourceData",
            "secrets_manager_secret_resource_data": "secretsManagerSecretResourceData",
        },
    )
    class ResourceDataContainerProperty:
        def __init__(
            self,
            *,
            local_device_resource_data: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResourceDefinitionVersionPropsMixin.LocalDeviceResourceDataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            local_volume_resource_data: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResourceDefinitionVersionPropsMixin.LocalVolumeResourceDataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3_machine_learning_model_resource_data: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResourceDefinitionVersionPropsMixin.S3MachineLearningModelResourceDataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sage_maker_machine_learning_model_resource_data: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResourceDefinitionVersionPropsMixin.SageMakerMachineLearningModelResourceDataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            secrets_manager_secret_resource_data: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResourceDefinitionVersionPropsMixin.SecretsManagerSecretResourceDataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A container for resource data, which defines the resource type.

            The container takes only one of the following supported resource data types: ``LocalDeviceResourceData`` , ``LocalVolumeResourceData`` , ``SageMakerMachineLearningModelResourceData`` , ``S3MachineLearningModelResourceData`` , or ``SecretsManagerSecretResourceData`` .
            .. epigraph::

               Only one resource type can be defined for a ``ResourceDataContainer`` instance.

            In an CloudFormation template, ``ResourceDataContainer`` is a property of the ```ResourceInstance`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourceinstance.html>`_ property type.

            :param local_device_resource_data: Settings for a local device resource.
            :param local_volume_resource_data: Settings for a local volume resource.
            :param s3_machine_learning_model_resource_data: Settings for a machine learning resource stored in Amazon S3 .
            :param sage_maker_machine_learning_model_resource_data: Settings for a machine learning resource saved as an SageMaker AI training job.
            :param secrets_manager_secret_resource_data: Settings for a secret resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourcedatacontainer.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                resource_data_container_property = greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.ResourceDataContainerProperty(
                    local_device_resource_data=greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.LocalDeviceResourceDataProperty(
                        group_owner_setting=greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.GroupOwnerSettingProperty(
                            auto_add_group_owner=False,
                            group_owner="groupOwner"
                        ),
                        source_path="sourcePath"
                    ),
                    local_volume_resource_data=greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.LocalVolumeResourceDataProperty(
                        destination_path="destinationPath",
                        group_owner_setting=greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.GroupOwnerSettingProperty(
                            auto_add_group_owner=False,
                            group_owner="groupOwner"
                        ),
                        source_path="sourcePath"
                    ),
                    s3_machine_learning_model_resource_data=greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.S3MachineLearningModelResourceDataProperty(
                        destination_path="destinationPath",
                        owner_setting=greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.ResourceDownloadOwnerSettingProperty(
                            group_owner="groupOwner",
                            group_permission="groupPermission"
                        ),
                        s3_uri="s3Uri"
                    ),
                    sage_maker_machine_learning_model_resource_data=greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.SageMakerMachineLearningModelResourceDataProperty(
                        destination_path="destinationPath",
                        owner_setting=greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.ResourceDownloadOwnerSettingProperty(
                            group_owner="groupOwner",
                            group_permission="groupPermission"
                        ),
                        sage_maker_job_arn="sageMakerJobArn"
                    ),
                    secrets_manager_secret_resource_data=greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.SecretsManagerSecretResourceDataProperty(
                        additional_staging_labels_to_download=["additionalStagingLabelsToDownload"],
                        arn="arn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4ea6583db51cf37ad18f59f6cc9813e9355105f12ed5febdd589f0b4395d940b)
                check_type(argname="argument local_device_resource_data", value=local_device_resource_data, expected_type=type_hints["local_device_resource_data"])
                check_type(argname="argument local_volume_resource_data", value=local_volume_resource_data, expected_type=type_hints["local_volume_resource_data"])
                check_type(argname="argument s3_machine_learning_model_resource_data", value=s3_machine_learning_model_resource_data, expected_type=type_hints["s3_machine_learning_model_resource_data"])
                check_type(argname="argument sage_maker_machine_learning_model_resource_data", value=sage_maker_machine_learning_model_resource_data, expected_type=type_hints["sage_maker_machine_learning_model_resource_data"])
                check_type(argname="argument secrets_manager_secret_resource_data", value=secrets_manager_secret_resource_data, expected_type=type_hints["secrets_manager_secret_resource_data"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if local_device_resource_data is not None:
                self._values["local_device_resource_data"] = local_device_resource_data
            if local_volume_resource_data is not None:
                self._values["local_volume_resource_data"] = local_volume_resource_data
            if s3_machine_learning_model_resource_data is not None:
                self._values["s3_machine_learning_model_resource_data"] = s3_machine_learning_model_resource_data
            if sage_maker_machine_learning_model_resource_data is not None:
                self._values["sage_maker_machine_learning_model_resource_data"] = sage_maker_machine_learning_model_resource_data
            if secrets_manager_secret_resource_data is not None:
                self._values["secrets_manager_secret_resource_data"] = secrets_manager_secret_resource_data

        @builtins.property
        def local_device_resource_data(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDefinitionVersionPropsMixin.LocalDeviceResourceDataProperty"]]:
            '''Settings for a local device resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourcedatacontainer.html#cfn-greengrass-resourcedefinitionversion-resourcedatacontainer-localdeviceresourcedata
            '''
            result = self._values.get("local_device_resource_data")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDefinitionVersionPropsMixin.LocalDeviceResourceDataProperty"]], result)

        @builtins.property
        def local_volume_resource_data(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDefinitionVersionPropsMixin.LocalVolumeResourceDataProperty"]]:
            '''Settings for a local volume resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourcedatacontainer.html#cfn-greengrass-resourcedefinitionversion-resourcedatacontainer-localvolumeresourcedata
            '''
            result = self._values.get("local_volume_resource_data")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDefinitionVersionPropsMixin.LocalVolumeResourceDataProperty"]], result)

        @builtins.property
        def s3_machine_learning_model_resource_data(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDefinitionVersionPropsMixin.S3MachineLearningModelResourceDataProperty"]]:
            '''Settings for a machine learning resource stored in Amazon S3 .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourcedatacontainer.html#cfn-greengrass-resourcedefinitionversion-resourcedatacontainer-s3machinelearningmodelresourcedata
            '''
            result = self._values.get("s3_machine_learning_model_resource_data")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDefinitionVersionPropsMixin.S3MachineLearningModelResourceDataProperty"]], result)

        @builtins.property
        def sage_maker_machine_learning_model_resource_data(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDefinitionVersionPropsMixin.SageMakerMachineLearningModelResourceDataProperty"]]:
            '''Settings for a machine learning resource saved as an SageMaker AI training job.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourcedatacontainer.html#cfn-greengrass-resourcedefinitionversion-resourcedatacontainer-sagemakermachinelearningmodelresourcedata
            '''
            result = self._values.get("sage_maker_machine_learning_model_resource_data")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDefinitionVersionPropsMixin.SageMakerMachineLearningModelResourceDataProperty"]], result)

        @builtins.property
        def secrets_manager_secret_resource_data(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDefinitionVersionPropsMixin.SecretsManagerSecretResourceDataProperty"]]:
            '''Settings for a secret resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourcedatacontainer.html#cfn-greengrass-resourcedefinitionversion-resourcedatacontainer-secretsmanagersecretresourcedata
            '''
            result = self._values.get("secrets_manager_secret_resource_data")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDefinitionVersionPropsMixin.SecretsManagerSecretResourceDataProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceDataContainerProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnResourceDefinitionVersionPropsMixin.ResourceDownloadOwnerSettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "group_owner": "groupOwner",
            "group_permission": "groupPermission",
        },
    )
    class ResourceDownloadOwnerSettingProperty:
        def __init__(
            self,
            *,
            group_owner: typing.Optional[builtins.str] = None,
            group_permission: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The owner setting for a downloaded machine learning resource.

            For more information, see `Access Machine Learning Resources from Lambda Functions <https://docs.aws.amazon.com/greengrass/v1/developerguide/access-ml-resources.html>`_ in the *Developer Guide* .

            In an CloudFormation template, ``ResourceDownloadOwnerSetting`` is the property type of the ``OwnerSetting`` property for the ```S3MachineLearningModelResourceData`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-s3machinelearningmodelresourcedata.html>`_ and ```SageMakerMachineLearningModelResourceData`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-sagemakermachinelearningmodelresourcedata.html>`_ property types.

            :param group_owner: The group owner of the machine learning resource. This is the group ID (GID) of an existing Linux OS group on the system. The group's permissions are added to the Lambda process.
            :param group_permission: The permissions that the group owner has to the machine learning resource. Valid values are ``rw`` (read-write) or ``ro`` (read-only).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourcedownloadownersetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                resource_download_owner_setting_property = greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.ResourceDownloadOwnerSettingProperty(
                    group_owner="groupOwner",
                    group_permission="groupPermission"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c98a20a58ec96f56c15679ea0487b6ba50eb03e338af74d8192aa649b929be75)
                check_type(argname="argument group_owner", value=group_owner, expected_type=type_hints["group_owner"])
                check_type(argname="argument group_permission", value=group_permission, expected_type=type_hints["group_permission"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if group_owner is not None:
                self._values["group_owner"] = group_owner
            if group_permission is not None:
                self._values["group_permission"] = group_permission

        @builtins.property
        def group_owner(self) -> typing.Optional[builtins.str]:
            '''The group owner of the machine learning resource.

            This is the group ID (GID) of an existing Linux OS group on the system. The group's permissions are added to the Lambda process.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourcedownloadownersetting.html#cfn-greengrass-resourcedefinitionversion-resourcedownloadownersetting-groupowner
            '''
            result = self._values.get("group_owner")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def group_permission(self) -> typing.Optional[builtins.str]:
            '''The permissions that the group owner has to the machine learning resource.

            Valid values are ``rw`` (read-write) or ``ro`` (read-only).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourcedownloadownersetting.html#cfn-greengrass-resourcedefinitionversion-resourcedownloadownersetting-grouppermission
            '''
            result = self._values.get("group_permission")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceDownloadOwnerSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnResourceDefinitionVersionPropsMixin.ResourceInstanceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "id": "id",
            "name": "name",
            "resource_data_container": "resourceDataContainer",
        },
    )
    class ResourceInstanceProperty:
        def __init__(
            self,
            *,
            id: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            resource_data_container: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResourceDefinitionVersionPropsMixin.ResourceDataContainerProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A local resource, machine learning resource, or secret resource.

            For more information, see `Access Local Resources with Lambda Functions <https://docs.aws.amazon.com/greengrass/v1/developerguide/access-local-resources.html>`_ , `Perform Machine Learning Inference <https://docs.aws.amazon.com/greengrass/v1/developerguide/ml-inference.html>`_ , and `Deploy Secrets to the AWS IoT Greengrass Core <https://docs.aws.amazon.com/greengrass/v1/developerguide/secrets.html>`_ in the *Developer Guide* .

            In an CloudFormation template, the ``Resources`` property of the ```AWS::Greengrass::ResourceDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-resourcedefinitionversion.html>`_ resource contains a list of ``ResourceInstance`` property types.

            :param id: A descriptive or arbitrary ID for the resource. This value must be unique within the resource definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .
            :param name: The descriptive resource name, which is displayed on the AWS IoT Greengrass console. Maximum length 128 characters with pattern [a-zA-Z0-9:_-]+. This must be unique within a Greengrass group.
            :param resource_data_container: A container for resource data. The container takes only one of the following supported resource data types: ``LocalDeviceResourceData`` , ``LocalVolumeResourceData`` , ``SageMakerMachineLearningModelResourceData`` , ``S3MachineLearningModelResourceData`` , or ``SecretsManagerSecretResourceData`` . .. epigraph:: Only one resource type can be defined for a ``ResourceDataContainer`` instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourceinstance.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                resource_instance_property = greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.ResourceInstanceProperty(
                    id="id",
                    name="name",
                    resource_data_container=greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.ResourceDataContainerProperty(
                        local_device_resource_data=greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.LocalDeviceResourceDataProperty(
                            group_owner_setting=greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.GroupOwnerSettingProperty(
                                auto_add_group_owner=False,
                                group_owner="groupOwner"
                            ),
                            source_path="sourcePath"
                        ),
                        local_volume_resource_data=greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.LocalVolumeResourceDataProperty(
                            destination_path="destinationPath",
                            group_owner_setting=greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.GroupOwnerSettingProperty(
                                auto_add_group_owner=False,
                                group_owner="groupOwner"
                            ),
                            source_path="sourcePath"
                        ),
                        s3_machine_learning_model_resource_data=greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.S3MachineLearningModelResourceDataProperty(
                            destination_path="destinationPath",
                            owner_setting=greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.ResourceDownloadOwnerSettingProperty(
                                group_owner="groupOwner",
                                group_permission="groupPermission"
                            ),
                            s3_uri="s3Uri"
                        ),
                        sage_maker_machine_learning_model_resource_data=greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.SageMakerMachineLearningModelResourceDataProperty(
                            destination_path="destinationPath",
                            owner_setting=greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.ResourceDownloadOwnerSettingProperty(
                                group_owner="groupOwner",
                                group_permission="groupPermission"
                            ),
                            sage_maker_job_arn="sageMakerJobArn"
                        ),
                        secrets_manager_secret_resource_data=greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.SecretsManagerSecretResourceDataProperty(
                            additional_staging_labels_to_download=["additionalStagingLabelsToDownload"],
                            arn="arn"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__690b34fa716ac0d8af7bb3dd7f42a72397283c46c99c1dd5c645f01ff06ca4b6)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument resource_data_container", value=resource_data_container, expected_type=type_hints["resource_data_container"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if id is not None:
                self._values["id"] = id
            if name is not None:
                self._values["name"] = name
            if resource_data_container is not None:
                self._values["resource_data_container"] = resource_data_container

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''A descriptive or arbitrary ID for the resource.

            This value must be unique within the resource definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourceinstance.html#cfn-greengrass-resourcedefinitionversion-resourceinstance-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The descriptive resource name, which is displayed on the AWS IoT Greengrass console.

            Maximum length 128 characters with pattern [a-zA-Z0-9:_-]+. This must be unique within a Greengrass group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourceinstance.html#cfn-greengrass-resourcedefinitionversion-resourceinstance-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_data_container(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDefinitionVersionPropsMixin.ResourceDataContainerProperty"]]:
            '''A container for resource data.

            The container takes only one of the following supported resource data types: ``LocalDeviceResourceData`` , ``LocalVolumeResourceData`` , ``SageMakerMachineLearningModelResourceData`` , ``S3MachineLearningModelResourceData`` , or ``SecretsManagerSecretResourceData`` .
            .. epigraph::

               Only one resource type can be defined for a ``ResourceDataContainer`` instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourceinstance.html#cfn-greengrass-resourcedefinitionversion-resourceinstance-resourcedatacontainer
            '''
            result = self._values.get("resource_data_container")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDefinitionVersionPropsMixin.ResourceDataContainerProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceInstanceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnResourceDefinitionVersionPropsMixin.S3MachineLearningModelResourceDataProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_path": "destinationPath",
            "owner_setting": "ownerSetting",
            "s3_uri": "s3Uri",
        },
    )
    class S3MachineLearningModelResourceDataProperty:
        def __init__(
            self,
            *,
            destination_path: typing.Optional[builtins.str] = None,
            owner_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResourceDefinitionVersionPropsMixin.ResourceDownloadOwnerSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3_uri: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Settings for an Amazon S3 machine learning resource.

            For more information, see `Perform Machine Learning Inference <https://docs.aws.amazon.com/greengrass/v1/developerguide/ml-inference.html>`_ in the *Developer Guide* .

            In an CloudFormation template, ``S3MachineLearningModelResourceData`` can be used in the ```ResourceDataContainer`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourcedatacontainer.html>`_ property type.

            :param destination_path: The absolute local path of the resource inside the Lambda environment.
            :param owner_setting: The owner setting for the downloaded machine learning resource. For more information, see `Access Machine Learning Resources from Lambda Functions <https://docs.aws.amazon.com/greengrass/v1/developerguide/access-ml-resources.html>`_ in the *Developer Guide* .
            :param s3_uri: The URI of the source model in an Amazon S3 bucket. The model package must be in ``tar.gz`` or ``.zip`` format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-s3machinelearningmodelresourcedata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                s3_machine_learning_model_resource_data_property = greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.S3MachineLearningModelResourceDataProperty(
                    destination_path="destinationPath",
                    owner_setting=greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.ResourceDownloadOwnerSettingProperty(
                        group_owner="groupOwner",
                        group_permission="groupPermission"
                    ),
                    s3_uri="s3Uri"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__65b9c079cae6925800e616c1f28429dea6bc333e2c0317369e1c09ff19288968)
                check_type(argname="argument destination_path", value=destination_path, expected_type=type_hints["destination_path"])
                check_type(argname="argument owner_setting", value=owner_setting, expected_type=type_hints["owner_setting"])
                check_type(argname="argument s3_uri", value=s3_uri, expected_type=type_hints["s3_uri"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination_path is not None:
                self._values["destination_path"] = destination_path
            if owner_setting is not None:
                self._values["owner_setting"] = owner_setting
            if s3_uri is not None:
                self._values["s3_uri"] = s3_uri

        @builtins.property
        def destination_path(self) -> typing.Optional[builtins.str]:
            '''The absolute local path of the resource inside the Lambda environment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-s3machinelearningmodelresourcedata.html#cfn-greengrass-resourcedefinitionversion-s3machinelearningmodelresourcedata-destinationpath
            '''
            result = self._values.get("destination_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def owner_setting(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDefinitionVersionPropsMixin.ResourceDownloadOwnerSettingProperty"]]:
            '''The owner setting for the downloaded machine learning resource.

            For more information, see `Access Machine Learning Resources from Lambda Functions <https://docs.aws.amazon.com/greengrass/v1/developerguide/access-ml-resources.html>`_ in the *Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-s3machinelearningmodelresourcedata.html#cfn-greengrass-resourcedefinitionversion-s3machinelearningmodelresourcedata-ownersetting
            '''
            result = self._values.get("owner_setting")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDefinitionVersionPropsMixin.ResourceDownloadOwnerSettingProperty"]], result)

        @builtins.property
        def s3_uri(self) -> typing.Optional[builtins.str]:
            '''The URI of the source model in an Amazon S3 bucket.

            The model package must be in ``tar.gz`` or ``.zip`` format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-s3machinelearningmodelresourcedata.html#cfn-greengrass-resourcedefinitionversion-s3machinelearningmodelresourcedata-s3uri
            '''
            result = self._values.get("s3_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3MachineLearningModelResourceDataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnResourceDefinitionVersionPropsMixin.SageMakerMachineLearningModelResourceDataProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_path": "destinationPath",
            "owner_setting": "ownerSetting",
            "sage_maker_job_arn": "sageMakerJobArn",
        },
    )
    class SageMakerMachineLearningModelResourceDataProperty:
        def __init__(
            self,
            *,
            destination_path: typing.Optional[builtins.str] = None,
            owner_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResourceDefinitionVersionPropsMixin.ResourceDownloadOwnerSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sage_maker_job_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Settings for an Secrets Manager machine learning resource.

            For more information, see `Perform Machine Learning Inference <https://docs.aws.amazon.com/greengrass/v1/developerguide/ml-inference.html>`_ in the *Developer Guide* .

            In an CloudFormation template, ``SageMakerMachineLearningModelResourceData`` can be used in the ```ResourceDataContainer`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourcedatacontainer.html>`_ property type.

            :param destination_path: The absolute local path of the resource inside the Lambda environment.
            :param owner_setting: The owner setting for the downloaded machine learning resource. For more information, see `Access Machine Learning Resources from Lambda Functions <https://docs.aws.amazon.com/greengrass/v1/developerguide/access-ml-resources.html>`_ in the *Developer Guide* .
            :param sage_maker_job_arn: The Amazon Resource Name (ARN) of the Amazon SageMaker AI training job that represents the source model.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-sagemakermachinelearningmodelresourcedata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                sage_maker_machine_learning_model_resource_data_property = greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.SageMakerMachineLearningModelResourceDataProperty(
                    destination_path="destinationPath",
                    owner_setting=greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.ResourceDownloadOwnerSettingProperty(
                        group_owner="groupOwner",
                        group_permission="groupPermission"
                    ),
                    sage_maker_job_arn="sageMakerJobArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__40855a038294c008cb9daaf4d2f687243b34f04f085f007d095f85fbf44e1c65)
                check_type(argname="argument destination_path", value=destination_path, expected_type=type_hints["destination_path"])
                check_type(argname="argument owner_setting", value=owner_setting, expected_type=type_hints["owner_setting"])
                check_type(argname="argument sage_maker_job_arn", value=sage_maker_job_arn, expected_type=type_hints["sage_maker_job_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination_path is not None:
                self._values["destination_path"] = destination_path
            if owner_setting is not None:
                self._values["owner_setting"] = owner_setting
            if sage_maker_job_arn is not None:
                self._values["sage_maker_job_arn"] = sage_maker_job_arn

        @builtins.property
        def destination_path(self) -> typing.Optional[builtins.str]:
            '''The absolute local path of the resource inside the Lambda environment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-sagemakermachinelearningmodelresourcedata.html#cfn-greengrass-resourcedefinitionversion-sagemakermachinelearningmodelresourcedata-destinationpath
            '''
            result = self._values.get("destination_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def owner_setting(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDefinitionVersionPropsMixin.ResourceDownloadOwnerSettingProperty"]]:
            '''The owner setting for the downloaded machine learning resource.

            For more information, see `Access Machine Learning Resources from Lambda Functions <https://docs.aws.amazon.com/greengrass/v1/developerguide/access-ml-resources.html>`_ in the *Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-sagemakermachinelearningmodelresourcedata.html#cfn-greengrass-resourcedefinitionversion-sagemakermachinelearningmodelresourcedata-ownersetting
            '''
            result = self._values.get("owner_setting")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDefinitionVersionPropsMixin.ResourceDownloadOwnerSettingProperty"]], result)

        @builtins.property
        def sage_maker_job_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Amazon SageMaker AI training job that represents the source model.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-sagemakermachinelearningmodelresourcedata.html#cfn-greengrass-resourcedefinitionversion-sagemakermachinelearningmodelresourcedata-sagemakerjobarn
            '''
            result = self._values.get("sage_maker_job_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SageMakerMachineLearningModelResourceDataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnResourceDefinitionVersionPropsMixin.SecretsManagerSecretResourceDataProperty",
        jsii_struct_bases=[],
        name_mapping={
            "additional_staging_labels_to_download": "additionalStagingLabelsToDownload",
            "arn": "arn",
        },
    )
    class SecretsManagerSecretResourceDataProperty:
        def __init__(
            self,
            *,
            additional_staging_labels_to_download: typing.Optional[typing.Sequence[builtins.str]] = None,
            arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Settings for a secret resource, which references a secret from AWS Secrets Manager .

            AWS IoT Greengrass stores a local, encrypted copy of the secret on the Greengrass core, where it can be securely accessed by connectors and Lambda functions. For more information, see `Deploy Secrets to the AWS IoT Greengrass Core <https://docs.aws.amazon.com/greengrass/v1/developerguide/secrets.html>`_ in the *Developer Guide* .

            In an CloudFormation template, ``SecretsManagerSecretResourceData`` can be used in the ```ResourceDataContainer`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourcedatacontainer.html>`_ property type.

            :param additional_staging_labels_to_download: The staging labels whose values you want to make available on the core, in addition to ``AWSCURRENT`` .
            :param arn: The Amazon Resource Name (ARN) of the Secrets Manager secret to make available on the core. The value of the secret's latest version (represented by the ``AWSCURRENT`` staging label) is included by default.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-secretsmanagersecretresourcedata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                secrets_manager_secret_resource_data_property = greengrass_mixins.CfnResourceDefinitionVersionPropsMixin.SecretsManagerSecretResourceDataProperty(
                    additional_staging_labels_to_download=["additionalStagingLabelsToDownload"],
                    arn="arn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cb717f43ec6dd9550cc46002b71b394730c2d5875fdf9533ff5783b3dc14e23a)
                check_type(argname="argument additional_staging_labels_to_download", value=additional_staging_labels_to_download, expected_type=type_hints["additional_staging_labels_to_download"])
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if additional_staging_labels_to_download is not None:
                self._values["additional_staging_labels_to_download"] = additional_staging_labels_to_download
            if arn is not None:
                self._values["arn"] = arn

        @builtins.property
        def additional_staging_labels_to_download(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''The staging labels whose values you want to make available on the core, in addition to ``AWSCURRENT`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-secretsmanagersecretresourcedata.html#cfn-greengrass-resourcedefinitionversion-secretsmanagersecretresourcedata-additionalstaginglabelstodownload
            '''
            result = self._values.get("additional_staging_labels_to_download")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Secrets Manager secret to make available on the core.

            The value of the secret's latest version (represented by the ``AWSCURRENT`` staging label) is included by default.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-secretsmanagersecretresourcedata.html#cfn-greengrass-resourcedefinitionversion-secretsmanagersecretresourcedata-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SecretsManagerSecretResourceDataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnSubscriptionDefinitionMixinProps",
    jsii_struct_bases=[],
    name_mapping={"initial_version": "initialVersion", "name": "name", "tags": "tags"},
)
class CfnSubscriptionDefinitionMixinProps:
    def __init__(
        self,
        *,
        initial_version: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSubscriptionDefinitionPropsMixin.SubscriptionDefinitionVersionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Properties for CfnSubscriptionDefinitionPropsMixin.

        :param initial_version: The subscription definition version to include when the subscription definition is created. A subscription definition version contains a list of ```subscription`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-subscriptiondefinition-subscription.html>`_ property types. .. epigraph:: To associate a subscription definition version after the subscription definition is created, create an ```AWS::Greengrass::SubscriptionDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-subscriptiondefinitionversion.html>`_ resource and specify the ID of this subscription definition.
        :param name: The name of the subscription definition.
        :param tags: Application-specific metadata to attach to the subscription definition. You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/v1/developerguide/tagging.html>`_ in the *Developer Guide* . This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in CloudFormation templates:: "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value" }

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-subscriptiondefinition.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
            
            # tags: Any
            
            cfn_subscription_definition_mixin_props = greengrass_mixins.CfnSubscriptionDefinitionMixinProps(
                initial_version=greengrass_mixins.CfnSubscriptionDefinitionPropsMixin.SubscriptionDefinitionVersionProperty(
                    subscriptions=[greengrass_mixins.CfnSubscriptionDefinitionPropsMixin.SubscriptionProperty(
                        id="id",
                        source="source",
                        subject="subject",
                        target="target"
                    )]
                ),
                name="name",
                tags=tags
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08e84ea0d858b33c68911de1da8773c93debf2b402ed5d2df7f04416e6779440)
            check_type(argname="argument initial_version", value=initial_version, expected_type=type_hints["initial_version"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if initial_version is not None:
            self._values["initial_version"] = initial_version
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def initial_version(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSubscriptionDefinitionPropsMixin.SubscriptionDefinitionVersionProperty"]]:
        '''The subscription definition version to include when the subscription definition is created.

        A subscription definition version contains a list of ```subscription`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-subscriptiondefinition-subscription.html>`_ property types.
        .. epigraph::

           To associate a subscription definition version after the subscription definition is created, create an ```AWS::Greengrass::SubscriptionDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-subscriptiondefinitionversion.html>`_ resource and specify the ID of this subscription definition.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-subscriptiondefinition.html#cfn-greengrass-subscriptiondefinition-initialversion
        '''
        result = self._values.get("initial_version")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSubscriptionDefinitionPropsMixin.SubscriptionDefinitionVersionProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the subscription definition.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-subscriptiondefinition.html#cfn-greengrass-subscriptiondefinition-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''Application-specific metadata to attach to the subscription definition.

        You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/v1/developerguide/tagging.html>`_ in the *Developer Guide* .

        This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in CloudFormation templates::

           "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value"
           }

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-subscriptiondefinition.html#cfn-greengrass-subscriptiondefinition-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSubscriptionDefinitionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSubscriptionDefinitionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnSubscriptionDefinitionPropsMixin",
):
    '''The ``AWS::Greengrass::SubscriptionDefinition`` resource represents a subscription definition for AWS IoT Greengrass .

    Subscription definitions are used to organize your subscription definition versions.

    Subscription definitions can reference multiple subscription definition versions. All subscription definition versions must be associated with a subscription definition. Each subscription definition version can contain one or more subscriptions.
    .. epigraph::

       When you create a subscription definition, you can optionally include an initial subscription definition version. To associate a subscription definition version later, create an ```AWS::Greengrass::SubscriptionDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-subscriptiondefinitionversion.html>`_ resource and specify the ID of this subscription definition.

       After you create the subscription definition version that contains the subscriptions you want to deploy, you must add it to your group version. For more information, see ```AWS::Greengrass::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-subscriptiondefinition.html
    :cloudformationResource: AWS::Greengrass::SubscriptionDefinition
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
        
        # tags: Any
        
        cfn_subscription_definition_props_mixin = greengrass_mixins.CfnSubscriptionDefinitionPropsMixin(greengrass_mixins.CfnSubscriptionDefinitionMixinProps(
            initial_version=greengrass_mixins.CfnSubscriptionDefinitionPropsMixin.SubscriptionDefinitionVersionProperty(
                subscriptions=[greengrass_mixins.CfnSubscriptionDefinitionPropsMixin.SubscriptionProperty(
                    id="id",
                    source="source",
                    subject="subject",
                    target="target"
                )]
            ),
            name="name",
            tags=tags
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnSubscriptionDefinitionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Greengrass::SubscriptionDefinition``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f700febfe9c3897661bec14c3c766f1d2f3948ff0ffd1efbe28975c2e05e4ca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__58dba9f17f55ac88df5562e965441e239795abf848d9fe73d24974dfa429edfa)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9893f013bbb531dd78fd742aa431545f2da5f44162206b6bb849a4003e8be71f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSubscriptionDefinitionMixinProps:
        return typing.cast(CfnSubscriptionDefinitionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnSubscriptionDefinitionPropsMixin.SubscriptionDefinitionVersionProperty",
        jsii_struct_bases=[],
        name_mapping={"subscriptions": "subscriptions"},
    )
    class SubscriptionDefinitionVersionProperty:
        def __init__(
            self,
            *,
            subscriptions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSubscriptionDefinitionPropsMixin.SubscriptionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''A subscription definition version contains a list of `subscriptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-subscriptiondefinition-subscription.html>`_ .

            .. epigraph::

               After you create a subscription definition version that contains the subscriptions you want to deploy, you must add it to your group version. For more information, see ```AWS::Greengrass::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html>`_ .

            In an CloudFormation template, ``SubscriptionDefinitionVersion`` is the property type of the ``InitialVersion`` property in the ```AWS::Greengrass::SubscriptionDefinition`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-subscriptiondefinition.html>`_ resource.

            :param subscriptions: The subscriptions in this version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-subscriptiondefinition-subscriptiondefinitionversion.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                subscription_definition_version_property = greengrass_mixins.CfnSubscriptionDefinitionPropsMixin.SubscriptionDefinitionVersionProperty(
                    subscriptions=[greengrass_mixins.CfnSubscriptionDefinitionPropsMixin.SubscriptionProperty(
                        id="id",
                        source="source",
                        subject="subject",
                        target="target"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__077ed8164db4a130c282172067190b82fa7cb8b3f4a48bf0da8107008bf41a2a)
                check_type(argname="argument subscriptions", value=subscriptions, expected_type=type_hints["subscriptions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if subscriptions is not None:
                self._values["subscriptions"] = subscriptions

        @builtins.property
        def subscriptions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSubscriptionDefinitionPropsMixin.SubscriptionProperty"]]]]:
            '''The subscriptions in this version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-subscriptiondefinition-subscriptiondefinitionversion.html#cfn-greengrass-subscriptiondefinition-subscriptiondefinitionversion-subscriptions
            '''
            result = self._values.get("subscriptions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSubscriptionDefinitionPropsMixin.SubscriptionProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubscriptionDefinitionVersionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnSubscriptionDefinitionPropsMixin.SubscriptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "id": "id",
            "source": "source",
            "subject": "subject",
            "target": "target",
        },
    )
    class SubscriptionProperty:
        def __init__(
            self,
            *,
            id: typing.Optional[builtins.str] = None,
            source: typing.Optional[builtins.str] = None,
            subject: typing.Optional[builtins.str] = None,
            target: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Subscriptions define how MQTT messages can be exchanged between devices, functions, and connectors in the group, and with AWS IoT or the local shadow service.

            A subscription defines a message source, message target, and a topic (or subject) that's used to route messages from the source to the target. A subscription defines the message flow in one direction, from the source to the target. For two-way communication, you must set up two subscriptions, one for each direction.

            In an CloudFormation template, the ``Subscriptions`` property of the ```SubscriptionDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-subscriptiondefinition-subscriptiondefinitionversion.html>`_ property type contains a list of ``Subscription`` property types.

            :param id: A descriptive or arbitrary ID for the subscription. This value must be unique within the subscription definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .
            :param source: The originator of the message. The value can be a thing ARN, the ARN of a Lambda function alias (recommended) or version, a connector ARN, ``cloud`` (which represents the AWS IoT cloud), or ``GGShadowService`` .
            :param subject: The MQTT topic used to route the message.
            :param target: The destination of the message. The value can be a thing ARN, the ARN of a Lambda function alias (recommended) or version, a connector ARN, ``cloud`` (which represents the AWS IoT cloud), or ``GGShadowService`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-subscriptiondefinition-subscription.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                subscription_property = greengrass_mixins.CfnSubscriptionDefinitionPropsMixin.SubscriptionProperty(
                    id="id",
                    source="source",
                    subject="subject",
                    target="target"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0172e0b73005a0e12d45e0c696cbeebe7f95fe667309824cbfe7a2659f425503)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument source", value=source, expected_type=type_hints["source"])
                check_type(argname="argument subject", value=subject, expected_type=type_hints["subject"])
                check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if id is not None:
                self._values["id"] = id
            if source is not None:
                self._values["source"] = source
            if subject is not None:
                self._values["subject"] = subject
            if target is not None:
                self._values["target"] = target

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''A descriptive or arbitrary ID for the subscription.

            This value must be unique within the subscription definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-subscriptiondefinition-subscription.html#cfn-greengrass-subscriptiondefinition-subscription-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source(self) -> typing.Optional[builtins.str]:
            '''The originator of the message.

            The value can be a thing ARN, the ARN of a Lambda function alias (recommended) or version, a connector ARN, ``cloud`` (which represents the AWS IoT cloud), or ``GGShadowService`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-subscriptiondefinition-subscription.html#cfn-greengrass-subscriptiondefinition-subscription-source
            '''
            result = self._values.get("source")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def subject(self) -> typing.Optional[builtins.str]:
            '''The MQTT topic used to route the message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-subscriptiondefinition-subscription.html#cfn-greengrass-subscriptiondefinition-subscription-subject
            '''
            result = self._values.get("subject")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target(self) -> typing.Optional[builtins.str]:
            '''The destination of the message.

            The value can be a thing ARN, the ARN of a Lambda function alias (recommended) or version, a connector ARN, ``cloud`` (which represents the AWS IoT cloud), or ``GGShadowService`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-subscriptiondefinition-subscription.html#cfn-greengrass-subscriptiondefinition-subscription-target
            '''
            result = self._values.get("target")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubscriptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnSubscriptionDefinitionVersionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "subscription_definition_id": "subscriptionDefinitionId",
        "subscriptions": "subscriptions",
    },
)
class CfnSubscriptionDefinitionVersionMixinProps:
    def __init__(
        self,
        *,
        subscription_definition_id: typing.Optional[builtins.str] = None,
        subscriptions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSubscriptionDefinitionVersionPropsMixin.SubscriptionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnSubscriptionDefinitionVersionPropsMixin.

        :param subscription_definition_id: The ID of the subscription definition associated with this version. This value is a GUID.
        :param subscriptions: The subscriptions in this version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-subscriptiondefinitionversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
            
            cfn_subscription_definition_version_mixin_props = greengrass_mixins.CfnSubscriptionDefinitionVersionMixinProps(
                subscription_definition_id="subscriptionDefinitionId",
                subscriptions=[greengrass_mixins.CfnSubscriptionDefinitionVersionPropsMixin.SubscriptionProperty(
                    id="id",
                    source="source",
                    subject="subject",
                    target="target"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dcda652525b0f50abffe091f69162f9b2dddc18eabc44e89d8bda38992cafd4)
            check_type(argname="argument subscription_definition_id", value=subscription_definition_id, expected_type=type_hints["subscription_definition_id"])
            check_type(argname="argument subscriptions", value=subscriptions, expected_type=type_hints["subscriptions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if subscription_definition_id is not None:
            self._values["subscription_definition_id"] = subscription_definition_id
        if subscriptions is not None:
            self._values["subscriptions"] = subscriptions

    @builtins.property
    def subscription_definition_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the subscription definition associated with this version.

        This value is a GUID.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-subscriptiondefinitionversion.html#cfn-greengrass-subscriptiondefinitionversion-subscriptiondefinitionid
        '''
        result = self._values.get("subscription_definition_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subscriptions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSubscriptionDefinitionVersionPropsMixin.SubscriptionProperty"]]]]:
        '''The subscriptions in this version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-subscriptiondefinitionversion.html#cfn-greengrass-subscriptiondefinitionversion-subscriptions
        '''
        result = self._values.get("subscriptions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSubscriptionDefinitionVersionPropsMixin.SubscriptionProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSubscriptionDefinitionVersionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSubscriptionDefinitionVersionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnSubscriptionDefinitionVersionPropsMixin",
):
    '''The ``AWS::Greengrass::SubscriptionDefinitionVersion`` resource represents a subscription definition version for AWS IoT Greengrass .

    A subscription definition version contains a list of subscriptions.
    .. epigraph::

       To create a subscription definition version, you must specify the ID of the subscription definition that you want to associate with the version. For information about creating a subscription definition, see ```AWS::Greengrass::SubscriptionDefinition`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-subscriptiondefinition.html>`_ .

       After you create a subscription definition version that contains the subscriptions you want to deploy, you must add it to your group version. For more information, see ```AWS::Greengrass::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-subscriptiondefinitionversion.html
    :cloudformationResource: AWS::Greengrass::SubscriptionDefinitionVersion
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
        
        cfn_subscription_definition_version_props_mixin = greengrass_mixins.CfnSubscriptionDefinitionVersionPropsMixin(greengrass_mixins.CfnSubscriptionDefinitionVersionMixinProps(
            subscription_definition_id="subscriptionDefinitionId",
            subscriptions=[greengrass_mixins.CfnSubscriptionDefinitionVersionPropsMixin.SubscriptionProperty(
                id="id",
                source="source",
                subject="subject",
                target="target"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnSubscriptionDefinitionVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Greengrass::SubscriptionDefinitionVersion``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0c954609dcc48f72874405378e2e37fb406d1c5f0e613af24bc9c93ffed1d84)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0784e9ee2f2572c8d96752e046518446ffc861444bba08126dc8db365325a1c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12c20176df8501f17eb5326ba91271f9639df30a1a12de673f1e3ffd3074566d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSubscriptionDefinitionVersionMixinProps:
        return typing.cast(CfnSubscriptionDefinitionVersionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrass.mixins.CfnSubscriptionDefinitionVersionPropsMixin.SubscriptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "id": "id",
            "source": "source",
            "subject": "subject",
            "target": "target",
        },
    )
    class SubscriptionProperty:
        def __init__(
            self,
            *,
            id: typing.Optional[builtins.str] = None,
            source: typing.Optional[builtins.str] = None,
            subject: typing.Optional[builtins.str] = None,
            target: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Subscriptions define how MQTT messages can be exchanged between devices, functions, and connectors in the group, and with AWS IoT or the local shadow service.

            A subscription defines a message source, message target, and a topic (or subject) that's used to route messages from the source to the target. A subscription defines the message flow in one direction, from the source to the target. For two-way communication, you must set up two subscriptions, one for each direction.

            In an CloudFormation template, the ``Subscriptions`` property of the ```AWS::Greengrass::SubscriptionDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-subscriptiondefinitionversion.html>`_ resource contains a list of ``Subscription`` property types.

            :param id: A descriptive or arbitrary ID for the subscription. This value must be unique within the subscription definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .
            :param source: The originator of the message. The value can be a thing ARN, the ARN of a Lambda function alias (recommended) or version, a connector ARN, ``cloud`` (which represents the AWS IoT cloud), or ``GGShadowService`` .
            :param subject: The MQTT topic used to route the message.
            :param target: The destination of the message. The value can be a thing ARN, the ARN of a Lambda function alias (recommended) or version, a connector ARN, ``cloud`` (which represents the AWS IoT cloud), or ``GGShadowService`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-subscriptiondefinitionversion-subscription.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrass import mixins as greengrass_mixins
                
                subscription_property = greengrass_mixins.CfnSubscriptionDefinitionVersionPropsMixin.SubscriptionProperty(
                    id="id",
                    source="source",
                    subject="subject",
                    target="target"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__39e92b95a4114ebce01a8eb24b8f43ba31cb4773d9e095b45ec8e9bbbbfa6957)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument source", value=source, expected_type=type_hints["source"])
                check_type(argname="argument subject", value=subject, expected_type=type_hints["subject"])
                check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if id is not None:
                self._values["id"] = id
            if source is not None:
                self._values["source"] = source
            if subject is not None:
                self._values["subject"] = subject
            if target is not None:
                self._values["target"] = target

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''A descriptive or arbitrary ID for the subscription.

            This value must be unique within the subscription definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-subscriptiondefinitionversion-subscription.html#cfn-greengrass-subscriptiondefinitionversion-subscription-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source(self) -> typing.Optional[builtins.str]:
            '''The originator of the message.

            The value can be a thing ARN, the ARN of a Lambda function alias (recommended) or version, a connector ARN, ``cloud`` (which represents the AWS IoT cloud), or ``GGShadowService`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-subscriptiondefinitionversion-subscription.html#cfn-greengrass-subscriptiondefinitionversion-subscription-source
            '''
            result = self._values.get("source")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def subject(self) -> typing.Optional[builtins.str]:
            '''The MQTT topic used to route the message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-subscriptiondefinitionversion-subscription.html#cfn-greengrass-subscriptiondefinitionversion-subscription-subject
            '''
            result = self._values.get("subject")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target(self) -> typing.Optional[builtins.str]:
            '''The destination of the message.

            The value can be a thing ARN, the ARN of a Lambda function alias (recommended) or version, a connector ARN, ``cloud`` (which represents the AWS IoT cloud), or ``GGShadowService`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-subscriptiondefinitionversion-subscription.html#cfn-greengrass-subscriptiondefinitionversion-subscription-target
            '''
            result = self._values.get("target")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubscriptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnConnectorDefinitionMixinProps",
    "CfnConnectorDefinitionPropsMixin",
    "CfnConnectorDefinitionVersionMixinProps",
    "CfnConnectorDefinitionVersionPropsMixin",
    "CfnCoreDefinitionMixinProps",
    "CfnCoreDefinitionPropsMixin",
    "CfnCoreDefinitionVersionMixinProps",
    "CfnCoreDefinitionVersionPropsMixin",
    "CfnDeviceDefinitionMixinProps",
    "CfnDeviceDefinitionPropsMixin",
    "CfnDeviceDefinitionVersionMixinProps",
    "CfnDeviceDefinitionVersionPropsMixin",
    "CfnFunctionDefinitionMixinProps",
    "CfnFunctionDefinitionPropsMixin",
    "CfnFunctionDefinitionVersionMixinProps",
    "CfnFunctionDefinitionVersionPropsMixin",
    "CfnGroupMixinProps",
    "CfnGroupPropsMixin",
    "CfnGroupVersionMixinProps",
    "CfnGroupVersionPropsMixin",
    "CfnLoggerDefinitionMixinProps",
    "CfnLoggerDefinitionPropsMixin",
    "CfnLoggerDefinitionVersionMixinProps",
    "CfnLoggerDefinitionVersionPropsMixin",
    "CfnResourceDefinitionMixinProps",
    "CfnResourceDefinitionPropsMixin",
    "CfnResourceDefinitionVersionMixinProps",
    "CfnResourceDefinitionVersionPropsMixin",
    "CfnSubscriptionDefinitionMixinProps",
    "CfnSubscriptionDefinitionPropsMixin",
    "CfnSubscriptionDefinitionVersionMixinProps",
    "CfnSubscriptionDefinitionVersionPropsMixin",
]

publication.publish()

def _typecheckingstub__57b0a4755acd51781d2f9f84eec1a2790e5f5c5725d638a6758ba57c0558bbf3(
    *,
    initial_version: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorDefinitionPropsMixin.ConnectorDefinitionVersionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d05b6b5845542c620a3fd58b27061f6babe75645d1e498b6370568d33d363569(
    props: typing.Union[CfnConnectorDefinitionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6af34f38b541dc02f89aa688fd31207fd075863315e41e94e21df98001c052d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b236ca7b34307777a7c8616b8cca6d84e8816a5bfa3c235a618d71f1d29094d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4931b0d72c72845a5d58d7b3306c33797814d1c231e0ed482d907421f500af73(
    *,
    connectors: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorDefinitionPropsMixin.ConnectorProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a3ea25d71d4e05d2954225f69ce30d85b3afc2375690c762e48c4e1043447a5(
    *,
    connector_arn: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    parameters: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e51fd100eaf9684a050144252e8f39ff4505dfe2c1aede84c481a2872bfc1539(
    *,
    connector_definition_id: typing.Optional[builtins.str] = None,
    connectors: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorDefinitionVersionPropsMixin.ConnectorProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42459fc68d474770bf7b84fdb6bc0039dc9dbcdcb6ecc9f9b14d939d103d7adb(
    props: typing.Union[CfnConnectorDefinitionVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d87930949e5cf54fb4262b7cf4ec885ab2f64eae6edd08d7f7841000eb55951(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f0f9699e20fde20c0ea31bea15dbd2c045892c96ccad19d1a145250f6b4d8c3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfd558649511aa07d06e2f6bbcd3b84047b24134ad3e3e25ca862124a9fced72(
    *,
    connector_arn: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    parameters: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95131d35a1833efb1cd1bed4b5d00ad13f68b49e4cda134dc6f14fbf78fbf412(
    *,
    initial_version: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCoreDefinitionPropsMixin.CoreDefinitionVersionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__101d3d5ebefd9192d680191fcd06b8e654c9f2001e2fdcc00d74697257c4be7b(
    props: typing.Union[CfnCoreDefinitionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ed56372505ef9536d61e6c261b887c83259d6d8a804fea0cb1c45d6d1f06d42(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcab1b2943fcc8f7063e32d5aac4d4688a334e16dd1dd0084bb2af91f16fff0f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86d1abafb9deb3dc9a8b6b301d5926082e500107e153275a85de34828683a206(
    *,
    cores: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCoreDefinitionPropsMixin.CoreProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d20f9a84bf47ad684a4ffe818b1a45c7cc087230a584e2a1fb8c4e7bb840261(
    *,
    certificate_arn: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    sync_shadow: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    thing_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a1eae3da3babded8ac784e4ccd67ae22eb8ef0d411e0c6caae46deb48b181bd(
    *,
    core_definition_id: typing.Optional[builtins.str] = None,
    cores: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCoreDefinitionVersionPropsMixin.CoreProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7140cb6af6123d37d747e0ba23913f963a96699c049b8b3106d01bcc4e922cf(
    props: typing.Union[CfnCoreDefinitionVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37a992e942f3582ab97784b0dd29bf4f08c7c06279801cc2ad7648ef31eff38f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1df06d798f4ab9fa481a3c6e5d63107bbdaa98bc2333ef5eb78b31f145d05bbe(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6cce34d8f08e949f96d6474026ef34913f128610a0dfc8dfe7aae7e67f77f9b(
    *,
    certificate_arn: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    sync_shadow: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    thing_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beb51de996764ae0259401f9f2259c09b0cd57fe89f76bcdf2c8963ddcd87335(
    *,
    initial_version: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeviceDefinitionPropsMixin.DeviceDefinitionVersionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b22dedd2758ff7883d497172c7b7fce6275ea0bbe94093b970383958585d1a4(
    props: typing.Union[CfnDeviceDefinitionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__453e8704d38e818d0cbb9d3d5d14fe6e1b0e93d3f0b07141d0a7b6c76f300918(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aab2dc8bdb0867789d43c7a2358c5562d1663c9c0de915a99975a060ab083b8d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18dfac721607b8042734c3b7a9f768487012bf34e90cc34cf123254fecb16ff7(
    *,
    devices: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeviceDefinitionPropsMixin.DeviceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06511ab24a1f53381ce0a089fb07dd67f852f14d10c0a546f9818be911f30d79(
    *,
    certificate_arn: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    sync_shadow: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    thing_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12006b6d7314ac3787bbdef126579715eaebabb2da2223abbf59980378375b96(
    *,
    device_definition_id: typing.Optional[builtins.str] = None,
    devices: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeviceDefinitionVersionPropsMixin.DeviceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bf4f2b3963c9821ae4051f1cca1c1f32db2ff8a09aae19ec5ec7c1ade2a902d(
    props: typing.Union[CfnDeviceDefinitionVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__048dac45aa803c49295100d20c6134e6e5cd4fe5cfaf725f2f87e7c0955e3723(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab8eeb9cf5809e32975425bb421bcbfc2459288ec121905910ab2eb4baad8946(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9833da919e59111af3d750c2d19725705748806013721c3a5e3ded085f7f59c(
    *,
    certificate_arn: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    sync_shadow: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    thing_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53f1a6d1f5345effb5ff39a7ca481f90ebc6e66ae92cbddcb37c1d32f6444173(
    *,
    initial_version: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionDefinitionPropsMixin.FunctionDefinitionVersionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3db7bcaaec4757d82ea19ea1a553a6550563efc4819087ed57a7a5c0309454f(
    props: typing.Union[CfnFunctionDefinitionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bea7ac6933b5fff22b6d765a312660e505f9e9e238dda961ab9e97a9dfb09268(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b3a42a15446032ebc4808c5190ef14ef7ea22f6ec0fcdb8b82219ac8f0f25fd(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9b25291096e3aeb0bae7d6068fa798989528fce1a35363084deab4d19e0a434(
    *,
    execution: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionDefinitionPropsMixin.ExecutionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d45f3ed05959bcd38ea39663723975acf4d25359b0a9cbdb5e3aab10f54a9361(
    *,
    access_sysfs: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    execution: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionDefinitionPropsMixin.ExecutionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    resource_access_policies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionDefinitionPropsMixin.ResourceAccessPolicyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    variables: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9054d318b6b0e0fb3af5a1d95cced6ea85cb8978c841296916fad4ecd5b0f5b2(
    *,
    isolation_mode: typing.Optional[builtins.str] = None,
    run_as: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionDefinitionPropsMixin.RunAsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56afe81deb77f187f00a0efe5c0fe13febeed01db0c2c4f991ab4322d38a3a19(
    *,
    encoding_type: typing.Optional[builtins.str] = None,
    environment: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionDefinitionPropsMixin.EnvironmentProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    exec_args: typing.Optional[builtins.str] = None,
    executable: typing.Optional[builtins.str] = None,
    memory_size: typing.Optional[jsii.Number] = None,
    pinned: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    timeout: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cb7be51cbd722ee899144c963c7328c7295c39dd8bc365601412af901ee54ec(
    *,
    default_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionDefinitionPropsMixin.DefaultConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    functions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionDefinitionPropsMixin.FunctionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deaa419483dc0ce7d7f542d404c94d81af0680e1c74fb46d8a83bedf450fd03f(
    *,
    function_arn: typing.Optional[builtins.str] = None,
    function_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionDefinitionPropsMixin.FunctionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54736471e1fd9485c2b5be546915791c0bab7f35f24a2c594fcb46a6e2097a95(
    *,
    permission: typing.Optional[builtins.str] = None,
    resource_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d177fd4caed497b9c4bc5deafc1de7872ba74e4f879dd40c917431c270981ad(
    *,
    gid: typing.Optional[jsii.Number] = None,
    uid: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d811cf337e0b6ebcf06d55ad5167305d47778dc675a0ae8539863345f807e03b(
    *,
    default_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionDefinitionVersionPropsMixin.DefaultConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    function_definition_id: typing.Optional[builtins.str] = None,
    functions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionDefinitionVersionPropsMixin.FunctionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a039f77f3a430812fc8e4af444955baac95da91ffc6dfd8246555e14c3cf42a4(
    props: typing.Union[CfnFunctionDefinitionVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91c92725d22fa4ae957b06a610fcbf1c4aca71633f5cf3e5333c52156af1e5f0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29de5e90428ecc574a3311208ef10e47ca62a5ef248ad9716383958e73e5c329(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc793b2556a3f488869f1c5ca9f394e85ff8be9d464adadc91fe88c81e01a9ea(
    *,
    execution: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionDefinitionVersionPropsMixin.ExecutionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__189a691d38edbdad466d8da7a8541a0f832bd04938ced99f567194298f7c76c0(
    *,
    access_sysfs: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    execution: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionDefinitionVersionPropsMixin.ExecutionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    resource_access_policies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionDefinitionVersionPropsMixin.ResourceAccessPolicyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    variables: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7cfdf69518effd74ab056c5e588c6e02927404315ddd856539884e49b1eafcb(
    *,
    isolation_mode: typing.Optional[builtins.str] = None,
    run_as: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionDefinitionVersionPropsMixin.RunAsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62356aa46ccb51619743fa732427bfcad665114c63941b941a10e86f2abc22c0(
    *,
    encoding_type: typing.Optional[builtins.str] = None,
    environment: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionDefinitionVersionPropsMixin.EnvironmentProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    exec_args: typing.Optional[builtins.str] = None,
    executable: typing.Optional[builtins.str] = None,
    memory_size: typing.Optional[jsii.Number] = None,
    pinned: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    timeout: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd8b1bcb4bdef10f4eb8cf98898ebb4ac0c276a61158abdc11eb0f6fc6cafc8a(
    *,
    function_arn: typing.Optional[builtins.str] = None,
    function_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionDefinitionVersionPropsMixin.FunctionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d3ec3c1504e9708d8df881573ffdd2eafc285970cb6c220f1a94aff857048bd(
    *,
    permission: typing.Optional[builtins.str] = None,
    resource_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55e9aad960236054930d6d8c620c5c54b971f3cff021a823f70b7f39dc32d4d5(
    *,
    gid: typing.Optional[jsii.Number] = None,
    uid: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab5af4731743d4248c39bfbb7132b4d007051d4e042149cb6bb5ce5cc618c604(
    *,
    initial_version: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGroupPropsMixin.GroupVersionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37b5fbb33e6b77d6af05adb6de78e4475f7c2e26574880af7314386f57db8fe8(
    props: typing.Union[CfnGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ea6dc2a679645b98ac17da0ca5210702c7b1a25c83098496c02a10a95f8921e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03e0f96b6f1df38d662191f7edd44268f5a9f0cc54651cbad15904799baef719(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06dc1246ebe173fb8ad4730bbde12b4595f1c1067740d1b5acd3955fa4b7cf7d(
    *,
    connector_definition_version_arn: typing.Optional[builtins.str] = None,
    core_definition_version_arn: typing.Optional[builtins.str] = None,
    device_definition_version_arn: typing.Optional[builtins.str] = None,
    function_definition_version_arn: typing.Optional[builtins.str] = None,
    logger_definition_version_arn: typing.Optional[builtins.str] = None,
    resource_definition_version_arn: typing.Optional[builtins.str] = None,
    subscription_definition_version_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f35dc189118a6d54675250cf9990576f5e6caaf57a288864c8599c36f491a41(
    *,
    connector_definition_version_arn: typing.Optional[builtins.str] = None,
    core_definition_version_arn: typing.Optional[builtins.str] = None,
    device_definition_version_arn: typing.Optional[builtins.str] = None,
    function_definition_version_arn: typing.Optional[builtins.str] = None,
    group_id: typing.Optional[builtins.str] = None,
    logger_definition_version_arn: typing.Optional[builtins.str] = None,
    resource_definition_version_arn: typing.Optional[builtins.str] = None,
    subscription_definition_version_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1116238c1d62e7d91cb9e43d666267890e5200cb9c8daa9037f92d8e50382d9b(
    props: typing.Union[CfnGroupVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8857dba89a5a73721d6b6b72c912056659750459f64e3d89446ad9b68b253ac(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a70a07a7db5527469a3273525f537f9b5db67081e3a32a31645a6be05de069d1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11488f1d2da72411620f6dd98a1e5b6ebdc91c2e33fc636b51b3a2feb408a7b7(
    *,
    initial_version: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLoggerDefinitionPropsMixin.LoggerDefinitionVersionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c373c68d89549c1574942186d772752254520688cb98b22fb5cf9c96871f8bca(
    props: typing.Union[CfnLoggerDefinitionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89cde0b938f6946a7e1c9b016e08f247080702b3d81b7059b70cc5461b3e0daf(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0645ca1531ae7861fd8bd4d669730d0f1b8bca118114320cf8b768723a3cf16(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d685a0b144be1b6473264f71dc12bcc6688812685e51f6e5dff03f8c03dab377(
    *,
    loggers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLoggerDefinitionPropsMixin.LoggerProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b64f857839660b799d536dde6360b80e9d67f5272fad5b5e863c64c5bc8e7dd(
    *,
    component: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    level: typing.Optional[builtins.str] = None,
    space: typing.Optional[jsii.Number] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5390edfbeefa03bf2aad0f5218bb18620c121f71b9da7b41d35569ec6dd4c0bb(
    *,
    logger_definition_id: typing.Optional[builtins.str] = None,
    loggers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLoggerDefinitionVersionPropsMixin.LoggerProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9aa8d6b3cc549cb0ee09ae09d60acb4d99258d13d5422ea62566cc738cbbfd2(
    props: typing.Union[CfnLoggerDefinitionVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__052f4d7c5fb10415b4a52ab7cbdbaa0b8d6ed2d217fd6e09661c13ea11a434b0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__964ad1c4fa1186099e65cc4da6200f56961b5c9ae67b7ac86b9bb9840e4f3f33(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cacdaa86e346686ae3c1e112658ce8ef33deafa29ce4fcaf668a37aa43750aba(
    *,
    component: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    level: typing.Optional[builtins.str] = None,
    space: typing.Optional[jsii.Number] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daec316b12d26e47c8dac50bc0b8e3fdf7d4b2217e32751e895025b145fea4f8(
    *,
    initial_version: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResourceDefinitionPropsMixin.ResourceDefinitionVersionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4e5d46e0b579098d4d6516c14fb858636b3544f39d6d45754a4c6826ecbd6e9(
    props: typing.Union[CfnResourceDefinitionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__291f087829390f873bd080fc16bc4c0d5d61620457587afda4f4704989eeb1b8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3c6fb32ecc6199ff434b5b811bf6ea266f6da5141de8b69236bf4639eb7d580(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d3f000210f1dc195a347e848b3fb22a2172648705124b2dd915ad9717d991c4(
    *,
    auto_add_group_owner: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    group_owner: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__076cb180e78bb2959e8dc327fd2901a0ec5ddf69eea8737e417814012fb17390(
    *,
    group_owner_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResourceDefinitionPropsMixin.GroupOwnerSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    source_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__905fc9d4c49b27aec236f0178dd769db292b78362d44983e5583fb687da623e2(
    *,
    destination_path: typing.Optional[builtins.str] = None,
    group_owner_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResourceDefinitionPropsMixin.GroupOwnerSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    source_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ee2633e07d5e0ee9f7ef319c08be058431ce90c7dc172cb4afb65048d4e65ad(
    *,
    local_device_resource_data: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResourceDefinitionPropsMixin.LocalDeviceResourceDataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    local_volume_resource_data: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResourceDefinitionPropsMixin.LocalVolumeResourceDataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_machine_learning_model_resource_data: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResourceDefinitionPropsMixin.S3MachineLearningModelResourceDataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sage_maker_machine_learning_model_resource_data: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResourceDefinitionPropsMixin.SageMakerMachineLearningModelResourceDataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    secrets_manager_secret_resource_data: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResourceDefinitionPropsMixin.SecretsManagerSecretResourceDataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ace4a1020dc67c92704d8bd2058ee04e2465c5c813824ab3ba9b10be2b6430a5(
    *,
    resources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResourceDefinitionPropsMixin.ResourceInstanceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a44afeb1dbca52baee179ecbe3563ed14d1720bb7eb2859671986aa767582a2(
    *,
    group_owner: typing.Optional[builtins.str] = None,
    group_permission: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89e2ca09d217847aa8aca952e0f8707f84a3b48430c8eb0d55788ea75681eff7(
    *,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    resource_data_container: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResourceDefinitionPropsMixin.ResourceDataContainerProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1757c8a3d80cae85eaf3a35c62cd360edc3d2700ad468a5d14d85c37851d7b11(
    *,
    destination_path: typing.Optional[builtins.str] = None,
    owner_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResourceDefinitionPropsMixin.ResourceDownloadOwnerSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abdb831801448da68595ed60f8754d61126f819c5ec63c11b8e167c9f193dbf9(
    *,
    destination_path: typing.Optional[builtins.str] = None,
    owner_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResourceDefinitionPropsMixin.ResourceDownloadOwnerSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sage_maker_job_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__726e4235d2c6af532b336c4fa97b43b044df064e8dd80698740e3e7f01706dc1(
    *,
    additional_staging_labels_to_download: typing.Optional[typing.Sequence[builtins.str]] = None,
    arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f9a7b0846b4c13bd74f9ec5ac53048e65db6e3a8e3e870e47a5e196bdb2999c(
    *,
    resource_definition_id: typing.Optional[builtins.str] = None,
    resources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResourceDefinitionVersionPropsMixin.ResourceInstanceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f028c34c2b3dd5fa2cb084a81e2c6cf9a36622c275ff749e1835dc303e51e8b5(
    props: typing.Union[CfnResourceDefinitionVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de0746b20847abf6ee330378fa518616d6dc17b2fd05e429485e16fe1cf62ef5(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25315b24341d185f256cafab933501168b49d9d4949a2cc26858ed1b60e90e7e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d60725ac803ffba779c0de5ca65f82c90080628c77d04af6cdc5fa1e02c5bd58(
    *,
    auto_add_group_owner: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    group_owner: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c0441d9b1560a13ba031a6f00970cb38777f71fd59a6e7fb009ffe41cd973c4(
    *,
    group_owner_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResourceDefinitionVersionPropsMixin.GroupOwnerSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    source_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9accb2d0ddbe8a720d68b2a33b19d7cb3c9237b114a20e4b85fbe1e003053fd(
    *,
    destination_path: typing.Optional[builtins.str] = None,
    group_owner_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResourceDefinitionVersionPropsMixin.GroupOwnerSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    source_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ea6583db51cf37ad18f59f6cc9813e9355105f12ed5febdd589f0b4395d940b(
    *,
    local_device_resource_data: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResourceDefinitionVersionPropsMixin.LocalDeviceResourceDataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    local_volume_resource_data: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResourceDefinitionVersionPropsMixin.LocalVolumeResourceDataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_machine_learning_model_resource_data: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResourceDefinitionVersionPropsMixin.S3MachineLearningModelResourceDataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sage_maker_machine_learning_model_resource_data: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResourceDefinitionVersionPropsMixin.SageMakerMachineLearningModelResourceDataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    secrets_manager_secret_resource_data: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResourceDefinitionVersionPropsMixin.SecretsManagerSecretResourceDataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c98a20a58ec96f56c15679ea0487b6ba50eb03e338af74d8192aa649b929be75(
    *,
    group_owner: typing.Optional[builtins.str] = None,
    group_permission: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__690b34fa716ac0d8af7bb3dd7f42a72397283c46c99c1dd5c645f01ff06ca4b6(
    *,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    resource_data_container: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResourceDefinitionVersionPropsMixin.ResourceDataContainerProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65b9c079cae6925800e616c1f28429dea6bc333e2c0317369e1c09ff19288968(
    *,
    destination_path: typing.Optional[builtins.str] = None,
    owner_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResourceDefinitionVersionPropsMixin.ResourceDownloadOwnerSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40855a038294c008cb9daaf4d2f687243b34f04f085f007d095f85fbf44e1c65(
    *,
    destination_path: typing.Optional[builtins.str] = None,
    owner_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResourceDefinitionVersionPropsMixin.ResourceDownloadOwnerSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sage_maker_job_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb717f43ec6dd9550cc46002b71b394730c2d5875fdf9533ff5783b3dc14e23a(
    *,
    additional_staging_labels_to_download: typing.Optional[typing.Sequence[builtins.str]] = None,
    arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08e84ea0d858b33c68911de1da8773c93debf2b402ed5d2df7f04416e6779440(
    *,
    initial_version: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSubscriptionDefinitionPropsMixin.SubscriptionDefinitionVersionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f700febfe9c3897661bec14c3c766f1d2f3948ff0ffd1efbe28975c2e05e4ca(
    props: typing.Union[CfnSubscriptionDefinitionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58dba9f17f55ac88df5562e965441e239795abf848d9fe73d24974dfa429edfa(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9893f013bbb531dd78fd742aa431545f2da5f44162206b6bb849a4003e8be71f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__077ed8164db4a130c282172067190b82fa7cb8b3f4a48bf0da8107008bf41a2a(
    *,
    subscriptions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSubscriptionDefinitionPropsMixin.SubscriptionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0172e0b73005a0e12d45e0c696cbeebe7f95fe667309824cbfe7a2659f425503(
    *,
    id: typing.Optional[builtins.str] = None,
    source: typing.Optional[builtins.str] = None,
    subject: typing.Optional[builtins.str] = None,
    target: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dcda652525b0f50abffe091f69162f9b2dddc18eabc44e89d8bda38992cafd4(
    *,
    subscription_definition_id: typing.Optional[builtins.str] = None,
    subscriptions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSubscriptionDefinitionVersionPropsMixin.SubscriptionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0c954609dcc48f72874405378e2e37fb406d1c5f0e613af24bc9c93ffed1d84(
    props: typing.Union[CfnSubscriptionDefinitionVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0784e9ee2f2572c8d96752e046518446ffc861444bba08126dc8db365325a1c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12c20176df8501f17eb5326ba91271f9639df30a1a12de673f1e3ffd3074566d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39e92b95a4114ebce01a8eb24b8f43ba31cb4773d9e095b45ec8e9bbbbfa6957(
    *,
    id: typing.Optional[builtins.str] = None,
    source: typing.Optional[builtins.str] = None,
    subject: typing.Optional[builtins.str] = None,
    target: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
