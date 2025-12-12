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
    jsii_type="@aws-cdk/mixins-preview.aws_devopsagent.mixins.CfnAgentSpaceMixinProps",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "name": "name"},
)
class CfnAgentSpaceMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnAgentSpacePropsMixin.

        :param description: The description of the AgentSpace.
        :param name: The name of the AgentSpace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsagent-agentspace.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_devopsagent import mixins as devopsagent_mixins
            
            cfn_agent_space_mixin_props = devopsagent_mixins.CfnAgentSpaceMixinProps(
                description="description",
                name="name"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbdd263ae3abff6b5cfec8e91d9de58428b834f2db8d486936e8a4f7357aa0e8)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the AgentSpace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsagent-agentspace.html#cfn-devopsagent-agentspace-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the AgentSpace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsagent-agentspace.html#cfn-devopsagent-agentspace-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAgentSpaceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAgentSpacePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_devopsagent.mixins.CfnAgentSpacePropsMixin",
):
    '''Resource Type definition for AWS::DevOpsAgent::AgentSpace.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsagent-agentspace.html
    :cloudformationResource: AWS::DevOpsAgent::AgentSpace
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_devopsagent import mixins as devopsagent_mixins
        
        cfn_agent_space_props_mixin = devopsagent_mixins.CfnAgentSpacePropsMixin(devopsagent_mixins.CfnAgentSpaceMixinProps(
            description="description",
            name="name"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAgentSpaceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DevOpsAgent::AgentSpace``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d61711350e89d0d475000f2052741ea118ca4ecd343a7123334f3f65792af5a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7d7857d5a30970573b711ff1657f799dd35453fb83790f6c255df3e03e19e14)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16e5c29fdba529bde10b22b077cb9551104b512fe299645edb91711e40257852)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAgentSpaceMixinProps:
        return typing.cast(CfnAgentSpaceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_devopsagent.mixins.CfnAssociationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "agent_space_id": "agentSpaceId",
        "configuration": "configuration",
        "service_id": "serviceId",
    },
)
class CfnAssociationMixinProps:
    def __init__(
        self,
        *,
        agent_space_id: typing.Optional[builtins.str] = None,
        configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAssociationPropsMixin.ServiceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        service_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnAssociationPropsMixin.

        :param agent_space_id: The unique identifier of the AgentSpace.
        :param configuration: The configuration that directs how AgentSpace interacts with the given service.
        :param service_id: The identifier for the associated service. For SourceAws and Aws configurations, this must be 'aws'. For all other service types, this is a UUID generated from the RegisterService command

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsagent-association.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_devopsagent import mixins as devopsagent_mixins
            
            # resource_metadata: Any
            
            cfn_association_mixin_props = devopsagent_mixins.CfnAssociationMixinProps(
                agent_space_id="agentSpaceId",
                configuration=devopsagent_mixins.CfnAssociationPropsMixin.ServiceConfigurationProperty(
                    aws=devopsagent_mixins.CfnAssociationPropsMixin.AWSConfigurationProperty(
                        account_id="accountId",
                        account_type="accountType",
                        assumable_role_arn="assumableRoleArn",
                        resources=[devopsagent_mixins.CfnAssociationPropsMixin.AWSResourceProperty(
                            resource_arn="resourceArn",
                            resource_metadata=resource_metadata,
                            resource_type="resourceType"
                        )],
                        tags=[devopsagent_mixins.CfnAssociationPropsMixin.KeyValuePairProperty(
                            key="key",
                            value="value"
                        )]
                    ),
                    dynatrace=devopsagent_mixins.CfnAssociationPropsMixin.DynatraceConfigurationProperty(
                        enable_webhook_updates=False,
                        env_id="envId",
                        resources=["resources"]
                    ),
                    event_channel=devopsagent_mixins.CfnAssociationPropsMixin.EventChannelConfigurationProperty(
                        enable_webhook_updates=False
                    ),
                    git_hub=devopsagent_mixins.CfnAssociationPropsMixin.GitHubConfigurationProperty(
                        owner="owner",
                        owner_type="ownerType",
                        repo_id="repoId",
                        repo_name="repoName"
                    ),
                    git_lab=devopsagent_mixins.CfnAssociationPropsMixin.GitLabConfigurationProperty(
                        enable_webhook_updates=False,
                        instance_identifier="instanceIdentifier",
                        project_id="projectId",
                        project_path="projectPath"
                    ),
                    mcp_server=devopsagent_mixins.CfnAssociationPropsMixin.MCPServerConfigurationProperty(
                        description="description",
                        enable_webhook_updates=False,
                        endpoint="endpoint",
                        name="name",
                        tools=["tools"]
                    ),
                    mcp_server_datadog=devopsagent_mixins.CfnAssociationPropsMixin.MCPServerDatadogConfigurationProperty(
                        description="description",
                        enable_webhook_updates=False,
                        endpoint="endpoint",
                        name="name"
                    ),
                    mcp_server_new_relic=devopsagent_mixins.CfnAssociationPropsMixin.MCPServerNewRelicConfigurationProperty(
                        account_id="accountId",
                        endpoint="endpoint"
                    ),
                    mcp_server_splunk=devopsagent_mixins.CfnAssociationPropsMixin.MCPServerSplunkConfigurationProperty(
                        description="description",
                        enable_webhook_updates=False,
                        endpoint="endpoint",
                        name="name"
                    ),
                    service_now=devopsagent_mixins.CfnAssociationPropsMixin.ServiceNowConfigurationProperty(
                        enable_webhook_updates=False,
                        instance_id="instanceId"
                    ),
                    slack=devopsagent_mixins.CfnAssociationPropsMixin.SlackConfigurationProperty(
                        transmission_target=devopsagent_mixins.CfnAssociationPropsMixin.SlackTransmissionTargetProperty(
                            incident_response_target=devopsagent_mixins.CfnAssociationPropsMixin.SlackChannelProperty(
                                channel_id="channelId",
                                channel_name="channelName"
                            )
                        ),
                        workspace_id="workspaceId",
                        workspace_name="workspaceName"
                    ),
                    source_aws=devopsagent_mixins.CfnAssociationPropsMixin.SourceAwsConfigurationProperty(
                        account_id="accountId",
                        account_type="accountType",
                        assumable_role_arn="assumableRoleArn",
                        resources=[devopsagent_mixins.CfnAssociationPropsMixin.AWSResourceProperty(
                            resource_arn="resourceArn",
                            resource_metadata=resource_metadata,
                            resource_type="resourceType"
                        )],
                        tags=[devopsagent_mixins.CfnAssociationPropsMixin.KeyValuePairProperty(
                            key="key",
                            value="value"
                        )]
                    )
                ),
                service_id="serviceId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__752652b0f356ef6b057c6d4c88cb6f15261ad4bd8630c44373893dbf672bffb8)
            check_type(argname="argument agent_space_id", value=agent_space_id, expected_type=type_hints["agent_space_id"])
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument service_id", value=service_id, expected_type=type_hints["service_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if agent_space_id is not None:
            self._values["agent_space_id"] = agent_space_id
        if configuration is not None:
            self._values["configuration"] = configuration
        if service_id is not None:
            self._values["service_id"] = service_id

    @builtins.property
    def agent_space_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the AgentSpace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsagent-association.html#cfn-devopsagent-association-agentspaceid
        '''
        result = self._values.get("agent_space_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssociationPropsMixin.ServiceConfigurationProperty"]]:
        '''The configuration that directs how AgentSpace interacts with the given service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsagent-association.html#cfn-devopsagent-association-configuration
        '''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssociationPropsMixin.ServiceConfigurationProperty"]], result)

    @builtins.property
    def service_id(self) -> typing.Optional[builtins.str]:
        '''The identifier for the associated service.

        For SourceAws and Aws configurations, this must be 'aws'. For all other service types, this is a UUID generated from the RegisterService command

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsagent-association.html#cfn-devopsagent-association-serviceid
        '''
        result = self._values.get("service_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAssociationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAssociationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_devopsagent.mixins.CfnAssociationPropsMixin",
):
    '''Resource Type definition for AWS::DevOpsAgent::Association defining how the AgentSpace interacts with external services like GitHub, Slack, AWS accounts, and others.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsagent-association.html
    :cloudformationResource: AWS::DevOpsAgent::Association
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_devopsagent import mixins as devopsagent_mixins
        
        # resource_metadata: Any
        
        cfn_association_props_mixin = devopsagent_mixins.CfnAssociationPropsMixin(devopsagent_mixins.CfnAssociationMixinProps(
            agent_space_id="agentSpaceId",
            configuration=devopsagent_mixins.CfnAssociationPropsMixin.ServiceConfigurationProperty(
                aws=devopsagent_mixins.CfnAssociationPropsMixin.AWSConfigurationProperty(
                    account_id="accountId",
                    account_type="accountType",
                    assumable_role_arn="assumableRoleArn",
                    resources=[devopsagent_mixins.CfnAssociationPropsMixin.AWSResourceProperty(
                        resource_arn="resourceArn",
                        resource_metadata=resource_metadata,
                        resource_type="resourceType"
                    )],
                    tags=[devopsagent_mixins.CfnAssociationPropsMixin.KeyValuePairProperty(
                        key="key",
                        value="value"
                    )]
                ),
                dynatrace=devopsagent_mixins.CfnAssociationPropsMixin.DynatraceConfigurationProperty(
                    enable_webhook_updates=False,
                    env_id="envId",
                    resources=["resources"]
                ),
                event_channel=devopsagent_mixins.CfnAssociationPropsMixin.EventChannelConfigurationProperty(
                    enable_webhook_updates=False
                ),
                git_hub=devopsagent_mixins.CfnAssociationPropsMixin.GitHubConfigurationProperty(
                    owner="owner",
                    owner_type="ownerType",
                    repo_id="repoId",
                    repo_name="repoName"
                ),
                git_lab=devopsagent_mixins.CfnAssociationPropsMixin.GitLabConfigurationProperty(
                    enable_webhook_updates=False,
                    instance_identifier="instanceIdentifier",
                    project_id="projectId",
                    project_path="projectPath"
                ),
                mcp_server=devopsagent_mixins.CfnAssociationPropsMixin.MCPServerConfigurationProperty(
                    description="description",
                    enable_webhook_updates=False,
                    endpoint="endpoint",
                    name="name",
                    tools=["tools"]
                ),
                mcp_server_datadog=devopsagent_mixins.CfnAssociationPropsMixin.MCPServerDatadogConfigurationProperty(
                    description="description",
                    enable_webhook_updates=False,
                    endpoint="endpoint",
                    name="name"
                ),
                mcp_server_new_relic=devopsagent_mixins.CfnAssociationPropsMixin.MCPServerNewRelicConfigurationProperty(
                    account_id="accountId",
                    endpoint="endpoint"
                ),
                mcp_server_splunk=devopsagent_mixins.CfnAssociationPropsMixin.MCPServerSplunkConfigurationProperty(
                    description="description",
                    enable_webhook_updates=False,
                    endpoint="endpoint",
                    name="name"
                ),
                service_now=devopsagent_mixins.CfnAssociationPropsMixin.ServiceNowConfigurationProperty(
                    enable_webhook_updates=False,
                    instance_id="instanceId"
                ),
                slack=devopsagent_mixins.CfnAssociationPropsMixin.SlackConfigurationProperty(
                    transmission_target=devopsagent_mixins.CfnAssociationPropsMixin.SlackTransmissionTargetProperty(
                        incident_response_target=devopsagent_mixins.CfnAssociationPropsMixin.SlackChannelProperty(
                            channel_id="channelId",
                            channel_name="channelName"
                        )
                    ),
                    workspace_id="workspaceId",
                    workspace_name="workspaceName"
                ),
                source_aws=devopsagent_mixins.CfnAssociationPropsMixin.SourceAwsConfigurationProperty(
                    account_id="accountId",
                    account_type="accountType",
                    assumable_role_arn="assumableRoleArn",
                    resources=[devopsagent_mixins.CfnAssociationPropsMixin.AWSResourceProperty(
                        resource_arn="resourceArn",
                        resource_metadata=resource_metadata,
                        resource_type="resourceType"
                    )],
                    tags=[devopsagent_mixins.CfnAssociationPropsMixin.KeyValuePairProperty(
                        key="key",
                        value="value"
                    )]
                )
            ),
            service_id="serviceId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DevOpsAgent::Association``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__014beb490a60ad6e6be3455292997200b97499f32c4803b28843e0b5045764c3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ca6f99f1695c45b527318e366474fcd4904af8b349a33534199aa9221b4ba5b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aea81dde36c1cd4873aaee380cfe21941d1f295fb46de835edb7ffe9893c6b3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAssociationMixinProps:
        return typing.cast(CfnAssociationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_devopsagent.mixins.CfnAssociationPropsMixin.AWSConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "account_id": "accountId",
            "account_type": "accountType",
            "assumable_role_arn": "assumableRoleArn",
            "resources": "resources",
            "tags": "tags",
        },
    )
    class AWSConfigurationProperty:
        def __init__(
            self,
            *,
            account_id: typing.Optional[builtins.str] = None,
            account_type: typing.Optional[builtins.str] = None,
            assumable_role_arn: typing.Optional[builtins.str] = None,
            resources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAssociationPropsMixin.AWSResourceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            tags: typing.Optional[typing.Sequence[typing.Union["CfnAssociationPropsMixin.KeyValuePairProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''AWS association for 'monitor' account.

            :param account_id: AWS Account Id corresponding to provided resources.
            :param account_type: Account Type 'monitor' for DevOpsAgent monitoring.
            :param assumable_role_arn: Role ARN to be assumed by DevOpsAgent to operate on behalf of customer.
            :param resources: List of AWS resources.
            :param tags: List of AWS tags as key-value pairs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-awsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_devopsagent import mixins as devopsagent_mixins
                
                # resource_metadata: Any
                
                a_wSConfiguration_property = devopsagent_mixins.CfnAssociationPropsMixin.AWSConfigurationProperty(
                    account_id="accountId",
                    account_type="accountType",
                    assumable_role_arn="assumableRoleArn",
                    resources=[devopsagent_mixins.CfnAssociationPropsMixin.AWSResourceProperty(
                        resource_arn="resourceArn",
                        resource_metadata=resource_metadata,
                        resource_type="resourceType"
                    )],
                    tags=[devopsagent_mixins.CfnAssociationPropsMixin.KeyValuePairProperty(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2db9191898db305fa9abd122576e2270bbecbfadd52929d152db9ab14524a8ac)
                check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
                check_type(argname="argument account_type", value=account_type, expected_type=type_hints["account_type"])
                check_type(argname="argument assumable_role_arn", value=assumable_role_arn, expected_type=type_hints["assumable_role_arn"])
                check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if account_id is not None:
                self._values["account_id"] = account_id
            if account_type is not None:
                self._values["account_type"] = account_type
            if assumable_role_arn is not None:
                self._values["assumable_role_arn"] = assumable_role_arn
            if resources is not None:
                self._values["resources"] = resources
            if tags is not None:
                self._values["tags"] = tags

        @builtins.property
        def account_id(self) -> typing.Optional[builtins.str]:
            '''AWS Account Id corresponding to provided resources.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-awsconfiguration.html#cfn-devopsagent-association-awsconfiguration-accountid
            '''
            result = self._values.get("account_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def account_type(self) -> typing.Optional[builtins.str]:
            '''Account Type 'monitor' for DevOpsAgent monitoring.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-awsconfiguration.html#cfn-devopsagent-association-awsconfiguration-accounttype
            '''
            result = self._values.get("account_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def assumable_role_arn(self) -> typing.Optional[builtins.str]:
            '''Role ARN to be assumed by DevOpsAgent to operate on behalf of customer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-awsconfiguration.html#cfn-devopsagent-association-awsconfiguration-assumablerolearn
            '''
            result = self._values.get("assumable_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resources(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssociationPropsMixin.AWSResourceProperty"]]]]:
            '''List of AWS resources.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-awsconfiguration.html#cfn-devopsagent-association-awsconfiguration-resources
            '''
            result = self._values.get("resources")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssociationPropsMixin.AWSResourceProperty"]]]], result)

        @builtins.property
        def tags(
            self,
        ) -> typing.Optional[typing.List["CfnAssociationPropsMixin.KeyValuePairProperty"]]:
            '''List of AWS tags as key-value pairs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-awsconfiguration.html#cfn-devopsagent-association-awsconfiguration-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List["CfnAssociationPropsMixin.KeyValuePairProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AWSConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_devopsagent.mixins.CfnAssociationPropsMixin.AWSResourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "resource_arn": "resourceArn",
            "resource_metadata": "resourceMetadata",
            "resource_type": "resourceType",
        },
    )
    class AWSResourceProperty:
        def __init__(
            self,
            *,
            resource_arn: typing.Optional[builtins.str] = None,
            resource_metadata: typing.Any = None,
            resource_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''AWS resource definition.

            :param resource_arn: The Amazon Resource Name (ARN) of the resource.
            :param resource_metadata: Additional metadata for the resource.
            :param resource_type: Resource type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-awsresource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_devopsagent import mixins as devopsagent_mixins
                
                # resource_metadata: Any
                
                a_wSResource_property = devopsagent_mixins.CfnAssociationPropsMixin.AWSResourceProperty(
                    resource_arn="resourceArn",
                    resource_metadata=resource_metadata,
                    resource_type="resourceType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__521c8c8915b7341a1856199e8052f3b28b1ddf3f10c5f2bc4ef2186999f47827)
                check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
                check_type(argname="argument resource_metadata", value=resource_metadata, expected_type=type_hints["resource_metadata"])
                check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if resource_arn is not None:
                self._values["resource_arn"] = resource_arn
            if resource_metadata is not None:
                self._values["resource_metadata"] = resource_metadata
            if resource_type is not None:
                self._values["resource_type"] = resource_type

        @builtins.property
        def resource_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-awsresource.html#cfn-devopsagent-association-awsresource-resourcearn
            '''
            result = self._values.get("resource_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_metadata(self) -> typing.Any:
            '''Additional metadata for the resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-awsresource.html#cfn-devopsagent-association-awsresource-resourcemetadata
            '''
            result = self._values.get("resource_metadata")
            return typing.cast(typing.Any, result)

        @builtins.property
        def resource_type(self) -> typing.Optional[builtins.str]:
            '''Resource type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-awsresource.html#cfn-devopsagent-association-awsresource-resourcetype
            '''
            result = self._values.get("resource_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AWSResourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_devopsagent.mixins.CfnAssociationPropsMixin.DynatraceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enable_webhook_updates": "enableWebhookUpdates",
            "env_id": "envId",
            "resources": "resources",
        },
    )
    class DynatraceConfigurationProperty:
        def __init__(
            self,
            *,
            enable_webhook_updates: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            env_id: typing.Optional[builtins.str] = None,
            resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Dynatrace monitoring configuration.

            :param enable_webhook_updates: When set to true, enables the Agent Space to create and update webhooks for receiving notifications and events from the service.
            :param env_id: Dynatrace environment id.
            :param resources: List of Dynatrace resources to monitor.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-dynatraceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_devopsagent import mixins as devopsagent_mixins
                
                dynatrace_configuration_property = devopsagent_mixins.CfnAssociationPropsMixin.DynatraceConfigurationProperty(
                    enable_webhook_updates=False,
                    env_id="envId",
                    resources=["resources"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__92ae8f30ff2804b5e5854a8e68a18660b6042ed84a304af9b79010746c56797e)
                check_type(argname="argument enable_webhook_updates", value=enable_webhook_updates, expected_type=type_hints["enable_webhook_updates"])
                check_type(argname="argument env_id", value=env_id, expected_type=type_hints["env_id"])
                check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enable_webhook_updates is not None:
                self._values["enable_webhook_updates"] = enable_webhook_updates
            if env_id is not None:
                self._values["env_id"] = env_id
            if resources is not None:
                self._values["resources"] = resources

        @builtins.property
        def enable_webhook_updates(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When set to true, enables the Agent Space to create and update webhooks for receiving notifications and events from the service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-dynatraceconfiguration.html#cfn-devopsagent-association-dynatraceconfiguration-enablewebhookupdates
            '''
            result = self._values.get("enable_webhook_updates")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def env_id(self) -> typing.Optional[builtins.str]:
            '''Dynatrace environment id.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-dynatraceconfiguration.html#cfn-devopsagent-association-dynatraceconfiguration-envid
            '''
            result = self._values.get("env_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resources(self) -> typing.Optional[typing.List[builtins.str]]:
            '''List of Dynatrace resources to monitor.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-dynatraceconfiguration.html#cfn-devopsagent-association-dynatraceconfiguration-resources
            '''
            result = self._values.get("resources")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DynatraceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_devopsagent.mixins.CfnAssociationPropsMixin.EventChannelConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"enable_webhook_updates": "enableWebhookUpdates"},
    )
    class EventChannelConfigurationProperty:
        def __init__(
            self,
            *,
            enable_webhook_updates: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''EventChannelconfiguration.

            :param enable_webhook_updates: When set to true, enables the Agent Space to create and update webhooks for receiving notifications and events from the service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-eventchannelconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_devopsagent import mixins as devopsagent_mixins
                
                event_channel_configuration_property = devopsagent_mixins.CfnAssociationPropsMixin.EventChannelConfigurationProperty(
                    enable_webhook_updates=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d391f7bdf8bec104897d523260fef5004a232899d706a5be4d1adeb7d6483a55)
                check_type(argname="argument enable_webhook_updates", value=enable_webhook_updates, expected_type=type_hints["enable_webhook_updates"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enable_webhook_updates is not None:
                self._values["enable_webhook_updates"] = enable_webhook_updates

        @builtins.property
        def enable_webhook_updates(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When set to true, enables the Agent Space to create and update webhooks for receiving notifications and events from the service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-eventchannelconfiguration.html#cfn-devopsagent-association-eventchannelconfiguration-enablewebhookupdates
            '''
            result = self._values.get("enable_webhook_updates")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventChannelConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_devopsagent.mixins.CfnAssociationPropsMixin.GitHubConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "owner": "owner",
            "owner_type": "ownerType",
            "repo_id": "repoId",
            "repo_name": "repoName",
        },
    )
    class GitHubConfigurationProperty:
        def __init__(
            self,
            *,
            owner: typing.Optional[builtins.str] = None,
            owner_type: typing.Optional[builtins.str] = None,
            repo_id: typing.Optional[builtins.str] = None,
            repo_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''GitHub repository integration configuration.

            :param owner: Repository owner.
            :param owner_type: Type of repository owner.
            :param repo_id: Associated Github repo ID.
            :param repo_name: Associated Github repo name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-githubconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_devopsagent import mixins as devopsagent_mixins
                
                git_hub_configuration_property = devopsagent_mixins.CfnAssociationPropsMixin.GitHubConfigurationProperty(
                    owner="owner",
                    owner_type="ownerType",
                    repo_id="repoId",
                    repo_name="repoName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2a749f613cac6f9899388d412be0f147648778a951e765435dbb776130f82ecc)
                check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
                check_type(argname="argument owner_type", value=owner_type, expected_type=type_hints["owner_type"])
                check_type(argname="argument repo_id", value=repo_id, expected_type=type_hints["repo_id"])
                check_type(argname="argument repo_name", value=repo_name, expected_type=type_hints["repo_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if owner is not None:
                self._values["owner"] = owner
            if owner_type is not None:
                self._values["owner_type"] = owner_type
            if repo_id is not None:
                self._values["repo_id"] = repo_id
            if repo_name is not None:
                self._values["repo_name"] = repo_name

        @builtins.property
        def owner(self) -> typing.Optional[builtins.str]:
            '''Repository owner.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-githubconfiguration.html#cfn-devopsagent-association-githubconfiguration-owner
            '''
            result = self._values.get("owner")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def owner_type(self) -> typing.Optional[builtins.str]:
            '''Type of repository owner.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-githubconfiguration.html#cfn-devopsagent-association-githubconfiguration-ownertype
            '''
            result = self._values.get("owner_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def repo_id(self) -> typing.Optional[builtins.str]:
            '''Associated Github repo ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-githubconfiguration.html#cfn-devopsagent-association-githubconfiguration-repoid
            '''
            result = self._values.get("repo_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def repo_name(self) -> typing.Optional[builtins.str]:
            '''Associated Github repo name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-githubconfiguration.html#cfn-devopsagent-association-githubconfiguration-reponame
            '''
            result = self._values.get("repo_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GitHubConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_devopsagent.mixins.CfnAssociationPropsMixin.GitLabConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enable_webhook_updates": "enableWebhookUpdates",
            "instance_identifier": "instanceIdentifier",
            "project_id": "projectId",
            "project_path": "projectPath",
        },
    )
    class GitLabConfigurationProperty:
        def __init__(
            self,
            *,
            enable_webhook_updates: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            instance_identifier: typing.Optional[builtins.str] = None,
            project_id: typing.Optional[builtins.str] = None,
            project_path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''GitLab project integration configuration.

            :param enable_webhook_updates: When set to true, enables the Agent Space to create and update webhooks for receiving notifications and events from the service.
            :param instance_identifier: GitLab instance identifier.
            :param project_id: GitLab numeric project ID.
            :param project_path: Full GitLab project path (e.g., namespace/project-name).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-gitlabconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_devopsagent import mixins as devopsagent_mixins
                
                git_lab_configuration_property = devopsagent_mixins.CfnAssociationPropsMixin.GitLabConfigurationProperty(
                    enable_webhook_updates=False,
                    instance_identifier="instanceIdentifier",
                    project_id="projectId",
                    project_path="projectPath"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3d0976b3a3d41c014d81cdffb72e6a2ebc93a7e0a8fca0cc1bc348ca2b73a313)
                check_type(argname="argument enable_webhook_updates", value=enable_webhook_updates, expected_type=type_hints["enable_webhook_updates"])
                check_type(argname="argument instance_identifier", value=instance_identifier, expected_type=type_hints["instance_identifier"])
                check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
                check_type(argname="argument project_path", value=project_path, expected_type=type_hints["project_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enable_webhook_updates is not None:
                self._values["enable_webhook_updates"] = enable_webhook_updates
            if instance_identifier is not None:
                self._values["instance_identifier"] = instance_identifier
            if project_id is not None:
                self._values["project_id"] = project_id
            if project_path is not None:
                self._values["project_path"] = project_path

        @builtins.property
        def enable_webhook_updates(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When set to true, enables the Agent Space to create and update webhooks for receiving notifications and events from the service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-gitlabconfiguration.html#cfn-devopsagent-association-gitlabconfiguration-enablewebhookupdates
            '''
            result = self._values.get("enable_webhook_updates")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def instance_identifier(self) -> typing.Optional[builtins.str]:
            '''GitLab instance identifier.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-gitlabconfiguration.html#cfn-devopsagent-association-gitlabconfiguration-instanceidentifier
            '''
            result = self._values.get("instance_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def project_id(self) -> typing.Optional[builtins.str]:
            '''GitLab numeric project ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-gitlabconfiguration.html#cfn-devopsagent-association-gitlabconfiguration-projectid
            '''
            result = self._values.get("project_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def project_path(self) -> typing.Optional[builtins.str]:
            '''Full GitLab project path (e.g., namespace/project-name).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-gitlabconfiguration.html#cfn-devopsagent-association-gitlabconfiguration-projectpath
            '''
            result = self._values.get("project_path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GitLabConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_devopsagent.mixins.CfnAssociationPropsMixin.KeyValuePairProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class KeyValuePairProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A key-value pair for tags.

            :param key: 
            :param value: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-keyvaluepair.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_devopsagent import mixins as devopsagent_mixins
                
                key_value_pair_property = devopsagent_mixins.CfnAssociationPropsMixin.KeyValuePairProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__24c1a46fa505a703cf6987cf3b6ecc97e995abf7092d97bba4ba2fe2ed632140)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-keyvaluepair.html#cfn-devopsagent-association-keyvaluepair-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-keyvaluepair.html#cfn-devopsagent-association-keyvaluepair-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KeyValuePairProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_devopsagent.mixins.CfnAssociationPropsMixin.MCPServerConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "description": "description",
            "enable_webhook_updates": "enableWebhookUpdates",
            "endpoint": "endpoint",
            "name": "name",
            "tools": "tools",
        },
    )
    class MCPServerConfigurationProperty:
        def __init__(
            self,
            *,
            description: typing.Optional[builtins.str] = None,
            enable_webhook_updates: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            endpoint: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            tools: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''MCP server configuration.

            :param description: The description of the MCP server.
            :param enable_webhook_updates: When set to true, enables the Agent Space to create and update webhooks for receiving notifications and events from the service.
            :param endpoint: MCP server endpoint URL.
            :param name: The name of the MCP server.
            :param tools: List of MCP tools that can be used with the association.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-mcpserverconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_devopsagent import mixins as devopsagent_mixins
                
                m_cPServer_configuration_property = devopsagent_mixins.CfnAssociationPropsMixin.MCPServerConfigurationProperty(
                    description="description",
                    enable_webhook_updates=False,
                    endpoint="endpoint",
                    name="name",
                    tools=["tools"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__43bcea1e8ec2ac05549389a3e48138055c6ad3cbcc715409f86b482e229c09ac)
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument enable_webhook_updates", value=enable_webhook_updates, expected_type=type_hints["enable_webhook_updates"])
                check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument tools", value=tools, expected_type=type_hints["tools"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if description is not None:
                self._values["description"] = description
            if enable_webhook_updates is not None:
                self._values["enable_webhook_updates"] = enable_webhook_updates
            if endpoint is not None:
                self._values["endpoint"] = endpoint
            if name is not None:
                self._values["name"] = name
            if tools is not None:
                self._values["tools"] = tools

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The description of the MCP server.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-mcpserverconfiguration.html#cfn-devopsagent-association-mcpserverconfiguration-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def enable_webhook_updates(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When set to true, enables the Agent Space to create and update webhooks for receiving notifications and events from the service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-mcpserverconfiguration.html#cfn-devopsagent-association-mcpserverconfiguration-enablewebhookupdates
            '''
            result = self._values.get("enable_webhook_updates")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def endpoint(self) -> typing.Optional[builtins.str]:
            '''MCP server endpoint URL.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-mcpserverconfiguration.html#cfn-devopsagent-association-mcpserverconfiguration-endpoint
            '''
            result = self._values.get("endpoint")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the MCP server.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-mcpserverconfiguration.html#cfn-devopsagent-association-mcpserverconfiguration-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tools(self) -> typing.Optional[typing.List[builtins.str]]:
            '''List of MCP tools that can be used with the association.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-mcpserverconfiguration.html#cfn-devopsagent-association-mcpserverconfiguration-tools
            '''
            result = self._values.get("tools")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MCPServerConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_devopsagent.mixins.CfnAssociationPropsMixin.MCPServerDatadogConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "description": "description",
            "enable_webhook_updates": "enableWebhookUpdates",
            "endpoint": "endpoint",
            "name": "name",
        },
    )
    class MCPServerDatadogConfigurationProperty:
        def __init__(
            self,
            *,
            description: typing.Optional[builtins.str] = None,
            enable_webhook_updates: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            endpoint: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Datadog MCP server configuration.

            :param description: The description of the MCP server.
            :param enable_webhook_updates: When set to true, enables the Agent Space to create and update webhooks for receiving notifications and events from the service.
            :param endpoint: MCP server endpoint URL.
            :param name: The name of the MCP server.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-mcpserverdatadogconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_devopsagent import mixins as devopsagent_mixins
                
                m_cPServer_datadog_configuration_property = devopsagent_mixins.CfnAssociationPropsMixin.MCPServerDatadogConfigurationProperty(
                    description="description",
                    enable_webhook_updates=False,
                    endpoint="endpoint",
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__934a691ebc2e40126a0a50a957ad415a92e55a4266bbcffe3d364640769858fd)
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument enable_webhook_updates", value=enable_webhook_updates, expected_type=type_hints["enable_webhook_updates"])
                check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if description is not None:
                self._values["description"] = description
            if enable_webhook_updates is not None:
                self._values["enable_webhook_updates"] = enable_webhook_updates
            if endpoint is not None:
                self._values["endpoint"] = endpoint
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The description of the MCP server.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-mcpserverdatadogconfiguration.html#cfn-devopsagent-association-mcpserverdatadogconfiguration-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def enable_webhook_updates(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When set to true, enables the Agent Space to create and update webhooks for receiving notifications and events from the service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-mcpserverdatadogconfiguration.html#cfn-devopsagent-association-mcpserverdatadogconfiguration-enablewebhookupdates
            '''
            result = self._values.get("enable_webhook_updates")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def endpoint(self) -> typing.Optional[builtins.str]:
            '''MCP server endpoint URL.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-mcpserverdatadogconfiguration.html#cfn-devopsagent-association-mcpserverdatadogconfiguration-endpoint
            '''
            result = self._values.get("endpoint")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the MCP server.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-mcpserverdatadogconfiguration.html#cfn-devopsagent-association-mcpserverdatadogconfiguration-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MCPServerDatadogConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_devopsagent.mixins.CfnAssociationPropsMixin.MCPServerNewRelicConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"account_id": "accountId", "endpoint": "endpoint"},
    )
    class MCPServerNewRelicConfigurationProperty:
        def __init__(
            self,
            *,
            account_id: typing.Optional[builtins.str] = None,
            endpoint: typing.Optional[builtins.str] = None,
        ) -> None:
            '''NewRelic MCP server configuration.

            :param account_id: New Relic Account ID.
            :param endpoint: MCP server endpoint URL (e.g., https://mcp.newrelic.com/mcp/).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-mcpservernewrelicconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_devopsagent import mixins as devopsagent_mixins
                
                m_cPServer_new_relic_configuration_property = devopsagent_mixins.CfnAssociationPropsMixin.MCPServerNewRelicConfigurationProperty(
                    account_id="accountId",
                    endpoint="endpoint"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__503deb88a5ef8d0c98a00f32a1081bde39ecb72372c34b6333a163ccb0ef81ed)
                check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
                check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if account_id is not None:
                self._values["account_id"] = account_id
            if endpoint is not None:
                self._values["endpoint"] = endpoint

        @builtins.property
        def account_id(self) -> typing.Optional[builtins.str]:
            '''New Relic Account ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-mcpservernewrelicconfiguration.html#cfn-devopsagent-association-mcpservernewrelicconfiguration-accountid
            '''
            result = self._values.get("account_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def endpoint(self) -> typing.Optional[builtins.str]:
            '''MCP server endpoint URL (e.g., https://mcp.newrelic.com/mcp/).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-mcpservernewrelicconfiguration.html#cfn-devopsagent-association-mcpservernewrelicconfiguration-endpoint
            '''
            result = self._values.get("endpoint")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MCPServerNewRelicConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_devopsagent.mixins.CfnAssociationPropsMixin.MCPServerSplunkConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "description": "description",
            "enable_webhook_updates": "enableWebhookUpdates",
            "endpoint": "endpoint",
            "name": "name",
        },
    )
    class MCPServerSplunkConfigurationProperty:
        def __init__(
            self,
            *,
            description: typing.Optional[builtins.str] = None,
            enable_webhook_updates: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            endpoint: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Splunk MCP server configuration.

            :param description: The description of the MCP server.
            :param enable_webhook_updates: When set to true, enables the Agent Space to create and update webhooks for receiving notifications and events from the service.
            :param endpoint: MCP server endpoint URL.
            :param name: The name of the MCP server.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-mcpserversplunkconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_devopsagent import mixins as devopsagent_mixins
                
                m_cPServer_splunk_configuration_property = devopsagent_mixins.CfnAssociationPropsMixin.MCPServerSplunkConfigurationProperty(
                    description="description",
                    enable_webhook_updates=False,
                    endpoint="endpoint",
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b8009d5c8e99a749acb046b3d08e0b1855ef3cdfec51f63cfbcd4f63e96682df)
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument enable_webhook_updates", value=enable_webhook_updates, expected_type=type_hints["enable_webhook_updates"])
                check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if description is not None:
                self._values["description"] = description
            if enable_webhook_updates is not None:
                self._values["enable_webhook_updates"] = enable_webhook_updates
            if endpoint is not None:
                self._values["endpoint"] = endpoint
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The description of the MCP server.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-mcpserversplunkconfiguration.html#cfn-devopsagent-association-mcpserversplunkconfiguration-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def enable_webhook_updates(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When set to true, enables the Agent Space to create and update webhooks for receiving notifications and events from the service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-mcpserversplunkconfiguration.html#cfn-devopsagent-association-mcpserversplunkconfiguration-enablewebhookupdates
            '''
            result = self._values.get("enable_webhook_updates")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def endpoint(self) -> typing.Optional[builtins.str]:
            '''MCP server endpoint URL.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-mcpserversplunkconfiguration.html#cfn-devopsagent-association-mcpserversplunkconfiguration-endpoint
            '''
            result = self._values.get("endpoint")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the MCP server.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-mcpserversplunkconfiguration.html#cfn-devopsagent-association-mcpserversplunkconfiguration-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MCPServerSplunkConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_devopsagent.mixins.CfnAssociationPropsMixin.ServiceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "aws": "aws",
            "dynatrace": "dynatrace",
            "event_channel": "eventChannel",
            "git_hub": "gitHub",
            "git_lab": "gitLab",
            "mcp_server": "mcpServer",
            "mcp_server_datadog": "mcpServerDatadog",
            "mcp_server_new_relic": "mcpServerNewRelic",
            "mcp_server_splunk": "mcpServerSplunk",
            "service_now": "serviceNow",
            "slack": "slack",
            "source_aws": "sourceAws",
        },
    )
    class ServiceConfigurationProperty:
        def __init__(
            self,
            *,
            aws: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAssociationPropsMixin.AWSConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            dynatrace: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAssociationPropsMixin.DynatraceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            event_channel: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAssociationPropsMixin.EventChannelConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            git_hub: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAssociationPropsMixin.GitHubConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            git_lab: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAssociationPropsMixin.GitLabConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            mcp_server: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAssociationPropsMixin.MCPServerConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            mcp_server_datadog: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAssociationPropsMixin.MCPServerDatadogConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            mcp_server_new_relic: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAssociationPropsMixin.MCPServerNewRelicConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            mcp_server_splunk: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAssociationPropsMixin.MCPServerSplunkConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            service_now: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAssociationPropsMixin.ServiceNowConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            slack: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAssociationPropsMixin.SlackConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            source_aws: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAssociationPropsMixin.SourceAwsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param aws: AWS association for 'monitor' account.
            :param dynatrace: Dynatrace monitoring configuration.
            :param event_channel: EventChannelconfiguration.
            :param git_hub: GitHub repository integration configuration.
            :param git_lab: GitLab project integration configuration.
            :param mcp_server: MCP server configuration.
            :param mcp_server_datadog: Datadog MCP server configuration.
            :param mcp_server_new_relic: NewRelic MCP server configuration.
            :param mcp_server_splunk: Splunk MCP server configuration.
            :param service_now: ServiceNow integration configuration.
            :param slack: Slack workspace integration configuration.
            :param source_aws: AWS association for 'source' account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-serviceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_devopsagent import mixins as devopsagent_mixins
                
                # resource_metadata: Any
                
                service_configuration_property = devopsagent_mixins.CfnAssociationPropsMixin.ServiceConfigurationProperty(
                    aws=devopsagent_mixins.CfnAssociationPropsMixin.AWSConfigurationProperty(
                        account_id="accountId",
                        account_type="accountType",
                        assumable_role_arn="assumableRoleArn",
                        resources=[devopsagent_mixins.CfnAssociationPropsMixin.AWSResourceProperty(
                            resource_arn="resourceArn",
                            resource_metadata=resource_metadata,
                            resource_type="resourceType"
                        )],
                        tags=[devopsagent_mixins.CfnAssociationPropsMixin.KeyValuePairProperty(
                            key="key",
                            value="value"
                        )]
                    ),
                    dynatrace=devopsagent_mixins.CfnAssociationPropsMixin.DynatraceConfigurationProperty(
                        enable_webhook_updates=False,
                        env_id="envId",
                        resources=["resources"]
                    ),
                    event_channel=devopsagent_mixins.CfnAssociationPropsMixin.EventChannelConfigurationProperty(
                        enable_webhook_updates=False
                    ),
                    git_hub=devopsagent_mixins.CfnAssociationPropsMixin.GitHubConfigurationProperty(
                        owner="owner",
                        owner_type="ownerType",
                        repo_id="repoId",
                        repo_name="repoName"
                    ),
                    git_lab=devopsagent_mixins.CfnAssociationPropsMixin.GitLabConfigurationProperty(
                        enable_webhook_updates=False,
                        instance_identifier="instanceIdentifier",
                        project_id="projectId",
                        project_path="projectPath"
                    ),
                    mcp_server=devopsagent_mixins.CfnAssociationPropsMixin.MCPServerConfigurationProperty(
                        description="description",
                        enable_webhook_updates=False,
                        endpoint="endpoint",
                        name="name",
                        tools=["tools"]
                    ),
                    mcp_server_datadog=devopsagent_mixins.CfnAssociationPropsMixin.MCPServerDatadogConfigurationProperty(
                        description="description",
                        enable_webhook_updates=False,
                        endpoint="endpoint",
                        name="name"
                    ),
                    mcp_server_new_relic=devopsagent_mixins.CfnAssociationPropsMixin.MCPServerNewRelicConfigurationProperty(
                        account_id="accountId",
                        endpoint="endpoint"
                    ),
                    mcp_server_splunk=devopsagent_mixins.CfnAssociationPropsMixin.MCPServerSplunkConfigurationProperty(
                        description="description",
                        enable_webhook_updates=False,
                        endpoint="endpoint",
                        name="name"
                    ),
                    service_now=devopsagent_mixins.CfnAssociationPropsMixin.ServiceNowConfigurationProperty(
                        enable_webhook_updates=False,
                        instance_id="instanceId"
                    ),
                    slack=devopsagent_mixins.CfnAssociationPropsMixin.SlackConfigurationProperty(
                        transmission_target=devopsagent_mixins.CfnAssociationPropsMixin.SlackTransmissionTargetProperty(
                            incident_response_target=devopsagent_mixins.CfnAssociationPropsMixin.SlackChannelProperty(
                                channel_id="channelId",
                                channel_name="channelName"
                            )
                        ),
                        workspace_id="workspaceId",
                        workspace_name="workspaceName"
                    ),
                    source_aws=devopsagent_mixins.CfnAssociationPropsMixin.SourceAwsConfigurationProperty(
                        account_id="accountId",
                        account_type="accountType",
                        assumable_role_arn="assumableRoleArn",
                        resources=[devopsagent_mixins.CfnAssociationPropsMixin.AWSResourceProperty(
                            resource_arn="resourceArn",
                            resource_metadata=resource_metadata,
                            resource_type="resourceType"
                        )],
                        tags=[devopsagent_mixins.CfnAssociationPropsMixin.KeyValuePairProperty(
                            key="key",
                            value="value"
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__650e48ec479e7a1b9064d59e020e37c2dc46ce45a4ca814e465d16a775c3ad5c)
                check_type(argname="argument aws", value=aws, expected_type=type_hints["aws"])
                check_type(argname="argument dynatrace", value=dynatrace, expected_type=type_hints["dynatrace"])
                check_type(argname="argument event_channel", value=event_channel, expected_type=type_hints["event_channel"])
                check_type(argname="argument git_hub", value=git_hub, expected_type=type_hints["git_hub"])
                check_type(argname="argument git_lab", value=git_lab, expected_type=type_hints["git_lab"])
                check_type(argname="argument mcp_server", value=mcp_server, expected_type=type_hints["mcp_server"])
                check_type(argname="argument mcp_server_datadog", value=mcp_server_datadog, expected_type=type_hints["mcp_server_datadog"])
                check_type(argname="argument mcp_server_new_relic", value=mcp_server_new_relic, expected_type=type_hints["mcp_server_new_relic"])
                check_type(argname="argument mcp_server_splunk", value=mcp_server_splunk, expected_type=type_hints["mcp_server_splunk"])
                check_type(argname="argument service_now", value=service_now, expected_type=type_hints["service_now"])
                check_type(argname="argument slack", value=slack, expected_type=type_hints["slack"])
                check_type(argname="argument source_aws", value=source_aws, expected_type=type_hints["source_aws"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if aws is not None:
                self._values["aws"] = aws
            if dynatrace is not None:
                self._values["dynatrace"] = dynatrace
            if event_channel is not None:
                self._values["event_channel"] = event_channel
            if git_hub is not None:
                self._values["git_hub"] = git_hub
            if git_lab is not None:
                self._values["git_lab"] = git_lab
            if mcp_server is not None:
                self._values["mcp_server"] = mcp_server
            if mcp_server_datadog is not None:
                self._values["mcp_server_datadog"] = mcp_server_datadog
            if mcp_server_new_relic is not None:
                self._values["mcp_server_new_relic"] = mcp_server_new_relic
            if mcp_server_splunk is not None:
                self._values["mcp_server_splunk"] = mcp_server_splunk
            if service_now is not None:
                self._values["service_now"] = service_now
            if slack is not None:
                self._values["slack"] = slack
            if source_aws is not None:
                self._values["source_aws"] = source_aws

        @builtins.property
        def aws(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssociationPropsMixin.AWSConfigurationProperty"]]:
            '''AWS association for 'monitor' account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-serviceconfiguration.html#cfn-devopsagent-association-serviceconfiguration-aws
            '''
            result = self._values.get("aws")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssociationPropsMixin.AWSConfigurationProperty"]], result)

        @builtins.property
        def dynatrace(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssociationPropsMixin.DynatraceConfigurationProperty"]]:
            '''Dynatrace monitoring configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-serviceconfiguration.html#cfn-devopsagent-association-serviceconfiguration-dynatrace
            '''
            result = self._values.get("dynatrace")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssociationPropsMixin.DynatraceConfigurationProperty"]], result)

        @builtins.property
        def event_channel(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssociationPropsMixin.EventChannelConfigurationProperty"]]:
            '''EventChannelconfiguration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-serviceconfiguration.html#cfn-devopsagent-association-serviceconfiguration-eventchannel
            '''
            result = self._values.get("event_channel")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssociationPropsMixin.EventChannelConfigurationProperty"]], result)

        @builtins.property
        def git_hub(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssociationPropsMixin.GitHubConfigurationProperty"]]:
            '''GitHub repository integration configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-serviceconfiguration.html#cfn-devopsagent-association-serviceconfiguration-github
            '''
            result = self._values.get("git_hub")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssociationPropsMixin.GitHubConfigurationProperty"]], result)

        @builtins.property
        def git_lab(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssociationPropsMixin.GitLabConfigurationProperty"]]:
            '''GitLab project integration configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-serviceconfiguration.html#cfn-devopsagent-association-serviceconfiguration-gitlab
            '''
            result = self._values.get("git_lab")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssociationPropsMixin.GitLabConfigurationProperty"]], result)

        @builtins.property
        def mcp_server(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssociationPropsMixin.MCPServerConfigurationProperty"]]:
            '''MCP server configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-serviceconfiguration.html#cfn-devopsagent-association-serviceconfiguration-mcpserver
            '''
            result = self._values.get("mcp_server")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssociationPropsMixin.MCPServerConfigurationProperty"]], result)

        @builtins.property
        def mcp_server_datadog(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssociationPropsMixin.MCPServerDatadogConfigurationProperty"]]:
            '''Datadog MCP server configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-serviceconfiguration.html#cfn-devopsagent-association-serviceconfiguration-mcpserverdatadog
            '''
            result = self._values.get("mcp_server_datadog")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssociationPropsMixin.MCPServerDatadogConfigurationProperty"]], result)

        @builtins.property
        def mcp_server_new_relic(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssociationPropsMixin.MCPServerNewRelicConfigurationProperty"]]:
            '''NewRelic MCP server configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-serviceconfiguration.html#cfn-devopsagent-association-serviceconfiguration-mcpservernewrelic
            '''
            result = self._values.get("mcp_server_new_relic")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssociationPropsMixin.MCPServerNewRelicConfigurationProperty"]], result)

        @builtins.property
        def mcp_server_splunk(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssociationPropsMixin.MCPServerSplunkConfigurationProperty"]]:
            '''Splunk MCP server configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-serviceconfiguration.html#cfn-devopsagent-association-serviceconfiguration-mcpserversplunk
            '''
            result = self._values.get("mcp_server_splunk")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssociationPropsMixin.MCPServerSplunkConfigurationProperty"]], result)

        @builtins.property
        def service_now(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssociationPropsMixin.ServiceNowConfigurationProperty"]]:
            '''ServiceNow integration configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-serviceconfiguration.html#cfn-devopsagent-association-serviceconfiguration-servicenow
            '''
            result = self._values.get("service_now")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssociationPropsMixin.ServiceNowConfigurationProperty"]], result)

        @builtins.property
        def slack(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssociationPropsMixin.SlackConfigurationProperty"]]:
            '''Slack workspace integration configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-serviceconfiguration.html#cfn-devopsagent-association-serviceconfiguration-slack
            '''
            result = self._values.get("slack")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssociationPropsMixin.SlackConfigurationProperty"]], result)

        @builtins.property
        def source_aws(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssociationPropsMixin.SourceAwsConfigurationProperty"]]:
            '''AWS association for 'source' account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-serviceconfiguration.html#cfn-devopsagent-association-serviceconfiguration-sourceaws
            '''
            result = self._values.get("source_aws")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssociationPropsMixin.SourceAwsConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServiceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_devopsagent.mixins.CfnAssociationPropsMixin.ServiceNowConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enable_webhook_updates": "enableWebhookUpdates",
            "instance_id": "instanceId",
        },
    )
    class ServiceNowConfigurationProperty:
        def __init__(
            self,
            *,
            enable_webhook_updates: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            instance_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''ServiceNow integration configuration.

            :param enable_webhook_updates: When set to true, enables the Agent Space to create and update webhooks for receiving notifications and events from the service.
            :param instance_id: ServiceNow instance ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-servicenowconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_devopsagent import mixins as devopsagent_mixins
                
                service_now_configuration_property = devopsagent_mixins.CfnAssociationPropsMixin.ServiceNowConfigurationProperty(
                    enable_webhook_updates=False,
                    instance_id="instanceId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__49dca394a6843a10955f8dff9541736e68d7a79ce88ec00b20d3e1faa58f23fa)
                check_type(argname="argument enable_webhook_updates", value=enable_webhook_updates, expected_type=type_hints["enable_webhook_updates"])
                check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enable_webhook_updates is not None:
                self._values["enable_webhook_updates"] = enable_webhook_updates
            if instance_id is not None:
                self._values["instance_id"] = instance_id

        @builtins.property
        def enable_webhook_updates(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When set to true, enables the Agent Space to create and update webhooks for receiving notifications and events from the service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-servicenowconfiguration.html#cfn-devopsagent-association-servicenowconfiguration-enablewebhookupdates
            '''
            result = self._values.get("enable_webhook_updates")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def instance_id(self) -> typing.Optional[builtins.str]:
            '''ServiceNow instance ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-servicenowconfiguration.html#cfn-devopsagent-association-servicenowconfiguration-instanceid
            '''
            result = self._values.get("instance_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServiceNowConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_devopsagent.mixins.CfnAssociationPropsMixin.SlackChannelProperty",
        jsii_struct_bases=[],
        name_mapping={"channel_id": "channelId", "channel_name": "channelName"},
    )
    class SlackChannelProperty:
        def __init__(
            self,
            *,
            channel_id: typing.Optional[builtins.str] = None,
            channel_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Slack channel configuration.

            :param channel_id: Slack channel ID.
            :param channel_name: Slack channel name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-slackchannel.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_devopsagent import mixins as devopsagent_mixins
                
                slack_channel_property = devopsagent_mixins.CfnAssociationPropsMixin.SlackChannelProperty(
                    channel_id="channelId",
                    channel_name="channelName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__30e2f3214ed4292c323738dd466e7f88ea6115602eb6fa37027e341b026d0c4f)
                check_type(argname="argument channel_id", value=channel_id, expected_type=type_hints["channel_id"])
                check_type(argname="argument channel_name", value=channel_name, expected_type=type_hints["channel_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if channel_id is not None:
                self._values["channel_id"] = channel_id
            if channel_name is not None:
                self._values["channel_name"] = channel_name

        @builtins.property
        def channel_id(self) -> typing.Optional[builtins.str]:
            '''Slack channel ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-slackchannel.html#cfn-devopsagent-association-slackchannel-channelid
            '''
            result = self._values.get("channel_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def channel_name(self) -> typing.Optional[builtins.str]:
            '''Slack channel name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-slackchannel.html#cfn-devopsagent-association-slackchannel-channelname
            '''
            result = self._values.get("channel_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlackChannelProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_devopsagent.mixins.CfnAssociationPropsMixin.SlackConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "transmission_target": "transmissionTarget",
            "workspace_id": "workspaceId",
            "workspace_name": "workspaceName",
        },
    )
    class SlackConfigurationProperty:
        def __init__(
            self,
            *,
            transmission_target: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAssociationPropsMixin.SlackTransmissionTargetProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            workspace_id: typing.Optional[builtins.str] = None,
            workspace_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Slack workspace integration configuration.

            :param transmission_target: Transmission targets for agent notifications.
            :param workspace_id: Associated Slack workspace ID.
            :param workspace_name: Associated Slack workspace name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-slackconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_devopsagent import mixins as devopsagent_mixins
                
                slack_configuration_property = devopsagent_mixins.CfnAssociationPropsMixin.SlackConfigurationProperty(
                    transmission_target=devopsagent_mixins.CfnAssociationPropsMixin.SlackTransmissionTargetProperty(
                        incident_response_target=devopsagent_mixins.CfnAssociationPropsMixin.SlackChannelProperty(
                            channel_id="channelId",
                            channel_name="channelName"
                        )
                    ),
                    workspace_id="workspaceId",
                    workspace_name="workspaceName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__160f70183a32c38a04104c4bab976707cfcabfa49c29b609fa3ca22092d72570)
                check_type(argname="argument transmission_target", value=transmission_target, expected_type=type_hints["transmission_target"])
                check_type(argname="argument workspace_id", value=workspace_id, expected_type=type_hints["workspace_id"])
                check_type(argname="argument workspace_name", value=workspace_name, expected_type=type_hints["workspace_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if transmission_target is not None:
                self._values["transmission_target"] = transmission_target
            if workspace_id is not None:
                self._values["workspace_id"] = workspace_id
            if workspace_name is not None:
                self._values["workspace_name"] = workspace_name

        @builtins.property
        def transmission_target(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssociationPropsMixin.SlackTransmissionTargetProperty"]]:
            '''Transmission targets for agent notifications.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-slackconfiguration.html#cfn-devopsagent-association-slackconfiguration-transmissiontarget
            '''
            result = self._values.get("transmission_target")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssociationPropsMixin.SlackTransmissionTargetProperty"]], result)

        @builtins.property
        def workspace_id(self) -> typing.Optional[builtins.str]:
            '''Associated Slack workspace ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-slackconfiguration.html#cfn-devopsagent-association-slackconfiguration-workspaceid
            '''
            result = self._values.get("workspace_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def workspace_name(self) -> typing.Optional[builtins.str]:
            '''Associated Slack workspace name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-slackconfiguration.html#cfn-devopsagent-association-slackconfiguration-workspacename
            '''
            result = self._values.get("workspace_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlackConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_devopsagent.mixins.CfnAssociationPropsMixin.SlackTransmissionTargetProperty",
        jsii_struct_bases=[],
        name_mapping={"incident_response_target": "incidentResponseTarget"},
    )
    class SlackTransmissionTargetProperty:
        def __init__(
            self,
            *,
            incident_response_target: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAssociationPropsMixin.SlackChannelProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Transmission targets for agent notifications.

            :param incident_response_target: Slack channel configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-slacktransmissiontarget.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_devopsagent import mixins as devopsagent_mixins
                
                slack_transmission_target_property = devopsagent_mixins.CfnAssociationPropsMixin.SlackTransmissionTargetProperty(
                    incident_response_target=devopsagent_mixins.CfnAssociationPropsMixin.SlackChannelProperty(
                        channel_id="channelId",
                        channel_name="channelName"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__aa95e7f44c940b8ede0b37995d7403b2401dab1e7c4bab1a4dcb16c9450f3ce8)
                check_type(argname="argument incident_response_target", value=incident_response_target, expected_type=type_hints["incident_response_target"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if incident_response_target is not None:
                self._values["incident_response_target"] = incident_response_target

        @builtins.property
        def incident_response_target(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssociationPropsMixin.SlackChannelProperty"]]:
            '''Slack channel configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-slacktransmissiontarget.html#cfn-devopsagent-association-slacktransmissiontarget-incidentresponsetarget
            '''
            result = self._values.get("incident_response_target")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssociationPropsMixin.SlackChannelProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlackTransmissionTargetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_devopsagent.mixins.CfnAssociationPropsMixin.SourceAwsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "account_id": "accountId",
            "account_type": "accountType",
            "assumable_role_arn": "assumableRoleArn",
            "resources": "resources",
            "tags": "tags",
        },
    )
    class SourceAwsConfigurationProperty:
        def __init__(
            self,
            *,
            account_id: typing.Optional[builtins.str] = None,
            account_type: typing.Optional[builtins.str] = None,
            assumable_role_arn: typing.Optional[builtins.str] = None,
            resources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAssociationPropsMixin.AWSResourceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            tags: typing.Optional[typing.Sequence[typing.Union["CfnAssociationPropsMixin.KeyValuePairProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''AWS association for 'source' account.

            :param account_id: AWS Account Id corresponding to provided resources.
            :param account_type: Account Type 'source' for DevOpsAgent monitoring.
            :param assumable_role_arn: Role ARN to be assumed by DevOpsAgent to operate on behalf of customer.
            :param resources: List of AWS resources.
            :param tags: List of AWS tags as key-value pairs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-sourceawsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_devopsagent import mixins as devopsagent_mixins
                
                # resource_metadata: Any
                
                source_aws_configuration_property = devopsagent_mixins.CfnAssociationPropsMixin.SourceAwsConfigurationProperty(
                    account_id="accountId",
                    account_type="accountType",
                    assumable_role_arn="assumableRoleArn",
                    resources=[devopsagent_mixins.CfnAssociationPropsMixin.AWSResourceProperty(
                        resource_arn="resourceArn",
                        resource_metadata=resource_metadata,
                        resource_type="resourceType"
                    )],
                    tags=[devopsagent_mixins.CfnAssociationPropsMixin.KeyValuePairProperty(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b80beab9a8ab2549cc9c140f097f3b6623b631007f54fe44a6c9a676bdb8242b)
                check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
                check_type(argname="argument account_type", value=account_type, expected_type=type_hints["account_type"])
                check_type(argname="argument assumable_role_arn", value=assumable_role_arn, expected_type=type_hints["assumable_role_arn"])
                check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if account_id is not None:
                self._values["account_id"] = account_id
            if account_type is not None:
                self._values["account_type"] = account_type
            if assumable_role_arn is not None:
                self._values["assumable_role_arn"] = assumable_role_arn
            if resources is not None:
                self._values["resources"] = resources
            if tags is not None:
                self._values["tags"] = tags

        @builtins.property
        def account_id(self) -> typing.Optional[builtins.str]:
            '''AWS Account Id corresponding to provided resources.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-sourceawsconfiguration.html#cfn-devopsagent-association-sourceawsconfiguration-accountid
            '''
            result = self._values.get("account_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def account_type(self) -> typing.Optional[builtins.str]:
            '''Account Type 'source' for DevOpsAgent monitoring.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-sourceawsconfiguration.html#cfn-devopsagent-association-sourceawsconfiguration-accounttype
            '''
            result = self._values.get("account_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def assumable_role_arn(self) -> typing.Optional[builtins.str]:
            '''Role ARN to be assumed by DevOpsAgent to operate on behalf of customer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-sourceawsconfiguration.html#cfn-devopsagent-association-sourceawsconfiguration-assumablerolearn
            '''
            result = self._values.get("assumable_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resources(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssociationPropsMixin.AWSResourceProperty"]]]]:
            '''List of AWS resources.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-sourceawsconfiguration.html#cfn-devopsagent-association-sourceawsconfiguration-resources
            '''
            result = self._values.get("resources")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssociationPropsMixin.AWSResourceProperty"]]]], result)

        @builtins.property
        def tags(
            self,
        ) -> typing.Optional[typing.List["CfnAssociationPropsMixin.KeyValuePairProperty"]]:
            '''List of AWS tags as key-value pairs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-sourceawsconfiguration.html#cfn-devopsagent-association-sourceawsconfiguration-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List["CfnAssociationPropsMixin.KeyValuePairProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceAwsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnAgentSpaceMixinProps",
    "CfnAgentSpacePropsMixin",
    "CfnAssociationMixinProps",
    "CfnAssociationPropsMixin",
]

publication.publish()

def _typecheckingstub__fbdd263ae3abff6b5cfec8e91d9de58428b834f2db8d486936e8a4f7357aa0e8(
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d61711350e89d0d475000f2052741ea118ca4ecd343a7123334f3f65792af5a(
    props: typing.Union[CfnAgentSpaceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7d7857d5a30970573b711ff1657f799dd35453fb83790f6c255df3e03e19e14(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16e5c29fdba529bde10b22b077cb9551104b512fe299645edb91711e40257852(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__752652b0f356ef6b057c6d4c88cb6f15261ad4bd8630c44373893dbf672bffb8(
    *,
    agent_space_id: typing.Optional[builtins.str] = None,
    configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAssociationPropsMixin.ServiceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    service_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__014beb490a60ad6e6be3455292997200b97499f32c4803b28843e0b5045764c3(
    props: typing.Union[CfnAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ca6f99f1695c45b527318e366474fcd4904af8b349a33534199aa9221b4ba5b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aea81dde36c1cd4873aaee380cfe21941d1f295fb46de835edb7ffe9893c6b3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2db9191898db305fa9abd122576e2270bbecbfadd52929d152db9ab14524a8ac(
    *,
    account_id: typing.Optional[builtins.str] = None,
    account_type: typing.Optional[builtins.str] = None,
    assumable_role_arn: typing.Optional[builtins.str] = None,
    resources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAssociationPropsMixin.AWSResourceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnAssociationPropsMixin.KeyValuePairProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__521c8c8915b7341a1856199e8052f3b28b1ddf3f10c5f2bc4ef2186999f47827(
    *,
    resource_arn: typing.Optional[builtins.str] = None,
    resource_metadata: typing.Any = None,
    resource_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92ae8f30ff2804b5e5854a8e68a18660b6042ed84a304af9b79010746c56797e(
    *,
    enable_webhook_updates: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    env_id: typing.Optional[builtins.str] = None,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d391f7bdf8bec104897d523260fef5004a232899d706a5be4d1adeb7d6483a55(
    *,
    enable_webhook_updates: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a749f613cac6f9899388d412be0f147648778a951e765435dbb776130f82ecc(
    *,
    owner: typing.Optional[builtins.str] = None,
    owner_type: typing.Optional[builtins.str] = None,
    repo_id: typing.Optional[builtins.str] = None,
    repo_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d0976b3a3d41c014d81cdffb72e6a2ebc93a7e0a8fca0cc1bc348ca2b73a313(
    *,
    enable_webhook_updates: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    instance_identifier: typing.Optional[builtins.str] = None,
    project_id: typing.Optional[builtins.str] = None,
    project_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24c1a46fa505a703cf6987cf3b6ecc97e995abf7092d97bba4ba2fe2ed632140(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43bcea1e8ec2ac05549389a3e48138055c6ad3cbcc715409f86b482e229c09ac(
    *,
    description: typing.Optional[builtins.str] = None,
    enable_webhook_updates: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    endpoint: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tools: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__934a691ebc2e40126a0a50a957ad415a92e55a4266bbcffe3d364640769858fd(
    *,
    description: typing.Optional[builtins.str] = None,
    enable_webhook_updates: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    endpoint: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__503deb88a5ef8d0c98a00f32a1081bde39ecb72372c34b6333a163ccb0ef81ed(
    *,
    account_id: typing.Optional[builtins.str] = None,
    endpoint: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8009d5c8e99a749acb046b3d08e0b1855ef3cdfec51f63cfbcd4f63e96682df(
    *,
    description: typing.Optional[builtins.str] = None,
    enable_webhook_updates: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    endpoint: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__650e48ec479e7a1b9064d59e020e37c2dc46ce45a4ca814e465d16a775c3ad5c(
    *,
    aws: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAssociationPropsMixin.AWSConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dynatrace: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAssociationPropsMixin.DynatraceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    event_channel: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAssociationPropsMixin.EventChannelConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    git_hub: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAssociationPropsMixin.GitHubConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    git_lab: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAssociationPropsMixin.GitLabConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    mcp_server: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAssociationPropsMixin.MCPServerConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    mcp_server_datadog: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAssociationPropsMixin.MCPServerDatadogConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    mcp_server_new_relic: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAssociationPropsMixin.MCPServerNewRelicConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    mcp_server_splunk: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAssociationPropsMixin.MCPServerSplunkConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    service_now: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAssociationPropsMixin.ServiceNowConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    slack: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAssociationPropsMixin.SlackConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    source_aws: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAssociationPropsMixin.SourceAwsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49dca394a6843a10955f8dff9541736e68d7a79ce88ec00b20d3e1faa58f23fa(
    *,
    enable_webhook_updates: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    instance_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30e2f3214ed4292c323738dd466e7f88ea6115602eb6fa37027e341b026d0c4f(
    *,
    channel_id: typing.Optional[builtins.str] = None,
    channel_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__160f70183a32c38a04104c4bab976707cfcabfa49c29b609fa3ca22092d72570(
    *,
    transmission_target: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAssociationPropsMixin.SlackTransmissionTargetProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    workspace_id: typing.Optional[builtins.str] = None,
    workspace_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa95e7f44c940b8ede0b37995d7403b2401dab1e7c4bab1a4dcb16c9450f3ce8(
    *,
    incident_response_target: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAssociationPropsMixin.SlackChannelProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b80beab9a8ab2549cc9c140f097f3b6623b631007f54fe44a6c9a676bdb8242b(
    *,
    account_id: typing.Optional[builtins.str] = None,
    account_type: typing.Optional[builtins.str] = None,
    assumable_role_arn: typing.Optional[builtins.str] = None,
    resources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAssociationPropsMixin.AWSResourceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnAssociationPropsMixin.KeyValuePairProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
