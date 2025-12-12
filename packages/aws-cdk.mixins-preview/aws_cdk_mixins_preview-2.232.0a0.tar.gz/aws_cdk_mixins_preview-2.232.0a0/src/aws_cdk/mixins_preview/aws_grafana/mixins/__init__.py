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
    jsii_type="@aws-cdk/mixins-preview.aws_grafana.mixins.CfnWorkspaceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "account_access_type": "accountAccessType",
        "authentication_providers": "authenticationProviders",
        "client_token": "clientToken",
        "data_sources": "dataSources",
        "description": "description",
        "grafana_version": "grafanaVersion",
        "name": "name",
        "network_access_control": "networkAccessControl",
        "notification_destinations": "notificationDestinations",
        "organizational_units": "organizationalUnits",
        "organization_role_name": "organizationRoleName",
        "permission_type": "permissionType",
        "plugin_admin_enabled": "pluginAdminEnabled",
        "role_arn": "roleArn",
        "saml_configuration": "samlConfiguration",
        "stack_set_name": "stackSetName",
        "vpc_configuration": "vpcConfiguration",
    },
)
class CfnWorkspaceMixinProps:
    def __init__(
        self,
        *,
        account_access_type: typing.Optional[builtins.str] = None,
        authentication_providers: typing.Optional[typing.Sequence[builtins.str]] = None,
        client_token: typing.Optional[builtins.str] = None,
        data_sources: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        grafana_version: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        network_access_control: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkspacePropsMixin.NetworkAccessControlProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        notification_destinations: typing.Optional[typing.Sequence[builtins.str]] = None,
        organizational_units: typing.Optional[typing.Sequence[builtins.str]] = None,
        organization_role_name: typing.Optional[builtins.str] = None,
        permission_type: typing.Optional[builtins.str] = None,
        plugin_admin_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        role_arn: typing.Optional[builtins.str] = None,
        saml_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkspacePropsMixin.SamlConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        stack_set_name: typing.Optional[builtins.str] = None,
        vpc_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkspacePropsMixin.VpcConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnWorkspacePropsMixin.

        :param account_access_type: Specifies whether the workspace can access AWS resources in this AWS account only, or whether it can also access AWS resources in other accounts in the same organization. If this is ``ORGANIZATION`` , the ``OrganizationalUnits`` parameter specifies which organizational units the workspace can access.
        :param authentication_providers: Specifies whether this workspace uses SAML 2.0, AWS IAM Identity Center , or both to authenticate users for using the Grafana console within a workspace. For more information, see `User authentication in Amazon Managed Grafana <https://docs.aws.amazon.com/grafana/latest/userguide/authentication-in-AMG.html>`_ . *Allowed Values* : ``AWS_SSO | SAML``
        :param client_token: A unique, case-sensitive, user-provided identifier to ensure the idempotency of the request.
        :param data_sources: Specifies the AWS data sources that have been configured to have IAM roles and permissions created to allow Amazon Managed Grafana to read data from these sources. This list is only used when the workspace was created through the AWS console, and the ``permissionType`` is ``SERVICE_MANAGED`` .
        :param description: The user-defined description of the workspace.
        :param grafana_version: Specifies the version of Grafana to support in the workspace. Defaults to the latest version on create (for example, 9.4), or the current version of the workspace on update. Can only be used to upgrade (for example, from 8.4 to 9.4), not downgrade (for example, from 9.4 to 8.4). To know what versions are available to upgrade to for a specific workspace, see the `ListVersions <https://docs.aws.amazon.com/grafana/latest/APIReference/API_ListVersions.html>`_ operation.
        :param name: The name of the workspace.
        :param network_access_control: The configuration settings for network access to your workspace.
        :param notification_destinations: The AWS notification channels that Amazon Managed Grafana can automatically create IAM roles and permissions for, to allow Amazon Managed Grafana to use these channels. *AllowedValues* : ``SNS``
        :param organizational_units: Specifies the organizational units that this workspace is allowed to use data sources from, if this workspace is in an account that is part of an organization.
        :param organization_role_name: The name of the IAM role that is used to access resources through Organizations.
        :param permission_type: If this is ``SERVICE_MANAGED`` , and the workplace was created through the Amazon Managed Grafana console, then Amazon Managed Grafana automatically creates the IAM roles and provisions the permissions that the workspace needs to use AWS data sources and notification channels. If this is ``CUSTOMER_MANAGED`` , you must manage those roles and permissions yourself. If you are working with a workspace in a member account of an organization and that account is not a delegated administrator account, and you want the workspace to access data sources in other AWS accounts in the organization, this parameter must be set to ``CUSTOMER_MANAGED`` . For more information about converting between customer and service managed, see `Managing permissions for data sources and notification channels <https://docs.aws.amazon.com/grafana/latest/userguide/AMG-datasource-and-notification.html>`_ . For more information about the roles and permissions that must be managed for customer managed workspaces, see `Amazon Managed Grafana permissions and policies for AWS data sources and notification channels <https://docs.aws.amazon.com/grafana/latest/userguide/AMG-manage-permissions.html>`_
        :param plugin_admin_enabled: Whether plugin administration is enabled in the workspace. Setting to ``true`` allows workspace admins to install, uninstall, and update plugins from within the Grafana workspace. .. epigraph:: This option is only valid for workspaces that support Grafana version 9 or newer.
        :param role_arn: The IAM role that grants permissions to the AWS resources that the workspace will view data from. This role must already exist.
        :param saml_configuration: If the workspace uses SAML, use this structure to map SAML assertion attributes to workspace user information and define which groups in the assertion attribute are to have the ``Admin`` and ``Editor`` roles in the workspace.
        :param stack_set_name: The name of the AWS CloudFormation stack set that is used to generate IAM roles to be used for this workspace.
        :param vpc_configuration: The configuration settings for an Amazon VPC that contains data sources for your Grafana workspace to connect to. .. epigraph:: Connecting to a private VPC is not yet available in the Asia Pacific (Seoul) Region (ap-northeast-2).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_grafana import mixins as grafana_mixins
            
            cfn_workspace_mixin_props = grafana_mixins.CfnWorkspaceMixinProps(
                account_access_type="accountAccessType",
                authentication_providers=["authenticationProviders"],
                client_token="clientToken",
                data_sources=["dataSources"],
                description="description",
                grafana_version="grafanaVersion",
                name="name",
                network_access_control=grafana_mixins.CfnWorkspacePropsMixin.NetworkAccessControlProperty(
                    prefix_list_ids=["prefixListIds"],
                    vpce_ids=["vpceIds"]
                ),
                notification_destinations=["notificationDestinations"],
                organizational_units=["organizationalUnits"],
                organization_role_name="organizationRoleName",
                permission_type="permissionType",
                plugin_admin_enabled=False,
                role_arn="roleArn",
                saml_configuration=grafana_mixins.CfnWorkspacePropsMixin.SamlConfigurationProperty(
                    allowed_organizations=["allowedOrganizations"],
                    assertion_attributes=grafana_mixins.CfnWorkspacePropsMixin.AssertionAttributesProperty(
                        email="email",
                        groups="groups",
                        login="login",
                        name="name",
                        org="org",
                        role="role"
                    ),
                    idp_metadata=grafana_mixins.CfnWorkspacePropsMixin.IdpMetadataProperty(
                        url="url",
                        xml="xml"
                    ),
                    login_validity_duration=123,
                    role_values=grafana_mixins.CfnWorkspacePropsMixin.RoleValuesProperty(
                        admin=["admin"],
                        editor=["editor"]
                    )
                ),
                stack_set_name="stackSetName",
                vpc_configuration=grafana_mixins.CfnWorkspacePropsMixin.VpcConfigurationProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a705f1191916a2dad2c1533ed75503cd13f7597b90f7d5961adcac45985e0878)
            check_type(argname="argument account_access_type", value=account_access_type, expected_type=type_hints["account_access_type"])
            check_type(argname="argument authentication_providers", value=authentication_providers, expected_type=type_hints["authentication_providers"])
            check_type(argname="argument client_token", value=client_token, expected_type=type_hints["client_token"])
            check_type(argname="argument data_sources", value=data_sources, expected_type=type_hints["data_sources"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument grafana_version", value=grafana_version, expected_type=type_hints["grafana_version"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network_access_control", value=network_access_control, expected_type=type_hints["network_access_control"])
            check_type(argname="argument notification_destinations", value=notification_destinations, expected_type=type_hints["notification_destinations"])
            check_type(argname="argument organizational_units", value=organizational_units, expected_type=type_hints["organizational_units"])
            check_type(argname="argument organization_role_name", value=organization_role_name, expected_type=type_hints["organization_role_name"])
            check_type(argname="argument permission_type", value=permission_type, expected_type=type_hints["permission_type"])
            check_type(argname="argument plugin_admin_enabled", value=plugin_admin_enabled, expected_type=type_hints["plugin_admin_enabled"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument saml_configuration", value=saml_configuration, expected_type=type_hints["saml_configuration"])
            check_type(argname="argument stack_set_name", value=stack_set_name, expected_type=type_hints["stack_set_name"])
            check_type(argname="argument vpc_configuration", value=vpc_configuration, expected_type=type_hints["vpc_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account_access_type is not None:
            self._values["account_access_type"] = account_access_type
        if authentication_providers is not None:
            self._values["authentication_providers"] = authentication_providers
        if client_token is not None:
            self._values["client_token"] = client_token
        if data_sources is not None:
            self._values["data_sources"] = data_sources
        if description is not None:
            self._values["description"] = description
        if grafana_version is not None:
            self._values["grafana_version"] = grafana_version
        if name is not None:
            self._values["name"] = name
        if network_access_control is not None:
            self._values["network_access_control"] = network_access_control
        if notification_destinations is not None:
            self._values["notification_destinations"] = notification_destinations
        if organizational_units is not None:
            self._values["organizational_units"] = organizational_units
        if organization_role_name is not None:
            self._values["organization_role_name"] = organization_role_name
        if permission_type is not None:
            self._values["permission_type"] = permission_type
        if plugin_admin_enabled is not None:
            self._values["plugin_admin_enabled"] = plugin_admin_enabled
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if saml_configuration is not None:
            self._values["saml_configuration"] = saml_configuration
        if stack_set_name is not None:
            self._values["stack_set_name"] = stack_set_name
        if vpc_configuration is not None:
            self._values["vpc_configuration"] = vpc_configuration

    @builtins.property
    def account_access_type(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the workspace can access AWS resources in this AWS account only, or whether it can also access AWS resources in other accounts in the same organization.

        If this is ``ORGANIZATION`` , the ``OrganizationalUnits`` parameter specifies which organizational units the workspace can access.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-accountaccesstype
        '''
        result = self._values.get("account_access_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authentication_providers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies whether this workspace uses SAML 2.0, AWS IAM Identity Center , or both to authenticate users for using the Grafana console within a workspace. For more information, see `User authentication in Amazon Managed Grafana <https://docs.aws.amazon.com/grafana/latest/userguide/authentication-in-AMG.html>`_ .

        *Allowed Values* : ``AWS_SSO | SAML``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-authenticationproviders
        '''
        result = self._values.get("authentication_providers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def client_token(self) -> typing.Optional[builtins.str]:
        '''A unique, case-sensitive, user-provided identifier to ensure the idempotency of the request.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-clienttoken
        '''
        result = self._values.get("client_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_sources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the AWS data sources that have been configured to have IAM roles and permissions created to allow Amazon Managed Grafana to read data from these sources.

        This list is only used when the workspace was created through the AWS console, and the ``permissionType`` is ``SERVICE_MANAGED`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-datasources
        '''
        result = self._values.get("data_sources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The user-defined description of the workspace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def grafana_version(self) -> typing.Optional[builtins.str]:
        '''Specifies the version of Grafana to support in the workspace.

        Defaults to the latest version on create (for example, 9.4), or the current version of the workspace on update.

        Can only be used to upgrade (for example, from 8.4 to 9.4), not downgrade (for example, from 9.4 to 8.4).

        To know what versions are available to upgrade to for a specific workspace, see the `ListVersions <https://docs.aws.amazon.com/grafana/latest/APIReference/API_ListVersions.html>`_ operation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-grafanaversion
        '''
        result = self._values.get("grafana_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the workspace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_access_control(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspacePropsMixin.NetworkAccessControlProperty"]]:
        '''The configuration settings for network access to your workspace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-networkaccesscontrol
        '''
        result = self._values.get("network_access_control")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspacePropsMixin.NetworkAccessControlProperty"]], result)

    @builtins.property
    def notification_destinations(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The AWS notification channels that Amazon Managed Grafana can automatically create IAM roles and permissions for, to allow Amazon Managed Grafana to use these channels.

        *AllowedValues* : ``SNS``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-notificationdestinations
        '''
        result = self._values.get("notification_destinations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def organizational_units(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the organizational units that this workspace is allowed to use data sources from, if this workspace is in an account that is part of an organization.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-organizationalunits
        '''
        result = self._values.get("organizational_units")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def organization_role_name(self) -> typing.Optional[builtins.str]:
        '''The name of the IAM role that is used to access resources through Organizations.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-organizationrolename
        '''
        result = self._values.get("organization_role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permission_type(self) -> typing.Optional[builtins.str]:
        '''If this is ``SERVICE_MANAGED`` , and the workplace was created through the Amazon Managed Grafana console, then Amazon Managed Grafana automatically creates the IAM roles and provisions the permissions that the workspace needs to use AWS data sources and notification channels.

        If this is ``CUSTOMER_MANAGED`` , you must manage those roles and permissions yourself.

        If you are working with a workspace in a member account of an organization and that account is not a delegated administrator account, and you want the workspace to access data sources in other AWS accounts in the organization, this parameter must be set to ``CUSTOMER_MANAGED`` .

        For more information about converting between customer and service managed, see `Managing permissions for data sources and notification channels <https://docs.aws.amazon.com/grafana/latest/userguide/AMG-datasource-and-notification.html>`_ . For more information about the roles and permissions that must be managed for customer managed workspaces, see `Amazon Managed Grafana permissions and policies for AWS data sources and notification channels <https://docs.aws.amazon.com/grafana/latest/userguide/AMG-manage-permissions.html>`_

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-permissiontype
        '''
        result = self._values.get("permission_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def plugin_admin_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Whether plugin administration is enabled in the workspace.

        Setting to ``true`` allows workspace admins to install, uninstall, and update plugins from within the Grafana workspace.
        .. epigraph::

           This option is only valid for workspaces that support Grafana version 9 or newer.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-pluginadminenabled
        '''
        result = self._values.get("plugin_admin_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The IAM role that grants permissions to the AWS resources that the workspace will view data from.

        This role must already exist.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def saml_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspacePropsMixin.SamlConfigurationProperty"]]:
        '''If the workspace uses SAML, use this structure to map SAML assertion attributes to workspace user information and define which groups in the assertion attribute are to have the ``Admin`` and ``Editor`` roles in the workspace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-samlconfiguration
        '''
        result = self._values.get("saml_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspacePropsMixin.SamlConfigurationProperty"]], result)

    @builtins.property
    def stack_set_name(self) -> typing.Optional[builtins.str]:
        '''The name of the AWS CloudFormation stack set that is used to generate IAM roles to be used for this workspace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-stacksetname
        '''
        result = self._values.get("stack_set_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspacePropsMixin.VpcConfigurationProperty"]]:
        '''The configuration settings for an Amazon VPC that contains data sources for your Grafana workspace to connect to.

        .. epigraph::

           Connecting to a private VPC is not yet available in the Asia Pacific (Seoul) Region (ap-northeast-2).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-vpcconfiguration
        '''
        result = self._values.get("vpc_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspacePropsMixin.VpcConfigurationProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWorkspaceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnWorkspacePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_grafana.mixins.CfnWorkspacePropsMixin",
):
    '''Specifies a *workspace* .

    In a workspace, you can create Grafana dashboards and visualizations to analyze your metrics, logs, and traces. You don't have to build, package, or deploy any hardware to run the Grafana server.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html
    :cloudformationResource: AWS::Grafana::Workspace
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_grafana import mixins as grafana_mixins
        
        cfn_workspace_props_mixin = grafana_mixins.CfnWorkspacePropsMixin(grafana_mixins.CfnWorkspaceMixinProps(
            account_access_type="accountAccessType",
            authentication_providers=["authenticationProviders"],
            client_token="clientToken",
            data_sources=["dataSources"],
            description="description",
            grafana_version="grafanaVersion",
            name="name",
            network_access_control=grafana_mixins.CfnWorkspacePropsMixin.NetworkAccessControlProperty(
                prefix_list_ids=["prefixListIds"],
                vpce_ids=["vpceIds"]
            ),
            notification_destinations=["notificationDestinations"],
            organizational_units=["organizationalUnits"],
            organization_role_name="organizationRoleName",
            permission_type="permissionType",
            plugin_admin_enabled=False,
            role_arn="roleArn",
            saml_configuration=grafana_mixins.CfnWorkspacePropsMixin.SamlConfigurationProperty(
                allowed_organizations=["allowedOrganizations"],
                assertion_attributes=grafana_mixins.CfnWorkspacePropsMixin.AssertionAttributesProperty(
                    email="email",
                    groups="groups",
                    login="login",
                    name="name",
                    org="org",
                    role="role"
                ),
                idp_metadata=grafana_mixins.CfnWorkspacePropsMixin.IdpMetadataProperty(
                    url="url",
                    xml="xml"
                ),
                login_validity_duration=123,
                role_values=grafana_mixins.CfnWorkspacePropsMixin.RoleValuesProperty(
                    admin=["admin"],
                    editor=["editor"]
                )
            ),
            stack_set_name="stackSetName",
            vpc_configuration=grafana_mixins.CfnWorkspacePropsMixin.VpcConfigurationProperty(
                security_group_ids=["securityGroupIds"],
                subnet_ids=["subnetIds"]
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnWorkspaceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Grafana::Workspace``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4798eac9a7ea066345f348e3e457a24ecb004c950f66770c8fa6a6bc3be889b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__73b816a6f6880e88c994230b3a17d08e28533a6ebf26288625ede5f740f8f4c5)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70e21f19fd9060b2899a4ed5133b0f32b3c0ed3dcc1a59632d19a01f1b0f635e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnWorkspaceMixinProps:
        return typing.cast(CfnWorkspaceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_grafana.mixins.CfnWorkspacePropsMixin.AssertionAttributesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "email": "email",
            "groups": "groups",
            "login": "login",
            "name": "name",
            "org": "org",
            "role": "role",
        },
    )
    class AssertionAttributesProperty:
        def __init__(
            self,
            *,
            email: typing.Optional[builtins.str] = None,
            groups: typing.Optional[builtins.str] = None,
            login: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            org: typing.Optional[builtins.str] = None,
            role: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure that defines which attributes in the IdP assertion are to be used to define information about the users authenticated by the IdP to use the workspace.

            :param email: The name of the attribute within the SAML assertion to use as the email names for SAML users.
            :param groups: The name of the attribute within the SAML assertion to use as the user full "friendly" names for user groups.
            :param login: The name of the attribute within the SAML assertion to use as the login names for SAML users.
            :param name: The name of the attribute within the SAML assertion to use as the user full "friendly" names for SAML users.
            :param org: The name of the attribute within the SAML assertion to use as the user full "friendly" names for the users' organizations.
            :param role: The name of the attribute within the SAML assertion to use as the user roles.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-assertionattributes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_grafana import mixins as grafana_mixins
                
                assertion_attributes_property = grafana_mixins.CfnWorkspacePropsMixin.AssertionAttributesProperty(
                    email="email",
                    groups="groups",
                    login="login",
                    name="name",
                    org="org",
                    role="role"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7407e3fcfda96090fbc375218fe13b05fd9d24de421bbc828c97264aeaf9dc54)
                check_type(argname="argument email", value=email, expected_type=type_hints["email"])
                check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
                check_type(argname="argument login", value=login, expected_type=type_hints["login"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument org", value=org, expected_type=type_hints["org"])
                check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if email is not None:
                self._values["email"] = email
            if groups is not None:
                self._values["groups"] = groups
            if login is not None:
                self._values["login"] = login
            if name is not None:
                self._values["name"] = name
            if org is not None:
                self._values["org"] = org
            if role is not None:
                self._values["role"] = role

        @builtins.property
        def email(self) -> typing.Optional[builtins.str]:
            '''The name of the attribute within the SAML assertion to use as the email names for SAML users.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-assertionattributes.html#cfn-grafana-workspace-assertionattributes-email
            '''
            result = self._values.get("email")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def groups(self) -> typing.Optional[builtins.str]:
            '''The name of the attribute within the SAML assertion to use as the user full "friendly" names for user groups.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-assertionattributes.html#cfn-grafana-workspace-assertionattributes-groups
            '''
            result = self._values.get("groups")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def login(self) -> typing.Optional[builtins.str]:
            '''The name of the attribute within the SAML assertion to use as the login names for SAML users.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-assertionattributes.html#cfn-grafana-workspace-assertionattributes-login
            '''
            result = self._values.get("login")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the attribute within the SAML assertion to use as the user full "friendly" names for SAML users.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-assertionattributes.html#cfn-grafana-workspace-assertionattributes-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def org(self) -> typing.Optional[builtins.str]:
            '''The name of the attribute within the SAML assertion to use as the user full "friendly" names for the users' organizations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-assertionattributes.html#cfn-grafana-workspace-assertionattributes-org
            '''
            result = self._values.get("org")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role(self) -> typing.Optional[builtins.str]:
            '''The name of the attribute within the SAML assertion to use as the user roles.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-assertionattributes.html#cfn-grafana-workspace-assertionattributes-role
            '''
            result = self._values.get("role")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssertionAttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_grafana.mixins.CfnWorkspacePropsMixin.IdpMetadataProperty",
        jsii_struct_bases=[],
        name_mapping={"url": "url", "xml": "xml"},
    )
    class IdpMetadataProperty:
        def __init__(
            self,
            *,
            url: typing.Optional[builtins.str] = None,
            xml: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure containing the identity provider (IdP) metadata used to integrate the identity provider with this workspace.

            You can specify the metadata either by providing a URL to its location in the ``url`` parameter, or by specifying the full metadata in XML format in the ``xml`` parameter. Specifying both will cause an error.

            :param url: The URL of the location containing the IdP metadata.
            :param xml: The full IdP metadata, in XML format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-idpmetadata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_grafana import mixins as grafana_mixins
                
                idp_metadata_property = grafana_mixins.CfnWorkspacePropsMixin.IdpMetadataProperty(
                    url="url",
                    xml="xml"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b7097fb81dd75a10941613f8888f6bd6681de3f4522ecf449fc1f6d77fc51beb)
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
                check_type(argname="argument xml", value=xml, expected_type=type_hints["xml"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if url is not None:
                self._values["url"] = url
            if xml is not None:
                self._values["xml"] = xml

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            '''The URL of the location containing the IdP metadata.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-idpmetadata.html#cfn-grafana-workspace-idpmetadata-url
            '''
            result = self._values.get("url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def xml(self) -> typing.Optional[builtins.str]:
            '''The full IdP metadata, in XML format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-idpmetadata.html#cfn-grafana-workspace-idpmetadata-xml
            '''
            result = self._values.get("xml")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IdpMetadataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_grafana.mixins.CfnWorkspacePropsMixin.NetworkAccessControlProperty",
        jsii_struct_bases=[],
        name_mapping={"prefix_list_ids": "prefixListIds", "vpce_ids": "vpceIds"},
    )
    class NetworkAccessControlProperty:
        def __init__(
            self,
            *,
            prefix_list_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            vpce_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The configuration settings for in-bound network access to your workspace.

            When this is configured, only listed IP addresses and VPC endpoints will be able to access your workspace. Standard Grafana authentication and authorization are still required.

            Access is granted to a caller that is in either the IP address list or the VPC endpoint list - they do not need to be in both.

            If this is not configured, or is removed, then all IP addresses and VPC endpoints are allowed. Standard Grafana authentication and authorization are still required.
            .. epigraph::

               While both ``prefixListIds`` and ``vpceIds`` are required, you can pass in an empty array of strings for either parameter if you do not want to allow any of that type.

               If both are passed as empty arrays, no traffic is allowed to the workspace, because only *explicitly* allowed connections are accepted.

            :param prefix_list_ids: An array of prefix list IDs. A prefix list is a list of CIDR ranges of IP addresses. The IP addresses specified are allowed to access your workspace. If the list is not included in the configuration (passed an empty array) then no IP addresses are allowed to access the workspace. You create a prefix list using the Amazon VPC console. Prefix list IDs have the format ``pl- *1a2b3c4d*`` . For more information about prefix lists, see `Group CIDR blocks using managed prefix lists <https://docs.aws.amazon.com/vpc/latest/userguide/managed-prefix-lists.html>`_ in the *Amazon Virtual Private Cloud User Guide* .
            :param vpce_ids: An array of Amazon VPC endpoint IDs for the workspace. You can create VPC endpoints to your Amazon Managed Grafana workspace for access from within a VPC. If a ``NetworkAccessConfiguration`` is specified then only VPC endpoints specified here are allowed to access the workspace. If you pass in an empty array of strings, then no VPCs are allowed to access the workspace. VPC endpoint IDs have the format ``vpce- *1a2b3c4d*`` . For more information about creating an interface VPC endpoint, see `Interface VPC endpoints <https://docs.aws.amazon.com/grafana/latest/userguide/VPC-endpoints>`_ in the *Amazon Managed Grafana User Guide* . .. epigraph:: The only VPC endpoints that can be specified here are interface VPC endpoints for Grafana workspaces (using the ``com.amazonaws.[region].grafana-workspace`` service endpoint). Other VPC endpoints are ignored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-networkaccesscontrol.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_grafana import mixins as grafana_mixins
                
                network_access_control_property = grafana_mixins.CfnWorkspacePropsMixin.NetworkAccessControlProperty(
                    prefix_list_ids=["prefixListIds"],
                    vpce_ids=["vpceIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ef8ecfe9f20e10d30097bc683074187453cd1d15f3d424a1cc11302d4fa82718)
                check_type(argname="argument prefix_list_ids", value=prefix_list_ids, expected_type=type_hints["prefix_list_ids"])
                check_type(argname="argument vpce_ids", value=vpce_ids, expected_type=type_hints["vpce_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if prefix_list_ids is not None:
                self._values["prefix_list_ids"] = prefix_list_ids
            if vpce_ids is not None:
                self._values["vpce_ids"] = vpce_ids

        @builtins.property
        def prefix_list_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An array of prefix list IDs.

            A prefix list is a list of CIDR ranges of IP addresses. The IP addresses specified are allowed to access your workspace. If the list is not included in the configuration (passed an empty array) then no IP addresses are allowed to access the workspace. You create a prefix list using the Amazon VPC console.

            Prefix list IDs have the format ``pl- *1a2b3c4d*`` .

            For more information about prefix lists, see `Group CIDR blocks using managed prefix lists <https://docs.aws.amazon.com/vpc/latest/userguide/managed-prefix-lists.html>`_ in the *Amazon Virtual Private Cloud User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-networkaccesscontrol.html#cfn-grafana-workspace-networkaccesscontrol-prefixlistids
            '''
            result = self._values.get("prefix_list_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def vpce_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An array of Amazon VPC endpoint IDs for the workspace.

            You can create VPC endpoints to your Amazon Managed Grafana workspace for access from within a VPC. If a ``NetworkAccessConfiguration`` is specified then only VPC endpoints specified here are allowed to access the workspace. If you pass in an empty array of strings, then no VPCs are allowed to access the workspace.

            VPC endpoint IDs have the format ``vpce- *1a2b3c4d*`` .

            For more information about creating an interface VPC endpoint, see `Interface VPC endpoints <https://docs.aws.amazon.com/grafana/latest/userguide/VPC-endpoints>`_ in the *Amazon Managed Grafana User Guide* .
            .. epigraph::

               The only VPC endpoints that can be specified here are interface VPC endpoints for Grafana workspaces (using the ``com.amazonaws.[region].grafana-workspace`` service endpoint). Other VPC endpoints are ignored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-networkaccesscontrol.html#cfn-grafana-workspace-networkaccesscontrol-vpceids
            '''
            result = self._values.get("vpce_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NetworkAccessControlProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_grafana.mixins.CfnWorkspacePropsMixin.RoleValuesProperty",
        jsii_struct_bases=[],
        name_mapping={"admin": "admin", "editor": "editor"},
    )
    class RoleValuesProperty:
        def __init__(
            self,
            *,
            admin: typing.Optional[typing.Sequence[builtins.str]] = None,
            editor: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''This structure defines which groups defined in the SAML assertion attribute are to be mapped to the Grafana ``Admin`` and ``Editor`` roles in the workspace.

            SAML authenticated users not part of ``Admin`` or ``Editor`` role groups have ``Viewer`` permission over the workspace.

            :param admin: A list of groups from the SAML assertion attribute to grant the Grafana ``Admin`` role to.
            :param editor: A list of groups from the SAML assertion attribute to grant the Grafana ``Editor`` role to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-rolevalues.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_grafana import mixins as grafana_mixins
                
                role_values_property = grafana_mixins.CfnWorkspacePropsMixin.RoleValuesProperty(
                    admin=["admin"],
                    editor=["editor"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bf7d6d57bab6f815bb5811114b99bbdf6dd24b1a90df50172cd44dac4fdabb6b)
                check_type(argname="argument admin", value=admin, expected_type=type_hints["admin"])
                check_type(argname="argument editor", value=editor, expected_type=type_hints["editor"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if admin is not None:
                self._values["admin"] = admin
            if editor is not None:
                self._values["editor"] = editor

        @builtins.property
        def admin(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of groups from the SAML assertion attribute to grant the Grafana ``Admin`` role to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-rolevalues.html#cfn-grafana-workspace-rolevalues-admin
            '''
            result = self._values.get("admin")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def editor(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of groups from the SAML assertion attribute to grant the Grafana ``Editor`` role to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-rolevalues.html#cfn-grafana-workspace-rolevalues-editor
            '''
            result = self._values.get("editor")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RoleValuesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_grafana.mixins.CfnWorkspacePropsMixin.SamlConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allowed_organizations": "allowedOrganizations",
            "assertion_attributes": "assertionAttributes",
            "idp_metadata": "idpMetadata",
            "login_validity_duration": "loginValidityDuration",
            "role_values": "roleValues",
        },
    )
    class SamlConfigurationProperty:
        def __init__(
            self,
            *,
            allowed_organizations: typing.Optional[typing.Sequence[builtins.str]] = None,
            assertion_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkspacePropsMixin.AssertionAttributesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            idp_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkspacePropsMixin.IdpMetadataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            login_validity_duration: typing.Optional[jsii.Number] = None,
            role_values: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkspacePropsMixin.RoleValuesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A structure containing information about how this workspace works with SAML.

            :param allowed_organizations: Lists which organizations defined in the SAML assertion are allowed to use the Amazon Managed Grafana workspace. If this is empty, all organizations in the assertion attribute have access.
            :param assertion_attributes: A structure that defines which attributes in the SAML assertion are to be used to define information about the users authenticated by that IdP to use the workspace.
            :param idp_metadata: A structure containing the identity provider (IdP) metadata used to integrate the identity provider with this workspace.
            :param login_validity_duration: How long a sign-on session by a SAML user is valid, before the user has to sign on again.
            :param role_values: A structure containing arrays that map group names in the SAML assertion to the Grafana ``Admin`` and ``Editor`` roles in the workspace.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-samlconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_grafana import mixins as grafana_mixins
                
                saml_configuration_property = grafana_mixins.CfnWorkspacePropsMixin.SamlConfigurationProperty(
                    allowed_organizations=["allowedOrganizations"],
                    assertion_attributes=grafana_mixins.CfnWorkspacePropsMixin.AssertionAttributesProperty(
                        email="email",
                        groups="groups",
                        login="login",
                        name="name",
                        org="org",
                        role="role"
                    ),
                    idp_metadata=grafana_mixins.CfnWorkspacePropsMixin.IdpMetadataProperty(
                        url="url",
                        xml="xml"
                    ),
                    login_validity_duration=123,
                    role_values=grafana_mixins.CfnWorkspacePropsMixin.RoleValuesProperty(
                        admin=["admin"],
                        editor=["editor"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5f5682539b03636a719de5cbcc090e68c355c586d34671c6e564c652c093cb9b)
                check_type(argname="argument allowed_organizations", value=allowed_organizations, expected_type=type_hints["allowed_organizations"])
                check_type(argname="argument assertion_attributes", value=assertion_attributes, expected_type=type_hints["assertion_attributes"])
                check_type(argname="argument idp_metadata", value=idp_metadata, expected_type=type_hints["idp_metadata"])
                check_type(argname="argument login_validity_duration", value=login_validity_duration, expected_type=type_hints["login_validity_duration"])
                check_type(argname="argument role_values", value=role_values, expected_type=type_hints["role_values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allowed_organizations is not None:
                self._values["allowed_organizations"] = allowed_organizations
            if assertion_attributes is not None:
                self._values["assertion_attributes"] = assertion_attributes
            if idp_metadata is not None:
                self._values["idp_metadata"] = idp_metadata
            if login_validity_duration is not None:
                self._values["login_validity_duration"] = login_validity_duration
            if role_values is not None:
                self._values["role_values"] = role_values

        @builtins.property
        def allowed_organizations(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Lists which organizations defined in the SAML assertion are allowed to use the Amazon Managed Grafana workspace.

            If this is empty, all organizations in the assertion attribute have access.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-samlconfiguration.html#cfn-grafana-workspace-samlconfiguration-allowedorganizations
            '''
            result = self._values.get("allowed_organizations")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def assertion_attributes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspacePropsMixin.AssertionAttributesProperty"]]:
            '''A structure that defines which attributes in the SAML assertion are to be used to define information about the users authenticated by that IdP to use the workspace.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-samlconfiguration.html#cfn-grafana-workspace-samlconfiguration-assertionattributes
            '''
            result = self._values.get("assertion_attributes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspacePropsMixin.AssertionAttributesProperty"]], result)

        @builtins.property
        def idp_metadata(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspacePropsMixin.IdpMetadataProperty"]]:
            '''A structure containing the identity provider (IdP) metadata used to integrate the identity provider with this workspace.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-samlconfiguration.html#cfn-grafana-workspace-samlconfiguration-idpmetadata
            '''
            result = self._values.get("idp_metadata")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspacePropsMixin.IdpMetadataProperty"]], result)

        @builtins.property
        def login_validity_duration(self) -> typing.Optional[jsii.Number]:
            '''How long a sign-on session by a SAML user is valid, before the user has to sign on again.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-samlconfiguration.html#cfn-grafana-workspace-samlconfiguration-loginvalidityduration
            '''
            result = self._values.get("login_validity_duration")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def role_values(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspacePropsMixin.RoleValuesProperty"]]:
            '''A structure containing arrays that map group names in the SAML assertion to the Grafana ``Admin`` and ``Editor`` roles in the workspace.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-samlconfiguration.html#cfn-grafana-workspace-samlconfiguration-rolevalues
            '''
            result = self._values.get("role_values")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspacePropsMixin.RoleValuesProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SamlConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_grafana.mixins.CfnWorkspacePropsMixin.VpcConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
        },
    )
    class VpcConfigurationProperty:
        def __init__(
            self,
            *,
            security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The configuration settings for an Amazon VPC that contains data sources for your Grafana workspace to connect to.

            .. epigraph::

               Provided ``securityGroupIds`` and ``subnetIds`` must be part of the same VPC.

               Connecting to a private VPC is not yet available in the Asia Pacific (Seoul) Region (ap-northeast-2).

            :param security_group_ids: The list of Amazon EC2 security group IDs attached to the Amazon VPC for your Grafana workspace to connect. Duplicates not allowed. *Array Members* : Minimum number of 1 items. Maximum number of 5 items. *Length* : Minimum length of 0. Maximum length of 255.
            :param subnet_ids: The list of Amazon EC2 subnet IDs created in the Amazon VPC for your Grafana workspace to connect. Duplicates not allowed. *Array Members* : Minimum number of 2 items. Maximum number of 6 items. *Length* : Minimum length of 0. Maximum length of 255.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-vpcconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_grafana import mixins as grafana_mixins
                
                vpc_configuration_property = grafana_mixins.CfnWorkspacePropsMixin.VpcConfigurationProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a69e45900e6e37e0036013579f4fe81ab9afada82d3f1b514dd4612f5d2d1e02)
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
                check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnet_ids is not None:
                self._values["subnet_ids"] = subnet_ids

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of Amazon EC2 security group IDs attached to the Amazon VPC for your Grafana workspace to connect.

            Duplicates not allowed.

            *Array Members* : Minimum number of 1 items. Maximum number of 5 items.

            *Length* : Minimum length of 0. Maximum length of 255.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-vpcconfiguration.html#cfn-grafana-workspace-vpcconfiguration-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of Amazon EC2 subnet IDs created in the Amazon VPC for your Grafana workspace to connect.

            Duplicates not allowed.

            *Array Members* : Minimum number of 2 items. Maximum number of 6 items.

            *Length* : Minimum length of 0. Maximum length of 255.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-vpcconfiguration.html#cfn-grafana-workspace-vpcconfiguration-subnetids
            '''
            result = self._values.get("subnet_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnWorkspaceMixinProps",
    "CfnWorkspacePropsMixin",
]

publication.publish()

def _typecheckingstub__a705f1191916a2dad2c1533ed75503cd13f7597b90f7d5961adcac45985e0878(
    *,
    account_access_type: typing.Optional[builtins.str] = None,
    authentication_providers: typing.Optional[typing.Sequence[builtins.str]] = None,
    client_token: typing.Optional[builtins.str] = None,
    data_sources: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    grafana_version: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    network_access_control: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkspacePropsMixin.NetworkAccessControlProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    notification_destinations: typing.Optional[typing.Sequence[builtins.str]] = None,
    organizational_units: typing.Optional[typing.Sequence[builtins.str]] = None,
    organization_role_name: typing.Optional[builtins.str] = None,
    permission_type: typing.Optional[builtins.str] = None,
    plugin_admin_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    role_arn: typing.Optional[builtins.str] = None,
    saml_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkspacePropsMixin.SamlConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    stack_set_name: typing.Optional[builtins.str] = None,
    vpc_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkspacePropsMixin.VpcConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4798eac9a7ea066345f348e3e457a24ecb004c950f66770c8fa6a6bc3be889b(
    props: typing.Union[CfnWorkspaceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73b816a6f6880e88c994230b3a17d08e28533a6ebf26288625ede5f740f8f4c5(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70e21f19fd9060b2899a4ed5133b0f32b3c0ed3dcc1a59632d19a01f1b0f635e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7407e3fcfda96090fbc375218fe13b05fd9d24de421bbc828c97264aeaf9dc54(
    *,
    email: typing.Optional[builtins.str] = None,
    groups: typing.Optional[builtins.str] = None,
    login: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    org: typing.Optional[builtins.str] = None,
    role: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7097fb81dd75a10941613f8888f6bd6681de3f4522ecf449fc1f6d77fc51beb(
    *,
    url: typing.Optional[builtins.str] = None,
    xml: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef8ecfe9f20e10d30097bc683074187453cd1d15f3d424a1cc11302d4fa82718(
    *,
    prefix_list_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpce_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf7d6d57bab6f815bb5811114b99bbdf6dd24b1a90df50172cd44dac4fdabb6b(
    *,
    admin: typing.Optional[typing.Sequence[builtins.str]] = None,
    editor: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f5682539b03636a719de5cbcc090e68c355c586d34671c6e564c652c093cb9b(
    *,
    allowed_organizations: typing.Optional[typing.Sequence[builtins.str]] = None,
    assertion_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkspacePropsMixin.AssertionAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    idp_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkspacePropsMixin.IdpMetadataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    login_validity_duration: typing.Optional[jsii.Number] = None,
    role_values: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkspacePropsMixin.RoleValuesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a69e45900e6e37e0036013579f4fe81ab9afada82d3f1b514dd4612f5d2d1e02(
    *,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
