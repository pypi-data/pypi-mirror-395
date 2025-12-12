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
    jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnConnectionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "aws_location": "awsLocation",
        "description": "description",
        "domain_identifier": "domainIdentifier",
        "enable_trusted_identity_propagation": "enableTrustedIdentityPropagation",
        "environment_identifier": "environmentIdentifier",
        "name": "name",
        "project_identifier": "projectIdentifier",
        "props": "props",
        "scope": "scope",
    },
)
class CfnConnectionMixinProps:
    def __init__(
        self,
        *,
        aws_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectionPropsMixin.AwsLocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        domain_identifier: typing.Optional[builtins.str] = None,
        enable_trusted_identity_propagation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        environment_identifier: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        project_identifier: typing.Optional[builtins.str] = None,
        props: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectionPropsMixin.ConnectionPropertiesInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        scope: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnConnectionPropsMixin.

        :param aws_location: The location where the connection is created.
        :param description: Connection description.
        :param domain_identifier: The ID of the domain where the connection is created.
        :param enable_trusted_identity_propagation: Specifies whether the trusted identity propagation is enabled.
        :param environment_identifier: The ID of the environment where the connection is created.
        :param name: The name of the connection.
        :param project_identifier: The identifier of the project in which the connection should be created. If
        :param props: Connection props.
        :param scope: The scope of the connection.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-connection.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
            
            cfn_connection_mixin_props = datazone_mixins.CfnConnectionMixinProps(
                aws_location=datazone_mixins.CfnConnectionPropsMixin.AwsLocationProperty(
                    access_role="accessRole",
                    aws_account_id="awsAccountId",
                    aws_region="awsRegion",
                    iam_connection_id="iamConnectionId"
                ),
                description="description",
                domain_identifier="domainIdentifier",
                enable_trusted_identity_propagation=False,
                environment_identifier="environmentIdentifier",
                name="name",
                project_identifier="projectIdentifier",
                props=datazone_mixins.CfnConnectionPropsMixin.ConnectionPropertiesInputProperty(
                    amazon_qProperties=datazone_mixins.CfnConnectionPropsMixin.AmazonQPropertiesInputProperty(
                        auth_mode="authMode",
                        is_enabled=False,
                        profile_arn="profileArn"
                    ),
                    athena_properties=datazone_mixins.CfnConnectionPropsMixin.AthenaPropertiesInputProperty(
                        workgroup_name="workgroupName"
                    ),
                    glue_properties=datazone_mixins.CfnConnectionPropsMixin.GluePropertiesInputProperty(
                        glue_connection_input=datazone_mixins.CfnConnectionPropsMixin.GlueConnectionInputProperty(
                            athena_properties={
                                "athena_properties_key": "athenaProperties"
                            },
                            authentication_configuration=datazone_mixins.CfnConnectionPropsMixin.AuthenticationConfigurationInputProperty(
                                authentication_type="authenticationType",
                                basic_authentication_credentials=datazone_mixins.CfnConnectionPropsMixin.BasicAuthenticationCredentialsProperty(
                                    password="password",
                                    user_name="userName"
                                ),
                                custom_authentication_credentials={
                                    "custom_authentication_credentials_key": "customAuthenticationCredentials"
                                },
                                kms_key_arn="kmsKeyArn",
                                o_auth2_properties=datazone_mixins.CfnConnectionPropsMixin.OAuth2PropertiesProperty(
                                    authorization_code_properties=datazone_mixins.CfnConnectionPropsMixin.AuthorizationCodePropertiesProperty(
                                        authorization_code="authorizationCode",
                                        redirect_uri="redirectUri"
                                    ),
                                    o_auth2_client_application=datazone_mixins.CfnConnectionPropsMixin.OAuth2ClientApplicationProperty(
                                        aws_managed_client_application_reference="awsManagedClientApplicationReference",
                                        user_managed_client_application_client_id="userManagedClientApplicationClientId"
                                    ),
                                    o_auth2_credentials=datazone_mixins.CfnConnectionPropsMixin.GlueOAuth2CredentialsProperty(
                                        access_token="accessToken",
                                        jwt_token="jwtToken",
                                        refresh_token="refreshToken",
                                        user_managed_client_application_client_secret="userManagedClientApplicationClientSecret"
                                    ),
                                    o_auth2_grant_type="oAuth2GrantType",
                                    token_url="tokenUrl",
                                    token_url_parameters_map={
                                        "token_url_parameters_map_key": "tokenUrlParametersMap"
                                    }
                                ),
                                secret_arn="secretArn"
                            ),
                            connection_properties={
                                "connection_properties_key": "connectionProperties"
                            },
                            connection_type="connectionType",
                            description="description",
                            match_criteria="matchCriteria",
                            name="name",
                            physical_connection_requirements=datazone_mixins.CfnConnectionPropsMixin.PhysicalConnectionRequirementsProperty(
                                availability_zone="availabilityZone",
                                security_group_id_list=["securityGroupIdList"],
                                subnet_id="subnetId",
                                subnet_id_list=["subnetIdList"]
                            ),
                            python_properties={
                                "python_properties_key": "pythonProperties"
                            },
                            spark_properties={
                                "spark_properties_key": "sparkProperties"
                            },
                            validate_credentials=False,
                            validate_for_compute_environments=["validateForComputeEnvironments"]
                        )
                    ),
                    hyper_pod_properties=datazone_mixins.CfnConnectionPropsMixin.HyperPodPropertiesInputProperty(
                        cluster_name="clusterName"
                    ),
                    iam_properties=datazone_mixins.CfnConnectionPropsMixin.IamPropertiesInputProperty(
                        glue_lineage_sync_enabled=False
                    ),
                    redshift_properties=datazone_mixins.CfnConnectionPropsMixin.RedshiftPropertiesInputProperty(
                        credentials=datazone_mixins.CfnConnectionPropsMixin.RedshiftCredentialsProperty(
                            secret_arn="secretArn",
                            username_password=datazone_mixins.CfnConnectionPropsMixin.UsernamePasswordProperty(
                                password="password",
                                username="username"
                            )
                        ),
                        database_name="databaseName",
                        host="host",
                        lineage_sync=datazone_mixins.CfnConnectionPropsMixin.RedshiftLineageSyncConfigurationInputProperty(
                            enabled=False,
                            schedule=datazone_mixins.CfnConnectionPropsMixin.LineageSyncScheduleProperty(
                                schedule="schedule"
                            )
                        ),
                        port=123,
                        storage=datazone_mixins.CfnConnectionPropsMixin.RedshiftStoragePropertiesProperty(
                            cluster_name="clusterName",
                            workgroup_name="workgroupName"
                        )
                    ),
                    s3_properties=datazone_mixins.CfnConnectionPropsMixin.S3PropertiesInputProperty(
                        s3_access_grant_location_id="s3AccessGrantLocationId",
                        s3_uri="s3Uri"
                    ),
                    spark_emr_properties=datazone_mixins.CfnConnectionPropsMixin.SparkEmrPropertiesInputProperty(
                        compute_arn="computeArn",
                        instance_profile_arn="instanceProfileArn",
                        java_virtual_env="javaVirtualEnv",
                        log_uri="logUri",
                        managed_endpoint_arn="managedEndpointArn",
                        python_virtual_env="pythonVirtualEnv",
                        runtime_role="runtimeRole",
                        trusted_certificates_s3_uri="trustedCertificatesS3Uri"
                    ),
                    spark_glue_properties=datazone_mixins.CfnConnectionPropsMixin.SparkGluePropertiesInputProperty(
                        additional_args=datazone_mixins.CfnConnectionPropsMixin.SparkGlueArgsProperty(
                            connection="connection"
                        ),
                        glue_connection_name="glueConnectionName",
                        glue_version="glueVersion",
                        idle_timeout=123,
                        java_virtual_env="javaVirtualEnv",
                        number_of_workers=123,
                        python_virtual_env="pythonVirtualEnv",
                        worker_type="workerType"
                    )
                ),
                scope="scope"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ca99ae038dddfa8cdd53cbd1df77d82f370778d850fc42849cfc7e4cceeabce)
            check_type(argname="argument aws_location", value=aws_location, expected_type=type_hints["aws_location"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument domain_identifier", value=domain_identifier, expected_type=type_hints["domain_identifier"])
            check_type(argname="argument enable_trusted_identity_propagation", value=enable_trusted_identity_propagation, expected_type=type_hints["enable_trusted_identity_propagation"])
            check_type(argname="argument environment_identifier", value=environment_identifier, expected_type=type_hints["environment_identifier"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument project_identifier", value=project_identifier, expected_type=type_hints["project_identifier"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_location is not None:
            self._values["aws_location"] = aws_location
        if description is not None:
            self._values["description"] = description
        if domain_identifier is not None:
            self._values["domain_identifier"] = domain_identifier
        if enable_trusted_identity_propagation is not None:
            self._values["enable_trusted_identity_propagation"] = enable_trusted_identity_propagation
        if environment_identifier is not None:
            self._values["environment_identifier"] = environment_identifier
        if name is not None:
            self._values["name"] = name
        if project_identifier is not None:
            self._values["project_identifier"] = project_identifier
        if props is not None:
            self._values["props"] = props
        if scope is not None:
            self._values["scope"] = scope

    @builtins.property
    def aws_location(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.AwsLocationProperty"]]:
        '''The location where the connection is created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-connection.html#cfn-datazone-connection-awslocation
        '''
        result = self._values.get("aws_location")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.AwsLocationProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Connection description.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-connection.html#cfn-datazone-connection-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_identifier(self) -> typing.Optional[builtins.str]:
        '''The ID of the domain where the connection is created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-connection.html#cfn-datazone-connection-domainidentifier
        '''
        result = self._values.get("domain_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_trusted_identity_propagation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether the trusted identity propagation is enabled.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-connection.html#cfn-datazone-connection-enabletrustedidentitypropagation
        '''
        result = self._values.get("enable_trusted_identity_propagation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def environment_identifier(self) -> typing.Optional[builtins.str]:
        '''The ID of the environment where the connection is created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-connection.html#cfn-datazone-connection-environmentidentifier
        '''
        result = self._values.get("environment_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the connection.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-connection.html#cfn-datazone-connection-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_identifier(self) -> typing.Optional[builtins.str]:
        '''The identifier of the project in which the connection should be created.

        If

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-connection.html#cfn-datazone-connection-projectidentifier
        '''
        result = self._values.get("project_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def props(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.ConnectionPropertiesInputProperty"]]:
        '''Connection props.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-connection.html#cfn-datazone-connection-props
        '''
        result = self._values.get("props")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.ConnectionPropertiesInputProperty"]], result)

    @builtins.property
    def scope(self) -> typing.Optional[builtins.str]:
        '''The scope of the connection.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-connection.html#cfn-datazone-connection-scope
        '''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConnectionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnConnectionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnConnectionPropsMixin",
):
    '''In Amazon DataZone, a connection enables you to connect your resources (domains, projects, and environments) to external resources and services.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-connection.html
    :cloudformationResource: AWS::DataZone::Connection
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
        
        cfn_connection_props_mixin = datazone_mixins.CfnConnectionPropsMixin(datazone_mixins.CfnConnectionMixinProps(
            aws_location=datazone_mixins.CfnConnectionPropsMixin.AwsLocationProperty(
                access_role="accessRole",
                aws_account_id="awsAccountId",
                aws_region="awsRegion",
                iam_connection_id="iamConnectionId"
            ),
            description="description",
            domain_identifier="domainIdentifier",
            enable_trusted_identity_propagation=False,
            environment_identifier="environmentIdentifier",
            name="name",
            project_identifier="projectIdentifier",
            props=datazone_mixins.CfnConnectionPropsMixin.ConnectionPropertiesInputProperty(
                amazon_qProperties=datazone_mixins.CfnConnectionPropsMixin.AmazonQPropertiesInputProperty(
                    auth_mode="authMode",
                    is_enabled=False,
                    profile_arn="profileArn"
                ),
                athena_properties=datazone_mixins.CfnConnectionPropsMixin.AthenaPropertiesInputProperty(
                    workgroup_name="workgroupName"
                ),
                glue_properties=datazone_mixins.CfnConnectionPropsMixin.GluePropertiesInputProperty(
                    glue_connection_input=datazone_mixins.CfnConnectionPropsMixin.GlueConnectionInputProperty(
                        athena_properties={
                            "athena_properties_key": "athenaProperties"
                        },
                        authentication_configuration=datazone_mixins.CfnConnectionPropsMixin.AuthenticationConfigurationInputProperty(
                            authentication_type="authenticationType",
                            basic_authentication_credentials=datazone_mixins.CfnConnectionPropsMixin.BasicAuthenticationCredentialsProperty(
                                password="password",
                                user_name="userName"
                            ),
                            custom_authentication_credentials={
                                "custom_authentication_credentials_key": "customAuthenticationCredentials"
                            },
                            kms_key_arn="kmsKeyArn",
                            o_auth2_properties=datazone_mixins.CfnConnectionPropsMixin.OAuth2PropertiesProperty(
                                authorization_code_properties=datazone_mixins.CfnConnectionPropsMixin.AuthorizationCodePropertiesProperty(
                                    authorization_code="authorizationCode",
                                    redirect_uri="redirectUri"
                                ),
                                o_auth2_client_application=datazone_mixins.CfnConnectionPropsMixin.OAuth2ClientApplicationProperty(
                                    aws_managed_client_application_reference="awsManagedClientApplicationReference",
                                    user_managed_client_application_client_id="userManagedClientApplicationClientId"
                                ),
                                o_auth2_credentials=datazone_mixins.CfnConnectionPropsMixin.GlueOAuth2CredentialsProperty(
                                    access_token="accessToken",
                                    jwt_token="jwtToken",
                                    refresh_token="refreshToken",
                                    user_managed_client_application_client_secret="userManagedClientApplicationClientSecret"
                                ),
                                o_auth2_grant_type="oAuth2GrantType",
                                token_url="tokenUrl",
                                token_url_parameters_map={
                                    "token_url_parameters_map_key": "tokenUrlParametersMap"
                                }
                            ),
                            secret_arn="secretArn"
                        ),
                        connection_properties={
                            "connection_properties_key": "connectionProperties"
                        },
                        connection_type="connectionType",
                        description="description",
                        match_criteria="matchCriteria",
                        name="name",
                        physical_connection_requirements=datazone_mixins.CfnConnectionPropsMixin.PhysicalConnectionRequirementsProperty(
                            availability_zone="availabilityZone",
                            security_group_id_list=["securityGroupIdList"],
                            subnet_id="subnetId",
                            subnet_id_list=["subnetIdList"]
                        ),
                        python_properties={
                            "python_properties_key": "pythonProperties"
                        },
                        spark_properties={
                            "spark_properties_key": "sparkProperties"
                        },
                        validate_credentials=False,
                        validate_for_compute_environments=["validateForComputeEnvironments"]
                    )
                ),
                hyper_pod_properties=datazone_mixins.CfnConnectionPropsMixin.HyperPodPropertiesInputProperty(
                    cluster_name="clusterName"
                ),
                iam_properties=datazone_mixins.CfnConnectionPropsMixin.IamPropertiesInputProperty(
                    glue_lineage_sync_enabled=False
                ),
                redshift_properties=datazone_mixins.CfnConnectionPropsMixin.RedshiftPropertiesInputProperty(
                    credentials=datazone_mixins.CfnConnectionPropsMixin.RedshiftCredentialsProperty(
                        secret_arn="secretArn",
                        username_password=datazone_mixins.CfnConnectionPropsMixin.UsernamePasswordProperty(
                            password="password",
                            username="username"
                        )
                    ),
                    database_name="databaseName",
                    host="host",
                    lineage_sync=datazone_mixins.CfnConnectionPropsMixin.RedshiftLineageSyncConfigurationInputProperty(
                        enabled=False,
                        schedule=datazone_mixins.CfnConnectionPropsMixin.LineageSyncScheduleProperty(
                            schedule="schedule"
                        )
                    ),
                    port=123,
                    storage=datazone_mixins.CfnConnectionPropsMixin.RedshiftStoragePropertiesProperty(
                        cluster_name="clusterName",
                        workgroup_name="workgroupName"
                    )
                ),
                s3_properties=datazone_mixins.CfnConnectionPropsMixin.S3PropertiesInputProperty(
                    s3_access_grant_location_id="s3AccessGrantLocationId",
                    s3_uri="s3Uri"
                ),
                spark_emr_properties=datazone_mixins.CfnConnectionPropsMixin.SparkEmrPropertiesInputProperty(
                    compute_arn="computeArn",
                    instance_profile_arn="instanceProfileArn",
                    java_virtual_env="javaVirtualEnv",
                    log_uri="logUri",
                    managed_endpoint_arn="managedEndpointArn",
                    python_virtual_env="pythonVirtualEnv",
                    runtime_role="runtimeRole",
                    trusted_certificates_s3_uri="trustedCertificatesS3Uri"
                ),
                spark_glue_properties=datazone_mixins.CfnConnectionPropsMixin.SparkGluePropertiesInputProperty(
                    additional_args=datazone_mixins.CfnConnectionPropsMixin.SparkGlueArgsProperty(
                        connection="connection"
                    ),
                    glue_connection_name="glueConnectionName",
                    glue_version="glueVersion",
                    idle_timeout=123,
                    java_virtual_env="javaVirtualEnv",
                    number_of_workers=123,
                    python_virtual_env="pythonVirtualEnv",
                    worker_type="workerType"
                )
            ),
            scope="scope"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnConnectionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DataZone::Connection``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e9c094929392b272fc04188e16b8fa4b9b33a49e818f22c32b4924ec0ce519e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__95b66b41b0178dfb9cafdf9c4658a046ecdbab891e8600a11da55ca0dfddc26a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a24c11f99646036a223c9eb490372322a2b516016e904be222b2e3bae5c96ce9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnConnectionMixinProps:
        return typing.cast(CfnConnectionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnConnectionPropsMixin.AmazonQPropertiesInputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "auth_mode": "authMode",
            "is_enabled": "isEnabled",
            "profile_arn": "profileArn",
        },
    )
    class AmazonQPropertiesInputProperty:
        def __init__(
            self,
            *,
            auth_mode: typing.Optional[builtins.str] = None,
            is_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            profile_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Amazon Q properties of the connection.

            :param auth_mode: The authentication mode of the connection's AmazonQ properties.
            :param is_enabled: Specifies whether Amazon Q is enabled for the connection.
            :param profile_arn: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-amazonqpropertiesinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                amazon_qProperties_input_property = datazone_mixins.CfnConnectionPropsMixin.AmazonQPropertiesInputProperty(
                    auth_mode="authMode",
                    is_enabled=False,
                    profile_arn="profileArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7bda8cd1983f1e7e08edb67eb5efa75442c2c87b222af1e4a7bc67fc382269b2)
                check_type(argname="argument auth_mode", value=auth_mode, expected_type=type_hints["auth_mode"])
                check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
                check_type(argname="argument profile_arn", value=profile_arn, expected_type=type_hints["profile_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auth_mode is not None:
                self._values["auth_mode"] = auth_mode
            if is_enabled is not None:
                self._values["is_enabled"] = is_enabled
            if profile_arn is not None:
                self._values["profile_arn"] = profile_arn

        @builtins.property
        def auth_mode(self) -> typing.Optional[builtins.str]:
            '''The authentication mode of the connection's AmazonQ properties.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-amazonqpropertiesinput.html#cfn-datazone-connection-amazonqpropertiesinput-authmode
            '''
            result = self._values.get("auth_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def is_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether Amazon Q is enabled for the connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-amazonqpropertiesinput.html#cfn-datazone-connection-amazonqpropertiesinput-isenabled
            '''
            result = self._values.get("is_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def profile_arn(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-amazonqpropertiesinput.html#cfn-datazone-connection-amazonqpropertiesinput-profilearn
            '''
            result = self._values.get("profile_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AmazonQPropertiesInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnConnectionPropsMixin.AthenaPropertiesInputProperty",
        jsii_struct_bases=[],
        name_mapping={"workgroup_name": "workgroupName"},
    )
    class AthenaPropertiesInputProperty:
        def __init__(
            self,
            *,
            workgroup_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The Amazon Athena properties of a connection.

            :param workgroup_name: The Amazon Athena workgroup name of a connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-athenapropertiesinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                athena_properties_input_property = datazone_mixins.CfnConnectionPropsMixin.AthenaPropertiesInputProperty(
                    workgroup_name="workgroupName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fd0abda7028f017acbb717b67a017e50e1fbfec7ffee2e2660f51917bc9e5ee4)
                check_type(argname="argument workgroup_name", value=workgroup_name, expected_type=type_hints["workgroup_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if workgroup_name is not None:
                self._values["workgroup_name"] = workgroup_name

        @builtins.property
        def workgroup_name(self) -> typing.Optional[builtins.str]:
            '''The Amazon Athena workgroup name of a connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-athenapropertiesinput.html#cfn-datazone-connection-athenapropertiesinput-workgroupname
            '''
            result = self._values.get("workgroup_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AthenaPropertiesInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnConnectionPropsMixin.AuthenticationConfigurationInputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "authentication_type": "authenticationType",
            "basic_authentication_credentials": "basicAuthenticationCredentials",
            "custom_authentication_credentials": "customAuthenticationCredentials",
            "kms_key_arn": "kmsKeyArn",
            "o_auth2_properties": "oAuth2Properties",
            "secret_arn": "secretArn",
        },
    )
    class AuthenticationConfigurationInputProperty:
        def __init__(
            self,
            *,
            authentication_type: typing.Optional[builtins.str] = None,
            basic_authentication_credentials: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectionPropsMixin.BasicAuthenticationCredentialsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            custom_authentication_credentials: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            kms_key_arn: typing.Optional[builtins.str] = None,
            o_auth2_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectionPropsMixin.OAuth2PropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            secret_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The authentication configuration of a connection.

            :param authentication_type: The authentication type of a connection.
            :param basic_authentication_credentials: The basic authentication credentials of a connection.
            :param custom_authentication_credentials: The custom authentication credentials of a connection.
            :param kms_key_arn: The KMS key ARN of a connection.
            :param o_auth2_properties: The oAuth2 properties of a connection.
            :param secret_arn: The secret ARN of a connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-authenticationconfigurationinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                authentication_configuration_input_property = datazone_mixins.CfnConnectionPropsMixin.AuthenticationConfigurationInputProperty(
                    authentication_type="authenticationType",
                    basic_authentication_credentials=datazone_mixins.CfnConnectionPropsMixin.BasicAuthenticationCredentialsProperty(
                        password="password",
                        user_name="userName"
                    ),
                    custom_authentication_credentials={
                        "custom_authentication_credentials_key": "customAuthenticationCredentials"
                    },
                    kms_key_arn="kmsKeyArn",
                    o_auth2_properties=datazone_mixins.CfnConnectionPropsMixin.OAuth2PropertiesProperty(
                        authorization_code_properties=datazone_mixins.CfnConnectionPropsMixin.AuthorizationCodePropertiesProperty(
                            authorization_code="authorizationCode",
                            redirect_uri="redirectUri"
                        ),
                        o_auth2_client_application=datazone_mixins.CfnConnectionPropsMixin.OAuth2ClientApplicationProperty(
                            aws_managed_client_application_reference="awsManagedClientApplicationReference",
                            user_managed_client_application_client_id="userManagedClientApplicationClientId"
                        ),
                        o_auth2_credentials=datazone_mixins.CfnConnectionPropsMixin.GlueOAuth2CredentialsProperty(
                            access_token="accessToken",
                            jwt_token="jwtToken",
                            refresh_token="refreshToken",
                            user_managed_client_application_client_secret="userManagedClientApplicationClientSecret"
                        ),
                        o_auth2_grant_type="oAuth2GrantType",
                        token_url="tokenUrl",
                        token_url_parameters_map={
                            "token_url_parameters_map_key": "tokenUrlParametersMap"
                        }
                    ),
                    secret_arn="secretArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2373b5f964ea9e7c0cca17573a69a36075214fd7308a0c8c3d3f7ae13b803625)
                check_type(argname="argument authentication_type", value=authentication_type, expected_type=type_hints["authentication_type"])
                check_type(argname="argument basic_authentication_credentials", value=basic_authentication_credentials, expected_type=type_hints["basic_authentication_credentials"])
                check_type(argname="argument custom_authentication_credentials", value=custom_authentication_credentials, expected_type=type_hints["custom_authentication_credentials"])
                check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
                check_type(argname="argument o_auth2_properties", value=o_auth2_properties, expected_type=type_hints["o_auth2_properties"])
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if authentication_type is not None:
                self._values["authentication_type"] = authentication_type
            if basic_authentication_credentials is not None:
                self._values["basic_authentication_credentials"] = basic_authentication_credentials
            if custom_authentication_credentials is not None:
                self._values["custom_authentication_credentials"] = custom_authentication_credentials
            if kms_key_arn is not None:
                self._values["kms_key_arn"] = kms_key_arn
            if o_auth2_properties is not None:
                self._values["o_auth2_properties"] = o_auth2_properties
            if secret_arn is not None:
                self._values["secret_arn"] = secret_arn

        @builtins.property
        def authentication_type(self) -> typing.Optional[builtins.str]:
            '''The authentication type of a connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-authenticationconfigurationinput.html#cfn-datazone-connection-authenticationconfigurationinput-authenticationtype
            '''
            result = self._values.get("authentication_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def basic_authentication_credentials(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.BasicAuthenticationCredentialsProperty"]]:
            '''The basic authentication credentials of a connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-authenticationconfigurationinput.html#cfn-datazone-connection-authenticationconfigurationinput-basicauthenticationcredentials
            '''
            result = self._values.get("basic_authentication_credentials")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.BasicAuthenticationCredentialsProperty"]], result)

        @builtins.property
        def custom_authentication_credentials(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''The custom authentication credentials of a connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-authenticationconfigurationinput.html#cfn-datazone-connection-authenticationconfigurationinput-customauthenticationcredentials
            '''
            result = self._values.get("custom_authentication_credentials")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def kms_key_arn(self) -> typing.Optional[builtins.str]:
            '''The KMS key ARN of a connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-authenticationconfigurationinput.html#cfn-datazone-connection-authenticationconfigurationinput-kmskeyarn
            '''
            result = self._values.get("kms_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def o_auth2_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.OAuth2PropertiesProperty"]]:
            '''The oAuth2 properties of a connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-authenticationconfigurationinput.html#cfn-datazone-connection-authenticationconfigurationinput-oauth2properties
            '''
            result = self._values.get("o_auth2_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.OAuth2PropertiesProperty"]], result)

        @builtins.property
        def secret_arn(self) -> typing.Optional[builtins.str]:
            '''The secret ARN of a connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-authenticationconfigurationinput.html#cfn-datazone-connection-authenticationconfigurationinput-secretarn
            '''
            result = self._values.get("secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthenticationConfigurationInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnConnectionPropsMixin.AuthorizationCodePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "authorization_code": "authorizationCode",
            "redirect_uri": "redirectUri",
        },
    )
    class AuthorizationCodePropertiesProperty:
        def __init__(
            self,
            *,
            authorization_code: typing.Optional[builtins.str] = None,
            redirect_uri: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The authorization code properties of a connection.

            :param authorization_code: The authorization code of a connection.
            :param redirect_uri: The redirect URI of a connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-authorizationcodeproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                authorization_code_properties_property = datazone_mixins.CfnConnectionPropsMixin.AuthorizationCodePropertiesProperty(
                    authorization_code="authorizationCode",
                    redirect_uri="redirectUri"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e95a19100de29b79778d33bf14ceb5e258e67ac98c8ba349566d3e20e3045b85)
                check_type(argname="argument authorization_code", value=authorization_code, expected_type=type_hints["authorization_code"])
                check_type(argname="argument redirect_uri", value=redirect_uri, expected_type=type_hints["redirect_uri"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if authorization_code is not None:
                self._values["authorization_code"] = authorization_code
            if redirect_uri is not None:
                self._values["redirect_uri"] = redirect_uri

        @builtins.property
        def authorization_code(self) -> typing.Optional[builtins.str]:
            '''The authorization code of a connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-authorizationcodeproperties.html#cfn-datazone-connection-authorizationcodeproperties-authorizationcode
            '''
            result = self._values.get("authorization_code")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def redirect_uri(self) -> typing.Optional[builtins.str]:
            '''The redirect URI of a connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-authorizationcodeproperties.html#cfn-datazone-connection-authorizationcodeproperties-redirecturi
            '''
            result = self._values.get("redirect_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthorizationCodePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnConnectionPropsMixin.AwsLocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_role": "accessRole",
            "aws_account_id": "awsAccountId",
            "aws_region": "awsRegion",
            "iam_connection_id": "iamConnectionId",
        },
    )
    class AwsLocationProperty:
        def __init__(
            self,
            *,
            access_role: typing.Optional[builtins.str] = None,
            aws_account_id: typing.Optional[builtins.str] = None,
            aws_region: typing.Optional[builtins.str] = None,
            iam_connection_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The location of a project.

            :param access_role: The access role of a connection.
            :param aws_account_id: The account ID of a connection.
            :param aws_region: The Region of a connection.
            :param iam_connection_id: The IAM connection ID of a connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-awslocation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                aws_location_property = datazone_mixins.CfnConnectionPropsMixin.AwsLocationProperty(
                    access_role="accessRole",
                    aws_account_id="awsAccountId",
                    aws_region="awsRegion",
                    iam_connection_id="iamConnectionId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b6a1ca03cc284fc24c6d252d4f951e18d76e4480f6fc384817572d829f7e7fc4)
                check_type(argname="argument access_role", value=access_role, expected_type=type_hints["access_role"])
                check_type(argname="argument aws_account_id", value=aws_account_id, expected_type=type_hints["aws_account_id"])
                check_type(argname="argument aws_region", value=aws_region, expected_type=type_hints["aws_region"])
                check_type(argname="argument iam_connection_id", value=iam_connection_id, expected_type=type_hints["iam_connection_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_role is not None:
                self._values["access_role"] = access_role
            if aws_account_id is not None:
                self._values["aws_account_id"] = aws_account_id
            if aws_region is not None:
                self._values["aws_region"] = aws_region
            if iam_connection_id is not None:
                self._values["iam_connection_id"] = iam_connection_id

        @builtins.property
        def access_role(self) -> typing.Optional[builtins.str]:
            '''The access role of a connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-awslocation.html#cfn-datazone-connection-awslocation-accessrole
            '''
            result = self._values.get("access_role")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def aws_account_id(self) -> typing.Optional[builtins.str]:
            '''The account ID of a connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-awslocation.html#cfn-datazone-connection-awslocation-awsaccountid
            '''
            result = self._values.get("aws_account_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def aws_region(self) -> typing.Optional[builtins.str]:
            '''The Region of a connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-awslocation.html#cfn-datazone-connection-awslocation-awsregion
            '''
            result = self._values.get("aws_region")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def iam_connection_id(self) -> typing.Optional[builtins.str]:
            '''The IAM connection ID of a connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-awslocation.html#cfn-datazone-connection-awslocation-iamconnectionid
            '''
            result = self._values.get("iam_connection_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AwsLocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnConnectionPropsMixin.BasicAuthenticationCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={"password": "password", "user_name": "userName"},
    )
    class BasicAuthenticationCredentialsProperty:
        def __init__(
            self,
            *,
            password: typing.Optional[builtins.str] = None,
            user_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The basic authentication credentials of a connection.

            :param password: The password for a connection.
            :param user_name: The user name for the connecion.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-basicauthenticationcredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                basic_authentication_credentials_property = datazone_mixins.CfnConnectionPropsMixin.BasicAuthenticationCredentialsProperty(
                    password="password",
                    user_name="userName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e7d39aac0e59cb1e3763c4f7086fbb5f45d90bf7152c6fc898a8b4e716bcf6ba)
                check_type(argname="argument password", value=password, expected_type=type_hints["password"])
                check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if password is not None:
                self._values["password"] = password
            if user_name is not None:
                self._values["user_name"] = user_name

        @builtins.property
        def password(self) -> typing.Optional[builtins.str]:
            '''The password for a connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-basicauthenticationcredentials.html#cfn-datazone-connection-basicauthenticationcredentials-password
            '''
            result = self._values.get("password")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user_name(self) -> typing.Optional[builtins.str]:
            '''The user name for the connecion.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-basicauthenticationcredentials.html#cfn-datazone-connection-basicauthenticationcredentials-username
            '''
            result = self._values.get("user_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BasicAuthenticationCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnConnectionPropsMixin.ConnectionPropertiesInputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "amazon_q_properties": "amazonQProperties",
            "athena_properties": "athenaProperties",
            "glue_properties": "glueProperties",
            "hyper_pod_properties": "hyperPodProperties",
            "iam_properties": "iamProperties",
            "redshift_properties": "redshiftProperties",
            "s3_properties": "s3Properties",
            "spark_emr_properties": "sparkEmrProperties",
            "spark_glue_properties": "sparkGlueProperties",
        },
    )
    class ConnectionPropertiesInputProperty:
        def __init__(
            self,
            *,
            amazon_q_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectionPropsMixin.AmazonQPropertiesInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            athena_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectionPropsMixin.AthenaPropertiesInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            glue_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectionPropsMixin.GluePropertiesInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            hyper_pod_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectionPropsMixin.HyperPodPropertiesInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            iam_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectionPropsMixin.IamPropertiesInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            redshift_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectionPropsMixin.RedshiftPropertiesInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectionPropsMixin.S3PropertiesInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            spark_emr_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectionPropsMixin.SparkEmrPropertiesInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            spark_glue_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectionPropsMixin.SparkGluePropertiesInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The properties of a connection.

            :param amazon_q_properties: Amazon Q properties of the connection.
            :param athena_properties: The Amazon Athena properties of a connection.
            :param glue_properties: The AWS Glue properties of a connection.
            :param hyper_pod_properties: The hyper pod properties of a connection.
            :param iam_properties: The IAM properties of a connection.
            :param redshift_properties: The Amazon Redshift properties of a connection.
            :param s3_properties: S3 Properties Input.
            :param spark_emr_properties: The Spark EMR properties of a connection.
            :param spark_glue_properties: The Spark AWS Glue properties of a connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-connectionpropertiesinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                connection_properties_input_property = datazone_mixins.CfnConnectionPropsMixin.ConnectionPropertiesInputProperty(
                    amazon_qProperties=datazone_mixins.CfnConnectionPropsMixin.AmazonQPropertiesInputProperty(
                        auth_mode="authMode",
                        is_enabled=False,
                        profile_arn="profileArn"
                    ),
                    athena_properties=datazone_mixins.CfnConnectionPropsMixin.AthenaPropertiesInputProperty(
                        workgroup_name="workgroupName"
                    ),
                    glue_properties=datazone_mixins.CfnConnectionPropsMixin.GluePropertiesInputProperty(
                        glue_connection_input=datazone_mixins.CfnConnectionPropsMixin.GlueConnectionInputProperty(
                            athena_properties={
                                "athena_properties_key": "athenaProperties"
                            },
                            authentication_configuration=datazone_mixins.CfnConnectionPropsMixin.AuthenticationConfigurationInputProperty(
                                authentication_type="authenticationType",
                                basic_authentication_credentials=datazone_mixins.CfnConnectionPropsMixin.BasicAuthenticationCredentialsProperty(
                                    password="password",
                                    user_name="userName"
                                ),
                                custom_authentication_credentials={
                                    "custom_authentication_credentials_key": "customAuthenticationCredentials"
                                },
                                kms_key_arn="kmsKeyArn",
                                o_auth2_properties=datazone_mixins.CfnConnectionPropsMixin.OAuth2PropertiesProperty(
                                    authorization_code_properties=datazone_mixins.CfnConnectionPropsMixin.AuthorizationCodePropertiesProperty(
                                        authorization_code="authorizationCode",
                                        redirect_uri="redirectUri"
                                    ),
                                    o_auth2_client_application=datazone_mixins.CfnConnectionPropsMixin.OAuth2ClientApplicationProperty(
                                        aws_managed_client_application_reference="awsManagedClientApplicationReference",
                                        user_managed_client_application_client_id="userManagedClientApplicationClientId"
                                    ),
                                    o_auth2_credentials=datazone_mixins.CfnConnectionPropsMixin.GlueOAuth2CredentialsProperty(
                                        access_token="accessToken",
                                        jwt_token="jwtToken",
                                        refresh_token="refreshToken",
                                        user_managed_client_application_client_secret="userManagedClientApplicationClientSecret"
                                    ),
                                    o_auth2_grant_type="oAuth2GrantType",
                                    token_url="tokenUrl",
                                    token_url_parameters_map={
                                        "token_url_parameters_map_key": "tokenUrlParametersMap"
                                    }
                                ),
                                secret_arn="secretArn"
                            ),
                            connection_properties={
                                "connection_properties_key": "connectionProperties"
                            },
                            connection_type="connectionType",
                            description="description",
                            match_criteria="matchCriteria",
                            name="name",
                            physical_connection_requirements=datazone_mixins.CfnConnectionPropsMixin.PhysicalConnectionRequirementsProperty(
                                availability_zone="availabilityZone",
                                security_group_id_list=["securityGroupIdList"],
                                subnet_id="subnetId",
                                subnet_id_list=["subnetIdList"]
                            ),
                            python_properties={
                                "python_properties_key": "pythonProperties"
                            },
                            spark_properties={
                                "spark_properties_key": "sparkProperties"
                            },
                            validate_credentials=False,
                            validate_for_compute_environments=["validateForComputeEnvironments"]
                        )
                    ),
                    hyper_pod_properties=datazone_mixins.CfnConnectionPropsMixin.HyperPodPropertiesInputProperty(
                        cluster_name="clusterName"
                    ),
                    iam_properties=datazone_mixins.CfnConnectionPropsMixin.IamPropertiesInputProperty(
                        glue_lineage_sync_enabled=False
                    ),
                    redshift_properties=datazone_mixins.CfnConnectionPropsMixin.RedshiftPropertiesInputProperty(
                        credentials=datazone_mixins.CfnConnectionPropsMixin.RedshiftCredentialsProperty(
                            secret_arn="secretArn",
                            username_password=datazone_mixins.CfnConnectionPropsMixin.UsernamePasswordProperty(
                                password="password",
                                username="username"
                            )
                        ),
                        database_name="databaseName",
                        host="host",
                        lineage_sync=datazone_mixins.CfnConnectionPropsMixin.RedshiftLineageSyncConfigurationInputProperty(
                            enabled=False,
                            schedule=datazone_mixins.CfnConnectionPropsMixin.LineageSyncScheduleProperty(
                                schedule="schedule"
                            )
                        ),
                        port=123,
                        storage=datazone_mixins.CfnConnectionPropsMixin.RedshiftStoragePropertiesProperty(
                            cluster_name="clusterName",
                            workgroup_name="workgroupName"
                        )
                    ),
                    s3_properties=datazone_mixins.CfnConnectionPropsMixin.S3PropertiesInputProperty(
                        s3_access_grant_location_id="s3AccessGrantLocationId",
                        s3_uri="s3Uri"
                    ),
                    spark_emr_properties=datazone_mixins.CfnConnectionPropsMixin.SparkEmrPropertiesInputProperty(
                        compute_arn="computeArn",
                        instance_profile_arn="instanceProfileArn",
                        java_virtual_env="javaVirtualEnv",
                        log_uri="logUri",
                        managed_endpoint_arn="managedEndpointArn",
                        python_virtual_env="pythonVirtualEnv",
                        runtime_role="runtimeRole",
                        trusted_certificates_s3_uri="trustedCertificatesS3Uri"
                    ),
                    spark_glue_properties=datazone_mixins.CfnConnectionPropsMixin.SparkGluePropertiesInputProperty(
                        additional_args=datazone_mixins.CfnConnectionPropsMixin.SparkGlueArgsProperty(
                            connection="connection"
                        ),
                        glue_connection_name="glueConnectionName",
                        glue_version="glueVersion",
                        idle_timeout=123,
                        java_virtual_env="javaVirtualEnv",
                        number_of_workers=123,
                        python_virtual_env="pythonVirtualEnv",
                        worker_type="workerType"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f141db480b1ef6dd0c9e368caf1e5665607a85286d6b15645fa2cd6865bd684a)
                check_type(argname="argument amazon_q_properties", value=amazon_q_properties, expected_type=type_hints["amazon_q_properties"])
                check_type(argname="argument athena_properties", value=athena_properties, expected_type=type_hints["athena_properties"])
                check_type(argname="argument glue_properties", value=glue_properties, expected_type=type_hints["glue_properties"])
                check_type(argname="argument hyper_pod_properties", value=hyper_pod_properties, expected_type=type_hints["hyper_pod_properties"])
                check_type(argname="argument iam_properties", value=iam_properties, expected_type=type_hints["iam_properties"])
                check_type(argname="argument redshift_properties", value=redshift_properties, expected_type=type_hints["redshift_properties"])
                check_type(argname="argument s3_properties", value=s3_properties, expected_type=type_hints["s3_properties"])
                check_type(argname="argument spark_emr_properties", value=spark_emr_properties, expected_type=type_hints["spark_emr_properties"])
                check_type(argname="argument spark_glue_properties", value=spark_glue_properties, expected_type=type_hints["spark_glue_properties"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if amazon_q_properties is not None:
                self._values["amazon_q_properties"] = amazon_q_properties
            if athena_properties is not None:
                self._values["athena_properties"] = athena_properties
            if glue_properties is not None:
                self._values["glue_properties"] = glue_properties
            if hyper_pod_properties is not None:
                self._values["hyper_pod_properties"] = hyper_pod_properties
            if iam_properties is not None:
                self._values["iam_properties"] = iam_properties
            if redshift_properties is not None:
                self._values["redshift_properties"] = redshift_properties
            if s3_properties is not None:
                self._values["s3_properties"] = s3_properties
            if spark_emr_properties is not None:
                self._values["spark_emr_properties"] = spark_emr_properties
            if spark_glue_properties is not None:
                self._values["spark_glue_properties"] = spark_glue_properties

        @builtins.property
        def amazon_q_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.AmazonQPropertiesInputProperty"]]:
            '''Amazon Q properties of the connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-connectionpropertiesinput.html#cfn-datazone-connection-connectionpropertiesinput-amazonqproperties
            '''
            result = self._values.get("amazon_q_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.AmazonQPropertiesInputProperty"]], result)

        @builtins.property
        def athena_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.AthenaPropertiesInputProperty"]]:
            '''The Amazon Athena properties of a connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-connectionpropertiesinput.html#cfn-datazone-connection-connectionpropertiesinput-athenaproperties
            '''
            result = self._values.get("athena_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.AthenaPropertiesInputProperty"]], result)

        @builtins.property
        def glue_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.GluePropertiesInputProperty"]]:
            '''The AWS Glue properties of a connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-connectionpropertiesinput.html#cfn-datazone-connection-connectionpropertiesinput-glueproperties
            '''
            result = self._values.get("glue_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.GluePropertiesInputProperty"]], result)

        @builtins.property
        def hyper_pod_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.HyperPodPropertiesInputProperty"]]:
            '''The hyper pod properties of a connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-connectionpropertiesinput.html#cfn-datazone-connection-connectionpropertiesinput-hyperpodproperties
            '''
            result = self._values.get("hyper_pod_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.HyperPodPropertiesInputProperty"]], result)

        @builtins.property
        def iam_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.IamPropertiesInputProperty"]]:
            '''The IAM properties of a connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-connectionpropertiesinput.html#cfn-datazone-connection-connectionpropertiesinput-iamproperties
            '''
            result = self._values.get("iam_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.IamPropertiesInputProperty"]], result)

        @builtins.property
        def redshift_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.RedshiftPropertiesInputProperty"]]:
            '''The Amazon Redshift properties of a connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-connectionpropertiesinput.html#cfn-datazone-connection-connectionpropertiesinput-redshiftproperties
            '''
            result = self._values.get("redshift_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.RedshiftPropertiesInputProperty"]], result)

        @builtins.property
        def s3_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.S3PropertiesInputProperty"]]:
            '''S3 Properties Input.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-connectionpropertiesinput.html#cfn-datazone-connection-connectionpropertiesinput-s3properties
            '''
            result = self._values.get("s3_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.S3PropertiesInputProperty"]], result)

        @builtins.property
        def spark_emr_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.SparkEmrPropertiesInputProperty"]]:
            '''The Spark EMR properties of a connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-connectionpropertiesinput.html#cfn-datazone-connection-connectionpropertiesinput-sparkemrproperties
            '''
            result = self._values.get("spark_emr_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.SparkEmrPropertiesInputProperty"]], result)

        @builtins.property
        def spark_glue_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.SparkGluePropertiesInputProperty"]]:
            '''The Spark AWS Glue properties of a connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-connectionpropertiesinput.html#cfn-datazone-connection-connectionpropertiesinput-sparkglueproperties
            '''
            result = self._values.get("spark_glue_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.SparkGluePropertiesInputProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectionPropertiesInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnConnectionPropsMixin.GlueConnectionInputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "athena_properties": "athenaProperties",
            "authentication_configuration": "authenticationConfiguration",
            "connection_properties": "connectionProperties",
            "connection_type": "connectionType",
            "description": "description",
            "match_criteria": "matchCriteria",
            "name": "name",
            "physical_connection_requirements": "physicalConnectionRequirements",
            "python_properties": "pythonProperties",
            "spark_properties": "sparkProperties",
            "validate_credentials": "validateCredentials",
            "validate_for_compute_environments": "validateForComputeEnvironments",
        },
    )
    class GlueConnectionInputProperty:
        def __init__(
            self,
            *,
            athena_properties: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            authentication_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectionPropsMixin.AuthenticationConfigurationInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            connection_properties: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            connection_type: typing.Optional[builtins.str] = None,
            description: typing.Optional[builtins.str] = None,
            match_criteria: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            physical_connection_requirements: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectionPropsMixin.PhysicalConnectionRequirementsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            python_properties: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            spark_properties: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            validate_credentials: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            validate_for_compute_environments: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The AWS Glue connecton input.

            :param athena_properties: The Amazon Athena properties of the AWS Glue connection.
            :param authentication_configuration: The authentication configuration of the AWS Glue connection.
            :param connection_properties: The connection properties of the AWS Glue connection.
            :param connection_type: The connection type of the AWS Glue connection.
            :param description: The description of the AWS Glue connection.
            :param match_criteria: The match criteria of the AWS Glue connection.
            :param name: The name of the AWS Glue connection.
            :param physical_connection_requirements: The physical connection requirements for the AWS Glue connection.
            :param python_properties: The Python properties of the AWS Glue connection.
            :param spark_properties: The Spark properties of the AWS Glue connection.
            :param validate_credentials: Speciefies whether to validate credentials of the AWS Glue connection.
            :param validate_for_compute_environments: Speciefies whether to validate for compute environments of the AWS Glue connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-glueconnectioninput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                glue_connection_input_property = datazone_mixins.CfnConnectionPropsMixin.GlueConnectionInputProperty(
                    athena_properties={
                        "athena_properties_key": "athenaProperties"
                    },
                    authentication_configuration=datazone_mixins.CfnConnectionPropsMixin.AuthenticationConfigurationInputProperty(
                        authentication_type="authenticationType",
                        basic_authentication_credentials=datazone_mixins.CfnConnectionPropsMixin.BasicAuthenticationCredentialsProperty(
                            password="password",
                            user_name="userName"
                        ),
                        custom_authentication_credentials={
                            "custom_authentication_credentials_key": "customAuthenticationCredentials"
                        },
                        kms_key_arn="kmsKeyArn",
                        o_auth2_properties=datazone_mixins.CfnConnectionPropsMixin.OAuth2PropertiesProperty(
                            authorization_code_properties=datazone_mixins.CfnConnectionPropsMixin.AuthorizationCodePropertiesProperty(
                                authorization_code="authorizationCode",
                                redirect_uri="redirectUri"
                            ),
                            o_auth2_client_application=datazone_mixins.CfnConnectionPropsMixin.OAuth2ClientApplicationProperty(
                                aws_managed_client_application_reference="awsManagedClientApplicationReference",
                                user_managed_client_application_client_id="userManagedClientApplicationClientId"
                            ),
                            o_auth2_credentials=datazone_mixins.CfnConnectionPropsMixin.GlueOAuth2CredentialsProperty(
                                access_token="accessToken",
                                jwt_token="jwtToken",
                                refresh_token="refreshToken",
                                user_managed_client_application_client_secret="userManagedClientApplicationClientSecret"
                            ),
                            o_auth2_grant_type="oAuth2GrantType",
                            token_url="tokenUrl",
                            token_url_parameters_map={
                                "token_url_parameters_map_key": "tokenUrlParametersMap"
                            }
                        ),
                        secret_arn="secretArn"
                    ),
                    connection_properties={
                        "connection_properties_key": "connectionProperties"
                    },
                    connection_type="connectionType",
                    description="description",
                    match_criteria="matchCriteria",
                    name="name",
                    physical_connection_requirements=datazone_mixins.CfnConnectionPropsMixin.PhysicalConnectionRequirementsProperty(
                        availability_zone="availabilityZone",
                        security_group_id_list=["securityGroupIdList"],
                        subnet_id="subnetId",
                        subnet_id_list=["subnetIdList"]
                    ),
                    python_properties={
                        "python_properties_key": "pythonProperties"
                    },
                    spark_properties={
                        "spark_properties_key": "sparkProperties"
                    },
                    validate_credentials=False,
                    validate_for_compute_environments=["validateForComputeEnvironments"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__08048b4d5fb5e3b0a9a76ada34206ca6c8654f423f2f1e8ee53603c79bc1d4e6)
                check_type(argname="argument athena_properties", value=athena_properties, expected_type=type_hints["athena_properties"])
                check_type(argname="argument authentication_configuration", value=authentication_configuration, expected_type=type_hints["authentication_configuration"])
                check_type(argname="argument connection_properties", value=connection_properties, expected_type=type_hints["connection_properties"])
                check_type(argname="argument connection_type", value=connection_type, expected_type=type_hints["connection_type"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument match_criteria", value=match_criteria, expected_type=type_hints["match_criteria"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument physical_connection_requirements", value=physical_connection_requirements, expected_type=type_hints["physical_connection_requirements"])
                check_type(argname="argument python_properties", value=python_properties, expected_type=type_hints["python_properties"])
                check_type(argname="argument spark_properties", value=spark_properties, expected_type=type_hints["spark_properties"])
                check_type(argname="argument validate_credentials", value=validate_credentials, expected_type=type_hints["validate_credentials"])
                check_type(argname="argument validate_for_compute_environments", value=validate_for_compute_environments, expected_type=type_hints["validate_for_compute_environments"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if athena_properties is not None:
                self._values["athena_properties"] = athena_properties
            if authentication_configuration is not None:
                self._values["authentication_configuration"] = authentication_configuration
            if connection_properties is not None:
                self._values["connection_properties"] = connection_properties
            if connection_type is not None:
                self._values["connection_type"] = connection_type
            if description is not None:
                self._values["description"] = description
            if match_criteria is not None:
                self._values["match_criteria"] = match_criteria
            if name is not None:
                self._values["name"] = name
            if physical_connection_requirements is not None:
                self._values["physical_connection_requirements"] = physical_connection_requirements
            if python_properties is not None:
                self._values["python_properties"] = python_properties
            if spark_properties is not None:
                self._values["spark_properties"] = spark_properties
            if validate_credentials is not None:
                self._values["validate_credentials"] = validate_credentials
            if validate_for_compute_environments is not None:
                self._values["validate_for_compute_environments"] = validate_for_compute_environments

        @builtins.property
        def athena_properties(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''The Amazon Athena properties of the AWS Glue connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-glueconnectioninput.html#cfn-datazone-connection-glueconnectioninput-athenaproperties
            '''
            result = self._values.get("athena_properties")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def authentication_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.AuthenticationConfigurationInputProperty"]]:
            '''The authentication configuration of the AWS Glue connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-glueconnectioninput.html#cfn-datazone-connection-glueconnectioninput-authenticationconfiguration
            '''
            result = self._values.get("authentication_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.AuthenticationConfigurationInputProperty"]], result)

        @builtins.property
        def connection_properties(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''The connection properties of the AWS Glue connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-glueconnectioninput.html#cfn-datazone-connection-glueconnectioninput-connectionproperties
            '''
            result = self._values.get("connection_properties")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def connection_type(self) -> typing.Optional[builtins.str]:
            '''The connection type of the AWS Glue connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-glueconnectioninput.html#cfn-datazone-connection-glueconnectioninput-connectiontype
            '''
            result = self._values.get("connection_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The description of the AWS Glue connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-glueconnectioninput.html#cfn-datazone-connection-glueconnectioninput-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def match_criteria(self) -> typing.Optional[builtins.str]:
            '''The match criteria of the AWS Glue connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-glueconnectioninput.html#cfn-datazone-connection-glueconnectioninput-matchcriteria
            '''
            result = self._values.get("match_criteria")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the AWS Glue connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-glueconnectioninput.html#cfn-datazone-connection-glueconnectioninput-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def physical_connection_requirements(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.PhysicalConnectionRequirementsProperty"]]:
            '''The physical connection requirements for the AWS Glue connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-glueconnectioninput.html#cfn-datazone-connection-glueconnectioninput-physicalconnectionrequirements
            '''
            result = self._values.get("physical_connection_requirements")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.PhysicalConnectionRequirementsProperty"]], result)

        @builtins.property
        def python_properties(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''The Python properties of the AWS Glue connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-glueconnectioninput.html#cfn-datazone-connection-glueconnectioninput-pythonproperties
            '''
            result = self._values.get("python_properties")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def spark_properties(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''The Spark properties of the AWS Glue connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-glueconnectioninput.html#cfn-datazone-connection-glueconnectioninput-sparkproperties
            '''
            result = self._values.get("spark_properties")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def validate_credentials(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Speciefies whether to validate credentials of the AWS Glue connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-glueconnectioninput.html#cfn-datazone-connection-glueconnectioninput-validatecredentials
            '''
            result = self._values.get("validate_credentials")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def validate_for_compute_environments(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''Speciefies whether to validate for compute environments of the AWS Glue connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-glueconnectioninput.html#cfn-datazone-connection-glueconnectioninput-validateforcomputeenvironments
            '''
            result = self._values.get("validate_for_compute_environments")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GlueConnectionInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnConnectionPropsMixin.GlueOAuth2CredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_token": "accessToken",
            "jwt_token": "jwtToken",
            "refresh_token": "refreshToken",
            "user_managed_client_application_client_secret": "userManagedClientApplicationClientSecret",
        },
    )
    class GlueOAuth2CredentialsProperty:
        def __init__(
            self,
            *,
            access_token: typing.Optional[builtins.str] = None,
            jwt_token: typing.Optional[builtins.str] = None,
            refresh_token: typing.Optional[builtins.str] = None,
            user_managed_client_application_client_secret: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The GlueOAuth2 credentials of a connection.

            :param access_token: The access token of a connection.
            :param jwt_token: The jwt token of the connection.
            :param refresh_token: The refresh token of the connection.
            :param user_managed_client_application_client_secret: The user managed client application client secret of the connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-glueoauth2credentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                glue_oAuth2_credentials_property = datazone_mixins.CfnConnectionPropsMixin.GlueOAuth2CredentialsProperty(
                    access_token="accessToken",
                    jwt_token="jwtToken",
                    refresh_token="refreshToken",
                    user_managed_client_application_client_secret="userManagedClientApplicationClientSecret"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e969a24019316cfdc513bafaf611986009beaa5dfaa39aa537a8c3b3c5f4967f)
                check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
                check_type(argname="argument jwt_token", value=jwt_token, expected_type=type_hints["jwt_token"])
                check_type(argname="argument refresh_token", value=refresh_token, expected_type=type_hints["refresh_token"])
                check_type(argname="argument user_managed_client_application_client_secret", value=user_managed_client_application_client_secret, expected_type=type_hints["user_managed_client_application_client_secret"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_token is not None:
                self._values["access_token"] = access_token
            if jwt_token is not None:
                self._values["jwt_token"] = jwt_token
            if refresh_token is not None:
                self._values["refresh_token"] = refresh_token
            if user_managed_client_application_client_secret is not None:
                self._values["user_managed_client_application_client_secret"] = user_managed_client_application_client_secret

        @builtins.property
        def access_token(self) -> typing.Optional[builtins.str]:
            '''The access token of a connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-glueoauth2credentials.html#cfn-datazone-connection-glueoauth2credentials-accesstoken
            '''
            result = self._values.get("access_token")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def jwt_token(self) -> typing.Optional[builtins.str]:
            '''The jwt token of the connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-glueoauth2credentials.html#cfn-datazone-connection-glueoauth2credentials-jwttoken
            '''
            result = self._values.get("jwt_token")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def refresh_token(self) -> typing.Optional[builtins.str]:
            '''The refresh token of the connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-glueoauth2credentials.html#cfn-datazone-connection-glueoauth2credentials-refreshtoken
            '''
            result = self._values.get("refresh_token")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user_managed_client_application_client_secret(
            self,
        ) -> typing.Optional[builtins.str]:
            '''The user managed client application client secret of the connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-glueoauth2credentials.html#cfn-datazone-connection-glueoauth2credentials-usermanagedclientapplicationclientsecret
            '''
            result = self._values.get("user_managed_client_application_client_secret")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GlueOAuth2CredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnConnectionPropsMixin.GluePropertiesInputProperty",
        jsii_struct_bases=[],
        name_mapping={"glue_connection_input": "glueConnectionInput"},
    )
    class GluePropertiesInputProperty:
        def __init__(
            self,
            *,
            glue_connection_input: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectionPropsMixin.GlueConnectionInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The AWS Glue properties of a connection.

            :param glue_connection_input: The AWS Glue connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-gluepropertiesinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                glue_properties_input_property = datazone_mixins.CfnConnectionPropsMixin.GluePropertiesInputProperty(
                    glue_connection_input=datazone_mixins.CfnConnectionPropsMixin.GlueConnectionInputProperty(
                        athena_properties={
                            "athena_properties_key": "athenaProperties"
                        },
                        authentication_configuration=datazone_mixins.CfnConnectionPropsMixin.AuthenticationConfigurationInputProperty(
                            authentication_type="authenticationType",
                            basic_authentication_credentials=datazone_mixins.CfnConnectionPropsMixin.BasicAuthenticationCredentialsProperty(
                                password="password",
                                user_name="userName"
                            ),
                            custom_authentication_credentials={
                                "custom_authentication_credentials_key": "customAuthenticationCredentials"
                            },
                            kms_key_arn="kmsKeyArn",
                            o_auth2_properties=datazone_mixins.CfnConnectionPropsMixin.OAuth2PropertiesProperty(
                                authorization_code_properties=datazone_mixins.CfnConnectionPropsMixin.AuthorizationCodePropertiesProperty(
                                    authorization_code="authorizationCode",
                                    redirect_uri="redirectUri"
                                ),
                                o_auth2_client_application=datazone_mixins.CfnConnectionPropsMixin.OAuth2ClientApplicationProperty(
                                    aws_managed_client_application_reference="awsManagedClientApplicationReference",
                                    user_managed_client_application_client_id="userManagedClientApplicationClientId"
                                ),
                                o_auth2_credentials=datazone_mixins.CfnConnectionPropsMixin.GlueOAuth2CredentialsProperty(
                                    access_token="accessToken",
                                    jwt_token="jwtToken",
                                    refresh_token="refreshToken",
                                    user_managed_client_application_client_secret="userManagedClientApplicationClientSecret"
                                ),
                                o_auth2_grant_type="oAuth2GrantType",
                                token_url="tokenUrl",
                                token_url_parameters_map={
                                    "token_url_parameters_map_key": "tokenUrlParametersMap"
                                }
                            ),
                            secret_arn="secretArn"
                        ),
                        connection_properties={
                            "connection_properties_key": "connectionProperties"
                        },
                        connection_type="connectionType",
                        description="description",
                        match_criteria="matchCriteria",
                        name="name",
                        physical_connection_requirements=datazone_mixins.CfnConnectionPropsMixin.PhysicalConnectionRequirementsProperty(
                            availability_zone="availabilityZone",
                            security_group_id_list=["securityGroupIdList"],
                            subnet_id="subnetId",
                            subnet_id_list=["subnetIdList"]
                        ),
                        python_properties={
                            "python_properties_key": "pythonProperties"
                        },
                        spark_properties={
                            "spark_properties_key": "sparkProperties"
                        },
                        validate_credentials=False,
                        validate_for_compute_environments=["validateForComputeEnvironments"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__450b1bed31fcd1c8b65795972913a54cf08f89b29add964a65991287c43468d4)
                check_type(argname="argument glue_connection_input", value=glue_connection_input, expected_type=type_hints["glue_connection_input"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if glue_connection_input is not None:
                self._values["glue_connection_input"] = glue_connection_input

        @builtins.property
        def glue_connection_input(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.GlueConnectionInputProperty"]]:
            '''The AWS Glue connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-gluepropertiesinput.html#cfn-datazone-connection-gluepropertiesinput-glueconnectioninput
            '''
            result = self._values.get("glue_connection_input")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.GlueConnectionInputProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GluePropertiesInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnConnectionPropsMixin.HyperPodPropertiesInputProperty",
        jsii_struct_bases=[],
        name_mapping={"cluster_name": "clusterName"},
    )
    class HyperPodPropertiesInputProperty:
        def __init__(
            self,
            *,
            cluster_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The hyper pod properties of a AWS Glue properties patch.

            :param cluster_name: The cluster name the hyper pod properties.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-hyperpodpropertiesinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                hyper_pod_properties_input_property = datazone_mixins.CfnConnectionPropsMixin.HyperPodPropertiesInputProperty(
                    cluster_name="clusterName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1c0fcfbcaab55f24ec59d84d2487d196f6b7eda519f210c4b6a985a5c6c5fdb2)
                check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cluster_name is not None:
                self._values["cluster_name"] = cluster_name

        @builtins.property
        def cluster_name(self) -> typing.Optional[builtins.str]:
            '''The cluster name the hyper pod properties.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-hyperpodpropertiesinput.html#cfn-datazone-connection-hyperpodpropertiesinput-clustername
            '''
            result = self._values.get("cluster_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HyperPodPropertiesInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnConnectionPropsMixin.IamPropertiesInputProperty",
        jsii_struct_bases=[],
        name_mapping={"glue_lineage_sync_enabled": "glueLineageSyncEnabled"},
    )
    class IamPropertiesInputProperty:
        def __init__(
            self,
            *,
            glue_lineage_sync_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The IAM properties of a connection.

            :param glue_lineage_sync_enabled: Specifies whether AWS Glue lineage sync is enabled for a connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-iampropertiesinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                iam_properties_input_property = datazone_mixins.CfnConnectionPropsMixin.IamPropertiesInputProperty(
                    glue_lineage_sync_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9011451acba4189a9a25f3bb9a239b4858b2156a01ec3694652a754231c9428b)
                check_type(argname="argument glue_lineage_sync_enabled", value=glue_lineage_sync_enabled, expected_type=type_hints["glue_lineage_sync_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if glue_lineage_sync_enabled is not None:
                self._values["glue_lineage_sync_enabled"] = glue_lineage_sync_enabled

        @builtins.property
        def glue_lineage_sync_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether AWS Glue lineage sync is enabled for a connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-iampropertiesinput.html#cfn-datazone-connection-iampropertiesinput-gluelineagesyncenabled
            '''
            result = self._values.get("glue_lineage_sync_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IamPropertiesInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnConnectionPropsMixin.LineageSyncScheduleProperty",
        jsii_struct_bases=[],
        name_mapping={"schedule": "schedule"},
    )
    class LineageSyncScheduleProperty:
        def __init__(self, *, schedule: typing.Optional[builtins.str] = None) -> None:
            '''The lineage sync schedule.

            :param schedule: The lineage sync schedule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-lineagesyncschedule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                lineage_sync_schedule_property = datazone_mixins.CfnConnectionPropsMixin.LineageSyncScheduleProperty(
                    schedule="schedule"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fa6025fa2c389b58a41b1d700fe74e02a95c3659fc9b9db57cc8cde33a7f7895)
                check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if schedule is not None:
                self._values["schedule"] = schedule

        @builtins.property
        def schedule(self) -> typing.Optional[builtins.str]:
            '''The lineage sync schedule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-lineagesyncschedule.html#cfn-datazone-connection-lineagesyncschedule-schedule
            '''
            result = self._values.get("schedule")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LineageSyncScheduleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnConnectionPropsMixin.OAuth2ClientApplicationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "aws_managed_client_application_reference": "awsManagedClientApplicationReference",
            "user_managed_client_application_client_id": "userManagedClientApplicationClientId",
        },
    )
    class OAuth2ClientApplicationProperty:
        def __init__(
            self,
            *,
            aws_managed_client_application_reference: typing.Optional[builtins.str] = None,
            user_managed_client_application_client_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The OAuth2Client application.

            :param aws_managed_client_application_reference: The AWS managed client application reference in the OAuth2Client application.
            :param user_managed_client_application_client_id: The user managed client application client ID in the OAuth2Client application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-oauth2clientapplication.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                o_auth2_client_application_property = datazone_mixins.CfnConnectionPropsMixin.OAuth2ClientApplicationProperty(
                    aws_managed_client_application_reference="awsManagedClientApplicationReference",
                    user_managed_client_application_client_id="userManagedClientApplicationClientId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5a6f564639d60ff6173c52c3471c29ca4bccd533d06ec7c84c60cef546616582)
                check_type(argname="argument aws_managed_client_application_reference", value=aws_managed_client_application_reference, expected_type=type_hints["aws_managed_client_application_reference"])
                check_type(argname="argument user_managed_client_application_client_id", value=user_managed_client_application_client_id, expected_type=type_hints["user_managed_client_application_client_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if aws_managed_client_application_reference is not None:
                self._values["aws_managed_client_application_reference"] = aws_managed_client_application_reference
            if user_managed_client_application_client_id is not None:
                self._values["user_managed_client_application_client_id"] = user_managed_client_application_client_id

        @builtins.property
        def aws_managed_client_application_reference(
            self,
        ) -> typing.Optional[builtins.str]:
            '''The AWS managed client application reference in the OAuth2Client application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-oauth2clientapplication.html#cfn-datazone-connection-oauth2clientapplication-awsmanagedclientapplicationreference
            '''
            result = self._values.get("aws_managed_client_application_reference")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user_managed_client_application_client_id(
            self,
        ) -> typing.Optional[builtins.str]:
            '''The user managed client application client ID in the OAuth2Client application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-oauth2clientapplication.html#cfn-datazone-connection-oauth2clientapplication-usermanagedclientapplicationclientid
            '''
            result = self._values.get("user_managed_client_application_client_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OAuth2ClientApplicationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnConnectionPropsMixin.OAuth2PropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "authorization_code_properties": "authorizationCodeProperties",
            "o_auth2_client_application": "oAuth2ClientApplication",
            "o_auth2_credentials": "oAuth2Credentials",
            "o_auth2_grant_type": "oAuth2GrantType",
            "token_url": "tokenUrl",
            "token_url_parameters_map": "tokenUrlParametersMap",
        },
    )
    class OAuth2PropertiesProperty:
        def __init__(
            self,
            *,
            authorization_code_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectionPropsMixin.AuthorizationCodePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            o_auth2_client_application: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectionPropsMixin.OAuth2ClientApplicationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            o_auth2_credentials: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectionPropsMixin.GlueOAuth2CredentialsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            o_auth2_grant_type: typing.Optional[builtins.str] = None,
            token_url: typing.Optional[builtins.str] = None,
            token_url_parameters_map: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The OAuth2 properties.

            :param authorization_code_properties: The authorization code properties of the OAuth2 properties.
            :param o_auth2_client_application: The OAuth2 client application of the OAuth2 properties.
            :param o_auth2_credentials: The OAuth2 credentials of the OAuth2 properties.
            :param o_auth2_grant_type: The OAuth2 grant type of the OAuth2 properties.
            :param token_url: The OAuth2 token URL of the OAuth2 properties.
            :param token_url_parameters_map: The OAuth2 token URL parameter map of the OAuth2 properties.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-oauth2properties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                o_auth2_properties_property = datazone_mixins.CfnConnectionPropsMixin.OAuth2PropertiesProperty(
                    authorization_code_properties=datazone_mixins.CfnConnectionPropsMixin.AuthorizationCodePropertiesProperty(
                        authorization_code="authorizationCode",
                        redirect_uri="redirectUri"
                    ),
                    o_auth2_client_application=datazone_mixins.CfnConnectionPropsMixin.OAuth2ClientApplicationProperty(
                        aws_managed_client_application_reference="awsManagedClientApplicationReference",
                        user_managed_client_application_client_id="userManagedClientApplicationClientId"
                    ),
                    o_auth2_credentials=datazone_mixins.CfnConnectionPropsMixin.GlueOAuth2CredentialsProperty(
                        access_token="accessToken",
                        jwt_token="jwtToken",
                        refresh_token="refreshToken",
                        user_managed_client_application_client_secret="userManagedClientApplicationClientSecret"
                    ),
                    o_auth2_grant_type="oAuth2GrantType",
                    token_url="tokenUrl",
                    token_url_parameters_map={
                        "token_url_parameters_map_key": "tokenUrlParametersMap"
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__26bee2cd414625f5ec412cbe59e591ebe3c64dc954e5b612fc33cf33a9ae9414)
                check_type(argname="argument authorization_code_properties", value=authorization_code_properties, expected_type=type_hints["authorization_code_properties"])
                check_type(argname="argument o_auth2_client_application", value=o_auth2_client_application, expected_type=type_hints["o_auth2_client_application"])
                check_type(argname="argument o_auth2_credentials", value=o_auth2_credentials, expected_type=type_hints["o_auth2_credentials"])
                check_type(argname="argument o_auth2_grant_type", value=o_auth2_grant_type, expected_type=type_hints["o_auth2_grant_type"])
                check_type(argname="argument token_url", value=token_url, expected_type=type_hints["token_url"])
                check_type(argname="argument token_url_parameters_map", value=token_url_parameters_map, expected_type=type_hints["token_url_parameters_map"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if authorization_code_properties is not None:
                self._values["authorization_code_properties"] = authorization_code_properties
            if o_auth2_client_application is not None:
                self._values["o_auth2_client_application"] = o_auth2_client_application
            if o_auth2_credentials is not None:
                self._values["o_auth2_credentials"] = o_auth2_credentials
            if o_auth2_grant_type is not None:
                self._values["o_auth2_grant_type"] = o_auth2_grant_type
            if token_url is not None:
                self._values["token_url"] = token_url
            if token_url_parameters_map is not None:
                self._values["token_url_parameters_map"] = token_url_parameters_map

        @builtins.property
        def authorization_code_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.AuthorizationCodePropertiesProperty"]]:
            '''The authorization code properties of the OAuth2 properties.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-oauth2properties.html#cfn-datazone-connection-oauth2properties-authorizationcodeproperties
            '''
            result = self._values.get("authorization_code_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.AuthorizationCodePropertiesProperty"]], result)

        @builtins.property
        def o_auth2_client_application(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.OAuth2ClientApplicationProperty"]]:
            '''The OAuth2 client application of the OAuth2 properties.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-oauth2properties.html#cfn-datazone-connection-oauth2properties-oauth2clientapplication
            '''
            result = self._values.get("o_auth2_client_application")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.OAuth2ClientApplicationProperty"]], result)

        @builtins.property
        def o_auth2_credentials(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.GlueOAuth2CredentialsProperty"]]:
            '''The OAuth2 credentials of the OAuth2 properties.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-oauth2properties.html#cfn-datazone-connection-oauth2properties-oauth2credentials
            '''
            result = self._values.get("o_auth2_credentials")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.GlueOAuth2CredentialsProperty"]], result)

        @builtins.property
        def o_auth2_grant_type(self) -> typing.Optional[builtins.str]:
            '''The OAuth2 grant type of the OAuth2 properties.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-oauth2properties.html#cfn-datazone-connection-oauth2properties-oauth2granttype
            '''
            result = self._values.get("o_auth2_grant_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def token_url(self) -> typing.Optional[builtins.str]:
            '''The OAuth2 token URL of the OAuth2 properties.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-oauth2properties.html#cfn-datazone-connection-oauth2properties-tokenurl
            '''
            result = self._values.get("token_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def token_url_parameters_map(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''The OAuth2 token URL parameter map of the OAuth2 properties.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-oauth2properties.html#cfn-datazone-connection-oauth2properties-tokenurlparametersmap
            '''
            result = self._values.get("token_url_parameters_map")
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
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnConnectionPropsMixin.PhysicalConnectionRequirementsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "availability_zone": "availabilityZone",
            "security_group_id_list": "securityGroupIdList",
            "subnet_id": "subnetId",
            "subnet_id_list": "subnetIdList",
        },
    )
    class PhysicalConnectionRequirementsProperty:
        def __init__(
            self,
            *,
            availability_zone: typing.Optional[builtins.str] = None,
            security_group_id_list: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnet_id: typing.Optional[builtins.str] = None,
            subnet_id_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Physical connection requirements of a connection.

            :param availability_zone: The availability zone of the physical connection requirements of a connection.
            :param security_group_id_list: The group ID list of the physical connection requirements of a connection.
            :param subnet_id: The subnet ID of the physical connection requirements of a connection.
            :param subnet_id_list: The subnet ID list of the physical connection requirements of a connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-physicalconnectionrequirements.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                physical_connection_requirements_property = datazone_mixins.CfnConnectionPropsMixin.PhysicalConnectionRequirementsProperty(
                    availability_zone="availabilityZone",
                    security_group_id_list=["securityGroupIdList"],
                    subnet_id="subnetId",
                    subnet_id_list=["subnetIdList"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b0fb0914a2bfddd3e7371cf4de5de998dcb2e82406733f4abd9caae59e440297)
                check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
                check_type(argname="argument security_group_id_list", value=security_group_id_list, expected_type=type_hints["security_group_id_list"])
                check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
                check_type(argname="argument subnet_id_list", value=subnet_id_list, expected_type=type_hints["subnet_id_list"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if availability_zone is not None:
                self._values["availability_zone"] = availability_zone
            if security_group_id_list is not None:
                self._values["security_group_id_list"] = security_group_id_list
            if subnet_id is not None:
                self._values["subnet_id"] = subnet_id
            if subnet_id_list is not None:
                self._values["subnet_id_list"] = subnet_id_list

        @builtins.property
        def availability_zone(self) -> typing.Optional[builtins.str]:
            '''The availability zone of the physical connection requirements of a connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-physicalconnectionrequirements.html#cfn-datazone-connection-physicalconnectionrequirements-availabilityzone
            '''
            result = self._values.get("availability_zone")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def security_group_id_list(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The group ID list of the physical connection requirements of a connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-physicalconnectionrequirements.html#cfn-datazone-connection-physicalconnectionrequirements-securitygroupidlist
            '''
            result = self._values.get("security_group_id_list")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnet_id(self) -> typing.Optional[builtins.str]:
            '''The subnet ID of the physical connection requirements of a connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-physicalconnectionrequirements.html#cfn-datazone-connection-physicalconnectionrequirements-subnetid
            '''
            result = self._values.get("subnet_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def subnet_id_list(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The subnet ID list of the physical connection requirements of a connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-physicalconnectionrequirements.html#cfn-datazone-connection-physicalconnectionrequirements-subnetidlist
            '''
            result = self._values.get("subnet_id_list")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PhysicalConnectionRequirementsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnConnectionPropsMixin.RedshiftCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "secret_arn": "secretArn",
            "username_password": "usernamePassword",
        },
    )
    class RedshiftCredentialsProperty:
        def __init__(
            self,
            *,
            secret_arn: typing.Optional[builtins.str] = None,
            username_password: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectionPropsMixin.UsernamePasswordProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Amazon Redshift credentials of a connection.

            :param secret_arn: The secret ARN of the Amazon Redshift credentials of a connection.
            :param username_password: The username and password of the Amazon Redshift credentials of a connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-redshiftcredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                redshift_credentials_property = datazone_mixins.CfnConnectionPropsMixin.RedshiftCredentialsProperty(
                    secret_arn="secretArn",
                    username_password=datazone_mixins.CfnConnectionPropsMixin.UsernamePasswordProperty(
                        password="password",
                        username="username"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7d060a57e1a6a8558b37f25eb6d872147a6681127e4b12dcf89159339ca03749)
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
                check_type(argname="argument username_password", value=username_password, expected_type=type_hints["username_password"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if secret_arn is not None:
                self._values["secret_arn"] = secret_arn
            if username_password is not None:
                self._values["username_password"] = username_password

        @builtins.property
        def secret_arn(self) -> typing.Optional[builtins.str]:
            '''The secret ARN of the Amazon Redshift credentials of a connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-redshiftcredentials.html#cfn-datazone-connection-redshiftcredentials-secretarn
            '''
            result = self._values.get("secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def username_password(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.UsernamePasswordProperty"]]:
            '''The username and password of the Amazon Redshift credentials of a connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-redshiftcredentials.html#cfn-datazone-connection-redshiftcredentials-usernamepassword
            '''
            result = self._values.get("username_password")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.UsernamePasswordProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RedshiftCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnConnectionPropsMixin.RedshiftLineageSyncConfigurationInputProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled", "schedule": "schedule"},
    )
    class RedshiftLineageSyncConfigurationInputProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            schedule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectionPropsMixin.LineageSyncScheduleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The Amaon Redshift lineage sync configuration.

            :param enabled: Specifies whether the Amaon Redshift lineage sync configuration is enabled.
            :param schedule: The schedule of the Amaon Redshift lineage sync configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-redshiftlineagesyncconfigurationinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                redshift_lineage_sync_configuration_input_property = datazone_mixins.CfnConnectionPropsMixin.RedshiftLineageSyncConfigurationInputProperty(
                    enabled=False,
                    schedule=datazone_mixins.CfnConnectionPropsMixin.LineageSyncScheduleProperty(
                        schedule="schedule"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0ced908ff5267251237cccb60db4c765130a752e987b920faa4801ff1905bba5)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if schedule is not None:
                self._values["schedule"] = schedule

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether the Amaon Redshift lineage sync configuration is enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-redshiftlineagesyncconfigurationinput.html#cfn-datazone-connection-redshiftlineagesyncconfigurationinput-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def schedule(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.LineageSyncScheduleProperty"]]:
            '''The schedule of the Amaon Redshift lineage sync configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-redshiftlineagesyncconfigurationinput.html#cfn-datazone-connection-redshiftlineagesyncconfigurationinput-schedule
            '''
            result = self._values.get("schedule")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.LineageSyncScheduleProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RedshiftLineageSyncConfigurationInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnConnectionPropsMixin.RedshiftPropertiesInputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "credentials": "credentials",
            "database_name": "databaseName",
            "host": "host",
            "lineage_sync": "lineageSync",
            "port": "port",
            "storage": "storage",
        },
    )
    class RedshiftPropertiesInputProperty:
        def __init__(
            self,
            *,
            credentials: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectionPropsMixin.RedshiftCredentialsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            database_name: typing.Optional[builtins.str] = None,
            host: typing.Optional[builtins.str] = None,
            lineage_sync: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectionPropsMixin.RedshiftLineageSyncConfigurationInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            port: typing.Optional[jsii.Number] = None,
            storage: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectionPropsMixin.RedshiftStoragePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The Amazon Redshift properties.

            :param credentials: The Amaon Redshift credentials.
            :param database_name: The Amazon Redshift database name.
            :param host: The Amazon Redshift host.
            :param lineage_sync: The lineage sync of the Amazon Redshift.
            :param port: The Amaon Redshift port.
            :param storage: The Amazon Redshift storage.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-redshiftpropertiesinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                redshift_properties_input_property = datazone_mixins.CfnConnectionPropsMixin.RedshiftPropertiesInputProperty(
                    credentials=datazone_mixins.CfnConnectionPropsMixin.RedshiftCredentialsProperty(
                        secret_arn="secretArn",
                        username_password=datazone_mixins.CfnConnectionPropsMixin.UsernamePasswordProperty(
                            password="password",
                            username="username"
                        )
                    ),
                    database_name="databaseName",
                    host="host",
                    lineage_sync=datazone_mixins.CfnConnectionPropsMixin.RedshiftLineageSyncConfigurationInputProperty(
                        enabled=False,
                        schedule=datazone_mixins.CfnConnectionPropsMixin.LineageSyncScheduleProperty(
                            schedule="schedule"
                        )
                    ),
                    port=123,
                    storage=datazone_mixins.CfnConnectionPropsMixin.RedshiftStoragePropertiesProperty(
                        cluster_name="clusterName",
                        workgroup_name="workgroupName"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fe65a531a84fc820d659ae0c1ee946c4f7a20edd20a4406c2bc48cfec411b44f)
                check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument host", value=host, expected_type=type_hints["host"])
                check_type(argname="argument lineage_sync", value=lineage_sync, expected_type=type_hints["lineage_sync"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument storage", value=storage, expected_type=type_hints["storage"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if credentials is not None:
                self._values["credentials"] = credentials
            if database_name is not None:
                self._values["database_name"] = database_name
            if host is not None:
                self._values["host"] = host
            if lineage_sync is not None:
                self._values["lineage_sync"] = lineage_sync
            if port is not None:
                self._values["port"] = port
            if storage is not None:
                self._values["storage"] = storage

        @builtins.property
        def credentials(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.RedshiftCredentialsProperty"]]:
            '''The Amaon Redshift credentials.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-redshiftpropertiesinput.html#cfn-datazone-connection-redshiftpropertiesinput-credentials
            '''
            result = self._values.get("credentials")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.RedshiftCredentialsProperty"]], result)

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            '''The Amazon Redshift database name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-redshiftpropertiesinput.html#cfn-datazone-connection-redshiftpropertiesinput-databasename
            '''
            result = self._values.get("database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def host(self) -> typing.Optional[builtins.str]:
            '''The Amazon Redshift host.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-redshiftpropertiesinput.html#cfn-datazone-connection-redshiftpropertiesinput-host
            '''
            result = self._values.get("host")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def lineage_sync(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.RedshiftLineageSyncConfigurationInputProperty"]]:
            '''The lineage sync of the Amazon Redshift.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-redshiftpropertiesinput.html#cfn-datazone-connection-redshiftpropertiesinput-lineagesync
            '''
            result = self._values.get("lineage_sync")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.RedshiftLineageSyncConfigurationInputProperty"]], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''The Amaon Redshift port.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-redshiftpropertiesinput.html#cfn-datazone-connection-redshiftpropertiesinput-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def storage(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.RedshiftStoragePropertiesProperty"]]:
            '''The Amazon Redshift storage.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-redshiftpropertiesinput.html#cfn-datazone-connection-redshiftpropertiesinput-storage
            '''
            result = self._values.get("storage")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.RedshiftStoragePropertiesProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RedshiftPropertiesInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnConnectionPropsMixin.RedshiftStoragePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cluster_name": "clusterName",
            "workgroup_name": "workgroupName",
        },
    )
    class RedshiftStoragePropertiesProperty:
        def __init__(
            self,
            *,
            cluster_name: typing.Optional[builtins.str] = None,
            workgroup_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The Amazon Redshift storage properties.

            :param cluster_name: The cluster name in the Amazon Redshift storage properties.
            :param workgroup_name: The workgroup name in the Amazon Redshift storage properties.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-redshiftstorageproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                redshift_storage_properties_property = datazone_mixins.CfnConnectionPropsMixin.RedshiftStoragePropertiesProperty(
                    cluster_name="clusterName",
                    workgroup_name="workgroupName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5ed73eb1679aa2af22d9a5fb093c36b117e2b7ae23b838cbae74c366cc4a59f7)
                check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
                check_type(argname="argument workgroup_name", value=workgroup_name, expected_type=type_hints["workgroup_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cluster_name is not None:
                self._values["cluster_name"] = cluster_name
            if workgroup_name is not None:
                self._values["workgroup_name"] = workgroup_name

        @builtins.property
        def cluster_name(self) -> typing.Optional[builtins.str]:
            '''The cluster name in the Amazon Redshift storage properties.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-redshiftstorageproperties.html#cfn-datazone-connection-redshiftstorageproperties-clustername
            '''
            result = self._values.get("cluster_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def workgroup_name(self) -> typing.Optional[builtins.str]:
            '''The workgroup name in the Amazon Redshift storage properties.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-redshiftstorageproperties.html#cfn-datazone-connection-redshiftstorageproperties-workgroupname
            '''
            result = self._values.get("workgroup_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RedshiftStoragePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnConnectionPropsMixin.S3PropertiesInputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "s3_access_grant_location_id": "s3AccessGrantLocationId",
            "s3_uri": "s3Uri",
        },
    )
    class S3PropertiesInputProperty:
        def __init__(
            self,
            *,
            s3_access_grant_location_id: typing.Optional[builtins.str] = None,
            s3_uri: typing.Optional[builtins.str] = None,
        ) -> None:
            '''S3 Properties Input.

            :param s3_access_grant_location_id: The Amazon S3 Access Grant location ID that's part of the Amazon S3 properties of a connection.
            :param s3_uri: The Amazon S3 URI that's part of the Amazon S3 properties of a connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-s3propertiesinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                s3_properties_input_property = datazone_mixins.CfnConnectionPropsMixin.S3PropertiesInputProperty(
                    s3_access_grant_location_id="s3AccessGrantLocationId",
                    s3_uri="s3Uri"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2df7ba0b6b76c9b5d1dae690761f5475fa91bb89b40c3576df10528f21d7e030)
                check_type(argname="argument s3_access_grant_location_id", value=s3_access_grant_location_id, expected_type=type_hints["s3_access_grant_location_id"])
                check_type(argname="argument s3_uri", value=s3_uri, expected_type=type_hints["s3_uri"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3_access_grant_location_id is not None:
                self._values["s3_access_grant_location_id"] = s3_access_grant_location_id
            if s3_uri is not None:
                self._values["s3_uri"] = s3_uri

        @builtins.property
        def s3_access_grant_location_id(self) -> typing.Optional[builtins.str]:
            '''The Amazon S3 Access Grant location ID that's part of the Amazon S3 properties of a connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-s3propertiesinput.html#cfn-datazone-connection-s3propertiesinput-s3accessgrantlocationid
            '''
            result = self._values.get("s3_access_grant_location_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_uri(self) -> typing.Optional[builtins.str]:
            '''The Amazon S3 URI that's part of the Amazon S3 properties of a connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-s3propertiesinput.html#cfn-datazone-connection-s3propertiesinput-s3uri
            '''
            result = self._values.get("s3_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3PropertiesInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnConnectionPropsMixin.SparkEmrPropertiesInputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "compute_arn": "computeArn",
            "instance_profile_arn": "instanceProfileArn",
            "java_virtual_env": "javaVirtualEnv",
            "log_uri": "logUri",
            "managed_endpoint_arn": "managedEndpointArn",
            "python_virtual_env": "pythonVirtualEnv",
            "runtime_role": "runtimeRole",
            "trusted_certificates_s3_uri": "trustedCertificatesS3Uri",
        },
    )
    class SparkEmrPropertiesInputProperty:
        def __init__(
            self,
            *,
            compute_arn: typing.Optional[builtins.str] = None,
            instance_profile_arn: typing.Optional[builtins.str] = None,
            java_virtual_env: typing.Optional[builtins.str] = None,
            log_uri: typing.Optional[builtins.str] = None,
            managed_endpoint_arn: typing.Optional[builtins.str] = None,
            python_virtual_env: typing.Optional[builtins.str] = None,
            runtime_role: typing.Optional[builtins.str] = None,
            trusted_certificates_s3_uri: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The Spark EMR properties.

            :param compute_arn: The compute ARN of Spark EMR.
            :param instance_profile_arn: The instance profile ARN of Spark EMR.
            :param java_virtual_env: The java virtual env of the Spark EMR.
            :param log_uri: The log URI of the Spark EMR.
            :param managed_endpoint_arn: 
            :param python_virtual_env: The Python virtual env of the Spark EMR.
            :param runtime_role: The runtime role of the Spark EMR.
            :param trusted_certificates_s3_uri: The certificates S3 URI of the Spark EMR.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-sparkemrpropertiesinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                spark_emr_properties_input_property = datazone_mixins.CfnConnectionPropsMixin.SparkEmrPropertiesInputProperty(
                    compute_arn="computeArn",
                    instance_profile_arn="instanceProfileArn",
                    java_virtual_env="javaVirtualEnv",
                    log_uri="logUri",
                    managed_endpoint_arn="managedEndpointArn",
                    python_virtual_env="pythonVirtualEnv",
                    runtime_role="runtimeRole",
                    trusted_certificates_s3_uri="trustedCertificatesS3Uri"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__39c202b1386f9006ff2f113353d49e792d833bf16177a4efa125aceaa63cf59e)
                check_type(argname="argument compute_arn", value=compute_arn, expected_type=type_hints["compute_arn"])
                check_type(argname="argument instance_profile_arn", value=instance_profile_arn, expected_type=type_hints["instance_profile_arn"])
                check_type(argname="argument java_virtual_env", value=java_virtual_env, expected_type=type_hints["java_virtual_env"])
                check_type(argname="argument log_uri", value=log_uri, expected_type=type_hints["log_uri"])
                check_type(argname="argument managed_endpoint_arn", value=managed_endpoint_arn, expected_type=type_hints["managed_endpoint_arn"])
                check_type(argname="argument python_virtual_env", value=python_virtual_env, expected_type=type_hints["python_virtual_env"])
                check_type(argname="argument runtime_role", value=runtime_role, expected_type=type_hints["runtime_role"])
                check_type(argname="argument trusted_certificates_s3_uri", value=trusted_certificates_s3_uri, expected_type=type_hints["trusted_certificates_s3_uri"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if compute_arn is not None:
                self._values["compute_arn"] = compute_arn
            if instance_profile_arn is not None:
                self._values["instance_profile_arn"] = instance_profile_arn
            if java_virtual_env is not None:
                self._values["java_virtual_env"] = java_virtual_env
            if log_uri is not None:
                self._values["log_uri"] = log_uri
            if managed_endpoint_arn is not None:
                self._values["managed_endpoint_arn"] = managed_endpoint_arn
            if python_virtual_env is not None:
                self._values["python_virtual_env"] = python_virtual_env
            if runtime_role is not None:
                self._values["runtime_role"] = runtime_role
            if trusted_certificates_s3_uri is not None:
                self._values["trusted_certificates_s3_uri"] = trusted_certificates_s3_uri

        @builtins.property
        def compute_arn(self) -> typing.Optional[builtins.str]:
            '''The compute ARN of Spark EMR.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-sparkemrpropertiesinput.html#cfn-datazone-connection-sparkemrpropertiesinput-computearn
            '''
            result = self._values.get("compute_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def instance_profile_arn(self) -> typing.Optional[builtins.str]:
            '''The instance profile ARN of Spark EMR.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-sparkemrpropertiesinput.html#cfn-datazone-connection-sparkemrpropertiesinput-instanceprofilearn
            '''
            result = self._values.get("instance_profile_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def java_virtual_env(self) -> typing.Optional[builtins.str]:
            '''The java virtual env of the Spark EMR.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-sparkemrpropertiesinput.html#cfn-datazone-connection-sparkemrpropertiesinput-javavirtualenv
            '''
            result = self._values.get("java_virtual_env")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_uri(self) -> typing.Optional[builtins.str]:
            '''The log URI of the Spark EMR.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-sparkemrpropertiesinput.html#cfn-datazone-connection-sparkemrpropertiesinput-loguri
            '''
            result = self._values.get("log_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def managed_endpoint_arn(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-sparkemrpropertiesinput.html#cfn-datazone-connection-sparkemrpropertiesinput-managedendpointarn
            '''
            result = self._values.get("managed_endpoint_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def python_virtual_env(self) -> typing.Optional[builtins.str]:
            '''The Python virtual env of the Spark EMR.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-sparkemrpropertiesinput.html#cfn-datazone-connection-sparkemrpropertiesinput-pythonvirtualenv
            '''
            result = self._values.get("python_virtual_env")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def runtime_role(self) -> typing.Optional[builtins.str]:
            '''The runtime role of the Spark EMR.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-sparkemrpropertiesinput.html#cfn-datazone-connection-sparkemrpropertiesinput-runtimerole
            '''
            result = self._values.get("runtime_role")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def trusted_certificates_s3_uri(self) -> typing.Optional[builtins.str]:
            '''The certificates S3 URI of the Spark EMR.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-sparkemrpropertiesinput.html#cfn-datazone-connection-sparkemrpropertiesinput-trustedcertificatess3uri
            '''
            result = self._values.get("trusted_certificates_s3_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SparkEmrPropertiesInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnConnectionPropsMixin.SparkGlueArgsProperty",
        jsii_struct_bases=[],
        name_mapping={"connection": "connection"},
    )
    class SparkGlueArgsProperty:
        def __init__(self, *, connection: typing.Optional[builtins.str] = None) -> None:
            '''The Spark AWS Glue args.

            :param connection: The connection in the Spark AWS Glue args.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-sparkglueargs.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                spark_glue_args_property = datazone_mixins.CfnConnectionPropsMixin.SparkGlueArgsProperty(
                    connection="connection"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6bc34d1eab5d30edccaf2e664c3fb46b351ee444d4a3c0ecffbcedec4cf5da7d)
                check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if connection is not None:
                self._values["connection"] = connection

        @builtins.property
        def connection(self) -> typing.Optional[builtins.str]:
            '''The connection in the Spark AWS Glue args.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-sparkglueargs.html#cfn-datazone-connection-sparkglueargs-connection
            '''
            result = self._values.get("connection")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SparkGlueArgsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnConnectionPropsMixin.SparkGluePropertiesInputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "additional_args": "additionalArgs",
            "glue_connection_name": "glueConnectionName",
            "glue_version": "glueVersion",
            "idle_timeout": "idleTimeout",
            "java_virtual_env": "javaVirtualEnv",
            "number_of_workers": "numberOfWorkers",
            "python_virtual_env": "pythonVirtualEnv",
            "worker_type": "workerType",
        },
    )
    class SparkGluePropertiesInputProperty:
        def __init__(
            self,
            *,
            additional_args: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectionPropsMixin.SparkGlueArgsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            glue_connection_name: typing.Optional[builtins.str] = None,
            glue_version: typing.Optional[builtins.str] = None,
            idle_timeout: typing.Optional[jsii.Number] = None,
            java_virtual_env: typing.Optional[builtins.str] = None,
            number_of_workers: typing.Optional[jsii.Number] = None,
            python_virtual_env: typing.Optional[builtins.str] = None,
            worker_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The Spark AWS Glue properties.

            :param additional_args: The additional args in the Spark AWS Glue properties.
            :param glue_connection_name: The AWS Glue connection name in the Spark AWS Glue properties.
            :param glue_version: The AWS Glue version in the Spark AWS Glue properties.
            :param idle_timeout: The idle timeout in the Spark AWS Glue properties.
            :param java_virtual_env: The Java virtual env in the Spark AWS Glue properties.
            :param number_of_workers: The number of workers in the Spark AWS Glue properties.
            :param python_virtual_env: The Python virtual env in the Spark AWS Glue properties.
            :param worker_type: The worker type in the Spark AWS Glue properties.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-sparkgluepropertiesinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                spark_glue_properties_input_property = datazone_mixins.CfnConnectionPropsMixin.SparkGluePropertiesInputProperty(
                    additional_args=datazone_mixins.CfnConnectionPropsMixin.SparkGlueArgsProperty(
                        connection="connection"
                    ),
                    glue_connection_name="glueConnectionName",
                    glue_version="glueVersion",
                    idle_timeout=123,
                    java_virtual_env="javaVirtualEnv",
                    number_of_workers=123,
                    python_virtual_env="pythonVirtualEnv",
                    worker_type="workerType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__09ceadb9c4ff9127188010bee62fa24b1ed26a5cf42b9c279b9f625cf3d28bba)
                check_type(argname="argument additional_args", value=additional_args, expected_type=type_hints["additional_args"])
                check_type(argname="argument glue_connection_name", value=glue_connection_name, expected_type=type_hints["glue_connection_name"])
                check_type(argname="argument glue_version", value=glue_version, expected_type=type_hints["glue_version"])
                check_type(argname="argument idle_timeout", value=idle_timeout, expected_type=type_hints["idle_timeout"])
                check_type(argname="argument java_virtual_env", value=java_virtual_env, expected_type=type_hints["java_virtual_env"])
                check_type(argname="argument number_of_workers", value=number_of_workers, expected_type=type_hints["number_of_workers"])
                check_type(argname="argument python_virtual_env", value=python_virtual_env, expected_type=type_hints["python_virtual_env"])
                check_type(argname="argument worker_type", value=worker_type, expected_type=type_hints["worker_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if additional_args is not None:
                self._values["additional_args"] = additional_args
            if glue_connection_name is not None:
                self._values["glue_connection_name"] = glue_connection_name
            if glue_version is not None:
                self._values["glue_version"] = glue_version
            if idle_timeout is not None:
                self._values["idle_timeout"] = idle_timeout
            if java_virtual_env is not None:
                self._values["java_virtual_env"] = java_virtual_env
            if number_of_workers is not None:
                self._values["number_of_workers"] = number_of_workers
            if python_virtual_env is not None:
                self._values["python_virtual_env"] = python_virtual_env
            if worker_type is not None:
                self._values["worker_type"] = worker_type

        @builtins.property
        def additional_args(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.SparkGlueArgsProperty"]]:
            '''The additional args in the Spark AWS Glue properties.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-sparkgluepropertiesinput.html#cfn-datazone-connection-sparkgluepropertiesinput-additionalargs
            '''
            result = self._values.get("additional_args")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.SparkGlueArgsProperty"]], result)

        @builtins.property
        def glue_connection_name(self) -> typing.Optional[builtins.str]:
            '''The AWS Glue connection name in the Spark AWS Glue properties.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-sparkgluepropertiesinput.html#cfn-datazone-connection-sparkgluepropertiesinput-glueconnectionname
            '''
            result = self._values.get("glue_connection_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def glue_version(self) -> typing.Optional[builtins.str]:
            '''The AWS Glue version in the Spark AWS Glue properties.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-sparkgluepropertiesinput.html#cfn-datazone-connection-sparkgluepropertiesinput-glueversion
            '''
            result = self._values.get("glue_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def idle_timeout(self) -> typing.Optional[jsii.Number]:
            '''The idle timeout in the Spark AWS Glue properties.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-sparkgluepropertiesinput.html#cfn-datazone-connection-sparkgluepropertiesinput-idletimeout
            '''
            result = self._values.get("idle_timeout")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def java_virtual_env(self) -> typing.Optional[builtins.str]:
            '''The Java virtual env in the Spark AWS Glue properties.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-sparkgluepropertiesinput.html#cfn-datazone-connection-sparkgluepropertiesinput-javavirtualenv
            '''
            result = self._values.get("java_virtual_env")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def number_of_workers(self) -> typing.Optional[jsii.Number]:
            '''The number of workers in the Spark AWS Glue properties.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-sparkgluepropertiesinput.html#cfn-datazone-connection-sparkgluepropertiesinput-numberofworkers
            '''
            result = self._values.get("number_of_workers")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def python_virtual_env(self) -> typing.Optional[builtins.str]:
            '''The Python virtual env in the Spark AWS Glue properties.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-sparkgluepropertiesinput.html#cfn-datazone-connection-sparkgluepropertiesinput-pythonvirtualenv
            '''
            result = self._values.get("python_virtual_env")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def worker_type(self) -> typing.Optional[builtins.str]:
            '''The worker type in the Spark AWS Glue properties.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-sparkgluepropertiesinput.html#cfn-datazone-connection-sparkgluepropertiesinput-workertype
            '''
            result = self._values.get("worker_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SparkGluePropertiesInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnConnectionPropsMixin.UsernamePasswordProperty",
        jsii_struct_bases=[],
        name_mapping={"password": "password", "username": "username"},
    )
    class UsernamePasswordProperty:
        def __init__(
            self,
            *,
            password: typing.Optional[builtins.str] = None,
            username: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The username and password of a connection.

            :param password: The password of a connection.
            :param username: The username of a connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-usernamepassword.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                username_password_property = datazone_mixins.CfnConnectionPropsMixin.UsernamePasswordProperty(
                    password="password",
                    username="username"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fc5ebb7e7cdfa9efb28b58fafe7f2a8107a5756a5ddc7a4e13b2e07baa5d3c9c)
                check_type(argname="argument password", value=password, expected_type=type_hints["password"])
                check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if password is not None:
                self._values["password"] = password
            if username is not None:
                self._values["username"] = username

        @builtins.property
        def password(self) -> typing.Optional[builtins.str]:
            '''The password of a connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-usernamepassword.html#cfn-datazone-connection-usernamepassword-password
            '''
            result = self._values.get("password")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def username(self) -> typing.Optional[builtins.str]:
            '''The username of a connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-connection-usernamepassword.html#cfn-datazone-connection-usernamepassword-username
            '''
            result = self._values.get("username")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UsernamePasswordProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnDataSourceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "asset_forms_input": "assetFormsInput",
        "configuration": "configuration",
        "connection_identifier": "connectionIdentifier",
        "description": "description",
        "domain_identifier": "domainIdentifier",
        "enable_setting": "enableSetting",
        "environment_identifier": "environmentIdentifier",
        "name": "name",
        "project_identifier": "projectIdentifier",
        "publish_on_import": "publishOnImport",
        "recommendation": "recommendation",
        "schedule": "schedule",
        "type": "type",
    },
)
class CfnDataSourceMixinProps:
    def __init__(
        self,
        *,
        asset_forms_input: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.FormInputProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.DataSourceConfigurationInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        connection_identifier: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        domain_identifier: typing.Optional[builtins.str] = None,
        enable_setting: typing.Optional[builtins.str] = None,
        environment_identifier: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        project_identifier: typing.Optional[builtins.str] = None,
        publish_on_import: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        recommendation: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.RecommendationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        schedule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.ScheduleConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnDataSourcePropsMixin.

        :param asset_forms_input: The metadata forms attached to the assets that the data source works with.
        :param configuration: The configuration of the data source.
        :param connection_identifier: The unique identifier of a connection used to fetch relevant parameters from connection during Datasource run.
        :param description: The description of the data source.
        :param domain_identifier: The ID of the Amazon DataZone domain where the data source is created.
        :param enable_setting: Specifies whether the data source is enabled.
        :param environment_identifier: The unique identifier of the Amazon DataZone environment to which the data source publishes assets.
        :param name: The name of the data source.
        :param project_identifier: The identifier of the Amazon DataZone project in which you want to add this data source.
        :param publish_on_import: Specifies whether the assets that this data source creates in the inventory are to be also automatically published to the catalog.
        :param recommendation: Specifies whether the business name generation is to be enabled for this data source.
        :param schedule: The schedule of the data source runs.
        :param type: The type of the data source. In Amazon DataZone, you can use data sources to import technical metadata of assets (data) from the source databases or data warehouses into Amazon DataZone. In the current release of Amazon DataZone, you can create and run data sources for AWS Glue and Amazon Redshift.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-datasource.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
            
            cfn_data_source_mixin_props = datazone_mixins.CfnDataSourceMixinProps(
                asset_forms_input=[datazone_mixins.CfnDataSourcePropsMixin.FormInputProperty(
                    content="content",
                    form_name="formName",
                    type_identifier="typeIdentifier",
                    type_revision="typeRevision"
                )],
                configuration=datazone_mixins.CfnDataSourcePropsMixin.DataSourceConfigurationInputProperty(
                    glue_run_configuration=datazone_mixins.CfnDataSourcePropsMixin.GlueRunConfigurationInputProperty(
                        auto_import_data_quality_result=False,
                        catalog_name="catalogName",
                        data_access_role="dataAccessRole",
                        relational_filter_configurations=[datazone_mixins.CfnDataSourcePropsMixin.RelationalFilterConfigurationProperty(
                            database_name="databaseName",
                            filter_expressions=[datazone_mixins.CfnDataSourcePropsMixin.FilterExpressionProperty(
                                expression="expression",
                                type="type"
                            )],
                            schema_name="schemaName"
                        )]
                    ),
                    redshift_run_configuration=datazone_mixins.CfnDataSourcePropsMixin.RedshiftRunConfigurationInputProperty(
                        data_access_role="dataAccessRole",
                        redshift_credential_configuration=datazone_mixins.CfnDataSourcePropsMixin.RedshiftCredentialConfigurationProperty(
                            secret_manager_arn="secretManagerArn"
                        ),
                        redshift_storage=datazone_mixins.CfnDataSourcePropsMixin.RedshiftStorageProperty(
                            redshift_cluster_source=datazone_mixins.CfnDataSourcePropsMixin.RedshiftClusterStorageProperty(
                                cluster_name="clusterName"
                            ),
                            redshift_serverless_source=datazone_mixins.CfnDataSourcePropsMixin.RedshiftServerlessStorageProperty(
                                workgroup_name="workgroupName"
                            )
                        ),
                        relational_filter_configurations=[datazone_mixins.CfnDataSourcePropsMixin.RelationalFilterConfigurationProperty(
                            database_name="databaseName",
                            filter_expressions=[datazone_mixins.CfnDataSourcePropsMixin.FilterExpressionProperty(
                                expression="expression",
                                type="type"
                            )],
                            schema_name="schemaName"
                        )]
                    ),
                    sage_maker_run_configuration=datazone_mixins.CfnDataSourcePropsMixin.SageMakerRunConfigurationInputProperty(
                        tracking_assets={
                            "tracking_assets_key": ["trackingAssets"]
                        }
                    )
                ),
                connection_identifier="connectionIdentifier",
                description="description",
                domain_identifier="domainIdentifier",
                enable_setting="enableSetting",
                environment_identifier="environmentIdentifier",
                name="name",
                project_identifier="projectIdentifier",
                publish_on_import=False,
                recommendation=datazone_mixins.CfnDataSourcePropsMixin.RecommendationConfigurationProperty(
                    enable_business_name_generation=False
                ),
                schedule=datazone_mixins.CfnDataSourcePropsMixin.ScheduleConfigurationProperty(
                    schedule="schedule",
                    timezone="timezone"
                ),
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b17101a94186c9c71e74e2b1916cf53e0c7cee6a94487f0b30257e56f4fa2456)
            check_type(argname="argument asset_forms_input", value=asset_forms_input, expected_type=type_hints["asset_forms_input"])
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument connection_identifier", value=connection_identifier, expected_type=type_hints["connection_identifier"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument domain_identifier", value=domain_identifier, expected_type=type_hints["domain_identifier"])
            check_type(argname="argument enable_setting", value=enable_setting, expected_type=type_hints["enable_setting"])
            check_type(argname="argument environment_identifier", value=environment_identifier, expected_type=type_hints["environment_identifier"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument project_identifier", value=project_identifier, expected_type=type_hints["project_identifier"])
            check_type(argname="argument publish_on_import", value=publish_on_import, expected_type=type_hints["publish_on_import"])
            check_type(argname="argument recommendation", value=recommendation, expected_type=type_hints["recommendation"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if asset_forms_input is not None:
            self._values["asset_forms_input"] = asset_forms_input
        if configuration is not None:
            self._values["configuration"] = configuration
        if connection_identifier is not None:
            self._values["connection_identifier"] = connection_identifier
        if description is not None:
            self._values["description"] = description
        if domain_identifier is not None:
            self._values["domain_identifier"] = domain_identifier
        if enable_setting is not None:
            self._values["enable_setting"] = enable_setting
        if environment_identifier is not None:
            self._values["environment_identifier"] = environment_identifier
        if name is not None:
            self._values["name"] = name
        if project_identifier is not None:
            self._values["project_identifier"] = project_identifier
        if publish_on_import is not None:
            self._values["publish_on_import"] = publish_on_import
        if recommendation is not None:
            self._values["recommendation"] = recommendation
        if schedule is not None:
            self._values["schedule"] = schedule
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def asset_forms_input(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.FormInputProperty"]]]]:
        '''The metadata forms attached to the assets that the data source works with.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-datasource.html#cfn-datazone-datasource-assetformsinput
        '''
        result = self._values.get("asset_forms_input")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.FormInputProperty"]]]], result)

    @builtins.property
    def configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DataSourceConfigurationInputProperty"]]:
        '''The configuration of the data source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-datasource.html#cfn-datazone-datasource-configuration
        '''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DataSourceConfigurationInputProperty"]], result)

    @builtins.property
    def connection_identifier(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of a connection used to fetch relevant parameters from connection during Datasource run.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-datasource.html#cfn-datazone-datasource-connectionidentifier
        '''
        result = self._values.get("connection_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the data source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-datasource.html#cfn-datazone-datasource-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_identifier(self) -> typing.Optional[builtins.str]:
        '''The ID of the Amazon DataZone domain where the data source is created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-datasource.html#cfn-datazone-datasource-domainidentifier
        '''
        result = self._values.get("domain_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_setting(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the data source is enabled.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-datasource.html#cfn-datazone-datasource-enablesetting
        '''
        result = self._values.get("enable_setting")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_identifier(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the Amazon DataZone environment to which the data source publishes assets.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-datasource.html#cfn-datazone-datasource-environmentidentifier
        '''
        result = self._values.get("environment_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the data source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-datasource.html#cfn-datazone-datasource-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_identifier(self) -> typing.Optional[builtins.str]:
        '''The identifier of the Amazon DataZone project in which you want to add this data source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-datasource.html#cfn-datazone-datasource-projectidentifier
        '''
        result = self._values.get("project_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def publish_on_import(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether the assets that this data source creates in the inventory are to be also automatically published to the catalog.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-datasource.html#cfn-datazone-datasource-publishonimport
        '''
        result = self._values.get("publish_on_import")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def recommendation(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.RecommendationConfigurationProperty"]]:
        '''Specifies whether the business name generation is to be enabled for this data source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-datasource.html#cfn-datazone-datasource-recommendation
        '''
        result = self._values.get("recommendation")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.RecommendationConfigurationProperty"]], result)

    @builtins.property
    def schedule(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.ScheduleConfigurationProperty"]]:
        '''The schedule of the data source runs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-datasource.html#cfn-datazone-datasource-schedule
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.ScheduleConfigurationProperty"]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of the data source.

        In Amazon DataZone, you can use data sources to import technical metadata of assets (data) from the source databases or data warehouses into Amazon DataZone. In the current release of Amazon DataZone, you can create and run data sources for AWS Glue and Amazon Redshift.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-datasource.html#cfn-datazone-datasource-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDataSourceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDataSourcePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnDataSourcePropsMixin",
):
    '''The ``AWS::DataZone::DataSource`` resource specifies an Amazon DataZone data source that is used to import technical metadata of assets (data) from the source databases or data warehouses into Amazon DataZone.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-datasource.html
    :cloudformationResource: AWS::DataZone::DataSource
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
        
        cfn_data_source_props_mixin = datazone_mixins.CfnDataSourcePropsMixin(datazone_mixins.CfnDataSourceMixinProps(
            asset_forms_input=[datazone_mixins.CfnDataSourcePropsMixin.FormInputProperty(
                content="content",
                form_name="formName",
                type_identifier="typeIdentifier",
                type_revision="typeRevision"
            )],
            configuration=datazone_mixins.CfnDataSourcePropsMixin.DataSourceConfigurationInputProperty(
                glue_run_configuration=datazone_mixins.CfnDataSourcePropsMixin.GlueRunConfigurationInputProperty(
                    auto_import_data_quality_result=False,
                    catalog_name="catalogName",
                    data_access_role="dataAccessRole",
                    relational_filter_configurations=[datazone_mixins.CfnDataSourcePropsMixin.RelationalFilterConfigurationProperty(
                        database_name="databaseName",
                        filter_expressions=[datazone_mixins.CfnDataSourcePropsMixin.FilterExpressionProperty(
                            expression="expression",
                            type="type"
                        )],
                        schema_name="schemaName"
                    )]
                ),
                redshift_run_configuration=datazone_mixins.CfnDataSourcePropsMixin.RedshiftRunConfigurationInputProperty(
                    data_access_role="dataAccessRole",
                    redshift_credential_configuration=datazone_mixins.CfnDataSourcePropsMixin.RedshiftCredentialConfigurationProperty(
                        secret_manager_arn="secretManagerArn"
                    ),
                    redshift_storage=datazone_mixins.CfnDataSourcePropsMixin.RedshiftStorageProperty(
                        redshift_cluster_source=datazone_mixins.CfnDataSourcePropsMixin.RedshiftClusterStorageProperty(
                            cluster_name="clusterName"
                        ),
                        redshift_serverless_source=datazone_mixins.CfnDataSourcePropsMixin.RedshiftServerlessStorageProperty(
                            workgroup_name="workgroupName"
                        )
                    ),
                    relational_filter_configurations=[datazone_mixins.CfnDataSourcePropsMixin.RelationalFilterConfigurationProperty(
                        database_name="databaseName",
                        filter_expressions=[datazone_mixins.CfnDataSourcePropsMixin.FilterExpressionProperty(
                            expression="expression",
                            type="type"
                        )],
                        schema_name="schemaName"
                    )]
                ),
                sage_maker_run_configuration=datazone_mixins.CfnDataSourcePropsMixin.SageMakerRunConfigurationInputProperty(
                    tracking_assets={
                        "tracking_assets_key": ["trackingAssets"]
                    }
                )
            ),
            connection_identifier="connectionIdentifier",
            description="description",
            domain_identifier="domainIdentifier",
            enable_setting="enableSetting",
            environment_identifier="environmentIdentifier",
            name="name",
            project_identifier="projectIdentifier",
            publish_on_import=False,
            recommendation=datazone_mixins.CfnDataSourcePropsMixin.RecommendationConfigurationProperty(
                enable_business_name_generation=False
            ),
            schedule=datazone_mixins.CfnDataSourcePropsMixin.ScheduleConfigurationProperty(
                schedule="schedule",
                timezone="timezone"
            ),
            type="type"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDataSourceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DataZone::DataSource``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97dfe47605dbb87ccbbe262f292763127ef5d758f6baa4d2f590467983a24bdf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c11e73196533c35e3d900830b3f50f68a1346ab8b7e91f03b6c2b8c3336d0937)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2516e95f01b70d41edbe694b681e8c77b0666e5332e8780d450866a2aec36f1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDataSourceMixinProps:
        return typing.cast(CfnDataSourceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnDataSourcePropsMixin.DataSourceConfigurationInputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "glue_run_configuration": "glueRunConfiguration",
            "redshift_run_configuration": "redshiftRunConfiguration",
            "sage_maker_run_configuration": "sageMakerRunConfiguration",
        },
    )
    class DataSourceConfigurationInputProperty:
        def __init__(
            self,
            *,
            glue_run_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.GlueRunConfigurationInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            redshift_run_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.RedshiftRunConfigurationInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sage_maker_run_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.SageMakerRunConfigurationInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The configuration of the data source.

            :param glue_run_configuration: The configuration of the AWS Glue data source.
            :param redshift_run_configuration: The configuration of the Amazon Redshift data source.
            :param sage_maker_run_configuration: The configuration details of the Amazon SageMaker data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-datasource-datasourceconfigurationinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                data_source_configuration_input_property = datazone_mixins.CfnDataSourcePropsMixin.DataSourceConfigurationInputProperty(
                    glue_run_configuration=datazone_mixins.CfnDataSourcePropsMixin.GlueRunConfigurationInputProperty(
                        auto_import_data_quality_result=False,
                        catalog_name="catalogName",
                        data_access_role="dataAccessRole",
                        relational_filter_configurations=[datazone_mixins.CfnDataSourcePropsMixin.RelationalFilterConfigurationProperty(
                            database_name="databaseName",
                            filter_expressions=[datazone_mixins.CfnDataSourcePropsMixin.FilterExpressionProperty(
                                expression="expression",
                                type="type"
                            )],
                            schema_name="schemaName"
                        )]
                    ),
                    redshift_run_configuration=datazone_mixins.CfnDataSourcePropsMixin.RedshiftRunConfigurationInputProperty(
                        data_access_role="dataAccessRole",
                        redshift_credential_configuration=datazone_mixins.CfnDataSourcePropsMixin.RedshiftCredentialConfigurationProperty(
                            secret_manager_arn="secretManagerArn"
                        ),
                        redshift_storage=datazone_mixins.CfnDataSourcePropsMixin.RedshiftStorageProperty(
                            redshift_cluster_source=datazone_mixins.CfnDataSourcePropsMixin.RedshiftClusterStorageProperty(
                                cluster_name="clusterName"
                            ),
                            redshift_serverless_source=datazone_mixins.CfnDataSourcePropsMixin.RedshiftServerlessStorageProperty(
                                workgroup_name="workgroupName"
                            )
                        ),
                        relational_filter_configurations=[datazone_mixins.CfnDataSourcePropsMixin.RelationalFilterConfigurationProperty(
                            database_name="databaseName",
                            filter_expressions=[datazone_mixins.CfnDataSourcePropsMixin.FilterExpressionProperty(
                                expression="expression",
                                type="type"
                            )],
                            schema_name="schemaName"
                        )]
                    ),
                    sage_maker_run_configuration=datazone_mixins.CfnDataSourcePropsMixin.SageMakerRunConfigurationInputProperty(
                        tracking_assets={
                            "tracking_assets_key": ["trackingAssets"]
                        }
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6d068d3193f450095760cd2d2e1db7907b188e5c969a373167f12d64246aa561)
                check_type(argname="argument glue_run_configuration", value=glue_run_configuration, expected_type=type_hints["glue_run_configuration"])
                check_type(argname="argument redshift_run_configuration", value=redshift_run_configuration, expected_type=type_hints["redshift_run_configuration"])
                check_type(argname="argument sage_maker_run_configuration", value=sage_maker_run_configuration, expected_type=type_hints["sage_maker_run_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if glue_run_configuration is not None:
                self._values["glue_run_configuration"] = glue_run_configuration
            if redshift_run_configuration is not None:
                self._values["redshift_run_configuration"] = redshift_run_configuration
            if sage_maker_run_configuration is not None:
                self._values["sage_maker_run_configuration"] = sage_maker_run_configuration

        @builtins.property
        def glue_run_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.GlueRunConfigurationInputProperty"]]:
            '''The configuration of the AWS Glue data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-datasource-datasourceconfigurationinput.html#cfn-datazone-datasource-datasourceconfigurationinput-gluerunconfiguration
            '''
            result = self._values.get("glue_run_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.GlueRunConfigurationInputProperty"]], result)

        @builtins.property
        def redshift_run_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.RedshiftRunConfigurationInputProperty"]]:
            '''The configuration of the Amazon Redshift data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-datasource-datasourceconfigurationinput.html#cfn-datazone-datasource-datasourceconfigurationinput-redshiftrunconfiguration
            '''
            result = self._values.get("redshift_run_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.RedshiftRunConfigurationInputProperty"]], result)

        @builtins.property
        def sage_maker_run_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.SageMakerRunConfigurationInputProperty"]]:
            '''The configuration details of the Amazon SageMaker data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-datasource-datasourceconfigurationinput.html#cfn-datazone-datasource-datasourceconfigurationinput-sagemakerrunconfiguration
            '''
            result = self._values.get("sage_maker_run_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.SageMakerRunConfigurationInputProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataSourceConfigurationInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnDataSourcePropsMixin.FilterExpressionProperty",
        jsii_struct_bases=[],
        name_mapping={"expression": "expression", "type": "type"},
    )
    class FilterExpressionProperty:
        def __init__(
            self,
            *,
            expression: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A filter expression in Amazon DataZone.

            :param expression: The search filter expression.
            :param type: The search filter explresison type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-datasource-filterexpression.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                filter_expression_property = datazone_mixins.CfnDataSourcePropsMixin.FilterExpressionProperty(
                    expression="expression",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0d7ed4fb955bc5269367dee7e8ae3f366c9f372cd3a09a145c70929ff001fd0d)
                check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if expression is not None:
                self._values["expression"] = expression
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def expression(self) -> typing.Optional[builtins.str]:
            '''The search filter expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-datasource-filterexpression.html#cfn-datazone-datasource-filterexpression-expression
            '''
            result = self._values.get("expression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The search filter explresison type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-datasource-filterexpression.html#cfn-datazone-datasource-filterexpression-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FilterExpressionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnDataSourcePropsMixin.FormInputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "content": "content",
            "form_name": "formName",
            "type_identifier": "typeIdentifier",
            "type_revision": "typeRevision",
        },
    )
    class FormInputProperty:
        def __init__(
            self,
            *,
            content: typing.Optional[builtins.str] = None,
            form_name: typing.Optional[builtins.str] = None,
            type_identifier: typing.Optional[builtins.str] = None,
            type_revision: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The details of a metadata form.

            :param content: The content of the metadata form.
            :param form_name: The name of the metadata form.
            :param type_identifier: The ID of the metadata form type.
            :param type_revision: The revision of the metadata form type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-datasource-forminput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                form_input_property = datazone_mixins.CfnDataSourcePropsMixin.FormInputProperty(
                    content="content",
                    form_name="formName",
                    type_identifier="typeIdentifier",
                    type_revision="typeRevision"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__36cacacb64745d07552baaec7ebf0c9af44fb4b410bb116c89eb9e6ebae40560)
                check_type(argname="argument content", value=content, expected_type=type_hints["content"])
                check_type(argname="argument form_name", value=form_name, expected_type=type_hints["form_name"])
                check_type(argname="argument type_identifier", value=type_identifier, expected_type=type_hints["type_identifier"])
                check_type(argname="argument type_revision", value=type_revision, expected_type=type_hints["type_revision"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if content is not None:
                self._values["content"] = content
            if form_name is not None:
                self._values["form_name"] = form_name
            if type_identifier is not None:
                self._values["type_identifier"] = type_identifier
            if type_revision is not None:
                self._values["type_revision"] = type_revision

        @builtins.property
        def content(self) -> typing.Optional[builtins.str]:
            '''The content of the metadata form.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-datasource-forminput.html#cfn-datazone-datasource-forminput-content
            '''
            result = self._values.get("content")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def form_name(self) -> typing.Optional[builtins.str]:
            '''The name of the metadata form.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-datasource-forminput.html#cfn-datazone-datasource-forminput-formname
            '''
            result = self._values.get("form_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type_identifier(self) -> typing.Optional[builtins.str]:
            '''The ID of the metadata form type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-datasource-forminput.html#cfn-datazone-datasource-forminput-typeidentifier
            '''
            result = self._values.get("type_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type_revision(self) -> typing.Optional[builtins.str]:
            '''The revision of the metadata form type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-datasource-forminput.html#cfn-datazone-datasource-forminput-typerevision
            '''
            result = self._values.get("type_revision")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FormInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnDataSourcePropsMixin.GlueRunConfigurationInputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "auto_import_data_quality_result": "autoImportDataQualityResult",
            "catalog_name": "catalogName",
            "data_access_role": "dataAccessRole",
            "relational_filter_configurations": "relationalFilterConfigurations",
        },
    )
    class GlueRunConfigurationInputProperty:
        def __init__(
            self,
            *,
            auto_import_data_quality_result: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            catalog_name: typing.Optional[builtins.str] = None,
            data_access_role: typing.Optional[builtins.str] = None,
            relational_filter_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.RelationalFilterConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The configuration details of the AWS Glue data source.

            :param auto_import_data_quality_result: Specifies whether to automatically import data quality metrics as part of the data source run.
            :param catalog_name: The catalog name in the AWS Glue run configuration.
            :param data_access_role: The data access role included in the configuration details of the AWS Glue data source.
            :param relational_filter_configurations: The relational filter configurations included in the configuration details of the AWS Glue data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-datasource-gluerunconfigurationinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                glue_run_configuration_input_property = datazone_mixins.CfnDataSourcePropsMixin.GlueRunConfigurationInputProperty(
                    auto_import_data_quality_result=False,
                    catalog_name="catalogName",
                    data_access_role="dataAccessRole",
                    relational_filter_configurations=[datazone_mixins.CfnDataSourcePropsMixin.RelationalFilterConfigurationProperty(
                        database_name="databaseName",
                        filter_expressions=[datazone_mixins.CfnDataSourcePropsMixin.FilterExpressionProperty(
                            expression="expression",
                            type="type"
                        )],
                        schema_name="schemaName"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2f2dc4471ff38c3517b8c2fd9ce406b406c3f84a0444bdbd0d580829f3f508d9)
                check_type(argname="argument auto_import_data_quality_result", value=auto_import_data_quality_result, expected_type=type_hints["auto_import_data_quality_result"])
                check_type(argname="argument catalog_name", value=catalog_name, expected_type=type_hints["catalog_name"])
                check_type(argname="argument data_access_role", value=data_access_role, expected_type=type_hints["data_access_role"])
                check_type(argname="argument relational_filter_configurations", value=relational_filter_configurations, expected_type=type_hints["relational_filter_configurations"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auto_import_data_quality_result is not None:
                self._values["auto_import_data_quality_result"] = auto_import_data_quality_result
            if catalog_name is not None:
                self._values["catalog_name"] = catalog_name
            if data_access_role is not None:
                self._values["data_access_role"] = data_access_role
            if relational_filter_configurations is not None:
                self._values["relational_filter_configurations"] = relational_filter_configurations

        @builtins.property
        def auto_import_data_quality_result(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether to automatically import data quality metrics as part of the data source run.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-datasource-gluerunconfigurationinput.html#cfn-datazone-datasource-gluerunconfigurationinput-autoimportdataqualityresult
            '''
            result = self._values.get("auto_import_data_quality_result")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def catalog_name(self) -> typing.Optional[builtins.str]:
            '''The catalog name in the AWS Glue run configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-datasource-gluerunconfigurationinput.html#cfn-datazone-datasource-gluerunconfigurationinput-catalogname
            '''
            result = self._values.get("catalog_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def data_access_role(self) -> typing.Optional[builtins.str]:
            '''The data access role included in the configuration details of the AWS Glue data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-datasource-gluerunconfigurationinput.html#cfn-datazone-datasource-gluerunconfigurationinput-dataaccessrole
            '''
            result = self._values.get("data_access_role")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def relational_filter_configurations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.RelationalFilterConfigurationProperty"]]]]:
            '''The relational filter configurations included in the configuration details of the AWS Glue data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-datasource-gluerunconfigurationinput.html#cfn-datazone-datasource-gluerunconfigurationinput-relationalfilterconfigurations
            '''
            result = self._values.get("relational_filter_configurations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.RelationalFilterConfigurationProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GlueRunConfigurationInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnDataSourcePropsMixin.RecommendationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enable_business_name_generation": "enableBusinessNameGeneration",
        },
    )
    class RecommendationConfigurationProperty:
        def __init__(
            self,
            *,
            enable_business_name_generation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The recommendation configuration for the data source.

            :param enable_business_name_generation: Specifies whether automatic business name generation is to be enabled or not as part of the recommendation configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-datasource-recommendationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                recommendation_configuration_property = datazone_mixins.CfnDataSourcePropsMixin.RecommendationConfigurationProperty(
                    enable_business_name_generation=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__660b6f84a16d272ee0b393c89f082a615fce2dd386f9e9f95a76e4720ce38906)
                check_type(argname="argument enable_business_name_generation", value=enable_business_name_generation, expected_type=type_hints["enable_business_name_generation"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enable_business_name_generation is not None:
                self._values["enable_business_name_generation"] = enable_business_name_generation

        @builtins.property
        def enable_business_name_generation(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether automatic business name generation is to be enabled or not as part of the recommendation configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-datasource-recommendationconfiguration.html#cfn-datazone-datasource-recommendationconfiguration-enablebusinessnamegeneration
            '''
            result = self._values.get("enable_business_name_generation")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RecommendationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnDataSourcePropsMixin.RedshiftClusterStorageProperty",
        jsii_struct_bases=[],
        name_mapping={"cluster_name": "clusterName"},
    )
    class RedshiftClusterStorageProperty:
        def __init__(
            self,
            *,
            cluster_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The details of the Amazon Redshift cluster storage.

            :param cluster_name: The name of an Amazon Redshift cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-datasource-redshiftclusterstorage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                redshift_cluster_storage_property = datazone_mixins.CfnDataSourcePropsMixin.RedshiftClusterStorageProperty(
                    cluster_name="clusterName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__59f2b0359caf418664272b43652cde32e11bf9aa52a3f27183f8eb574fa31d7e)
                check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cluster_name is not None:
                self._values["cluster_name"] = cluster_name

        @builtins.property
        def cluster_name(self) -> typing.Optional[builtins.str]:
            '''The name of an Amazon Redshift cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-datasource-redshiftclusterstorage.html#cfn-datazone-datasource-redshiftclusterstorage-clustername
            '''
            result = self._values.get("cluster_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RedshiftClusterStorageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnDataSourcePropsMixin.RedshiftCredentialConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"secret_manager_arn": "secretManagerArn"},
    )
    class RedshiftCredentialConfigurationProperty:
        def __init__(
            self,
            *,
            secret_manager_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The details of the credentials required to access an Amazon Redshift cluster.

            :param secret_manager_arn: The ARN of a secret manager for an Amazon Redshift cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-datasource-redshiftcredentialconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                redshift_credential_configuration_property = datazone_mixins.CfnDataSourcePropsMixin.RedshiftCredentialConfigurationProperty(
                    secret_manager_arn="secretManagerArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e9dd81037daeed32cd4d31da001af5dbc17f4900f62578371138b8677ed8f48d)
                check_type(argname="argument secret_manager_arn", value=secret_manager_arn, expected_type=type_hints["secret_manager_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if secret_manager_arn is not None:
                self._values["secret_manager_arn"] = secret_manager_arn

        @builtins.property
        def secret_manager_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of a secret manager for an Amazon Redshift cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-datasource-redshiftcredentialconfiguration.html#cfn-datazone-datasource-redshiftcredentialconfiguration-secretmanagerarn
            '''
            result = self._values.get("secret_manager_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RedshiftCredentialConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnDataSourcePropsMixin.RedshiftRunConfigurationInputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_access_role": "dataAccessRole",
            "redshift_credential_configuration": "redshiftCredentialConfiguration",
            "redshift_storage": "redshiftStorage",
            "relational_filter_configurations": "relationalFilterConfigurations",
        },
    )
    class RedshiftRunConfigurationInputProperty:
        def __init__(
            self,
            *,
            data_access_role: typing.Optional[builtins.str] = None,
            redshift_credential_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.RedshiftCredentialConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            redshift_storage: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.RedshiftStorageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            relational_filter_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.RelationalFilterConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The relational filter configurations included in the configuration details of the Amazon Redshift data source.

            :param data_access_role: The data access role included in the configuration details of the Amazon Redshift data source.
            :param redshift_credential_configuration: The details of the credentials required to access an Amazon Redshift cluster.
            :param redshift_storage: The details of the Amazon Redshift storage as part of the configuration of an Amazon Redshift data source run.
            :param relational_filter_configurations: The relational filter configurations included in the configuration details of the AWS Glue data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-datasource-redshiftrunconfigurationinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                redshift_run_configuration_input_property = datazone_mixins.CfnDataSourcePropsMixin.RedshiftRunConfigurationInputProperty(
                    data_access_role="dataAccessRole",
                    redshift_credential_configuration=datazone_mixins.CfnDataSourcePropsMixin.RedshiftCredentialConfigurationProperty(
                        secret_manager_arn="secretManagerArn"
                    ),
                    redshift_storage=datazone_mixins.CfnDataSourcePropsMixin.RedshiftStorageProperty(
                        redshift_cluster_source=datazone_mixins.CfnDataSourcePropsMixin.RedshiftClusterStorageProperty(
                            cluster_name="clusterName"
                        ),
                        redshift_serverless_source=datazone_mixins.CfnDataSourcePropsMixin.RedshiftServerlessStorageProperty(
                            workgroup_name="workgroupName"
                        )
                    ),
                    relational_filter_configurations=[datazone_mixins.CfnDataSourcePropsMixin.RelationalFilterConfigurationProperty(
                        database_name="databaseName",
                        filter_expressions=[datazone_mixins.CfnDataSourcePropsMixin.FilterExpressionProperty(
                            expression="expression",
                            type="type"
                        )],
                        schema_name="schemaName"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5f4ebaa25226101e239c7e0bfcc7cbfd5f5639816ffb257a325ff4dc3f49160c)
                check_type(argname="argument data_access_role", value=data_access_role, expected_type=type_hints["data_access_role"])
                check_type(argname="argument redshift_credential_configuration", value=redshift_credential_configuration, expected_type=type_hints["redshift_credential_configuration"])
                check_type(argname="argument redshift_storage", value=redshift_storage, expected_type=type_hints["redshift_storage"])
                check_type(argname="argument relational_filter_configurations", value=relational_filter_configurations, expected_type=type_hints["relational_filter_configurations"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data_access_role is not None:
                self._values["data_access_role"] = data_access_role
            if redshift_credential_configuration is not None:
                self._values["redshift_credential_configuration"] = redshift_credential_configuration
            if redshift_storage is not None:
                self._values["redshift_storage"] = redshift_storage
            if relational_filter_configurations is not None:
                self._values["relational_filter_configurations"] = relational_filter_configurations

        @builtins.property
        def data_access_role(self) -> typing.Optional[builtins.str]:
            '''The data access role included in the configuration details of the Amazon Redshift data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-datasource-redshiftrunconfigurationinput.html#cfn-datazone-datasource-redshiftrunconfigurationinput-dataaccessrole
            '''
            result = self._values.get("data_access_role")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def redshift_credential_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.RedshiftCredentialConfigurationProperty"]]:
            '''The details of the credentials required to access an Amazon Redshift cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-datasource-redshiftrunconfigurationinput.html#cfn-datazone-datasource-redshiftrunconfigurationinput-redshiftcredentialconfiguration
            '''
            result = self._values.get("redshift_credential_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.RedshiftCredentialConfigurationProperty"]], result)

        @builtins.property
        def redshift_storage(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.RedshiftStorageProperty"]]:
            '''The details of the Amazon Redshift storage as part of the configuration of an Amazon Redshift data source run.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-datasource-redshiftrunconfigurationinput.html#cfn-datazone-datasource-redshiftrunconfigurationinput-redshiftstorage
            '''
            result = self._values.get("redshift_storage")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.RedshiftStorageProperty"]], result)

        @builtins.property
        def relational_filter_configurations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.RelationalFilterConfigurationProperty"]]]]:
            '''The relational filter configurations included in the configuration details of the AWS Glue data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-datasource-redshiftrunconfigurationinput.html#cfn-datazone-datasource-redshiftrunconfigurationinput-relationalfilterconfigurations
            '''
            result = self._values.get("relational_filter_configurations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.RelationalFilterConfigurationProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RedshiftRunConfigurationInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnDataSourcePropsMixin.RedshiftServerlessStorageProperty",
        jsii_struct_bases=[],
        name_mapping={"workgroup_name": "workgroupName"},
    )
    class RedshiftServerlessStorageProperty:
        def __init__(
            self,
            *,
            workgroup_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The details of the Amazon Redshift Serverless workgroup storage.

            :param workgroup_name: The name of the Amazon Redshift Serverless workgroup.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-datasource-redshiftserverlessstorage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                redshift_serverless_storage_property = datazone_mixins.CfnDataSourcePropsMixin.RedshiftServerlessStorageProperty(
                    workgroup_name="workgroupName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bd36f268182471efa7ddd5df4fd3c87a2895bcf6c77b4315914ef73365bf9206)
                check_type(argname="argument workgroup_name", value=workgroup_name, expected_type=type_hints["workgroup_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if workgroup_name is not None:
                self._values["workgroup_name"] = workgroup_name

        @builtins.property
        def workgroup_name(self) -> typing.Optional[builtins.str]:
            '''The name of the Amazon Redshift Serverless workgroup.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-datasource-redshiftserverlessstorage.html#cfn-datazone-datasource-redshiftserverlessstorage-workgroupname
            '''
            result = self._values.get("workgroup_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RedshiftServerlessStorageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnDataSourcePropsMixin.RedshiftStorageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "redshift_cluster_source": "redshiftClusterSource",
            "redshift_serverless_source": "redshiftServerlessSource",
        },
    )
    class RedshiftStorageProperty:
        def __init__(
            self,
            *,
            redshift_cluster_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.RedshiftClusterStorageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            redshift_serverless_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.RedshiftServerlessStorageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The details of the Amazon Redshift storage as part of the configuration of an Amazon Redshift data source run.

            :param redshift_cluster_source: The details of the Amazon Redshift cluster source.
            :param redshift_serverless_source: The details of the Amazon Redshift Serverless workgroup source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-datasource-redshiftstorage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                redshift_storage_property = datazone_mixins.CfnDataSourcePropsMixin.RedshiftStorageProperty(
                    redshift_cluster_source=datazone_mixins.CfnDataSourcePropsMixin.RedshiftClusterStorageProperty(
                        cluster_name="clusterName"
                    ),
                    redshift_serverless_source=datazone_mixins.CfnDataSourcePropsMixin.RedshiftServerlessStorageProperty(
                        workgroup_name="workgroupName"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__caaae179ea54cd864186f703b8b80af9ba3d031e35818087c1842f796e35d622)
                check_type(argname="argument redshift_cluster_source", value=redshift_cluster_source, expected_type=type_hints["redshift_cluster_source"])
                check_type(argname="argument redshift_serverless_source", value=redshift_serverless_source, expected_type=type_hints["redshift_serverless_source"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if redshift_cluster_source is not None:
                self._values["redshift_cluster_source"] = redshift_cluster_source
            if redshift_serverless_source is not None:
                self._values["redshift_serverless_source"] = redshift_serverless_source

        @builtins.property
        def redshift_cluster_source(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.RedshiftClusterStorageProperty"]]:
            '''The details of the Amazon Redshift cluster source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-datasource-redshiftstorage.html#cfn-datazone-datasource-redshiftstorage-redshiftclustersource
            '''
            result = self._values.get("redshift_cluster_source")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.RedshiftClusterStorageProperty"]], result)

        @builtins.property
        def redshift_serverless_source(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.RedshiftServerlessStorageProperty"]]:
            '''The details of the Amazon Redshift Serverless workgroup source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-datasource-redshiftstorage.html#cfn-datazone-datasource-redshiftstorage-redshiftserverlesssource
            '''
            result = self._values.get("redshift_serverless_source")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.RedshiftServerlessStorageProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RedshiftStorageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnDataSourcePropsMixin.RelationalFilterConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "database_name": "databaseName",
            "filter_expressions": "filterExpressions",
            "schema_name": "schemaName",
        },
    )
    class RelationalFilterConfigurationProperty:
        def __init__(
            self,
            *,
            database_name: typing.Optional[builtins.str] = None,
            filter_expressions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.FilterExpressionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            schema_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The relational filter configuration for the data source.

            :param database_name: The database name specified in the relational filter configuration for the data source.
            :param filter_expressions: The filter expressions specified in the relational filter configuration for the data source.
            :param schema_name: The schema name specified in the relational filter configuration for the data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-datasource-relationalfilterconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                relational_filter_configuration_property = datazone_mixins.CfnDataSourcePropsMixin.RelationalFilterConfigurationProperty(
                    database_name="databaseName",
                    filter_expressions=[datazone_mixins.CfnDataSourcePropsMixin.FilterExpressionProperty(
                        expression="expression",
                        type="type"
                    )],
                    schema_name="schemaName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c9326e933183228790b23db2ea9a56713b28613ec1a70fc284ce305ad84447df)
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument filter_expressions", value=filter_expressions, expected_type=type_hints["filter_expressions"])
                check_type(argname="argument schema_name", value=schema_name, expected_type=type_hints["schema_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if database_name is not None:
                self._values["database_name"] = database_name
            if filter_expressions is not None:
                self._values["filter_expressions"] = filter_expressions
            if schema_name is not None:
                self._values["schema_name"] = schema_name

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            '''The database name specified in the relational filter configuration for the data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-datasource-relationalfilterconfiguration.html#cfn-datazone-datasource-relationalfilterconfiguration-databasename
            '''
            result = self._values.get("database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def filter_expressions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.FilterExpressionProperty"]]]]:
            '''The filter expressions specified in the relational filter configuration for the data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-datasource-relationalfilterconfiguration.html#cfn-datazone-datasource-relationalfilterconfiguration-filterexpressions
            '''
            result = self._values.get("filter_expressions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.FilterExpressionProperty"]]]], result)

        @builtins.property
        def schema_name(self) -> typing.Optional[builtins.str]:
            '''The schema name specified in the relational filter configuration for the data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-datasource-relationalfilterconfiguration.html#cfn-datazone-datasource-relationalfilterconfiguration-schemaname
            '''
            result = self._values.get("schema_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RelationalFilterConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnDataSourcePropsMixin.SageMakerRunConfigurationInputProperty",
        jsii_struct_bases=[],
        name_mapping={"tracking_assets": "trackingAssets"},
    )
    class SageMakerRunConfigurationInputProperty:
        def __init__(
            self,
            *,
            tracking_assets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Sequence[builtins.str]]]] = None,
        ) -> None:
            '''The configuration details of the Amazon SageMaker data source.

            :param tracking_assets: The tracking assets of the Amazon SageMaker run.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-datasource-sagemakerrunconfigurationinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                sage_maker_run_configuration_input_property = datazone_mixins.CfnDataSourcePropsMixin.SageMakerRunConfigurationInputProperty(
                    tracking_assets={
                        "tracking_assets_key": ["trackingAssets"]
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__903a03288a74a71d337e91fc80c82f8456a7bdc2460fb985267b158d74d99fae)
                check_type(argname="argument tracking_assets", value=tracking_assets, expected_type=type_hints["tracking_assets"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if tracking_assets is not None:
                self._values["tracking_assets"] = tracking_assets

        @builtins.property
        def tracking_assets(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.List[builtins.str]]]]:
            '''The tracking assets of the Amazon SageMaker run.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-datasource-sagemakerrunconfigurationinput.html#cfn-datazone-datasource-sagemakerrunconfigurationinput-trackingassets
            '''
            result = self._values.get("tracking_assets")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.List[builtins.str]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SageMakerRunConfigurationInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnDataSourcePropsMixin.ScheduleConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"schedule": "schedule", "timezone": "timezone"},
    )
    class ScheduleConfigurationProperty:
        def __init__(
            self,
            *,
            schedule: typing.Optional[builtins.str] = None,
            timezone: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The details of the schedule of the data source runs.

            :param schedule: The schedule of the data source runs.
            :param timezone: The timezone of the data source run.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-datasource-scheduleconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                schedule_configuration_property = datazone_mixins.CfnDataSourcePropsMixin.ScheduleConfigurationProperty(
                    schedule="schedule",
                    timezone="timezone"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8e928c10522fb42f71b1d428fce5f0d9884cabe8eca6726a6f7b9f78ef59b869)
                check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
                check_type(argname="argument timezone", value=timezone, expected_type=type_hints["timezone"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if schedule is not None:
                self._values["schedule"] = schedule
            if timezone is not None:
                self._values["timezone"] = timezone

        @builtins.property
        def schedule(self) -> typing.Optional[builtins.str]:
            '''The schedule of the data source runs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-datasource-scheduleconfiguration.html#cfn-datazone-datasource-scheduleconfiguration-schedule
            '''
            result = self._values.get("schedule")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def timezone(self) -> typing.Optional[builtins.str]:
            '''The timezone of the data source run.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-datasource-scheduleconfiguration.html#cfn-datazone-datasource-scheduleconfiguration-timezone
            '''
            result = self._values.get("timezone")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScheduleConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnDomainMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "domain_execution_role": "domainExecutionRole",
        "domain_version": "domainVersion",
        "kms_key_identifier": "kmsKeyIdentifier",
        "name": "name",
        "service_role": "serviceRole",
        "single_sign_on": "singleSignOn",
        "tags": "tags",
    },
)
class CfnDomainMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        domain_execution_role: typing.Optional[builtins.str] = None,
        domain_version: typing.Optional[builtins.str] = None,
        kms_key_identifier: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        service_role: typing.Optional[builtins.str] = None,
        single_sign_on: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainPropsMixin.SingleSignOnProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDomainPropsMixin.

        :param description: The description of the Amazon DataZone domain.
        :param domain_execution_role: The domain execution role that is created when an Amazon DataZone domain is created. The domain execution role is created in the AWS account that houses the Amazon DataZone domain.
        :param domain_version: The domain version.
        :param kms_key_identifier: The identifier of the AWS Key Management Service (KMS) key that is used to encrypt the Amazon DataZone domain, metadata, and reporting data.
        :param name: The name of the Amazon DataZone domain.
        :param service_role: The service role of the domain.
        :param single_sign_on: The single sign-on details in Amazon DataZone.
        :param tags: The tags specified for the Amazon DataZone domain.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-domain.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
            
            cfn_domain_mixin_props = datazone_mixins.CfnDomainMixinProps(
                description="description",
                domain_execution_role="domainExecutionRole",
                domain_version="domainVersion",
                kms_key_identifier="kmsKeyIdentifier",
                name="name",
                service_role="serviceRole",
                single_sign_on=datazone_mixins.CfnDomainPropsMixin.SingleSignOnProperty(
                    idc_instance_arn="idcInstanceArn",
                    type="type",
                    user_assignment="userAssignment"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cc9c5a29897c93bd2f95061787b9e33629fdabb4f1d55f1090b594465c309d7)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument domain_execution_role", value=domain_execution_role, expected_type=type_hints["domain_execution_role"])
            check_type(argname="argument domain_version", value=domain_version, expected_type=type_hints["domain_version"])
            check_type(argname="argument kms_key_identifier", value=kms_key_identifier, expected_type=type_hints["kms_key_identifier"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument service_role", value=service_role, expected_type=type_hints["service_role"])
            check_type(argname="argument single_sign_on", value=single_sign_on, expected_type=type_hints["single_sign_on"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if domain_execution_role is not None:
            self._values["domain_execution_role"] = domain_execution_role
        if domain_version is not None:
            self._values["domain_version"] = domain_version
        if kms_key_identifier is not None:
            self._values["kms_key_identifier"] = kms_key_identifier
        if name is not None:
            self._values["name"] = name
        if service_role is not None:
            self._values["service_role"] = service_role
        if single_sign_on is not None:
            self._values["single_sign_on"] = single_sign_on
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the Amazon DataZone domain.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-domain.html#cfn-datazone-domain-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_execution_role(self) -> typing.Optional[builtins.str]:
        '''The domain execution role that is created when an Amazon DataZone domain is created.

        The domain execution role is created in the AWS account that houses the Amazon DataZone domain.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-domain.html#cfn-datazone-domain-domainexecutionrole
        '''
        result = self._values.get("domain_execution_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_version(self) -> typing.Optional[builtins.str]:
        '''The domain version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-domain.html#cfn-datazone-domain-domainversion
        '''
        result = self._values.get("domain_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_identifier(self) -> typing.Optional[builtins.str]:
        '''The identifier of the AWS Key Management Service (KMS) key that is used to encrypt the Amazon DataZone domain, metadata, and reporting data.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-domain.html#cfn-datazone-domain-kmskeyidentifier
        '''
        result = self._values.get("kms_key_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the Amazon DataZone domain.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-domain.html#cfn-datazone-domain-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_role(self) -> typing.Optional[builtins.str]:
        '''The service role of the domain.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-domain.html#cfn-datazone-domain-servicerole
        '''
        result = self._values.get("service_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def single_sign_on(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.SingleSignOnProperty"]]:
        '''The single sign-on details in Amazon DataZone.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-domain.html#cfn-datazone-domain-singlesignon
        '''
        result = self._values.get("single_sign_on")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.SingleSignOnProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags specified for the Amazon DataZone domain.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-domain.html#cfn-datazone-domain-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDomainMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDomainPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnDomainPropsMixin",
):
    '''The ``AWS::DataZone::Domain`` resource specifies an Amazon DataZone domain.

    You can use domains to organize your assets, users, and their projects.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-domain.html
    :cloudformationResource: AWS::DataZone::Domain
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
        
        cfn_domain_props_mixin = datazone_mixins.CfnDomainPropsMixin(datazone_mixins.CfnDomainMixinProps(
            description="description",
            domain_execution_role="domainExecutionRole",
            domain_version="domainVersion",
            kms_key_identifier="kmsKeyIdentifier",
            name="name",
            service_role="serviceRole",
            single_sign_on=datazone_mixins.CfnDomainPropsMixin.SingleSignOnProperty(
                idc_instance_arn="idcInstanceArn",
                type="type",
                user_assignment="userAssignment"
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
        props: typing.Union[CfnDomainMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DataZone::Domain``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0231c16af25ae96a053012b837e6619e179351c0f45276e60e55065358d2f032)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2af63ed70682396625d248e3d29a13134618b14332247c449333e5c095cbeee)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9d79413c927fc5f0db1efaa96bfc3a86b1e4bf98836908729953c8b0da603c3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDomainMixinProps:
        return typing.cast(CfnDomainMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnDomainPropsMixin.SingleSignOnProperty",
        jsii_struct_bases=[],
        name_mapping={
            "idc_instance_arn": "idcInstanceArn",
            "type": "type",
            "user_assignment": "userAssignment",
        },
    )
    class SingleSignOnProperty:
        def __init__(
            self,
            *,
            idc_instance_arn: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
            user_assignment: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The single sign-on details in Amazon DataZone.

            :param idc_instance_arn: The ARN of the IDC instance.
            :param type: The type of single sign-on in Amazon DataZone.
            :param user_assignment: The single sign-on user assignment in Amazon DataZone.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-domain-singlesignon.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                single_sign_on_property = datazone_mixins.CfnDomainPropsMixin.SingleSignOnProperty(
                    idc_instance_arn="idcInstanceArn",
                    type="type",
                    user_assignment="userAssignment"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b1cf7f62bb1eefcfe6cc0eee73e2a3c27a41680fcc61e045debe2ae61a8fa292)
                check_type(argname="argument idc_instance_arn", value=idc_instance_arn, expected_type=type_hints["idc_instance_arn"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument user_assignment", value=user_assignment, expected_type=type_hints["user_assignment"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if idc_instance_arn is not None:
                self._values["idc_instance_arn"] = idc_instance_arn
            if type is not None:
                self._values["type"] = type
            if user_assignment is not None:
                self._values["user_assignment"] = user_assignment

        @builtins.property
        def idc_instance_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the IDC instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-domain-singlesignon.html#cfn-datazone-domain-singlesignon-idcinstancearn
            '''
            result = self._values.get("idc_instance_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of single sign-on in Amazon DataZone.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-domain-singlesignon.html#cfn-datazone-domain-singlesignon-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user_assignment(self) -> typing.Optional[builtins.str]:
            '''The single sign-on user assignment in Amazon DataZone.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-domain-singlesignon.html#cfn-datazone-domain-singlesignon-userassignment
            '''
            result = self._values.get("user_assignment")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SingleSignOnProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnDomainUnitMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "domain_identifier": "domainIdentifier",
        "name": "name",
        "parent_domain_unit_identifier": "parentDomainUnitIdentifier",
    },
)
class CfnDomainUnitMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        domain_identifier: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        parent_domain_unit_identifier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnDomainUnitPropsMixin.

        :param description: The description of the domain unit.
        :param domain_identifier: The ID of the domain where you want to crate a domain unit.
        :param name: The name of the domain unit.
        :param parent_domain_unit_identifier: The ID of the parent domain unit.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-domainunit.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
            
            cfn_domain_unit_mixin_props = datazone_mixins.CfnDomainUnitMixinProps(
                description="description",
                domain_identifier="domainIdentifier",
                name="name",
                parent_domain_unit_identifier="parentDomainUnitIdentifier"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb6dadf30b844c2e40ac1d02ed42e9b411c76cfc7d75ee43b0a91c7b303560ac)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument domain_identifier", value=domain_identifier, expected_type=type_hints["domain_identifier"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument parent_domain_unit_identifier", value=parent_domain_unit_identifier, expected_type=type_hints["parent_domain_unit_identifier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if domain_identifier is not None:
            self._values["domain_identifier"] = domain_identifier
        if name is not None:
            self._values["name"] = name
        if parent_domain_unit_identifier is not None:
            self._values["parent_domain_unit_identifier"] = parent_domain_unit_identifier

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the domain unit.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-domainunit.html#cfn-datazone-domainunit-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_identifier(self) -> typing.Optional[builtins.str]:
        '''The ID of the domain where you want to crate a domain unit.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-domainunit.html#cfn-datazone-domainunit-domainidentifier
        '''
        result = self._values.get("domain_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the domain unit.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-domainunit.html#cfn-datazone-domainunit-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parent_domain_unit_identifier(self) -> typing.Optional[builtins.str]:
        '''The ID of the parent domain unit.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-domainunit.html#cfn-datazone-domainunit-parentdomainunitidentifier
        '''
        result = self._values.get("parent_domain_unit_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDomainUnitMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDomainUnitPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnDomainUnitPropsMixin",
):
    '''The summary of the domain unit.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-domainunit.html
    :cloudformationResource: AWS::DataZone::DomainUnit
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
        
        cfn_domain_unit_props_mixin = datazone_mixins.CfnDomainUnitPropsMixin(datazone_mixins.CfnDomainUnitMixinProps(
            description="description",
            domain_identifier="domainIdentifier",
            name="name",
            parent_domain_unit_identifier="parentDomainUnitIdentifier"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDomainUnitMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DataZone::DomainUnit``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1b0d053215edd29e56463a34c3cc3b284f79584fbf81ff9a54c887afbb6c98f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6006f66a1cfd2e13a74ab9052cf8d385365f9202e44ecab1c2ffa2e9193441ab)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3275d5340d618e54500682f053c2634e9648d32ae9d654112666a077f1e6c6e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDomainUnitMixinProps:
        return typing.cast(CfnDomainUnitMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnEnvironmentActionsMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "domain_identifier": "domainIdentifier",
        "environment_identifier": "environmentIdentifier",
        "identifier": "identifier",
        "name": "name",
        "parameters": "parameters",
    },
)
class CfnEnvironmentActionsMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        domain_identifier: typing.Optional[builtins.str] = None,
        environment_identifier: typing.Optional[builtins.str] = None,
        identifier: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEnvironmentActionsPropsMixin.AwsConsoleLinkParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnEnvironmentActionsPropsMixin.

        :param description: The environment action description.
        :param domain_identifier: The Amazon DataZone domain ID of the environment action.
        :param environment_identifier: The environment ID of the environment action.
        :param identifier: The ID of the environment action.
        :param name: The name of the environment action.
        :param parameters: The parameters of the environment action.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environmentactions.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
            
            cfn_environment_actions_mixin_props = datazone_mixins.CfnEnvironmentActionsMixinProps(
                description="description",
                domain_identifier="domainIdentifier",
                environment_identifier="environmentIdentifier",
                identifier="identifier",
                name="name",
                parameters=datazone_mixins.CfnEnvironmentActionsPropsMixin.AwsConsoleLinkParametersProperty(
                    uri="uri"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e532cc5f450965ea79a0d5b035aa33e6b528f46a85cfc52acb0a7385be1eb39)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument domain_identifier", value=domain_identifier, expected_type=type_hints["domain_identifier"])
            check_type(argname="argument environment_identifier", value=environment_identifier, expected_type=type_hints["environment_identifier"])
            check_type(argname="argument identifier", value=identifier, expected_type=type_hints["identifier"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if domain_identifier is not None:
            self._values["domain_identifier"] = domain_identifier
        if environment_identifier is not None:
            self._values["environment_identifier"] = environment_identifier
        if identifier is not None:
            self._values["identifier"] = identifier
        if name is not None:
            self._values["name"] = name
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The environment action description.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environmentactions.html#cfn-datazone-environmentactions-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_identifier(self) -> typing.Optional[builtins.str]:
        '''The Amazon DataZone domain ID of the environment action.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environmentactions.html#cfn-datazone-environmentactions-domainidentifier
        '''
        result = self._values.get("domain_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_identifier(self) -> typing.Optional[builtins.str]:
        '''The environment ID of the environment action.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environmentactions.html#cfn-datazone-environmentactions-environmentidentifier
        '''
        result = self._values.get("environment_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identifier(self) -> typing.Optional[builtins.str]:
        '''The ID of the environment action.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environmentactions.html#cfn-datazone-environmentactions-identifier
        '''
        result = self._values.get("identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the environment action.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environmentactions.html#cfn-datazone-environmentactions-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentActionsPropsMixin.AwsConsoleLinkParametersProperty"]]:
        '''The parameters of the environment action.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environmentactions.html#cfn-datazone-environmentactions-parameters
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentActionsPropsMixin.AwsConsoleLinkParametersProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEnvironmentActionsMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnEnvironmentActionsPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnEnvironmentActionsPropsMixin",
):
    '''The details about the specified action configured for an environment.

    For example, the details of the specified console links for an analytics tool that is available in this environment.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environmentactions.html
    :cloudformationResource: AWS::DataZone::EnvironmentActions
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
        
        cfn_environment_actions_props_mixin = datazone_mixins.CfnEnvironmentActionsPropsMixin(datazone_mixins.CfnEnvironmentActionsMixinProps(
            description="description",
            domain_identifier="domainIdentifier",
            environment_identifier="environmentIdentifier",
            identifier="identifier",
            name="name",
            parameters=datazone_mixins.CfnEnvironmentActionsPropsMixin.AwsConsoleLinkParametersProperty(
                uri="uri"
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnEnvironmentActionsMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DataZone::EnvironmentActions``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d53c0226ca85d454d8eeafa829de114002acf6ff12899af976cd211de7b001dc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__10f03164e3dd3e40bb2ec31913e1652070a7553b722456cda515074a3c7a0eab)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b80b6bdc0e4af03186f3be7f55b096220710d227a6bf1b40c5491181feca710)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnEnvironmentActionsMixinProps:
        return typing.cast(CfnEnvironmentActionsMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnEnvironmentActionsPropsMixin.AwsConsoleLinkParametersProperty",
        jsii_struct_bases=[],
        name_mapping={"uri": "uri"},
    )
    class AwsConsoleLinkParametersProperty:
        def __init__(self, *, uri: typing.Optional[builtins.str] = None) -> None:
            '''The parameters of the console link specified as part of the environment action.

            :param uri: The URI of the console link specified as part of the environment action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-environmentactions-awsconsolelinkparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                aws_console_link_parameters_property = datazone_mixins.CfnEnvironmentActionsPropsMixin.AwsConsoleLinkParametersProperty(
                    uri="uri"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__99aee996bf57858454c8c8e5ca17384b22dc8f7640419c2d2a23d799a8e781ed)
                check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if uri is not None:
                self._values["uri"] = uri

        @builtins.property
        def uri(self) -> typing.Optional[builtins.str]:
            '''The URI of the console link specified as part of the environment action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-environmentactions-awsconsolelinkparameters.html#cfn-datazone-environmentactions-awsconsolelinkparameters-uri
            '''
            result = self._values.get("uri")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AwsConsoleLinkParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnEnvironmentBlueprintConfigurationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "domain_identifier": "domainIdentifier",
        "enabled_regions": "enabledRegions",
        "environment_blueprint_identifier": "environmentBlueprintIdentifier",
        "environment_role_permission_boundary": "environmentRolePermissionBoundary",
        "manage_access_role_arn": "manageAccessRoleArn",
        "provisioning_configurations": "provisioningConfigurations",
        "provisioning_role_arn": "provisioningRoleArn",
        "regional_parameters": "regionalParameters",
    },
)
class CfnEnvironmentBlueprintConfigurationMixinProps:
    def __init__(
        self,
        *,
        domain_identifier: typing.Optional[builtins.str] = None,
        enabled_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        environment_blueprint_identifier: typing.Optional[builtins.str] = None,
        environment_role_permission_boundary: typing.Optional[builtins.str] = None,
        manage_access_role_arn: typing.Optional[builtins.str] = None,
        provisioning_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEnvironmentBlueprintConfigurationPropsMixin.ProvisioningConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        provisioning_role_arn: typing.Optional[builtins.str] = None,
        regional_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEnvironmentBlueprintConfigurationPropsMixin.RegionalParameterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnEnvironmentBlueprintConfigurationPropsMixin.

        :param domain_identifier: The identifier of the Amazon DataZone domain in which an environment blueprint exists.
        :param enabled_regions: The enabled AWS Regions specified in a blueprint configuration.
        :param environment_blueprint_identifier: The identifier of the environment blueprint. In the current release, only the following values are supported: ``DefaultDataLake`` and ``DefaultDataWarehouse`` .
        :param environment_role_permission_boundary: The environment role permission boundary.
        :param manage_access_role_arn: The ARN of the manage access role.
        :param provisioning_configurations: The provisioning configuration of a blueprint.
        :param provisioning_role_arn: The ARN of the provisioning role.
        :param regional_parameters: The regional parameters of the environment blueprint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environmentblueprintconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
            
            cfn_environment_blueprint_configuration_mixin_props = datazone_mixins.CfnEnvironmentBlueprintConfigurationMixinProps(
                domain_identifier="domainIdentifier",
                enabled_regions=["enabledRegions"],
                environment_blueprint_identifier="environmentBlueprintIdentifier",
                environment_role_permission_boundary="environmentRolePermissionBoundary",
                manage_access_role_arn="manageAccessRoleArn",
                provisioning_configurations=[datazone_mixins.CfnEnvironmentBlueprintConfigurationPropsMixin.ProvisioningConfigurationProperty(
                    lake_formation_configuration=datazone_mixins.CfnEnvironmentBlueprintConfigurationPropsMixin.LakeFormationConfigurationProperty(
                        location_registration_exclude_s3_locations=["locationRegistrationExcludeS3Locations"],
                        location_registration_role="locationRegistrationRole"
                    )
                )],
                provisioning_role_arn="provisioningRoleArn",
                regional_parameters=[datazone_mixins.CfnEnvironmentBlueprintConfigurationPropsMixin.RegionalParameterProperty(
                    parameters={
                        "parameters_key": "parameters"
                    },
                    region="region"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f648c5778f26a1b92d4f8d5df19efc275b27b1f215eae5f54f9247ca74ae8057)
            check_type(argname="argument domain_identifier", value=domain_identifier, expected_type=type_hints["domain_identifier"])
            check_type(argname="argument enabled_regions", value=enabled_regions, expected_type=type_hints["enabled_regions"])
            check_type(argname="argument environment_blueprint_identifier", value=environment_blueprint_identifier, expected_type=type_hints["environment_blueprint_identifier"])
            check_type(argname="argument environment_role_permission_boundary", value=environment_role_permission_boundary, expected_type=type_hints["environment_role_permission_boundary"])
            check_type(argname="argument manage_access_role_arn", value=manage_access_role_arn, expected_type=type_hints["manage_access_role_arn"])
            check_type(argname="argument provisioning_configurations", value=provisioning_configurations, expected_type=type_hints["provisioning_configurations"])
            check_type(argname="argument provisioning_role_arn", value=provisioning_role_arn, expected_type=type_hints["provisioning_role_arn"])
            check_type(argname="argument regional_parameters", value=regional_parameters, expected_type=type_hints["regional_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if domain_identifier is not None:
            self._values["domain_identifier"] = domain_identifier
        if enabled_regions is not None:
            self._values["enabled_regions"] = enabled_regions
        if environment_blueprint_identifier is not None:
            self._values["environment_blueprint_identifier"] = environment_blueprint_identifier
        if environment_role_permission_boundary is not None:
            self._values["environment_role_permission_boundary"] = environment_role_permission_boundary
        if manage_access_role_arn is not None:
            self._values["manage_access_role_arn"] = manage_access_role_arn
        if provisioning_configurations is not None:
            self._values["provisioning_configurations"] = provisioning_configurations
        if provisioning_role_arn is not None:
            self._values["provisioning_role_arn"] = provisioning_role_arn
        if regional_parameters is not None:
            self._values["regional_parameters"] = regional_parameters

    @builtins.property
    def domain_identifier(self) -> typing.Optional[builtins.str]:
        '''The identifier of the Amazon DataZone domain in which an environment blueprint exists.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environmentblueprintconfiguration.html#cfn-datazone-environmentblueprintconfiguration-domainidentifier
        '''
        result = self._values.get("domain_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The enabled AWS Regions specified in a blueprint configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environmentblueprintconfiguration.html#cfn-datazone-environmentblueprintconfiguration-enabledregions
        '''
        result = self._values.get("enabled_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def environment_blueprint_identifier(self) -> typing.Optional[builtins.str]:
        '''The identifier of the environment blueprint.

        In the current release, only the following values are supported: ``DefaultDataLake`` and ``DefaultDataWarehouse`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environmentblueprintconfiguration.html#cfn-datazone-environmentblueprintconfiguration-environmentblueprintidentifier
        '''
        result = self._values.get("environment_blueprint_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_role_permission_boundary(self) -> typing.Optional[builtins.str]:
        '''The environment role permission boundary.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environmentblueprintconfiguration.html#cfn-datazone-environmentblueprintconfiguration-environmentrolepermissionboundary
        '''
        result = self._values.get("environment_role_permission_boundary")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def manage_access_role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the manage access role.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environmentblueprintconfiguration.html#cfn-datazone-environmentblueprintconfiguration-manageaccessrolearn
        '''
        result = self._values.get("manage_access_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provisioning_configurations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentBlueprintConfigurationPropsMixin.ProvisioningConfigurationProperty"]]]]:
        '''The provisioning configuration of a blueprint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environmentblueprintconfiguration.html#cfn-datazone-environmentblueprintconfiguration-provisioningconfigurations
        '''
        result = self._values.get("provisioning_configurations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentBlueprintConfigurationPropsMixin.ProvisioningConfigurationProperty"]]]], result)

    @builtins.property
    def provisioning_role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the provisioning role.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environmentblueprintconfiguration.html#cfn-datazone-environmentblueprintconfiguration-provisioningrolearn
        '''
        result = self._values.get("provisioning_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def regional_parameters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentBlueprintConfigurationPropsMixin.RegionalParameterProperty"]]]]:
        '''The regional parameters of the environment blueprint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environmentblueprintconfiguration.html#cfn-datazone-environmentblueprintconfiguration-regionalparameters
        '''
        result = self._values.get("regional_parameters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentBlueprintConfigurationPropsMixin.RegionalParameterProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEnvironmentBlueprintConfigurationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnEnvironmentBlueprintConfigurationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnEnvironmentBlueprintConfigurationPropsMixin",
):
    '''The configuration details of an environment blueprint.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environmentblueprintconfiguration.html
    :cloudformationResource: AWS::DataZone::EnvironmentBlueprintConfiguration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
        
        cfn_environment_blueprint_configuration_props_mixin = datazone_mixins.CfnEnvironmentBlueprintConfigurationPropsMixin(datazone_mixins.CfnEnvironmentBlueprintConfigurationMixinProps(
            domain_identifier="domainIdentifier",
            enabled_regions=["enabledRegions"],
            environment_blueprint_identifier="environmentBlueprintIdentifier",
            environment_role_permission_boundary="environmentRolePermissionBoundary",
            manage_access_role_arn="manageAccessRoleArn",
            provisioning_configurations=[datazone_mixins.CfnEnvironmentBlueprintConfigurationPropsMixin.ProvisioningConfigurationProperty(
                lake_formation_configuration=datazone_mixins.CfnEnvironmentBlueprintConfigurationPropsMixin.LakeFormationConfigurationProperty(
                    location_registration_exclude_s3_locations=["locationRegistrationExcludeS3Locations"],
                    location_registration_role="locationRegistrationRole"
                )
            )],
            provisioning_role_arn="provisioningRoleArn",
            regional_parameters=[datazone_mixins.CfnEnvironmentBlueprintConfigurationPropsMixin.RegionalParameterProperty(
                parameters={
                    "parameters_key": "parameters"
                },
                region="region"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnEnvironmentBlueprintConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DataZone::EnvironmentBlueprintConfiguration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13bc2299343995424d0a7a6afe7469f5941079b46f1cebe1b090a7ef0bcdaa22)
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
            type_hints = typing.get_type_hints(_typecheckingstub__31f39f3d678a7ef5574a416af2637d44c60ddba7b327eab2fdbd523c2d1ccf52)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b7f23e8ee44c5c18d130452cd4b58aa33fb2ce8b12a792f81d69f8792cdb8d9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnEnvironmentBlueprintConfigurationMixinProps:
        return typing.cast(CfnEnvironmentBlueprintConfigurationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnEnvironmentBlueprintConfigurationPropsMixin.LakeFormationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "location_registration_exclude_s3_locations": "locationRegistrationExcludeS3Locations",
            "location_registration_role": "locationRegistrationRole",
        },
    )
    class LakeFormationConfigurationProperty:
        def __init__(
            self,
            *,
            location_registration_exclude_s3_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
            location_registration_role: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The Lake Formation configuration of the Data Lake blueprint.

            :param location_registration_exclude_s3_locations: Specifies certain Amazon S3 locations if you do not want Amazon DataZone to automatically register them in hybrid mode.
            :param location_registration_role: The role that is used to manage read/write access to the chosen Amazon S3 bucket(s) for Data Lake using AWS Lake Formation hybrid access mode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-environmentblueprintconfiguration-lakeformationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                lake_formation_configuration_property = datazone_mixins.CfnEnvironmentBlueprintConfigurationPropsMixin.LakeFormationConfigurationProperty(
                    location_registration_exclude_s3_locations=["locationRegistrationExcludeS3Locations"],
                    location_registration_role="locationRegistrationRole"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0567ff0a6c1acd665b8391ce57e262a78a7e5a17f3e590610b82aaafbcc5dd5a)
                check_type(argname="argument location_registration_exclude_s3_locations", value=location_registration_exclude_s3_locations, expected_type=type_hints["location_registration_exclude_s3_locations"])
                check_type(argname="argument location_registration_role", value=location_registration_role, expected_type=type_hints["location_registration_role"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if location_registration_exclude_s3_locations is not None:
                self._values["location_registration_exclude_s3_locations"] = location_registration_exclude_s3_locations
            if location_registration_role is not None:
                self._values["location_registration_role"] = location_registration_role

        @builtins.property
        def location_registration_exclude_s3_locations(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''Specifies certain Amazon S3 locations if you do not want Amazon DataZone to automatically register them in hybrid mode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-environmentblueprintconfiguration-lakeformationconfiguration.html#cfn-datazone-environmentblueprintconfiguration-lakeformationconfiguration-locationregistrationexcludes3locations
            '''
            result = self._values.get("location_registration_exclude_s3_locations")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def location_registration_role(self) -> typing.Optional[builtins.str]:
            '''The role that is used to manage read/write access to the chosen Amazon S3 bucket(s) for Data Lake using AWS Lake Formation hybrid access mode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-environmentblueprintconfiguration-lakeformationconfiguration.html#cfn-datazone-environmentblueprintconfiguration-lakeformationconfiguration-locationregistrationrole
            '''
            result = self._values.get("location_registration_role")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LakeFormationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnEnvironmentBlueprintConfigurationPropsMixin.ProvisioningConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"lake_formation_configuration": "lakeFormationConfiguration"},
    )
    class ProvisioningConfigurationProperty:
        def __init__(
            self,
            *,
            lake_formation_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEnvironmentBlueprintConfigurationPropsMixin.LakeFormationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The provisioning configuration of the blueprint.

            :param lake_formation_configuration: The Lake Formation configuration of the Data Lake blueprint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-environmentblueprintconfiguration-provisioningconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                provisioning_configuration_property = datazone_mixins.CfnEnvironmentBlueprintConfigurationPropsMixin.ProvisioningConfigurationProperty(
                    lake_formation_configuration=datazone_mixins.CfnEnvironmentBlueprintConfigurationPropsMixin.LakeFormationConfigurationProperty(
                        location_registration_exclude_s3_locations=["locationRegistrationExcludeS3Locations"],
                        location_registration_role="locationRegistrationRole"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f4d3467ec9543b98c002aa55202af69ba96e2cc2af787244c70d9f39e2e0521e)
                check_type(argname="argument lake_formation_configuration", value=lake_formation_configuration, expected_type=type_hints["lake_formation_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if lake_formation_configuration is not None:
                self._values["lake_formation_configuration"] = lake_formation_configuration

        @builtins.property
        def lake_formation_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentBlueprintConfigurationPropsMixin.LakeFormationConfigurationProperty"]]:
            '''The Lake Formation configuration of the Data Lake blueprint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-environmentblueprintconfiguration-provisioningconfiguration.html#cfn-datazone-environmentblueprintconfiguration-provisioningconfiguration-lakeformationconfiguration
            '''
            result = self._values.get("lake_formation_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentBlueprintConfigurationPropsMixin.LakeFormationConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProvisioningConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnEnvironmentBlueprintConfigurationPropsMixin.RegionalParameterProperty",
        jsii_struct_bases=[],
        name_mapping={"parameters": "parameters", "region": "region"},
    )
    class RegionalParameterProperty:
        def __init__(
            self,
            *,
            parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            region: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The regional parameters in the environment blueprint.

            :param parameters: A string to string map containing parameters for the region.
            :param region: The region specified in the environment parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-environmentblueprintconfiguration-regionalparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                regional_parameter_property = datazone_mixins.CfnEnvironmentBlueprintConfigurationPropsMixin.RegionalParameterProperty(
                    parameters={
                        "parameters_key": "parameters"
                    },
                    region="region"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cfe4f6e0c2f705acdfd343395f8a8f4d7be26ab32c5cd8245aea3be15423bd3a)
                check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
                check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if parameters is not None:
                self._values["parameters"] = parameters
            if region is not None:
                self._values["region"] = region

        @builtins.property
        def parameters(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''A string to string map containing parameters for the region.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-environmentblueprintconfiguration-regionalparameter.html#cfn-datazone-environmentblueprintconfiguration-regionalparameter-parameters
            '''
            result = self._values.get("parameters")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def region(self) -> typing.Optional[builtins.str]:
            '''The region specified in the environment parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-environmentblueprintconfiguration-regionalparameter.html#cfn-datazone-environmentblueprintconfiguration-regionalparameter-region
            '''
            result = self._values.get("region")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RegionalParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnEnvironmentMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "domain_identifier": "domainIdentifier",
        "environment_account_identifier": "environmentAccountIdentifier",
        "environment_account_region": "environmentAccountRegion",
        "environment_profile_identifier": "environmentProfileIdentifier",
        "environment_role_arn": "environmentRoleArn",
        "glossary_terms": "glossaryTerms",
        "name": "name",
        "project_identifier": "projectIdentifier",
        "user_parameters": "userParameters",
    },
)
class CfnEnvironmentMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        domain_identifier: typing.Optional[builtins.str] = None,
        environment_account_identifier: typing.Optional[builtins.str] = None,
        environment_account_region: typing.Optional[builtins.str] = None,
        environment_profile_identifier: typing.Optional[builtins.str] = None,
        environment_role_arn: typing.Optional[builtins.str] = None,
        glossary_terms: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        project_identifier: typing.Optional[builtins.str] = None,
        user_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEnvironmentPropsMixin.EnvironmentParameterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnEnvironmentPropsMixin.

        :param description: The description of the environment.
        :param domain_identifier: The identifier of the Amazon DataZone domain in which the environment is created.
        :param environment_account_identifier: The identifier of the AWS account in which an environment exists.
        :param environment_account_region: The AWS Region in which an environment exists.
        :param environment_profile_identifier: The identifier of the environment profile that is used to create this Amazon DataZone environment.
        :param environment_role_arn: The ARN of the environment role.
        :param glossary_terms: The glossary terms that can be used in this Amazon DataZone environment.
        :param name: The name of the Amazon DataZone environment.
        :param project_identifier: The identifier of the Amazon DataZone project in which this environment is created.
        :param user_parameters: The user parameters of this Amazon DataZone environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
            
            cfn_environment_mixin_props = datazone_mixins.CfnEnvironmentMixinProps(
                description="description",
                domain_identifier="domainIdentifier",
                environment_account_identifier="environmentAccountIdentifier",
                environment_account_region="environmentAccountRegion",
                environment_profile_identifier="environmentProfileIdentifier",
                environment_role_arn="environmentRoleArn",
                glossary_terms=["glossaryTerms"],
                name="name",
                project_identifier="projectIdentifier",
                user_parameters=[datazone_mixins.CfnEnvironmentPropsMixin.EnvironmentParameterProperty(
                    name="name",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60c8c23614e820064fa4fa09334ff89de65fc765d99fdc49bc9d163d8353be7b)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument domain_identifier", value=domain_identifier, expected_type=type_hints["domain_identifier"])
            check_type(argname="argument environment_account_identifier", value=environment_account_identifier, expected_type=type_hints["environment_account_identifier"])
            check_type(argname="argument environment_account_region", value=environment_account_region, expected_type=type_hints["environment_account_region"])
            check_type(argname="argument environment_profile_identifier", value=environment_profile_identifier, expected_type=type_hints["environment_profile_identifier"])
            check_type(argname="argument environment_role_arn", value=environment_role_arn, expected_type=type_hints["environment_role_arn"])
            check_type(argname="argument glossary_terms", value=glossary_terms, expected_type=type_hints["glossary_terms"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument project_identifier", value=project_identifier, expected_type=type_hints["project_identifier"])
            check_type(argname="argument user_parameters", value=user_parameters, expected_type=type_hints["user_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if domain_identifier is not None:
            self._values["domain_identifier"] = domain_identifier
        if environment_account_identifier is not None:
            self._values["environment_account_identifier"] = environment_account_identifier
        if environment_account_region is not None:
            self._values["environment_account_region"] = environment_account_region
        if environment_profile_identifier is not None:
            self._values["environment_profile_identifier"] = environment_profile_identifier
        if environment_role_arn is not None:
            self._values["environment_role_arn"] = environment_role_arn
        if glossary_terms is not None:
            self._values["glossary_terms"] = glossary_terms
        if name is not None:
            self._values["name"] = name
        if project_identifier is not None:
            self._values["project_identifier"] = project_identifier
        if user_parameters is not None:
            self._values["user_parameters"] = user_parameters

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environment.html#cfn-datazone-environment-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_identifier(self) -> typing.Optional[builtins.str]:
        '''The identifier of the Amazon DataZone domain in which the environment is created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environment.html#cfn-datazone-environment-domainidentifier
        '''
        result = self._values.get("domain_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_account_identifier(self) -> typing.Optional[builtins.str]:
        '''The identifier of the AWS account in which an environment exists.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environment.html#cfn-datazone-environment-environmentaccountidentifier
        '''
        result = self._values.get("environment_account_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_account_region(self) -> typing.Optional[builtins.str]:
        '''The AWS Region in which an environment exists.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environment.html#cfn-datazone-environment-environmentaccountregion
        '''
        result = self._values.get("environment_account_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_profile_identifier(self) -> typing.Optional[builtins.str]:
        '''The identifier of the environment profile that is used to create this Amazon DataZone environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environment.html#cfn-datazone-environment-environmentprofileidentifier
        '''
        result = self._values.get("environment_profile_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the environment role.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environment.html#cfn-datazone-environment-environmentrolearn
        '''
        result = self._values.get("environment_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def glossary_terms(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The glossary terms that can be used in this Amazon DataZone environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environment.html#cfn-datazone-environment-glossaryterms
        '''
        result = self._values.get("glossary_terms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the Amazon DataZone environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environment.html#cfn-datazone-environment-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_identifier(self) -> typing.Optional[builtins.str]:
        '''The identifier of the Amazon DataZone project in which this environment is created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environment.html#cfn-datazone-environment-projectidentifier
        '''
        result = self._values.get("project_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_parameters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.EnvironmentParameterProperty"]]]]:
        '''The user parameters of this Amazon DataZone environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environment.html#cfn-datazone-environment-userparameters
        '''
        result = self._values.get("user_parameters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.EnvironmentParameterProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEnvironmentMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnEnvironmentProfileMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "aws_account_id": "awsAccountId",
        "aws_account_region": "awsAccountRegion",
        "description": "description",
        "domain_identifier": "domainIdentifier",
        "environment_blueprint_identifier": "environmentBlueprintIdentifier",
        "name": "name",
        "project_identifier": "projectIdentifier",
        "user_parameters": "userParameters",
    },
)
class CfnEnvironmentProfileMixinProps:
    def __init__(
        self,
        *,
        aws_account_id: typing.Optional[builtins.str] = None,
        aws_account_region: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        domain_identifier: typing.Optional[builtins.str] = None,
        environment_blueprint_identifier: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        project_identifier: typing.Optional[builtins.str] = None,
        user_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEnvironmentProfilePropsMixin.EnvironmentParameterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnEnvironmentProfilePropsMixin.

        :param aws_account_id: The identifier of an AWS account in which an environment profile exists.
        :param aws_account_region: The AWS Region in which an environment profile exists.
        :param description: The description of the environment profile.
        :param domain_identifier: The identifier of the Amazon DataZone domain in which the environment profile exists.
        :param environment_blueprint_identifier: The identifier of a blueprint with which an environment profile is created.
        :param name: The name of the environment profile.
        :param project_identifier: The identifier of a project in which an environment profile exists.
        :param user_parameters: The user parameters of this Amazon DataZone environment profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environmentprofile.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
            
            cfn_environment_profile_mixin_props = datazone_mixins.CfnEnvironmentProfileMixinProps(
                aws_account_id="awsAccountId",
                aws_account_region="awsAccountRegion",
                description="description",
                domain_identifier="domainIdentifier",
                environment_blueprint_identifier="environmentBlueprintIdentifier",
                name="name",
                project_identifier="projectIdentifier",
                user_parameters=[datazone_mixins.CfnEnvironmentProfilePropsMixin.EnvironmentParameterProperty(
                    name="name",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6363d5c6236631f6931464c990d3c8049a3a475aec64a472f5b4b0983d903f41)
            check_type(argname="argument aws_account_id", value=aws_account_id, expected_type=type_hints["aws_account_id"])
            check_type(argname="argument aws_account_region", value=aws_account_region, expected_type=type_hints["aws_account_region"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument domain_identifier", value=domain_identifier, expected_type=type_hints["domain_identifier"])
            check_type(argname="argument environment_blueprint_identifier", value=environment_blueprint_identifier, expected_type=type_hints["environment_blueprint_identifier"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument project_identifier", value=project_identifier, expected_type=type_hints["project_identifier"])
            check_type(argname="argument user_parameters", value=user_parameters, expected_type=type_hints["user_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_account_id is not None:
            self._values["aws_account_id"] = aws_account_id
        if aws_account_region is not None:
            self._values["aws_account_region"] = aws_account_region
        if description is not None:
            self._values["description"] = description
        if domain_identifier is not None:
            self._values["domain_identifier"] = domain_identifier
        if environment_blueprint_identifier is not None:
            self._values["environment_blueprint_identifier"] = environment_blueprint_identifier
        if name is not None:
            self._values["name"] = name
        if project_identifier is not None:
            self._values["project_identifier"] = project_identifier
        if user_parameters is not None:
            self._values["user_parameters"] = user_parameters

    @builtins.property
    def aws_account_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of an AWS account in which an environment profile exists.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environmentprofile.html#cfn-datazone-environmentprofile-awsaccountid
        '''
        result = self._values.get("aws_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def aws_account_region(self) -> typing.Optional[builtins.str]:
        '''The AWS Region in which an environment profile exists.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environmentprofile.html#cfn-datazone-environmentprofile-awsaccountregion
        '''
        result = self._values.get("aws_account_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the environment profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environmentprofile.html#cfn-datazone-environmentprofile-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_identifier(self) -> typing.Optional[builtins.str]:
        '''The identifier of the Amazon DataZone domain in which the environment profile exists.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environmentprofile.html#cfn-datazone-environmentprofile-domainidentifier
        '''
        result = self._values.get("domain_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_blueprint_identifier(self) -> typing.Optional[builtins.str]:
        '''The identifier of a blueprint with which an environment profile is created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environmentprofile.html#cfn-datazone-environmentprofile-environmentblueprintidentifier
        '''
        result = self._values.get("environment_blueprint_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the environment profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environmentprofile.html#cfn-datazone-environmentprofile-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_identifier(self) -> typing.Optional[builtins.str]:
        '''The identifier of a project in which an environment profile exists.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environmentprofile.html#cfn-datazone-environmentprofile-projectidentifier
        '''
        result = self._values.get("project_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_parameters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentProfilePropsMixin.EnvironmentParameterProperty"]]]]:
        '''The user parameters of this Amazon DataZone environment profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environmentprofile.html#cfn-datazone-environmentprofile-userparameters
        '''
        result = self._values.get("user_parameters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentProfilePropsMixin.EnvironmentParameterProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEnvironmentProfileMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnEnvironmentProfilePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnEnvironmentProfilePropsMixin",
):
    '''The details of an environment profile.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environmentprofile.html
    :cloudformationResource: AWS::DataZone::EnvironmentProfile
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
        
        cfn_environment_profile_props_mixin = datazone_mixins.CfnEnvironmentProfilePropsMixin(datazone_mixins.CfnEnvironmentProfileMixinProps(
            aws_account_id="awsAccountId",
            aws_account_region="awsAccountRegion",
            description="description",
            domain_identifier="domainIdentifier",
            environment_blueprint_identifier="environmentBlueprintIdentifier",
            name="name",
            project_identifier="projectIdentifier",
            user_parameters=[datazone_mixins.CfnEnvironmentProfilePropsMixin.EnvironmentParameterProperty(
                name="name",
                value="value"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnEnvironmentProfileMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DataZone::EnvironmentProfile``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a56642316673db881ea7b008cf7562aaeeba96e3e3a7dbadc58696cc2fca8cf7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e0de04a1963dd16eb973e2110b436c1919a33bdec51b601e59f6f6ab89d5d41)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ac61f36bf807794b45d1c60604eb3091d2c2027020f2e5ae8270ce3b09924cd)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnEnvironmentProfileMixinProps:
        return typing.cast(CfnEnvironmentProfileMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnEnvironmentProfilePropsMixin.EnvironmentParameterProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class EnvironmentParameterProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The parameter details of an environment profile.

            :param name: The name specified in the environment parameter.
            :param value: The value of the environment profile.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-environmentprofile-environmentparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                environment_parameter_property = datazone_mixins.CfnEnvironmentProfilePropsMixin.EnvironmentParameterProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3a4ad7188de7e0538cff76886de88b7232ac003dda65d4d8ce12f0b32e003d50)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name specified in the environment parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-environmentprofile-environmentparameter.html#cfn-datazone-environmentprofile-environmentparameter-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value of the environment profile.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-environmentprofile-environmentparameter.html#cfn-datazone-environmentprofile-environmentparameter-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EnvironmentParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IMixin_11e4b965)
class CfnEnvironmentPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnEnvironmentPropsMixin",
):
    '''The ``AWS::DataZone::Environment`` resource specifies an Amazon DataZone environment, which is a collection of zero or more configured resources with a given set of IAM principals who can operate on those resources.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environment.html
    :cloudformationResource: AWS::DataZone::Environment
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
        
        cfn_environment_props_mixin = datazone_mixins.CfnEnvironmentPropsMixin(datazone_mixins.CfnEnvironmentMixinProps(
            description="description",
            domain_identifier="domainIdentifier",
            environment_account_identifier="environmentAccountIdentifier",
            environment_account_region="environmentAccountRegion",
            environment_profile_identifier="environmentProfileIdentifier",
            environment_role_arn="environmentRoleArn",
            glossary_terms=["glossaryTerms"],
            name="name",
            project_identifier="projectIdentifier",
            user_parameters=[datazone_mixins.CfnEnvironmentPropsMixin.EnvironmentParameterProperty(
                name="name",
                value="value"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnEnvironmentMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DataZone::Environment``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d4c368cbeac8b5477d2780a8e0764c6b50587cb54a2e13476a72f7520cc628c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef87958fb07af031c16ff87f512f9060432a0f5fb478a46c8ce2ecb30a433eed)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7954752937fef374217943bf7696453c26d50b3d4226e689dde84cbc6e7dc225)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnEnvironmentMixinProps:
        return typing.cast(CfnEnvironmentMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnEnvironmentPropsMixin.EnvironmentParameterProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class EnvironmentParameterProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The parameter details of the environment.

            :param name: The name of the environment parameter.
            :param value: The value of the environment parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-environment-environmentparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                environment_parameter_property = datazone_mixins.CfnEnvironmentPropsMixin.EnvironmentParameterProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f35b6cdd950b506968a0e979010d47306c2cc204ee46a58b3553723a1aa4e267)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the environment parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-environment-environmentparameter.html#cfn-datazone-environment-environmentparameter-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value of the environment parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-environment-environmentparameter.html#cfn-datazone-environment-environmentparameter-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EnvironmentParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnFormTypeMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "domain_identifier": "domainIdentifier",
        "model": "model",
        "name": "name",
        "owning_project_identifier": "owningProjectIdentifier",
        "status": "status",
    },
)
class CfnFormTypeMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        domain_identifier: typing.Optional[builtins.str] = None,
        model: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFormTypePropsMixin.ModelProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        owning_project_identifier: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnFormTypePropsMixin.

        :param description: The description of the metadata form type.
        :param domain_identifier: The identifier of the Amazon DataZone domain in which the form type exists.
        :param model: The model of the form type.
        :param name: The name of the form type.
        :param owning_project_identifier: The identifier of the project that owns the form type.
        :param status: The status of the form type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-formtype.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
            
            cfn_form_type_mixin_props = datazone_mixins.CfnFormTypeMixinProps(
                description="description",
                domain_identifier="domainIdentifier",
                model=datazone_mixins.CfnFormTypePropsMixin.ModelProperty(
                    smithy="smithy"
                ),
                name="name",
                owning_project_identifier="owningProjectIdentifier",
                status="status"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6ebafed279b613f6265187ea10c87fd84115ff112ad6d82406728b059aa5466)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument domain_identifier", value=domain_identifier, expected_type=type_hints["domain_identifier"])
            check_type(argname="argument model", value=model, expected_type=type_hints["model"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument owning_project_identifier", value=owning_project_identifier, expected_type=type_hints["owning_project_identifier"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if domain_identifier is not None:
            self._values["domain_identifier"] = domain_identifier
        if model is not None:
            self._values["model"] = model
        if name is not None:
            self._values["name"] = name
        if owning_project_identifier is not None:
            self._values["owning_project_identifier"] = owning_project_identifier
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the metadata form type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-formtype.html#cfn-datazone-formtype-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_identifier(self) -> typing.Optional[builtins.str]:
        '''The identifier of the Amazon DataZone domain in which the form type exists.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-formtype.html#cfn-datazone-formtype-domainidentifier
        '''
        result = self._values.get("domain_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def model(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormTypePropsMixin.ModelProperty"]]:
        '''The model of the form type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-formtype.html#cfn-datazone-formtype-model
        '''
        result = self._values.get("model")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormTypePropsMixin.ModelProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the form type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-formtype.html#cfn-datazone-formtype-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def owning_project_identifier(self) -> typing.Optional[builtins.str]:
        '''The identifier of the project that owns the form type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-formtype.html#cfn-datazone-formtype-owningprojectidentifier
        '''
        result = self._values.get("owning_project_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''The status of the form type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-formtype.html#cfn-datazone-formtype-status
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFormTypeMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnFormTypePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnFormTypePropsMixin",
):
    '''The details of the metadata form type.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-formtype.html
    :cloudformationResource: AWS::DataZone::FormType
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
        
        cfn_form_type_props_mixin = datazone_mixins.CfnFormTypePropsMixin(datazone_mixins.CfnFormTypeMixinProps(
            description="description",
            domain_identifier="domainIdentifier",
            model=datazone_mixins.CfnFormTypePropsMixin.ModelProperty(
                smithy="smithy"
            ),
            name="name",
            owning_project_identifier="owningProjectIdentifier",
            status="status"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnFormTypeMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DataZone::FormType``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7193b39b68d1e3cc2091cec7ff8541ec590f4ede540878026792596fe4569aea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1717c98302443f9d1bdda877c3d3cdded6387662adeae782ac5c053808aeb12e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec213309a8b99d3365dbc019f560c00981c927d8025745b9f4d26f2eb351149c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnFormTypeMixinProps:
        return typing.cast(CfnFormTypeMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnFormTypePropsMixin.ModelProperty",
        jsii_struct_bases=[],
        name_mapping={"smithy": "smithy"},
    )
    class ModelProperty:
        def __init__(self, *, smithy: typing.Optional[builtins.str] = None) -> None:
            '''Indicates the smithy model of the API.

            :param smithy: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-formtype-model.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                model_property = datazone_mixins.CfnFormTypePropsMixin.ModelProperty(
                    smithy="smithy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__55a16529eff75aff941a429c115435744572a76d0af30f848596d4dcdee8824c)
                check_type(argname="argument smithy", value=smithy, expected_type=type_hints["smithy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if smithy is not None:
                self._values["smithy"] = smithy

        @builtins.property
        def smithy(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-formtype-model.html#cfn-datazone-formtype-model-smithy
            '''
            result = self._values.get("smithy")
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
    jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnGroupProfileMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "domain_identifier": "domainIdentifier",
        "group_identifier": "groupIdentifier",
        "status": "status",
    },
)
class CfnGroupProfileMixinProps:
    def __init__(
        self,
        *,
        domain_identifier: typing.Optional[builtins.str] = None,
        group_identifier: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnGroupProfilePropsMixin.

        :param domain_identifier: The identifier of the Amazon DataZone domain in which a group profile exists.
        :param group_identifier: The ID of the group of a project member.
        :param status: The status of a group profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-groupprofile.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
            
            cfn_group_profile_mixin_props = datazone_mixins.CfnGroupProfileMixinProps(
                domain_identifier="domainIdentifier",
                group_identifier="groupIdentifier",
                status="status"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ceed13c14cc781ec411a58f27d38502b64f7581d33f989a2ccada7cb2d225d7)
            check_type(argname="argument domain_identifier", value=domain_identifier, expected_type=type_hints["domain_identifier"])
            check_type(argname="argument group_identifier", value=group_identifier, expected_type=type_hints["group_identifier"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if domain_identifier is not None:
            self._values["domain_identifier"] = domain_identifier
        if group_identifier is not None:
            self._values["group_identifier"] = group_identifier
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def domain_identifier(self) -> typing.Optional[builtins.str]:
        '''The identifier of the Amazon DataZone domain in which a group profile exists.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-groupprofile.html#cfn-datazone-groupprofile-domainidentifier
        '''
        result = self._values.get("domain_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def group_identifier(self) -> typing.Optional[builtins.str]:
        '''The ID of the group of a project member.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-groupprofile.html#cfn-datazone-groupprofile-groupidentifier
        '''
        result = self._values.get("group_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''The status of a group profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-groupprofile.html#cfn-datazone-groupprofile-status
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupProfileMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnGroupProfilePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnGroupProfilePropsMixin",
):
    '''The details of a group profile in Amazon DataZone.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-groupprofile.html
    :cloudformationResource: AWS::DataZone::GroupProfile
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
        
        cfn_group_profile_props_mixin = datazone_mixins.CfnGroupProfilePropsMixin(datazone_mixins.CfnGroupProfileMixinProps(
            domain_identifier="domainIdentifier",
            group_identifier="groupIdentifier",
            status="status"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnGroupProfileMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DataZone::GroupProfile``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c027c8f5b624f22aff2f881b70032eb08da82f57088075b822a75847f9d21a20)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c98983d8b94dde4b66eb773a0857fd686e9596285a0a6dfec9c1e6d140e65fe)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9a7a768ccc2f61b0c68c4d0701817776dcca2252fcaa1cd75fe8c071724cd47)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnGroupProfileMixinProps:
        return typing.cast(CfnGroupProfileMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnOwnerMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "domain_identifier": "domainIdentifier",
        "entity_identifier": "entityIdentifier",
        "entity_type": "entityType",
        "owner": "owner",
    },
)
class CfnOwnerMixinProps:
    def __init__(
        self,
        *,
        domain_identifier: typing.Optional[builtins.str] = None,
        entity_identifier: typing.Optional[builtins.str] = None,
        entity_type: typing.Optional[builtins.str] = None,
        owner: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOwnerPropsMixin.OwnerPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnOwnerPropsMixin.

        :param domain_identifier: The ID of the domain in which you want to add the entity owner.
        :param entity_identifier: The ID of the entity to which you want to add an owner.
        :param entity_type: The type of an entity.
        :param owner: The owner that you want to add to the entity.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-owner.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
            
            cfn_owner_mixin_props = datazone_mixins.CfnOwnerMixinProps(
                domain_identifier="domainIdentifier",
                entity_identifier="entityIdentifier",
                entity_type="entityType",
                owner=datazone_mixins.CfnOwnerPropsMixin.OwnerPropertiesProperty(
                    group=datazone_mixins.CfnOwnerPropsMixin.OwnerGroupPropertiesProperty(
                        group_identifier="groupIdentifier"
                    ),
                    user=datazone_mixins.CfnOwnerPropsMixin.OwnerUserPropertiesProperty(
                        user_identifier="userIdentifier"
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1a26a7a00fe9988d332432c09985c9476c5152169714f5c986ea836d732ff6b)
            check_type(argname="argument domain_identifier", value=domain_identifier, expected_type=type_hints["domain_identifier"])
            check_type(argname="argument entity_identifier", value=entity_identifier, expected_type=type_hints["entity_identifier"])
            check_type(argname="argument entity_type", value=entity_type, expected_type=type_hints["entity_type"])
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if domain_identifier is not None:
            self._values["domain_identifier"] = domain_identifier
        if entity_identifier is not None:
            self._values["entity_identifier"] = entity_identifier
        if entity_type is not None:
            self._values["entity_type"] = entity_type
        if owner is not None:
            self._values["owner"] = owner

    @builtins.property
    def domain_identifier(self) -> typing.Optional[builtins.str]:
        '''The ID of the domain in which you want to add the entity owner.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-owner.html#cfn-datazone-owner-domainidentifier
        '''
        result = self._values.get("domain_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def entity_identifier(self) -> typing.Optional[builtins.str]:
        '''The ID of the entity to which you want to add an owner.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-owner.html#cfn-datazone-owner-entityidentifier
        '''
        result = self._values.get("entity_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def entity_type(self) -> typing.Optional[builtins.str]:
        '''The type of an entity.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-owner.html#cfn-datazone-owner-entitytype
        '''
        result = self._values.get("entity_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def owner(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOwnerPropsMixin.OwnerPropertiesProperty"]]:
        '''The owner that you want to add to the entity.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-owner.html#cfn-datazone-owner-owner
        '''
        result = self._values.get("owner")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOwnerPropsMixin.OwnerPropertiesProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnOwnerMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnOwnerPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnOwnerPropsMixin",
):
    '''The owner that you want to add to the entity.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-owner.html
    :cloudformationResource: AWS::DataZone::Owner
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
        
        cfn_owner_props_mixin = datazone_mixins.CfnOwnerPropsMixin(datazone_mixins.CfnOwnerMixinProps(
            domain_identifier="domainIdentifier",
            entity_identifier="entityIdentifier",
            entity_type="entityType",
            owner=datazone_mixins.CfnOwnerPropsMixin.OwnerPropertiesProperty(
                group=datazone_mixins.CfnOwnerPropsMixin.OwnerGroupPropertiesProperty(
                    group_identifier="groupIdentifier"
                ),
                user=datazone_mixins.CfnOwnerPropsMixin.OwnerUserPropertiesProperty(
                    user_identifier="userIdentifier"
                )
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnOwnerMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DataZone::Owner``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70b2424bdc582664b3c5802b2fea8ed695fc9be1ec801f16705dace63ad4da30)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2f8fb760b1d80d024de47de60a35c470748ca12a61f3a3ccc0ae5af3b2d510c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91e702fcbc8670affff9a27efd14fee4101c3da0aa1a0c1fcdacacf9ca487457)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnOwnerMixinProps:
        return typing.cast(CfnOwnerMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnOwnerPropsMixin.OwnerGroupPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"group_identifier": "groupIdentifier"},
    )
    class OwnerGroupPropertiesProperty:
        def __init__(
            self,
            *,
            group_identifier: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The properties of the domain unit owners group.

            :param group_identifier: The ID of the domain unit owners group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-owner-ownergroupproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                owner_group_properties_property = datazone_mixins.CfnOwnerPropsMixin.OwnerGroupPropertiesProperty(
                    group_identifier="groupIdentifier"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__814a5dbe8db5abfd9acbd7071b5f62d344fbe0fc0cc7b98e278d63c21d0adf88)
                check_type(argname="argument group_identifier", value=group_identifier, expected_type=type_hints["group_identifier"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if group_identifier is not None:
                self._values["group_identifier"] = group_identifier

        @builtins.property
        def group_identifier(self) -> typing.Optional[builtins.str]:
            '''The ID of the domain unit owners group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-owner-ownergroupproperties.html#cfn-datazone-owner-ownergroupproperties-groupidentifier
            '''
            result = self._values.get("group_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OwnerGroupPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnOwnerPropsMixin.OwnerPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"group": "group", "user": "user"},
    )
    class OwnerPropertiesProperty:
        def __init__(
            self,
            *,
            group: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOwnerPropsMixin.OwnerGroupPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            user: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOwnerPropsMixin.OwnerUserPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The properties of a domain unit's owner.

            :param group: Specifies that the domain unit owner is a group.
            :param user: Specifies that the domain unit owner is a user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-owner-ownerproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                owner_properties_property = datazone_mixins.CfnOwnerPropsMixin.OwnerPropertiesProperty(
                    group=datazone_mixins.CfnOwnerPropsMixin.OwnerGroupPropertiesProperty(
                        group_identifier="groupIdentifier"
                    ),
                    user=datazone_mixins.CfnOwnerPropsMixin.OwnerUserPropertiesProperty(
                        user_identifier="userIdentifier"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__312f0c87cd85e7d121c743c41c4e335bb0f21b876c280b8d823bac0b8e51d61d)
                check_type(argname="argument group", value=group, expected_type=type_hints["group"])
                check_type(argname="argument user", value=user, expected_type=type_hints["user"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if group is not None:
                self._values["group"] = group
            if user is not None:
                self._values["user"] = user

        @builtins.property
        def group(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOwnerPropsMixin.OwnerGroupPropertiesProperty"]]:
            '''Specifies that the domain unit owner is a group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-owner-ownerproperties.html#cfn-datazone-owner-ownerproperties-group
            '''
            result = self._values.get("group")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOwnerPropsMixin.OwnerGroupPropertiesProperty"]], result)

        @builtins.property
        def user(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOwnerPropsMixin.OwnerUserPropertiesProperty"]]:
            '''Specifies that the domain unit owner is a user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-owner-ownerproperties.html#cfn-datazone-owner-ownerproperties-user
            '''
            result = self._values.get("user")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOwnerPropsMixin.OwnerUserPropertiesProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OwnerPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnOwnerPropsMixin.OwnerUserPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"user_identifier": "userIdentifier"},
    )
    class OwnerUserPropertiesProperty:
        def __init__(
            self,
            *,
            user_identifier: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The properties of the owner user.

            :param user_identifier: The ID of the owner user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-owner-owneruserproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                owner_user_properties_property = datazone_mixins.CfnOwnerPropsMixin.OwnerUserPropertiesProperty(
                    user_identifier="userIdentifier"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2e59aa7dc3d8971606aa889f1c8dd2a742bf5238b7119b00ca6158a4e11ae8d4)
                check_type(argname="argument user_identifier", value=user_identifier, expected_type=type_hints["user_identifier"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if user_identifier is not None:
                self._values["user_identifier"] = user_identifier

        @builtins.property
        def user_identifier(self) -> typing.Optional[builtins.str]:
            '''The ID of the owner user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-owner-owneruserproperties.html#cfn-datazone-owner-owneruserproperties-useridentifier
            '''
            result = self._values.get("user_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OwnerUserPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnPolicyGrantMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "detail": "detail",
        "domain_identifier": "domainIdentifier",
        "entity_identifier": "entityIdentifier",
        "entity_type": "entityType",
        "policy_type": "policyType",
        "principal": "principal",
    },
)
class CfnPolicyGrantMixinProps:
    def __init__(
        self,
        *,
        detail: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPolicyGrantPropsMixin.PolicyGrantDetailProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        domain_identifier: typing.Optional[builtins.str] = None,
        entity_identifier: typing.Optional[builtins.str] = None,
        entity_type: typing.Optional[builtins.str] = None,
        policy_type: typing.Optional[builtins.str] = None,
        principal: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPolicyGrantPropsMixin.PolicyGrantPrincipalProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnPolicyGrantPropsMixin.

        :param detail: The details of the policy grant member.
        :param domain_identifier: The ID of the domain where you want to add a policy grant.
        :param entity_identifier: The ID of the entity (resource) to which you want to add a policy grant.
        :param entity_type: The type of entity (resource) to which the grant is added.
        :param policy_type: The type of policy that you want to grant.
        :param principal: The principal of the policy grant member.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-policygrant.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
            
            # all_domain_units_grant_filter: Any
            # all_users_grant_filter: Any
            # create_environment: Any
            # create_environment_from_blueprint: Any
            # delegate_create_environment_profile: Any
            
            cfn_policy_grant_mixin_props = datazone_mixins.CfnPolicyGrantMixinProps(
                detail=datazone_mixins.CfnPolicyGrantPropsMixin.PolicyGrantDetailProperty(
                    add_to_project_member_pool=datazone_mixins.CfnPolicyGrantPropsMixin.AddToProjectMemberPoolPolicyGrantDetailProperty(
                        include_child_domain_units=False
                    ),
                    create_asset_type=datazone_mixins.CfnPolicyGrantPropsMixin.CreateAssetTypePolicyGrantDetailProperty(
                        include_child_domain_units=False
                    ),
                    create_domain_unit=datazone_mixins.CfnPolicyGrantPropsMixin.CreateDomainUnitPolicyGrantDetailProperty(
                        include_child_domain_units=False
                    ),
                    create_environment=create_environment,
                    create_environment_from_blueprint=create_environment_from_blueprint,
                    create_environment_profile=datazone_mixins.CfnPolicyGrantPropsMixin.CreateEnvironmentProfilePolicyGrantDetailProperty(
                        domain_unit_id="domainUnitId"
                    ),
                    create_form_type=datazone_mixins.CfnPolicyGrantPropsMixin.CreateFormTypePolicyGrantDetailProperty(
                        include_child_domain_units=False
                    ),
                    create_glossary=datazone_mixins.CfnPolicyGrantPropsMixin.CreateGlossaryPolicyGrantDetailProperty(
                        include_child_domain_units=False
                    ),
                    create_project=datazone_mixins.CfnPolicyGrantPropsMixin.CreateProjectPolicyGrantDetailProperty(
                        include_child_domain_units=False
                    ),
                    create_project_from_project_profile=datazone_mixins.CfnPolicyGrantPropsMixin.CreateProjectFromProjectProfilePolicyGrantDetailProperty(
                        include_child_domain_units=False,
                        project_profiles=["projectProfiles"]
                    ),
                    delegate_create_environment_profile=delegate_create_environment_profile,
                    override_domain_unit_owners=datazone_mixins.CfnPolicyGrantPropsMixin.OverrideDomainUnitOwnersPolicyGrantDetailProperty(
                        include_child_domain_units=False
                    ),
                    override_project_owners=datazone_mixins.CfnPolicyGrantPropsMixin.OverrideProjectOwnersPolicyGrantDetailProperty(
                        include_child_domain_units=False
                    )
                ),
                domain_identifier="domainIdentifier",
                entity_identifier="entityIdentifier",
                entity_type="entityType",
                policy_type="policyType",
                principal=datazone_mixins.CfnPolicyGrantPropsMixin.PolicyGrantPrincipalProperty(
                    domain_unit=datazone_mixins.CfnPolicyGrantPropsMixin.DomainUnitPolicyGrantPrincipalProperty(
                        domain_unit_designation="domainUnitDesignation",
                        domain_unit_grant_filter=datazone_mixins.CfnPolicyGrantPropsMixin.DomainUnitGrantFilterProperty(
                            all_domain_units_grant_filter=all_domain_units_grant_filter
                        ),
                        domain_unit_identifier="domainUnitIdentifier"
                    ),
                    group=datazone_mixins.CfnPolicyGrantPropsMixin.GroupPolicyGrantPrincipalProperty(
                        group_identifier="groupIdentifier"
                    ),
                    project=datazone_mixins.CfnPolicyGrantPropsMixin.ProjectPolicyGrantPrincipalProperty(
                        project_designation="projectDesignation",
                        project_grant_filter=datazone_mixins.CfnPolicyGrantPropsMixin.ProjectGrantFilterProperty(
                            domain_unit_filter=datazone_mixins.CfnPolicyGrantPropsMixin.DomainUnitFilterForProjectProperty(
                                domain_unit="domainUnit",
                                include_child_domain_units=False
                            )
                        ),
                        project_identifier="projectIdentifier"
                    ),
                    user=datazone_mixins.CfnPolicyGrantPropsMixin.UserPolicyGrantPrincipalProperty(
                        all_users_grant_filter=all_users_grant_filter,
                        user_identifier="userIdentifier"
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a384813d18ed257fb9fe940ccc0afb57ecd54672339329490ee56354100c1e55)
            check_type(argname="argument detail", value=detail, expected_type=type_hints["detail"])
            check_type(argname="argument domain_identifier", value=domain_identifier, expected_type=type_hints["domain_identifier"])
            check_type(argname="argument entity_identifier", value=entity_identifier, expected_type=type_hints["entity_identifier"])
            check_type(argname="argument entity_type", value=entity_type, expected_type=type_hints["entity_type"])
            check_type(argname="argument policy_type", value=policy_type, expected_type=type_hints["policy_type"])
            check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if detail is not None:
            self._values["detail"] = detail
        if domain_identifier is not None:
            self._values["domain_identifier"] = domain_identifier
        if entity_identifier is not None:
            self._values["entity_identifier"] = entity_identifier
        if entity_type is not None:
            self._values["entity_type"] = entity_type
        if policy_type is not None:
            self._values["policy_type"] = policy_type
        if principal is not None:
            self._values["principal"] = principal

    @builtins.property
    def detail(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyGrantPropsMixin.PolicyGrantDetailProperty"]]:
        '''The details of the policy grant member.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-policygrant.html#cfn-datazone-policygrant-detail
        '''
        result = self._values.get("detail")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyGrantPropsMixin.PolicyGrantDetailProperty"]], result)

    @builtins.property
    def domain_identifier(self) -> typing.Optional[builtins.str]:
        '''The ID of the domain where you want to add a policy grant.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-policygrant.html#cfn-datazone-policygrant-domainidentifier
        '''
        result = self._values.get("domain_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def entity_identifier(self) -> typing.Optional[builtins.str]:
        '''The ID of the entity (resource) to which you want to add a policy grant.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-policygrant.html#cfn-datazone-policygrant-entityidentifier
        '''
        result = self._values.get("entity_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def entity_type(self) -> typing.Optional[builtins.str]:
        '''The type of entity (resource) to which the grant is added.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-policygrant.html#cfn-datazone-policygrant-entitytype
        '''
        result = self._values.get("entity_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_type(self) -> typing.Optional[builtins.str]:
        '''The type of policy that you want to grant.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-policygrant.html#cfn-datazone-policygrant-policytype
        '''
        result = self._values.get("policy_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def principal(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyGrantPropsMixin.PolicyGrantPrincipalProperty"]]:
        '''The principal of the policy grant member.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-policygrant.html#cfn-datazone-policygrant-principal
        '''
        result = self._values.get("principal")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyGrantPropsMixin.PolicyGrantPrincipalProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPolicyGrantMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPolicyGrantPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnPolicyGrantPropsMixin",
):
    '''Adds a policy grant (an authorization policy) to a specified entity, including domain units, environment blueprint configurations, or environment profiles.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-policygrant.html
    :cloudformationResource: AWS::DataZone::PolicyGrant
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
        
        # all_domain_units_grant_filter: Any
        # all_users_grant_filter: Any
        # create_environment: Any
        # create_environment_from_blueprint: Any
        # delegate_create_environment_profile: Any
        
        cfn_policy_grant_props_mixin = datazone_mixins.CfnPolicyGrantPropsMixin(datazone_mixins.CfnPolicyGrantMixinProps(
            detail=datazone_mixins.CfnPolicyGrantPropsMixin.PolicyGrantDetailProperty(
                add_to_project_member_pool=datazone_mixins.CfnPolicyGrantPropsMixin.AddToProjectMemberPoolPolicyGrantDetailProperty(
                    include_child_domain_units=False
                ),
                create_asset_type=datazone_mixins.CfnPolicyGrantPropsMixin.CreateAssetTypePolicyGrantDetailProperty(
                    include_child_domain_units=False
                ),
                create_domain_unit=datazone_mixins.CfnPolicyGrantPropsMixin.CreateDomainUnitPolicyGrantDetailProperty(
                    include_child_domain_units=False
                ),
                create_environment=create_environment,
                create_environment_from_blueprint=create_environment_from_blueprint,
                create_environment_profile=datazone_mixins.CfnPolicyGrantPropsMixin.CreateEnvironmentProfilePolicyGrantDetailProperty(
                    domain_unit_id="domainUnitId"
                ),
                create_form_type=datazone_mixins.CfnPolicyGrantPropsMixin.CreateFormTypePolicyGrantDetailProperty(
                    include_child_domain_units=False
                ),
                create_glossary=datazone_mixins.CfnPolicyGrantPropsMixin.CreateGlossaryPolicyGrantDetailProperty(
                    include_child_domain_units=False
                ),
                create_project=datazone_mixins.CfnPolicyGrantPropsMixin.CreateProjectPolicyGrantDetailProperty(
                    include_child_domain_units=False
                ),
                create_project_from_project_profile=datazone_mixins.CfnPolicyGrantPropsMixin.CreateProjectFromProjectProfilePolicyGrantDetailProperty(
                    include_child_domain_units=False,
                    project_profiles=["projectProfiles"]
                ),
                delegate_create_environment_profile=delegate_create_environment_profile,
                override_domain_unit_owners=datazone_mixins.CfnPolicyGrantPropsMixin.OverrideDomainUnitOwnersPolicyGrantDetailProperty(
                    include_child_domain_units=False
                ),
                override_project_owners=datazone_mixins.CfnPolicyGrantPropsMixin.OverrideProjectOwnersPolicyGrantDetailProperty(
                    include_child_domain_units=False
                )
            ),
            domain_identifier="domainIdentifier",
            entity_identifier="entityIdentifier",
            entity_type="entityType",
            policy_type="policyType",
            principal=datazone_mixins.CfnPolicyGrantPropsMixin.PolicyGrantPrincipalProperty(
                domain_unit=datazone_mixins.CfnPolicyGrantPropsMixin.DomainUnitPolicyGrantPrincipalProperty(
                    domain_unit_designation="domainUnitDesignation",
                    domain_unit_grant_filter=datazone_mixins.CfnPolicyGrantPropsMixin.DomainUnitGrantFilterProperty(
                        all_domain_units_grant_filter=all_domain_units_grant_filter
                    ),
                    domain_unit_identifier="domainUnitIdentifier"
                ),
                group=datazone_mixins.CfnPolicyGrantPropsMixin.GroupPolicyGrantPrincipalProperty(
                    group_identifier="groupIdentifier"
                ),
                project=datazone_mixins.CfnPolicyGrantPropsMixin.ProjectPolicyGrantPrincipalProperty(
                    project_designation="projectDesignation",
                    project_grant_filter=datazone_mixins.CfnPolicyGrantPropsMixin.ProjectGrantFilterProperty(
                        domain_unit_filter=datazone_mixins.CfnPolicyGrantPropsMixin.DomainUnitFilterForProjectProperty(
                            domain_unit="domainUnit",
                            include_child_domain_units=False
                        )
                    ),
                    project_identifier="projectIdentifier"
                ),
                user=datazone_mixins.CfnPolicyGrantPropsMixin.UserPolicyGrantPrincipalProperty(
                    all_users_grant_filter=all_users_grant_filter,
                    user_identifier="userIdentifier"
                )
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnPolicyGrantMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DataZone::PolicyGrant``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbcececaf9f67561a7abbba8d9d83d13be3d1c24f05fae8ab385aecd99cf8631)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ffc3b3f2b10267853c1fa65abb5bf71c63f6c4ae693d113993bffc9acb0aa558)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4f17711752c7dc90429018f94b025e7c90b19a413edcc33a78ab8954430b2c7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPolicyGrantMixinProps:
        return typing.cast(CfnPolicyGrantMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnPolicyGrantPropsMixin.AddToProjectMemberPoolPolicyGrantDetailProperty",
        jsii_struct_bases=[],
        name_mapping={"include_child_domain_units": "includeChildDomainUnits"},
    )
    class AddToProjectMemberPoolPolicyGrantDetailProperty:
        def __init__(
            self,
            *,
            include_child_domain_units: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The details of the policy grant.

            :param include_child_domain_units: Specifies whether the policy grant is applied to child domain units.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-addtoprojectmemberpoolpolicygrantdetail.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                add_to_project_member_pool_policy_grant_detail_property = datazone_mixins.CfnPolicyGrantPropsMixin.AddToProjectMemberPoolPolicyGrantDetailProperty(
                    include_child_domain_units=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0f2d6141ff52ea3add4ba7bb37d115f13f9e4c9e38b548b8792afe4bfe596365)
                check_type(argname="argument include_child_domain_units", value=include_child_domain_units, expected_type=type_hints["include_child_domain_units"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if include_child_domain_units is not None:
                self._values["include_child_domain_units"] = include_child_domain_units

        @builtins.property
        def include_child_domain_units(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether the policy grant is applied to child domain units.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-addtoprojectmemberpoolpolicygrantdetail.html#cfn-datazone-policygrant-addtoprojectmemberpoolpolicygrantdetail-includechilddomainunits
            '''
            result = self._values.get("include_child_domain_units")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AddToProjectMemberPoolPolicyGrantDetailProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnPolicyGrantPropsMixin.CreateAssetTypePolicyGrantDetailProperty",
        jsii_struct_bases=[],
        name_mapping={"include_child_domain_units": "includeChildDomainUnits"},
    )
    class CreateAssetTypePolicyGrantDetailProperty:
        def __init__(
            self,
            *,
            include_child_domain_units: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The details of the policy grant.

            :param include_child_domain_units: Specifies whether the policy grant is applied to child domain units.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-createassettypepolicygrantdetail.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                create_asset_type_policy_grant_detail_property = datazone_mixins.CfnPolicyGrantPropsMixin.CreateAssetTypePolicyGrantDetailProperty(
                    include_child_domain_units=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__243801ca298e871b3ac9738db1312f93297bd30599f91267a6a8b04ba2879168)
                check_type(argname="argument include_child_domain_units", value=include_child_domain_units, expected_type=type_hints["include_child_domain_units"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if include_child_domain_units is not None:
                self._values["include_child_domain_units"] = include_child_domain_units

        @builtins.property
        def include_child_domain_units(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether the policy grant is applied to child domain units.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-createassettypepolicygrantdetail.html#cfn-datazone-policygrant-createassettypepolicygrantdetail-includechilddomainunits
            '''
            result = self._values.get("include_child_domain_units")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CreateAssetTypePolicyGrantDetailProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnPolicyGrantPropsMixin.CreateDomainUnitPolicyGrantDetailProperty",
        jsii_struct_bases=[],
        name_mapping={"include_child_domain_units": "includeChildDomainUnits"},
    )
    class CreateDomainUnitPolicyGrantDetailProperty:
        def __init__(
            self,
            *,
            include_child_domain_units: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The details of the policy grant.

            :param include_child_domain_units: Specifies whether the policy grant is applied to child domain units.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-createdomainunitpolicygrantdetail.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                create_domain_unit_policy_grant_detail_property = datazone_mixins.CfnPolicyGrantPropsMixin.CreateDomainUnitPolicyGrantDetailProperty(
                    include_child_domain_units=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6df3f203ca6db2d8b11a71e0e33152de08d2088936e32249795018cf78f0202a)
                check_type(argname="argument include_child_domain_units", value=include_child_domain_units, expected_type=type_hints["include_child_domain_units"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if include_child_domain_units is not None:
                self._values["include_child_domain_units"] = include_child_domain_units

        @builtins.property
        def include_child_domain_units(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether the policy grant is applied to child domain units.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-createdomainunitpolicygrantdetail.html#cfn-datazone-policygrant-createdomainunitpolicygrantdetail-includechilddomainunits
            '''
            result = self._values.get("include_child_domain_units")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CreateDomainUnitPolicyGrantDetailProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnPolicyGrantPropsMixin.CreateEnvironmentProfilePolicyGrantDetailProperty",
        jsii_struct_bases=[],
        name_mapping={"domain_unit_id": "domainUnitId"},
    )
    class CreateEnvironmentProfilePolicyGrantDetailProperty:
        def __init__(
            self,
            *,
            domain_unit_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The details of the policy grant.

            :param domain_unit_id: The ID of the domain unit.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-createenvironmentprofilepolicygrantdetail.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                create_environment_profile_policy_grant_detail_property = datazone_mixins.CfnPolicyGrantPropsMixin.CreateEnvironmentProfilePolicyGrantDetailProperty(
                    domain_unit_id="domainUnitId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bbab87c353e0aa6608b1d69a3a5622a80cf5a18d2b79d8b4caa9f8305b779b9c)
                check_type(argname="argument domain_unit_id", value=domain_unit_id, expected_type=type_hints["domain_unit_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if domain_unit_id is not None:
                self._values["domain_unit_id"] = domain_unit_id

        @builtins.property
        def domain_unit_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the domain unit.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-createenvironmentprofilepolicygrantdetail.html#cfn-datazone-policygrant-createenvironmentprofilepolicygrantdetail-domainunitid
            '''
            result = self._values.get("domain_unit_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CreateEnvironmentProfilePolicyGrantDetailProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnPolicyGrantPropsMixin.CreateFormTypePolicyGrantDetailProperty",
        jsii_struct_bases=[],
        name_mapping={"include_child_domain_units": "includeChildDomainUnits"},
    )
    class CreateFormTypePolicyGrantDetailProperty:
        def __init__(
            self,
            *,
            include_child_domain_units: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The details of the policy grant.

            :param include_child_domain_units: Specifies whether the policy grant is applied to child domain units.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-createformtypepolicygrantdetail.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                create_form_type_policy_grant_detail_property = datazone_mixins.CfnPolicyGrantPropsMixin.CreateFormTypePolicyGrantDetailProperty(
                    include_child_domain_units=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__507b28dbc0ee9a701d0543da6bb84339a2f8b4949df591fde6c7811d258ce0d1)
                check_type(argname="argument include_child_domain_units", value=include_child_domain_units, expected_type=type_hints["include_child_domain_units"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if include_child_domain_units is not None:
                self._values["include_child_domain_units"] = include_child_domain_units

        @builtins.property
        def include_child_domain_units(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether the policy grant is applied to child domain units.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-createformtypepolicygrantdetail.html#cfn-datazone-policygrant-createformtypepolicygrantdetail-includechilddomainunits
            '''
            result = self._values.get("include_child_domain_units")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CreateFormTypePolicyGrantDetailProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnPolicyGrantPropsMixin.CreateGlossaryPolicyGrantDetailProperty",
        jsii_struct_bases=[],
        name_mapping={"include_child_domain_units": "includeChildDomainUnits"},
    )
    class CreateGlossaryPolicyGrantDetailProperty:
        def __init__(
            self,
            *,
            include_child_domain_units: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The details of the policy grant.

            :param include_child_domain_units: Specifies whether the policy grant is applied to child domain units.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-createglossarypolicygrantdetail.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                create_glossary_policy_grant_detail_property = datazone_mixins.CfnPolicyGrantPropsMixin.CreateGlossaryPolicyGrantDetailProperty(
                    include_child_domain_units=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__df7e46166241996a3abe9a99e0d8453bd021b8f07ed07b6cf63ef67c6466fb89)
                check_type(argname="argument include_child_domain_units", value=include_child_domain_units, expected_type=type_hints["include_child_domain_units"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if include_child_domain_units is not None:
                self._values["include_child_domain_units"] = include_child_domain_units

        @builtins.property
        def include_child_domain_units(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether the policy grant is applied to child domain units.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-createglossarypolicygrantdetail.html#cfn-datazone-policygrant-createglossarypolicygrantdetail-includechilddomainunits
            '''
            result = self._values.get("include_child_domain_units")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CreateGlossaryPolicyGrantDetailProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnPolicyGrantPropsMixin.CreateProjectFromProjectProfilePolicyGrantDetailProperty",
        jsii_struct_bases=[],
        name_mapping={
            "include_child_domain_units": "includeChildDomainUnits",
            "project_profiles": "projectProfiles",
        },
    )
    class CreateProjectFromProjectProfilePolicyGrantDetailProperty:
        def __init__(
            self,
            *,
            include_child_domain_units: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            project_profiles: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Specifies whether to create a project from project profile policy grant details.

            :param include_child_domain_units: Specifies whether to include child domain units when creating a project from project profile policy grant details.
            :param project_profiles: Specifies project profiles when creating a project from project profile policy grant details.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-createprojectfromprojectprofilepolicygrantdetail.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                create_project_from_project_profile_policy_grant_detail_property = datazone_mixins.CfnPolicyGrantPropsMixin.CreateProjectFromProjectProfilePolicyGrantDetailProperty(
                    include_child_domain_units=False,
                    project_profiles=["projectProfiles"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1b747b3565bf4602734c6e9df4e9cb154ae69dea5aa363a0aa4f8f17186df377)
                check_type(argname="argument include_child_domain_units", value=include_child_domain_units, expected_type=type_hints["include_child_domain_units"])
                check_type(argname="argument project_profiles", value=project_profiles, expected_type=type_hints["project_profiles"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if include_child_domain_units is not None:
                self._values["include_child_domain_units"] = include_child_domain_units
            if project_profiles is not None:
                self._values["project_profiles"] = project_profiles

        @builtins.property
        def include_child_domain_units(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether to include child domain units when creating a project from project profile policy grant details.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-createprojectfromprojectprofilepolicygrantdetail.html#cfn-datazone-policygrant-createprojectfromprojectprofilepolicygrantdetail-includechilddomainunits
            '''
            result = self._values.get("include_child_domain_units")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def project_profiles(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Specifies project profiles when creating a project from project profile policy grant details.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-createprojectfromprojectprofilepolicygrantdetail.html#cfn-datazone-policygrant-createprojectfromprojectprofilepolicygrantdetail-projectprofiles
            '''
            result = self._values.get("project_profiles")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CreateProjectFromProjectProfilePolicyGrantDetailProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnPolicyGrantPropsMixin.CreateProjectPolicyGrantDetailProperty",
        jsii_struct_bases=[],
        name_mapping={"include_child_domain_units": "includeChildDomainUnits"},
    )
    class CreateProjectPolicyGrantDetailProperty:
        def __init__(
            self,
            *,
            include_child_domain_units: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The details of the policy grant.

            :param include_child_domain_units: Specifies whether the policy grant is applied to child domain units.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-createprojectpolicygrantdetail.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                create_project_policy_grant_detail_property = datazone_mixins.CfnPolicyGrantPropsMixin.CreateProjectPolicyGrantDetailProperty(
                    include_child_domain_units=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ee429e5e238529a6a47c5e20fd8ebd8e9cce18d783f9578f8442ac1ccae6e579)
                check_type(argname="argument include_child_domain_units", value=include_child_domain_units, expected_type=type_hints["include_child_domain_units"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if include_child_domain_units is not None:
                self._values["include_child_domain_units"] = include_child_domain_units

        @builtins.property
        def include_child_domain_units(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether the policy grant is applied to child domain units.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-createprojectpolicygrantdetail.html#cfn-datazone-policygrant-createprojectpolicygrantdetail-includechilddomainunits
            '''
            result = self._values.get("include_child_domain_units")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CreateProjectPolicyGrantDetailProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnPolicyGrantPropsMixin.DomainUnitFilterForProjectProperty",
        jsii_struct_bases=[],
        name_mapping={
            "domain_unit": "domainUnit",
            "include_child_domain_units": "includeChildDomainUnits",
        },
    )
    class DomainUnitFilterForProjectProperty:
        def __init__(
            self,
            *,
            domain_unit: typing.Optional[builtins.str] = None,
            include_child_domain_units: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The domain unit filter of the project grant filter.

            :param domain_unit: The domain unit ID to use in the filter.
            :param include_child_domain_units: Specifies whether to include child domain units. Default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-domainunitfilterforproject.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                domain_unit_filter_for_project_property = datazone_mixins.CfnPolicyGrantPropsMixin.DomainUnitFilterForProjectProperty(
                    domain_unit="domainUnit",
                    include_child_domain_units=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__639e67758d17d3b0c93d7f0e667a9725c302e51c08b89125ba36a2fabf560ef1)
                check_type(argname="argument domain_unit", value=domain_unit, expected_type=type_hints["domain_unit"])
                check_type(argname="argument include_child_domain_units", value=include_child_domain_units, expected_type=type_hints["include_child_domain_units"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if domain_unit is not None:
                self._values["domain_unit"] = domain_unit
            if include_child_domain_units is not None:
                self._values["include_child_domain_units"] = include_child_domain_units

        @builtins.property
        def domain_unit(self) -> typing.Optional[builtins.str]:
            '''The domain unit ID to use in the filter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-domainunitfilterforproject.html#cfn-datazone-policygrant-domainunitfilterforproject-domainunit
            '''
            result = self._values.get("domain_unit")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def include_child_domain_units(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether to include child domain units.

            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-domainunitfilterforproject.html#cfn-datazone-policygrant-domainunitfilterforproject-includechilddomainunits
            '''
            result = self._values.get("include_child_domain_units")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DomainUnitFilterForProjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnPolicyGrantPropsMixin.DomainUnitGrantFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"all_domain_units_grant_filter": "allDomainUnitsGrantFilter"},
    )
    class DomainUnitGrantFilterProperty:
        def __init__(self, *, all_domain_units_grant_filter: typing.Any = None) -> None:
            '''The grant filter for the domain unit.

            In the current release of Amazon DataZone, the only supported filter is the ``allDomainUnitsGrantFilter`` .

            :param all_domain_units_grant_filter: Specifies a grant filter containing all domain units.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-domainunitgrantfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                # all_domain_units_grant_filter: Any
                
                domain_unit_grant_filter_property = datazone_mixins.CfnPolicyGrantPropsMixin.DomainUnitGrantFilterProperty(
                    all_domain_units_grant_filter=all_domain_units_grant_filter
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cfb3e90fcb84a09ba1197c48526a93d6a739b07d7c81eed661c67802adac95a8)
                check_type(argname="argument all_domain_units_grant_filter", value=all_domain_units_grant_filter, expected_type=type_hints["all_domain_units_grant_filter"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if all_domain_units_grant_filter is not None:
                self._values["all_domain_units_grant_filter"] = all_domain_units_grant_filter

        @builtins.property
        def all_domain_units_grant_filter(self) -> typing.Any:
            '''Specifies a grant filter containing all domain units.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-domainunitgrantfilter.html#cfn-datazone-policygrant-domainunitgrantfilter-alldomainunitsgrantfilter
            '''
            result = self._values.get("all_domain_units_grant_filter")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DomainUnitGrantFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnPolicyGrantPropsMixin.DomainUnitPolicyGrantPrincipalProperty",
        jsii_struct_bases=[],
        name_mapping={
            "domain_unit_designation": "domainUnitDesignation",
            "domain_unit_grant_filter": "domainUnitGrantFilter",
            "domain_unit_identifier": "domainUnitIdentifier",
        },
    )
    class DomainUnitPolicyGrantPrincipalProperty:
        def __init__(
            self,
            *,
            domain_unit_designation: typing.Optional[builtins.str] = None,
            domain_unit_grant_filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPolicyGrantPropsMixin.DomainUnitGrantFilterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            domain_unit_identifier: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The domain unit principal to whom the policy is granted.

            :param domain_unit_designation: Specifes the designation of the domain unit users.
            :param domain_unit_grant_filter: The grant filter for the domain unit.
            :param domain_unit_identifier: The ID of the domain unit.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-domainunitpolicygrantprincipal.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                # all_domain_units_grant_filter: Any
                
                domain_unit_policy_grant_principal_property = datazone_mixins.CfnPolicyGrantPropsMixin.DomainUnitPolicyGrantPrincipalProperty(
                    domain_unit_designation="domainUnitDesignation",
                    domain_unit_grant_filter=datazone_mixins.CfnPolicyGrantPropsMixin.DomainUnitGrantFilterProperty(
                        all_domain_units_grant_filter=all_domain_units_grant_filter
                    ),
                    domain_unit_identifier="domainUnitIdentifier"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__da1bf6d9f26020ea6fe47991b861fd6d2451cc479100ae3e3cd2d8e3daa5fd4a)
                check_type(argname="argument domain_unit_designation", value=domain_unit_designation, expected_type=type_hints["domain_unit_designation"])
                check_type(argname="argument domain_unit_grant_filter", value=domain_unit_grant_filter, expected_type=type_hints["domain_unit_grant_filter"])
                check_type(argname="argument domain_unit_identifier", value=domain_unit_identifier, expected_type=type_hints["domain_unit_identifier"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if domain_unit_designation is not None:
                self._values["domain_unit_designation"] = domain_unit_designation
            if domain_unit_grant_filter is not None:
                self._values["domain_unit_grant_filter"] = domain_unit_grant_filter
            if domain_unit_identifier is not None:
                self._values["domain_unit_identifier"] = domain_unit_identifier

        @builtins.property
        def domain_unit_designation(self) -> typing.Optional[builtins.str]:
            '''Specifes the designation of the domain unit users.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-domainunitpolicygrantprincipal.html#cfn-datazone-policygrant-domainunitpolicygrantprincipal-domainunitdesignation
            '''
            result = self._values.get("domain_unit_designation")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def domain_unit_grant_filter(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyGrantPropsMixin.DomainUnitGrantFilterProperty"]]:
            '''The grant filter for the domain unit.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-domainunitpolicygrantprincipal.html#cfn-datazone-policygrant-domainunitpolicygrantprincipal-domainunitgrantfilter
            '''
            result = self._values.get("domain_unit_grant_filter")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyGrantPropsMixin.DomainUnitGrantFilterProperty"]], result)

        @builtins.property
        def domain_unit_identifier(self) -> typing.Optional[builtins.str]:
            '''The ID of the domain unit.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-domainunitpolicygrantprincipal.html#cfn-datazone-policygrant-domainunitpolicygrantprincipal-domainunitidentifier
            '''
            result = self._values.get("domain_unit_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DomainUnitPolicyGrantPrincipalProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnPolicyGrantPropsMixin.GroupPolicyGrantPrincipalProperty",
        jsii_struct_bases=[],
        name_mapping={"group_identifier": "groupIdentifier"},
    )
    class GroupPolicyGrantPrincipalProperty:
        def __init__(
            self,
            *,
            group_identifier: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The group principal to whom the policy is granted.

            :param group_identifier: The ID Of the group of the group principal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-grouppolicygrantprincipal.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                group_policy_grant_principal_property = datazone_mixins.CfnPolicyGrantPropsMixin.GroupPolicyGrantPrincipalProperty(
                    group_identifier="groupIdentifier"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a6743efcff410080aafa26d1f63db78131ca414a712c1d1b3ab90754466d3ae7)
                check_type(argname="argument group_identifier", value=group_identifier, expected_type=type_hints["group_identifier"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if group_identifier is not None:
                self._values["group_identifier"] = group_identifier

        @builtins.property
        def group_identifier(self) -> typing.Optional[builtins.str]:
            '''The ID Of the group of the group principal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-grouppolicygrantprincipal.html#cfn-datazone-policygrant-grouppolicygrantprincipal-groupidentifier
            '''
            result = self._values.get("group_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GroupPolicyGrantPrincipalProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnPolicyGrantPropsMixin.OverrideDomainUnitOwnersPolicyGrantDetailProperty",
        jsii_struct_bases=[],
        name_mapping={"include_child_domain_units": "includeChildDomainUnits"},
    )
    class OverrideDomainUnitOwnersPolicyGrantDetailProperty:
        def __init__(
            self,
            *,
            include_child_domain_units: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The grant details of the override domain unit owners policy.

            :param include_child_domain_units: Specifies whether the policy is inherited by child domain units.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-overridedomainunitownerspolicygrantdetail.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                override_domain_unit_owners_policy_grant_detail_property = datazone_mixins.CfnPolicyGrantPropsMixin.OverrideDomainUnitOwnersPolicyGrantDetailProperty(
                    include_child_domain_units=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3665c090328a64bbc04304ab819e2b109490babd2f5bfecd4950819c9a815b75)
                check_type(argname="argument include_child_domain_units", value=include_child_domain_units, expected_type=type_hints["include_child_domain_units"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if include_child_domain_units is not None:
                self._values["include_child_domain_units"] = include_child_domain_units

        @builtins.property
        def include_child_domain_units(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether the policy is inherited by child domain units.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-overridedomainunitownerspolicygrantdetail.html#cfn-datazone-policygrant-overridedomainunitownerspolicygrantdetail-includechilddomainunits
            '''
            result = self._values.get("include_child_domain_units")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OverrideDomainUnitOwnersPolicyGrantDetailProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnPolicyGrantPropsMixin.OverrideProjectOwnersPolicyGrantDetailProperty",
        jsii_struct_bases=[],
        name_mapping={"include_child_domain_units": "includeChildDomainUnits"},
    )
    class OverrideProjectOwnersPolicyGrantDetailProperty:
        def __init__(
            self,
            *,
            include_child_domain_units: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The details of the override project owners policy grant.

            :param include_child_domain_units: Specifies whether the policy is inherited by child domain units.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-overrideprojectownerspolicygrantdetail.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                override_project_owners_policy_grant_detail_property = datazone_mixins.CfnPolicyGrantPropsMixin.OverrideProjectOwnersPolicyGrantDetailProperty(
                    include_child_domain_units=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cb431944bc3a0856964b19a0371d2d5b7d1799f1b1156594e3218706ce119f2f)
                check_type(argname="argument include_child_domain_units", value=include_child_domain_units, expected_type=type_hints["include_child_domain_units"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if include_child_domain_units is not None:
                self._values["include_child_domain_units"] = include_child_domain_units

        @builtins.property
        def include_child_domain_units(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether the policy is inherited by child domain units.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-overrideprojectownerspolicygrantdetail.html#cfn-datazone-policygrant-overrideprojectownerspolicygrantdetail-includechilddomainunits
            '''
            result = self._values.get("include_child_domain_units")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OverrideProjectOwnersPolicyGrantDetailProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnPolicyGrantPropsMixin.PolicyGrantDetailProperty",
        jsii_struct_bases=[],
        name_mapping={
            "add_to_project_member_pool": "addToProjectMemberPool",
            "create_asset_type": "createAssetType",
            "create_domain_unit": "createDomainUnit",
            "create_environment": "createEnvironment",
            "create_environment_from_blueprint": "createEnvironmentFromBlueprint",
            "create_environment_profile": "createEnvironmentProfile",
            "create_form_type": "createFormType",
            "create_glossary": "createGlossary",
            "create_project": "createProject",
            "create_project_from_project_profile": "createProjectFromProjectProfile",
            "delegate_create_environment_profile": "delegateCreateEnvironmentProfile",
            "override_domain_unit_owners": "overrideDomainUnitOwners",
            "override_project_owners": "overrideProjectOwners",
        },
    )
    class PolicyGrantDetailProperty:
        def __init__(
            self,
            *,
            add_to_project_member_pool: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPolicyGrantPropsMixin.AddToProjectMemberPoolPolicyGrantDetailProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            create_asset_type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPolicyGrantPropsMixin.CreateAssetTypePolicyGrantDetailProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            create_domain_unit: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPolicyGrantPropsMixin.CreateDomainUnitPolicyGrantDetailProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            create_environment: typing.Any = None,
            create_environment_from_blueprint: typing.Any = None,
            create_environment_profile: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPolicyGrantPropsMixin.CreateEnvironmentProfilePolicyGrantDetailProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            create_form_type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPolicyGrantPropsMixin.CreateFormTypePolicyGrantDetailProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            create_glossary: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPolicyGrantPropsMixin.CreateGlossaryPolicyGrantDetailProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            create_project: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPolicyGrantPropsMixin.CreateProjectPolicyGrantDetailProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            create_project_from_project_profile: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPolicyGrantPropsMixin.CreateProjectFromProjectProfilePolicyGrantDetailProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            delegate_create_environment_profile: typing.Any = None,
            override_domain_unit_owners: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPolicyGrantPropsMixin.OverrideDomainUnitOwnersPolicyGrantDetailProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            override_project_owners: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPolicyGrantPropsMixin.OverrideProjectOwnersPolicyGrantDetailProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The details of the policy grant.

            :param add_to_project_member_pool: Specifies that the policy grant is to be added to the members of the project.
            :param create_asset_type: Specifies that this is a create asset type policy.
            :param create_domain_unit: Specifies that this is a create domain unit policy.
            :param create_environment: Specifies that this is a create environment policy.
            :param create_environment_from_blueprint: The details of the policy of creating an environment.
            :param create_environment_profile: Specifies that this is a create environment profile policy.
            :param create_form_type: Specifies that this is a create form type policy.
            :param create_glossary: Specifies that this is a create glossary policy.
            :param create_project: Specifies that this is a create project policy.
            :param create_project_from_project_profile: Specifies whether to create a project from project profile.
            :param delegate_create_environment_profile: Specifies that this is the delegation of the create environment profile policy.
            :param override_domain_unit_owners: Specifies whether to override domain unit owners.
            :param override_project_owners: Specifies whether to override project owners.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-policygrantdetail.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                # create_environment: Any
                # create_environment_from_blueprint: Any
                # delegate_create_environment_profile: Any
                
                policy_grant_detail_property = datazone_mixins.CfnPolicyGrantPropsMixin.PolicyGrantDetailProperty(
                    add_to_project_member_pool=datazone_mixins.CfnPolicyGrantPropsMixin.AddToProjectMemberPoolPolicyGrantDetailProperty(
                        include_child_domain_units=False
                    ),
                    create_asset_type=datazone_mixins.CfnPolicyGrantPropsMixin.CreateAssetTypePolicyGrantDetailProperty(
                        include_child_domain_units=False
                    ),
                    create_domain_unit=datazone_mixins.CfnPolicyGrantPropsMixin.CreateDomainUnitPolicyGrantDetailProperty(
                        include_child_domain_units=False
                    ),
                    create_environment=create_environment,
                    create_environment_from_blueprint=create_environment_from_blueprint,
                    create_environment_profile=datazone_mixins.CfnPolicyGrantPropsMixin.CreateEnvironmentProfilePolicyGrantDetailProperty(
                        domain_unit_id="domainUnitId"
                    ),
                    create_form_type=datazone_mixins.CfnPolicyGrantPropsMixin.CreateFormTypePolicyGrantDetailProperty(
                        include_child_domain_units=False
                    ),
                    create_glossary=datazone_mixins.CfnPolicyGrantPropsMixin.CreateGlossaryPolicyGrantDetailProperty(
                        include_child_domain_units=False
                    ),
                    create_project=datazone_mixins.CfnPolicyGrantPropsMixin.CreateProjectPolicyGrantDetailProperty(
                        include_child_domain_units=False
                    ),
                    create_project_from_project_profile=datazone_mixins.CfnPolicyGrantPropsMixin.CreateProjectFromProjectProfilePolicyGrantDetailProperty(
                        include_child_domain_units=False,
                        project_profiles=["projectProfiles"]
                    ),
                    delegate_create_environment_profile=delegate_create_environment_profile,
                    override_domain_unit_owners=datazone_mixins.CfnPolicyGrantPropsMixin.OverrideDomainUnitOwnersPolicyGrantDetailProperty(
                        include_child_domain_units=False
                    ),
                    override_project_owners=datazone_mixins.CfnPolicyGrantPropsMixin.OverrideProjectOwnersPolicyGrantDetailProperty(
                        include_child_domain_units=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b33e36591c89ca092629fcca453def5a6f5690d0933de9351691e234842322b6)
                check_type(argname="argument add_to_project_member_pool", value=add_to_project_member_pool, expected_type=type_hints["add_to_project_member_pool"])
                check_type(argname="argument create_asset_type", value=create_asset_type, expected_type=type_hints["create_asset_type"])
                check_type(argname="argument create_domain_unit", value=create_domain_unit, expected_type=type_hints["create_domain_unit"])
                check_type(argname="argument create_environment", value=create_environment, expected_type=type_hints["create_environment"])
                check_type(argname="argument create_environment_from_blueprint", value=create_environment_from_blueprint, expected_type=type_hints["create_environment_from_blueprint"])
                check_type(argname="argument create_environment_profile", value=create_environment_profile, expected_type=type_hints["create_environment_profile"])
                check_type(argname="argument create_form_type", value=create_form_type, expected_type=type_hints["create_form_type"])
                check_type(argname="argument create_glossary", value=create_glossary, expected_type=type_hints["create_glossary"])
                check_type(argname="argument create_project", value=create_project, expected_type=type_hints["create_project"])
                check_type(argname="argument create_project_from_project_profile", value=create_project_from_project_profile, expected_type=type_hints["create_project_from_project_profile"])
                check_type(argname="argument delegate_create_environment_profile", value=delegate_create_environment_profile, expected_type=type_hints["delegate_create_environment_profile"])
                check_type(argname="argument override_domain_unit_owners", value=override_domain_unit_owners, expected_type=type_hints["override_domain_unit_owners"])
                check_type(argname="argument override_project_owners", value=override_project_owners, expected_type=type_hints["override_project_owners"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if add_to_project_member_pool is not None:
                self._values["add_to_project_member_pool"] = add_to_project_member_pool
            if create_asset_type is not None:
                self._values["create_asset_type"] = create_asset_type
            if create_domain_unit is not None:
                self._values["create_domain_unit"] = create_domain_unit
            if create_environment is not None:
                self._values["create_environment"] = create_environment
            if create_environment_from_blueprint is not None:
                self._values["create_environment_from_blueprint"] = create_environment_from_blueprint
            if create_environment_profile is not None:
                self._values["create_environment_profile"] = create_environment_profile
            if create_form_type is not None:
                self._values["create_form_type"] = create_form_type
            if create_glossary is not None:
                self._values["create_glossary"] = create_glossary
            if create_project is not None:
                self._values["create_project"] = create_project
            if create_project_from_project_profile is not None:
                self._values["create_project_from_project_profile"] = create_project_from_project_profile
            if delegate_create_environment_profile is not None:
                self._values["delegate_create_environment_profile"] = delegate_create_environment_profile
            if override_domain_unit_owners is not None:
                self._values["override_domain_unit_owners"] = override_domain_unit_owners
            if override_project_owners is not None:
                self._values["override_project_owners"] = override_project_owners

        @builtins.property
        def add_to_project_member_pool(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyGrantPropsMixin.AddToProjectMemberPoolPolicyGrantDetailProperty"]]:
            '''Specifies that the policy grant is to be added to the members of the project.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-policygrantdetail.html#cfn-datazone-policygrant-policygrantdetail-addtoprojectmemberpool
            '''
            result = self._values.get("add_to_project_member_pool")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyGrantPropsMixin.AddToProjectMemberPoolPolicyGrantDetailProperty"]], result)

        @builtins.property
        def create_asset_type(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyGrantPropsMixin.CreateAssetTypePolicyGrantDetailProperty"]]:
            '''Specifies that this is a create asset type policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-policygrantdetail.html#cfn-datazone-policygrant-policygrantdetail-createassettype
            '''
            result = self._values.get("create_asset_type")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyGrantPropsMixin.CreateAssetTypePolicyGrantDetailProperty"]], result)

        @builtins.property
        def create_domain_unit(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyGrantPropsMixin.CreateDomainUnitPolicyGrantDetailProperty"]]:
            '''Specifies that this is a create domain unit policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-policygrantdetail.html#cfn-datazone-policygrant-policygrantdetail-createdomainunit
            '''
            result = self._values.get("create_domain_unit")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyGrantPropsMixin.CreateDomainUnitPolicyGrantDetailProperty"]], result)

        @builtins.property
        def create_environment(self) -> typing.Any:
            '''Specifies that this is a create environment policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-policygrantdetail.html#cfn-datazone-policygrant-policygrantdetail-createenvironment
            '''
            result = self._values.get("create_environment")
            return typing.cast(typing.Any, result)

        @builtins.property
        def create_environment_from_blueprint(self) -> typing.Any:
            '''The details of the policy of creating an environment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-policygrantdetail.html#cfn-datazone-policygrant-policygrantdetail-createenvironmentfromblueprint
            '''
            result = self._values.get("create_environment_from_blueprint")
            return typing.cast(typing.Any, result)

        @builtins.property
        def create_environment_profile(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyGrantPropsMixin.CreateEnvironmentProfilePolicyGrantDetailProperty"]]:
            '''Specifies that this is a create environment profile policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-policygrantdetail.html#cfn-datazone-policygrant-policygrantdetail-createenvironmentprofile
            '''
            result = self._values.get("create_environment_profile")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyGrantPropsMixin.CreateEnvironmentProfilePolicyGrantDetailProperty"]], result)

        @builtins.property
        def create_form_type(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyGrantPropsMixin.CreateFormTypePolicyGrantDetailProperty"]]:
            '''Specifies that this is a create form type policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-policygrantdetail.html#cfn-datazone-policygrant-policygrantdetail-createformtype
            '''
            result = self._values.get("create_form_type")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyGrantPropsMixin.CreateFormTypePolicyGrantDetailProperty"]], result)

        @builtins.property
        def create_glossary(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyGrantPropsMixin.CreateGlossaryPolicyGrantDetailProperty"]]:
            '''Specifies that this is a create glossary policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-policygrantdetail.html#cfn-datazone-policygrant-policygrantdetail-createglossary
            '''
            result = self._values.get("create_glossary")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyGrantPropsMixin.CreateGlossaryPolicyGrantDetailProperty"]], result)

        @builtins.property
        def create_project(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyGrantPropsMixin.CreateProjectPolicyGrantDetailProperty"]]:
            '''Specifies that this is a create project policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-policygrantdetail.html#cfn-datazone-policygrant-policygrantdetail-createproject
            '''
            result = self._values.get("create_project")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyGrantPropsMixin.CreateProjectPolicyGrantDetailProperty"]], result)

        @builtins.property
        def create_project_from_project_profile(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyGrantPropsMixin.CreateProjectFromProjectProfilePolicyGrantDetailProperty"]]:
            '''Specifies whether to create a project from project profile.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-policygrantdetail.html#cfn-datazone-policygrant-policygrantdetail-createprojectfromprojectprofile
            '''
            result = self._values.get("create_project_from_project_profile")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyGrantPropsMixin.CreateProjectFromProjectProfilePolicyGrantDetailProperty"]], result)

        @builtins.property
        def delegate_create_environment_profile(self) -> typing.Any:
            '''Specifies that this is the delegation of the create environment profile policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-policygrantdetail.html#cfn-datazone-policygrant-policygrantdetail-delegatecreateenvironmentprofile
            '''
            result = self._values.get("delegate_create_environment_profile")
            return typing.cast(typing.Any, result)

        @builtins.property
        def override_domain_unit_owners(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyGrantPropsMixin.OverrideDomainUnitOwnersPolicyGrantDetailProperty"]]:
            '''Specifies whether to override domain unit owners.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-policygrantdetail.html#cfn-datazone-policygrant-policygrantdetail-overridedomainunitowners
            '''
            result = self._values.get("override_domain_unit_owners")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyGrantPropsMixin.OverrideDomainUnitOwnersPolicyGrantDetailProperty"]], result)

        @builtins.property
        def override_project_owners(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyGrantPropsMixin.OverrideProjectOwnersPolicyGrantDetailProperty"]]:
            '''Specifies whether to override project owners.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-policygrantdetail.html#cfn-datazone-policygrant-policygrantdetail-overrideprojectowners
            '''
            result = self._values.get("override_project_owners")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyGrantPropsMixin.OverrideProjectOwnersPolicyGrantDetailProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PolicyGrantDetailProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnPolicyGrantPropsMixin.PolicyGrantPrincipalProperty",
        jsii_struct_bases=[],
        name_mapping={
            "domain_unit": "domainUnit",
            "group": "group",
            "project": "project",
            "user": "user",
        },
    )
    class PolicyGrantPrincipalProperty:
        def __init__(
            self,
            *,
            domain_unit: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPolicyGrantPropsMixin.DomainUnitPolicyGrantPrincipalProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            group: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPolicyGrantPropsMixin.GroupPolicyGrantPrincipalProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            project: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPolicyGrantPropsMixin.ProjectPolicyGrantPrincipalProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            user: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPolicyGrantPropsMixin.UserPolicyGrantPrincipalProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The policy grant principal.

            :param domain_unit: The domain unit of the policy grant principal.
            :param group: The group of the policy grant principal.
            :param project: The project of the policy grant principal.
            :param user: The user of the policy grant principal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-policygrantprincipal.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                # all_domain_units_grant_filter: Any
                # all_users_grant_filter: Any
                
                policy_grant_principal_property = datazone_mixins.CfnPolicyGrantPropsMixin.PolicyGrantPrincipalProperty(
                    domain_unit=datazone_mixins.CfnPolicyGrantPropsMixin.DomainUnitPolicyGrantPrincipalProperty(
                        domain_unit_designation="domainUnitDesignation",
                        domain_unit_grant_filter=datazone_mixins.CfnPolicyGrantPropsMixin.DomainUnitGrantFilterProperty(
                            all_domain_units_grant_filter=all_domain_units_grant_filter
                        ),
                        domain_unit_identifier="domainUnitIdentifier"
                    ),
                    group=datazone_mixins.CfnPolicyGrantPropsMixin.GroupPolicyGrantPrincipalProperty(
                        group_identifier="groupIdentifier"
                    ),
                    project=datazone_mixins.CfnPolicyGrantPropsMixin.ProjectPolicyGrantPrincipalProperty(
                        project_designation="projectDesignation",
                        project_grant_filter=datazone_mixins.CfnPolicyGrantPropsMixin.ProjectGrantFilterProperty(
                            domain_unit_filter=datazone_mixins.CfnPolicyGrantPropsMixin.DomainUnitFilterForProjectProperty(
                                domain_unit="domainUnit",
                                include_child_domain_units=False
                            )
                        ),
                        project_identifier="projectIdentifier"
                    ),
                    user=datazone_mixins.CfnPolicyGrantPropsMixin.UserPolicyGrantPrincipalProperty(
                        all_users_grant_filter=all_users_grant_filter,
                        user_identifier="userIdentifier"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4aa7abdddb67c265dbef959d13e6781120c69fb15e47b2dc2dfde43822b8fb4f)
                check_type(argname="argument domain_unit", value=domain_unit, expected_type=type_hints["domain_unit"])
                check_type(argname="argument group", value=group, expected_type=type_hints["group"])
                check_type(argname="argument project", value=project, expected_type=type_hints["project"])
                check_type(argname="argument user", value=user, expected_type=type_hints["user"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if domain_unit is not None:
                self._values["domain_unit"] = domain_unit
            if group is not None:
                self._values["group"] = group
            if project is not None:
                self._values["project"] = project
            if user is not None:
                self._values["user"] = user

        @builtins.property
        def domain_unit(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyGrantPropsMixin.DomainUnitPolicyGrantPrincipalProperty"]]:
            '''The domain unit of the policy grant principal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-policygrantprincipal.html#cfn-datazone-policygrant-policygrantprincipal-domainunit
            '''
            result = self._values.get("domain_unit")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyGrantPropsMixin.DomainUnitPolicyGrantPrincipalProperty"]], result)

        @builtins.property
        def group(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyGrantPropsMixin.GroupPolicyGrantPrincipalProperty"]]:
            '''The group of the policy grant principal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-policygrantprincipal.html#cfn-datazone-policygrant-policygrantprincipal-group
            '''
            result = self._values.get("group")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyGrantPropsMixin.GroupPolicyGrantPrincipalProperty"]], result)

        @builtins.property
        def project(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyGrantPropsMixin.ProjectPolicyGrantPrincipalProperty"]]:
            '''The project of the policy grant principal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-policygrantprincipal.html#cfn-datazone-policygrant-policygrantprincipal-project
            '''
            result = self._values.get("project")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyGrantPropsMixin.ProjectPolicyGrantPrincipalProperty"]], result)

        @builtins.property
        def user(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyGrantPropsMixin.UserPolicyGrantPrincipalProperty"]]:
            '''The user of the policy grant principal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-policygrantprincipal.html#cfn-datazone-policygrant-policygrantprincipal-user
            '''
            result = self._values.get("user")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyGrantPropsMixin.UserPolicyGrantPrincipalProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PolicyGrantPrincipalProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnPolicyGrantPropsMixin.ProjectGrantFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"domain_unit_filter": "domainUnitFilter"},
    )
    class ProjectGrantFilterProperty:
        def __init__(
            self,
            *,
            domain_unit_filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPolicyGrantPropsMixin.DomainUnitFilterForProjectProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The project grant filter.

            :param domain_unit_filter: The domain unit filter of the project grant filter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-projectgrantfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                project_grant_filter_property = datazone_mixins.CfnPolicyGrantPropsMixin.ProjectGrantFilterProperty(
                    domain_unit_filter=datazone_mixins.CfnPolicyGrantPropsMixin.DomainUnitFilterForProjectProperty(
                        domain_unit="domainUnit",
                        include_child_domain_units=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9c3606b596404821a6fc53ec77e9d5b5b969fb655c0f157ca9b25f02e6f875ca)
                check_type(argname="argument domain_unit_filter", value=domain_unit_filter, expected_type=type_hints["domain_unit_filter"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if domain_unit_filter is not None:
                self._values["domain_unit_filter"] = domain_unit_filter

        @builtins.property
        def domain_unit_filter(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyGrantPropsMixin.DomainUnitFilterForProjectProperty"]]:
            '''The domain unit filter of the project grant filter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-projectgrantfilter.html#cfn-datazone-policygrant-projectgrantfilter-domainunitfilter
            '''
            result = self._values.get("domain_unit_filter")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyGrantPropsMixin.DomainUnitFilterForProjectProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProjectGrantFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnPolicyGrantPropsMixin.ProjectPolicyGrantPrincipalProperty",
        jsii_struct_bases=[],
        name_mapping={
            "project_designation": "projectDesignation",
            "project_grant_filter": "projectGrantFilter",
            "project_identifier": "projectIdentifier",
        },
    )
    class ProjectPolicyGrantPrincipalProperty:
        def __init__(
            self,
            *,
            project_designation: typing.Optional[builtins.str] = None,
            project_grant_filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPolicyGrantPropsMixin.ProjectGrantFilterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            project_identifier: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The project policy grant principal.

            :param project_designation: The project designation of the project policy grant principal.
            :param project_grant_filter: The project grant filter of the project policy grant principal.
            :param project_identifier: The project ID of the project policy grant principal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-projectpolicygrantprincipal.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                project_policy_grant_principal_property = datazone_mixins.CfnPolicyGrantPropsMixin.ProjectPolicyGrantPrincipalProperty(
                    project_designation="projectDesignation",
                    project_grant_filter=datazone_mixins.CfnPolicyGrantPropsMixin.ProjectGrantFilterProperty(
                        domain_unit_filter=datazone_mixins.CfnPolicyGrantPropsMixin.DomainUnitFilterForProjectProperty(
                            domain_unit="domainUnit",
                            include_child_domain_units=False
                        )
                    ),
                    project_identifier="projectIdentifier"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7d8b44e11106274b2b5a2f972cd76f511340a8eef2c67b2a1606964df7403c91)
                check_type(argname="argument project_designation", value=project_designation, expected_type=type_hints["project_designation"])
                check_type(argname="argument project_grant_filter", value=project_grant_filter, expected_type=type_hints["project_grant_filter"])
                check_type(argname="argument project_identifier", value=project_identifier, expected_type=type_hints["project_identifier"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if project_designation is not None:
                self._values["project_designation"] = project_designation
            if project_grant_filter is not None:
                self._values["project_grant_filter"] = project_grant_filter
            if project_identifier is not None:
                self._values["project_identifier"] = project_identifier

        @builtins.property
        def project_designation(self) -> typing.Optional[builtins.str]:
            '''The project designation of the project policy grant principal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-projectpolicygrantprincipal.html#cfn-datazone-policygrant-projectpolicygrantprincipal-projectdesignation
            '''
            result = self._values.get("project_designation")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def project_grant_filter(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyGrantPropsMixin.ProjectGrantFilterProperty"]]:
            '''The project grant filter of the project policy grant principal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-projectpolicygrantprincipal.html#cfn-datazone-policygrant-projectpolicygrantprincipal-projectgrantfilter
            '''
            result = self._values.get("project_grant_filter")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyGrantPropsMixin.ProjectGrantFilterProperty"]], result)

        @builtins.property
        def project_identifier(self) -> typing.Optional[builtins.str]:
            '''The project ID of the project policy grant principal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-projectpolicygrantprincipal.html#cfn-datazone-policygrant-projectpolicygrantprincipal-projectidentifier
            '''
            result = self._values.get("project_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProjectPolicyGrantPrincipalProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnPolicyGrantPropsMixin.UserPolicyGrantPrincipalProperty",
        jsii_struct_bases=[],
        name_mapping={
            "all_users_grant_filter": "allUsersGrantFilter",
            "user_identifier": "userIdentifier",
        },
    )
    class UserPolicyGrantPrincipalProperty:
        def __init__(
            self,
            *,
            all_users_grant_filter: typing.Any = None,
            user_identifier: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The user policy grant principal.

            :param all_users_grant_filter: The all users grant filter of the user policy grant principal.
            :param user_identifier: The user ID of the user policy grant principal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-userpolicygrantprincipal.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                # all_users_grant_filter: Any
                
                user_policy_grant_principal_property = datazone_mixins.CfnPolicyGrantPropsMixin.UserPolicyGrantPrincipalProperty(
                    all_users_grant_filter=all_users_grant_filter,
                    user_identifier="userIdentifier"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__809b5d4b5d74b4f35c7a251183b45371c0443a7e8641a35e6029d9711b3e2145)
                check_type(argname="argument all_users_grant_filter", value=all_users_grant_filter, expected_type=type_hints["all_users_grant_filter"])
                check_type(argname="argument user_identifier", value=user_identifier, expected_type=type_hints["user_identifier"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if all_users_grant_filter is not None:
                self._values["all_users_grant_filter"] = all_users_grant_filter
            if user_identifier is not None:
                self._values["user_identifier"] = user_identifier

        @builtins.property
        def all_users_grant_filter(self) -> typing.Any:
            '''The all users grant filter of the user policy grant principal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-userpolicygrantprincipal.html#cfn-datazone-policygrant-userpolicygrantprincipal-allusersgrantfilter
            '''
            result = self._values.get("all_users_grant_filter")
            return typing.cast(typing.Any, result)

        @builtins.property
        def user_identifier(self) -> typing.Optional[builtins.str]:
            '''The user ID of the user policy grant principal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-policygrant-userpolicygrantprincipal.html#cfn-datazone-policygrant-userpolicygrantprincipal-useridentifier
            '''
            result = self._values.get("user_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UserPolicyGrantPrincipalProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnProjectMembershipMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "designation": "designation",
        "domain_identifier": "domainIdentifier",
        "member": "member",
        "project_identifier": "projectIdentifier",
    },
)
class CfnProjectMembershipMixinProps:
    def __init__(
        self,
        *,
        designation: typing.Optional[builtins.str] = None,
        domain_identifier: typing.Optional[builtins.str] = None,
        member: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProjectMembershipPropsMixin.MemberProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        project_identifier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnProjectMembershipPropsMixin.

        :param designation: The designated role of a project member.
        :param domain_identifier: The ID of the Amazon DataZone domain in which project membership is created.
        :param member: The details about a project member.
        :param project_identifier: The ID of the project for which this project membership was created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-projectmembership.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
            
            cfn_project_membership_mixin_props = datazone_mixins.CfnProjectMembershipMixinProps(
                designation="designation",
                domain_identifier="domainIdentifier",
                member=datazone_mixins.CfnProjectMembershipPropsMixin.MemberProperty(
                    group_identifier="groupIdentifier",
                    user_identifier="userIdentifier"
                ),
                project_identifier="projectIdentifier"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f5703f431726287b0868836e521692ce54a41a9ed4d188f40bd4289b641bb2d)
            check_type(argname="argument designation", value=designation, expected_type=type_hints["designation"])
            check_type(argname="argument domain_identifier", value=domain_identifier, expected_type=type_hints["domain_identifier"])
            check_type(argname="argument member", value=member, expected_type=type_hints["member"])
            check_type(argname="argument project_identifier", value=project_identifier, expected_type=type_hints["project_identifier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if designation is not None:
            self._values["designation"] = designation
        if domain_identifier is not None:
            self._values["domain_identifier"] = domain_identifier
        if member is not None:
            self._values["member"] = member
        if project_identifier is not None:
            self._values["project_identifier"] = project_identifier

    @builtins.property
    def designation(self) -> typing.Optional[builtins.str]:
        '''The designated role of a project member.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-projectmembership.html#cfn-datazone-projectmembership-designation
        '''
        result = self._values.get("designation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_identifier(self) -> typing.Optional[builtins.str]:
        '''The ID of the Amazon DataZone domain in which project membership is created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-projectmembership.html#cfn-datazone-projectmembership-domainidentifier
        '''
        result = self._values.get("domain_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def member(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectMembershipPropsMixin.MemberProperty"]]:
        '''The details about a project member.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-projectmembership.html#cfn-datazone-projectmembership-member
        '''
        result = self._values.get("member")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectMembershipPropsMixin.MemberProperty"]], result)

    @builtins.property
    def project_identifier(self) -> typing.Optional[builtins.str]:
        '''The ID of the project for which this project membership was created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-projectmembership.html#cfn-datazone-projectmembership-projectidentifier
        '''
        result = self._values.get("project_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnProjectMembershipMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnProjectMembershipPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnProjectMembershipPropsMixin",
):
    '''The ``AWS::DataZone::ProjectMembership`` resource adds a member to an Amazon DataZone project.

    Project members consume assets from the Amazon DataZone catalog and produce new assets using one or more analytical workflows.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-projectmembership.html
    :cloudformationResource: AWS::DataZone::ProjectMembership
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
        
        cfn_project_membership_props_mixin = datazone_mixins.CfnProjectMembershipPropsMixin(datazone_mixins.CfnProjectMembershipMixinProps(
            designation="designation",
            domain_identifier="domainIdentifier",
            member=datazone_mixins.CfnProjectMembershipPropsMixin.MemberProperty(
                group_identifier="groupIdentifier",
                user_identifier="userIdentifier"
            ),
            project_identifier="projectIdentifier"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnProjectMembershipMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DataZone::ProjectMembership``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f92c3693329474bc4aac8680ce6ca5fcb3ff6e0bff4fffb012f3dabbdbcac1e6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b34100031a4e0dcb69b9a86fff2bb0a0fcc1584c94899f75b077f0a550d3fdf0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f717494b229fa7ea3ab3ad432a0d071525df35124fcf03011ed9d67a987b4ed4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnProjectMembershipMixinProps:
        return typing.cast(CfnProjectMembershipMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnProjectMembershipPropsMixin.MemberProperty",
        jsii_struct_bases=[],
        name_mapping={
            "group_identifier": "groupIdentifier",
            "user_identifier": "userIdentifier",
        },
    )
    class MemberProperty:
        def __init__(
            self,
            *,
            group_identifier: typing.Optional[builtins.str] = None,
            user_identifier: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The details about a project member.

            Important - this data type is a UNION, so only one of the following members can be specified when used or returned.

            :param group_identifier: The ID of the group of a project member.
            :param user_identifier: The user ID of a project member.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-projectmembership-member.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                member_property = datazone_mixins.CfnProjectMembershipPropsMixin.MemberProperty(
                    group_identifier="groupIdentifier",
                    user_identifier="userIdentifier"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4a800caa33ff96a0011456db73ca977b03b79bab8a26066b84a77fd652d5ec93)
                check_type(argname="argument group_identifier", value=group_identifier, expected_type=type_hints["group_identifier"])
                check_type(argname="argument user_identifier", value=user_identifier, expected_type=type_hints["user_identifier"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if group_identifier is not None:
                self._values["group_identifier"] = group_identifier
            if user_identifier is not None:
                self._values["user_identifier"] = user_identifier

        @builtins.property
        def group_identifier(self) -> typing.Optional[builtins.str]:
            '''The ID of the group of a project member.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-projectmembership-member.html#cfn-datazone-projectmembership-member-groupidentifier
            '''
            result = self._values.get("group_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user_identifier(self) -> typing.Optional[builtins.str]:
            '''The user ID of a project member.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-projectmembership-member.html#cfn-datazone-projectmembership-member-useridentifier
            '''
            result = self._values.get("user_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MemberProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnProjectMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "domain_identifier": "domainIdentifier",
        "domain_unit_id": "domainUnitId",
        "glossary_terms": "glossaryTerms",
        "name": "name",
        "project_profile_id": "projectProfileId",
        "project_profile_version": "projectProfileVersion",
        "user_parameters": "userParameters",
    },
)
class CfnProjectMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        domain_identifier: typing.Optional[builtins.str] = None,
        domain_unit_id: typing.Optional[builtins.str] = None,
        glossary_terms: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        project_profile_id: typing.Optional[builtins.str] = None,
        project_profile_version: typing.Optional[builtins.str] = None,
        user_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProjectPropsMixin.EnvironmentConfigurationUserParameterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnProjectPropsMixin.

        :param description: The description of a project.
        :param domain_identifier: The identifier of a Amazon DataZone domain where the project exists.
        :param domain_unit_id: The ID of the domain unit. This parameter is not required and if it is not specified, then the project is created at the root domain unit level.
        :param glossary_terms: The glossary terms that can be used in this Amazon DataZone project.
        :param name: The name of a project.
        :param project_profile_id: The ID of the project profile.
        :param project_profile_version: The project profile version to which the project should be updated. You can only specify the following string for this parameter: ``latest`` .
        :param user_parameters: The user parameters of the project.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-project.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
            
            cfn_project_mixin_props = datazone_mixins.CfnProjectMixinProps(
                description="description",
                domain_identifier="domainIdentifier",
                domain_unit_id="domainUnitId",
                glossary_terms=["glossaryTerms"],
                name="name",
                project_profile_id="projectProfileId",
                project_profile_version="projectProfileVersion",
                user_parameters=[datazone_mixins.CfnProjectPropsMixin.EnvironmentConfigurationUserParameterProperty(
                    environment_configuration_name="environmentConfigurationName",
                    environment_id="environmentId",
                    environment_parameters=[datazone_mixins.CfnProjectPropsMixin.EnvironmentParameterProperty(
                        name="name",
                        value="value"
                    )]
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dab82cb125a933cae2e48ac97bd712614fcfba86981f53f5c0d309a555246836)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument domain_identifier", value=domain_identifier, expected_type=type_hints["domain_identifier"])
            check_type(argname="argument domain_unit_id", value=domain_unit_id, expected_type=type_hints["domain_unit_id"])
            check_type(argname="argument glossary_terms", value=glossary_terms, expected_type=type_hints["glossary_terms"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument project_profile_id", value=project_profile_id, expected_type=type_hints["project_profile_id"])
            check_type(argname="argument project_profile_version", value=project_profile_version, expected_type=type_hints["project_profile_version"])
            check_type(argname="argument user_parameters", value=user_parameters, expected_type=type_hints["user_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if domain_identifier is not None:
            self._values["domain_identifier"] = domain_identifier
        if domain_unit_id is not None:
            self._values["domain_unit_id"] = domain_unit_id
        if glossary_terms is not None:
            self._values["glossary_terms"] = glossary_terms
        if name is not None:
            self._values["name"] = name
        if project_profile_id is not None:
            self._values["project_profile_id"] = project_profile_id
        if project_profile_version is not None:
            self._values["project_profile_version"] = project_profile_version
        if user_parameters is not None:
            self._values["user_parameters"] = user_parameters

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of a project.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-project.html#cfn-datazone-project-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_identifier(self) -> typing.Optional[builtins.str]:
        '''The identifier of a Amazon DataZone domain where the project exists.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-project.html#cfn-datazone-project-domainidentifier
        '''
        result = self._values.get("domain_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_unit_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the domain unit.

        This parameter is not required and if it is not specified, then the project is created at the root domain unit level.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-project.html#cfn-datazone-project-domainunitid
        '''
        result = self._values.get("domain_unit_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def glossary_terms(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The glossary terms that can be used in this Amazon DataZone project.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-project.html#cfn-datazone-project-glossaryterms
        '''
        result = self._values.get("glossary_terms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of a project.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-project.html#cfn-datazone-project-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_profile_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the project profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-project.html#cfn-datazone-project-projectprofileid
        '''
        result = self._values.get("project_profile_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_profile_version(self) -> typing.Optional[builtins.str]:
        '''The project profile version to which the project should be updated.

        You can only specify the following string for this parameter: ``latest`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-project.html#cfn-datazone-project-projectprofileversion
        '''
        result = self._values.get("project_profile_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_parameters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.EnvironmentConfigurationUserParameterProperty"]]]]:
        '''The user parameters of the project.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-project.html#cfn-datazone-project-userparameters
        '''
        result = self._values.get("user_parameters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.EnvironmentConfigurationUserParameterProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnProjectMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnProjectProfileMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "domain_identifier": "domainIdentifier",
        "domain_unit_identifier": "domainUnitIdentifier",
        "environment_configurations": "environmentConfigurations",
        "name": "name",
        "status": "status",
    },
)
class CfnProjectProfileMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        domain_identifier: typing.Optional[builtins.str] = None,
        domain_unit_identifier: typing.Optional[builtins.str] = None,
        environment_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProjectProfilePropsMixin.EnvironmentConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        name: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnProjectProfilePropsMixin.

        :param description: The description of the project profile.
        :param domain_identifier: A domain ID of the project profile.
        :param domain_unit_identifier: A domain unit ID of the project profile.
        :param environment_configurations: Environment configurations of a project profile.
        :param name: The name of a project profile.
        :param status: The status of a project profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-projectprofile.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
            
            cfn_project_profile_mixin_props = datazone_mixins.CfnProjectProfileMixinProps(
                description="description",
                domain_identifier="domainIdentifier",
                domain_unit_identifier="domainUnitIdentifier",
                environment_configurations=[datazone_mixins.CfnProjectProfilePropsMixin.EnvironmentConfigurationProperty(
                    aws_account=datazone_mixins.CfnProjectProfilePropsMixin.AwsAccountProperty(
                        aws_account_id="awsAccountId"
                    ),
                    aws_region=datazone_mixins.CfnProjectProfilePropsMixin.RegionProperty(
                        region_name="regionName"
                    ),
                    configuration_parameters=datazone_mixins.CfnProjectProfilePropsMixin.EnvironmentConfigurationParametersDetailsProperty(
                        parameter_overrides=[datazone_mixins.CfnProjectProfilePropsMixin.EnvironmentConfigurationParameterProperty(
                            is_editable=False,
                            name="name",
                            value="value"
                        )],
                        resolved_parameters=[datazone_mixins.CfnProjectProfilePropsMixin.EnvironmentConfigurationParameterProperty(
                            is_editable=False,
                            name="name",
                            value="value"
                        )],
                        ssm_path="ssmPath"
                    ),
                    deployment_mode="deploymentMode",
                    deployment_order=123,
                    description="description",
                    environment_blueprint_id="environmentBlueprintId",
                    environment_configuration_id="environmentConfigurationId",
                    name="name"
                )],
                name="name",
                status="status"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a81c5cc9dac80cb482163a48cd33f4a24739c194a1165bbd0dd5f860d9eb087)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument domain_identifier", value=domain_identifier, expected_type=type_hints["domain_identifier"])
            check_type(argname="argument domain_unit_identifier", value=domain_unit_identifier, expected_type=type_hints["domain_unit_identifier"])
            check_type(argname="argument environment_configurations", value=environment_configurations, expected_type=type_hints["environment_configurations"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if domain_identifier is not None:
            self._values["domain_identifier"] = domain_identifier
        if domain_unit_identifier is not None:
            self._values["domain_unit_identifier"] = domain_unit_identifier
        if environment_configurations is not None:
            self._values["environment_configurations"] = environment_configurations
        if name is not None:
            self._values["name"] = name
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the project profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-projectprofile.html#cfn-datazone-projectprofile-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_identifier(self) -> typing.Optional[builtins.str]:
        '''A domain ID of the project profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-projectprofile.html#cfn-datazone-projectprofile-domainidentifier
        '''
        result = self._values.get("domain_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_unit_identifier(self) -> typing.Optional[builtins.str]:
        '''A domain unit ID of the project profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-projectprofile.html#cfn-datazone-projectprofile-domainunitidentifier
        '''
        result = self._values.get("domain_unit_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_configurations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectProfilePropsMixin.EnvironmentConfigurationProperty"]]]]:
        '''Environment configurations of a project profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-projectprofile.html#cfn-datazone-projectprofile-environmentconfigurations
        '''
        result = self._values.get("environment_configurations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectProfilePropsMixin.EnvironmentConfigurationProperty"]]]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of a project profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-projectprofile.html#cfn-datazone-projectprofile-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''The status of a project profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-projectprofile.html#cfn-datazone-projectprofile-status
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnProjectProfileMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnProjectProfilePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnProjectProfilePropsMixin",
):
    '''The summary of a project profile.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-projectprofile.html
    :cloudformationResource: AWS::DataZone::ProjectProfile
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
        
        cfn_project_profile_props_mixin = datazone_mixins.CfnProjectProfilePropsMixin(datazone_mixins.CfnProjectProfileMixinProps(
            description="description",
            domain_identifier="domainIdentifier",
            domain_unit_identifier="domainUnitIdentifier",
            environment_configurations=[datazone_mixins.CfnProjectProfilePropsMixin.EnvironmentConfigurationProperty(
                aws_account=datazone_mixins.CfnProjectProfilePropsMixin.AwsAccountProperty(
                    aws_account_id="awsAccountId"
                ),
                aws_region=datazone_mixins.CfnProjectProfilePropsMixin.RegionProperty(
                    region_name="regionName"
                ),
                configuration_parameters=datazone_mixins.CfnProjectProfilePropsMixin.EnvironmentConfigurationParametersDetailsProperty(
                    parameter_overrides=[datazone_mixins.CfnProjectProfilePropsMixin.EnvironmentConfigurationParameterProperty(
                        is_editable=False,
                        name="name",
                        value="value"
                    )],
                    resolved_parameters=[datazone_mixins.CfnProjectProfilePropsMixin.EnvironmentConfigurationParameterProperty(
                        is_editable=False,
                        name="name",
                        value="value"
                    )],
                    ssm_path="ssmPath"
                ),
                deployment_mode="deploymentMode",
                deployment_order=123,
                description="description",
                environment_blueprint_id="environmentBlueprintId",
                environment_configuration_id="environmentConfigurationId",
                name="name"
            )],
            name="name",
            status="status"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnProjectProfileMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DataZone::ProjectProfile``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12b3bc78ba483281a971617a16ffcd6afb35dd5209fbeccaedb0a655ff02db04)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc131c07dc28b8be4016b8f1fe0dd7eb5a915bf40add412530da55140e222dfe)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fd1099f8954b7ea0d8dd0640a67ca8844e99be0d6eb4c39a14d87b345a267ca)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnProjectProfileMixinProps:
        return typing.cast(CfnProjectProfileMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnProjectProfilePropsMixin.AwsAccountProperty",
        jsii_struct_bases=[],
        name_mapping={"aws_account_id": "awsAccountId"},
    )
    class AwsAccountProperty:
        def __init__(
            self,
            *,
            aws_account_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The AWS account of the environment.

            :param aws_account_id: The account ID of a project.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-projectprofile-awsaccount.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                aws_account_property = datazone_mixins.CfnProjectProfilePropsMixin.AwsAccountProperty(
                    aws_account_id="awsAccountId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f1aea1e8f8374658123a9a360f0e0d72eb893056b58d0c236a9e107ecb80ec83)
                check_type(argname="argument aws_account_id", value=aws_account_id, expected_type=type_hints["aws_account_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if aws_account_id is not None:
                self._values["aws_account_id"] = aws_account_id

        @builtins.property
        def aws_account_id(self) -> typing.Optional[builtins.str]:
            '''The account ID of a project.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-projectprofile-awsaccount.html#cfn-datazone-projectprofile-awsaccount-awsaccountid
            '''
            result = self._values.get("aws_account_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AwsAccountProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnProjectProfilePropsMixin.EnvironmentConfigurationParameterProperty",
        jsii_struct_bases=[],
        name_mapping={"is_editable": "isEditable", "name": "name", "value": "value"},
    )
    class EnvironmentConfigurationParameterProperty:
        def __init__(
            self,
            *,
            is_editable: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            name: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The environment configuration parameter.

            :param is_editable: Specifies whether the environment parameter is editable.
            :param name: The name of the environment configuration parameter.
            :param value: The value of the environment configuration parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-projectprofile-environmentconfigurationparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                environment_configuration_parameter_property = datazone_mixins.CfnProjectProfilePropsMixin.EnvironmentConfigurationParameterProperty(
                    is_editable=False,
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0501da66c963197468ad3efa65ddbfe8744590e5a480ab65d1c29d3c3a0902ba)
                check_type(argname="argument is_editable", value=is_editable, expected_type=type_hints["is_editable"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if is_editable is not None:
                self._values["is_editable"] = is_editable
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def is_editable(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether the environment parameter is editable.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-projectprofile-environmentconfigurationparameter.html#cfn-datazone-projectprofile-environmentconfigurationparameter-iseditable
            '''
            result = self._values.get("is_editable")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the environment configuration parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-projectprofile-environmentconfigurationparameter.html#cfn-datazone-projectprofile-environmentconfigurationparameter-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value of the environment configuration parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-projectprofile-environmentconfigurationparameter.html#cfn-datazone-projectprofile-environmentconfigurationparameter-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EnvironmentConfigurationParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnProjectProfilePropsMixin.EnvironmentConfigurationParametersDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "parameter_overrides": "parameterOverrides",
            "resolved_parameters": "resolvedParameters",
            "ssm_path": "ssmPath",
        },
    )
    class EnvironmentConfigurationParametersDetailsProperty:
        def __init__(
            self,
            *,
            parameter_overrides: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProjectProfilePropsMixin.EnvironmentConfigurationParameterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            resolved_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProjectProfilePropsMixin.EnvironmentConfigurationParameterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            ssm_path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The details of the environment configuration parameter.

            :param parameter_overrides: The parameter overrides.
            :param resolved_parameters: The resolved environment configuration parameters.
            :param ssm_path: Ssm path environment configuration parameters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-projectprofile-environmentconfigurationparametersdetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                environment_configuration_parameters_details_property = datazone_mixins.CfnProjectProfilePropsMixin.EnvironmentConfigurationParametersDetailsProperty(
                    parameter_overrides=[datazone_mixins.CfnProjectProfilePropsMixin.EnvironmentConfigurationParameterProperty(
                        is_editable=False,
                        name="name",
                        value="value"
                    )],
                    resolved_parameters=[datazone_mixins.CfnProjectProfilePropsMixin.EnvironmentConfigurationParameterProperty(
                        is_editable=False,
                        name="name",
                        value="value"
                    )],
                    ssm_path="ssmPath"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d83d8991794b9eefbd9f068be7d652aee1506bbd374b08c2cb821145071cc3c0)
                check_type(argname="argument parameter_overrides", value=parameter_overrides, expected_type=type_hints["parameter_overrides"])
                check_type(argname="argument resolved_parameters", value=resolved_parameters, expected_type=type_hints["resolved_parameters"])
                check_type(argname="argument ssm_path", value=ssm_path, expected_type=type_hints["ssm_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if parameter_overrides is not None:
                self._values["parameter_overrides"] = parameter_overrides
            if resolved_parameters is not None:
                self._values["resolved_parameters"] = resolved_parameters
            if ssm_path is not None:
                self._values["ssm_path"] = ssm_path

        @builtins.property
        def parameter_overrides(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectProfilePropsMixin.EnvironmentConfigurationParameterProperty"]]]]:
            '''The parameter overrides.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-projectprofile-environmentconfigurationparametersdetails.html#cfn-datazone-projectprofile-environmentconfigurationparametersdetails-parameteroverrides
            '''
            result = self._values.get("parameter_overrides")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectProfilePropsMixin.EnvironmentConfigurationParameterProperty"]]]], result)

        @builtins.property
        def resolved_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectProfilePropsMixin.EnvironmentConfigurationParameterProperty"]]]]:
            '''The resolved environment configuration parameters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-projectprofile-environmentconfigurationparametersdetails.html#cfn-datazone-projectprofile-environmentconfigurationparametersdetails-resolvedparameters
            '''
            result = self._values.get("resolved_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectProfilePropsMixin.EnvironmentConfigurationParameterProperty"]]]], result)

        @builtins.property
        def ssm_path(self) -> typing.Optional[builtins.str]:
            '''Ssm path environment configuration parameters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-projectprofile-environmentconfigurationparametersdetails.html#cfn-datazone-projectprofile-environmentconfigurationparametersdetails-ssmpath
            '''
            result = self._values.get("ssm_path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EnvironmentConfigurationParametersDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnProjectProfilePropsMixin.EnvironmentConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "aws_account": "awsAccount",
            "aws_region": "awsRegion",
            "configuration_parameters": "configurationParameters",
            "deployment_mode": "deploymentMode",
            "deployment_order": "deploymentOrder",
            "description": "description",
            "environment_blueprint_id": "environmentBlueprintId",
            "environment_configuration_id": "environmentConfigurationId",
            "name": "name",
        },
    )
    class EnvironmentConfigurationProperty:
        def __init__(
            self,
            *,
            aws_account: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProjectProfilePropsMixin.AwsAccountProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            aws_region: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProjectProfilePropsMixin.RegionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            configuration_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProjectProfilePropsMixin.EnvironmentConfigurationParametersDetailsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            deployment_mode: typing.Optional[builtins.str] = None,
            deployment_order: typing.Optional[jsii.Number] = None,
            description: typing.Optional[builtins.str] = None,
            environment_blueprint_id: typing.Optional[builtins.str] = None,
            environment_configuration_id: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration of an environment.

            :param aws_account: The AWS account of the environment.
            :param aws_region: The AWS Region of the environment.
            :param configuration_parameters: The configuration parameters of the environment.
            :param deployment_mode: The deployment mode of the environment.
            :param deployment_order: The deployment order of the environment.
            :param description: The environment description.
            :param environment_blueprint_id: The environment blueprint ID.
            :param environment_configuration_id: 
            :param name: The environment name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-projectprofile-environmentconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                environment_configuration_property = datazone_mixins.CfnProjectProfilePropsMixin.EnvironmentConfigurationProperty(
                    aws_account=datazone_mixins.CfnProjectProfilePropsMixin.AwsAccountProperty(
                        aws_account_id="awsAccountId"
                    ),
                    aws_region=datazone_mixins.CfnProjectProfilePropsMixin.RegionProperty(
                        region_name="regionName"
                    ),
                    configuration_parameters=datazone_mixins.CfnProjectProfilePropsMixin.EnvironmentConfigurationParametersDetailsProperty(
                        parameter_overrides=[datazone_mixins.CfnProjectProfilePropsMixin.EnvironmentConfigurationParameterProperty(
                            is_editable=False,
                            name="name",
                            value="value"
                        )],
                        resolved_parameters=[datazone_mixins.CfnProjectProfilePropsMixin.EnvironmentConfigurationParameterProperty(
                            is_editable=False,
                            name="name",
                            value="value"
                        )],
                        ssm_path="ssmPath"
                    ),
                    deployment_mode="deploymentMode",
                    deployment_order=123,
                    description="description",
                    environment_blueprint_id="environmentBlueprintId",
                    environment_configuration_id="environmentConfigurationId",
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6851456ab6150bef28b03895778dfb3b1e59a4d1afd0767f258c2effc4f0acc3)
                check_type(argname="argument aws_account", value=aws_account, expected_type=type_hints["aws_account"])
                check_type(argname="argument aws_region", value=aws_region, expected_type=type_hints["aws_region"])
                check_type(argname="argument configuration_parameters", value=configuration_parameters, expected_type=type_hints["configuration_parameters"])
                check_type(argname="argument deployment_mode", value=deployment_mode, expected_type=type_hints["deployment_mode"])
                check_type(argname="argument deployment_order", value=deployment_order, expected_type=type_hints["deployment_order"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument environment_blueprint_id", value=environment_blueprint_id, expected_type=type_hints["environment_blueprint_id"])
                check_type(argname="argument environment_configuration_id", value=environment_configuration_id, expected_type=type_hints["environment_configuration_id"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if aws_account is not None:
                self._values["aws_account"] = aws_account
            if aws_region is not None:
                self._values["aws_region"] = aws_region
            if configuration_parameters is not None:
                self._values["configuration_parameters"] = configuration_parameters
            if deployment_mode is not None:
                self._values["deployment_mode"] = deployment_mode
            if deployment_order is not None:
                self._values["deployment_order"] = deployment_order
            if description is not None:
                self._values["description"] = description
            if environment_blueprint_id is not None:
                self._values["environment_blueprint_id"] = environment_blueprint_id
            if environment_configuration_id is not None:
                self._values["environment_configuration_id"] = environment_configuration_id
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def aws_account(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectProfilePropsMixin.AwsAccountProperty"]]:
            '''The AWS account of the environment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-projectprofile-environmentconfiguration.html#cfn-datazone-projectprofile-environmentconfiguration-awsaccount
            '''
            result = self._values.get("aws_account")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectProfilePropsMixin.AwsAccountProperty"]], result)

        @builtins.property
        def aws_region(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectProfilePropsMixin.RegionProperty"]]:
            '''The AWS Region of the environment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-projectprofile-environmentconfiguration.html#cfn-datazone-projectprofile-environmentconfiguration-awsregion
            '''
            result = self._values.get("aws_region")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectProfilePropsMixin.RegionProperty"]], result)

        @builtins.property
        def configuration_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectProfilePropsMixin.EnvironmentConfigurationParametersDetailsProperty"]]:
            '''The configuration parameters of the environment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-projectprofile-environmentconfiguration.html#cfn-datazone-projectprofile-environmentconfiguration-configurationparameters
            '''
            result = self._values.get("configuration_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectProfilePropsMixin.EnvironmentConfigurationParametersDetailsProperty"]], result)

        @builtins.property
        def deployment_mode(self) -> typing.Optional[builtins.str]:
            '''The deployment mode of the environment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-projectprofile-environmentconfiguration.html#cfn-datazone-projectprofile-environmentconfiguration-deploymentmode
            '''
            result = self._values.get("deployment_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def deployment_order(self) -> typing.Optional[jsii.Number]:
            '''The deployment order of the environment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-projectprofile-environmentconfiguration.html#cfn-datazone-projectprofile-environmentconfiguration-deploymentorder
            '''
            result = self._values.get("deployment_order")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The environment description.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-projectprofile-environmentconfiguration.html#cfn-datazone-projectprofile-environmentconfiguration-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def environment_blueprint_id(self) -> typing.Optional[builtins.str]:
            '''The environment blueprint ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-projectprofile-environmentconfiguration.html#cfn-datazone-projectprofile-environmentconfiguration-environmentblueprintid
            '''
            result = self._values.get("environment_blueprint_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def environment_configuration_id(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-projectprofile-environmentconfiguration.html#cfn-datazone-projectprofile-environmentconfiguration-environmentconfigurationid
            '''
            result = self._values.get("environment_configuration_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The environment name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-projectprofile-environmentconfiguration.html#cfn-datazone-projectprofile-environmentconfiguration-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EnvironmentConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnProjectProfilePropsMixin.RegionProperty",
        jsii_struct_bases=[],
        name_mapping={"region_name": "regionName"},
    )
    class RegionProperty:
        def __init__(
            self,
            *,
            region_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The AWS Region.

            :param region_name: The AWS Region name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-projectprofile-region.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                region_property = datazone_mixins.CfnProjectProfilePropsMixin.RegionProperty(
                    region_name="regionName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__04845c541d0e45395b74b0f8762aa2a833a22a08d6e5ef0d60c288fc4fa4335a)
                check_type(argname="argument region_name", value=region_name, expected_type=type_hints["region_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if region_name is not None:
                self._values["region_name"] = region_name

        @builtins.property
        def region_name(self) -> typing.Optional[builtins.str]:
            '''The AWS Region name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-projectprofile-region.html#cfn-datazone-projectprofile-region-regionname
            '''
            result = self._values.get("region_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RegionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IMixin_11e4b965)
class CfnProjectPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnProjectPropsMixin",
):
    '''The ``AWS::DataZone::Project`` resource specifies an Amazon DataZone project.

    Projects enable a group of users to collaborate on various business use cases that involve publishing, discovering, subscribing to, and consuming data in the Amazon DataZone catalog. Project members consume assets from the Amazon DataZone catalog and produce new assets using one or more analytical workflows.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-project.html
    :cloudformationResource: AWS::DataZone::Project
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
        
        cfn_project_props_mixin = datazone_mixins.CfnProjectPropsMixin(datazone_mixins.CfnProjectMixinProps(
            description="description",
            domain_identifier="domainIdentifier",
            domain_unit_id="domainUnitId",
            glossary_terms=["glossaryTerms"],
            name="name",
            project_profile_id="projectProfileId",
            project_profile_version="projectProfileVersion",
            user_parameters=[datazone_mixins.CfnProjectPropsMixin.EnvironmentConfigurationUserParameterProperty(
                environment_configuration_name="environmentConfigurationName",
                environment_id="environmentId",
                environment_parameters=[datazone_mixins.CfnProjectPropsMixin.EnvironmentParameterProperty(
                    name="name",
                    value="value"
                )]
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnProjectMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DataZone::Project``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edf16b5e398529a02ef4ad3cdc2b222250ed73c3b1edaba474ea71a1c1863729)
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
            type_hints = typing.get_type_hints(_typecheckingstub__80896da0fbcfde1b3b09ef0065d49ad1b2bcc70c2acb004ae0bb748dcdfe907d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0999d1b4e832dc9f5eb0fcc55b32f751ab640a1d696cf74dda3e46072d22a81)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnProjectMixinProps:
        return typing.cast(CfnProjectMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnProjectPropsMixin.EnvironmentConfigurationUserParameterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "environment_configuration_name": "environmentConfigurationName",
            "environment_id": "environmentId",
            "environment_parameters": "environmentParameters",
        },
    )
    class EnvironmentConfigurationUserParameterProperty:
        def __init__(
            self,
            *,
            environment_configuration_name: typing.Optional[builtins.str] = None,
            environment_id: typing.Optional[builtins.str] = None,
            environment_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProjectPropsMixin.EnvironmentParameterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The environment configuration user parameters.

            :param environment_configuration_name: The environment configuration name.
            :param environment_id: The ID of the environment.
            :param environment_parameters: The environment parameters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-project-environmentconfigurationuserparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                environment_configuration_user_parameter_property = datazone_mixins.CfnProjectPropsMixin.EnvironmentConfigurationUserParameterProperty(
                    environment_configuration_name="environmentConfigurationName",
                    environment_id="environmentId",
                    environment_parameters=[datazone_mixins.CfnProjectPropsMixin.EnvironmentParameterProperty(
                        name="name",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2ba49e4c515b41286712fd660f4dc1ff1beb7f8862bcac728df2c4c9500a7445)
                check_type(argname="argument environment_configuration_name", value=environment_configuration_name, expected_type=type_hints["environment_configuration_name"])
                check_type(argname="argument environment_id", value=environment_id, expected_type=type_hints["environment_id"])
                check_type(argname="argument environment_parameters", value=environment_parameters, expected_type=type_hints["environment_parameters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if environment_configuration_name is not None:
                self._values["environment_configuration_name"] = environment_configuration_name
            if environment_id is not None:
                self._values["environment_id"] = environment_id
            if environment_parameters is not None:
                self._values["environment_parameters"] = environment_parameters

        @builtins.property
        def environment_configuration_name(self) -> typing.Optional[builtins.str]:
            '''The environment configuration name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-project-environmentconfigurationuserparameter.html#cfn-datazone-project-environmentconfigurationuserparameter-environmentconfigurationname
            '''
            result = self._values.get("environment_configuration_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def environment_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the environment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-project-environmentconfigurationuserparameter.html#cfn-datazone-project-environmentconfigurationuserparameter-environmentid
            '''
            result = self._values.get("environment_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def environment_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.EnvironmentParameterProperty"]]]]:
            '''The environment parameters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-project-environmentconfigurationuserparameter.html#cfn-datazone-project-environmentconfigurationuserparameter-environmentparameters
            '''
            result = self._values.get("environment_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.EnvironmentParameterProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EnvironmentConfigurationUserParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnProjectPropsMixin.EnvironmentParameterProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class EnvironmentParameterProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The parameter details of an evironment profile.

            :param name: The name of an environment profile parameter.
            :param value: The value of an environment profile parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-project-environmentparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                environment_parameter_property = datazone_mixins.CfnProjectPropsMixin.EnvironmentParameterProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b52e32344bad00058f361c5248e5ef2e3d7375f58485de9e80e33119a6962465)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of an environment profile parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-project-environmentparameter.html#cfn-datazone-project-environmentparameter-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value of an environment profile parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-project-environmentparameter.html#cfn-datazone-project-environmentparameter-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EnvironmentParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnSubscriptionTargetMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "applicable_asset_types": "applicableAssetTypes",
        "authorized_principals": "authorizedPrincipals",
        "domain_identifier": "domainIdentifier",
        "environment_identifier": "environmentIdentifier",
        "manage_access_role": "manageAccessRole",
        "name": "name",
        "provider": "provider",
        "subscription_target_config": "subscriptionTargetConfig",
        "type": "type",
    },
)
class CfnSubscriptionTargetMixinProps:
    def __init__(
        self,
        *,
        applicable_asset_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        authorized_principals: typing.Optional[typing.Sequence[builtins.str]] = None,
        domain_identifier: typing.Optional[builtins.str] = None,
        environment_identifier: typing.Optional[builtins.str] = None,
        manage_access_role: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        provider: typing.Optional[builtins.str] = None,
        subscription_target_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSubscriptionTargetPropsMixin.SubscriptionTargetFormProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnSubscriptionTargetPropsMixin.

        :param applicable_asset_types: The asset types included in the subscription target.
        :param authorized_principals: The authorized principals included in the subscription target.
        :param domain_identifier: The ID of the Amazon DataZone domain in which subscription target is created.
        :param environment_identifier: The ID of the environment in which subscription target is created.
        :param manage_access_role: The manage access role that is used to create the subscription target.
        :param name: The name of the subscription target.
        :param provider: The provider of the subscription target.
        :param subscription_target_config: The configuration of the subscription target.
        :param type: The type of the subscription target.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-subscriptiontarget.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
            
            cfn_subscription_target_mixin_props = datazone_mixins.CfnSubscriptionTargetMixinProps(
                applicable_asset_types=["applicableAssetTypes"],
                authorized_principals=["authorizedPrincipals"],
                domain_identifier="domainIdentifier",
                environment_identifier="environmentIdentifier",
                manage_access_role="manageAccessRole",
                name="name",
                provider="provider",
                subscription_target_config=[datazone_mixins.CfnSubscriptionTargetPropsMixin.SubscriptionTargetFormProperty(
                    content="content",
                    form_name="formName"
                )],
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86154684569854cd554232051e2c0572bc7343decf3088b8098354bd5cd7d499)
            check_type(argname="argument applicable_asset_types", value=applicable_asset_types, expected_type=type_hints["applicable_asset_types"])
            check_type(argname="argument authorized_principals", value=authorized_principals, expected_type=type_hints["authorized_principals"])
            check_type(argname="argument domain_identifier", value=domain_identifier, expected_type=type_hints["domain_identifier"])
            check_type(argname="argument environment_identifier", value=environment_identifier, expected_type=type_hints["environment_identifier"])
            check_type(argname="argument manage_access_role", value=manage_access_role, expected_type=type_hints["manage_access_role"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument subscription_target_config", value=subscription_target_config, expected_type=type_hints["subscription_target_config"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if applicable_asset_types is not None:
            self._values["applicable_asset_types"] = applicable_asset_types
        if authorized_principals is not None:
            self._values["authorized_principals"] = authorized_principals
        if domain_identifier is not None:
            self._values["domain_identifier"] = domain_identifier
        if environment_identifier is not None:
            self._values["environment_identifier"] = environment_identifier
        if manage_access_role is not None:
            self._values["manage_access_role"] = manage_access_role
        if name is not None:
            self._values["name"] = name
        if provider is not None:
            self._values["provider"] = provider
        if subscription_target_config is not None:
            self._values["subscription_target_config"] = subscription_target_config
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def applicable_asset_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The asset types included in the subscription target.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-subscriptiontarget.html#cfn-datazone-subscriptiontarget-applicableassettypes
        '''
        result = self._values.get("applicable_asset_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def authorized_principals(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The authorized principals included in the subscription target.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-subscriptiontarget.html#cfn-datazone-subscriptiontarget-authorizedprincipals
        '''
        result = self._values.get("authorized_principals")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def domain_identifier(self) -> typing.Optional[builtins.str]:
        '''The ID of the Amazon DataZone domain in which subscription target is created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-subscriptiontarget.html#cfn-datazone-subscriptiontarget-domainidentifier
        '''
        result = self._values.get("domain_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_identifier(self) -> typing.Optional[builtins.str]:
        '''The ID of the environment in which subscription target is created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-subscriptiontarget.html#cfn-datazone-subscriptiontarget-environmentidentifier
        '''
        result = self._values.get("environment_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def manage_access_role(self) -> typing.Optional[builtins.str]:
        '''The manage access role that is used to create the subscription target.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-subscriptiontarget.html#cfn-datazone-subscriptiontarget-manageaccessrole
        '''
        result = self._values.get("manage_access_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the subscription target.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-subscriptiontarget.html#cfn-datazone-subscriptiontarget-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provider(self) -> typing.Optional[builtins.str]:
        '''The provider of the subscription target.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-subscriptiontarget.html#cfn-datazone-subscriptiontarget-provider
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subscription_target_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSubscriptionTargetPropsMixin.SubscriptionTargetFormProperty"]]]]:
        '''The configuration of the subscription target.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-subscriptiontarget.html#cfn-datazone-subscriptiontarget-subscriptiontargetconfig
        '''
        result = self._values.get("subscription_target_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSubscriptionTargetPropsMixin.SubscriptionTargetFormProperty"]]]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of the subscription target.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-subscriptiontarget.html#cfn-datazone-subscriptiontarget-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSubscriptionTargetMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSubscriptionTargetPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnSubscriptionTargetPropsMixin",
):
    '''The ``AWS::DataZone::SubscriptionTarget`` resource specifies an Amazon DataZone subscription target.

    Subscription targets enable you to access the data to which you have subscribed in your projects. A subscription target specifies the location (for example, a database or a schema) and the required permissions (for example, an IAM role) that Amazon DataZone can use to establish a connection with the source data and to create the necessary grants so that members of the Amazon DataZone project can start querying the data to which they have subscribed.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-subscriptiontarget.html
    :cloudformationResource: AWS::DataZone::SubscriptionTarget
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
        
        cfn_subscription_target_props_mixin = datazone_mixins.CfnSubscriptionTargetPropsMixin(datazone_mixins.CfnSubscriptionTargetMixinProps(
            applicable_asset_types=["applicableAssetTypes"],
            authorized_principals=["authorizedPrincipals"],
            domain_identifier="domainIdentifier",
            environment_identifier="environmentIdentifier",
            manage_access_role="manageAccessRole",
            name="name",
            provider="provider",
            subscription_target_config=[datazone_mixins.CfnSubscriptionTargetPropsMixin.SubscriptionTargetFormProperty(
                content="content",
                form_name="formName"
            )],
            type="type"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnSubscriptionTargetMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DataZone::SubscriptionTarget``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae2093e93ce7728ce11d93d9f1cdc48aa8adfd61da09b3215640bcb9560b71c8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0abc9cb3b5e112933723a17a15ddd1446443eeedf86266f92b8f7c0964842708)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__708f31f0686b1211b83d8985884223f28dc83d3da683578d5764df880bc7c434)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSubscriptionTargetMixinProps:
        return typing.cast(CfnSubscriptionTargetMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnSubscriptionTargetPropsMixin.SubscriptionTargetFormProperty",
        jsii_struct_bases=[],
        name_mapping={"content": "content", "form_name": "formName"},
    )
    class SubscriptionTargetFormProperty:
        def __init__(
            self,
            *,
            content: typing.Optional[builtins.str] = None,
            form_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The details of the subscription target configuration.

            :param content: The content of the subscription target configuration.
            :param form_name: The form name included in the subscription target configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-subscriptiontarget-subscriptiontargetform.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                subscription_target_form_property = datazone_mixins.CfnSubscriptionTargetPropsMixin.SubscriptionTargetFormProperty(
                    content="content",
                    form_name="formName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3691e01e2282b16009e1b38afb9ade98c67417c4e976160b727c9724fdef7946)
                check_type(argname="argument content", value=content, expected_type=type_hints["content"])
                check_type(argname="argument form_name", value=form_name, expected_type=type_hints["form_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if content is not None:
                self._values["content"] = content
            if form_name is not None:
                self._values["form_name"] = form_name

        @builtins.property
        def content(self) -> typing.Optional[builtins.str]:
            '''The content of the subscription target configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-subscriptiontarget-subscriptiontargetform.html#cfn-datazone-subscriptiontarget-subscriptiontargetform-content
            '''
            result = self._values.get("content")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def form_name(self) -> typing.Optional[builtins.str]:
            '''The form name included in the subscription target configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-subscriptiontarget-subscriptiontargetform.html#cfn-datazone-subscriptiontarget-subscriptiontargetform-formname
            '''
            result = self._values.get("form_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubscriptionTargetFormProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnUserProfileMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "domain_identifier": "domainIdentifier",
        "status": "status",
        "user_identifier": "userIdentifier",
        "user_type": "userType",
    },
)
class CfnUserProfileMixinProps:
    def __init__(
        self,
        *,
        domain_identifier: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        user_identifier: typing.Optional[builtins.str] = None,
        user_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnUserProfilePropsMixin.

        :param domain_identifier: The identifier of a Amazon DataZone domain in which a user profile exists.
        :param status: The status of the user profile.
        :param user_identifier: The identifier of the user for which the user profile is created.
        :param user_type: The user type of the user for which the user profile is created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-userprofile.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
            
            cfn_user_profile_mixin_props = datazone_mixins.CfnUserProfileMixinProps(
                domain_identifier="domainIdentifier",
                status="status",
                user_identifier="userIdentifier",
                user_type="userType"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64e344f8db1efaaef798ecba0f83d742564f5a3e87e4aadfcbc968b2900b8135)
            check_type(argname="argument domain_identifier", value=domain_identifier, expected_type=type_hints["domain_identifier"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument user_identifier", value=user_identifier, expected_type=type_hints["user_identifier"])
            check_type(argname="argument user_type", value=user_type, expected_type=type_hints["user_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if domain_identifier is not None:
            self._values["domain_identifier"] = domain_identifier
        if status is not None:
            self._values["status"] = status
        if user_identifier is not None:
            self._values["user_identifier"] = user_identifier
        if user_type is not None:
            self._values["user_type"] = user_type

    @builtins.property
    def domain_identifier(self) -> typing.Optional[builtins.str]:
        '''The identifier of a Amazon DataZone domain in which a user profile exists.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-userprofile.html#cfn-datazone-userprofile-domainidentifier
        '''
        result = self._values.get("domain_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''The status of the user profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-userprofile.html#cfn-datazone-userprofile-status
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_identifier(self) -> typing.Optional[builtins.str]:
        '''The identifier of the user for which the user profile is created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-userprofile.html#cfn-datazone-userprofile-useridentifier
        '''
        result = self._values.get("user_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_type(self) -> typing.Optional[builtins.str]:
        '''The user type of the user for which the user profile is created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-userprofile.html#cfn-datazone-userprofile-usertype
        '''
        result = self._values.get("user_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserProfileMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnUserProfilePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnUserProfilePropsMixin",
):
    '''The user type of the user for which the user profile is created.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-userprofile.html
    :cloudformationResource: AWS::DataZone::UserProfile
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
        
        cfn_user_profile_props_mixin = datazone_mixins.CfnUserProfilePropsMixin(datazone_mixins.CfnUserProfileMixinProps(
            domain_identifier="domainIdentifier",
            status="status",
            user_identifier="userIdentifier",
            user_type="userType"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnUserProfileMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DataZone::UserProfile``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cce776297c684025be14c010cbd544fd589a264134fdd3a48ae0166144fe3813)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dffa632b6e5cbc8128b6346e943da37b7e9f9f6326d5e4816c0d2ed74682e463)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a723c650ada28a6a5376c86b214cacaa25e124195edde9540a7ccabd017c7d9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnUserProfileMixinProps:
        return typing.cast(CfnUserProfileMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnUserProfilePropsMixin.IamUserProfileDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={"arn": "arn"},
    )
    class IamUserProfileDetailsProperty:
        def __init__(self, *, arn: typing.Optional[builtins.str] = None) -> None:
            '''The details of the IAM User Profile.

            :param arn: The ARN of the IAM User Profile.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-userprofile-iamuserprofiledetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                iam_user_profile_details_property = datazone_mixins.CfnUserProfilePropsMixin.IamUserProfileDetailsProperty(
                    arn="arn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ca800bf8ac185199b62bcfc3b7536d9a7dff650bc97623c53ec6df747cf8e356)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the IAM User Profile.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-userprofile-iamuserprofiledetails.html#cfn-datazone-userprofile-iamuserprofiledetails-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IamUserProfileDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnUserProfilePropsMixin.SsoUserProfileDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "first_name": "firstName",
            "last_name": "lastName",
            "username": "username",
        },
    )
    class SsoUserProfileDetailsProperty:
        def __init__(
            self,
            *,
            first_name: typing.Optional[builtins.str] = None,
            last_name: typing.Optional[builtins.str] = None,
            username: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The details of the SSO User Profile.

            :param first_name: The First Name of the IAM User Profile.
            :param last_name: The Last Name of the IAM User Profile.
            :param username: The username of the SSO User Profile.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-userprofile-ssouserprofiledetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                sso_user_profile_details_property = datazone_mixins.CfnUserProfilePropsMixin.SsoUserProfileDetailsProperty(
                    first_name="firstName",
                    last_name="lastName",
                    username="username"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__398093199f2d8d3e450f108718e0b2da8d31045919d84e8436c86e9166ca629a)
                check_type(argname="argument first_name", value=first_name, expected_type=type_hints["first_name"])
                check_type(argname="argument last_name", value=last_name, expected_type=type_hints["last_name"])
                check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if first_name is not None:
                self._values["first_name"] = first_name
            if last_name is not None:
                self._values["last_name"] = last_name
            if username is not None:
                self._values["username"] = username

        @builtins.property
        def first_name(self) -> typing.Optional[builtins.str]:
            '''The First Name of the IAM User Profile.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-userprofile-ssouserprofiledetails.html#cfn-datazone-userprofile-ssouserprofiledetails-firstname
            '''
            result = self._values.get("first_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def last_name(self) -> typing.Optional[builtins.str]:
            '''The Last Name of the IAM User Profile.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-userprofile-ssouserprofiledetails.html#cfn-datazone-userprofile-ssouserprofiledetails-lastname
            '''
            result = self._values.get("last_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def username(self) -> typing.Optional[builtins.str]:
            '''The username of the SSO User Profile.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-userprofile-ssouserprofiledetails.html#cfn-datazone-userprofile-ssouserprofiledetails-username
            '''
            result = self._values.get("username")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SsoUserProfileDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datazone.mixins.CfnUserProfilePropsMixin.UserProfileDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={"iam": "iam", "sso": "sso"},
    )
    class UserProfileDetailsProperty:
        def __init__(
            self,
            *,
            iam: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserProfilePropsMixin.IamUserProfileDetailsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sso: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserProfilePropsMixin.SsoUserProfileDetailsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param iam: The details of the IAM User Profile.
            :param sso: The details of the SSO User Profile.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-userprofile-userprofiledetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datazone import mixins as datazone_mixins
                
                user_profile_details_property = datazone_mixins.CfnUserProfilePropsMixin.UserProfileDetailsProperty(
                    iam=datazone_mixins.CfnUserProfilePropsMixin.IamUserProfileDetailsProperty(
                        arn="arn"
                    ),
                    sso=datazone_mixins.CfnUserProfilePropsMixin.SsoUserProfileDetailsProperty(
                        first_name="firstName",
                        last_name="lastName",
                        username="username"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b8737a875264aad6de430a5e2a9c232b2ad85d290e5e58b7b23c0b55eb232690)
                check_type(argname="argument iam", value=iam, expected_type=type_hints["iam"])
                check_type(argname="argument sso", value=sso, expected_type=type_hints["sso"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if iam is not None:
                self._values["iam"] = iam
            if sso is not None:
                self._values["sso"] = sso

        @builtins.property
        def iam(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserProfilePropsMixin.IamUserProfileDetailsProperty"]]:
            '''The details of the IAM User Profile.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-userprofile-userprofiledetails.html#cfn-datazone-userprofile-userprofiledetails-iam
            '''
            result = self._values.get("iam")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserProfilePropsMixin.IamUserProfileDetailsProperty"]], result)

        @builtins.property
        def sso(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserProfilePropsMixin.SsoUserProfileDetailsProperty"]]:
            '''The details of the SSO User Profile.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datazone-userprofile-userprofiledetails.html#cfn-datazone-userprofile-userprofiledetails-sso
            '''
            result = self._values.get("sso")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserProfilePropsMixin.SsoUserProfileDetailsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UserProfileDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnConnectionMixinProps",
    "CfnConnectionPropsMixin",
    "CfnDataSourceMixinProps",
    "CfnDataSourcePropsMixin",
    "CfnDomainMixinProps",
    "CfnDomainPropsMixin",
    "CfnDomainUnitMixinProps",
    "CfnDomainUnitPropsMixin",
    "CfnEnvironmentActionsMixinProps",
    "CfnEnvironmentActionsPropsMixin",
    "CfnEnvironmentBlueprintConfigurationMixinProps",
    "CfnEnvironmentBlueprintConfigurationPropsMixin",
    "CfnEnvironmentMixinProps",
    "CfnEnvironmentProfileMixinProps",
    "CfnEnvironmentProfilePropsMixin",
    "CfnEnvironmentPropsMixin",
    "CfnFormTypeMixinProps",
    "CfnFormTypePropsMixin",
    "CfnGroupProfileMixinProps",
    "CfnGroupProfilePropsMixin",
    "CfnOwnerMixinProps",
    "CfnOwnerPropsMixin",
    "CfnPolicyGrantMixinProps",
    "CfnPolicyGrantPropsMixin",
    "CfnProjectMembershipMixinProps",
    "CfnProjectMembershipPropsMixin",
    "CfnProjectMixinProps",
    "CfnProjectProfileMixinProps",
    "CfnProjectProfilePropsMixin",
    "CfnProjectPropsMixin",
    "CfnSubscriptionTargetMixinProps",
    "CfnSubscriptionTargetPropsMixin",
    "CfnUserProfileMixinProps",
    "CfnUserProfilePropsMixin",
]

publication.publish()

def _typecheckingstub__2ca99ae038dddfa8cdd53cbd1df77d82f370778d850fc42849cfc7e4cceeabce(
    *,
    aws_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectionPropsMixin.AwsLocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    domain_identifier: typing.Optional[builtins.str] = None,
    enable_trusted_identity_propagation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    environment_identifier: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    project_identifier: typing.Optional[builtins.str] = None,
    props: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectionPropsMixin.ConnectionPropertiesInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    scope: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e9c094929392b272fc04188e16b8fa4b9b33a49e818f22c32b4924ec0ce519e(
    props: typing.Union[CfnConnectionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95b66b41b0178dfb9cafdf9c4658a046ecdbab891e8600a11da55ca0dfddc26a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a24c11f99646036a223c9eb490372322a2b516016e904be222b2e3bae5c96ce9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bda8cd1983f1e7e08edb67eb5efa75442c2c87b222af1e4a7bc67fc382269b2(
    *,
    auth_mode: typing.Optional[builtins.str] = None,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    profile_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd0abda7028f017acbb717b67a017e50e1fbfec7ffee2e2660f51917bc9e5ee4(
    *,
    workgroup_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2373b5f964ea9e7c0cca17573a69a36075214fd7308a0c8c3d3f7ae13b803625(
    *,
    authentication_type: typing.Optional[builtins.str] = None,
    basic_authentication_credentials: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectionPropsMixin.BasicAuthenticationCredentialsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    custom_authentication_credentials: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    o_auth2_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectionPropsMixin.OAuth2PropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    secret_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e95a19100de29b79778d33bf14ceb5e258e67ac98c8ba349566d3e20e3045b85(
    *,
    authorization_code: typing.Optional[builtins.str] = None,
    redirect_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6a1ca03cc284fc24c6d252d4f951e18d76e4480f6fc384817572d829f7e7fc4(
    *,
    access_role: typing.Optional[builtins.str] = None,
    aws_account_id: typing.Optional[builtins.str] = None,
    aws_region: typing.Optional[builtins.str] = None,
    iam_connection_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7d39aac0e59cb1e3763c4f7086fbb5f45d90bf7152c6fc898a8b4e716bcf6ba(
    *,
    password: typing.Optional[builtins.str] = None,
    user_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f141db480b1ef6dd0c9e368caf1e5665607a85286d6b15645fa2cd6865bd684a(
    *,
    amazon_q_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectionPropsMixin.AmazonQPropertiesInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    athena_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectionPropsMixin.AthenaPropertiesInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    glue_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectionPropsMixin.GluePropertiesInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    hyper_pod_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectionPropsMixin.HyperPodPropertiesInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    iam_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectionPropsMixin.IamPropertiesInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    redshift_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectionPropsMixin.RedshiftPropertiesInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectionPropsMixin.S3PropertiesInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    spark_emr_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectionPropsMixin.SparkEmrPropertiesInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    spark_glue_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectionPropsMixin.SparkGluePropertiesInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08048b4d5fb5e3b0a9a76ada34206ca6c8654f423f2f1e8ee53603c79bc1d4e6(
    *,
    athena_properties: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    authentication_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectionPropsMixin.AuthenticationConfigurationInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    connection_properties: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    connection_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    match_criteria: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    physical_connection_requirements: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectionPropsMixin.PhysicalConnectionRequirementsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    python_properties: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    spark_properties: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    validate_credentials: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    validate_for_compute_environments: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e969a24019316cfdc513bafaf611986009beaa5dfaa39aa537a8c3b3c5f4967f(
    *,
    access_token: typing.Optional[builtins.str] = None,
    jwt_token: typing.Optional[builtins.str] = None,
    refresh_token: typing.Optional[builtins.str] = None,
    user_managed_client_application_client_secret: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__450b1bed31fcd1c8b65795972913a54cf08f89b29add964a65991287c43468d4(
    *,
    glue_connection_input: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectionPropsMixin.GlueConnectionInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c0fcfbcaab55f24ec59d84d2487d196f6b7eda519f210c4b6a985a5c6c5fdb2(
    *,
    cluster_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9011451acba4189a9a25f3bb9a239b4858b2156a01ec3694652a754231c9428b(
    *,
    glue_lineage_sync_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa6025fa2c389b58a41b1d700fe74e02a95c3659fc9b9db57cc8cde33a7f7895(
    *,
    schedule: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a6f564639d60ff6173c52c3471c29ca4bccd533d06ec7c84c60cef546616582(
    *,
    aws_managed_client_application_reference: typing.Optional[builtins.str] = None,
    user_managed_client_application_client_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26bee2cd414625f5ec412cbe59e591ebe3c64dc954e5b612fc33cf33a9ae9414(
    *,
    authorization_code_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectionPropsMixin.AuthorizationCodePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    o_auth2_client_application: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectionPropsMixin.OAuth2ClientApplicationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    o_auth2_credentials: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectionPropsMixin.GlueOAuth2CredentialsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    o_auth2_grant_type: typing.Optional[builtins.str] = None,
    token_url: typing.Optional[builtins.str] = None,
    token_url_parameters_map: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0fb0914a2bfddd3e7371cf4de5de998dcb2e82406733f4abd9caae59e440297(
    *,
    availability_zone: typing.Optional[builtins.str] = None,
    security_group_id_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_id: typing.Optional[builtins.str] = None,
    subnet_id_list: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d060a57e1a6a8558b37f25eb6d872147a6681127e4b12dcf89159339ca03749(
    *,
    secret_arn: typing.Optional[builtins.str] = None,
    username_password: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectionPropsMixin.UsernamePasswordProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ced908ff5267251237cccb60db4c765130a752e987b920faa4801ff1905bba5(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    schedule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectionPropsMixin.LineageSyncScheduleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe65a531a84fc820d659ae0c1ee946c4f7a20edd20a4406c2bc48cfec411b44f(
    *,
    credentials: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectionPropsMixin.RedshiftCredentialsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    database_name: typing.Optional[builtins.str] = None,
    host: typing.Optional[builtins.str] = None,
    lineage_sync: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectionPropsMixin.RedshiftLineageSyncConfigurationInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    port: typing.Optional[jsii.Number] = None,
    storage: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectionPropsMixin.RedshiftStoragePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ed73eb1679aa2af22d9a5fb093c36b117e2b7ae23b838cbae74c366cc4a59f7(
    *,
    cluster_name: typing.Optional[builtins.str] = None,
    workgroup_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2df7ba0b6b76c9b5d1dae690761f5475fa91bb89b40c3576df10528f21d7e030(
    *,
    s3_access_grant_location_id: typing.Optional[builtins.str] = None,
    s3_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39c202b1386f9006ff2f113353d49e792d833bf16177a4efa125aceaa63cf59e(
    *,
    compute_arn: typing.Optional[builtins.str] = None,
    instance_profile_arn: typing.Optional[builtins.str] = None,
    java_virtual_env: typing.Optional[builtins.str] = None,
    log_uri: typing.Optional[builtins.str] = None,
    managed_endpoint_arn: typing.Optional[builtins.str] = None,
    python_virtual_env: typing.Optional[builtins.str] = None,
    runtime_role: typing.Optional[builtins.str] = None,
    trusted_certificates_s3_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bc34d1eab5d30edccaf2e664c3fb46b351ee444d4a3c0ecffbcedec4cf5da7d(
    *,
    connection: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09ceadb9c4ff9127188010bee62fa24b1ed26a5cf42b9c279b9f625cf3d28bba(
    *,
    additional_args: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectionPropsMixin.SparkGlueArgsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    glue_connection_name: typing.Optional[builtins.str] = None,
    glue_version: typing.Optional[builtins.str] = None,
    idle_timeout: typing.Optional[jsii.Number] = None,
    java_virtual_env: typing.Optional[builtins.str] = None,
    number_of_workers: typing.Optional[jsii.Number] = None,
    python_virtual_env: typing.Optional[builtins.str] = None,
    worker_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc5ebb7e7cdfa9efb28b58fafe7f2a8107a5756a5ddc7a4e13b2e07baa5d3c9c(
    *,
    password: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b17101a94186c9c71e74e2b1916cf53e0c7cee6a94487f0b30257e56f4fa2456(
    *,
    asset_forms_input: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.FormInputProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.DataSourceConfigurationInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    connection_identifier: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    domain_identifier: typing.Optional[builtins.str] = None,
    enable_setting: typing.Optional[builtins.str] = None,
    environment_identifier: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    project_identifier: typing.Optional[builtins.str] = None,
    publish_on_import: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    recommendation: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.RecommendationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    schedule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.ScheduleConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97dfe47605dbb87ccbbe262f292763127ef5d758f6baa4d2f590467983a24bdf(
    props: typing.Union[CfnDataSourceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c11e73196533c35e3d900830b3f50f68a1346ab8b7e91f03b6c2b8c3336d0937(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2516e95f01b70d41edbe694b681e8c77b0666e5332e8780d450866a2aec36f1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d068d3193f450095760cd2d2e1db7907b188e5c969a373167f12d64246aa561(
    *,
    glue_run_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.GlueRunConfigurationInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    redshift_run_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.RedshiftRunConfigurationInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sage_maker_run_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.SageMakerRunConfigurationInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d7ed4fb955bc5269367dee7e8ae3f366c9f372cd3a09a145c70929ff001fd0d(
    *,
    expression: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36cacacb64745d07552baaec7ebf0c9af44fb4b410bb116c89eb9e6ebae40560(
    *,
    content: typing.Optional[builtins.str] = None,
    form_name: typing.Optional[builtins.str] = None,
    type_identifier: typing.Optional[builtins.str] = None,
    type_revision: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f2dc4471ff38c3517b8c2fd9ce406b406c3f84a0444bdbd0d580829f3f508d9(
    *,
    auto_import_data_quality_result: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    catalog_name: typing.Optional[builtins.str] = None,
    data_access_role: typing.Optional[builtins.str] = None,
    relational_filter_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.RelationalFilterConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__660b6f84a16d272ee0b393c89f082a615fce2dd386f9e9f95a76e4720ce38906(
    *,
    enable_business_name_generation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59f2b0359caf418664272b43652cde32e11bf9aa52a3f27183f8eb574fa31d7e(
    *,
    cluster_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9dd81037daeed32cd4d31da001af5dbc17f4900f62578371138b8677ed8f48d(
    *,
    secret_manager_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f4ebaa25226101e239c7e0bfcc7cbfd5f5639816ffb257a325ff4dc3f49160c(
    *,
    data_access_role: typing.Optional[builtins.str] = None,
    redshift_credential_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.RedshiftCredentialConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    redshift_storage: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.RedshiftStorageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    relational_filter_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.RelationalFilterConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd36f268182471efa7ddd5df4fd3c87a2895bcf6c77b4315914ef73365bf9206(
    *,
    workgroup_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caaae179ea54cd864186f703b8b80af9ba3d031e35818087c1842f796e35d622(
    *,
    redshift_cluster_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.RedshiftClusterStorageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    redshift_serverless_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.RedshiftServerlessStorageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9326e933183228790b23db2ea9a56713b28613ec1a70fc284ce305ad84447df(
    *,
    database_name: typing.Optional[builtins.str] = None,
    filter_expressions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.FilterExpressionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    schema_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__903a03288a74a71d337e91fc80c82f8456a7bdc2460fb985267b158d74d99fae(
    *,
    tracking_assets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Sequence[builtins.str]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e928c10522fb42f71b1d428fce5f0d9884cabe8eca6726a6f7b9f78ef59b869(
    *,
    schedule: typing.Optional[builtins.str] = None,
    timezone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cc9c5a29897c93bd2f95061787b9e33629fdabb4f1d55f1090b594465c309d7(
    *,
    description: typing.Optional[builtins.str] = None,
    domain_execution_role: typing.Optional[builtins.str] = None,
    domain_version: typing.Optional[builtins.str] = None,
    kms_key_identifier: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    service_role: typing.Optional[builtins.str] = None,
    single_sign_on: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainPropsMixin.SingleSignOnProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0231c16af25ae96a053012b837e6619e179351c0f45276e60e55065358d2f032(
    props: typing.Union[CfnDomainMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2af63ed70682396625d248e3d29a13134618b14332247c449333e5c095cbeee(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9d79413c927fc5f0db1efaa96bfc3a86b1e4bf98836908729953c8b0da603c3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1cf7f62bb1eefcfe6cc0eee73e2a3c27a41680fcc61e045debe2ae61a8fa292(
    *,
    idc_instance_arn: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    user_assignment: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb6dadf30b844c2e40ac1d02ed42e9b411c76cfc7d75ee43b0a91c7b303560ac(
    *,
    description: typing.Optional[builtins.str] = None,
    domain_identifier: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    parent_domain_unit_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1b0d053215edd29e56463a34c3cc3b284f79584fbf81ff9a54c887afbb6c98f(
    props: typing.Union[CfnDomainUnitMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6006f66a1cfd2e13a74ab9052cf8d385365f9202e44ecab1c2ffa2e9193441ab(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3275d5340d618e54500682f053c2634e9648d32ae9d654112666a077f1e6c6e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e532cc5f450965ea79a0d5b035aa33e6b528f46a85cfc52acb0a7385be1eb39(
    *,
    description: typing.Optional[builtins.str] = None,
    domain_identifier: typing.Optional[builtins.str] = None,
    environment_identifier: typing.Optional[builtins.str] = None,
    identifier: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEnvironmentActionsPropsMixin.AwsConsoleLinkParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d53c0226ca85d454d8eeafa829de114002acf6ff12899af976cd211de7b001dc(
    props: typing.Union[CfnEnvironmentActionsMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10f03164e3dd3e40bb2ec31913e1652070a7553b722456cda515074a3c7a0eab(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b80b6bdc0e4af03186f3be7f55b096220710d227a6bf1b40c5491181feca710(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99aee996bf57858454c8c8e5ca17384b22dc8f7640419c2d2a23d799a8e781ed(
    *,
    uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f648c5778f26a1b92d4f8d5df19efc275b27b1f215eae5f54f9247ca74ae8057(
    *,
    domain_identifier: typing.Optional[builtins.str] = None,
    enabled_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    environment_blueprint_identifier: typing.Optional[builtins.str] = None,
    environment_role_permission_boundary: typing.Optional[builtins.str] = None,
    manage_access_role_arn: typing.Optional[builtins.str] = None,
    provisioning_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEnvironmentBlueprintConfigurationPropsMixin.ProvisioningConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    provisioning_role_arn: typing.Optional[builtins.str] = None,
    regional_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEnvironmentBlueprintConfigurationPropsMixin.RegionalParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13bc2299343995424d0a7a6afe7469f5941079b46f1cebe1b090a7ef0bcdaa22(
    props: typing.Union[CfnEnvironmentBlueprintConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31f39f3d678a7ef5574a416af2637d44c60ddba7b327eab2fdbd523c2d1ccf52(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b7f23e8ee44c5c18d130452cd4b58aa33fb2ce8b12a792f81d69f8792cdb8d9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0567ff0a6c1acd665b8391ce57e262a78a7e5a17f3e590610b82aaafbcc5dd5a(
    *,
    location_registration_exclude_s3_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
    location_registration_role: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4d3467ec9543b98c002aa55202af69ba96e2cc2af787244c70d9f39e2e0521e(
    *,
    lake_formation_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEnvironmentBlueprintConfigurationPropsMixin.LakeFormationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfe4f6e0c2f705acdfd343395f8a8f4d7be26ab32c5cd8245aea3be15423bd3a(
    *,
    parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60c8c23614e820064fa4fa09334ff89de65fc765d99fdc49bc9d163d8353be7b(
    *,
    description: typing.Optional[builtins.str] = None,
    domain_identifier: typing.Optional[builtins.str] = None,
    environment_account_identifier: typing.Optional[builtins.str] = None,
    environment_account_region: typing.Optional[builtins.str] = None,
    environment_profile_identifier: typing.Optional[builtins.str] = None,
    environment_role_arn: typing.Optional[builtins.str] = None,
    glossary_terms: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    project_identifier: typing.Optional[builtins.str] = None,
    user_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEnvironmentPropsMixin.EnvironmentParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6363d5c6236631f6931464c990d3c8049a3a475aec64a472f5b4b0983d903f41(
    *,
    aws_account_id: typing.Optional[builtins.str] = None,
    aws_account_region: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    domain_identifier: typing.Optional[builtins.str] = None,
    environment_blueprint_identifier: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    project_identifier: typing.Optional[builtins.str] = None,
    user_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEnvironmentProfilePropsMixin.EnvironmentParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a56642316673db881ea7b008cf7562aaeeba96e3e3a7dbadc58696cc2fca8cf7(
    props: typing.Union[CfnEnvironmentProfileMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e0de04a1963dd16eb973e2110b436c1919a33bdec51b601e59f6f6ab89d5d41(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ac61f36bf807794b45d1c60604eb3091d2c2027020f2e5ae8270ce3b09924cd(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a4ad7188de7e0538cff76886de88b7232ac003dda65d4d8ce12f0b32e003d50(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d4c368cbeac8b5477d2780a8e0764c6b50587cb54a2e13476a72f7520cc628c(
    props: typing.Union[CfnEnvironmentMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef87958fb07af031c16ff87f512f9060432a0f5fb478a46c8ce2ecb30a433eed(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7954752937fef374217943bf7696453c26d50b3d4226e689dde84cbc6e7dc225(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f35b6cdd950b506968a0e979010d47306c2cc204ee46a58b3553723a1aa4e267(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6ebafed279b613f6265187ea10c87fd84115ff112ad6d82406728b059aa5466(
    *,
    description: typing.Optional[builtins.str] = None,
    domain_identifier: typing.Optional[builtins.str] = None,
    model: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFormTypePropsMixin.ModelProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    owning_project_identifier: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7193b39b68d1e3cc2091cec7ff8541ec590f4ede540878026792596fe4569aea(
    props: typing.Union[CfnFormTypeMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1717c98302443f9d1bdda877c3d3cdded6387662adeae782ac5c053808aeb12e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec213309a8b99d3365dbc019f560c00981c927d8025745b9f4d26f2eb351149c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55a16529eff75aff941a429c115435744572a76d0af30f848596d4dcdee8824c(
    *,
    smithy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ceed13c14cc781ec411a58f27d38502b64f7581d33f989a2ccada7cb2d225d7(
    *,
    domain_identifier: typing.Optional[builtins.str] = None,
    group_identifier: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c027c8f5b624f22aff2f881b70032eb08da82f57088075b822a75847f9d21a20(
    props: typing.Union[CfnGroupProfileMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c98983d8b94dde4b66eb773a0857fd686e9596285a0a6dfec9c1e6d140e65fe(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9a7a768ccc2f61b0c68c4d0701817776dcca2252fcaa1cd75fe8c071724cd47(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1a26a7a00fe9988d332432c09985c9476c5152169714f5c986ea836d732ff6b(
    *,
    domain_identifier: typing.Optional[builtins.str] = None,
    entity_identifier: typing.Optional[builtins.str] = None,
    entity_type: typing.Optional[builtins.str] = None,
    owner: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOwnerPropsMixin.OwnerPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70b2424bdc582664b3c5802b2fea8ed695fc9be1ec801f16705dace63ad4da30(
    props: typing.Union[CfnOwnerMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2f8fb760b1d80d024de47de60a35c470748ca12a61f3a3ccc0ae5af3b2d510c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91e702fcbc8670affff9a27efd14fee4101c3da0aa1a0c1fcdacacf9ca487457(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__814a5dbe8db5abfd9acbd7071b5f62d344fbe0fc0cc7b98e278d63c21d0adf88(
    *,
    group_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__312f0c87cd85e7d121c743c41c4e335bb0f21b876c280b8d823bac0b8e51d61d(
    *,
    group: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOwnerPropsMixin.OwnerGroupPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    user: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOwnerPropsMixin.OwnerUserPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e59aa7dc3d8971606aa889f1c8dd2a742bf5238b7119b00ca6158a4e11ae8d4(
    *,
    user_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a384813d18ed257fb9fe940ccc0afb57ecd54672339329490ee56354100c1e55(
    *,
    detail: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPolicyGrantPropsMixin.PolicyGrantDetailProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    domain_identifier: typing.Optional[builtins.str] = None,
    entity_identifier: typing.Optional[builtins.str] = None,
    entity_type: typing.Optional[builtins.str] = None,
    policy_type: typing.Optional[builtins.str] = None,
    principal: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPolicyGrantPropsMixin.PolicyGrantPrincipalProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbcececaf9f67561a7abbba8d9d83d13be3d1c24f05fae8ab385aecd99cf8631(
    props: typing.Union[CfnPolicyGrantMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffc3b3f2b10267853c1fa65abb5bf71c63f6c4ae693d113993bffc9acb0aa558(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4f17711752c7dc90429018f94b025e7c90b19a413edcc33a78ab8954430b2c7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f2d6141ff52ea3add4ba7bb37d115f13f9e4c9e38b548b8792afe4bfe596365(
    *,
    include_child_domain_units: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__243801ca298e871b3ac9738db1312f93297bd30599f91267a6a8b04ba2879168(
    *,
    include_child_domain_units: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6df3f203ca6db2d8b11a71e0e33152de08d2088936e32249795018cf78f0202a(
    *,
    include_child_domain_units: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbab87c353e0aa6608b1d69a3a5622a80cf5a18d2b79d8b4caa9f8305b779b9c(
    *,
    domain_unit_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__507b28dbc0ee9a701d0543da6bb84339a2f8b4949df591fde6c7811d258ce0d1(
    *,
    include_child_domain_units: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df7e46166241996a3abe9a99e0d8453bd021b8f07ed07b6cf63ef67c6466fb89(
    *,
    include_child_domain_units: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b747b3565bf4602734c6e9df4e9cb154ae69dea5aa363a0aa4f8f17186df377(
    *,
    include_child_domain_units: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    project_profiles: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee429e5e238529a6a47c5e20fd8ebd8e9cce18d783f9578f8442ac1ccae6e579(
    *,
    include_child_domain_units: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__639e67758d17d3b0c93d7f0e667a9725c302e51c08b89125ba36a2fabf560ef1(
    *,
    domain_unit: typing.Optional[builtins.str] = None,
    include_child_domain_units: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfb3e90fcb84a09ba1197c48526a93d6a739b07d7c81eed661c67802adac95a8(
    *,
    all_domain_units_grant_filter: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da1bf6d9f26020ea6fe47991b861fd6d2451cc479100ae3e3cd2d8e3daa5fd4a(
    *,
    domain_unit_designation: typing.Optional[builtins.str] = None,
    domain_unit_grant_filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPolicyGrantPropsMixin.DomainUnitGrantFilterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    domain_unit_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6743efcff410080aafa26d1f63db78131ca414a712c1d1b3ab90754466d3ae7(
    *,
    group_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3665c090328a64bbc04304ab819e2b109490babd2f5bfecd4950819c9a815b75(
    *,
    include_child_domain_units: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb431944bc3a0856964b19a0371d2d5b7d1799f1b1156594e3218706ce119f2f(
    *,
    include_child_domain_units: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b33e36591c89ca092629fcca453def5a6f5690d0933de9351691e234842322b6(
    *,
    add_to_project_member_pool: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPolicyGrantPropsMixin.AddToProjectMemberPoolPolicyGrantDetailProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    create_asset_type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPolicyGrantPropsMixin.CreateAssetTypePolicyGrantDetailProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    create_domain_unit: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPolicyGrantPropsMixin.CreateDomainUnitPolicyGrantDetailProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    create_environment: typing.Any = None,
    create_environment_from_blueprint: typing.Any = None,
    create_environment_profile: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPolicyGrantPropsMixin.CreateEnvironmentProfilePolicyGrantDetailProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    create_form_type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPolicyGrantPropsMixin.CreateFormTypePolicyGrantDetailProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    create_glossary: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPolicyGrantPropsMixin.CreateGlossaryPolicyGrantDetailProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    create_project: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPolicyGrantPropsMixin.CreateProjectPolicyGrantDetailProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    create_project_from_project_profile: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPolicyGrantPropsMixin.CreateProjectFromProjectProfilePolicyGrantDetailProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    delegate_create_environment_profile: typing.Any = None,
    override_domain_unit_owners: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPolicyGrantPropsMixin.OverrideDomainUnitOwnersPolicyGrantDetailProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    override_project_owners: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPolicyGrantPropsMixin.OverrideProjectOwnersPolicyGrantDetailProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aa7abdddb67c265dbef959d13e6781120c69fb15e47b2dc2dfde43822b8fb4f(
    *,
    domain_unit: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPolicyGrantPropsMixin.DomainUnitPolicyGrantPrincipalProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    group: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPolicyGrantPropsMixin.GroupPolicyGrantPrincipalProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    project: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPolicyGrantPropsMixin.ProjectPolicyGrantPrincipalProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    user: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPolicyGrantPropsMixin.UserPolicyGrantPrincipalProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c3606b596404821a6fc53ec77e9d5b5b969fb655c0f157ca9b25f02e6f875ca(
    *,
    domain_unit_filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPolicyGrantPropsMixin.DomainUnitFilterForProjectProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d8b44e11106274b2b5a2f972cd76f511340a8eef2c67b2a1606964df7403c91(
    *,
    project_designation: typing.Optional[builtins.str] = None,
    project_grant_filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPolicyGrantPropsMixin.ProjectGrantFilterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    project_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__809b5d4b5d74b4f35c7a251183b45371c0443a7e8641a35e6029d9711b3e2145(
    *,
    all_users_grant_filter: typing.Any = None,
    user_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f5703f431726287b0868836e521692ce54a41a9ed4d188f40bd4289b641bb2d(
    *,
    designation: typing.Optional[builtins.str] = None,
    domain_identifier: typing.Optional[builtins.str] = None,
    member: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProjectMembershipPropsMixin.MemberProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    project_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f92c3693329474bc4aac8680ce6ca5fcb3ff6e0bff4fffb012f3dabbdbcac1e6(
    props: typing.Union[CfnProjectMembershipMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b34100031a4e0dcb69b9a86fff2bb0a0fcc1584c94899f75b077f0a550d3fdf0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f717494b229fa7ea3ab3ad432a0d071525df35124fcf03011ed9d67a987b4ed4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a800caa33ff96a0011456db73ca977b03b79bab8a26066b84a77fd652d5ec93(
    *,
    group_identifier: typing.Optional[builtins.str] = None,
    user_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dab82cb125a933cae2e48ac97bd712614fcfba86981f53f5c0d309a555246836(
    *,
    description: typing.Optional[builtins.str] = None,
    domain_identifier: typing.Optional[builtins.str] = None,
    domain_unit_id: typing.Optional[builtins.str] = None,
    glossary_terms: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    project_profile_id: typing.Optional[builtins.str] = None,
    project_profile_version: typing.Optional[builtins.str] = None,
    user_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProjectPropsMixin.EnvironmentConfigurationUserParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a81c5cc9dac80cb482163a48cd33f4a24739c194a1165bbd0dd5f860d9eb087(
    *,
    description: typing.Optional[builtins.str] = None,
    domain_identifier: typing.Optional[builtins.str] = None,
    domain_unit_identifier: typing.Optional[builtins.str] = None,
    environment_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProjectProfilePropsMixin.EnvironmentConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    name: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12b3bc78ba483281a971617a16ffcd6afb35dd5209fbeccaedb0a655ff02db04(
    props: typing.Union[CfnProjectProfileMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc131c07dc28b8be4016b8f1fe0dd7eb5a915bf40add412530da55140e222dfe(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fd1099f8954b7ea0d8dd0640a67ca8844e99be0d6eb4c39a14d87b345a267ca(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1aea1e8f8374658123a9a360f0e0d72eb893056b58d0c236a9e107ecb80ec83(
    *,
    aws_account_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0501da66c963197468ad3efa65ddbfe8744590e5a480ab65d1c29d3c3a0902ba(
    *,
    is_editable: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d83d8991794b9eefbd9f068be7d652aee1506bbd374b08c2cb821145071cc3c0(
    *,
    parameter_overrides: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProjectProfilePropsMixin.EnvironmentConfigurationParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resolved_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProjectProfilePropsMixin.EnvironmentConfigurationParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ssm_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6851456ab6150bef28b03895778dfb3b1e59a4d1afd0767f258c2effc4f0acc3(
    *,
    aws_account: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProjectProfilePropsMixin.AwsAccountProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    aws_region: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProjectProfilePropsMixin.RegionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    configuration_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProjectProfilePropsMixin.EnvironmentConfigurationParametersDetailsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    deployment_mode: typing.Optional[builtins.str] = None,
    deployment_order: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    environment_blueprint_id: typing.Optional[builtins.str] = None,
    environment_configuration_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04845c541d0e45395b74b0f8762aa2a833a22a08d6e5ef0d60c288fc4fa4335a(
    *,
    region_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edf16b5e398529a02ef4ad3cdc2b222250ed73c3b1edaba474ea71a1c1863729(
    props: typing.Union[CfnProjectMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80896da0fbcfde1b3b09ef0065d49ad1b2bcc70c2acb004ae0bb748dcdfe907d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0999d1b4e832dc9f5eb0fcc55b32f751ab640a1d696cf74dda3e46072d22a81(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ba49e4c515b41286712fd660f4dc1ff1beb7f8862bcac728df2c4c9500a7445(
    *,
    environment_configuration_name: typing.Optional[builtins.str] = None,
    environment_id: typing.Optional[builtins.str] = None,
    environment_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProjectPropsMixin.EnvironmentParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b52e32344bad00058f361c5248e5ef2e3d7375f58485de9e80e33119a6962465(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86154684569854cd554232051e2c0572bc7343decf3088b8098354bd5cd7d499(
    *,
    applicable_asset_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    authorized_principals: typing.Optional[typing.Sequence[builtins.str]] = None,
    domain_identifier: typing.Optional[builtins.str] = None,
    environment_identifier: typing.Optional[builtins.str] = None,
    manage_access_role: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    provider: typing.Optional[builtins.str] = None,
    subscription_target_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSubscriptionTargetPropsMixin.SubscriptionTargetFormProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae2093e93ce7728ce11d93d9f1cdc48aa8adfd61da09b3215640bcb9560b71c8(
    props: typing.Union[CfnSubscriptionTargetMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0abc9cb3b5e112933723a17a15ddd1446443eeedf86266f92b8f7c0964842708(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__708f31f0686b1211b83d8985884223f28dc83d3da683578d5764df880bc7c434(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3691e01e2282b16009e1b38afb9ade98c67417c4e976160b727c9724fdef7946(
    *,
    content: typing.Optional[builtins.str] = None,
    form_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64e344f8db1efaaef798ecba0f83d742564f5a3e87e4aadfcbc968b2900b8135(
    *,
    domain_identifier: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    user_identifier: typing.Optional[builtins.str] = None,
    user_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cce776297c684025be14c010cbd544fd589a264134fdd3a48ae0166144fe3813(
    props: typing.Union[CfnUserProfileMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dffa632b6e5cbc8128b6346e943da37b7e9f9f6326d5e4816c0d2ed74682e463(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a723c650ada28a6a5376c86b214cacaa25e124195edde9540a7ccabd017c7d9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca800bf8ac185199b62bcfc3b7536d9a7dff650bc97623c53ec6df747cf8e356(
    *,
    arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__398093199f2d8d3e450f108718e0b2da8d31045919d84e8436c86e9166ca629a(
    *,
    first_name: typing.Optional[builtins.str] = None,
    last_name: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8737a875264aad6de430a5e2a9c232b2ad85d290e5e58b7b23c0b55eb232690(
    *,
    iam: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserProfilePropsMixin.IamUserProfileDetailsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sso: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserProfilePropsMixin.SsoUserProfileDetailsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
