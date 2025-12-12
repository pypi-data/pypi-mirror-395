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
    jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "connector_label": "connectorLabel",
        "connector_provisioning_config": "connectorProvisioningConfig",
        "connector_provisioning_type": "connectorProvisioningType",
        "description": "description",
    },
)
class CfnConnectorMixinProps:
    def __init__(
        self,
        *,
        connector_label: typing.Optional[builtins.str] = None,
        connector_provisioning_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorPropsMixin.ConnectorProvisioningConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        connector_provisioning_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnConnectorPropsMixin.

        :param connector_label: The label used for registering the connector.
        :param connector_provisioning_config: The configuration required for registering the connector.
        :param connector_provisioning_type: The provisioning type used to register the connector.
        :param description: A description about the connector runtime setting.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connector.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
            
            cfn_connector_mixin_props = appflow_mixins.CfnConnectorMixinProps(
                connector_label="connectorLabel",
                connector_provisioning_config=appflow_mixins.CfnConnectorPropsMixin.ConnectorProvisioningConfigProperty(
                    lambda_=appflow_mixins.CfnConnectorPropsMixin.LambdaConnectorProvisioningConfigProperty(
                        lambda_arn="lambdaArn"
                    )
                ),
                connector_provisioning_type="connectorProvisioningType",
                description="description"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b688737a9dc541ee06befd87c4543a4ed816d85cc98d2d4631ddd99511343f8f)
            check_type(argname="argument connector_label", value=connector_label, expected_type=type_hints["connector_label"])
            check_type(argname="argument connector_provisioning_config", value=connector_provisioning_config, expected_type=type_hints["connector_provisioning_config"])
            check_type(argname="argument connector_provisioning_type", value=connector_provisioning_type, expected_type=type_hints["connector_provisioning_type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connector_label is not None:
            self._values["connector_label"] = connector_label
        if connector_provisioning_config is not None:
            self._values["connector_provisioning_config"] = connector_provisioning_config
        if connector_provisioning_type is not None:
            self._values["connector_provisioning_type"] = connector_provisioning_type
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def connector_label(self) -> typing.Optional[builtins.str]:
        '''The label used for registering the connector.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connector.html#cfn-appflow-connector-connectorlabel
        '''
        result = self._values.get("connector_label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connector_provisioning_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.ConnectorProvisioningConfigProperty"]]:
        '''The configuration required for registering the connector.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connector.html#cfn-appflow-connector-connectorprovisioningconfig
        '''
        result = self._values.get("connector_provisioning_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.ConnectorProvisioningConfigProperty"]], result)

    @builtins.property
    def connector_provisioning_type(self) -> typing.Optional[builtins.str]:
        '''The provisioning type used to register the connector.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connector.html#cfn-appflow-connector-connectorprovisioningtype
        '''
        result = self._values.get("connector_provisioning_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description about the connector runtime setting.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connector.html#cfn-appflow-connector-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConnectorMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorProfileMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "connection_mode": "connectionMode",
        "connector_label": "connectorLabel",
        "connector_profile_config": "connectorProfileConfig",
        "connector_profile_name": "connectorProfileName",
        "connector_type": "connectorType",
        "kms_arn": "kmsArn",
    },
)
class CfnConnectorProfileMixinProps:
    def __init__(
        self,
        *,
        connection_mode: typing.Optional[builtins.str] = None,
        connector_label: typing.Optional[builtins.str] = None,
        connector_profile_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.ConnectorProfileConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        connector_profile_name: typing.Optional[builtins.str] = None,
        connector_type: typing.Optional[builtins.str] = None,
        kms_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnConnectorProfilePropsMixin.

        :param connection_mode: Indicates the connection mode and if it is public or private.
        :param connector_label: The label for the connector profile being created.
        :param connector_profile_config: Defines the connector-specific configuration and credentials.
        :param connector_profile_name: The name of the connector profile. The name is unique for each ``ConnectorProfile`` in the AWS account .
        :param connector_type: The type of connector, such as Salesforce, Amplitude, and so on.
        :param kms_arn: The ARN (Amazon Resource Name) of the Key Management Service (KMS) key you provide for encryption. This is required if you do not want to use the Amazon AppFlow-managed KMS key. If you don't provide anything here, Amazon AppFlow uses the Amazon AppFlow-managed KMS key.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connectorprofile.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
            
            cfn_connector_profile_mixin_props = appflow_mixins.CfnConnectorProfileMixinProps(
                connection_mode="connectionMode",
                connector_label="connectorLabel",
                connector_profile_config=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorProfileConfigProperty(
                    connector_profile_credentials=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorProfileCredentialsProperty(
                        amplitude=appflow_mixins.CfnConnectorProfilePropsMixin.AmplitudeConnectorProfileCredentialsProperty(
                            api_key="apiKey",
                            secret_key="secretKey"
                        ),
                        custom_connector=appflow_mixins.CfnConnectorProfilePropsMixin.CustomConnectorProfileCredentialsProperty(
                            api_key=appflow_mixins.CfnConnectorProfilePropsMixin.ApiKeyCredentialsProperty(
                                api_key="apiKey",
                                api_secret_key="apiSecretKey"
                            ),
                            authentication_type="authenticationType",
                            basic=appflow_mixins.CfnConnectorProfilePropsMixin.BasicAuthCredentialsProperty(
                                password="password",
                                username="username"
                            ),
                            custom=appflow_mixins.CfnConnectorProfilePropsMixin.CustomAuthCredentialsProperty(
                                credentials_map={
                                    "credentials_map_key": "credentialsMap"
                                },
                                custom_authentication_type="customAuthenticationType"
                            ),
                            oauth2=appflow_mixins.CfnConnectorProfilePropsMixin.OAuth2CredentialsProperty(
                                access_token="accessToken",
                                client_id="clientId",
                                client_secret="clientSecret",
                                o_auth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                                    auth_code="authCode",
                                    redirect_uri="redirectUri"
                                ),
                                refresh_token="refreshToken"
                            )
                        ),
                        datadog=appflow_mixins.CfnConnectorProfilePropsMixin.DatadogConnectorProfileCredentialsProperty(
                            api_key="apiKey",
                            application_key="applicationKey"
                        ),
                        dynatrace=appflow_mixins.CfnConnectorProfilePropsMixin.DynatraceConnectorProfileCredentialsProperty(
                            api_token="apiToken"
                        ),
                        google_analytics=appflow_mixins.CfnConnectorProfilePropsMixin.GoogleAnalyticsConnectorProfileCredentialsProperty(
                            access_token="accessToken",
                            client_id="clientId",
                            client_secret="clientSecret",
                            connector_oAuth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                                auth_code="authCode",
                                redirect_uri="redirectUri"
                            ),
                            refresh_token="refreshToken"
                        ),
                        infor_nexus=appflow_mixins.CfnConnectorProfilePropsMixin.InforNexusConnectorProfileCredentialsProperty(
                            access_key_id="accessKeyId",
                            datakey="datakey",
                            secret_access_key="secretAccessKey",
                            user_id="userId"
                        ),
                        marketo=appflow_mixins.CfnConnectorProfilePropsMixin.MarketoConnectorProfileCredentialsProperty(
                            access_token="accessToken",
                            client_id="clientId",
                            client_secret="clientSecret",
                            connector_oAuth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                                auth_code="authCode",
                                redirect_uri="redirectUri"
                            )
                        ),
                        pardot=appflow_mixins.CfnConnectorProfilePropsMixin.PardotConnectorProfileCredentialsProperty(
                            access_token="accessToken",
                            client_credentials_arn="clientCredentialsArn",
                            connector_oAuth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                                auth_code="authCode",
                                redirect_uri="redirectUri"
                            ),
                            refresh_token="refreshToken"
                        ),
                        redshift=appflow_mixins.CfnConnectorProfilePropsMixin.RedshiftConnectorProfileCredentialsProperty(
                            password="password",
                            username="username"
                        ),
                        salesforce=appflow_mixins.CfnConnectorProfilePropsMixin.SalesforceConnectorProfileCredentialsProperty(
                            access_token="accessToken",
                            client_credentials_arn="clientCredentialsArn",
                            connector_oAuth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                                auth_code="authCode",
                                redirect_uri="redirectUri"
                            ),
                            jwt_token="jwtToken",
                            o_auth2_grant_type="oAuth2GrantType",
                            refresh_token="refreshToken"
                        ),
                        sapo_data=appflow_mixins.CfnConnectorProfilePropsMixin.SAPODataConnectorProfileCredentialsProperty(
                            basic_auth_credentials=appflow_mixins.CfnConnectorProfilePropsMixin.BasicAuthCredentialsProperty(
                                password="password",
                                username="username"
                            ),
                            o_auth_credentials=appflow_mixins.CfnConnectorProfilePropsMixin.OAuthCredentialsProperty(
                                access_token="accessToken",
                                client_id="clientId",
                                client_secret="clientSecret",
                                connector_oAuth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                                    auth_code="authCode",
                                    redirect_uri="redirectUri"
                                ),
                                refresh_token="refreshToken"
                            )
                        ),
                        service_now=appflow_mixins.CfnConnectorProfilePropsMixin.ServiceNowConnectorProfileCredentialsProperty(
                            o_auth2_credentials=appflow_mixins.CfnConnectorProfilePropsMixin.OAuth2CredentialsProperty(
                                access_token="accessToken",
                                client_id="clientId",
                                client_secret="clientSecret",
                                o_auth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                                    auth_code="authCode",
                                    redirect_uri="redirectUri"
                                ),
                                refresh_token="refreshToken"
                            ),
                            password="password",
                            username="username"
                        ),
                        singular=appflow_mixins.CfnConnectorProfilePropsMixin.SingularConnectorProfileCredentialsProperty(
                            api_key="apiKey"
                        ),
                        slack=appflow_mixins.CfnConnectorProfilePropsMixin.SlackConnectorProfileCredentialsProperty(
                            access_token="accessToken",
                            client_id="clientId",
                            client_secret="clientSecret",
                            connector_oAuth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                                auth_code="authCode",
                                redirect_uri="redirectUri"
                            )
                        ),
                        snowflake=appflow_mixins.CfnConnectorProfilePropsMixin.SnowflakeConnectorProfileCredentialsProperty(
                            password="password",
                            username="username"
                        ),
                        trendmicro=appflow_mixins.CfnConnectorProfilePropsMixin.TrendmicroConnectorProfileCredentialsProperty(
                            api_secret_key="apiSecretKey"
                        ),
                        veeva=appflow_mixins.CfnConnectorProfilePropsMixin.VeevaConnectorProfileCredentialsProperty(
                            password="password",
                            username="username"
                        ),
                        zendesk=appflow_mixins.CfnConnectorProfilePropsMixin.ZendeskConnectorProfileCredentialsProperty(
                            access_token="accessToken",
                            client_id="clientId",
                            client_secret="clientSecret",
                            connector_oAuth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                                auth_code="authCode",
                                redirect_uri="redirectUri"
                            )
                        )
                    ),
                    connector_profile_properties=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorProfilePropertiesProperty(
                        custom_connector=appflow_mixins.CfnConnectorProfilePropsMixin.CustomConnectorProfilePropertiesProperty(
                            o_auth2_properties=appflow_mixins.CfnConnectorProfilePropsMixin.OAuth2PropertiesProperty(
                                o_auth2_grant_type="oAuth2GrantType",
                                token_url="tokenUrl",
                                token_url_custom_properties={
                                    "token_url_custom_properties_key": "tokenUrlCustomProperties"
                                }
                            ),
                            profile_properties={
                                "profile_properties_key": "profileProperties"
                            }
                        ),
                        datadog=appflow_mixins.CfnConnectorProfilePropsMixin.DatadogConnectorProfilePropertiesProperty(
                            instance_url="instanceUrl"
                        ),
                        dynatrace=appflow_mixins.CfnConnectorProfilePropsMixin.DynatraceConnectorProfilePropertiesProperty(
                            instance_url="instanceUrl"
                        ),
                        infor_nexus=appflow_mixins.CfnConnectorProfilePropsMixin.InforNexusConnectorProfilePropertiesProperty(
                            instance_url="instanceUrl"
                        ),
                        marketo=appflow_mixins.CfnConnectorProfilePropsMixin.MarketoConnectorProfilePropertiesProperty(
                            instance_url="instanceUrl"
                        ),
                        pardot=appflow_mixins.CfnConnectorProfilePropsMixin.PardotConnectorProfilePropertiesProperty(
                            business_unit_id="businessUnitId",
                            instance_url="instanceUrl",
                            is_sandbox_environment=False
                        ),
                        redshift=appflow_mixins.CfnConnectorProfilePropsMixin.RedshiftConnectorProfilePropertiesProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix",
                            cluster_identifier="clusterIdentifier",
                            data_api_role_arn="dataApiRoleArn",
                            database_name="databaseName",
                            database_url="databaseUrl",
                            is_redshift_serverless=False,
                            role_arn="roleArn",
                            workgroup_name="workgroupName"
                        ),
                        salesforce=appflow_mixins.CfnConnectorProfilePropsMixin.SalesforceConnectorProfilePropertiesProperty(
                            instance_url="instanceUrl",
                            is_sandbox_environment=False,
                            use_private_link_for_metadata_and_authorization=False
                        ),
                        sapo_data=appflow_mixins.CfnConnectorProfilePropsMixin.SAPODataConnectorProfilePropertiesProperty(
                            application_host_url="applicationHostUrl",
                            application_service_path="applicationServicePath",
                            client_number="clientNumber",
                            disable_sso=False,
                            logon_language="logonLanguage",
                            o_auth_properties=appflow_mixins.CfnConnectorProfilePropsMixin.OAuthPropertiesProperty(
                                auth_code_url="authCodeUrl",
                                o_auth_scopes=["oAuthScopes"],
                                token_url="tokenUrl"
                            ),
                            port_number=123,
                            private_link_service_name="privateLinkServiceName"
                        ),
                        service_now=appflow_mixins.CfnConnectorProfilePropsMixin.ServiceNowConnectorProfilePropertiesProperty(
                            instance_url="instanceUrl"
                        ),
                        slack=appflow_mixins.CfnConnectorProfilePropsMixin.SlackConnectorProfilePropertiesProperty(
                            instance_url="instanceUrl"
                        ),
                        snowflake=appflow_mixins.CfnConnectorProfilePropsMixin.SnowflakeConnectorProfilePropertiesProperty(
                            account_name="accountName",
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix",
                            private_link_service_name="privateLinkServiceName",
                            region="region",
                            stage="stage",
                            warehouse="warehouse"
                        ),
                        veeva=appflow_mixins.CfnConnectorProfilePropsMixin.VeevaConnectorProfilePropertiesProperty(
                            instance_url="instanceUrl"
                        ),
                        zendesk=appflow_mixins.CfnConnectorProfilePropsMixin.ZendeskConnectorProfilePropertiesProperty(
                            instance_url="instanceUrl"
                        )
                    )
                ),
                connector_profile_name="connectorProfileName",
                connector_type="connectorType",
                kms_arn="kmsArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__616c02b61a44852d825fee625a6ce8b7be3ccb947496187cffd3837faa165fef)
            check_type(argname="argument connection_mode", value=connection_mode, expected_type=type_hints["connection_mode"])
            check_type(argname="argument connector_label", value=connector_label, expected_type=type_hints["connector_label"])
            check_type(argname="argument connector_profile_config", value=connector_profile_config, expected_type=type_hints["connector_profile_config"])
            check_type(argname="argument connector_profile_name", value=connector_profile_name, expected_type=type_hints["connector_profile_name"])
            check_type(argname="argument connector_type", value=connector_type, expected_type=type_hints["connector_type"])
            check_type(argname="argument kms_arn", value=kms_arn, expected_type=type_hints["kms_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connection_mode is not None:
            self._values["connection_mode"] = connection_mode
        if connector_label is not None:
            self._values["connector_label"] = connector_label
        if connector_profile_config is not None:
            self._values["connector_profile_config"] = connector_profile_config
        if connector_profile_name is not None:
            self._values["connector_profile_name"] = connector_profile_name
        if connector_type is not None:
            self._values["connector_type"] = connector_type
        if kms_arn is not None:
            self._values["kms_arn"] = kms_arn

    @builtins.property
    def connection_mode(self) -> typing.Optional[builtins.str]:
        '''Indicates the connection mode and if it is public or private.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connectorprofile.html#cfn-appflow-connectorprofile-connectionmode
        '''
        result = self._values.get("connection_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connector_label(self) -> typing.Optional[builtins.str]:
        '''The label for the connector profile being created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connectorprofile.html#cfn-appflow-connectorprofile-connectorlabel
        '''
        result = self._values.get("connector_label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connector_profile_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.ConnectorProfileConfigProperty"]]:
        '''Defines the connector-specific configuration and credentials.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connectorprofile.html#cfn-appflow-connectorprofile-connectorprofileconfig
        '''
        result = self._values.get("connector_profile_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.ConnectorProfileConfigProperty"]], result)

    @builtins.property
    def connector_profile_name(self) -> typing.Optional[builtins.str]:
        '''The name of the connector profile.

        The name is unique for each ``ConnectorProfile`` in the AWS account .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connectorprofile.html#cfn-appflow-connectorprofile-connectorprofilename
        '''
        result = self._values.get("connector_profile_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connector_type(self) -> typing.Optional[builtins.str]:
        '''The type of connector, such as Salesforce, Amplitude, and so on.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connectorprofile.html#cfn-appflow-connectorprofile-connectortype
        '''
        result = self._values.get("connector_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN (Amazon Resource Name) of the Key Management Service (KMS) key you provide for encryption.

        This is required if you do not want to use the Amazon AppFlow-managed KMS key. If you don't provide anything here, Amazon AppFlow uses the Amazon AppFlow-managed KMS key.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connectorprofile.html#cfn-appflow-connectorprofile-kmsarn
        '''
        result = self._values.get("kms_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConnectorProfileMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnConnectorProfilePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorProfilePropsMixin",
):
    '''The ``AWS::AppFlow::ConnectorProfile`` resource is an Amazon AppFlow resource type that specifies the configuration profile for an instance of a connector.

    This includes the provided name, credentials ARN, connection-mode, and so on. The fields that are common to all types of connector profiles are explicitly specified under the ``Properties`` field. The rest of the connector-specific properties are specified under ``Properties/ConnectorProfileConfig`` .
    .. epigraph::

       If you want to use CloudFormation to create a connector profile for connectors that implement OAuth (such as Salesforce, Slack, Zendesk, and Google Analytics), you must fetch the access and refresh tokens. You can do this by implementing your own UI for OAuth, or by retrieving the tokens from elsewhere. Alternatively, you can use the Amazon AppFlow console to create the connector profile, and then use that connector profile in the flow creation CloudFormation template.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connectorprofile.html
    :cloudformationResource: AWS::AppFlow::ConnectorProfile
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
        
        cfn_connector_profile_props_mixin = appflow_mixins.CfnConnectorProfilePropsMixin(appflow_mixins.CfnConnectorProfileMixinProps(
            connection_mode="connectionMode",
            connector_label="connectorLabel",
            connector_profile_config=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorProfileConfigProperty(
                connector_profile_credentials=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorProfileCredentialsProperty(
                    amplitude=appflow_mixins.CfnConnectorProfilePropsMixin.AmplitudeConnectorProfileCredentialsProperty(
                        api_key="apiKey",
                        secret_key="secretKey"
                    ),
                    custom_connector=appflow_mixins.CfnConnectorProfilePropsMixin.CustomConnectorProfileCredentialsProperty(
                        api_key=appflow_mixins.CfnConnectorProfilePropsMixin.ApiKeyCredentialsProperty(
                            api_key="apiKey",
                            api_secret_key="apiSecretKey"
                        ),
                        authentication_type="authenticationType",
                        basic=appflow_mixins.CfnConnectorProfilePropsMixin.BasicAuthCredentialsProperty(
                            password="password",
                            username="username"
                        ),
                        custom=appflow_mixins.CfnConnectorProfilePropsMixin.CustomAuthCredentialsProperty(
                            credentials_map={
                                "credentials_map_key": "credentialsMap"
                            },
                            custom_authentication_type="customAuthenticationType"
                        ),
                        oauth2=appflow_mixins.CfnConnectorProfilePropsMixin.OAuth2CredentialsProperty(
                            access_token="accessToken",
                            client_id="clientId",
                            client_secret="clientSecret",
                            o_auth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                                auth_code="authCode",
                                redirect_uri="redirectUri"
                            ),
                            refresh_token="refreshToken"
                        )
                    ),
                    datadog=appflow_mixins.CfnConnectorProfilePropsMixin.DatadogConnectorProfileCredentialsProperty(
                        api_key="apiKey",
                        application_key="applicationKey"
                    ),
                    dynatrace=appflow_mixins.CfnConnectorProfilePropsMixin.DynatraceConnectorProfileCredentialsProperty(
                        api_token="apiToken"
                    ),
                    google_analytics=appflow_mixins.CfnConnectorProfilePropsMixin.GoogleAnalyticsConnectorProfileCredentialsProperty(
                        access_token="accessToken",
                        client_id="clientId",
                        client_secret="clientSecret",
                        connector_oAuth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                            auth_code="authCode",
                            redirect_uri="redirectUri"
                        ),
                        refresh_token="refreshToken"
                    ),
                    infor_nexus=appflow_mixins.CfnConnectorProfilePropsMixin.InforNexusConnectorProfileCredentialsProperty(
                        access_key_id="accessKeyId",
                        datakey="datakey",
                        secret_access_key="secretAccessKey",
                        user_id="userId"
                    ),
                    marketo=appflow_mixins.CfnConnectorProfilePropsMixin.MarketoConnectorProfileCredentialsProperty(
                        access_token="accessToken",
                        client_id="clientId",
                        client_secret="clientSecret",
                        connector_oAuth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                            auth_code="authCode",
                            redirect_uri="redirectUri"
                        )
                    ),
                    pardot=appflow_mixins.CfnConnectorProfilePropsMixin.PardotConnectorProfileCredentialsProperty(
                        access_token="accessToken",
                        client_credentials_arn="clientCredentialsArn",
                        connector_oAuth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                            auth_code="authCode",
                            redirect_uri="redirectUri"
                        ),
                        refresh_token="refreshToken"
                    ),
                    redshift=appflow_mixins.CfnConnectorProfilePropsMixin.RedshiftConnectorProfileCredentialsProperty(
                        password="password",
                        username="username"
                    ),
                    salesforce=appflow_mixins.CfnConnectorProfilePropsMixin.SalesforceConnectorProfileCredentialsProperty(
                        access_token="accessToken",
                        client_credentials_arn="clientCredentialsArn",
                        connector_oAuth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                            auth_code="authCode",
                            redirect_uri="redirectUri"
                        ),
                        jwt_token="jwtToken",
                        o_auth2_grant_type="oAuth2GrantType",
                        refresh_token="refreshToken"
                    ),
                    sapo_data=appflow_mixins.CfnConnectorProfilePropsMixin.SAPODataConnectorProfileCredentialsProperty(
                        basic_auth_credentials=appflow_mixins.CfnConnectorProfilePropsMixin.BasicAuthCredentialsProperty(
                            password="password",
                            username="username"
                        ),
                        o_auth_credentials=appflow_mixins.CfnConnectorProfilePropsMixin.OAuthCredentialsProperty(
                            access_token="accessToken",
                            client_id="clientId",
                            client_secret="clientSecret",
                            connector_oAuth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                                auth_code="authCode",
                                redirect_uri="redirectUri"
                            ),
                            refresh_token="refreshToken"
                        )
                    ),
                    service_now=appflow_mixins.CfnConnectorProfilePropsMixin.ServiceNowConnectorProfileCredentialsProperty(
                        o_auth2_credentials=appflow_mixins.CfnConnectorProfilePropsMixin.OAuth2CredentialsProperty(
                            access_token="accessToken",
                            client_id="clientId",
                            client_secret="clientSecret",
                            o_auth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                                auth_code="authCode",
                                redirect_uri="redirectUri"
                            ),
                            refresh_token="refreshToken"
                        ),
                        password="password",
                        username="username"
                    ),
                    singular=appflow_mixins.CfnConnectorProfilePropsMixin.SingularConnectorProfileCredentialsProperty(
                        api_key="apiKey"
                    ),
                    slack=appflow_mixins.CfnConnectorProfilePropsMixin.SlackConnectorProfileCredentialsProperty(
                        access_token="accessToken",
                        client_id="clientId",
                        client_secret="clientSecret",
                        connector_oAuth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                            auth_code="authCode",
                            redirect_uri="redirectUri"
                        )
                    ),
                    snowflake=appflow_mixins.CfnConnectorProfilePropsMixin.SnowflakeConnectorProfileCredentialsProperty(
                        password="password",
                        username="username"
                    ),
                    trendmicro=appflow_mixins.CfnConnectorProfilePropsMixin.TrendmicroConnectorProfileCredentialsProperty(
                        api_secret_key="apiSecretKey"
                    ),
                    veeva=appflow_mixins.CfnConnectorProfilePropsMixin.VeevaConnectorProfileCredentialsProperty(
                        password="password",
                        username="username"
                    ),
                    zendesk=appflow_mixins.CfnConnectorProfilePropsMixin.ZendeskConnectorProfileCredentialsProperty(
                        access_token="accessToken",
                        client_id="clientId",
                        client_secret="clientSecret",
                        connector_oAuth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                            auth_code="authCode",
                            redirect_uri="redirectUri"
                        )
                    )
                ),
                connector_profile_properties=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorProfilePropertiesProperty(
                    custom_connector=appflow_mixins.CfnConnectorProfilePropsMixin.CustomConnectorProfilePropertiesProperty(
                        o_auth2_properties=appflow_mixins.CfnConnectorProfilePropsMixin.OAuth2PropertiesProperty(
                            o_auth2_grant_type="oAuth2GrantType",
                            token_url="tokenUrl",
                            token_url_custom_properties={
                                "token_url_custom_properties_key": "tokenUrlCustomProperties"
                            }
                        ),
                        profile_properties={
                            "profile_properties_key": "profileProperties"
                        }
                    ),
                    datadog=appflow_mixins.CfnConnectorProfilePropsMixin.DatadogConnectorProfilePropertiesProperty(
                        instance_url="instanceUrl"
                    ),
                    dynatrace=appflow_mixins.CfnConnectorProfilePropsMixin.DynatraceConnectorProfilePropertiesProperty(
                        instance_url="instanceUrl"
                    ),
                    infor_nexus=appflow_mixins.CfnConnectorProfilePropsMixin.InforNexusConnectorProfilePropertiesProperty(
                        instance_url="instanceUrl"
                    ),
                    marketo=appflow_mixins.CfnConnectorProfilePropsMixin.MarketoConnectorProfilePropertiesProperty(
                        instance_url="instanceUrl"
                    ),
                    pardot=appflow_mixins.CfnConnectorProfilePropsMixin.PardotConnectorProfilePropertiesProperty(
                        business_unit_id="businessUnitId",
                        instance_url="instanceUrl",
                        is_sandbox_environment=False
                    ),
                    redshift=appflow_mixins.CfnConnectorProfilePropsMixin.RedshiftConnectorProfilePropertiesProperty(
                        bucket_name="bucketName",
                        bucket_prefix="bucketPrefix",
                        cluster_identifier="clusterIdentifier",
                        data_api_role_arn="dataApiRoleArn",
                        database_name="databaseName",
                        database_url="databaseUrl",
                        is_redshift_serverless=False,
                        role_arn="roleArn",
                        workgroup_name="workgroupName"
                    ),
                    salesforce=appflow_mixins.CfnConnectorProfilePropsMixin.SalesforceConnectorProfilePropertiesProperty(
                        instance_url="instanceUrl",
                        is_sandbox_environment=False,
                        use_private_link_for_metadata_and_authorization=False
                    ),
                    sapo_data=appflow_mixins.CfnConnectorProfilePropsMixin.SAPODataConnectorProfilePropertiesProperty(
                        application_host_url="applicationHostUrl",
                        application_service_path="applicationServicePath",
                        client_number="clientNumber",
                        disable_sso=False,
                        logon_language="logonLanguage",
                        o_auth_properties=appflow_mixins.CfnConnectorProfilePropsMixin.OAuthPropertiesProperty(
                            auth_code_url="authCodeUrl",
                            o_auth_scopes=["oAuthScopes"],
                            token_url="tokenUrl"
                        ),
                        port_number=123,
                        private_link_service_name="privateLinkServiceName"
                    ),
                    service_now=appflow_mixins.CfnConnectorProfilePropsMixin.ServiceNowConnectorProfilePropertiesProperty(
                        instance_url="instanceUrl"
                    ),
                    slack=appflow_mixins.CfnConnectorProfilePropsMixin.SlackConnectorProfilePropertiesProperty(
                        instance_url="instanceUrl"
                    ),
                    snowflake=appflow_mixins.CfnConnectorProfilePropsMixin.SnowflakeConnectorProfilePropertiesProperty(
                        account_name="accountName",
                        bucket_name="bucketName",
                        bucket_prefix="bucketPrefix",
                        private_link_service_name="privateLinkServiceName",
                        region="region",
                        stage="stage",
                        warehouse="warehouse"
                    ),
                    veeva=appflow_mixins.CfnConnectorProfilePropsMixin.VeevaConnectorProfilePropertiesProperty(
                        instance_url="instanceUrl"
                    ),
                    zendesk=appflow_mixins.CfnConnectorProfilePropsMixin.ZendeskConnectorProfilePropertiesProperty(
                        instance_url="instanceUrl"
                    )
                )
            ),
            connector_profile_name="connectorProfileName",
            connector_type="connectorType",
            kms_arn="kmsArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnConnectorProfileMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AppFlow::ConnectorProfile``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56ae9522601d40fc2242c76e3c6c580bde26b2382a4fe7e7f5092f8784359d2b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5bcd640fe28e820fa355967fe5d027874aa67fd4e7b40b17f3b273f98db68b6a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6557c6094438c01903da683975baf009d9cab04fd53335bb62dc33b2e0af7434)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnConnectorProfileMixinProps:
        return typing.cast(CfnConnectorProfileMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorProfilePropsMixin.AmplitudeConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={"api_key": "apiKey", "secret_key": "secretKey"},
    )
    class AmplitudeConnectorProfileCredentialsProperty:
        def __init__(
            self,
            *,
            api_key: typing.Optional[builtins.str] = None,
            secret_key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The connector-specific credentials required when using Amplitude.

            :param api_key: A unique alphanumeric identifier used to authenticate a user, developer, or calling program to your API.
            :param secret_key: The Secret Access Key portion of the credentials.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-amplitudeconnectorprofilecredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                amplitude_connector_profile_credentials_property = appflow_mixins.CfnConnectorProfilePropsMixin.AmplitudeConnectorProfileCredentialsProperty(
                    api_key="apiKey",
                    secret_key="secretKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3b75e9c3175d6f1cb737df207dda7b1aebb81dfdf73a5f0a4757d3750285655f)
                check_type(argname="argument api_key", value=api_key, expected_type=type_hints["api_key"])
                check_type(argname="argument secret_key", value=secret_key, expected_type=type_hints["secret_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if api_key is not None:
                self._values["api_key"] = api_key
            if secret_key is not None:
                self._values["secret_key"] = secret_key

        @builtins.property
        def api_key(self) -> typing.Optional[builtins.str]:
            '''A unique alphanumeric identifier used to authenticate a user, developer, or calling program to your API.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-amplitudeconnectorprofilecredentials.html#cfn-appflow-connectorprofile-amplitudeconnectorprofilecredentials-apikey
            '''
            result = self._values.get("api_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secret_key(self) -> typing.Optional[builtins.str]:
            '''The Secret Access Key portion of the credentials.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-amplitudeconnectorprofilecredentials.html#cfn-appflow-connectorprofile-amplitudeconnectorprofilecredentials-secretkey
            '''
            result = self._values.get("secret_key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AmplitudeConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorProfilePropsMixin.ApiKeyCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={"api_key": "apiKey", "api_secret_key": "apiSecretKey"},
    )
    class ApiKeyCredentialsProperty:
        def __init__(
            self,
            *,
            api_key: typing.Optional[builtins.str] = None,
            api_secret_key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The API key credentials required for API key authentication.

            :param api_key: The API key required for API key authentication.
            :param api_secret_key: The API secret key required for API key authentication.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-apikeycredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                api_key_credentials_property = appflow_mixins.CfnConnectorProfilePropsMixin.ApiKeyCredentialsProperty(
                    api_key="apiKey",
                    api_secret_key="apiSecretKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__12c1a3d822ffe619d0f4c80e8044e2f33f46bc2d26db79ba9c90fcd7c8e47264)
                check_type(argname="argument api_key", value=api_key, expected_type=type_hints["api_key"])
                check_type(argname="argument api_secret_key", value=api_secret_key, expected_type=type_hints["api_secret_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if api_key is not None:
                self._values["api_key"] = api_key
            if api_secret_key is not None:
                self._values["api_secret_key"] = api_secret_key

        @builtins.property
        def api_key(self) -> typing.Optional[builtins.str]:
            '''The API key required for API key authentication.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-apikeycredentials.html#cfn-appflow-connectorprofile-apikeycredentials-apikey
            '''
            result = self._values.get("api_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def api_secret_key(self) -> typing.Optional[builtins.str]:
            '''The API secret key required for API key authentication.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-apikeycredentials.html#cfn-appflow-connectorprofile-apikeycredentials-apisecretkey
            '''
            result = self._values.get("api_secret_key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApiKeyCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorProfilePropsMixin.BasicAuthCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={"password": "password", "username": "username"},
    )
    class BasicAuthCredentialsProperty:
        def __init__(
            self,
            *,
            password: typing.Optional[builtins.str] = None,
            username: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The basic auth credentials required for basic authentication.

            :param password: The password to use to connect to a resource.
            :param username: The username to use to connect to a resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-basicauthcredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                basic_auth_credentials_property = appflow_mixins.CfnConnectorProfilePropsMixin.BasicAuthCredentialsProperty(
                    password="password",
                    username="username"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c73d87c88877efc56205917020005d0b3ba3df0e33e6ca3430b923d71fa034c9)
                check_type(argname="argument password", value=password, expected_type=type_hints["password"])
                check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if password is not None:
                self._values["password"] = password
            if username is not None:
                self._values["username"] = username

        @builtins.property
        def password(self) -> typing.Optional[builtins.str]:
            '''The password to use to connect to a resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-basicauthcredentials.html#cfn-appflow-connectorprofile-basicauthcredentials-password
            '''
            result = self._values.get("password")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def username(self) -> typing.Optional[builtins.str]:
            '''The username to use to connect to a resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-basicauthcredentials.html#cfn-appflow-connectorprofile-basicauthcredentials-username
            '''
            result = self._values.get("username")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BasicAuthCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty",
        jsii_struct_bases=[],
        name_mapping={"auth_code": "authCode", "redirect_uri": "redirectUri"},
    )
    class ConnectorOAuthRequestProperty:
        def __init__(
            self,
            *,
            auth_code: typing.Optional[builtins.str] = None,
            redirect_uri: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Used by select connectors for which the OAuth workflow is supported, such as Salesforce, Google Analytics, Marketo, Zendesk, and Slack.

            :param auth_code: The code provided by the connector when it has been authenticated via the connected app.
            :param redirect_uri: The URL to which the authentication server redirects the browser after authorization has been granted.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectoroauthrequest.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                connector_oAuth_request_property = appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                    auth_code="authCode",
                    redirect_uri="redirectUri"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8d98ef7bcb3ffa68249b1c8e23a0c87b751d4b6b4542680c309507a050f17871)
                check_type(argname="argument auth_code", value=auth_code, expected_type=type_hints["auth_code"])
                check_type(argname="argument redirect_uri", value=redirect_uri, expected_type=type_hints["redirect_uri"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auth_code is not None:
                self._values["auth_code"] = auth_code
            if redirect_uri is not None:
                self._values["redirect_uri"] = redirect_uri

        @builtins.property
        def auth_code(self) -> typing.Optional[builtins.str]:
            '''The code provided by the connector when it has been authenticated via the connected app.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectoroauthrequest.html#cfn-appflow-connectorprofile-connectoroauthrequest-authcode
            '''
            result = self._values.get("auth_code")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def redirect_uri(self) -> typing.Optional[builtins.str]:
            '''The URL to which the authentication server redirects the browser after authorization has been granted.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectoroauthrequest.html#cfn-appflow-connectorprofile-connectoroauthrequest-redirecturi
            '''
            result = self._values.get("redirect_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectorOAuthRequestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorProfilePropsMixin.ConnectorProfileConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "connector_profile_credentials": "connectorProfileCredentials",
            "connector_profile_properties": "connectorProfileProperties",
        },
    )
    class ConnectorProfileConfigProperty:
        def __init__(
            self,
            *,
            connector_profile_credentials: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.ConnectorProfileCredentialsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            connector_profile_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.ConnectorProfilePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Defines the connector-specific configuration and credentials for the connector profile.

            :param connector_profile_credentials: The connector-specific credentials required by each connector.
            :param connector_profile_properties: The connector-specific properties of the profile configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                connector_profile_config_property = appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorProfileConfigProperty(
                    connector_profile_credentials=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorProfileCredentialsProperty(
                        amplitude=appflow_mixins.CfnConnectorProfilePropsMixin.AmplitudeConnectorProfileCredentialsProperty(
                            api_key="apiKey",
                            secret_key="secretKey"
                        ),
                        custom_connector=appflow_mixins.CfnConnectorProfilePropsMixin.CustomConnectorProfileCredentialsProperty(
                            api_key=appflow_mixins.CfnConnectorProfilePropsMixin.ApiKeyCredentialsProperty(
                                api_key="apiKey",
                                api_secret_key="apiSecretKey"
                            ),
                            authentication_type="authenticationType",
                            basic=appflow_mixins.CfnConnectorProfilePropsMixin.BasicAuthCredentialsProperty(
                                password="password",
                                username="username"
                            ),
                            custom=appflow_mixins.CfnConnectorProfilePropsMixin.CustomAuthCredentialsProperty(
                                credentials_map={
                                    "credentials_map_key": "credentialsMap"
                                },
                                custom_authentication_type="customAuthenticationType"
                            ),
                            oauth2=appflow_mixins.CfnConnectorProfilePropsMixin.OAuth2CredentialsProperty(
                                access_token="accessToken",
                                client_id="clientId",
                                client_secret="clientSecret",
                                o_auth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                                    auth_code="authCode",
                                    redirect_uri="redirectUri"
                                ),
                                refresh_token="refreshToken"
                            )
                        ),
                        datadog=appflow_mixins.CfnConnectorProfilePropsMixin.DatadogConnectorProfileCredentialsProperty(
                            api_key="apiKey",
                            application_key="applicationKey"
                        ),
                        dynatrace=appflow_mixins.CfnConnectorProfilePropsMixin.DynatraceConnectorProfileCredentialsProperty(
                            api_token="apiToken"
                        ),
                        google_analytics=appflow_mixins.CfnConnectorProfilePropsMixin.GoogleAnalyticsConnectorProfileCredentialsProperty(
                            access_token="accessToken",
                            client_id="clientId",
                            client_secret="clientSecret",
                            connector_oAuth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                                auth_code="authCode",
                                redirect_uri="redirectUri"
                            ),
                            refresh_token="refreshToken"
                        ),
                        infor_nexus=appflow_mixins.CfnConnectorProfilePropsMixin.InforNexusConnectorProfileCredentialsProperty(
                            access_key_id="accessKeyId",
                            datakey="datakey",
                            secret_access_key="secretAccessKey",
                            user_id="userId"
                        ),
                        marketo=appflow_mixins.CfnConnectorProfilePropsMixin.MarketoConnectorProfileCredentialsProperty(
                            access_token="accessToken",
                            client_id="clientId",
                            client_secret="clientSecret",
                            connector_oAuth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                                auth_code="authCode",
                                redirect_uri="redirectUri"
                            )
                        ),
                        pardot=appflow_mixins.CfnConnectorProfilePropsMixin.PardotConnectorProfileCredentialsProperty(
                            access_token="accessToken",
                            client_credentials_arn="clientCredentialsArn",
                            connector_oAuth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                                auth_code="authCode",
                                redirect_uri="redirectUri"
                            ),
                            refresh_token="refreshToken"
                        ),
                        redshift=appflow_mixins.CfnConnectorProfilePropsMixin.RedshiftConnectorProfileCredentialsProperty(
                            password="password",
                            username="username"
                        ),
                        salesforce=appflow_mixins.CfnConnectorProfilePropsMixin.SalesforceConnectorProfileCredentialsProperty(
                            access_token="accessToken",
                            client_credentials_arn="clientCredentialsArn",
                            connector_oAuth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                                auth_code="authCode",
                                redirect_uri="redirectUri"
                            ),
                            jwt_token="jwtToken",
                            o_auth2_grant_type="oAuth2GrantType",
                            refresh_token="refreshToken"
                        ),
                        sapo_data=appflow_mixins.CfnConnectorProfilePropsMixin.SAPODataConnectorProfileCredentialsProperty(
                            basic_auth_credentials=appflow_mixins.CfnConnectorProfilePropsMixin.BasicAuthCredentialsProperty(
                                password="password",
                                username="username"
                            ),
                            o_auth_credentials=appflow_mixins.CfnConnectorProfilePropsMixin.OAuthCredentialsProperty(
                                access_token="accessToken",
                                client_id="clientId",
                                client_secret="clientSecret",
                                connector_oAuth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                                    auth_code="authCode",
                                    redirect_uri="redirectUri"
                                ),
                                refresh_token="refreshToken"
                            )
                        ),
                        service_now=appflow_mixins.CfnConnectorProfilePropsMixin.ServiceNowConnectorProfileCredentialsProperty(
                            o_auth2_credentials=appflow_mixins.CfnConnectorProfilePropsMixin.OAuth2CredentialsProperty(
                                access_token="accessToken",
                                client_id="clientId",
                                client_secret="clientSecret",
                                o_auth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                                    auth_code="authCode",
                                    redirect_uri="redirectUri"
                                ),
                                refresh_token="refreshToken"
                            ),
                            password="password",
                            username="username"
                        ),
                        singular=appflow_mixins.CfnConnectorProfilePropsMixin.SingularConnectorProfileCredentialsProperty(
                            api_key="apiKey"
                        ),
                        slack=appflow_mixins.CfnConnectorProfilePropsMixin.SlackConnectorProfileCredentialsProperty(
                            access_token="accessToken",
                            client_id="clientId",
                            client_secret="clientSecret",
                            connector_oAuth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                                auth_code="authCode",
                                redirect_uri="redirectUri"
                            )
                        ),
                        snowflake=appflow_mixins.CfnConnectorProfilePropsMixin.SnowflakeConnectorProfileCredentialsProperty(
                            password="password",
                            username="username"
                        ),
                        trendmicro=appflow_mixins.CfnConnectorProfilePropsMixin.TrendmicroConnectorProfileCredentialsProperty(
                            api_secret_key="apiSecretKey"
                        ),
                        veeva=appflow_mixins.CfnConnectorProfilePropsMixin.VeevaConnectorProfileCredentialsProperty(
                            password="password",
                            username="username"
                        ),
                        zendesk=appflow_mixins.CfnConnectorProfilePropsMixin.ZendeskConnectorProfileCredentialsProperty(
                            access_token="accessToken",
                            client_id="clientId",
                            client_secret="clientSecret",
                            connector_oAuth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                                auth_code="authCode",
                                redirect_uri="redirectUri"
                            )
                        )
                    ),
                    connector_profile_properties=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorProfilePropertiesProperty(
                        custom_connector=appflow_mixins.CfnConnectorProfilePropsMixin.CustomConnectorProfilePropertiesProperty(
                            o_auth2_properties=appflow_mixins.CfnConnectorProfilePropsMixin.OAuth2PropertiesProperty(
                                o_auth2_grant_type="oAuth2GrantType",
                                token_url="tokenUrl",
                                token_url_custom_properties={
                                    "token_url_custom_properties_key": "tokenUrlCustomProperties"
                                }
                            ),
                            profile_properties={
                                "profile_properties_key": "profileProperties"
                            }
                        ),
                        datadog=appflow_mixins.CfnConnectorProfilePropsMixin.DatadogConnectorProfilePropertiesProperty(
                            instance_url="instanceUrl"
                        ),
                        dynatrace=appflow_mixins.CfnConnectorProfilePropsMixin.DynatraceConnectorProfilePropertiesProperty(
                            instance_url="instanceUrl"
                        ),
                        infor_nexus=appflow_mixins.CfnConnectorProfilePropsMixin.InforNexusConnectorProfilePropertiesProperty(
                            instance_url="instanceUrl"
                        ),
                        marketo=appflow_mixins.CfnConnectorProfilePropsMixin.MarketoConnectorProfilePropertiesProperty(
                            instance_url="instanceUrl"
                        ),
                        pardot=appflow_mixins.CfnConnectorProfilePropsMixin.PardotConnectorProfilePropertiesProperty(
                            business_unit_id="businessUnitId",
                            instance_url="instanceUrl",
                            is_sandbox_environment=False
                        ),
                        redshift=appflow_mixins.CfnConnectorProfilePropsMixin.RedshiftConnectorProfilePropertiesProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix",
                            cluster_identifier="clusterIdentifier",
                            data_api_role_arn="dataApiRoleArn",
                            database_name="databaseName",
                            database_url="databaseUrl",
                            is_redshift_serverless=False,
                            role_arn="roleArn",
                            workgroup_name="workgroupName"
                        ),
                        salesforce=appflow_mixins.CfnConnectorProfilePropsMixin.SalesforceConnectorProfilePropertiesProperty(
                            instance_url="instanceUrl",
                            is_sandbox_environment=False,
                            use_private_link_for_metadata_and_authorization=False
                        ),
                        sapo_data=appflow_mixins.CfnConnectorProfilePropsMixin.SAPODataConnectorProfilePropertiesProperty(
                            application_host_url="applicationHostUrl",
                            application_service_path="applicationServicePath",
                            client_number="clientNumber",
                            disable_sso=False,
                            logon_language="logonLanguage",
                            o_auth_properties=appflow_mixins.CfnConnectorProfilePropsMixin.OAuthPropertiesProperty(
                                auth_code_url="authCodeUrl",
                                o_auth_scopes=["oAuthScopes"],
                                token_url="tokenUrl"
                            ),
                            port_number=123,
                            private_link_service_name="privateLinkServiceName"
                        ),
                        service_now=appflow_mixins.CfnConnectorProfilePropsMixin.ServiceNowConnectorProfilePropertiesProperty(
                            instance_url="instanceUrl"
                        ),
                        slack=appflow_mixins.CfnConnectorProfilePropsMixin.SlackConnectorProfilePropertiesProperty(
                            instance_url="instanceUrl"
                        ),
                        snowflake=appflow_mixins.CfnConnectorProfilePropsMixin.SnowflakeConnectorProfilePropertiesProperty(
                            account_name="accountName",
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix",
                            private_link_service_name="privateLinkServiceName",
                            region="region",
                            stage="stage",
                            warehouse="warehouse"
                        ),
                        veeva=appflow_mixins.CfnConnectorProfilePropsMixin.VeevaConnectorProfilePropertiesProperty(
                            instance_url="instanceUrl"
                        ),
                        zendesk=appflow_mixins.CfnConnectorProfilePropsMixin.ZendeskConnectorProfilePropertiesProperty(
                            instance_url="instanceUrl"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1658835a6d8641ac55e57fff2b1fa1cb665f39019a1eab06d8f6bf580436f133)
                check_type(argname="argument connector_profile_credentials", value=connector_profile_credentials, expected_type=type_hints["connector_profile_credentials"])
                check_type(argname="argument connector_profile_properties", value=connector_profile_properties, expected_type=type_hints["connector_profile_properties"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if connector_profile_credentials is not None:
                self._values["connector_profile_credentials"] = connector_profile_credentials
            if connector_profile_properties is not None:
                self._values["connector_profile_properties"] = connector_profile_properties

        @builtins.property
        def connector_profile_credentials(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.ConnectorProfileCredentialsProperty"]]:
            '''The connector-specific credentials required by each connector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileconfig.html#cfn-appflow-connectorprofile-connectorprofileconfig-connectorprofilecredentials
            '''
            result = self._values.get("connector_profile_credentials")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.ConnectorProfileCredentialsProperty"]], result)

        @builtins.property
        def connector_profile_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.ConnectorProfilePropertiesProperty"]]:
            '''The connector-specific properties of the profile configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileconfig.html#cfn-appflow-connectorprofile-connectorprofileconfig-connectorprofileproperties
            '''
            result = self._values.get("connector_profile_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.ConnectorProfilePropertiesProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectorProfileConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorProfilePropsMixin.ConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "amplitude": "amplitude",
            "custom_connector": "customConnector",
            "datadog": "datadog",
            "dynatrace": "dynatrace",
            "google_analytics": "googleAnalytics",
            "infor_nexus": "inforNexus",
            "marketo": "marketo",
            "pardot": "pardot",
            "redshift": "redshift",
            "salesforce": "salesforce",
            "sapo_data": "sapoData",
            "service_now": "serviceNow",
            "singular": "singular",
            "slack": "slack",
            "snowflake": "snowflake",
            "trendmicro": "trendmicro",
            "veeva": "veeva",
            "zendesk": "zendesk",
        },
    )
    class ConnectorProfileCredentialsProperty:
        def __init__(
            self,
            *,
            amplitude: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.AmplitudeConnectorProfileCredentialsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            custom_connector: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.CustomConnectorProfileCredentialsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            datadog: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.DatadogConnectorProfileCredentialsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            dynatrace: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.DynatraceConnectorProfileCredentialsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            google_analytics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.GoogleAnalyticsConnectorProfileCredentialsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            infor_nexus: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.InforNexusConnectorProfileCredentialsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            marketo: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.MarketoConnectorProfileCredentialsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            pardot: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.PardotConnectorProfileCredentialsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            redshift: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.RedshiftConnectorProfileCredentialsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            salesforce: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.SalesforceConnectorProfileCredentialsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sapo_data: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.SAPODataConnectorProfileCredentialsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            service_now: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.ServiceNowConnectorProfileCredentialsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            singular: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.SingularConnectorProfileCredentialsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            slack: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.SlackConnectorProfileCredentialsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            snowflake: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.SnowflakeConnectorProfileCredentialsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            trendmicro: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.TrendmicroConnectorProfileCredentialsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            veeva: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.VeevaConnectorProfileCredentialsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            zendesk: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.ZendeskConnectorProfileCredentialsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The connector-specific credentials required by a connector.

            :param amplitude: The connector-specific credentials required when using Amplitude.
            :param custom_connector: The connector-specific profile credentials that are required when using the custom connector.
            :param datadog: The connector-specific credentials required when using Datadog.
            :param dynatrace: The connector-specific credentials required when using Dynatrace.
            :param google_analytics: The connector-specific credentials required when using Google Analytics.
            :param infor_nexus: The connector-specific credentials required when using Infor Nexus.
            :param marketo: The connector-specific credentials required when using Marketo.
            :param pardot: The connector-specific credentials required when using Salesforce Pardot.
            :param redshift: The connector-specific credentials required when using Amazon Redshift.
            :param salesforce: The connector-specific credentials required when using Salesforce.
            :param sapo_data: The connector-specific profile credentials required when using SAPOData.
            :param service_now: The connector-specific credentials required when using ServiceNow.
            :param singular: The connector-specific credentials required when using Singular.
            :param slack: The connector-specific credentials required when using Slack.
            :param snowflake: The connector-specific credentials required when using Snowflake.
            :param trendmicro: The connector-specific credentials required when using Trend Micro.
            :param veeva: The connector-specific credentials required when using Veeva.
            :param zendesk: The connector-specific credentials required when using Zendesk.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                connector_profile_credentials_property = appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorProfileCredentialsProperty(
                    amplitude=appflow_mixins.CfnConnectorProfilePropsMixin.AmplitudeConnectorProfileCredentialsProperty(
                        api_key="apiKey",
                        secret_key="secretKey"
                    ),
                    custom_connector=appflow_mixins.CfnConnectorProfilePropsMixin.CustomConnectorProfileCredentialsProperty(
                        api_key=appflow_mixins.CfnConnectorProfilePropsMixin.ApiKeyCredentialsProperty(
                            api_key="apiKey",
                            api_secret_key="apiSecretKey"
                        ),
                        authentication_type="authenticationType",
                        basic=appflow_mixins.CfnConnectorProfilePropsMixin.BasicAuthCredentialsProperty(
                            password="password",
                            username="username"
                        ),
                        custom=appflow_mixins.CfnConnectorProfilePropsMixin.CustomAuthCredentialsProperty(
                            credentials_map={
                                "credentials_map_key": "credentialsMap"
                            },
                            custom_authentication_type="customAuthenticationType"
                        ),
                        oauth2=appflow_mixins.CfnConnectorProfilePropsMixin.OAuth2CredentialsProperty(
                            access_token="accessToken",
                            client_id="clientId",
                            client_secret="clientSecret",
                            o_auth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                                auth_code="authCode",
                                redirect_uri="redirectUri"
                            ),
                            refresh_token="refreshToken"
                        )
                    ),
                    datadog=appflow_mixins.CfnConnectorProfilePropsMixin.DatadogConnectorProfileCredentialsProperty(
                        api_key="apiKey",
                        application_key="applicationKey"
                    ),
                    dynatrace=appflow_mixins.CfnConnectorProfilePropsMixin.DynatraceConnectorProfileCredentialsProperty(
                        api_token="apiToken"
                    ),
                    google_analytics=appflow_mixins.CfnConnectorProfilePropsMixin.GoogleAnalyticsConnectorProfileCredentialsProperty(
                        access_token="accessToken",
                        client_id="clientId",
                        client_secret="clientSecret",
                        connector_oAuth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                            auth_code="authCode",
                            redirect_uri="redirectUri"
                        ),
                        refresh_token="refreshToken"
                    ),
                    infor_nexus=appflow_mixins.CfnConnectorProfilePropsMixin.InforNexusConnectorProfileCredentialsProperty(
                        access_key_id="accessKeyId",
                        datakey="datakey",
                        secret_access_key="secretAccessKey",
                        user_id="userId"
                    ),
                    marketo=appflow_mixins.CfnConnectorProfilePropsMixin.MarketoConnectorProfileCredentialsProperty(
                        access_token="accessToken",
                        client_id="clientId",
                        client_secret="clientSecret",
                        connector_oAuth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                            auth_code="authCode",
                            redirect_uri="redirectUri"
                        )
                    ),
                    pardot=appflow_mixins.CfnConnectorProfilePropsMixin.PardotConnectorProfileCredentialsProperty(
                        access_token="accessToken",
                        client_credentials_arn="clientCredentialsArn",
                        connector_oAuth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                            auth_code="authCode",
                            redirect_uri="redirectUri"
                        ),
                        refresh_token="refreshToken"
                    ),
                    redshift=appflow_mixins.CfnConnectorProfilePropsMixin.RedshiftConnectorProfileCredentialsProperty(
                        password="password",
                        username="username"
                    ),
                    salesforce=appflow_mixins.CfnConnectorProfilePropsMixin.SalesforceConnectorProfileCredentialsProperty(
                        access_token="accessToken",
                        client_credentials_arn="clientCredentialsArn",
                        connector_oAuth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                            auth_code="authCode",
                            redirect_uri="redirectUri"
                        ),
                        jwt_token="jwtToken",
                        o_auth2_grant_type="oAuth2GrantType",
                        refresh_token="refreshToken"
                    ),
                    sapo_data=appflow_mixins.CfnConnectorProfilePropsMixin.SAPODataConnectorProfileCredentialsProperty(
                        basic_auth_credentials=appflow_mixins.CfnConnectorProfilePropsMixin.BasicAuthCredentialsProperty(
                            password="password",
                            username="username"
                        ),
                        o_auth_credentials=appflow_mixins.CfnConnectorProfilePropsMixin.OAuthCredentialsProperty(
                            access_token="accessToken",
                            client_id="clientId",
                            client_secret="clientSecret",
                            connector_oAuth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                                auth_code="authCode",
                                redirect_uri="redirectUri"
                            ),
                            refresh_token="refreshToken"
                        )
                    ),
                    service_now=appflow_mixins.CfnConnectorProfilePropsMixin.ServiceNowConnectorProfileCredentialsProperty(
                        o_auth2_credentials=appflow_mixins.CfnConnectorProfilePropsMixin.OAuth2CredentialsProperty(
                            access_token="accessToken",
                            client_id="clientId",
                            client_secret="clientSecret",
                            o_auth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                                auth_code="authCode",
                                redirect_uri="redirectUri"
                            ),
                            refresh_token="refreshToken"
                        ),
                        password="password",
                        username="username"
                    ),
                    singular=appflow_mixins.CfnConnectorProfilePropsMixin.SingularConnectorProfileCredentialsProperty(
                        api_key="apiKey"
                    ),
                    slack=appflow_mixins.CfnConnectorProfilePropsMixin.SlackConnectorProfileCredentialsProperty(
                        access_token="accessToken",
                        client_id="clientId",
                        client_secret="clientSecret",
                        connector_oAuth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                            auth_code="authCode",
                            redirect_uri="redirectUri"
                        )
                    ),
                    snowflake=appflow_mixins.CfnConnectorProfilePropsMixin.SnowflakeConnectorProfileCredentialsProperty(
                        password="password",
                        username="username"
                    ),
                    trendmicro=appflow_mixins.CfnConnectorProfilePropsMixin.TrendmicroConnectorProfileCredentialsProperty(
                        api_secret_key="apiSecretKey"
                    ),
                    veeva=appflow_mixins.CfnConnectorProfilePropsMixin.VeevaConnectorProfileCredentialsProperty(
                        password="password",
                        username="username"
                    ),
                    zendesk=appflow_mixins.CfnConnectorProfilePropsMixin.ZendeskConnectorProfileCredentialsProperty(
                        access_token="accessToken",
                        client_id="clientId",
                        client_secret="clientSecret",
                        connector_oAuth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                            auth_code="authCode",
                            redirect_uri="redirectUri"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c26030621b6284cac5ddf7e4ed54997b7c2aa055ea2ef910346c1578190bdc31)
                check_type(argname="argument amplitude", value=amplitude, expected_type=type_hints["amplitude"])
                check_type(argname="argument custom_connector", value=custom_connector, expected_type=type_hints["custom_connector"])
                check_type(argname="argument datadog", value=datadog, expected_type=type_hints["datadog"])
                check_type(argname="argument dynatrace", value=dynatrace, expected_type=type_hints["dynatrace"])
                check_type(argname="argument google_analytics", value=google_analytics, expected_type=type_hints["google_analytics"])
                check_type(argname="argument infor_nexus", value=infor_nexus, expected_type=type_hints["infor_nexus"])
                check_type(argname="argument marketo", value=marketo, expected_type=type_hints["marketo"])
                check_type(argname="argument pardot", value=pardot, expected_type=type_hints["pardot"])
                check_type(argname="argument redshift", value=redshift, expected_type=type_hints["redshift"])
                check_type(argname="argument salesforce", value=salesforce, expected_type=type_hints["salesforce"])
                check_type(argname="argument sapo_data", value=sapo_data, expected_type=type_hints["sapo_data"])
                check_type(argname="argument service_now", value=service_now, expected_type=type_hints["service_now"])
                check_type(argname="argument singular", value=singular, expected_type=type_hints["singular"])
                check_type(argname="argument slack", value=slack, expected_type=type_hints["slack"])
                check_type(argname="argument snowflake", value=snowflake, expected_type=type_hints["snowflake"])
                check_type(argname="argument trendmicro", value=trendmicro, expected_type=type_hints["trendmicro"])
                check_type(argname="argument veeva", value=veeva, expected_type=type_hints["veeva"])
                check_type(argname="argument zendesk", value=zendesk, expected_type=type_hints["zendesk"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if amplitude is not None:
                self._values["amplitude"] = amplitude
            if custom_connector is not None:
                self._values["custom_connector"] = custom_connector
            if datadog is not None:
                self._values["datadog"] = datadog
            if dynatrace is not None:
                self._values["dynatrace"] = dynatrace
            if google_analytics is not None:
                self._values["google_analytics"] = google_analytics
            if infor_nexus is not None:
                self._values["infor_nexus"] = infor_nexus
            if marketo is not None:
                self._values["marketo"] = marketo
            if pardot is not None:
                self._values["pardot"] = pardot
            if redshift is not None:
                self._values["redshift"] = redshift
            if salesforce is not None:
                self._values["salesforce"] = salesforce
            if sapo_data is not None:
                self._values["sapo_data"] = sapo_data
            if service_now is not None:
                self._values["service_now"] = service_now
            if singular is not None:
                self._values["singular"] = singular
            if slack is not None:
                self._values["slack"] = slack
            if snowflake is not None:
                self._values["snowflake"] = snowflake
            if trendmicro is not None:
                self._values["trendmicro"] = trendmicro
            if veeva is not None:
                self._values["veeva"] = veeva
            if zendesk is not None:
                self._values["zendesk"] = zendesk

        @builtins.property
        def amplitude(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.AmplitudeConnectorProfileCredentialsProperty"]]:
            '''The connector-specific credentials required when using Amplitude.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-amplitude
            '''
            result = self._values.get("amplitude")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.AmplitudeConnectorProfileCredentialsProperty"]], result)

        @builtins.property
        def custom_connector(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.CustomConnectorProfileCredentialsProperty"]]:
            '''The connector-specific profile credentials that are required when using the custom connector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-customconnector
            '''
            result = self._values.get("custom_connector")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.CustomConnectorProfileCredentialsProperty"]], result)

        @builtins.property
        def datadog(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.DatadogConnectorProfileCredentialsProperty"]]:
            '''The connector-specific credentials required when using Datadog.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-datadog
            '''
            result = self._values.get("datadog")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.DatadogConnectorProfileCredentialsProperty"]], result)

        @builtins.property
        def dynatrace(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.DynatraceConnectorProfileCredentialsProperty"]]:
            '''The connector-specific credentials required when using Dynatrace.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-dynatrace
            '''
            result = self._values.get("dynatrace")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.DynatraceConnectorProfileCredentialsProperty"]], result)

        @builtins.property
        def google_analytics(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.GoogleAnalyticsConnectorProfileCredentialsProperty"]]:
            '''The connector-specific credentials required when using Google Analytics.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-googleanalytics
            '''
            result = self._values.get("google_analytics")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.GoogleAnalyticsConnectorProfileCredentialsProperty"]], result)

        @builtins.property
        def infor_nexus(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.InforNexusConnectorProfileCredentialsProperty"]]:
            '''The connector-specific credentials required when using Infor Nexus.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-infornexus
            '''
            result = self._values.get("infor_nexus")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.InforNexusConnectorProfileCredentialsProperty"]], result)

        @builtins.property
        def marketo(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.MarketoConnectorProfileCredentialsProperty"]]:
            '''The connector-specific credentials required when using Marketo.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-marketo
            '''
            result = self._values.get("marketo")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.MarketoConnectorProfileCredentialsProperty"]], result)

        @builtins.property
        def pardot(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.PardotConnectorProfileCredentialsProperty"]]:
            '''The connector-specific credentials required when using Salesforce Pardot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-pardot
            '''
            result = self._values.get("pardot")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.PardotConnectorProfileCredentialsProperty"]], result)

        @builtins.property
        def redshift(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.RedshiftConnectorProfileCredentialsProperty"]]:
            '''The connector-specific credentials required when using Amazon Redshift.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-redshift
            '''
            result = self._values.get("redshift")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.RedshiftConnectorProfileCredentialsProperty"]], result)

        @builtins.property
        def salesforce(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.SalesforceConnectorProfileCredentialsProperty"]]:
            '''The connector-specific credentials required when using Salesforce.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-salesforce
            '''
            result = self._values.get("salesforce")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.SalesforceConnectorProfileCredentialsProperty"]], result)

        @builtins.property
        def sapo_data(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.SAPODataConnectorProfileCredentialsProperty"]]:
            '''The connector-specific profile credentials required when using SAPOData.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-sapodata
            '''
            result = self._values.get("sapo_data")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.SAPODataConnectorProfileCredentialsProperty"]], result)

        @builtins.property
        def service_now(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.ServiceNowConnectorProfileCredentialsProperty"]]:
            '''The connector-specific credentials required when using ServiceNow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-servicenow
            '''
            result = self._values.get("service_now")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.ServiceNowConnectorProfileCredentialsProperty"]], result)

        @builtins.property
        def singular(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.SingularConnectorProfileCredentialsProperty"]]:
            '''The connector-specific credentials required when using Singular.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-singular
            '''
            result = self._values.get("singular")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.SingularConnectorProfileCredentialsProperty"]], result)

        @builtins.property
        def slack(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.SlackConnectorProfileCredentialsProperty"]]:
            '''The connector-specific credentials required when using Slack.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-slack
            '''
            result = self._values.get("slack")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.SlackConnectorProfileCredentialsProperty"]], result)

        @builtins.property
        def snowflake(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.SnowflakeConnectorProfileCredentialsProperty"]]:
            '''The connector-specific credentials required when using Snowflake.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-snowflake
            '''
            result = self._values.get("snowflake")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.SnowflakeConnectorProfileCredentialsProperty"]], result)

        @builtins.property
        def trendmicro(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.TrendmicroConnectorProfileCredentialsProperty"]]:
            '''The connector-specific credentials required when using Trend Micro.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-trendmicro
            '''
            result = self._values.get("trendmicro")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.TrendmicroConnectorProfileCredentialsProperty"]], result)

        @builtins.property
        def veeva(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.VeevaConnectorProfileCredentialsProperty"]]:
            '''The connector-specific credentials required when using Veeva.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-veeva
            '''
            result = self._values.get("veeva")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.VeevaConnectorProfileCredentialsProperty"]], result)

        @builtins.property
        def zendesk(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.ZendeskConnectorProfileCredentialsProperty"]]:
            '''The connector-specific credentials required when using Zendesk.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-zendesk
            '''
            result = self._values.get("zendesk")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.ZendeskConnectorProfileCredentialsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorProfilePropsMixin.ConnectorProfilePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "custom_connector": "customConnector",
            "datadog": "datadog",
            "dynatrace": "dynatrace",
            "infor_nexus": "inforNexus",
            "marketo": "marketo",
            "pardot": "pardot",
            "redshift": "redshift",
            "salesforce": "salesforce",
            "sapo_data": "sapoData",
            "service_now": "serviceNow",
            "slack": "slack",
            "snowflake": "snowflake",
            "veeva": "veeva",
            "zendesk": "zendesk",
        },
    )
    class ConnectorProfilePropertiesProperty:
        def __init__(
            self,
            *,
            custom_connector: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.CustomConnectorProfilePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            datadog: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.DatadogConnectorProfilePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            dynatrace: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.DynatraceConnectorProfilePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            infor_nexus: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.InforNexusConnectorProfilePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            marketo: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.MarketoConnectorProfilePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            pardot: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.PardotConnectorProfilePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            redshift: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.RedshiftConnectorProfilePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            salesforce: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.SalesforceConnectorProfilePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sapo_data: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.SAPODataConnectorProfilePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            service_now: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.ServiceNowConnectorProfilePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            slack: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.SlackConnectorProfilePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            snowflake: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.SnowflakeConnectorProfilePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            veeva: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.VeevaConnectorProfilePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            zendesk: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.ZendeskConnectorProfilePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The connector-specific profile properties required by each connector.

            :param custom_connector: The properties required by the custom connector.
            :param datadog: The connector-specific properties required by Datadog.
            :param dynatrace: The connector-specific properties required by Dynatrace.
            :param infor_nexus: The connector-specific properties required by Infor Nexus.
            :param marketo: The connector-specific properties required by Marketo.
            :param pardot: The connector-specific properties required by Salesforce Pardot.
            :param redshift: The connector-specific properties required by Amazon Redshift.
            :param salesforce: The connector-specific properties required by Salesforce.
            :param sapo_data: The connector-specific profile properties required when using SAPOData.
            :param service_now: The connector-specific properties required by serviceNow.
            :param slack: The connector-specific properties required by Slack.
            :param snowflake: The connector-specific properties required by Snowflake.
            :param veeva: The connector-specific properties required by Veeva.
            :param zendesk: The connector-specific properties required by Zendesk.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                connector_profile_properties_property = appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorProfilePropertiesProperty(
                    custom_connector=appflow_mixins.CfnConnectorProfilePropsMixin.CustomConnectorProfilePropertiesProperty(
                        o_auth2_properties=appflow_mixins.CfnConnectorProfilePropsMixin.OAuth2PropertiesProperty(
                            o_auth2_grant_type="oAuth2GrantType",
                            token_url="tokenUrl",
                            token_url_custom_properties={
                                "token_url_custom_properties_key": "tokenUrlCustomProperties"
                            }
                        ),
                        profile_properties={
                            "profile_properties_key": "profileProperties"
                        }
                    ),
                    datadog=appflow_mixins.CfnConnectorProfilePropsMixin.DatadogConnectorProfilePropertiesProperty(
                        instance_url="instanceUrl"
                    ),
                    dynatrace=appflow_mixins.CfnConnectorProfilePropsMixin.DynatraceConnectorProfilePropertiesProperty(
                        instance_url="instanceUrl"
                    ),
                    infor_nexus=appflow_mixins.CfnConnectorProfilePropsMixin.InforNexusConnectorProfilePropertiesProperty(
                        instance_url="instanceUrl"
                    ),
                    marketo=appflow_mixins.CfnConnectorProfilePropsMixin.MarketoConnectorProfilePropertiesProperty(
                        instance_url="instanceUrl"
                    ),
                    pardot=appflow_mixins.CfnConnectorProfilePropsMixin.PardotConnectorProfilePropertiesProperty(
                        business_unit_id="businessUnitId",
                        instance_url="instanceUrl",
                        is_sandbox_environment=False
                    ),
                    redshift=appflow_mixins.CfnConnectorProfilePropsMixin.RedshiftConnectorProfilePropertiesProperty(
                        bucket_name="bucketName",
                        bucket_prefix="bucketPrefix",
                        cluster_identifier="clusterIdentifier",
                        data_api_role_arn="dataApiRoleArn",
                        database_name="databaseName",
                        database_url="databaseUrl",
                        is_redshift_serverless=False,
                        role_arn="roleArn",
                        workgroup_name="workgroupName"
                    ),
                    salesforce=appflow_mixins.CfnConnectorProfilePropsMixin.SalesforceConnectorProfilePropertiesProperty(
                        instance_url="instanceUrl",
                        is_sandbox_environment=False,
                        use_private_link_for_metadata_and_authorization=False
                    ),
                    sapo_data=appflow_mixins.CfnConnectorProfilePropsMixin.SAPODataConnectorProfilePropertiesProperty(
                        application_host_url="applicationHostUrl",
                        application_service_path="applicationServicePath",
                        client_number="clientNumber",
                        disable_sso=False,
                        logon_language="logonLanguage",
                        o_auth_properties=appflow_mixins.CfnConnectorProfilePropsMixin.OAuthPropertiesProperty(
                            auth_code_url="authCodeUrl",
                            o_auth_scopes=["oAuthScopes"],
                            token_url="tokenUrl"
                        ),
                        port_number=123,
                        private_link_service_name="privateLinkServiceName"
                    ),
                    service_now=appflow_mixins.CfnConnectorProfilePropsMixin.ServiceNowConnectorProfilePropertiesProperty(
                        instance_url="instanceUrl"
                    ),
                    slack=appflow_mixins.CfnConnectorProfilePropsMixin.SlackConnectorProfilePropertiesProperty(
                        instance_url="instanceUrl"
                    ),
                    snowflake=appflow_mixins.CfnConnectorProfilePropsMixin.SnowflakeConnectorProfilePropertiesProperty(
                        account_name="accountName",
                        bucket_name="bucketName",
                        bucket_prefix="bucketPrefix",
                        private_link_service_name="privateLinkServiceName",
                        region="region",
                        stage="stage",
                        warehouse="warehouse"
                    ),
                    veeva=appflow_mixins.CfnConnectorProfilePropsMixin.VeevaConnectorProfilePropertiesProperty(
                        instance_url="instanceUrl"
                    ),
                    zendesk=appflow_mixins.CfnConnectorProfilePropsMixin.ZendeskConnectorProfilePropertiesProperty(
                        instance_url="instanceUrl"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__42c9f5518a432918c5de510ce82007e540b82507dfe62dddf30a9f582dcda0ae)
                check_type(argname="argument custom_connector", value=custom_connector, expected_type=type_hints["custom_connector"])
                check_type(argname="argument datadog", value=datadog, expected_type=type_hints["datadog"])
                check_type(argname="argument dynatrace", value=dynatrace, expected_type=type_hints["dynatrace"])
                check_type(argname="argument infor_nexus", value=infor_nexus, expected_type=type_hints["infor_nexus"])
                check_type(argname="argument marketo", value=marketo, expected_type=type_hints["marketo"])
                check_type(argname="argument pardot", value=pardot, expected_type=type_hints["pardot"])
                check_type(argname="argument redshift", value=redshift, expected_type=type_hints["redshift"])
                check_type(argname="argument salesforce", value=salesforce, expected_type=type_hints["salesforce"])
                check_type(argname="argument sapo_data", value=sapo_data, expected_type=type_hints["sapo_data"])
                check_type(argname="argument service_now", value=service_now, expected_type=type_hints["service_now"])
                check_type(argname="argument slack", value=slack, expected_type=type_hints["slack"])
                check_type(argname="argument snowflake", value=snowflake, expected_type=type_hints["snowflake"])
                check_type(argname="argument veeva", value=veeva, expected_type=type_hints["veeva"])
                check_type(argname="argument zendesk", value=zendesk, expected_type=type_hints["zendesk"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if custom_connector is not None:
                self._values["custom_connector"] = custom_connector
            if datadog is not None:
                self._values["datadog"] = datadog
            if dynatrace is not None:
                self._values["dynatrace"] = dynatrace
            if infor_nexus is not None:
                self._values["infor_nexus"] = infor_nexus
            if marketo is not None:
                self._values["marketo"] = marketo
            if pardot is not None:
                self._values["pardot"] = pardot
            if redshift is not None:
                self._values["redshift"] = redshift
            if salesforce is not None:
                self._values["salesforce"] = salesforce
            if sapo_data is not None:
                self._values["sapo_data"] = sapo_data
            if service_now is not None:
                self._values["service_now"] = service_now
            if slack is not None:
                self._values["slack"] = slack
            if snowflake is not None:
                self._values["snowflake"] = snowflake
            if veeva is not None:
                self._values["veeva"] = veeva
            if zendesk is not None:
                self._values["zendesk"] = zendesk

        @builtins.property
        def custom_connector(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.CustomConnectorProfilePropertiesProperty"]]:
            '''The properties required by the custom connector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileproperties.html#cfn-appflow-connectorprofile-connectorprofileproperties-customconnector
            '''
            result = self._values.get("custom_connector")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.CustomConnectorProfilePropertiesProperty"]], result)

        @builtins.property
        def datadog(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.DatadogConnectorProfilePropertiesProperty"]]:
            '''The connector-specific properties required by Datadog.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileproperties.html#cfn-appflow-connectorprofile-connectorprofileproperties-datadog
            '''
            result = self._values.get("datadog")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.DatadogConnectorProfilePropertiesProperty"]], result)

        @builtins.property
        def dynatrace(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.DynatraceConnectorProfilePropertiesProperty"]]:
            '''The connector-specific properties required by Dynatrace.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileproperties.html#cfn-appflow-connectorprofile-connectorprofileproperties-dynatrace
            '''
            result = self._values.get("dynatrace")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.DynatraceConnectorProfilePropertiesProperty"]], result)

        @builtins.property
        def infor_nexus(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.InforNexusConnectorProfilePropertiesProperty"]]:
            '''The connector-specific properties required by Infor Nexus.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileproperties.html#cfn-appflow-connectorprofile-connectorprofileproperties-infornexus
            '''
            result = self._values.get("infor_nexus")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.InforNexusConnectorProfilePropertiesProperty"]], result)

        @builtins.property
        def marketo(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.MarketoConnectorProfilePropertiesProperty"]]:
            '''The connector-specific properties required by Marketo.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileproperties.html#cfn-appflow-connectorprofile-connectorprofileproperties-marketo
            '''
            result = self._values.get("marketo")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.MarketoConnectorProfilePropertiesProperty"]], result)

        @builtins.property
        def pardot(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.PardotConnectorProfilePropertiesProperty"]]:
            '''The connector-specific properties required by Salesforce Pardot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileproperties.html#cfn-appflow-connectorprofile-connectorprofileproperties-pardot
            '''
            result = self._values.get("pardot")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.PardotConnectorProfilePropertiesProperty"]], result)

        @builtins.property
        def redshift(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.RedshiftConnectorProfilePropertiesProperty"]]:
            '''The connector-specific properties required by Amazon Redshift.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileproperties.html#cfn-appflow-connectorprofile-connectorprofileproperties-redshift
            '''
            result = self._values.get("redshift")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.RedshiftConnectorProfilePropertiesProperty"]], result)

        @builtins.property
        def salesforce(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.SalesforceConnectorProfilePropertiesProperty"]]:
            '''The connector-specific properties required by Salesforce.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileproperties.html#cfn-appflow-connectorprofile-connectorprofileproperties-salesforce
            '''
            result = self._values.get("salesforce")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.SalesforceConnectorProfilePropertiesProperty"]], result)

        @builtins.property
        def sapo_data(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.SAPODataConnectorProfilePropertiesProperty"]]:
            '''The connector-specific profile properties required when using SAPOData.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileproperties.html#cfn-appflow-connectorprofile-connectorprofileproperties-sapodata
            '''
            result = self._values.get("sapo_data")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.SAPODataConnectorProfilePropertiesProperty"]], result)

        @builtins.property
        def service_now(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.ServiceNowConnectorProfilePropertiesProperty"]]:
            '''The connector-specific properties required by serviceNow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileproperties.html#cfn-appflow-connectorprofile-connectorprofileproperties-servicenow
            '''
            result = self._values.get("service_now")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.ServiceNowConnectorProfilePropertiesProperty"]], result)

        @builtins.property
        def slack(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.SlackConnectorProfilePropertiesProperty"]]:
            '''The connector-specific properties required by Slack.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileproperties.html#cfn-appflow-connectorprofile-connectorprofileproperties-slack
            '''
            result = self._values.get("slack")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.SlackConnectorProfilePropertiesProperty"]], result)

        @builtins.property
        def snowflake(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.SnowflakeConnectorProfilePropertiesProperty"]]:
            '''The connector-specific properties required by Snowflake.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileproperties.html#cfn-appflow-connectorprofile-connectorprofileproperties-snowflake
            '''
            result = self._values.get("snowflake")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.SnowflakeConnectorProfilePropertiesProperty"]], result)

        @builtins.property
        def veeva(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.VeevaConnectorProfilePropertiesProperty"]]:
            '''The connector-specific properties required by Veeva.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileproperties.html#cfn-appflow-connectorprofile-connectorprofileproperties-veeva
            '''
            result = self._values.get("veeva")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.VeevaConnectorProfilePropertiesProperty"]], result)

        @builtins.property
        def zendesk(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.ZendeskConnectorProfilePropertiesProperty"]]:
            '''The connector-specific properties required by Zendesk.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileproperties.html#cfn-appflow-connectorprofile-connectorprofileproperties-zendesk
            '''
            result = self._values.get("zendesk")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.ZendeskConnectorProfilePropertiesProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectorProfilePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorProfilePropsMixin.CustomAuthCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "credentials_map": "credentialsMap",
            "custom_authentication_type": "customAuthenticationType",
        },
    )
    class CustomAuthCredentialsProperty:
        def __init__(
            self,
            *,
            credentials_map: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            custom_authentication_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The custom credentials required for custom authentication.

            :param credentials_map: A map that holds custom authentication credentials.
            :param custom_authentication_type: The custom authentication type that the connector uses.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-customauthcredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                custom_auth_credentials_property = appflow_mixins.CfnConnectorProfilePropsMixin.CustomAuthCredentialsProperty(
                    credentials_map={
                        "credentials_map_key": "credentialsMap"
                    },
                    custom_authentication_type="customAuthenticationType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__68c7c8e82201ad0d7db7eecfee433a3070b6db776463d7efd6da5539c2fead4c)
                check_type(argname="argument credentials_map", value=credentials_map, expected_type=type_hints["credentials_map"])
                check_type(argname="argument custom_authentication_type", value=custom_authentication_type, expected_type=type_hints["custom_authentication_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if credentials_map is not None:
                self._values["credentials_map"] = credentials_map
            if custom_authentication_type is not None:
                self._values["custom_authentication_type"] = custom_authentication_type

        @builtins.property
        def credentials_map(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''A map that holds custom authentication credentials.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-customauthcredentials.html#cfn-appflow-connectorprofile-customauthcredentials-credentialsmap
            '''
            result = self._values.get("credentials_map")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def custom_authentication_type(self) -> typing.Optional[builtins.str]:
            '''The custom authentication type that the connector uses.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-customauthcredentials.html#cfn-appflow-connectorprofile-customauthcredentials-customauthenticationtype
            '''
            result = self._values.get("custom_authentication_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomAuthCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorProfilePropsMixin.CustomConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "api_key": "apiKey",
            "authentication_type": "authenticationType",
            "basic": "basic",
            "custom": "custom",
            "oauth2": "oauth2",
        },
    )
    class CustomConnectorProfileCredentialsProperty:
        def __init__(
            self,
            *,
            api_key: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.ApiKeyCredentialsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            authentication_type: typing.Optional[builtins.str] = None,
            basic: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.BasicAuthCredentialsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            custom: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.CustomAuthCredentialsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            oauth2: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.OAuth2CredentialsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The connector-specific profile credentials that are required when using the custom connector.

            :param api_key: The API keys required for the authentication of the user.
            :param authentication_type: The authentication type that the custom connector uses for authenticating while creating a connector profile.
            :param basic: The basic credentials that are required for the authentication of the user.
            :param custom: If the connector uses the custom authentication mechanism, this holds the required credentials.
            :param oauth2: The OAuth 2.0 credentials required for the authentication of the user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-customconnectorprofilecredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                custom_connector_profile_credentials_property = appflow_mixins.CfnConnectorProfilePropsMixin.CustomConnectorProfileCredentialsProperty(
                    api_key=appflow_mixins.CfnConnectorProfilePropsMixin.ApiKeyCredentialsProperty(
                        api_key="apiKey",
                        api_secret_key="apiSecretKey"
                    ),
                    authentication_type="authenticationType",
                    basic=appflow_mixins.CfnConnectorProfilePropsMixin.BasicAuthCredentialsProperty(
                        password="password",
                        username="username"
                    ),
                    custom=appflow_mixins.CfnConnectorProfilePropsMixin.CustomAuthCredentialsProperty(
                        credentials_map={
                            "credentials_map_key": "credentialsMap"
                        },
                        custom_authentication_type="customAuthenticationType"
                    ),
                    oauth2=appflow_mixins.CfnConnectorProfilePropsMixin.OAuth2CredentialsProperty(
                        access_token="accessToken",
                        client_id="clientId",
                        client_secret="clientSecret",
                        o_auth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                            auth_code="authCode",
                            redirect_uri="redirectUri"
                        ),
                        refresh_token="refreshToken"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__be3c0e48c0c2435eb752cc2ceb29ff848dd87958a1429d9ca25544ea592ebd33)
                check_type(argname="argument api_key", value=api_key, expected_type=type_hints["api_key"])
                check_type(argname="argument authentication_type", value=authentication_type, expected_type=type_hints["authentication_type"])
                check_type(argname="argument basic", value=basic, expected_type=type_hints["basic"])
                check_type(argname="argument custom", value=custom, expected_type=type_hints["custom"])
                check_type(argname="argument oauth2", value=oauth2, expected_type=type_hints["oauth2"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if api_key is not None:
                self._values["api_key"] = api_key
            if authentication_type is not None:
                self._values["authentication_type"] = authentication_type
            if basic is not None:
                self._values["basic"] = basic
            if custom is not None:
                self._values["custom"] = custom
            if oauth2 is not None:
                self._values["oauth2"] = oauth2

        @builtins.property
        def api_key(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.ApiKeyCredentialsProperty"]]:
            '''The API keys required for the authentication of the user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-customconnectorprofilecredentials.html#cfn-appflow-connectorprofile-customconnectorprofilecredentials-apikey
            '''
            result = self._values.get("api_key")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.ApiKeyCredentialsProperty"]], result)

        @builtins.property
        def authentication_type(self) -> typing.Optional[builtins.str]:
            '''The authentication type that the custom connector uses for authenticating while creating a connector profile.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-customconnectorprofilecredentials.html#cfn-appflow-connectorprofile-customconnectorprofilecredentials-authenticationtype
            '''
            result = self._values.get("authentication_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def basic(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.BasicAuthCredentialsProperty"]]:
            '''The basic credentials that are required for the authentication of the user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-customconnectorprofilecredentials.html#cfn-appflow-connectorprofile-customconnectorprofilecredentials-basic
            '''
            result = self._values.get("basic")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.BasicAuthCredentialsProperty"]], result)

        @builtins.property
        def custom(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.CustomAuthCredentialsProperty"]]:
            '''If the connector uses the custom authentication mechanism, this holds the required credentials.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-customconnectorprofilecredentials.html#cfn-appflow-connectorprofile-customconnectorprofilecredentials-custom
            '''
            result = self._values.get("custom")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.CustomAuthCredentialsProperty"]], result)

        @builtins.property
        def oauth2(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.OAuth2CredentialsProperty"]]:
            '''The OAuth 2.0 credentials required for the authentication of the user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-customconnectorprofilecredentials.html#cfn-appflow-connectorprofile-customconnectorprofilecredentials-oauth2
            '''
            result = self._values.get("oauth2")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.OAuth2CredentialsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorProfilePropsMixin.CustomConnectorProfilePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "o_auth2_properties": "oAuth2Properties",
            "profile_properties": "profileProperties",
        },
    )
    class CustomConnectorProfilePropertiesProperty:
        def __init__(
            self,
            *,
            o_auth2_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.OAuth2PropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            profile_properties: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The profile properties required by the custom connector.

            :param o_auth2_properties: The OAuth 2.0 properties required for OAuth 2.0 authentication.
            :param profile_properties: A map of properties that are required to create a profile for the custom connector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-customconnectorprofileproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                custom_connector_profile_properties_property = appflow_mixins.CfnConnectorProfilePropsMixin.CustomConnectorProfilePropertiesProperty(
                    o_auth2_properties=appflow_mixins.CfnConnectorProfilePropsMixin.OAuth2PropertiesProperty(
                        o_auth2_grant_type="oAuth2GrantType",
                        token_url="tokenUrl",
                        token_url_custom_properties={
                            "token_url_custom_properties_key": "tokenUrlCustomProperties"
                        }
                    ),
                    profile_properties={
                        "profile_properties_key": "profileProperties"
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__137a606e63a6b4cfa545ced0408d05476d64e43df4b05b47bf896dab50e3e1d6)
                check_type(argname="argument o_auth2_properties", value=o_auth2_properties, expected_type=type_hints["o_auth2_properties"])
                check_type(argname="argument profile_properties", value=profile_properties, expected_type=type_hints["profile_properties"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if o_auth2_properties is not None:
                self._values["o_auth2_properties"] = o_auth2_properties
            if profile_properties is not None:
                self._values["profile_properties"] = profile_properties

        @builtins.property
        def o_auth2_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.OAuth2PropertiesProperty"]]:
            '''The OAuth 2.0 properties required for OAuth 2.0 authentication.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-customconnectorprofileproperties.html#cfn-appflow-connectorprofile-customconnectorprofileproperties-oauth2properties
            '''
            result = self._values.get("o_auth2_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.OAuth2PropertiesProperty"]], result)

        @builtins.property
        def profile_properties(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''A map of properties that are required to create a profile for the custom connector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-customconnectorprofileproperties.html#cfn-appflow-connectorprofile-customconnectorprofileproperties-profileproperties
            '''
            result = self._values.get("profile_properties")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomConnectorProfilePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorProfilePropsMixin.DatadogConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={"api_key": "apiKey", "application_key": "applicationKey"},
    )
    class DatadogConnectorProfileCredentialsProperty:
        def __init__(
            self,
            *,
            api_key: typing.Optional[builtins.str] = None,
            application_key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The connector-specific credentials required by Datadog.

            :param api_key: A unique alphanumeric identifier used to authenticate a user, developer, or calling program to your API.
            :param application_key: Application keys, in conjunction with your API key, give you full access to Datadog’s programmatic API. Application keys are associated with the user account that created them. The application key is used to log all requests made to the API.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-datadogconnectorprofilecredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                datadog_connector_profile_credentials_property = appflow_mixins.CfnConnectorProfilePropsMixin.DatadogConnectorProfileCredentialsProperty(
                    api_key="apiKey",
                    application_key="applicationKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a499b3939b5d77883fdab18c50f768a4dad9cef9bdddcd558e7c4dffaa796a7d)
                check_type(argname="argument api_key", value=api_key, expected_type=type_hints["api_key"])
                check_type(argname="argument application_key", value=application_key, expected_type=type_hints["application_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if api_key is not None:
                self._values["api_key"] = api_key
            if application_key is not None:
                self._values["application_key"] = application_key

        @builtins.property
        def api_key(self) -> typing.Optional[builtins.str]:
            '''A unique alphanumeric identifier used to authenticate a user, developer, or calling program to your API.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-datadogconnectorprofilecredentials.html#cfn-appflow-connectorprofile-datadogconnectorprofilecredentials-apikey
            '''
            result = self._values.get("api_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def application_key(self) -> typing.Optional[builtins.str]:
            '''Application keys, in conjunction with your API key, give you full access to Datadog’s programmatic API.

            Application keys are associated with the user account that created them. The application key is used to log all requests made to the API.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-datadogconnectorprofilecredentials.html#cfn-appflow-connectorprofile-datadogconnectorprofilecredentials-applicationkey
            '''
            result = self._values.get("application_key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DatadogConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorProfilePropsMixin.DatadogConnectorProfilePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"instance_url": "instanceUrl"},
    )
    class DatadogConnectorProfilePropertiesProperty:
        def __init__(
            self,
            *,
            instance_url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The connector-specific profile properties required by Datadog.

            :param instance_url: The location of the Datadog resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-datadogconnectorprofileproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                datadog_connector_profile_properties_property = appflow_mixins.CfnConnectorProfilePropsMixin.DatadogConnectorProfilePropertiesProperty(
                    instance_url="instanceUrl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e53e94bf856c66366647d7f144bc0e7bf12aa8f1e7086e6fa9ce1a1c2330efce)
                check_type(argname="argument instance_url", value=instance_url, expected_type=type_hints["instance_url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if instance_url is not None:
                self._values["instance_url"] = instance_url

        @builtins.property
        def instance_url(self) -> typing.Optional[builtins.str]:
            '''The location of the Datadog resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-datadogconnectorprofileproperties.html#cfn-appflow-connectorprofile-datadogconnectorprofileproperties-instanceurl
            '''
            result = self._values.get("instance_url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DatadogConnectorProfilePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorProfilePropsMixin.DynatraceConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={"api_token": "apiToken"},
    )
    class DynatraceConnectorProfileCredentialsProperty:
        def __init__(self, *, api_token: typing.Optional[builtins.str] = None) -> None:
            '''The connector-specific profile credentials required by Dynatrace.

            :param api_token: The API tokens used by Dynatrace API to authenticate various API calls.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-dynatraceconnectorprofilecredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                dynatrace_connector_profile_credentials_property = appflow_mixins.CfnConnectorProfilePropsMixin.DynatraceConnectorProfileCredentialsProperty(
                    api_token="apiToken"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d36c22e9d75908d30e008193ab40c6055eea17706ce1effe13a867b1f012771b)
                check_type(argname="argument api_token", value=api_token, expected_type=type_hints["api_token"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if api_token is not None:
                self._values["api_token"] = api_token

        @builtins.property
        def api_token(self) -> typing.Optional[builtins.str]:
            '''The API tokens used by Dynatrace API to authenticate various API calls.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-dynatraceconnectorprofilecredentials.html#cfn-appflow-connectorprofile-dynatraceconnectorprofilecredentials-apitoken
            '''
            result = self._values.get("api_token")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DynatraceConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorProfilePropsMixin.DynatraceConnectorProfilePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"instance_url": "instanceUrl"},
    )
    class DynatraceConnectorProfilePropertiesProperty:
        def __init__(
            self,
            *,
            instance_url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The connector-specific profile properties required by Dynatrace.

            :param instance_url: The location of the Dynatrace resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-dynatraceconnectorprofileproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                dynatrace_connector_profile_properties_property = appflow_mixins.CfnConnectorProfilePropsMixin.DynatraceConnectorProfilePropertiesProperty(
                    instance_url="instanceUrl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__04b07602c368786946816996d5d3ff2c0414ea3a1c2e2e6925f803bfa16ec6a8)
                check_type(argname="argument instance_url", value=instance_url, expected_type=type_hints["instance_url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if instance_url is not None:
                self._values["instance_url"] = instance_url

        @builtins.property
        def instance_url(self) -> typing.Optional[builtins.str]:
            '''The location of the Dynatrace resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-dynatraceconnectorprofileproperties.html#cfn-appflow-connectorprofile-dynatraceconnectorprofileproperties-instanceurl
            '''
            result = self._values.get("instance_url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DynatraceConnectorProfilePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorProfilePropsMixin.GoogleAnalyticsConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_token": "accessToken",
            "client_id": "clientId",
            "client_secret": "clientSecret",
            "connector_o_auth_request": "connectorOAuthRequest",
            "refresh_token": "refreshToken",
        },
    )
    class GoogleAnalyticsConnectorProfileCredentialsProperty:
        def __init__(
            self,
            *,
            access_token: typing.Optional[builtins.str] = None,
            client_id: typing.Optional[builtins.str] = None,
            client_secret: typing.Optional[builtins.str] = None,
            connector_o_auth_request: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            refresh_token: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The connector-specific profile credentials required by Google Analytics.

            :param access_token: The credentials used to access protected Google Analytics resources.
            :param client_id: The identifier for the desired client.
            :param client_secret: The client secret used by the OAuth client to authenticate to the authorization server.
            :param connector_o_auth_request: Used by select connectors for which the OAuth workflow is supported, such as Salesforce, Google Analytics, Marketo, Zendesk, and Slack.
            :param refresh_token: The credentials used to acquire new access tokens. This is required only for OAuth2 access tokens, and is not required for OAuth1 access tokens.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-googleanalyticsconnectorprofilecredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                google_analytics_connector_profile_credentials_property = appflow_mixins.CfnConnectorProfilePropsMixin.GoogleAnalyticsConnectorProfileCredentialsProperty(
                    access_token="accessToken",
                    client_id="clientId",
                    client_secret="clientSecret",
                    connector_oAuth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                        auth_code="authCode",
                        redirect_uri="redirectUri"
                    ),
                    refresh_token="refreshToken"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__44b968662f544f8fe0a61123f41ae86437601fa816fb7077cacf33da77003f2f)
                check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
                check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
                check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
                check_type(argname="argument connector_o_auth_request", value=connector_o_auth_request, expected_type=type_hints["connector_o_auth_request"])
                check_type(argname="argument refresh_token", value=refresh_token, expected_type=type_hints["refresh_token"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_token is not None:
                self._values["access_token"] = access_token
            if client_id is not None:
                self._values["client_id"] = client_id
            if client_secret is not None:
                self._values["client_secret"] = client_secret
            if connector_o_auth_request is not None:
                self._values["connector_o_auth_request"] = connector_o_auth_request
            if refresh_token is not None:
                self._values["refresh_token"] = refresh_token

        @builtins.property
        def access_token(self) -> typing.Optional[builtins.str]:
            '''The credentials used to access protected Google Analytics resources.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-googleanalyticsconnectorprofilecredentials.html#cfn-appflow-connectorprofile-googleanalyticsconnectorprofilecredentials-accesstoken
            '''
            result = self._values.get("access_token")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def client_id(self) -> typing.Optional[builtins.str]:
            '''The identifier for the desired client.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-googleanalyticsconnectorprofilecredentials.html#cfn-appflow-connectorprofile-googleanalyticsconnectorprofilecredentials-clientid
            '''
            result = self._values.get("client_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def client_secret(self) -> typing.Optional[builtins.str]:
            '''The client secret used by the OAuth client to authenticate to the authorization server.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-googleanalyticsconnectorprofilecredentials.html#cfn-appflow-connectorprofile-googleanalyticsconnectorprofilecredentials-clientsecret
            '''
            result = self._values.get("client_secret")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def connector_o_auth_request(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty"]]:
            '''Used by select connectors for which the OAuth workflow is supported, such as Salesforce, Google Analytics, Marketo, Zendesk, and Slack.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-googleanalyticsconnectorprofilecredentials.html#cfn-appflow-connectorprofile-googleanalyticsconnectorprofilecredentials-connectoroauthrequest
            '''
            result = self._values.get("connector_o_auth_request")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty"]], result)

        @builtins.property
        def refresh_token(self) -> typing.Optional[builtins.str]:
            '''The credentials used to acquire new access tokens.

            This is required only for OAuth2 access tokens, and is not required for OAuth1 access tokens.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-googleanalyticsconnectorprofilecredentials.html#cfn-appflow-connectorprofile-googleanalyticsconnectorprofilecredentials-refreshtoken
            '''
            result = self._values.get("refresh_token")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GoogleAnalyticsConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorProfilePropsMixin.InforNexusConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_key_id": "accessKeyId",
            "datakey": "datakey",
            "secret_access_key": "secretAccessKey",
            "user_id": "userId",
        },
    )
    class InforNexusConnectorProfileCredentialsProperty:
        def __init__(
            self,
            *,
            access_key_id: typing.Optional[builtins.str] = None,
            datakey: typing.Optional[builtins.str] = None,
            secret_access_key: typing.Optional[builtins.str] = None,
            user_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The connector-specific profile credentials required by Infor Nexus.

            :param access_key_id: The Access Key portion of the credentials.
            :param datakey: The encryption keys used to encrypt data.
            :param secret_access_key: The secret key used to sign requests.
            :param user_id: The identifier for the user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-infornexusconnectorprofilecredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                infor_nexus_connector_profile_credentials_property = appflow_mixins.CfnConnectorProfilePropsMixin.InforNexusConnectorProfileCredentialsProperty(
                    access_key_id="accessKeyId",
                    datakey="datakey",
                    secret_access_key="secretAccessKey",
                    user_id="userId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e9a1288438d705acf6103dbb0f6de84702321065586fc9a9137e7f516c46598f)
                check_type(argname="argument access_key_id", value=access_key_id, expected_type=type_hints["access_key_id"])
                check_type(argname="argument datakey", value=datakey, expected_type=type_hints["datakey"])
                check_type(argname="argument secret_access_key", value=secret_access_key, expected_type=type_hints["secret_access_key"])
                check_type(argname="argument user_id", value=user_id, expected_type=type_hints["user_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_key_id is not None:
                self._values["access_key_id"] = access_key_id
            if datakey is not None:
                self._values["datakey"] = datakey
            if secret_access_key is not None:
                self._values["secret_access_key"] = secret_access_key
            if user_id is not None:
                self._values["user_id"] = user_id

        @builtins.property
        def access_key_id(self) -> typing.Optional[builtins.str]:
            '''The Access Key portion of the credentials.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-infornexusconnectorprofilecredentials.html#cfn-appflow-connectorprofile-infornexusconnectorprofilecredentials-accesskeyid
            '''
            result = self._values.get("access_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def datakey(self) -> typing.Optional[builtins.str]:
            '''The encryption keys used to encrypt data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-infornexusconnectorprofilecredentials.html#cfn-appflow-connectorprofile-infornexusconnectorprofilecredentials-datakey
            '''
            result = self._values.get("datakey")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secret_access_key(self) -> typing.Optional[builtins.str]:
            '''The secret key used to sign requests.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-infornexusconnectorprofilecredentials.html#cfn-appflow-connectorprofile-infornexusconnectorprofilecredentials-secretaccesskey
            '''
            result = self._values.get("secret_access_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user_id(self) -> typing.Optional[builtins.str]:
            '''The identifier for the user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-infornexusconnectorprofilecredentials.html#cfn-appflow-connectorprofile-infornexusconnectorprofilecredentials-userid
            '''
            result = self._values.get("user_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InforNexusConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorProfilePropsMixin.InforNexusConnectorProfilePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"instance_url": "instanceUrl"},
    )
    class InforNexusConnectorProfilePropertiesProperty:
        def __init__(
            self,
            *,
            instance_url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The connector-specific profile properties required by Infor Nexus.

            :param instance_url: The location of the Infor Nexus resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-infornexusconnectorprofileproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                infor_nexus_connector_profile_properties_property = appflow_mixins.CfnConnectorProfilePropsMixin.InforNexusConnectorProfilePropertiesProperty(
                    instance_url="instanceUrl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5ba63f4a603127c9973d777327b774c293f2dddbc21925f7900377d8005f2dc5)
                check_type(argname="argument instance_url", value=instance_url, expected_type=type_hints["instance_url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if instance_url is not None:
                self._values["instance_url"] = instance_url

        @builtins.property
        def instance_url(self) -> typing.Optional[builtins.str]:
            '''The location of the Infor Nexus resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-infornexusconnectorprofileproperties.html#cfn-appflow-connectorprofile-infornexusconnectorprofileproperties-instanceurl
            '''
            result = self._values.get("instance_url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InforNexusConnectorProfilePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorProfilePropsMixin.MarketoConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_token": "accessToken",
            "client_id": "clientId",
            "client_secret": "clientSecret",
            "connector_o_auth_request": "connectorOAuthRequest",
        },
    )
    class MarketoConnectorProfileCredentialsProperty:
        def __init__(
            self,
            *,
            access_token: typing.Optional[builtins.str] = None,
            client_id: typing.Optional[builtins.str] = None,
            client_secret: typing.Optional[builtins.str] = None,
            connector_o_auth_request: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The connector-specific profile credentials required by Marketo.

            :param access_token: The credentials used to access protected Marketo resources.
            :param client_id: The identifier for the desired client.
            :param client_secret: The client secret used by the OAuth client to authenticate to the authorization server.
            :param connector_o_auth_request: Used by select connectors for which the OAuth workflow is supported, such as Salesforce, Google Analytics, Marketo, Zendesk, and Slack.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-marketoconnectorprofilecredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                marketo_connector_profile_credentials_property = appflow_mixins.CfnConnectorProfilePropsMixin.MarketoConnectorProfileCredentialsProperty(
                    access_token="accessToken",
                    client_id="clientId",
                    client_secret="clientSecret",
                    connector_oAuth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                        auth_code="authCode",
                        redirect_uri="redirectUri"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6a597e43c9eed964535f959ef98f0052df1102ee44f65803081357a31960d2e5)
                check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
                check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
                check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
                check_type(argname="argument connector_o_auth_request", value=connector_o_auth_request, expected_type=type_hints["connector_o_auth_request"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_token is not None:
                self._values["access_token"] = access_token
            if client_id is not None:
                self._values["client_id"] = client_id
            if client_secret is not None:
                self._values["client_secret"] = client_secret
            if connector_o_auth_request is not None:
                self._values["connector_o_auth_request"] = connector_o_auth_request

        @builtins.property
        def access_token(self) -> typing.Optional[builtins.str]:
            '''The credentials used to access protected Marketo resources.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-marketoconnectorprofilecredentials.html#cfn-appflow-connectorprofile-marketoconnectorprofilecredentials-accesstoken
            '''
            result = self._values.get("access_token")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def client_id(self) -> typing.Optional[builtins.str]:
            '''The identifier for the desired client.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-marketoconnectorprofilecredentials.html#cfn-appflow-connectorprofile-marketoconnectorprofilecredentials-clientid
            '''
            result = self._values.get("client_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def client_secret(self) -> typing.Optional[builtins.str]:
            '''The client secret used by the OAuth client to authenticate to the authorization server.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-marketoconnectorprofilecredentials.html#cfn-appflow-connectorprofile-marketoconnectorprofilecredentials-clientsecret
            '''
            result = self._values.get("client_secret")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def connector_o_auth_request(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty"]]:
            '''Used by select connectors for which the OAuth workflow is supported, such as Salesforce, Google Analytics, Marketo, Zendesk, and Slack.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-marketoconnectorprofilecredentials.html#cfn-appflow-connectorprofile-marketoconnectorprofilecredentials-connectoroauthrequest
            '''
            result = self._values.get("connector_o_auth_request")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MarketoConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorProfilePropsMixin.MarketoConnectorProfilePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"instance_url": "instanceUrl"},
    )
    class MarketoConnectorProfilePropertiesProperty:
        def __init__(
            self,
            *,
            instance_url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The connector-specific profile properties required when using Marketo.

            :param instance_url: The location of the Marketo resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-marketoconnectorprofileproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                marketo_connector_profile_properties_property = appflow_mixins.CfnConnectorProfilePropsMixin.MarketoConnectorProfilePropertiesProperty(
                    instance_url="instanceUrl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__66549bd7502d034d51fd17edf1c6efbd8ea21a3edf31dde5c364786c68476985)
                check_type(argname="argument instance_url", value=instance_url, expected_type=type_hints["instance_url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if instance_url is not None:
                self._values["instance_url"] = instance_url

        @builtins.property
        def instance_url(self) -> typing.Optional[builtins.str]:
            '''The location of the Marketo resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-marketoconnectorprofileproperties.html#cfn-appflow-connectorprofile-marketoconnectorprofileproperties-instanceurl
            '''
            result = self._values.get("instance_url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MarketoConnectorProfilePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorProfilePropsMixin.OAuth2CredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_token": "accessToken",
            "client_id": "clientId",
            "client_secret": "clientSecret",
            "o_auth_request": "oAuthRequest",
            "refresh_token": "refreshToken",
        },
    )
    class OAuth2CredentialsProperty:
        def __init__(
            self,
            *,
            access_token: typing.Optional[builtins.str] = None,
            client_id: typing.Optional[builtins.str] = None,
            client_secret: typing.Optional[builtins.str] = None,
            o_auth_request: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            refresh_token: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The OAuth 2.0 credentials required for OAuth 2.0 authentication.

            :param access_token: The access token used to access the connector on your behalf.
            :param client_id: The identifier for the desired client.
            :param client_secret: The client secret used by the OAuth client to authenticate to the authorization server.
            :param o_auth_request: 
            :param refresh_token: The refresh token used to refresh an expired access token.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-oauth2credentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                o_auth2_credentials_property = appflow_mixins.CfnConnectorProfilePropsMixin.OAuth2CredentialsProperty(
                    access_token="accessToken",
                    client_id="clientId",
                    client_secret="clientSecret",
                    o_auth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                        auth_code="authCode",
                        redirect_uri="redirectUri"
                    ),
                    refresh_token="refreshToken"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1bd52b9793e4e2f694b91fb23b192c734322eb4b4ccb52c9546f783ad1958af2)
                check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
                check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
                check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
                check_type(argname="argument o_auth_request", value=o_auth_request, expected_type=type_hints["o_auth_request"])
                check_type(argname="argument refresh_token", value=refresh_token, expected_type=type_hints["refresh_token"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_token is not None:
                self._values["access_token"] = access_token
            if client_id is not None:
                self._values["client_id"] = client_id
            if client_secret is not None:
                self._values["client_secret"] = client_secret
            if o_auth_request is not None:
                self._values["o_auth_request"] = o_auth_request
            if refresh_token is not None:
                self._values["refresh_token"] = refresh_token

        @builtins.property
        def access_token(self) -> typing.Optional[builtins.str]:
            '''The access token used to access the connector on your behalf.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-oauth2credentials.html#cfn-appflow-connectorprofile-oauth2credentials-accesstoken
            '''
            result = self._values.get("access_token")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def client_id(self) -> typing.Optional[builtins.str]:
            '''The identifier for the desired client.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-oauth2credentials.html#cfn-appflow-connectorprofile-oauth2credentials-clientid
            '''
            result = self._values.get("client_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def client_secret(self) -> typing.Optional[builtins.str]:
            '''The client secret used by the OAuth client to authenticate to the authorization server.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-oauth2credentials.html#cfn-appflow-connectorprofile-oauth2credentials-clientsecret
            '''
            result = self._values.get("client_secret")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def o_auth_request(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-oauth2credentials.html#cfn-appflow-connectorprofile-oauth2credentials-oauthrequest
            '''
            result = self._values.get("o_auth_request")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty"]], result)

        @builtins.property
        def refresh_token(self) -> typing.Optional[builtins.str]:
            '''The refresh token used to refresh an expired access token.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-oauth2credentials.html#cfn-appflow-connectorprofile-oauth2credentials-refreshtoken
            '''
            result = self._values.get("refresh_token")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OAuth2CredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorProfilePropsMixin.OAuth2PropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "o_auth2_grant_type": "oAuth2GrantType",
            "token_url": "tokenUrl",
            "token_url_custom_properties": "tokenUrlCustomProperties",
        },
    )
    class OAuth2PropertiesProperty:
        def __init__(
            self,
            *,
            o_auth2_grant_type: typing.Optional[builtins.str] = None,
            token_url: typing.Optional[builtins.str] = None,
            token_url_custom_properties: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The OAuth 2.0 properties required for OAuth 2.0 authentication.

            :param o_auth2_grant_type: The OAuth 2.0 grant type used by connector for OAuth 2.0 authentication.
            :param token_url: The token URL required for OAuth 2.0 authentication.
            :param token_url_custom_properties: Associates your token URL with a map of properties that you define. Use this parameter to provide any additional details that the connector requires to authenticate your request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-oauth2properties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                o_auth2_properties_property = appflow_mixins.CfnConnectorProfilePropsMixin.OAuth2PropertiesProperty(
                    o_auth2_grant_type="oAuth2GrantType",
                    token_url="tokenUrl",
                    token_url_custom_properties={
                        "token_url_custom_properties_key": "tokenUrlCustomProperties"
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f76bc658ee8a586a5a4121ac225ddc9e65c0401ca8c25f41c3031345b8251675)
                check_type(argname="argument o_auth2_grant_type", value=o_auth2_grant_type, expected_type=type_hints["o_auth2_grant_type"])
                check_type(argname="argument token_url", value=token_url, expected_type=type_hints["token_url"])
                check_type(argname="argument token_url_custom_properties", value=token_url_custom_properties, expected_type=type_hints["token_url_custom_properties"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if o_auth2_grant_type is not None:
                self._values["o_auth2_grant_type"] = o_auth2_grant_type
            if token_url is not None:
                self._values["token_url"] = token_url
            if token_url_custom_properties is not None:
                self._values["token_url_custom_properties"] = token_url_custom_properties

        @builtins.property
        def o_auth2_grant_type(self) -> typing.Optional[builtins.str]:
            '''The OAuth 2.0 grant type used by connector for OAuth 2.0 authentication.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-oauth2properties.html#cfn-appflow-connectorprofile-oauth2properties-oauth2granttype
            '''
            result = self._values.get("o_auth2_grant_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def token_url(self) -> typing.Optional[builtins.str]:
            '''The token URL required for OAuth 2.0 authentication.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-oauth2properties.html#cfn-appflow-connectorprofile-oauth2properties-tokenurl
            '''
            result = self._values.get("token_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def token_url_custom_properties(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''Associates your token URL with a map of properties that you define.

            Use this parameter to provide any additional details that the connector requires to authenticate your request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-oauth2properties.html#cfn-appflow-connectorprofile-oauth2properties-tokenurlcustomproperties
            '''
            result = self._values.get("token_url_custom_properties")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OAuth2PropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorProfilePropsMixin.OAuthCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_token": "accessToken",
            "client_id": "clientId",
            "client_secret": "clientSecret",
            "connector_o_auth_request": "connectorOAuthRequest",
            "refresh_token": "refreshToken",
        },
    )
    class OAuthCredentialsProperty:
        def __init__(
            self,
            *,
            access_token: typing.Optional[builtins.str] = None,
            client_id: typing.Optional[builtins.str] = None,
            client_secret: typing.Optional[builtins.str] = None,
            connector_o_auth_request: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            refresh_token: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The OAuth credentials required for OAuth type authentication.

            :param access_token: The access token used to access protected SAPOData resources.
            :param client_id: The identifier for the desired client.
            :param client_secret: The client secret used by the OAuth client to authenticate to the authorization server.
            :param connector_o_auth_request: 
            :param refresh_token: The refresh token used to refresh expired access token.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-oauthcredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                o_auth_credentials_property = appflow_mixins.CfnConnectorProfilePropsMixin.OAuthCredentialsProperty(
                    access_token="accessToken",
                    client_id="clientId",
                    client_secret="clientSecret",
                    connector_oAuth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                        auth_code="authCode",
                        redirect_uri="redirectUri"
                    ),
                    refresh_token="refreshToken"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f5ae19965f35aff50d6468c49a046c9111626f3f4e4333fab18828db4d83c25e)
                check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
                check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
                check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
                check_type(argname="argument connector_o_auth_request", value=connector_o_auth_request, expected_type=type_hints["connector_o_auth_request"])
                check_type(argname="argument refresh_token", value=refresh_token, expected_type=type_hints["refresh_token"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_token is not None:
                self._values["access_token"] = access_token
            if client_id is not None:
                self._values["client_id"] = client_id
            if client_secret is not None:
                self._values["client_secret"] = client_secret
            if connector_o_auth_request is not None:
                self._values["connector_o_auth_request"] = connector_o_auth_request
            if refresh_token is not None:
                self._values["refresh_token"] = refresh_token

        @builtins.property
        def access_token(self) -> typing.Optional[builtins.str]:
            '''The access token used to access protected SAPOData resources.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-oauthcredentials.html#cfn-appflow-connectorprofile-oauthcredentials-accesstoken
            '''
            result = self._values.get("access_token")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def client_id(self) -> typing.Optional[builtins.str]:
            '''The identifier for the desired client.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-oauthcredentials.html#cfn-appflow-connectorprofile-oauthcredentials-clientid
            '''
            result = self._values.get("client_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def client_secret(self) -> typing.Optional[builtins.str]:
            '''The client secret used by the OAuth client to authenticate to the authorization server.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-oauthcredentials.html#cfn-appflow-connectorprofile-oauthcredentials-clientsecret
            '''
            result = self._values.get("client_secret")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def connector_o_auth_request(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-oauthcredentials.html#cfn-appflow-connectorprofile-oauthcredentials-connectoroauthrequest
            '''
            result = self._values.get("connector_o_auth_request")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty"]], result)

        @builtins.property
        def refresh_token(self) -> typing.Optional[builtins.str]:
            '''The refresh token used to refresh expired access token.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-oauthcredentials.html#cfn-appflow-connectorprofile-oauthcredentials-refreshtoken
            '''
            result = self._values.get("refresh_token")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OAuthCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorProfilePropsMixin.OAuthPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "auth_code_url": "authCodeUrl",
            "o_auth_scopes": "oAuthScopes",
            "token_url": "tokenUrl",
        },
    )
    class OAuthPropertiesProperty:
        def __init__(
            self,
            *,
            auth_code_url: typing.Optional[builtins.str] = None,
            o_auth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
            token_url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The OAuth properties required for OAuth type authentication.

            :param auth_code_url: The authorization code url required to redirect to SAP Login Page to fetch authorization code for OAuth type authentication.
            :param o_auth_scopes: The OAuth scopes required for OAuth type authentication.
            :param token_url: The token url required to fetch access/refresh tokens using authorization code and also to refresh expired access token using refresh token.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-oauthproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                o_auth_properties_property = appflow_mixins.CfnConnectorProfilePropsMixin.OAuthPropertiesProperty(
                    auth_code_url="authCodeUrl",
                    o_auth_scopes=["oAuthScopes"],
                    token_url="tokenUrl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__69bfe5bc4f93cf5fe4c61ffce3033f07a9d597afb8acadc8e8233a750f0baa32)
                check_type(argname="argument auth_code_url", value=auth_code_url, expected_type=type_hints["auth_code_url"])
                check_type(argname="argument o_auth_scopes", value=o_auth_scopes, expected_type=type_hints["o_auth_scopes"])
                check_type(argname="argument token_url", value=token_url, expected_type=type_hints["token_url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auth_code_url is not None:
                self._values["auth_code_url"] = auth_code_url
            if o_auth_scopes is not None:
                self._values["o_auth_scopes"] = o_auth_scopes
            if token_url is not None:
                self._values["token_url"] = token_url

        @builtins.property
        def auth_code_url(self) -> typing.Optional[builtins.str]:
            '''The authorization code url required to redirect to SAP Login Page to fetch authorization code for OAuth type authentication.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-oauthproperties.html#cfn-appflow-connectorprofile-oauthproperties-authcodeurl
            '''
            result = self._values.get("auth_code_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def o_auth_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The OAuth scopes required for OAuth type authentication.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-oauthproperties.html#cfn-appflow-connectorprofile-oauthproperties-oauthscopes
            '''
            result = self._values.get("o_auth_scopes")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def token_url(self) -> typing.Optional[builtins.str]:
            '''The token url required to fetch access/refresh tokens using authorization code and also to refresh expired access token using refresh token.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-oauthproperties.html#cfn-appflow-connectorprofile-oauthproperties-tokenurl
            '''
            result = self._values.get("token_url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OAuthPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorProfilePropsMixin.PardotConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_token": "accessToken",
            "client_credentials_arn": "clientCredentialsArn",
            "connector_o_auth_request": "connectorOAuthRequest",
            "refresh_token": "refreshToken",
        },
    )
    class PardotConnectorProfileCredentialsProperty:
        def __init__(
            self,
            *,
            access_token: typing.Optional[builtins.str] = None,
            client_credentials_arn: typing.Optional[builtins.str] = None,
            connector_o_auth_request: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            refresh_token: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The connector-specific profile credentials required when using Salesforce Pardot.

            :param access_token: The credentials used to access protected Salesforce Pardot resources.
            :param client_credentials_arn: The secret manager ARN, which contains the client ID and client secret of the connected app.
            :param connector_o_auth_request: 
            :param refresh_token: The credentials used to acquire new access tokens.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-pardotconnectorprofilecredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                pardot_connector_profile_credentials_property = appflow_mixins.CfnConnectorProfilePropsMixin.PardotConnectorProfileCredentialsProperty(
                    access_token="accessToken",
                    client_credentials_arn="clientCredentialsArn",
                    connector_oAuth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                        auth_code="authCode",
                        redirect_uri="redirectUri"
                    ),
                    refresh_token="refreshToken"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2f723aa7e3dd5ad7db2cbd59d52b03c7d23915692b2713f8ad8bf50d64e2fd20)
                check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
                check_type(argname="argument client_credentials_arn", value=client_credentials_arn, expected_type=type_hints["client_credentials_arn"])
                check_type(argname="argument connector_o_auth_request", value=connector_o_auth_request, expected_type=type_hints["connector_o_auth_request"])
                check_type(argname="argument refresh_token", value=refresh_token, expected_type=type_hints["refresh_token"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_token is not None:
                self._values["access_token"] = access_token
            if client_credentials_arn is not None:
                self._values["client_credentials_arn"] = client_credentials_arn
            if connector_o_auth_request is not None:
                self._values["connector_o_auth_request"] = connector_o_auth_request
            if refresh_token is not None:
                self._values["refresh_token"] = refresh_token

        @builtins.property
        def access_token(self) -> typing.Optional[builtins.str]:
            '''The credentials used to access protected Salesforce Pardot resources.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-pardotconnectorprofilecredentials.html#cfn-appflow-connectorprofile-pardotconnectorprofilecredentials-accesstoken
            '''
            result = self._values.get("access_token")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def client_credentials_arn(self) -> typing.Optional[builtins.str]:
            '''The secret manager ARN, which contains the client ID and client secret of the connected app.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-pardotconnectorprofilecredentials.html#cfn-appflow-connectorprofile-pardotconnectorprofilecredentials-clientcredentialsarn
            '''
            result = self._values.get("client_credentials_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def connector_o_auth_request(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-pardotconnectorprofilecredentials.html#cfn-appflow-connectorprofile-pardotconnectorprofilecredentials-connectoroauthrequest
            '''
            result = self._values.get("connector_o_auth_request")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty"]], result)

        @builtins.property
        def refresh_token(self) -> typing.Optional[builtins.str]:
            '''The credentials used to acquire new access tokens.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-pardotconnectorprofilecredentials.html#cfn-appflow-connectorprofile-pardotconnectorprofilecredentials-refreshtoken
            '''
            result = self._values.get("refresh_token")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PardotConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorProfilePropsMixin.PardotConnectorProfilePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "business_unit_id": "businessUnitId",
            "instance_url": "instanceUrl",
            "is_sandbox_environment": "isSandboxEnvironment",
        },
    )
    class PardotConnectorProfilePropertiesProperty:
        def __init__(
            self,
            *,
            business_unit_id: typing.Optional[builtins.str] = None,
            instance_url: typing.Optional[builtins.str] = None,
            is_sandbox_environment: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The connector-specific profile properties required when using Salesforce Pardot.

            :param business_unit_id: The business unit id of Salesforce Pardot instance.
            :param instance_url: The location of the Salesforce Pardot resource.
            :param is_sandbox_environment: Indicates whether the connector profile applies to a sandbox or production environment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-pardotconnectorprofileproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                pardot_connector_profile_properties_property = appflow_mixins.CfnConnectorProfilePropsMixin.PardotConnectorProfilePropertiesProperty(
                    business_unit_id="businessUnitId",
                    instance_url="instanceUrl",
                    is_sandbox_environment=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__244e28bb4c3ab8d346e4a2b89a2e910f29f0f2b058b682e9d9a2f973513cb2b4)
                check_type(argname="argument business_unit_id", value=business_unit_id, expected_type=type_hints["business_unit_id"])
                check_type(argname="argument instance_url", value=instance_url, expected_type=type_hints["instance_url"])
                check_type(argname="argument is_sandbox_environment", value=is_sandbox_environment, expected_type=type_hints["is_sandbox_environment"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if business_unit_id is not None:
                self._values["business_unit_id"] = business_unit_id
            if instance_url is not None:
                self._values["instance_url"] = instance_url
            if is_sandbox_environment is not None:
                self._values["is_sandbox_environment"] = is_sandbox_environment

        @builtins.property
        def business_unit_id(self) -> typing.Optional[builtins.str]:
            '''The business unit id of Salesforce Pardot instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-pardotconnectorprofileproperties.html#cfn-appflow-connectorprofile-pardotconnectorprofileproperties-businessunitid
            '''
            result = self._values.get("business_unit_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def instance_url(self) -> typing.Optional[builtins.str]:
            '''The location of the Salesforce Pardot resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-pardotconnectorprofileproperties.html#cfn-appflow-connectorprofile-pardotconnectorprofileproperties-instanceurl
            '''
            result = self._values.get("instance_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def is_sandbox_environment(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether the connector profile applies to a sandbox or production environment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-pardotconnectorprofileproperties.html#cfn-appflow-connectorprofile-pardotconnectorprofileproperties-issandboxenvironment
            '''
            result = self._values.get("is_sandbox_environment")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PardotConnectorProfilePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorProfilePropsMixin.RedshiftConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={"password": "password", "username": "username"},
    )
    class RedshiftConnectorProfileCredentialsProperty:
        def __init__(
            self,
            *,
            password: typing.Optional[builtins.str] = None,
            username: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The connector-specific profile credentials required when using Amazon Redshift.

            :param password: The password that corresponds to the user name.
            :param username: The name of the user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-redshiftconnectorprofilecredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                redshift_connector_profile_credentials_property = appflow_mixins.CfnConnectorProfilePropsMixin.RedshiftConnectorProfileCredentialsProperty(
                    password="password",
                    username="username"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f9bd0499091e4eab819322ba94275493ec3e9de5d24965fe5e40758ac0fda6ee)
                check_type(argname="argument password", value=password, expected_type=type_hints["password"])
                check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if password is not None:
                self._values["password"] = password
            if username is not None:
                self._values["username"] = username

        @builtins.property
        def password(self) -> typing.Optional[builtins.str]:
            '''The password that corresponds to the user name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-redshiftconnectorprofilecredentials.html#cfn-appflow-connectorprofile-redshiftconnectorprofilecredentials-password
            '''
            result = self._values.get("password")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def username(self) -> typing.Optional[builtins.str]:
            '''The name of the user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-redshiftconnectorprofilecredentials.html#cfn-appflow-connectorprofile-redshiftconnectorprofilecredentials-username
            '''
            result = self._values.get("username")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RedshiftConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorProfilePropsMixin.RedshiftConnectorProfilePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_name": "bucketName",
            "bucket_prefix": "bucketPrefix",
            "cluster_identifier": "clusterIdentifier",
            "data_api_role_arn": "dataApiRoleArn",
            "database_name": "databaseName",
            "database_url": "databaseUrl",
            "is_redshift_serverless": "isRedshiftServerless",
            "role_arn": "roleArn",
            "workgroup_name": "workgroupName",
        },
    )
    class RedshiftConnectorProfilePropertiesProperty:
        def __init__(
            self,
            *,
            bucket_name: typing.Optional[builtins.str] = None,
            bucket_prefix: typing.Optional[builtins.str] = None,
            cluster_identifier: typing.Optional[builtins.str] = None,
            data_api_role_arn: typing.Optional[builtins.str] = None,
            database_name: typing.Optional[builtins.str] = None,
            database_url: typing.Optional[builtins.str] = None,
            is_redshift_serverless: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            role_arn: typing.Optional[builtins.str] = None,
            workgroup_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The connector-specific profile properties when using Amazon Redshift.

            :param bucket_name: A name for the associated Amazon S3 bucket.
            :param bucket_prefix: The object key for the destination bucket in which Amazon AppFlow places the files.
            :param cluster_identifier: The unique ID that's assigned to an Amazon Redshift cluster.
            :param data_api_role_arn: The Amazon Resource Name (ARN) of an IAM role that permits Amazon AppFlow to access your Amazon Redshift database through the Data API. For more information, and for the polices that you attach to this role, see `Allow Amazon AppFlow to access Amazon Redshift databases with the Data API <https://docs.aws.amazon.com/appflow/latest/userguide/security_iam_service-role-policies.html#access-redshift>`_ .
            :param database_name: The name of an Amazon Redshift database.
            :param database_url: The JDBC URL of the Amazon Redshift cluster.
            :param is_redshift_serverless: Indicates whether the connector profile defines a connection to an Amazon Redshift Serverless data warehouse.
            :param role_arn: The Amazon Resource Name (ARN) of IAM role that grants Amazon Redshift read-only access to Amazon S3. For more information, and for the polices that you attach to this role, see `Allow Amazon Redshift to access your Amazon AppFlow data in Amazon S3 <https://docs.aws.amazon.com/appflow/latest/userguide/security_iam_service-role-policies.html#redshift-access-s3>`_ .
            :param workgroup_name: The name of an Amazon Redshift workgroup.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-redshiftconnectorprofileproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                redshift_connector_profile_properties_property = appflow_mixins.CfnConnectorProfilePropsMixin.RedshiftConnectorProfilePropertiesProperty(
                    bucket_name="bucketName",
                    bucket_prefix="bucketPrefix",
                    cluster_identifier="clusterIdentifier",
                    data_api_role_arn="dataApiRoleArn",
                    database_name="databaseName",
                    database_url="databaseUrl",
                    is_redshift_serverless=False,
                    role_arn="roleArn",
                    workgroup_name="workgroupName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c58a7acd58839763a5646d7e0d03fdab26dd6b160a71e6c16ea85323e6ebec8b)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
                check_type(argname="argument cluster_identifier", value=cluster_identifier, expected_type=type_hints["cluster_identifier"])
                check_type(argname="argument data_api_role_arn", value=data_api_role_arn, expected_type=type_hints["data_api_role_arn"])
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument database_url", value=database_url, expected_type=type_hints["database_url"])
                check_type(argname="argument is_redshift_serverless", value=is_redshift_serverless, expected_type=type_hints["is_redshift_serverless"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument workgroup_name", value=workgroup_name, expected_type=type_hints["workgroup_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_name is not None:
                self._values["bucket_name"] = bucket_name
            if bucket_prefix is not None:
                self._values["bucket_prefix"] = bucket_prefix
            if cluster_identifier is not None:
                self._values["cluster_identifier"] = cluster_identifier
            if data_api_role_arn is not None:
                self._values["data_api_role_arn"] = data_api_role_arn
            if database_name is not None:
                self._values["database_name"] = database_name
            if database_url is not None:
                self._values["database_url"] = database_url
            if is_redshift_serverless is not None:
                self._values["is_redshift_serverless"] = is_redshift_serverless
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if workgroup_name is not None:
                self._values["workgroup_name"] = workgroup_name

        @builtins.property
        def bucket_name(self) -> typing.Optional[builtins.str]:
            '''A name for the associated Amazon S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-redshiftconnectorprofileproperties.html#cfn-appflow-connectorprofile-redshiftconnectorprofileproperties-bucketname
            '''
            result = self._values.get("bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bucket_prefix(self) -> typing.Optional[builtins.str]:
            '''The object key for the destination bucket in which Amazon AppFlow places the files.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-redshiftconnectorprofileproperties.html#cfn-appflow-connectorprofile-redshiftconnectorprofileproperties-bucketprefix
            '''
            result = self._values.get("bucket_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def cluster_identifier(self) -> typing.Optional[builtins.str]:
            '''The unique ID that's assigned to an Amazon Redshift cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-redshiftconnectorprofileproperties.html#cfn-appflow-connectorprofile-redshiftconnectorprofileproperties-clusteridentifier
            '''
            result = self._values.get("cluster_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def data_api_role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of an IAM role that permits Amazon AppFlow to access your Amazon Redshift database through the Data API.

            For more information, and for the polices that you attach to this role, see `Allow Amazon AppFlow to access Amazon Redshift databases with the Data API <https://docs.aws.amazon.com/appflow/latest/userguide/security_iam_service-role-policies.html#access-redshift>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-redshiftconnectorprofileproperties.html#cfn-appflow-connectorprofile-redshiftconnectorprofileproperties-dataapirolearn
            '''
            result = self._values.get("data_api_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            '''The name of an Amazon Redshift database.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-redshiftconnectorprofileproperties.html#cfn-appflow-connectorprofile-redshiftconnectorprofileproperties-databasename
            '''
            result = self._values.get("database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def database_url(self) -> typing.Optional[builtins.str]:
            '''The JDBC URL of the Amazon Redshift cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-redshiftconnectorprofileproperties.html#cfn-appflow-connectorprofile-redshiftconnectorprofileproperties-databaseurl
            '''
            result = self._values.get("database_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def is_redshift_serverless(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether the connector profile defines a connection to an Amazon Redshift Serverless data warehouse.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-redshiftconnectorprofileproperties.html#cfn-appflow-connectorprofile-redshiftconnectorprofileproperties-isredshiftserverless
            '''
            result = self._values.get("is_redshift_serverless")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of IAM role that grants Amazon Redshift read-only access to Amazon S3.

            For more information, and for the polices that you attach to this role, see `Allow Amazon Redshift to access your Amazon AppFlow data in Amazon S3 <https://docs.aws.amazon.com/appflow/latest/userguide/security_iam_service-role-policies.html#redshift-access-s3>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-redshiftconnectorprofileproperties.html#cfn-appflow-connectorprofile-redshiftconnectorprofileproperties-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def workgroup_name(self) -> typing.Optional[builtins.str]:
            '''The name of an Amazon Redshift workgroup.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-redshiftconnectorprofileproperties.html#cfn-appflow-connectorprofile-redshiftconnectorprofileproperties-workgroupname
            '''
            result = self._values.get("workgroup_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RedshiftConnectorProfilePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorProfilePropsMixin.SAPODataConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "basic_auth_credentials": "basicAuthCredentials",
            "o_auth_credentials": "oAuthCredentials",
        },
    )
    class SAPODataConnectorProfileCredentialsProperty:
        def __init__(
            self,
            *,
            basic_auth_credentials: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.BasicAuthCredentialsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            o_auth_credentials: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.OAuthCredentialsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The connector-specific profile credentials required when using SAPOData.

            :param basic_auth_credentials: The SAPOData basic authentication credentials.
            :param o_auth_credentials: The SAPOData OAuth type authentication credentials.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-sapodataconnectorprofilecredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                s_aPOData_connector_profile_credentials_property = appflow_mixins.CfnConnectorProfilePropsMixin.SAPODataConnectorProfileCredentialsProperty(
                    basic_auth_credentials=appflow_mixins.CfnConnectorProfilePropsMixin.BasicAuthCredentialsProperty(
                        password="password",
                        username="username"
                    ),
                    o_auth_credentials=appflow_mixins.CfnConnectorProfilePropsMixin.OAuthCredentialsProperty(
                        access_token="accessToken",
                        client_id="clientId",
                        client_secret="clientSecret",
                        connector_oAuth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                            auth_code="authCode",
                            redirect_uri="redirectUri"
                        ),
                        refresh_token="refreshToken"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__052b03410cd136f1f606593889ec16dcbd19f3ae470efe383e9ed2c1c3907c45)
                check_type(argname="argument basic_auth_credentials", value=basic_auth_credentials, expected_type=type_hints["basic_auth_credentials"])
                check_type(argname="argument o_auth_credentials", value=o_auth_credentials, expected_type=type_hints["o_auth_credentials"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if basic_auth_credentials is not None:
                self._values["basic_auth_credentials"] = basic_auth_credentials
            if o_auth_credentials is not None:
                self._values["o_auth_credentials"] = o_auth_credentials

        @builtins.property
        def basic_auth_credentials(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.BasicAuthCredentialsProperty"]]:
            '''The SAPOData basic authentication credentials.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-sapodataconnectorprofilecredentials.html#cfn-appflow-connectorprofile-sapodataconnectorprofilecredentials-basicauthcredentials
            '''
            result = self._values.get("basic_auth_credentials")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.BasicAuthCredentialsProperty"]], result)

        @builtins.property
        def o_auth_credentials(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.OAuthCredentialsProperty"]]:
            '''The SAPOData OAuth type authentication credentials.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-sapodataconnectorprofilecredentials.html#cfn-appflow-connectorprofile-sapodataconnectorprofilecredentials-oauthcredentials
            '''
            result = self._values.get("o_auth_credentials")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.OAuthCredentialsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SAPODataConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorProfilePropsMixin.SAPODataConnectorProfilePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "application_host_url": "applicationHostUrl",
            "application_service_path": "applicationServicePath",
            "client_number": "clientNumber",
            "disable_sso": "disableSso",
            "logon_language": "logonLanguage",
            "o_auth_properties": "oAuthProperties",
            "port_number": "portNumber",
            "private_link_service_name": "privateLinkServiceName",
        },
    )
    class SAPODataConnectorProfilePropertiesProperty:
        def __init__(
            self,
            *,
            application_host_url: typing.Optional[builtins.str] = None,
            application_service_path: typing.Optional[builtins.str] = None,
            client_number: typing.Optional[builtins.str] = None,
            disable_sso: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            logon_language: typing.Optional[builtins.str] = None,
            o_auth_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.OAuthPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            port_number: typing.Optional[jsii.Number] = None,
            private_link_service_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The connector-specific profile properties required when using SAPOData.

            :param application_host_url: The location of the SAPOData resource.
            :param application_service_path: The application path to catalog service.
            :param client_number: The client number for the client creating the connection.
            :param disable_sso: If you set this parameter to ``true`` , Amazon AppFlow bypasses the single sign-on (SSO) settings in your SAP account when it accesses your SAP OData instance. Whether you need this option depends on the types of credentials that you applied to your SAP OData connection profile. If your profile uses basic authentication credentials, SAP SSO can prevent Amazon AppFlow from connecting to your account with your username and password. In this case, bypassing SSO makes it possible for Amazon AppFlow to connect successfully. However, if your profile uses OAuth credentials, this parameter has no affect.
            :param logon_language: The logon language of SAPOData instance.
            :param o_auth_properties: The SAPOData OAuth properties required for OAuth type authentication.
            :param port_number: The port number of the SAPOData instance.
            :param private_link_service_name: The SAPOData Private Link service name to be used for private data transfers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-sapodataconnectorprofileproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                s_aPOData_connector_profile_properties_property = appflow_mixins.CfnConnectorProfilePropsMixin.SAPODataConnectorProfilePropertiesProperty(
                    application_host_url="applicationHostUrl",
                    application_service_path="applicationServicePath",
                    client_number="clientNumber",
                    disable_sso=False,
                    logon_language="logonLanguage",
                    o_auth_properties=appflow_mixins.CfnConnectorProfilePropsMixin.OAuthPropertiesProperty(
                        auth_code_url="authCodeUrl",
                        o_auth_scopes=["oAuthScopes"],
                        token_url="tokenUrl"
                    ),
                    port_number=123,
                    private_link_service_name="privateLinkServiceName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e5b3de1976e617be5326b07f40b3bfb1b693d8305472338cfefd20a21e6973bc)
                check_type(argname="argument application_host_url", value=application_host_url, expected_type=type_hints["application_host_url"])
                check_type(argname="argument application_service_path", value=application_service_path, expected_type=type_hints["application_service_path"])
                check_type(argname="argument client_number", value=client_number, expected_type=type_hints["client_number"])
                check_type(argname="argument disable_sso", value=disable_sso, expected_type=type_hints["disable_sso"])
                check_type(argname="argument logon_language", value=logon_language, expected_type=type_hints["logon_language"])
                check_type(argname="argument o_auth_properties", value=o_auth_properties, expected_type=type_hints["o_auth_properties"])
                check_type(argname="argument port_number", value=port_number, expected_type=type_hints["port_number"])
                check_type(argname="argument private_link_service_name", value=private_link_service_name, expected_type=type_hints["private_link_service_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if application_host_url is not None:
                self._values["application_host_url"] = application_host_url
            if application_service_path is not None:
                self._values["application_service_path"] = application_service_path
            if client_number is not None:
                self._values["client_number"] = client_number
            if disable_sso is not None:
                self._values["disable_sso"] = disable_sso
            if logon_language is not None:
                self._values["logon_language"] = logon_language
            if o_auth_properties is not None:
                self._values["o_auth_properties"] = o_auth_properties
            if port_number is not None:
                self._values["port_number"] = port_number
            if private_link_service_name is not None:
                self._values["private_link_service_name"] = private_link_service_name

        @builtins.property
        def application_host_url(self) -> typing.Optional[builtins.str]:
            '''The location of the SAPOData resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-sapodataconnectorprofileproperties.html#cfn-appflow-connectorprofile-sapodataconnectorprofileproperties-applicationhosturl
            '''
            result = self._values.get("application_host_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def application_service_path(self) -> typing.Optional[builtins.str]:
            '''The application path to catalog service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-sapodataconnectorprofileproperties.html#cfn-appflow-connectorprofile-sapodataconnectorprofileproperties-applicationservicepath
            '''
            result = self._values.get("application_service_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def client_number(self) -> typing.Optional[builtins.str]:
            '''The client number for the client creating the connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-sapodataconnectorprofileproperties.html#cfn-appflow-connectorprofile-sapodataconnectorprofileproperties-clientnumber
            '''
            result = self._values.get("client_number")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def disable_sso(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If you set this parameter to ``true`` , Amazon AppFlow bypasses the single sign-on (SSO) settings in your SAP account when it accesses your SAP OData instance.

            Whether you need this option depends on the types of credentials that you applied to your SAP OData connection profile. If your profile uses basic authentication credentials, SAP SSO can prevent Amazon AppFlow from connecting to your account with your username and password. In this case, bypassing SSO makes it possible for Amazon AppFlow to connect successfully. However, if your profile uses OAuth credentials, this parameter has no affect.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-sapodataconnectorprofileproperties.html#cfn-appflow-connectorprofile-sapodataconnectorprofileproperties-disablesso
            '''
            result = self._values.get("disable_sso")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def logon_language(self) -> typing.Optional[builtins.str]:
            '''The logon language of SAPOData instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-sapodataconnectorprofileproperties.html#cfn-appflow-connectorprofile-sapodataconnectorprofileproperties-logonlanguage
            '''
            result = self._values.get("logon_language")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def o_auth_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.OAuthPropertiesProperty"]]:
            '''The SAPOData OAuth properties required for OAuth type authentication.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-sapodataconnectorprofileproperties.html#cfn-appflow-connectorprofile-sapodataconnectorprofileproperties-oauthproperties
            '''
            result = self._values.get("o_auth_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.OAuthPropertiesProperty"]], result)

        @builtins.property
        def port_number(self) -> typing.Optional[jsii.Number]:
            '''The port number of the SAPOData instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-sapodataconnectorprofileproperties.html#cfn-appflow-connectorprofile-sapodataconnectorprofileproperties-portnumber
            '''
            result = self._values.get("port_number")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def private_link_service_name(self) -> typing.Optional[builtins.str]:
            '''The SAPOData Private Link service name to be used for private data transfers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-sapodataconnectorprofileproperties.html#cfn-appflow-connectorprofile-sapodataconnectorprofileproperties-privatelinkservicename
            '''
            result = self._values.get("private_link_service_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SAPODataConnectorProfilePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorProfilePropsMixin.SalesforceConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_token": "accessToken",
            "client_credentials_arn": "clientCredentialsArn",
            "connector_o_auth_request": "connectorOAuthRequest",
            "jwt_token": "jwtToken",
            "o_auth2_grant_type": "oAuth2GrantType",
            "refresh_token": "refreshToken",
        },
    )
    class SalesforceConnectorProfileCredentialsProperty:
        def __init__(
            self,
            *,
            access_token: typing.Optional[builtins.str] = None,
            client_credentials_arn: typing.Optional[builtins.str] = None,
            connector_o_auth_request: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            jwt_token: typing.Optional[builtins.str] = None,
            o_auth2_grant_type: typing.Optional[builtins.str] = None,
            refresh_token: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The connector-specific profile credentials required when using Salesforce.

            :param access_token: The credentials used to access protected Salesforce resources.
            :param client_credentials_arn: The secret manager ARN, which contains the client ID and client secret of the connected app.
            :param connector_o_auth_request: Used by select connectors for which the OAuth workflow is supported, such as Salesforce, Google Analytics, Marketo, Zendesk, and Slack.
            :param jwt_token: A JSON web token (JWT) that authorizes Amazon AppFlow to access your Salesforce records.
            :param o_auth2_grant_type: Specifies the OAuth 2.0 grant type that Amazon AppFlow uses when it requests an access token from Salesforce. Amazon AppFlow requires an access token each time it attempts to access your Salesforce records. You can specify one of the following values: - **AUTHORIZATION_CODE** - Amazon AppFlow passes an authorization code when it requests the access token from Salesforce. Amazon AppFlow receives the authorization code from Salesforce after you log in to your Salesforce account and authorize Amazon AppFlow to access your records. - **JWT_BEARER** - Amazon AppFlow passes a JSON web token (JWT) when it requests the access token from Salesforce. You provide the JWT to Amazon AppFlow when you define the connection to your Salesforce account. When you use this grant type, you don't need to log in to your Salesforce account to authorize Amazon AppFlow to access your records. .. epigraph:: The CLIENT_CREDENTIALS value is not supported for Salesforce.
            :param refresh_token: The credentials used to acquire new access tokens.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-salesforceconnectorprofilecredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                salesforce_connector_profile_credentials_property = appflow_mixins.CfnConnectorProfilePropsMixin.SalesforceConnectorProfileCredentialsProperty(
                    access_token="accessToken",
                    client_credentials_arn="clientCredentialsArn",
                    connector_oAuth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                        auth_code="authCode",
                        redirect_uri="redirectUri"
                    ),
                    jwt_token="jwtToken",
                    o_auth2_grant_type="oAuth2GrantType",
                    refresh_token="refreshToken"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__438746ccf4f09ca419124f99f4ab4e1e7af61f6dd746c834f4807962667c1d34)
                check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
                check_type(argname="argument client_credentials_arn", value=client_credentials_arn, expected_type=type_hints["client_credentials_arn"])
                check_type(argname="argument connector_o_auth_request", value=connector_o_auth_request, expected_type=type_hints["connector_o_auth_request"])
                check_type(argname="argument jwt_token", value=jwt_token, expected_type=type_hints["jwt_token"])
                check_type(argname="argument o_auth2_grant_type", value=o_auth2_grant_type, expected_type=type_hints["o_auth2_grant_type"])
                check_type(argname="argument refresh_token", value=refresh_token, expected_type=type_hints["refresh_token"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_token is not None:
                self._values["access_token"] = access_token
            if client_credentials_arn is not None:
                self._values["client_credentials_arn"] = client_credentials_arn
            if connector_o_auth_request is not None:
                self._values["connector_o_auth_request"] = connector_o_auth_request
            if jwt_token is not None:
                self._values["jwt_token"] = jwt_token
            if o_auth2_grant_type is not None:
                self._values["o_auth2_grant_type"] = o_auth2_grant_type
            if refresh_token is not None:
                self._values["refresh_token"] = refresh_token

        @builtins.property
        def access_token(self) -> typing.Optional[builtins.str]:
            '''The credentials used to access protected Salesforce resources.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-salesforceconnectorprofilecredentials.html#cfn-appflow-connectorprofile-salesforceconnectorprofilecredentials-accesstoken
            '''
            result = self._values.get("access_token")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def client_credentials_arn(self) -> typing.Optional[builtins.str]:
            '''The secret manager ARN, which contains the client ID and client secret of the connected app.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-salesforceconnectorprofilecredentials.html#cfn-appflow-connectorprofile-salesforceconnectorprofilecredentials-clientcredentialsarn
            '''
            result = self._values.get("client_credentials_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def connector_o_auth_request(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty"]]:
            '''Used by select connectors for which the OAuth workflow is supported, such as Salesforce, Google Analytics, Marketo, Zendesk, and Slack.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-salesforceconnectorprofilecredentials.html#cfn-appflow-connectorprofile-salesforceconnectorprofilecredentials-connectoroauthrequest
            '''
            result = self._values.get("connector_o_auth_request")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty"]], result)

        @builtins.property
        def jwt_token(self) -> typing.Optional[builtins.str]:
            '''A JSON web token (JWT) that authorizes Amazon AppFlow to access your Salesforce records.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-salesforceconnectorprofilecredentials.html#cfn-appflow-connectorprofile-salesforceconnectorprofilecredentials-jwttoken
            '''
            result = self._values.get("jwt_token")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def o_auth2_grant_type(self) -> typing.Optional[builtins.str]:
            '''Specifies the OAuth 2.0 grant type that Amazon AppFlow uses when it requests an access token from Salesforce. Amazon AppFlow requires an access token each time it attempts to access your Salesforce records.

            You can specify one of the following values:

            - **AUTHORIZATION_CODE** - Amazon AppFlow passes an authorization code when it requests the access token from Salesforce. Amazon AppFlow receives the authorization code from Salesforce after you log in to your Salesforce account and authorize Amazon AppFlow to access your records.
            - **JWT_BEARER** - Amazon AppFlow passes a JSON web token (JWT) when it requests the access token from Salesforce. You provide the JWT to Amazon AppFlow when you define the connection to your Salesforce account. When you use this grant type, you don't need to log in to your Salesforce account to authorize Amazon AppFlow to access your records.

            .. epigraph::

               The CLIENT_CREDENTIALS value is not supported for Salesforce.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-salesforceconnectorprofilecredentials.html#cfn-appflow-connectorprofile-salesforceconnectorprofilecredentials-oauth2granttype
            '''
            result = self._values.get("o_auth2_grant_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def refresh_token(self) -> typing.Optional[builtins.str]:
            '''The credentials used to acquire new access tokens.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-salesforceconnectorprofilecredentials.html#cfn-appflow-connectorprofile-salesforceconnectorprofilecredentials-refreshtoken
            '''
            result = self._values.get("refresh_token")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SalesforceConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorProfilePropsMixin.SalesforceConnectorProfilePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "instance_url": "instanceUrl",
            "is_sandbox_environment": "isSandboxEnvironment",
            "use_private_link_for_metadata_and_authorization": "usePrivateLinkForMetadataAndAuthorization",
        },
    )
    class SalesforceConnectorProfilePropertiesProperty:
        def __init__(
            self,
            *,
            instance_url: typing.Optional[builtins.str] = None,
            is_sandbox_environment: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            use_private_link_for_metadata_and_authorization: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The connector-specific profile properties required when using Salesforce.

            :param instance_url: The location of the Salesforce resource.
            :param is_sandbox_environment: Indicates whether the connector profile applies to a sandbox or production environment.
            :param use_private_link_for_metadata_and_authorization: If the connection mode for the connector profile is private, this parameter sets whether Amazon AppFlow uses the private network to send metadata and authorization calls to Salesforce. Amazon AppFlow sends private calls through AWS PrivateLink . These calls travel through AWS infrastructure without being exposed to the public internet. Set either of the following values: - **true** - Amazon AppFlow sends all calls to Salesforce over the private network. These private calls are: - Calls to get metadata about your Salesforce records. This metadata describes your Salesforce objects and their fields. - Calls to get or refresh access tokens that allow Amazon AppFlow to access your Salesforce records. - Calls to transfer your Salesforce records as part of a flow run. - **false** - The default value. Amazon AppFlow sends some calls to Salesforce privately and other calls over the public internet. The public calls are: - Calls to get metadata about your Salesforce records. - Calls to get or refresh access tokens. The private calls are: - Calls to transfer your Salesforce records as part of a flow run.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-salesforceconnectorprofileproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                salesforce_connector_profile_properties_property = appflow_mixins.CfnConnectorProfilePropsMixin.SalesforceConnectorProfilePropertiesProperty(
                    instance_url="instanceUrl",
                    is_sandbox_environment=False,
                    use_private_link_for_metadata_and_authorization=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__440877404d04efb4be2b66706d9261862060211e67575ce1e7b3e70f8136a65e)
                check_type(argname="argument instance_url", value=instance_url, expected_type=type_hints["instance_url"])
                check_type(argname="argument is_sandbox_environment", value=is_sandbox_environment, expected_type=type_hints["is_sandbox_environment"])
                check_type(argname="argument use_private_link_for_metadata_and_authorization", value=use_private_link_for_metadata_and_authorization, expected_type=type_hints["use_private_link_for_metadata_and_authorization"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if instance_url is not None:
                self._values["instance_url"] = instance_url
            if is_sandbox_environment is not None:
                self._values["is_sandbox_environment"] = is_sandbox_environment
            if use_private_link_for_metadata_and_authorization is not None:
                self._values["use_private_link_for_metadata_and_authorization"] = use_private_link_for_metadata_and_authorization

        @builtins.property
        def instance_url(self) -> typing.Optional[builtins.str]:
            '''The location of the Salesforce resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-salesforceconnectorprofileproperties.html#cfn-appflow-connectorprofile-salesforceconnectorprofileproperties-instanceurl
            '''
            result = self._values.get("instance_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def is_sandbox_environment(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether the connector profile applies to a sandbox or production environment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-salesforceconnectorprofileproperties.html#cfn-appflow-connectorprofile-salesforceconnectorprofileproperties-issandboxenvironment
            '''
            result = self._values.get("is_sandbox_environment")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def use_private_link_for_metadata_and_authorization(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If the connection mode for the connector profile is private, this parameter sets whether Amazon AppFlow uses the private network to send metadata and authorization calls to Salesforce.

            Amazon AppFlow sends private calls through AWS PrivateLink . These calls travel through AWS infrastructure without being exposed to the public internet.

            Set either of the following values:

            - **true** - Amazon AppFlow sends all calls to Salesforce over the private network.

            These private calls are:

            - Calls to get metadata about your Salesforce records. This metadata describes your Salesforce objects and their fields.
            - Calls to get or refresh access tokens that allow Amazon AppFlow to access your Salesforce records.
            - Calls to transfer your Salesforce records as part of a flow run.
            - **false** - The default value. Amazon AppFlow sends some calls to Salesforce privately and other calls over the public internet.

            The public calls are:

            - Calls to get metadata about your Salesforce records.
            - Calls to get or refresh access tokens.

            The private calls are:

            - Calls to transfer your Salesforce records as part of a flow run.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-salesforceconnectorprofileproperties.html#cfn-appflow-connectorprofile-salesforceconnectorprofileproperties-useprivatelinkformetadataandauthorization
            '''
            result = self._values.get("use_private_link_for_metadata_and_authorization")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SalesforceConnectorProfilePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorProfilePropsMixin.ServiceNowConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "o_auth2_credentials": "oAuth2Credentials",
            "password": "password",
            "username": "username",
        },
    )
    class ServiceNowConnectorProfileCredentialsProperty:
        def __init__(
            self,
            *,
            o_auth2_credentials: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.OAuth2CredentialsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            password: typing.Optional[builtins.str] = None,
            username: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The connector-specific profile credentials required when using ServiceNow.

            :param o_auth2_credentials: The OAuth 2.0 credentials required to authenticate the user.
            :param password: The password that corresponds to the user name.
            :param username: The name of the user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-servicenowconnectorprofilecredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                service_now_connector_profile_credentials_property = appflow_mixins.CfnConnectorProfilePropsMixin.ServiceNowConnectorProfileCredentialsProperty(
                    o_auth2_credentials=appflow_mixins.CfnConnectorProfilePropsMixin.OAuth2CredentialsProperty(
                        access_token="accessToken",
                        client_id="clientId",
                        client_secret="clientSecret",
                        o_auth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                            auth_code="authCode",
                            redirect_uri="redirectUri"
                        ),
                        refresh_token="refreshToken"
                    ),
                    password="password",
                    username="username"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a6c84c861fe401a42808f31b97bc4bd11a01004c4115f3f2fc4eddafc000fd1e)
                check_type(argname="argument o_auth2_credentials", value=o_auth2_credentials, expected_type=type_hints["o_auth2_credentials"])
                check_type(argname="argument password", value=password, expected_type=type_hints["password"])
                check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if o_auth2_credentials is not None:
                self._values["o_auth2_credentials"] = o_auth2_credentials
            if password is not None:
                self._values["password"] = password
            if username is not None:
                self._values["username"] = username

        @builtins.property
        def o_auth2_credentials(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.OAuth2CredentialsProperty"]]:
            '''The OAuth 2.0 credentials required to authenticate the user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-servicenowconnectorprofilecredentials.html#cfn-appflow-connectorprofile-servicenowconnectorprofilecredentials-oauth2credentials
            '''
            result = self._values.get("o_auth2_credentials")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.OAuth2CredentialsProperty"]], result)

        @builtins.property
        def password(self) -> typing.Optional[builtins.str]:
            '''The password that corresponds to the user name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-servicenowconnectorprofilecredentials.html#cfn-appflow-connectorprofile-servicenowconnectorprofilecredentials-password
            '''
            result = self._values.get("password")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def username(self) -> typing.Optional[builtins.str]:
            '''The name of the user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-servicenowconnectorprofilecredentials.html#cfn-appflow-connectorprofile-servicenowconnectorprofilecredentials-username
            '''
            result = self._values.get("username")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServiceNowConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorProfilePropsMixin.ServiceNowConnectorProfilePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"instance_url": "instanceUrl"},
    )
    class ServiceNowConnectorProfilePropertiesProperty:
        def __init__(
            self,
            *,
            instance_url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The connector-specific profile properties required when using ServiceNow.

            :param instance_url: The location of the ServiceNow resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-servicenowconnectorprofileproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                service_now_connector_profile_properties_property = appflow_mixins.CfnConnectorProfilePropsMixin.ServiceNowConnectorProfilePropertiesProperty(
                    instance_url="instanceUrl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c63dc2bbf0186db6fea27f0466fbf9b29f75f34608c0b81be3c27f8a01b05c94)
                check_type(argname="argument instance_url", value=instance_url, expected_type=type_hints["instance_url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if instance_url is not None:
                self._values["instance_url"] = instance_url

        @builtins.property
        def instance_url(self) -> typing.Optional[builtins.str]:
            '''The location of the ServiceNow resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-servicenowconnectorprofileproperties.html#cfn-appflow-connectorprofile-servicenowconnectorprofileproperties-instanceurl
            '''
            result = self._values.get("instance_url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServiceNowConnectorProfilePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorProfilePropsMixin.SingularConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={"api_key": "apiKey"},
    )
    class SingularConnectorProfileCredentialsProperty:
        def __init__(self, *, api_key: typing.Optional[builtins.str] = None) -> None:
            '''The connector-specific profile credentials required when using Singular.

            :param api_key: A unique alphanumeric identifier used to authenticate a user, developer, or calling program to your API.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-singularconnectorprofilecredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                singular_connector_profile_credentials_property = appflow_mixins.CfnConnectorProfilePropsMixin.SingularConnectorProfileCredentialsProperty(
                    api_key="apiKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ea7cfda8cd1042a1f9d054ee09932b1c35d066a6be8dc4582c94b368c5f2e035)
                check_type(argname="argument api_key", value=api_key, expected_type=type_hints["api_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if api_key is not None:
                self._values["api_key"] = api_key

        @builtins.property
        def api_key(self) -> typing.Optional[builtins.str]:
            '''A unique alphanumeric identifier used to authenticate a user, developer, or calling program to your API.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-singularconnectorprofilecredentials.html#cfn-appflow-connectorprofile-singularconnectorprofilecredentials-apikey
            '''
            result = self._values.get("api_key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SingularConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorProfilePropsMixin.SlackConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_token": "accessToken",
            "client_id": "clientId",
            "client_secret": "clientSecret",
            "connector_o_auth_request": "connectorOAuthRequest",
        },
    )
    class SlackConnectorProfileCredentialsProperty:
        def __init__(
            self,
            *,
            access_token: typing.Optional[builtins.str] = None,
            client_id: typing.Optional[builtins.str] = None,
            client_secret: typing.Optional[builtins.str] = None,
            connector_o_auth_request: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The connector-specific profile credentials required when using Slack.

            :param access_token: The credentials used to access protected Slack resources.
            :param client_id: The identifier for the client.
            :param client_secret: The client secret used by the OAuth client to authenticate to the authorization server.
            :param connector_o_auth_request: Used by select connectors for which the OAuth workflow is supported, such as Salesforce, Google Analytics, Marketo, Zendesk, and Slack.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-slackconnectorprofilecredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                slack_connector_profile_credentials_property = appflow_mixins.CfnConnectorProfilePropsMixin.SlackConnectorProfileCredentialsProperty(
                    access_token="accessToken",
                    client_id="clientId",
                    client_secret="clientSecret",
                    connector_oAuth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                        auth_code="authCode",
                        redirect_uri="redirectUri"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d83fcfc7fef569f6264046286cba7b5a0d94ec800dd52611a81228c708c30560)
                check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
                check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
                check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
                check_type(argname="argument connector_o_auth_request", value=connector_o_auth_request, expected_type=type_hints["connector_o_auth_request"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_token is not None:
                self._values["access_token"] = access_token
            if client_id is not None:
                self._values["client_id"] = client_id
            if client_secret is not None:
                self._values["client_secret"] = client_secret
            if connector_o_auth_request is not None:
                self._values["connector_o_auth_request"] = connector_o_auth_request

        @builtins.property
        def access_token(self) -> typing.Optional[builtins.str]:
            '''The credentials used to access protected Slack resources.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-slackconnectorprofilecredentials.html#cfn-appflow-connectorprofile-slackconnectorprofilecredentials-accesstoken
            '''
            result = self._values.get("access_token")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def client_id(self) -> typing.Optional[builtins.str]:
            '''The identifier for the client.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-slackconnectorprofilecredentials.html#cfn-appflow-connectorprofile-slackconnectorprofilecredentials-clientid
            '''
            result = self._values.get("client_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def client_secret(self) -> typing.Optional[builtins.str]:
            '''The client secret used by the OAuth client to authenticate to the authorization server.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-slackconnectorprofilecredentials.html#cfn-appflow-connectorprofile-slackconnectorprofilecredentials-clientsecret
            '''
            result = self._values.get("client_secret")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def connector_o_auth_request(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty"]]:
            '''Used by select connectors for which the OAuth workflow is supported, such as Salesforce, Google Analytics, Marketo, Zendesk, and Slack.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-slackconnectorprofilecredentials.html#cfn-appflow-connectorprofile-slackconnectorprofilecredentials-connectoroauthrequest
            '''
            result = self._values.get("connector_o_auth_request")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlackConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorProfilePropsMixin.SlackConnectorProfilePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"instance_url": "instanceUrl"},
    )
    class SlackConnectorProfilePropertiesProperty:
        def __init__(
            self,
            *,
            instance_url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The connector-specific profile properties required when using Slack.

            :param instance_url: The location of the Slack resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-slackconnectorprofileproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                slack_connector_profile_properties_property = appflow_mixins.CfnConnectorProfilePropsMixin.SlackConnectorProfilePropertiesProperty(
                    instance_url="instanceUrl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b31b52814e341e3b85fc9f475f4911290ef6d6ce054afa2d7fc704894e551efd)
                check_type(argname="argument instance_url", value=instance_url, expected_type=type_hints["instance_url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if instance_url is not None:
                self._values["instance_url"] = instance_url

        @builtins.property
        def instance_url(self) -> typing.Optional[builtins.str]:
            '''The location of the Slack resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-slackconnectorprofileproperties.html#cfn-appflow-connectorprofile-slackconnectorprofileproperties-instanceurl
            '''
            result = self._values.get("instance_url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlackConnectorProfilePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorProfilePropsMixin.SnowflakeConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={"password": "password", "username": "username"},
    )
    class SnowflakeConnectorProfileCredentialsProperty:
        def __init__(
            self,
            *,
            password: typing.Optional[builtins.str] = None,
            username: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The connector-specific profile credentials required when using Snowflake.

            :param password: The password that corresponds to the user name.
            :param username: The name of the user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-snowflakeconnectorprofilecredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                snowflake_connector_profile_credentials_property = appflow_mixins.CfnConnectorProfilePropsMixin.SnowflakeConnectorProfileCredentialsProperty(
                    password="password",
                    username="username"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1c62add8b09d7bf74aabae4145968ec5794dcfb8adf028cfe0a073de79f5c977)
                check_type(argname="argument password", value=password, expected_type=type_hints["password"])
                check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if password is not None:
                self._values["password"] = password
            if username is not None:
                self._values["username"] = username

        @builtins.property
        def password(self) -> typing.Optional[builtins.str]:
            '''The password that corresponds to the user name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-snowflakeconnectorprofilecredentials.html#cfn-appflow-connectorprofile-snowflakeconnectorprofilecredentials-password
            '''
            result = self._values.get("password")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def username(self) -> typing.Optional[builtins.str]:
            '''The name of the user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-snowflakeconnectorprofilecredentials.html#cfn-appflow-connectorprofile-snowflakeconnectorprofilecredentials-username
            '''
            result = self._values.get("username")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SnowflakeConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorProfilePropsMixin.SnowflakeConnectorProfilePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "account_name": "accountName",
            "bucket_name": "bucketName",
            "bucket_prefix": "bucketPrefix",
            "private_link_service_name": "privateLinkServiceName",
            "region": "region",
            "stage": "stage",
            "warehouse": "warehouse",
        },
    )
    class SnowflakeConnectorProfilePropertiesProperty:
        def __init__(
            self,
            *,
            account_name: typing.Optional[builtins.str] = None,
            bucket_name: typing.Optional[builtins.str] = None,
            bucket_prefix: typing.Optional[builtins.str] = None,
            private_link_service_name: typing.Optional[builtins.str] = None,
            region: typing.Optional[builtins.str] = None,
            stage: typing.Optional[builtins.str] = None,
            warehouse: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The connector-specific profile properties required when using Snowflake.

            :param account_name: The name of the account.
            :param bucket_name: The name of the Amazon S3 bucket associated with Snowflake.
            :param bucket_prefix: The bucket path that refers to the Amazon S3 bucket associated with Snowflake.
            :param private_link_service_name: The Snowflake Private Link service name to be used for private data transfers.
            :param region: The AWS Region of the Snowflake account.
            :param stage: The name of the Amazon S3 stage that was created while setting up an Amazon S3 stage in the Snowflake account. This is written in the following format: < Database>< Schema>.
            :param warehouse: The name of the Snowflake warehouse.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-snowflakeconnectorprofileproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                snowflake_connector_profile_properties_property = appflow_mixins.CfnConnectorProfilePropsMixin.SnowflakeConnectorProfilePropertiesProperty(
                    account_name="accountName",
                    bucket_name="bucketName",
                    bucket_prefix="bucketPrefix",
                    private_link_service_name="privateLinkServiceName",
                    region="region",
                    stage="stage",
                    warehouse="warehouse"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__81a6d0c4e8947d2ba97151a274df03479c5e0a4e096a49337f7968396135b23b)
                check_type(argname="argument account_name", value=account_name, expected_type=type_hints["account_name"])
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
                check_type(argname="argument private_link_service_name", value=private_link_service_name, expected_type=type_hints["private_link_service_name"])
                check_type(argname="argument region", value=region, expected_type=type_hints["region"])
                check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
                check_type(argname="argument warehouse", value=warehouse, expected_type=type_hints["warehouse"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if account_name is not None:
                self._values["account_name"] = account_name
            if bucket_name is not None:
                self._values["bucket_name"] = bucket_name
            if bucket_prefix is not None:
                self._values["bucket_prefix"] = bucket_prefix
            if private_link_service_name is not None:
                self._values["private_link_service_name"] = private_link_service_name
            if region is not None:
                self._values["region"] = region
            if stage is not None:
                self._values["stage"] = stage
            if warehouse is not None:
                self._values["warehouse"] = warehouse

        @builtins.property
        def account_name(self) -> typing.Optional[builtins.str]:
            '''The name of the account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-snowflakeconnectorprofileproperties.html#cfn-appflow-connectorprofile-snowflakeconnectorprofileproperties-accountname
            '''
            result = self._values.get("account_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bucket_name(self) -> typing.Optional[builtins.str]:
            '''The name of the Amazon S3 bucket associated with Snowflake.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-snowflakeconnectorprofileproperties.html#cfn-appflow-connectorprofile-snowflakeconnectorprofileproperties-bucketname
            '''
            result = self._values.get("bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bucket_prefix(self) -> typing.Optional[builtins.str]:
            '''The bucket path that refers to the Amazon S3 bucket associated with Snowflake.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-snowflakeconnectorprofileproperties.html#cfn-appflow-connectorprofile-snowflakeconnectorprofileproperties-bucketprefix
            '''
            result = self._values.get("bucket_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def private_link_service_name(self) -> typing.Optional[builtins.str]:
            '''The Snowflake Private Link service name to be used for private data transfers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-snowflakeconnectorprofileproperties.html#cfn-appflow-connectorprofile-snowflakeconnectorprofileproperties-privatelinkservicename
            '''
            result = self._values.get("private_link_service_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def region(self) -> typing.Optional[builtins.str]:
            '''The AWS Region of the Snowflake account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-snowflakeconnectorprofileproperties.html#cfn-appflow-connectorprofile-snowflakeconnectorprofileproperties-region
            '''
            result = self._values.get("region")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def stage(self) -> typing.Optional[builtins.str]:
            '''The name of the Amazon S3 stage that was created while setting up an Amazon S3 stage in the Snowflake account.

            This is written in the following format: < Database>< Schema>.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-snowflakeconnectorprofileproperties.html#cfn-appflow-connectorprofile-snowflakeconnectorprofileproperties-stage
            '''
            result = self._values.get("stage")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def warehouse(self) -> typing.Optional[builtins.str]:
            '''The name of the Snowflake warehouse.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-snowflakeconnectorprofileproperties.html#cfn-appflow-connectorprofile-snowflakeconnectorprofileproperties-warehouse
            '''
            result = self._values.get("warehouse")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SnowflakeConnectorProfilePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorProfilePropsMixin.TrendmicroConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={"api_secret_key": "apiSecretKey"},
    )
    class TrendmicroConnectorProfileCredentialsProperty:
        def __init__(
            self,
            *,
            api_secret_key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The connector-specific profile credentials required when using Trend Micro.

            :param api_secret_key: The Secret Access Key portion of the credentials.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-trendmicroconnectorprofilecredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                trendmicro_connector_profile_credentials_property = appflow_mixins.CfnConnectorProfilePropsMixin.TrendmicroConnectorProfileCredentialsProperty(
                    api_secret_key="apiSecretKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6e9310323b51e30591843a82e9ef6bb548c957e7769d4874f99f125174b04bc0)
                check_type(argname="argument api_secret_key", value=api_secret_key, expected_type=type_hints["api_secret_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if api_secret_key is not None:
                self._values["api_secret_key"] = api_secret_key

        @builtins.property
        def api_secret_key(self) -> typing.Optional[builtins.str]:
            '''The Secret Access Key portion of the credentials.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-trendmicroconnectorprofilecredentials.html#cfn-appflow-connectorprofile-trendmicroconnectorprofilecredentials-apisecretkey
            '''
            result = self._values.get("api_secret_key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TrendmicroConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorProfilePropsMixin.VeevaConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={"password": "password", "username": "username"},
    )
    class VeevaConnectorProfileCredentialsProperty:
        def __init__(
            self,
            *,
            password: typing.Optional[builtins.str] = None,
            username: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The connector-specific profile credentials required when using Veeva.

            :param password: The password that corresponds to the user name.
            :param username: The name of the user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-veevaconnectorprofilecredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                veeva_connector_profile_credentials_property = appflow_mixins.CfnConnectorProfilePropsMixin.VeevaConnectorProfileCredentialsProperty(
                    password="password",
                    username="username"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f9e8f711433dc7612dd152670aeb3d6adfd2bb5a6787a42b189b0132a0938f80)
                check_type(argname="argument password", value=password, expected_type=type_hints["password"])
                check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if password is not None:
                self._values["password"] = password
            if username is not None:
                self._values["username"] = username

        @builtins.property
        def password(self) -> typing.Optional[builtins.str]:
            '''The password that corresponds to the user name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-veevaconnectorprofilecredentials.html#cfn-appflow-connectorprofile-veevaconnectorprofilecredentials-password
            '''
            result = self._values.get("password")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def username(self) -> typing.Optional[builtins.str]:
            '''The name of the user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-veevaconnectorprofilecredentials.html#cfn-appflow-connectorprofile-veevaconnectorprofilecredentials-username
            '''
            result = self._values.get("username")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VeevaConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorProfilePropsMixin.VeevaConnectorProfilePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"instance_url": "instanceUrl"},
    )
    class VeevaConnectorProfilePropertiesProperty:
        def __init__(
            self,
            *,
            instance_url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The connector-specific profile properties required when using Veeva.

            :param instance_url: The location of the Veeva resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-veevaconnectorprofileproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                veeva_connector_profile_properties_property = appflow_mixins.CfnConnectorProfilePropsMixin.VeevaConnectorProfilePropertiesProperty(
                    instance_url="instanceUrl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f98cafd94131004eb42183a84351b5405e23be6011cfe4fed0622d54515e9c03)
                check_type(argname="argument instance_url", value=instance_url, expected_type=type_hints["instance_url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if instance_url is not None:
                self._values["instance_url"] = instance_url

        @builtins.property
        def instance_url(self) -> typing.Optional[builtins.str]:
            '''The location of the Veeva resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-veevaconnectorprofileproperties.html#cfn-appflow-connectorprofile-veevaconnectorprofileproperties-instanceurl
            '''
            result = self._values.get("instance_url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VeevaConnectorProfilePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorProfilePropsMixin.ZendeskConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_token": "accessToken",
            "client_id": "clientId",
            "client_secret": "clientSecret",
            "connector_o_auth_request": "connectorOAuthRequest",
        },
    )
    class ZendeskConnectorProfileCredentialsProperty:
        def __init__(
            self,
            *,
            access_token: typing.Optional[builtins.str] = None,
            client_id: typing.Optional[builtins.str] = None,
            client_secret: typing.Optional[builtins.str] = None,
            connector_o_auth_request: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The connector-specific profile credentials required when using Zendesk.

            :param access_token: The credentials used to access protected Zendesk resources.
            :param client_id: The identifier for the desired client.
            :param client_secret: The client secret used by the OAuth client to authenticate to the authorization server.
            :param connector_o_auth_request: Used by select connectors for which the OAuth workflow is supported, such as Salesforce, Google Analytics, Marketo, Zendesk, and Slack.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-zendeskconnectorprofilecredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                zendesk_connector_profile_credentials_property = appflow_mixins.CfnConnectorProfilePropsMixin.ZendeskConnectorProfileCredentialsProperty(
                    access_token="accessToken",
                    client_id="clientId",
                    client_secret="clientSecret",
                    connector_oAuth_request=appflow_mixins.CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty(
                        auth_code="authCode",
                        redirect_uri="redirectUri"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__458961bcc0045f8bffad26ee111a8a44ca6ff260a85304aad38fc175632ecd24)
                check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
                check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
                check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
                check_type(argname="argument connector_o_auth_request", value=connector_o_auth_request, expected_type=type_hints["connector_o_auth_request"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_token is not None:
                self._values["access_token"] = access_token
            if client_id is not None:
                self._values["client_id"] = client_id
            if client_secret is not None:
                self._values["client_secret"] = client_secret
            if connector_o_auth_request is not None:
                self._values["connector_o_auth_request"] = connector_o_auth_request

        @builtins.property
        def access_token(self) -> typing.Optional[builtins.str]:
            '''The credentials used to access protected Zendesk resources.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-zendeskconnectorprofilecredentials.html#cfn-appflow-connectorprofile-zendeskconnectorprofilecredentials-accesstoken
            '''
            result = self._values.get("access_token")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def client_id(self) -> typing.Optional[builtins.str]:
            '''The identifier for the desired client.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-zendeskconnectorprofilecredentials.html#cfn-appflow-connectorprofile-zendeskconnectorprofilecredentials-clientid
            '''
            result = self._values.get("client_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def client_secret(self) -> typing.Optional[builtins.str]:
            '''The client secret used by the OAuth client to authenticate to the authorization server.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-zendeskconnectorprofilecredentials.html#cfn-appflow-connectorprofile-zendeskconnectorprofilecredentials-clientsecret
            '''
            result = self._values.get("client_secret")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def connector_o_auth_request(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty"]]:
            '''Used by select connectors for which the OAuth workflow is supported, such as Salesforce, Google Analytics, Marketo, Zendesk, and Slack.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-zendeskconnectorprofilecredentials.html#cfn-appflow-connectorprofile-zendeskconnectorprofilecredentials-connectoroauthrequest
            '''
            result = self._values.get("connector_o_auth_request")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ZendeskConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorProfilePropsMixin.ZendeskConnectorProfilePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"instance_url": "instanceUrl"},
    )
    class ZendeskConnectorProfilePropertiesProperty:
        def __init__(
            self,
            *,
            instance_url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The connector-specific profile properties required when using Zendesk.

            :param instance_url: The location of the Zendesk resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-zendeskconnectorprofileproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                zendesk_connector_profile_properties_property = appflow_mixins.CfnConnectorProfilePropsMixin.ZendeskConnectorProfilePropertiesProperty(
                    instance_url="instanceUrl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__118b4554c4e2cc23e2d61439d569cc5c1c86f40ce011bd330cf60a73d45f3ad8)
                check_type(argname="argument instance_url", value=instance_url, expected_type=type_hints["instance_url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if instance_url is not None:
                self._values["instance_url"] = instance_url

        @builtins.property
        def instance_url(self) -> typing.Optional[builtins.str]:
            '''The location of the Zendesk resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-zendeskconnectorprofileproperties.html#cfn-appflow-connectorprofile-zendeskconnectorprofileproperties-instanceurl
            '''
            result = self._values.get("instance_url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ZendeskConnectorProfilePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IMixin_11e4b965)
class CfnConnectorPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorPropsMixin",
):
    '''Creates a new connector profile associated with your AWS account .

    There is a soft quota of 100 connector profiles per AWS account . If you need more connector profiles than this quota allows, you can submit a request to the Amazon AppFlow team through the Amazon AppFlow support channel. In each connector profile that you create, you can provide the credentials and properties for only one connector.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connector.html
    :cloudformationResource: AWS::AppFlow::Connector
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
        
        cfn_connector_props_mixin = appflow_mixins.CfnConnectorPropsMixin(appflow_mixins.CfnConnectorMixinProps(
            connector_label="connectorLabel",
            connector_provisioning_config=appflow_mixins.CfnConnectorPropsMixin.ConnectorProvisioningConfigProperty(
                lambda_=appflow_mixins.CfnConnectorPropsMixin.LambdaConnectorProvisioningConfigProperty(
                    lambda_arn="lambdaArn"
                )
            ),
            connector_provisioning_type="connectorProvisioningType",
            description="description"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnConnectorMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AppFlow::Connector``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a72738a5c2ea1ea2ffff0d320882fa202b88ee18be11b0020ed82f3ada21f33b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__101624703bf09f5e755abdc24c0bad5fc52a24162f9dba6078ab333fb67706ca)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f75ceb787f3b7f6cc4752609f47c74f59875a54a40a7a91b1507ca745950500f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnConnectorMixinProps:
        return typing.cast(CfnConnectorMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorPropsMixin.ConnectorProvisioningConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"lambda_": "lambda"},
    )
    class ConnectorProvisioningConfigProperty:
        def __init__(
            self,
            *,
            lambda_: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorPropsMixin.LambdaConnectorProvisioningConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains information about the configuration of the connector being registered.

            :param lambda_: Contains information about the configuration of the lambda which is being registered as the connector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connector-connectorprovisioningconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                connector_provisioning_config_property = appflow_mixins.CfnConnectorPropsMixin.ConnectorProvisioningConfigProperty(
                    lambda_=appflow_mixins.CfnConnectorPropsMixin.LambdaConnectorProvisioningConfigProperty(
                        lambda_arn="lambdaArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bcf94d39bcdc77f9e2f060b1b7ff7d7500c3130a005f6f87f12e7906763ac4b8)
                check_type(argname="argument lambda_", value=lambda_, expected_type=type_hints["lambda_"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if lambda_ is not None:
                self._values["lambda_"] = lambda_

        @builtins.property
        def lambda_(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.LambdaConnectorProvisioningConfigProperty"]]:
            '''Contains information about the configuration of the lambda which is being registered as the connector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connector-connectorprovisioningconfig.html#cfn-appflow-connector-connectorprovisioningconfig-lambda
            '''
            result = self._values.get("lambda_")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.LambdaConnectorProvisioningConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectorProvisioningConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnConnectorPropsMixin.LambdaConnectorProvisioningConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"lambda_arn": "lambdaArn"},
    )
    class LambdaConnectorProvisioningConfigProperty:
        def __init__(self, *, lambda_arn: typing.Optional[builtins.str] = None) -> None:
            '''Contains information about the configuration of the lambda which is being registered as the connector.

            :param lambda_arn: Lambda ARN of the connector being registered.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connector-lambdaconnectorprovisioningconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                lambda_connector_provisioning_config_property = appflow_mixins.CfnConnectorPropsMixin.LambdaConnectorProvisioningConfigProperty(
                    lambda_arn="lambdaArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6681cf7a0a07d8c45015302bc81074ae1fbc7788225c55abbb984b2ed6199c6f)
                check_type(argname="argument lambda_arn", value=lambda_arn, expected_type=type_hints["lambda_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if lambda_arn is not None:
                self._values["lambda_arn"] = lambda_arn

        @builtins.property
        def lambda_arn(self) -> typing.Optional[builtins.str]:
            '''Lambda ARN of the connector being registered.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connector-lambdaconnectorprovisioningconfig.html#cfn-appflow-connector-lambdaconnectorprovisioningconfig-lambdaarn
            '''
            result = self._values.get("lambda_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaConnectorProvisioningConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "destination_flow_config_list": "destinationFlowConfigList",
        "flow_name": "flowName",
        "flow_status": "flowStatus",
        "kms_arn": "kmsArn",
        "metadata_catalog_config": "metadataCatalogConfig",
        "source_flow_config": "sourceFlowConfig",
        "tags": "tags",
        "tasks": "tasks",
        "trigger_config": "triggerConfig",
    },
)
class CfnFlowMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        destination_flow_config_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.DestinationFlowConfigProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        flow_name: typing.Optional[builtins.str] = None,
        flow_status: typing.Optional[builtins.str] = None,
        kms_arn: typing.Optional[builtins.str] = None,
        metadata_catalog_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.MetadataCatalogConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        source_flow_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.SourceFlowConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        tasks: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.TaskProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        trigger_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.TriggerConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnFlowPropsMixin.

        :param description: A user-entered description of the flow.
        :param destination_flow_config_list: The configuration that controls how Amazon AppFlow places data in the destination connector.
        :param flow_name: The specified name of the flow. Spaces are not allowed. Use underscores (_) or hyphens (-) only.
        :param flow_status: Sets the status of the flow. You can specify one of the following values:. - **Active** - The flow runs based on the trigger settings that you defined. Active scheduled flows run as scheduled, and active event-triggered flows run when the specified change event occurs. However, active on-demand flows run only when you manually start them by using Amazon AppFlow. - **Suspended** - You can use this option to deactivate an active flow. Scheduled and event-triggered flows will cease to run until you reactive them. This value only affects scheduled and event-triggered flows. It has no effect for on-demand flows. If you omit the FlowStatus parameter, Amazon AppFlow creates the flow with a default status. The default status for on-demand flows is Active. The default status for scheduled and event-triggered flows is Draft, which means they’re not yet active.
        :param kms_arn: The ARN (Amazon Resource Name) of the Key Management Service (KMS) key you provide for encryption. This is required if you do not want to use the Amazon AppFlow-managed KMS key. If you don't provide anything here, Amazon AppFlow uses the Amazon AppFlow-managed KMS key.
        :param metadata_catalog_config: Specifies the configuration that Amazon AppFlow uses when it catalogs your data. When Amazon AppFlow catalogs your data, it stores metadata in a data catalog.
        :param source_flow_config: Contains information about the configuration of the source connector used in the flow.
        :param tags: The tags used to organize, track, or control access for your flow.
        :param tasks: A list of tasks that Amazon AppFlow performs while transferring the data in the flow run.
        :param trigger_config: The trigger settings that determine how and when Amazon AppFlow runs the specified flow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
            
            cfn_flow_mixin_props = appflow_mixins.CfnFlowMixinProps(
                description="description",
                destination_flow_config_list=[appflow_mixins.CfnFlowPropsMixin.DestinationFlowConfigProperty(
                    api_version="apiVersion",
                    connector_profile_name="connectorProfileName",
                    connector_type="connectorType",
                    destination_connector_properties=appflow_mixins.CfnFlowPropsMixin.DestinationConnectorPropertiesProperty(
                        custom_connector=appflow_mixins.CfnFlowPropsMixin.CustomConnectorDestinationPropertiesProperty(
                            custom_properties={
                                "custom_properties_key": "customProperties"
                            },
                            entity_name="entityName",
                            error_handling_config=appflow_mixins.CfnFlowPropsMixin.ErrorHandlingConfigProperty(
                                bucket_name="bucketName",
                                bucket_prefix="bucketPrefix",
                                fail_on_first_error=False
                            ),
                            id_field_names=["idFieldNames"],
                            write_operation_type="writeOperationType"
                        ),
                        event_bridge=appflow_mixins.CfnFlowPropsMixin.EventBridgeDestinationPropertiesProperty(
                            error_handling_config=appflow_mixins.CfnFlowPropsMixin.ErrorHandlingConfigProperty(
                                bucket_name="bucketName",
                                bucket_prefix="bucketPrefix",
                                fail_on_first_error=False
                            ),
                            object="object"
                        ),
                        lookout_metrics=appflow_mixins.CfnFlowPropsMixin.LookoutMetricsDestinationPropertiesProperty(
                            object="object"
                        ),
                        marketo=appflow_mixins.CfnFlowPropsMixin.MarketoDestinationPropertiesProperty(
                            error_handling_config=appflow_mixins.CfnFlowPropsMixin.ErrorHandlingConfigProperty(
                                bucket_name="bucketName",
                                bucket_prefix="bucketPrefix",
                                fail_on_first_error=False
                            ),
                            object="object"
                        ),
                        redshift=appflow_mixins.CfnFlowPropsMixin.RedshiftDestinationPropertiesProperty(
                            bucket_prefix="bucketPrefix",
                            error_handling_config=appflow_mixins.CfnFlowPropsMixin.ErrorHandlingConfigProperty(
                                bucket_name="bucketName",
                                bucket_prefix="bucketPrefix",
                                fail_on_first_error=False
                            ),
                            intermediate_bucket_name="intermediateBucketName",
                            object="object"
                        ),
                        s3=appflow_mixins.CfnFlowPropsMixin.S3DestinationPropertiesProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix",
                            s3_output_format_config=appflow_mixins.CfnFlowPropsMixin.S3OutputFormatConfigProperty(
                                aggregation_config=appflow_mixins.CfnFlowPropsMixin.AggregationConfigProperty(
                                    aggregation_type="aggregationType",
                                    target_file_size=123
                                ),
                                file_type="fileType",
                                prefix_config=appflow_mixins.CfnFlowPropsMixin.PrefixConfigProperty(
                                    path_prefix_hierarchy=["pathPrefixHierarchy"],
                                    prefix_format="prefixFormat",
                                    prefix_type="prefixType"
                                ),
                                preserve_source_data_typing=False
                            )
                        ),
                        salesforce=appflow_mixins.CfnFlowPropsMixin.SalesforceDestinationPropertiesProperty(
                            data_transfer_api="dataTransferApi",
                            error_handling_config=appflow_mixins.CfnFlowPropsMixin.ErrorHandlingConfigProperty(
                                bucket_name="bucketName",
                                bucket_prefix="bucketPrefix",
                                fail_on_first_error=False
                            ),
                            id_field_names=["idFieldNames"],
                            object="object",
                            write_operation_type="writeOperationType"
                        ),
                        sapo_data=appflow_mixins.CfnFlowPropsMixin.SAPODataDestinationPropertiesProperty(
                            error_handling_config=appflow_mixins.CfnFlowPropsMixin.ErrorHandlingConfigProperty(
                                bucket_name="bucketName",
                                bucket_prefix="bucketPrefix",
                                fail_on_first_error=False
                            ),
                            id_field_names=["idFieldNames"],
                            object_path="objectPath",
                            success_response_handling_config=appflow_mixins.CfnFlowPropsMixin.SuccessResponseHandlingConfigProperty(
                                bucket_name="bucketName",
                                bucket_prefix="bucketPrefix"
                            ),
                            write_operation_type="writeOperationType"
                        ),
                        snowflake=appflow_mixins.CfnFlowPropsMixin.SnowflakeDestinationPropertiesProperty(
                            bucket_prefix="bucketPrefix",
                            error_handling_config=appflow_mixins.CfnFlowPropsMixin.ErrorHandlingConfigProperty(
                                bucket_name="bucketName",
                                bucket_prefix="bucketPrefix",
                                fail_on_first_error=False
                            ),
                            intermediate_bucket_name="intermediateBucketName",
                            object="object"
                        ),
                        upsolver=appflow_mixins.CfnFlowPropsMixin.UpsolverDestinationPropertiesProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix",
                            s3_output_format_config=appflow_mixins.CfnFlowPropsMixin.UpsolverS3OutputFormatConfigProperty(
                                aggregation_config=appflow_mixins.CfnFlowPropsMixin.AggregationConfigProperty(
                                    aggregation_type="aggregationType",
                                    target_file_size=123
                                ),
                                file_type="fileType",
                                prefix_config=appflow_mixins.CfnFlowPropsMixin.PrefixConfigProperty(
                                    path_prefix_hierarchy=["pathPrefixHierarchy"],
                                    prefix_format="prefixFormat",
                                    prefix_type="prefixType"
                                )
                            )
                        ),
                        zendesk=appflow_mixins.CfnFlowPropsMixin.ZendeskDestinationPropertiesProperty(
                            error_handling_config=appflow_mixins.CfnFlowPropsMixin.ErrorHandlingConfigProperty(
                                bucket_name="bucketName",
                                bucket_prefix="bucketPrefix",
                                fail_on_first_error=False
                            ),
                            id_field_names=["idFieldNames"],
                            object="object",
                            write_operation_type="writeOperationType"
                        )
                    )
                )],
                flow_name="flowName",
                flow_status="flowStatus",
                kms_arn="kmsArn",
                metadata_catalog_config=appflow_mixins.CfnFlowPropsMixin.MetadataCatalogConfigProperty(
                    glue_data_catalog=appflow_mixins.CfnFlowPropsMixin.GlueDataCatalogProperty(
                        database_name="databaseName",
                        role_arn="roleArn",
                        table_prefix="tablePrefix"
                    )
                ),
                source_flow_config=appflow_mixins.CfnFlowPropsMixin.SourceFlowConfigProperty(
                    api_version="apiVersion",
                    connector_profile_name="connectorProfileName",
                    connector_type="connectorType",
                    incremental_pull_config=appflow_mixins.CfnFlowPropsMixin.IncrementalPullConfigProperty(
                        datetime_type_field_name="datetimeTypeFieldName"
                    ),
                    source_connector_properties=appflow_mixins.CfnFlowPropsMixin.SourceConnectorPropertiesProperty(
                        amplitude=appflow_mixins.CfnFlowPropsMixin.AmplitudeSourcePropertiesProperty(
                            object="object"
                        ),
                        custom_connector=appflow_mixins.CfnFlowPropsMixin.CustomConnectorSourcePropertiesProperty(
                            custom_properties={
                                "custom_properties_key": "customProperties"
                            },
                            data_transfer_api=appflow_mixins.CfnFlowPropsMixin.DataTransferApiProperty(
                                name="name",
                                type="type"
                            ),
                            entity_name="entityName"
                        ),
                        datadog=appflow_mixins.CfnFlowPropsMixin.DatadogSourcePropertiesProperty(
                            object="object"
                        ),
                        dynatrace=appflow_mixins.CfnFlowPropsMixin.DynatraceSourcePropertiesProperty(
                            object="object"
                        ),
                        google_analytics=appflow_mixins.CfnFlowPropsMixin.GoogleAnalyticsSourcePropertiesProperty(
                            object="object"
                        ),
                        infor_nexus=appflow_mixins.CfnFlowPropsMixin.InforNexusSourcePropertiesProperty(
                            object="object"
                        ),
                        marketo=appflow_mixins.CfnFlowPropsMixin.MarketoSourcePropertiesProperty(
                            object="object"
                        ),
                        pardot=appflow_mixins.CfnFlowPropsMixin.PardotSourcePropertiesProperty(
                            object="object"
                        ),
                        s3=appflow_mixins.CfnFlowPropsMixin.S3SourcePropertiesProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix",
                            s3_input_format_config=appflow_mixins.CfnFlowPropsMixin.S3InputFormatConfigProperty(
                                s3_input_file_type="s3InputFileType"
                            )
                        ),
                        salesforce=appflow_mixins.CfnFlowPropsMixin.SalesforceSourcePropertiesProperty(
                            data_transfer_api="dataTransferApi",
                            enable_dynamic_field_update=False,
                            include_deleted_records=False,
                            object="object"
                        ),
                        sapo_data=appflow_mixins.CfnFlowPropsMixin.SAPODataSourcePropertiesProperty(
                            object_path="objectPath",
                            pagination_config=appflow_mixins.CfnFlowPropsMixin.SAPODataPaginationConfigProperty(
                                max_page_size=123
                            ),
                            parallelism_config=appflow_mixins.CfnFlowPropsMixin.SAPODataParallelismConfigProperty(
                                max_parallelism=123
                            )
                        ),
                        service_now=appflow_mixins.CfnFlowPropsMixin.ServiceNowSourcePropertiesProperty(
                            object="object"
                        ),
                        singular=appflow_mixins.CfnFlowPropsMixin.SingularSourcePropertiesProperty(
                            object="object"
                        ),
                        slack=appflow_mixins.CfnFlowPropsMixin.SlackSourcePropertiesProperty(
                            object="object"
                        ),
                        trendmicro=appflow_mixins.CfnFlowPropsMixin.TrendmicroSourcePropertiesProperty(
                            object="object"
                        ),
                        veeva=appflow_mixins.CfnFlowPropsMixin.VeevaSourcePropertiesProperty(
                            document_type="documentType",
                            include_all_versions=False,
                            include_renditions=False,
                            include_source_files=False,
                            object="object"
                        ),
                        zendesk=appflow_mixins.CfnFlowPropsMixin.ZendeskSourcePropertiesProperty(
                            object="object"
                        )
                    )
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                tasks=[appflow_mixins.CfnFlowPropsMixin.TaskProperty(
                    connector_operator=appflow_mixins.CfnFlowPropsMixin.ConnectorOperatorProperty(
                        amplitude="amplitude",
                        custom_connector="customConnector",
                        datadog="datadog",
                        dynatrace="dynatrace",
                        google_analytics="googleAnalytics",
                        infor_nexus="inforNexus",
                        marketo="marketo",
                        pardot="pardot",
                        s3="s3",
                        salesforce="salesforce",
                        sapo_data="sapoData",
                        service_now="serviceNow",
                        singular="singular",
                        slack="slack",
                        trendmicro="trendmicro",
                        veeva="veeva",
                        zendesk="zendesk"
                    ),
                    destination_field="destinationField",
                    source_fields=["sourceFields"],
                    task_properties=[appflow_mixins.CfnFlowPropsMixin.TaskPropertiesObjectProperty(
                        key="key",
                        value="value"
                    )],
                    task_type="taskType"
                )],
                trigger_config=appflow_mixins.CfnFlowPropsMixin.TriggerConfigProperty(
                    trigger_properties=appflow_mixins.CfnFlowPropsMixin.ScheduledTriggerPropertiesProperty(
                        data_pull_mode="dataPullMode",
                        first_execution_from=123,
                        flow_error_deactivation_threshold=123,
                        schedule_end_time=123,
                        schedule_expression="scheduleExpression",
                        schedule_offset=123,
                        schedule_start_time=123,
                        time_zone="timeZone"
                    ),
                    trigger_type="triggerType"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc96d5aa9ea8401c816efcad2a92f807b1a086b7801e0d79ce9d78fe7717302e)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument destination_flow_config_list", value=destination_flow_config_list, expected_type=type_hints["destination_flow_config_list"])
            check_type(argname="argument flow_name", value=flow_name, expected_type=type_hints["flow_name"])
            check_type(argname="argument flow_status", value=flow_status, expected_type=type_hints["flow_status"])
            check_type(argname="argument kms_arn", value=kms_arn, expected_type=type_hints["kms_arn"])
            check_type(argname="argument metadata_catalog_config", value=metadata_catalog_config, expected_type=type_hints["metadata_catalog_config"])
            check_type(argname="argument source_flow_config", value=source_flow_config, expected_type=type_hints["source_flow_config"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tasks", value=tasks, expected_type=type_hints["tasks"])
            check_type(argname="argument trigger_config", value=trigger_config, expected_type=type_hints["trigger_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if destination_flow_config_list is not None:
            self._values["destination_flow_config_list"] = destination_flow_config_list
        if flow_name is not None:
            self._values["flow_name"] = flow_name
        if flow_status is not None:
            self._values["flow_status"] = flow_status
        if kms_arn is not None:
            self._values["kms_arn"] = kms_arn
        if metadata_catalog_config is not None:
            self._values["metadata_catalog_config"] = metadata_catalog_config
        if source_flow_config is not None:
            self._values["source_flow_config"] = source_flow_config
        if tags is not None:
            self._values["tags"] = tags
        if tasks is not None:
            self._values["tasks"] = tasks
        if trigger_config is not None:
            self._values["trigger_config"] = trigger_config

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A user-entered description of the flow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html#cfn-appflow-flow-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destination_flow_config_list(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.DestinationFlowConfigProperty"]]]]:
        '''The configuration that controls how Amazon AppFlow places data in the destination connector.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html#cfn-appflow-flow-destinationflowconfiglist
        '''
        result = self._values.get("destination_flow_config_list")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.DestinationFlowConfigProperty"]]]], result)

    @builtins.property
    def flow_name(self) -> typing.Optional[builtins.str]:
        '''The specified name of the flow.

        Spaces are not allowed. Use underscores (_) or hyphens (-) only.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html#cfn-appflow-flow-flowname
        '''
        result = self._values.get("flow_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def flow_status(self) -> typing.Optional[builtins.str]:
        '''Sets the status of the flow. You can specify one of the following values:.

        - **Active** - The flow runs based on the trigger settings that you defined. Active scheduled flows run as scheduled, and active event-triggered flows run when the specified change event occurs. However, active on-demand flows run only when you manually start them by using Amazon AppFlow.
        - **Suspended** - You can use this option to deactivate an active flow. Scheduled and event-triggered flows will cease to run until you reactive them. This value only affects scheduled and event-triggered flows. It has no effect for on-demand flows.

        If you omit the FlowStatus parameter, Amazon AppFlow creates the flow with a default status. The default status for on-demand flows is Active. The default status for scheduled and event-triggered flows is Draft, which means they’re not yet active.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html#cfn-appflow-flow-flowstatus
        '''
        result = self._values.get("flow_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN (Amazon Resource Name) of the Key Management Service (KMS) key you provide for encryption.

        This is required if you do not want to use the Amazon AppFlow-managed KMS key. If you don't provide anything here, Amazon AppFlow uses the Amazon AppFlow-managed KMS key.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html#cfn-appflow-flow-kmsarn
        '''
        result = self._values.get("kms_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metadata_catalog_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.MetadataCatalogConfigProperty"]]:
        '''Specifies the configuration that Amazon AppFlow uses when it catalogs your data.

        When Amazon AppFlow catalogs your data, it stores metadata in a data catalog.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html#cfn-appflow-flow-metadatacatalogconfig
        '''
        result = self._values.get("metadata_catalog_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.MetadataCatalogConfigProperty"]], result)

    @builtins.property
    def source_flow_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.SourceFlowConfigProperty"]]:
        '''Contains information about the configuration of the source connector used in the flow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html#cfn-appflow-flow-sourceflowconfig
        '''
        result = self._values.get("source_flow_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.SourceFlowConfigProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags used to organize, track, or control access for your flow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html#cfn-appflow-flow-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def tasks(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.TaskProperty"]]]]:
        '''A list of tasks that Amazon AppFlow performs while transferring the data in the flow run.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html#cfn-appflow-flow-tasks
        '''
        result = self._values.get("tasks")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.TaskProperty"]]]], result)

    @builtins.property
    def trigger_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.TriggerConfigProperty"]]:
        '''The trigger settings that determine how and when Amazon AppFlow runs the specified flow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html#cfn-appflow-flow-triggerconfig
        '''
        result = self._values.get("trigger_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.TriggerConfigProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFlowMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnFlowPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin",
):
    '''The ``AWS::AppFlow::Flow`` resource is an Amazon AppFlow resource type that specifies a new flow.

    .. epigraph::

       If you want to use CloudFormation to create a connector profile for connectors that implement OAuth (such as Salesforce, Slack, Zendesk, and Google Analytics), you must fetch the access and refresh tokens. You can do this by implementing your own UI for OAuth, or by retrieving the tokens from elsewhere. Alternatively, you can use the Amazon AppFlow console to create the connector profile, and then use that connector profile in the flow creation CloudFormation template.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html
    :cloudformationResource: AWS::AppFlow::Flow
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
        
        cfn_flow_props_mixin = appflow_mixins.CfnFlowPropsMixin(appflow_mixins.CfnFlowMixinProps(
            description="description",
            destination_flow_config_list=[appflow_mixins.CfnFlowPropsMixin.DestinationFlowConfigProperty(
                api_version="apiVersion",
                connector_profile_name="connectorProfileName",
                connector_type="connectorType",
                destination_connector_properties=appflow_mixins.CfnFlowPropsMixin.DestinationConnectorPropertiesProperty(
                    custom_connector=appflow_mixins.CfnFlowPropsMixin.CustomConnectorDestinationPropertiesProperty(
                        custom_properties={
                            "custom_properties_key": "customProperties"
                        },
                        entity_name="entityName",
                        error_handling_config=appflow_mixins.CfnFlowPropsMixin.ErrorHandlingConfigProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix",
                            fail_on_first_error=False
                        ),
                        id_field_names=["idFieldNames"],
                        write_operation_type="writeOperationType"
                    ),
                    event_bridge=appflow_mixins.CfnFlowPropsMixin.EventBridgeDestinationPropertiesProperty(
                        error_handling_config=appflow_mixins.CfnFlowPropsMixin.ErrorHandlingConfigProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix",
                            fail_on_first_error=False
                        ),
                        object="object"
                    ),
                    lookout_metrics=appflow_mixins.CfnFlowPropsMixin.LookoutMetricsDestinationPropertiesProperty(
                        object="object"
                    ),
                    marketo=appflow_mixins.CfnFlowPropsMixin.MarketoDestinationPropertiesProperty(
                        error_handling_config=appflow_mixins.CfnFlowPropsMixin.ErrorHandlingConfigProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix",
                            fail_on_first_error=False
                        ),
                        object="object"
                    ),
                    redshift=appflow_mixins.CfnFlowPropsMixin.RedshiftDestinationPropertiesProperty(
                        bucket_prefix="bucketPrefix",
                        error_handling_config=appflow_mixins.CfnFlowPropsMixin.ErrorHandlingConfigProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix",
                            fail_on_first_error=False
                        ),
                        intermediate_bucket_name="intermediateBucketName",
                        object="object"
                    ),
                    s3=appflow_mixins.CfnFlowPropsMixin.S3DestinationPropertiesProperty(
                        bucket_name="bucketName",
                        bucket_prefix="bucketPrefix",
                        s3_output_format_config=appflow_mixins.CfnFlowPropsMixin.S3OutputFormatConfigProperty(
                            aggregation_config=appflow_mixins.CfnFlowPropsMixin.AggregationConfigProperty(
                                aggregation_type="aggregationType",
                                target_file_size=123
                            ),
                            file_type="fileType",
                            prefix_config=appflow_mixins.CfnFlowPropsMixin.PrefixConfigProperty(
                                path_prefix_hierarchy=["pathPrefixHierarchy"],
                                prefix_format="prefixFormat",
                                prefix_type="prefixType"
                            ),
                            preserve_source_data_typing=False
                        )
                    ),
                    salesforce=appflow_mixins.CfnFlowPropsMixin.SalesforceDestinationPropertiesProperty(
                        data_transfer_api="dataTransferApi",
                        error_handling_config=appflow_mixins.CfnFlowPropsMixin.ErrorHandlingConfigProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix",
                            fail_on_first_error=False
                        ),
                        id_field_names=["idFieldNames"],
                        object="object",
                        write_operation_type="writeOperationType"
                    ),
                    sapo_data=appflow_mixins.CfnFlowPropsMixin.SAPODataDestinationPropertiesProperty(
                        error_handling_config=appflow_mixins.CfnFlowPropsMixin.ErrorHandlingConfigProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix",
                            fail_on_first_error=False
                        ),
                        id_field_names=["idFieldNames"],
                        object_path="objectPath",
                        success_response_handling_config=appflow_mixins.CfnFlowPropsMixin.SuccessResponseHandlingConfigProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix"
                        ),
                        write_operation_type="writeOperationType"
                    ),
                    snowflake=appflow_mixins.CfnFlowPropsMixin.SnowflakeDestinationPropertiesProperty(
                        bucket_prefix="bucketPrefix",
                        error_handling_config=appflow_mixins.CfnFlowPropsMixin.ErrorHandlingConfigProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix",
                            fail_on_first_error=False
                        ),
                        intermediate_bucket_name="intermediateBucketName",
                        object="object"
                    ),
                    upsolver=appflow_mixins.CfnFlowPropsMixin.UpsolverDestinationPropertiesProperty(
                        bucket_name="bucketName",
                        bucket_prefix="bucketPrefix",
                        s3_output_format_config=appflow_mixins.CfnFlowPropsMixin.UpsolverS3OutputFormatConfigProperty(
                            aggregation_config=appflow_mixins.CfnFlowPropsMixin.AggregationConfigProperty(
                                aggregation_type="aggregationType",
                                target_file_size=123
                            ),
                            file_type="fileType",
                            prefix_config=appflow_mixins.CfnFlowPropsMixin.PrefixConfigProperty(
                                path_prefix_hierarchy=["pathPrefixHierarchy"],
                                prefix_format="prefixFormat",
                                prefix_type="prefixType"
                            )
                        )
                    ),
                    zendesk=appflow_mixins.CfnFlowPropsMixin.ZendeskDestinationPropertiesProperty(
                        error_handling_config=appflow_mixins.CfnFlowPropsMixin.ErrorHandlingConfigProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix",
                            fail_on_first_error=False
                        ),
                        id_field_names=["idFieldNames"],
                        object="object",
                        write_operation_type="writeOperationType"
                    )
                )
            )],
            flow_name="flowName",
            flow_status="flowStatus",
            kms_arn="kmsArn",
            metadata_catalog_config=appflow_mixins.CfnFlowPropsMixin.MetadataCatalogConfigProperty(
                glue_data_catalog=appflow_mixins.CfnFlowPropsMixin.GlueDataCatalogProperty(
                    database_name="databaseName",
                    role_arn="roleArn",
                    table_prefix="tablePrefix"
                )
            ),
            source_flow_config=appflow_mixins.CfnFlowPropsMixin.SourceFlowConfigProperty(
                api_version="apiVersion",
                connector_profile_name="connectorProfileName",
                connector_type="connectorType",
                incremental_pull_config=appflow_mixins.CfnFlowPropsMixin.IncrementalPullConfigProperty(
                    datetime_type_field_name="datetimeTypeFieldName"
                ),
                source_connector_properties=appflow_mixins.CfnFlowPropsMixin.SourceConnectorPropertiesProperty(
                    amplitude=appflow_mixins.CfnFlowPropsMixin.AmplitudeSourcePropertiesProperty(
                        object="object"
                    ),
                    custom_connector=appflow_mixins.CfnFlowPropsMixin.CustomConnectorSourcePropertiesProperty(
                        custom_properties={
                            "custom_properties_key": "customProperties"
                        },
                        data_transfer_api=appflow_mixins.CfnFlowPropsMixin.DataTransferApiProperty(
                            name="name",
                            type="type"
                        ),
                        entity_name="entityName"
                    ),
                    datadog=appflow_mixins.CfnFlowPropsMixin.DatadogSourcePropertiesProperty(
                        object="object"
                    ),
                    dynatrace=appflow_mixins.CfnFlowPropsMixin.DynatraceSourcePropertiesProperty(
                        object="object"
                    ),
                    google_analytics=appflow_mixins.CfnFlowPropsMixin.GoogleAnalyticsSourcePropertiesProperty(
                        object="object"
                    ),
                    infor_nexus=appflow_mixins.CfnFlowPropsMixin.InforNexusSourcePropertiesProperty(
                        object="object"
                    ),
                    marketo=appflow_mixins.CfnFlowPropsMixin.MarketoSourcePropertiesProperty(
                        object="object"
                    ),
                    pardot=appflow_mixins.CfnFlowPropsMixin.PardotSourcePropertiesProperty(
                        object="object"
                    ),
                    s3=appflow_mixins.CfnFlowPropsMixin.S3SourcePropertiesProperty(
                        bucket_name="bucketName",
                        bucket_prefix="bucketPrefix",
                        s3_input_format_config=appflow_mixins.CfnFlowPropsMixin.S3InputFormatConfigProperty(
                            s3_input_file_type="s3InputFileType"
                        )
                    ),
                    salesforce=appflow_mixins.CfnFlowPropsMixin.SalesforceSourcePropertiesProperty(
                        data_transfer_api="dataTransferApi",
                        enable_dynamic_field_update=False,
                        include_deleted_records=False,
                        object="object"
                    ),
                    sapo_data=appflow_mixins.CfnFlowPropsMixin.SAPODataSourcePropertiesProperty(
                        object_path="objectPath",
                        pagination_config=appflow_mixins.CfnFlowPropsMixin.SAPODataPaginationConfigProperty(
                            max_page_size=123
                        ),
                        parallelism_config=appflow_mixins.CfnFlowPropsMixin.SAPODataParallelismConfigProperty(
                            max_parallelism=123
                        )
                    ),
                    service_now=appflow_mixins.CfnFlowPropsMixin.ServiceNowSourcePropertiesProperty(
                        object="object"
                    ),
                    singular=appflow_mixins.CfnFlowPropsMixin.SingularSourcePropertiesProperty(
                        object="object"
                    ),
                    slack=appflow_mixins.CfnFlowPropsMixin.SlackSourcePropertiesProperty(
                        object="object"
                    ),
                    trendmicro=appflow_mixins.CfnFlowPropsMixin.TrendmicroSourcePropertiesProperty(
                        object="object"
                    ),
                    veeva=appflow_mixins.CfnFlowPropsMixin.VeevaSourcePropertiesProperty(
                        document_type="documentType",
                        include_all_versions=False,
                        include_renditions=False,
                        include_source_files=False,
                        object="object"
                    ),
                    zendesk=appflow_mixins.CfnFlowPropsMixin.ZendeskSourcePropertiesProperty(
                        object="object"
                    )
                )
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            tasks=[appflow_mixins.CfnFlowPropsMixin.TaskProperty(
                connector_operator=appflow_mixins.CfnFlowPropsMixin.ConnectorOperatorProperty(
                    amplitude="amplitude",
                    custom_connector="customConnector",
                    datadog="datadog",
                    dynatrace="dynatrace",
                    google_analytics="googleAnalytics",
                    infor_nexus="inforNexus",
                    marketo="marketo",
                    pardot="pardot",
                    s3="s3",
                    salesforce="salesforce",
                    sapo_data="sapoData",
                    service_now="serviceNow",
                    singular="singular",
                    slack="slack",
                    trendmicro="trendmicro",
                    veeva="veeva",
                    zendesk="zendesk"
                ),
                destination_field="destinationField",
                source_fields=["sourceFields"],
                task_properties=[appflow_mixins.CfnFlowPropsMixin.TaskPropertiesObjectProperty(
                    key="key",
                    value="value"
                )],
                task_type="taskType"
            )],
            trigger_config=appflow_mixins.CfnFlowPropsMixin.TriggerConfigProperty(
                trigger_properties=appflow_mixins.CfnFlowPropsMixin.ScheduledTriggerPropertiesProperty(
                    data_pull_mode="dataPullMode",
                    first_execution_from=123,
                    flow_error_deactivation_threshold=123,
                    schedule_end_time=123,
                    schedule_expression="scheduleExpression",
                    schedule_offset=123,
                    schedule_start_time=123,
                    time_zone="timeZone"
                ),
                trigger_type="triggerType"
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnFlowMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AppFlow::Flow``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c502d7408c8258708710ecf0e2408c7cc3752c5ca34fb3c04dc4b1ece1caf8ea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e722a34a7335b46d6f83ee2598d169dc79800ee44d1565c6076f8f57c50b95a8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bd6020242eb35eaaa1aee1b815f8876a3dda4e2a915401116c37fb791876200)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnFlowMixinProps:
        return typing.cast(CfnFlowMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.AggregationConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "aggregation_type": "aggregationType",
            "target_file_size": "targetFileSize",
        },
    )
    class AggregationConfigProperty:
        def __init__(
            self,
            *,
            aggregation_type: typing.Optional[builtins.str] = None,
            target_file_size: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The aggregation settings that you can use to customize the output format of your flow data.

            :param aggregation_type: Specifies whether Amazon AppFlow aggregates the flow records into a single file, or leave them unaggregated.
            :param target_file_size: The desired file size, in MB, for each output file that Amazon AppFlow writes to the flow destination. For each file, Amazon AppFlow attempts to achieve the size that you specify. The actual file sizes might differ from this target based on the number and size of the records that each file contains.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-aggregationconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                aggregation_config_property = appflow_mixins.CfnFlowPropsMixin.AggregationConfigProperty(
                    aggregation_type="aggregationType",
                    target_file_size=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d028e4dd84c95e074f477551c9f2f2ce206947bdb0e495a5eef2f84ed97e98fd)
                check_type(argname="argument aggregation_type", value=aggregation_type, expected_type=type_hints["aggregation_type"])
                check_type(argname="argument target_file_size", value=target_file_size, expected_type=type_hints["target_file_size"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if aggregation_type is not None:
                self._values["aggregation_type"] = aggregation_type
            if target_file_size is not None:
                self._values["target_file_size"] = target_file_size

        @builtins.property
        def aggregation_type(self) -> typing.Optional[builtins.str]:
            '''Specifies whether Amazon AppFlow aggregates the flow records into a single file, or leave them unaggregated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-aggregationconfig.html#cfn-appflow-flow-aggregationconfig-aggregationtype
            '''
            result = self._values.get("aggregation_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_file_size(self) -> typing.Optional[jsii.Number]:
            '''The desired file size, in MB, for each output file that Amazon AppFlow writes to the flow destination.

            For each file, Amazon AppFlow attempts to achieve the size that you specify. The actual file sizes might differ from this target based on the number and size of the records that each file contains.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-aggregationconfig.html#cfn-appflow-flow-aggregationconfig-targetfilesize
            '''
            result = self._values.get("target_file_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AggregationConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.AmplitudeSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"object": "object"},
    )
    class AmplitudeSourcePropertiesProperty:
        def __init__(self, *, object: typing.Optional[builtins.str] = None) -> None:
            '''The properties that are applied when Amplitude is being used as a source.

            :param object: The object specified in the Amplitude flow source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-amplitudesourceproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                amplitude_source_properties_property = appflow_mixins.CfnFlowPropsMixin.AmplitudeSourcePropertiesProperty(
                    object="object"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ce786fc2531ba1c14a6987a4dea9e11d2bb423a083eb13259bab3422fa2fe8d9)
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if object is not None:
                self._values["object"] = object

        @builtins.property
        def object(self) -> typing.Optional[builtins.str]:
            '''The object specified in the Amplitude flow source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-amplitudesourceproperties.html#cfn-appflow-flow-amplitudesourceproperties-object
            '''
            result = self._values.get("object")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AmplitudeSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.ConnectorOperatorProperty",
        jsii_struct_bases=[],
        name_mapping={
            "amplitude": "amplitude",
            "custom_connector": "customConnector",
            "datadog": "datadog",
            "dynatrace": "dynatrace",
            "google_analytics": "googleAnalytics",
            "infor_nexus": "inforNexus",
            "marketo": "marketo",
            "pardot": "pardot",
            "s3": "s3",
            "salesforce": "salesforce",
            "sapo_data": "sapoData",
            "service_now": "serviceNow",
            "singular": "singular",
            "slack": "slack",
            "trendmicro": "trendmicro",
            "veeva": "veeva",
            "zendesk": "zendesk",
        },
    )
    class ConnectorOperatorProperty:
        def __init__(
            self,
            *,
            amplitude: typing.Optional[builtins.str] = None,
            custom_connector: typing.Optional[builtins.str] = None,
            datadog: typing.Optional[builtins.str] = None,
            dynatrace: typing.Optional[builtins.str] = None,
            google_analytics: typing.Optional[builtins.str] = None,
            infor_nexus: typing.Optional[builtins.str] = None,
            marketo: typing.Optional[builtins.str] = None,
            pardot: typing.Optional[builtins.str] = None,
            s3: typing.Optional[builtins.str] = None,
            salesforce: typing.Optional[builtins.str] = None,
            sapo_data: typing.Optional[builtins.str] = None,
            service_now: typing.Optional[builtins.str] = None,
            singular: typing.Optional[builtins.str] = None,
            slack: typing.Optional[builtins.str] = None,
            trendmicro: typing.Optional[builtins.str] = None,
            veeva: typing.Optional[builtins.str] = None,
            zendesk: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The operation to be performed on the provided source fields.

            :param amplitude: The operation to be performed on the provided Amplitude source fields.
            :param custom_connector: Operators supported by the custom connector.
            :param datadog: The operation to be performed on the provided Datadog source fields.
            :param dynatrace: The operation to be performed on the provided Dynatrace source fields.
            :param google_analytics: The operation to be performed on the provided Google Analytics source fields.
            :param infor_nexus: The operation to be performed on the provided Infor Nexus source fields.
            :param marketo: The operation to be performed on the provided Marketo source fields.
            :param pardot: The operation to be performed on the provided Salesforce Pardot source fields.
            :param s3: The operation to be performed on the provided Amazon S3 source fields.
            :param salesforce: The operation to be performed on the provided Salesforce source fields.
            :param sapo_data: The operation to be performed on the provided SAPOData source fields.
            :param service_now: The operation to be performed on the provided ServiceNow source fields.
            :param singular: The operation to be performed on the provided Singular source fields.
            :param slack: The operation to be performed on the provided Slack source fields.
            :param trendmicro: The operation to be performed on the provided Trend Micro source fields.
            :param veeva: The operation to be performed on the provided Veeva source fields.
            :param zendesk: The operation to be performed on the provided Zendesk source fields.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                connector_operator_property = appflow_mixins.CfnFlowPropsMixin.ConnectorOperatorProperty(
                    amplitude="amplitude",
                    custom_connector="customConnector",
                    datadog="datadog",
                    dynatrace="dynatrace",
                    google_analytics="googleAnalytics",
                    infor_nexus="inforNexus",
                    marketo="marketo",
                    pardot="pardot",
                    s3="s3",
                    salesforce="salesforce",
                    sapo_data="sapoData",
                    service_now="serviceNow",
                    singular="singular",
                    slack="slack",
                    trendmicro="trendmicro",
                    veeva="veeva",
                    zendesk="zendesk"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__787267d13b6cacdc6806f0412a1d678c57105393e1ca5fb95c29830eb55b488d)
                check_type(argname="argument amplitude", value=amplitude, expected_type=type_hints["amplitude"])
                check_type(argname="argument custom_connector", value=custom_connector, expected_type=type_hints["custom_connector"])
                check_type(argname="argument datadog", value=datadog, expected_type=type_hints["datadog"])
                check_type(argname="argument dynatrace", value=dynatrace, expected_type=type_hints["dynatrace"])
                check_type(argname="argument google_analytics", value=google_analytics, expected_type=type_hints["google_analytics"])
                check_type(argname="argument infor_nexus", value=infor_nexus, expected_type=type_hints["infor_nexus"])
                check_type(argname="argument marketo", value=marketo, expected_type=type_hints["marketo"])
                check_type(argname="argument pardot", value=pardot, expected_type=type_hints["pardot"])
                check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
                check_type(argname="argument salesforce", value=salesforce, expected_type=type_hints["salesforce"])
                check_type(argname="argument sapo_data", value=sapo_data, expected_type=type_hints["sapo_data"])
                check_type(argname="argument service_now", value=service_now, expected_type=type_hints["service_now"])
                check_type(argname="argument singular", value=singular, expected_type=type_hints["singular"])
                check_type(argname="argument slack", value=slack, expected_type=type_hints["slack"])
                check_type(argname="argument trendmicro", value=trendmicro, expected_type=type_hints["trendmicro"])
                check_type(argname="argument veeva", value=veeva, expected_type=type_hints["veeva"])
                check_type(argname="argument zendesk", value=zendesk, expected_type=type_hints["zendesk"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if amplitude is not None:
                self._values["amplitude"] = amplitude
            if custom_connector is not None:
                self._values["custom_connector"] = custom_connector
            if datadog is not None:
                self._values["datadog"] = datadog
            if dynatrace is not None:
                self._values["dynatrace"] = dynatrace
            if google_analytics is not None:
                self._values["google_analytics"] = google_analytics
            if infor_nexus is not None:
                self._values["infor_nexus"] = infor_nexus
            if marketo is not None:
                self._values["marketo"] = marketo
            if pardot is not None:
                self._values["pardot"] = pardot
            if s3 is not None:
                self._values["s3"] = s3
            if salesforce is not None:
                self._values["salesforce"] = salesforce
            if sapo_data is not None:
                self._values["sapo_data"] = sapo_data
            if service_now is not None:
                self._values["service_now"] = service_now
            if singular is not None:
                self._values["singular"] = singular
            if slack is not None:
                self._values["slack"] = slack
            if trendmicro is not None:
                self._values["trendmicro"] = trendmicro
            if veeva is not None:
                self._values["veeva"] = veeva
            if zendesk is not None:
                self._values["zendesk"] = zendesk

        @builtins.property
        def amplitude(self) -> typing.Optional[builtins.str]:
            '''The operation to be performed on the provided Amplitude source fields.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-amplitude
            '''
            result = self._values.get("amplitude")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def custom_connector(self) -> typing.Optional[builtins.str]:
            '''Operators supported by the custom connector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-customconnector
            '''
            result = self._values.get("custom_connector")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def datadog(self) -> typing.Optional[builtins.str]:
            '''The operation to be performed on the provided Datadog source fields.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-datadog
            '''
            result = self._values.get("datadog")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def dynatrace(self) -> typing.Optional[builtins.str]:
            '''The operation to be performed on the provided Dynatrace source fields.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-dynatrace
            '''
            result = self._values.get("dynatrace")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def google_analytics(self) -> typing.Optional[builtins.str]:
            '''The operation to be performed on the provided Google Analytics source fields.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-googleanalytics
            '''
            result = self._values.get("google_analytics")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def infor_nexus(self) -> typing.Optional[builtins.str]:
            '''The operation to be performed on the provided Infor Nexus source fields.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-infornexus
            '''
            result = self._values.get("infor_nexus")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def marketo(self) -> typing.Optional[builtins.str]:
            '''The operation to be performed on the provided Marketo source fields.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-marketo
            '''
            result = self._values.get("marketo")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def pardot(self) -> typing.Optional[builtins.str]:
            '''The operation to be performed on the provided Salesforce Pardot source fields.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-pardot
            '''
            result = self._values.get("pardot")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3(self) -> typing.Optional[builtins.str]:
            '''The operation to be performed on the provided Amazon S3 source fields.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-s3
            '''
            result = self._values.get("s3")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def salesforce(self) -> typing.Optional[builtins.str]:
            '''The operation to be performed on the provided Salesforce source fields.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-salesforce
            '''
            result = self._values.get("salesforce")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sapo_data(self) -> typing.Optional[builtins.str]:
            '''The operation to be performed on the provided SAPOData source fields.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-sapodata
            '''
            result = self._values.get("sapo_data")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def service_now(self) -> typing.Optional[builtins.str]:
            '''The operation to be performed on the provided ServiceNow source fields.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-servicenow
            '''
            result = self._values.get("service_now")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def singular(self) -> typing.Optional[builtins.str]:
            '''The operation to be performed on the provided Singular source fields.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-singular
            '''
            result = self._values.get("singular")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def slack(self) -> typing.Optional[builtins.str]:
            '''The operation to be performed on the provided Slack source fields.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-slack
            '''
            result = self._values.get("slack")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def trendmicro(self) -> typing.Optional[builtins.str]:
            '''The operation to be performed on the provided Trend Micro source fields.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-trendmicro
            '''
            result = self._values.get("trendmicro")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def veeva(self) -> typing.Optional[builtins.str]:
            '''The operation to be performed on the provided Veeva source fields.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-veeva
            '''
            result = self._values.get("veeva")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def zendesk(self) -> typing.Optional[builtins.str]:
            '''The operation to be performed on the provided Zendesk source fields.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-zendesk
            '''
            result = self._values.get("zendesk")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectorOperatorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.CustomConnectorDestinationPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "custom_properties": "customProperties",
            "entity_name": "entityName",
            "error_handling_config": "errorHandlingConfig",
            "id_field_names": "idFieldNames",
            "write_operation_type": "writeOperationType",
        },
    )
    class CustomConnectorDestinationPropertiesProperty:
        def __init__(
            self,
            *,
            custom_properties: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            entity_name: typing.Optional[builtins.str] = None,
            error_handling_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.ErrorHandlingConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            id_field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
            write_operation_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The properties that are applied when the custom connector is being used as a destination.

            :param custom_properties: The custom properties that are specific to the connector when it's used as a destination in the flow.
            :param entity_name: The entity specified in the custom connector as a destination in the flow.
            :param error_handling_config: The settings that determine how Amazon AppFlow handles an error when placing data in the custom connector as destination.
            :param id_field_names: The name of the field that Amazon AppFlow uses as an ID when performing a write operation such as update, delete, or upsert.
            :param write_operation_type: Specifies the type of write operation to be performed in the custom connector when it's used as destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-customconnectordestinationproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                custom_connector_destination_properties_property = appflow_mixins.CfnFlowPropsMixin.CustomConnectorDestinationPropertiesProperty(
                    custom_properties={
                        "custom_properties_key": "customProperties"
                    },
                    entity_name="entityName",
                    error_handling_config=appflow_mixins.CfnFlowPropsMixin.ErrorHandlingConfigProperty(
                        bucket_name="bucketName",
                        bucket_prefix="bucketPrefix",
                        fail_on_first_error=False
                    ),
                    id_field_names=["idFieldNames"],
                    write_operation_type="writeOperationType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4f851e88bcbc39b239ad177df5430beacae4369c62e6eee6f985e4571e076261)
                check_type(argname="argument custom_properties", value=custom_properties, expected_type=type_hints["custom_properties"])
                check_type(argname="argument entity_name", value=entity_name, expected_type=type_hints["entity_name"])
                check_type(argname="argument error_handling_config", value=error_handling_config, expected_type=type_hints["error_handling_config"])
                check_type(argname="argument id_field_names", value=id_field_names, expected_type=type_hints["id_field_names"])
                check_type(argname="argument write_operation_type", value=write_operation_type, expected_type=type_hints["write_operation_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if custom_properties is not None:
                self._values["custom_properties"] = custom_properties
            if entity_name is not None:
                self._values["entity_name"] = entity_name
            if error_handling_config is not None:
                self._values["error_handling_config"] = error_handling_config
            if id_field_names is not None:
                self._values["id_field_names"] = id_field_names
            if write_operation_type is not None:
                self._values["write_operation_type"] = write_operation_type

        @builtins.property
        def custom_properties(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''The custom properties that are specific to the connector when it's used as a destination in the flow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-customconnectordestinationproperties.html#cfn-appflow-flow-customconnectordestinationproperties-customproperties
            '''
            result = self._values.get("custom_properties")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def entity_name(self) -> typing.Optional[builtins.str]:
            '''The entity specified in the custom connector as a destination in the flow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-customconnectordestinationproperties.html#cfn-appflow-flow-customconnectordestinationproperties-entityname
            '''
            result = self._values.get("entity_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def error_handling_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.ErrorHandlingConfigProperty"]]:
            '''The settings that determine how Amazon AppFlow handles an error when placing data in the custom connector as destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-customconnectordestinationproperties.html#cfn-appflow-flow-customconnectordestinationproperties-errorhandlingconfig
            '''
            result = self._values.get("error_handling_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.ErrorHandlingConfigProperty"]], result)

        @builtins.property
        def id_field_names(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The name of the field that Amazon AppFlow uses as an ID when performing a write operation such as update, delete, or upsert.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-customconnectordestinationproperties.html#cfn-appflow-flow-customconnectordestinationproperties-idfieldnames
            '''
            result = self._values.get("id_field_names")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def write_operation_type(self) -> typing.Optional[builtins.str]:
            '''Specifies the type of write operation to be performed in the custom connector when it's used as destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-customconnectordestinationproperties.html#cfn-appflow-flow-customconnectordestinationproperties-writeoperationtype
            '''
            result = self._values.get("write_operation_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomConnectorDestinationPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.CustomConnectorSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "custom_properties": "customProperties",
            "data_transfer_api": "dataTransferApi",
            "entity_name": "entityName",
        },
    )
    class CustomConnectorSourcePropertiesProperty:
        def __init__(
            self,
            *,
            custom_properties: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            data_transfer_api: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.DataTransferApiProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            entity_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The properties that are applied when the custom connector is being used as a source.

            :param custom_properties: Custom properties that are required to use the custom connector as a source.
            :param data_transfer_api: The API of the connector application that Amazon AppFlow uses to transfer your data.
            :param entity_name: The entity specified in the custom connector as a source in the flow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-customconnectorsourceproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                custom_connector_source_properties_property = appflow_mixins.CfnFlowPropsMixin.CustomConnectorSourcePropertiesProperty(
                    custom_properties={
                        "custom_properties_key": "customProperties"
                    },
                    data_transfer_api=appflow_mixins.CfnFlowPropsMixin.DataTransferApiProperty(
                        name="name",
                        type="type"
                    ),
                    entity_name="entityName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__48fa68bc02b3388e65e044412a92064faf19fdf21bb02b13a694a3428d8af132)
                check_type(argname="argument custom_properties", value=custom_properties, expected_type=type_hints["custom_properties"])
                check_type(argname="argument data_transfer_api", value=data_transfer_api, expected_type=type_hints["data_transfer_api"])
                check_type(argname="argument entity_name", value=entity_name, expected_type=type_hints["entity_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if custom_properties is not None:
                self._values["custom_properties"] = custom_properties
            if data_transfer_api is not None:
                self._values["data_transfer_api"] = data_transfer_api
            if entity_name is not None:
                self._values["entity_name"] = entity_name

        @builtins.property
        def custom_properties(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''Custom properties that are required to use the custom connector as a source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-customconnectorsourceproperties.html#cfn-appflow-flow-customconnectorsourceproperties-customproperties
            '''
            result = self._values.get("custom_properties")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def data_transfer_api(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.DataTransferApiProperty"]]:
            '''The API of the connector application that Amazon AppFlow uses to transfer your data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-customconnectorsourceproperties.html#cfn-appflow-flow-customconnectorsourceproperties-datatransferapi
            '''
            result = self._values.get("data_transfer_api")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.DataTransferApiProperty"]], result)

        @builtins.property
        def entity_name(self) -> typing.Optional[builtins.str]:
            '''The entity specified in the custom connector as a source in the flow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-customconnectorsourceproperties.html#cfn-appflow-flow-customconnectorsourceproperties-entityname
            '''
            result = self._values.get("entity_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomConnectorSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.DataTransferApiProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "type": "type"},
    )
    class DataTransferApiProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The API of the connector application that Amazon AppFlow uses to transfer your data.

            :param name: The name of the connector application API.
            :param type: You can specify one of the following types:. - **AUTOMATIC** - The default. Optimizes a flow for datasets that fluctuate in size from small to large. For each flow run, Amazon AppFlow chooses to use the SYNC or ASYNC API type based on the amount of data that the run transfers. - **SYNC** - A synchronous API. This type of API optimizes a flow for small to medium-sized datasets. - **ASYNC** - An asynchronous API. This type of API optimizes a flow for large datasets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-datatransferapi.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                data_transfer_api_property = appflow_mixins.CfnFlowPropsMixin.DataTransferApiProperty(
                    name="name",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2638f8d895abf4c8627e2cf3cb75a94b8b115803626f81f2eec85294945d68f9)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the connector application API.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-datatransferapi.html#cfn-appflow-flow-datatransferapi-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''You can specify one of the following types:.

            - **AUTOMATIC** - The default. Optimizes a flow for datasets that fluctuate in size from small to large. For each flow run, Amazon AppFlow chooses to use the SYNC or ASYNC API type based on the amount of data that the run transfers.
            - **SYNC** - A synchronous API. This type of API optimizes a flow for small to medium-sized datasets.
            - **ASYNC** - An asynchronous API. This type of API optimizes a flow for large datasets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-datatransferapi.html#cfn-appflow-flow-datatransferapi-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataTransferApiProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.DatadogSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"object": "object"},
    )
    class DatadogSourcePropertiesProperty:
        def __init__(self, *, object: typing.Optional[builtins.str] = None) -> None:
            '''The properties that are applied when Datadog is being used as a source.

            :param object: The object specified in the Datadog flow source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-datadogsourceproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                datadog_source_properties_property = appflow_mixins.CfnFlowPropsMixin.DatadogSourcePropertiesProperty(
                    object="object"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c3131157fcb7022cc91f6632ca988c81c73a894b289593b2dcdda0efb30f6fa5)
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if object is not None:
                self._values["object"] = object

        @builtins.property
        def object(self) -> typing.Optional[builtins.str]:
            '''The object specified in the Datadog flow source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-datadogsourceproperties.html#cfn-appflow-flow-datadogsourceproperties-object
            '''
            result = self._values.get("object")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DatadogSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.DestinationConnectorPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "custom_connector": "customConnector",
            "event_bridge": "eventBridge",
            "lookout_metrics": "lookoutMetrics",
            "marketo": "marketo",
            "redshift": "redshift",
            "s3": "s3",
            "salesforce": "salesforce",
            "sapo_data": "sapoData",
            "snowflake": "snowflake",
            "upsolver": "upsolver",
            "zendesk": "zendesk",
        },
    )
    class DestinationConnectorPropertiesProperty:
        def __init__(
            self,
            *,
            custom_connector: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.CustomConnectorDestinationPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            event_bridge: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.EventBridgeDestinationPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            lookout_metrics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.LookoutMetricsDestinationPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            marketo: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.MarketoDestinationPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            redshift: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.RedshiftDestinationPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.S3DestinationPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            salesforce: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.SalesforceDestinationPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sapo_data: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.SAPODataDestinationPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            snowflake: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.SnowflakeDestinationPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            upsolver: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.UpsolverDestinationPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            zendesk: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.ZendeskDestinationPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''This stores the information that is required to query a particular connector.

            :param custom_connector: The properties that are required to query the custom Connector.
            :param event_bridge: The properties required to query Amazon EventBridge.
            :param lookout_metrics: The properties required to query Amazon Lookout for Metrics.
            :param marketo: The properties required to query Marketo.
            :param redshift: The properties required to query Amazon Redshift.
            :param s3: The properties required to query Amazon S3.
            :param salesforce: The properties required to query Salesforce.
            :param sapo_data: The properties required to query SAPOData.
            :param snowflake: The properties required to query Snowflake.
            :param upsolver: The properties required to query Upsolver.
            :param zendesk: The properties required to query Zendesk.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-destinationconnectorproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                destination_connector_properties_property = appflow_mixins.CfnFlowPropsMixin.DestinationConnectorPropertiesProperty(
                    custom_connector=appflow_mixins.CfnFlowPropsMixin.CustomConnectorDestinationPropertiesProperty(
                        custom_properties={
                            "custom_properties_key": "customProperties"
                        },
                        entity_name="entityName",
                        error_handling_config=appflow_mixins.CfnFlowPropsMixin.ErrorHandlingConfigProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix",
                            fail_on_first_error=False
                        ),
                        id_field_names=["idFieldNames"],
                        write_operation_type="writeOperationType"
                    ),
                    event_bridge=appflow_mixins.CfnFlowPropsMixin.EventBridgeDestinationPropertiesProperty(
                        error_handling_config=appflow_mixins.CfnFlowPropsMixin.ErrorHandlingConfigProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix",
                            fail_on_first_error=False
                        ),
                        object="object"
                    ),
                    lookout_metrics=appflow_mixins.CfnFlowPropsMixin.LookoutMetricsDestinationPropertiesProperty(
                        object="object"
                    ),
                    marketo=appflow_mixins.CfnFlowPropsMixin.MarketoDestinationPropertiesProperty(
                        error_handling_config=appflow_mixins.CfnFlowPropsMixin.ErrorHandlingConfigProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix",
                            fail_on_first_error=False
                        ),
                        object="object"
                    ),
                    redshift=appflow_mixins.CfnFlowPropsMixin.RedshiftDestinationPropertiesProperty(
                        bucket_prefix="bucketPrefix",
                        error_handling_config=appflow_mixins.CfnFlowPropsMixin.ErrorHandlingConfigProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix",
                            fail_on_first_error=False
                        ),
                        intermediate_bucket_name="intermediateBucketName",
                        object="object"
                    ),
                    s3=appflow_mixins.CfnFlowPropsMixin.S3DestinationPropertiesProperty(
                        bucket_name="bucketName",
                        bucket_prefix="bucketPrefix",
                        s3_output_format_config=appflow_mixins.CfnFlowPropsMixin.S3OutputFormatConfigProperty(
                            aggregation_config=appflow_mixins.CfnFlowPropsMixin.AggregationConfigProperty(
                                aggregation_type="aggregationType",
                                target_file_size=123
                            ),
                            file_type="fileType",
                            prefix_config=appflow_mixins.CfnFlowPropsMixin.PrefixConfigProperty(
                                path_prefix_hierarchy=["pathPrefixHierarchy"],
                                prefix_format="prefixFormat",
                                prefix_type="prefixType"
                            ),
                            preserve_source_data_typing=False
                        )
                    ),
                    salesforce=appflow_mixins.CfnFlowPropsMixin.SalesforceDestinationPropertiesProperty(
                        data_transfer_api="dataTransferApi",
                        error_handling_config=appflow_mixins.CfnFlowPropsMixin.ErrorHandlingConfigProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix",
                            fail_on_first_error=False
                        ),
                        id_field_names=["idFieldNames"],
                        object="object",
                        write_operation_type="writeOperationType"
                    ),
                    sapo_data=appflow_mixins.CfnFlowPropsMixin.SAPODataDestinationPropertiesProperty(
                        error_handling_config=appflow_mixins.CfnFlowPropsMixin.ErrorHandlingConfigProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix",
                            fail_on_first_error=False
                        ),
                        id_field_names=["idFieldNames"],
                        object_path="objectPath",
                        success_response_handling_config=appflow_mixins.CfnFlowPropsMixin.SuccessResponseHandlingConfigProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix"
                        ),
                        write_operation_type="writeOperationType"
                    ),
                    snowflake=appflow_mixins.CfnFlowPropsMixin.SnowflakeDestinationPropertiesProperty(
                        bucket_prefix="bucketPrefix",
                        error_handling_config=appflow_mixins.CfnFlowPropsMixin.ErrorHandlingConfigProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix",
                            fail_on_first_error=False
                        ),
                        intermediate_bucket_name="intermediateBucketName",
                        object="object"
                    ),
                    upsolver=appflow_mixins.CfnFlowPropsMixin.UpsolverDestinationPropertiesProperty(
                        bucket_name="bucketName",
                        bucket_prefix="bucketPrefix",
                        s3_output_format_config=appflow_mixins.CfnFlowPropsMixin.UpsolverS3OutputFormatConfigProperty(
                            aggregation_config=appflow_mixins.CfnFlowPropsMixin.AggregationConfigProperty(
                                aggregation_type="aggregationType",
                                target_file_size=123
                            ),
                            file_type="fileType",
                            prefix_config=appflow_mixins.CfnFlowPropsMixin.PrefixConfigProperty(
                                path_prefix_hierarchy=["pathPrefixHierarchy"],
                                prefix_format="prefixFormat",
                                prefix_type="prefixType"
                            )
                        )
                    ),
                    zendesk=appflow_mixins.CfnFlowPropsMixin.ZendeskDestinationPropertiesProperty(
                        error_handling_config=appflow_mixins.CfnFlowPropsMixin.ErrorHandlingConfigProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix",
                            fail_on_first_error=False
                        ),
                        id_field_names=["idFieldNames"],
                        object="object",
                        write_operation_type="writeOperationType"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__82264f976c13c1d2f4fd0cc33da6f943f7823cee1ed981a4cec76237e4894bf2)
                check_type(argname="argument custom_connector", value=custom_connector, expected_type=type_hints["custom_connector"])
                check_type(argname="argument event_bridge", value=event_bridge, expected_type=type_hints["event_bridge"])
                check_type(argname="argument lookout_metrics", value=lookout_metrics, expected_type=type_hints["lookout_metrics"])
                check_type(argname="argument marketo", value=marketo, expected_type=type_hints["marketo"])
                check_type(argname="argument redshift", value=redshift, expected_type=type_hints["redshift"])
                check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
                check_type(argname="argument salesforce", value=salesforce, expected_type=type_hints["salesforce"])
                check_type(argname="argument sapo_data", value=sapo_data, expected_type=type_hints["sapo_data"])
                check_type(argname="argument snowflake", value=snowflake, expected_type=type_hints["snowflake"])
                check_type(argname="argument upsolver", value=upsolver, expected_type=type_hints["upsolver"])
                check_type(argname="argument zendesk", value=zendesk, expected_type=type_hints["zendesk"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if custom_connector is not None:
                self._values["custom_connector"] = custom_connector
            if event_bridge is not None:
                self._values["event_bridge"] = event_bridge
            if lookout_metrics is not None:
                self._values["lookout_metrics"] = lookout_metrics
            if marketo is not None:
                self._values["marketo"] = marketo
            if redshift is not None:
                self._values["redshift"] = redshift
            if s3 is not None:
                self._values["s3"] = s3
            if salesforce is not None:
                self._values["salesforce"] = salesforce
            if sapo_data is not None:
                self._values["sapo_data"] = sapo_data
            if snowflake is not None:
                self._values["snowflake"] = snowflake
            if upsolver is not None:
                self._values["upsolver"] = upsolver
            if zendesk is not None:
                self._values["zendesk"] = zendesk

        @builtins.property
        def custom_connector(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.CustomConnectorDestinationPropertiesProperty"]]:
            '''The properties that are required to query the custom Connector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-destinationconnectorproperties.html#cfn-appflow-flow-destinationconnectorproperties-customconnector
            '''
            result = self._values.get("custom_connector")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.CustomConnectorDestinationPropertiesProperty"]], result)

        @builtins.property
        def event_bridge(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.EventBridgeDestinationPropertiesProperty"]]:
            '''The properties required to query Amazon EventBridge.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-destinationconnectorproperties.html#cfn-appflow-flow-destinationconnectorproperties-eventbridge
            '''
            result = self._values.get("event_bridge")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.EventBridgeDestinationPropertiesProperty"]], result)

        @builtins.property
        def lookout_metrics(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.LookoutMetricsDestinationPropertiesProperty"]]:
            '''The properties required to query Amazon Lookout for Metrics.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-destinationconnectorproperties.html#cfn-appflow-flow-destinationconnectorproperties-lookoutmetrics
            '''
            result = self._values.get("lookout_metrics")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.LookoutMetricsDestinationPropertiesProperty"]], result)

        @builtins.property
        def marketo(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.MarketoDestinationPropertiesProperty"]]:
            '''The properties required to query Marketo.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-destinationconnectorproperties.html#cfn-appflow-flow-destinationconnectorproperties-marketo
            '''
            result = self._values.get("marketo")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.MarketoDestinationPropertiesProperty"]], result)

        @builtins.property
        def redshift(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.RedshiftDestinationPropertiesProperty"]]:
            '''The properties required to query Amazon Redshift.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-destinationconnectorproperties.html#cfn-appflow-flow-destinationconnectorproperties-redshift
            '''
            result = self._values.get("redshift")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.RedshiftDestinationPropertiesProperty"]], result)

        @builtins.property
        def s3(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.S3DestinationPropertiesProperty"]]:
            '''The properties required to query Amazon S3.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-destinationconnectorproperties.html#cfn-appflow-flow-destinationconnectorproperties-s3
            '''
            result = self._values.get("s3")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.S3DestinationPropertiesProperty"]], result)

        @builtins.property
        def salesforce(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.SalesforceDestinationPropertiesProperty"]]:
            '''The properties required to query Salesforce.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-destinationconnectorproperties.html#cfn-appflow-flow-destinationconnectorproperties-salesforce
            '''
            result = self._values.get("salesforce")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.SalesforceDestinationPropertiesProperty"]], result)

        @builtins.property
        def sapo_data(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.SAPODataDestinationPropertiesProperty"]]:
            '''The properties required to query SAPOData.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-destinationconnectorproperties.html#cfn-appflow-flow-destinationconnectorproperties-sapodata
            '''
            result = self._values.get("sapo_data")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.SAPODataDestinationPropertiesProperty"]], result)

        @builtins.property
        def snowflake(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.SnowflakeDestinationPropertiesProperty"]]:
            '''The properties required to query Snowflake.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-destinationconnectorproperties.html#cfn-appflow-flow-destinationconnectorproperties-snowflake
            '''
            result = self._values.get("snowflake")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.SnowflakeDestinationPropertiesProperty"]], result)

        @builtins.property
        def upsolver(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.UpsolverDestinationPropertiesProperty"]]:
            '''The properties required to query Upsolver.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-destinationconnectorproperties.html#cfn-appflow-flow-destinationconnectorproperties-upsolver
            '''
            result = self._values.get("upsolver")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.UpsolverDestinationPropertiesProperty"]], result)

        @builtins.property
        def zendesk(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.ZendeskDestinationPropertiesProperty"]]:
            '''The properties required to query Zendesk.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-destinationconnectorproperties.html#cfn-appflow-flow-destinationconnectorproperties-zendesk
            '''
            result = self._values.get("zendesk")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.ZendeskDestinationPropertiesProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DestinationConnectorPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.DestinationFlowConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "api_version": "apiVersion",
            "connector_profile_name": "connectorProfileName",
            "connector_type": "connectorType",
            "destination_connector_properties": "destinationConnectorProperties",
        },
    )
    class DestinationFlowConfigProperty:
        def __init__(
            self,
            *,
            api_version: typing.Optional[builtins.str] = None,
            connector_profile_name: typing.Optional[builtins.str] = None,
            connector_type: typing.Optional[builtins.str] = None,
            destination_connector_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.DestinationConnectorPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains information about the configuration of destination connectors present in the flow.

            :param api_version: The API version that the destination connector uses.
            :param connector_profile_name: The name of the connector profile. This name must be unique for each connector profile in the AWS account .
            :param connector_type: The type of destination connector, such as Sales force, Amazon S3, and so on.
            :param destination_connector_properties: This stores the information that is required to query a particular connector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-destinationflowconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                destination_flow_config_property = appflow_mixins.CfnFlowPropsMixin.DestinationFlowConfigProperty(
                    api_version="apiVersion",
                    connector_profile_name="connectorProfileName",
                    connector_type="connectorType",
                    destination_connector_properties=appflow_mixins.CfnFlowPropsMixin.DestinationConnectorPropertiesProperty(
                        custom_connector=appflow_mixins.CfnFlowPropsMixin.CustomConnectorDestinationPropertiesProperty(
                            custom_properties={
                                "custom_properties_key": "customProperties"
                            },
                            entity_name="entityName",
                            error_handling_config=appflow_mixins.CfnFlowPropsMixin.ErrorHandlingConfigProperty(
                                bucket_name="bucketName",
                                bucket_prefix="bucketPrefix",
                                fail_on_first_error=False
                            ),
                            id_field_names=["idFieldNames"],
                            write_operation_type="writeOperationType"
                        ),
                        event_bridge=appflow_mixins.CfnFlowPropsMixin.EventBridgeDestinationPropertiesProperty(
                            error_handling_config=appflow_mixins.CfnFlowPropsMixin.ErrorHandlingConfigProperty(
                                bucket_name="bucketName",
                                bucket_prefix="bucketPrefix",
                                fail_on_first_error=False
                            ),
                            object="object"
                        ),
                        lookout_metrics=appflow_mixins.CfnFlowPropsMixin.LookoutMetricsDestinationPropertiesProperty(
                            object="object"
                        ),
                        marketo=appflow_mixins.CfnFlowPropsMixin.MarketoDestinationPropertiesProperty(
                            error_handling_config=appflow_mixins.CfnFlowPropsMixin.ErrorHandlingConfigProperty(
                                bucket_name="bucketName",
                                bucket_prefix="bucketPrefix",
                                fail_on_first_error=False
                            ),
                            object="object"
                        ),
                        redshift=appflow_mixins.CfnFlowPropsMixin.RedshiftDestinationPropertiesProperty(
                            bucket_prefix="bucketPrefix",
                            error_handling_config=appflow_mixins.CfnFlowPropsMixin.ErrorHandlingConfigProperty(
                                bucket_name="bucketName",
                                bucket_prefix="bucketPrefix",
                                fail_on_first_error=False
                            ),
                            intermediate_bucket_name="intermediateBucketName",
                            object="object"
                        ),
                        s3=appflow_mixins.CfnFlowPropsMixin.S3DestinationPropertiesProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix",
                            s3_output_format_config=appflow_mixins.CfnFlowPropsMixin.S3OutputFormatConfigProperty(
                                aggregation_config=appflow_mixins.CfnFlowPropsMixin.AggregationConfigProperty(
                                    aggregation_type="aggregationType",
                                    target_file_size=123
                                ),
                                file_type="fileType",
                                prefix_config=appflow_mixins.CfnFlowPropsMixin.PrefixConfigProperty(
                                    path_prefix_hierarchy=["pathPrefixHierarchy"],
                                    prefix_format="prefixFormat",
                                    prefix_type="prefixType"
                                ),
                                preserve_source_data_typing=False
                            )
                        ),
                        salesforce=appflow_mixins.CfnFlowPropsMixin.SalesforceDestinationPropertiesProperty(
                            data_transfer_api="dataTransferApi",
                            error_handling_config=appflow_mixins.CfnFlowPropsMixin.ErrorHandlingConfigProperty(
                                bucket_name="bucketName",
                                bucket_prefix="bucketPrefix",
                                fail_on_first_error=False
                            ),
                            id_field_names=["idFieldNames"],
                            object="object",
                            write_operation_type="writeOperationType"
                        ),
                        sapo_data=appflow_mixins.CfnFlowPropsMixin.SAPODataDestinationPropertiesProperty(
                            error_handling_config=appflow_mixins.CfnFlowPropsMixin.ErrorHandlingConfigProperty(
                                bucket_name="bucketName",
                                bucket_prefix="bucketPrefix",
                                fail_on_first_error=False
                            ),
                            id_field_names=["idFieldNames"],
                            object_path="objectPath",
                            success_response_handling_config=appflow_mixins.CfnFlowPropsMixin.SuccessResponseHandlingConfigProperty(
                                bucket_name="bucketName",
                                bucket_prefix="bucketPrefix"
                            ),
                            write_operation_type="writeOperationType"
                        ),
                        snowflake=appflow_mixins.CfnFlowPropsMixin.SnowflakeDestinationPropertiesProperty(
                            bucket_prefix="bucketPrefix",
                            error_handling_config=appflow_mixins.CfnFlowPropsMixin.ErrorHandlingConfigProperty(
                                bucket_name="bucketName",
                                bucket_prefix="bucketPrefix",
                                fail_on_first_error=False
                            ),
                            intermediate_bucket_name="intermediateBucketName",
                            object="object"
                        ),
                        upsolver=appflow_mixins.CfnFlowPropsMixin.UpsolverDestinationPropertiesProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix",
                            s3_output_format_config=appflow_mixins.CfnFlowPropsMixin.UpsolverS3OutputFormatConfigProperty(
                                aggregation_config=appflow_mixins.CfnFlowPropsMixin.AggregationConfigProperty(
                                    aggregation_type="aggregationType",
                                    target_file_size=123
                                ),
                                file_type="fileType",
                                prefix_config=appflow_mixins.CfnFlowPropsMixin.PrefixConfigProperty(
                                    path_prefix_hierarchy=["pathPrefixHierarchy"],
                                    prefix_format="prefixFormat",
                                    prefix_type="prefixType"
                                )
                            )
                        ),
                        zendesk=appflow_mixins.CfnFlowPropsMixin.ZendeskDestinationPropertiesProperty(
                            error_handling_config=appflow_mixins.CfnFlowPropsMixin.ErrorHandlingConfigProperty(
                                bucket_name="bucketName",
                                bucket_prefix="bucketPrefix",
                                fail_on_first_error=False
                            ),
                            id_field_names=["idFieldNames"],
                            object="object",
                            write_operation_type="writeOperationType"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c0c6cb1a11a4744b0ddec04a6a20c5ab48cff62bb192e8ee68ced63263548445)
                check_type(argname="argument api_version", value=api_version, expected_type=type_hints["api_version"])
                check_type(argname="argument connector_profile_name", value=connector_profile_name, expected_type=type_hints["connector_profile_name"])
                check_type(argname="argument connector_type", value=connector_type, expected_type=type_hints["connector_type"])
                check_type(argname="argument destination_connector_properties", value=destination_connector_properties, expected_type=type_hints["destination_connector_properties"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if api_version is not None:
                self._values["api_version"] = api_version
            if connector_profile_name is not None:
                self._values["connector_profile_name"] = connector_profile_name
            if connector_type is not None:
                self._values["connector_type"] = connector_type
            if destination_connector_properties is not None:
                self._values["destination_connector_properties"] = destination_connector_properties

        @builtins.property
        def api_version(self) -> typing.Optional[builtins.str]:
            '''The API version that the destination connector uses.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-destinationflowconfig.html#cfn-appflow-flow-destinationflowconfig-apiversion
            '''
            result = self._values.get("api_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def connector_profile_name(self) -> typing.Optional[builtins.str]:
            '''The name of the connector profile.

            This name must be unique for each connector profile in the AWS account .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-destinationflowconfig.html#cfn-appflow-flow-destinationflowconfig-connectorprofilename
            '''
            result = self._values.get("connector_profile_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def connector_type(self) -> typing.Optional[builtins.str]:
            '''The type of destination connector, such as Sales force, Amazon S3, and so on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-destinationflowconfig.html#cfn-appflow-flow-destinationflowconfig-connectortype
            '''
            result = self._values.get("connector_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def destination_connector_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.DestinationConnectorPropertiesProperty"]]:
            '''This stores the information that is required to query a particular connector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-destinationflowconfig.html#cfn-appflow-flow-destinationflowconfig-destinationconnectorproperties
            '''
            result = self._values.get("destination_connector_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.DestinationConnectorPropertiesProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DestinationFlowConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.DynatraceSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"object": "object"},
    )
    class DynatraceSourcePropertiesProperty:
        def __init__(self, *, object: typing.Optional[builtins.str] = None) -> None:
            '''The properties that are applied when Dynatrace is being used as a source.

            :param object: The object specified in the Dynatrace flow source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-dynatracesourceproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                dynatrace_source_properties_property = appflow_mixins.CfnFlowPropsMixin.DynatraceSourcePropertiesProperty(
                    object="object"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__230fd2d312288e46e403b645485df1d31fedf726b694ca0680d239d9e1193031)
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if object is not None:
                self._values["object"] = object

        @builtins.property
        def object(self) -> typing.Optional[builtins.str]:
            '''The object specified in the Dynatrace flow source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-dynatracesourceproperties.html#cfn-appflow-flow-dynatracesourceproperties-object
            '''
            result = self._values.get("object")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DynatraceSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.ErrorHandlingConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_name": "bucketName",
            "bucket_prefix": "bucketPrefix",
            "fail_on_first_error": "failOnFirstError",
        },
    )
    class ErrorHandlingConfigProperty:
        def __init__(
            self,
            *,
            bucket_name: typing.Optional[builtins.str] = None,
            bucket_prefix: typing.Optional[builtins.str] = None,
            fail_on_first_error: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The settings that determine how Amazon AppFlow handles an error when placing data in the destination.

            For example, this setting would determine if the flow should fail after one insertion error, or continue and attempt to insert every record regardless of the initial failure. ``ErrorHandlingConfig`` is a part of the destination connector details.

            :param bucket_name: Specifies the name of the Amazon S3 bucket.
            :param bucket_prefix: Specifies the Amazon S3 bucket prefix.
            :param fail_on_first_error: Specifies if the flow should fail after the first instance of a failure when attempting to place data in the destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-errorhandlingconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                error_handling_config_property = appflow_mixins.CfnFlowPropsMixin.ErrorHandlingConfigProperty(
                    bucket_name="bucketName",
                    bucket_prefix="bucketPrefix",
                    fail_on_first_error=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4065dce4d72c826afb191d7e5c205f49b7d4b79b630b1055b46d7d4affc0c363)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
                check_type(argname="argument fail_on_first_error", value=fail_on_first_error, expected_type=type_hints["fail_on_first_error"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_name is not None:
                self._values["bucket_name"] = bucket_name
            if bucket_prefix is not None:
                self._values["bucket_prefix"] = bucket_prefix
            if fail_on_first_error is not None:
                self._values["fail_on_first_error"] = fail_on_first_error

        @builtins.property
        def bucket_name(self) -> typing.Optional[builtins.str]:
            '''Specifies the name of the Amazon S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-errorhandlingconfig.html#cfn-appflow-flow-errorhandlingconfig-bucketname
            '''
            result = self._values.get("bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bucket_prefix(self) -> typing.Optional[builtins.str]:
            '''Specifies the Amazon S3 bucket prefix.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-errorhandlingconfig.html#cfn-appflow-flow-errorhandlingconfig-bucketprefix
            '''
            result = self._values.get("bucket_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def fail_on_first_error(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies if the flow should fail after the first instance of a failure when attempting to place data in the destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-errorhandlingconfig.html#cfn-appflow-flow-errorhandlingconfig-failonfirsterror
            '''
            result = self._values.get("fail_on_first_error")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ErrorHandlingConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.EventBridgeDestinationPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "error_handling_config": "errorHandlingConfig",
            "object": "object",
        },
    )
    class EventBridgeDestinationPropertiesProperty:
        def __init__(
            self,
            *,
            error_handling_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.ErrorHandlingConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            object: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The properties that are applied when Amazon EventBridge is being used as a destination.

            :param error_handling_config: The object specified in the Amplitude flow source.
            :param object: The object specified in the Amazon EventBridge flow destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-eventbridgedestinationproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                event_bridge_destination_properties_property = appflow_mixins.CfnFlowPropsMixin.EventBridgeDestinationPropertiesProperty(
                    error_handling_config=appflow_mixins.CfnFlowPropsMixin.ErrorHandlingConfigProperty(
                        bucket_name="bucketName",
                        bucket_prefix="bucketPrefix",
                        fail_on_first_error=False
                    ),
                    object="object"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__91769fd2a2e5ba352dcfe82d3a2351114da4a3aa609ecc97faa422a432e0ed4f)
                check_type(argname="argument error_handling_config", value=error_handling_config, expected_type=type_hints["error_handling_config"])
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if error_handling_config is not None:
                self._values["error_handling_config"] = error_handling_config
            if object is not None:
                self._values["object"] = object

        @builtins.property
        def error_handling_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.ErrorHandlingConfigProperty"]]:
            '''The object specified in the Amplitude flow source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-eventbridgedestinationproperties.html#cfn-appflow-flow-eventbridgedestinationproperties-errorhandlingconfig
            '''
            result = self._values.get("error_handling_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.ErrorHandlingConfigProperty"]], result)

        @builtins.property
        def object(self) -> typing.Optional[builtins.str]:
            '''The object specified in the Amazon EventBridge flow destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-eventbridgedestinationproperties.html#cfn-appflow-flow-eventbridgedestinationproperties-object
            '''
            result = self._values.get("object")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventBridgeDestinationPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.GlueDataCatalogProperty",
        jsii_struct_bases=[],
        name_mapping={
            "database_name": "databaseName",
            "role_arn": "roleArn",
            "table_prefix": "tablePrefix",
        },
    )
    class GlueDataCatalogProperty:
        def __init__(
            self,
            *,
            database_name: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
            table_prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Trigger settings of the flow.

            :param database_name: A string containing the value for the tag.
            :param role_arn: A string containing the value for the tag.
            :param table_prefix: A string containing the value for the tag.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-gluedatacatalog.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                glue_data_catalog_property = appflow_mixins.CfnFlowPropsMixin.GlueDataCatalogProperty(
                    database_name="databaseName",
                    role_arn="roleArn",
                    table_prefix="tablePrefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6e5b8c56e9f469ca6ed7056151eb4e985ccbf952270662668a90610fc16fff47)
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument table_prefix", value=table_prefix, expected_type=type_hints["table_prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if database_name is not None:
                self._values["database_name"] = database_name
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if table_prefix is not None:
                self._values["table_prefix"] = table_prefix

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            '''A string containing the value for the tag.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-gluedatacatalog.html#cfn-appflow-flow-gluedatacatalog-databasename
            '''
            result = self._values.get("database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''A string containing the value for the tag.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-gluedatacatalog.html#cfn-appflow-flow-gluedatacatalog-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def table_prefix(self) -> typing.Optional[builtins.str]:
            '''A string containing the value for the tag.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-gluedatacatalog.html#cfn-appflow-flow-gluedatacatalog-tableprefix
            '''
            result = self._values.get("table_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GlueDataCatalogProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.GoogleAnalyticsSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"object": "object"},
    )
    class GoogleAnalyticsSourcePropertiesProperty:
        def __init__(self, *, object: typing.Optional[builtins.str] = None) -> None:
            '''The properties that are applied when Google Analytics is being used as a source.

            :param object: The object specified in the Google Analytics flow source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-googleanalyticssourceproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                google_analytics_source_properties_property = appflow_mixins.CfnFlowPropsMixin.GoogleAnalyticsSourcePropertiesProperty(
                    object="object"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c57fecab276c04362dedb9aa45b2664e1d0c73d24cbeb270702b15c53af04b1f)
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if object is not None:
                self._values["object"] = object

        @builtins.property
        def object(self) -> typing.Optional[builtins.str]:
            '''The object specified in the Google Analytics flow source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-googleanalyticssourceproperties.html#cfn-appflow-flow-googleanalyticssourceproperties-object
            '''
            result = self._values.get("object")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GoogleAnalyticsSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.IncrementalPullConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"datetime_type_field_name": "datetimeTypeFieldName"},
    )
    class IncrementalPullConfigProperty:
        def __init__(
            self,
            *,
            datetime_type_field_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the configuration used when importing incremental records from the source.

            :param datetime_type_field_name: A field that specifies the date time or timestamp field as the criteria to use when importing incremental records from the source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-incrementalpullconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                incremental_pull_config_property = appflow_mixins.CfnFlowPropsMixin.IncrementalPullConfigProperty(
                    datetime_type_field_name="datetimeTypeFieldName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1c391fc6658aeec845d9832ec03c3c0551bda52952cb0b07fad03d150ed811de)
                check_type(argname="argument datetime_type_field_name", value=datetime_type_field_name, expected_type=type_hints["datetime_type_field_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if datetime_type_field_name is not None:
                self._values["datetime_type_field_name"] = datetime_type_field_name

        @builtins.property
        def datetime_type_field_name(self) -> typing.Optional[builtins.str]:
            '''A field that specifies the date time or timestamp field as the criteria to use when importing incremental records from the source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-incrementalpullconfig.html#cfn-appflow-flow-incrementalpullconfig-datetimetypefieldname
            '''
            result = self._values.get("datetime_type_field_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IncrementalPullConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.InforNexusSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"object": "object"},
    )
    class InforNexusSourcePropertiesProperty:
        def __init__(self, *, object: typing.Optional[builtins.str] = None) -> None:
            '''The properties that are applied when Infor Nexus is being used as a source.

            :param object: The object specified in the Infor Nexus flow source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-infornexussourceproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                infor_nexus_source_properties_property = appflow_mixins.CfnFlowPropsMixin.InforNexusSourcePropertiesProperty(
                    object="object"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2ab075e0721a114cd264c2300b3e7b3065266f858d3c013f15c22f182e7abcdf)
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if object is not None:
                self._values["object"] = object

        @builtins.property
        def object(self) -> typing.Optional[builtins.str]:
            '''The object specified in the Infor Nexus flow source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-infornexussourceproperties.html#cfn-appflow-flow-infornexussourceproperties-object
            '''
            result = self._values.get("object")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InforNexusSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.LookoutMetricsDestinationPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"object": "object"},
    )
    class LookoutMetricsDestinationPropertiesProperty:
        def __init__(self, *, object: typing.Optional[builtins.str] = None) -> None:
            '''The properties that are applied when Amazon Lookout for Metrics is used as a destination.

            :param object: The object specified in the Amazon Lookout for Metrics flow destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-lookoutmetricsdestinationproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                lookout_metrics_destination_properties_property = appflow_mixins.CfnFlowPropsMixin.LookoutMetricsDestinationPropertiesProperty(
                    object="object"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f75576f4a7df4defda9b8d3439b3daaadd07fd8a04de852f2a5a0d42f7e936d1)
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if object is not None:
                self._values["object"] = object

        @builtins.property
        def object(self) -> typing.Optional[builtins.str]:
            '''The object specified in the Amazon Lookout for Metrics flow destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-lookoutmetricsdestinationproperties.html#cfn-appflow-flow-lookoutmetricsdestinationproperties-object
            '''
            result = self._values.get("object")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LookoutMetricsDestinationPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.MarketoDestinationPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "error_handling_config": "errorHandlingConfig",
            "object": "object",
        },
    )
    class MarketoDestinationPropertiesProperty:
        def __init__(
            self,
            *,
            error_handling_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.ErrorHandlingConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            object: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The properties that Amazon AppFlow applies when you use Marketo as a flow destination.

            :param error_handling_config: The settings that determine how Amazon AppFlow handles an error when placing data in the destination. For example, this setting would determine if the flow should fail after one insertion error, or continue and attempt to insert every record regardless of the initial failure. ``ErrorHandlingConfig`` is a part of the destination connector details.
            :param object: The object specified in the Marketo flow destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-marketodestinationproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                marketo_destination_properties_property = appflow_mixins.CfnFlowPropsMixin.MarketoDestinationPropertiesProperty(
                    error_handling_config=appflow_mixins.CfnFlowPropsMixin.ErrorHandlingConfigProperty(
                        bucket_name="bucketName",
                        bucket_prefix="bucketPrefix",
                        fail_on_first_error=False
                    ),
                    object="object"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a032965665352407c05567bbc0542e3603006cc1e91df1a65d220dc914e83232)
                check_type(argname="argument error_handling_config", value=error_handling_config, expected_type=type_hints["error_handling_config"])
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if error_handling_config is not None:
                self._values["error_handling_config"] = error_handling_config
            if object is not None:
                self._values["object"] = object

        @builtins.property
        def error_handling_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.ErrorHandlingConfigProperty"]]:
            '''The settings that determine how Amazon AppFlow handles an error when placing data in the destination.

            For example, this setting would determine if the flow should fail after one insertion error, or continue and attempt to insert every record regardless of the initial failure. ``ErrorHandlingConfig`` is a part of the destination connector details.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-marketodestinationproperties.html#cfn-appflow-flow-marketodestinationproperties-errorhandlingconfig
            '''
            result = self._values.get("error_handling_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.ErrorHandlingConfigProperty"]], result)

        @builtins.property
        def object(self) -> typing.Optional[builtins.str]:
            '''The object specified in the Marketo flow destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-marketodestinationproperties.html#cfn-appflow-flow-marketodestinationproperties-object
            '''
            result = self._values.get("object")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MarketoDestinationPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.MarketoSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"object": "object"},
    )
    class MarketoSourcePropertiesProperty:
        def __init__(self, *, object: typing.Optional[builtins.str] = None) -> None:
            '''The properties that are applied when Marketo is being used as a source.

            :param object: The object specified in the Marketo flow source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-marketosourceproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                marketo_source_properties_property = appflow_mixins.CfnFlowPropsMixin.MarketoSourcePropertiesProperty(
                    object="object"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d3e08ff283d02957c52927dd1b19805cee773593c794ef2d18513c29cbe0f13f)
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if object is not None:
                self._values["object"] = object

        @builtins.property
        def object(self) -> typing.Optional[builtins.str]:
            '''The object specified in the Marketo flow source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-marketosourceproperties.html#cfn-appflow-flow-marketosourceproperties-object
            '''
            result = self._values.get("object")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MarketoSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.MetadataCatalogConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"glue_data_catalog": "glueDataCatalog"},
    )
    class MetadataCatalogConfigProperty:
        def __init__(
            self,
            *,
            glue_data_catalog: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.GlueDataCatalogProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the configuration that Amazon AppFlow uses when it catalogs your data.

            When Amazon AppFlow catalogs your data, it stores metadata in a data catalog.

            :param glue_data_catalog: Specifies the configuration that Amazon AppFlow uses when it catalogs your data with the AWS Glue Data Catalog .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-metadatacatalogconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                metadata_catalog_config_property = appflow_mixins.CfnFlowPropsMixin.MetadataCatalogConfigProperty(
                    glue_data_catalog=appflow_mixins.CfnFlowPropsMixin.GlueDataCatalogProperty(
                        database_name="databaseName",
                        role_arn="roleArn",
                        table_prefix="tablePrefix"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5e8f0aff3574c300354ec0e97f9aee4605c9b2d7f82973165b9466b47993d64d)
                check_type(argname="argument glue_data_catalog", value=glue_data_catalog, expected_type=type_hints["glue_data_catalog"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if glue_data_catalog is not None:
                self._values["glue_data_catalog"] = glue_data_catalog

        @builtins.property
        def glue_data_catalog(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.GlueDataCatalogProperty"]]:
            '''Specifies the configuration that Amazon AppFlow uses when it catalogs your data with the AWS Glue Data Catalog .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-metadatacatalogconfig.html#cfn-appflow-flow-metadatacatalogconfig-gluedatacatalog
            '''
            result = self._values.get("glue_data_catalog")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.GlueDataCatalogProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetadataCatalogConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.PardotSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"object": "object"},
    )
    class PardotSourcePropertiesProperty:
        def __init__(self, *, object: typing.Optional[builtins.str] = None) -> None:
            '''The properties that are applied when Salesforce Pardot is being used as a source.

            :param object: The object specified in the Salesforce Pardot flow source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-pardotsourceproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                pardot_source_properties_property = appflow_mixins.CfnFlowPropsMixin.PardotSourcePropertiesProperty(
                    object="object"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a8f87275ad5594ba16ab4c0e439b6f31f310425a0db994a6505780d974b618cc)
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if object is not None:
                self._values["object"] = object

        @builtins.property
        def object(self) -> typing.Optional[builtins.str]:
            '''The object specified in the Salesforce Pardot flow source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-pardotsourceproperties.html#cfn-appflow-flow-pardotsourceproperties-object
            '''
            result = self._values.get("object")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PardotSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.PrefixConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "path_prefix_hierarchy": "pathPrefixHierarchy",
            "prefix_format": "prefixFormat",
            "prefix_type": "prefixType",
        },
    )
    class PrefixConfigProperty:
        def __init__(
            self,
            *,
            path_prefix_hierarchy: typing.Optional[typing.Sequence[builtins.str]] = None,
            prefix_format: typing.Optional[builtins.str] = None,
            prefix_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies elements that Amazon AppFlow includes in the file and folder names in the flow destination.

            :param path_prefix_hierarchy: Specifies whether the destination file path includes either or both of the following elements:. - **EXECUTION_ID** - The ID that Amazon AppFlow assigns to the flow run. - **SCHEMA_VERSION** - The version number of your data schema. Amazon AppFlow assigns this version number. The version number increases by one when you change any of the following settings in your flow configuration: - Source-to-destination field mappings - Field data types - Partition keys
            :param prefix_format: Determines the level of granularity for the date and time that's included in the prefix.
            :param prefix_type: Determines the format of the prefix, and whether it applies to the file name, file path, or both.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-prefixconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                prefix_config_property = appflow_mixins.CfnFlowPropsMixin.PrefixConfigProperty(
                    path_prefix_hierarchy=["pathPrefixHierarchy"],
                    prefix_format="prefixFormat",
                    prefix_type="prefixType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4918cb993dc2b15c90f54d46fa3e513eeaa934b9df15c67cd9b6c0236db7728a)
                check_type(argname="argument path_prefix_hierarchy", value=path_prefix_hierarchy, expected_type=type_hints["path_prefix_hierarchy"])
                check_type(argname="argument prefix_format", value=prefix_format, expected_type=type_hints["prefix_format"])
                check_type(argname="argument prefix_type", value=prefix_type, expected_type=type_hints["prefix_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if path_prefix_hierarchy is not None:
                self._values["path_prefix_hierarchy"] = path_prefix_hierarchy
            if prefix_format is not None:
                self._values["prefix_format"] = prefix_format
            if prefix_type is not None:
                self._values["prefix_type"] = prefix_type

        @builtins.property
        def path_prefix_hierarchy(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Specifies whether the destination file path includes either or both of the following elements:.

            - **EXECUTION_ID** - The ID that Amazon AppFlow assigns to the flow run.
            - **SCHEMA_VERSION** - The version number of your data schema. Amazon AppFlow assigns this version number. The version number increases by one when you change any of the following settings in your flow configuration:
            - Source-to-destination field mappings
            - Field data types
            - Partition keys

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-prefixconfig.html#cfn-appflow-flow-prefixconfig-pathprefixhierarchy
            '''
            result = self._values.get("path_prefix_hierarchy")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def prefix_format(self) -> typing.Optional[builtins.str]:
            '''Determines the level of granularity for the date and time that's included in the prefix.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-prefixconfig.html#cfn-appflow-flow-prefixconfig-prefixformat
            '''
            result = self._values.get("prefix_format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prefix_type(self) -> typing.Optional[builtins.str]:
            '''Determines the format of the prefix, and whether it applies to the file name, file path, or both.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-prefixconfig.html#cfn-appflow-flow-prefixconfig-prefixtype
            '''
            result = self._values.get("prefix_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PrefixConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.RedshiftDestinationPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_prefix": "bucketPrefix",
            "error_handling_config": "errorHandlingConfig",
            "intermediate_bucket_name": "intermediateBucketName",
            "object": "object",
        },
    )
    class RedshiftDestinationPropertiesProperty:
        def __init__(
            self,
            *,
            bucket_prefix: typing.Optional[builtins.str] = None,
            error_handling_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.ErrorHandlingConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            intermediate_bucket_name: typing.Optional[builtins.str] = None,
            object: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The properties that are applied when Amazon Redshift is being used as a destination.

            :param bucket_prefix: The object key for the bucket in which Amazon AppFlow places the destination files.
            :param error_handling_config: The settings that determine how Amazon AppFlow handles an error when placing data in the Amazon Redshift destination. For example, this setting would determine if the flow should fail after one insertion error, or continue and attempt to insert every record regardless of the initial failure. ``ErrorHandlingConfig`` is a part of the destination connector details.
            :param intermediate_bucket_name: The intermediate bucket that Amazon AppFlow uses when moving data into Amazon Redshift.
            :param object: The object specified in the Amazon Redshift flow destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-redshiftdestinationproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                redshift_destination_properties_property = appflow_mixins.CfnFlowPropsMixin.RedshiftDestinationPropertiesProperty(
                    bucket_prefix="bucketPrefix",
                    error_handling_config=appflow_mixins.CfnFlowPropsMixin.ErrorHandlingConfigProperty(
                        bucket_name="bucketName",
                        bucket_prefix="bucketPrefix",
                        fail_on_first_error=False
                    ),
                    intermediate_bucket_name="intermediateBucketName",
                    object="object"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__050232b583fbe45b3f1fbd8985b229d9828a9f7a15aa2d5750849b19b0d7d043)
                check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
                check_type(argname="argument error_handling_config", value=error_handling_config, expected_type=type_hints["error_handling_config"])
                check_type(argname="argument intermediate_bucket_name", value=intermediate_bucket_name, expected_type=type_hints["intermediate_bucket_name"])
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_prefix is not None:
                self._values["bucket_prefix"] = bucket_prefix
            if error_handling_config is not None:
                self._values["error_handling_config"] = error_handling_config
            if intermediate_bucket_name is not None:
                self._values["intermediate_bucket_name"] = intermediate_bucket_name
            if object is not None:
                self._values["object"] = object

        @builtins.property
        def bucket_prefix(self) -> typing.Optional[builtins.str]:
            '''The object key for the bucket in which Amazon AppFlow places the destination files.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-redshiftdestinationproperties.html#cfn-appflow-flow-redshiftdestinationproperties-bucketprefix
            '''
            result = self._values.get("bucket_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def error_handling_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.ErrorHandlingConfigProperty"]]:
            '''The settings that determine how Amazon AppFlow handles an error when placing data in the Amazon Redshift destination.

            For example, this setting would determine if the flow should fail after one insertion error, or continue and attempt to insert every record regardless of the initial failure. ``ErrorHandlingConfig`` is a part of the destination connector details.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-redshiftdestinationproperties.html#cfn-appflow-flow-redshiftdestinationproperties-errorhandlingconfig
            '''
            result = self._values.get("error_handling_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.ErrorHandlingConfigProperty"]], result)

        @builtins.property
        def intermediate_bucket_name(self) -> typing.Optional[builtins.str]:
            '''The intermediate bucket that Amazon AppFlow uses when moving data into Amazon Redshift.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-redshiftdestinationproperties.html#cfn-appflow-flow-redshiftdestinationproperties-intermediatebucketname
            '''
            result = self._values.get("intermediate_bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def object(self) -> typing.Optional[builtins.str]:
            '''The object specified in the Amazon Redshift flow destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-redshiftdestinationproperties.html#cfn-appflow-flow-redshiftdestinationproperties-object
            '''
            result = self._values.get("object")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RedshiftDestinationPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.S3DestinationPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_name": "bucketName",
            "bucket_prefix": "bucketPrefix",
            "s3_output_format_config": "s3OutputFormatConfig",
        },
    )
    class S3DestinationPropertiesProperty:
        def __init__(
            self,
            *,
            bucket_name: typing.Optional[builtins.str] = None,
            bucket_prefix: typing.Optional[builtins.str] = None,
            s3_output_format_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.S3OutputFormatConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The properties that are applied when Amazon S3 is used as a destination.

            :param bucket_name: The Amazon S3 bucket name in which Amazon AppFlow places the transferred data.
            :param bucket_prefix: The object key for the destination bucket in which Amazon AppFlow places the files.
            :param s3_output_format_config: The configuration that determines how Amazon AppFlow should format the flow output data when Amazon S3 is used as the destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-s3destinationproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                s3_destination_properties_property = appflow_mixins.CfnFlowPropsMixin.S3DestinationPropertiesProperty(
                    bucket_name="bucketName",
                    bucket_prefix="bucketPrefix",
                    s3_output_format_config=appflow_mixins.CfnFlowPropsMixin.S3OutputFormatConfigProperty(
                        aggregation_config=appflow_mixins.CfnFlowPropsMixin.AggregationConfigProperty(
                            aggregation_type="aggregationType",
                            target_file_size=123
                        ),
                        file_type="fileType",
                        prefix_config=appflow_mixins.CfnFlowPropsMixin.PrefixConfigProperty(
                            path_prefix_hierarchy=["pathPrefixHierarchy"],
                            prefix_format="prefixFormat",
                            prefix_type="prefixType"
                        ),
                        preserve_source_data_typing=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0d7a2315dd70b0fdb4076ef6ae297b0d6c7906fc0d3aeb992977332cb7eddd6d)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
                check_type(argname="argument s3_output_format_config", value=s3_output_format_config, expected_type=type_hints["s3_output_format_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_name is not None:
                self._values["bucket_name"] = bucket_name
            if bucket_prefix is not None:
                self._values["bucket_prefix"] = bucket_prefix
            if s3_output_format_config is not None:
                self._values["s3_output_format_config"] = s3_output_format_config

        @builtins.property
        def bucket_name(self) -> typing.Optional[builtins.str]:
            '''The Amazon S3 bucket name in which Amazon AppFlow places the transferred data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-s3destinationproperties.html#cfn-appflow-flow-s3destinationproperties-bucketname
            '''
            result = self._values.get("bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bucket_prefix(self) -> typing.Optional[builtins.str]:
            '''The object key for the destination bucket in which Amazon AppFlow places the files.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-s3destinationproperties.html#cfn-appflow-flow-s3destinationproperties-bucketprefix
            '''
            result = self._values.get("bucket_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_output_format_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.S3OutputFormatConfigProperty"]]:
            '''The configuration that determines how Amazon AppFlow should format the flow output data when Amazon S3 is used as the destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-s3destinationproperties.html#cfn-appflow-flow-s3destinationproperties-s3outputformatconfig
            '''
            result = self._values.get("s3_output_format_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.S3OutputFormatConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3DestinationPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.S3InputFormatConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_input_file_type": "s3InputFileType"},
    )
    class S3InputFormatConfigProperty:
        def __init__(
            self,
            *,
            s3_input_file_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''When you use Amazon S3 as the source, the configuration format that you provide the flow input data.

            :param s3_input_file_type: The file type that Amazon AppFlow gets from your Amazon S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-s3inputformatconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                s3_input_format_config_property = appflow_mixins.CfnFlowPropsMixin.S3InputFormatConfigProperty(
                    s3_input_file_type="s3InputFileType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9f0da923523d1ecf8325831f2ae1af46e4d7b6f3d2bf05afff6ec0750355393c)
                check_type(argname="argument s3_input_file_type", value=s3_input_file_type, expected_type=type_hints["s3_input_file_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3_input_file_type is not None:
                self._values["s3_input_file_type"] = s3_input_file_type

        @builtins.property
        def s3_input_file_type(self) -> typing.Optional[builtins.str]:
            '''The file type that Amazon AppFlow gets from your Amazon S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-s3inputformatconfig.html#cfn-appflow-flow-s3inputformatconfig-s3inputfiletype
            '''
            result = self._values.get("s3_input_file_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3InputFormatConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.S3OutputFormatConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "aggregation_config": "aggregationConfig",
            "file_type": "fileType",
            "prefix_config": "prefixConfig",
            "preserve_source_data_typing": "preserveSourceDataTyping",
        },
    )
    class S3OutputFormatConfigProperty:
        def __init__(
            self,
            *,
            aggregation_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.AggregationConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            file_type: typing.Optional[builtins.str] = None,
            prefix_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.PrefixConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            preserve_source_data_typing: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The configuration that determines how Amazon AppFlow should format the flow output data when Amazon S3 is used as the destination.

            :param aggregation_config: The aggregation settings that you can use to customize the output format of your flow data.
            :param file_type: Indicates the file type that Amazon AppFlow places in the Amazon S3 bucket.
            :param prefix_config: Determines the prefix that Amazon AppFlow applies to the folder name in the Amazon S3 bucket. You can name folders according to the flow frequency and date.
            :param preserve_source_data_typing: If your file output format is Parquet, use this parameter to set whether Amazon AppFlow preserves the data types in your source data when it writes the output to Amazon S3. - ``true`` : Amazon AppFlow preserves the data types when it writes to Amazon S3. For example, an integer or ``1`` in your source data is still an integer in your output. - ``false`` : Amazon AppFlow converts all of the source data into strings when it writes to Amazon S3. For example, an integer of ``1`` in your source data becomes the string ``"1"`` in the output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-s3outputformatconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                s3_output_format_config_property = appflow_mixins.CfnFlowPropsMixin.S3OutputFormatConfigProperty(
                    aggregation_config=appflow_mixins.CfnFlowPropsMixin.AggregationConfigProperty(
                        aggregation_type="aggregationType",
                        target_file_size=123
                    ),
                    file_type="fileType",
                    prefix_config=appflow_mixins.CfnFlowPropsMixin.PrefixConfigProperty(
                        path_prefix_hierarchy=["pathPrefixHierarchy"],
                        prefix_format="prefixFormat",
                        prefix_type="prefixType"
                    ),
                    preserve_source_data_typing=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__11017116846bda1d4f21a1c8ec35e3f18faf07a1c2fda0214a8f9218d6fb8aee)
                check_type(argname="argument aggregation_config", value=aggregation_config, expected_type=type_hints["aggregation_config"])
                check_type(argname="argument file_type", value=file_type, expected_type=type_hints["file_type"])
                check_type(argname="argument prefix_config", value=prefix_config, expected_type=type_hints["prefix_config"])
                check_type(argname="argument preserve_source_data_typing", value=preserve_source_data_typing, expected_type=type_hints["preserve_source_data_typing"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if aggregation_config is not None:
                self._values["aggregation_config"] = aggregation_config
            if file_type is not None:
                self._values["file_type"] = file_type
            if prefix_config is not None:
                self._values["prefix_config"] = prefix_config
            if preserve_source_data_typing is not None:
                self._values["preserve_source_data_typing"] = preserve_source_data_typing

        @builtins.property
        def aggregation_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.AggregationConfigProperty"]]:
            '''The aggregation settings that you can use to customize the output format of your flow data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-s3outputformatconfig.html#cfn-appflow-flow-s3outputformatconfig-aggregationconfig
            '''
            result = self._values.get("aggregation_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.AggregationConfigProperty"]], result)

        @builtins.property
        def file_type(self) -> typing.Optional[builtins.str]:
            '''Indicates the file type that Amazon AppFlow places in the Amazon S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-s3outputformatconfig.html#cfn-appflow-flow-s3outputformatconfig-filetype
            '''
            result = self._values.get("file_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prefix_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.PrefixConfigProperty"]]:
            '''Determines the prefix that Amazon AppFlow applies to the folder name in the Amazon S3 bucket.

            You can name folders according to the flow frequency and date.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-s3outputformatconfig.html#cfn-appflow-flow-s3outputformatconfig-prefixconfig
            '''
            result = self._values.get("prefix_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.PrefixConfigProperty"]], result)

        @builtins.property
        def preserve_source_data_typing(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If your file output format is Parquet, use this parameter to set whether Amazon AppFlow preserves the data types in your source data when it writes the output to Amazon S3.

            - ``true`` : Amazon AppFlow preserves the data types when it writes to Amazon S3. For example, an integer or ``1`` in your source data is still an integer in your output.
            - ``false`` : Amazon AppFlow converts all of the source data into strings when it writes to Amazon S3. For example, an integer of ``1`` in your source data becomes the string ``"1"`` in the output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-s3outputformatconfig.html#cfn-appflow-flow-s3outputformatconfig-preservesourcedatatyping
            '''
            result = self._values.get("preserve_source_data_typing")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3OutputFormatConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.S3SourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_name": "bucketName",
            "bucket_prefix": "bucketPrefix",
            "s3_input_format_config": "s3InputFormatConfig",
        },
    )
    class S3SourcePropertiesProperty:
        def __init__(
            self,
            *,
            bucket_name: typing.Optional[builtins.str] = None,
            bucket_prefix: typing.Optional[builtins.str] = None,
            s3_input_format_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.S3InputFormatConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The properties that are applied when Amazon S3 is being used as the flow source.

            :param bucket_name: The Amazon S3 bucket name where the source files are stored.
            :param bucket_prefix: The object key for the Amazon S3 bucket in which the source files are stored.
            :param s3_input_format_config: When you use Amazon S3 as the source, the configuration format that you provide the flow input data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-s3sourceproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                s3_source_properties_property = appflow_mixins.CfnFlowPropsMixin.S3SourcePropertiesProperty(
                    bucket_name="bucketName",
                    bucket_prefix="bucketPrefix",
                    s3_input_format_config=appflow_mixins.CfnFlowPropsMixin.S3InputFormatConfigProperty(
                        s3_input_file_type="s3InputFileType"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b608c2f0272c79d437e7860b11877a30347d41fad50c5471aa0d7fda8836d836)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
                check_type(argname="argument s3_input_format_config", value=s3_input_format_config, expected_type=type_hints["s3_input_format_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_name is not None:
                self._values["bucket_name"] = bucket_name
            if bucket_prefix is not None:
                self._values["bucket_prefix"] = bucket_prefix
            if s3_input_format_config is not None:
                self._values["s3_input_format_config"] = s3_input_format_config

        @builtins.property
        def bucket_name(self) -> typing.Optional[builtins.str]:
            '''The Amazon S3 bucket name where the source files are stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-s3sourceproperties.html#cfn-appflow-flow-s3sourceproperties-bucketname
            '''
            result = self._values.get("bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bucket_prefix(self) -> typing.Optional[builtins.str]:
            '''The object key for the Amazon S3 bucket in which the source files are stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-s3sourceproperties.html#cfn-appflow-flow-s3sourceproperties-bucketprefix
            '''
            result = self._values.get("bucket_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_input_format_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.S3InputFormatConfigProperty"]]:
            '''When you use Amazon S3 as the source, the configuration format that you provide the flow input data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-s3sourceproperties.html#cfn-appflow-flow-s3sourceproperties-s3inputformatconfig
            '''
            result = self._values.get("s3_input_format_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.S3InputFormatConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3SourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.SAPODataDestinationPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "error_handling_config": "errorHandlingConfig",
            "id_field_names": "idFieldNames",
            "object_path": "objectPath",
            "success_response_handling_config": "successResponseHandlingConfig",
            "write_operation_type": "writeOperationType",
        },
    )
    class SAPODataDestinationPropertiesProperty:
        def __init__(
            self,
            *,
            error_handling_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.ErrorHandlingConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            id_field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
            object_path: typing.Optional[builtins.str] = None,
            success_response_handling_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.SuccessResponseHandlingConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            write_operation_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The properties that are applied when using SAPOData as a flow destination.

            :param error_handling_config: The settings that determine how Amazon AppFlow handles an error when placing data in the destination. For example, this setting would determine if the flow should fail after one insertion error, or continue and attempt to insert every record regardless of the initial failure. ``ErrorHandlingConfig`` is a part of the destination connector details.
            :param id_field_names: A list of field names that can be used as an ID field when performing a write operation.
            :param object_path: The object path specified in the SAPOData flow destination.
            :param success_response_handling_config: Determines how Amazon AppFlow handles the success response that it gets from the connector after placing data. For example, this setting would determine where to write the response from a destination connector upon a successful insert operation.
            :param write_operation_type: The possible write operations in the destination connector. When this value is not provided, this defaults to the ``INSERT`` operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sapodatadestinationproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                s_aPOData_destination_properties_property = appflow_mixins.CfnFlowPropsMixin.SAPODataDestinationPropertiesProperty(
                    error_handling_config=appflow_mixins.CfnFlowPropsMixin.ErrorHandlingConfigProperty(
                        bucket_name="bucketName",
                        bucket_prefix="bucketPrefix",
                        fail_on_first_error=False
                    ),
                    id_field_names=["idFieldNames"],
                    object_path="objectPath",
                    success_response_handling_config=appflow_mixins.CfnFlowPropsMixin.SuccessResponseHandlingConfigProperty(
                        bucket_name="bucketName",
                        bucket_prefix="bucketPrefix"
                    ),
                    write_operation_type="writeOperationType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__63d045e8c1d465903b7d12bcdfee49f3dadeb1582165f5549befa3cea1784201)
                check_type(argname="argument error_handling_config", value=error_handling_config, expected_type=type_hints["error_handling_config"])
                check_type(argname="argument id_field_names", value=id_field_names, expected_type=type_hints["id_field_names"])
                check_type(argname="argument object_path", value=object_path, expected_type=type_hints["object_path"])
                check_type(argname="argument success_response_handling_config", value=success_response_handling_config, expected_type=type_hints["success_response_handling_config"])
                check_type(argname="argument write_operation_type", value=write_operation_type, expected_type=type_hints["write_operation_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if error_handling_config is not None:
                self._values["error_handling_config"] = error_handling_config
            if id_field_names is not None:
                self._values["id_field_names"] = id_field_names
            if object_path is not None:
                self._values["object_path"] = object_path
            if success_response_handling_config is not None:
                self._values["success_response_handling_config"] = success_response_handling_config
            if write_operation_type is not None:
                self._values["write_operation_type"] = write_operation_type

        @builtins.property
        def error_handling_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.ErrorHandlingConfigProperty"]]:
            '''The settings that determine how Amazon AppFlow handles an error when placing data in the destination.

            For example, this setting would determine if the flow should fail after one insertion error, or continue and attempt to insert every record regardless of the initial failure. ``ErrorHandlingConfig`` is a part of the destination connector details.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sapodatadestinationproperties.html#cfn-appflow-flow-sapodatadestinationproperties-errorhandlingconfig
            '''
            result = self._values.get("error_handling_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.ErrorHandlingConfigProperty"]], result)

        @builtins.property
        def id_field_names(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of field names that can be used as an ID field when performing a write operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sapodatadestinationproperties.html#cfn-appflow-flow-sapodatadestinationproperties-idfieldnames
            '''
            result = self._values.get("id_field_names")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def object_path(self) -> typing.Optional[builtins.str]:
            '''The object path specified in the SAPOData flow destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sapodatadestinationproperties.html#cfn-appflow-flow-sapodatadestinationproperties-objectpath
            '''
            result = self._values.get("object_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def success_response_handling_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.SuccessResponseHandlingConfigProperty"]]:
            '''Determines how Amazon AppFlow handles the success response that it gets from the connector after placing data.

            For example, this setting would determine where to write the response from a destination connector upon a successful insert operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sapodatadestinationproperties.html#cfn-appflow-flow-sapodatadestinationproperties-successresponsehandlingconfig
            '''
            result = self._values.get("success_response_handling_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.SuccessResponseHandlingConfigProperty"]], result)

        @builtins.property
        def write_operation_type(self) -> typing.Optional[builtins.str]:
            '''The possible write operations in the destination connector.

            When this value is not provided, this defaults to the ``INSERT`` operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sapodatadestinationproperties.html#cfn-appflow-flow-sapodatadestinationproperties-writeoperationtype
            '''
            result = self._values.get("write_operation_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SAPODataDestinationPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.SAPODataPaginationConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"max_page_size": "maxPageSize"},
    )
    class SAPODataPaginationConfigProperty:
        def __init__(
            self,
            *,
            max_page_size: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Sets the page size for each *concurrent process* that transfers OData records from your SAP instance.

            A concurrent process is query that retrieves a batch of records as part of a flow run. Amazon AppFlow can run multiple concurrent processes in parallel to transfer data faster.

            :param max_page_size: The maximum number of records that Amazon AppFlow receives in each page of the response from your SAP application. For transfers of OData records, the maximum page size is 3,000. For transfers of data that comes from an ODP provider, the maximum page size is 10,000.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sapodatapaginationconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                s_aPOData_pagination_config_property = appflow_mixins.CfnFlowPropsMixin.SAPODataPaginationConfigProperty(
                    max_page_size=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4c908481354573b0589b95471fc9c44ea5038a248c8927569ab42e1fbc704bb9)
                check_type(argname="argument max_page_size", value=max_page_size, expected_type=type_hints["max_page_size"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_page_size is not None:
                self._values["max_page_size"] = max_page_size

        @builtins.property
        def max_page_size(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of records that Amazon AppFlow receives in each page of the response from your SAP application.

            For transfers of OData records, the maximum page size is 3,000. For transfers of data that comes from an ODP provider, the maximum page size is 10,000.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sapodatapaginationconfig.html#cfn-appflow-flow-sapodatapaginationconfig-maxpagesize
            '''
            result = self._values.get("max_page_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SAPODataPaginationConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.SAPODataParallelismConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"max_parallelism": "maxParallelism"},
    )
    class SAPODataParallelismConfigProperty:
        def __init__(
            self,
            *,
            max_parallelism: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Sets the number of *concurrent processes* that transfer OData records from your SAP instance.

            A concurrent process is query that retrieves a batch of records as part of a flow run. Amazon AppFlow can run multiple concurrent processes in parallel to transfer data faster.

            :param max_parallelism: The maximum number of processes that Amazon AppFlow runs at the same time when it retrieves your data from your SAP application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sapodataparallelismconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                s_aPOData_parallelism_config_property = appflow_mixins.CfnFlowPropsMixin.SAPODataParallelismConfigProperty(
                    max_parallelism=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__292021d2998e059ebadeed06d9c649bcd9f47eef218876fd1c4f261aaa36c1e5)
                check_type(argname="argument max_parallelism", value=max_parallelism, expected_type=type_hints["max_parallelism"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_parallelism is not None:
                self._values["max_parallelism"] = max_parallelism

        @builtins.property
        def max_parallelism(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of processes that Amazon AppFlow runs at the same time when it retrieves your data from your SAP application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sapodataparallelismconfig.html#cfn-appflow-flow-sapodataparallelismconfig-maxparallelism
            '''
            result = self._values.get("max_parallelism")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SAPODataParallelismConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.SAPODataSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "object_path": "objectPath",
            "pagination_config": "paginationConfig",
            "parallelism_config": "parallelismConfig",
        },
    )
    class SAPODataSourcePropertiesProperty:
        def __init__(
            self,
            *,
            object_path: typing.Optional[builtins.str] = None,
            pagination_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.SAPODataPaginationConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            parallelism_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.SAPODataParallelismConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The properties that are applied when using SAPOData as a flow source.

            :param object_path: The object path specified in the SAPOData flow source.
            :param pagination_config: Sets the page size for each concurrent process that transfers OData records from your SAP instance.
            :param parallelism_config: Sets the number of concurrent processes that transfers OData records from your SAP instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sapodatasourceproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                s_aPOData_source_properties_property = appflow_mixins.CfnFlowPropsMixin.SAPODataSourcePropertiesProperty(
                    object_path="objectPath",
                    pagination_config=appflow_mixins.CfnFlowPropsMixin.SAPODataPaginationConfigProperty(
                        max_page_size=123
                    ),
                    parallelism_config=appflow_mixins.CfnFlowPropsMixin.SAPODataParallelismConfigProperty(
                        max_parallelism=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fcebee339e7afa43a72a37af511bd5019925bbd6b043637f0fa6589ee84d0d70)
                check_type(argname="argument object_path", value=object_path, expected_type=type_hints["object_path"])
                check_type(argname="argument pagination_config", value=pagination_config, expected_type=type_hints["pagination_config"])
                check_type(argname="argument parallelism_config", value=parallelism_config, expected_type=type_hints["parallelism_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if object_path is not None:
                self._values["object_path"] = object_path
            if pagination_config is not None:
                self._values["pagination_config"] = pagination_config
            if parallelism_config is not None:
                self._values["parallelism_config"] = parallelism_config

        @builtins.property
        def object_path(self) -> typing.Optional[builtins.str]:
            '''The object path specified in the SAPOData flow source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sapodatasourceproperties.html#cfn-appflow-flow-sapodatasourceproperties-objectpath
            '''
            result = self._values.get("object_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def pagination_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.SAPODataPaginationConfigProperty"]]:
            '''Sets the page size for each concurrent process that transfers OData records from your SAP instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sapodatasourceproperties.html#cfn-appflow-flow-sapodatasourceproperties-paginationconfig
            '''
            result = self._values.get("pagination_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.SAPODataPaginationConfigProperty"]], result)

        @builtins.property
        def parallelism_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.SAPODataParallelismConfigProperty"]]:
            '''Sets the number of concurrent processes that transfers OData records from your SAP instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sapodatasourceproperties.html#cfn-appflow-flow-sapodatasourceproperties-parallelismconfig
            '''
            result = self._values.get("parallelism_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.SAPODataParallelismConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SAPODataSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.SalesforceDestinationPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_transfer_api": "dataTransferApi",
            "error_handling_config": "errorHandlingConfig",
            "id_field_names": "idFieldNames",
            "object": "object",
            "write_operation_type": "writeOperationType",
        },
    )
    class SalesforceDestinationPropertiesProperty:
        def __init__(
            self,
            *,
            data_transfer_api: typing.Optional[builtins.str] = None,
            error_handling_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.ErrorHandlingConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            id_field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
            object: typing.Optional[builtins.str] = None,
            write_operation_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The properties that are applied when Salesforce is being used as a destination.

            :param data_transfer_api: Specifies which Salesforce API is used by Amazon AppFlow when your flow transfers data to Salesforce. - **AUTOMATIC** - The default. Amazon AppFlow selects which API to use based on the number of records that your flow transfers to Salesforce. If your flow transfers fewer than 1,000 records, Amazon AppFlow uses Salesforce REST API. If your flow transfers 1,000 records or more, Amazon AppFlow uses Salesforce Bulk API 2.0. Each of these Salesforce APIs structures data differently. If Amazon AppFlow selects the API automatically, be aware that, for recurring flows, the data output might vary from one flow run to the next. For example, if a flow runs daily, it might use REST API on one day to transfer 900 records, and it might use Bulk API 2.0 on the next day to transfer 1,100 records. For each of these flow runs, the respective Salesforce API formats the data differently. Some of the differences include how dates are formatted and null values are represented. Also, Bulk API 2.0 doesn't transfer Salesforce compound fields. By choosing this option, you optimize flow performance for both small and large data transfers, but the tradeoff is inconsistent formatting in the output. - **BULKV2** - Amazon AppFlow uses only Salesforce Bulk API 2.0. This API runs asynchronous data transfers, and it's optimal for large sets of data. By choosing this option, you ensure that your flow writes consistent output, but you optimize performance only for large data transfers. Note that Bulk API 2.0 does not transfer Salesforce compound fields. - **REST_SYNC** - Amazon AppFlow uses only Salesforce REST API. By choosing this option, you ensure that your flow writes consistent output, but you decrease performance for large data transfers that are better suited for Bulk API 2.0. In some cases, if your flow attempts to transfer a vary large set of data, it might fail with a timed out error.
            :param error_handling_config: The settings that determine how Amazon AppFlow handles an error when placing data in the Salesforce destination. For example, this setting would determine if the flow should fail after one insertion error, or continue and attempt to insert every record regardless of the initial failure. ``ErrorHandlingConfig`` is a part of the destination connector details.
            :param id_field_names: The name of the field that Amazon AppFlow uses as an ID when performing a write operation such as update or delete.
            :param object: The object specified in the Salesforce flow destination.
            :param write_operation_type: This specifies the type of write operation to be performed in Salesforce. When the value is ``UPSERT`` , then ``idFieldNames`` is required.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-salesforcedestinationproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                salesforce_destination_properties_property = appflow_mixins.CfnFlowPropsMixin.SalesforceDestinationPropertiesProperty(
                    data_transfer_api="dataTransferApi",
                    error_handling_config=appflow_mixins.CfnFlowPropsMixin.ErrorHandlingConfigProperty(
                        bucket_name="bucketName",
                        bucket_prefix="bucketPrefix",
                        fail_on_first_error=False
                    ),
                    id_field_names=["idFieldNames"],
                    object="object",
                    write_operation_type="writeOperationType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c3cdf139dc0f3e657e6a3b5b07cfe3055c5c130c6cd8daeb2f091cdc8fe961d2)
                check_type(argname="argument data_transfer_api", value=data_transfer_api, expected_type=type_hints["data_transfer_api"])
                check_type(argname="argument error_handling_config", value=error_handling_config, expected_type=type_hints["error_handling_config"])
                check_type(argname="argument id_field_names", value=id_field_names, expected_type=type_hints["id_field_names"])
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
                check_type(argname="argument write_operation_type", value=write_operation_type, expected_type=type_hints["write_operation_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data_transfer_api is not None:
                self._values["data_transfer_api"] = data_transfer_api
            if error_handling_config is not None:
                self._values["error_handling_config"] = error_handling_config
            if id_field_names is not None:
                self._values["id_field_names"] = id_field_names
            if object is not None:
                self._values["object"] = object
            if write_operation_type is not None:
                self._values["write_operation_type"] = write_operation_type

        @builtins.property
        def data_transfer_api(self) -> typing.Optional[builtins.str]:
            '''Specifies which Salesforce API is used by Amazon AppFlow when your flow transfers data to Salesforce.

            - **AUTOMATIC** - The default. Amazon AppFlow selects which API to use based on the number of records that your flow transfers to Salesforce. If your flow transfers fewer than 1,000 records, Amazon AppFlow uses Salesforce REST API. If your flow transfers 1,000 records or more, Amazon AppFlow uses Salesforce Bulk API 2.0.

            Each of these Salesforce APIs structures data differently. If Amazon AppFlow selects the API automatically, be aware that, for recurring flows, the data output might vary from one flow run to the next. For example, if a flow runs daily, it might use REST API on one day to transfer 900 records, and it might use Bulk API 2.0 on the next day to transfer 1,100 records. For each of these flow runs, the respective Salesforce API formats the data differently. Some of the differences include how dates are formatted and null values are represented. Also, Bulk API 2.0 doesn't transfer Salesforce compound fields.

            By choosing this option, you optimize flow performance for both small and large data transfers, but the tradeoff is inconsistent formatting in the output.

            - **BULKV2** - Amazon AppFlow uses only Salesforce Bulk API 2.0. This API runs asynchronous data transfers, and it's optimal for large sets of data. By choosing this option, you ensure that your flow writes consistent output, but you optimize performance only for large data transfers.

            Note that Bulk API 2.0 does not transfer Salesforce compound fields.

            - **REST_SYNC** - Amazon AppFlow uses only Salesforce REST API. By choosing this option, you ensure that your flow writes consistent output, but you decrease performance for large data transfers that are better suited for Bulk API 2.0. In some cases, if your flow attempts to transfer a vary large set of data, it might fail with a timed out error.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-salesforcedestinationproperties.html#cfn-appflow-flow-salesforcedestinationproperties-datatransferapi
            '''
            result = self._values.get("data_transfer_api")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def error_handling_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.ErrorHandlingConfigProperty"]]:
            '''The settings that determine how Amazon AppFlow handles an error when placing data in the Salesforce destination.

            For example, this setting would determine if the flow should fail after one insertion error, or continue and attempt to insert every record regardless of the initial failure. ``ErrorHandlingConfig`` is a part of the destination connector details.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-salesforcedestinationproperties.html#cfn-appflow-flow-salesforcedestinationproperties-errorhandlingconfig
            '''
            result = self._values.get("error_handling_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.ErrorHandlingConfigProperty"]], result)

        @builtins.property
        def id_field_names(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The name of the field that Amazon AppFlow uses as an ID when performing a write operation such as update or delete.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-salesforcedestinationproperties.html#cfn-appflow-flow-salesforcedestinationproperties-idfieldnames
            '''
            result = self._values.get("id_field_names")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def object(self) -> typing.Optional[builtins.str]:
            '''The object specified in the Salesforce flow destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-salesforcedestinationproperties.html#cfn-appflow-flow-salesforcedestinationproperties-object
            '''
            result = self._values.get("object")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def write_operation_type(self) -> typing.Optional[builtins.str]:
            '''This specifies the type of write operation to be performed in Salesforce.

            When the value is ``UPSERT`` , then ``idFieldNames`` is required.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-salesforcedestinationproperties.html#cfn-appflow-flow-salesforcedestinationproperties-writeoperationtype
            '''
            result = self._values.get("write_operation_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SalesforceDestinationPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.SalesforceSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_transfer_api": "dataTransferApi",
            "enable_dynamic_field_update": "enableDynamicFieldUpdate",
            "include_deleted_records": "includeDeletedRecords",
            "object": "object",
        },
    )
    class SalesforceSourcePropertiesProperty:
        def __init__(
            self,
            *,
            data_transfer_api: typing.Optional[builtins.str] = None,
            enable_dynamic_field_update: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            include_deleted_records: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            object: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The properties that are applied when Salesforce is being used as a source.

            :param data_transfer_api: Specifies which Salesforce API is used by Amazon AppFlow when your flow transfers data from Salesforce. - **AUTOMATIC** - The default. Amazon AppFlow selects which API to use based on the number of records that your flow transfers from Salesforce. If your flow transfers fewer than 1,000,000 records, Amazon AppFlow uses Salesforce REST API. If your flow transfers 1,000,000 records or more, Amazon AppFlow uses Salesforce Bulk API 2.0. Each of these Salesforce APIs structures data differently. If Amazon AppFlow selects the API automatically, be aware that, for recurring flows, the data output might vary from one flow run to the next. For example, if a flow runs daily, it might use REST API on one day to transfer 900,000 records, and it might use Bulk API 2.0 on the next day to transfer 1,100,000 records. For each of these flow runs, the respective Salesforce API formats the data differently. Some of the differences include how dates are formatted and null values are represented. Also, Bulk API 2.0 doesn't transfer Salesforce compound fields. By choosing this option, you optimize flow performance for both small and large data transfers, but the tradeoff is inconsistent formatting in the output. - **BULKV2** - Amazon AppFlow uses only Salesforce Bulk API 2.0. This API runs asynchronous data transfers, and it's optimal for large sets of data. By choosing this option, you ensure that your flow writes consistent output, but you optimize performance only for large data transfers. Note that Bulk API 2.0 does not transfer Salesforce compound fields. - **REST_SYNC** - Amazon AppFlow uses only Salesforce REST API. By choosing this option, you ensure that your flow writes consistent output, but you decrease performance for large data transfers that are better suited for Bulk API 2.0. In some cases, if your flow attempts to transfer a vary large set of data, it might fail wituh a timed out error.
            :param enable_dynamic_field_update: The flag that enables dynamic fetching of new (recently added) fields in the Salesforce objects while running a flow.
            :param include_deleted_records: Indicates whether Amazon AppFlow includes deleted files in the flow run.
            :param object: The object specified in the Salesforce flow source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-salesforcesourceproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                salesforce_source_properties_property = appflow_mixins.CfnFlowPropsMixin.SalesforceSourcePropertiesProperty(
                    data_transfer_api="dataTransferApi",
                    enable_dynamic_field_update=False,
                    include_deleted_records=False,
                    object="object"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__eab8c820a0beb16bbf79d54d683678c75fcad3b265997588e27dae4ee4293a52)
                check_type(argname="argument data_transfer_api", value=data_transfer_api, expected_type=type_hints["data_transfer_api"])
                check_type(argname="argument enable_dynamic_field_update", value=enable_dynamic_field_update, expected_type=type_hints["enable_dynamic_field_update"])
                check_type(argname="argument include_deleted_records", value=include_deleted_records, expected_type=type_hints["include_deleted_records"])
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data_transfer_api is not None:
                self._values["data_transfer_api"] = data_transfer_api
            if enable_dynamic_field_update is not None:
                self._values["enable_dynamic_field_update"] = enable_dynamic_field_update
            if include_deleted_records is not None:
                self._values["include_deleted_records"] = include_deleted_records
            if object is not None:
                self._values["object"] = object

        @builtins.property
        def data_transfer_api(self) -> typing.Optional[builtins.str]:
            '''Specifies which Salesforce API is used by Amazon AppFlow when your flow transfers data from Salesforce.

            - **AUTOMATIC** - The default. Amazon AppFlow selects which API to use based on the number of records that your flow transfers from Salesforce. If your flow transfers fewer than 1,000,000 records, Amazon AppFlow uses Salesforce REST API. If your flow transfers 1,000,000 records or more, Amazon AppFlow uses Salesforce Bulk API 2.0.

            Each of these Salesforce APIs structures data differently. If Amazon AppFlow selects the API automatically, be aware that, for recurring flows, the data output might vary from one flow run to the next. For example, if a flow runs daily, it might use REST API on one day to transfer 900,000 records, and it might use Bulk API 2.0 on the next day to transfer 1,100,000 records. For each of these flow runs, the respective Salesforce API formats the data differently. Some of the differences include how dates are formatted and null values are represented. Also, Bulk API 2.0 doesn't transfer Salesforce compound fields.

            By choosing this option, you optimize flow performance for both small and large data transfers, but the tradeoff is inconsistent formatting in the output.

            - **BULKV2** - Amazon AppFlow uses only Salesforce Bulk API 2.0. This API runs asynchronous data transfers, and it's optimal for large sets of data. By choosing this option, you ensure that your flow writes consistent output, but you optimize performance only for large data transfers.

            Note that Bulk API 2.0 does not transfer Salesforce compound fields.

            - **REST_SYNC** - Amazon AppFlow uses only Salesforce REST API. By choosing this option, you ensure that your flow writes consistent output, but you decrease performance for large data transfers that are better suited for Bulk API 2.0. In some cases, if your flow attempts to transfer a vary large set of data, it might fail wituh a timed out error.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-salesforcesourceproperties.html#cfn-appflow-flow-salesforcesourceproperties-datatransferapi
            '''
            result = self._values.get("data_transfer_api")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def enable_dynamic_field_update(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''The flag that enables dynamic fetching of new (recently added) fields in the Salesforce objects while running a flow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-salesforcesourceproperties.html#cfn-appflow-flow-salesforcesourceproperties-enabledynamicfieldupdate
            '''
            result = self._values.get("enable_dynamic_field_update")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def include_deleted_records(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether Amazon AppFlow includes deleted files in the flow run.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-salesforcesourceproperties.html#cfn-appflow-flow-salesforcesourceproperties-includedeletedrecords
            '''
            result = self._values.get("include_deleted_records")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def object(self) -> typing.Optional[builtins.str]:
            '''The object specified in the Salesforce flow source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-salesforcesourceproperties.html#cfn-appflow-flow-salesforcesourceproperties-object
            '''
            result = self._values.get("object")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SalesforceSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.ScheduledTriggerPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_pull_mode": "dataPullMode",
            "first_execution_from": "firstExecutionFrom",
            "flow_error_deactivation_threshold": "flowErrorDeactivationThreshold",
            "schedule_end_time": "scheduleEndTime",
            "schedule_expression": "scheduleExpression",
            "schedule_offset": "scheduleOffset",
            "schedule_start_time": "scheduleStartTime",
            "time_zone": "timeZone",
        },
    )
    class ScheduledTriggerPropertiesProperty:
        def __init__(
            self,
            *,
            data_pull_mode: typing.Optional[builtins.str] = None,
            first_execution_from: typing.Optional[jsii.Number] = None,
            flow_error_deactivation_threshold: typing.Optional[jsii.Number] = None,
            schedule_end_time: typing.Optional[jsii.Number] = None,
            schedule_expression: typing.Optional[builtins.str] = None,
            schedule_offset: typing.Optional[jsii.Number] = None,
            schedule_start_time: typing.Optional[jsii.Number] = None,
            time_zone: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the configuration details of a schedule-triggered flow as defined by the user.

            Currently, these settings only apply to the ``Scheduled`` trigger type.

            :param data_pull_mode: Specifies whether a scheduled flow has an incremental data transfer or a complete data transfer for each flow run.
            :param first_execution_from: Specifies the date range for the records to import from the connector in the first flow run.
            :param flow_error_deactivation_threshold: Defines how many times a scheduled flow fails consecutively before Amazon AppFlow deactivates it.
            :param schedule_end_time: The time at which the scheduled flow ends. The time is formatted as a timestamp that follows the ISO 8601 standard, such as ``2022-04-27T13:00:00-07:00`` .
            :param schedule_expression: The scheduling expression that determines the rate at which the schedule will run, for example ``rate(5minutes)`` .
            :param schedule_offset: Specifies the optional offset that is added to the time interval for a schedule-triggered flow.
            :param schedule_start_time: The time at which the scheduled flow starts. The time is formatted as a timestamp that follows the ISO 8601 standard, such as ``2022-04-26T13:00:00-07:00`` .
            :param time_zone: Specifies the time zone used when referring to the dates and times of a scheduled flow, such as ``America/New_York`` . This time zone is only a descriptive label. It doesn't affect how Amazon AppFlow interprets the timestamps that you specify to schedule the flow. If you want to schedule a flow by using times in a particular time zone, indicate the time zone as a UTC offset in your timestamps. For example, the UTC offsets for the ``America/New_York`` timezone are ``-04:00`` EDT and ``-05:00 EST`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-scheduledtriggerproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                scheduled_trigger_properties_property = appflow_mixins.CfnFlowPropsMixin.ScheduledTriggerPropertiesProperty(
                    data_pull_mode="dataPullMode",
                    first_execution_from=123,
                    flow_error_deactivation_threshold=123,
                    schedule_end_time=123,
                    schedule_expression="scheduleExpression",
                    schedule_offset=123,
                    schedule_start_time=123,
                    time_zone="timeZone"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__39c074bb2c4e76cf5f1d76ef5ef8dabead16d20d0f60154e219a437b5a21240a)
                check_type(argname="argument data_pull_mode", value=data_pull_mode, expected_type=type_hints["data_pull_mode"])
                check_type(argname="argument first_execution_from", value=first_execution_from, expected_type=type_hints["first_execution_from"])
                check_type(argname="argument flow_error_deactivation_threshold", value=flow_error_deactivation_threshold, expected_type=type_hints["flow_error_deactivation_threshold"])
                check_type(argname="argument schedule_end_time", value=schedule_end_time, expected_type=type_hints["schedule_end_time"])
                check_type(argname="argument schedule_expression", value=schedule_expression, expected_type=type_hints["schedule_expression"])
                check_type(argname="argument schedule_offset", value=schedule_offset, expected_type=type_hints["schedule_offset"])
                check_type(argname="argument schedule_start_time", value=schedule_start_time, expected_type=type_hints["schedule_start_time"])
                check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data_pull_mode is not None:
                self._values["data_pull_mode"] = data_pull_mode
            if first_execution_from is not None:
                self._values["first_execution_from"] = first_execution_from
            if flow_error_deactivation_threshold is not None:
                self._values["flow_error_deactivation_threshold"] = flow_error_deactivation_threshold
            if schedule_end_time is not None:
                self._values["schedule_end_time"] = schedule_end_time
            if schedule_expression is not None:
                self._values["schedule_expression"] = schedule_expression
            if schedule_offset is not None:
                self._values["schedule_offset"] = schedule_offset
            if schedule_start_time is not None:
                self._values["schedule_start_time"] = schedule_start_time
            if time_zone is not None:
                self._values["time_zone"] = time_zone

        @builtins.property
        def data_pull_mode(self) -> typing.Optional[builtins.str]:
            '''Specifies whether a scheduled flow has an incremental data transfer or a complete data transfer for each flow run.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-scheduledtriggerproperties.html#cfn-appflow-flow-scheduledtriggerproperties-datapullmode
            '''
            result = self._values.get("data_pull_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def first_execution_from(self) -> typing.Optional[jsii.Number]:
            '''Specifies the date range for the records to import from the connector in the first flow run.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-scheduledtriggerproperties.html#cfn-appflow-flow-scheduledtriggerproperties-firstexecutionfrom
            '''
            result = self._values.get("first_execution_from")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def flow_error_deactivation_threshold(self) -> typing.Optional[jsii.Number]:
            '''Defines how many times a scheduled flow fails consecutively before Amazon AppFlow deactivates it.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-scheduledtriggerproperties.html#cfn-appflow-flow-scheduledtriggerproperties-flowerrordeactivationthreshold
            '''
            result = self._values.get("flow_error_deactivation_threshold")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def schedule_end_time(self) -> typing.Optional[jsii.Number]:
            '''The time at which the scheduled flow ends.

            The time is formatted as a timestamp that follows the ISO 8601 standard, such as ``2022-04-27T13:00:00-07:00`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-scheduledtriggerproperties.html#cfn-appflow-flow-scheduledtriggerproperties-scheduleendtime
            '''
            result = self._values.get("schedule_end_time")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def schedule_expression(self) -> typing.Optional[builtins.str]:
            '''The scheduling expression that determines the rate at which the schedule will run, for example ``rate(5minutes)`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-scheduledtriggerproperties.html#cfn-appflow-flow-scheduledtriggerproperties-scheduleexpression
            '''
            result = self._values.get("schedule_expression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def schedule_offset(self) -> typing.Optional[jsii.Number]:
            '''Specifies the optional offset that is added to the time interval for a schedule-triggered flow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-scheduledtriggerproperties.html#cfn-appflow-flow-scheduledtriggerproperties-scheduleoffset
            '''
            result = self._values.get("schedule_offset")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def schedule_start_time(self) -> typing.Optional[jsii.Number]:
            '''The time at which the scheduled flow starts.

            The time is formatted as a timestamp that follows the ISO 8601 standard, such as ``2022-04-26T13:00:00-07:00`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-scheduledtriggerproperties.html#cfn-appflow-flow-scheduledtriggerproperties-schedulestarttime
            '''
            result = self._values.get("schedule_start_time")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def time_zone(self) -> typing.Optional[builtins.str]:
            '''Specifies the time zone used when referring to the dates and times of a scheduled flow, such as ``America/New_York`` .

            This time zone is only a descriptive label. It doesn't affect how Amazon AppFlow interprets the timestamps that you specify to schedule the flow.

            If you want to schedule a flow by using times in a particular time zone, indicate the time zone as a UTC offset in your timestamps. For example, the UTC offsets for the ``America/New_York`` timezone are ``-04:00`` EDT and ``-05:00 EST`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-scheduledtriggerproperties.html#cfn-appflow-flow-scheduledtriggerproperties-timezone
            '''
            result = self._values.get("time_zone")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScheduledTriggerPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.ServiceNowSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"object": "object"},
    )
    class ServiceNowSourcePropertiesProperty:
        def __init__(self, *, object: typing.Optional[builtins.str] = None) -> None:
            '''The properties that are applied when ServiceNow is being used as a source.

            :param object: The object specified in the ServiceNow flow source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-servicenowsourceproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                service_now_source_properties_property = appflow_mixins.CfnFlowPropsMixin.ServiceNowSourcePropertiesProperty(
                    object="object"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3612c45ddc8ca51659ab259a61b521de2af262a15007dcc846b3f9da37cb4188)
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if object is not None:
                self._values["object"] = object

        @builtins.property
        def object(self) -> typing.Optional[builtins.str]:
            '''The object specified in the ServiceNow flow source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-servicenowsourceproperties.html#cfn-appflow-flow-servicenowsourceproperties-object
            '''
            result = self._values.get("object")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServiceNowSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.SingularSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"object": "object"},
    )
    class SingularSourcePropertiesProperty:
        def __init__(self, *, object: typing.Optional[builtins.str] = None) -> None:
            '''The properties that are applied when Singular is being used as a source.

            :param object: The object specified in the Singular flow source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-singularsourceproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                singular_source_properties_property = appflow_mixins.CfnFlowPropsMixin.SingularSourcePropertiesProperty(
                    object="object"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__04b88fa137861d14c3c51cb521164b2cfcab22d5bd38499564d39e1733b105dc)
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if object is not None:
                self._values["object"] = object

        @builtins.property
        def object(self) -> typing.Optional[builtins.str]:
            '''The object specified in the Singular flow source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-singularsourceproperties.html#cfn-appflow-flow-singularsourceproperties-object
            '''
            result = self._values.get("object")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SingularSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.SlackSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"object": "object"},
    )
    class SlackSourcePropertiesProperty:
        def __init__(self, *, object: typing.Optional[builtins.str] = None) -> None:
            '''The properties that are applied when Slack is being used as a source.

            :param object: The object specified in the Slack flow source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-slacksourceproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                slack_source_properties_property = appflow_mixins.CfnFlowPropsMixin.SlackSourcePropertiesProperty(
                    object="object"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2e2bca9da6080ccc621d291b7e1bca23699b1788186c27a38c06aa2b9076e2f4)
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if object is not None:
                self._values["object"] = object

        @builtins.property
        def object(self) -> typing.Optional[builtins.str]:
            '''The object specified in the Slack flow source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-slacksourceproperties.html#cfn-appflow-flow-slacksourceproperties-object
            '''
            result = self._values.get("object")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlackSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.SnowflakeDestinationPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_prefix": "bucketPrefix",
            "error_handling_config": "errorHandlingConfig",
            "intermediate_bucket_name": "intermediateBucketName",
            "object": "object",
        },
    )
    class SnowflakeDestinationPropertiesProperty:
        def __init__(
            self,
            *,
            bucket_prefix: typing.Optional[builtins.str] = None,
            error_handling_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.ErrorHandlingConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            intermediate_bucket_name: typing.Optional[builtins.str] = None,
            object: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The properties that are applied when Snowflake is being used as a destination.

            :param bucket_prefix: The object key for the destination bucket in which Amazon AppFlow places the files.
            :param error_handling_config: The settings that determine how Amazon AppFlow handles an error when placing data in the Snowflake destination. For example, this setting would determine if the flow should fail after one insertion error, or continue and attempt to insert every record regardless of the initial failure. ``ErrorHandlingConfig`` is a part of the destination connector details.
            :param intermediate_bucket_name: The intermediate bucket that Amazon AppFlow uses when moving data into Snowflake.
            :param object: The object specified in the Snowflake flow destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-snowflakedestinationproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                snowflake_destination_properties_property = appflow_mixins.CfnFlowPropsMixin.SnowflakeDestinationPropertiesProperty(
                    bucket_prefix="bucketPrefix",
                    error_handling_config=appflow_mixins.CfnFlowPropsMixin.ErrorHandlingConfigProperty(
                        bucket_name="bucketName",
                        bucket_prefix="bucketPrefix",
                        fail_on_first_error=False
                    ),
                    intermediate_bucket_name="intermediateBucketName",
                    object="object"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__eeab24d3778d99ef17ff5419af894e61e26258ce5241e2fd49ceca2e22338c5c)
                check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
                check_type(argname="argument error_handling_config", value=error_handling_config, expected_type=type_hints["error_handling_config"])
                check_type(argname="argument intermediate_bucket_name", value=intermediate_bucket_name, expected_type=type_hints["intermediate_bucket_name"])
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_prefix is not None:
                self._values["bucket_prefix"] = bucket_prefix
            if error_handling_config is not None:
                self._values["error_handling_config"] = error_handling_config
            if intermediate_bucket_name is not None:
                self._values["intermediate_bucket_name"] = intermediate_bucket_name
            if object is not None:
                self._values["object"] = object

        @builtins.property
        def bucket_prefix(self) -> typing.Optional[builtins.str]:
            '''The object key for the destination bucket in which Amazon AppFlow places the files.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-snowflakedestinationproperties.html#cfn-appflow-flow-snowflakedestinationproperties-bucketprefix
            '''
            result = self._values.get("bucket_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def error_handling_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.ErrorHandlingConfigProperty"]]:
            '''The settings that determine how Amazon AppFlow handles an error when placing data in the Snowflake destination.

            For example, this setting would determine if the flow should fail after one insertion error, or continue and attempt to insert every record regardless of the initial failure. ``ErrorHandlingConfig`` is a part of the destination connector details.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-snowflakedestinationproperties.html#cfn-appflow-flow-snowflakedestinationproperties-errorhandlingconfig
            '''
            result = self._values.get("error_handling_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.ErrorHandlingConfigProperty"]], result)

        @builtins.property
        def intermediate_bucket_name(self) -> typing.Optional[builtins.str]:
            '''The intermediate bucket that Amazon AppFlow uses when moving data into Snowflake.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-snowflakedestinationproperties.html#cfn-appflow-flow-snowflakedestinationproperties-intermediatebucketname
            '''
            result = self._values.get("intermediate_bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def object(self) -> typing.Optional[builtins.str]:
            '''The object specified in the Snowflake flow destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-snowflakedestinationproperties.html#cfn-appflow-flow-snowflakedestinationproperties-object
            '''
            result = self._values.get("object")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SnowflakeDestinationPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.SourceConnectorPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "amplitude": "amplitude",
            "custom_connector": "customConnector",
            "datadog": "datadog",
            "dynatrace": "dynatrace",
            "google_analytics": "googleAnalytics",
            "infor_nexus": "inforNexus",
            "marketo": "marketo",
            "pardot": "pardot",
            "s3": "s3",
            "salesforce": "salesforce",
            "sapo_data": "sapoData",
            "service_now": "serviceNow",
            "singular": "singular",
            "slack": "slack",
            "trendmicro": "trendmicro",
            "veeva": "veeva",
            "zendesk": "zendesk",
        },
    )
    class SourceConnectorPropertiesProperty:
        def __init__(
            self,
            *,
            amplitude: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.AmplitudeSourcePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            custom_connector: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.CustomConnectorSourcePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            datadog: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.DatadogSourcePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            dynatrace: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.DynatraceSourcePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            google_analytics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.GoogleAnalyticsSourcePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            infor_nexus: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.InforNexusSourcePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            marketo: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.MarketoSourcePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            pardot: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.PardotSourcePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.S3SourcePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            salesforce: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.SalesforceSourcePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sapo_data: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.SAPODataSourcePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            service_now: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.ServiceNowSourcePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            singular: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.SingularSourcePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            slack: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.SlackSourcePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            trendmicro: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.TrendmicroSourcePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            veeva: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.VeevaSourcePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            zendesk: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.ZendeskSourcePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the information that is required to query a particular connector.

            :param amplitude: Specifies the information that is required for querying Amplitude.
            :param custom_connector: The properties that are applied when the custom connector is being used as a source.
            :param datadog: Specifies the information that is required for querying Datadog.
            :param dynatrace: Specifies the information that is required for querying Dynatrace.
            :param google_analytics: Specifies the information that is required for querying Google Analytics.
            :param infor_nexus: Specifies the information that is required for querying Infor Nexus.
            :param marketo: Specifies the information that is required for querying Marketo.
            :param pardot: Specifies the information that is required for querying Salesforce Pardot.
            :param s3: Specifies the information that is required for querying Amazon S3.
            :param salesforce: Specifies the information that is required for querying Salesforce.
            :param sapo_data: The properties that are applied when using SAPOData as a flow source.
            :param service_now: Specifies the information that is required for querying ServiceNow.
            :param singular: Specifies the information that is required for querying Singular.
            :param slack: Specifies the information that is required for querying Slack.
            :param trendmicro: Specifies the information that is required for querying Trend Micro.
            :param veeva: Specifies the information that is required for querying Veeva.
            :param zendesk: Specifies the information that is required for querying Zendesk.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                source_connector_properties_property = appflow_mixins.CfnFlowPropsMixin.SourceConnectorPropertiesProperty(
                    amplitude=appflow_mixins.CfnFlowPropsMixin.AmplitudeSourcePropertiesProperty(
                        object="object"
                    ),
                    custom_connector=appflow_mixins.CfnFlowPropsMixin.CustomConnectorSourcePropertiesProperty(
                        custom_properties={
                            "custom_properties_key": "customProperties"
                        },
                        data_transfer_api=appflow_mixins.CfnFlowPropsMixin.DataTransferApiProperty(
                            name="name",
                            type="type"
                        ),
                        entity_name="entityName"
                    ),
                    datadog=appflow_mixins.CfnFlowPropsMixin.DatadogSourcePropertiesProperty(
                        object="object"
                    ),
                    dynatrace=appflow_mixins.CfnFlowPropsMixin.DynatraceSourcePropertiesProperty(
                        object="object"
                    ),
                    google_analytics=appflow_mixins.CfnFlowPropsMixin.GoogleAnalyticsSourcePropertiesProperty(
                        object="object"
                    ),
                    infor_nexus=appflow_mixins.CfnFlowPropsMixin.InforNexusSourcePropertiesProperty(
                        object="object"
                    ),
                    marketo=appflow_mixins.CfnFlowPropsMixin.MarketoSourcePropertiesProperty(
                        object="object"
                    ),
                    pardot=appflow_mixins.CfnFlowPropsMixin.PardotSourcePropertiesProperty(
                        object="object"
                    ),
                    s3=appflow_mixins.CfnFlowPropsMixin.S3SourcePropertiesProperty(
                        bucket_name="bucketName",
                        bucket_prefix="bucketPrefix",
                        s3_input_format_config=appflow_mixins.CfnFlowPropsMixin.S3InputFormatConfigProperty(
                            s3_input_file_type="s3InputFileType"
                        )
                    ),
                    salesforce=appflow_mixins.CfnFlowPropsMixin.SalesforceSourcePropertiesProperty(
                        data_transfer_api="dataTransferApi",
                        enable_dynamic_field_update=False,
                        include_deleted_records=False,
                        object="object"
                    ),
                    sapo_data=appflow_mixins.CfnFlowPropsMixin.SAPODataSourcePropertiesProperty(
                        object_path="objectPath",
                        pagination_config=appflow_mixins.CfnFlowPropsMixin.SAPODataPaginationConfigProperty(
                            max_page_size=123
                        ),
                        parallelism_config=appflow_mixins.CfnFlowPropsMixin.SAPODataParallelismConfigProperty(
                            max_parallelism=123
                        )
                    ),
                    service_now=appflow_mixins.CfnFlowPropsMixin.ServiceNowSourcePropertiesProperty(
                        object="object"
                    ),
                    singular=appflow_mixins.CfnFlowPropsMixin.SingularSourcePropertiesProperty(
                        object="object"
                    ),
                    slack=appflow_mixins.CfnFlowPropsMixin.SlackSourcePropertiesProperty(
                        object="object"
                    ),
                    trendmicro=appflow_mixins.CfnFlowPropsMixin.TrendmicroSourcePropertiesProperty(
                        object="object"
                    ),
                    veeva=appflow_mixins.CfnFlowPropsMixin.VeevaSourcePropertiesProperty(
                        document_type="documentType",
                        include_all_versions=False,
                        include_renditions=False,
                        include_source_files=False,
                        object="object"
                    ),
                    zendesk=appflow_mixins.CfnFlowPropsMixin.ZendeskSourcePropertiesProperty(
                        object="object"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5522685b84294bc774e4be814ac166f368d66c76db6bda1048672cd8c48f487b)
                check_type(argname="argument amplitude", value=amplitude, expected_type=type_hints["amplitude"])
                check_type(argname="argument custom_connector", value=custom_connector, expected_type=type_hints["custom_connector"])
                check_type(argname="argument datadog", value=datadog, expected_type=type_hints["datadog"])
                check_type(argname="argument dynatrace", value=dynatrace, expected_type=type_hints["dynatrace"])
                check_type(argname="argument google_analytics", value=google_analytics, expected_type=type_hints["google_analytics"])
                check_type(argname="argument infor_nexus", value=infor_nexus, expected_type=type_hints["infor_nexus"])
                check_type(argname="argument marketo", value=marketo, expected_type=type_hints["marketo"])
                check_type(argname="argument pardot", value=pardot, expected_type=type_hints["pardot"])
                check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
                check_type(argname="argument salesforce", value=salesforce, expected_type=type_hints["salesforce"])
                check_type(argname="argument sapo_data", value=sapo_data, expected_type=type_hints["sapo_data"])
                check_type(argname="argument service_now", value=service_now, expected_type=type_hints["service_now"])
                check_type(argname="argument singular", value=singular, expected_type=type_hints["singular"])
                check_type(argname="argument slack", value=slack, expected_type=type_hints["slack"])
                check_type(argname="argument trendmicro", value=trendmicro, expected_type=type_hints["trendmicro"])
                check_type(argname="argument veeva", value=veeva, expected_type=type_hints["veeva"])
                check_type(argname="argument zendesk", value=zendesk, expected_type=type_hints["zendesk"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if amplitude is not None:
                self._values["amplitude"] = amplitude
            if custom_connector is not None:
                self._values["custom_connector"] = custom_connector
            if datadog is not None:
                self._values["datadog"] = datadog
            if dynatrace is not None:
                self._values["dynatrace"] = dynatrace
            if google_analytics is not None:
                self._values["google_analytics"] = google_analytics
            if infor_nexus is not None:
                self._values["infor_nexus"] = infor_nexus
            if marketo is not None:
                self._values["marketo"] = marketo
            if pardot is not None:
                self._values["pardot"] = pardot
            if s3 is not None:
                self._values["s3"] = s3
            if salesforce is not None:
                self._values["salesforce"] = salesforce
            if sapo_data is not None:
                self._values["sapo_data"] = sapo_data
            if service_now is not None:
                self._values["service_now"] = service_now
            if singular is not None:
                self._values["singular"] = singular
            if slack is not None:
                self._values["slack"] = slack
            if trendmicro is not None:
                self._values["trendmicro"] = trendmicro
            if veeva is not None:
                self._values["veeva"] = veeva
            if zendesk is not None:
                self._values["zendesk"] = zendesk

        @builtins.property
        def amplitude(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.AmplitudeSourcePropertiesProperty"]]:
            '''Specifies the information that is required for querying Amplitude.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-amplitude
            '''
            result = self._values.get("amplitude")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.AmplitudeSourcePropertiesProperty"]], result)

        @builtins.property
        def custom_connector(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.CustomConnectorSourcePropertiesProperty"]]:
            '''The properties that are applied when the custom connector is being used as a source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-customconnector
            '''
            result = self._values.get("custom_connector")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.CustomConnectorSourcePropertiesProperty"]], result)

        @builtins.property
        def datadog(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.DatadogSourcePropertiesProperty"]]:
            '''Specifies the information that is required for querying Datadog.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-datadog
            '''
            result = self._values.get("datadog")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.DatadogSourcePropertiesProperty"]], result)

        @builtins.property
        def dynatrace(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.DynatraceSourcePropertiesProperty"]]:
            '''Specifies the information that is required for querying Dynatrace.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-dynatrace
            '''
            result = self._values.get("dynatrace")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.DynatraceSourcePropertiesProperty"]], result)

        @builtins.property
        def google_analytics(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.GoogleAnalyticsSourcePropertiesProperty"]]:
            '''Specifies the information that is required for querying Google Analytics.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-googleanalytics
            '''
            result = self._values.get("google_analytics")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.GoogleAnalyticsSourcePropertiesProperty"]], result)

        @builtins.property
        def infor_nexus(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.InforNexusSourcePropertiesProperty"]]:
            '''Specifies the information that is required for querying Infor Nexus.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-infornexus
            '''
            result = self._values.get("infor_nexus")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.InforNexusSourcePropertiesProperty"]], result)

        @builtins.property
        def marketo(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.MarketoSourcePropertiesProperty"]]:
            '''Specifies the information that is required for querying Marketo.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-marketo
            '''
            result = self._values.get("marketo")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.MarketoSourcePropertiesProperty"]], result)

        @builtins.property
        def pardot(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.PardotSourcePropertiesProperty"]]:
            '''Specifies the information that is required for querying Salesforce Pardot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-pardot
            '''
            result = self._values.get("pardot")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.PardotSourcePropertiesProperty"]], result)

        @builtins.property
        def s3(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.S3SourcePropertiesProperty"]]:
            '''Specifies the information that is required for querying Amazon S3.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-s3
            '''
            result = self._values.get("s3")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.S3SourcePropertiesProperty"]], result)

        @builtins.property
        def salesforce(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.SalesforceSourcePropertiesProperty"]]:
            '''Specifies the information that is required for querying Salesforce.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-salesforce
            '''
            result = self._values.get("salesforce")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.SalesforceSourcePropertiesProperty"]], result)

        @builtins.property
        def sapo_data(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.SAPODataSourcePropertiesProperty"]]:
            '''The properties that are applied when using SAPOData as a flow source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-sapodata
            '''
            result = self._values.get("sapo_data")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.SAPODataSourcePropertiesProperty"]], result)

        @builtins.property
        def service_now(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.ServiceNowSourcePropertiesProperty"]]:
            '''Specifies the information that is required for querying ServiceNow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-servicenow
            '''
            result = self._values.get("service_now")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.ServiceNowSourcePropertiesProperty"]], result)

        @builtins.property
        def singular(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.SingularSourcePropertiesProperty"]]:
            '''Specifies the information that is required for querying Singular.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-singular
            '''
            result = self._values.get("singular")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.SingularSourcePropertiesProperty"]], result)

        @builtins.property
        def slack(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.SlackSourcePropertiesProperty"]]:
            '''Specifies the information that is required for querying Slack.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-slack
            '''
            result = self._values.get("slack")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.SlackSourcePropertiesProperty"]], result)

        @builtins.property
        def trendmicro(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.TrendmicroSourcePropertiesProperty"]]:
            '''Specifies the information that is required for querying Trend Micro.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-trendmicro
            '''
            result = self._values.get("trendmicro")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.TrendmicroSourcePropertiesProperty"]], result)

        @builtins.property
        def veeva(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.VeevaSourcePropertiesProperty"]]:
            '''Specifies the information that is required for querying Veeva.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-veeva
            '''
            result = self._values.get("veeva")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.VeevaSourcePropertiesProperty"]], result)

        @builtins.property
        def zendesk(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.ZendeskSourcePropertiesProperty"]]:
            '''Specifies the information that is required for querying Zendesk.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-zendesk
            '''
            result = self._values.get("zendesk")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.ZendeskSourcePropertiesProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceConnectorPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.SourceFlowConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "api_version": "apiVersion",
            "connector_profile_name": "connectorProfileName",
            "connector_type": "connectorType",
            "incremental_pull_config": "incrementalPullConfig",
            "source_connector_properties": "sourceConnectorProperties",
        },
    )
    class SourceFlowConfigProperty:
        def __init__(
            self,
            *,
            api_version: typing.Optional[builtins.str] = None,
            connector_profile_name: typing.Optional[builtins.str] = None,
            connector_type: typing.Optional[builtins.str] = None,
            incremental_pull_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.IncrementalPullConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            source_connector_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.SourceConnectorPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains information about the configuration of the source connector used in the flow.

            :param api_version: The API version of the connector when it's used as a source in the flow.
            :param connector_profile_name: The name of the connector profile. This name must be unique for each connector profile in the AWS account .
            :param connector_type: The type of connector, such as Salesforce, Amplitude, and so on.
            :param incremental_pull_config: Defines the configuration for a scheduled incremental data pull. If a valid configuration is provided, the fields specified in the configuration are used when querying for the incremental data pull.
            :param source_connector_properties: Specifies the information that is required to query a particular source connector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceflowconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                source_flow_config_property = appflow_mixins.CfnFlowPropsMixin.SourceFlowConfigProperty(
                    api_version="apiVersion",
                    connector_profile_name="connectorProfileName",
                    connector_type="connectorType",
                    incremental_pull_config=appflow_mixins.CfnFlowPropsMixin.IncrementalPullConfigProperty(
                        datetime_type_field_name="datetimeTypeFieldName"
                    ),
                    source_connector_properties=appflow_mixins.CfnFlowPropsMixin.SourceConnectorPropertiesProperty(
                        amplitude=appflow_mixins.CfnFlowPropsMixin.AmplitudeSourcePropertiesProperty(
                            object="object"
                        ),
                        custom_connector=appflow_mixins.CfnFlowPropsMixin.CustomConnectorSourcePropertiesProperty(
                            custom_properties={
                                "custom_properties_key": "customProperties"
                            },
                            data_transfer_api=appflow_mixins.CfnFlowPropsMixin.DataTransferApiProperty(
                                name="name",
                                type="type"
                            ),
                            entity_name="entityName"
                        ),
                        datadog=appflow_mixins.CfnFlowPropsMixin.DatadogSourcePropertiesProperty(
                            object="object"
                        ),
                        dynatrace=appflow_mixins.CfnFlowPropsMixin.DynatraceSourcePropertiesProperty(
                            object="object"
                        ),
                        google_analytics=appflow_mixins.CfnFlowPropsMixin.GoogleAnalyticsSourcePropertiesProperty(
                            object="object"
                        ),
                        infor_nexus=appflow_mixins.CfnFlowPropsMixin.InforNexusSourcePropertiesProperty(
                            object="object"
                        ),
                        marketo=appflow_mixins.CfnFlowPropsMixin.MarketoSourcePropertiesProperty(
                            object="object"
                        ),
                        pardot=appflow_mixins.CfnFlowPropsMixin.PardotSourcePropertiesProperty(
                            object="object"
                        ),
                        s3=appflow_mixins.CfnFlowPropsMixin.S3SourcePropertiesProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix",
                            s3_input_format_config=appflow_mixins.CfnFlowPropsMixin.S3InputFormatConfigProperty(
                                s3_input_file_type="s3InputFileType"
                            )
                        ),
                        salesforce=appflow_mixins.CfnFlowPropsMixin.SalesforceSourcePropertiesProperty(
                            data_transfer_api="dataTransferApi",
                            enable_dynamic_field_update=False,
                            include_deleted_records=False,
                            object="object"
                        ),
                        sapo_data=appflow_mixins.CfnFlowPropsMixin.SAPODataSourcePropertiesProperty(
                            object_path="objectPath",
                            pagination_config=appflow_mixins.CfnFlowPropsMixin.SAPODataPaginationConfigProperty(
                                max_page_size=123
                            ),
                            parallelism_config=appflow_mixins.CfnFlowPropsMixin.SAPODataParallelismConfigProperty(
                                max_parallelism=123
                            )
                        ),
                        service_now=appflow_mixins.CfnFlowPropsMixin.ServiceNowSourcePropertiesProperty(
                            object="object"
                        ),
                        singular=appflow_mixins.CfnFlowPropsMixin.SingularSourcePropertiesProperty(
                            object="object"
                        ),
                        slack=appflow_mixins.CfnFlowPropsMixin.SlackSourcePropertiesProperty(
                            object="object"
                        ),
                        trendmicro=appflow_mixins.CfnFlowPropsMixin.TrendmicroSourcePropertiesProperty(
                            object="object"
                        ),
                        veeva=appflow_mixins.CfnFlowPropsMixin.VeevaSourcePropertiesProperty(
                            document_type="documentType",
                            include_all_versions=False,
                            include_renditions=False,
                            include_source_files=False,
                            object="object"
                        ),
                        zendesk=appflow_mixins.CfnFlowPropsMixin.ZendeskSourcePropertiesProperty(
                            object="object"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__48f78bc2a729b54459ab83913b643507c7819fe54a2759fb46212d3f57566a35)
                check_type(argname="argument api_version", value=api_version, expected_type=type_hints["api_version"])
                check_type(argname="argument connector_profile_name", value=connector_profile_name, expected_type=type_hints["connector_profile_name"])
                check_type(argname="argument connector_type", value=connector_type, expected_type=type_hints["connector_type"])
                check_type(argname="argument incremental_pull_config", value=incremental_pull_config, expected_type=type_hints["incremental_pull_config"])
                check_type(argname="argument source_connector_properties", value=source_connector_properties, expected_type=type_hints["source_connector_properties"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if api_version is not None:
                self._values["api_version"] = api_version
            if connector_profile_name is not None:
                self._values["connector_profile_name"] = connector_profile_name
            if connector_type is not None:
                self._values["connector_type"] = connector_type
            if incremental_pull_config is not None:
                self._values["incremental_pull_config"] = incremental_pull_config
            if source_connector_properties is not None:
                self._values["source_connector_properties"] = source_connector_properties

        @builtins.property
        def api_version(self) -> typing.Optional[builtins.str]:
            '''The API version of the connector when it's used as a source in the flow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceflowconfig.html#cfn-appflow-flow-sourceflowconfig-apiversion
            '''
            result = self._values.get("api_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def connector_profile_name(self) -> typing.Optional[builtins.str]:
            '''The name of the connector profile.

            This name must be unique for each connector profile in the AWS account .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceflowconfig.html#cfn-appflow-flow-sourceflowconfig-connectorprofilename
            '''
            result = self._values.get("connector_profile_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def connector_type(self) -> typing.Optional[builtins.str]:
            '''The type of connector, such as Salesforce, Amplitude, and so on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceflowconfig.html#cfn-appflow-flow-sourceflowconfig-connectortype
            '''
            result = self._values.get("connector_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def incremental_pull_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.IncrementalPullConfigProperty"]]:
            '''Defines the configuration for a scheduled incremental data pull.

            If a valid configuration is provided, the fields specified in the configuration are used when querying for the incremental data pull.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceflowconfig.html#cfn-appflow-flow-sourceflowconfig-incrementalpullconfig
            '''
            result = self._values.get("incremental_pull_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.IncrementalPullConfigProperty"]], result)

        @builtins.property
        def source_connector_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.SourceConnectorPropertiesProperty"]]:
            '''Specifies the information that is required to query a particular source connector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceflowconfig.html#cfn-appflow-flow-sourceflowconfig-sourceconnectorproperties
            '''
            result = self._values.get("source_connector_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.SourceConnectorPropertiesProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceFlowConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.SuccessResponseHandlingConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket_name": "bucketName", "bucket_prefix": "bucketPrefix"},
    )
    class SuccessResponseHandlingConfigProperty:
        def __init__(
            self,
            *,
            bucket_name: typing.Optional[builtins.str] = None,
            bucket_prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Determines how Amazon AppFlow handles the success response that it gets from the connector after placing data.

            For example, this setting would determine where to write the response from the destination connector upon a successful insert operation.

            :param bucket_name: The name of the Amazon S3 bucket.
            :param bucket_prefix: The Amazon S3 bucket prefix.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-successresponsehandlingconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                success_response_handling_config_property = appflow_mixins.CfnFlowPropsMixin.SuccessResponseHandlingConfigProperty(
                    bucket_name="bucketName",
                    bucket_prefix="bucketPrefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__12956c0582e1c3fb11603c1bd73683132eba8d6c43127f30af1c442283849bca)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_name is not None:
                self._values["bucket_name"] = bucket_name
            if bucket_prefix is not None:
                self._values["bucket_prefix"] = bucket_prefix

        @builtins.property
        def bucket_name(self) -> typing.Optional[builtins.str]:
            '''The name of the Amazon S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-successresponsehandlingconfig.html#cfn-appflow-flow-successresponsehandlingconfig-bucketname
            '''
            result = self._values.get("bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bucket_prefix(self) -> typing.Optional[builtins.str]:
            '''The Amazon S3 bucket prefix.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-successresponsehandlingconfig.html#cfn-appflow-flow-successresponsehandlingconfig-bucketprefix
            '''
            result = self._values.get("bucket_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SuccessResponseHandlingConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.TaskPropertiesObjectProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TaskPropertiesObjectProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A map used to store task-related information.

            The execution service looks for particular information based on the ``TaskType`` .

            :param key: The task property key.
            :param value: The task property value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-taskpropertiesobject.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                task_properties_object_property = appflow_mixins.CfnFlowPropsMixin.TaskPropertiesObjectProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2a55cb35fc2a4de31d45e25643b8d072bd13301c9a7d8150ea662bd9ade865e4)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The task property key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-taskpropertiesobject.html#cfn-appflow-flow-taskpropertiesobject-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The task property value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-taskpropertiesobject.html#cfn-appflow-flow-taskpropertiesobject-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TaskPropertiesObjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.TaskProperty",
        jsii_struct_bases=[],
        name_mapping={
            "connector_operator": "connectorOperator",
            "destination_field": "destinationField",
            "source_fields": "sourceFields",
            "task_properties": "taskProperties",
            "task_type": "taskType",
        },
    )
    class TaskProperty:
        def __init__(
            self,
            *,
            connector_operator: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.ConnectorOperatorProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            destination_field: typing.Optional[builtins.str] = None,
            source_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
            task_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.TaskPropertiesObjectProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            task_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A class for modeling different type of tasks.

            Task implementation varies based on the ``TaskType`` .

            :param connector_operator: The operation to be performed on the provided source fields.
            :param destination_field: A field in a destination connector, or a field value against which Amazon AppFlow validates a source field.
            :param source_fields: The source fields to which a particular task is applied.
            :param task_properties: A map used to store task-related information. The execution service looks for particular information based on the ``TaskType`` .
            :param task_type: Specifies the particular task implementation that Amazon AppFlow performs. *Allowed values* : ``Arithmetic`` | ``Filter`` | ``Map`` | ``Map_all`` | ``Mask`` | ``Merge`` | ``Truncate`` | ``Validate``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-task.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                task_property = appflow_mixins.CfnFlowPropsMixin.TaskProperty(
                    connector_operator=appflow_mixins.CfnFlowPropsMixin.ConnectorOperatorProperty(
                        amplitude="amplitude",
                        custom_connector="customConnector",
                        datadog="datadog",
                        dynatrace="dynatrace",
                        google_analytics="googleAnalytics",
                        infor_nexus="inforNexus",
                        marketo="marketo",
                        pardot="pardot",
                        s3="s3",
                        salesforce="salesforce",
                        sapo_data="sapoData",
                        service_now="serviceNow",
                        singular="singular",
                        slack="slack",
                        trendmicro="trendmicro",
                        veeva="veeva",
                        zendesk="zendesk"
                    ),
                    destination_field="destinationField",
                    source_fields=["sourceFields"],
                    task_properties=[appflow_mixins.CfnFlowPropsMixin.TaskPropertiesObjectProperty(
                        key="key",
                        value="value"
                    )],
                    task_type="taskType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__934543d9fe7310e35a4e48aa66e90f93f6855a2fb50e275982f5f88bfd23a901)
                check_type(argname="argument connector_operator", value=connector_operator, expected_type=type_hints["connector_operator"])
                check_type(argname="argument destination_field", value=destination_field, expected_type=type_hints["destination_field"])
                check_type(argname="argument source_fields", value=source_fields, expected_type=type_hints["source_fields"])
                check_type(argname="argument task_properties", value=task_properties, expected_type=type_hints["task_properties"])
                check_type(argname="argument task_type", value=task_type, expected_type=type_hints["task_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if connector_operator is not None:
                self._values["connector_operator"] = connector_operator
            if destination_field is not None:
                self._values["destination_field"] = destination_field
            if source_fields is not None:
                self._values["source_fields"] = source_fields
            if task_properties is not None:
                self._values["task_properties"] = task_properties
            if task_type is not None:
                self._values["task_type"] = task_type

        @builtins.property
        def connector_operator(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.ConnectorOperatorProperty"]]:
            '''The operation to be performed on the provided source fields.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-task.html#cfn-appflow-flow-task-connectoroperator
            '''
            result = self._values.get("connector_operator")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.ConnectorOperatorProperty"]], result)

        @builtins.property
        def destination_field(self) -> typing.Optional[builtins.str]:
            '''A field in a destination connector, or a field value against which Amazon AppFlow validates a source field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-task.html#cfn-appflow-flow-task-destinationfield
            '''
            result = self._values.get("destination_field")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_fields(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The source fields to which a particular task is applied.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-task.html#cfn-appflow-flow-task-sourcefields
            '''
            result = self._values.get("source_fields")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def task_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.TaskPropertiesObjectProperty"]]]]:
            '''A map used to store task-related information.

            The execution service looks for particular information based on the ``TaskType`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-task.html#cfn-appflow-flow-task-taskproperties
            '''
            result = self._values.get("task_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.TaskPropertiesObjectProperty"]]]], result)

        @builtins.property
        def task_type(self) -> typing.Optional[builtins.str]:
            '''Specifies the particular task implementation that Amazon AppFlow performs.

            *Allowed values* : ``Arithmetic`` | ``Filter`` | ``Map`` | ``Map_all`` | ``Mask`` | ``Merge`` | ``Truncate`` | ``Validate``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-task.html#cfn-appflow-flow-task-tasktype
            '''
            result = self._values.get("task_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TaskProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.TrendmicroSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"object": "object"},
    )
    class TrendmicroSourcePropertiesProperty:
        def __init__(self, *, object: typing.Optional[builtins.str] = None) -> None:
            '''The properties that are applied when using Trend Micro as a flow source.

            :param object: The object specified in the Trend Micro flow source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-trendmicrosourceproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                trendmicro_source_properties_property = appflow_mixins.CfnFlowPropsMixin.TrendmicroSourcePropertiesProperty(
                    object="object"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d4e73c0cef5d4e41c087ce3a3a2cb81db80fd3f192a5add84ee79a568d7e6a58)
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if object is not None:
                self._values["object"] = object

        @builtins.property
        def object(self) -> typing.Optional[builtins.str]:
            '''The object specified in the Trend Micro flow source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-trendmicrosourceproperties.html#cfn-appflow-flow-trendmicrosourceproperties-object
            '''
            result = self._values.get("object")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TrendmicroSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.TriggerConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "trigger_properties": "triggerProperties",
            "trigger_type": "triggerType",
        },
    )
    class TriggerConfigProperty:
        def __init__(
            self,
            *,
            trigger_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.ScheduledTriggerPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            trigger_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The trigger settings that determine how and when Amazon AppFlow runs the specified flow.

            :param trigger_properties: Specifies the configuration details of a schedule-triggered flow as defined by the user. Currently, these settings only apply to the ``Scheduled`` trigger type.
            :param trigger_type: Specifies the type of flow trigger. This can be ``OnDemand`` , ``Scheduled`` , or ``Event`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-triggerconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                trigger_config_property = appflow_mixins.CfnFlowPropsMixin.TriggerConfigProperty(
                    trigger_properties=appflow_mixins.CfnFlowPropsMixin.ScheduledTriggerPropertiesProperty(
                        data_pull_mode="dataPullMode",
                        first_execution_from=123,
                        flow_error_deactivation_threshold=123,
                        schedule_end_time=123,
                        schedule_expression="scheduleExpression",
                        schedule_offset=123,
                        schedule_start_time=123,
                        time_zone="timeZone"
                    ),
                    trigger_type="triggerType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4447b4f2a058dbef5a3ad9fd47462cd0ab9349f4080fe38893eb8a8dadcfb463)
                check_type(argname="argument trigger_properties", value=trigger_properties, expected_type=type_hints["trigger_properties"])
                check_type(argname="argument trigger_type", value=trigger_type, expected_type=type_hints["trigger_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if trigger_properties is not None:
                self._values["trigger_properties"] = trigger_properties
            if trigger_type is not None:
                self._values["trigger_type"] = trigger_type

        @builtins.property
        def trigger_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.ScheduledTriggerPropertiesProperty"]]:
            '''Specifies the configuration details of a schedule-triggered flow as defined by the user.

            Currently, these settings only apply to the ``Scheduled`` trigger type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-triggerconfig.html#cfn-appflow-flow-triggerconfig-triggerproperties
            '''
            result = self._values.get("trigger_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.ScheduledTriggerPropertiesProperty"]], result)

        @builtins.property
        def trigger_type(self) -> typing.Optional[builtins.str]:
            '''Specifies the type of flow trigger.

            This can be ``OnDemand`` , ``Scheduled`` , or ``Event`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-triggerconfig.html#cfn-appflow-flow-triggerconfig-triggertype
            '''
            result = self._values.get("trigger_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TriggerConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.UpsolverDestinationPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_name": "bucketName",
            "bucket_prefix": "bucketPrefix",
            "s3_output_format_config": "s3OutputFormatConfig",
        },
    )
    class UpsolverDestinationPropertiesProperty:
        def __init__(
            self,
            *,
            bucket_name: typing.Optional[builtins.str] = None,
            bucket_prefix: typing.Optional[builtins.str] = None,
            s3_output_format_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.UpsolverS3OutputFormatConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The properties that are applied when Upsolver is used as a destination.

            :param bucket_name: The Upsolver Amazon S3 bucket name in which Amazon AppFlow places the transferred data.
            :param bucket_prefix: The object key for the destination Upsolver Amazon S3 bucket in which Amazon AppFlow places the files.
            :param s3_output_format_config: The configuration that determines how data is formatted when Upsolver is used as the flow destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-upsolverdestinationproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                upsolver_destination_properties_property = appflow_mixins.CfnFlowPropsMixin.UpsolverDestinationPropertiesProperty(
                    bucket_name="bucketName",
                    bucket_prefix="bucketPrefix",
                    s3_output_format_config=appflow_mixins.CfnFlowPropsMixin.UpsolverS3OutputFormatConfigProperty(
                        aggregation_config=appflow_mixins.CfnFlowPropsMixin.AggregationConfigProperty(
                            aggregation_type="aggregationType",
                            target_file_size=123
                        ),
                        file_type="fileType",
                        prefix_config=appflow_mixins.CfnFlowPropsMixin.PrefixConfigProperty(
                            path_prefix_hierarchy=["pathPrefixHierarchy"],
                            prefix_format="prefixFormat",
                            prefix_type="prefixType"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1520165278288281bbdc54c6fcc91e877ae4cbbc2e0528215944e6dddd64bc73)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
                check_type(argname="argument s3_output_format_config", value=s3_output_format_config, expected_type=type_hints["s3_output_format_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_name is not None:
                self._values["bucket_name"] = bucket_name
            if bucket_prefix is not None:
                self._values["bucket_prefix"] = bucket_prefix
            if s3_output_format_config is not None:
                self._values["s3_output_format_config"] = s3_output_format_config

        @builtins.property
        def bucket_name(self) -> typing.Optional[builtins.str]:
            '''The Upsolver Amazon S3 bucket name in which Amazon AppFlow places the transferred data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-upsolverdestinationproperties.html#cfn-appflow-flow-upsolverdestinationproperties-bucketname
            '''
            result = self._values.get("bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bucket_prefix(self) -> typing.Optional[builtins.str]:
            '''The object key for the destination Upsolver Amazon S3 bucket in which Amazon AppFlow places the files.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-upsolverdestinationproperties.html#cfn-appflow-flow-upsolverdestinationproperties-bucketprefix
            '''
            result = self._values.get("bucket_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_output_format_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.UpsolverS3OutputFormatConfigProperty"]]:
            '''The configuration that determines how data is formatted when Upsolver is used as the flow destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-upsolverdestinationproperties.html#cfn-appflow-flow-upsolverdestinationproperties-s3outputformatconfig
            '''
            result = self._values.get("s3_output_format_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.UpsolverS3OutputFormatConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UpsolverDestinationPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.UpsolverS3OutputFormatConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "aggregation_config": "aggregationConfig",
            "file_type": "fileType",
            "prefix_config": "prefixConfig",
        },
    )
    class UpsolverS3OutputFormatConfigProperty:
        def __init__(
            self,
            *,
            aggregation_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.AggregationConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            file_type: typing.Optional[builtins.str] = None,
            prefix_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.PrefixConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The configuration that determines how Amazon AppFlow formats the flow output data when Upsolver is used as the destination.

            :param aggregation_config: The aggregation settings that you can use to customize the output format of your flow data.
            :param file_type: Indicates the file type that Amazon AppFlow places in the Upsolver Amazon S3 bucket.
            :param prefix_config: Specifies elements that Amazon AppFlow includes in the file and folder names in the flow destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-upsolvers3outputformatconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                upsolver_s3_output_format_config_property = appflow_mixins.CfnFlowPropsMixin.UpsolverS3OutputFormatConfigProperty(
                    aggregation_config=appflow_mixins.CfnFlowPropsMixin.AggregationConfigProperty(
                        aggregation_type="aggregationType",
                        target_file_size=123
                    ),
                    file_type="fileType",
                    prefix_config=appflow_mixins.CfnFlowPropsMixin.PrefixConfigProperty(
                        path_prefix_hierarchy=["pathPrefixHierarchy"],
                        prefix_format="prefixFormat",
                        prefix_type="prefixType"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4b604ac71f7ccd33e21ef94aa8009fb4189479cbb513063819c40ac292af71d2)
                check_type(argname="argument aggregation_config", value=aggregation_config, expected_type=type_hints["aggregation_config"])
                check_type(argname="argument file_type", value=file_type, expected_type=type_hints["file_type"])
                check_type(argname="argument prefix_config", value=prefix_config, expected_type=type_hints["prefix_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if aggregation_config is not None:
                self._values["aggregation_config"] = aggregation_config
            if file_type is not None:
                self._values["file_type"] = file_type
            if prefix_config is not None:
                self._values["prefix_config"] = prefix_config

        @builtins.property
        def aggregation_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.AggregationConfigProperty"]]:
            '''The aggregation settings that you can use to customize the output format of your flow data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-upsolvers3outputformatconfig.html#cfn-appflow-flow-upsolvers3outputformatconfig-aggregationconfig
            '''
            result = self._values.get("aggregation_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.AggregationConfigProperty"]], result)

        @builtins.property
        def file_type(self) -> typing.Optional[builtins.str]:
            '''Indicates the file type that Amazon AppFlow places in the Upsolver Amazon S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-upsolvers3outputformatconfig.html#cfn-appflow-flow-upsolvers3outputformatconfig-filetype
            '''
            result = self._values.get("file_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prefix_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.PrefixConfigProperty"]]:
            '''Specifies elements that Amazon AppFlow includes in the file and folder names in the flow destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-upsolvers3outputformatconfig.html#cfn-appflow-flow-upsolvers3outputformatconfig-prefixconfig
            '''
            result = self._values.get("prefix_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.PrefixConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UpsolverS3OutputFormatConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.VeevaSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "document_type": "documentType",
            "include_all_versions": "includeAllVersions",
            "include_renditions": "includeRenditions",
            "include_source_files": "includeSourceFiles",
            "object": "object",
        },
    )
    class VeevaSourcePropertiesProperty:
        def __init__(
            self,
            *,
            document_type: typing.Optional[builtins.str] = None,
            include_all_versions: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            include_renditions: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            include_source_files: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            object: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The properties that are applied when using Veeva as a flow source.

            :param document_type: The document type specified in the Veeva document extract flow.
            :param include_all_versions: Boolean value to include All Versions of files in Veeva document extract flow.
            :param include_renditions: Boolean value to include file renditions in Veeva document extract flow.
            :param include_source_files: Boolean value to include source files in Veeva document extract flow.
            :param object: The object specified in the Veeva flow source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-veevasourceproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                veeva_source_properties_property = appflow_mixins.CfnFlowPropsMixin.VeevaSourcePropertiesProperty(
                    document_type="documentType",
                    include_all_versions=False,
                    include_renditions=False,
                    include_source_files=False,
                    object="object"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d40770102231334fdd67ef58ed638f294bd221af97953273f209d1b133b7dbb2)
                check_type(argname="argument document_type", value=document_type, expected_type=type_hints["document_type"])
                check_type(argname="argument include_all_versions", value=include_all_versions, expected_type=type_hints["include_all_versions"])
                check_type(argname="argument include_renditions", value=include_renditions, expected_type=type_hints["include_renditions"])
                check_type(argname="argument include_source_files", value=include_source_files, expected_type=type_hints["include_source_files"])
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if document_type is not None:
                self._values["document_type"] = document_type
            if include_all_versions is not None:
                self._values["include_all_versions"] = include_all_versions
            if include_renditions is not None:
                self._values["include_renditions"] = include_renditions
            if include_source_files is not None:
                self._values["include_source_files"] = include_source_files
            if object is not None:
                self._values["object"] = object

        @builtins.property
        def document_type(self) -> typing.Optional[builtins.str]:
            '''The document type specified in the Veeva document extract flow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-veevasourceproperties.html#cfn-appflow-flow-veevasourceproperties-documenttype
            '''
            result = self._values.get("document_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def include_all_versions(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Boolean value to include All Versions of files in Veeva document extract flow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-veevasourceproperties.html#cfn-appflow-flow-veevasourceproperties-includeallversions
            '''
            result = self._values.get("include_all_versions")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def include_renditions(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Boolean value to include file renditions in Veeva document extract flow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-veevasourceproperties.html#cfn-appflow-flow-veevasourceproperties-includerenditions
            '''
            result = self._values.get("include_renditions")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def include_source_files(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Boolean value to include source files in Veeva document extract flow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-veevasourceproperties.html#cfn-appflow-flow-veevasourceproperties-includesourcefiles
            '''
            result = self._values.get("include_source_files")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def object(self) -> typing.Optional[builtins.str]:
            '''The object specified in the Veeva flow source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-veevasourceproperties.html#cfn-appflow-flow-veevasourceproperties-object
            '''
            result = self._values.get("object")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VeevaSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.ZendeskDestinationPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "error_handling_config": "errorHandlingConfig",
            "id_field_names": "idFieldNames",
            "object": "object",
            "write_operation_type": "writeOperationType",
        },
    )
    class ZendeskDestinationPropertiesProperty:
        def __init__(
            self,
            *,
            error_handling_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.ErrorHandlingConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            id_field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
            object: typing.Optional[builtins.str] = None,
            write_operation_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The properties that are applied when Zendesk is used as a destination.

            :param error_handling_config: The settings that determine how Amazon AppFlow handles an error when placing data in the destination. For example, this setting would determine if the flow should fail after one insertion error, or continue and attempt to insert every record regardless of the initial failure. ``ErrorHandlingConfig`` is a part of the destination connector details.
            :param id_field_names: A list of field names that can be used as an ID field when performing a write operation.
            :param object: The object specified in the Zendesk flow destination.
            :param write_operation_type: The possible write operations in the destination connector. When this value is not provided, this defaults to the ``INSERT`` operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-zendeskdestinationproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                zendesk_destination_properties_property = appflow_mixins.CfnFlowPropsMixin.ZendeskDestinationPropertiesProperty(
                    error_handling_config=appflow_mixins.CfnFlowPropsMixin.ErrorHandlingConfigProperty(
                        bucket_name="bucketName",
                        bucket_prefix="bucketPrefix",
                        fail_on_first_error=False
                    ),
                    id_field_names=["idFieldNames"],
                    object="object",
                    write_operation_type="writeOperationType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ec14c6181d25df50352936b05add3f1d56052633d17805f9f3bd1978a38a4e9b)
                check_type(argname="argument error_handling_config", value=error_handling_config, expected_type=type_hints["error_handling_config"])
                check_type(argname="argument id_field_names", value=id_field_names, expected_type=type_hints["id_field_names"])
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
                check_type(argname="argument write_operation_type", value=write_operation_type, expected_type=type_hints["write_operation_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if error_handling_config is not None:
                self._values["error_handling_config"] = error_handling_config
            if id_field_names is not None:
                self._values["id_field_names"] = id_field_names
            if object is not None:
                self._values["object"] = object
            if write_operation_type is not None:
                self._values["write_operation_type"] = write_operation_type

        @builtins.property
        def error_handling_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.ErrorHandlingConfigProperty"]]:
            '''The settings that determine how Amazon AppFlow handles an error when placing data in the destination.

            For example, this setting would determine if the flow should fail after one insertion error, or continue and attempt to insert every record regardless of the initial failure. ``ErrorHandlingConfig`` is a part of the destination connector details.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-zendeskdestinationproperties.html#cfn-appflow-flow-zendeskdestinationproperties-errorhandlingconfig
            '''
            result = self._values.get("error_handling_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.ErrorHandlingConfigProperty"]], result)

        @builtins.property
        def id_field_names(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of field names that can be used as an ID field when performing a write operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-zendeskdestinationproperties.html#cfn-appflow-flow-zendeskdestinationproperties-idfieldnames
            '''
            result = self._values.get("id_field_names")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def object(self) -> typing.Optional[builtins.str]:
            '''The object specified in the Zendesk flow destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-zendeskdestinationproperties.html#cfn-appflow-flow-zendeskdestinationproperties-object
            '''
            result = self._values.get("object")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def write_operation_type(self) -> typing.Optional[builtins.str]:
            '''The possible write operations in the destination connector.

            When this value is not provided, this defaults to the ``INSERT`` operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-zendeskdestinationproperties.html#cfn-appflow-flow-zendeskdestinationproperties-writeoperationtype
            '''
            result = self._values.get("write_operation_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ZendeskDestinationPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appflow.mixins.CfnFlowPropsMixin.ZendeskSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"object": "object"},
    )
    class ZendeskSourcePropertiesProperty:
        def __init__(self, *, object: typing.Optional[builtins.str] = None) -> None:
            '''The properties that are applied when using Zendesk as a flow source.

            :param object: The object specified in the Zendesk flow source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-zendesksourceproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appflow import mixins as appflow_mixins
                
                zendesk_source_properties_property = appflow_mixins.CfnFlowPropsMixin.ZendeskSourcePropertiesProperty(
                    object="object"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__43e6d46c0b6881a8cacaaa59444dc6a2238e59e61294c6096c3fd1c4c2528e2a)
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if object is not None:
                self._values["object"] = object

        @builtins.property
        def object(self) -> typing.Optional[builtins.str]:
            '''The object specified in the Zendesk flow source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-zendesksourceproperties.html#cfn-appflow-flow-zendesksourceproperties-object
            '''
            result = self._values.get("object")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ZendeskSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnConnectorMixinProps",
    "CfnConnectorProfileMixinProps",
    "CfnConnectorProfilePropsMixin",
    "CfnConnectorPropsMixin",
    "CfnFlowMixinProps",
    "CfnFlowPropsMixin",
]

publication.publish()

def _typecheckingstub__b688737a9dc541ee06befd87c4543a4ed816d85cc98d2d4631ddd99511343f8f(
    *,
    connector_label: typing.Optional[builtins.str] = None,
    connector_provisioning_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorPropsMixin.ConnectorProvisioningConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    connector_provisioning_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__616c02b61a44852d825fee625a6ce8b7be3ccb947496187cffd3837faa165fef(
    *,
    connection_mode: typing.Optional[builtins.str] = None,
    connector_label: typing.Optional[builtins.str] = None,
    connector_profile_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.ConnectorProfileConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    connector_profile_name: typing.Optional[builtins.str] = None,
    connector_type: typing.Optional[builtins.str] = None,
    kms_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56ae9522601d40fc2242c76e3c6c580bde26b2382a4fe7e7f5092f8784359d2b(
    props: typing.Union[CfnConnectorProfileMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bcd640fe28e820fa355967fe5d027874aa67fd4e7b40b17f3b273f98db68b6a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6557c6094438c01903da683975baf009d9cab04fd53335bb62dc33b2e0af7434(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b75e9c3175d6f1cb737df207dda7b1aebb81dfdf73a5f0a4757d3750285655f(
    *,
    api_key: typing.Optional[builtins.str] = None,
    secret_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12c1a3d822ffe619d0f4c80e8044e2f33f46bc2d26db79ba9c90fcd7c8e47264(
    *,
    api_key: typing.Optional[builtins.str] = None,
    api_secret_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c73d87c88877efc56205917020005d0b3ba3df0e33e6ca3430b923d71fa034c9(
    *,
    password: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d98ef7bcb3ffa68249b1c8e23a0c87b751d4b6b4542680c309507a050f17871(
    *,
    auth_code: typing.Optional[builtins.str] = None,
    redirect_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1658835a6d8641ac55e57fff2b1fa1cb665f39019a1eab06d8f6bf580436f133(
    *,
    connector_profile_credentials: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.ConnectorProfileCredentialsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    connector_profile_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.ConnectorProfilePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c26030621b6284cac5ddf7e4ed54997b7c2aa055ea2ef910346c1578190bdc31(
    *,
    amplitude: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.AmplitudeConnectorProfileCredentialsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    custom_connector: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.CustomConnectorProfileCredentialsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    datadog: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.DatadogConnectorProfileCredentialsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dynatrace: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.DynatraceConnectorProfileCredentialsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    google_analytics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.GoogleAnalyticsConnectorProfileCredentialsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    infor_nexus: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.InforNexusConnectorProfileCredentialsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    marketo: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.MarketoConnectorProfileCredentialsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    pardot: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.PardotConnectorProfileCredentialsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    redshift: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.RedshiftConnectorProfileCredentialsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    salesforce: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.SalesforceConnectorProfileCredentialsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sapo_data: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.SAPODataConnectorProfileCredentialsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    service_now: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.ServiceNowConnectorProfileCredentialsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    singular: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.SingularConnectorProfileCredentialsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    slack: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.SlackConnectorProfileCredentialsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    snowflake: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.SnowflakeConnectorProfileCredentialsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    trendmicro: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.TrendmicroConnectorProfileCredentialsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    veeva: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.VeevaConnectorProfileCredentialsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    zendesk: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.ZendeskConnectorProfileCredentialsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42c9f5518a432918c5de510ce82007e540b82507dfe62dddf30a9f582dcda0ae(
    *,
    custom_connector: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.CustomConnectorProfilePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    datadog: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.DatadogConnectorProfilePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dynatrace: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.DynatraceConnectorProfilePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    infor_nexus: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.InforNexusConnectorProfilePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    marketo: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.MarketoConnectorProfilePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    pardot: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.PardotConnectorProfilePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    redshift: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.RedshiftConnectorProfilePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    salesforce: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.SalesforceConnectorProfilePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sapo_data: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.SAPODataConnectorProfilePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    service_now: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.ServiceNowConnectorProfilePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    slack: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.SlackConnectorProfilePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    snowflake: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.SnowflakeConnectorProfilePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    veeva: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.VeevaConnectorProfilePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    zendesk: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.ZendeskConnectorProfilePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68c7c8e82201ad0d7db7eecfee433a3070b6db776463d7efd6da5539c2fead4c(
    *,
    credentials_map: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    custom_authentication_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be3c0e48c0c2435eb752cc2ceb29ff848dd87958a1429d9ca25544ea592ebd33(
    *,
    api_key: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.ApiKeyCredentialsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    authentication_type: typing.Optional[builtins.str] = None,
    basic: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.BasicAuthCredentialsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    custom: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.CustomAuthCredentialsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    oauth2: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.OAuth2CredentialsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__137a606e63a6b4cfa545ced0408d05476d64e43df4b05b47bf896dab50e3e1d6(
    *,
    o_auth2_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.OAuth2PropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    profile_properties: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a499b3939b5d77883fdab18c50f768a4dad9cef9bdddcd558e7c4dffaa796a7d(
    *,
    api_key: typing.Optional[builtins.str] = None,
    application_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e53e94bf856c66366647d7f144bc0e7bf12aa8f1e7086e6fa9ce1a1c2330efce(
    *,
    instance_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d36c22e9d75908d30e008193ab40c6055eea17706ce1effe13a867b1f012771b(
    *,
    api_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04b07602c368786946816996d5d3ff2c0414ea3a1c2e2e6925f803bfa16ec6a8(
    *,
    instance_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44b968662f544f8fe0a61123f41ae86437601fa816fb7077cacf33da77003f2f(
    *,
    access_token: typing.Optional[builtins.str] = None,
    client_id: typing.Optional[builtins.str] = None,
    client_secret: typing.Optional[builtins.str] = None,
    connector_o_auth_request: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    refresh_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9a1288438d705acf6103dbb0f6de84702321065586fc9a9137e7f516c46598f(
    *,
    access_key_id: typing.Optional[builtins.str] = None,
    datakey: typing.Optional[builtins.str] = None,
    secret_access_key: typing.Optional[builtins.str] = None,
    user_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ba63f4a603127c9973d777327b774c293f2dddbc21925f7900377d8005f2dc5(
    *,
    instance_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a597e43c9eed964535f959ef98f0052df1102ee44f65803081357a31960d2e5(
    *,
    access_token: typing.Optional[builtins.str] = None,
    client_id: typing.Optional[builtins.str] = None,
    client_secret: typing.Optional[builtins.str] = None,
    connector_o_auth_request: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66549bd7502d034d51fd17edf1c6efbd8ea21a3edf31dde5c364786c68476985(
    *,
    instance_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bd52b9793e4e2f694b91fb23b192c734322eb4b4ccb52c9546f783ad1958af2(
    *,
    access_token: typing.Optional[builtins.str] = None,
    client_id: typing.Optional[builtins.str] = None,
    client_secret: typing.Optional[builtins.str] = None,
    o_auth_request: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    refresh_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f76bc658ee8a586a5a4121ac225ddc9e65c0401ca8c25f41c3031345b8251675(
    *,
    o_auth2_grant_type: typing.Optional[builtins.str] = None,
    token_url: typing.Optional[builtins.str] = None,
    token_url_custom_properties: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5ae19965f35aff50d6468c49a046c9111626f3f4e4333fab18828db4d83c25e(
    *,
    access_token: typing.Optional[builtins.str] = None,
    client_id: typing.Optional[builtins.str] = None,
    client_secret: typing.Optional[builtins.str] = None,
    connector_o_auth_request: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    refresh_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69bfe5bc4f93cf5fe4c61ffce3033f07a9d597afb8acadc8e8233a750f0baa32(
    *,
    auth_code_url: typing.Optional[builtins.str] = None,
    o_auth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    token_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f723aa7e3dd5ad7db2cbd59d52b03c7d23915692b2713f8ad8bf50d64e2fd20(
    *,
    access_token: typing.Optional[builtins.str] = None,
    client_credentials_arn: typing.Optional[builtins.str] = None,
    connector_o_auth_request: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    refresh_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__244e28bb4c3ab8d346e4a2b89a2e910f29f0f2b058b682e9d9a2f973513cb2b4(
    *,
    business_unit_id: typing.Optional[builtins.str] = None,
    instance_url: typing.Optional[builtins.str] = None,
    is_sandbox_environment: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9bd0499091e4eab819322ba94275493ec3e9de5d24965fe5e40758ac0fda6ee(
    *,
    password: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c58a7acd58839763a5646d7e0d03fdab26dd6b160a71e6c16ea85323e6ebec8b(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    bucket_prefix: typing.Optional[builtins.str] = None,
    cluster_identifier: typing.Optional[builtins.str] = None,
    data_api_role_arn: typing.Optional[builtins.str] = None,
    database_name: typing.Optional[builtins.str] = None,
    database_url: typing.Optional[builtins.str] = None,
    is_redshift_serverless: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    role_arn: typing.Optional[builtins.str] = None,
    workgroup_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__052b03410cd136f1f606593889ec16dcbd19f3ae470efe383e9ed2c1c3907c45(
    *,
    basic_auth_credentials: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.BasicAuthCredentialsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    o_auth_credentials: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.OAuthCredentialsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5b3de1976e617be5326b07f40b3bfb1b693d8305472338cfefd20a21e6973bc(
    *,
    application_host_url: typing.Optional[builtins.str] = None,
    application_service_path: typing.Optional[builtins.str] = None,
    client_number: typing.Optional[builtins.str] = None,
    disable_sso: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    logon_language: typing.Optional[builtins.str] = None,
    o_auth_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.OAuthPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    port_number: typing.Optional[jsii.Number] = None,
    private_link_service_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__438746ccf4f09ca419124f99f4ab4e1e7af61f6dd746c834f4807962667c1d34(
    *,
    access_token: typing.Optional[builtins.str] = None,
    client_credentials_arn: typing.Optional[builtins.str] = None,
    connector_o_auth_request: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    jwt_token: typing.Optional[builtins.str] = None,
    o_auth2_grant_type: typing.Optional[builtins.str] = None,
    refresh_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__440877404d04efb4be2b66706d9261862060211e67575ce1e7b3e70f8136a65e(
    *,
    instance_url: typing.Optional[builtins.str] = None,
    is_sandbox_environment: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    use_private_link_for_metadata_and_authorization: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6c84c861fe401a42808f31b97bc4bd11a01004c4115f3f2fc4eddafc000fd1e(
    *,
    o_auth2_credentials: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.OAuth2CredentialsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    password: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c63dc2bbf0186db6fea27f0466fbf9b29f75f34608c0b81be3c27f8a01b05c94(
    *,
    instance_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea7cfda8cd1042a1f9d054ee09932b1c35d066a6be8dc4582c94b368c5f2e035(
    *,
    api_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d83fcfc7fef569f6264046286cba7b5a0d94ec800dd52611a81228c708c30560(
    *,
    access_token: typing.Optional[builtins.str] = None,
    client_id: typing.Optional[builtins.str] = None,
    client_secret: typing.Optional[builtins.str] = None,
    connector_o_auth_request: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b31b52814e341e3b85fc9f475f4911290ef6d6ce054afa2d7fc704894e551efd(
    *,
    instance_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c62add8b09d7bf74aabae4145968ec5794dcfb8adf028cfe0a073de79f5c977(
    *,
    password: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81a6d0c4e8947d2ba97151a274df03479c5e0a4e096a49337f7968396135b23b(
    *,
    account_name: typing.Optional[builtins.str] = None,
    bucket_name: typing.Optional[builtins.str] = None,
    bucket_prefix: typing.Optional[builtins.str] = None,
    private_link_service_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    stage: typing.Optional[builtins.str] = None,
    warehouse: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e9310323b51e30591843a82e9ef6bb548c957e7769d4874f99f125174b04bc0(
    *,
    api_secret_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9e8f711433dc7612dd152670aeb3d6adfd2bb5a6787a42b189b0132a0938f80(
    *,
    password: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f98cafd94131004eb42183a84351b5405e23be6011cfe4fed0622d54515e9c03(
    *,
    instance_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__458961bcc0045f8bffad26ee111a8a44ca6ff260a85304aad38fc175632ecd24(
    *,
    access_token: typing.Optional[builtins.str] = None,
    client_id: typing.Optional[builtins.str] = None,
    client_secret: typing.Optional[builtins.str] = None,
    connector_o_auth_request: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorProfilePropsMixin.ConnectorOAuthRequestProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__118b4554c4e2cc23e2d61439d569cc5c1c86f40ce011bd330cf60a73d45f3ad8(
    *,
    instance_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a72738a5c2ea1ea2ffff0d320882fa202b88ee18be11b0020ed82f3ada21f33b(
    props: typing.Union[CfnConnectorMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__101624703bf09f5e755abdc24c0bad5fc52a24162f9dba6078ab333fb67706ca(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f75ceb787f3b7f6cc4752609f47c74f59875a54a40a7a91b1507ca745950500f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcf94d39bcdc77f9e2f060b1b7ff7d7500c3130a005f6f87f12e7906763ac4b8(
    *,
    lambda_: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorPropsMixin.LambdaConnectorProvisioningConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6681cf7a0a07d8c45015302bc81074ae1fbc7788225c55abbb984b2ed6199c6f(
    *,
    lambda_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc96d5aa9ea8401c816efcad2a92f807b1a086b7801e0d79ce9d78fe7717302e(
    *,
    description: typing.Optional[builtins.str] = None,
    destination_flow_config_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.DestinationFlowConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    flow_name: typing.Optional[builtins.str] = None,
    flow_status: typing.Optional[builtins.str] = None,
    kms_arn: typing.Optional[builtins.str] = None,
    metadata_catalog_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.MetadataCatalogConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    source_flow_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.SourceFlowConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    tasks: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.TaskProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    trigger_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.TriggerConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c502d7408c8258708710ecf0e2408c7cc3752c5ca34fb3c04dc4b1ece1caf8ea(
    props: typing.Union[CfnFlowMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e722a34a7335b46d6f83ee2598d169dc79800ee44d1565c6076f8f57c50b95a8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bd6020242eb35eaaa1aee1b815f8876a3dda4e2a915401116c37fb791876200(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d028e4dd84c95e074f477551c9f2f2ce206947bdb0e495a5eef2f84ed97e98fd(
    *,
    aggregation_type: typing.Optional[builtins.str] = None,
    target_file_size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce786fc2531ba1c14a6987a4dea9e11d2bb423a083eb13259bab3422fa2fe8d9(
    *,
    object: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__787267d13b6cacdc6806f0412a1d678c57105393e1ca5fb95c29830eb55b488d(
    *,
    amplitude: typing.Optional[builtins.str] = None,
    custom_connector: typing.Optional[builtins.str] = None,
    datadog: typing.Optional[builtins.str] = None,
    dynatrace: typing.Optional[builtins.str] = None,
    google_analytics: typing.Optional[builtins.str] = None,
    infor_nexus: typing.Optional[builtins.str] = None,
    marketo: typing.Optional[builtins.str] = None,
    pardot: typing.Optional[builtins.str] = None,
    s3: typing.Optional[builtins.str] = None,
    salesforce: typing.Optional[builtins.str] = None,
    sapo_data: typing.Optional[builtins.str] = None,
    service_now: typing.Optional[builtins.str] = None,
    singular: typing.Optional[builtins.str] = None,
    slack: typing.Optional[builtins.str] = None,
    trendmicro: typing.Optional[builtins.str] = None,
    veeva: typing.Optional[builtins.str] = None,
    zendesk: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f851e88bcbc39b239ad177df5430beacae4369c62e6eee6f985e4571e076261(
    *,
    custom_properties: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    entity_name: typing.Optional[builtins.str] = None,
    error_handling_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.ErrorHandlingConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    id_field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    write_operation_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48fa68bc02b3388e65e044412a92064faf19fdf21bb02b13a694a3428d8af132(
    *,
    custom_properties: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    data_transfer_api: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.DataTransferApiProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    entity_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2638f8d895abf4c8627e2cf3cb75a94b8b115803626f81f2eec85294945d68f9(
    *,
    name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3131157fcb7022cc91f6632ca988c81c73a894b289593b2dcdda0efb30f6fa5(
    *,
    object: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82264f976c13c1d2f4fd0cc33da6f943f7823cee1ed981a4cec76237e4894bf2(
    *,
    custom_connector: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.CustomConnectorDestinationPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    event_bridge: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.EventBridgeDestinationPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    lookout_metrics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.LookoutMetricsDestinationPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    marketo: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.MarketoDestinationPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    redshift: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.RedshiftDestinationPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.S3DestinationPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    salesforce: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.SalesforceDestinationPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sapo_data: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.SAPODataDestinationPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    snowflake: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.SnowflakeDestinationPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    upsolver: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.UpsolverDestinationPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    zendesk: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.ZendeskDestinationPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0c6cb1a11a4744b0ddec04a6a20c5ab48cff62bb192e8ee68ced63263548445(
    *,
    api_version: typing.Optional[builtins.str] = None,
    connector_profile_name: typing.Optional[builtins.str] = None,
    connector_type: typing.Optional[builtins.str] = None,
    destination_connector_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.DestinationConnectorPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__230fd2d312288e46e403b645485df1d31fedf726b694ca0680d239d9e1193031(
    *,
    object: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4065dce4d72c826afb191d7e5c205f49b7d4b79b630b1055b46d7d4affc0c363(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    bucket_prefix: typing.Optional[builtins.str] = None,
    fail_on_first_error: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91769fd2a2e5ba352dcfe82d3a2351114da4a3aa609ecc97faa422a432e0ed4f(
    *,
    error_handling_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.ErrorHandlingConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    object: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e5b8c56e9f469ca6ed7056151eb4e985ccbf952270662668a90610fc16fff47(
    *,
    database_name: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    table_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c57fecab276c04362dedb9aa45b2664e1d0c73d24cbeb270702b15c53af04b1f(
    *,
    object: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c391fc6658aeec845d9832ec03c3c0551bda52952cb0b07fad03d150ed811de(
    *,
    datetime_type_field_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ab075e0721a114cd264c2300b3e7b3065266f858d3c013f15c22f182e7abcdf(
    *,
    object: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f75576f4a7df4defda9b8d3439b3daaadd07fd8a04de852f2a5a0d42f7e936d1(
    *,
    object: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a032965665352407c05567bbc0542e3603006cc1e91df1a65d220dc914e83232(
    *,
    error_handling_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.ErrorHandlingConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    object: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3e08ff283d02957c52927dd1b19805cee773593c794ef2d18513c29cbe0f13f(
    *,
    object: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e8f0aff3574c300354ec0e97f9aee4605c9b2d7f82973165b9466b47993d64d(
    *,
    glue_data_catalog: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.GlueDataCatalogProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8f87275ad5594ba16ab4c0e439b6f31f310425a0db994a6505780d974b618cc(
    *,
    object: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4918cb993dc2b15c90f54d46fa3e513eeaa934b9df15c67cd9b6c0236db7728a(
    *,
    path_prefix_hierarchy: typing.Optional[typing.Sequence[builtins.str]] = None,
    prefix_format: typing.Optional[builtins.str] = None,
    prefix_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__050232b583fbe45b3f1fbd8985b229d9828a9f7a15aa2d5750849b19b0d7d043(
    *,
    bucket_prefix: typing.Optional[builtins.str] = None,
    error_handling_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.ErrorHandlingConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    intermediate_bucket_name: typing.Optional[builtins.str] = None,
    object: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d7a2315dd70b0fdb4076ef6ae297b0d6c7906fc0d3aeb992977332cb7eddd6d(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    bucket_prefix: typing.Optional[builtins.str] = None,
    s3_output_format_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.S3OutputFormatConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f0da923523d1ecf8325831f2ae1af46e4d7b6f3d2bf05afff6ec0750355393c(
    *,
    s3_input_file_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11017116846bda1d4f21a1c8ec35e3f18faf07a1c2fda0214a8f9218d6fb8aee(
    *,
    aggregation_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.AggregationConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    file_type: typing.Optional[builtins.str] = None,
    prefix_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.PrefixConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    preserve_source_data_typing: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b608c2f0272c79d437e7860b11877a30347d41fad50c5471aa0d7fda8836d836(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    bucket_prefix: typing.Optional[builtins.str] = None,
    s3_input_format_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.S3InputFormatConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63d045e8c1d465903b7d12bcdfee49f3dadeb1582165f5549befa3cea1784201(
    *,
    error_handling_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.ErrorHandlingConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    id_field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    object_path: typing.Optional[builtins.str] = None,
    success_response_handling_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.SuccessResponseHandlingConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    write_operation_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c908481354573b0589b95471fc9c44ea5038a248c8927569ab42e1fbc704bb9(
    *,
    max_page_size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__292021d2998e059ebadeed06d9c649bcd9f47eef218876fd1c4f261aaa36c1e5(
    *,
    max_parallelism: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcebee339e7afa43a72a37af511bd5019925bbd6b043637f0fa6589ee84d0d70(
    *,
    object_path: typing.Optional[builtins.str] = None,
    pagination_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.SAPODataPaginationConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    parallelism_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.SAPODataParallelismConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3cdf139dc0f3e657e6a3b5b07cfe3055c5c130c6cd8daeb2f091cdc8fe961d2(
    *,
    data_transfer_api: typing.Optional[builtins.str] = None,
    error_handling_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.ErrorHandlingConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    id_field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    object: typing.Optional[builtins.str] = None,
    write_operation_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eab8c820a0beb16bbf79d54d683678c75fcad3b265997588e27dae4ee4293a52(
    *,
    data_transfer_api: typing.Optional[builtins.str] = None,
    enable_dynamic_field_update: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    include_deleted_records: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    object: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39c074bb2c4e76cf5f1d76ef5ef8dabead16d20d0f60154e219a437b5a21240a(
    *,
    data_pull_mode: typing.Optional[builtins.str] = None,
    first_execution_from: typing.Optional[jsii.Number] = None,
    flow_error_deactivation_threshold: typing.Optional[jsii.Number] = None,
    schedule_end_time: typing.Optional[jsii.Number] = None,
    schedule_expression: typing.Optional[builtins.str] = None,
    schedule_offset: typing.Optional[jsii.Number] = None,
    schedule_start_time: typing.Optional[jsii.Number] = None,
    time_zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3612c45ddc8ca51659ab259a61b521de2af262a15007dcc846b3f9da37cb4188(
    *,
    object: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04b88fa137861d14c3c51cb521164b2cfcab22d5bd38499564d39e1733b105dc(
    *,
    object: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e2bca9da6080ccc621d291b7e1bca23699b1788186c27a38c06aa2b9076e2f4(
    *,
    object: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeab24d3778d99ef17ff5419af894e61e26258ce5241e2fd49ceca2e22338c5c(
    *,
    bucket_prefix: typing.Optional[builtins.str] = None,
    error_handling_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.ErrorHandlingConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    intermediate_bucket_name: typing.Optional[builtins.str] = None,
    object: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5522685b84294bc774e4be814ac166f368d66c76db6bda1048672cd8c48f487b(
    *,
    amplitude: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.AmplitudeSourcePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    custom_connector: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.CustomConnectorSourcePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    datadog: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.DatadogSourcePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dynatrace: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.DynatraceSourcePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    google_analytics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.GoogleAnalyticsSourcePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    infor_nexus: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.InforNexusSourcePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    marketo: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.MarketoSourcePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    pardot: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.PardotSourcePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.S3SourcePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    salesforce: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.SalesforceSourcePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sapo_data: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.SAPODataSourcePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    service_now: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.ServiceNowSourcePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    singular: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.SingularSourcePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    slack: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.SlackSourcePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    trendmicro: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.TrendmicroSourcePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    veeva: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.VeevaSourcePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    zendesk: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.ZendeskSourcePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48f78bc2a729b54459ab83913b643507c7819fe54a2759fb46212d3f57566a35(
    *,
    api_version: typing.Optional[builtins.str] = None,
    connector_profile_name: typing.Optional[builtins.str] = None,
    connector_type: typing.Optional[builtins.str] = None,
    incremental_pull_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.IncrementalPullConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    source_connector_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.SourceConnectorPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12956c0582e1c3fb11603c1bd73683132eba8d6c43127f30af1c442283849bca(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    bucket_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a55cb35fc2a4de31d45e25643b8d072bd13301c9a7d8150ea662bd9ade865e4(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__934543d9fe7310e35a4e48aa66e90f93f6855a2fb50e275982f5f88bfd23a901(
    *,
    connector_operator: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.ConnectorOperatorProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    destination_field: typing.Optional[builtins.str] = None,
    source_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
    task_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.TaskPropertiesObjectProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    task_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4e73c0cef5d4e41c087ce3a3a2cb81db80fd3f192a5add84ee79a568d7e6a58(
    *,
    object: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4447b4f2a058dbef5a3ad9fd47462cd0ab9349f4080fe38893eb8a8dadcfb463(
    *,
    trigger_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.ScheduledTriggerPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    trigger_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1520165278288281bbdc54c6fcc91e877ae4cbbc2e0528215944e6dddd64bc73(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    bucket_prefix: typing.Optional[builtins.str] = None,
    s3_output_format_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.UpsolverS3OutputFormatConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b604ac71f7ccd33e21ef94aa8009fb4189479cbb513063819c40ac292af71d2(
    *,
    aggregation_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.AggregationConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    file_type: typing.Optional[builtins.str] = None,
    prefix_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.PrefixConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d40770102231334fdd67ef58ed638f294bd221af97953273f209d1b133b7dbb2(
    *,
    document_type: typing.Optional[builtins.str] = None,
    include_all_versions: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    include_renditions: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    include_source_files: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    object: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec14c6181d25df50352936b05add3f1d56052633d17805f9f3bd1978a38a4e9b(
    *,
    error_handling_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.ErrorHandlingConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    id_field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    object: typing.Optional[builtins.str] = None,
    write_operation_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43e6d46c0b6881a8cacaaa59444dc6a2238e59e61294c6096c3fd1c4c2528e2a(
    *,
    object: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
