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
    jsii_type="@aws-cdk/mixins-preview.aws_timestream.mixins.CfnDatabaseMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "database_name": "databaseName",
        "kms_key_id": "kmsKeyId",
        "tags": "tags",
    },
)
class CfnDatabaseMixinProps:
    def __init__(
        self,
        *,
        database_name: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDatabasePropsMixin.

        :param database_name: The name of the Timestream database. *Length Constraints* : Minimum length of 3 bytes. Maximum length of 256 bytes.
        :param kms_key_id: The identifier of the AWS key used to encrypt the data stored in the database.
        :param tags: The tags to add to the database.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-database.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_timestream import mixins as timestream_mixins
            
            cfn_database_mixin_props = timestream_mixins.CfnDatabaseMixinProps(
                database_name="databaseName",
                kms_key_id="kmsKeyId",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1e9846d2f16cc8dce581e7f97542c56eed18d1b54b5f31c90fca23a20198515)
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if database_name is not None:
            self._values["database_name"] = database_name
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def database_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Timestream database.

        *Length Constraints* : Minimum length of 3 bytes. Maximum length of 256 bytes.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-database.html#cfn-timestream-database-databasename
        '''
        result = self._values.get("database_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the AWS  key used to encrypt the data stored in the database.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-database.html#cfn-timestream-database-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags to add to the database.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-database.html#cfn-timestream-database-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDatabaseMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDatabasePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_timestream.mixins.CfnDatabasePropsMixin",
):
    '''Creates a new Timestream database.

    If the AWS  key is not specified, the database will be encrypted with a Timestream managed AWS  key located in your account. Refer to `AWS managed AWS  keys <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#aws-managed-cmk>`_ for more info. `Service quotas apply <https://docs.aws.amazon.com/timestream/latest/developerguide/ts-limits.html>`_ . See `code sample <https://docs.aws.amazon.com/timestream/latest/developerguide/code-samples.create-db.html>`_ for details.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-database.html
    :cloudformationResource: AWS::Timestream::Database
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_timestream import mixins as timestream_mixins
        
        cfn_database_props_mixin = timestream_mixins.CfnDatabasePropsMixin(timestream_mixins.CfnDatabaseMixinProps(
            database_name="databaseName",
            kms_key_id="kmsKeyId",
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
        props: typing.Union[CfnDatabaseMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Timestream::Database``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6452e68c861457e83198f369445a760611e35b723aca7ef25f9035c8deca2c8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__de2c902b01e428376ef84f7406836d4c0486da6872af53e6673bc7eb5f664601)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8bfb650f52755e250c0bda0bbd74a3a995b5491a12ccc31f23342b9a053a8b9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDatabaseMixinProps:
        return typing.cast(CfnDatabaseMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_timestream.mixins.CfnInfluxDBInstanceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "allocated_storage": "allocatedStorage",
        "bucket": "bucket",
        "db_instance_type": "dbInstanceType",
        "db_parameter_group_identifier": "dbParameterGroupIdentifier",
        "db_storage_type": "dbStorageType",
        "deployment_type": "deploymentType",
        "log_delivery_configuration": "logDeliveryConfiguration",
        "name": "name",
        "network_type": "networkType",
        "organization": "organization",
        "password": "password",
        "port": "port",
        "publicly_accessible": "publiclyAccessible",
        "tags": "tags",
        "username": "username",
        "vpc_security_group_ids": "vpcSecurityGroupIds",
        "vpc_subnet_ids": "vpcSubnetIds",
    },
)
class CfnInfluxDBInstanceMixinProps:
    def __init__(
        self,
        *,
        allocated_storage: typing.Optional[jsii.Number] = None,
        bucket: typing.Optional[builtins.str] = None,
        db_instance_type: typing.Optional[builtins.str] = None,
        db_parameter_group_identifier: typing.Optional[builtins.str] = None,
        db_storage_type: typing.Optional[builtins.str] = None,
        deployment_type: typing.Optional[builtins.str] = None,
        log_delivery_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInfluxDBInstancePropsMixin.LogDeliveryConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        network_type: typing.Optional[builtins.str] = None,
        organization: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        publicly_accessible: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        username: typing.Optional[builtins.str] = None,
        vpc_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpc_subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for CfnInfluxDBInstancePropsMixin.

        :param allocated_storage: The amount of storage to allocate for your DB storage type in GiB (gibibytes).
        :param bucket: The name of the initial InfluxDB bucket. All InfluxDB data is stored in a bucket. A bucket combines the concept of a database and a retention period (the duration of time that each data point persists). A bucket belongs to an organization.
        :param db_instance_type: The Timestream for InfluxDB DB instance type to run on.
        :param db_parameter_group_identifier: The name or id of the DB parameter group to assign to your DB instance. DB parameter groups specify how the database is configured. For example, DB parameter groups can specify the limit for query concurrency.
        :param db_storage_type: The Timestream for InfluxDB DB storage type to read and write InfluxDB data. You can choose between 3 different types of provisioned Influx IOPS included storage according to your workloads requirements: - Influx IO Included 3000 IOPS - Influx IO Included 12000 IOPS - Influx IO Included 16000 IOPS
        :param deployment_type: Specifies whether the Timestream for InfluxDB is deployed as Single-AZ or with a MultiAZ Standby for High availability.
        :param log_delivery_configuration: Configuration for sending InfluxDB engine logs to a specified S3 bucket.
        :param name: The name that uniquely identifies the DB instance when interacting with the Amazon Timestream for InfluxDB API and CLI commands. This name will also be a prefix included in the endpoint. DB instance names must be unique per customer and per region.
        :param network_type: Network type of the InfluxDB Instance.
        :param organization: The name of the initial organization for the initial admin user in InfluxDB. An InfluxDB organization is a workspace for a group of users.
        :param password: The password of the initial admin user created in InfluxDB. This password will allow you to access the InfluxDB UI to perform various administrative tasks and also use the InfluxDB CLI to create an operator token. These attributes will be stored in a Secret created in Amazon SecretManager in your account.
        :param port: The port number on which InfluxDB accepts connections.
        :param publicly_accessible: Configures the DB instance with a public IP to facilitate access. Default: - false
        :param tags: A list of key-value pairs to associate with the DB instance.
        :param username: The username of the initial admin user created in InfluxDB. Must start with a letter and can't end with a hyphen or contain two consecutive hyphens. For example, my-user1. This username will allow you to access the InfluxDB UI to perform various administrative tasks and also use the InfluxDB CLI to create an operator token. These attributes will be stored in a Secret created in Amazon Secrets Manager in your account.
        :param vpc_security_group_ids: A list of VPC security group IDs to associate with the DB instance.
        :param vpc_subnet_ids: A list of VPC subnet IDs to associate with the DB instance. Provide at least two VPC subnet IDs in different availability zones when deploying with a Multi-AZ standby.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-influxdbinstance.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_timestream import mixins as timestream_mixins
            
            cfn_influx_dBInstance_mixin_props = timestream_mixins.CfnInfluxDBInstanceMixinProps(
                allocated_storage=123,
                bucket="bucket",
                db_instance_type="dbInstanceType",
                db_parameter_group_identifier="dbParameterGroupIdentifier",
                db_storage_type="dbStorageType",
                deployment_type="deploymentType",
                log_delivery_configuration=timestream_mixins.CfnInfluxDBInstancePropsMixin.LogDeliveryConfigurationProperty(
                    s3_configuration=timestream_mixins.CfnInfluxDBInstancePropsMixin.S3ConfigurationProperty(
                        bucket_name="bucketName",
                        enabled=False
                    )
                ),
                name="name",
                network_type="networkType",
                organization="organization",
                password="password",
                port=123,
                publicly_accessible=False,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                username="username",
                vpc_security_group_ids=["vpcSecurityGroupIds"],
                vpc_subnet_ids=["vpcSubnetIds"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7c20324dcab11aed90e73132d2d2d67817629388742b7bb4bc1695bff32f467)
            check_type(argname="argument allocated_storage", value=allocated_storage, expected_type=type_hints["allocated_storage"])
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument db_instance_type", value=db_instance_type, expected_type=type_hints["db_instance_type"])
            check_type(argname="argument db_parameter_group_identifier", value=db_parameter_group_identifier, expected_type=type_hints["db_parameter_group_identifier"])
            check_type(argname="argument db_storage_type", value=db_storage_type, expected_type=type_hints["db_storage_type"])
            check_type(argname="argument deployment_type", value=deployment_type, expected_type=type_hints["deployment_type"])
            check_type(argname="argument log_delivery_configuration", value=log_delivery_configuration, expected_type=type_hints["log_delivery_configuration"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network_type", value=network_type, expected_type=type_hints["network_type"])
            check_type(argname="argument organization", value=organization, expected_type=type_hints["organization"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument publicly_accessible", value=publicly_accessible, expected_type=type_hints["publicly_accessible"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument vpc_security_group_ids", value=vpc_security_group_ids, expected_type=type_hints["vpc_security_group_ids"])
            check_type(argname="argument vpc_subnet_ids", value=vpc_subnet_ids, expected_type=type_hints["vpc_subnet_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allocated_storage is not None:
            self._values["allocated_storage"] = allocated_storage
        if bucket is not None:
            self._values["bucket"] = bucket
        if db_instance_type is not None:
            self._values["db_instance_type"] = db_instance_type
        if db_parameter_group_identifier is not None:
            self._values["db_parameter_group_identifier"] = db_parameter_group_identifier
        if db_storage_type is not None:
            self._values["db_storage_type"] = db_storage_type
        if deployment_type is not None:
            self._values["deployment_type"] = deployment_type
        if log_delivery_configuration is not None:
            self._values["log_delivery_configuration"] = log_delivery_configuration
        if name is not None:
            self._values["name"] = name
        if network_type is not None:
            self._values["network_type"] = network_type
        if organization is not None:
            self._values["organization"] = organization
        if password is not None:
            self._values["password"] = password
        if port is not None:
            self._values["port"] = port
        if publicly_accessible is not None:
            self._values["publicly_accessible"] = publicly_accessible
        if tags is not None:
            self._values["tags"] = tags
        if username is not None:
            self._values["username"] = username
        if vpc_security_group_ids is not None:
            self._values["vpc_security_group_ids"] = vpc_security_group_ids
        if vpc_subnet_ids is not None:
            self._values["vpc_subnet_ids"] = vpc_subnet_ids

    @builtins.property
    def allocated_storage(self) -> typing.Optional[jsii.Number]:
        '''The amount of storage to allocate for your DB storage type in GiB (gibibytes).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-influxdbinstance.html#cfn-timestream-influxdbinstance-allocatedstorage
        '''
        result = self._values.get("allocated_storage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def bucket(self) -> typing.Optional[builtins.str]:
        '''The name of the initial InfluxDB bucket.

        All InfluxDB data is stored in a bucket. A bucket combines the concept of a database and a retention period (the duration of time that each data point persists). A bucket belongs to an organization.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-influxdbinstance.html#cfn-timestream-influxdbinstance-bucket
        '''
        result = self._values.get("bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def db_instance_type(self) -> typing.Optional[builtins.str]:
        '''The Timestream for InfluxDB DB instance type to run on.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-influxdbinstance.html#cfn-timestream-influxdbinstance-dbinstancetype
        '''
        result = self._values.get("db_instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def db_parameter_group_identifier(self) -> typing.Optional[builtins.str]:
        '''The name or id of the DB parameter group to assign to your DB instance.

        DB parameter groups specify how the database is configured. For example, DB parameter groups can specify the limit for query concurrency.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-influxdbinstance.html#cfn-timestream-influxdbinstance-dbparametergroupidentifier
        '''
        result = self._values.get("db_parameter_group_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def db_storage_type(self) -> typing.Optional[builtins.str]:
        '''The Timestream for InfluxDB DB storage type to read and write InfluxDB data.

        You can choose between 3 different types of provisioned Influx IOPS included storage according to your workloads requirements:

        - Influx IO Included 3000 IOPS
        - Influx IO Included 12000 IOPS
        - Influx IO Included 16000 IOPS

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-influxdbinstance.html#cfn-timestream-influxdbinstance-dbstoragetype
        '''
        result = self._values.get("db_storage_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deployment_type(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the Timestream for InfluxDB is deployed as Single-AZ or with a MultiAZ Standby for High availability.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-influxdbinstance.html#cfn-timestream-influxdbinstance-deploymenttype
        '''
        result = self._values.get("deployment_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_delivery_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInfluxDBInstancePropsMixin.LogDeliveryConfigurationProperty"]]:
        '''Configuration for sending InfluxDB engine logs to a specified S3 bucket.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-influxdbinstance.html#cfn-timestream-influxdbinstance-logdeliveryconfiguration
        '''
        result = self._values.get("log_delivery_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInfluxDBInstancePropsMixin.LogDeliveryConfigurationProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name that uniquely identifies the DB instance when interacting with the Amazon Timestream for InfluxDB API and CLI commands.

        This name will also be a prefix included in the endpoint. DB instance names must be unique per customer and per region.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-influxdbinstance.html#cfn-timestream-influxdbinstance-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_type(self) -> typing.Optional[builtins.str]:
        '''Network type of the InfluxDB Instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-influxdbinstance.html#cfn-timestream-influxdbinstance-networktype
        '''
        result = self._values.get("network_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def organization(self) -> typing.Optional[builtins.str]:
        '''The name of the initial organization for the initial admin user in InfluxDB.

        An InfluxDB organization is a workspace for a group of users.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-influxdbinstance.html#cfn-timestream-influxdbinstance-organization
        '''
        result = self._values.get("organization")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''The password of the initial admin user created in InfluxDB.

        This password will allow you to access the InfluxDB UI to perform various administrative tasks and also use the InfluxDB CLI to create an operator token. These attributes will be stored in a Secret created in Amazon SecretManager in your account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-influxdbinstance.html#cfn-timestream-influxdbinstance-password
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The port number on which InfluxDB accepts connections.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-influxdbinstance.html#cfn-timestream-influxdbinstance-port
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def publicly_accessible(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Configures the DB instance with a public IP to facilitate access.

        :default: - false

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-influxdbinstance.html#cfn-timestream-influxdbinstance-publiclyaccessible
        '''
        result = self._values.get("publicly_accessible")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of key-value pairs to associate with the DB instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-influxdbinstance.html#cfn-timestream-influxdbinstance-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''The username of the initial admin user created in InfluxDB.

        Must start with a letter and can't end with a hyphen or contain two consecutive hyphens. For example, my-user1. This username will allow you to access the InfluxDB UI to perform various administrative tasks and also use the InfluxDB CLI to create an operator token. These attributes will be stored in a Secret created in Amazon Secrets Manager in your account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-influxdbinstance.html#cfn-timestream-influxdbinstance-username
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of VPC security group IDs to associate with the DB instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-influxdbinstance.html#cfn-timestream-influxdbinstance-vpcsecuritygroupids
        '''
        result = self._values.get("vpc_security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def vpc_subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of VPC subnet IDs to associate with the DB instance.

        Provide at least two VPC subnet IDs in different availability zones when deploying with a Multi-AZ standby.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-influxdbinstance.html#cfn-timestream-influxdbinstance-vpcsubnetids
        '''
        result = self._values.get("vpc_subnet_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnInfluxDBInstanceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnInfluxDBInstancePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_timestream.mixins.CfnInfluxDBInstancePropsMixin",
):
    '''A DB instance is an isolated database environment running in the cloud.

    It is the basic building block of Amazon Timestream for InfluxDB. A DB instance can contain multiple user-created databases (or organizations and buckets for the case of InfluxDb 2.x databases), and can be accessed using the same client tools and applications you might use to access a standalone self-managed InfluxDB instance.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-influxdbinstance.html
    :cloudformationResource: AWS::Timestream::InfluxDBInstance
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_timestream import mixins as timestream_mixins
        
        cfn_influx_dBInstance_props_mixin = timestream_mixins.CfnInfluxDBInstancePropsMixin(timestream_mixins.CfnInfluxDBInstanceMixinProps(
            allocated_storage=123,
            bucket="bucket",
            db_instance_type="dbInstanceType",
            db_parameter_group_identifier="dbParameterGroupIdentifier",
            db_storage_type="dbStorageType",
            deployment_type="deploymentType",
            log_delivery_configuration=timestream_mixins.CfnInfluxDBInstancePropsMixin.LogDeliveryConfigurationProperty(
                s3_configuration=timestream_mixins.CfnInfluxDBInstancePropsMixin.S3ConfigurationProperty(
                    bucket_name="bucketName",
                    enabled=False
                )
            ),
            name="name",
            network_type="networkType",
            organization="organization",
            password="password",
            port=123,
            publicly_accessible=False,
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            username="username",
            vpc_security_group_ids=["vpcSecurityGroupIds"],
            vpc_subnet_ids=["vpcSubnetIds"]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnInfluxDBInstanceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Timestream::InfluxDBInstance``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcccec0d5b15c9785d2a950e7005cc1bf9e91a10852c5c965f6b697163abfb4b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d80ce4ff7bee3dee043ec8dd347b83c275ffb8f181d82dd5a6e093e03cf8d41)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60da0a513573533398fd2c2aef91402674fe1d19d84584bb0884df23cde39a70)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnInfluxDBInstanceMixinProps:
        return typing.cast(CfnInfluxDBInstanceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_timestream.mixins.CfnInfluxDBInstancePropsMixin.LogDeliveryConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_configuration": "s3Configuration"},
    )
    class LogDeliveryConfigurationProperty:
        def __init__(
            self,
            *,
            s3_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInfluxDBInstancePropsMixin.S3ConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Configuration for sending InfluxDB engine logs to a specified S3 bucket.

            :param s3_configuration: Configuration for S3 bucket log delivery.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-influxdbinstance-logdeliveryconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_timestream import mixins as timestream_mixins
                
                log_delivery_configuration_property = timestream_mixins.CfnInfluxDBInstancePropsMixin.LogDeliveryConfigurationProperty(
                    s3_configuration=timestream_mixins.CfnInfluxDBInstancePropsMixin.S3ConfigurationProperty(
                        bucket_name="bucketName",
                        enabled=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1aa13ba0b579a4b2225be37b9123170bea434ff47911481d8edc64b8b0d0b358)
                check_type(argname="argument s3_configuration", value=s3_configuration, expected_type=type_hints["s3_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3_configuration is not None:
                self._values["s3_configuration"] = s3_configuration

        @builtins.property
        def s3_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInfluxDBInstancePropsMixin.S3ConfigurationProperty"]]:
            '''Configuration for S3 bucket log delivery.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-influxdbinstance-logdeliveryconfiguration.html#cfn-timestream-influxdbinstance-logdeliveryconfiguration-s3configuration
            '''
            result = self._values.get("s3_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInfluxDBInstancePropsMixin.S3ConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogDeliveryConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_timestream.mixins.CfnInfluxDBInstancePropsMixin.S3ConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket_name": "bucketName", "enabled": "enabled"},
    )
    class S3ConfigurationProperty:
        def __init__(
            self,
            *,
            bucket_name: typing.Optional[builtins.str] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Configuration for S3 bucket log delivery.

            :param bucket_name: The bucket name of the customer S3 bucket.
            :param enabled: Indicates whether log delivery to the S3 bucket is enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-influxdbinstance-s3configuration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_timestream import mixins as timestream_mixins
                
                s3_configuration_property = timestream_mixins.CfnInfluxDBInstancePropsMixin.S3ConfigurationProperty(
                    bucket_name="bucketName",
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bd4786b9a5d59b59ab7bbaae6ae745ed7a7ef2576e5b33d22bc424985a15bfdb)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_name is not None:
                self._values["bucket_name"] = bucket_name
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def bucket_name(self) -> typing.Optional[builtins.str]:
            '''The bucket name of the customer S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-influxdbinstance-s3configuration.html#cfn-timestream-influxdbinstance-s3configuration-bucketname
            '''
            result = self._values.get("bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether log delivery to the S3 bucket is enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-influxdbinstance-s3configuration.html#cfn-timestream-influxdbinstance-s3configuration-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3ConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_timestream.mixins.CfnScheduledQueryMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "client_token": "clientToken",
        "error_report_configuration": "errorReportConfiguration",
        "kms_key_id": "kmsKeyId",
        "notification_configuration": "notificationConfiguration",
        "query_string": "queryString",
        "schedule_configuration": "scheduleConfiguration",
        "scheduled_query_execution_role_arn": "scheduledQueryExecutionRoleArn",
        "scheduled_query_name": "scheduledQueryName",
        "tags": "tags",
        "target_configuration": "targetConfiguration",
    },
)
class CfnScheduledQueryMixinProps:
    def __init__(
        self,
        *,
        client_token: typing.Optional[builtins.str] = None,
        error_report_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScheduledQueryPropsMixin.ErrorReportConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        notification_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScheduledQueryPropsMixin.NotificationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        query_string: typing.Optional[builtins.str] = None,
        schedule_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScheduledQueryPropsMixin.ScheduleConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        scheduled_query_execution_role_arn: typing.Optional[builtins.str] = None,
        scheduled_query_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        target_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScheduledQueryPropsMixin.TargetConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnScheduledQueryPropsMixin.

        :param client_token: Using a ClientToken makes the call to CreateScheduledQuery idempotent, in other words, making the same request repeatedly will produce the same result. Making multiple identical CreateScheduledQuery requests has the same effect as making a single request. - If CreateScheduledQuery is called without a ``ClientToken`` , the Query SDK generates a ``ClientToken`` on your behalf. - After 8 hours, any request with the same ``ClientToken`` is treated as a new request.
        :param error_report_configuration: Configuration for error reporting. Error reports will be generated when a problem is encountered when writing the query results.
        :param kms_key_id: The Amazon KMS key used to encrypt the scheduled query resource, at-rest. If the Amazon KMS key is not specified, the scheduled query resource will be encrypted with a Timestream owned Amazon KMS key. To specify a KMS key, use the key ID, key ARN, alias name, or alias ARN. When using an alias name, prefix the name with *alias/* If ErrorReportConfiguration uses ``SSE_KMS`` as encryption type, the same KmsKeyId is used to encrypt the error report at rest.
        :param notification_configuration: Notification configuration for the scheduled query. A notification is sent by Timestream when a query run finishes, when the state is updated or when you delete it.
        :param query_string: The query string to run. Parameter names can be specified in the query string ``@`` character followed by an identifier. The named Parameter ``@scheduled_runtime`` is reserved and can be used in the query to get the time at which the query is scheduled to run. The timestamp calculated according to the ScheduleConfiguration parameter, will be the value of ``@scheduled_runtime`` paramater for each query run. For example, consider an instance of a scheduled query executing on 2021-12-01 00:00:00. For this instance, the ``@scheduled_runtime`` parameter is initialized to the timestamp 2021-12-01 00:00:00 when invoking the query.
        :param schedule_configuration: Schedule configuration.
        :param scheduled_query_execution_role_arn: The ARN for the IAM role that Timestream will assume when running the scheduled query.
        :param scheduled_query_name: A name for the query. Scheduled query names must be unique within each Region.
        :param tags: A list of key-value pairs to label the scheduled query.
        :param target_configuration: Scheduled query target store configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_timestream import mixins as timestream_mixins
            
            cfn_scheduled_query_mixin_props = timestream_mixins.CfnScheduledQueryMixinProps(
                client_token="clientToken",
                error_report_configuration=timestream_mixins.CfnScheduledQueryPropsMixin.ErrorReportConfigurationProperty(
                    s3_configuration=timestream_mixins.CfnScheduledQueryPropsMixin.S3ConfigurationProperty(
                        bucket_name="bucketName",
                        encryption_option="encryptionOption",
                        object_key_prefix="objectKeyPrefix"
                    )
                ),
                kms_key_id="kmsKeyId",
                notification_configuration=timestream_mixins.CfnScheduledQueryPropsMixin.NotificationConfigurationProperty(
                    sns_configuration=timestream_mixins.CfnScheduledQueryPropsMixin.SnsConfigurationProperty(
                        topic_arn="topicArn"
                    )
                ),
                query_string="queryString",
                schedule_configuration=timestream_mixins.CfnScheduledQueryPropsMixin.ScheduleConfigurationProperty(
                    schedule_expression="scheduleExpression"
                ),
                scheduled_query_execution_role_arn="scheduledQueryExecutionRoleArn",
                scheduled_query_name="scheduledQueryName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                target_configuration=timestream_mixins.CfnScheduledQueryPropsMixin.TargetConfigurationProperty(
                    timestream_configuration=timestream_mixins.CfnScheduledQueryPropsMixin.TimestreamConfigurationProperty(
                        database_name="databaseName",
                        dimension_mappings=[timestream_mixins.CfnScheduledQueryPropsMixin.DimensionMappingProperty(
                            dimension_value_type="dimensionValueType",
                            name="name"
                        )],
                        measure_name_column="measureNameColumn",
                        mixed_measure_mappings=[timestream_mixins.CfnScheduledQueryPropsMixin.MixedMeasureMappingProperty(
                            measure_name="measureName",
                            measure_value_type="measureValueType",
                            multi_measure_attribute_mappings=[timestream_mixins.CfnScheduledQueryPropsMixin.MultiMeasureAttributeMappingProperty(
                                measure_value_type="measureValueType",
                                source_column="sourceColumn",
                                target_multi_measure_attribute_name="targetMultiMeasureAttributeName"
                            )],
                            source_column="sourceColumn",
                            target_measure_name="targetMeasureName"
                        )],
                        multi_measure_mappings=timestream_mixins.CfnScheduledQueryPropsMixin.MultiMeasureMappingsProperty(
                            multi_measure_attribute_mappings=[timestream_mixins.CfnScheduledQueryPropsMixin.MultiMeasureAttributeMappingProperty(
                                measure_value_type="measureValueType",
                                source_column="sourceColumn",
                                target_multi_measure_attribute_name="targetMultiMeasureAttributeName"
                            )],
                            target_multi_measure_name="targetMultiMeasureName"
                        ),
                        table_name="tableName",
                        time_column="timeColumn"
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4babe77ab1b35efb3124eba9bff6d0d2adbfa346b9ca667c619b7658b2097af)
            check_type(argname="argument client_token", value=client_token, expected_type=type_hints["client_token"])
            check_type(argname="argument error_report_configuration", value=error_report_configuration, expected_type=type_hints["error_report_configuration"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument notification_configuration", value=notification_configuration, expected_type=type_hints["notification_configuration"])
            check_type(argname="argument query_string", value=query_string, expected_type=type_hints["query_string"])
            check_type(argname="argument schedule_configuration", value=schedule_configuration, expected_type=type_hints["schedule_configuration"])
            check_type(argname="argument scheduled_query_execution_role_arn", value=scheduled_query_execution_role_arn, expected_type=type_hints["scheduled_query_execution_role_arn"])
            check_type(argname="argument scheduled_query_name", value=scheduled_query_name, expected_type=type_hints["scheduled_query_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument target_configuration", value=target_configuration, expected_type=type_hints["target_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_token is not None:
            self._values["client_token"] = client_token
        if error_report_configuration is not None:
            self._values["error_report_configuration"] = error_report_configuration
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if notification_configuration is not None:
            self._values["notification_configuration"] = notification_configuration
        if query_string is not None:
            self._values["query_string"] = query_string
        if schedule_configuration is not None:
            self._values["schedule_configuration"] = schedule_configuration
        if scheduled_query_execution_role_arn is not None:
            self._values["scheduled_query_execution_role_arn"] = scheduled_query_execution_role_arn
        if scheduled_query_name is not None:
            self._values["scheduled_query_name"] = scheduled_query_name
        if tags is not None:
            self._values["tags"] = tags
        if target_configuration is not None:
            self._values["target_configuration"] = target_configuration

    @builtins.property
    def client_token(self) -> typing.Optional[builtins.str]:
        '''Using a ClientToken makes the call to CreateScheduledQuery idempotent, in other words, making the same request repeatedly will produce the same result.

        Making multiple identical CreateScheduledQuery requests has the same effect as making a single request.

        - If CreateScheduledQuery is called without a ``ClientToken`` , the Query SDK generates a ``ClientToken`` on your behalf.
        - After 8 hours, any request with the same ``ClientToken`` is treated as a new request.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-clienttoken
        '''
        result = self._values.get("client_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def error_report_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScheduledQueryPropsMixin.ErrorReportConfigurationProperty"]]:
        '''Configuration for error reporting.

        Error reports will be generated when a problem is encountered when writing the query results.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-errorreportconfiguration
        '''
        result = self._values.get("error_report_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScheduledQueryPropsMixin.ErrorReportConfigurationProperty"]], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The Amazon KMS key used to encrypt the scheduled query resource, at-rest.

        If the Amazon KMS key is not specified, the scheduled query resource will be encrypted with a Timestream owned Amazon KMS key. To specify a KMS key, use the key ID, key ARN, alias name, or alias ARN. When using an alias name, prefix the name with *alias/*

        If ErrorReportConfiguration uses ``SSE_KMS`` as encryption type, the same KmsKeyId is used to encrypt the error report at rest.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScheduledQueryPropsMixin.NotificationConfigurationProperty"]]:
        '''Notification configuration for the scheduled query.

        A notification is sent by Timestream when a query run finishes, when the state is updated or when you delete it.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-notificationconfiguration
        '''
        result = self._values.get("notification_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScheduledQueryPropsMixin.NotificationConfigurationProperty"]], result)

    @builtins.property
    def query_string(self) -> typing.Optional[builtins.str]:
        '''The query string to run.

        Parameter names can be specified in the query string ``@`` character followed by an identifier. The named Parameter ``@scheduled_runtime`` is reserved and can be used in the query to get the time at which the query is scheduled to run.

        The timestamp calculated according to the ScheduleConfiguration parameter, will be the value of ``@scheduled_runtime`` paramater for each query run. For example, consider an instance of a scheduled query executing on 2021-12-01 00:00:00. For this instance, the ``@scheduled_runtime`` parameter is initialized to the timestamp 2021-12-01 00:00:00 when invoking the query.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-querystring
        '''
        result = self._values.get("query_string")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScheduledQueryPropsMixin.ScheduleConfigurationProperty"]]:
        '''Schedule configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-scheduleconfiguration
        '''
        result = self._values.get("schedule_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScheduledQueryPropsMixin.ScheduleConfigurationProperty"]], result)

    @builtins.property
    def scheduled_query_execution_role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN for the IAM role that Timestream will assume when running the scheduled query.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-scheduledqueryexecutionrolearn
        '''
        result = self._values.get("scheduled_query_execution_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scheduled_query_name(self) -> typing.Optional[builtins.str]:
        '''A name for the query.

        Scheduled query names must be unique within each Region.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-scheduledqueryname
        '''
        result = self._values.get("scheduled_query_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of key-value pairs to label the scheduled query.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def target_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScheduledQueryPropsMixin.TargetConfigurationProperty"]]:
        '''Scheduled query target store configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-targetconfiguration
        '''
        result = self._values.get("target_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScheduledQueryPropsMixin.TargetConfigurationProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnScheduledQueryMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnScheduledQueryPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_timestream.mixins.CfnScheduledQueryPropsMixin",
):
    '''Create a scheduled query that will be run on your behalf at the configured schedule.

    Timestream assumes the execution role provided as part of the ``ScheduledQueryExecutionRoleArn`` parameter to run the query. You can use the ``NotificationConfiguration`` parameter to configure notification for your scheduled query operations.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html
    :cloudformationResource: AWS::Timestream::ScheduledQuery
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_timestream import mixins as timestream_mixins
        
        cfn_scheduled_query_props_mixin = timestream_mixins.CfnScheduledQueryPropsMixin(timestream_mixins.CfnScheduledQueryMixinProps(
            client_token="clientToken",
            error_report_configuration=timestream_mixins.CfnScheduledQueryPropsMixin.ErrorReportConfigurationProperty(
                s3_configuration=timestream_mixins.CfnScheduledQueryPropsMixin.S3ConfigurationProperty(
                    bucket_name="bucketName",
                    encryption_option="encryptionOption",
                    object_key_prefix="objectKeyPrefix"
                )
            ),
            kms_key_id="kmsKeyId",
            notification_configuration=timestream_mixins.CfnScheduledQueryPropsMixin.NotificationConfigurationProperty(
                sns_configuration=timestream_mixins.CfnScheduledQueryPropsMixin.SnsConfigurationProperty(
                    topic_arn="topicArn"
                )
            ),
            query_string="queryString",
            schedule_configuration=timestream_mixins.CfnScheduledQueryPropsMixin.ScheduleConfigurationProperty(
                schedule_expression="scheduleExpression"
            ),
            scheduled_query_execution_role_arn="scheduledQueryExecutionRoleArn",
            scheduled_query_name="scheduledQueryName",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            target_configuration=timestream_mixins.CfnScheduledQueryPropsMixin.TargetConfigurationProperty(
                timestream_configuration=timestream_mixins.CfnScheduledQueryPropsMixin.TimestreamConfigurationProperty(
                    database_name="databaseName",
                    dimension_mappings=[timestream_mixins.CfnScheduledQueryPropsMixin.DimensionMappingProperty(
                        dimension_value_type="dimensionValueType",
                        name="name"
                    )],
                    measure_name_column="measureNameColumn",
                    mixed_measure_mappings=[timestream_mixins.CfnScheduledQueryPropsMixin.MixedMeasureMappingProperty(
                        measure_name="measureName",
                        measure_value_type="measureValueType",
                        multi_measure_attribute_mappings=[timestream_mixins.CfnScheduledQueryPropsMixin.MultiMeasureAttributeMappingProperty(
                            measure_value_type="measureValueType",
                            source_column="sourceColumn",
                            target_multi_measure_attribute_name="targetMultiMeasureAttributeName"
                        )],
                        source_column="sourceColumn",
                        target_measure_name="targetMeasureName"
                    )],
                    multi_measure_mappings=timestream_mixins.CfnScheduledQueryPropsMixin.MultiMeasureMappingsProperty(
                        multi_measure_attribute_mappings=[timestream_mixins.CfnScheduledQueryPropsMixin.MultiMeasureAttributeMappingProperty(
                            measure_value_type="measureValueType",
                            source_column="sourceColumn",
                            target_multi_measure_attribute_name="targetMultiMeasureAttributeName"
                        )],
                        target_multi_measure_name="targetMultiMeasureName"
                    ),
                    table_name="tableName",
                    time_column="timeColumn"
                )
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnScheduledQueryMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Timestream::ScheduledQuery``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4e8543e82a440b3ba9607bb1abbf1dbbfde2554a5f08e60923a20518a95c74a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cca2b47866664dbe1859392fefa064718351f3acb690c6e6e54ccb47227460c0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bbe644cb9f7be5265f4b6f4024be89fae7cc5bb59b9751de0135e748a052fb2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnScheduledQueryMixinProps:
        return typing.cast(CfnScheduledQueryMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_timestream.mixins.CfnScheduledQueryPropsMixin.DimensionMappingProperty",
        jsii_struct_bases=[],
        name_mapping={"dimension_value_type": "dimensionValueType", "name": "name"},
    )
    class DimensionMappingProperty:
        def __init__(
            self,
            *,
            dimension_value_type: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''This type is used to map column(s) from the query result to a dimension in the destination table.

            :param dimension_value_type: Type for the dimension: VARCHAR.
            :param name: Column name from query result.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-dimensionmapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_timestream import mixins as timestream_mixins
                
                dimension_mapping_property = timestream_mixins.CfnScheduledQueryPropsMixin.DimensionMappingProperty(
                    dimension_value_type="dimensionValueType",
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e83e5459a50bd38cdb34166b5b2fdac660a84024ffa7bb4afeca0febfb7e32a2)
                check_type(argname="argument dimension_value_type", value=dimension_value_type, expected_type=type_hints["dimension_value_type"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dimension_value_type is not None:
                self._values["dimension_value_type"] = dimension_value_type
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def dimension_value_type(self) -> typing.Optional[builtins.str]:
            '''Type for the dimension: VARCHAR.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-dimensionmapping.html#cfn-timestream-scheduledquery-dimensionmapping-dimensionvaluetype
            '''
            result = self._values.get("dimension_value_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''Column name from query result.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-dimensionmapping.html#cfn-timestream-scheduledquery-dimensionmapping-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DimensionMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_timestream.mixins.CfnScheduledQueryPropsMixin.ErrorReportConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_configuration": "s3Configuration"},
    )
    class ErrorReportConfigurationProperty:
        def __init__(
            self,
            *,
            s3_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScheduledQueryPropsMixin.S3ConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Configuration required for error reporting.

            :param s3_configuration: The S3 configuration for the error reports.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-errorreportconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_timestream import mixins as timestream_mixins
                
                error_report_configuration_property = timestream_mixins.CfnScheduledQueryPropsMixin.ErrorReportConfigurationProperty(
                    s3_configuration=timestream_mixins.CfnScheduledQueryPropsMixin.S3ConfigurationProperty(
                        bucket_name="bucketName",
                        encryption_option="encryptionOption",
                        object_key_prefix="objectKeyPrefix"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__504800b998db83569e18d8c1a90089505b18052d62954488dad69d66f2cdf583)
                check_type(argname="argument s3_configuration", value=s3_configuration, expected_type=type_hints["s3_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3_configuration is not None:
                self._values["s3_configuration"] = s3_configuration

        @builtins.property
        def s3_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScheduledQueryPropsMixin.S3ConfigurationProperty"]]:
            '''The S3 configuration for the error reports.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-errorreportconfiguration.html#cfn-timestream-scheduledquery-errorreportconfiguration-s3configuration
            '''
            result = self._values.get("s3_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScheduledQueryPropsMixin.S3ConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ErrorReportConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_timestream.mixins.CfnScheduledQueryPropsMixin.MixedMeasureMappingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "measure_name": "measureName",
            "measure_value_type": "measureValueType",
            "multi_measure_attribute_mappings": "multiMeasureAttributeMappings",
            "source_column": "sourceColumn",
            "target_measure_name": "targetMeasureName",
        },
    )
    class MixedMeasureMappingProperty:
        def __init__(
            self,
            *,
            measure_name: typing.Optional[builtins.str] = None,
            measure_value_type: typing.Optional[builtins.str] = None,
            multi_measure_attribute_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScheduledQueryPropsMixin.MultiMeasureAttributeMappingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            source_column: typing.Optional[builtins.str] = None,
            target_measure_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''MixedMeasureMappings are mappings that can be used to ingest data into a mixture of narrow and multi measures in the derived table.

            :param measure_name: Refers to the value of measure_name in a result row. This field is required if MeasureNameColumn is provided.
            :param measure_value_type: Type of the value that is to be read from sourceColumn. If the mapping is for MULTI, use MeasureValueType.MULTI.
            :param multi_measure_attribute_mappings: Required when measureValueType is MULTI. Attribute mappings for MULTI value measures.
            :param source_column: This field refers to the source column from which measure-value is to be read for result materialization.
            :param target_measure_name: Target measure name to be used. If not provided, the target measure name by default would be measure-name if provided, or sourceColumn otherwise.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-mixedmeasuremapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_timestream import mixins as timestream_mixins
                
                mixed_measure_mapping_property = timestream_mixins.CfnScheduledQueryPropsMixin.MixedMeasureMappingProperty(
                    measure_name="measureName",
                    measure_value_type="measureValueType",
                    multi_measure_attribute_mappings=[timestream_mixins.CfnScheduledQueryPropsMixin.MultiMeasureAttributeMappingProperty(
                        measure_value_type="measureValueType",
                        source_column="sourceColumn",
                        target_multi_measure_attribute_name="targetMultiMeasureAttributeName"
                    )],
                    source_column="sourceColumn",
                    target_measure_name="targetMeasureName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e0a98b35cdf5e53f5c9bba7b6db900ed30206ef9ee94380bbdd8598d068a2d0c)
                check_type(argname="argument measure_name", value=measure_name, expected_type=type_hints["measure_name"])
                check_type(argname="argument measure_value_type", value=measure_value_type, expected_type=type_hints["measure_value_type"])
                check_type(argname="argument multi_measure_attribute_mappings", value=multi_measure_attribute_mappings, expected_type=type_hints["multi_measure_attribute_mappings"])
                check_type(argname="argument source_column", value=source_column, expected_type=type_hints["source_column"])
                check_type(argname="argument target_measure_name", value=target_measure_name, expected_type=type_hints["target_measure_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if measure_name is not None:
                self._values["measure_name"] = measure_name
            if measure_value_type is not None:
                self._values["measure_value_type"] = measure_value_type
            if multi_measure_attribute_mappings is not None:
                self._values["multi_measure_attribute_mappings"] = multi_measure_attribute_mappings
            if source_column is not None:
                self._values["source_column"] = source_column
            if target_measure_name is not None:
                self._values["target_measure_name"] = target_measure_name

        @builtins.property
        def measure_name(self) -> typing.Optional[builtins.str]:
            '''Refers to the value of measure_name in a result row.

            This field is required if MeasureNameColumn is provided.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-mixedmeasuremapping.html#cfn-timestream-scheduledquery-mixedmeasuremapping-measurename
            '''
            result = self._values.get("measure_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def measure_value_type(self) -> typing.Optional[builtins.str]:
            '''Type of the value that is to be read from sourceColumn.

            If the mapping is for MULTI, use MeasureValueType.MULTI.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-mixedmeasuremapping.html#cfn-timestream-scheduledquery-mixedmeasuremapping-measurevaluetype
            '''
            result = self._values.get("measure_value_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def multi_measure_attribute_mappings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScheduledQueryPropsMixin.MultiMeasureAttributeMappingProperty"]]]]:
            '''Required when measureValueType is MULTI.

            Attribute mappings for MULTI value measures.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-mixedmeasuremapping.html#cfn-timestream-scheduledquery-mixedmeasuremapping-multimeasureattributemappings
            '''
            result = self._values.get("multi_measure_attribute_mappings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScheduledQueryPropsMixin.MultiMeasureAttributeMappingProperty"]]]], result)

        @builtins.property
        def source_column(self) -> typing.Optional[builtins.str]:
            '''This field refers to the source column from which measure-value is to be read for result materialization.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-mixedmeasuremapping.html#cfn-timestream-scheduledquery-mixedmeasuremapping-sourcecolumn
            '''
            result = self._values.get("source_column")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_measure_name(self) -> typing.Optional[builtins.str]:
            '''Target measure name to be used.

            If not provided, the target measure name by default would be measure-name if provided, or sourceColumn otherwise.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-mixedmeasuremapping.html#cfn-timestream-scheduledquery-mixedmeasuremapping-targetmeasurename
            '''
            result = self._values.get("target_measure_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MixedMeasureMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_timestream.mixins.CfnScheduledQueryPropsMixin.MultiMeasureAttributeMappingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "measure_value_type": "measureValueType",
            "source_column": "sourceColumn",
            "target_multi_measure_attribute_name": "targetMultiMeasureAttributeName",
        },
    )
    class MultiMeasureAttributeMappingProperty:
        def __init__(
            self,
            *,
            measure_value_type: typing.Optional[builtins.str] = None,
            source_column: typing.Optional[builtins.str] = None,
            target_multi_measure_attribute_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Attribute mapping for MULTI value measures.

            :param measure_value_type: Type of the attribute to be read from the source column.
            :param source_column: Source column from where the attribute value is to be read.
            :param target_multi_measure_attribute_name: Custom name to be used for attribute name in derived table. If not provided, source column name would be used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-multimeasureattributemapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_timestream import mixins as timestream_mixins
                
                multi_measure_attribute_mapping_property = timestream_mixins.CfnScheduledQueryPropsMixin.MultiMeasureAttributeMappingProperty(
                    measure_value_type="measureValueType",
                    source_column="sourceColumn",
                    target_multi_measure_attribute_name="targetMultiMeasureAttributeName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5019f5c4e75d9dd91b50b9ebb68612fb27e61f82145f72ccb6838cbe96ef0649)
                check_type(argname="argument measure_value_type", value=measure_value_type, expected_type=type_hints["measure_value_type"])
                check_type(argname="argument source_column", value=source_column, expected_type=type_hints["source_column"])
                check_type(argname="argument target_multi_measure_attribute_name", value=target_multi_measure_attribute_name, expected_type=type_hints["target_multi_measure_attribute_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if measure_value_type is not None:
                self._values["measure_value_type"] = measure_value_type
            if source_column is not None:
                self._values["source_column"] = source_column
            if target_multi_measure_attribute_name is not None:
                self._values["target_multi_measure_attribute_name"] = target_multi_measure_attribute_name

        @builtins.property
        def measure_value_type(self) -> typing.Optional[builtins.str]:
            '''Type of the attribute to be read from the source column.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-multimeasureattributemapping.html#cfn-timestream-scheduledquery-multimeasureattributemapping-measurevaluetype
            '''
            result = self._values.get("measure_value_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_column(self) -> typing.Optional[builtins.str]:
            '''Source column from where the attribute value is to be read.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-multimeasureattributemapping.html#cfn-timestream-scheduledquery-multimeasureattributemapping-sourcecolumn
            '''
            result = self._values.get("source_column")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_multi_measure_attribute_name(self) -> typing.Optional[builtins.str]:
            '''Custom name to be used for attribute name in derived table.

            If not provided, source column name would be used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-multimeasureattributemapping.html#cfn-timestream-scheduledquery-multimeasureattributemapping-targetmultimeasureattributename
            '''
            result = self._values.get("target_multi_measure_attribute_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MultiMeasureAttributeMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_timestream.mixins.CfnScheduledQueryPropsMixin.MultiMeasureMappingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "multi_measure_attribute_mappings": "multiMeasureAttributeMappings",
            "target_multi_measure_name": "targetMultiMeasureName",
        },
    )
    class MultiMeasureMappingsProperty:
        def __init__(
            self,
            *,
            multi_measure_attribute_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScheduledQueryPropsMixin.MultiMeasureAttributeMappingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            target_multi_measure_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Only one of MixedMeasureMappings or MultiMeasureMappings is to be provided.

            MultiMeasureMappings can be used to ingest data as multi measures in the derived table.

            :param multi_measure_attribute_mappings: Required. Attribute mappings to be used for mapping query results to ingest data for multi-measure attributes.
            :param target_multi_measure_name: The name of the target multi-measure name in the derived table. This input is required when measureNameColumn is not provided. If MeasureNameColumn is provided, then value from that column will be used as multi-measure name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-multimeasuremappings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_timestream import mixins as timestream_mixins
                
                multi_measure_mappings_property = timestream_mixins.CfnScheduledQueryPropsMixin.MultiMeasureMappingsProperty(
                    multi_measure_attribute_mappings=[timestream_mixins.CfnScheduledQueryPropsMixin.MultiMeasureAttributeMappingProperty(
                        measure_value_type="measureValueType",
                        source_column="sourceColumn",
                        target_multi_measure_attribute_name="targetMultiMeasureAttributeName"
                    )],
                    target_multi_measure_name="targetMultiMeasureName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5244fe6fc4a3eade1a814b9f3a46620c570a9ae6195516774c3e5852f5f143be)
                check_type(argname="argument multi_measure_attribute_mappings", value=multi_measure_attribute_mappings, expected_type=type_hints["multi_measure_attribute_mappings"])
                check_type(argname="argument target_multi_measure_name", value=target_multi_measure_name, expected_type=type_hints["target_multi_measure_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if multi_measure_attribute_mappings is not None:
                self._values["multi_measure_attribute_mappings"] = multi_measure_attribute_mappings
            if target_multi_measure_name is not None:
                self._values["target_multi_measure_name"] = target_multi_measure_name

        @builtins.property
        def multi_measure_attribute_mappings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScheduledQueryPropsMixin.MultiMeasureAttributeMappingProperty"]]]]:
            '''Required.

            Attribute mappings to be used for mapping query results to ingest data for multi-measure attributes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-multimeasuremappings.html#cfn-timestream-scheduledquery-multimeasuremappings-multimeasureattributemappings
            '''
            result = self._values.get("multi_measure_attribute_mappings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScheduledQueryPropsMixin.MultiMeasureAttributeMappingProperty"]]]], result)

        @builtins.property
        def target_multi_measure_name(self) -> typing.Optional[builtins.str]:
            '''The name of the target multi-measure name in the derived table.

            This input is required when measureNameColumn is not provided. If MeasureNameColumn is provided, then value from that column will be used as multi-measure name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-multimeasuremappings.html#cfn-timestream-scheduledquery-multimeasuremappings-targetmultimeasurename
            '''
            result = self._values.get("target_multi_measure_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MultiMeasureMappingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_timestream.mixins.CfnScheduledQueryPropsMixin.NotificationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"sns_configuration": "snsConfiguration"},
    )
    class NotificationConfigurationProperty:
        def __init__(
            self,
            *,
            sns_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScheduledQueryPropsMixin.SnsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Notification configuration for a scheduled query.

            A notification is sent by Timestream when a scheduled query is created, its state is updated or when it is deleted.

            :param sns_configuration: Details on SNS configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-notificationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_timestream import mixins as timestream_mixins
                
                notification_configuration_property = timestream_mixins.CfnScheduledQueryPropsMixin.NotificationConfigurationProperty(
                    sns_configuration=timestream_mixins.CfnScheduledQueryPropsMixin.SnsConfigurationProperty(
                        topic_arn="topicArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c52fc1af9f4f46b365fd7f37bb73ae788ec4861b881f8fd7bbb0e9d96774e35a)
                check_type(argname="argument sns_configuration", value=sns_configuration, expected_type=type_hints["sns_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if sns_configuration is not None:
                self._values["sns_configuration"] = sns_configuration

        @builtins.property
        def sns_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScheduledQueryPropsMixin.SnsConfigurationProperty"]]:
            '''Details on SNS configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-notificationconfiguration.html#cfn-timestream-scheduledquery-notificationconfiguration-snsconfiguration
            '''
            result = self._values.get("sns_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScheduledQueryPropsMixin.SnsConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NotificationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_timestream.mixins.CfnScheduledQueryPropsMixin.S3ConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_name": "bucketName",
            "encryption_option": "encryptionOption",
            "object_key_prefix": "objectKeyPrefix",
        },
    )
    class S3ConfigurationProperty:
        def __init__(
            self,
            *,
            bucket_name: typing.Optional[builtins.str] = None,
            encryption_option: typing.Optional[builtins.str] = None,
            object_key_prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Details on S3 location for error reports that result from running a query.

            :param bucket_name: Name of the S3 bucket under which error reports will be created.
            :param encryption_option: Encryption at rest options for the error reports. If no encryption option is specified, Timestream will choose SSE_S3 as default.
            :param object_key_prefix: Prefix for the error report key. Timestream by default adds the following prefix to the error report path.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-s3configuration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_timestream import mixins as timestream_mixins
                
                s3_configuration_property = timestream_mixins.CfnScheduledQueryPropsMixin.S3ConfigurationProperty(
                    bucket_name="bucketName",
                    encryption_option="encryptionOption",
                    object_key_prefix="objectKeyPrefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b857960eafe1612c06bf9b365c54d7260e454926930108ed46528f9d33ec7e12)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument encryption_option", value=encryption_option, expected_type=type_hints["encryption_option"])
                check_type(argname="argument object_key_prefix", value=object_key_prefix, expected_type=type_hints["object_key_prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_name is not None:
                self._values["bucket_name"] = bucket_name
            if encryption_option is not None:
                self._values["encryption_option"] = encryption_option
            if object_key_prefix is not None:
                self._values["object_key_prefix"] = object_key_prefix

        @builtins.property
        def bucket_name(self) -> typing.Optional[builtins.str]:
            '''Name of the S3 bucket under which error reports will be created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-s3configuration.html#cfn-timestream-scheduledquery-s3configuration-bucketname
            '''
            result = self._values.get("bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def encryption_option(self) -> typing.Optional[builtins.str]:
            '''Encryption at rest options for the error reports.

            If no encryption option is specified, Timestream will choose SSE_S3 as default.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-s3configuration.html#cfn-timestream-scheduledquery-s3configuration-encryptionoption
            '''
            result = self._values.get("encryption_option")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def object_key_prefix(self) -> typing.Optional[builtins.str]:
            '''Prefix for the error report key.

            Timestream by default adds the following prefix to the error report path.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-s3configuration.html#cfn-timestream-scheduledquery-s3configuration-objectkeyprefix
            '''
            result = self._values.get("object_key_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3ConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_timestream.mixins.CfnScheduledQueryPropsMixin.ScheduleConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"schedule_expression": "scheduleExpression"},
    )
    class ScheduleConfigurationProperty:
        def __init__(
            self,
            *,
            schedule_expression: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration of the schedule of the query.

            :param schedule_expression: An expression that denotes when to trigger the scheduled query run. This can be a cron expression or a rate expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-scheduleconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_timestream import mixins as timestream_mixins
                
                schedule_configuration_property = timestream_mixins.CfnScheduledQueryPropsMixin.ScheduleConfigurationProperty(
                    schedule_expression="scheduleExpression"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fccfe5fcb114b391a10bdfc7519bc97b4d96e1ba00090bf9f565ec8cad3b4272)
                check_type(argname="argument schedule_expression", value=schedule_expression, expected_type=type_hints["schedule_expression"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if schedule_expression is not None:
                self._values["schedule_expression"] = schedule_expression

        @builtins.property
        def schedule_expression(self) -> typing.Optional[builtins.str]:
            '''An expression that denotes when to trigger the scheduled query run.

            This can be a cron expression or a rate expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-scheduleconfiguration.html#cfn-timestream-scheduledquery-scheduleconfiguration-scheduleexpression
            '''
            result = self._values.get("schedule_expression")
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
        jsii_type="@aws-cdk/mixins-preview.aws_timestream.mixins.CfnScheduledQueryPropsMixin.SnsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"topic_arn": "topicArn"},
    )
    class SnsConfigurationProperty:
        def __init__(self, *, topic_arn: typing.Optional[builtins.str] = None) -> None:
            '''Details on SNS that are required to send the notification.

            :param topic_arn: SNS topic ARN that the scheduled query status notifications will be sent to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-snsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_timestream import mixins as timestream_mixins
                
                sns_configuration_property = timestream_mixins.CfnScheduledQueryPropsMixin.SnsConfigurationProperty(
                    topic_arn="topicArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__db6fb6a60b3bb34786f09b81775ae95831610938ea2871d0fafb33d09c07798e)
                check_type(argname="argument topic_arn", value=topic_arn, expected_type=type_hints["topic_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if topic_arn is not None:
                self._values["topic_arn"] = topic_arn

        @builtins.property
        def topic_arn(self) -> typing.Optional[builtins.str]:
            '''SNS topic ARN that the scheduled query status notifications will be sent to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-snsconfiguration.html#cfn-timestream-scheduledquery-snsconfiguration-topicarn
            '''
            result = self._values.get("topic_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SnsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_timestream.mixins.CfnScheduledQueryPropsMixin.TargetConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"timestream_configuration": "timestreamConfiguration"},
    )
    class TargetConfigurationProperty:
        def __init__(
            self,
            *,
            timestream_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScheduledQueryPropsMixin.TimestreamConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Configuration used for writing the output of a query.

            :param timestream_configuration: Configuration needed to write data into the Timestream database and table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-targetconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_timestream import mixins as timestream_mixins
                
                target_configuration_property = timestream_mixins.CfnScheduledQueryPropsMixin.TargetConfigurationProperty(
                    timestream_configuration=timestream_mixins.CfnScheduledQueryPropsMixin.TimestreamConfigurationProperty(
                        database_name="databaseName",
                        dimension_mappings=[timestream_mixins.CfnScheduledQueryPropsMixin.DimensionMappingProperty(
                            dimension_value_type="dimensionValueType",
                            name="name"
                        )],
                        measure_name_column="measureNameColumn",
                        mixed_measure_mappings=[timestream_mixins.CfnScheduledQueryPropsMixin.MixedMeasureMappingProperty(
                            measure_name="measureName",
                            measure_value_type="measureValueType",
                            multi_measure_attribute_mappings=[timestream_mixins.CfnScheduledQueryPropsMixin.MultiMeasureAttributeMappingProperty(
                                measure_value_type="measureValueType",
                                source_column="sourceColumn",
                                target_multi_measure_attribute_name="targetMultiMeasureAttributeName"
                            )],
                            source_column="sourceColumn",
                            target_measure_name="targetMeasureName"
                        )],
                        multi_measure_mappings=timestream_mixins.CfnScheduledQueryPropsMixin.MultiMeasureMappingsProperty(
                            multi_measure_attribute_mappings=[timestream_mixins.CfnScheduledQueryPropsMixin.MultiMeasureAttributeMappingProperty(
                                measure_value_type="measureValueType",
                                source_column="sourceColumn",
                                target_multi_measure_attribute_name="targetMultiMeasureAttributeName"
                            )],
                            target_multi_measure_name="targetMultiMeasureName"
                        ),
                        table_name="tableName",
                        time_column="timeColumn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__218abc17ad74adc0e33da7e1df2b66e0c9de6a8462a236fb5f3a54c8e14a7d25)
                check_type(argname="argument timestream_configuration", value=timestream_configuration, expected_type=type_hints["timestream_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if timestream_configuration is not None:
                self._values["timestream_configuration"] = timestream_configuration

        @builtins.property
        def timestream_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScheduledQueryPropsMixin.TimestreamConfigurationProperty"]]:
            '''Configuration needed to write data into the Timestream database and table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-targetconfiguration.html#cfn-timestream-scheduledquery-targetconfiguration-timestreamconfiguration
            '''
            result = self._values.get("timestream_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScheduledQueryPropsMixin.TimestreamConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_timestream.mixins.CfnScheduledQueryPropsMixin.TimestreamConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "database_name": "databaseName",
            "dimension_mappings": "dimensionMappings",
            "measure_name_column": "measureNameColumn",
            "mixed_measure_mappings": "mixedMeasureMappings",
            "multi_measure_mappings": "multiMeasureMappings",
            "table_name": "tableName",
            "time_column": "timeColumn",
        },
    )
    class TimestreamConfigurationProperty:
        def __init__(
            self,
            *,
            database_name: typing.Optional[builtins.str] = None,
            dimension_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScheduledQueryPropsMixin.DimensionMappingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            measure_name_column: typing.Optional[builtins.str] = None,
            mixed_measure_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScheduledQueryPropsMixin.MixedMeasureMappingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            multi_measure_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScheduledQueryPropsMixin.MultiMeasureMappingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            table_name: typing.Optional[builtins.str] = None,
            time_column: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration to write data into Timestream database and table.

            This configuration allows the user to map the query result select columns into the destination table columns.

            :param database_name: Name of Timestream database to which the query result will be written.
            :param dimension_mappings: This is to allow mapping column(s) from the query result to the dimension in the destination table.
            :param measure_name_column: Name of the measure column. Also see ``MultiMeasureMappings`` and ``MixedMeasureMappings`` for how measure name properties on those relate to ``MeasureNameColumn`` .
            :param mixed_measure_mappings: Specifies how to map measures to multi-measure records.
            :param multi_measure_mappings: Multi-measure mappings.
            :param table_name: Name of Timestream table that the query result will be written to. The table should be within the same database that is provided in Timestream configuration.
            :param time_column: Column from query result that should be used as the time column in destination table. Column type for this should be TIMESTAMP.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-timestreamconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_timestream import mixins as timestream_mixins
                
                timestream_configuration_property = timestream_mixins.CfnScheduledQueryPropsMixin.TimestreamConfigurationProperty(
                    database_name="databaseName",
                    dimension_mappings=[timestream_mixins.CfnScheduledQueryPropsMixin.DimensionMappingProperty(
                        dimension_value_type="dimensionValueType",
                        name="name"
                    )],
                    measure_name_column="measureNameColumn",
                    mixed_measure_mappings=[timestream_mixins.CfnScheduledQueryPropsMixin.MixedMeasureMappingProperty(
                        measure_name="measureName",
                        measure_value_type="measureValueType",
                        multi_measure_attribute_mappings=[timestream_mixins.CfnScheduledQueryPropsMixin.MultiMeasureAttributeMappingProperty(
                            measure_value_type="measureValueType",
                            source_column="sourceColumn",
                            target_multi_measure_attribute_name="targetMultiMeasureAttributeName"
                        )],
                        source_column="sourceColumn",
                        target_measure_name="targetMeasureName"
                    )],
                    multi_measure_mappings=timestream_mixins.CfnScheduledQueryPropsMixin.MultiMeasureMappingsProperty(
                        multi_measure_attribute_mappings=[timestream_mixins.CfnScheduledQueryPropsMixin.MultiMeasureAttributeMappingProperty(
                            measure_value_type="measureValueType",
                            source_column="sourceColumn",
                            target_multi_measure_attribute_name="targetMultiMeasureAttributeName"
                        )],
                        target_multi_measure_name="targetMultiMeasureName"
                    ),
                    table_name="tableName",
                    time_column="timeColumn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5b85ee464e1c9ee26d4f120fe642c1d312bc95c8b9b25590cf6a6fb329cc9504)
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument dimension_mappings", value=dimension_mappings, expected_type=type_hints["dimension_mappings"])
                check_type(argname="argument measure_name_column", value=measure_name_column, expected_type=type_hints["measure_name_column"])
                check_type(argname="argument mixed_measure_mappings", value=mixed_measure_mappings, expected_type=type_hints["mixed_measure_mappings"])
                check_type(argname="argument multi_measure_mappings", value=multi_measure_mappings, expected_type=type_hints["multi_measure_mappings"])
                check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
                check_type(argname="argument time_column", value=time_column, expected_type=type_hints["time_column"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if database_name is not None:
                self._values["database_name"] = database_name
            if dimension_mappings is not None:
                self._values["dimension_mappings"] = dimension_mappings
            if measure_name_column is not None:
                self._values["measure_name_column"] = measure_name_column
            if mixed_measure_mappings is not None:
                self._values["mixed_measure_mappings"] = mixed_measure_mappings
            if multi_measure_mappings is not None:
                self._values["multi_measure_mappings"] = multi_measure_mappings
            if table_name is not None:
                self._values["table_name"] = table_name
            if time_column is not None:
                self._values["time_column"] = time_column

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            '''Name of Timestream database to which the query result will be written.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-timestreamconfiguration.html#cfn-timestream-scheduledquery-timestreamconfiguration-databasename
            '''
            result = self._values.get("database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def dimension_mappings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScheduledQueryPropsMixin.DimensionMappingProperty"]]]]:
            '''This is to allow mapping column(s) from the query result to the dimension in the destination table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-timestreamconfiguration.html#cfn-timestream-scheduledquery-timestreamconfiguration-dimensionmappings
            '''
            result = self._values.get("dimension_mappings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScheduledQueryPropsMixin.DimensionMappingProperty"]]]], result)

        @builtins.property
        def measure_name_column(self) -> typing.Optional[builtins.str]:
            '''Name of the measure column.

            Also see ``MultiMeasureMappings`` and ``MixedMeasureMappings`` for how measure name properties on those relate to ``MeasureNameColumn`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-timestreamconfiguration.html#cfn-timestream-scheduledquery-timestreamconfiguration-measurenamecolumn
            '''
            result = self._values.get("measure_name_column")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mixed_measure_mappings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScheduledQueryPropsMixin.MixedMeasureMappingProperty"]]]]:
            '''Specifies how to map measures to multi-measure records.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-timestreamconfiguration.html#cfn-timestream-scheduledquery-timestreamconfiguration-mixedmeasuremappings
            '''
            result = self._values.get("mixed_measure_mappings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScheduledQueryPropsMixin.MixedMeasureMappingProperty"]]]], result)

        @builtins.property
        def multi_measure_mappings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScheduledQueryPropsMixin.MultiMeasureMappingsProperty"]]:
            '''Multi-measure mappings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-timestreamconfiguration.html#cfn-timestream-scheduledquery-timestreamconfiguration-multimeasuremappings
            '''
            result = self._values.get("multi_measure_mappings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScheduledQueryPropsMixin.MultiMeasureMappingsProperty"]], result)

        @builtins.property
        def table_name(self) -> typing.Optional[builtins.str]:
            '''Name of Timestream table that the query result will be written to.

            The table should be within the same database that is provided in Timestream configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-timestreamconfiguration.html#cfn-timestream-scheduledquery-timestreamconfiguration-tablename
            '''
            result = self._values.get("table_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def time_column(self) -> typing.Optional[builtins.str]:
            '''Column from query result that should be used as the time column in destination table.

            Column type for this should be TIMESTAMP.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-timestreamconfiguration.html#cfn-timestream-scheduledquery-timestreamconfiguration-timecolumn
            '''
            result = self._values.get("time_column")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TimestreamConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_timestream.mixins.CfnTableMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "database_name": "databaseName",
        "magnetic_store_write_properties": "magneticStoreWriteProperties",
        "retention_properties": "retentionProperties",
        "schema": "schema",
        "table_name": "tableName",
        "tags": "tags",
    },
)
class CfnTableMixinProps:
    def __init__(
        self,
        *,
        database_name: typing.Optional[builtins.str] = None,
        magnetic_store_write_properties: typing.Any = None,
        retention_properties: typing.Any = None,
        schema: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.SchemaProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        table_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnTablePropsMixin.

        :param database_name: The name of the Timestream database that contains this table. *Length Constraints* : Minimum length of 3 bytes. Maximum length of 256 bytes.
        :param magnetic_store_write_properties: Contains properties to set on the table when enabling magnetic store writes. This object has the following attributes: - *EnableMagneticStoreWrites* : A ``boolean`` flag to enable magnetic store writes. - *MagneticStoreRejectedDataLocation* : The location to write error reports for records rejected, asynchronously, during magnetic store writes. Only ``S3Configuration`` objects are allowed. The ``S3Configuration`` object has the following attributes: - *BucketName* : The name of the S3 bucket. - *EncryptionOption* : The encryption option for the S3 location. Valid values are S3 server-side encryption with an S3 managed key ( ``SSE_S3`` ) or AWS managed key ( ``SSE_KMS`` ). - *KmsKeyId* : The AWS KMS key ID to use when encrypting with an AWS managed key. - *ObjectKeyPrefix* : The prefix to use option for the objects stored in S3. Both ``BucketName`` and ``EncryptionOption`` are *required* when ``S3Configuration`` is specified. If you specify ``SSE_KMS`` as your ``EncryptionOption`` then ``KmsKeyId`` is *required* . ``EnableMagneticStoreWrites`` attribute is *required* when ``MagneticStoreWriteProperties`` is specified. ``MagneticStoreRejectedDataLocation`` attribute is *required* when ``EnableMagneticStoreWrites`` is set to ``true`` . See the following examples: *JSON:: { "Type" : AWS::Timestream::Table", "Properties":{ "DatabaseName":"TestDatabase", "TableName":"TestTable", "MagneticStoreWriteProperties":{ "EnableMagneticStoreWrites":true, "MagneticStoreRejectedDataLocation":{ "S3Configuration":{ "BucketName":" amzn-s3-demo-bucket ", "EncryptionOption":"SSE_KMS", "KmsKeyId":"1234abcd-12ab-34cd-56ef-1234567890ab", "ObjectKeyPrefix":"prefix" } } } } } *YAML:: Type: AWS::Timestream::Table DependsOn: TestDatabase Properties: TableName: "TestTable" DatabaseName: "TestDatabase" MagneticStoreWriteProperties: EnableMagneticStoreWrites: true MagneticStoreRejectedDataLocation: S3Configuration: BucketName: " amzn-s3-demo-bucket " EncryptionOption: "SSE_KMS" KmsKeyId: "1234abcd-12ab-34cd-56ef-1234567890ab" ObjectKeyPrefix: "prefix"
        :param retention_properties: The retention duration for the memory store and magnetic store. This object has the following attributes:. - *MemoryStoreRetentionPeriodInHours* : Retention duration for memory store, in hours. - *MagneticStoreRetentionPeriodInDays* : Retention duration for magnetic store, in days. Both attributes are of type ``string`` . Both attributes are *required* when ``RetentionProperties`` is specified. See the following examples: *JSON* ``{ "Type" : AWS::Timestream::Table", "Properties" : { "DatabaseName" : "TestDatabase", "TableName" : "TestTable", "RetentionProperties" : { "MemoryStoreRetentionPeriodInHours": "24", "MagneticStoreRetentionPeriodInDays": "7" } } }`` *YAML:: Type: AWS::Timestream::Table DependsOn: TestDatabase Properties: TableName: "TestTable" DatabaseName: "TestDatabase" RetentionProperties: MemoryStoreRetentionPeriodInHours: "24" MagneticStoreRetentionPeriodInDays: "7"
        :param schema: The schema of the table.
        :param table_name: The name of the Timestream table. *Length Constraints* : Minimum length of 3 bytes. Maximum length of 256 bytes.
        :param tags: The tags to add to the table.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-table.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_timestream import mixins as timestream_mixins
            
            # magnetic_store_write_properties: Any
            # retention_properties: Any
            
            cfn_table_mixin_props = timestream_mixins.CfnTableMixinProps(
                database_name="databaseName",
                magnetic_store_write_properties=magnetic_store_write_properties,
                retention_properties=retention_properties,
                schema=timestream_mixins.CfnTablePropsMixin.SchemaProperty(
                    composite_partition_key=[timestream_mixins.CfnTablePropsMixin.PartitionKeyProperty(
                        enforcement_in_record="enforcementInRecord",
                        name="name",
                        type="type"
                    )]
                ),
                table_name="tableName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7510f1869d2ccdf443e8ee9a7405717aeb11315c2f8d14fb73d25ae27e0a4f5a)
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument magnetic_store_write_properties", value=magnetic_store_write_properties, expected_type=type_hints["magnetic_store_write_properties"])
            check_type(argname="argument retention_properties", value=retention_properties, expected_type=type_hints["retention_properties"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if database_name is not None:
            self._values["database_name"] = database_name
        if magnetic_store_write_properties is not None:
            self._values["magnetic_store_write_properties"] = magnetic_store_write_properties
        if retention_properties is not None:
            self._values["retention_properties"] = retention_properties
        if schema is not None:
            self._values["schema"] = schema
        if table_name is not None:
            self._values["table_name"] = table_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def database_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Timestream database that contains this table.

        *Length Constraints* : Minimum length of 3 bytes. Maximum length of 256 bytes.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-table.html#cfn-timestream-table-databasename
        '''
        result = self._values.get("database_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def magnetic_store_write_properties(self) -> typing.Any:
        '''Contains properties to set on the table when enabling magnetic store writes.

        This object has the following attributes:

        - *EnableMagneticStoreWrites* : A ``boolean`` flag to enable magnetic store writes.
        - *MagneticStoreRejectedDataLocation* : The location to write error reports for records rejected, asynchronously, during magnetic store writes. Only ``S3Configuration`` objects are allowed. The ``S3Configuration`` object has the following attributes:
        - *BucketName* : The name of the S3 bucket.
        - *EncryptionOption* : The encryption option for the S3 location. Valid values are S3 server-side encryption with an S3 managed key ( ``SSE_S3`` ) or AWS managed key ( ``SSE_KMS`` ).
        - *KmsKeyId* : The AWS KMS key ID to use when encrypting with an AWS managed key.
        - *ObjectKeyPrefix* : The prefix to use option for the objects stored in S3.

        Both ``BucketName`` and ``EncryptionOption`` are *required* when ``S3Configuration`` is specified. If you specify ``SSE_KMS`` as your ``EncryptionOption`` then ``KmsKeyId`` is *required* .

        ``EnableMagneticStoreWrites`` attribute is *required* when ``MagneticStoreWriteProperties`` is specified. ``MagneticStoreRejectedDataLocation`` attribute is *required* when ``EnableMagneticStoreWrites`` is set to ``true`` .

        See the following examples:

        *JSON::

           { "Type" : AWS::Timestream::Table", "Properties":{ "DatabaseName":"TestDatabase", "TableName":"TestTable", "MagneticStoreWriteProperties":{ "EnableMagneticStoreWrites":true, "MagneticStoreRejectedDataLocation":{ "S3Configuration":{ "BucketName":" amzn-s3-demo-bucket ", "EncryptionOption":"SSE_KMS", "KmsKeyId":"1234abcd-12ab-34cd-56ef-1234567890ab", "ObjectKeyPrefix":"prefix" } } } }
           }

        *YAML::

           Type: AWS::Timestream::Table
           DependsOn: TestDatabase
           Properties: TableName: "TestTable" DatabaseName: "TestDatabase" MagneticStoreWriteProperties: EnableMagneticStoreWrites: true MagneticStoreRejectedDataLocation: S3Configuration: BucketName: " amzn-s3-demo-bucket " EncryptionOption: "SSE_KMS" KmsKeyId: "1234abcd-12ab-34cd-56ef-1234567890ab" ObjectKeyPrefix: "prefix"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-table.html#cfn-timestream-table-magneticstorewriteproperties
        '''
        result = self._values.get("magnetic_store_write_properties")
        return typing.cast(typing.Any, result)

    @builtins.property
    def retention_properties(self) -> typing.Any:
        '''The retention duration for the memory store and magnetic store. This object has the following attributes:.

        - *MemoryStoreRetentionPeriodInHours* : Retention duration for memory store, in hours.
        - *MagneticStoreRetentionPeriodInDays* : Retention duration for magnetic store, in days.

        Both attributes are of type ``string`` . Both attributes are *required* when ``RetentionProperties`` is specified.

        See the following examples:

        *JSON*

        ``{ "Type" : AWS::Timestream::Table", "Properties" : { "DatabaseName" : "TestDatabase", "TableName" : "TestTable", "RetentionProperties" : { "MemoryStoreRetentionPeriodInHours": "24", "MagneticStoreRetentionPeriodInDays": "7" } } }``

        *YAML::

           Type: AWS::Timestream::Table
           DependsOn: TestDatabase
           Properties: TableName: "TestTable" DatabaseName: "TestDatabase" RetentionProperties: MemoryStoreRetentionPeriodInHours: "24" MagneticStoreRetentionPeriodInDays: "7"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-table.html#cfn-timestream-table-retentionproperties
        '''
        result = self._values.get("retention_properties")
        return typing.cast(typing.Any, result)

    @builtins.property
    def schema(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.SchemaProperty"]]:
        '''The schema of the table.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-table.html#cfn-timestream-table-schema
        '''
        result = self._values.get("schema")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.SchemaProperty"]], result)

    @builtins.property
    def table_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Timestream table.

        *Length Constraints* : Minimum length of 3 bytes. Maximum length of 256 bytes.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-table.html#cfn-timestream-table-tablename
        '''
        result = self._values.get("table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags to add to the table.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-table.html#cfn-timestream-table-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTableMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnTablePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_timestream.mixins.CfnTablePropsMixin",
):
    '''The CreateTable operation adds a new table to an existing database in your account.

    In an AWS account, table names must be at least unique within each Region if they are in the same database. You may have identical table names in the same Region if the tables are in separate databases. While creating the table, you must specify the table name, database name, and the retention properties. `Service quotas apply <https://docs.aws.amazon.com/timestream/latest/developerguide/ts-limits.html>`_ . See `code sample <https://docs.aws.amazon.com/timestream/latest/developerguide/code-samples.create-table.html>`_ for details.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-table.html
    :cloudformationResource: AWS::Timestream::Table
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_timestream import mixins as timestream_mixins
        
        # magnetic_store_write_properties: Any
        # retention_properties: Any
        
        cfn_table_props_mixin = timestream_mixins.CfnTablePropsMixin(timestream_mixins.CfnTableMixinProps(
            database_name="databaseName",
            magnetic_store_write_properties=magnetic_store_write_properties,
            retention_properties=retention_properties,
            schema=timestream_mixins.CfnTablePropsMixin.SchemaProperty(
                composite_partition_key=[timestream_mixins.CfnTablePropsMixin.PartitionKeyProperty(
                    enforcement_in_record="enforcementInRecord",
                    name="name",
                    type="type"
                )]
            ),
            table_name="tableName",
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
        props: typing.Union[CfnTableMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Timestream::Table``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a52c01e7c9966d494ec1fb76cef8510811158eab8664cb08c3265e75af0d8ca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__54ee50c2523e708ded600b531de362efaba5866ee21d06eae8300afc40121d93)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a740111a931635c7631a0acb1308ca8847e7a756afd0b50159ed904540737f74)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTableMixinProps:
        return typing.cast(CfnTableMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_timestream.mixins.CfnTablePropsMixin.MagneticStoreRejectedDataLocationProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_configuration": "s3Configuration"},
    )
    class MagneticStoreRejectedDataLocationProperty:
        def __init__(
            self,
            *,
            s3_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.S3ConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The location to write error reports for records rejected, asynchronously, during magnetic store writes.

            :param s3_configuration: Configuration of an S3 location to write error reports for records rejected, asynchronously, during magnetic store writes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-table-magneticstorerejecteddatalocation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_timestream import mixins as timestream_mixins
                
                magnetic_store_rejected_data_location_property = timestream_mixins.CfnTablePropsMixin.MagneticStoreRejectedDataLocationProperty(
                    s3_configuration=timestream_mixins.CfnTablePropsMixin.S3ConfigurationProperty(
                        bucket_name="bucketName",
                        encryption_option="encryptionOption",
                        kms_key_id="kmsKeyId",
                        object_key_prefix="objectKeyPrefix"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ece3d791085385420eea88391e3dcece3d03bf4fbcd9a710a563388a52be3711)
                check_type(argname="argument s3_configuration", value=s3_configuration, expected_type=type_hints["s3_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3_configuration is not None:
                self._values["s3_configuration"] = s3_configuration

        @builtins.property
        def s3_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.S3ConfigurationProperty"]]:
            '''Configuration of an S3 location to write error reports for records rejected, asynchronously, during magnetic store writes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-table-magneticstorerejecteddatalocation.html#cfn-timestream-table-magneticstorerejecteddatalocation-s3configuration
            '''
            result = self._values.get("s3_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.S3ConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MagneticStoreRejectedDataLocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_timestream.mixins.CfnTablePropsMixin.MagneticStoreWritePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enable_magnetic_store_writes": "enableMagneticStoreWrites",
            "magnetic_store_rejected_data_location": "magneticStoreRejectedDataLocation",
        },
    )
    class MagneticStoreWritePropertiesProperty:
        def __init__(
            self,
            *,
            enable_magnetic_store_writes: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            magnetic_store_rejected_data_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.MagneticStoreRejectedDataLocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The set of properties on a table for configuring magnetic store writes.

            :param enable_magnetic_store_writes: A flag to enable magnetic store writes.
            :param magnetic_store_rejected_data_location: The location to write error reports for records rejected asynchronously during magnetic store writes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-table-magneticstorewriteproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_timestream import mixins as timestream_mixins
                
                magnetic_store_write_properties_property = timestream_mixins.CfnTablePropsMixin.MagneticStoreWritePropertiesProperty(
                    enable_magnetic_store_writes=False,
                    magnetic_store_rejected_data_location=timestream_mixins.CfnTablePropsMixin.MagneticStoreRejectedDataLocationProperty(
                        s3_configuration=timestream_mixins.CfnTablePropsMixin.S3ConfigurationProperty(
                            bucket_name="bucketName",
                            encryption_option="encryptionOption",
                            kms_key_id="kmsKeyId",
                            object_key_prefix="objectKeyPrefix"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__917f0bc7072fba003849c6326766b3cc507eb5afe2b17ba29ec5afb53c234873)
                check_type(argname="argument enable_magnetic_store_writes", value=enable_magnetic_store_writes, expected_type=type_hints["enable_magnetic_store_writes"])
                check_type(argname="argument magnetic_store_rejected_data_location", value=magnetic_store_rejected_data_location, expected_type=type_hints["magnetic_store_rejected_data_location"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enable_magnetic_store_writes is not None:
                self._values["enable_magnetic_store_writes"] = enable_magnetic_store_writes
            if magnetic_store_rejected_data_location is not None:
                self._values["magnetic_store_rejected_data_location"] = magnetic_store_rejected_data_location

        @builtins.property
        def enable_magnetic_store_writes(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A flag to enable magnetic store writes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-table-magneticstorewriteproperties.html#cfn-timestream-table-magneticstorewriteproperties-enablemagneticstorewrites
            '''
            result = self._values.get("enable_magnetic_store_writes")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def magnetic_store_rejected_data_location(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.MagneticStoreRejectedDataLocationProperty"]]:
            '''The location to write error reports for records rejected asynchronously during magnetic store writes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-table-magneticstorewriteproperties.html#cfn-timestream-table-magneticstorewriteproperties-magneticstorerejecteddatalocation
            '''
            result = self._values.get("magnetic_store_rejected_data_location")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.MagneticStoreRejectedDataLocationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MagneticStoreWritePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_timestream.mixins.CfnTablePropsMixin.PartitionKeyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enforcement_in_record": "enforcementInRecord",
            "name": "name",
            "type": "type",
        },
    )
    class PartitionKeyProperty:
        def __init__(
            self,
            *,
            enforcement_in_record: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An attribute used in partitioning data in a table.

            A dimension key partitions data using the values of the dimension specified by the dimension-name as partition key, while a measure key partitions data using measure names (values of the 'measure_name' column).

            :param enforcement_in_record: The level of enforcement for the specification of a dimension key in ingested records. Options are REQUIRED (dimension key must be specified) and OPTIONAL (dimension key does not have to be specified).
            :param name: The name of the attribute used for a dimension key.
            :param type: The type of the partition key. Options are DIMENSION (dimension key) and MEASURE (measure key).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-table-partitionkey.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_timestream import mixins as timestream_mixins
                
                partition_key_property = timestream_mixins.CfnTablePropsMixin.PartitionKeyProperty(
                    enforcement_in_record="enforcementInRecord",
                    name="name",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f7e054ad2ca10baf1629d415fb3a2f6f64d8ccbb75fcacbc8a97e68cd0123859)
                check_type(argname="argument enforcement_in_record", value=enforcement_in_record, expected_type=type_hints["enforcement_in_record"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enforcement_in_record is not None:
                self._values["enforcement_in_record"] = enforcement_in_record
            if name is not None:
                self._values["name"] = name
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def enforcement_in_record(self) -> typing.Optional[builtins.str]:
            '''The level of enforcement for the specification of a dimension key in ingested records.

            Options are REQUIRED (dimension key must be specified) and OPTIONAL (dimension key does not have to be specified).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-table-partitionkey.html#cfn-timestream-table-partitionkey-enforcementinrecord
            '''
            result = self._values.get("enforcement_in_record")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the attribute used for a dimension key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-table-partitionkey.html#cfn-timestream-table-partitionkey-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of the partition key.

            Options are DIMENSION (dimension key) and MEASURE (measure key).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-table-partitionkey.html#cfn-timestream-table-partitionkey-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PartitionKeyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_timestream.mixins.CfnTablePropsMixin.RetentionPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "magnetic_store_retention_period_in_days": "magneticStoreRetentionPeriodInDays",
            "memory_store_retention_period_in_hours": "memoryStoreRetentionPeriodInHours",
        },
    )
    class RetentionPropertiesProperty:
        def __init__(
            self,
            *,
            magnetic_store_retention_period_in_days: typing.Optional[builtins.str] = None,
            memory_store_retention_period_in_hours: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Retention properties contain the duration for which your time-series data must be stored in the magnetic store and the memory store.

            :param magnetic_store_retention_period_in_days: The duration for which data must be stored in the magnetic store.
            :param memory_store_retention_period_in_hours: The duration for which data must be stored in the memory store.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-table-retentionproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_timestream import mixins as timestream_mixins
                
                retention_properties_property = timestream_mixins.CfnTablePropsMixin.RetentionPropertiesProperty(
                    magnetic_store_retention_period_in_days="magneticStoreRetentionPeriodInDays",
                    memory_store_retention_period_in_hours="memoryStoreRetentionPeriodInHours"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__962f864ef98a1899ac8ce278dc73f6965002cc7412a7d5b427a4d2349f63aceb)
                check_type(argname="argument magnetic_store_retention_period_in_days", value=magnetic_store_retention_period_in_days, expected_type=type_hints["magnetic_store_retention_period_in_days"])
                check_type(argname="argument memory_store_retention_period_in_hours", value=memory_store_retention_period_in_hours, expected_type=type_hints["memory_store_retention_period_in_hours"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if magnetic_store_retention_period_in_days is not None:
                self._values["magnetic_store_retention_period_in_days"] = magnetic_store_retention_period_in_days
            if memory_store_retention_period_in_hours is not None:
                self._values["memory_store_retention_period_in_hours"] = memory_store_retention_period_in_hours

        @builtins.property
        def magnetic_store_retention_period_in_days(
            self,
        ) -> typing.Optional[builtins.str]:
            '''The duration for which data must be stored in the magnetic store.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-table-retentionproperties.html#cfn-timestream-table-retentionproperties-magneticstoreretentionperiodindays
            '''
            result = self._values.get("magnetic_store_retention_period_in_days")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def memory_store_retention_period_in_hours(
            self,
        ) -> typing.Optional[builtins.str]:
            '''The duration for which data must be stored in the memory store.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-table-retentionproperties.html#cfn-timestream-table-retentionproperties-memorystoreretentionperiodinhours
            '''
            result = self._values.get("memory_store_retention_period_in_hours")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RetentionPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_timestream.mixins.CfnTablePropsMixin.S3ConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_name": "bucketName",
            "encryption_option": "encryptionOption",
            "kms_key_id": "kmsKeyId",
            "object_key_prefix": "objectKeyPrefix",
        },
    )
    class S3ConfigurationProperty:
        def __init__(
            self,
            *,
            bucket_name: typing.Optional[builtins.str] = None,
            encryption_option: typing.Optional[builtins.str] = None,
            kms_key_id: typing.Optional[builtins.str] = None,
            object_key_prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration that specifies an S3 location.

            :param bucket_name: The bucket name of the customer S3 bucket.
            :param encryption_option: The encryption option for the customer S3 location. Options are S3 server-side encryption with an S3 managed key or AWS managed key.
            :param kms_key_id: The AWS key ID for the customer S3 location when encrypting with an AWS managed key.
            :param object_key_prefix: The object key preview for the customer S3 location.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-table-s3configuration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_timestream import mixins as timestream_mixins
                
                s3_configuration_property = timestream_mixins.CfnTablePropsMixin.S3ConfigurationProperty(
                    bucket_name="bucketName",
                    encryption_option="encryptionOption",
                    kms_key_id="kmsKeyId",
                    object_key_prefix="objectKeyPrefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__33bc1c6c047e0abf7346aa0566ff1969c268ccacbd398e5b8b94b385043d79fc)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument encryption_option", value=encryption_option, expected_type=type_hints["encryption_option"])
                check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
                check_type(argname="argument object_key_prefix", value=object_key_prefix, expected_type=type_hints["object_key_prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_name is not None:
                self._values["bucket_name"] = bucket_name
            if encryption_option is not None:
                self._values["encryption_option"] = encryption_option
            if kms_key_id is not None:
                self._values["kms_key_id"] = kms_key_id
            if object_key_prefix is not None:
                self._values["object_key_prefix"] = object_key_prefix

        @builtins.property
        def bucket_name(self) -> typing.Optional[builtins.str]:
            '''The bucket name of the customer S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-table-s3configuration.html#cfn-timestream-table-s3configuration-bucketname
            '''
            result = self._values.get("bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def encryption_option(self) -> typing.Optional[builtins.str]:
            '''The encryption option for the customer S3 location.

            Options are S3 server-side encryption with an S3 managed key or AWS managed key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-table-s3configuration.html#cfn-timestream-table-s3configuration-encryptionoption
            '''
            result = self._values.get("encryption_option")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def kms_key_id(self) -> typing.Optional[builtins.str]:
            '''The AWS  key ID for the customer S3 location when encrypting with an AWS managed key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-table-s3configuration.html#cfn-timestream-table-s3configuration-kmskeyid
            '''
            result = self._values.get("kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def object_key_prefix(self) -> typing.Optional[builtins.str]:
            '''The object key preview for the customer S3 location.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-table-s3configuration.html#cfn-timestream-table-s3configuration-objectkeyprefix
            '''
            result = self._values.get("object_key_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3ConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_timestream.mixins.CfnTablePropsMixin.SchemaProperty",
        jsii_struct_bases=[],
        name_mapping={"composite_partition_key": "compositePartitionKey"},
    )
    class SchemaProperty:
        def __init__(
            self,
            *,
            composite_partition_key: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.PartitionKeyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''A Schema specifies the expected data model of the table.

            :param composite_partition_key: A non-empty list of partition keys defining the attributes used to partition the table data. The order of the list determines the partition hierarchy. The name and type of each partition key as well as the partition key order cannot be changed after the table is created. However, the enforcement level of each partition key can be changed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-table-schema.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_timestream import mixins as timestream_mixins
                
                schema_property = timestream_mixins.CfnTablePropsMixin.SchemaProperty(
                    composite_partition_key=[timestream_mixins.CfnTablePropsMixin.PartitionKeyProperty(
                        enforcement_in_record="enforcementInRecord",
                        name="name",
                        type="type"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__518ac82354748ddff3d7340c953afca32d998340808c9688e4944465aa074e0b)
                check_type(argname="argument composite_partition_key", value=composite_partition_key, expected_type=type_hints["composite_partition_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if composite_partition_key is not None:
                self._values["composite_partition_key"] = composite_partition_key

        @builtins.property
        def composite_partition_key(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.PartitionKeyProperty"]]]]:
            '''A non-empty list of partition keys defining the attributes used to partition the table data.

            The order of the list determines the partition hierarchy. The name and type of each partition key as well as the partition key order cannot be changed after the table is created. However, the enforcement level of each partition key can be changed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-table-schema.html#cfn-timestream-table-schema-compositepartitionkey
            '''
            result = self._values.get("composite_partition_key")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.PartitionKeyProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SchemaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnDatabaseMixinProps",
    "CfnDatabasePropsMixin",
    "CfnInfluxDBInstanceMixinProps",
    "CfnInfluxDBInstancePropsMixin",
    "CfnScheduledQueryMixinProps",
    "CfnScheduledQueryPropsMixin",
    "CfnTableMixinProps",
    "CfnTablePropsMixin",
]

publication.publish()

def _typecheckingstub__b1e9846d2f16cc8dce581e7f97542c56eed18d1b54b5f31c90fca23a20198515(
    *,
    database_name: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6452e68c861457e83198f369445a760611e35b723aca7ef25f9035c8deca2c8(
    props: typing.Union[CfnDatabaseMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de2c902b01e428376ef84f7406836d4c0486da6872af53e6673bc7eb5f664601(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8bfb650f52755e250c0bda0bbd74a3a995b5491a12ccc31f23342b9a053a8b9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7c20324dcab11aed90e73132d2d2d67817629388742b7bb4bc1695bff32f467(
    *,
    allocated_storage: typing.Optional[jsii.Number] = None,
    bucket: typing.Optional[builtins.str] = None,
    db_instance_type: typing.Optional[builtins.str] = None,
    db_parameter_group_identifier: typing.Optional[builtins.str] = None,
    db_storage_type: typing.Optional[builtins.str] = None,
    deployment_type: typing.Optional[builtins.str] = None,
    log_delivery_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInfluxDBInstancePropsMixin.LogDeliveryConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    network_type: typing.Optional[builtins.str] = None,
    organization: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    publicly_accessible: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    username: typing.Optional[builtins.str] = None,
    vpc_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc_subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcccec0d5b15c9785d2a950e7005cc1bf9e91a10852c5c965f6b697163abfb4b(
    props: typing.Union[CfnInfluxDBInstanceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d80ce4ff7bee3dee043ec8dd347b83c275ffb8f181d82dd5a6e093e03cf8d41(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60da0a513573533398fd2c2aef91402674fe1d19d84584bb0884df23cde39a70(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aa13ba0b579a4b2225be37b9123170bea434ff47911481d8edc64b8b0d0b358(
    *,
    s3_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInfluxDBInstancePropsMixin.S3ConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd4786b9a5d59b59ab7bbaae6ae745ed7a7ef2576e5b33d22bc424985a15bfdb(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4babe77ab1b35efb3124eba9bff6d0d2adbfa346b9ca667c619b7658b2097af(
    *,
    client_token: typing.Optional[builtins.str] = None,
    error_report_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScheduledQueryPropsMixin.ErrorReportConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    notification_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScheduledQueryPropsMixin.NotificationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    query_string: typing.Optional[builtins.str] = None,
    schedule_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScheduledQueryPropsMixin.ScheduleConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    scheduled_query_execution_role_arn: typing.Optional[builtins.str] = None,
    scheduled_query_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScheduledQueryPropsMixin.TargetConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4e8543e82a440b3ba9607bb1abbf1dbbfde2554a5f08e60923a20518a95c74a(
    props: typing.Union[CfnScheduledQueryMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cca2b47866664dbe1859392fefa064718351f3acb690c6e6e54ccb47227460c0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bbe644cb9f7be5265f4b6f4024be89fae7cc5bb59b9751de0135e748a052fb2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e83e5459a50bd38cdb34166b5b2fdac660a84024ffa7bb4afeca0febfb7e32a2(
    *,
    dimension_value_type: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__504800b998db83569e18d8c1a90089505b18052d62954488dad69d66f2cdf583(
    *,
    s3_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScheduledQueryPropsMixin.S3ConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0a98b35cdf5e53f5c9bba7b6db900ed30206ef9ee94380bbdd8598d068a2d0c(
    *,
    measure_name: typing.Optional[builtins.str] = None,
    measure_value_type: typing.Optional[builtins.str] = None,
    multi_measure_attribute_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScheduledQueryPropsMixin.MultiMeasureAttributeMappingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    source_column: typing.Optional[builtins.str] = None,
    target_measure_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5019f5c4e75d9dd91b50b9ebb68612fb27e61f82145f72ccb6838cbe96ef0649(
    *,
    measure_value_type: typing.Optional[builtins.str] = None,
    source_column: typing.Optional[builtins.str] = None,
    target_multi_measure_attribute_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5244fe6fc4a3eade1a814b9f3a46620c570a9ae6195516774c3e5852f5f143be(
    *,
    multi_measure_attribute_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScheduledQueryPropsMixin.MultiMeasureAttributeMappingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    target_multi_measure_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c52fc1af9f4f46b365fd7f37bb73ae788ec4861b881f8fd7bbb0e9d96774e35a(
    *,
    sns_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScheduledQueryPropsMixin.SnsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b857960eafe1612c06bf9b365c54d7260e454926930108ed46528f9d33ec7e12(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    encryption_option: typing.Optional[builtins.str] = None,
    object_key_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fccfe5fcb114b391a10bdfc7519bc97b4d96e1ba00090bf9f565ec8cad3b4272(
    *,
    schedule_expression: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db6fb6a60b3bb34786f09b81775ae95831610938ea2871d0fafb33d09c07798e(
    *,
    topic_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__218abc17ad74adc0e33da7e1df2b66e0c9de6a8462a236fb5f3a54c8e14a7d25(
    *,
    timestream_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScheduledQueryPropsMixin.TimestreamConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b85ee464e1c9ee26d4f120fe642c1d312bc95c8b9b25590cf6a6fb329cc9504(
    *,
    database_name: typing.Optional[builtins.str] = None,
    dimension_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScheduledQueryPropsMixin.DimensionMappingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    measure_name_column: typing.Optional[builtins.str] = None,
    mixed_measure_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScheduledQueryPropsMixin.MixedMeasureMappingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    multi_measure_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScheduledQueryPropsMixin.MultiMeasureMappingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    table_name: typing.Optional[builtins.str] = None,
    time_column: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7510f1869d2ccdf443e8ee9a7405717aeb11315c2f8d14fb73d25ae27e0a4f5a(
    *,
    database_name: typing.Optional[builtins.str] = None,
    magnetic_store_write_properties: typing.Any = None,
    retention_properties: typing.Any = None,
    schema: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.SchemaProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    table_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a52c01e7c9966d494ec1fb76cef8510811158eab8664cb08c3265e75af0d8ca(
    props: typing.Union[CfnTableMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54ee50c2523e708ded600b531de362efaba5866ee21d06eae8300afc40121d93(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a740111a931635c7631a0acb1308ca8847e7a756afd0b50159ed904540737f74(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ece3d791085385420eea88391e3dcece3d03bf4fbcd9a710a563388a52be3711(
    *,
    s3_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.S3ConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__917f0bc7072fba003849c6326766b3cc507eb5afe2b17ba29ec5afb53c234873(
    *,
    enable_magnetic_store_writes: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    magnetic_store_rejected_data_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.MagneticStoreRejectedDataLocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7e054ad2ca10baf1629d415fb3a2f6f64d8ccbb75fcacbc8a97e68cd0123859(
    *,
    enforcement_in_record: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__962f864ef98a1899ac8ce278dc73f6965002cc7412a7d5b427a4d2349f63aceb(
    *,
    magnetic_store_retention_period_in_days: typing.Optional[builtins.str] = None,
    memory_store_retention_period_in_hours: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33bc1c6c047e0abf7346aa0566ff1969c268ccacbd398e5b8b94b385043d79fc(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    encryption_option: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    object_key_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__518ac82354748ddff3d7340c953afca32d998340808c9688e4944465aa074e0b(
    *,
    composite_partition_key: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.PartitionKeyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
