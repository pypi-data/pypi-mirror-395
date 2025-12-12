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
    jsii_type="@aws-cdk/mixins-preview.aws_emrserverless.mixins.CfnApplicationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "architecture": "architecture",
        "auto_start_configuration": "autoStartConfiguration",
        "auto_stop_configuration": "autoStopConfiguration",
        "identity_center_configuration": "identityCenterConfiguration",
        "image_configuration": "imageConfiguration",
        "initial_capacity": "initialCapacity",
        "interactive_configuration": "interactiveConfiguration",
        "maximum_capacity": "maximumCapacity",
        "monitoring_configuration": "monitoringConfiguration",
        "name": "name",
        "network_configuration": "networkConfiguration",
        "release_label": "releaseLabel",
        "runtime_configuration": "runtimeConfiguration",
        "scheduler_configuration": "schedulerConfiguration",
        "tags": "tags",
        "type": "type",
        "worker_type_specifications": "workerTypeSpecifications",
    },
)
class CfnApplicationMixinProps:
    def __init__(
        self,
        *,
        architecture: typing.Optional[builtins.str] = None,
        auto_start_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.AutoStartConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        auto_stop_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.AutoStopConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        identity_center_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.IdentityCenterConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        image_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.ImageConfigurationInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        initial_capacity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.InitialCapacityConfigKeyValuePairProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        interactive_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.InteractiveConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        maximum_capacity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.MaximumAllowedResourcesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        monitoring_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.MonitoringConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        network_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.NetworkConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        release_label: typing.Optional[builtins.str] = None,
        runtime_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.ConfigurationObjectProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        scheduler_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.SchedulerConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
        worker_type_specifications: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.WorkerTypeSpecificationInputProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnApplicationPropsMixin.

        :param architecture: The CPU architecture of an application.
        :param auto_start_configuration: The configuration for an application to automatically start on job submission.
        :param auto_stop_configuration: The configuration for an application to automatically stop after a certain amount of time being idle.
        :param identity_center_configuration: The IAM Identity Center configuration applied to enable trusted identity propagation.
        :param image_configuration: The image configuration applied to all worker types.
        :param initial_capacity: The initial capacity of the application.
        :param interactive_configuration: The interactive configuration object that enables the interactive use cases for an application.
        :param maximum_capacity: The maximum capacity of the application. This is cumulative across all workers at any given point in time during the lifespan of the application is created. No new resources will be created once any one of the defined limits is hit.
        :param monitoring_configuration: A configuration specification to be used when provisioning an application. A configuration consists of a classification, properties, and optional nested configurations. A classification refers to an application-specific configuration file. Properties are the settings you want to change in that file.
        :param name: The name of the application.
        :param network_configuration: The network configuration for customer VPC connectivity for the application.
        :param release_label: The EMR release associated with the application.
        :param runtime_configuration: The `Configuration <https://docs.aws.amazon.com/emr-serverless/latest/APIReference/API_Configuration.html>`_ specifications of an application. Each configuration consists of a classification and properties. You use this parameter when creating or updating an application. To see the runtimeConfiguration object of an application, run the `GetApplication <https://docs.aws.amazon.com/emr-serverless/latest/APIReference/API_GetApplication.html>`_ API operation.
        :param scheduler_configuration: The scheduler configuration for batch and streaming jobs running on this application. Supported with release labels emr-7.0.0 and above.
        :param tags: The tags assigned to the application.
        :param type: The type of application, such as Spark or Hive.
        :param worker_type_specifications: The specification applied to each worker type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrserverless-application.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_emrserverless import mixins as emrserverless_mixins
            
            # configuration_object_property_: emrserverless_mixins.CfnApplicationPropsMixin.ConfigurationObjectProperty
            
            cfn_application_mixin_props = emrserverless_mixins.CfnApplicationMixinProps(
                architecture="architecture",
                auto_start_configuration=emrserverless_mixins.CfnApplicationPropsMixin.AutoStartConfigurationProperty(
                    enabled=False
                ),
                auto_stop_configuration=emrserverless_mixins.CfnApplicationPropsMixin.AutoStopConfigurationProperty(
                    enabled=False,
                    idle_timeout_minutes=123
                ),
                identity_center_configuration=emrserverless_mixins.CfnApplicationPropsMixin.IdentityCenterConfigurationProperty(
                    identity_center_instance_arn="identityCenterInstanceArn"
                ),
                image_configuration=emrserverless_mixins.CfnApplicationPropsMixin.ImageConfigurationInputProperty(
                    image_uri="imageUri"
                ),
                initial_capacity=[emrserverless_mixins.CfnApplicationPropsMixin.InitialCapacityConfigKeyValuePairProperty(
                    key="key",
                    value=emrserverless_mixins.CfnApplicationPropsMixin.InitialCapacityConfigProperty(
                        worker_configuration=emrserverless_mixins.CfnApplicationPropsMixin.WorkerConfigurationProperty(
                            cpu="cpu",
                            disk="disk",
                            disk_type="diskType",
                            memory="memory"
                        ),
                        worker_count=123
                    )
                )],
                interactive_configuration=emrserverless_mixins.CfnApplicationPropsMixin.InteractiveConfigurationProperty(
                    livy_endpoint_enabled=False,
                    studio_enabled=False
                ),
                maximum_capacity=emrserverless_mixins.CfnApplicationPropsMixin.MaximumAllowedResourcesProperty(
                    cpu="cpu",
                    disk="disk",
                    memory="memory"
                ),
                monitoring_configuration=emrserverless_mixins.CfnApplicationPropsMixin.MonitoringConfigurationProperty(
                    cloud_watch_logging_configuration=emrserverless_mixins.CfnApplicationPropsMixin.CloudWatchLoggingConfigurationProperty(
                        enabled=False,
                        encryption_key_arn="encryptionKeyArn",
                        log_group_name="logGroupName",
                        log_stream_name_prefix="logStreamNamePrefix",
                        log_type_map=[emrserverless_mixins.CfnApplicationPropsMixin.LogTypeMapKeyValuePairProperty(
                            key="key",
                            value=["value"]
                        )]
                    ),
                    managed_persistence_monitoring_configuration=emrserverless_mixins.CfnApplicationPropsMixin.ManagedPersistenceMonitoringConfigurationProperty(
                        enabled=False,
                        encryption_key_arn="encryptionKeyArn"
                    ),
                    prometheus_monitoring_configuration=emrserverless_mixins.CfnApplicationPropsMixin.PrometheusMonitoringConfigurationProperty(
                        remote_write_url="remoteWriteUrl"
                    ),
                    s3_monitoring_configuration=emrserverless_mixins.CfnApplicationPropsMixin.S3MonitoringConfigurationProperty(
                        encryption_key_arn="encryptionKeyArn",
                        log_uri="logUri"
                    )
                ),
                name="name",
                network_configuration=emrserverless_mixins.CfnApplicationPropsMixin.NetworkConfigurationProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                ),
                release_label="releaseLabel",
                runtime_configuration=[emrserverless_mixins.CfnApplicationPropsMixin.ConfigurationObjectProperty(
                    classification="classification",
                    configurations=[configuration_object_property_],
                    properties={
                        "properties_key": "properties"
                    }
                )],
                scheduler_configuration=emrserverless_mixins.CfnApplicationPropsMixin.SchedulerConfigurationProperty(
                    max_concurrent_runs=123,
                    queue_timeout_minutes=123
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                type="type",
                worker_type_specifications={
                    "worker_type_specifications_key": emrserverless_mixins.CfnApplicationPropsMixin.WorkerTypeSpecificationInputProperty(
                        image_configuration=emrserverless_mixins.CfnApplicationPropsMixin.ImageConfigurationInputProperty(
                            image_uri="imageUri"
                        )
                    )
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8750ae43bdfa18bedb8e43d4aab1c17f3f33d7428ab897cfe52911e61320a92)
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
            check_type(argname="argument auto_start_configuration", value=auto_start_configuration, expected_type=type_hints["auto_start_configuration"])
            check_type(argname="argument auto_stop_configuration", value=auto_stop_configuration, expected_type=type_hints["auto_stop_configuration"])
            check_type(argname="argument identity_center_configuration", value=identity_center_configuration, expected_type=type_hints["identity_center_configuration"])
            check_type(argname="argument image_configuration", value=image_configuration, expected_type=type_hints["image_configuration"])
            check_type(argname="argument initial_capacity", value=initial_capacity, expected_type=type_hints["initial_capacity"])
            check_type(argname="argument interactive_configuration", value=interactive_configuration, expected_type=type_hints["interactive_configuration"])
            check_type(argname="argument maximum_capacity", value=maximum_capacity, expected_type=type_hints["maximum_capacity"])
            check_type(argname="argument monitoring_configuration", value=monitoring_configuration, expected_type=type_hints["monitoring_configuration"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network_configuration", value=network_configuration, expected_type=type_hints["network_configuration"])
            check_type(argname="argument release_label", value=release_label, expected_type=type_hints["release_label"])
            check_type(argname="argument runtime_configuration", value=runtime_configuration, expected_type=type_hints["runtime_configuration"])
            check_type(argname="argument scheduler_configuration", value=scheduler_configuration, expected_type=type_hints["scheduler_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument worker_type_specifications", value=worker_type_specifications, expected_type=type_hints["worker_type_specifications"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if architecture is not None:
            self._values["architecture"] = architecture
        if auto_start_configuration is not None:
            self._values["auto_start_configuration"] = auto_start_configuration
        if auto_stop_configuration is not None:
            self._values["auto_stop_configuration"] = auto_stop_configuration
        if identity_center_configuration is not None:
            self._values["identity_center_configuration"] = identity_center_configuration
        if image_configuration is not None:
            self._values["image_configuration"] = image_configuration
        if initial_capacity is not None:
            self._values["initial_capacity"] = initial_capacity
        if interactive_configuration is not None:
            self._values["interactive_configuration"] = interactive_configuration
        if maximum_capacity is not None:
            self._values["maximum_capacity"] = maximum_capacity
        if monitoring_configuration is not None:
            self._values["monitoring_configuration"] = monitoring_configuration
        if name is not None:
            self._values["name"] = name
        if network_configuration is not None:
            self._values["network_configuration"] = network_configuration
        if release_label is not None:
            self._values["release_label"] = release_label
        if runtime_configuration is not None:
            self._values["runtime_configuration"] = runtime_configuration
        if scheduler_configuration is not None:
            self._values["scheduler_configuration"] = scheduler_configuration
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type
        if worker_type_specifications is not None:
            self._values["worker_type_specifications"] = worker_type_specifications

    @builtins.property
    def architecture(self) -> typing.Optional[builtins.str]:
        '''The CPU architecture of an application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrserverless-application.html#cfn-emrserverless-application-architecture
        '''
        result = self._values.get("architecture")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_start_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.AutoStartConfigurationProperty"]]:
        '''The configuration for an application to automatically start on job submission.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrserverless-application.html#cfn-emrserverless-application-autostartconfiguration
        '''
        result = self._values.get("auto_start_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.AutoStartConfigurationProperty"]], result)

    @builtins.property
    def auto_stop_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.AutoStopConfigurationProperty"]]:
        '''The configuration for an application to automatically stop after a certain amount of time being idle.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrserverless-application.html#cfn-emrserverless-application-autostopconfiguration
        '''
        result = self._values.get("auto_stop_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.AutoStopConfigurationProperty"]], result)

    @builtins.property
    def identity_center_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.IdentityCenterConfigurationProperty"]]:
        '''The IAM Identity Center configuration applied to enable trusted identity propagation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrserverless-application.html#cfn-emrserverless-application-identitycenterconfiguration
        '''
        result = self._values.get("identity_center_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.IdentityCenterConfigurationProperty"]], result)

    @builtins.property
    def image_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ImageConfigurationInputProperty"]]:
        '''The image configuration applied to all worker types.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrserverless-application.html#cfn-emrserverless-application-imageconfiguration
        '''
        result = self._values.get("image_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ImageConfigurationInputProperty"]], result)

    @builtins.property
    def initial_capacity(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.InitialCapacityConfigKeyValuePairProperty"]]]]:
        '''The initial capacity of the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrserverless-application.html#cfn-emrserverless-application-initialcapacity
        '''
        result = self._values.get("initial_capacity")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.InitialCapacityConfigKeyValuePairProperty"]]]], result)

    @builtins.property
    def interactive_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.InteractiveConfigurationProperty"]]:
        '''The interactive configuration object that enables the interactive use cases for an application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrserverless-application.html#cfn-emrserverless-application-interactiveconfiguration
        '''
        result = self._values.get("interactive_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.InteractiveConfigurationProperty"]], result)

    @builtins.property
    def maximum_capacity(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.MaximumAllowedResourcesProperty"]]:
        '''The maximum capacity of the application.

        This is cumulative across all workers at any given point in time during the lifespan of the application is created. No new resources will be created once any one of the defined limits is hit.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrserverless-application.html#cfn-emrserverless-application-maximumcapacity
        '''
        result = self._values.get("maximum_capacity")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.MaximumAllowedResourcesProperty"]], result)

    @builtins.property
    def monitoring_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.MonitoringConfigurationProperty"]]:
        '''A configuration specification to be used when provisioning an application.

        A configuration consists of a classification, properties, and optional nested configurations. A classification refers to an application-specific configuration file. Properties are the settings you want to change in that file.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrserverless-application.html#cfn-emrserverless-application-monitoringconfiguration
        '''
        result = self._values.get("monitoring_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.MonitoringConfigurationProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrserverless-application.html#cfn-emrserverless-application-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.NetworkConfigurationProperty"]]:
        '''The network configuration for customer VPC connectivity for the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrserverless-application.html#cfn-emrserverless-application-networkconfiguration
        '''
        result = self._values.get("network_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.NetworkConfigurationProperty"]], result)

    @builtins.property
    def release_label(self) -> typing.Optional[builtins.str]:
        '''The EMR release associated with the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrserverless-application.html#cfn-emrserverless-application-releaselabel
        '''
        result = self._values.get("release_label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ConfigurationObjectProperty"]]]]:
        '''The `Configuration <https://docs.aws.amazon.com/emr-serverless/latest/APIReference/API_Configuration.html>`_ specifications of an application. Each configuration consists of a classification and properties. You use this parameter when creating or updating an application. To see the runtimeConfiguration object of an application, run the `GetApplication <https://docs.aws.amazon.com/emr-serverless/latest/APIReference/API_GetApplication.html>`_ API operation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrserverless-application.html#cfn-emrserverless-application-runtimeconfiguration
        '''
        result = self._values.get("runtime_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ConfigurationObjectProperty"]]]], result)

    @builtins.property
    def scheduler_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.SchedulerConfigurationProperty"]]:
        '''The scheduler configuration for batch and streaming jobs running on this application.

        Supported with release labels emr-7.0.0 and above.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrserverless-application.html#cfn-emrserverless-application-schedulerconfiguration
        '''
        result = self._values.get("scheduler_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.SchedulerConfigurationProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags assigned to the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrserverless-application.html#cfn-emrserverless-application-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of application, such as Spark or Hive.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrserverless-application.html#cfn-emrserverless-application-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def worker_type_specifications(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.WorkerTypeSpecificationInputProperty"]]]]:
        '''The specification applied to each worker type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrserverless-application.html#cfn-emrserverless-application-workertypespecifications
        '''
        result = self._values.get("worker_type_specifications")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.WorkerTypeSpecificationInputProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnApplicationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_emrserverless.mixins.CfnApplicationPropsMixin",
):
    '''The ``AWS::EMRServerless::Application`` resource specifies an EMR Serverless application.

    An application uses open source analytics frameworks to run jobs that process data. To create an application, you must specify the release version for the open source framework version you want to use and the type of application you want, such as Apache Spark or Apache Hive. After you create an application, you can submit data processing jobs or interactive requests to it.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrserverless-application.html
    :cloudformationResource: AWS::EMRServerless::Application
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_emrserverless import mixins as emrserverless_mixins
        
        # configuration_object_property_: emrserverless_mixins.CfnApplicationPropsMixin.ConfigurationObjectProperty
        
        cfn_application_props_mixin = emrserverless_mixins.CfnApplicationPropsMixin(emrserverless_mixins.CfnApplicationMixinProps(
            architecture="architecture",
            auto_start_configuration=emrserverless_mixins.CfnApplicationPropsMixin.AutoStartConfigurationProperty(
                enabled=False
            ),
            auto_stop_configuration=emrserverless_mixins.CfnApplicationPropsMixin.AutoStopConfigurationProperty(
                enabled=False,
                idle_timeout_minutes=123
            ),
            identity_center_configuration=emrserverless_mixins.CfnApplicationPropsMixin.IdentityCenterConfigurationProperty(
                identity_center_instance_arn="identityCenterInstanceArn"
            ),
            image_configuration=emrserverless_mixins.CfnApplicationPropsMixin.ImageConfigurationInputProperty(
                image_uri="imageUri"
            ),
            initial_capacity=[emrserverless_mixins.CfnApplicationPropsMixin.InitialCapacityConfigKeyValuePairProperty(
                key="key",
                value=emrserverless_mixins.CfnApplicationPropsMixin.InitialCapacityConfigProperty(
                    worker_configuration=emrserverless_mixins.CfnApplicationPropsMixin.WorkerConfigurationProperty(
                        cpu="cpu",
                        disk="disk",
                        disk_type="diskType",
                        memory="memory"
                    ),
                    worker_count=123
                )
            )],
            interactive_configuration=emrserverless_mixins.CfnApplicationPropsMixin.InteractiveConfigurationProperty(
                livy_endpoint_enabled=False,
                studio_enabled=False
            ),
            maximum_capacity=emrserverless_mixins.CfnApplicationPropsMixin.MaximumAllowedResourcesProperty(
                cpu="cpu",
                disk="disk",
                memory="memory"
            ),
            monitoring_configuration=emrserverless_mixins.CfnApplicationPropsMixin.MonitoringConfigurationProperty(
                cloud_watch_logging_configuration=emrserverless_mixins.CfnApplicationPropsMixin.CloudWatchLoggingConfigurationProperty(
                    enabled=False,
                    encryption_key_arn="encryptionKeyArn",
                    log_group_name="logGroupName",
                    log_stream_name_prefix="logStreamNamePrefix",
                    log_type_map=[emrserverless_mixins.CfnApplicationPropsMixin.LogTypeMapKeyValuePairProperty(
                        key="key",
                        value=["value"]
                    )]
                ),
                managed_persistence_monitoring_configuration=emrserverless_mixins.CfnApplicationPropsMixin.ManagedPersistenceMonitoringConfigurationProperty(
                    enabled=False,
                    encryption_key_arn="encryptionKeyArn"
                ),
                prometheus_monitoring_configuration=emrserverless_mixins.CfnApplicationPropsMixin.PrometheusMonitoringConfigurationProperty(
                    remote_write_url="remoteWriteUrl"
                ),
                s3_monitoring_configuration=emrserverless_mixins.CfnApplicationPropsMixin.S3MonitoringConfigurationProperty(
                    encryption_key_arn="encryptionKeyArn",
                    log_uri="logUri"
                )
            ),
            name="name",
            network_configuration=emrserverless_mixins.CfnApplicationPropsMixin.NetworkConfigurationProperty(
                security_group_ids=["securityGroupIds"],
                subnet_ids=["subnetIds"]
            ),
            release_label="releaseLabel",
            runtime_configuration=[emrserverless_mixins.CfnApplicationPropsMixin.ConfigurationObjectProperty(
                classification="classification",
                configurations=[configuration_object_property_],
                properties={
                    "properties_key": "properties"
                }
            )],
            scheduler_configuration=emrserverless_mixins.CfnApplicationPropsMixin.SchedulerConfigurationProperty(
                max_concurrent_runs=123,
                queue_timeout_minutes=123
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            type="type",
            worker_type_specifications={
                "worker_type_specifications_key": emrserverless_mixins.CfnApplicationPropsMixin.WorkerTypeSpecificationInputProperty(
                    image_configuration=emrserverless_mixins.CfnApplicationPropsMixin.ImageConfigurationInputProperty(
                        image_uri="imageUri"
                    )
                )
            }
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnApplicationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::EMRServerless::Application``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba49db0e9531388bf92d5d5743a439d407a597fecfee636aff73109074d464df)
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
            type_hints = typing.get_type_hints(_typecheckingstub__af4d8dac07097a7489a69d540cf211f80709f24334836f2a8ee6e6665c7b3df6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba3f75f11fc41ab850ca9a38a25c7f6baf66e56889032402dfa14f286849cda5)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnApplicationMixinProps:
        return typing.cast(CfnApplicationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emrserverless.mixins.CfnApplicationPropsMixin.AutoStartConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled"},
    )
    class AutoStartConfigurationProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The configuration for an application to automatically start on job submission.

            :param enabled: Enables the application to automatically start on job submission. Default: - true

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-autostartconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emrserverless import mixins as emrserverless_mixins
                
                auto_start_configuration_property = emrserverless_mixins.CfnApplicationPropsMixin.AutoStartConfigurationProperty(
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__afee23267facef6f3f0c56579c2d518117826e719e15fe841e3e00e28562d84b)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Enables the application to automatically start on job submission.

            :default: - true

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-autostartconfiguration.html#cfn-emrserverless-application-autostartconfiguration-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AutoStartConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emrserverless.mixins.CfnApplicationPropsMixin.AutoStopConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "idle_timeout_minutes": "idleTimeoutMinutes",
        },
    )
    class AutoStopConfigurationProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            idle_timeout_minutes: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The configuration for an application to automatically stop after a certain amount of time being idle.

            :param enabled: Enables the application to automatically stop after a certain amount of time being idle. Defaults to true. Default: - true
            :param idle_timeout_minutes: The amount of idle time in minutes after which your application will automatically stop. Defaults to 15 minutes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-autostopconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emrserverless import mixins as emrserverless_mixins
                
                auto_stop_configuration_property = emrserverless_mixins.CfnApplicationPropsMixin.AutoStopConfigurationProperty(
                    enabled=False,
                    idle_timeout_minutes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d24c5fb6ac38bfbbd5553244c3d38f51183c4a90f7b87a50bdf34ae7294aab09)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument idle_timeout_minutes", value=idle_timeout_minutes, expected_type=type_hints["idle_timeout_minutes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if idle_timeout_minutes is not None:
                self._values["idle_timeout_minutes"] = idle_timeout_minutes

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Enables the application to automatically stop after a certain amount of time being idle.

            Defaults to true.

            :default: - true

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-autostopconfiguration.html#cfn-emrserverless-application-autostopconfiguration-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def idle_timeout_minutes(self) -> typing.Optional[jsii.Number]:
            '''The amount of idle time in minutes after which your application will automatically stop.

            Defaults to 15 minutes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-autostopconfiguration.html#cfn-emrserverless-application-autostopconfiguration-idletimeoutminutes
            '''
            result = self._values.get("idle_timeout_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AutoStopConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emrserverless.mixins.CfnApplicationPropsMixin.CloudWatchLoggingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "encryption_key_arn": "encryptionKeyArn",
            "log_group_name": "logGroupName",
            "log_stream_name_prefix": "logStreamNamePrefix",
            "log_type_map": "logTypeMap",
        },
    )
    class CloudWatchLoggingConfigurationProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            encryption_key_arn: typing.Optional[builtins.str] = None,
            log_group_name: typing.Optional[builtins.str] = None,
            log_stream_name_prefix: typing.Optional[builtins.str] = None,
            log_type_map: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.LogTypeMapKeyValuePairProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The Amazon CloudWatch configuration for monitoring logs.

            You can configure your jobs to send log information to CloudWatch.

            :param enabled: Enables CloudWatch logging. Default: - false
            :param encryption_key_arn: The AWS Key Management Service (KMS) key ARN to encrypt the logs that you store in CloudWatch Logs.
            :param log_group_name: The name of the log group in Amazon CloudWatch Logs where you want to publish your logs.
            :param log_stream_name_prefix: Prefix for the CloudWatch log stream name.
            :param log_type_map: The specific log-streams which need to be uploaded to CloudWatch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-cloudwatchloggingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emrserverless import mixins as emrserverless_mixins
                
                cloud_watch_logging_configuration_property = emrserverless_mixins.CfnApplicationPropsMixin.CloudWatchLoggingConfigurationProperty(
                    enabled=False,
                    encryption_key_arn="encryptionKeyArn",
                    log_group_name="logGroupName",
                    log_stream_name_prefix="logStreamNamePrefix",
                    log_type_map=[emrserverless_mixins.CfnApplicationPropsMixin.LogTypeMapKeyValuePairProperty(
                        key="key",
                        value=["value"]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dd9be9f889b20d62cb99f53b7773f86bdfcbc9c055488fbc7263e9ae4f43be44)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument encryption_key_arn", value=encryption_key_arn, expected_type=type_hints["encryption_key_arn"])
                check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
                check_type(argname="argument log_stream_name_prefix", value=log_stream_name_prefix, expected_type=type_hints["log_stream_name_prefix"])
                check_type(argname="argument log_type_map", value=log_type_map, expected_type=type_hints["log_type_map"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if encryption_key_arn is not None:
                self._values["encryption_key_arn"] = encryption_key_arn
            if log_group_name is not None:
                self._values["log_group_name"] = log_group_name
            if log_stream_name_prefix is not None:
                self._values["log_stream_name_prefix"] = log_stream_name_prefix
            if log_type_map is not None:
                self._values["log_type_map"] = log_type_map

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Enables CloudWatch logging.

            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-cloudwatchloggingconfiguration.html#cfn-emrserverless-application-cloudwatchloggingconfiguration-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def encryption_key_arn(self) -> typing.Optional[builtins.str]:
            '''The AWS Key Management Service (KMS) key ARN to encrypt the logs that you store in CloudWatch Logs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-cloudwatchloggingconfiguration.html#cfn-emrserverless-application-cloudwatchloggingconfiguration-encryptionkeyarn
            '''
            result = self._values.get("encryption_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_group_name(self) -> typing.Optional[builtins.str]:
            '''The name of the log group in Amazon CloudWatch Logs where you want to publish your logs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-cloudwatchloggingconfiguration.html#cfn-emrserverless-application-cloudwatchloggingconfiguration-loggroupname
            '''
            result = self._values.get("log_group_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_stream_name_prefix(self) -> typing.Optional[builtins.str]:
            '''Prefix for the CloudWatch log stream name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-cloudwatchloggingconfiguration.html#cfn-emrserverless-application-cloudwatchloggingconfiguration-logstreamnameprefix
            '''
            result = self._values.get("log_stream_name_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_type_map(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.LogTypeMapKeyValuePairProperty"]]]]:
            '''The specific log-streams which need to be uploaded to CloudWatch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-cloudwatchloggingconfiguration.html#cfn-emrserverless-application-cloudwatchloggingconfiguration-logtypemap
            '''
            result = self._values.get("log_type_map")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.LogTypeMapKeyValuePairProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchLoggingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emrserverless.mixins.CfnApplicationPropsMixin.ConfigurationObjectProperty",
        jsii_struct_bases=[],
        name_mapping={
            "classification": "classification",
            "configurations": "configurations",
            "properties": "properties",
        },
    )
    class ConfigurationObjectProperty:
        def __init__(
            self,
            *,
            classification: typing.Optional[builtins.str] = None,
            configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.ConfigurationObjectProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            properties: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''A configuration specification to be used when provisioning an application.

            A configuration consists of a classification, properties, and optional nested configurations. A classification refers to an application-specific configuration file. Properties are the settings you want to change in that file.

            :param classification: The classification within a configuration.
            :param configurations: A list of additional configurations to apply within a configuration object.
            :param properties: A set of properties specified within a configuration classification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-configurationobject.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emrserverless import mixins as emrserverless_mixins
                
                # configuration_object_property_: emrserverless_mixins.CfnApplicationPropsMixin.ConfigurationObjectProperty
                
                configuration_object_property = emrserverless_mixins.CfnApplicationPropsMixin.ConfigurationObjectProperty(
                    classification="classification",
                    configurations=[configuration_object_property_],
                    properties={
                        "properties_key": "properties"
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8e75b6815f4ca03c8aceb5b9406ebb99110019f424a3d677ab097abec61f98a7)
                check_type(argname="argument classification", value=classification, expected_type=type_hints["classification"])
                check_type(argname="argument configurations", value=configurations, expected_type=type_hints["configurations"])
                check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if classification is not None:
                self._values["classification"] = classification
            if configurations is not None:
                self._values["configurations"] = configurations
            if properties is not None:
                self._values["properties"] = properties

        @builtins.property
        def classification(self) -> typing.Optional[builtins.str]:
            '''The classification within a configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-configurationobject.html#cfn-emrserverless-application-configurationobject-classification
            '''
            result = self._values.get("classification")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def configurations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ConfigurationObjectProperty"]]]]:
            '''A list of additional configurations to apply within a configuration object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-configurationobject.html#cfn-emrserverless-application-configurationobject-configurations
            '''
            result = self._values.get("configurations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ConfigurationObjectProperty"]]]], result)

        @builtins.property
        def properties(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''A set of properties specified within a configuration classification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-configurationobject.html#cfn-emrserverless-application-configurationobject-properties
            '''
            result = self._values.get("properties")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfigurationObjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emrserverless.mixins.CfnApplicationPropsMixin.IdentityCenterConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"identity_center_instance_arn": "identityCenterInstanceArn"},
    )
    class IdentityCenterConfigurationProperty:
        def __init__(
            self,
            *,
            identity_center_instance_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The IAM Identity Center Configuration accepts the Identity Center instance parameter required to enable trusted identity propagation.

            This configuration allows identity propagation between integrated services and the Identity Center instance.

            :param identity_center_instance_arn: The ARN of the IAM Identity Center instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-identitycenterconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emrserverless import mixins as emrserverless_mixins
                
                identity_center_configuration_property = emrserverless_mixins.CfnApplicationPropsMixin.IdentityCenterConfigurationProperty(
                    identity_center_instance_arn="identityCenterInstanceArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__45610a6bae6cbe51fdff45e10174886af5dca4df8eb5ddbe40b5caa6771c6d22)
                check_type(argname="argument identity_center_instance_arn", value=identity_center_instance_arn, expected_type=type_hints["identity_center_instance_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if identity_center_instance_arn is not None:
                self._values["identity_center_instance_arn"] = identity_center_instance_arn

        @builtins.property
        def identity_center_instance_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the IAM Identity Center instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-identitycenterconfiguration.html#cfn-emrserverless-application-identitycenterconfiguration-identitycenterinstancearn
            '''
            result = self._values.get("identity_center_instance_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IdentityCenterConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emrserverless.mixins.CfnApplicationPropsMixin.ImageConfigurationInputProperty",
        jsii_struct_bases=[],
        name_mapping={"image_uri": "imageUri"},
    )
    class ImageConfigurationInputProperty:
        def __init__(self, *, image_uri: typing.Optional[builtins.str] = None) -> None:
            '''The image configuration.

            :param image_uri: The URI of an image in the Amazon ECR registry. This field is required when you create a new application. If you leave this field blank in an update, Amazon EMR will remove the image configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-imageconfigurationinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emrserverless import mixins as emrserverless_mixins
                
                image_configuration_input_property = emrserverless_mixins.CfnApplicationPropsMixin.ImageConfigurationInputProperty(
                    image_uri="imageUri"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bcf4ae1349c80a9668c062b817c4eb1f0692c9787af20a24d8316d565439f0f4)
                check_type(argname="argument image_uri", value=image_uri, expected_type=type_hints["image_uri"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if image_uri is not None:
                self._values["image_uri"] = image_uri

        @builtins.property
        def image_uri(self) -> typing.Optional[builtins.str]:
            '''The URI of an image in the Amazon ECR registry.

            This field is required when you create a new application. If you leave this field blank in an update, Amazon EMR will remove the image configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-imageconfigurationinput.html#cfn-emrserverless-application-imageconfigurationinput-imageuri
            '''
            result = self._values.get("image_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ImageConfigurationInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emrserverless.mixins.CfnApplicationPropsMixin.InitialCapacityConfigKeyValuePairProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class InitialCapacityConfigKeyValuePairProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.InitialCapacityConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param key: Worker type for an analytics framework.
            :param value: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-initialcapacityconfigkeyvaluepair.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emrserverless import mixins as emrserverless_mixins
                
                initial_capacity_config_key_value_pair_property = emrserverless_mixins.CfnApplicationPropsMixin.InitialCapacityConfigKeyValuePairProperty(
                    key="key",
                    value=emrserverless_mixins.CfnApplicationPropsMixin.InitialCapacityConfigProperty(
                        worker_configuration=emrserverless_mixins.CfnApplicationPropsMixin.WorkerConfigurationProperty(
                            cpu="cpu",
                            disk="disk",
                            disk_type="diskType",
                            memory="memory"
                        ),
                        worker_count=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2dd701b1c04e09e513bdb8848606ca691c2892468c6a9d2c41a49b631baff9f2)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''Worker type for an analytics framework.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-initialcapacityconfigkeyvaluepair.html#cfn-emrserverless-application-initialcapacityconfigkeyvaluepair-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.InitialCapacityConfigProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-initialcapacityconfigkeyvaluepair.html#cfn-emrserverless-application-initialcapacityconfigkeyvaluepair-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.InitialCapacityConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InitialCapacityConfigKeyValuePairProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emrserverless.mixins.CfnApplicationPropsMixin.InitialCapacityConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "worker_configuration": "workerConfiguration",
            "worker_count": "workerCount",
        },
    )
    class InitialCapacityConfigProperty:
        def __init__(
            self,
            *,
            worker_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.WorkerConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            worker_count: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The initial capacity configuration per worker.

            :param worker_configuration: The resource configuration of the initial capacity configuration.
            :param worker_count: The number of workers in the initial capacity configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-initialcapacityconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emrserverless import mixins as emrserverless_mixins
                
                initial_capacity_config_property = emrserverless_mixins.CfnApplicationPropsMixin.InitialCapacityConfigProperty(
                    worker_configuration=emrserverless_mixins.CfnApplicationPropsMixin.WorkerConfigurationProperty(
                        cpu="cpu",
                        disk="disk",
                        disk_type="diskType",
                        memory="memory"
                    ),
                    worker_count=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__aa2b6eba62777a70496202b936fd555ea245017f762c66f3599f37d89a1dc84a)
                check_type(argname="argument worker_configuration", value=worker_configuration, expected_type=type_hints["worker_configuration"])
                check_type(argname="argument worker_count", value=worker_count, expected_type=type_hints["worker_count"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if worker_configuration is not None:
                self._values["worker_configuration"] = worker_configuration
            if worker_count is not None:
                self._values["worker_count"] = worker_count

        @builtins.property
        def worker_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.WorkerConfigurationProperty"]]:
            '''The resource configuration of the initial capacity configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-initialcapacityconfig.html#cfn-emrserverless-application-initialcapacityconfig-workerconfiguration
            '''
            result = self._values.get("worker_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.WorkerConfigurationProperty"]], result)

        @builtins.property
        def worker_count(self) -> typing.Optional[jsii.Number]:
            '''The number of workers in the initial capacity configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-initialcapacityconfig.html#cfn-emrserverless-application-initialcapacityconfig-workercount
            '''
            result = self._values.get("worker_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InitialCapacityConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emrserverless.mixins.CfnApplicationPropsMixin.InteractiveConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "livy_endpoint_enabled": "livyEndpointEnabled",
            "studio_enabled": "studioEnabled",
        },
    )
    class InteractiveConfigurationProperty:
        def __init__(
            self,
            *,
            livy_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            studio_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The configuration to use to enable the different types of interactive use cases in an application.

            :param livy_endpoint_enabled: Enables an Apache Livy endpoint that you can connect to and run interactive jobs. Default: - false
            :param studio_enabled: Enables you to connect an application to Amazon EMR Studio to run interactive workloads in a notebook. Default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-interactiveconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emrserverless import mixins as emrserverless_mixins
                
                interactive_configuration_property = emrserverless_mixins.CfnApplicationPropsMixin.InteractiveConfigurationProperty(
                    livy_endpoint_enabled=False,
                    studio_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f2cd8d5b0592c821e33c86d5de2acce8e3cbfe45ef574451771f4cc61013f039)
                check_type(argname="argument livy_endpoint_enabled", value=livy_endpoint_enabled, expected_type=type_hints["livy_endpoint_enabled"])
                check_type(argname="argument studio_enabled", value=studio_enabled, expected_type=type_hints["studio_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if livy_endpoint_enabled is not None:
                self._values["livy_endpoint_enabled"] = livy_endpoint_enabled
            if studio_enabled is not None:
                self._values["studio_enabled"] = studio_enabled

        @builtins.property
        def livy_endpoint_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Enables an Apache Livy endpoint that you can connect to and run interactive jobs.

            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-interactiveconfiguration.html#cfn-emrserverless-application-interactiveconfiguration-livyendpointenabled
            '''
            result = self._values.get("livy_endpoint_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def studio_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Enables you to connect an application to Amazon EMR Studio to run interactive workloads in a notebook.

            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-interactiveconfiguration.html#cfn-emrserverless-application-interactiveconfiguration-studioenabled
            '''
            result = self._values.get("studio_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InteractiveConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emrserverless.mixins.CfnApplicationPropsMixin.LogTypeMapKeyValuePairProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class LogTypeMapKeyValuePairProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''
            :param key: 
            :param value: List of Applicable values: [STDOUT, STDERR, HIVE_LOG, TEZ_AM, SYSTEM_LOGS].

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-logtypemapkeyvaluepair.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emrserverless import mixins as emrserverless_mixins
                
                log_type_map_key_value_pair_property = emrserverless_mixins.CfnApplicationPropsMixin.LogTypeMapKeyValuePairProperty(
                    key="key",
                    value=["value"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c0b3130bb0699add1d2a589577d32d3fd5cc77de472bbdbf6b20c06c2b6d5db6)
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
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-logtypemapkeyvaluepair.html#cfn-emrserverless-application-logtypemapkeyvaluepair-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[typing.List[builtins.str]]:
            '''List of Applicable values: [STDOUT, STDERR, HIVE_LOG, TEZ_AM, SYSTEM_LOGS].

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-logtypemapkeyvaluepair.html#cfn-emrserverless-application-logtypemapkeyvaluepair-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogTypeMapKeyValuePairProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emrserverless.mixins.CfnApplicationPropsMixin.ManagedPersistenceMonitoringConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled", "encryption_key_arn": "encryptionKeyArn"},
    )
    class ManagedPersistenceMonitoringConfigurationProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            encryption_key_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The managed log persistence configuration for a job run.

            :param enabled: Enables managed logging and defaults to true. If set to false, managed logging will be turned off. Default: - true
            :param encryption_key_arn: The KMS key ARN to encrypt the logs stored in managed log persistence.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-managedpersistencemonitoringconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emrserverless import mixins as emrserverless_mixins
                
                managed_persistence_monitoring_configuration_property = emrserverless_mixins.CfnApplicationPropsMixin.ManagedPersistenceMonitoringConfigurationProperty(
                    enabled=False,
                    encryption_key_arn="encryptionKeyArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7e099f65b76866097a766a336e7717353ce820f002bc0cc3da10fe376f9dd5f6)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument encryption_key_arn", value=encryption_key_arn, expected_type=type_hints["encryption_key_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if encryption_key_arn is not None:
                self._values["encryption_key_arn"] = encryption_key_arn

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Enables managed logging and defaults to true.

            If set to false, managed logging will be turned off.

            :default: - true

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-managedpersistencemonitoringconfiguration.html#cfn-emrserverless-application-managedpersistencemonitoringconfiguration-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def encryption_key_arn(self) -> typing.Optional[builtins.str]:
            '''The KMS key ARN to encrypt the logs stored in managed log persistence.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-managedpersistencemonitoringconfiguration.html#cfn-emrserverless-application-managedpersistencemonitoringconfiguration-encryptionkeyarn
            '''
            result = self._values.get("encryption_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ManagedPersistenceMonitoringConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emrserverless.mixins.CfnApplicationPropsMixin.MaximumAllowedResourcesProperty",
        jsii_struct_bases=[],
        name_mapping={"cpu": "cpu", "disk": "disk", "memory": "memory"},
    )
    class MaximumAllowedResourcesProperty:
        def __init__(
            self,
            *,
            cpu: typing.Optional[builtins.str] = None,
            disk: typing.Optional[builtins.str] = None,
            memory: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The maximum allowed cumulative resources for an application.

            No new resources will be created once the limit is hit.

            :param cpu: The maximum allowed CPU for an application.
            :param disk: The maximum allowed disk for an application.
            :param memory: The maximum allowed resources for an application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-maximumallowedresources.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emrserverless import mixins as emrserverless_mixins
                
                maximum_allowed_resources_property = emrserverless_mixins.CfnApplicationPropsMixin.MaximumAllowedResourcesProperty(
                    cpu="cpu",
                    disk="disk",
                    memory="memory"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9d20903a5b07c069d97ff3ea55d83a43dd1c03c1321be285cb4e00b52523316a)
                check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
                check_type(argname="argument disk", value=disk, expected_type=type_hints["disk"])
                check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cpu is not None:
                self._values["cpu"] = cpu
            if disk is not None:
                self._values["disk"] = disk
            if memory is not None:
                self._values["memory"] = memory

        @builtins.property
        def cpu(self) -> typing.Optional[builtins.str]:
            '''The maximum allowed CPU for an application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-maximumallowedresources.html#cfn-emrserverless-application-maximumallowedresources-cpu
            '''
            result = self._values.get("cpu")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def disk(self) -> typing.Optional[builtins.str]:
            '''The maximum allowed disk for an application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-maximumallowedresources.html#cfn-emrserverless-application-maximumallowedresources-disk
            '''
            result = self._values.get("disk")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def memory(self) -> typing.Optional[builtins.str]:
            '''The maximum allowed resources for an application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-maximumallowedresources.html#cfn-emrserverless-application-maximumallowedresources-memory
            '''
            result = self._values.get("memory")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MaximumAllowedResourcesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emrserverless.mixins.CfnApplicationPropsMixin.MonitoringConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cloud_watch_logging_configuration": "cloudWatchLoggingConfiguration",
            "managed_persistence_monitoring_configuration": "managedPersistenceMonitoringConfiguration",
            "prometheus_monitoring_configuration": "prometheusMonitoringConfiguration",
            "s3_monitoring_configuration": "s3MonitoringConfiguration",
        },
    )
    class MonitoringConfigurationProperty:
        def __init__(
            self,
            *,
            cloud_watch_logging_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.CloudWatchLoggingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            managed_persistence_monitoring_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.ManagedPersistenceMonitoringConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            prometheus_monitoring_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.PrometheusMonitoringConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3_monitoring_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.S3MonitoringConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The configuration setting for monitoring logs.

            :param cloud_watch_logging_configuration: The Amazon CloudWatch configuration for monitoring logs. You can configure your jobs to send log information to CloudWatch.
            :param managed_persistence_monitoring_configuration: The managed log persistence configuration for a job run.
            :param prometheus_monitoring_configuration: The monitoring configuration object you can configure to send metrics to Amazon Managed Service for Prometheus for a job run.
            :param s3_monitoring_configuration: The Amazon S3 configuration for monitoring log publishing.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-monitoringconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emrserverless import mixins as emrserverless_mixins
                
                monitoring_configuration_property = emrserverless_mixins.CfnApplicationPropsMixin.MonitoringConfigurationProperty(
                    cloud_watch_logging_configuration=emrserverless_mixins.CfnApplicationPropsMixin.CloudWatchLoggingConfigurationProperty(
                        enabled=False,
                        encryption_key_arn="encryptionKeyArn",
                        log_group_name="logGroupName",
                        log_stream_name_prefix="logStreamNamePrefix",
                        log_type_map=[emrserverless_mixins.CfnApplicationPropsMixin.LogTypeMapKeyValuePairProperty(
                            key="key",
                            value=["value"]
                        )]
                    ),
                    managed_persistence_monitoring_configuration=emrserverless_mixins.CfnApplicationPropsMixin.ManagedPersistenceMonitoringConfigurationProperty(
                        enabled=False,
                        encryption_key_arn="encryptionKeyArn"
                    ),
                    prometheus_monitoring_configuration=emrserverless_mixins.CfnApplicationPropsMixin.PrometheusMonitoringConfigurationProperty(
                        remote_write_url="remoteWriteUrl"
                    ),
                    s3_monitoring_configuration=emrserverless_mixins.CfnApplicationPropsMixin.S3MonitoringConfigurationProperty(
                        encryption_key_arn="encryptionKeyArn",
                        log_uri="logUri"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__47a8171bf03132575f4ee0f2e5b32d42c9e357122e358e053b179812dba7ee1b)
                check_type(argname="argument cloud_watch_logging_configuration", value=cloud_watch_logging_configuration, expected_type=type_hints["cloud_watch_logging_configuration"])
                check_type(argname="argument managed_persistence_monitoring_configuration", value=managed_persistence_monitoring_configuration, expected_type=type_hints["managed_persistence_monitoring_configuration"])
                check_type(argname="argument prometheus_monitoring_configuration", value=prometheus_monitoring_configuration, expected_type=type_hints["prometheus_monitoring_configuration"])
                check_type(argname="argument s3_monitoring_configuration", value=s3_monitoring_configuration, expected_type=type_hints["s3_monitoring_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloud_watch_logging_configuration is not None:
                self._values["cloud_watch_logging_configuration"] = cloud_watch_logging_configuration
            if managed_persistence_monitoring_configuration is not None:
                self._values["managed_persistence_monitoring_configuration"] = managed_persistence_monitoring_configuration
            if prometheus_monitoring_configuration is not None:
                self._values["prometheus_monitoring_configuration"] = prometheus_monitoring_configuration
            if s3_monitoring_configuration is not None:
                self._values["s3_monitoring_configuration"] = s3_monitoring_configuration

        @builtins.property
        def cloud_watch_logging_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.CloudWatchLoggingConfigurationProperty"]]:
            '''The Amazon CloudWatch configuration for monitoring logs.

            You can configure your jobs to send log information to CloudWatch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-monitoringconfiguration.html#cfn-emrserverless-application-monitoringconfiguration-cloudwatchloggingconfiguration
            '''
            result = self._values.get("cloud_watch_logging_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.CloudWatchLoggingConfigurationProperty"]], result)

        @builtins.property
        def managed_persistence_monitoring_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ManagedPersistenceMonitoringConfigurationProperty"]]:
            '''The managed log persistence configuration for a job run.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-monitoringconfiguration.html#cfn-emrserverless-application-monitoringconfiguration-managedpersistencemonitoringconfiguration
            '''
            result = self._values.get("managed_persistence_monitoring_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ManagedPersistenceMonitoringConfigurationProperty"]], result)

        @builtins.property
        def prometheus_monitoring_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.PrometheusMonitoringConfigurationProperty"]]:
            '''The monitoring configuration object you can configure to send metrics to Amazon Managed Service for Prometheus for a job run.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-monitoringconfiguration.html#cfn-emrserverless-application-monitoringconfiguration-prometheusmonitoringconfiguration
            '''
            result = self._values.get("prometheus_monitoring_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.PrometheusMonitoringConfigurationProperty"]], result)

        @builtins.property
        def s3_monitoring_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.S3MonitoringConfigurationProperty"]]:
            '''The Amazon S3 configuration for monitoring log publishing.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-monitoringconfiguration.html#cfn-emrserverless-application-monitoringconfiguration-s3monitoringconfiguration
            '''
            result = self._values.get("s3_monitoring_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.S3MonitoringConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MonitoringConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emrserverless.mixins.CfnApplicationPropsMixin.NetworkConfigurationProperty",
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
            '''The network configuration for customer VPC connectivity.

            :param security_group_ids: The array of security group Ids for customer VPC connectivity.
            :param subnet_ids: The array of subnet Ids for customer VPC connectivity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-networkconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emrserverless import mixins as emrserverless_mixins
                
                network_configuration_property = emrserverless_mixins.CfnApplicationPropsMixin.NetworkConfigurationProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__355f42a883935ade27ad6f0a600f4f8db071f6ca4e2077123aa7b6d99e4bb781)
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
                check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnet_ids is not None:
                self._values["subnet_ids"] = subnet_ids

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The array of security group Ids for customer VPC connectivity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-networkconfiguration.html#cfn-emrserverless-application-networkconfiguration-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The array of subnet Ids for customer VPC connectivity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-networkconfiguration.html#cfn-emrserverless-application-networkconfiguration-subnetids
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

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emrserverless.mixins.CfnApplicationPropsMixin.PrometheusMonitoringConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"remote_write_url": "remoteWriteUrl"},
    )
    class PrometheusMonitoringConfigurationProperty:
        def __init__(
            self,
            *,
            remote_write_url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The monitoring configuration object you can configure to send metrics to Amazon Managed Service for Prometheus for a job run.

            :param remote_write_url: The remote write URL in the Amazon Managed Service for Prometheus workspace to send metrics to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-prometheusmonitoringconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emrserverless import mixins as emrserverless_mixins
                
                prometheus_monitoring_configuration_property = emrserverless_mixins.CfnApplicationPropsMixin.PrometheusMonitoringConfigurationProperty(
                    remote_write_url="remoteWriteUrl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__358afe9e87a8cc619b0fb4550a5e1ca01d06dcb6e076a0886464879fa2e14b42)
                check_type(argname="argument remote_write_url", value=remote_write_url, expected_type=type_hints["remote_write_url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if remote_write_url is not None:
                self._values["remote_write_url"] = remote_write_url

        @builtins.property
        def remote_write_url(self) -> typing.Optional[builtins.str]:
            '''The remote write URL in the Amazon Managed Service for Prometheus workspace to send metrics to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-prometheusmonitoringconfiguration.html#cfn-emrserverless-application-prometheusmonitoringconfiguration-remotewriteurl
            '''
            result = self._values.get("remote_write_url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PrometheusMonitoringConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emrserverless.mixins.CfnApplicationPropsMixin.S3MonitoringConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"encryption_key_arn": "encryptionKeyArn", "log_uri": "logUri"},
    )
    class S3MonitoringConfigurationProperty:
        def __init__(
            self,
            *,
            encryption_key_arn: typing.Optional[builtins.str] = None,
            log_uri: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The Amazon S3 configuration for monitoring log publishing.

            You can configure your jobs to send log information to Amazon S3.

            :param encryption_key_arn: The KMS key ARN to encrypt the logs published to the given Amazon S3 destination.
            :param log_uri: The Amazon S3 destination URI for log publishing.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-s3monitoringconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emrserverless import mixins as emrserverless_mixins
                
                s3_monitoring_configuration_property = emrserverless_mixins.CfnApplicationPropsMixin.S3MonitoringConfigurationProperty(
                    encryption_key_arn="encryptionKeyArn",
                    log_uri="logUri"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9be3ffb1e5c5d88717bd6d19e11ba0a73196b7fc8b10123d71e469a56f7a3c1d)
                check_type(argname="argument encryption_key_arn", value=encryption_key_arn, expected_type=type_hints["encryption_key_arn"])
                check_type(argname="argument log_uri", value=log_uri, expected_type=type_hints["log_uri"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encryption_key_arn is not None:
                self._values["encryption_key_arn"] = encryption_key_arn
            if log_uri is not None:
                self._values["log_uri"] = log_uri

        @builtins.property
        def encryption_key_arn(self) -> typing.Optional[builtins.str]:
            '''The KMS key ARN to encrypt the logs published to the given Amazon S3 destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-s3monitoringconfiguration.html#cfn-emrserverless-application-s3monitoringconfiguration-encryptionkeyarn
            '''
            result = self._values.get("encryption_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_uri(self) -> typing.Optional[builtins.str]:
            '''The Amazon S3 destination URI for log publishing.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-s3monitoringconfiguration.html#cfn-emrserverless-application-s3monitoringconfiguration-loguri
            '''
            result = self._values.get("log_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3MonitoringConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emrserverless.mixins.CfnApplicationPropsMixin.SchedulerConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "max_concurrent_runs": "maxConcurrentRuns",
            "queue_timeout_minutes": "queueTimeoutMinutes",
        },
    )
    class SchedulerConfigurationProperty:
        def __init__(
            self,
            *,
            max_concurrent_runs: typing.Optional[jsii.Number] = None,
            queue_timeout_minutes: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The scheduler configuration for batch and streaming jobs running on this application.

            Supported with release labels emr-7.0.0 and above.

            :param max_concurrent_runs: The maximum concurrent job runs on this application. If scheduler configuration is enabled on your application, the default value is 15. The valid range is 1 to 1000.
            :param queue_timeout_minutes: The maximum duration in minutes for the job in QUEUED state. If scheduler configuration is enabled on your application, the default value is 360 minutes (6 hours). The valid range is from 15 to 720.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-schedulerconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emrserverless import mixins as emrserverless_mixins
                
                scheduler_configuration_property = emrserverless_mixins.CfnApplicationPropsMixin.SchedulerConfigurationProperty(
                    max_concurrent_runs=123,
                    queue_timeout_minutes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2d622570854453c66095d7f74603185ba580f6fa26c9e0c865610cd2d4cdf259)
                check_type(argname="argument max_concurrent_runs", value=max_concurrent_runs, expected_type=type_hints["max_concurrent_runs"])
                check_type(argname="argument queue_timeout_minutes", value=queue_timeout_minutes, expected_type=type_hints["queue_timeout_minutes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_concurrent_runs is not None:
                self._values["max_concurrent_runs"] = max_concurrent_runs
            if queue_timeout_minutes is not None:
                self._values["queue_timeout_minutes"] = queue_timeout_minutes

        @builtins.property
        def max_concurrent_runs(self) -> typing.Optional[jsii.Number]:
            '''The maximum concurrent job runs on this application.

            If scheduler configuration is enabled on your application, the default value is 15. The valid range is 1 to 1000.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-schedulerconfiguration.html#cfn-emrserverless-application-schedulerconfiguration-maxconcurrentruns
            '''
            result = self._values.get("max_concurrent_runs")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def queue_timeout_minutes(self) -> typing.Optional[jsii.Number]:
            '''The maximum duration in minutes for the job in QUEUED state.

            If scheduler configuration is enabled on your application, the default value is 360 minutes (6 hours). The valid range is from 15 to 720.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-schedulerconfiguration.html#cfn-emrserverless-application-schedulerconfiguration-queuetimeoutminutes
            '''
            result = self._values.get("queue_timeout_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SchedulerConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emrserverless.mixins.CfnApplicationPropsMixin.WorkerConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cpu": "cpu",
            "disk": "disk",
            "disk_type": "diskType",
            "memory": "memory",
        },
    )
    class WorkerConfigurationProperty:
        def __init__(
            self,
            *,
            cpu: typing.Optional[builtins.str] = None,
            disk: typing.Optional[builtins.str] = None,
            disk_type: typing.Optional[builtins.str] = None,
            memory: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration of a worker.

            For more information, see `Supported worker configurations <https://docs.aws.amazon.com/emr/latest/EMR-Serverless-UserGuide/app-behavior.html#worker-configs>`_ .

            :param cpu: The CPU requirements of the worker configuration. Each worker can have 1, 2, 4, 8, or 16 vCPUs.
            :param disk: The disk requirements of the worker configuration.
            :param disk_type: The disk type for every worker instance of the work type. Shuffle optimized disks have higher performance characteristics and are better for shuffle heavy workloads. Default is ``STANDARD`` .
            :param memory: The memory requirements of the worker configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-workerconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emrserverless import mixins as emrserverless_mixins
                
                worker_configuration_property = emrserverless_mixins.CfnApplicationPropsMixin.WorkerConfigurationProperty(
                    cpu="cpu",
                    disk="disk",
                    disk_type="diskType",
                    memory="memory"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__47eea65eeafbaceb3e21c9e5db3dcf06f102a29901e6a21cdb12d13a33d573bc)
                check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
                check_type(argname="argument disk", value=disk, expected_type=type_hints["disk"])
                check_type(argname="argument disk_type", value=disk_type, expected_type=type_hints["disk_type"])
                check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cpu is not None:
                self._values["cpu"] = cpu
            if disk is not None:
                self._values["disk"] = disk
            if disk_type is not None:
                self._values["disk_type"] = disk_type
            if memory is not None:
                self._values["memory"] = memory

        @builtins.property
        def cpu(self) -> typing.Optional[builtins.str]:
            '''The CPU requirements of the worker configuration.

            Each worker can have 1, 2, 4, 8, or 16 vCPUs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-workerconfiguration.html#cfn-emrserverless-application-workerconfiguration-cpu
            '''
            result = self._values.get("cpu")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def disk(self) -> typing.Optional[builtins.str]:
            '''The disk requirements of the worker configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-workerconfiguration.html#cfn-emrserverless-application-workerconfiguration-disk
            '''
            result = self._values.get("disk")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def disk_type(self) -> typing.Optional[builtins.str]:
            '''The disk type for every worker instance of the work type.

            Shuffle optimized disks have higher performance characteristics and are better for shuffle heavy workloads. Default is ``STANDARD`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-workerconfiguration.html#cfn-emrserverless-application-workerconfiguration-disktype
            '''
            result = self._values.get("disk_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def memory(self) -> typing.Optional[builtins.str]:
            '''The memory requirements of the worker configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-workerconfiguration.html#cfn-emrserverless-application-workerconfiguration-memory
            '''
            result = self._values.get("memory")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WorkerConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emrserverless.mixins.CfnApplicationPropsMixin.WorkerTypeSpecificationInputProperty",
        jsii_struct_bases=[],
        name_mapping={"image_configuration": "imageConfiguration"},
    )
    class WorkerTypeSpecificationInputProperty:
        def __init__(
            self,
            *,
            image_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.ImageConfigurationInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The specifications for a worker type.

            :param image_configuration: The image configuration for a worker type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-workertypespecificationinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emrserverless import mixins as emrserverless_mixins
                
                worker_type_specification_input_property = emrserverless_mixins.CfnApplicationPropsMixin.WorkerTypeSpecificationInputProperty(
                    image_configuration=emrserverless_mixins.CfnApplicationPropsMixin.ImageConfigurationInputProperty(
                        image_uri="imageUri"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d3d69c81fb3b0dfec31b7e6a3e6b36337ed2556c735b9b031868a0b0b6bfe91e)
                check_type(argname="argument image_configuration", value=image_configuration, expected_type=type_hints["image_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if image_configuration is not None:
                self._values["image_configuration"] = image_configuration

        @builtins.property
        def image_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ImageConfigurationInputProperty"]]:
            '''The image configuration for a worker type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-workertypespecificationinput.html#cfn-emrserverless-application-workertypespecificationinput-imageconfiguration
            '''
            result = self._values.get("image_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ImageConfigurationInputProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WorkerTypeSpecificationInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnApplicationMixinProps",
    "CfnApplicationPropsMixin",
]

publication.publish()

def _typecheckingstub__c8750ae43bdfa18bedb8e43d4aab1c17f3f33d7428ab897cfe52911e61320a92(
    *,
    architecture: typing.Optional[builtins.str] = None,
    auto_start_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.AutoStartConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    auto_stop_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.AutoStopConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    identity_center_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.IdentityCenterConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    image_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.ImageConfigurationInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    initial_capacity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.InitialCapacityConfigKeyValuePairProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    interactive_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.InteractiveConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    maximum_capacity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.MaximumAllowedResourcesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    monitoring_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.MonitoringConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    network_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.NetworkConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    release_label: typing.Optional[builtins.str] = None,
    runtime_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.ConfigurationObjectProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    scheduler_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.SchedulerConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
    worker_type_specifications: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.WorkerTypeSpecificationInputProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba49db0e9531388bf92d5d5743a439d407a597fecfee636aff73109074d464df(
    props: typing.Union[CfnApplicationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af4d8dac07097a7489a69d540cf211f80709f24334836f2a8ee6e6665c7b3df6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba3f75f11fc41ab850ca9a38a25c7f6baf66e56889032402dfa14f286849cda5(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afee23267facef6f3f0c56579c2d518117826e719e15fe841e3e00e28562d84b(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d24c5fb6ac38bfbbd5553244c3d38f51183c4a90f7b87a50bdf34ae7294aab09(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    idle_timeout_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd9be9f889b20d62cb99f53b7773f86bdfcbc9c055488fbc7263e9ae4f43be44(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    encryption_key_arn: typing.Optional[builtins.str] = None,
    log_group_name: typing.Optional[builtins.str] = None,
    log_stream_name_prefix: typing.Optional[builtins.str] = None,
    log_type_map: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.LogTypeMapKeyValuePairProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e75b6815f4ca03c8aceb5b9406ebb99110019f424a3d677ab097abec61f98a7(
    *,
    classification: typing.Optional[builtins.str] = None,
    configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.ConfigurationObjectProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    properties: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45610a6bae6cbe51fdff45e10174886af5dca4df8eb5ddbe40b5caa6771c6d22(
    *,
    identity_center_instance_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcf4ae1349c80a9668c062b817c4eb1f0692c9787af20a24d8316d565439f0f4(
    *,
    image_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dd701b1c04e09e513bdb8848606ca691c2892468c6a9d2c41a49b631baff9f2(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.InitialCapacityConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa2b6eba62777a70496202b936fd555ea245017f762c66f3599f37d89a1dc84a(
    *,
    worker_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.WorkerConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    worker_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2cd8d5b0592c821e33c86d5de2acce8e3cbfe45ef574451771f4cc61013f039(
    *,
    livy_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    studio_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0b3130bb0699add1d2a589577d32d3fd5cc77de472bbdbf6b20c06c2b6d5db6(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e099f65b76866097a766a336e7717353ce820f002bc0cc3da10fe376f9dd5f6(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    encryption_key_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d20903a5b07c069d97ff3ea55d83a43dd1c03c1321be285cb4e00b52523316a(
    *,
    cpu: typing.Optional[builtins.str] = None,
    disk: typing.Optional[builtins.str] = None,
    memory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47a8171bf03132575f4ee0f2e5b32d42c9e357122e358e053b179812dba7ee1b(
    *,
    cloud_watch_logging_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.CloudWatchLoggingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    managed_persistence_monitoring_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.ManagedPersistenceMonitoringConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    prometheus_monitoring_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.PrometheusMonitoringConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_monitoring_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.S3MonitoringConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__355f42a883935ade27ad6f0a600f4f8db071f6ca4e2077123aa7b6d99e4bb781(
    *,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__358afe9e87a8cc619b0fb4550a5e1ca01d06dcb6e076a0886464879fa2e14b42(
    *,
    remote_write_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9be3ffb1e5c5d88717bd6d19e11ba0a73196b7fc8b10123d71e469a56f7a3c1d(
    *,
    encryption_key_arn: typing.Optional[builtins.str] = None,
    log_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d622570854453c66095d7f74603185ba580f6fa26c9e0c865610cd2d4cdf259(
    *,
    max_concurrent_runs: typing.Optional[jsii.Number] = None,
    queue_timeout_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47eea65eeafbaceb3e21c9e5db3dcf06f102a29901e6a21cdb12d13a33d573bc(
    *,
    cpu: typing.Optional[builtins.str] = None,
    disk: typing.Optional[builtins.str] = None,
    disk_type: typing.Optional[builtins.str] = None,
    memory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3d69c81fb3b0dfec31b7e6a3e6b36337ed2556c735b9b031868a0b0b6bfe91e(
    *,
    image_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.ImageConfigurationInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
