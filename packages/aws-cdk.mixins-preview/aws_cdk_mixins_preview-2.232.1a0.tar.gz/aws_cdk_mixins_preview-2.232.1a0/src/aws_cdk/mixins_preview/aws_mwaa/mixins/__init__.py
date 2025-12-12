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
    jsii_type="@aws-cdk/mixins-preview.aws_mwaa.mixins.CfnEnvironmentMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "airflow_configuration_options": "airflowConfigurationOptions",
        "airflow_version": "airflowVersion",
        "dag_s3_path": "dagS3Path",
        "endpoint_management": "endpointManagement",
        "environment_class": "environmentClass",
        "execution_role_arn": "executionRoleArn",
        "kms_key": "kmsKey",
        "logging_configuration": "loggingConfiguration",
        "max_webservers": "maxWebservers",
        "max_workers": "maxWorkers",
        "min_webservers": "minWebservers",
        "min_workers": "minWorkers",
        "name": "name",
        "network_configuration": "networkConfiguration",
        "plugins_s3_object_version": "pluginsS3ObjectVersion",
        "plugins_s3_path": "pluginsS3Path",
        "requirements_s3_object_version": "requirementsS3ObjectVersion",
        "requirements_s3_path": "requirementsS3Path",
        "schedulers": "schedulers",
        "source_bucket_arn": "sourceBucketArn",
        "startup_script_s3_object_version": "startupScriptS3ObjectVersion",
        "startup_script_s3_path": "startupScriptS3Path",
        "tags": "tags",
        "webserver_access_mode": "webserverAccessMode",
        "weekly_maintenance_window_start": "weeklyMaintenanceWindowStart",
        "worker_replacement_strategy": "workerReplacementStrategy",
    },
)
class CfnEnvironmentMixinProps:
    def __init__(
        self,
        *,
        airflow_configuration_options: typing.Any = None,
        airflow_version: typing.Optional[builtins.str] = None,
        dag_s3_path: typing.Optional[builtins.str] = None,
        endpoint_management: typing.Optional[builtins.str] = None,
        environment_class: typing.Optional[builtins.str] = None,
        execution_role_arn: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[builtins.str] = None,
        logging_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEnvironmentPropsMixin.LoggingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        max_webservers: typing.Optional[jsii.Number] = None,
        max_workers: typing.Optional[jsii.Number] = None,
        min_webservers: typing.Optional[jsii.Number] = None,
        min_workers: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        network_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEnvironmentPropsMixin.NetworkConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        plugins_s3_object_version: typing.Optional[builtins.str] = None,
        plugins_s3_path: typing.Optional[builtins.str] = None,
        requirements_s3_object_version: typing.Optional[builtins.str] = None,
        requirements_s3_path: typing.Optional[builtins.str] = None,
        schedulers: typing.Optional[jsii.Number] = None,
        source_bucket_arn: typing.Optional[builtins.str] = None,
        startup_script_s3_object_version: typing.Optional[builtins.str] = None,
        startup_script_s3_path: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
        webserver_access_mode: typing.Optional[builtins.str] = None,
        weekly_maintenance_window_start: typing.Optional[builtins.str] = None,
        worker_replacement_strategy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnEnvironmentPropsMixin.

        :param airflow_configuration_options: A list of key-value pairs containing the Airflow configuration options for your environment. For example, ``core.default_timezone: utc`` . To learn more, see `Apache Airflow configuration options <https://docs.aws.amazon.com/mwaa/latest/userguide/configuring-env-variables.html>`_ .
        :param airflow_version: The version of Apache Airflow to use for the environment. If no value is specified, defaults to the latest version. If you specify a newer version number for an existing environment, the version update requires some service interruption before taking effect. *Allowed Values* : ``2.7.2`` | ``2.8.1`` | ``2.9.2`` | ``2.10.1`` | ``2.10.3`` | ``3.0.6`` (latest)
        :param dag_s3_path: The relative path to the DAGs folder on your Amazon S3 bucket. For example, ``dags`` . To learn more, see `Adding or updating DAGs <https://docs.aws.amazon.com/mwaa/latest/userguide/configuring-dag-folder.html>`_ .
        :param endpoint_management: Defines whether the VPC endpoints configured for the environment are created, and managed, by the customer or by Amazon MWAA. If set to ``SERVICE`` , Amazon MWAA will create and manage the required VPC endpoints in your VPC. If set to ``CUSTOMER`` , you must create, and manage, the VPC endpoints in your VPC.
        :param environment_class: The environment class type. Valid values: ``mw1.micro`` , ``mw1.small`` , ``mw1.medium`` , ``mw1.large`` , ``mw1.1large`` , and ``mw1.2large`` . To learn more, see `Amazon MWAA environment class <https://docs.aws.amazon.com/mwaa/latest/userguide/environment-class.html>`_ .
        :param execution_role_arn: The Amazon Resource Name (ARN) of the execution role in IAM that allows MWAA to access AWS resources in your environment. For example, ``arn:aws:iam::123456789:role/my-execution-role`` . To learn more, see `Amazon MWAA Execution role <https://docs.aws.amazon.com/mwaa/latest/userguide/mwaa-create-role.html>`_ .
        :param kms_key: The AWS Key Management Service (KMS) key to encrypt and decrypt the data in your environment. You can use an AWS KMS key managed by MWAA, or a customer-managed KMS key (advanced).
        :param logging_configuration: The Apache Airflow logs being sent to CloudWatch Logs: ``DagProcessingLogs`` , ``SchedulerLogs`` , ``TaskLogs`` , ``WebserverLogs`` , ``WorkerLogs`` .
        :param max_webservers: The maximum number of web servers that you want to run in your environment. Amazon MWAA scales the number of Apache Airflow web servers up to the number you specify for ``MaxWebservers`` when you interact with your Apache Airflow environment using Apache Airflow REST API, or the Apache Airflow CLI. For example, in scenarios where your workload requires network calls to the Apache Airflow REST API with a high transaction-per-second (TPS) rate, Amazon MWAA will increase the number of web servers up to the number set in ``MaxWebserers`` . As TPS rates decrease Amazon MWAA disposes of the additional web servers, and scales down to the number set in ``MinxWebserers`` . Valid values: For environments larger than mw1.micro, accepts values from ``2`` to ``5`` . Defaults to ``2`` for all environment sizes except mw1.micro, which defaults to ``1`` .
        :param max_workers: The maximum number of workers that you want to run in your environment. MWAA scales the number of Apache Airflow workers up to the number you specify in the ``MaxWorkers`` field. For example, ``20`` . When there are no more tasks running, and no more in the queue, MWAA disposes of the extra workers leaving the one worker that is included with your environment, or the number you specify in ``MinWorkers`` .
        :param min_webservers: The minimum number of web servers that you want to run in your environment. Amazon MWAA scales the number of Apache Airflow web servers up to the number you specify for ``MaxWebservers`` when you interact with your Apache Airflow environment using Apache Airflow REST API, or the Apache Airflow CLI. As the transaction-per-second rate, and the network load, decrease, Amazon MWAA disposes of the additional web servers, and scales down to the number set in ``MinxWebserers`` . Valid values: For environments larger than mw1.micro, accepts values from ``2`` to ``5`` . Defaults to ``2`` for all environment sizes except mw1.micro, which defaults to ``1`` .
        :param min_workers: The minimum number of workers that you want to run in your environment. MWAA scales the number of Apache Airflow workers up to the number you specify in the ``MaxWorkers`` field. When there are no more tasks running, and no more in the queue, MWAA disposes of the extra workers leaving the worker count you specify in the ``MinWorkers`` field. For example, ``2`` .
        :param name: The name of your Amazon MWAA environment.
        :param network_configuration: The VPC networking components used to secure and enable network traffic between the AWS resources for your environment. To learn more, see `About networking on Amazon MWAA <https://docs.aws.amazon.com/mwaa/latest/userguide/networking-about.html>`_ .
        :param plugins_s3_object_version: The version of the plugins.zip file on your Amazon S3 bucket. To learn more, see `Installing custom plugins <https://docs.aws.amazon.com/mwaa/latest/userguide/configuring-dag-import-plugins.html>`_ .
        :param plugins_s3_path: The relative path to the ``plugins.zip`` file on your Amazon S3 bucket. For example, ``plugins.zip`` . To learn more, see `Installing custom plugins <https://docs.aws.amazon.com/mwaa/latest/userguide/configuring-dag-import-plugins.html>`_ .
        :param requirements_s3_object_version: The version of the requirements.txt file on your Amazon S3 bucket. To learn more, see `Installing Python dependencies <https://docs.aws.amazon.com/mwaa/latest/userguide/working-dags-dependencies.html>`_ .
        :param requirements_s3_path: The relative path to the ``requirements.txt`` file on your Amazon S3 bucket. For example, ``requirements.txt`` . To learn more, see `Installing Python dependencies <https://docs.aws.amazon.com/mwaa/latest/userguide/working-dags-dependencies.html>`_ .
        :param schedulers: The number of schedulers that you want to run in your environment. Valid values:. - *v2* - For environments larger than mw1.micro, accepts values from 2 to 5. Defaults to 2 for all environment sizes except mw1.micro, which defaults to 1. - *v1* - Accepts 1.
        :param source_bucket_arn: The Amazon Resource Name (ARN) of the Amazon S3 bucket where your DAG code and supporting files are stored. For example, ``arn:aws:s3:::my-airflow-bucket-unique-name`` . To learn more, see `Create an Amazon S3 bucket for Amazon MWAA <https://docs.aws.amazon.com/mwaa/latest/userguide/mwaa-s3-bucket.html>`_ .
        :param startup_script_s3_object_version: The version of the startup shell script in your Amazon S3 bucket. You must specify the `version ID <https://docs.aws.amazon.com/AmazonS3/latest/userguide/versioning-workflows.html>`_ that Amazon S3 assigns to the file every time you update the script. Version IDs are Unicode, UTF-8 encoded, URL-ready, opaque strings that are no more than 1,024 bytes long. The following is an example: ``3sL4kqtJlcpXroDTDmJ+rmSpXd3dIbrHY+MTRCxf3vjVBH40Nr8X8gdRQBpUMLUo`` For more information, see `Using a startup script <https://docs.aws.amazon.com/mwaa/latest/userguide/using-startup-script.html>`_ .
        :param startup_script_s3_path: The relative path to the startup shell script in your Amazon S3 bucket. For example, ``s3://mwaa-environment/startup.sh`` . Amazon MWAA runs the script as your environment starts, and before running the Apache Airflow process. You can use this script to install dependencies, modify Apache Airflow configuration options, and set environment variables. For more information, see `Using a startup script <https://docs.aws.amazon.com/mwaa/latest/userguide/using-startup-script.html>`_ .
        :param tags: The key-value tag pairs associated to your environment. For example, ``"Environment": "Staging"`` . To learn more, see `Tagging <https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`_ . If you specify new tags for an existing environment, the update requires service interruption before taking effect.
        :param webserver_access_mode: The Apache Airflow *Web server* access mode. To learn more, see `Apache Airflow access modes <https://docs.aws.amazon.com/mwaa/latest/userguide/configuring-networking.html>`_ . Valid values: ``PRIVATE_ONLY`` or ``PUBLIC_ONLY`` .
        :param weekly_maintenance_window_start: The day and time of the week to start weekly maintenance updates of your environment in the following format: ``DAY:HH:MM`` . For example: ``TUE:03:30`` . You can specify a start time in 30 minute increments only. Supported input includes the following: - MON|TUE|WED|THU|FRI|SAT|SUN:([01]\\d|2[0-3]):(00|30)
        :param worker_replacement_strategy: The worker replacement strategy to use when updating the environment. Valid values: ``FORCED``, ``GRACEFUL``. FORCED means Apache Airflow workers will be stopped and replaced without waiting for tasks to complete before an update. GRACEFUL means Apache Airflow workers will be able to complete running tasks for up to 12 hours during an update before being stopped and replaced.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_mwaa import mixins as mwaa_mixins
            
            # airflow_configuration_options: Any
            # tags: Any
            
            cfn_environment_mixin_props = mwaa_mixins.CfnEnvironmentMixinProps(
                airflow_configuration_options=airflow_configuration_options,
                airflow_version="airflowVersion",
                dag_s3_path="dagS3Path",
                endpoint_management="endpointManagement",
                environment_class="environmentClass",
                execution_role_arn="executionRoleArn",
                kms_key="kmsKey",
                logging_configuration=mwaa_mixins.CfnEnvironmentPropsMixin.LoggingConfigurationProperty(
                    dag_processing_logs=mwaa_mixins.CfnEnvironmentPropsMixin.ModuleLoggingConfigurationProperty(
                        cloud_watch_log_group_arn="cloudWatchLogGroupArn",
                        enabled=False,
                        log_level="logLevel"
                    ),
                    scheduler_logs=mwaa_mixins.CfnEnvironmentPropsMixin.ModuleLoggingConfigurationProperty(
                        cloud_watch_log_group_arn="cloudWatchLogGroupArn",
                        enabled=False,
                        log_level="logLevel"
                    ),
                    task_logs=mwaa_mixins.CfnEnvironmentPropsMixin.ModuleLoggingConfigurationProperty(
                        cloud_watch_log_group_arn="cloudWatchLogGroupArn",
                        enabled=False,
                        log_level="logLevel"
                    ),
                    webserver_logs=mwaa_mixins.CfnEnvironmentPropsMixin.ModuleLoggingConfigurationProperty(
                        cloud_watch_log_group_arn="cloudWatchLogGroupArn",
                        enabled=False,
                        log_level="logLevel"
                    ),
                    worker_logs=mwaa_mixins.CfnEnvironmentPropsMixin.ModuleLoggingConfigurationProperty(
                        cloud_watch_log_group_arn="cloudWatchLogGroupArn",
                        enabled=False,
                        log_level="logLevel"
                    )
                ),
                max_webservers=123,
                max_workers=123,
                min_webservers=123,
                min_workers=123,
                name="name",
                network_configuration=mwaa_mixins.CfnEnvironmentPropsMixin.NetworkConfigurationProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                ),
                plugins_s3_object_version="pluginsS3ObjectVersion",
                plugins_s3_path="pluginsS3Path",
                requirements_s3_object_version="requirementsS3ObjectVersion",
                requirements_s3_path="requirementsS3Path",
                schedulers=123,
                source_bucket_arn="sourceBucketArn",
                startup_script_s3_object_version="startupScriptS3ObjectVersion",
                startup_script_s3_path="startupScriptS3Path",
                tags=tags,
                webserver_access_mode="webserverAccessMode",
                weekly_maintenance_window_start="weeklyMaintenanceWindowStart",
                worker_replacement_strategy="workerReplacementStrategy"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2079f9bcb3de1193b14b7dcb9de63c2adcf4e68fa55b12000c315e3b0a6b005c)
            check_type(argname="argument airflow_configuration_options", value=airflow_configuration_options, expected_type=type_hints["airflow_configuration_options"])
            check_type(argname="argument airflow_version", value=airflow_version, expected_type=type_hints["airflow_version"])
            check_type(argname="argument dag_s3_path", value=dag_s3_path, expected_type=type_hints["dag_s3_path"])
            check_type(argname="argument endpoint_management", value=endpoint_management, expected_type=type_hints["endpoint_management"])
            check_type(argname="argument environment_class", value=environment_class, expected_type=type_hints["environment_class"])
            check_type(argname="argument execution_role_arn", value=execution_role_arn, expected_type=type_hints["execution_role_arn"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument logging_configuration", value=logging_configuration, expected_type=type_hints["logging_configuration"])
            check_type(argname="argument max_webservers", value=max_webservers, expected_type=type_hints["max_webservers"])
            check_type(argname="argument max_workers", value=max_workers, expected_type=type_hints["max_workers"])
            check_type(argname="argument min_webservers", value=min_webservers, expected_type=type_hints["min_webservers"])
            check_type(argname="argument min_workers", value=min_workers, expected_type=type_hints["min_workers"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network_configuration", value=network_configuration, expected_type=type_hints["network_configuration"])
            check_type(argname="argument plugins_s3_object_version", value=plugins_s3_object_version, expected_type=type_hints["plugins_s3_object_version"])
            check_type(argname="argument plugins_s3_path", value=plugins_s3_path, expected_type=type_hints["plugins_s3_path"])
            check_type(argname="argument requirements_s3_object_version", value=requirements_s3_object_version, expected_type=type_hints["requirements_s3_object_version"])
            check_type(argname="argument requirements_s3_path", value=requirements_s3_path, expected_type=type_hints["requirements_s3_path"])
            check_type(argname="argument schedulers", value=schedulers, expected_type=type_hints["schedulers"])
            check_type(argname="argument source_bucket_arn", value=source_bucket_arn, expected_type=type_hints["source_bucket_arn"])
            check_type(argname="argument startup_script_s3_object_version", value=startup_script_s3_object_version, expected_type=type_hints["startup_script_s3_object_version"])
            check_type(argname="argument startup_script_s3_path", value=startup_script_s3_path, expected_type=type_hints["startup_script_s3_path"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument webserver_access_mode", value=webserver_access_mode, expected_type=type_hints["webserver_access_mode"])
            check_type(argname="argument weekly_maintenance_window_start", value=weekly_maintenance_window_start, expected_type=type_hints["weekly_maintenance_window_start"])
            check_type(argname="argument worker_replacement_strategy", value=worker_replacement_strategy, expected_type=type_hints["worker_replacement_strategy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if airflow_configuration_options is not None:
            self._values["airflow_configuration_options"] = airflow_configuration_options
        if airflow_version is not None:
            self._values["airflow_version"] = airflow_version
        if dag_s3_path is not None:
            self._values["dag_s3_path"] = dag_s3_path
        if endpoint_management is not None:
            self._values["endpoint_management"] = endpoint_management
        if environment_class is not None:
            self._values["environment_class"] = environment_class
        if execution_role_arn is not None:
            self._values["execution_role_arn"] = execution_role_arn
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if logging_configuration is not None:
            self._values["logging_configuration"] = logging_configuration
        if max_webservers is not None:
            self._values["max_webservers"] = max_webservers
        if max_workers is not None:
            self._values["max_workers"] = max_workers
        if min_webservers is not None:
            self._values["min_webservers"] = min_webservers
        if min_workers is not None:
            self._values["min_workers"] = min_workers
        if name is not None:
            self._values["name"] = name
        if network_configuration is not None:
            self._values["network_configuration"] = network_configuration
        if plugins_s3_object_version is not None:
            self._values["plugins_s3_object_version"] = plugins_s3_object_version
        if plugins_s3_path is not None:
            self._values["plugins_s3_path"] = plugins_s3_path
        if requirements_s3_object_version is not None:
            self._values["requirements_s3_object_version"] = requirements_s3_object_version
        if requirements_s3_path is not None:
            self._values["requirements_s3_path"] = requirements_s3_path
        if schedulers is not None:
            self._values["schedulers"] = schedulers
        if source_bucket_arn is not None:
            self._values["source_bucket_arn"] = source_bucket_arn
        if startup_script_s3_object_version is not None:
            self._values["startup_script_s3_object_version"] = startup_script_s3_object_version
        if startup_script_s3_path is not None:
            self._values["startup_script_s3_path"] = startup_script_s3_path
        if tags is not None:
            self._values["tags"] = tags
        if webserver_access_mode is not None:
            self._values["webserver_access_mode"] = webserver_access_mode
        if weekly_maintenance_window_start is not None:
            self._values["weekly_maintenance_window_start"] = weekly_maintenance_window_start
        if worker_replacement_strategy is not None:
            self._values["worker_replacement_strategy"] = worker_replacement_strategy

    @builtins.property
    def airflow_configuration_options(self) -> typing.Any:
        '''A list of key-value pairs containing the Airflow configuration options for your environment.

        For example, ``core.default_timezone: utc`` . To learn more, see `Apache Airflow configuration options <https://docs.aws.amazon.com/mwaa/latest/userguide/configuring-env-variables.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-airflowconfigurationoptions
        '''
        result = self._values.get("airflow_configuration_options")
        return typing.cast(typing.Any, result)

    @builtins.property
    def airflow_version(self) -> typing.Optional[builtins.str]:
        '''The version of Apache Airflow to use for the environment.

        If no value is specified, defaults to the latest version.

        If you specify a newer version number for an existing environment, the version update requires some service interruption before taking effect.

        *Allowed Values* : ``2.7.2`` | ``2.8.1`` | ``2.9.2`` | ``2.10.1`` | ``2.10.3`` | ``3.0.6`` (latest)

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-airflowversion
        '''
        result = self._values.get("airflow_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dag_s3_path(self) -> typing.Optional[builtins.str]:
        '''The relative path to the DAGs folder on your Amazon S3 bucket.

        For example, ``dags`` . To learn more, see `Adding or updating DAGs <https://docs.aws.amazon.com/mwaa/latest/userguide/configuring-dag-folder.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-dags3path
        '''
        result = self._values.get("dag_s3_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoint_management(self) -> typing.Optional[builtins.str]:
        '''Defines whether the VPC endpoints configured for the environment are created, and managed, by the customer or by Amazon MWAA.

        If set to ``SERVICE`` , Amazon MWAA will create and manage the required VPC endpoints in your VPC. If set to ``CUSTOMER`` , you must create, and manage, the VPC endpoints in your VPC.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-endpointmanagement
        '''
        result = self._values.get("endpoint_management")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_class(self) -> typing.Optional[builtins.str]:
        '''The environment class type.

        Valid values: ``mw1.micro`` , ``mw1.small`` , ``mw1.medium`` , ``mw1.large`` , ``mw1.1large`` , and ``mw1.2large`` . To learn more, see `Amazon MWAA environment class <https://docs.aws.amazon.com/mwaa/latest/userguide/environment-class.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-environmentclass
        '''
        result = self._values.get("environment_class")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execution_role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the execution role in IAM that allows MWAA to access AWS resources in your environment.

        For example, ``arn:aws:iam::123456789:role/my-execution-role`` . To learn more, see `Amazon MWAA Execution role <https://docs.aws.amazon.com/mwaa/latest/userguide/mwaa-create-role.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-executionrolearn
        '''
        result = self._values.get("execution_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[builtins.str]:
        '''The AWS Key Management Service (KMS) key to encrypt and decrypt the data in your environment.

        You can use an AWS KMS key managed by MWAA, or a customer-managed KMS key (advanced).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-kmskey
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.LoggingConfigurationProperty"]]:
        '''The Apache Airflow logs being sent to CloudWatch Logs: ``DagProcessingLogs`` , ``SchedulerLogs`` , ``TaskLogs`` , ``WebserverLogs`` , ``WorkerLogs`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-loggingconfiguration
        '''
        result = self._values.get("logging_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.LoggingConfigurationProperty"]], result)

    @builtins.property
    def max_webservers(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of web servers that you want to run in your environment.

        Amazon MWAA scales the number of Apache Airflow web servers up to the number you specify for ``MaxWebservers`` when you interact with your Apache Airflow environment using Apache Airflow REST API, or the Apache Airflow CLI. For example, in scenarios where your workload requires network calls to the Apache Airflow REST API with a high transaction-per-second (TPS) rate, Amazon MWAA will increase the number of web servers up to the number set in ``MaxWebserers`` . As TPS rates decrease Amazon MWAA disposes of the additional web servers, and scales down to the number set in ``MinxWebserers`` .

        Valid values: For environments larger than mw1.micro, accepts values from ``2`` to ``5`` . Defaults to ``2`` for all environment sizes except mw1.micro, which defaults to ``1`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-maxwebservers
        '''
        result = self._values.get("max_webservers")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_workers(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of workers that you want to run in your environment.

        MWAA scales the number of Apache Airflow workers up to the number you specify in the ``MaxWorkers`` field. For example, ``20`` . When there are no more tasks running, and no more in the queue, MWAA disposes of the extra workers leaving the one worker that is included with your environment, or the number you specify in ``MinWorkers`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-maxworkers
        '''
        result = self._values.get("max_workers")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_webservers(self) -> typing.Optional[jsii.Number]:
        '''The minimum number of web servers that you want to run in your environment.

        Amazon MWAA scales the number of Apache Airflow web servers up to the number you specify for ``MaxWebservers`` when you interact with your Apache Airflow environment using Apache Airflow REST API, or the Apache Airflow CLI. As the transaction-per-second rate, and the network load, decrease, Amazon MWAA disposes of the additional web servers, and scales down to the number set in ``MinxWebserers`` .

        Valid values: For environments larger than mw1.micro, accepts values from ``2`` to ``5`` . Defaults to ``2`` for all environment sizes except mw1.micro, which defaults to ``1`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-minwebservers
        '''
        result = self._values.get("min_webservers")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_workers(self) -> typing.Optional[jsii.Number]:
        '''The minimum number of workers that you want to run in your environment.

        MWAA scales the number of Apache Airflow workers up to the number you specify in the ``MaxWorkers`` field. When there are no more tasks running, and no more in the queue, MWAA disposes of the extra workers leaving the worker count you specify in the ``MinWorkers`` field. For example, ``2`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-minworkers
        '''
        result = self._values.get("min_workers")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of your Amazon MWAA environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.NetworkConfigurationProperty"]]:
        '''The VPC networking components used to secure and enable network traffic between the AWS resources for your environment.

        To learn more, see `About networking on Amazon MWAA <https://docs.aws.amazon.com/mwaa/latest/userguide/networking-about.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-networkconfiguration
        '''
        result = self._values.get("network_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.NetworkConfigurationProperty"]], result)

    @builtins.property
    def plugins_s3_object_version(self) -> typing.Optional[builtins.str]:
        '''The version of the plugins.zip file on your Amazon S3 bucket. To learn more, see `Installing custom plugins <https://docs.aws.amazon.com/mwaa/latest/userguide/configuring-dag-import-plugins.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-pluginss3objectversion
        '''
        result = self._values.get("plugins_s3_object_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def plugins_s3_path(self) -> typing.Optional[builtins.str]:
        '''The relative path to the ``plugins.zip`` file on your Amazon S3 bucket. For example, ``plugins.zip`` . To learn more, see `Installing custom plugins <https://docs.aws.amazon.com/mwaa/latest/userguide/configuring-dag-import-plugins.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-pluginss3path
        '''
        result = self._values.get("plugins_s3_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def requirements_s3_object_version(self) -> typing.Optional[builtins.str]:
        '''The version of the requirements.txt file on your Amazon S3 bucket. To learn more, see `Installing Python dependencies <https://docs.aws.amazon.com/mwaa/latest/userguide/working-dags-dependencies.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-requirementss3objectversion
        '''
        result = self._values.get("requirements_s3_object_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def requirements_s3_path(self) -> typing.Optional[builtins.str]:
        '''The relative path to the ``requirements.txt`` file on your Amazon S3 bucket. For example, ``requirements.txt`` . To learn more, see `Installing Python dependencies <https://docs.aws.amazon.com/mwaa/latest/userguide/working-dags-dependencies.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-requirementss3path
        '''
        result = self._values.get("requirements_s3_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedulers(self) -> typing.Optional[jsii.Number]:
        '''The number of schedulers that you want to run in your environment. Valid values:.

        - *v2* - For environments larger than mw1.micro, accepts values from 2 to 5. Defaults to 2 for all environment sizes except mw1.micro, which defaults to 1.
        - *v1* - Accepts 1.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-schedulers
        '''
        result = self._values.get("schedulers")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def source_bucket_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the Amazon S3 bucket where your DAG code and supporting files are stored.

        For example, ``arn:aws:s3:::my-airflow-bucket-unique-name`` . To learn more, see `Create an Amazon S3 bucket for Amazon MWAA <https://docs.aws.amazon.com/mwaa/latest/userguide/mwaa-s3-bucket.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-sourcebucketarn
        '''
        result = self._values.get("source_bucket_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def startup_script_s3_object_version(self) -> typing.Optional[builtins.str]:
        '''The version of the startup shell script in your Amazon S3 bucket.

        You must specify the `version ID <https://docs.aws.amazon.com/AmazonS3/latest/userguide/versioning-workflows.html>`_ that Amazon S3 assigns to the file every time you update the script.

        Version IDs are Unicode, UTF-8 encoded, URL-ready, opaque strings that are no more than 1,024 bytes long. The following is an example:

        ``3sL4kqtJlcpXroDTDmJ+rmSpXd3dIbrHY+MTRCxf3vjVBH40Nr8X8gdRQBpUMLUo``

        For more information, see `Using a startup script <https://docs.aws.amazon.com/mwaa/latest/userguide/using-startup-script.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-startupscripts3objectversion
        '''
        result = self._values.get("startup_script_s3_object_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def startup_script_s3_path(self) -> typing.Optional[builtins.str]:
        '''The relative path to the startup shell script in your Amazon S3 bucket. For example, ``s3://mwaa-environment/startup.sh`` .

        Amazon MWAA runs the script as your environment starts, and before running the Apache Airflow process. You can use this script to install dependencies, modify Apache Airflow configuration options, and set environment variables. For more information, see `Using a startup script <https://docs.aws.amazon.com/mwaa/latest/userguide/using-startup-script.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-startupscripts3path
        '''
        result = self._values.get("startup_script_s3_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''The key-value tag pairs associated to your environment. For example, ``"Environment": "Staging"`` . To learn more, see `Tagging <https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`_ .

        If you specify new tags for an existing environment, the update requires service interruption before taking effect.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    @builtins.property
    def webserver_access_mode(self) -> typing.Optional[builtins.str]:
        '''The Apache Airflow *Web server* access mode.

        To learn more, see `Apache Airflow access modes <https://docs.aws.amazon.com/mwaa/latest/userguide/configuring-networking.html>`_ . Valid values: ``PRIVATE_ONLY`` or ``PUBLIC_ONLY`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-webserveraccessmode
        '''
        result = self._values.get("webserver_access_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def weekly_maintenance_window_start(self) -> typing.Optional[builtins.str]:
        '''The day and time of the week to start weekly maintenance updates of your environment in the following format: ``DAY:HH:MM`` .

        For example: ``TUE:03:30`` . You can specify a start time in 30 minute increments only. Supported input includes the following:

        - MON|TUE|WED|THU|FRI|SAT|SUN:([01]\\d|2[0-3]):(00|30)

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-weeklymaintenancewindowstart
        '''
        result = self._values.get("weekly_maintenance_window_start")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def worker_replacement_strategy(self) -> typing.Optional[builtins.str]:
        '''The worker replacement strategy to use when updating the environment.

        Valid values: ``FORCED``, ``GRACEFUL``. FORCED means Apache Airflow workers will be stopped and replaced without waiting for tasks to complete before an update. GRACEFUL means Apache Airflow workers will be able to complete running tasks for up to 12 hours during an update before being stopped and replaced.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-workerreplacementstrategy
        '''
        result = self._values.get("worker_replacement_strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEnvironmentMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnEnvironmentPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_mwaa.mixins.CfnEnvironmentPropsMixin",
):
    '''The ``AWS::MWAA::Environment`` resource creates an Amazon Managed Workflows for Apache Airflow (MWAA) environment.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html
    :cloudformationResource: AWS::MWAA::Environment
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_mwaa import mixins as mwaa_mixins
        
        # airflow_configuration_options: Any
        # tags: Any
        
        cfn_environment_props_mixin = mwaa_mixins.CfnEnvironmentPropsMixin(mwaa_mixins.CfnEnvironmentMixinProps(
            airflow_configuration_options=airflow_configuration_options,
            airflow_version="airflowVersion",
            dag_s3_path="dagS3Path",
            endpoint_management="endpointManagement",
            environment_class="environmentClass",
            execution_role_arn="executionRoleArn",
            kms_key="kmsKey",
            logging_configuration=mwaa_mixins.CfnEnvironmentPropsMixin.LoggingConfigurationProperty(
                dag_processing_logs=mwaa_mixins.CfnEnvironmentPropsMixin.ModuleLoggingConfigurationProperty(
                    cloud_watch_log_group_arn="cloudWatchLogGroupArn",
                    enabled=False,
                    log_level="logLevel"
                ),
                scheduler_logs=mwaa_mixins.CfnEnvironmentPropsMixin.ModuleLoggingConfigurationProperty(
                    cloud_watch_log_group_arn="cloudWatchLogGroupArn",
                    enabled=False,
                    log_level="logLevel"
                ),
                task_logs=mwaa_mixins.CfnEnvironmentPropsMixin.ModuleLoggingConfigurationProperty(
                    cloud_watch_log_group_arn="cloudWatchLogGroupArn",
                    enabled=False,
                    log_level="logLevel"
                ),
                webserver_logs=mwaa_mixins.CfnEnvironmentPropsMixin.ModuleLoggingConfigurationProperty(
                    cloud_watch_log_group_arn="cloudWatchLogGroupArn",
                    enabled=False,
                    log_level="logLevel"
                ),
                worker_logs=mwaa_mixins.CfnEnvironmentPropsMixin.ModuleLoggingConfigurationProperty(
                    cloud_watch_log_group_arn="cloudWatchLogGroupArn",
                    enabled=False,
                    log_level="logLevel"
                )
            ),
            max_webservers=123,
            max_workers=123,
            min_webservers=123,
            min_workers=123,
            name="name",
            network_configuration=mwaa_mixins.CfnEnvironmentPropsMixin.NetworkConfigurationProperty(
                security_group_ids=["securityGroupIds"],
                subnet_ids=["subnetIds"]
            ),
            plugins_s3_object_version="pluginsS3ObjectVersion",
            plugins_s3_path="pluginsS3Path",
            requirements_s3_object_version="requirementsS3ObjectVersion",
            requirements_s3_path="requirementsS3Path",
            schedulers=123,
            source_bucket_arn="sourceBucketArn",
            startup_script_s3_object_version="startupScriptS3ObjectVersion",
            startup_script_s3_path="startupScriptS3Path",
            tags=tags,
            webserver_access_mode="webserverAccessMode",
            weekly_maintenance_window_start="weeklyMaintenanceWindowStart",
            worker_replacement_strategy="workerReplacementStrategy"
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
        '''Create a mixin to apply properties to ``AWS::MWAA::Environment``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__320deaf270d9364358f4c5adb28acf054ea0c93c1359eb47331eae79bcc11ec1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2449f729b0f90f2c1d6216e3b523931a484a432cc64b9f5465961b9522f444f4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39a36626065205798e96a1dfc800e91b6b46481b629d0dc11d3d4883d56578c5)
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
        jsii_type="@aws-cdk/mixins-preview.aws_mwaa.mixins.CfnEnvironmentPropsMixin.LoggingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dag_processing_logs": "dagProcessingLogs",
            "scheduler_logs": "schedulerLogs",
            "task_logs": "taskLogs",
            "webserver_logs": "webserverLogs",
            "worker_logs": "workerLogs",
        },
    )
    class LoggingConfigurationProperty:
        def __init__(
            self,
            *,
            dag_processing_logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEnvironmentPropsMixin.ModuleLoggingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            scheduler_logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEnvironmentPropsMixin.ModuleLoggingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            task_logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEnvironmentPropsMixin.ModuleLoggingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            webserver_logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEnvironmentPropsMixin.ModuleLoggingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            worker_logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEnvironmentPropsMixin.ModuleLoggingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The type of Apache Airflow logs to send to CloudWatch Logs.

            :param dag_processing_logs: Defines the processing logs sent to CloudWatch Logs and the logging level to send.
            :param scheduler_logs: Defines the scheduler logs sent to CloudWatch Logs and the logging level to send.
            :param task_logs: Defines the task logs sent to CloudWatch Logs and the logging level to send.
            :param webserver_logs: Defines the web server logs sent to CloudWatch Logs and the logging level to send.
            :param worker_logs: Defines the worker logs sent to CloudWatch Logs and the logging level to send.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mwaa-environment-loggingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mwaa import mixins as mwaa_mixins
                
                logging_configuration_property = mwaa_mixins.CfnEnvironmentPropsMixin.LoggingConfigurationProperty(
                    dag_processing_logs=mwaa_mixins.CfnEnvironmentPropsMixin.ModuleLoggingConfigurationProperty(
                        cloud_watch_log_group_arn="cloudWatchLogGroupArn",
                        enabled=False,
                        log_level="logLevel"
                    ),
                    scheduler_logs=mwaa_mixins.CfnEnvironmentPropsMixin.ModuleLoggingConfigurationProperty(
                        cloud_watch_log_group_arn="cloudWatchLogGroupArn",
                        enabled=False,
                        log_level="logLevel"
                    ),
                    task_logs=mwaa_mixins.CfnEnvironmentPropsMixin.ModuleLoggingConfigurationProperty(
                        cloud_watch_log_group_arn="cloudWatchLogGroupArn",
                        enabled=False,
                        log_level="logLevel"
                    ),
                    webserver_logs=mwaa_mixins.CfnEnvironmentPropsMixin.ModuleLoggingConfigurationProperty(
                        cloud_watch_log_group_arn="cloudWatchLogGroupArn",
                        enabled=False,
                        log_level="logLevel"
                    ),
                    worker_logs=mwaa_mixins.CfnEnvironmentPropsMixin.ModuleLoggingConfigurationProperty(
                        cloud_watch_log_group_arn="cloudWatchLogGroupArn",
                        enabled=False,
                        log_level="logLevel"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3db96e0f4f391e79b053716c17633ae038683b2a3938f9ee5b925b25e2dd4a74)
                check_type(argname="argument dag_processing_logs", value=dag_processing_logs, expected_type=type_hints["dag_processing_logs"])
                check_type(argname="argument scheduler_logs", value=scheduler_logs, expected_type=type_hints["scheduler_logs"])
                check_type(argname="argument task_logs", value=task_logs, expected_type=type_hints["task_logs"])
                check_type(argname="argument webserver_logs", value=webserver_logs, expected_type=type_hints["webserver_logs"])
                check_type(argname="argument worker_logs", value=worker_logs, expected_type=type_hints["worker_logs"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dag_processing_logs is not None:
                self._values["dag_processing_logs"] = dag_processing_logs
            if scheduler_logs is not None:
                self._values["scheduler_logs"] = scheduler_logs
            if task_logs is not None:
                self._values["task_logs"] = task_logs
            if webserver_logs is not None:
                self._values["webserver_logs"] = webserver_logs
            if worker_logs is not None:
                self._values["worker_logs"] = worker_logs

        @builtins.property
        def dag_processing_logs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.ModuleLoggingConfigurationProperty"]]:
            '''Defines the processing logs sent to CloudWatch Logs and the logging level to send.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mwaa-environment-loggingconfiguration.html#cfn-mwaa-environment-loggingconfiguration-dagprocessinglogs
            '''
            result = self._values.get("dag_processing_logs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.ModuleLoggingConfigurationProperty"]], result)

        @builtins.property
        def scheduler_logs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.ModuleLoggingConfigurationProperty"]]:
            '''Defines the scheduler logs sent to CloudWatch Logs and the logging level to send.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mwaa-environment-loggingconfiguration.html#cfn-mwaa-environment-loggingconfiguration-schedulerlogs
            '''
            result = self._values.get("scheduler_logs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.ModuleLoggingConfigurationProperty"]], result)

        @builtins.property
        def task_logs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.ModuleLoggingConfigurationProperty"]]:
            '''Defines the task logs sent to CloudWatch Logs and the logging level to send.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mwaa-environment-loggingconfiguration.html#cfn-mwaa-environment-loggingconfiguration-tasklogs
            '''
            result = self._values.get("task_logs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.ModuleLoggingConfigurationProperty"]], result)

        @builtins.property
        def webserver_logs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.ModuleLoggingConfigurationProperty"]]:
            '''Defines the web server logs sent to CloudWatch Logs and the logging level to send.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mwaa-environment-loggingconfiguration.html#cfn-mwaa-environment-loggingconfiguration-webserverlogs
            '''
            result = self._values.get("webserver_logs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.ModuleLoggingConfigurationProperty"]], result)

        @builtins.property
        def worker_logs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.ModuleLoggingConfigurationProperty"]]:
            '''Defines the worker logs sent to CloudWatch Logs and the logging level to send.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mwaa-environment-loggingconfiguration.html#cfn-mwaa-environment-loggingconfiguration-workerlogs
            '''
            result = self._values.get("worker_logs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.ModuleLoggingConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mwaa.mixins.CfnEnvironmentPropsMixin.ModuleLoggingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cloud_watch_log_group_arn": "cloudWatchLogGroupArn",
            "enabled": "enabled",
            "log_level": "logLevel",
        },
    )
    class ModuleLoggingConfigurationProperty:
        def __init__(
            self,
            *,
            cloud_watch_log_group_arn: typing.Optional[builtins.str] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            log_level: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines the type of logs to send for the Apache Airflow log type (e.g. ``DagProcessingLogs`` ).

            :param cloud_watch_log_group_arn: The ARN of the CloudWatch Logs log group for each type of Apache Airflow log type that you have enabled. .. epigraph:: ``CloudWatchLogGroupArn`` is available only as a return value, accessible when specified as an attribute in the ```Fn:GetAtt`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#aws-resource-mwaa-environment-return-values>`_ intrinsic function. Any value you provide for ``CloudWatchLogGroupArn`` is discarded by Amazon MWAA.
            :param enabled: Indicates whether to enable the Apache Airflow log type (e.g. ``DagProcessingLogs`` ) in CloudWatch Logs.
            :param log_level: Defines the Apache Airflow logs to send for the log type (e.g. ``DagProcessingLogs`` ) to CloudWatch Logs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mwaa-environment-moduleloggingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mwaa import mixins as mwaa_mixins
                
                module_logging_configuration_property = mwaa_mixins.CfnEnvironmentPropsMixin.ModuleLoggingConfigurationProperty(
                    cloud_watch_log_group_arn="cloudWatchLogGroupArn",
                    enabled=False,
                    log_level="logLevel"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f551e18a19c11d875cacc6ed087aace983bd9b6f22337d9e4e1b80fbeb663009)
                check_type(argname="argument cloud_watch_log_group_arn", value=cloud_watch_log_group_arn, expected_type=type_hints["cloud_watch_log_group_arn"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument log_level", value=log_level, expected_type=type_hints["log_level"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloud_watch_log_group_arn is not None:
                self._values["cloud_watch_log_group_arn"] = cloud_watch_log_group_arn
            if enabled is not None:
                self._values["enabled"] = enabled
            if log_level is not None:
                self._values["log_level"] = log_level

        @builtins.property
        def cloud_watch_log_group_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the CloudWatch Logs log group for each type of Apache Airflow log type that you have enabled.

            .. epigraph::

               ``CloudWatchLogGroupArn`` is available only as a return value, accessible when specified as an attribute in the ```Fn:GetAtt`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#aws-resource-mwaa-environment-return-values>`_ intrinsic function. Any value you provide for ``CloudWatchLogGroupArn`` is discarded by Amazon MWAA.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mwaa-environment-moduleloggingconfiguration.html#cfn-mwaa-environment-moduleloggingconfiguration-cloudwatchloggrouparn
            '''
            result = self._values.get("cloud_watch_log_group_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether to enable the Apache Airflow log type (e.g. ``DagProcessingLogs`` ) in CloudWatch Logs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mwaa-environment-moduleloggingconfiguration.html#cfn-mwaa-environment-moduleloggingconfiguration-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def log_level(self) -> typing.Optional[builtins.str]:
            '''Defines the Apache Airflow logs to send for the log type (e.g. ``DagProcessingLogs`` ) to CloudWatch Logs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mwaa-environment-moduleloggingconfiguration.html#cfn-mwaa-environment-moduleloggingconfiguration-loglevel
            '''
            result = self._values.get("log_level")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ModuleLoggingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mwaa.mixins.CfnEnvironmentPropsMixin.NetworkConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
        },
    )
    class NetworkConfigurationProperty:
        def __init__(
            self,
            *,
            security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The VPC networking components used to secure and enable network traffic between the AWS resources for your environment.

            To learn more, see `About networking on Amazon MWAA <https://docs.aws.amazon.com/mwaa/latest/userguide/networking-about.html>`_ .

            :param security_group_ids: A list of one or more security group IDs. Accepts up to 5 security group IDs. A security group must be attached to the same VPC as the subnets. To learn more, see `Security in your VPC on Amazon MWAA <https://docs.aws.amazon.com/mwaa/latest/userguide/vpc-security.html>`_ .
            :param subnet_ids: A list of subnet IDs. *Required* to create an environment. Must be private subnets in two different availability zones. A subnet must be attached to the same VPC as the security group. To learn more, see `About networking on Amazon MWAA <https://docs.aws.amazon.com/mwaa/latest/userguide/networking-about.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mwaa-environment-networkconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mwaa import mixins as mwaa_mixins
                
                network_configuration_property = mwaa_mixins.CfnEnvironmentPropsMixin.NetworkConfigurationProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1d20b5537b88258cc4f4ee1ab2d3eec1612bb12dd8fc88401380dd49dc4ce569)
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
                check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnet_ids is not None:
                self._values["subnet_ids"] = subnet_ids

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of one or more security group IDs.

            Accepts up to 5 security group IDs. A security group must be attached to the same VPC as the subnets. To learn more, see `Security in your VPC on Amazon MWAA <https://docs.aws.amazon.com/mwaa/latest/userguide/vpc-security.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mwaa-environment-networkconfiguration.html#cfn-mwaa-environment-networkconfiguration-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of subnet IDs.

            *Required* to create an environment. Must be private subnets in two different availability zones. A subnet must be attached to the same VPC as the security group. To learn more, see `About networking on Amazon MWAA <https://docs.aws.amazon.com/mwaa/latest/userguide/networking-about.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mwaa-environment-networkconfiguration.html#cfn-mwaa-environment-networkconfiguration-subnetids
            '''
            result = self._values.get("subnet_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NetworkConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnEnvironmentMixinProps",
    "CfnEnvironmentPropsMixin",
]

publication.publish()

def _typecheckingstub__2079f9bcb3de1193b14b7dcb9de63c2adcf4e68fa55b12000c315e3b0a6b005c(
    *,
    airflow_configuration_options: typing.Any = None,
    airflow_version: typing.Optional[builtins.str] = None,
    dag_s3_path: typing.Optional[builtins.str] = None,
    endpoint_management: typing.Optional[builtins.str] = None,
    environment_class: typing.Optional[builtins.str] = None,
    execution_role_arn: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[builtins.str] = None,
    logging_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEnvironmentPropsMixin.LoggingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    max_webservers: typing.Optional[jsii.Number] = None,
    max_workers: typing.Optional[jsii.Number] = None,
    min_webservers: typing.Optional[jsii.Number] = None,
    min_workers: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    network_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEnvironmentPropsMixin.NetworkConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    plugins_s3_object_version: typing.Optional[builtins.str] = None,
    plugins_s3_path: typing.Optional[builtins.str] = None,
    requirements_s3_object_version: typing.Optional[builtins.str] = None,
    requirements_s3_path: typing.Optional[builtins.str] = None,
    schedulers: typing.Optional[jsii.Number] = None,
    source_bucket_arn: typing.Optional[builtins.str] = None,
    startup_script_s3_object_version: typing.Optional[builtins.str] = None,
    startup_script_s3_path: typing.Optional[builtins.str] = None,
    tags: typing.Any = None,
    webserver_access_mode: typing.Optional[builtins.str] = None,
    weekly_maintenance_window_start: typing.Optional[builtins.str] = None,
    worker_replacement_strategy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__320deaf270d9364358f4c5adb28acf054ea0c93c1359eb47331eae79bcc11ec1(
    props: typing.Union[CfnEnvironmentMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2449f729b0f90f2c1d6216e3b523931a484a432cc64b9f5465961b9522f444f4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39a36626065205798e96a1dfc800e91b6b46481b629d0dc11d3d4883d56578c5(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3db96e0f4f391e79b053716c17633ae038683b2a3938f9ee5b925b25e2dd4a74(
    *,
    dag_processing_logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEnvironmentPropsMixin.ModuleLoggingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    scheduler_logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEnvironmentPropsMixin.ModuleLoggingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    task_logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEnvironmentPropsMixin.ModuleLoggingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    webserver_logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEnvironmentPropsMixin.ModuleLoggingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    worker_logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEnvironmentPropsMixin.ModuleLoggingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f551e18a19c11d875cacc6ed087aace983bd9b6f22337d9e4e1b80fbeb663009(
    *,
    cloud_watch_log_group_arn: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    log_level: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d20b5537b88258cc4f4ee1ab2d3eec1612bb12dd8fc88401380dd49dc4ce569(
    *,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
