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
    jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnAgentMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "activation_key": "activationKey",
        "agent_name": "agentName",
        "security_group_arns": "securityGroupArns",
        "subnet_arns": "subnetArns",
        "tags": "tags",
        "vpc_endpoint_id": "vpcEndpointId",
    },
)
class CfnAgentMixinProps:
    def __init__(
        self,
        *,
        activation_key: typing.Optional[builtins.str] = None,
        agent_name: typing.Optional[builtins.str] = None,
        security_group_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_endpoint_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnAgentPropsMixin.

        :param activation_key: Specifies your DataSync agent's activation key. If you don't have an activation key, see `Activating your agent <https://docs.aws.amazon.com/datasync/latest/userguide/activate-agent.html>`_ .
        :param agent_name: Specifies a name for your agent. We recommend specifying a name that you can remember.
        :param security_group_arns: The Amazon Resource Names (ARNs) of the security groups used to protect your data transfer task subnets. See `SecurityGroupArns <https://docs.aws.amazon.com/datasync/latest/userguide/API_Ec2Config.html#DataSync-Type-Ec2Config-SecurityGroupArns>`_ . *Pattern* : ``^arn:(aws|aws-cn|aws-us-gov|aws-iso|aws-iso-b):ec2:[a-z\\-0-9]*:[0-9]{12}:security-group/.*$``
        :param subnet_arns: Specifies the ARN of the subnet where your VPC service endpoint is located. You can only specify one ARN.
        :param tags: Specifies labels that help you categorize, filter, and search for your AWS resources. We recommend creating at least one tag for your agent.
        :param vpc_endpoint_id: The ID of the virtual private cloud (VPC) endpoint that the agent has access to. This is the client-side VPC endpoint, powered by AWS PrivateLink . If you don't have an AWS PrivateLink VPC endpoint, see `AWS PrivateLink and VPC endpoints <https://docs.aws.amazon.com//vpc/latest/userguide/endpoint-services-overview.html>`_ in the *Amazon VPC User Guide* . For more information about activating your agent in a private network based on a VPC, see `Using AWS DataSync in a Virtual Private Cloud <https://docs.aws.amazon.com/datasync/latest/userguide/datasync-in-vpc.html>`_ in the *AWS DataSync User Guide.* A VPC endpoint ID looks like this: ``vpce-01234d5aff67890e1`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-agent.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
            
            cfn_agent_mixin_props = datasync_mixins.CfnAgentMixinProps(
                activation_key="activationKey",
                agent_name="agentName",
                security_group_arns=["securityGroupArns"],
                subnet_arns=["subnetArns"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vpc_endpoint_id="vpcEndpointId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d7d4b26d9f158899fae559f9c890079968a2368d819b5bd1dd4438329578ab4)
            check_type(argname="argument activation_key", value=activation_key, expected_type=type_hints["activation_key"])
            check_type(argname="argument agent_name", value=agent_name, expected_type=type_hints["agent_name"])
            check_type(argname="argument security_group_arns", value=security_group_arns, expected_type=type_hints["security_group_arns"])
            check_type(argname="argument subnet_arns", value=subnet_arns, expected_type=type_hints["subnet_arns"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc_endpoint_id", value=vpc_endpoint_id, expected_type=type_hints["vpc_endpoint_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if activation_key is not None:
            self._values["activation_key"] = activation_key
        if agent_name is not None:
            self._values["agent_name"] = agent_name
        if security_group_arns is not None:
            self._values["security_group_arns"] = security_group_arns
        if subnet_arns is not None:
            self._values["subnet_arns"] = subnet_arns
        if tags is not None:
            self._values["tags"] = tags
        if vpc_endpoint_id is not None:
            self._values["vpc_endpoint_id"] = vpc_endpoint_id

    @builtins.property
    def activation_key(self) -> typing.Optional[builtins.str]:
        '''Specifies your DataSync agent's activation key.

        If you don't have an activation key, see `Activating your agent <https://docs.aws.amazon.com/datasync/latest/userguide/activate-agent.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-agent.html#cfn-datasync-agent-activationkey
        '''
        result = self._values.get("activation_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def agent_name(self) -> typing.Optional[builtins.str]:
        '''Specifies a name for your agent.

        We recommend specifying a name that you can remember.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-agent.html#cfn-datasync-agent-agentname
        '''
        result = self._values.get("agent_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_group_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Amazon Resource Names (ARNs) of the security groups used to protect your data transfer task subnets.

        See `SecurityGroupArns <https://docs.aws.amazon.com/datasync/latest/userguide/API_Ec2Config.html#DataSync-Type-Ec2Config-SecurityGroupArns>`_ .

        *Pattern* : ``^arn:(aws|aws-cn|aws-us-gov|aws-iso|aws-iso-b):ec2:[a-z\\-0-9]*:[0-9]{12}:security-group/.*$``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-agent.html#cfn-datasync-agent-securitygrouparns
        '''
        result = self._values.get("security_group_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnet_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the ARN of the subnet where your VPC service endpoint is located.

        You can only specify one ARN.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-agent.html#cfn-datasync-agent-subnetarns
        '''
        result = self._values.get("subnet_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Specifies labels that help you categorize, filter, and search for your AWS resources.

        We recommend creating at least one tag for your agent.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-agent.html#cfn-datasync-agent-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def vpc_endpoint_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the virtual private cloud (VPC) endpoint that the agent has access to.

        This is the client-side VPC endpoint, powered by AWS PrivateLink . If you don't have an AWS PrivateLink VPC endpoint, see `AWS PrivateLink and VPC endpoints <https://docs.aws.amazon.com//vpc/latest/userguide/endpoint-services-overview.html>`_ in the *Amazon VPC User Guide* .

        For more information about activating your agent in a private network based on a VPC, see `Using AWS DataSync in a Virtual Private Cloud <https://docs.aws.amazon.com/datasync/latest/userguide/datasync-in-vpc.html>`_ in the *AWS DataSync User Guide.*

        A VPC endpoint ID looks like this: ``vpce-01234d5aff67890e1`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-agent.html#cfn-datasync-agent-vpcendpointid
        '''
        result = self._values.get("vpc_endpoint_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAgentMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAgentPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnAgentPropsMixin",
):
    '''The ``AWS::DataSync::Agent`` resource activates an AWS DataSync agent that you've deployed for storage discovery or data transfers.

    The activation process associates the agent with your AWS account .

    For more information, see the following topics in the *AWS DataSync User Guide* :

    - `DataSync agent requirements <https://docs.aws.amazon.com/datasync/latest/userguide/agent-requirements.html>`_
    - `DataSync network requirements <https://docs.aws.amazon.com/datasync/latest/userguide/datasync-network.html>`_
    - `Create a DataSync agent <https://docs.aws.amazon.com/datasync/latest/userguide/configure-agent.html>`_

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-agent.html
    :cloudformationResource: AWS::DataSync::Agent
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
        
        cfn_agent_props_mixin = datasync_mixins.CfnAgentPropsMixin(datasync_mixins.CfnAgentMixinProps(
            activation_key="activationKey",
            agent_name="agentName",
            security_group_arns=["securityGroupArns"],
            subnet_arns=["subnetArns"],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            vpc_endpoint_id="vpcEndpointId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAgentMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DataSync::Agent``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a65940522089a7f8ef836f336e68c65f01eedba3e7ed01a6c520643b49ea42e0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__41600be1a89df94cc8258d7690a94d0f560bca09f64b341210bcfeba419435ad)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a2012611f3af3dd0317a80564291068f63274a325d3049bd456418ff29c34a6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAgentMixinProps:
        return typing.cast(CfnAgentMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationAzureBlobMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "agent_arns": "agentArns",
        "azure_access_tier": "azureAccessTier",
        "azure_blob_authentication_type": "azureBlobAuthenticationType",
        "azure_blob_container_url": "azureBlobContainerUrl",
        "azure_blob_sas_configuration": "azureBlobSasConfiguration",
        "azure_blob_type": "azureBlobType",
        "cmk_secret_config": "cmkSecretConfig",
        "custom_secret_config": "customSecretConfig",
        "subdirectory": "subdirectory",
        "tags": "tags",
    },
)
class CfnLocationAzureBlobMixinProps:
    def __init__(
        self,
        *,
        agent_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        azure_access_tier: typing.Optional[builtins.str] = None,
        azure_blob_authentication_type: typing.Optional[builtins.str] = None,
        azure_blob_container_url: typing.Optional[builtins.str] = None,
        azure_blob_sas_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLocationAzureBlobPropsMixin.AzureBlobSasConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        azure_blob_type: typing.Optional[builtins.str] = None,
        cmk_secret_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLocationAzureBlobPropsMixin.CmkSecretConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        custom_secret_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLocationAzureBlobPropsMixin.CustomSecretConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnLocationAzureBlobPropsMixin.

        :param agent_arns: (Optional) Specifies the Amazon Resource Name (ARN) of the DataSync agent that can connect with your Azure Blob Storage container. If you are setting up an agentless cross-cloud transfer, you do not need to specify a value for this parameter. You can specify more than one agent. For more information, see `Using multiple agents for your transfer <https://docs.aws.amazon.com/datasync/latest/userguide/multiple-agents.html>`_ . .. epigraph:: Make sure you configure this parameter correctly when you first create your storage location. You cannot add or remove agents from a storage location after you create it.
        :param azure_access_tier: Specifies the access tier that you want your objects or files transferred into. This only applies when using the location as a transfer destination. For more information, see `Access tiers <https://docs.aws.amazon.com/datasync/latest/userguide/creating-azure-blob-location.html#azure-blob-access-tiers>`_ . Default: - "HOT"
        :param azure_blob_authentication_type: Specifies the authentication method DataSync uses to access your Azure Blob Storage. DataSync can access blob storage using a shared access signature (SAS). Default: - "SAS"
        :param azure_blob_container_url: Specifies the URL of the Azure Blob Storage container involved in your transfer.
        :param azure_blob_sas_configuration: Specifies the SAS configuration that allows DataSync to access your Azure Blob Storage. .. epigraph:: If you provide an authentication token using ``SasConfiguration`` , but do not provide secret configuration details using ``CmkSecretConfig`` or ``CustomSecretConfig`` , then DataSync stores the token using your AWS account's secrets manager secret.
        :param azure_blob_type: Specifies the type of blob that you want your objects or files to be when transferring them into Azure Blob Storage. Currently, DataSync only supports moving data into Azure Blob Storage as block blobs. For more information on blob types, see the `Azure Blob Storage documentation <https://docs.aws.amazon.com/https://learn.microsoft.com/en-us/rest/api/storageservices/understanding-block-blobs--append-blobs--and-page-blobs>`_ . Default: - "BLOCK"
        :param cmk_secret_config: Specifies configuration information for a DataSync-managed secret, such as an authentication token or secret key that DataSync uses to access a specific storage location, with a customer-managed AWS KMS key . .. epigraph:: You can use either ``CmkSecretConfig`` or ``CustomSecretConfig`` to provide credentials for a ``CreateLocation`` request. Do not provide both parameters for the same request.
        :param custom_secret_config: Specifies configuration information for a customer-managed Secrets Manager secret where a storage location authentication token or secret key is stored in plain text. This configuration includes the secret ARN, and the ARN for an IAM role that provides access to the secret. .. epigraph:: You can use either ``CmkSecretConfig`` or ``CustomSecretConfig`` to provide credentials for a ``CreateLocation`` request. Do not provide both parameters for the same request.
        :param subdirectory: Specifies path segments if you want to limit your transfer to a virtual directory in your container (for example, ``/my/images`` ).
        :param tags: Specifies labels that help you categorize, filter, and search for your AWS resources. We recommend creating at least a name tag for your transfer location.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationazureblob.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
            
            cfn_location_azure_blob_mixin_props = datasync_mixins.CfnLocationAzureBlobMixinProps(
                agent_arns=["agentArns"],
                azure_access_tier="azureAccessTier",
                azure_blob_authentication_type="azureBlobAuthenticationType",
                azure_blob_container_url="azureBlobContainerUrl",
                azure_blob_sas_configuration=datasync_mixins.CfnLocationAzureBlobPropsMixin.AzureBlobSasConfigurationProperty(
                    azure_blob_sas_token="azureBlobSasToken"
                ),
                azure_blob_type="azureBlobType",
                cmk_secret_config=datasync_mixins.CfnLocationAzureBlobPropsMixin.CmkSecretConfigProperty(
                    kms_key_arn="kmsKeyArn",
                    secret_arn="secretArn"
                ),
                custom_secret_config=datasync_mixins.CfnLocationAzureBlobPropsMixin.CustomSecretConfigProperty(
                    secret_access_role_arn="secretAccessRoleArn",
                    secret_arn="secretArn"
                ),
                subdirectory="subdirectory",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67951bcbec4c86da66984ecc87e648fea5ab58f81cd3b5d7d2d9679b6fb288c3)
            check_type(argname="argument agent_arns", value=agent_arns, expected_type=type_hints["agent_arns"])
            check_type(argname="argument azure_access_tier", value=azure_access_tier, expected_type=type_hints["azure_access_tier"])
            check_type(argname="argument azure_blob_authentication_type", value=azure_blob_authentication_type, expected_type=type_hints["azure_blob_authentication_type"])
            check_type(argname="argument azure_blob_container_url", value=azure_blob_container_url, expected_type=type_hints["azure_blob_container_url"])
            check_type(argname="argument azure_blob_sas_configuration", value=azure_blob_sas_configuration, expected_type=type_hints["azure_blob_sas_configuration"])
            check_type(argname="argument azure_blob_type", value=azure_blob_type, expected_type=type_hints["azure_blob_type"])
            check_type(argname="argument cmk_secret_config", value=cmk_secret_config, expected_type=type_hints["cmk_secret_config"])
            check_type(argname="argument custom_secret_config", value=custom_secret_config, expected_type=type_hints["custom_secret_config"])
            check_type(argname="argument subdirectory", value=subdirectory, expected_type=type_hints["subdirectory"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if agent_arns is not None:
            self._values["agent_arns"] = agent_arns
        if azure_access_tier is not None:
            self._values["azure_access_tier"] = azure_access_tier
        if azure_blob_authentication_type is not None:
            self._values["azure_blob_authentication_type"] = azure_blob_authentication_type
        if azure_blob_container_url is not None:
            self._values["azure_blob_container_url"] = azure_blob_container_url
        if azure_blob_sas_configuration is not None:
            self._values["azure_blob_sas_configuration"] = azure_blob_sas_configuration
        if azure_blob_type is not None:
            self._values["azure_blob_type"] = azure_blob_type
        if cmk_secret_config is not None:
            self._values["cmk_secret_config"] = cmk_secret_config
        if custom_secret_config is not None:
            self._values["custom_secret_config"] = custom_secret_config
        if subdirectory is not None:
            self._values["subdirectory"] = subdirectory
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def agent_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(Optional) Specifies the Amazon Resource Name (ARN) of the DataSync agent that can connect with your Azure Blob Storage container.

        If you are setting up an agentless cross-cloud transfer, you do not need to specify a value for this parameter.

        You can specify more than one agent. For more information, see `Using multiple agents for your transfer <https://docs.aws.amazon.com/datasync/latest/userguide/multiple-agents.html>`_ .
        .. epigraph::

           Make sure you configure this parameter correctly when you first create your storage location. You cannot add or remove agents from a storage location after you create it.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationazureblob.html#cfn-datasync-locationazureblob-agentarns
        '''
        result = self._values.get("agent_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def azure_access_tier(self) -> typing.Optional[builtins.str]:
        '''Specifies the access tier that you want your objects or files transferred into.

        This only applies when using the location as a transfer destination. For more information, see `Access tiers <https://docs.aws.amazon.com/datasync/latest/userguide/creating-azure-blob-location.html#azure-blob-access-tiers>`_ .

        :default: - "HOT"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationazureblob.html#cfn-datasync-locationazureblob-azureaccesstier
        '''
        result = self._values.get("azure_access_tier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def azure_blob_authentication_type(self) -> typing.Optional[builtins.str]:
        '''Specifies the authentication method DataSync uses to access your Azure Blob Storage.

        DataSync can access blob storage using a shared access signature (SAS).

        :default: - "SAS"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationazureblob.html#cfn-datasync-locationazureblob-azureblobauthenticationtype
        '''
        result = self._values.get("azure_blob_authentication_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def azure_blob_container_url(self) -> typing.Optional[builtins.str]:
        '''Specifies the URL of the Azure Blob Storage container involved in your transfer.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationazureblob.html#cfn-datasync-locationazureblob-azureblobcontainerurl
        '''
        result = self._values.get("azure_blob_container_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def azure_blob_sas_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLocationAzureBlobPropsMixin.AzureBlobSasConfigurationProperty"]]:
        '''Specifies the SAS configuration that allows DataSync to access your Azure Blob Storage.

        .. epigraph::

           If you provide an authentication token using ``SasConfiguration`` , but do not provide secret configuration details using ``CmkSecretConfig`` or ``CustomSecretConfig`` , then DataSync stores the token using your AWS account's secrets manager secret.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationazureblob.html#cfn-datasync-locationazureblob-azureblobsasconfiguration
        '''
        result = self._values.get("azure_blob_sas_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLocationAzureBlobPropsMixin.AzureBlobSasConfigurationProperty"]], result)

    @builtins.property
    def azure_blob_type(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of blob that you want your objects or files to be when transferring them into Azure Blob Storage.

        Currently, DataSync only supports moving data into Azure Blob Storage as block blobs. For more information on blob types, see the `Azure Blob Storage documentation <https://docs.aws.amazon.com/https://learn.microsoft.com/en-us/rest/api/storageservices/understanding-block-blobs--append-blobs--and-page-blobs>`_ .

        :default: - "BLOCK"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationazureblob.html#cfn-datasync-locationazureblob-azureblobtype
        '''
        result = self._values.get("azure_blob_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cmk_secret_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLocationAzureBlobPropsMixin.CmkSecretConfigProperty"]]:
        '''Specifies configuration information for a DataSync-managed secret, such as an authentication token or secret key that DataSync uses to access a specific storage location, with a customer-managed AWS KMS key .

        .. epigraph::

           You can use either ``CmkSecretConfig`` or ``CustomSecretConfig`` to provide credentials for a ``CreateLocation`` request. Do not provide both parameters for the same request.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationazureblob.html#cfn-datasync-locationazureblob-cmksecretconfig
        '''
        result = self._values.get("cmk_secret_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLocationAzureBlobPropsMixin.CmkSecretConfigProperty"]], result)

    @builtins.property
    def custom_secret_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLocationAzureBlobPropsMixin.CustomSecretConfigProperty"]]:
        '''Specifies configuration information for a customer-managed Secrets Manager secret where a storage location authentication token or secret key is stored in plain text.

        This configuration includes the secret ARN, and the ARN for an IAM role that provides access to the secret.
        .. epigraph::

           You can use either ``CmkSecretConfig`` or ``CustomSecretConfig`` to provide credentials for a ``CreateLocation`` request. Do not provide both parameters for the same request.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationazureblob.html#cfn-datasync-locationazureblob-customsecretconfig
        '''
        result = self._values.get("custom_secret_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLocationAzureBlobPropsMixin.CustomSecretConfigProperty"]], result)

    @builtins.property
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''Specifies path segments if you want to limit your transfer to a virtual directory in your container (for example, ``/my/images`` ).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationazureblob.html#cfn-datasync-locationazureblob-subdirectory
        '''
        result = self._values.get("subdirectory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Specifies labels that help you categorize, filter, and search for your AWS resources.

        We recommend creating at least a name tag for your transfer location.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationazureblob.html#cfn-datasync-locationazureblob-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLocationAzureBlobMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLocationAzureBlobPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationAzureBlobPropsMixin",
):
    '''Creates a transfer *location* for a Microsoft Azure Blob Storage container.

    AWS DataSync can use this location as a transfer source or destination. You can make transfers with or without a `DataSync agent <https://docs.aws.amazon.com/datasync/latest/userguide/creating-azure-blob-location.html#azure-blob-creating-agent>`_ that connects to your container.

    Before you begin, make sure you know `how DataSync accesses Azure Blob Storage <https://docs.aws.amazon.com/datasync/latest/userguide/creating-azure-blob-location.html#azure-blob-access>`_ and works with `access tiers <https://docs.aws.amazon.com/datasync/latest/userguide/creating-azure-blob-location.html#azure-blob-access-tiers>`_ and `blob types <https://docs.aws.amazon.com/datasync/latest/userguide/creating-azure-blob-location.html#blob-types>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationazureblob.html
    :cloudformationResource: AWS::DataSync::LocationAzureBlob
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
        
        cfn_location_azure_blob_props_mixin = datasync_mixins.CfnLocationAzureBlobPropsMixin(datasync_mixins.CfnLocationAzureBlobMixinProps(
            agent_arns=["agentArns"],
            azure_access_tier="azureAccessTier",
            azure_blob_authentication_type="azureBlobAuthenticationType",
            azure_blob_container_url="azureBlobContainerUrl",
            azure_blob_sas_configuration=datasync_mixins.CfnLocationAzureBlobPropsMixin.AzureBlobSasConfigurationProperty(
                azure_blob_sas_token="azureBlobSasToken"
            ),
            azure_blob_type="azureBlobType",
            cmk_secret_config=datasync_mixins.CfnLocationAzureBlobPropsMixin.CmkSecretConfigProperty(
                kms_key_arn="kmsKeyArn",
                secret_arn="secretArn"
            ),
            custom_secret_config=datasync_mixins.CfnLocationAzureBlobPropsMixin.CustomSecretConfigProperty(
                secret_access_role_arn="secretAccessRoleArn",
                secret_arn="secretArn"
            ),
            subdirectory="subdirectory",
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
        props: typing.Union[CfnLocationAzureBlobMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DataSync::LocationAzureBlob``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfe247a39ab08b5fb90c9385c6e0eae46366bca760b52d4f73d35fa197cb05a2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7114695f5f2ec1586a6d1f27fafbf3dfe9d37e5a409b2af750d1528ffb70cb80)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1a61b7f591ecdd66d2670ca1e80f7f9f333ce2a255aa08c7693dcb34e32e148)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLocationAzureBlobMixinProps:
        return typing.cast(CfnLocationAzureBlobMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationAzureBlobPropsMixin.AzureBlobSasConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"azure_blob_sas_token": "azureBlobSasToken"},
    )
    class AzureBlobSasConfigurationProperty:
        def __init__(
            self,
            *,
            azure_blob_sas_token: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The shared access signature (SAS) configuration that allows AWS DataSync to access your Microsoft Azure Blob Storage.

            For more information, see `SAS tokens <https://docs.aws.amazon.com/datasync/latest/userguide/creating-azure-blob-location.html#azure-blob-sas-tokens>`_ for accessing your Azure Blob Storage.

            :param azure_blob_sas_token: Specifies a SAS token that provides permissions to access your Azure Blob Storage. The token is part of the SAS URI string that comes after the storage resource URI and a question mark. A token looks something like this: ``sp=r&st=2023-12-20T14:54:52Z&se=2023-12-20T22:54:52Z&spr=https&sv=2021-06-08&sr=c&sig=aBBKDWQvyuVcTPH9EBp%2FXTI9E%2F%2Fmq171%2BZU178wcwqU%3D``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationazureblob-azureblobsasconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
                
                azure_blob_sas_configuration_property = datasync_mixins.CfnLocationAzureBlobPropsMixin.AzureBlobSasConfigurationProperty(
                    azure_blob_sas_token="azureBlobSasToken"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__14518bd8f202346c76820b9c4d27950d9a4e5fb259be0e26bdfec531651fec50)
                check_type(argname="argument azure_blob_sas_token", value=azure_blob_sas_token, expected_type=type_hints["azure_blob_sas_token"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if azure_blob_sas_token is not None:
                self._values["azure_blob_sas_token"] = azure_blob_sas_token

        @builtins.property
        def azure_blob_sas_token(self) -> typing.Optional[builtins.str]:
            '''Specifies a SAS token that provides permissions to access your Azure Blob Storage.

            The token is part of the SAS URI string that comes after the storage resource URI and a question mark. A token looks something like this:

            ``sp=r&st=2023-12-20T14:54:52Z&se=2023-12-20T22:54:52Z&spr=https&sv=2021-06-08&sr=c&sig=aBBKDWQvyuVcTPH9EBp%2FXTI9E%2F%2Fmq171%2BZU178wcwqU%3D``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationazureblob-azureblobsasconfiguration.html#cfn-datasync-locationazureblob-azureblobsasconfiguration-azureblobsastoken
            '''
            result = self._values.get("azure_blob_sas_token")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AzureBlobSasConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationAzureBlobPropsMixin.CmkSecretConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"kms_key_arn": "kmsKeyArn", "secret_arn": "secretArn"},
    )
    class CmkSecretConfigProperty:
        def __init__(
            self,
            *,
            kms_key_arn: typing.Optional[builtins.str] = None,
            secret_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies configuration information for a DataSync-managed secret, such as an authentication token or secret key that DataSync uses to access a specific storage location, with a customer-managed AWS KMS key .

            .. epigraph::

               You can use either ``CmkSecretConfig`` or ``CustomSecretConfig`` to provide credentials for a ``CreateLocation`` request. Do not provide both parameters for the same request.

            :param kms_key_arn: Specifies the ARN for the customer-managed AWS KMS key that DataSync uses to encrypt the DataSync-managed secret stored for ``SecretArn`` . DataSync provides this key to AWS Secrets Manager .
            :param secret_arn: Specifies the ARN for the DataSync-managed AWS Secrets Manager secret that that is used to access a specific storage location. This property is generated by DataSync and is read-only. DataSync encrypts this secret with the KMS key that you specify for ``KmsKeyArn`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationazureblob-cmksecretconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
                
                cmk_secret_config_property = datasync_mixins.CfnLocationAzureBlobPropsMixin.CmkSecretConfigProperty(
                    kms_key_arn="kmsKeyArn",
                    secret_arn="secretArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1b09e2923bcb8a00a6809a590350ccd7934e31670599d7cf878c47947d6049f4)
                check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kms_key_arn is not None:
                self._values["kms_key_arn"] = kms_key_arn
            if secret_arn is not None:
                self._values["secret_arn"] = secret_arn

        @builtins.property
        def kms_key_arn(self) -> typing.Optional[builtins.str]:
            '''Specifies the ARN for the customer-managed AWS KMS key that DataSync uses to encrypt the DataSync-managed secret stored for ``SecretArn`` .

            DataSync provides this key to AWS Secrets Manager .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationazureblob-cmksecretconfig.html#cfn-datasync-locationazureblob-cmksecretconfig-kmskeyarn
            '''
            result = self._values.get("kms_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secret_arn(self) -> typing.Optional[builtins.str]:
            '''Specifies the ARN for the DataSync-managed AWS Secrets Manager secret that that is used to access a specific storage location.

            This property is generated by DataSync and is read-only. DataSync encrypts this secret with the KMS key that you specify for ``KmsKeyArn`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationazureblob-cmksecretconfig.html#cfn-datasync-locationazureblob-cmksecretconfig-secretarn
            '''
            result = self._values.get("secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CmkSecretConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationAzureBlobPropsMixin.CustomSecretConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "secret_access_role_arn": "secretAccessRoleArn",
            "secret_arn": "secretArn",
        },
    )
    class CustomSecretConfigProperty:
        def __init__(
            self,
            *,
            secret_access_role_arn: typing.Optional[builtins.str] = None,
            secret_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies configuration information for a customer-managed Secrets Manager secret where a storage location authentication token or secret key is stored in plain text.

            This configuration includes the secret ARN, and the ARN for an IAM role that provides access to the secret.
            .. epigraph::

               You can use either ``CmkSecretConfig`` or ``CustomSecretConfig`` to provide credentials for a ``CreateLocation`` request. Do not provide both parameters for the same request.

            :param secret_access_role_arn: Specifies the ARN for the AWS Identity and Access Management role that DataSync uses to access the secret specified for ``SecretArn`` .
            :param secret_arn: Specifies the ARN for an AWS Secrets Manager secret.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationazureblob-customsecretconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
                
                custom_secret_config_property = datasync_mixins.CfnLocationAzureBlobPropsMixin.CustomSecretConfigProperty(
                    secret_access_role_arn="secretAccessRoleArn",
                    secret_arn="secretArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4dce7e81c193e9850efff4f58f2722c7eaf9354512cd8da636cb8e9236e39b6b)
                check_type(argname="argument secret_access_role_arn", value=secret_access_role_arn, expected_type=type_hints["secret_access_role_arn"])
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if secret_access_role_arn is not None:
                self._values["secret_access_role_arn"] = secret_access_role_arn
            if secret_arn is not None:
                self._values["secret_arn"] = secret_arn

        @builtins.property
        def secret_access_role_arn(self) -> typing.Optional[builtins.str]:
            '''Specifies the ARN for the AWS Identity and Access Management role that DataSync uses to access the secret specified for ``SecretArn`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationazureblob-customsecretconfig.html#cfn-datasync-locationazureblob-customsecretconfig-secretaccessrolearn
            '''
            result = self._values.get("secret_access_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secret_arn(self) -> typing.Optional[builtins.str]:
            '''Specifies the ARN for an AWS Secrets Manager secret.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationazureblob-customsecretconfig.html#cfn-datasync-locationazureblob-customsecretconfig-secretarn
            '''
            result = self._values.get("secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomSecretConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationAzureBlobPropsMixin.ManagedSecretConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"secret_arn": "secretArn"},
    )
    class ManagedSecretConfigProperty:
        def __init__(self, *, secret_arn: typing.Optional[builtins.str] = None) -> None:
            '''Specifies configuration information for a DataSync-managed secret, such as an authentication token or set of credentials that DataSync uses to access a specific transfer location.

            DataSync uses the default AWS -managed KMS key to encrypt this secret in AWS Secrets Manager .

            :param secret_arn: Specifies the ARN for an AWS Secrets Manager secret.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationazureblob-managedsecretconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
                
                managed_secret_config_property = datasync_mixins.CfnLocationAzureBlobPropsMixin.ManagedSecretConfigProperty(
                    secret_arn="secretArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2aa1625ab26252b7cf9ec933c9cb0688cfa2ed9c0944add4299eceb38ad7fefa)
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if secret_arn is not None:
                self._values["secret_arn"] = secret_arn

        @builtins.property
        def secret_arn(self) -> typing.Optional[builtins.str]:
            '''Specifies the ARN for an AWS Secrets Manager secret.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationazureblob-managedsecretconfig.html#cfn-datasync-locationazureblob-managedsecretconfig-secretarn
            '''
            result = self._values.get("secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ManagedSecretConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationEFSMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_point_arn": "accessPointArn",
        "ec2_config": "ec2Config",
        "efs_filesystem_arn": "efsFilesystemArn",
        "file_system_access_role_arn": "fileSystemAccessRoleArn",
        "in_transit_encryption": "inTransitEncryption",
        "subdirectory": "subdirectory",
        "tags": "tags",
    },
)
class CfnLocationEFSMixinProps:
    def __init__(
        self,
        *,
        access_point_arn: typing.Optional[builtins.str] = None,
        ec2_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLocationEFSPropsMixin.Ec2ConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        efs_filesystem_arn: typing.Optional[builtins.str] = None,
        file_system_access_role_arn: typing.Optional[builtins.str] = None,
        in_transit_encryption: typing.Optional[builtins.str] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnLocationEFSPropsMixin.

        :param access_point_arn: Specifies the Amazon Resource Name (ARN) of the access point that DataSync uses to mount your Amazon EFS file system. For more information, see `Accessing restricted file systems <https://docs.aws.amazon.com/datasync/latest/userguide/create-efs-location.html#create-efs-location-iam>`_ .
        :param ec2_config: Specifies the subnet and security groups DataSync uses to connect to one of your Amazon EFS file system's `mount targets <https://docs.aws.amazon.com/efs/latest/ug/accessing-fs.html>`_ .
        :param efs_filesystem_arn: Specifies the ARN for your Amazon EFS file system.
        :param file_system_access_role_arn: Specifies an AWS Identity and Access Management (IAM) role that allows DataSync to access your Amazon EFS file system. For information on creating this role, see `Creating a DataSync IAM role for file system access <https://docs.aws.amazon.com/datasync/latest/userguide/create-efs-location.html#create-efs-location-iam-role>`_ .
        :param in_transit_encryption: Specifies whether you want DataSync to use Transport Layer Security (TLS) 1.2 encryption when it transfers data to or from your Amazon EFS file system. If you specify an access point using ``AccessPointArn`` or an IAM role using ``FileSystemAccessRoleArn`` , you must set this parameter to ``TLS1_2`` .
        :param subdirectory: Specifies a mount path for your Amazon EFS file system. This is where DataSync reads or writes data on your file system (depending on if this is a source or destination location). By default, DataSync uses the root directory (or `access point <https://docs.aws.amazon.com/efs/latest/ug/efs-access-points.html>`_ if you provide one by using ``AccessPointArn`` ). You can also include subdirectories using forward slashes (for example, ``/path/to/folder`` ).
        :param tags: Specifies the key-value pair that represents a tag that you want to add to the resource. The value can be an empty string. This value helps you manage, filter, and search for your resources. We recommend that you create a name tag for your location.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationefs.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
            
            cfn_location_eFSMixin_props = datasync_mixins.CfnLocationEFSMixinProps(
                access_point_arn="accessPointArn",
                ec2_config=datasync_mixins.CfnLocationEFSPropsMixin.Ec2ConfigProperty(
                    security_group_arns=["securityGroupArns"],
                    subnet_arn="subnetArn"
                ),
                efs_filesystem_arn="efsFilesystemArn",
                file_system_access_role_arn="fileSystemAccessRoleArn",
                in_transit_encryption="inTransitEncryption",
                subdirectory="subdirectory",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae34944de38d87d1b06e65c9cc28e881fcbf025a9a2fc9f01d59d6a1a5e102e2)
            check_type(argname="argument access_point_arn", value=access_point_arn, expected_type=type_hints["access_point_arn"])
            check_type(argname="argument ec2_config", value=ec2_config, expected_type=type_hints["ec2_config"])
            check_type(argname="argument efs_filesystem_arn", value=efs_filesystem_arn, expected_type=type_hints["efs_filesystem_arn"])
            check_type(argname="argument file_system_access_role_arn", value=file_system_access_role_arn, expected_type=type_hints["file_system_access_role_arn"])
            check_type(argname="argument in_transit_encryption", value=in_transit_encryption, expected_type=type_hints["in_transit_encryption"])
            check_type(argname="argument subdirectory", value=subdirectory, expected_type=type_hints["subdirectory"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_point_arn is not None:
            self._values["access_point_arn"] = access_point_arn
        if ec2_config is not None:
            self._values["ec2_config"] = ec2_config
        if efs_filesystem_arn is not None:
            self._values["efs_filesystem_arn"] = efs_filesystem_arn
        if file_system_access_role_arn is not None:
            self._values["file_system_access_role_arn"] = file_system_access_role_arn
        if in_transit_encryption is not None:
            self._values["in_transit_encryption"] = in_transit_encryption
        if subdirectory is not None:
            self._values["subdirectory"] = subdirectory
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def access_point_arn(self) -> typing.Optional[builtins.str]:
        '''Specifies the Amazon Resource Name (ARN) of the access point that DataSync uses to mount your Amazon EFS file system.

        For more information, see `Accessing restricted file systems <https://docs.aws.amazon.com/datasync/latest/userguide/create-efs-location.html#create-efs-location-iam>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationefs.html#cfn-datasync-locationefs-accesspointarn
        '''
        result = self._values.get("access_point_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ec2_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLocationEFSPropsMixin.Ec2ConfigProperty"]]:
        '''Specifies the subnet and security groups DataSync uses to connect to one of your Amazon EFS file system's `mount targets <https://docs.aws.amazon.com/efs/latest/ug/accessing-fs.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationefs.html#cfn-datasync-locationefs-ec2config
        '''
        result = self._values.get("ec2_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLocationEFSPropsMixin.Ec2ConfigProperty"]], result)

    @builtins.property
    def efs_filesystem_arn(self) -> typing.Optional[builtins.str]:
        '''Specifies the ARN for your Amazon EFS file system.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationefs.html#cfn-datasync-locationefs-efsfilesystemarn
        '''
        result = self._values.get("efs_filesystem_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_system_access_role_arn(self) -> typing.Optional[builtins.str]:
        '''Specifies an AWS Identity and Access Management (IAM) role that allows DataSync to access your Amazon EFS file system.

        For information on creating this role, see `Creating a DataSync IAM role for file system access <https://docs.aws.amazon.com/datasync/latest/userguide/create-efs-location.html#create-efs-location-iam-role>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationefs.html#cfn-datasync-locationefs-filesystemaccessrolearn
        '''
        result = self._values.get("file_system_access_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def in_transit_encryption(self) -> typing.Optional[builtins.str]:
        '''Specifies whether you want DataSync to use Transport Layer Security (TLS) 1.2 encryption when it transfers data to or from your Amazon EFS file system.

        If you specify an access point using ``AccessPointArn`` or an IAM role using ``FileSystemAccessRoleArn`` , you must set this parameter to ``TLS1_2`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationefs.html#cfn-datasync-locationefs-intransitencryption
        '''
        result = self._values.get("in_transit_encryption")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''Specifies a mount path for your Amazon EFS file system.

        This is where DataSync reads or writes data on your file system (depending on if this is a source or destination location).

        By default, DataSync uses the root directory (or `access point <https://docs.aws.amazon.com/efs/latest/ug/efs-access-points.html>`_ if you provide one by using ``AccessPointArn`` ). You can also include subdirectories using forward slashes (for example, ``/path/to/folder`` ).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationefs.html#cfn-datasync-locationefs-subdirectory
        '''
        result = self._values.get("subdirectory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Specifies the key-value pair that represents a tag that you want to add to the resource.

        The value can be an empty string. This value helps you manage, filter, and search for your resources. We recommend that you create a name tag for your location.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationefs.html#cfn-datasync-locationefs-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLocationEFSMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLocationEFSPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationEFSPropsMixin",
):
    '''The ``AWS::DataSync::LocationEFS`` resource creates an endpoint for an Amazon EFS file system.

    AWS DataSync can access this endpoint as a source or destination location.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationefs.html
    :cloudformationResource: AWS::DataSync::LocationEFS
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
        
        cfn_location_eFSProps_mixin = datasync_mixins.CfnLocationEFSPropsMixin(datasync_mixins.CfnLocationEFSMixinProps(
            access_point_arn="accessPointArn",
            ec2_config=datasync_mixins.CfnLocationEFSPropsMixin.Ec2ConfigProperty(
                security_group_arns=["securityGroupArns"],
                subnet_arn="subnetArn"
            ),
            efs_filesystem_arn="efsFilesystemArn",
            file_system_access_role_arn="fileSystemAccessRoleArn",
            in_transit_encryption="inTransitEncryption",
            subdirectory="subdirectory",
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
        props: typing.Union[CfnLocationEFSMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DataSync::LocationEFS``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__573d52c7904564165bbd3df6d0f54e94cc70fbbbc2010d40e8ba2227d30e2b54)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b297a0b06bb833d04e972efc96ef19ec7969d712f36c40020f18258f93aca4f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__677566f29bc34951d9704c619bf330d64f8e1fd080a7404751d11ff2345228bb)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLocationEFSMixinProps:
        return typing.cast(CfnLocationEFSMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationEFSPropsMixin.Ec2ConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "security_group_arns": "securityGroupArns",
            "subnet_arn": "subnetArn",
        },
    )
    class Ec2ConfigProperty:
        def __init__(
            self,
            *,
            security_group_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnet_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The subnet and security groups that AWS DataSync uses to connect to one of your Amazon EFS file system's `mount targets <https://docs.aws.amazon.com/efs/latest/ug/accessing-fs.html>`_ .

            :param security_group_arns: Specifies the Amazon Resource Names (ARNs) of the security groups associated with an Amazon EFS file system's mount target.
            :param subnet_arn: Specifies the ARN of a subnet where DataSync creates the `network interfaces <https://docs.aws.amazon.com/datasync/latest/userguide/datasync-network.html#required-network-interfaces.html>`_ for managing traffic during your transfer. The subnet must be located: - In the same virtual private cloud (VPC) as the Amazon EFS file system. - In the same Availability Zone as at least one mount target for the Amazon EFS file system. .. epigraph:: You don't need to specify a subnet that includes a file system mount target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationefs-ec2config.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
                
                ec2_config_property = datasync_mixins.CfnLocationEFSPropsMixin.Ec2ConfigProperty(
                    security_group_arns=["securityGroupArns"],
                    subnet_arn="subnetArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3acf17eee817f4ce5fc3c2e9d9a2a64e626a3b78e0d1eb6763cfb259db839da7)
                check_type(argname="argument security_group_arns", value=security_group_arns, expected_type=type_hints["security_group_arns"])
                check_type(argname="argument subnet_arn", value=subnet_arn, expected_type=type_hints["subnet_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if security_group_arns is not None:
                self._values["security_group_arns"] = security_group_arns
            if subnet_arn is not None:
                self._values["subnet_arn"] = subnet_arn

        @builtins.property
        def security_group_arns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Specifies the Amazon Resource Names (ARNs) of the security groups associated with an Amazon EFS file system's mount target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationefs-ec2config.html#cfn-datasync-locationefs-ec2config-securitygrouparns
            '''
            result = self._values.get("security_group_arns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnet_arn(self) -> typing.Optional[builtins.str]:
            '''Specifies the ARN of a subnet where DataSync creates the `network interfaces <https://docs.aws.amazon.com/datasync/latest/userguide/datasync-network.html#required-network-interfaces.html>`_ for managing traffic during your transfer.

            The subnet must be located:

            - In the same virtual private cloud (VPC) as the Amazon EFS file system.
            - In the same Availability Zone as at least one mount target for the Amazon EFS file system.

            .. epigraph::

               You don't need to specify a subnet that includes a file system mount target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationefs-ec2config.html#cfn-datasync-locationefs-ec2config-subnetarn
            '''
            result = self._values.get("subnet_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "Ec2ConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationFSxLustreMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "fsx_filesystem_arn": "fsxFilesystemArn",
        "security_group_arns": "securityGroupArns",
        "subdirectory": "subdirectory",
        "tags": "tags",
    },
)
class CfnLocationFSxLustreMixinProps:
    def __init__(
        self,
        *,
        fsx_filesystem_arn: typing.Optional[builtins.str] = None,
        security_group_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnLocationFSxLustrePropsMixin.

        :param fsx_filesystem_arn: Specifies the Amazon Resource Name (ARN) of the FSx for Lustre file system.
        :param security_group_arns: The ARNs of the security groups that are used to configure the FSx for Lustre file system. *Pattern* : ``^arn:(aws|aws-cn|aws-us-gov|aws-iso|aws-iso-b):ec2:[a-z\\-0-9]*:[0-9]{12}:security-group/.*$`` *Length constraints* : Maximum length of 128.
        :param subdirectory: Specifies a mount path for your FSx for Lustre file system. The path can include subdirectories. When the location is used as a source, DataSync reads data from the mount path. When the location is used as a destination, DataSync writes data to the mount path. If you don't include this parameter, DataSync uses the file system's root directory ( ``/`` ).
        :param tags: Specifies labels that help you categorize, filter, and search for your AWS resources. We recommend creating at least a name tag for your location.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxlustre.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
            
            cfn_location_fSx_lustre_mixin_props = datasync_mixins.CfnLocationFSxLustreMixinProps(
                fsx_filesystem_arn="fsxFilesystemArn",
                security_group_arns=["securityGroupArns"],
                subdirectory="subdirectory",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df6ff31826a0beb0cd1646320b66171d62ee204afe5d72676ff6cad6524d678e)
            check_type(argname="argument fsx_filesystem_arn", value=fsx_filesystem_arn, expected_type=type_hints["fsx_filesystem_arn"])
            check_type(argname="argument security_group_arns", value=security_group_arns, expected_type=type_hints["security_group_arns"])
            check_type(argname="argument subdirectory", value=subdirectory, expected_type=type_hints["subdirectory"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if fsx_filesystem_arn is not None:
            self._values["fsx_filesystem_arn"] = fsx_filesystem_arn
        if security_group_arns is not None:
            self._values["security_group_arns"] = security_group_arns
        if subdirectory is not None:
            self._values["subdirectory"] = subdirectory
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def fsx_filesystem_arn(self) -> typing.Optional[builtins.str]:
        '''Specifies the Amazon Resource Name (ARN) of the FSx for Lustre file system.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxlustre.html#cfn-datasync-locationfsxlustre-fsxfilesystemarn
        '''
        result = self._values.get("fsx_filesystem_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_group_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The ARNs of the security groups that are used to configure the FSx for Lustre file system.

        *Pattern* : ``^arn:(aws|aws-cn|aws-us-gov|aws-iso|aws-iso-b):ec2:[a-z\\-0-9]*:[0-9]{12}:security-group/.*$``

        *Length constraints* : Maximum length of 128.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxlustre.html#cfn-datasync-locationfsxlustre-securitygrouparns
        '''
        result = self._values.get("security_group_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''Specifies a mount path for your FSx for Lustre file system. The path can include subdirectories.

        When the location is used as a source, DataSync reads data from the mount path. When the location is used as a destination, DataSync writes data to the mount path. If you don't include this parameter, DataSync uses the file system's root directory ( ``/`` ).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxlustre.html#cfn-datasync-locationfsxlustre-subdirectory
        '''
        result = self._values.get("subdirectory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Specifies labels that help you categorize, filter, and search for your AWS resources.

        We recommend creating at least a name tag for your location.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxlustre.html#cfn-datasync-locationfsxlustre-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLocationFSxLustreMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLocationFSxLustrePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationFSxLustrePropsMixin",
):
    '''The ``AWS::DataSync::LocationFSxLustre`` resource specifies an endpoint for an Amazon FSx for Lustre file system.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxlustre.html
    :cloudformationResource: AWS::DataSync::LocationFSxLustre
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
        
        cfn_location_fSx_lustre_props_mixin = datasync_mixins.CfnLocationFSxLustrePropsMixin(datasync_mixins.CfnLocationFSxLustreMixinProps(
            fsx_filesystem_arn="fsxFilesystemArn",
            security_group_arns=["securityGroupArns"],
            subdirectory="subdirectory",
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
        props: typing.Union[CfnLocationFSxLustreMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DataSync::LocationFSxLustre``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8407ef1349bb5f56b8ebb237e8dd80c1a4f4a591b6bb8805758184730fe76863)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b9067c95729e3fc5e916596d47bbd124e56572fb9586883adae097f06d08984)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2af2bbfe1027387526ef37bd6a548375d6424420f951d7404a998acd683d1c24)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLocationFSxLustreMixinProps:
        return typing.cast(CfnLocationFSxLustreMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationFSxONTAPMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "protocol": "protocol",
        "security_group_arns": "securityGroupArns",
        "storage_virtual_machine_arn": "storageVirtualMachineArn",
        "subdirectory": "subdirectory",
        "tags": "tags",
    },
)
class CfnLocationFSxONTAPMixinProps:
    def __init__(
        self,
        *,
        protocol: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLocationFSxONTAPPropsMixin.ProtocolProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        security_group_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        storage_virtual_machine_arn: typing.Optional[builtins.str] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnLocationFSxONTAPPropsMixin.

        :param protocol: Specifies the data transfer protocol that DataSync uses to access your Amazon FSx file system.
        :param security_group_arns: Specifies the Amazon Resource Names (ARNs) of the security groups that DataSync can use to access your FSx for ONTAP file system. You must configure the security groups to allow outbound traffic on the following ports (depending on the protocol that you're using): - *Network File System (NFS)* : TCP ports 111, 635, and 2049 - *Server Message Block (SMB)* : TCP port 445 Your file system's security groups must also allow inbound traffic on the same port.
        :param storage_virtual_machine_arn: Specifies the ARN of the storage virtual machine (SVM) in your file system where you want to copy data to or from.
        :param subdirectory: Specifies a path to the file share in the SVM where you want to transfer data to or from. You can specify a junction path (also known as a mount point), qtree path (for NFS file shares), or share name (for SMB file shares). For example, your mount path might be ``/vol1`` , ``/vol1/tree1`` , or ``/share1`` . .. epigraph:: Don't specify a junction path in the SVM's root volume. For more information, see `Managing FSx for ONTAP storage virtual machines <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/managing-svms.html>`_ in the *Amazon FSx for NetApp ONTAP User Guide* .
        :param tags: Specifies labels that help you categorize, filter, and search for your AWS resources. We recommend creating at least a name tag for your location.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxontap.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
            
            cfn_location_fSx_oNTAPMixin_props = datasync_mixins.CfnLocationFSxONTAPMixinProps(
                protocol=datasync_mixins.CfnLocationFSxONTAPPropsMixin.ProtocolProperty(
                    nfs=datasync_mixins.CfnLocationFSxONTAPPropsMixin.NFSProperty(
                        mount_options=datasync_mixins.CfnLocationFSxONTAPPropsMixin.NfsMountOptionsProperty(
                            version="version"
                        )
                    ),
                    smb=datasync_mixins.CfnLocationFSxONTAPPropsMixin.SMBProperty(
                        domain="domain",
                        mount_options=datasync_mixins.CfnLocationFSxONTAPPropsMixin.SmbMountOptionsProperty(
                            version="version"
                        ),
                        password="password",
                        user="user"
                    )
                ),
                security_group_arns=["securityGroupArns"],
                storage_virtual_machine_arn="storageVirtualMachineArn",
                subdirectory="subdirectory",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__667c2d0f299966414edd21d1ff6a903d3ad6d50eb172e531c57d8d67a825c89d)
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument security_group_arns", value=security_group_arns, expected_type=type_hints["security_group_arns"])
            check_type(argname="argument storage_virtual_machine_arn", value=storage_virtual_machine_arn, expected_type=type_hints["storage_virtual_machine_arn"])
            check_type(argname="argument subdirectory", value=subdirectory, expected_type=type_hints["subdirectory"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if protocol is not None:
            self._values["protocol"] = protocol
        if security_group_arns is not None:
            self._values["security_group_arns"] = security_group_arns
        if storage_virtual_machine_arn is not None:
            self._values["storage_virtual_machine_arn"] = storage_virtual_machine_arn
        if subdirectory is not None:
            self._values["subdirectory"] = subdirectory
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def protocol(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLocationFSxONTAPPropsMixin.ProtocolProperty"]]:
        '''Specifies the data transfer protocol that DataSync uses to access your Amazon FSx file system.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxontap.html#cfn-datasync-locationfsxontap-protocol
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLocationFSxONTAPPropsMixin.ProtocolProperty"]], result)

    @builtins.property
    def security_group_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the Amazon Resource Names (ARNs) of the security groups that DataSync can use to access your FSx for ONTAP file system.

        You must configure the security groups to allow outbound traffic on the following ports (depending on the protocol that you're using):

        - *Network File System (NFS)* : TCP ports 111, 635, and 2049
        - *Server Message Block (SMB)* : TCP port 445

        Your file system's security groups must also allow inbound traffic on the same port.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxontap.html#cfn-datasync-locationfsxontap-securitygrouparns
        '''
        result = self._values.get("security_group_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def storage_virtual_machine_arn(self) -> typing.Optional[builtins.str]:
        '''Specifies the ARN of the storage virtual machine (SVM) in your file system where you want to copy data to or from.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxontap.html#cfn-datasync-locationfsxontap-storagevirtualmachinearn
        '''
        result = self._values.get("storage_virtual_machine_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''Specifies a path to the file share in the SVM where you want to transfer data to or from.

        You can specify a junction path (also known as a mount point), qtree path (for NFS file shares), or share name (for SMB file shares). For example, your mount path might be ``/vol1`` , ``/vol1/tree1`` , or ``/share1`` .
        .. epigraph::

           Don't specify a junction path in the SVM's root volume. For more information, see `Managing FSx for ONTAP storage virtual machines <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/managing-svms.html>`_ in the *Amazon FSx for NetApp ONTAP User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxontap.html#cfn-datasync-locationfsxontap-subdirectory
        '''
        result = self._values.get("subdirectory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Specifies labels that help you categorize, filter, and search for your AWS resources.

        We recommend creating at least a name tag for your location.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxontap.html#cfn-datasync-locationfsxontap-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLocationFSxONTAPMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLocationFSxONTAPPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationFSxONTAPPropsMixin",
):
    '''The ``AWS::DataSync::LocationFSxONTAP`` resource creates an endpoint for an Amazon FSx for NetApp ONTAP file system.

    AWS DataSync can access this endpoint as a source or destination location.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxontap.html
    :cloudformationResource: AWS::DataSync::LocationFSxONTAP
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
        
        cfn_location_fSx_oNTAPProps_mixin = datasync_mixins.CfnLocationFSxONTAPPropsMixin(datasync_mixins.CfnLocationFSxONTAPMixinProps(
            protocol=datasync_mixins.CfnLocationFSxONTAPPropsMixin.ProtocolProperty(
                nfs=datasync_mixins.CfnLocationFSxONTAPPropsMixin.NFSProperty(
                    mount_options=datasync_mixins.CfnLocationFSxONTAPPropsMixin.NfsMountOptionsProperty(
                        version="version"
                    )
                ),
                smb=datasync_mixins.CfnLocationFSxONTAPPropsMixin.SMBProperty(
                    domain="domain",
                    mount_options=datasync_mixins.CfnLocationFSxONTAPPropsMixin.SmbMountOptionsProperty(
                        version="version"
                    ),
                    password="password",
                    user="user"
                )
            ),
            security_group_arns=["securityGroupArns"],
            storage_virtual_machine_arn="storageVirtualMachineArn",
            subdirectory="subdirectory",
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
        props: typing.Union[CfnLocationFSxONTAPMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DataSync::LocationFSxONTAP``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2b309c8a891e240b2131c0180bd10702f98cfd4c7ed286672a5156c9a6d7fe2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__88c96cbb1c504b34b6ae32ef99efa82fde0ddf630fe074b48255275e808d65a0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02017f238138b2ac0a7a0bb64c1600791e2dc55d0d021fd42ca2695485c84e0b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLocationFSxONTAPMixinProps:
        return typing.cast(CfnLocationFSxONTAPMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationFSxONTAPPropsMixin.NFSProperty",
        jsii_struct_bases=[],
        name_mapping={"mount_options": "mountOptions"},
    )
    class NFSProperty:
        def __init__(
            self,
            *,
            mount_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLocationFSxONTAPPropsMixin.NfsMountOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the Network File System (NFS) protocol configuration that AWS DataSync uses to access a storage virtual machine (SVM) on your Amazon FSx for NetApp ONTAP file system.

            For more information, see `Accessing FSx for ONTAP file systems <https://docs.aws.amazon.com/datasync/latest/userguide/create-ontap-location.html#create-ontap-location-access>`_ .

            :param mount_options: Specifies how DataSync can access a location using the NFS protocol.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxontap-nfs.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
                
                n_fSProperty = datasync_mixins.CfnLocationFSxONTAPPropsMixin.NFSProperty(
                    mount_options=datasync_mixins.CfnLocationFSxONTAPPropsMixin.NfsMountOptionsProperty(
                        version="version"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__78ee71dad9d5850fd4000573f9ce217346b578b062b42ff396ad1817281dbfa1)
                check_type(argname="argument mount_options", value=mount_options, expected_type=type_hints["mount_options"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if mount_options is not None:
                self._values["mount_options"] = mount_options

        @builtins.property
        def mount_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLocationFSxONTAPPropsMixin.NfsMountOptionsProperty"]]:
            '''Specifies how DataSync can access a location using the NFS protocol.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxontap-nfs.html#cfn-datasync-locationfsxontap-nfs-mountoptions
            '''
            result = self._values.get("mount_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLocationFSxONTAPPropsMixin.NfsMountOptionsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NFSProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationFSxONTAPPropsMixin.NfsMountOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"version": "version"},
    )
    class NfsMountOptionsProperty:
        def __init__(self, *, version: typing.Optional[builtins.str] = None) -> None:
            '''Specifies how DataSync can access a location using the NFS protocol.

            :param version: Specifies the NFS version that you want DataSync to use when mounting your NFS share. If the server refuses to use the version specified, the task fails. You can specify the following options: - ``AUTOMATIC`` (default): DataSync chooses NFS version 4.1. - ``NFS3`` : Stateless protocol version that allows for asynchronous writes on the server. - ``NFSv4_0`` : Stateful, firewall-friendly protocol version that supports delegations and pseudo file systems. - ``NFSv4_1`` : Stateful protocol version that supports sessions, directory delegations, and parallel data processing. NFS version 4.1 also includes all features available in version 4.0. .. epigraph:: DataSync currently only supports NFS version 3 with Amazon FSx for NetApp ONTAP locations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxontap-nfsmountoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
                
                nfs_mount_options_property = datasync_mixins.CfnLocationFSxONTAPPropsMixin.NfsMountOptionsProperty(
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bc1dc3f334d63bdf9ec100ef1d51832f13ea840464f53bdfb3828625111c2f66)
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''Specifies the NFS version that you want DataSync to use when mounting your NFS share.

            If the server refuses to use the version specified, the task fails.

            You can specify the following options:

            - ``AUTOMATIC`` (default): DataSync chooses NFS version 4.1.
            - ``NFS3`` : Stateless protocol version that allows for asynchronous writes on the server.
            - ``NFSv4_0`` : Stateful, firewall-friendly protocol version that supports delegations and pseudo file systems.
            - ``NFSv4_1`` : Stateful protocol version that supports sessions, directory delegations, and parallel data processing. NFS version 4.1 also includes all features available in version 4.0.

            .. epigraph::

               DataSync currently only supports NFS version 3 with Amazon FSx for NetApp ONTAP locations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxontap-nfsmountoptions.html#cfn-datasync-locationfsxontap-nfsmountoptions-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NfsMountOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationFSxONTAPPropsMixin.ProtocolProperty",
        jsii_struct_bases=[],
        name_mapping={"nfs": "nfs", "smb": "smb"},
    )
    class ProtocolProperty:
        def __init__(
            self,
            *,
            nfs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLocationFSxONTAPPropsMixin.NFSProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            smb: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLocationFSxONTAPPropsMixin.SMBProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the data transfer protocol that AWS DataSync uses to access your Amazon FSx file system.

            :param nfs: Specifies the Network File System (NFS) protocol configuration that DataSync uses to access your FSx for ONTAP file system's storage virtual machine (SVM).
            :param smb: Specifies the Server Message Block (SMB) protocol configuration that DataSync uses to access your FSx for ONTAP file system's SVM.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxontap-protocol.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
                
                protocol_property = datasync_mixins.CfnLocationFSxONTAPPropsMixin.ProtocolProperty(
                    nfs=datasync_mixins.CfnLocationFSxONTAPPropsMixin.NFSProperty(
                        mount_options=datasync_mixins.CfnLocationFSxONTAPPropsMixin.NfsMountOptionsProperty(
                            version="version"
                        )
                    ),
                    smb=datasync_mixins.CfnLocationFSxONTAPPropsMixin.SMBProperty(
                        domain="domain",
                        mount_options=datasync_mixins.CfnLocationFSxONTAPPropsMixin.SmbMountOptionsProperty(
                            version="version"
                        ),
                        password="password",
                        user="user"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e2a64d2a8b6cd443b425c69cd529ffc944119b8c377b1dd408995a3dc6d89d82)
                check_type(argname="argument nfs", value=nfs, expected_type=type_hints["nfs"])
                check_type(argname="argument smb", value=smb, expected_type=type_hints["smb"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if nfs is not None:
                self._values["nfs"] = nfs
            if smb is not None:
                self._values["smb"] = smb

        @builtins.property
        def nfs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLocationFSxONTAPPropsMixin.NFSProperty"]]:
            '''Specifies the Network File System (NFS) protocol configuration that DataSync uses to access your FSx for ONTAP file system's storage virtual machine (SVM).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxontap-protocol.html#cfn-datasync-locationfsxontap-protocol-nfs
            '''
            result = self._values.get("nfs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLocationFSxONTAPPropsMixin.NFSProperty"]], result)

        @builtins.property
        def smb(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLocationFSxONTAPPropsMixin.SMBProperty"]]:
            '''Specifies the Server Message Block (SMB) protocol configuration that DataSync uses to access your FSx for ONTAP file system's SVM.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxontap-protocol.html#cfn-datasync-locationfsxontap-protocol-smb
            '''
            result = self._values.get("smb")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLocationFSxONTAPPropsMixin.SMBProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProtocolProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationFSxONTAPPropsMixin.SMBProperty",
        jsii_struct_bases=[],
        name_mapping={
            "domain": "domain",
            "mount_options": "mountOptions",
            "password": "password",
            "user": "user",
        },
    )
    class SMBProperty:
        def __init__(
            self,
            *,
            domain: typing.Optional[builtins.str] = None,
            mount_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLocationFSxONTAPPropsMixin.SmbMountOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            password: typing.Optional[builtins.str] = None,
            user: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the Server Message Block (SMB) protocol configuration that AWS DataSync uses to access a storage virtual machine (SVM) on your Amazon FSx for NetApp ONTAP file system.

            For more information, see `Accessing FSx for ONTAP file systems <https://docs.aws.amazon.com/datasync/latest/userguide/create-ontap-location.html#create-ontap-location-access>`_ .

            :param domain: Specifies the name of the Windows domain that your storage virtual machine (SVM) belongs to. If you have multiple domains in your environment, configuring this setting makes sure that DataSync connects to the right SVM. If you have multiple Active Directory domains in your environment, configuring this parameter makes sure that DataSync connects to the right SVM.
            :param mount_options: Specifies how DataSync can access a location using the SMB protocol.
            :param password: Specifies the password of a user who has permission to access your SVM.
            :param user: Specifies a user name that can mount the location and access the files, folders, and metadata that you need in the SVM. If you provide a user in your Active Directory, note the following: - If you're using AWS Directory Service for Microsoft Active Directory , the user must be a member of the AWS Delegated FSx Administrators group. - If you're using a self-managed Active Directory, the user must be a member of either the Domain Admins group or a custom group that you specified for file system administration when you created your file system. Make sure that the user has the permissions it needs to copy the data you want: - ``SE_TCB_NAME`` : Required to set object ownership and file metadata. With this privilege, you also can copy NTFS discretionary access lists (DACLs). - ``SE_SECURITY_NAME`` : May be needed to copy NTFS system access control lists (SACLs). This operation specifically requires the Windows privilege, which is granted to members of the Domain Admins group. If you configure your task to copy SACLs, make sure that the user has the required privileges. For information about copying SACLs, see `Ownership and permissions-related options <https://docs.aws.amazon.com/datasync/latest/userguide/create-task.html#configure-ownership-and-permissions>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxontap-smb.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
                
                s_mBProperty = datasync_mixins.CfnLocationFSxONTAPPropsMixin.SMBProperty(
                    domain="domain",
                    mount_options=datasync_mixins.CfnLocationFSxONTAPPropsMixin.SmbMountOptionsProperty(
                        version="version"
                    ),
                    password="password",
                    user="user"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8f65078aa7ceb43e6ecf3c39f60d7c7286a334dd113c870354ea398d7bcd0bb5)
                check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
                check_type(argname="argument mount_options", value=mount_options, expected_type=type_hints["mount_options"])
                check_type(argname="argument password", value=password, expected_type=type_hints["password"])
                check_type(argname="argument user", value=user, expected_type=type_hints["user"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if domain is not None:
                self._values["domain"] = domain
            if mount_options is not None:
                self._values["mount_options"] = mount_options
            if password is not None:
                self._values["password"] = password
            if user is not None:
                self._values["user"] = user

        @builtins.property
        def domain(self) -> typing.Optional[builtins.str]:
            '''Specifies the name of the Windows domain that your storage virtual machine (SVM) belongs to.

            If you have multiple domains in your environment, configuring this setting makes sure that DataSync connects to the right SVM.

            If you have multiple Active Directory domains in your environment, configuring this parameter makes sure that DataSync connects to the right SVM.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxontap-smb.html#cfn-datasync-locationfsxontap-smb-domain
            '''
            result = self._values.get("domain")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mount_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLocationFSxONTAPPropsMixin.SmbMountOptionsProperty"]]:
            '''Specifies how DataSync can access a location using the SMB protocol.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxontap-smb.html#cfn-datasync-locationfsxontap-smb-mountoptions
            '''
            result = self._values.get("mount_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLocationFSxONTAPPropsMixin.SmbMountOptionsProperty"]], result)

        @builtins.property
        def password(self) -> typing.Optional[builtins.str]:
            '''Specifies the password of a user who has permission to access your SVM.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxontap-smb.html#cfn-datasync-locationfsxontap-smb-password
            '''
            result = self._values.get("password")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user(self) -> typing.Optional[builtins.str]:
            '''Specifies a user name that can mount the location and access the files, folders, and metadata that you need in the SVM.

            If you provide a user in your Active Directory, note the following:

            - If you're using AWS Directory Service for Microsoft Active Directory , the user must be a member of the AWS Delegated FSx Administrators group.
            - If you're using a self-managed Active Directory, the user must be a member of either the Domain Admins group or a custom group that you specified for file system administration when you created your file system.

            Make sure that the user has the permissions it needs to copy the data you want:

            - ``SE_TCB_NAME`` : Required to set object ownership and file metadata. With this privilege, you also can copy NTFS discretionary access lists (DACLs).
            - ``SE_SECURITY_NAME`` : May be needed to copy NTFS system access control lists (SACLs). This operation specifically requires the Windows privilege, which is granted to members of the Domain Admins group. If you configure your task to copy SACLs, make sure that the user has the required privileges. For information about copying SACLs, see `Ownership and permissions-related options <https://docs.aws.amazon.com/datasync/latest/userguide/create-task.html#configure-ownership-and-permissions>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxontap-smb.html#cfn-datasync-locationfsxontap-smb-user
            '''
            result = self._values.get("user")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SMBProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationFSxONTAPPropsMixin.SmbMountOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"version": "version"},
    )
    class SmbMountOptionsProperty:
        def __init__(self, *, version: typing.Optional[builtins.str] = None) -> None:
            '''Specifies the version of the Server Message Block (SMB) protocol that AWS DataSync uses to access an SMB file server.

            :param version: By default, DataSync automatically chooses an SMB protocol version based on negotiation with your SMB file server. You also can configure DataSync to use a specific SMB version, but we recommend doing this only if DataSync has trouble negotiating with the SMB file server automatically. These are the following options for configuring the SMB version: - ``AUTOMATIC`` (default): DataSync and the SMB file server negotiate the highest version of SMB that they mutually support between 2.1 and 3.1.1. This is the recommended option. If you instead choose a specific version that your file server doesn't support, you may get an ``Operation Not Supported`` error. - ``SMB3`` : Restricts the protocol negotiation to only SMB version 3.0.2. - ``SMB2`` : Restricts the protocol negotiation to only SMB version 2.1. - ``SMB2_0`` : Restricts the protocol negotiation to only SMB version 2.0. - ``SMB1`` : Restricts the protocol negotiation to only SMB version 1.0. .. epigraph:: The ``SMB1`` option isn't available when `creating an Amazon FSx for NetApp ONTAP location <https://docs.aws.amazon.com/datasync/latest/userguide/API_CreateLocationFsxOntap.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxontap-smbmountoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
                
                smb_mount_options_property = datasync_mixins.CfnLocationFSxONTAPPropsMixin.SmbMountOptionsProperty(
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__98a9583555011c9c3362edcb41dbd8b27ab39ec5e7be5db661cfe1f8eb2762eb)
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''By default, DataSync automatically chooses an SMB protocol version based on negotiation with your SMB file server.

            You also can configure DataSync to use a specific SMB version, but we recommend doing this only if DataSync has trouble negotiating with the SMB file server automatically.

            These are the following options for configuring the SMB version:

            - ``AUTOMATIC`` (default): DataSync and the SMB file server negotiate the highest version of SMB that they mutually support between 2.1 and 3.1.1.

            This is the recommended option. If you instead choose a specific version that your file server doesn't support, you may get an ``Operation Not Supported`` error.

            - ``SMB3`` : Restricts the protocol negotiation to only SMB version 3.0.2.
            - ``SMB2`` : Restricts the protocol negotiation to only SMB version 2.1.
            - ``SMB2_0`` : Restricts the protocol negotiation to only SMB version 2.0.
            - ``SMB1`` : Restricts the protocol negotiation to only SMB version 1.0.

            .. epigraph::

               The ``SMB1`` option isn't available when `creating an Amazon FSx for NetApp ONTAP location <https://docs.aws.amazon.com/datasync/latest/userguide/API_CreateLocationFsxOntap.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxontap-smbmountoptions.html#cfn-datasync-locationfsxontap-smbmountoptions-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SmbMountOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationFSxOpenZFSMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "fsx_filesystem_arn": "fsxFilesystemArn",
        "protocol": "protocol",
        "security_group_arns": "securityGroupArns",
        "subdirectory": "subdirectory",
        "tags": "tags",
    },
)
class CfnLocationFSxOpenZFSMixinProps:
    def __init__(
        self,
        *,
        fsx_filesystem_arn: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLocationFSxOpenZFSPropsMixin.ProtocolProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        security_group_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnLocationFSxOpenZFSPropsMixin.

        :param fsx_filesystem_arn: The Amazon Resource Name (ARN) of the FSx for OpenZFS file system.
        :param protocol: The type of protocol that AWS DataSync uses to access your file system.
        :param security_group_arns: The ARNs of the security groups that are used to configure the FSx for OpenZFS file system. *Pattern* : ``^arn:(aws|aws-cn|aws-us-gov|aws-iso|aws-iso-b):ec2:[a-z\\-0-9]*:[0-9]{12}:security-group/.*$`` *Length constraints* : Maximum length of 128.
        :param subdirectory: A subdirectory in the location's path that must begin with ``/fsx`` . DataSync uses this subdirectory to read or write data (depending on whether the file system is a source or destination location).
        :param tags: The key-value pair that represents a tag that you want to add to the resource. The value can be an empty string. This value helps you manage, filter, and search for your resources. We recommend that you create a name tag for your location.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxopenzfs.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
            
            cfn_location_fSx_open_zFSMixin_props = datasync_mixins.CfnLocationFSxOpenZFSMixinProps(
                fsx_filesystem_arn="fsxFilesystemArn",
                protocol=datasync_mixins.CfnLocationFSxOpenZFSPropsMixin.ProtocolProperty(
                    nfs=datasync_mixins.CfnLocationFSxOpenZFSPropsMixin.NFSProperty(
                        mount_options=datasync_mixins.CfnLocationFSxOpenZFSPropsMixin.MountOptionsProperty(
                            version="version"
                        )
                    )
                ),
                security_group_arns=["securityGroupArns"],
                subdirectory="subdirectory",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d10dcb7b4728c6606e0100e14010d2ed9c174305c88a601d1b3f0ce271afb86)
            check_type(argname="argument fsx_filesystem_arn", value=fsx_filesystem_arn, expected_type=type_hints["fsx_filesystem_arn"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument security_group_arns", value=security_group_arns, expected_type=type_hints["security_group_arns"])
            check_type(argname="argument subdirectory", value=subdirectory, expected_type=type_hints["subdirectory"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if fsx_filesystem_arn is not None:
            self._values["fsx_filesystem_arn"] = fsx_filesystem_arn
        if protocol is not None:
            self._values["protocol"] = protocol
        if security_group_arns is not None:
            self._values["security_group_arns"] = security_group_arns
        if subdirectory is not None:
            self._values["subdirectory"] = subdirectory
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def fsx_filesystem_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the FSx for OpenZFS file system.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxopenzfs.html#cfn-datasync-locationfsxopenzfs-fsxfilesystemarn
        '''
        result = self._values.get("fsx_filesystem_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLocationFSxOpenZFSPropsMixin.ProtocolProperty"]]:
        '''The type of protocol that AWS DataSync uses to access your file system.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxopenzfs.html#cfn-datasync-locationfsxopenzfs-protocol
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLocationFSxOpenZFSPropsMixin.ProtocolProperty"]], result)

    @builtins.property
    def security_group_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The ARNs of the security groups that are used to configure the FSx for OpenZFS file system.

        *Pattern* : ``^arn:(aws|aws-cn|aws-us-gov|aws-iso|aws-iso-b):ec2:[a-z\\-0-9]*:[0-9]{12}:security-group/.*$``

        *Length constraints* : Maximum length of 128.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxopenzfs.html#cfn-datasync-locationfsxopenzfs-securitygrouparns
        '''
        result = self._values.get("security_group_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''A subdirectory in the location's path that must begin with ``/fsx`` .

        DataSync uses this subdirectory to read or write data (depending on whether the file system is a source or destination location).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxopenzfs.html#cfn-datasync-locationfsxopenzfs-subdirectory
        '''
        result = self._values.get("subdirectory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The key-value pair that represents a tag that you want to add to the resource.

        The value can be an empty string. This value helps you manage, filter, and search for your resources. We recommend that you create a name tag for your location.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxopenzfs.html#cfn-datasync-locationfsxopenzfs-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLocationFSxOpenZFSMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLocationFSxOpenZFSPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationFSxOpenZFSPropsMixin",
):
    '''The ``AWS::DataSync::LocationFSxOpenZFS`` resource specifies an endpoint for an Amazon FSx for OpenZFS file system.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxopenzfs.html
    :cloudformationResource: AWS::DataSync::LocationFSxOpenZFS
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
        
        cfn_location_fSx_open_zFSProps_mixin = datasync_mixins.CfnLocationFSxOpenZFSPropsMixin(datasync_mixins.CfnLocationFSxOpenZFSMixinProps(
            fsx_filesystem_arn="fsxFilesystemArn",
            protocol=datasync_mixins.CfnLocationFSxOpenZFSPropsMixin.ProtocolProperty(
                nfs=datasync_mixins.CfnLocationFSxOpenZFSPropsMixin.NFSProperty(
                    mount_options=datasync_mixins.CfnLocationFSxOpenZFSPropsMixin.MountOptionsProperty(
                        version="version"
                    )
                )
            ),
            security_group_arns=["securityGroupArns"],
            subdirectory="subdirectory",
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
        props: typing.Union[CfnLocationFSxOpenZFSMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DataSync::LocationFSxOpenZFS``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0824e2cfd74162218f82fcdc39a1c5ae4b9cfc10caef8334637288682394608e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4aef43e68cd2f62cbc54e17d06a103fd57caeb2c3dcf12652d65387fabd7b477)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a48448457fec0e501747a2a0a94444335f34d0cd4edca08a90ba0ce8b7d0424e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLocationFSxOpenZFSMixinProps:
        return typing.cast(CfnLocationFSxOpenZFSMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationFSxOpenZFSPropsMixin.MountOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"version": "version"},
    )
    class MountOptionsProperty:
        def __init__(self, *, version: typing.Optional[builtins.str] = None) -> None:
            '''Represents the mount options that are available for DataSync to access a Network File System (NFS) location.

            :param version: The specific NFS version that you want DataSync to use to mount your NFS share. If the server refuses to use the version specified, the sync will fail. If you don't specify a version, DataSync defaults to ``AUTOMATIC`` . That is, DataSync automatically selects a version based on negotiation with the NFS server. You can specify the following NFS versions: - *`NFSv3 <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc1813>`_* : Stateless protocol version that allows for asynchronous writes on the server. - *`NFSv4.0 <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc3530>`_* : Stateful, firewall-friendly protocol version that supports delegations and pseudo file systems. - *`NFSv4.1 <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc5661>`_* : Stateful protocol version that supports sessions, directory delegations, and parallel data processing. Version 4.1 also includes all features available in version 4.0.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxopenzfs-mountoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
                
                mount_options_property = datasync_mixins.CfnLocationFSxOpenZFSPropsMixin.MountOptionsProperty(
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b84d624d1174a64ccdb4b414248cce02b9f5e3d203d8fb6af3ca5066c5026017)
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''The specific NFS version that you want DataSync to use to mount your NFS share.

            If the server refuses to use the version specified, the sync will fail. If you don't specify a version, DataSync defaults to ``AUTOMATIC`` . That is, DataSync automatically selects a version based on negotiation with the NFS server.

            You can specify the following NFS versions:

            - *`NFSv3 <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc1813>`_* : Stateless protocol version that allows for asynchronous writes on the server.
            - *`NFSv4.0 <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc3530>`_* : Stateful, firewall-friendly protocol version that supports delegations and pseudo file systems.
            - *`NFSv4.1 <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc5661>`_* : Stateful protocol version that supports sessions, directory delegations, and parallel data processing. Version 4.1 also includes all features available in version 4.0.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxopenzfs-mountoptions.html#cfn-datasync-locationfsxopenzfs-mountoptions-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MountOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationFSxOpenZFSPropsMixin.NFSProperty",
        jsii_struct_bases=[],
        name_mapping={"mount_options": "mountOptions"},
    )
    class NFSProperty:
        def __init__(
            self,
            *,
            mount_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLocationFSxOpenZFSPropsMixin.MountOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Represents the Network File System (NFS) protocol that AWS DataSync uses to access your Amazon FSx for OpenZFS file system.

            :param mount_options: Represents the mount options that are available for DataSync to access an NFS location.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxopenzfs-nfs.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
                
                n_fSProperty = datasync_mixins.CfnLocationFSxOpenZFSPropsMixin.NFSProperty(
                    mount_options=datasync_mixins.CfnLocationFSxOpenZFSPropsMixin.MountOptionsProperty(
                        version="version"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0d4d44c314b8aeecf19bde222f3bd99a8d5b2ae94c2e506917a7d188fda0d53b)
                check_type(argname="argument mount_options", value=mount_options, expected_type=type_hints["mount_options"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if mount_options is not None:
                self._values["mount_options"] = mount_options

        @builtins.property
        def mount_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLocationFSxOpenZFSPropsMixin.MountOptionsProperty"]]:
            '''Represents the mount options that are available for DataSync to access an NFS location.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxopenzfs-nfs.html#cfn-datasync-locationfsxopenzfs-nfs-mountoptions
            '''
            result = self._values.get("mount_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLocationFSxOpenZFSPropsMixin.MountOptionsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NFSProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationFSxOpenZFSPropsMixin.ProtocolProperty",
        jsii_struct_bases=[],
        name_mapping={"nfs": "nfs"},
    )
    class ProtocolProperty:
        def __init__(
            self,
            *,
            nfs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLocationFSxOpenZFSPropsMixin.NFSProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Represents the protocol that AWS DataSync uses to access your Amazon FSx for OpenZFS file system.

            :param nfs: Represents the Network File System (NFS) protocol that DataSync uses to access your FSx for OpenZFS file system.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxopenzfs-protocol.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
                
                protocol_property = datasync_mixins.CfnLocationFSxOpenZFSPropsMixin.ProtocolProperty(
                    nfs=datasync_mixins.CfnLocationFSxOpenZFSPropsMixin.NFSProperty(
                        mount_options=datasync_mixins.CfnLocationFSxOpenZFSPropsMixin.MountOptionsProperty(
                            version="version"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4b6bb88b3242797dafd6d16c8fda57f8d1ee9e8688c54bb47f1955e3b79505cf)
                check_type(argname="argument nfs", value=nfs, expected_type=type_hints["nfs"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if nfs is not None:
                self._values["nfs"] = nfs

        @builtins.property
        def nfs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLocationFSxOpenZFSPropsMixin.NFSProperty"]]:
            '''Represents the Network File System (NFS) protocol that DataSync uses to access your FSx for OpenZFS file system.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxopenzfs-protocol.html#cfn-datasync-locationfsxopenzfs-protocol-nfs
            '''
            result = self._values.get("nfs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLocationFSxOpenZFSPropsMixin.NFSProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProtocolProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationFSxWindowsMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "domain": "domain",
        "fsx_filesystem_arn": "fsxFilesystemArn",
        "password": "password",
        "security_group_arns": "securityGroupArns",
        "subdirectory": "subdirectory",
        "tags": "tags",
        "user": "user",
    },
)
class CfnLocationFSxWindowsMixinProps:
    def __init__(
        self,
        *,
        domain: typing.Optional[builtins.str] = None,
        fsx_filesystem_arn: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        security_group_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        user: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnLocationFSxWindowsPropsMixin.

        :param domain: Specifies the name of the Windows domain that the FSx for Windows File Server file system belongs to. If you have multiple Active Directory domains in your environment, configuring this parameter makes sure that DataSync connects to the right file system.
        :param fsx_filesystem_arn: Specifies the Amazon Resource Name (ARN) for the FSx for Windows File Server file system.
        :param password: Specifies the password of the user with the permissions to mount and access the files, folders, and file metadata in your FSx for Windows File Server file system.
        :param security_group_arns: The Amazon Resource Names (ARNs) of the security groups that are used to configure the FSx for Windows File Server file system. *Pattern* : ``^arn:(aws|aws-cn|aws-us-gov|aws-iso|aws-iso-b):ec2:[a-z\\-0-9]*:[0-9]{12}:security-group/.*$`` *Length constraints* : Maximum length of 128.
        :param subdirectory: Specifies a mount path for your file system using forward slashes. This is where DataSync reads or writes data (depending on if this is a source or destination location).
        :param tags: Specifies labels that help you categorize, filter, and search for your AWS resources. We recommend creating at least a name tag for your location.
        :param user: The user who has the permissions to access files and folders in the FSx for Windows File Server file system. For information about choosing a user name that ensures sufficient permissions to files, folders, and metadata, see `user <https://docs.aws.amazon.com/datasync/latest/userguide/create-fsx-location.html#FSxWuser>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxwindows.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
            
            cfn_location_fSx_windows_mixin_props = datasync_mixins.CfnLocationFSxWindowsMixinProps(
                domain="domain",
                fsx_filesystem_arn="fsxFilesystemArn",
                password="password",
                security_group_arns=["securityGroupArns"],
                subdirectory="subdirectory",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                user="user"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20b4ada2de7d454b794a5399617cd50b6e5bb69953c7b8565922085c6c1e4441)
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument fsx_filesystem_arn", value=fsx_filesystem_arn, expected_type=type_hints["fsx_filesystem_arn"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument security_group_arns", value=security_group_arns, expected_type=type_hints["security_group_arns"])
            check_type(argname="argument subdirectory", value=subdirectory, expected_type=type_hints["subdirectory"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if domain is not None:
            self._values["domain"] = domain
        if fsx_filesystem_arn is not None:
            self._values["fsx_filesystem_arn"] = fsx_filesystem_arn
        if password is not None:
            self._values["password"] = password
        if security_group_arns is not None:
            self._values["security_group_arns"] = security_group_arns
        if subdirectory is not None:
            self._values["subdirectory"] = subdirectory
        if tags is not None:
            self._values["tags"] = tags
        if user is not None:
            self._values["user"] = user

    @builtins.property
    def domain(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the Windows domain that the FSx for Windows File Server file system belongs to.

        If you have multiple Active Directory domains in your environment, configuring this parameter makes sure that DataSync connects to the right file system.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxwindows.html#cfn-datasync-locationfsxwindows-domain
        '''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fsx_filesystem_arn(self) -> typing.Optional[builtins.str]:
        '''Specifies the Amazon Resource Name (ARN) for the FSx for Windows File Server file system.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxwindows.html#cfn-datasync-locationfsxwindows-fsxfilesystemarn
        '''
        result = self._values.get("fsx_filesystem_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Specifies the password of the user with the permissions to mount and access the files, folders, and file metadata in your FSx for Windows File Server file system.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxwindows.html#cfn-datasync-locationfsxwindows-password
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_group_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Amazon Resource Names (ARNs) of the security groups that are used to configure the FSx for Windows File Server file system.

        *Pattern* : ``^arn:(aws|aws-cn|aws-us-gov|aws-iso|aws-iso-b):ec2:[a-z\\-0-9]*:[0-9]{12}:security-group/.*$``

        *Length constraints* : Maximum length of 128.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxwindows.html#cfn-datasync-locationfsxwindows-securitygrouparns
        '''
        result = self._values.get("security_group_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''Specifies a mount path for your file system using forward slashes.

        This is where DataSync reads or writes data (depending on if this is a source or destination location).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxwindows.html#cfn-datasync-locationfsxwindows-subdirectory
        '''
        result = self._values.get("subdirectory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Specifies labels that help you categorize, filter, and search for your AWS resources.

        We recommend creating at least a name tag for your location.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxwindows.html#cfn-datasync-locationfsxwindows-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def user(self) -> typing.Optional[builtins.str]:
        '''The user who has the permissions to access files and folders in the FSx for Windows File Server file system.

        For information about choosing a user name that ensures sufficient permissions to files, folders, and metadata, see `user <https://docs.aws.amazon.com/datasync/latest/userguide/create-fsx-location.html#FSxWuser>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxwindows.html#cfn-datasync-locationfsxwindows-user
        '''
        result = self._values.get("user")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLocationFSxWindowsMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLocationFSxWindowsPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationFSxWindowsPropsMixin",
):
    '''The ``AWS::DataSync::LocationFSxWindows`` resource specifies an endpoint for an Amazon FSx for Windows Server file system.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxwindows.html
    :cloudformationResource: AWS::DataSync::LocationFSxWindows
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
        
        cfn_location_fSx_windows_props_mixin = datasync_mixins.CfnLocationFSxWindowsPropsMixin(datasync_mixins.CfnLocationFSxWindowsMixinProps(
            domain="domain",
            fsx_filesystem_arn="fsxFilesystemArn",
            password="password",
            security_group_arns=["securityGroupArns"],
            subdirectory="subdirectory",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            user="user"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnLocationFSxWindowsMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DataSync::LocationFSxWindows``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__749472fa57712afd2fd6c279839d193d58de96b3c214179a37a768ad33ed3a62)
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
            type_hints = typing.get_type_hints(_typecheckingstub__92b985ce733a45be8d3a5a76716dd163ea32d5e43f7a2b16f6f58db3673cddd3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5fa8d48fd6d61cb4bb5faa87e0a4dd17fa7c96d171fe83e3ba11cbe662bce42)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLocationFSxWindowsMixinProps:
        return typing.cast(CfnLocationFSxWindowsMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationHDFSMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "agent_arns": "agentArns",
        "authentication_type": "authenticationType",
        "block_size": "blockSize",
        "kerberos_keytab": "kerberosKeytab",
        "kerberos_krb5_conf": "kerberosKrb5Conf",
        "kerberos_principal": "kerberosPrincipal",
        "kms_key_provider_uri": "kmsKeyProviderUri",
        "name_nodes": "nameNodes",
        "qop_configuration": "qopConfiguration",
        "replication_factor": "replicationFactor",
        "simple_user": "simpleUser",
        "subdirectory": "subdirectory",
        "tags": "tags",
    },
)
class CfnLocationHDFSMixinProps:
    def __init__(
        self,
        *,
        agent_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        authentication_type: typing.Optional[builtins.str] = None,
        block_size: typing.Optional[jsii.Number] = None,
        kerberos_keytab: typing.Optional[builtins.str] = None,
        kerberos_krb5_conf: typing.Optional[builtins.str] = None,
        kerberos_principal: typing.Optional[builtins.str] = None,
        kms_key_provider_uri: typing.Optional[builtins.str] = None,
        name_nodes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLocationHDFSPropsMixin.NameNodeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        qop_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLocationHDFSPropsMixin.QopConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        replication_factor: typing.Optional[jsii.Number] = None,
        simple_user: typing.Optional[builtins.str] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnLocationHDFSPropsMixin.

        :param agent_arns: The Amazon Resource Names (ARNs) of the DataSync agents that can connect to your HDFS cluster.
        :param authentication_type: The authentication mode used to determine identity of user.
        :param block_size: The size of data blocks to write into the HDFS cluster. The block size must be a multiple of 512 bytes. The default block size is 128 mebibytes (MiB).
        :param kerberos_keytab: The Kerberos key table (keytab) that contains mappings between the defined Kerberos principal and the encrypted keys. Provide the base64-encoded file text. If ``KERBEROS`` is specified for ``AuthType`` , this value is required.
        :param kerberos_krb5_conf: The ``krb5.conf`` file that contains the Kerberos configuration information. You can load the ``krb5.conf`` by providing a string of the file's contents or an Amazon S3 presigned URL of the file. If ``KERBEROS`` is specified for ``AuthType`` , this value is required.
        :param kerberos_principal: The Kerberos principal with access to the files and folders on the HDFS cluster. .. epigraph:: If ``KERBEROS`` is specified for ``AuthenticationType`` , this parameter is required.
        :param kms_key_provider_uri: The URI of the HDFS cluster's Key Management Server (KMS).
        :param name_nodes: The NameNode that manages the HDFS namespace. The NameNode performs operations such as opening, closing, and renaming files and directories. The NameNode contains the information to map blocks of data to the DataNodes. You can use only one NameNode.
        :param qop_configuration: The Quality of Protection (QOP) configuration specifies the Remote Procedure Call (RPC) and data transfer protection settings configured on the Hadoop Distributed File System (HDFS) cluster. If ``QopConfiguration`` isn't specified, ``RpcProtection`` and ``DataTransferProtection`` default to ``PRIVACY`` . If you set ``RpcProtection`` or ``DataTransferProtection`` , the other parameter assumes the same value.
        :param replication_factor: The number of DataNodes to replicate the data to when writing to the HDFS cluster. By default, data is replicated to three DataNodes. Default: - 3
        :param simple_user: The user name used to identify the client on the host operating system. .. epigraph:: If ``SIMPLE`` is specified for ``AuthenticationType`` , this parameter is required.
        :param subdirectory: A subdirectory in the HDFS cluster. This subdirectory is used to read data from or write data to the HDFS cluster. If the subdirectory isn't specified, it will default to ``/`` .
        :param tags: The key-value pair that represents the tag that you want to add to the location. The value can be an empty string. We recommend using tags to name your resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
            
            cfn_location_hDFSMixin_props = datasync_mixins.CfnLocationHDFSMixinProps(
                agent_arns=["agentArns"],
                authentication_type="authenticationType",
                block_size=123,
                kerberos_keytab="kerberosKeytab",
                kerberos_krb5_conf="kerberosKrb5Conf",
                kerberos_principal="kerberosPrincipal",
                kms_key_provider_uri="kmsKeyProviderUri",
                name_nodes=[datasync_mixins.CfnLocationHDFSPropsMixin.NameNodeProperty(
                    hostname="hostname",
                    port=123
                )],
                qop_configuration=datasync_mixins.CfnLocationHDFSPropsMixin.QopConfigurationProperty(
                    data_transfer_protection="dataTransferProtection",
                    rpc_protection="rpcProtection"
                ),
                replication_factor=123,
                simple_user="simpleUser",
                subdirectory="subdirectory",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0187c6f0cf30a18094c17379d9509f1658ebe223cee0384d47baeda748c8f895)
            check_type(argname="argument agent_arns", value=agent_arns, expected_type=type_hints["agent_arns"])
            check_type(argname="argument authentication_type", value=authentication_type, expected_type=type_hints["authentication_type"])
            check_type(argname="argument block_size", value=block_size, expected_type=type_hints["block_size"])
            check_type(argname="argument kerberos_keytab", value=kerberos_keytab, expected_type=type_hints["kerberos_keytab"])
            check_type(argname="argument kerberos_krb5_conf", value=kerberos_krb5_conf, expected_type=type_hints["kerberos_krb5_conf"])
            check_type(argname="argument kerberos_principal", value=kerberos_principal, expected_type=type_hints["kerberos_principal"])
            check_type(argname="argument kms_key_provider_uri", value=kms_key_provider_uri, expected_type=type_hints["kms_key_provider_uri"])
            check_type(argname="argument name_nodes", value=name_nodes, expected_type=type_hints["name_nodes"])
            check_type(argname="argument qop_configuration", value=qop_configuration, expected_type=type_hints["qop_configuration"])
            check_type(argname="argument replication_factor", value=replication_factor, expected_type=type_hints["replication_factor"])
            check_type(argname="argument simple_user", value=simple_user, expected_type=type_hints["simple_user"])
            check_type(argname="argument subdirectory", value=subdirectory, expected_type=type_hints["subdirectory"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if agent_arns is not None:
            self._values["agent_arns"] = agent_arns
        if authentication_type is not None:
            self._values["authentication_type"] = authentication_type
        if block_size is not None:
            self._values["block_size"] = block_size
        if kerberos_keytab is not None:
            self._values["kerberos_keytab"] = kerberos_keytab
        if kerberos_krb5_conf is not None:
            self._values["kerberos_krb5_conf"] = kerberos_krb5_conf
        if kerberos_principal is not None:
            self._values["kerberos_principal"] = kerberos_principal
        if kms_key_provider_uri is not None:
            self._values["kms_key_provider_uri"] = kms_key_provider_uri
        if name_nodes is not None:
            self._values["name_nodes"] = name_nodes
        if qop_configuration is not None:
            self._values["qop_configuration"] = qop_configuration
        if replication_factor is not None:
            self._values["replication_factor"] = replication_factor
        if simple_user is not None:
            self._values["simple_user"] = simple_user
        if subdirectory is not None:
            self._values["subdirectory"] = subdirectory
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def agent_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Amazon Resource Names (ARNs) of the DataSync agents that can connect to your HDFS cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-agentarns
        '''
        result = self._values.get("agent_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def authentication_type(self) -> typing.Optional[builtins.str]:
        '''The authentication mode used to determine identity of user.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-authenticationtype
        '''
        result = self._values.get("authentication_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def block_size(self) -> typing.Optional[jsii.Number]:
        '''The size of data blocks to write into the HDFS cluster.

        The block size must be a multiple of 512 bytes. The default block size is 128 mebibytes (MiB).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-blocksize
        '''
        result = self._values.get("block_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def kerberos_keytab(self) -> typing.Optional[builtins.str]:
        '''The Kerberos key table (keytab) that contains mappings between the defined Kerberos principal and the encrypted keys.

        Provide the base64-encoded file text. If ``KERBEROS`` is specified for ``AuthType`` , this value is required.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-kerberoskeytab
        '''
        result = self._values.get("kerberos_keytab")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kerberos_krb5_conf(self) -> typing.Optional[builtins.str]:
        '''The ``krb5.conf`` file that contains the Kerberos configuration information. You can load the ``krb5.conf`` by providing a string of the file's contents or an Amazon S3 presigned URL of the file. If ``KERBEROS`` is specified for ``AuthType`` , this value is required.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-kerberoskrb5conf
        '''
        result = self._values.get("kerberos_krb5_conf")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kerberos_principal(self) -> typing.Optional[builtins.str]:
        '''The Kerberos principal with access to the files and folders on the HDFS cluster.

        .. epigraph::

           If ``KERBEROS`` is specified for ``AuthenticationType`` , this parameter is required.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-kerberosprincipal
        '''
        result = self._values.get("kerberos_principal")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_provider_uri(self) -> typing.Optional[builtins.str]:
        '''The URI of the HDFS cluster's Key Management Server (KMS).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-kmskeyprovideruri
        '''
        result = self._values.get("kms_key_provider_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name_nodes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLocationHDFSPropsMixin.NameNodeProperty"]]]]:
        '''The NameNode that manages the HDFS namespace.

        The NameNode performs operations such as opening, closing, and renaming files and directories. The NameNode contains the information to map blocks of data to the DataNodes. You can use only one NameNode.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-namenodes
        '''
        result = self._values.get("name_nodes")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLocationHDFSPropsMixin.NameNodeProperty"]]]], result)

    @builtins.property
    def qop_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLocationHDFSPropsMixin.QopConfigurationProperty"]]:
        '''The Quality of Protection (QOP) configuration specifies the Remote Procedure Call (RPC) and data transfer protection settings configured on the Hadoop Distributed File System (HDFS) cluster.

        If ``QopConfiguration`` isn't specified, ``RpcProtection`` and ``DataTransferProtection`` default to ``PRIVACY`` . If you set ``RpcProtection`` or ``DataTransferProtection`` , the other parameter assumes the same value.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-qopconfiguration
        '''
        result = self._values.get("qop_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLocationHDFSPropsMixin.QopConfigurationProperty"]], result)

    @builtins.property
    def replication_factor(self) -> typing.Optional[jsii.Number]:
        '''The number of DataNodes to replicate the data to when writing to the HDFS cluster.

        By default, data is replicated to three DataNodes.

        :default: - 3

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-replicationfactor
        '''
        result = self._values.get("replication_factor")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def simple_user(self) -> typing.Optional[builtins.str]:
        '''The user name used to identify the client on the host operating system.

        .. epigraph::

           If ``SIMPLE`` is specified for ``AuthenticationType`` , this parameter is required.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-simpleuser
        '''
        result = self._values.get("simple_user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''A subdirectory in the HDFS cluster.

        This subdirectory is used to read data from or write data to the HDFS cluster. If the subdirectory isn't specified, it will default to ``/`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-subdirectory
        '''
        result = self._values.get("subdirectory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The key-value pair that represents the tag that you want to add to the location.

        The value can be an empty string. We recommend using tags to name your resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLocationHDFSMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLocationHDFSPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationHDFSPropsMixin",
):
    '''The ``AWS::DataSync::LocationHDFS`` resource specifies an endpoint for a Hadoop Distributed File System (HDFS).

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html
    :cloudformationResource: AWS::DataSync::LocationHDFS
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
        
        cfn_location_hDFSProps_mixin = datasync_mixins.CfnLocationHDFSPropsMixin(datasync_mixins.CfnLocationHDFSMixinProps(
            agent_arns=["agentArns"],
            authentication_type="authenticationType",
            block_size=123,
            kerberos_keytab="kerberosKeytab",
            kerberos_krb5_conf="kerberosKrb5Conf",
            kerberos_principal="kerberosPrincipal",
            kms_key_provider_uri="kmsKeyProviderUri",
            name_nodes=[datasync_mixins.CfnLocationHDFSPropsMixin.NameNodeProperty(
                hostname="hostname",
                port=123
            )],
            qop_configuration=datasync_mixins.CfnLocationHDFSPropsMixin.QopConfigurationProperty(
                data_transfer_protection="dataTransferProtection",
                rpc_protection="rpcProtection"
            ),
            replication_factor=123,
            simple_user="simpleUser",
            subdirectory="subdirectory",
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
        props: typing.Union[CfnLocationHDFSMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DataSync::LocationHDFS``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e21015cde3d5a1222e09c1c85e8463a7b207760b9ca1b81140a3e96bb54fed92)
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
            type_hints = typing.get_type_hints(_typecheckingstub__60a2f4204244aaf404e41eb479a3f69b4b6890df88466a04ec1b81145a140d29)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad3e05fc945c76530c387f2c1646833b8a39855bad6f0ed05addbb03aa564f6f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLocationHDFSMixinProps:
        return typing.cast(CfnLocationHDFSMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationHDFSPropsMixin.NameNodeProperty",
        jsii_struct_bases=[],
        name_mapping={"hostname": "hostname", "port": "port"},
    )
    class NameNodeProperty:
        def __init__(
            self,
            *,
            hostname: typing.Optional[builtins.str] = None,
            port: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The NameNode of the Hadoop Distributed File System (HDFS).

            The NameNode manages the file system's namespace and performs operations such as opening, closing, and renaming files and directories. The NameNode also contains the information to map blocks of data to the DataNodes.

            :param hostname: The hostname of the NameNode in the HDFS cluster. This value is the IP address or Domain Name Service (DNS) name of the NameNode. An agent that's installed on-premises uses this hostname to communicate with the NameNode in the network.
            :param port: The port that the NameNode uses to listen to client requests.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationhdfs-namenode.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
                
                name_node_property = datasync_mixins.CfnLocationHDFSPropsMixin.NameNodeProperty(
                    hostname="hostname",
                    port=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2bc52206954aa9bc6ff20021519027203cf31eed7ec8e3fb16a403feee5bf199)
                check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if hostname is not None:
                self._values["hostname"] = hostname
            if port is not None:
                self._values["port"] = port

        @builtins.property
        def hostname(self) -> typing.Optional[builtins.str]:
            '''The hostname of the NameNode in the HDFS cluster.

            This value is the IP address or Domain Name Service (DNS) name of the NameNode. An agent that's installed on-premises uses this hostname to communicate with the NameNode in the network.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationhdfs-namenode.html#cfn-datasync-locationhdfs-namenode-hostname
            '''
            result = self._values.get("hostname")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''The port that the NameNode uses to listen to client requests.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationhdfs-namenode.html#cfn-datasync-locationhdfs-namenode-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NameNodeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationHDFSPropsMixin.QopConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_transfer_protection": "dataTransferProtection",
            "rpc_protection": "rpcProtection",
        },
    )
    class QopConfigurationProperty:
        def __init__(
            self,
            *,
            data_transfer_protection: typing.Optional[builtins.str] = None,
            rpc_protection: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The Quality of Protection (QOP) configuration specifies the Remote Procedure Call (RPC) and data transfer privacy settings configured on the Hadoop Distributed File System (HDFS) cluster.

            :param data_transfer_protection: The data transfer protection setting configured on the HDFS cluster. This setting corresponds to your ``dfs.data.transfer.protection`` setting in the ``hdfs-site.xml`` file on your Hadoop cluster. Default: - "PRIVACY"
            :param rpc_protection: The Remote Procedure Call (RPC) protection setting configured on the HDFS cluster. This setting corresponds to your ``hadoop.rpc.protection`` setting in your ``core-site.xml`` file on your Hadoop cluster. Default: - "PRIVACY"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationhdfs-qopconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
                
                qop_configuration_property = datasync_mixins.CfnLocationHDFSPropsMixin.QopConfigurationProperty(
                    data_transfer_protection="dataTransferProtection",
                    rpc_protection="rpcProtection"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c6c8596dfe59a5234a9f5be7da8f5b1253a80fe148174dc4edc66a86746cfb34)
                check_type(argname="argument data_transfer_protection", value=data_transfer_protection, expected_type=type_hints["data_transfer_protection"])
                check_type(argname="argument rpc_protection", value=rpc_protection, expected_type=type_hints["rpc_protection"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data_transfer_protection is not None:
                self._values["data_transfer_protection"] = data_transfer_protection
            if rpc_protection is not None:
                self._values["rpc_protection"] = rpc_protection

        @builtins.property
        def data_transfer_protection(self) -> typing.Optional[builtins.str]:
            '''The data transfer protection setting configured on the HDFS cluster.

            This setting corresponds to your ``dfs.data.transfer.protection`` setting in the ``hdfs-site.xml`` file on your Hadoop cluster.

            :default: - "PRIVACY"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationhdfs-qopconfiguration.html#cfn-datasync-locationhdfs-qopconfiguration-datatransferprotection
            '''
            result = self._values.get("data_transfer_protection")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def rpc_protection(self) -> typing.Optional[builtins.str]:
            '''The Remote Procedure Call (RPC) protection setting configured on the HDFS cluster.

            This setting corresponds to your ``hadoop.rpc.protection`` setting in your ``core-site.xml`` file on your Hadoop cluster.

            :default: - "PRIVACY"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationhdfs-qopconfiguration.html#cfn-datasync-locationhdfs-qopconfiguration-rpcprotection
            '''
            result = self._values.get("rpc_protection")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QopConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationNFSMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "mount_options": "mountOptions",
        "on_prem_config": "onPremConfig",
        "server_hostname": "serverHostname",
        "subdirectory": "subdirectory",
        "tags": "tags",
    },
)
class CfnLocationNFSMixinProps:
    def __init__(
        self,
        *,
        mount_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLocationNFSPropsMixin.MountOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        on_prem_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLocationNFSPropsMixin.OnPremConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        server_hostname: typing.Optional[builtins.str] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnLocationNFSPropsMixin.

        :param mount_options: Specifies the options that DataSync can use to mount your NFS file server.
        :param on_prem_config: Specifies the Amazon Resource Name (ARN) of the DataSync agent that can connect to your NFS file server. You can specify more than one agent. For more information, see `Using multiple DataSync agents <https://docs.aws.amazon.com/datasync/latest/userguide/do-i-need-datasync-agent.html#multiple-agents>`_ .
        :param server_hostname: Specifies the DNS name or IP address (IPv4 or IPv6) of the NFS file server that your DataSync agent connects to.
        :param subdirectory: Specifies the export path in your NFS file server that you want DataSync to mount. This path (or a subdirectory of the path) is where DataSync transfers data to or from. For information on configuring an export for DataSync, see `Accessing NFS file servers <https://docs.aws.amazon.com/datasync/latest/userguide/create-nfs-location.html#accessing-nfs>`_ .
        :param tags: Specifies labels that help you categorize, filter, and search for your AWS resources. We recommend creating at least a name tag for your location.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationnfs.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
            
            cfn_location_nFSMixin_props = datasync_mixins.CfnLocationNFSMixinProps(
                mount_options=datasync_mixins.CfnLocationNFSPropsMixin.MountOptionsProperty(
                    version="version"
                ),
                on_prem_config=datasync_mixins.CfnLocationNFSPropsMixin.OnPremConfigProperty(
                    agent_arns=["agentArns"]
                ),
                server_hostname="serverHostname",
                subdirectory="subdirectory",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ada638f32c0f0f174bca979ed1ba88215f29cd914120d31600705c140ea07dfb)
            check_type(argname="argument mount_options", value=mount_options, expected_type=type_hints["mount_options"])
            check_type(argname="argument on_prem_config", value=on_prem_config, expected_type=type_hints["on_prem_config"])
            check_type(argname="argument server_hostname", value=server_hostname, expected_type=type_hints["server_hostname"])
            check_type(argname="argument subdirectory", value=subdirectory, expected_type=type_hints["subdirectory"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if mount_options is not None:
            self._values["mount_options"] = mount_options
        if on_prem_config is not None:
            self._values["on_prem_config"] = on_prem_config
        if server_hostname is not None:
            self._values["server_hostname"] = server_hostname
        if subdirectory is not None:
            self._values["subdirectory"] = subdirectory
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def mount_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLocationNFSPropsMixin.MountOptionsProperty"]]:
        '''Specifies the options that DataSync can use to mount your NFS file server.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationnfs.html#cfn-datasync-locationnfs-mountoptions
        '''
        result = self._values.get("mount_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLocationNFSPropsMixin.MountOptionsProperty"]], result)

    @builtins.property
    def on_prem_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLocationNFSPropsMixin.OnPremConfigProperty"]]:
        '''Specifies the Amazon Resource Name (ARN) of the DataSync agent that can connect to your NFS file server.

        You can specify more than one agent. For more information, see `Using multiple DataSync agents <https://docs.aws.amazon.com/datasync/latest/userguide/do-i-need-datasync-agent.html#multiple-agents>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationnfs.html#cfn-datasync-locationnfs-onpremconfig
        '''
        result = self._values.get("on_prem_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLocationNFSPropsMixin.OnPremConfigProperty"]], result)

    @builtins.property
    def server_hostname(self) -> typing.Optional[builtins.str]:
        '''Specifies the DNS name or IP address (IPv4 or IPv6) of the NFS file server that your DataSync agent connects to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationnfs.html#cfn-datasync-locationnfs-serverhostname
        '''
        result = self._values.get("server_hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''Specifies the export path in your NFS file server that you want DataSync to mount.

        This path (or a subdirectory of the path) is where DataSync transfers data to or from. For information on configuring an export for DataSync, see `Accessing NFS file servers <https://docs.aws.amazon.com/datasync/latest/userguide/create-nfs-location.html#accessing-nfs>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationnfs.html#cfn-datasync-locationnfs-subdirectory
        '''
        result = self._values.get("subdirectory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Specifies labels that help you categorize, filter, and search for your AWS resources.

        We recommend creating at least a name tag for your location.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationnfs.html#cfn-datasync-locationnfs-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLocationNFSMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLocationNFSPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationNFSPropsMixin",
):
    '''The ``AWS::DataSync::LocationNFS`` resource specifies a Network File System (NFS) file server that AWS DataSync can use as a transfer source or destination.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationnfs.html
    :cloudformationResource: AWS::DataSync::LocationNFS
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
        
        cfn_location_nFSProps_mixin = datasync_mixins.CfnLocationNFSPropsMixin(datasync_mixins.CfnLocationNFSMixinProps(
            mount_options=datasync_mixins.CfnLocationNFSPropsMixin.MountOptionsProperty(
                version="version"
            ),
            on_prem_config=datasync_mixins.CfnLocationNFSPropsMixin.OnPremConfigProperty(
                agent_arns=["agentArns"]
            ),
            server_hostname="serverHostname",
            subdirectory="subdirectory",
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
        props: typing.Union[CfnLocationNFSMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DataSync::LocationNFS``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49f478964494ffeb95b93101c9479a834025a966d819800e3fae90e1f45e0af9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__671cae39883f866987bd96781d9ae7430ea1ae8b15e0821615e32e580efb2df3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b764a79077c12cedef360b1304b7d603214d97821298769c6d27dfffe4daf9e3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLocationNFSMixinProps:
        return typing.cast(CfnLocationNFSMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationNFSPropsMixin.MountOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"version": "version"},
    )
    class MountOptionsProperty:
        def __init__(self, *, version: typing.Optional[builtins.str] = None) -> None:
            '''Specifies the options that DataSync can use to mount your NFS file server.

            :param version: Specifies the NFS version that you want DataSync to use when mounting your NFS share. If the server refuses to use the version specified, the task fails. You can specify the following options: - ``AUTOMATIC`` (default): DataSync chooses NFS version 4.1. - ``NFS3`` : Stateless protocol version that allows for asynchronous writes on the server. - ``NFSv4_0`` : Stateful, firewall-friendly protocol version that supports delegations and pseudo file systems. - ``NFSv4_1`` : Stateful protocol version that supports sessions, directory delegations, and parallel data processing. NFS version 4.1 also includes all features available in version 4.0. .. epigraph:: DataSync currently only supports NFS version 3 with Amazon FSx for NetApp ONTAP locations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationnfs-mountoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
                
                mount_options_property = datasync_mixins.CfnLocationNFSPropsMixin.MountOptionsProperty(
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e703d7f420543484e20dfc5e10e272415e866d1f7dcc7c31430fb795558df1c7)
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''Specifies the NFS version that you want DataSync to use when mounting your NFS share.

            If the server refuses to use the version specified, the task fails.

            You can specify the following options:

            - ``AUTOMATIC`` (default): DataSync chooses NFS version 4.1.
            - ``NFS3`` : Stateless protocol version that allows for asynchronous writes on the server.
            - ``NFSv4_0`` : Stateful, firewall-friendly protocol version that supports delegations and pseudo file systems.
            - ``NFSv4_1`` : Stateful protocol version that supports sessions, directory delegations, and parallel data processing. NFS version 4.1 also includes all features available in version 4.0.

            .. epigraph::

               DataSync currently only supports NFS version 3 with Amazon FSx for NetApp ONTAP locations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationnfs-mountoptions.html#cfn-datasync-locationnfs-mountoptions-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MountOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationNFSPropsMixin.OnPremConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"agent_arns": "agentArns"},
    )
    class OnPremConfigProperty:
        def __init__(
            self,
            *,
            agent_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The AWS DataSync agents that can connect to your Network File System (NFS) file server.

            :param agent_arns: The Amazon Resource Names (ARNs) of the DataSync agents that can connect to your NFS file server. You can specify more than one agent. For more information, see `Using multiple DataSync agents <https://docs.aws.amazon.com/datasync/latest/userguide/do-i-need-datasync-agent.html#multiple-agents>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationnfs-onpremconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
                
                on_prem_config_property = datasync_mixins.CfnLocationNFSPropsMixin.OnPremConfigProperty(
                    agent_arns=["agentArns"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__eb51a6f879a2d1e491c4ffd87d9a9c1b2ed8eb7cbd631b0d1fb1c06c899b1fc2)
                check_type(argname="argument agent_arns", value=agent_arns, expected_type=type_hints["agent_arns"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if agent_arns is not None:
                self._values["agent_arns"] = agent_arns

        @builtins.property
        def agent_arns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The Amazon Resource Names (ARNs) of the DataSync agents that can connect to your NFS file server.

            You can specify more than one agent. For more information, see `Using multiple DataSync agents <https://docs.aws.amazon.com/datasync/latest/userguide/do-i-need-datasync-agent.html#multiple-agents>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationnfs-onpremconfig.html#cfn-datasync-locationnfs-onpremconfig-agentarns
            '''
            result = self._values.get("agent_arns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OnPremConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationObjectStorageMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_key": "accessKey",
        "agent_arns": "agentArns",
        "bucket_name": "bucketName",
        "cmk_secret_config": "cmkSecretConfig",
        "custom_secret_config": "customSecretConfig",
        "secret_key": "secretKey",
        "server_certificate": "serverCertificate",
        "server_hostname": "serverHostname",
        "server_port": "serverPort",
        "server_protocol": "serverProtocol",
        "subdirectory": "subdirectory",
        "tags": "tags",
    },
)
class CfnLocationObjectStorageMixinProps:
    def __init__(
        self,
        *,
        access_key: typing.Optional[builtins.str] = None,
        agent_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        bucket_name: typing.Optional[builtins.str] = None,
        cmk_secret_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLocationObjectStoragePropsMixin.CmkSecretConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        custom_secret_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLocationObjectStoragePropsMixin.CustomSecretConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        secret_key: typing.Optional[builtins.str] = None,
        server_certificate: typing.Optional[builtins.str] = None,
        server_hostname: typing.Optional[builtins.str] = None,
        server_port: typing.Optional[jsii.Number] = None,
        server_protocol: typing.Optional[builtins.str] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnLocationObjectStoragePropsMixin.

        :param access_key: Specifies the access key (for example, a user name) if credentials are required to authenticate with the object storage server.
        :param agent_arns: (Optional) Specifies the Amazon Resource Names (ARNs) of the DataSync agents that can connect with your object storage system. If you are setting up an agentless cross-cloud transfer, you do not need to specify a value for this parameter. .. epigraph:: Make sure you configure this parameter correctly when you first create your storage location. You cannot add or remove agents from a storage location after you create it.
        :param bucket_name: Specifies the name of the object storage bucket involved in the transfer.
        :param cmk_secret_config: Specifies configuration information for a DataSync-managed secret, which includes the ``SecretKey`` that DataSync uses to access a specific object storage location, with a customer-managed AWS KMS key . When you include this paramater as part of a ``CreateLocationObjectStorage`` request, you provide only the KMS key ARN. DataSync uses this KMS key together with the value you specify for the ``SecretKey`` parameter to create a DataSync-managed secret to store the location access credentials. Make sure the DataSync has permission to access the KMS key that you specify. .. epigraph:: You can use either ``CmkSecretConfig`` (with ``SecretKey`` ) or ``CustomSecretConfig`` (without ``SecretKey`` ) to provide credentials for a ``CreateLocationObjectStorage`` request. Do not provide both parameters for the same request.
        :param custom_secret_config: Specifies configuration information for a customer-managed Secrets Manager secret where the secret key for a specific object storage location is stored in plain text. This configuration includes the secret ARN, and the ARN for an IAM role that provides access to the secret. .. epigraph:: You can use either ``CmkSecretConfig`` (with ``SecretKey`` ) or ``CustomSecretConfig`` (without ``SecretKey`` ) to provide credentials for a ``CreateLocationObjectStorage`` request. Do not provide both parameters for the same request.
        :param secret_key: Specifies the secret key (for example, a password) if credentials are required to authenticate with the object storage server. .. epigraph:: If you provide a secret using ``SecretKey`` , but do not provide secret configuration details using ``CmkSecretConfig`` or ``CustomSecretConfig`` , then DataSync stores the token using your AWS account's Secrets Manager secret.
        :param server_certificate: Specifies a certificate chain for DataSync to authenticate with your object storage system if the system uses a private or self-signed certificate authority (CA). You must specify a single ``.pem`` file with a full certificate chain (for example, ``file:///home/user/.ssh/object_storage_certificates.pem`` ). The certificate chain might include: - The object storage system's certificate - All intermediate certificates (if there are any) - The root certificate of the signing CA You can concatenate your certificates into a ``.pem`` file (which can be up to 32768 bytes before base64 encoding). The following example ``cat`` command creates an ``object_storage_certificates.pem`` file that includes three certificates: ``cat object_server_certificate.pem intermediate_certificate.pem ca_root_certificate.pem > object_storage_certificates.pem`` To use this parameter, configure ``ServerProtocol`` to ``HTTPS`` .
        :param server_hostname: Specifies the domain name or IP address (IPv4 or IPv6) of the object storage server that your DataSync agent connects to.
        :param server_port: Specifies the port that your object storage server accepts inbound network traffic on (for example, port 443).
        :param server_protocol: Specifies the protocol that your object storage server uses to communicate. If not specified, the default value is ``HTTPS`` .
        :param subdirectory: Specifies the object prefix for your object storage server. If this is a source location, DataSync only copies objects with this prefix. If this is a destination location, DataSync writes all objects with this prefix.
        :param tags: Specifies the key-value pair that represents a tag that you want to add to the resource. Tags can help you manage, filter, and search for your resources. We recommend creating a name tag for your location.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
            
            cfn_location_object_storage_mixin_props = datasync_mixins.CfnLocationObjectStorageMixinProps(
                access_key="accessKey",
                agent_arns=["agentArns"],
                bucket_name="bucketName",
                cmk_secret_config=datasync_mixins.CfnLocationObjectStoragePropsMixin.CmkSecretConfigProperty(
                    kms_key_arn="kmsKeyArn",
                    secret_arn="secretArn"
                ),
                custom_secret_config=datasync_mixins.CfnLocationObjectStoragePropsMixin.CustomSecretConfigProperty(
                    secret_access_role_arn="secretAccessRoleArn",
                    secret_arn="secretArn"
                ),
                secret_key="secretKey",
                server_certificate="serverCertificate",
                server_hostname="serverHostname",
                server_port=123,
                server_protocol="serverProtocol",
                subdirectory="subdirectory",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbe0ebd284440526d635f8eae1b7373d04b3939929aa541a2f6d5c6d738a7f7b)
            check_type(argname="argument access_key", value=access_key, expected_type=type_hints["access_key"])
            check_type(argname="argument agent_arns", value=agent_arns, expected_type=type_hints["agent_arns"])
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument cmk_secret_config", value=cmk_secret_config, expected_type=type_hints["cmk_secret_config"])
            check_type(argname="argument custom_secret_config", value=custom_secret_config, expected_type=type_hints["custom_secret_config"])
            check_type(argname="argument secret_key", value=secret_key, expected_type=type_hints["secret_key"])
            check_type(argname="argument server_certificate", value=server_certificate, expected_type=type_hints["server_certificate"])
            check_type(argname="argument server_hostname", value=server_hostname, expected_type=type_hints["server_hostname"])
            check_type(argname="argument server_port", value=server_port, expected_type=type_hints["server_port"])
            check_type(argname="argument server_protocol", value=server_protocol, expected_type=type_hints["server_protocol"])
            check_type(argname="argument subdirectory", value=subdirectory, expected_type=type_hints["subdirectory"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_key is not None:
            self._values["access_key"] = access_key
        if agent_arns is not None:
            self._values["agent_arns"] = agent_arns
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if cmk_secret_config is not None:
            self._values["cmk_secret_config"] = cmk_secret_config
        if custom_secret_config is not None:
            self._values["custom_secret_config"] = custom_secret_config
        if secret_key is not None:
            self._values["secret_key"] = secret_key
        if server_certificate is not None:
            self._values["server_certificate"] = server_certificate
        if server_hostname is not None:
            self._values["server_hostname"] = server_hostname
        if server_port is not None:
            self._values["server_port"] = server_port
        if server_protocol is not None:
            self._values["server_protocol"] = server_protocol
        if subdirectory is not None:
            self._values["subdirectory"] = subdirectory
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def access_key(self) -> typing.Optional[builtins.str]:
        '''Specifies the access key (for example, a user name) if credentials are required to authenticate with the object storage server.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-accesskey
        '''
        result = self._values.get("access_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def agent_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(Optional) Specifies the Amazon Resource Names (ARNs) of the DataSync agents that can connect with your object storage system.

        If you are setting up an agentless cross-cloud transfer, you do not need to specify a value for this parameter.
        .. epigraph::

           Make sure you configure this parameter correctly when you first create your storage location. You cannot add or remove agents from a storage location after you create it.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-agentarns
        '''
        result = self._values.get("agent_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the object storage bucket involved in the transfer.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-bucketname
        '''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cmk_secret_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLocationObjectStoragePropsMixin.CmkSecretConfigProperty"]]:
        '''Specifies configuration information for a DataSync-managed secret, which includes the ``SecretKey`` that DataSync uses to access a specific object storage location, with a customer-managed AWS KMS key .

        When you include this paramater as part of a ``CreateLocationObjectStorage`` request, you provide only the KMS key ARN. DataSync uses this KMS key together with the value you specify for the ``SecretKey`` parameter to create a DataSync-managed secret to store the location access credentials.

        Make sure the DataSync has permission to access the KMS key that you specify.
        .. epigraph::

           You can use either ``CmkSecretConfig`` (with ``SecretKey`` ) or ``CustomSecretConfig`` (without ``SecretKey`` ) to provide credentials for a ``CreateLocationObjectStorage`` request. Do not provide both parameters for the same request.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-cmksecretconfig
        '''
        result = self._values.get("cmk_secret_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLocationObjectStoragePropsMixin.CmkSecretConfigProperty"]], result)

    @builtins.property
    def custom_secret_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLocationObjectStoragePropsMixin.CustomSecretConfigProperty"]]:
        '''Specifies configuration information for a customer-managed Secrets Manager secret where the secret key for a specific object storage location is stored in plain text.

        This configuration includes the secret ARN, and the ARN for an IAM role that provides access to the secret.
        .. epigraph::

           You can use either ``CmkSecretConfig`` (with ``SecretKey`` ) or ``CustomSecretConfig`` (without ``SecretKey`` ) to provide credentials for a ``CreateLocationObjectStorage`` request. Do not provide both parameters for the same request.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-customsecretconfig
        '''
        result = self._values.get("custom_secret_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLocationObjectStoragePropsMixin.CustomSecretConfigProperty"]], result)

    @builtins.property
    def secret_key(self) -> typing.Optional[builtins.str]:
        '''Specifies the secret key (for example, a password) if credentials are required to authenticate with the object storage server.

        .. epigraph::

           If you provide a secret using ``SecretKey`` , but do not provide secret configuration details using ``CmkSecretConfig`` or ``CustomSecretConfig`` , then DataSync stores the token using your AWS account's Secrets Manager secret.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-secretkey
        '''
        result = self._values.get("secret_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_certificate(self) -> typing.Optional[builtins.str]:
        '''Specifies a certificate chain for DataSync to authenticate with your object storage system if the system uses a private or self-signed certificate authority (CA).

        You must specify a single ``.pem`` file with a full certificate chain (for example, ``file:///home/user/.ssh/object_storage_certificates.pem`` ).

        The certificate chain might include:

        - The object storage system's certificate
        - All intermediate certificates (if there are any)
        - The root certificate of the signing CA

        You can concatenate your certificates into a ``.pem`` file (which can be up to 32768 bytes before base64 encoding). The following example ``cat`` command creates an ``object_storage_certificates.pem`` file that includes three certificates:

        ``cat object_server_certificate.pem intermediate_certificate.pem ca_root_certificate.pem > object_storage_certificates.pem``

        To use this parameter, configure ``ServerProtocol`` to ``HTTPS`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-servercertificate
        '''
        result = self._values.get("server_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_hostname(self) -> typing.Optional[builtins.str]:
        '''Specifies the domain name or IP address (IPv4 or IPv6) of the object storage server that your DataSync agent connects to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-serverhostname
        '''
        result = self._values.get("server_hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_port(self) -> typing.Optional[jsii.Number]:
        '''Specifies the port that your object storage server accepts inbound network traffic on (for example, port 443).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-serverport
        '''
        result = self._values.get("server_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def server_protocol(self) -> typing.Optional[builtins.str]:
        '''Specifies the protocol that your object storage server uses to communicate.

        If not specified, the default value is ``HTTPS`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-serverprotocol
        '''
        result = self._values.get("server_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''Specifies the object prefix for your object storage server.

        If this is a source location, DataSync only copies objects with this prefix. If this is a destination location, DataSync writes all objects with this prefix.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-subdirectory
        '''
        result = self._values.get("subdirectory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Specifies the key-value pair that represents a tag that you want to add to the resource.

        Tags can help you manage, filter, and search for your resources. We recommend creating a name tag for your location.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLocationObjectStorageMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLocationObjectStoragePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationObjectStoragePropsMixin",
):
    '''The ``AWS::DataSync::LocationObjectStorage`` resource specifies an endpoint for a self-managed object storage bucket.

    For more information about self-managed object storage locations, see `Creating a Location for Object Storage <https://docs.aws.amazon.com/datasync/latest/userguide/create-object-location.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html
    :cloudformationResource: AWS::DataSync::LocationObjectStorage
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
        
        cfn_location_object_storage_props_mixin = datasync_mixins.CfnLocationObjectStoragePropsMixin(datasync_mixins.CfnLocationObjectStorageMixinProps(
            access_key="accessKey",
            agent_arns=["agentArns"],
            bucket_name="bucketName",
            cmk_secret_config=datasync_mixins.CfnLocationObjectStoragePropsMixin.CmkSecretConfigProperty(
                kms_key_arn="kmsKeyArn",
                secret_arn="secretArn"
            ),
            custom_secret_config=datasync_mixins.CfnLocationObjectStoragePropsMixin.CustomSecretConfigProperty(
                secret_access_role_arn="secretAccessRoleArn",
                secret_arn="secretArn"
            ),
            secret_key="secretKey",
            server_certificate="serverCertificate",
            server_hostname="serverHostname",
            server_port=123,
            server_protocol="serverProtocol",
            subdirectory="subdirectory",
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
        props: typing.Union[CfnLocationObjectStorageMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DataSync::LocationObjectStorage``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e789c05d1b4756ff600d44cb7bde66733dff21b5db8b90bdb7b3e545c523d12a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad905740c3cce3d6ffca2ca438b0a62ef07a052cfd39057dfbdd836187c699f2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__618ea8be1f7f7d2bf56013972da49d61c9e7bf6eb7436b700779df7b11de748f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLocationObjectStorageMixinProps:
        return typing.cast(CfnLocationObjectStorageMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationObjectStoragePropsMixin.CmkSecretConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"kms_key_arn": "kmsKeyArn", "secret_arn": "secretArn"},
    )
    class CmkSecretConfigProperty:
        def __init__(
            self,
            *,
            kms_key_arn: typing.Optional[builtins.str] = None,
            secret_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies configuration information for a DataSync-managed secret, such as an authentication token or secret key that DataSync uses to access a specific storage location, with a customer-managed AWS KMS key .

            .. epigraph::

               You can use either ``CmkSecretConfig`` or ``CustomSecretConfig`` to provide credentials for a ``CreateLocation`` request. Do not provide both parameters for the same request.

            :param kms_key_arn: Specifies the ARN for the customer-managed AWS KMS key that DataSync uses to encrypt the DataSync-managed secret stored for ``SecretArn`` . DataSync provides this key to AWS Secrets Manager .
            :param secret_arn: Specifies the ARN for the DataSync-managed AWS Secrets Manager secret that that is used to access a specific storage location. This property is generated by DataSync and is read-only. DataSync encrypts this secret with the KMS key that you specify for ``KmsKeyArn`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationobjectstorage-cmksecretconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
                
                cmk_secret_config_property = datasync_mixins.CfnLocationObjectStoragePropsMixin.CmkSecretConfigProperty(
                    kms_key_arn="kmsKeyArn",
                    secret_arn="secretArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8bfe345346efd3deb6aac94e9ff19c7aff7c46eb170fede8d4a4a080cd9250e7)
                check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kms_key_arn is not None:
                self._values["kms_key_arn"] = kms_key_arn
            if secret_arn is not None:
                self._values["secret_arn"] = secret_arn

        @builtins.property
        def kms_key_arn(self) -> typing.Optional[builtins.str]:
            '''Specifies the ARN for the customer-managed AWS KMS key that DataSync uses to encrypt the DataSync-managed secret stored for ``SecretArn`` .

            DataSync provides this key to AWS Secrets Manager .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationobjectstorage-cmksecretconfig.html#cfn-datasync-locationobjectstorage-cmksecretconfig-kmskeyarn
            '''
            result = self._values.get("kms_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secret_arn(self) -> typing.Optional[builtins.str]:
            '''Specifies the ARN for the DataSync-managed AWS Secrets Manager secret that that is used to access a specific storage location.

            This property is generated by DataSync and is read-only. DataSync encrypts this secret with the KMS key that you specify for ``KmsKeyArn`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationobjectstorage-cmksecretconfig.html#cfn-datasync-locationobjectstorage-cmksecretconfig-secretarn
            '''
            result = self._values.get("secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CmkSecretConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationObjectStoragePropsMixin.CustomSecretConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "secret_access_role_arn": "secretAccessRoleArn",
            "secret_arn": "secretArn",
        },
    )
    class CustomSecretConfigProperty:
        def __init__(
            self,
            *,
            secret_access_role_arn: typing.Optional[builtins.str] = None,
            secret_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies configuration information for a customer-managed Secrets Manager secret where a storage location authentication token or secret key is stored in plain text.

            This configuration includes the secret ARN, and the ARN for an IAM role that provides access to the secret.
            .. epigraph::

               You can use either ``CmkSecretConfig`` or ``CustomSecretConfig`` to provide credentials for a ``CreateLocation`` request. Do not provide both parameters for the same request.

            :param secret_access_role_arn: Specifies the ARN for the AWS Identity and Access Management role that DataSync uses to access the secret specified for ``SecretArn`` .
            :param secret_arn: Specifies the ARN for an AWS Secrets Manager secret.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationobjectstorage-customsecretconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
                
                custom_secret_config_property = datasync_mixins.CfnLocationObjectStoragePropsMixin.CustomSecretConfigProperty(
                    secret_access_role_arn="secretAccessRoleArn",
                    secret_arn="secretArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__39241196e53799d1361a71e778596a390aebba75c48ad47a9151f400fe523027)
                check_type(argname="argument secret_access_role_arn", value=secret_access_role_arn, expected_type=type_hints["secret_access_role_arn"])
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if secret_access_role_arn is not None:
                self._values["secret_access_role_arn"] = secret_access_role_arn
            if secret_arn is not None:
                self._values["secret_arn"] = secret_arn

        @builtins.property
        def secret_access_role_arn(self) -> typing.Optional[builtins.str]:
            '''Specifies the ARN for the AWS Identity and Access Management role that DataSync uses to access the secret specified for ``SecretArn`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationobjectstorage-customsecretconfig.html#cfn-datasync-locationobjectstorage-customsecretconfig-secretaccessrolearn
            '''
            result = self._values.get("secret_access_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secret_arn(self) -> typing.Optional[builtins.str]:
            '''Specifies the ARN for an AWS Secrets Manager secret.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationobjectstorage-customsecretconfig.html#cfn-datasync-locationobjectstorage-customsecretconfig-secretarn
            '''
            result = self._values.get("secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomSecretConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationObjectStoragePropsMixin.ManagedSecretConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"secret_arn": "secretArn"},
    )
    class ManagedSecretConfigProperty:
        def __init__(self, *, secret_arn: typing.Optional[builtins.str] = None) -> None:
            '''Specifies configuration information for a DataSync-managed secret, such as an authentication token or set of credentials that DataSync uses to access a specific transfer location.

            DataSync uses the default AWS -managed KMS key to encrypt this secret in AWS Secrets Manager .

            :param secret_arn: Specifies the ARN for an AWS Secrets Manager secret.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationobjectstorage-managedsecretconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
                
                managed_secret_config_property = datasync_mixins.CfnLocationObjectStoragePropsMixin.ManagedSecretConfigProperty(
                    secret_arn="secretArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1b71a9d5790f11e2ac1f1d619ce12a79dc5d33768ec161ba58a765ef6fb13d71)
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if secret_arn is not None:
                self._values["secret_arn"] = secret_arn

        @builtins.property
        def secret_arn(self) -> typing.Optional[builtins.str]:
            '''Specifies the ARN for an AWS Secrets Manager secret.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationobjectstorage-managedsecretconfig.html#cfn-datasync-locationobjectstorage-managedsecretconfig-secretarn
            '''
            result = self._values.get("secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ManagedSecretConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationS3MixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "s3_bucket_arn": "s3BucketArn",
        "s3_config": "s3Config",
        "s3_storage_class": "s3StorageClass",
        "subdirectory": "subdirectory",
        "tags": "tags",
    },
)
class CfnLocationS3MixinProps:
    def __init__(
        self,
        *,
        s3_bucket_arn: typing.Optional[builtins.str] = None,
        s3_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLocationS3PropsMixin.S3ConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        s3_storage_class: typing.Optional[builtins.str] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnLocationS3PropsMixin.

        :param s3_bucket_arn: The ARN of the Amazon S3 bucket.
        :param s3_config: The Amazon Resource Name (ARN) of the AWS Identity and Access Management (IAM) role that is used to access an Amazon S3 bucket. For detailed information about using such a role, see `Creating a Location for Amazon S3 <https://docs.aws.amazon.com/datasync/latest/userguide/working-with-locations.html#create-s3-location>`_ in the *AWS DataSync User Guide* .
        :param s3_storage_class: The Amazon S3 storage class that you want to store your files in when this location is used as a task destination. For buckets in AWS Regions , the storage class defaults to S3 Standard. For more information about S3 storage classes, see `Amazon S3 Storage Classes <https://docs.aws.amazon.com/s3/storage-classes/>`_ . Some storage classes have behaviors that can affect your S3 storage costs. For detailed information, see `Considerations When Working with Amazon S3 Storage Classes in DataSync <https://docs.aws.amazon.com/datasync/latest/userguide/create-s3-location.html#using-storage-classes>`_ . Default: - "STANDARD"
        :param subdirectory: Specifies a prefix in the S3 bucket that DataSync reads from or writes to (depending on whether the bucket is a source or destination location). .. epigraph:: DataSync can't transfer objects with a prefix that begins with a slash ( ``/`` ) or includes ``//`` , ``/./`` , or ``/../`` patterns. For example: - ``/photos`` - ``photos//2006/January`` - ``photos/./2006/February`` - ``photos/../2006/March``
        :param tags: Specifies labels that help you categorize, filter, and search for your AWS resources. We recommend creating at least a name tag for your transfer location.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locations3.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
            
            cfn_location_s3_mixin_props = datasync_mixins.CfnLocationS3MixinProps(
                s3_bucket_arn="s3BucketArn",
                s3_config=datasync_mixins.CfnLocationS3PropsMixin.S3ConfigProperty(
                    bucket_access_role_arn="bucketAccessRoleArn"
                ),
                s3_storage_class="s3StorageClass",
                subdirectory="subdirectory",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__656eb6bb026f0c3f34441309f36f73fe36d3d24858ceecf249da584b3c461938)
            check_type(argname="argument s3_bucket_arn", value=s3_bucket_arn, expected_type=type_hints["s3_bucket_arn"])
            check_type(argname="argument s3_config", value=s3_config, expected_type=type_hints["s3_config"])
            check_type(argname="argument s3_storage_class", value=s3_storage_class, expected_type=type_hints["s3_storage_class"])
            check_type(argname="argument subdirectory", value=subdirectory, expected_type=type_hints["subdirectory"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if s3_bucket_arn is not None:
            self._values["s3_bucket_arn"] = s3_bucket_arn
        if s3_config is not None:
            self._values["s3_config"] = s3_config
        if s3_storage_class is not None:
            self._values["s3_storage_class"] = s3_storage_class
        if subdirectory is not None:
            self._values["subdirectory"] = subdirectory
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def s3_bucket_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the Amazon S3 bucket.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locations3.html#cfn-datasync-locations3-s3bucketarn
        '''
        result = self._values.get("s3_bucket_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLocationS3PropsMixin.S3ConfigProperty"]]:
        '''The Amazon Resource Name (ARN) of the AWS Identity and Access Management (IAM) role that is used to access an Amazon S3 bucket.

        For detailed information about using such a role, see `Creating a Location for Amazon S3 <https://docs.aws.amazon.com/datasync/latest/userguide/working-with-locations.html#create-s3-location>`_ in the *AWS DataSync User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locations3.html#cfn-datasync-locations3-s3config
        '''
        result = self._values.get("s3_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLocationS3PropsMixin.S3ConfigProperty"]], result)

    @builtins.property
    def s3_storage_class(self) -> typing.Optional[builtins.str]:
        '''The Amazon S3 storage class that you want to store your files in when this location is used as a task destination.

        For buckets in AWS Regions , the storage class defaults to S3 Standard.

        For more information about S3 storage classes, see `Amazon S3 Storage Classes <https://docs.aws.amazon.com/s3/storage-classes/>`_ . Some storage classes have behaviors that can affect your S3 storage costs. For detailed information, see `Considerations When Working with Amazon S3 Storage Classes in DataSync <https://docs.aws.amazon.com/datasync/latest/userguide/create-s3-location.html#using-storage-classes>`_ .

        :default: - "STANDARD"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locations3.html#cfn-datasync-locations3-s3storageclass
        '''
        result = self._values.get("s3_storage_class")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''Specifies a prefix in the S3 bucket that DataSync reads from or writes to (depending on whether the bucket is a source or destination location).

        .. epigraph::

           DataSync can't transfer objects with a prefix that begins with a slash ( ``/`` ) or includes ``//`` , ``/./`` , or ``/../`` patterns. For example:

           - ``/photos``
           - ``photos//2006/January``
           - ``photos/./2006/February``
           - ``photos/../2006/March``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locations3.html#cfn-datasync-locations3-subdirectory
        '''
        result = self._values.get("subdirectory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Specifies labels that help you categorize, filter, and search for your AWS resources.

        We recommend creating at least a name tag for your transfer location.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locations3.html#cfn-datasync-locations3-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLocationS3MixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLocationS3PropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationS3PropsMixin",
):
    '''The ``AWS::DataSync::LocationS3`` resource specifies an endpoint for an Amazon S3 bucket.

    For more information, see the `*AWS DataSync User Guide* <https://docs.aws.amazon.com/datasync/latest/userguide/create-s3-location.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locations3.html
    :cloudformationResource: AWS::DataSync::LocationS3
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
        
        cfn_location_s3_props_mixin = datasync_mixins.CfnLocationS3PropsMixin(datasync_mixins.CfnLocationS3MixinProps(
            s3_bucket_arn="s3BucketArn",
            s3_config=datasync_mixins.CfnLocationS3PropsMixin.S3ConfigProperty(
                bucket_access_role_arn="bucketAccessRoleArn"
            ),
            s3_storage_class="s3StorageClass",
            subdirectory="subdirectory",
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
        props: typing.Union[CfnLocationS3MixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DataSync::LocationS3``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__415c0d71ed755061dad92a43d06b3447026976fa22a594224f159ff3e6c22936)
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
            type_hints = typing.get_type_hints(_typecheckingstub__92e047460a21fa9c0107c94f41635712ad431b6c29595072943fcce763f9cdc7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cafdae1aef2d6882140388fddf767ffd112c8debe8aef68ceb30998797ed73cd)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLocationS3MixinProps:
        return typing.cast(CfnLocationS3MixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationS3PropsMixin.S3ConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket_access_role_arn": "bucketAccessRoleArn"},
    )
    class S3ConfigProperty:
        def __init__(
            self,
            *,
            bucket_access_role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the Amazon Resource Name (ARN) of the AWS Identity and Access Management (IAM) role that DataSync uses to access your S3 bucket.

            For more information, see `Providing DataSync access to S3 buckets <https://docs.aws.amazon.com/datasync/latest/userguide/create-s3-location.html#create-s3-location-access>`_ .

            :param bucket_access_role_arn: Specifies the ARN of the IAM role that DataSync uses to access your S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locations3-s3config.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
                
                s3_config_property = datasync_mixins.CfnLocationS3PropsMixin.S3ConfigProperty(
                    bucket_access_role_arn="bucketAccessRoleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__644bbf37d26e2680a087414f9f8732d79a89aacf3332d3ba59a1ec95eb0c5bb7)
                check_type(argname="argument bucket_access_role_arn", value=bucket_access_role_arn, expected_type=type_hints["bucket_access_role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_access_role_arn is not None:
                self._values["bucket_access_role_arn"] = bucket_access_role_arn

        @builtins.property
        def bucket_access_role_arn(self) -> typing.Optional[builtins.str]:
            '''Specifies the ARN of the IAM role that DataSync uses to access your S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locations3-s3config.html#cfn-datasync-locations3-s3config-bucketaccessrolearn
            '''
            result = self._values.get("bucket_access_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3ConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationSMBMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "agent_arns": "agentArns",
        "authentication_type": "authenticationType",
        "cmk_secret_config": "cmkSecretConfig",
        "custom_secret_config": "customSecretConfig",
        "dns_ip_addresses": "dnsIpAddresses",
        "domain": "domain",
        "kerberos_keytab": "kerberosKeytab",
        "kerberos_krb5_conf": "kerberosKrb5Conf",
        "kerberos_principal": "kerberosPrincipal",
        "mount_options": "mountOptions",
        "password": "password",
        "server_hostname": "serverHostname",
        "subdirectory": "subdirectory",
        "tags": "tags",
        "user": "user",
    },
)
class CfnLocationSMBMixinProps:
    def __init__(
        self,
        *,
        agent_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        authentication_type: typing.Optional[builtins.str] = None,
        cmk_secret_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLocationSMBPropsMixin.CmkSecretConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        custom_secret_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLocationSMBPropsMixin.CustomSecretConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        dns_ip_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        domain: typing.Optional[builtins.str] = None,
        kerberos_keytab: typing.Optional[builtins.str] = None,
        kerberos_krb5_conf: typing.Optional[builtins.str] = None,
        kerberos_principal: typing.Optional[builtins.str] = None,
        mount_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLocationSMBPropsMixin.MountOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        password: typing.Optional[builtins.str] = None,
        server_hostname: typing.Optional[builtins.str] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        user: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnLocationSMBPropsMixin.

        :param agent_arns: Specifies the DataSync agent (or agents) that can connect to your SMB file server. You specify an agent by using its Amazon Resource Name (ARN).
        :param authentication_type: The authentication mode used to determine identity of user.
        :param cmk_secret_config: Specifies configuration information for a DataSync-managed secret, such as an authentication token or secret key that DataSync uses to access a specific storage location, with a customer-managed AWS KMS key . .. epigraph:: You can use either ``CmkSecretConfig`` or ``CustomSecretConfig`` to provide credentials for a ``CreateLocation`` request. Do not provide both parameters for the same request.
        :param custom_secret_config: Specifies configuration information for a customer-managed Secrets Manager secret where a storage location authentication token or secret key is stored in plain text. This configuration includes the secret ARN, and the ARN for an IAM role that provides access to the secret. .. epigraph:: You can use either ``CmkSecretConfig`` or ``CustomSecretConfig`` to provide credentials for a ``CreateLocation`` request. Do not provide both parameters for the same request.
        :param dns_ip_addresses: Specifies the IPv4 addresses for the DNS servers that your SMB file server belongs to. This parameter applies only if AuthenticationType is set to KERBEROS. If you have multiple domains in your environment, configuring this parameter makes sure that DataSync connects to the right SMB file server.
        :param domain: Specifies the Windows domain name that your SMB file server belongs to. This parameter applies only if ``AuthenticationType`` is set to ``NTLM`` . If you have multiple domains in your environment, configuring this parameter makes sure that DataSync connects to the right file server.
        :param kerberos_keytab: The Base64 string representation of the Keytab file. Specifies your Kerberos key table (keytab) file, which includes mappings between your service principal name (SPN) and encryption keys. To avoid task execution errors, make sure that the SPN in the keytab file matches exactly what you specify for KerberosPrincipal and in your krb5.conf file.
        :param kerberos_krb5_conf: The string representation of the Krb5Conf file, or the presigned URL to access the Krb5.conf file within an S3 bucket. Specifies a Kerberos configuration file (krb5.conf) that defines your Kerberos realm configuration. To avoid task execution errors, make sure that the service principal name (SPN) in the krb5.conf file matches exactly what you specify for KerberosPrincipal and in your keytab file.
        :param kerberos_principal: Specifies a service principal name (SPN), which is an identity in your Kerberos realm that has permission to access the files, folders, and file metadata in your SMB file server. SPNs are case sensitive and must include a prepended cifs/. For example, an SPN might look like cifs/kerberosuser@EXAMPLE.COM. Your task execution will fail if the SPN that you provide for this parameter doesn't match exactly what's in your keytab or krb5.conf files.
        :param mount_options: Specifies the version of the SMB protocol that DataSync uses to access your SMB file server.
        :param password: Specifies the password of the user who can mount your SMB file server and has permission to access the files and folders involved in your transfer. This parameter applies only if ``AuthenticationType`` is set to ``NTLM`` .
        :param server_hostname: Specifies the domain name or IP address (IPv4 or IPv6) of the SMB file server that your DataSync agent connects to. .. epigraph:: If you're using Kerberos authentication, you must specify a domain name.
        :param subdirectory: Specifies the name of the share exported by your SMB file server where DataSync will read or write data. You can include a subdirectory in the share path (for example, ``/path/to/subdirectory`` ). Make sure that other SMB clients in your network can also mount this path. To copy all data in the subdirectory, DataSync must be able to mount the SMB share and access all of its data. For more information, see `Providing DataSync access to SMB file servers <https://docs.aws.amazon.com/datasync/latest/userguide/create-smb-location.html#configuring-smb-permissions>`_ .
        :param tags: Specifies labels that help you categorize, filter, and search for your AWS resources. We recommend creating at least a name tag for your location.
        :param user: Specifies the user that can mount and access the files, folders, and file metadata in your SMB file server. This parameter applies only if ``AuthenticationType`` is set to ``NTLM`` . For information about choosing a user with the right level of access for your transfer, see `Providing DataSync access to SMB file servers <https://docs.aws.amazon.com/datasync/latest/userguide/create-smb-location.html#configuring-smb-permissions>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
            
            cfn_location_sMBMixin_props = datasync_mixins.CfnLocationSMBMixinProps(
                agent_arns=["agentArns"],
                authentication_type="authenticationType",
                cmk_secret_config=datasync_mixins.CfnLocationSMBPropsMixin.CmkSecretConfigProperty(
                    kms_key_arn="kmsKeyArn",
                    secret_arn="secretArn"
                ),
                custom_secret_config=datasync_mixins.CfnLocationSMBPropsMixin.CustomSecretConfigProperty(
                    secret_access_role_arn="secretAccessRoleArn",
                    secret_arn="secretArn"
                ),
                dns_ip_addresses=["dnsIpAddresses"],
                domain="domain",
                kerberos_keytab="kerberosKeytab",
                kerberos_krb5_conf="kerberosKrb5Conf",
                kerberos_principal="kerberosPrincipal",
                mount_options=datasync_mixins.CfnLocationSMBPropsMixin.MountOptionsProperty(
                    version="version"
                ),
                password="password",
                server_hostname="serverHostname",
                subdirectory="subdirectory",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                user="user"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7d429531019a939be774c6ae4a4ca85dc87c258d2542dadc14546d4a9235e5f)
            check_type(argname="argument agent_arns", value=agent_arns, expected_type=type_hints["agent_arns"])
            check_type(argname="argument authentication_type", value=authentication_type, expected_type=type_hints["authentication_type"])
            check_type(argname="argument cmk_secret_config", value=cmk_secret_config, expected_type=type_hints["cmk_secret_config"])
            check_type(argname="argument custom_secret_config", value=custom_secret_config, expected_type=type_hints["custom_secret_config"])
            check_type(argname="argument dns_ip_addresses", value=dns_ip_addresses, expected_type=type_hints["dns_ip_addresses"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument kerberos_keytab", value=kerberos_keytab, expected_type=type_hints["kerberos_keytab"])
            check_type(argname="argument kerberos_krb5_conf", value=kerberos_krb5_conf, expected_type=type_hints["kerberos_krb5_conf"])
            check_type(argname="argument kerberos_principal", value=kerberos_principal, expected_type=type_hints["kerberos_principal"])
            check_type(argname="argument mount_options", value=mount_options, expected_type=type_hints["mount_options"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument server_hostname", value=server_hostname, expected_type=type_hints["server_hostname"])
            check_type(argname="argument subdirectory", value=subdirectory, expected_type=type_hints["subdirectory"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if agent_arns is not None:
            self._values["agent_arns"] = agent_arns
        if authentication_type is not None:
            self._values["authentication_type"] = authentication_type
        if cmk_secret_config is not None:
            self._values["cmk_secret_config"] = cmk_secret_config
        if custom_secret_config is not None:
            self._values["custom_secret_config"] = custom_secret_config
        if dns_ip_addresses is not None:
            self._values["dns_ip_addresses"] = dns_ip_addresses
        if domain is not None:
            self._values["domain"] = domain
        if kerberos_keytab is not None:
            self._values["kerberos_keytab"] = kerberos_keytab
        if kerberos_krb5_conf is not None:
            self._values["kerberos_krb5_conf"] = kerberos_krb5_conf
        if kerberos_principal is not None:
            self._values["kerberos_principal"] = kerberos_principal
        if mount_options is not None:
            self._values["mount_options"] = mount_options
        if password is not None:
            self._values["password"] = password
        if server_hostname is not None:
            self._values["server_hostname"] = server_hostname
        if subdirectory is not None:
            self._values["subdirectory"] = subdirectory
        if tags is not None:
            self._values["tags"] = tags
        if user is not None:
            self._values["user"] = user

    @builtins.property
    def agent_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the DataSync agent (or agents) that can connect to your SMB file server.

        You specify an agent by using its Amazon Resource Name (ARN).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-agentarns
        '''
        result = self._values.get("agent_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def authentication_type(self) -> typing.Optional[builtins.str]:
        '''The authentication mode used to determine identity of user.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-authenticationtype
        '''
        result = self._values.get("authentication_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cmk_secret_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLocationSMBPropsMixin.CmkSecretConfigProperty"]]:
        '''Specifies configuration information for a DataSync-managed secret, such as an authentication token or secret key that DataSync uses to access a specific storage location, with a customer-managed AWS KMS key .

        .. epigraph::

           You can use either ``CmkSecretConfig`` or ``CustomSecretConfig`` to provide credentials for a ``CreateLocation`` request. Do not provide both parameters for the same request.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-cmksecretconfig
        '''
        result = self._values.get("cmk_secret_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLocationSMBPropsMixin.CmkSecretConfigProperty"]], result)

    @builtins.property
    def custom_secret_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLocationSMBPropsMixin.CustomSecretConfigProperty"]]:
        '''Specifies configuration information for a customer-managed Secrets Manager secret where a storage location authentication token or secret key is stored in plain text.

        This configuration includes the secret ARN, and the ARN for an IAM role that provides access to the secret.
        .. epigraph::

           You can use either ``CmkSecretConfig`` or ``CustomSecretConfig`` to provide credentials for a ``CreateLocation`` request. Do not provide both parameters for the same request.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-customsecretconfig
        '''
        result = self._values.get("custom_secret_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLocationSMBPropsMixin.CustomSecretConfigProperty"]], result)

    @builtins.property
    def dns_ip_addresses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the IPv4 addresses for the DNS servers that your SMB file server belongs to.

        This parameter applies only if AuthenticationType is set to KERBEROS. If you have multiple domains in your environment, configuring this parameter makes sure that DataSync connects to the right SMB file server.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-dnsipaddresses
        '''
        result = self._values.get("dns_ip_addresses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def domain(self) -> typing.Optional[builtins.str]:
        '''Specifies the Windows domain name that your SMB file server belongs to.

        This parameter applies only if ``AuthenticationType`` is set to ``NTLM`` .

        If you have multiple domains in your environment, configuring this parameter makes sure that DataSync connects to the right file server.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-domain
        '''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kerberos_keytab(self) -> typing.Optional[builtins.str]:
        '''The Base64 string representation of the Keytab file.

        Specifies your Kerberos key table (keytab) file, which includes mappings between your service principal name (SPN) and encryption keys. To avoid task execution errors, make sure that the SPN in the keytab file matches exactly what you specify for KerberosPrincipal and in your krb5.conf file.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-kerberoskeytab
        '''
        result = self._values.get("kerberos_keytab")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kerberos_krb5_conf(self) -> typing.Optional[builtins.str]:
        '''The string representation of the Krb5Conf file, or the presigned URL to access the Krb5.conf file within an S3 bucket. Specifies a Kerberos configuration file (krb5.conf) that defines your Kerberos realm configuration. To avoid task execution errors, make sure that the service principal name (SPN) in the krb5.conf file matches exactly what you specify for KerberosPrincipal and in your keytab file.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-kerberoskrb5conf
        '''
        result = self._values.get("kerberos_krb5_conf")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kerberos_principal(self) -> typing.Optional[builtins.str]:
        '''Specifies a service principal name (SPN), which is an identity in your Kerberos realm that has permission to access the files, folders, and file metadata in your SMB file server.

        SPNs are case sensitive and must include a prepended cifs/. For example, an SPN might look like cifs/kerberosuser@EXAMPLE.COM. Your task execution will fail if the SPN that you provide for this parameter doesn't match exactly what's in your keytab or krb5.conf files.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-kerberosprincipal
        '''
        result = self._values.get("kerberos_principal")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mount_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLocationSMBPropsMixin.MountOptionsProperty"]]:
        '''Specifies the version of the SMB protocol that DataSync uses to access your SMB file server.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-mountoptions
        '''
        result = self._values.get("mount_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLocationSMBPropsMixin.MountOptionsProperty"]], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Specifies the password of the user who can mount your SMB file server and has permission to access the files and folders involved in your transfer.

        This parameter applies only if ``AuthenticationType`` is set to ``NTLM`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-password
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_hostname(self) -> typing.Optional[builtins.str]:
        '''Specifies the domain name or IP address (IPv4 or IPv6) of the SMB file server that your DataSync agent connects to.

        .. epigraph::

           If you're using Kerberos authentication, you must specify a domain name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-serverhostname
        '''
        result = self._values.get("server_hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the share exported by your SMB file server where DataSync will read or write data.

        You can include a subdirectory in the share path (for example, ``/path/to/subdirectory`` ). Make sure that other SMB clients in your network can also mount this path.

        To copy all data in the subdirectory, DataSync must be able to mount the SMB share and access all of its data. For more information, see `Providing DataSync access to SMB file servers <https://docs.aws.amazon.com/datasync/latest/userguide/create-smb-location.html#configuring-smb-permissions>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-subdirectory
        '''
        result = self._values.get("subdirectory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Specifies labels that help you categorize, filter, and search for your AWS resources.

        We recommend creating at least a name tag for your location.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def user(self) -> typing.Optional[builtins.str]:
        '''Specifies the user that can mount and access the files, folders, and file metadata in your SMB file server.

        This parameter applies only if ``AuthenticationType`` is set to ``NTLM`` .

        For information about choosing a user with the right level of access for your transfer, see `Providing DataSync access to SMB file servers <https://docs.aws.amazon.com/datasync/latest/userguide/create-smb-location.html#configuring-smb-permissions>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-user
        '''
        result = self._values.get("user")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLocationSMBMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLocationSMBPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationSMBPropsMixin",
):
    '''The ``AWS::DataSync::LocationSMB`` resource specifies a Server Message Block (SMB) location that AWS DataSync can use as a transfer source or destination.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html
    :cloudformationResource: AWS::DataSync::LocationSMB
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
        
        cfn_location_sMBProps_mixin = datasync_mixins.CfnLocationSMBPropsMixin(datasync_mixins.CfnLocationSMBMixinProps(
            agent_arns=["agentArns"],
            authentication_type="authenticationType",
            cmk_secret_config=datasync_mixins.CfnLocationSMBPropsMixin.CmkSecretConfigProperty(
                kms_key_arn="kmsKeyArn",
                secret_arn="secretArn"
            ),
            custom_secret_config=datasync_mixins.CfnLocationSMBPropsMixin.CustomSecretConfigProperty(
                secret_access_role_arn="secretAccessRoleArn",
                secret_arn="secretArn"
            ),
            dns_ip_addresses=["dnsIpAddresses"],
            domain="domain",
            kerberos_keytab="kerberosKeytab",
            kerberos_krb5_conf="kerberosKrb5Conf",
            kerberos_principal="kerberosPrincipal",
            mount_options=datasync_mixins.CfnLocationSMBPropsMixin.MountOptionsProperty(
                version="version"
            ),
            password="password",
            server_hostname="serverHostname",
            subdirectory="subdirectory",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            user="user"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnLocationSMBMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DataSync::LocationSMB``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3f3a18717cf39ef1d7e4f2416b655db54c978709f67d34437e5e3bce5175b75)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4263f4fb101808df8a91a9fc3e164cc1546e206598743760e5e3afbe95a78d4e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69f836fd342c50c89773448e71d40ae19261f67601ba772930a8813fbaf8ba09)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLocationSMBMixinProps:
        return typing.cast(CfnLocationSMBMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationSMBPropsMixin.CmkSecretConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"kms_key_arn": "kmsKeyArn", "secret_arn": "secretArn"},
    )
    class CmkSecretConfigProperty:
        def __init__(
            self,
            *,
            kms_key_arn: typing.Optional[builtins.str] = None,
            secret_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies configuration information for a DataSync-managed secret, such as an authentication token or secret key that DataSync uses to access a specific storage location, with a customer-managed AWS KMS key .

            .. epigraph::

               You can use either ``CmkSecretConfig`` or ``CustomSecretConfig`` to provide credentials for a ``CreateLocation`` request. Do not provide both parameters for the same request.

            :param kms_key_arn: Specifies the ARN for the customer-managed AWS KMS key that DataSync uses to encrypt the DataSync-managed secret stored for ``SecretArn`` . DataSync provides this key to AWS Secrets Manager .
            :param secret_arn: Specifies the ARN for the DataSync-managed AWS Secrets Manager secret that that is used to access a specific storage location. This property is generated by DataSync and is read-only. DataSync encrypts this secret with the KMS key that you specify for ``KmsKeyArn`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationsmb-cmksecretconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
                
                cmk_secret_config_property = datasync_mixins.CfnLocationSMBPropsMixin.CmkSecretConfigProperty(
                    kms_key_arn="kmsKeyArn",
                    secret_arn="secretArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5469c1fbd310b23a62274a06930d7c86228cd37e3e6e581c674c5704fd9b59ed)
                check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kms_key_arn is not None:
                self._values["kms_key_arn"] = kms_key_arn
            if secret_arn is not None:
                self._values["secret_arn"] = secret_arn

        @builtins.property
        def kms_key_arn(self) -> typing.Optional[builtins.str]:
            '''Specifies the ARN for the customer-managed AWS KMS key that DataSync uses to encrypt the DataSync-managed secret stored for ``SecretArn`` .

            DataSync provides this key to AWS Secrets Manager .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationsmb-cmksecretconfig.html#cfn-datasync-locationsmb-cmksecretconfig-kmskeyarn
            '''
            result = self._values.get("kms_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secret_arn(self) -> typing.Optional[builtins.str]:
            '''Specifies the ARN for the DataSync-managed AWS Secrets Manager secret that that is used to access a specific storage location.

            This property is generated by DataSync and is read-only. DataSync encrypts this secret with the KMS key that you specify for ``KmsKeyArn`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationsmb-cmksecretconfig.html#cfn-datasync-locationsmb-cmksecretconfig-secretarn
            '''
            result = self._values.get("secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CmkSecretConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationSMBPropsMixin.CustomSecretConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "secret_access_role_arn": "secretAccessRoleArn",
            "secret_arn": "secretArn",
        },
    )
    class CustomSecretConfigProperty:
        def __init__(
            self,
            *,
            secret_access_role_arn: typing.Optional[builtins.str] = None,
            secret_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies configuration information for a customer-managed Secrets Manager secret where a storage location authentication token or secret key is stored in plain text.

            This configuration includes the secret ARN, and the ARN for an IAM role that provides access to the secret.
            .. epigraph::

               You can use either ``CmkSecretConfig`` or ``CustomSecretConfig`` to provide credentials for a ``CreateLocation`` request. Do not provide both parameters for the same request.

            :param secret_access_role_arn: Specifies the ARN for the AWS Identity and Access Management role that DataSync uses to access the secret specified for ``SecretArn`` .
            :param secret_arn: Specifies the ARN for an AWS Secrets Manager secret.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationsmb-customsecretconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
                
                custom_secret_config_property = datasync_mixins.CfnLocationSMBPropsMixin.CustomSecretConfigProperty(
                    secret_access_role_arn="secretAccessRoleArn",
                    secret_arn="secretArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__851d7b600fa1338b3f6f0b57edd688e5f47f5e17ade25dcfc8057350ea58e1a2)
                check_type(argname="argument secret_access_role_arn", value=secret_access_role_arn, expected_type=type_hints["secret_access_role_arn"])
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if secret_access_role_arn is not None:
                self._values["secret_access_role_arn"] = secret_access_role_arn
            if secret_arn is not None:
                self._values["secret_arn"] = secret_arn

        @builtins.property
        def secret_access_role_arn(self) -> typing.Optional[builtins.str]:
            '''Specifies the ARN for the AWS Identity and Access Management role that DataSync uses to access the secret specified for ``SecretArn`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationsmb-customsecretconfig.html#cfn-datasync-locationsmb-customsecretconfig-secretaccessrolearn
            '''
            result = self._values.get("secret_access_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secret_arn(self) -> typing.Optional[builtins.str]:
            '''Specifies the ARN for an AWS Secrets Manager secret.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationsmb-customsecretconfig.html#cfn-datasync-locationsmb-customsecretconfig-secretarn
            '''
            result = self._values.get("secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomSecretConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationSMBPropsMixin.ManagedSecretConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"secret_arn": "secretArn"},
    )
    class ManagedSecretConfigProperty:
        def __init__(self, *, secret_arn: typing.Optional[builtins.str] = None) -> None:
            '''Specifies configuration information for a DataSync-managed secret, such as an authentication token or set of credentials that DataSync uses to access a specific transfer location.

            DataSync uses the default AWS -managed KMS key to encrypt this secret in AWS Secrets Manager .

            :param secret_arn: Specifies the ARN for an AWS Secrets Manager secret.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationsmb-managedsecretconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
                
                managed_secret_config_property = datasync_mixins.CfnLocationSMBPropsMixin.ManagedSecretConfigProperty(
                    secret_arn="secretArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5f4ba9fcfa4421bb729413b89333f25150d9a3d0327531f7e617f263b631ae95)
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if secret_arn is not None:
                self._values["secret_arn"] = secret_arn

        @builtins.property
        def secret_arn(self) -> typing.Optional[builtins.str]:
            '''Specifies the ARN for an AWS Secrets Manager secret.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationsmb-managedsecretconfig.html#cfn-datasync-locationsmb-managedsecretconfig-secretarn
            '''
            result = self._values.get("secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ManagedSecretConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnLocationSMBPropsMixin.MountOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"version": "version"},
    )
    class MountOptionsProperty:
        def __init__(self, *, version: typing.Optional[builtins.str] = None) -> None:
            '''Specifies the version of the SMB protocol that DataSync uses to access your SMB file server.

            :param version: By default, DataSync automatically chooses an SMB protocol version based on negotiation with your SMB file server. You also can configure DataSync to use a specific SMB version, but we recommend doing this only if DataSync has trouble negotiating with the SMB file server automatically. These are the following options for configuring the SMB version: - ``AUTOMATIC`` (default): DataSync and the SMB file server negotiate the highest version of SMB that they mutually support between 2.1 and 3.1.1. This is the recommended option. If you instead choose a specific version that your file server doesn't support, you may get an ``Operation Not Supported`` error. - ``SMB3`` : Restricts the protocol negotiation to only SMB version 3.0.2. - ``SMB2`` : Restricts the protocol negotiation to only SMB version 2.1. - ``SMB2_0`` : Restricts the protocol negotiation to only SMB version 2.0. - ``SMB1`` : Restricts the protocol negotiation to only SMB version 1.0. .. epigraph:: The ``SMB1`` option isn't available when `creating an Amazon FSx for NetApp ONTAP location <https://docs.aws.amazon.com/datasync/latest/userguide/API_CreateLocationFsxOntap.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationsmb-mountoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
                
                mount_options_property = datasync_mixins.CfnLocationSMBPropsMixin.MountOptionsProperty(
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__90cfe3a95a2f7af220983de86fe4c7daad60483ed0f587c54c4c9583525aa77c)
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''By default, DataSync automatically chooses an SMB protocol version based on negotiation with your SMB file server.

            You also can configure DataSync to use a specific SMB version, but we recommend doing this only if DataSync has trouble negotiating with the SMB file server automatically.

            These are the following options for configuring the SMB version:

            - ``AUTOMATIC`` (default): DataSync and the SMB file server negotiate the highest version of SMB that they mutually support between 2.1 and 3.1.1.

            This is the recommended option. If you instead choose a specific version that your file server doesn't support, you may get an ``Operation Not Supported`` error.

            - ``SMB3`` : Restricts the protocol negotiation to only SMB version 3.0.2.
            - ``SMB2`` : Restricts the protocol negotiation to only SMB version 2.1.
            - ``SMB2_0`` : Restricts the protocol negotiation to only SMB version 2.0.
            - ``SMB1`` : Restricts the protocol negotiation to only SMB version 1.0.

            .. epigraph::

               The ``SMB1`` option isn't available when `creating an Amazon FSx for NetApp ONTAP location <https://docs.aws.amazon.com/datasync/latest/userguide/API_CreateLocationFsxOntap.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationsmb-mountoptions.html#cfn-datasync-locationsmb-mountoptions-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MountOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnTaskMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_watch_log_group_arn": "cloudWatchLogGroupArn",
        "destination_location_arn": "destinationLocationArn",
        "excludes": "excludes",
        "includes": "includes",
        "manifest_config": "manifestConfig",
        "name": "name",
        "options": "options",
        "schedule": "schedule",
        "source_location_arn": "sourceLocationArn",
        "tags": "tags",
        "task_mode": "taskMode",
        "task_report_config": "taskReportConfig",
    },
)
class CfnTaskMixinProps:
    def __init__(
        self,
        *,
        cloud_watch_log_group_arn: typing.Optional[builtins.str] = None,
        destination_location_arn: typing.Optional[builtins.str] = None,
        excludes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTaskPropsMixin.FilterRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        includes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTaskPropsMixin.FilterRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        manifest_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTaskPropsMixin.ManifestConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTaskPropsMixin.OptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        schedule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTaskPropsMixin.TaskScheduleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        source_location_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        task_mode: typing.Optional[builtins.str] = None,
        task_report_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTaskPropsMixin.TaskReportConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnTaskPropsMixin.

        :param cloud_watch_log_group_arn: Specifies the Amazon Resource Name (ARN) of an Amazon CloudWatch log group for monitoring your task. For Enhanced mode tasks, you don't need to specify anything. DataSync automatically sends logs to a CloudWatch log group named ``/aws/datasync`` . For more information, see `Monitoring data transfers with CloudWatch Logs <https://docs.aws.amazon.com/datasync/latest/userguide/configure-logging.html>`_ .
        :param destination_location_arn: The Amazon Resource Name (ARN) of an AWS storage resource's location.
        :param excludes: Specifies exclude filters that define the files, objects, and folders in your source location that you don't want DataSync to transfer. For more information and examples, see `Specifying what DataSync transfers by using filters <https://docs.aws.amazon.com/datasync/latest/userguide/filtering.html>`_ .
        :param includes: Specifies include filters that define the files, objects, and folders in your source location that you want DataSync to transfer. For more information and examples, see `Specifying what DataSync transfers by using filters <https://docs.aws.amazon.com/datasync/latest/userguide/filtering.html>`_ .
        :param manifest_config: The configuration of the manifest that lists the files or objects that you want DataSync to transfer. For more information, see `Specifying what DataSync transfers by using a manifest <https://docs.aws.amazon.com/datasync/latest/userguide/transferring-with-manifest.html>`_ .
        :param name: Specifies the name of your task.
        :param options: Specifies your task's settings, such as preserving file metadata, verifying data integrity, among other options.
        :param schedule: Specifies a schedule for when you want your task to run. For more information, see `Scheduling your task <https://docs.aws.amazon.com/datasync/latest/userguide/task-scheduling.html>`_ .
        :param source_location_arn: Specifies the ARN of your transfer's source location.
        :param tags: Specifies the tags that you want to apply to your task. *Tags* are key-value pairs that help you manage, filter, and search for your DataSync resources.
        :param task_mode: The task mode that you're using. For more information, see `Choosing a task mode for your data transfer <https://docs.aws.amazon.com/datasync/latest/userguide/choosing-task-mode.html>`_ .
        :param task_report_config: The configuration of your task report, which provides detailed information about your DataSync transfer. For more information, see `Monitoring your DataSync transfers with task reports <https://docs.aws.amazon.com/datasync/latest/userguide/task-reports.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
            
            cfn_task_mixin_props = datasync_mixins.CfnTaskMixinProps(
                cloud_watch_log_group_arn="cloudWatchLogGroupArn",
                destination_location_arn="destinationLocationArn",
                excludes=[datasync_mixins.CfnTaskPropsMixin.FilterRuleProperty(
                    filter_type="filterType",
                    value="value"
                )],
                includes=[datasync_mixins.CfnTaskPropsMixin.FilterRuleProperty(
                    filter_type="filterType",
                    value="value"
                )],
                manifest_config=datasync_mixins.CfnTaskPropsMixin.ManifestConfigProperty(
                    action="action",
                    format="format",
                    source=datasync_mixins.CfnTaskPropsMixin.SourceProperty(
                        s3=datasync_mixins.CfnTaskPropsMixin.ManifestConfigSourceS3Property(
                            bucket_access_role_arn="bucketAccessRoleArn",
                            manifest_object_path="manifestObjectPath",
                            manifest_object_version_id="manifestObjectVersionId",
                            s3_bucket_arn="s3BucketArn"
                        )
                    )
                ),
                name="name",
                options=datasync_mixins.CfnTaskPropsMixin.OptionsProperty(
                    atime="atime",
                    bytes_per_second=123,
                    gid="gid",
                    log_level="logLevel",
                    mtime="mtime",
                    object_tags="objectTags",
                    overwrite_mode="overwriteMode",
                    posix_permissions="posixPermissions",
                    preserve_deleted_files="preserveDeletedFiles",
                    preserve_devices="preserveDevices",
                    security_descriptor_copy_flags="securityDescriptorCopyFlags",
                    task_queueing="taskQueueing",
                    transfer_mode="transferMode",
                    uid="uid",
                    verify_mode="verifyMode"
                ),
                schedule=datasync_mixins.CfnTaskPropsMixin.TaskScheduleProperty(
                    schedule_expression="scheduleExpression",
                    status="status"
                ),
                source_location_arn="sourceLocationArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                task_mode="taskMode",
                task_report_config=datasync_mixins.CfnTaskPropsMixin.TaskReportConfigProperty(
                    destination=datasync_mixins.CfnTaskPropsMixin.DestinationProperty(
                        s3=datasync_mixins.CfnTaskPropsMixin.S3Property(
                            bucket_access_role_arn="bucketAccessRoleArn",
                            s3_bucket_arn="s3BucketArn",
                            subdirectory="subdirectory"
                        )
                    ),
                    object_version_ids="objectVersionIds",
                    output_type="outputType",
                    overrides=datasync_mixins.CfnTaskPropsMixin.OverridesProperty(
                        deleted=datasync_mixins.CfnTaskPropsMixin.DeletedProperty(
                            report_level="reportLevel"
                        ),
                        skipped=datasync_mixins.CfnTaskPropsMixin.SkippedProperty(
                            report_level="reportLevel"
                        ),
                        transferred=datasync_mixins.CfnTaskPropsMixin.TransferredProperty(
                            report_level="reportLevel"
                        ),
                        verified=datasync_mixins.CfnTaskPropsMixin.VerifiedProperty(
                            report_level="reportLevel"
                        )
                    ),
                    report_level="reportLevel"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cd24647ab1bd031aa4f0ce1758f29f57c6a8aaca31fee525466cea4db090603)
            check_type(argname="argument cloud_watch_log_group_arn", value=cloud_watch_log_group_arn, expected_type=type_hints["cloud_watch_log_group_arn"])
            check_type(argname="argument destination_location_arn", value=destination_location_arn, expected_type=type_hints["destination_location_arn"])
            check_type(argname="argument excludes", value=excludes, expected_type=type_hints["excludes"])
            check_type(argname="argument includes", value=includes, expected_type=type_hints["includes"])
            check_type(argname="argument manifest_config", value=manifest_config, expected_type=type_hints["manifest_config"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument source_location_arn", value=source_location_arn, expected_type=type_hints["source_location_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument task_mode", value=task_mode, expected_type=type_hints["task_mode"])
            check_type(argname="argument task_report_config", value=task_report_config, expected_type=type_hints["task_report_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cloud_watch_log_group_arn is not None:
            self._values["cloud_watch_log_group_arn"] = cloud_watch_log_group_arn
        if destination_location_arn is not None:
            self._values["destination_location_arn"] = destination_location_arn
        if excludes is not None:
            self._values["excludes"] = excludes
        if includes is not None:
            self._values["includes"] = includes
        if manifest_config is not None:
            self._values["manifest_config"] = manifest_config
        if name is not None:
            self._values["name"] = name
        if options is not None:
            self._values["options"] = options
        if schedule is not None:
            self._values["schedule"] = schedule
        if source_location_arn is not None:
            self._values["source_location_arn"] = source_location_arn
        if tags is not None:
            self._values["tags"] = tags
        if task_mode is not None:
            self._values["task_mode"] = task_mode
        if task_report_config is not None:
            self._values["task_report_config"] = task_report_config

    @builtins.property
    def cloud_watch_log_group_arn(self) -> typing.Optional[builtins.str]:
        '''Specifies the Amazon Resource Name (ARN) of an Amazon CloudWatch log group for monitoring your task.

        For Enhanced mode tasks, you don't need to specify anything. DataSync automatically sends logs to a CloudWatch log group named ``/aws/datasync`` .

        For more information, see `Monitoring data transfers with CloudWatch Logs <https://docs.aws.amazon.com/datasync/latest/userguide/configure-logging.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-cloudwatchloggrouparn
        '''
        result = self._values.get("cloud_watch_log_group_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destination_location_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of an AWS storage resource's location.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-destinationlocationarn
        '''
        result = self._values.get("destination_location_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def excludes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskPropsMixin.FilterRuleProperty"]]]]:
        '''Specifies exclude filters that define the files, objects, and folders in your source location that you don't want DataSync to transfer.

        For more information and examples, see `Specifying what DataSync transfers by using filters <https://docs.aws.amazon.com/datasync/latest/userguide/filtering.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-excludes
        '''
        result = self._values.get("excludes")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskPropsMixin.FilterRuleProperty"]]]], result)

    @builtins.property
    def includes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskPropsMixin.FilterRuleProperty"]]]]:
        '''Specifies include filters that define the files, objects, and folders in your source location that you want DataSync to transfer.

        For more information and examples, see `Specifying what DataSync transfers by using filters <https://docs.aws.amazon.com/datasync/latest/userguide/filtering.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-includes
        '''
        result = self._values.get("includes")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskPropsMixin.FilterRuleProperty"]]]], result)

    @builtins.property
    def manifest_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskPropsMixin.ManifestConfigProperty"]]:
        '''The configuration of the manifest that lists the files or objects that you want DataSync to transfer.

        For more information, see `Specifying what DataSync transfers by using a manifest <https://docs.aws.amazon.com/datasync/latest/userguide/transferring-with-manifest.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-manifestconfig
        '''
        result = self._values.get("manifest_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskPropsMixin.ManifestConfigProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of your task.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskPropsMixin.OptionsProperty"]]:
        '''Specifies your task's settings, such as preserving file metadata, verifying data integrity, among other options.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-options
        '''
        result = self._values.get("options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskPropsMixin.OptionsProperty"]], result)

    @builtins.property
    def schedule(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskPropsMixin.TaskScheduleProperty"]]:
        '''Specifies a schedule for when you want your task to run.

        For more information, see `Scheduling your task <https://docs.aws.amazon.com/datasync/latest/userguide/task-scheduling.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-schedule
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskPropsMixin.TaskScheduleProperty"]], result)

    @builtins.property
    def source_location_arn(self) -> typing.Optional[builtins.str]:
        '''Specifies the ARN of your transfer's source location.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-sourcelocationarn
        '''
        result = self._values.get("source_location_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Specifies the tags that you want to apply to your task.

        *Tags* are key-value pairs that help you manage, filter, and search for your DataSync resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def task_mode(self) -> typing.Optional[builtins.str]:
        '''The task mode that you're using.

        For more information, see `Choosing a task mode for your data transfer <https://docs.aws.amazon.com/datasync/latest/userguide/choosing-task-mode.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-taskmode
        '''
        result = self._values.get("task_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def task_report_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskPropsMixin.TaskReportConfigProperty"]]:
        '''The configuration of your task report, which provides detailed information about your DataSync transfer.

        For more information, see `Monitoring your DataSync transfers with task reports <https://docs.aws.amazon.com/datasync/latest/userguide/task-reports.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-taskreportconfig
        '''
        result = self._values.get("task_report_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskPropsMixin.TaskReportConfigProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTaskMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnTaskPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnTaskPropsMixin",
):
    '''The ``AWS::DataSync::Task`` resource specifies a task.

    A task is a set of two locations (source and destination) and a set of ``Options`` that you use to control the behavior of a task. If you don't specify ``Options`` when you create a task, AWS DataSync populates them with service defaults.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html
    :cloudformationResource: AWS::DataSync::Task
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
        
        cfn_task_props_mixin = datasync_mixins.CfnTaskPropsMixin(datasync_mixins.CfnTaskMixinProps(
            cloud_watch_log_group_arn="cloudWatchLogGroupArn",
            destination_location_arn="destinationLocationArn",
            excludes=[datasync_mixins.CfnTaskPropsMixin.FilterRuleProperty(
                filter_type="filterType",
                value="value"
            )],
            includes=[datasync_mixins.CfnTaskPropsMixin.FilterRuleProperty(
                filter_type="filterType",
                value="value"
            )],
            manifest_config=datasync_mixins.CfnTaskPropsMixin.ManifestConfigProperty(
                action="action",
                format="format",
                source=datasync_mixins.CfnTaskPropsMixin.SourceProperty(
                    s3=datasync_mixins.CfnTaskPropsMixin.ManifestConfigSourceS3Property(
                        bucket_access_role_arn="bucketAccessRoleArn",
                        manifest_object_path="manifestObjectPath",
                        manifest_object_version_id="manifestObjectVersionId",
                        s3_bucket_arn="s3BucketArn"
                    )
                )
            ),
            name="name",
            options=datasync_mixins.CfnTaskPropsMixin.OptionsProperty(
                atime="atime",
                bytes_per_second=123,
                gid="gid",
                log_level="logLevel",
                mtime="mtime",
                object_tags="objectTags",
                overwrite_mode="overwriteMode",
                posix_permissions="posixPermissions",
                preserve_deleted_files="preserveDeletedFiles",
                preserve_devices="preserveDevices",
                security_descriptor_copy_flags="securityDescriptorCopyFlags",
                task_queueing="taskQueueing",
                transfer_mode="transferMode",
                uid="uid",
                verify_mode="verifyMode"
            ),
            schedule=datasync_mixins.CfnTaskPropsMixin.TaskScheduleProperty(
                schedule_expression="scheduleExpression",
                status="status"
            ),
            source_location_arn="sourceLocationArn",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            task_mode="taskMode",
            task_report_config=datasync_mixins.CfnTaskPropsMixin.TaskReportConfigProperty(
                destination=datasync_mixins.CfnTaskPropsMixin.DestinationProperty(
                    s3=datasync_mixins.CfnTaskPropsMixin.S3Property(
                        bucket_access_role_arn="bucketAccessRoleArn",
                        s3_bucket_arn="s3BucketArn",
                        subdirectory="subdirectory"
                    )
                ),
                object_version_ids="objectVersionIds",
                output_type="outputType",
                overrides=datasync_mixins.CfnTaskPropsMixin.OverridesProperty(
                    deleted=datasync_mixins.CfnTaskPropsMixin.DeletedProperty(
                        report_level="reportLevel"
                    ),
                    skipped=datasync_mixins.CfnTaskPropsMixin.SkippedProperty(
                        report_level="reportLevel"
                    ),
                    transferred=datasync_mixins.CfnTaskPropsMixin.TransferredProperty(
                        report_level="reportLevel"
                    ),
                    verified=datasync_mixins.CfnTaskPropsMixin.VerifiedProperty(
                        report_level="reportLevel"
                    )
                ),
                report_level="reportLevel"
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnTaskMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DataSync::Task``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14d57e5aa12bdcf06cc1627e7cfa6e8c86aa8bdc657e0865a35a22f7888eab64)
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
            type_hints = typing.get_type_hints(_typecheckingstub__26918e3f47aa37fdf914c653ea3c15b622c53d6bb8783d0e68188d989f0c9d3f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82b2ebe6cfe18103e280b05a84db8ba77dee36e00b9b51031a8f44040c651c89)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTaskMixinProps:
        return typing.cast(CfnTaskMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnTaskPropsMixin.DeletedProperty",
        jsii_struct_bases=[],
        name_mapping={"report_level": "reportLevel"},
    )
    class DeletedProperty:
        def __init__(
            self,
            *,
            report_level: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the level of reporting for the files, objects, and directories that Datasync attempted to delete in your destination location.

            This only applies if you configure your task to delete data in the destination that isn't in the source.

            :param report_level: Specifies whether you want your task report to include only what went wrong with your transfer or a list of what succeeded and didn't.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-deleted.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
                
                deleted_property = datasync_mixins.CfnTaskPropsMixin.DeletedProperty(
                    report_level="reportLevel"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9b30a01031a7c22b1f8de5b4df730f476b962ea398321fdfd0d370d22a8d57c3)
                check_type(argname="argument report_level", value=report_level, expected_type=type_hints["report_level"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if report_level is not None:
                self._values["report_level"] = report_level

        @builtins.property
        def report_level(self) -> typing.Optional[builtins.str]:
            '''Specifies whether you want your task report to include only what went wrong with your transfer or a list of what succeeded and didn't.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-deleted.html#cfn-datasync-task-deleted-reportlevel
            '''
            result = self._values.get("report_level")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeletedProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnTaskPropsMixin.DestinationProperty",
        jsii_struct_bases=[],
        name_mapping={"s3": "s3"},
    )
    class DestinationProperty:
        def __init__(
            self,
            *,
            s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTaskPropsMixin.S3Property", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies where DataSync uploads your task report.

            :param s3: Specifies the Amazon S3 bucket where DataSync uploads your task report.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-destination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
                
                destination_property = datasync_mixins.CfnTaskPropsMixin.DestinationProperty(
                    s3=datasync_mixins.CfnTaskPropsMixin.S3Property(
                        bucket_access_role_arn="bucketAccessRoleArn",
                        s3_bucket_arn="s3BucketArn",
                        subdirectory="subdirectory"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9f08afa70199d4e0348c183196ede7a43ad406ffe9659dc9d6ec841310c9cab0)
                check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3 is not None:
                self._values["s3"] = s3

        @builtins.property
        def s3(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskPropsMixin.S3Property"]]:
            '''Specifies the Amazon S3 bucket where DataSync uploads your task report.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-destination.html#cfn-datasync-task-destination-s3
            '''
            result = self._values.get("s3")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskPropsMixin.S3Property"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnTaskPropsMixin.FilterRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"filter_type": "filterType", "value": "value"},
    )
    class FilterRuleProperty:
        def __init__(
            self,
            *,
            filter_type: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies which files, folders, and objects to include or exclude when transferring files from source to destination.

            :param filter_type: The type of filter rule to apply. AWS DataSync only supports the SIMPLE_PATTERN rule type.
            :param value: A single filter string that consists of the patterns to include or exclude. The patterns are delimited by "|" (that is, a pipe), for example: ``/folder1|/folder2``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-filterrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
                
                filter_rule_property = datasync_mixins.CfnTaskPropsMixin.FilterRuleProperty(
                    filter_type="filterType",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2255697b19fa11c754964d96d9043eff5784d95083d1dff53a99883ca8e55dbc)
                check_type(argname="argument filter_type", value=filter_type, expected_type=type_hints["filter_type"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if filter_type is not None:
                self._values["filter_type"] = filter_type
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def filter_type(self) -> typing.Optional[builtins.str]:
            '''The type of filter rule to apply.

            AWS DataSync only supports the SIMPLE_PATTERN rule type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-filterrule.html#cfn-datasync-task-filterrule-filtertype
            '''
            result = self._values.get("filter_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''A single filter string that consists of the patterns to include or exclude.

            The patterns are delimited by "|" (that is, a pipe), for example: ``/folder1|/folder2``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-filterrule.html#cfn-datasync-task-filterrule-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FilterRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnTaskPropsMixin.ManifestConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"action": "action", "format": "format", "source": "source"},
    )
    class ManifestConfigProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[builtins.str] = None,
            format: typing.Optional[builtins.str] = None,
            source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTaskPropsMixin.SourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Configures a manifest, which is a list of files or objects that you want AWS DataSync to transfer.

            For more information and configuration examples, see `Specifying what DataSync transfers by using a manifest <https://docs.aws.amazon.com/datasync/latest/userguide/transferring-with-manifest.html>`_ .

            :param action: Specifies what DataSync uses the manifest for.
            :param format: Specifies the file format of your manifest. For more information, see `Creating a manifest <https://docs.aws.amazon.com/datasync/latest/userguide/transferring-with-manifest.html#transferring-with-manifest-create>`_ .
            :param source: Specifies the manifest that you want DataSync to use and where it's hosted. .. epigraph:: You must specify this parameter if you're configuring a new manifest on or after February 7, 2024. If you don't, you'll get a 400 status code and ``ValidationException`` error stating that you're missing the IAM role for DataSync to access the S3 bucket where you're hosting your manifest. For more information, see `Providing DataSync access to your manifest <https://docs.aws.amazon.com/datasync/latest/userguide/transferring-with-manifest.html#transferring-with-manifest-access>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-manifestconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
                
                manifest_config_property = datasync_mixins.CfnTaskPropsMixin.ManifestConfigProperty(
                    action="action",
                    format="format",
                    source=datasync_mixins.CfnTaskPropsMixin.SourceProperty(
                        s3=datasync_mixins.CfnTaskPropsMixin.ManifestConfigSourceS3Property(
                            bucket_access_role_arn="bucketAccessRoleArn",
                            manifest_object_path="manifestObjectPath",
                            manifest_object_version_id="manifestObjectVersionId",
                            s3_bucket_arn="s3BucketArn"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__40272ee1902201b1f35caa63d858041621d9049eebd9dcf631061b5941681be7)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument format", value=format, expected_type=type_hints["format"])
                check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if format is not None:
                self._values["format"] = format
            if source is not None:
                self._values["source"] = source

        @builtins.property
        def action(self) -> typing.Optional[builtins.str]:
            '''Specifies what DataSync uses the manifest for.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-manifestconfig.html#cfn-datasync-task-manifestconfig-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def format(self) -> typing.Optional[builtins.str]:
            '''Specifies the file format of your manifest.

            For more information, see `Creating a manifest <https://docs.aws.amazon.com/datasync/latest/userguide/transferring-with-manifest.html#transferring-with-manifest-create>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-manifestconfig.html#cfn-datasync-task-manifestconfig-format
            '''
            result = self._values.get("format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskPropsMixin.SourceProperty"]]:
            '''Specifies the manifest that you want DataSync to use and where it's hosted.

            .. epigraph::

               You must specify this parameter if you're configuring a new manifest on or after February 7, 2024.

               If you don't, you'll get a 400 status code and ``ValidationException`` error stating that you're missing the IAM role for DataSync to access the S3 bucket where you're hosting your manifest. For more information, see `Providing DataSync access to your manifest <https://docs.aws.amazon.com/datasync/latest/userguide/transferring-with-manifest.html#transferring-with-manifest-access>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-manifestconfig.html#cfn-datasync-task-manifestconfig-source
            '''
            result = self._values.get("source")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskPropsMixin.SourceProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ManifestConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnTaskPropsMixin.ManifestConfigSourceS3Property",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_access_role_arn": "bucketAccessRoleArn",
            "manifest_object_path": "manifestObjectPath",
            "manifest_object_version_id": "manifestObjectVersionId",
            "s3_bucket_arn": "s3BucketArn",
        },
    )
    class ManifestConfigSourceS3Property:
        def __init__(
            self,
            *,
            bucket_access_role_arn: typing.Optional[builtins.str] = None,
            manifest_object_path: typing.Optional[builtins.str] = None,
            manifest_object_version_id: typing.Optional[builtins.str] = None,
            s3_bucket_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the S3 bucket where you're hosting the manifest that you want AWS DataSync to use.

            :param bucket_access_role_arn: Specifies the AWS Identity and Access Management (IAM) role that allows DataSync to access your manifest.
            :param manifest_object_path: Specifies the Amazon S3 object key of your manifest.
            :param manifest_object_version_id: Specifies the object version ID of the manifest that you want DataSync to use.
            :param s3_bucket_arn: Specifies the Amazon Resource Name (ARN) of the S3 bucket where you're hosting your manifest.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-manifestconfigsources3.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
                
                manifest_config_source_s3_property = datasync_mixins.CfnTaskPropsMixin.ManifestConfigSourceS3Property(
                    bucket_access_role_arn="bucketAccessRoleArn",
                    manifest_object_path="manifestObjectPath",
                    manifest_object_version_id="manifestObjectVersionId",
                    s3_bucket_arn="s3BucketArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c5786c00148d8574a3b16a4d63fb20995bdadbf31b86c1acc1d191f2c2b6eb9d)
                check_type(argname="argument bucket_access_role_arn", value=bucket_access_role_arn, expected_type=type_hints["bucket_access_role_arn"])
                check_type(argname="argument manifest_object_path", value=manifest_object_path, expected_type=type_hints["manifest_object_path"])
                check_type(argname="argument manifest_object_version_id", value=manifest_object_version_id, expected_type=type_hints["manifest_object_version_id"])
                check_type(argname="argument s3_bucket_arn", value=s3_bucket_arn, expected_type=type_hints["s3_bucket_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_access_role_arn is not None:
                self._values["bucket_access_role_arn"] = bucket_access_role_arn
            if manifest_object_path is not None:
                self._values["manifest_object_path"] = manifest_object_path
            if manifest_object_version_id is not None:
                self._values["manifest_object_version_id"] = manifest_object_version_id
            if s3_bucket_arn is not None:
                self._values["s3_bucket_arn"] = s3_bucket_arn

        @builtins.property
        def bucket_access_role_arn(self) -> typing.Optional[builtins.str]:
            '''Specifies the AWS Identity and Access Management (IAM) role that allows DataSync to access your manifest.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-manifestconfigsources3.html#cfn-datasync-task-manifestconfigsources3-bucketaccessrolearn
            '''
            result = self._values.get("bucket_access_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def manifest_object_path(self) -> typing.Optional[builtins.str]:
            '''Specifies the Amazon S3 object key of your manifest.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-manifestconfigsources3.html#cfn-datasync-task-manifestconfigsources3-manifestobjectpath
            '''
            result = self._values.get("manifest_object_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def manifest_object_version_id(self) -> typing.Optional[builtins.str]:
            '''Specifies the object version ID of the manifest that you want DataSync to use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-manifestconfigsources3.html#cfn-datasync-task-manifestconfigsources3-manifestobjectversionid
            '''
            result = self._values.get("manifest_object_version_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_bucket_arn(self) -> typing.Optional[builtins.str]:
            '''Specifies the Amazon Resource Name (ARN) of the S3 bucket where you're hosting your manifest.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-manifestconfigsources3.html#cfn-datasync-task-manifestconfigsources3-s3bucketarn
            '''
            result = self._values.get("s3_bucket_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ManifestConfigSourceS3Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnTaskPropsMixin.OptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "atime": "atime",
            "bytes_per_second": "bytesPerSecond",
            "gid": "gid",
            "log_level": "logLevel",
            "mtime": "mtime",
            "object_tags": "objectTags",
            "overwrite_mode": "overwriteMode",
            "posix_permissions": "posixPermissions",
            "preserve_deleted_files": "preserveDeletedFiles",
            "preserve_devices": "preserveDevices",
            "security_descriptor_copy_flags": "securityDescriptorCopyFlags",
            "task_queueing": "taskQueueing",
            "transfer_mode": "transferMode",
            "uid": "uid",
            "verify_mode": "verifyMode",
        },
    )
    class OptionsProperty:
        def __init__(
            self,
            *,
            atime: typing.Optional[builtins.str] = None,
            bytes_per_second: typing.Optional[jsii.Number] = None,
            gid: typing.Optional[builtins.str] = None,
            log_level: typing.Optional[builtins.str] = None,
            mtime: typing.Optional[builtins.str] = None,
            object_tags: typing.Optional[builtins.str] = None,
            overwrite_mode: typing.Optional[builtins.str] = None,
            posix_permissions: typing.Optional[builtins.str] = None,
            preserve_deleted_files: typing.Optional[builtins.str] = None,
            preserve_devices: typing.Optional[builtins.str] = None,
            security_descriptor_copy_flags: typing.Optional[builtins.str] = None,
            task_queueing: typing.Optional[builtins.str] = None,
            transfer_mode: typing.Optional[builtins.str] = None,
            uid: typing.Optional[builtins.str] = None,
            verify_mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents the options that are available to control the behavior of a `StartTaskExecution <https://docs.aws.amazon.com/datasync/latest/userguide/API_StartTaskExecution.html>`_ operation. This behavior includes preserving metadata, such as user ID (UID), group ID (GID), and file permissions; overwriting files in the destination; data integrity verification; and so on.

            A task has a set of default options associated with it. If you don't specify an option in `StartTaskExecution <https://docs.aws.amazon.com/datasync/latest/userguide/API_StartTaskExecution.html>`_ , the default value is used. You can override the default options on each task execution by specifying an overriding ``Options`` value to `StartTaskExecution <https://docs.aws.amazon.com/datasync/latest/userguide/API_StartTaskExecution.html>`_ .

            :param atime: A file metadata value that shows the last time that a file was accessed (that is, when the file was read or written to). If you set ``Atime`` to ``BEST_EFFORT`` , AWS DataSync attempts to preserve the original ``Atime`` attribute on all source files (that is, the version before the PREPARING phase). However, ``Atime`` 's behavior is not fully standard across platforms, so AWS DataSync can only do this on a best-effort basis. Default value: ``BEST_EFFORT`` ``BEST_EFFORT`` : Attempt to preserve the per-file ``Atime`` value (recommended). ``NONE`` : Ignore ``Atime`` . .. epigraph:: If ``Atime`` is set to ``BEST_EFFORT`` , ``Mtime`` must be set to ``PRESERVE`` . If ``Atime`` is set to ``NONE`` , ``Mtime`` must also be ``NONE`` .
            :param bytes_per_second: A value that limits the bandwidth used by AWS DataSync . For example, if you want AWS DataSync to use a maximum of 1 MB, set this value to ``1048576`` (=1024*1024).
            :param gid: The group ID (GID) of the file's owners. Default value: ``INT_VALUE`` ``INT_VALUE`` : Preserve the integer value of the user ID (UID) and group ID (GID) (recommended). ``NAME`` : Currently not supported. ``NONE`` : Ignore the UID and GID.
            :param log_level: Specifies the type of logs that DataSync publishes to a Amazon CloudWatch Logs log group. To specify the log group, see `CloudWatchLogGroupArn <https://docs.aws.amazon.com/datasync/latest/userguide/API_CreateTask.html#DataSync-CreateTask-request-CloudWatchLogGroupArn>`_ . - ``BASIC`` - Publishes logs with only basic information (such as transfer errors). - ``TRANSFER`` - Publishes logs for all files or objects that your DataSync task transfers and performs data-integrity checks on. - ``OFF`` - No logs are published.
            :param mtime: A value that indicates the last time that a file was modified (that is, a file was written to) before the PREPARING phase. This option is required for cases when you need to run the same task more than one time. Default value: ``PRESERVE`` ``PRESERVE`` : Preserve original ``Mtime`` (recommended) ``NONE`` : Ignore ``Mtime`` . .. epigraph:: If ``Mtime`` is set to ``PRESERVE`` , ``Atime`` must be set to ``BEST_EFFORT`` . If ``Mtime`` is set to ``NONE`` , ``Atime`` must also be set to ``NONE`` .
            :param object_tags: Specifies whether you want DataSync to ``PRESERVE`` object tags (default behavior) when transferring between object storage systems. If you want your DataSync task to ignore object tags, specify the ``NONE`` value.
            :param overwrite_mode: Specifies whether DataSync should modify or preserve data at the destination location. - ``ALWAYS`` (default) - DataSync modifies data in the destination location when source data (including metadata) has changed. If DataSync overwrites objects, you might incur additional charges for certain Amazon S3 storage classes (for example, for retrieval or early deletion). For more information, see `Storage class considerations with Amazon S3 transfers <https://docs.aws.amazon.com/datasync/latest/userguide/create-s3-location.html#using-storage-classes>`_ . - ``NEVER`` - DataSync doesn't overwrite data in the destination location even if the source data has changed. You can use this option to protect against overwriting changes made to files or objects in the destination.
            :param posix_permissions: A value that determines which users or groups can access a file for a specific purpose, such as reading, writing, or execution of the file. This option should be set only for Network File System (NFS), Amazon EFS, and Amazon S3 locations. For more information about what metadata is copied by DataSync, see `Metadata Copied by DataSync <https://docs.aws.amazon.com/datasync/latest/userguide/special-files.html#metadata-copied>`_ . Default value: ``PRESERVE`` ``PRESERVE`` : Preserve POSIX-style permissions (recommended). ``NONE`` : Ignore permissions. .. epigraph:: AWS DataSync can preserve extant permissions of a source location.
            :param preserve_deleted_files: A value that specifies whether files in the destination that don't exist in the source file system are preserved. This option can affect your storage costs. If your task deletes objects, you might incur minimum storage duration charges for certain storage classes. For detailed information, see `Considerations when working with Amazon S3 storage classes in DataSync <https://docs.aws.amazon.com/datasync/latest/userguide/create-s3-location.html#using-storage-classes>`_ in the *AWS DataSync User Guide* . Default value: ``PRESERVE`` ``PRESERVE`` : Ignore destination files that aren't present in the source (recommended). ``REMOVE`` : Delete destination files that aren't present in the source.
            :param preserve_devices: A value that determines whether AWS DataSync should preserve the metadata of block and character devices in the source file system, and re-create the files with that device name and metadata on the destination. DataSync does not copy the contents of such devices, only the name and metadata. .. epigraph:: AWS DataSync can't sync the actual contents of such devices, because they are nonterminal and don't return an end-of-file (EOF) marker. Default value: ``NONE`` ``NONE`` : Ignore special devices (recommended). ``PRESERVE`` : Preserve character and block device metadata. This option isn't currently supported for Amazon EFS.
            :param security_descriptor_copy_flags: A value that determines which components of the SMB security descriptor are copied from source to destination objects. This value is only used for transfers between SMB and Amazon FSx for Windows File Server locations, or between two Amazon FSx for Windows File Server locations. For more information about how DataSync handles metadata, see `How DataSync Handles Metadata and Special Files <https://docs.aws.amazon.com/datasync/latest/userguide/special-files.html>`_ . Default value: ``OWNER_DACL`` ``OWNER_DACL`` : For each copied object, DataSync copies the following metadata: - Object owner. - NTFS discretionary access control lists (DACLs), which determine whether to grant access to an object. When you use option, DataSync does NOT copy the NTFS system access control lists (SACLs), which are used by administrators to log attempts to access a secured object. ``OWNER_DACL_SACL`` : For each copied object, DataSync copies the following metadata: - Object owner. - NTFS discretionary access control lists (DACLs), which determine whether to grant access to an object. - NTFS system access control lists (SACLs), which are used by administrators to log attempts to access a secured object. Copying SACLs requires granting additional permissions to the Windows user that DataSync uses to access your SMB location. For information about choosing a user that ensures sufficient permissions to files, folders, and metadata, see `user <https://docs.aws.amazon.com/datasync/latest/userguide/create-smb-location.html#SMBuser>`_ . ``NONE`` : None of the SMB security descriptor components are copied. Destination objects are owned by the user that was provided for accessing the destination location. DACLs and SACLs are set based on the destination server’s configuration.
            :param task_queueing: Specifies whether your transfer tasks should be put into a queue during certain scenarios when `running multiple tasks <https://docs.aws.amazon.com/datasync/latest/userguide/run-task.html#running-multiple-tasks>`_ . This is ``ENABLED`` by default.
            :param transfer_mode: A value that determines whether DataSync transfers only the data and metadata that differ between the source and the destination location, or whether DataSync transfers all the content from the source, without comparing it to the destination location. ``CHANGED`` : DataSync copies only data or metadata that is new or different from the source location to the destination location. ``ALL`` : DataSync copies all source location content to the destination, without comparing it to existing content on the destination.
            :param uid: The user ID (UID) of the file's owner. Default value: ``INT_VALUE`` ``INT_VALUE`` : Preserve the integer value of the UID and group ID (GID) (recommended). ``NAME`` : Currently not supported ``NONE`` : Ignore the UID and GID.
            :param verify_mode: A value that determines whether a data integrity verification is performed at the end of a task execution after all data and metadata have been transferred. For more information, see `Configure task settings <https://docs.aws.amazon.com/datasync/latest/userguide/create-task.html>`_ . Default value: ``POINT_IN_TIME_CONSISTENT`` ``ONLY_FILES_TRANSFERRED`` (recommended): Perform verification only on files that were transferred. ``POINT_IN_TIME_CONSISTENT`` : Scan the entire source and entire destination at the end of the transfer to verify that the source and destination are fully synchronized. This option isn't supported when transferring to S3 Glacier or S3 Glacier Deep Archive storage classes. ``NONE`` : No additional verification is done at the end of the transfer, but all data transmissions are integrity-checked with checksum verification during the transfer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
                
                options_property = datasync_mixins.CfnTaskPropsMixin.OptionsProperty(
                    atime="atime",
                    bytes_per_second=123,
                    gid="gid",
                    log_level="logLevel",
                    mtime="mtime",
                    object_tags="objectTags",
                    overwrite_mode="overwriteMode",
                    posix_permissions="posixPermissions",
                    preserve_deleted_files="preserveDeletedFiles",
                    preserve_devices="preserveDevices",
                    security_descriptor_copy_flags="securityDescriptorCopyFlags",
                    task_queueing="taskQueueing",
                    transfer_mode="transferMode",
                    uid="uid",
                    verify_mode="verifyMode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7bb3689cfbc145157b41909be370c4455b75c32204f75eacd61753fe9e88e487)
                check_type(argname="argument atime", value=atime, expected_type=type_hints["atime"])
                check_type(argname="argument bytes_per_second", value=bytes_per_second, expected_type=type_hints["bytes_per_second"])
                check_type(argname="argument gid", value=gid, expected_type=type_hints["gid"])
                check_type(argname="argument log_level", value=log_level, expected_type=type_hints["log_level"])
                check_type(argname="argument mtime", value=mtime, expected_type=type_hints["mtime"])
                check_type(argname="argument object_tags", value=object_tags, expected_type=type_hints["object_tags"])
                check_type(argname="argument overwrite_mode", value=overwrite_mode, expected_type=type_hints["overwrite_mode"])
                check_type(argname="argument posix_permissions", value=posix_permissions, expected_type=type_hints["posix_permissions"])
                check_type(argname="argument preserve_deleted_files", value=preserve_deleted_files, expected_type=type_hints["preserve_deleted_files"])
                check_type(argname="argument preserve_devices", value=preserve_devices, expected_type=type_hints["preserve_devices"])
                check_type(argname="argument security_descriptor_copy_flags", value=security_descriptor_copy_flags, expected_type=type_hints["security_descriptor_copy_flags"])
                check_type(argname="argument task_queueing", value=task_queueing, expected_type=type_hints["task_queueing"])
                check_type(argname="argument transfer_mode", value=transfer_mode, expected_type=type_hints["transfer_mode"])
                check_type(argname="argument uid", value=uid, expected_type=type_hints["uid"])
                check_type(argname="argument verify_mode", value=verify_mode, expected_type=type_hints["verify_mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if atime is not None:
                self._values["atime"] = atime
            if bytes_per_second is not None:
                self._values["bytes_per_second"] = bytes_per_second
            if gid is not None:
                self._values["gid"] = gid
            if log_level is not None:
                self._values["log_level"] = log_level
            if mtime is not None:
                self._values["mtime"] = mtime
            if object_tags is not None:
                self._values["object_tags"] = object_tags
            if overwrite_mode is not None:
                self._values["overwrite_mode"] = overwrite_mode
            if posix_permissions is not None:
                self._values["posix_permissions"] = posix_permissions
            if preserve_deleted_files is not None:
                self._values["preserve_deleted_files"] = preserve_deleted_files
            if preserve_devices is not None:
                self._values["preserve_devices"] = preserve_devices
            if security_descriptor_copy_flags is not None:
                self._values["security_descriptor_copy_flags"] = security_descriptor_copy_flags
            if task_queueing is not None:
                self._values["task_queueing"] = task_queueing
            if transfer_mode is not None:
                self._values["transfer_mode"] = transfer_mode
            if uid is not None:
                self._values["uid"] = uid
            if verify_mode is not None:
                self._values["verify_mode"] = verify_mode

        @builtins.property
        def atime(self) -> typing.Optional[builtins.str]:
            '''A file metadata value that shows the last time that a file was accessed (that is, when the file was read or written to).

            If you set ``Atime`` to ``BEST_EFFORT`` , AWS DataSync attempts to preserve the original ``Atime`` attribute on all source files (that is, the version before the PREPARING phase). However, ``Atime`` 's behavior is not fully standard across platforms, so AWS DataSync can only do this on a best-effort basis.

            Default value: ``BEST_EFFORT``

            ``BEST_EFFORT`` : Attempt to preserve the per-file ``Atime`` value (recommended).

            ``NONE`` : Ignore ``Atime`` .
            .. epigraph::

               If ``Atime`` is set to ``BEST_EFFORT`` , ``Mtime`` must be set to ``PRESERVE`` .

               If ``Atime`` is set to ``NONE`` , ``Mtime`` must also be ``NONE`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html#cfn-datasync-task-options-atime
            '''
            result = self._values.get("atime")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bytes_per_second(self) -> typing.Optional[jsii.Number]:
            '''A value that limits the bandwidth used by AWS DataSync .

            For example, if you want AWS DataSync to use a maximum of 1 MB, set this value to ``1048576`` (=1024*1024).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html#cfn-datasync-task-options-bytespersecond
            '''
            result = self._values.get("bytes_per_second")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def gid(self) -> typing.Optional[builtins.str]:
            '''The group ID (GID) of the file's owners.

            Default value: ``INT_VALUE``

            ``INT_VALUE`` : Preserve the integer value of the user ID (UID) and group ID (GID) (recommended).

            ``NAME`` : Currently not supported.

            ``NONE`` : Ignore the UID and GID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html#cfn-datasync-task-options-gid
            '''
            result = self._values.get("gid")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_level(self) -> typing.Optional[builtins.str]:
            '''Specifies the type of logs that DataSync publishes to a Amazon CloudWatch Logs log group.

            To specify the log group, see `CloudWatchLogGroupArn <https://docs.aws.amazon.com/datasync/latest/userguide/API_CreateTask.html#DataSync-CreateTask-request-CloudWatchLogGroupArn>`_ .

            - ``BASIC`` - Publishes logs with only basic information (such as transfer errors).
            - ``TRANSFER`` - Publishes logs for all files or objects that your DataSync task transfers and performs data-integrity checks on.
            - ``OFF`` - No logs are published.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html#cfn-datasync-task-options-loglevel
            '''
            result = self._values.get("log_level")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mtime(self) -> typing.Optional[builtins.str]:
            '''A value that indicates the last time that a file was modified (that is, a file was written to) before the PREPARING phase.

            This option is required for cases when you need to run the same task more than one time.

            Default value: ``PRESERVE``

            ``PRESERVE`` : Preserve original ``Mtime`` (recommended)

            ``NONE`` : Ignore ``Mtime`` .
            .. epigraph::

               If ``Mtime`` is set to ``PRESERVE`` , ``Atime`` must be set to ``BEST_EFFORT`` .

               If ``Mtime`` is set to ``NONE`` , ``Atime`` must also be set to ``NONE`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html#cfn-datasync-task-options-mtime
            '''
            result = self._values.get("mtime")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def object_tags(self) -> typing.Optional[builtins.str]:
            '''Specifies whether you want DataSync to ``PRESERVE`` object tags (default behavior) when transferring between object storage systems.

            If you want your DataSync task to ignore object tags, specify the ``NONE`` value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html#cfn-datasync-task-options-objecttags
            '''
            result = self._values.get("object_tags")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def overwrite_mode(self) -> typing.Optional[builtins.str]:
            '''Specifies whether DataSync should modify or preserve data at the destination location.

            - ``ALWAYS`` (default) - DataSync modifies data in the destination location when source data (including metadata) has changed.

            If DataSync overwrites objects, you might incur additional charges for certain Amazon S3 storage classes (for example, for retrieval or early deletion). For more information, see `Storage class considerations with Amazon S3 transfers <https://docs.aws.amazon.com/datasync/latest/userguide/create-s3-location.html#using-storage-classes>`_ .

            - ``NEVER`` - DataSync doesn't overwrite data in the destination location even if the source data has changed. You can use this option to protect against overwriting changes made to files or objects in the destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html#cfn-datasync-task-options-overwritemode
            '''
            result = self._values.get("overwrite_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def posix_permissions(self) -> typing.Optional[builtins.str]:
            '''A value that determines which users or groups can access a file for a specific purpose, such as reading, writing, or execution of the file.

            This option should be set only for Network File System (NFS), Amazon EFS, and Amazon S3 locations. For more information about what metadata is copied by DataSync, see `Metadata Copied by DataSync <https://docs.aws.amazon.com/datasync/latest/userguide/special-files.html#metadata-copied>`_ .

            Default value: ``PRESERVE``

            ``PRESERVE`` : Preserve POSIX-style permissions (recommended).

            ``NONE`` : Ignore permissions.
            .. epigraph::

               AWS DataSync can preserve extant permissions of a source location.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html#cfn-datasync-task-options-posixpermissions
            '''
            result = self._values.get("posix_permissions")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def preserve_deleted_files(self) -> typing.Optional[builtins.str]:
            '''A value that specifies whether files in the destination that don't exist in the source file system are preserved.

            This option can affect your storage costs. If your task deletes objects, you might incur minimum storage duration charges for certain storage classes. For detailed information, see `Considerations when working with Amazon S3 storage classes in DataSync <https://docs.aws.amazon.com/datasync/latest/userguide/create-s3-location.html#using-storage-classes>`_ in the *AWS DataSync User Guide* .

            Default value: ``PRESERVE``

            ``PRESERVE`` : Ignore destination files that aren't present in the source (recommended).

            ``REMOVE`` : Delete destination files that aren't present in the source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html#cfn-datasync-task-options-preservedeletedfiles
            '''
            result = self._values.get("preserve_deleted_files")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def preserve_devices(self) -> typing.Optional[builtins.str]:
            '''A value that determines whether AWS DataSync should preserve the metadata of block and character devices in the source file system, and re-create the files with that device name and metadata on the destination.

            DataSync does not copy the contents of such devices, only the name and metadata.
            .. epigraph::

               AWS DataSync can't sync the actual contents of such devices, because they are nonterminal and don't return an end-of-file (EOF) marker.

            Default value: ``NONE``

            ``NONE`` : Ignore special devices (recommended).

            ``PRESERVE`` : Preserve character and block device metadata. This option isn't currently supported for Amazon EFS.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html#cfn-datasync-task-options-preservedevices
            '''
            result = self._values.get("preserve_devices")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def security_descriptor_copy_flags(self) -> typing.Optional[builtins.str]:
            '''A value that determines which components of the SMB security descriptor are copied from source to destination objects.

            This value is only used for transfers between SMB and Amazon FSx for Windows File Server locations, or between two Amazon FSx for Windows File Server locations. For more information about how DataSync handles metadata, see `How DataSync Handles Metadata and Special Files <https://docs.aws.amazon.com/datasync/latest/userguide/special-files.html>`_ .

            Default value: ``OWNER_DACL``

            ``OWNER_DACL`` : For each copied object, DataSync copies the following metadata:

            - Object owner.
            - NTFS discretionary access control lists (DACLs), which determine whether to grant access to an object.

            When you use option, DataSync does NOT copy the NTFS system access control lists (SACLs), which are used by administrators to log attempts to access a secured object.

            ``OWNER_DACL_SACL`` : For each copied object, DataSync copies the following metadata:

            - Object owner.
            - NTFS discretionary access control lists (DACLs), which determine whether to grant access to an object.
            - NTFS system access control lists (SACLs), which are used by administrators to log attempts to access a secured object.

            Copying SACLs requires granting additional permissions to the Windows user that DataSync uses to access your SMB location. For information about choosing a user that ensures sufficient permissions to files, folders, and metadata, see `user <https://docs.aws.amazon.com/datasync/latest/userguide/create-smb-location.html#SMBuser>`_ .

            ``NONE`` : None of the SMB security descriptor components are copied. Destination objects are owned by the user that was provided for accessing the destination location. DACLs and SACLs are set based on the destination server’s configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html#cfn-datasync-task-options-securitydescriptorcopyflags
            '''
            result = self._values.get("security_descriptor_copy_flags")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def task_queueing(self) -> typing.Optional[builtins.str]:
            '''Specifies whether your transfer tasks should be put into a queue during certain scenarios when `running multiple tasks <https://docs.aws.amazon.com/datasync/latest/userguide/run-task.html#running-multiple-tasks>`_ . This is ``ENABLED`` by default.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html#cfn-datasync-task-options-taskqueueing
            '''
            result = self._values.get("task_queueing")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def transfer_mode(self) -> typing.Optional[builtins.str]:
            '''A value that determines whether DataSync transfers only the data and metadata that differ between the source and the destination location, or whether DataSync transfers all the content from the source, without comparing it to the destination location.

            ``CHANGED`` : DataSync copies only data or metadata that is new or different from the source location to the destination location.

            ``ALL`` : DataSync copies all source location content to the destination, without comparing it to existing content on the destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html#cfn-datasync-task-options-transfermode
            '''
            result = self._values.get("transfer_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def uid(self) -> typing.Optional[builtins.str]:
            '''The user ID (UID) of the file's owner.

            Default value: ``INT_VALUE``

            ``INT_VALUE`` : Preserve the integer value of the UID and group ID (GID) (recommended).

            ``NAME`` : Currently not supported

            ``NONE`` : Ignore the UID and GID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html#cfn-datasync-task-options-uid
            '''
            result = self._values.get("uid")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def verify_mode(self) -> typing.Optional[builtins.str]:
            '''A value that determines whether a data integrity verification is performed at the end of a task execution after all data and metadata have been transferred.

            For more information, see `Configure task settings <https://docs.aws.amazon.com/datasync/latest/userguide/create-task.html>`_ .

            Default value: ``POINT_IN_TIME_CONSISTENT``

            ``ONLY_FILES_TRANSFERRED`` (recommended): Perform verification only on files that were transferred.

            ``POINT_IN_TIME_CONSISTENT`` : Scan the entire source and entire destination at the end of the transfer to verify that the source and destination are fully synchronized. This option isn't supported when transferring to S3 Glacier or S3 Glacier Deep Archive storage classes.

            ``NONE`` : No additional verification is done at the end of the transfer, but all data transmissions are integrity-checked with checksum verification during the transfer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html#cfn-datasync-task-options-verifymode
            '''
            result = self._values.get("verify_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnTaskPropsMixin.OverridesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "deleted": "deleted",
            "skipped": "skipped",
            "transferred": "transferred",
            "verified": "verified",
        },
    )
    class OverridesProperty:
        def __init__(
            self,
            *,
            deleted: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTaskPropsMixin.DeletedProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            skipped: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTaskPropsMixin.SkippedProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            transferred: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTaskPropsMixin.TransferredProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            verified: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTaskPropsMixin.VerifiedProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Customizes the reporting level for aspects of your task report.

            For example, your report might generally only include errors, but you could specify that you want a list of successes and errors just for the files that Datasync attempted to delete in your destination location.

            :param deleted: Specifies the level of reporting for the files, objects, and directories that Datasync attempted to delete in your destination location. This only applies if you configure your task to delete data in the destination that isn't in the source.
            :param skipped: Specifies the level of reporting for the files, objects, and directories that Datasync attempted to skip during your transfer.
            :param transferred: Specifies the level of reporting for the files, objects, and directories that Datasync attempted to transfer.
            :param verified: Specifies the level of reporting for the files, objects, and directories that Datasync attempted to verify at the end of your transfer. This only applies if you configure your task to verify data during and after the transfer (which Datasync does by default)

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-overrides.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
                
                overrides_property = datasync_mixins.CfnTaskPropsMixin.OverridesProperty(
                    deleted=datasync_mixins.CfnTaskPropsMixin.DeletedProperty(
                        report_level="reportLevel"
                    ),
                    skipped=datasync_mixins.CfnTaskPropsMixin.SkippedProperty(
                        report_level="reportLevel"
                    ),
                    transferred=datasync_mixins.CfnTaskPropsMixin.TransferredProperty(
                        report_level="reportLevel"
                    ),
                    verified=datasync_mixins.CfnTaskPropsMixin.VerifiedProperty(
                        report_level="reportLevel"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7e0b6b93a9ac50f1f33263560ab2352640da4dad4edcfc5d660ec567f39495b4)
                check_type(argname="argument deleted", value=deleted, expected_type=type_hints["deleted"])
                check_type(argname="argument skipped", value=skipped, expected_type=type_hints["skipped"])
                check_type(argname="argument transferred", value=transferred, expected_type=type_hints["transferred"])
                check_type(argname="argument verified", value=verified, expected_type=type_hints["verified"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if deleted is not None:
                self._values["deleted"] = deleted
            if skipped is not None:
                self._values["skipped"] = skipped
            if transferred is not None:
                self._values["transferred"] = transferred
            if verified is not None:
                self._values["verified"] = verified

        @builtins.property
        def deleted(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskPropsMixin.DeletedProperty"]]:
            '''Specifies the level of reporting for the files, objects, and directories that Datasync attempted to delete in your destination location.

            This only applies if you configure your task to delete data in the destination that isn't in the source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-overrides.html#cfn-datasync-task-overrides-deleted
            '''
            result = self._values.get("deleted")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskPropsMixin.DeletedProperty"]], result)

        @builtins.property
        def skipped(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskPropsMixin.SkippedProperty"]]:
            '''Specifies the level of reporting for the files, objects, and directories that Datasync attempted to skip during your transfer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-overrides.html#cfn-datasync-task-overrides-skipped
            '''
            result = self._values.get("skipped")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskPropsMixin.SkippedProperty"]], result)

        @builtins.property
        def transferred(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskPropsMixin.TransferredProperty"]]:
            '''Specifies the level of reporting for the files, objects, and directories that Datasync attempted to transfer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-overrides.html#cfn-datasync-task-overrides-transferred
            '''
            result = self._values.get("transferred")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskPropsMixin.TransferredProperty"]], result)

        @builtins.property
        def verified(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskPropsMixin.VerifiedProperty"]]:
            '''Specifies the level of reporting for the files, objects, and directories that Datasync attempted to verify at the end of your transfer.

            This only applies if you configure your task to verify data during and after the transfer (which Datasync does by default)

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-overrides.html#cfn-datasync-task-overrides-verified
            '''
            result = self._values.get("verified")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskPropsMixin.VerifiedProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OverridesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnTaskPropsMixin.S3Property",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_access_role_arn": "bucketAccessRoleArn",
            "s3_bucket_arn": "s3BucketArn",
            "subdirectory": "subdirectory",
        },
    )
    class S3Property:
        def __init__(
            self,
            *,
            bucket_access_role_arn: typing.Optional[builtins.str] = None,
            s3_bucket_arn: typing.Optional[builtins.str] = None,
            subdirectory: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param bucket_access_role_arn: 
            :param s3_bucket_arn: 
            :param subdirectory: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-s3.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
                
                s3_property = datasync_mixins.CfnTaskPropsMixin.S3Property(
                    bucket_access_role_arn="bucketAccessRoleArn",
                    s3_bucket_arn="s3BucketArn",
                    subdirectory="subdirectory"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__62db86586683b3fcfcfa81793611f694e37765c3070d7a71629f91c635fc6c2c)
                check_type(argname="argument bucket_access_role_arn", value=bucket_access_role_arn, expected_type=type_hints["bucket_access_role_arn"])
                check_type(argname="argument s3_bucket_arn", value=s3_bucket_arn, expected_type=type_hints["s3_bucket_arn"])
                check_type(argname="argument subdirectory", value=subdirectory, expected_type=type_hints["subdirectory"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_access_role_arn is not None:
                self._values["bucket_access_role_arn"] = bucket_access_role_arn
            if s3_bucket_arn is not None:
                self._values["s3_bucket_arn"] = s3_bucket_arn
            if subdirectory is not None:
                self._values["subdirectory"] = subdirectory

        @builtins.property
        def bucket_access_role_arn(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-s3.html#cfn-datasync-task-s3-bucketaccessrolearn
            '''
            result = self._values.get("bucket_access_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_bucket_arn(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-s3.html#cfn-datasync-task-s3-s3bucketarn
            '''
            result = self._values.get("s3_bucket_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def subdirectory(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-s3.html#cfn-datasync-task-s3-subdirectory
            '''
            result = self._values.get("subdirectory")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnTaskPropsMixin.SkippedProperty",
        jsii_struct_bases=[],
        name_mapping={"report_level": "reportLevel"},
    )
    class SkippedProperty:
        def __init__(
            self,
            *,
            report_level: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the level of reporting for the files, objects, and directories that Datasync attempted to skip during your transfer.

            :param report_level: Specifies whether you want your task report to include only what went wrong with your transfer or a list of what succeeded and didn't.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-skipped.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
                
                skipped_property = datasync_mixins.CfnTaskPropsMixin.SkippedProperty(
                    report_level="reportLevel"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d5a593a15d461357d12fd9516cf735e0b83bec8ad3434a8ca02bdded633a062f)
                check_type(argname="argument report_level", value=report_level, expected_type=type_hints["report_level"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if report_level is not None:
                self._values["report_level"] = report_level

        @builtins.property
        def report_level(self) -> typing.Optional[builtins.str]:
            '''Specifies whether you want your task report to include only what went wrong with your transfer or a list of what succeeded and didn't.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-skipped.html#cfn-datasync-task-skipped-reportlevel
            '''
            result = self._values.get("report_level")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SkippedProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnTaskPropsMixin.SourceProperty",
        jsii_struct_bases=[],
        name_mapping={"s3": "s3"},
    )
    class SourceProperty:
        def __init__(
            self,
            *,
            s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTaskPropsMixin.ManifestConfigSourceS3Property", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the manifest that you want DataSync to use and where it's hosted.

            :param s3: Specifies the S3 bucket where you're hosting the manifest that you want AWS DataSync to use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-source.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
                
                source_property = datasync_mixins.CfnTaskPropsMixin.SourceProperty(
                    s3=datasync_mixins.CfnTaskPropsMixin.ManifestConfigSourceS3Property(
                        bucket_access_role_arn="bucketAccessRoleArn",
                        manifest_object_path="manifestObjectPath",
                        manifest_object_version_id="manifestObjectVersionId",
                        s3_bucket_arn="s3BucketArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9206fcbdc6f42e5b92766412758371ff516e5ce85b01d4448217f7946a9dde4b)
                check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3 is not None:
                self._values["s3"] = s3

        @builtins.property
        def s3(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskPropsMixin.ManifestConfigSourceS3Property"]]:
            '''Specifies the S3 bucket where you're hosting the manifest that you want AWS DataSync to use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-source.html#cfn-datasync-task-source-s3
            '''
            result = self._values.get("s3")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskPropsMixin.ManifestConfigSourceS3Property"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnTaskPropsMixin.TaskReportConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination": "destination",
            "object_version_ids": "objectVersionIds",
            "output_type": "outputType",
            "overrides": "overrides",
            "report_level": "reportLevel",
        },
    )
    class TaskReportConfigProperty:
        def __init__(
            self,
            *,
            destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTaskPropsMixin.DestinationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            object_version_ids: typing.Optional[builtins.str] = None,
            output_type: typing.Optional[builtins.str] = None,
            overrides: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTaskPropsMixin.OverridesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            report_level: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies how you want to configure a task report, which provides detailed information about for your AWS DataSync transfer.

            For more information, see `Task reports <https://docs.aws.amazon.com/datasync/latest/userguide/task-reports.html>`_ .

            :param destination: Specifies the Amazon S3 bucket where DataSync uploads your task report. For more information, see `Task reports <https://docs.aws.amazon.com/datasync/latest/userguide/task-reports.html#task-report-access>`_ .
            :param object_version_ids: Specifies whether your task report includes the new version of each object transferred into an S3 bucket. This only applies if you `enable versioning on your bucket <https://docs.aws.amazon.com/AmazonS3/latest/userguide/manage-versioning-examples.html>`_ . Keep in mind that setting this to ``INCLUDE`` can increase the duration of your task execution.
            :param output_type: Specifies the type of task report that you want:. - ``SUMMARY_ONLY`` : Provides necessary details about your task, including the number of files, objects, and directories transferred and transfer duration. - ``STANDARD`` : Provides complete details about your task, including a full list of files, objects, and directories that were transferred, skipped, verified, and more.
            :param overrides: Customizes the reporting level for aspects of your task report. For example, your report might generally only include errors, but you could specify that you want a list of successes and errors just for the files that DataSync attempted to delete in your destination location.
            :param report_level: Specifies whether you want your task report to include only what went wrong with your transfer or a list of what succeeded and didn't. - ``ERRORS_ONLY`` : A report shows what DataSync was unable to transfer, skip, verify, and delete. - ``SUCCESSES_AND_ERRORS`` : A report shows what DataSync was able and unable to transfer, skip, verify, and delete.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-taskreportconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
                
                task_report_config_property = datasync_mixins.CfnTaskPropsMixin.TaskReportConfigProperty(
                    destination=datasync_mixins.CfnTaskPropsMixin.DestinationProperty(
                        s3=datasync_mixins.CfnTaskPropsMixin.S3Property(
                            bucket_access_role_arn="bucketAccessRoleArn",
                            s3_bucket_arn="s3BucketArn",
                            subdirectory="subdirectory"
                        )
                    ),
                    object_version_ids="objectVersionIds",
                    output_type="outputType",
                    overrides=datasync_mixins.CfnTaskPropsMixin.OverridesProperty(
                        deleted=datasync_mixins.CfnTaskPropsMixin.DeletedProperty(
                            report_level="reportLevel"
                        ),
                        skipped=datasync_mixins.CfnTaskPropsMixin.SkippedProperty(
                            report_level="reportLevel"
                        ),
                        transferred=datasync_mixins.CfnTaskPropsMixin.TransferredProperty(
                            report_level="reportLevel"
                        ),
                        verified=datasync_mixins.CfnTaskPropsMixin.VerifiedProperty(
                            report_level="reportLevel"
                        )
                    ),
                    report_level="reportLevel"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3056034e344b889a8aff8994504d82f581f89b42f748f93659fa34070deb27c4)
                check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
                check_type(argname="argument object_version_ids", value=object_version_ids, expected_type=type_hints["object_version_ids"])
                check_type(argname="argument output_type", value=output_type, expected_type=type_hints["output_type"])
                check_type(argname="argument overrides", value=overrides, expected_type=type_hints["overrides"])
                check_type(argname="argument report_level", value=report_level, expected_type=type_hints["report_level"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination is not None:
                self._values["destination"] = destination
            if object_version_ids is not None:
                self._values["object_version_ids"] = object_version_ids
            if output_type is not None:
                self._values["output_type"] = output_type
            if overrides is not None:
                self._values["overrides"] = overrides
            if report_level is not None:
                self._values["report_level"] = report_level

        @builtins.property
        def destination(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskPropsMixin.DestinationProperty"]]:
            '''Specifies the Amazon S3 bucket where DataSync uploads your task report.

            For more information, see `Task reports <https://docs.aws.amazon.com/datasync/latest/userguide/task-reports.html#task-report-access>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-taskreportconfig.html#cfn-datasync-task-taskreportconfig-destination
            '''
            result = self._values.get("destination")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskPropsMixin.DestinationProperty"]], result)

        @builtins.property
        def object_version_ids(self) -> typing.Optional[builtins.str]:
            '''Specifies whether your task report includes the new version of each object transferred into an S3 bucket.

            This only applies if you `enable versioning on your bucket <https://docs.aws.amazon.com/AmazonS3/latest/userguide/manage-versioning-examples.html>`_ . Keep in mind that setting this to ``INCLUDE`` can increase the duration of your task execution.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-taskreportconfig.html#cfn-datasync-task-taskreportconfig-objectversionids
            '''
            result = self._values.get("object_version_ids")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def output_type(self) -> typing.Optional[builtins.str]:
            '''Specifies the type of task report that you want:.

            - ``SUMMARY_ONLY`` : Provides necessary details about your task, including the number of files, objects, and directories transferred and transfer duration.
            - ``STANDARD`` : Provides complete details about your task, including a full list of files, objects, and directories that were transferred, skipped, verified, and more.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-taskreportconfig.html#cfn-datasync-task-taskreportconfig-outputtype
            '''
            result = self._values.get("output_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def overrides(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskPropsMixin.OverridesProperty"]]:
            '''Customizes the reporting level for aspects of your task report.

            For example, your report might generally only include errors, but you could specify that you want a list of successes and errors just for the files that DataSync attempted to delete in your destination location.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-taskreportconfig.html#cfn-datasync-task-taskreportconfig-overrides
            '''
            result = self._values.get("overrides")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskPropsMixin.OverridesProperty"]], result)

        @builtins.property
        def report_level(self) -> typing.Optional[builtins.str]:
            '''Specifies whether you want your task report to include only what went wrong with your transfer or a list of what succeeded and didn't.

            - ``ERRORS_ONLY`` : A report shows what DataSync was unable to transfer, skip, verify, and delete.
            - ``SUCCESSES_AND_ERRORS`` : A report shows what DataSync was able and unable to transfer, skip, verify, and delete.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-taskreportconfig.html#cfn-datasync-task-taskreportconfig-reportlevel
            '''
            result = self._values.get("report_level")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TaskReportConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnTaskPropsMixin.TaskScheduleProperty",
        jsii_struct_bases=[],
        name_mapping={"schedule_expression": "scheduleExpression", "status": "status"},
    )
    class TaskScheduleProperty:
        def __init__(
            self,
            *,
            schedule_expression: typing.Optional[builtins.str] = None,
            status: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configures your AWS DataSync task to run on a `schedule <https://docs.aws.amazon.com/datasync/latest/userguide/task-scheduling.html>`_ (at a minimum interval of 1 hour).

            :param schedule_expression: Specifies your task schedule by using a cron or rate expression. Use cron expressions for task schedules that run on a specific time and day. For example, the following cron expression creates a task schedule that runs at 8 AM on the first Wednesday of every month: ``cron(0 8 * * 3#1)`` Use rate expressions for task schedules that run on a regular interval. For example, the following rate expression creates a task schedule that runs every 12 hours: ``rate(12 hours)`` For information about cron and rate expression syntax, see the `*Amazon EventBridge User Guide* <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-scheduled-rule-pattern.html>`_ .
            :param status: Specifies whether to enable or disable your task schedule. Your schedule is enabled by default, but there can be situations where you need to disable it. For example, you might need to pause a recurring transfer to fix an issue with your task or perform maintenance on your storage system. DataSync might disable your schedule automatically if your task fails repeatedly with the same error. For more information, see `TaskScheduleDetails <https://docs.aws.amazon.com/datasync/latest/userguide/API_TaskScheduleDetails.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-taskschedule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
                
                task_schedule_property = datasync_mixins.CfnTaskPropsMixin.TaskScheduleProperty(
                    schedule_expression="scheduleExpression",
                    status="status"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4ffd9f64847bf2f5fc9044c7b5e49d88f204195f847f3a2b1a44574fe2319afa)
                check_type(argname="argument schedule_expression", value=schedule_expression, expected_type=type_hints["schedule_expression"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if schedule_expression is not None:
                self._values["schedule_expression"] = schedule_expression
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def schedule_expression(self) -> typing.Optional[builtins.str]:
            '''Specifies your task schedule by using a cron or rate expression.

            Use cron expressions for task schedules that run on a specific time and day. For example, the following cron expression creates a task schedule that runs at 8 AM on the first Wednesday of every month:

            ``cron(0 8 * * 3#1)``

            Use rate expressions for task schedules that run on a regular interval. For example, the following rate expression creates a task schedule that runs every 12 hours:

            ``rate(12 hours)``

            For information about cron and rate expression syntax, see the `*Amazon EventBridge User Guide* <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-scheduled-rule-pattern.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-taskschedule.html#cfn-datasync-task-taskschedule-scheduleexpression
            '''
            result = self._values.get("schedule_expression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''Specifies whether to enable or disable your task schedule.

            Your schedule is enabled by default, but there can be situations where you need to disable it. For example, you might need to pause a recurring transfer to fix an issue with your task or perform maintenance on your storage system.

            DataSync might disable your schedule automatically if your task fails repeatedly with the same error. For more information, see `TaskScheduleDetails <https://docs.aws.amazon.com/datasync/latest/userguide/API_TaskScheduleDetails.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-taskschedule.html#cfn-datasync-task-taskschedule-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TaskScheduleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnTaskPropsMixin.TransferredProperty",
        jsii_struct_bases=[],
        name_mapping={"report_level": "reportLevel"},
    )
    class TransferredProperty:
        def __init__(
            self,
            *,
            report_level: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the level of reporting for the files, objects, and directories that Datasync attempted to transfer.

            :param report_level: Specifies whether you want your task report to include only what went wrong with your transfer or a list of what succeeded and didn't.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-transferred.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
                
                transferred_property = datasync_mixins.CfnTaskPropsMixin.TransferredProperty(
                    report_level="reportLevel"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0225b0488036f237bd3914fa64e68f62a7ae327228469caca1130200a40d53f9)
                check_type(argname="argument report_level", value=report_level, expected_type=type_hints["report_level"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if report_level is not None:
                self._values["report_level"] = report_level

        @builtins.property
        def report_level(self) -> typing.Optional[builtins.str]:
            '''Specifies whether you want your task report to include only what went wrong with your transfer or a list of what succeeded and didn't.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-transferred.html#cfn-datasync-task-transferred-reportlevel
            '''
            result = self._values.get("report_level")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TransferredProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datasync.mixins.CfnTaskPropsMixin.VerifiedProperty",
        jsii_struct_bases=[],
        name_mapping={"report_level": "reportLevel"},
    )
    class VerifiedProperty:
        def __init__(
            self,
            *,
            report_level: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the level of reporting for the files, objects, and directories that Datasync attempted to verify at the end of your transfer.

            This only applies if you configure your task to verify data during and after the transfer (which Datasync does by default)

            :param report_level: Specifies whether you want your task report to include only what went wrong with your transfer or a list of what succeeded and didn't.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-verified.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datasync import mixins as datasync_mixins
                
                verified_property = datasync_mixins.CfnTaskPropsMixin.VerifiedProperty(
                    report_level="reportLevel"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8c10fdce63761a763224bcffb17acf44811d4701c82cf6208cf62088af6c7d2a)
                check_type(argname="argument report_level", value=report_level, expected_type=type_hints["report_level"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if report_level is not None:
                self._values["report_level"] = report_level

        @builtins.property
        def report_level(self) -> typing.Optional[builtins.str]:
            '''Specifies whether you want your task report to include only what went wrong with your transfer or a list of what succeeded and didn't.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-verified.html#cfn-datasync-task-verified-reportlevel
            '''
            result = self._values.get("report_level")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VerifiedProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnAgentMixinProps",
    "CfnAgentPropsMixin",
    "CfnLocationAzureBlobMixinProps",
    "CfnLocationAzureBlobPropsMixin",
    "CfnLocationEFSMixinProps",
    "CfnLocationEFSPropsMixin",
    "CfnLocationFSxLustreMixinProps",
    "CfnLocationFSxLustrePropsMixin",
    "CfnLocationFSxONTAPMixinProps",
    "CfnLocationFSxONTAPPropsMixin",
    "CfnLocationFSxOpenZFSMixinProps",
    "CfnLocationFSxOpenZFSPropsMixin",
    "CfnLocationFSxWindowsMixinProps",
    "CfnLocationFSxWindowsPropsMixin",
    "CfnLocationHDFSMixinProps",
    "CfnLocationHDFSPropsMixin",
    "CfnLocationNFSMixinProps",
    "CfnLocationNFSPropsMixin",
    "CfnLocationObjectStorageMixinProps",
    "CfnLocationObjectStoragePropsMixin",
    "CfnLocationS3MixinProps",
    "CfnLocationS3PropsMixin",
    "CfnLocationSMBMixinProps",
    "CfnLocationSMBPropsMixin",
    "CfnTaskMixinProps",
    "CfnTaskPropsMixin",
]

publication.publish()

def _typecheckingstub__2d7d4b26d9f158899fae559f9c890079968a2368d819b5bd1dd4438329578ab4(
    *,
    activation_key: typing.Optional[builtins.str] = None,
    agent_name: typing.Optional[builtins.str] = None,
    security_group_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_endpoint_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a65940522089a7f8ef836f336e68c65f01eedba3e7ed01a6c520643b49ea42e0(
    props: typing.Union[CfnAgentMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41600be1a89df94cc8258d7690a94d0f560bca09f64b341210bcfeba419435ad(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a2012611f3af3dd0317a80564291068f63274a325d3049bd456418ff29c34a6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67951bcbec4c86da66984ecc87e648fea5ab58f81cd3b5d7d2d9679b6fb288c3(
    *,
    agent_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    azure_access_tier: typing.Optional[builtins.str] = None,
    azure_blob_authentication_type: typing.Optional[builtins.str] = None,
    azure_blob_container_url: typing.Optional[builtins.str] = None,
    azure_blob_sas_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLocationAzureBlobPropsMixin.AzureBlobSasConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    azure_blob_type: typing.Optional[builtins.str] = None,
    cmk_secret_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLocationAzureBlobPropsMixin.CmkSecretConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    custom_secret_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLocationAzureBlobPropsMixin.CustomSecretConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfe247a39ab08b5fb90c9385c6e0eae46366bca760b52d4f73d35fa197cb05a2(
    props: typing.Union[CfnLocationAzureBlobMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7114695f5f2ec1586a6d1f27fafbf3dfe9d37e5a409b2af750d1528ffb70cb80(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1a61b7f591ecdd66d2670ca1e80f7f9f333ce2a255aa08c7693dcb34e32e148(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14518bd8f202346c76820b9c4d27950d9a4e5fb259be0e26bdfec531651fec50(
    *,
    azure_blob_sas_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b09e2923bcb8a00a6809a590350ccd7934e31670599d7cf878c47947d6049f4(
    *,
    kms_key_arn: typing.Optional[builtins.str] = None,
    secret_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dce7e81c193e9850efff4f58f2722c7eaf9354512cd8da636cb8e9236e39b6b(
    *,
    secret_access_role_arn: typing.Optional[builtins.str] = None,
    secret_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aa1625ab26252b7cf9ec933c9cb0688cfa2ed9c0944add4299eceb38ad7fefa(
    *,
    secret_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae34944de38d87d1b06e65c9cc28e881fcbf025a9a2fc9f01d59d6a1a5e102e2(
    *,
    access_point_arn: typing.Optional[builtins.str] = None,
    ec2_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLocationEFSPropsMixin.Ec2ConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    efs_filesystem_arn: typing.Optional[builtins.str] = None,
    file_system_access_role_arn: typing.Optional[builtins.str] = None,
    in_transit_encryption: typing.Optional[builtins.str] = None,
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__573d52c7904564165bbd3df6d0f54e94cc70fbbbc2010d40e8ba2227d30e2b54(
    props: typing.Union[CfnLocationEFSMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b297a0b06bb833d04e972efc96ef19ec7969d712f36c40020f18258f93aca4f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__677566f29bc34951d9704c619bf330d64f8e1fd080a7404751d11ff2345228bb(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3acf17eee817f4ce5fc3c2e9d9a2a64e626a3b78e0d1eb6763cfb259db839da7(
    *,
    security_group_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df6ff31826a0beb0cd1646320b66171d62ee204afe5d72676ff6cad6524d678e(
    *,
    fsx_filesystem_arn: typing.Optional[builtins.str] = None,
    security_group_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8407ef1349bb5f56b8ebb237e8dd80c1a4f4a591b6bb8805758184730fe76863(
    props: typing.Union[CfnLocationFSxLustreMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b9067c95729e3fc5e916596d47bbd124e56572fb9586883adae097f06d08984(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2af2bbfe1027387526ef37bd6a548375d6424420f951d7404a998acd683d1c24(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__667c2d0f299966414edd21d1ff6a903d3ad6d50eb172e531c57d8d67a825c89d(
    *,
    protocol: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLocationFSxONTAPPropsMixin.ProtocolProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    security_group_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    storage_virtual_machine_arn: typing.Optional[builtins.str] = None,
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2b309c8a891e240b2131c0180bd10702f98cfd4c7ed286672a5156c9a6d7fe2(
    props: typing.Union[CfnLocationFSxONTAPMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88c96cbb1c504b34b6ae32ef99efa82fde0ddf630fe074b48255275e808d65a0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02017f238138b2ac0a7a0bb64c1600791e2dc55d0d021fd42ca2695485c84e0b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78ee71dad9d5850fd4000573f9ce217346b578b062b42ff396ad1817281dbfa1(
    *,
    mount_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLocationFSxONTAPPropsMixin.NfsMountOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc1dc3f334d63bdf9ec100ef1d51832f13ea840464f53bdfb3828625111c2f66(
    *,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2a64d2a8b6cd443b425c69cd529ffc944119b8c377b1dd408995a3dc6d89d82(
    *,
    nfs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLocationFSxONTAPPropsMixin.NFSProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    smb: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLocationFSxONTAPPropsMixin.SMBProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f65078aa7ceb43e6ecf3c39f60d7c7286a334dd113c870354ea398d7bcd0bb5(
    *,
    domain: typing.Optional[builtins.str] = None,
    mount_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLocationFSxONTAPPropsMixin.SmbMountOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    password: typing.Optional[builtins.str] = None,
    user: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98a9583555011c9c3362edcb41dbd8b27ab39ec5e7be5db661cfe1f8eb2762eb(
    *,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d10dcb7b4728c6606e0100e14010d2ed9c174305c88a601d1b3f0ce271afb86(
    *,
    fsx_filesystem_arn: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLocationFSxOpenZFSPropsMixin.ProtocolProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    security_group_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0824e2cfd74162218f82fcdc39a1c5ae4b9cfc10caef8334637288682394608e(
    props: typing.Union[CfnLocationFSxOpenZFSMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aef43e68cd2f62cbc54e17d06a103fd57caeb2c3dcf12652d65387fabd7b477(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a48448457fec0e501747a2a0a94444335f34d0cd4edca08a90ba0ce8b7d0424e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b84d624d1174a64ccdb4b414248cce02b9f5e3d203d8fb6af3ca5066c5026017(
    *,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d4d44c314b8aeecf19bde222f3bd99a8d5b2ae94c2e506917a7d188fda0d53b(
    *,
    mount_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLocationFSxOpenZFSPropsMixin.MountOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b6bb88b3242797dafd6d16c8fda57f8d1ee9e8688c54bb47f1955e3b79505cf(
    *,
    nfs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLocationFSxOpenZFSPropsMixin.NFSProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20b4ada2de7d454b794a5399617cd50b6e5bb69953c7b8565922085c6c1e4441(
    *,
    domain: typing.Optional[builtins.str] = None,
    fsx_filesystem_arn: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    security_group_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    user: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__749472fa57712afd2fd6c279839d193d58de96b3c214179a37a768ad33ed3a62(
    props: typing.Union[CfnLocationFSxWindowsMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92b985ce733a45be8d3a5a76716dd163ea32d5e43f7a2b16f6f58db3673cddd3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5fa8d48fd6d61cb4bb5faa87e0a4dd17fa7c96d171fe83e3ba11cbe662bce42(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0187c6f0cf30a18094c17379d9509f1658ebe223cee0384d47baeda748c8f895(
    *,
    agent_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    authentication_type: typing.Optional[builtins.str] = None,
    block_size: typing.Optional[jsii.Number] = None,
    kerberos_keytab: typing.Optional[builtins.str] = None,
    kerberos_krb5_conf: typing.Optional[builtins.str] = None,
    kerberos_principal: typing.Optional[builtins.str] = None,
    kms_key_provider_uri: typing.Optional[builtins.str] = None,
    name_nodes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLocationHDFSPropsMixin.NameNodeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    qop_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLocationHDFSPropsMixin.QopConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    replication_factor: typing.Optional[jsii.Number] = None,
    simple_user: typing.Optional[builtins.str] = None,
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e21015cde3d5a1222e09c1c85e8463a7b207760b9ca1b81140a3e96bb54fed92(
    props: typing.Union[CfnLocationHDFSMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60a2f4204244aaf404e41eb479a3f69b4b6890df88466a04ec1b81145a140d29(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad3e05fc945c76530c387f2c1646833b8a39855bad6f0ed05addbb03aa564f6f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bc52206954aa9bc6ff20021519027203cf31eed7ec8e3fb16a403feee5bf199(
    *,
    hostname: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6c8596dfe59a5234a9f5be7da8f5b1253a80fe148174dc4edc66a86746cfb34(
    *,
    data_transfer_protection: typing.Optional[builtins.str] = None,
    rpc_protection: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ada638f32c0f0f174bca979ed1ba88215f29cd914120d31600705c140ea07dfb(
    *,
    mount_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLocationNFSPropsMixin.MountOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    on_prem_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLocationNFSPropsMixin.OnPremConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    server_hostname: typing.Optional[builtins.str] = None,
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49f478964494ffeb95b93101c9479a834025a966d819800e3fae90e1f45e0af9(
    props: typing.Union[CfnLocationNFSMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__671cae39883f866987bd96781d9ae7430ea1ae8b15e0821615e32e580efb2df3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b764a79077c12cedef360b1304b7d603214d97821298769c6d27dfffe4daf9e3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e703d7f420543484e20dfc5e10e272415e866d1f7dcc7c31430fb795558df1c7(
    *,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb51a6f879a2d1e491c4ffd87d9a9c1b2ed8eb7cbd631b0d1fb1c06c899b1fc2(
    *,
    agent_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbe0ebd284440526d635f8eae1b7373d04b3939929aa541a2f6d5c6d738a7f7b(
    *,
    access_key: typing.Optional[builtins.str] = None,
    agent_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    bucket_name: typing.Optional[builtins.str] = None,
    cmk_secret_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLocationObjectStoragePropsMixin.CmkSecretConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    custom_secret_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLocationObjectStoragePropsMixin.CustomSecretConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    secret_key: typing.Optional[builtins.str] = None,
    server_certificate: typing.Optional[builtins.str] = None,
    server_hostname: typing.Optional[builtins.str] = None,
    server_port: typing.Optional[jsii.Number] = None,
    server_protocol: typing.Optional[builtins.str] = None,
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e789c05d1b4756ff600d44cb7bde66733dff21b5db8b90bdb7b3e545c523d12a(
    props: typing.Union[CfnLocationObjectStorageMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad905740c3cce3d6ffca2ca438b0a62ef07a052cfd39057dfbdd836187c699f2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__618ea8be1f7f7d2bf56013972da49d61c9e7bf6eb7436b700779df7b11de748f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bfe345346efd3deb6aac94e9ff19c7aff7c46eb170fede8d4a4a080cd9250e7(
    *,
    kms_key_arn: typing.Optional[builtins.str] = None,
    secret_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39241196e53799d1361a71e778596a390aebba75c48ad47a9151f400fe523027(
    *,
    secret_access_role_arn: typing.Optional[builtins.str] = None,
    secret_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b71a9d5790f11e2ac1f1d619ce12a79dc5d33768ec161ba58a765ef6fb13d71(
    *,
    secret_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__656eb6bb026f0c3f34441309f36f73fe36d3d24858ceecf249da584b3c461938(
    *,
    s3_bucket_arn: typing.Optional[builtins.str] = None,
    s3_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLocationS3PropsMixin.S3ConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_storage_class: typing.Optional[builtins.str] = None,
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__415c0d71ed755061dad92a43d06b3447026976fa22a594224f159ff3e6c22936(
    props: typing.Union[CfnLocationS3MixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92e047460a21fa9c0107c94f41635712ad431b6c29595072943fcce763f9cdc7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cafdae1aef2d6882140388fddf767ffd112c8debe8aef68ceb30998797ed73cd(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__644bbf37d26e2680a087414f9f8732d79a89aacf3332d3ba59a1ec95eb0c5bb7(
    *,
    bucket_access_role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7d429531019a939be774c6ae4a4ca85dc87c258d2542dadc14546d4a9235e5f(
    *,
    agent_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    authentication_type: typing.Optional[builtins.str] = None,
    cmk_secret_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLocationSMBPropsMixin.CmkSecretConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    custom_secret_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLocationSMBPropsMixin.CustomSecretConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dns_ip_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    domain: typing.Optional[builtins.str] = None,
    kerberos_keytab: typing.Optional[builtins.str] = None,
    kerberos_krb5_conf: typing.Optional[builtins.str] = None,
    kerberos_principal: typing.Optional[builtins.str] = None,
    mount_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLocationSMBPropsMixin.MountOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    password: typing.Optional[builtins.str] = None,
    server_hostname: typing.Optional[builtins.str] = None,
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    user: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3f3a18717cf39ef1d7e4f2416b655db54c978709f67d34437e5e3bce5175b75(
    props: typing.Union[CfnLocationSMBMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4263f4fb101808df8a91a9fc3e164cc1546e206598743760e5e3afbe95a78d4e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69f836fd342c50c89773448e71d40ae19261f67601ba772930a8813fbaf8ba09(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5469c1fbd310b23a62274a06930d7c86228cd37e3e6e581c674c5704fd9b59ed(
    *,
    kms_key_arn: typing.Optional[builtins.str] = None,
    secret_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__851d7b600fa1338b3f6f0b57edd688e5f47f5e17ade25dcfc8057350ea58e1a2(
    *,
    secret_access_role_arn: typing.Optional[builtins.str] = None,
    secret_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f4ba9fcfa4421bb729413b89333f25150d9a3d0327531f7e617f263b631ae95(
    *,
    secret_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90cfe3a95a2f7af220983de86fe4c7daad60483ed0f587c54c4c9583525aa77c(
    *,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cd24647ab1bd031aa4f0ce1758f29f57c6a8aaca31fee525466cea4db090603(
    *,
    cloud_watch_log_group_arn: typing.Optional[builtins.str] = None,
    destination_location_arn: typing.Optional[builtins.str] = None,
    excludes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTaskPropsMixin.FilterRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    includes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTaskPropsMixin.FilterRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    manifest_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTaskPropsMixin.ManifestConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTaskPropsMixin.OptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    schedule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTaskPropsMixin.TaskScheduleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    source_location_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    task_mode: typing.Optional[builtins.str] = None,
    task_report_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTaskPropsMixin.TaskReportConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14d57e5aa12bdcf06cc1627e7cfa6e8c86aa8bdc657e0865a35a22f7888eab64(
    props: typing.Union[CfnTaskMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26918e3f47aa37fdf914c653ea3c15b622c53d6bb8783d0e68188d989f0c9d3f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82b2ebe6cfe18103e280b05a84db8ba77dee36e00b9b51031a8f44040c651c89(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b30a01031a7c22b1f8de5b4df730f476b962ea398321fdfd0d370d22a8d57c3(
    *,
    report_level: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f08afa70199d4e0348c183196ede7a43ad406ffe9659dc9d6ec841310c9cab0(
    *,
    s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTaskPropsMixin.S3Property, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2255697b19fa11c754964d96d9043eff5784d95083d1dff53a99883ca8e55dbc(
    *,
    filter_type: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40272ee1902201b1f35caa63d858041621d9049eebd9dcf631061b5941681be7(
    *,
    action: typing.Optional[builtins.str] = None,
    format: typing.Optional[builtins.str] = None,
    source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTaskPropsMixin.SourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5786c00148d8574a3b16a4d63fb20995bdadbf31b86c1acc1d191f2c2b6eb9d(
    *,
    bucket_access_role_arn: typing.Optional[builtins.str] = None,
    manifest_object_path: typing.Optional[builtins.str] = None,
    manifest_object_version_id: typing.Optional[builtins.str] = None,
    s3_bucket_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bb3689cfbc145157b41909be370c4455b75c32204f75eacd61753fe9e88e487(
    *,
    atime: typing.Optional[builtins.str] = None,
    bytes_per_second: typing.Optional[jsii.Number] = None,
    gid: typing.Optional[builtins.str] = None,
    log_level: typing.Optional[builtins.str] = None,
    mtime: typing.Optional[builtins.str] = None,
    object_tags: typing.Optional[builtins.str] = None,
    overwrite_mode: typing.Optional[builtins.str] = None,
    posix_permissions: typing.Optional[builtins.str] = None,
    preserve_deleted_files: typing.Optional[builtins.str] = None,
    preserve_devices: typing.Optional[builtins.str] = None,
    security_descriptor_copy_flags: typing.Optional[builtins.str] = None,
    task_queueing: typing.Optional[builtins.str] = None,
    transfer_mode: typing.Optional[builtins.str] = None,
    uid: typing.Optional[builtins.str] = None,
    verify_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e0b6b93a9ac50f1f33263560ab2352640da4dad4edcfc5d660ec567f39495b4(
    *,
    deleted: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTaskPropsMixin.DeletedProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    skipped: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTaskPropsMixin.SkippedProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    transferred: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTaskPropsMixin.TransferredProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    verified: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTaskPropsMixin.VerifiedProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62db86586683b3fcfcfa81793611f694e37765c3070d7a71629f91c635fc6c2c(
    *,
    bucket_access_role_arn: typing.Optional[builtins.str] = None,
    s3_bucket_arn: typing.Optional[builtins.str] = None,
    subdirectory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5a593a15d461357d12fd9516cf735e0b83bec8ad3434a8ca02bdded633a062f(
    *,
    report_level: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9206fcbdc6f42e5b92766412758371ff516e5ce85b01d4448217f7946a9dde4b(
    *,
    s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTaskPropsMixin.ManifestConfigSourceS3Property, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3056034e344b889a8aff8994504d82f581f89b42f748f93659fa34070deb27c4(
    *,
    destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTaskPropsMixin.DestinationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    object_version_ids: typing.Optional[builtins.str] = None,
    output_type: typing.Optional[builtins.str] = None,
    overrides: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTaskPropsMixin.OverridesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    report_level: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ffd9f64847bf2f5fc9044c7b5e49d88f204195f847f3a2b1a44574fe2319afa(
    *,
    schedule_expression: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0225b0488036f237bd3914fa64e68f62a7ae327228469caca1130200a40d53f9(
    *,
    report_level: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c10fdce63761a763224bcffb17acf44811d4701c82cf6208cf62088af6c7d2a(
    *,
    report_level: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
