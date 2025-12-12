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
    jsii_type="@aws-cdk/mixins-preview.aws_opsworkscm.mixins.CfnServerMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "associate_public_ip_address": "associatePublicIpAddress",
        "backup_id": "backupId",
        "backup_retention_count": "backupRetentionCount",
        "custom_certificate": "customCertificate",
        "custom_domain": "customDomain",
        "custom_private_key": "customPrivateKey",
        "disable_automated_backup": "disableAutomatedBackup",
        "engine": "engine",
        "engine_attributes": "engineAttributes",
        "engine_model": "engineModel",
        "engine_version": "engineVersion",
        "instance_profile_arn": "instanceProfileArn",
        "instance_type": "instanceType",
        "key_pair": "keyPair",
        "preferred_backup_window": "preferredBackupWindow",
        "preferred_maintenance_window": "preferredMaintenanceWindow",
        "security_group_ids": "securityGroupIds",
        "service_role_arn": "serviceRoleArn",
        "subnet_ids": "subnetIds",
        "tags": "tags",
    },
)
class CfnServerMixinProps:
    def __init__(
        self,
        *,
        associate_public_ip_address: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        backup_id: typing.Optional[builtins.str] = None,
        backup_retention_count: typing.Optional[jsii.Number] = None,
        custom_certificate: typing.Optional[builtins.str] = None,
        custom_domain: typing.Optional[builtins.str] = None,
        custom_private_key: typing.Optional[builtins.str] = None,
        disable_automated_backup: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        engine: typing.Optional[builtins.str] = None,
        engine_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServerPropsMixin.EngineAttributeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        engine_model: typing.Optional[builtins.str] = None,
        engine_version: typing.Optional[builtins.str] = None,
        instance_profile_arn: typing.Optional[builtins.str] = None,
        instance_type: typing.Optional[builtins.str] = None,
        key_pair: typing.Optional[builtins.str] = None,
        preferred_backup_window: typing.Optional[builtins.str] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        service_role_arn: typing.Optional[builtins.str] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnServerPropsMixin.

        :param associate_public_ip_address: Associate a public IP address with a server that you are launching. Valid values are ``true`` or ``false`` . The default value is ``true`` .
        :param backup_id: If you specify this field, AWS OpsWorks CM creates the server by using the backup represented by BackupId.
        :param backup_retention_count: The number of automated backups that you want to keep. Whenever a new backup is created, AWS OpsWorks CM deletes the oldest backups if this number is exceeded. The default value is ``1`` .
        :param custom_certificate: Supported on servers running Chef Automate 2.0 only. A PEM-formatted HTTPS certificate. The value can be be a single, self-signed certificate, or a certificate chain. If you specify a custom certificate, you must also specify values for ``CustomDomain`` and ``CustomPrivateKey`` . The following are requirements for the ``CustomCertificate`` value:. - You can provide either a self-signed, custom certificate, or the full certificate chain. - The certificate must be a valid X509 certificate, or a certificate chain in PEM format. - The certificate must be valid at the time of upload. A certificate can't be used before its validity period begins (the certificate's ``NotBefore`` date), or after it expires (the certificate's ``NotAfter`` date). - The certificate’s common name or subject alternative names (SANs), if present, must match the value of ``CustomDomain`` . - The certificate must match the value of ``CustomPrivateKey`` .
        :param custom_domain: Supported on servers running Chef Automate 2.0 only. An optional public endpoint of a server, such as ``https://aws.my-company.com`` . To access the server, create a CNAME DNS record in your preferred DNS service that points the custom domain to the endpoint that is generated when the server is created (the value of the CreateServer Endpoint attribute). You cannot access the server by using the generated ``Endpoint`` value if the server is using a custom domain. If you specify a custom domain, you must also specify values for ``CustomCertificate`` and ``CustomPrivateKey`` .
        :param custom_private_key: Supported on servers running Chef Automate 2.0 only. A private key in PEM format for connecting to the server by using HTTPS. The private key must not be encrypted; it cannot be protected by a password or passphrase. If you specify a custom private key, you must also specify values for ``CustomDomain`` and ``CustomCertificate`` .
        :param disable_automated_backup: Enable or disable scheduled backups. Valid values are ``true`` or ``false`` . The default value is ``true`` .
        :param engine: The configuration management engine to use. Valid values include ``ChefAutomate`` and ``Puppet`` .
        :param engine_attributes: Optional engine attributes on a specified server. **Attributes accepted in a Chef createServer request:** - ``CHEF_AUTOMATE_PIVOTAL_KEY`` : A base64-encoded RSA public key. The corresponding private key is required to access the Chef API. When no CHEF_AUTOMATE_PIVOTAL_KEY is set, a private key is generated and returned in the response. When you are specifying the value of CHEF_AUTOMATE_PIVOTAL_KEY as a parameter in the CloudFormation console, you must add newline ( ``\\n`` ) characters at the end of each line of the pivotal key value. - ``CHEF_AUTOMATE_ADMIN_PASSWORD`` : The password for the administrative user in the Chef Automate web-based dashboard. The password length is a minimum of eight characters, and a maximum of 32. The password can contain letters, numbers, and special characters (!/@#$%^&+=_). The password must contain at least one lower case letter, one upper case letter, one number, and one special character. When no CHEF_AUTOMATE_ADMIN_PASSWORD is set, one is generated and returned in the response. **Attributes accepted in a Puppet createServer request:** - ``PUPPET_ADMIN_PASSWORD`` : To work with the Puppet Enterprise console, a password must use ASCII characters. - ``PUPPET_R10K_REMOTE`` : The r10k remote is the URL of your control repository (for example, ssh://git@your.git-repo.com:user/control-repo.git). Specifying an r10k remote opens TCP port 8170. - ``PUPPET_R10K_PRIVATE_KEY`` : If you are using a private Git repository, add PUPPET_R10K_PRIVATE_KEY to specify a PEM-encoded private SSH key.
        :param engine_model: The engine model of the server. Valid values in this release include ``Monolithic`` for Puppet and ``Single`` for Chef.
        :param engine_version: The major release version of the engine that you want to use. For a Chef server, the valid value for EngineVersion is currently ``2`` . For a Puppet server, valid values are ``2019`` or ``2017`` .
        :param instance_profile_arn: The ARN of the instance profile that your Amazon EC2 instances use.
        :param instance_type: The Amazon EC2 instance type to use. For example, ``m5.large`` .
        :param key_pair: The Amazon EC2 key pair to set for the instance. This parameter is optional; if desired, you may specify this parameter to connect to your instances by using SSH.
        :param preferred_backup_window: The start time for a one-hour period during which AWS OpsWorks CM backs up application-level data on your server if automated backups are enabled. Valid values must be specified in one of the following formats: - ``HH:MM`` for daily backups - ``DDD:HH:MM`` for weekly backups ``MM`` must be specified as ``00`` . The specified time is in coordinated universal time (UTC). The default value is a random, daily start time. *Example:* ``08:00`` , which represents a daily start time of 08:00 UTC. *Example:* ``Mon:08:00`` , which represents a start time of every Monday at 08:00 UTC. (8:00 a.m.)
        :param preferred_maintenance_window: The start time for a one-hour period each week during which AWS OpsWorks CM performs maintenance on the instance. Valid values must be specified in the following format: ``DDD:HH:MM`` . ``MM`` must be specified as ``00`` . The specified time is in coordinated universal time (UTC). The default value is a random one-hour period on Tuesday, Wednesday, or Friday. See ``TimeWindowDefinition`` for more information. *Example:* ``Mon:08:00`` , which represents a start time of every Monday at 08:00 UTC. (8:00 a.m.)
        :param security_group_ids: A list of security group IDs to attach to the Amazon EC2 instance. If you add this parameter, the specified security groups must be within the VPC that is specified by ``SubnetIds`` . If you do not specify this parameter, AWS OpsWorks CM creates one new security group that uses TCP ports 22 and 443, open to 0.0.0.0/0 (everyone).
        :param service_role_arn: The service role that the AWS OpsWorks CM service backend uses to work with your account.
        :param subnet_ids: The IDs of subnets in which to launch the server EC2 instance. Amazon EC2-Classic customers: This field is required. All servers must run within a VPC. The VPC must have "Auto Assign Public IP" enabled. EC2-VPC customers: This field is optional. If you do not specify subnet IDs, your EC2 instances are created in a default subnet that is selected by Amazon EC2. If you specify subnet IDs, the VPC must have "Auto Assign Public IP" enabled. For more information about supported Amazon EC2 platforms, see `Supported Platforms <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-supported-platforms.html>`_ .
        :param tags: A map that contains tag keys and tag values to attach to an AWS OpsWorks for Chef Automate or OpsWorks for Puppet Enterprise server. - The key cannot be empty. - The key can be a maximum of 127 characters, and can contain only Unicode letters, numbers, or separators, or the following special characters: `+ - = . _ : /

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_opsworkscm import mixins as opsworkscm_mixins
            
            cfn_server_mixin_props = opsworkscm_mixins.CfnServerMixinProps(
                associate_public_ip_address=False,
                backup_id="backupId",
                backup_retention_count=123,
                custom_certificate="customCertificate",
                custom_domain="customDomain",
                custom_private_key="customPrivateKey",
                disable_automated_backup=False,
                engine="engine",
                engine_attributes=[opsworkscm_mixins.CfnServerPropsMixin.EngineAttributeProperty(
                    name="name",
                    value="value"
                )],
                engine_model="engineModel",
                engine_version="engineVersion",
                instance_profile_arn="instanceProfileArn",
                instance_type="instanceType",
                key_pair="keyPair",
                preferred_backup_window="preferredBackupWindow",
                preferred_maintenance_window="preferredMaintenanceWindow",
                security_group_ids=["securityGroupIds"],
                service_role_arn="serviceRoleArn",
                subnet_ids=["subnetIds"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a4b9fd1539c56f5b63ed04f3bb4fa395570646f65147323c3a65b72654a345a)
            check_type(argname="argument associate_public_ip_address", value=associate_public_ip_address, expected_type=type_hints["associate_public_ip_address"])
            check_type(argname="argument backup_id", value=backup_id, expected_type=type_hints["backup_id"])
            check_type(argname="argument backup_retention_count", value=backup_retention_count, expected_type=type_hints["backup_retention_count"])
            check_type(argname="argument custom_certificate", value=custom_certificate, expected_type=type_hints["custom_certificate"])
            check_type(argname="argument custom_domain", value=custom_domain, expected_type=type_hints["custom_domain"])
            check_type(argname="argument custom_private_key", value=custom_private_key, expected_type=type_hints["custom_private_key"])
            check_type(argname="argument disable_automated_backup", value=disable_automated_backup, expected_type=type_hints["disable_automated_backup"])
            check_type(argname="argument engine", value=engine, expected_type=type_hints["engine"])
            check_type(argname="argument engine_attributes", value=engine_attributes, expected_type=type_hints["engine_attributes"])
            check_type(argname="argument engine_model", value=engine_model, expected_type=type_hints["engine_model"])
            check_type(argname="argument engine_version", value=engine_version, expected_type=type_hints["engine_version"])
            check_type(argname="argument instance_profile_arn", value=instance_profile_arn, expected_type=type_hints["instance_profile_arn"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument key_pair", value=key_pair, expected_type=type_hints["key_pair"])
            check_type(argname="argument preferred_backup_window", value=preferred_backup_window, expected_type=type_hints["preferred_backup_window"])
            check_type(argname="argument preferred_maintenance_window", value=preferred_maintenance_window, expected_type=type_hints["preferred_maintenance_window"])
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument service_role_arn", value=service_role_arn, expected_type=type_hints["service_role_arn"])
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if associate_public_ip_address is not None:
            self._values["associate_public_ip_address"] = associate_public_ip_address
        if backup_id is not None:
            self._values["backup_id"] = backup_id
        if backup_retention_count is not None:
            self._values["backup_retention_count"] = backup_retention_count
        if custom_certificate is not None:
            self._values["custom_certificate"] = custom_certificate
        if custom_domain is not None:
            self._values["custom_domain"] = custom_domain
        if custom_private_key is not None:
            self._values["custom_private_key"] = custom_private_key
        if disable_automated_backup is not None:
            self._values["disable_automated_backup"] = disable_automated_backup
        if engine is not None:
            self._values["engine"] = engine
        if engine_attributes is not None:
            self._values["engine_attributes"] = engine_attributes
        if engine_model is not None:
            self._values["engine_model"] = engine_model
        if engine_version is not None:
            self._values["engine_version"] = engine_version
        if instance_profile_arn is not None:
            self._values["instance_profile_arn"] = instance_profile_arn
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if key_pair is not None:
            self._values["key_pair"] = key_pair
        if preferred_backup_window is not None:
            self._values["preferred_backup_window"] = preferred_backup_window
        if preferred_maintenance_window is not None:
            self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if service_role_arn is not None:
            self._values["service_role_arn"] = service_role_arn
        if subnet_ids is not None:
            self._values["subnet_ids"] = subnet_ids
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def associate_public_ip_address(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Associate a public IP address with a server that you are launching.

        Valid values are ``true`` or ``false`` . The default value is ``true`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-associatepublicipaddress
        '''
        result = self._values.get("associate_public_ip_address")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def backup_id(self) -> typing.Optional[builtins.str]:
        '''If you specify this field, AWS OpsWorks CM creates the server by using the backup represented by BackupId.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-backupid
        '''
        result = self._values.get("backup_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def backup_retention_count(self) -> typing.Optional[jsii.Number]:
        '''The number of automated backups that you want to keep.

        Whenever a new backup is created, AWS OpsWorks CM deletes the oldest backups if this number is exceeded. The default value is ``1`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-backupretentioncount
        '''
        result = self._values.get("backup_retention_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def custom_certificate(self) -> typing.Optional[builtins.str]:
        '''Supported on servers running Chef Automate 2.0 only. A PEM-formatted HTTPS certificate. The value can be be a single, self-signed certificate, or a certificate chain. If you specify a custom certificate, you must also specify values for ``CustomDomain`` and ``CustomPrivateKey`` . The following are requirements for the ``CustomCertificate`` value:.

        - You can provide either a self-signed, custom certificate, or the full certificate chain.
        - The certificate must be a valid X509 certificate, or a certificate chain in PEM format.
        - The certificate must be valid at the time of upload. A certificate can't be used before its validity period begins (the certificate's ``NotBefore`` date), or after it expires (the certificate's ``NotAfter`` date).
        - The certificate’s common name or subject alternative names (SANs), if present, must match the value of ``CustomDomain`` .
        - The certificate must match the value of ``CustomPrivateKey`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-customcertificate
        '''
        result = self._values.get("custom_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_domain(self) -> typing.Optional[builtins.str]:
        '''Supported on servers running Chef Automate 2.0 only. An optional public endpoint of a server, such as ``https://aws.my-company.com`` . To access the server, create a CNAME DNS record in your preferred DNS service that points the custom domain to the endpoint that is generated when the server is created (the value of the CreateServer Endpoint attribute). You cannot access the server by using the generated ``Endpoint`` value if the server is using a custom domain. If you specify a custom domain, you must also specify values for ``CustomCertificate`` and ``CustomPrivateKey`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-customdomain
        '''
        result = self._values.get("custom_domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_private_key(self) -> typing.Optional[builtins.str]:
        '''Supported on servers running Chef Automate 2.0 only. A private key in PEM format for connecting to the server by using HTTPS. The private key must not be encrypted; it cannot be protected by a password or passphrase. If you specify a custom private key, you must also specify values for ``CustomDomain`` and ``CustomCertificate`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-customprivatekey
        '''
        result = self._values.get("custom_private_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_automated_backup(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Enable or disable scheduled backups.

        Valid values are ``true`` or ``false`` . The default value is ``true`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-disableautomatedbackup
        '''
        result = self._values.get("disable_automated_backup")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def engine(self) -> typing.Optional[builtins.str]:
        '''The configuration management engine to use.

        Valid values include ``ChefAutomate`` and ``Puppet`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-engine
        '''
        result = self._values.get("engine")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def engine_attributes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServerPropsMixin.EngineAttributeProperty"]]]]:
        '''Optional engine attributes on a specified server.

        **Attributes accepted in a Chef createServer request:** - ``CHEF_AUTOMATE_PIVOTAL_KEY`` : A base64-encoded RSA public key. The corresponding private key is required to access the Chef API. When no CHEF_AUTOMATE_PIVOTAL_KEY is set, a private key is generated and returned in the response. When you are specifying the value of CHEF_AUTOMATE_PIVOTAL_KEY as a parameter in the CloudFormation console, you must add newline ( ``\\n`` ) characters at the end of each line of the pivotal key value.

        - ``CHEF_AUTOMATE_ADMIN_PASSWORD`` : The password for the administrative user in the Chef Automate web-based dashboard. The password length is a minimum of eight characters, and a maximum of 32. The password can contain letters, numbers, and special characters (!/@#$%^&+=_). The password must contain at least one lower case letter, one upper case letter, one number, and one special character. When no CHEF_AUTOMATE_ADMIN_PASSWORD is set, one is generated and returned in the response.

        **Attributes accepted in a Puppet createServer request:** - ``PUPPET_ADMIN_PASSWORD`` : To work with the Puppet Enterprise console, a password must use ASCII characters.

        - ``PUPPET_R10K_REMOTE`` : The r10k remote is the URL of your control repository (for example, ssh://git@your.git-repo.com:user/control-repo.git). Specifying an r10k remote opens TCP port 8170.
        - ``PUPPET_R10K_PRIVATE_KEY`` : If you are using a private Git repository, add PUPPET_R10K_PRIVATE_KEY to specify a PEM-encoded private SSH key.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-engineattributes
        '''
        result = self._values.get("engine_attributes")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServerPropsMixin.EngineAttributeProperty"]]]], result)

    @builtins.property
    def engine_model(self) -> typing.Optional[builtins.str]:
        '''The engine model of the server.

        Valid values in this release include ``Monolithic`` for Puppet and ``Single`` for Chef.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-enginemodel
        '''
        result = self._values.get("engine_model")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def engine_version(self) -> typing.Optional[builtins.str]:
        '''The major release version of the engine that you want to use.

        For a Chef server, the valid value for EngineVersion is currently ``2`` . For a Puppet server, valid values are ``2019`` or ``2017`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-engineversion
        '''
        result = self._values.get("engine_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_profile_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the instance profile that your Amazon EC2 instances use.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-instanceprofilearn
        '''
        result = self._values.get("instance_profile_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[builtins.str]:
        '''The Amazon EC2 instance type to use.

        For example, ``m5.large`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-instancetype
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_pair(self) -> typing.Optional[builtins.str]:
        '''The Amazon EC2 key pair to set for the instance.

        This parameter is optional; if desired, you may specify this parameter to connect to your instances by using SSH.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-keypair
        '''
        result = self._values.get("key_pair")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preferred_backup_window(self) -> typing.Optional[builtins.str]:
        '''The start time for a one-hour period during which AWS OpsWorks CM backs up application-level data on your server if automated backups are enabled.

        Valid values must be specified in one of the following formats:

        - ``HH:MM`` for daily backups
        - ``DDD:HH:MM`` for weekly backups

        ``MM`` must be specified as ``00`` . The specified time is in coordinated universal time (UTC). The default value is a random, daily start time.

        *Example:* ``08:00`` , which represents a daily start time of 08:00 UTC.

        *Example:* ``Mon:08:00`` , which represents a start time of every Monday at 08:00 UTC. (8:00 a.m.)

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-preferredbackupwindow
        '''
        result = self._values.get("preferred_backup_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        '''The start time for a one-hour period each week during which AWS OpsWorks CM performs maintenance on the instance.

        Valid values must be specified in the following format: ``DDD:HH:MM`` . ``MM`` must be specified as ``00`` . The specified time is in coordinated universal time (UTC). The default value is a random one-hour period on Tuesday, Wednesday, or Friday. See ``TimeWindowDefinition`` for more information.

        *Example:* ``Mon:08:00`` , which represents a start time of every Monday at 08:00 UTC. (8:00 a.m.)

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-preferredmaintenancewindow
        '''
        result = self._values.get("preferred_maintenance_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of security group IDs to attach to the Amazon EC2 instance.

        If you add this parameter, the specified security groups must be within the VPC that is specified by ``SubnetIds`` .

        If you do not specify this parameter, AWS OpsWorks CM creates one new security group that uses TCP ports 22 and 443, open to 0.0.0.0/0 (everyone).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-securitygroupids
        '''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def service_role_arn(self) -> typing.Optional[builtins.str]:
        '''The service role that the AWS OpsWorks CM service backend uses to work with your account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-servicerolearn
        '''
        result = self._values.get("service_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The IDs of subnets in which to launch the server EC2 instance.

        Amazon EC2-Classic customers: This field is required. All servers must run within a VPC. The VPC must have "Auto Assign Public IP" enabled.

        EC2-VPC customers: This field is optional. If you do not specify subnet IDs, your EC2 instances are created in a default subnet that is selected by Amazon EC2. If you specify subnet IDs, the VPC must have "Auto Assign Public IP" enabled.

        For more information about supported Amazon EC2 platforms, see `Supported Platforms <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-supported-platforms.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-subnetids
        '''
        result = self._values.get("subnet_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A map that contains tag keys and tag values to attach to an AWS OpsWorks for Chef Automate or OpsWorks for Puppet Enterprise server.

        - The key cannot be empty.
        - The key can be a maximum of 127 characters, and can contain only Unicode letters, numbers, or separators, or the following special characters: `+ - = . _ : /

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-tags
        ::

        `

        - The value can be a maximum 255 characters, and contain only Unicode letters, numbers, or separators, or the following special characters: ``+ - = . _ : / @``
        - Leading and trailing spaces are trimmed from both the key and value.
        - A maximum of 50 user-applied tags is allowed for any AWS OpsWorks CM server.
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnServerMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnServerPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_opsworkscm.mixins.CfnServerPropsMixin",
):
    '''The ``AWS::OpsWorksCM::Server`` resource creates an AWS OpsWorks for Chef Automate or OpsWorks for Puppet Enterprise configuration management server.

    For more information, see `Create a Chef Automate Server in CloudFormation <https://docs.aws.amazon.com/opsworks/latest/userguide/opscm-create-server-cfn.html>`_ or `Create a Puppet Enterprise Master in CloudFormation <https://docs.aws.amazon.com/opsworks/latest/userguide/opspup-create-server-cfn.html>`_ in the *OpsWorks User Guide* , and `CreateServer <https://docs.aws.amazon.com/opsworks-cm/latest/APIReference/API_CreateServer.html>`_ in the *AWS OpsWorks CM API Reference* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html
    :cloudformationResource: AWS::OpsWorksCM::Server
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_opsworkscm import mixins as opsworkscm_mixins
        
        cfn_server_props_mixin = opsworkscm_mixins.CfnServerPropsMixin(opsworkscm_mixins.CfnServerMixinProps(
            associate_public_ip_address=False,
            backup_id="backupId",
            backup_retention_count=123,
            custom_certificate="customCertificate",
            custom_domain="customDomain",
            custom_private_key="customPrivateKey",
            disable_automated_backup=False,
            engine="engine",
            engine_attributes=[opsworkscm_mixins.CfnServerPropsMixin.EngineAttributeProperty(
                name="name",
                value="value"
            )],
            engine_model="engineModel",
            engine_version="engineVersion",
            instance_profile_arn="instanceProfileArn",
            instance_type="instanceType",
            key_pair="keyPair",
            preferred_backup_window="preferredBackupWindow",
            preferred_maintenance_window="preferredMaintenanceWindow",
            security_group_ids=["securityGroupIds"],
            service_role_arn="serviceRoleArn",
            subnet_ids=["subnetIds"],
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
        props: typing.Union[CfnServerMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::OpsWorksCM::Server``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f2df4b6a8266cc0e3a6ab1c06189b95fac1f5b137675594f2838beb07f221df)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c1a8f8a1e9952c30662f9914d03eab0a70bf0140e168d979d67e2b19687c77b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7694eab7ed2080771950b41b624f8192d5300d56890fabbcb38795f8c1fb815)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnServerMixinProps:
        return typing.cast(CfnServerMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opsworkscm.mixins.CfnServerPropsMixin.EngineAttributeProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class EngineAttributeProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``EngineAttribute`` property type specifies administrator credentials for an AWS OpsWorks for Chef Automate or OpsWorks for Puppet Enterprise server.

            ``EngineAttribute`` is a property of the ``AWS::OpsWorksCM::Server`` resource type.

            :param name: The name of the engine attribute. *Attribute name for Chef Automate servers:* - ``CHEF_AUTOMATE_ADMIN_PASSWORD`` *Attribute names for Puppet Enterprise servers:* - ``PUPPET_ADMIN_PASSWORD`` - ``PUPPET_R10K_REMOTE`` - ``PUPPET_R10K_PRIVATE_KEY``
            :param value: The value of the engine attribute. *Attribute value for Chef Automate servers:* - ``CHEF_AUTOMATE_PIVOTAL_KEY`` : A base64-encoded RSA public key. The corresponding private key is required to access the Chef API. You can generate this key by running the following `OpenSSL <https://docs.aws.amazon.com/https://www.openssl.org/>`_ command on Linux-based computers. ``openssl genrsa -out *pivotal_key_file_name* .pem 2048`` On Windows-based computers, you can use the PuTTYgen utility to generate a base64-encoded RSA private key. For more information, see `PuTTYgen - Key Generator for PuTTY on Windows <https://docs.aws.amazon.com/https://www.ssh.com/ssh/putty/windows/puttygen>`_ on SSH.com. *Attribute values for Puppet Enterprise servers:* - ``PUPPET_ADMIN_PASSWORD`` : An administrator password that you can use to sign in to the Puppet Enterprise console webpage after the server is online. The password must use between 8 and 32 ASCII characters. - ``PUPPET_R10K_REMOTE`` : The r10k remote is the URL of your control repository (for example, ssh://git@your.git-repo.com:user/control-repo.git). Specifying an r10k remote opens TCP port 8170. - ``PUPPET_R10K_PRIVATE_KEY`` : If you are using a private Git repository, add ``PUPPET_R10K_PRIVATE_KEY`` to specify a PEM-encoded private SSH key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworkscm-server-engineattribute.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opsworkscm import mixins as opsworkscm_mixins
                
                engine_attribute_property = opsworkscm_mixins.CfnServerPropsMixin.EngineAttributeProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6f2fa23a018fdfe702e238908e8722b966ccac4da81fa6d210db82373976114f)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the engine attribute.

            *Attribute name for Chef Automate servers:*

            - ``CHEF_AUTOMATE_ADMIN_PASSWORD``

            *Attribute names for Puppet Enterprise servers:*

            - ``PUPPET_ADMIN_PASSWORD``
            - ``PUPPET_R10K_REMOTE``
            - ``PUPPET_R10K_PRIVATE_KEY``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworkscm-server-engineattribute.html#cfn-opsworkscm-server-engineattribute-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value of the engine attribute.

            *Attribute value for Chef Automate servers:*

            - ``CHEF_AUTOMATE_PIVOTAL_KEY`` : A base64-encoded RSA public key. The corresponding private key is required to access the Chef API. You can generate this key by running the following `OpenSSL <https://docs.aws.amazon.com/https://www.openssl.org/>`_ command on Linux-based computers.

            ``openssl genrsa -out *pivotal_key_file_name* .pem 2048``

            On Windows-based computers, you can use the PuTTYgen utility to generate a base64-encoded RSA private key. For more information, see `PuTTYgen - Key Generator for PuTTY on Windows <https://docs.aws.amazon.com/https://www.ssh.com/ssh/putty/windows/puttygen>`_ on SSH.com.

            *Attribute values for Puppet Enterprise servers:*

            - ``PUPPET_ADMIN_PASSWORD`` : An administrator password that you can use to sign in to the Puppet Enterprise console webpage after the server is online. The password must use between 8 and 32 ASCII characters.
            - ``PUPPET_R10K_REMOTE`` : The r10k remote is the URL of your control repository (for example, ssh://git@your.git-repo.com:user/control-repo.git). Specifying an r10k remote opens TCP port 8170.
            - ``PUPPET_R10K_PRIVATE_KEY`` : If you are using a private Git repository, add ``PUPPET_R10K_PRIVATE_KEY`` to specify a PEM-encoded private SSH key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworkscm-server-engineattribute.html#cfn-opsworkscm-server-engineattribute-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EngineAttributeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnServerMixinProps",
    "CfnServerPropsMixin",
]

publication.publish()

def _typecheckingstub__5a4b9fd1539c56f5b63ed04f3bb4fa395570646f65147323c3a65b72654a345a(
    *,
    associate_public_ip_address: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    backup_id: typing.Optional[builtins.str] = None,
    backup_retention_count: typing.Optional[jsii.Number] = None,
    custom_certificate: typing.Optional[builtins.str] = None,
    custom_domain: typing.Optional[builtins.str] = None,
    custom_private_key: typing.Optional[builtins.str] = None,
    disable_automated_backup: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    engine: typing.Optional[builtins.str] = None,
    engine_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServerPropsMixin.EngineAttributeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    engine_model: typing.Optional[builtins.str] = None,
    engine_version: typing.Optional[builtins.str] = None,
    instance_profile_arn: typing.Optional[builtins.str] = None,
    instance_type: typing.Optional[builtins.str] = None,
    key_pair: typing.Optional[builtins.str] = None,
    preferred_backup_window: typing.Optional[builtins.str] = None,
    preferred_maintenance_window: typing.Optional[builtins.str] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    service_role_arn: typing.Optional[builtins.str] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f2df4b6a8266cc0e3a6ab1c06189b95fac1f5b137675594f2838beb07f221df(
    props: typing.Union[CfnServerMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c1a8f8a1e9952c30662f9914d03eab0a70bf0140e168d979d67e2b19687c77b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7694eab7ed2080771950b41b624f8192d5300d56890fabbcb38795f8c1fb815(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f2fa23a018fdfe702e238908e8722b966ccac4da81fa6d210db82373976114f(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
