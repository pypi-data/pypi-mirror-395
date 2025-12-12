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
import aws_cdk.aws_events as _aws_cdk_aws_events_ceddda9d
import aws_cdk.interfaces.aws_sagemaker as _aws_cdk_interfaces_aws_sagemaker_ceddda9d


class EndpointConfigEvents(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_sagemaker.events.EndpointConfigEvents",
):
    '''(experimental) EventBridge event patterns for EndpointConfig.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_sagemaker import events as sagemaker_events
        from aws_cdk.interfaces import aws_sagemaker as interfaces_sagemaker
        
        # endpoint_config_ref: interfaces_sagemaker.IEndpointConfigRef
        
        endpoint_config_events = sagemaker_events.EndpointConfigEvents.from_endpoint_config(endpoint_config_ref)
    '''

    @jsii.member(jsii_name="fromEndpointConfig")
    @builtins.classmethod
    def from_endpoint_config(
        cls,
        endpoint_config_ref: _aws_cdk_interfaces_aws_sagemaker_ceddda9d.IEndpointConfigRef,
    ) -> "EndpointConfigEvents":
        '''(experimental) Create EndpointConfigEvents from a EndpointConfig reference.

        :param endpoint_config_ref: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89bc78d1a42c6f2ff82f20a6a7795085c79302c38cfa5dd975930ba03b128982)
            check_type(argname="argument endpoint_config_ref", value=endpoint_config_ref, expected_type=type_hints["endpoint_config_ref"])
        return typing.cast("EndpointConfigEvents", jsii.sinvoke(cls, "fromEndpointConfig", [endpoint_config_ref]))

    @jsii.member(jsii_name="sageMakerEndpointConfigStateChangePattern")
    def sage_maker_endpoint_config_state_change_pattern(
        self,
        *,
        creation_time: typing.Optional[typing.Sequence[builtins.str]] = None,
        endpoint_config_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
        endpoint_config_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        production_variants: typing.Optional[typing.Sequence[typing.Union["EndpointConfigEvents.SageMakerEndpointConfigStateChange.SageMakerEndpointConfigStateChangeItem", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["EndpointConfigEvents.SageMakerEndpointConfigStateChange.Tags", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for EndpointConfig SageMaker Endpoint Config State Change.

        :param creation_time: (experimental) CreationTime property. Specify an array of string values to match this event if the actual value of CreationTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param endpoint_config_arn: (experimental) EndpointConfigArn property. Specify an array of string values to match this event if the actual value of EndpointConfigArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param endpoint_config_name: (experimental) EndpointConfigName property. Specify an array of string values to match this event if the actual value of EndpointConfigName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the EndpointConfig reference
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param production_variants: (experimental) ProductionVariants property. Specify an array of string values to match this event if the actual value of ProductionVariants is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param tags: (experimental) Tags property. Specify an array of string values to match this event if the actual value of Tags is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = EndpointConfigEvents.SageMakerEndpointConfigStateChange.SageMakerEndpointConfigStateChangeProps(
            creation_time=creation_time,
            endpoint_config_arn=endpoint_config_arn,
            endpoint_config_name=endpoint_config_name,
            event_metadata=event_metadata,
            production_variants=production_variants,
            tags=tags,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "sageMakerEndpointConfigStateChangePattern", [options]))

    class SageMakerEndpointConfigStateChange(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_sagemaker.events.EndpointConfigEvents.SageMakerEndpointConfigStateChange",
    ):
        '''(experimental) aws.sagemaker@SageMakerEndpointConfigStateChange event types for EndpointConfig.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_sagemaker import events as sagemaker_events
            
            sage_maker_endpoint_config_state_change = sagemaker_events.EndpointConfigEvents.SageMakerEndpointConfigStateChange()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_sagemaker.events.EndpointConfigEvents.SageMakerEndpointConfigStateChange.SageMakerEndpointConfigStateChangeItem",
            jsii_struct_bases=[],
            name_mapping={
                "initial_instance_count": "initialInstanceCount",
                "initial_variant_weight": "initialVariantWeight",
                "instance_type": "instanceType",
                "model_name": "modelName",
                "variant_name": "variantName",
            },
        )
        class SageMakerEndpointConfigStateChangeItem:
            def __init__(
                self,
                *,
                initial_instance_count: typing.Optional[typing.Sequence[builtins.str]] = None,
                initial_variant_weight: typing.Optional[typing.Sequence[builtins.str]] = None,
                instance_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                model_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                variant_name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for SageMakerEndpointConfigStateChangeItem.

                :param initial_instance_count: (experimental) InitialInstanceCount property. Specify an array of string values to match this event if the actual value of InitialInstanceCount is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param initial_variant_weight: (experimental) InitialVariantWeight property. Specify an array of string values to match this event if the actual value of InitialVariantWeight is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param instance_type: (experimental) InstanceType property. Specify an array of string values to match this event if the actual value of InstanceType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param model_name: (experimental) ModelName property. Specify an array of string values to match this event if the actual value of ModelName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param variant_name: (experimental) VariantName property. Specify an array of string values to match this event if the actual value of VariantName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_sagemaker import events as sagemaker_events
                    
                    sage_maker_endpoint_config_state_change_item = sagemaker_events.EndpointConfigEvents.SageMakerEndpointConfigStateChange.SageMakerEndpointConfigStateChangeItem(
                        initial_instance_count=["initialInstanceCount"],
                        initial_variant_weight=["initialVariantWeight"],
                        instance_type=["instanceType"],
                        model_name=["modelName"],
                        variant_name=["variantName"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__0d60854929854047702e56f68c1eefd8fd7d8498b09f18bffdd3e9fa0565804f)
                    check_type(argname="argument initial_instance_count", value=initial_instance_count, expected_type=type_hints["initial_instance_count"])
                    check_type(argname="argument initial_variant_weight", value=initial_variant_weight, expected_type=type_hints["initial_variant_weight"])
                    check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
                    check_type(argname="argument model_name", value=model_name, expected_type=type_hints["model_name"])
                    check_type(argname="argument variant_name", value=variant_name, expected_type=type_hints["variant_name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if initial_instance_count is not None:
                    self._values["initial_instance_count"] = initial_instance_count
                if initial_variant_weight is not None:
                    self._values["initial_variant_weight"] = initial_variant_weight
                if instance_type is not None:
                    self._values["instance_type"] = instance_type
                if model_name is not None:
                    self._values["model_name"] = model_name
                if variant_name is not None:
                    self._values["variant_name"] = variant_name

            @builtins.property
            def initial_instance_count(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) InitialInstanceCount property.

                Specify an array of string values to match this event if the actual value of InitialInstanceCount is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("initial_instance_count")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def initial_variant_weight(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) InitialVariantWeight property.

                Specify an array of string values to match this event if the actual value of InitialVariantWeight is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("initial_variant_weight")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def instance_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) InstanceType property.

                Specify an array of string values to match this event if the actual value of InstanceType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("instance_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def model_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) ModelName property.

                Specify an array of string values to match this event if the actual value of ModelName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("model_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def variant_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) VariantName property.

                Specify an array of string values to match this event if the actual value of VariantName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("variant_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "SageMakerEndpointConfigStateChangeItem(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_sagemaker.events.EndpointConfigEvents.SageMakerEndpointConfigStateChange.SageMakerEndpointConfigStateChangeProps",
            jsii_struct_bases=[],
            name_mapping={
                "creation_time": "creationTime",
                "endpoint_config_arn": "endpointConfigArn",
                "endpoint_config_name": "endpointConfigName",
                "event_metadata": "eventMetadata",
                "production_variants": "productionVariants",
                "tags": "tags",
            },
        )
        class SageMakerEndpointConfigStateChangeProps:
            def __init__(
                self,
                *,
                creation_time: typing.Optional[typing.Sequence[builtins.str]] = None,
                endpoint_config_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                endpoint_config_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                production_variants: typing.Optional[typing.Sequence[typing.Union["EndpointConfigEvents.SageMakerEndpointConfigStateChange.SageMakerEndpointConfigStateChangeItem", typing.Dict[builtins.str, typing.Any]]]] = None,
                tags: typing.Optional[typing.Sequence[typing.Union["EndpointConfigEvents.SageMakerEndpointConfigStateChange.Tags", typing.Dict[builtins.str, typing.Any]]]] = None,
            ) -> None:
                '''(experimental) Props type for EndpointConfig aws.sagemaker@SageMakerEndpointConfigStateChange event.

                :param creation_time: (experimental) CreationTime property. Specify an array of string values to match this event if the actual value of CreationTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param endpoint_config_arn: (experimental) EndpointConfigArn property. Specify an array of string values to match this event if the actual value of EndpointConfigArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param endpoint_config_name: (experimental) EndpointConfigName property. Specify an array of string values to match this event if the actual value of EndpointConfigName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the EndpointConfig reference
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param production_variants: (experimental) ProductionVariants property. Specify an array of string values to match this event if the actual value of ProductionVariants is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param tags: (experimental) Tags property. Specify an array of string values to match this event if the actual value of Tags is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_sagemaker import events as sagemaker_events
                    
                    sage_maker_endpoint_config_state_change_props = sagemaker_events.EndpointConfigEvents.SageMakerEndpointConfigStateChange.SageMakerEndpointConfigStateChangeProps(
                        creation_time=["creationTime"],
                        endpoint_config_arn=["endpointConfigArn"],
                        endpoint_config_name=["endpointConfigName"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        production_variants=[sagemaker_events.EndpointConfigEvents.SageMakerEndpointConfigStateChange.SageMakerEndpointConfigStateChangeItem(
                            initial_instance_count=["initialInstanceCount"],
                            initial_variant_weight=["initialVariantWeight"],
                            instance_type=["instanceType"],
                            model_name=["modelName"],
                            variant_name=["variantName"]
                        )],
                        tags=[sagemaker_events.EndpointConfigEvents.SageMakerEndpointConfigStateChange.Tags(
                            key=["key"],
                            value=["value"]
                        )]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__b901fbb36ee28e177f9275f75d0ca195e0b11174b79c79a47821e9882165cf5c)
                    check_type(argname="argument creation_time", value=creation_time, expected_type=type_hints["creation_time"])
                    check_type(argname="argument endpoint_config_arn", value=endpoint_config_arn, expected_type=type_hints["endpoint_config_arn"])
                    check_type(argname="argument endpoint_config_name", value=endpoint_config_name, expected_type=type_hints["endpoint_config_name"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument production_variants", value=production_variants, expected_type=type_hints["production_variants"])
                    check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if creation_time is not None:
                    self._values["creation_time"] = creation_time
                if endpoint_config_arn is not None:
                    self._values["endpoint_config_arn"] = endpoint_config_arn
                if endpoint_config_name is not None:
                    self._values["endpoint_config_name"] = endpoint_config_name
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if production_variants is not None:
                    self._values["production_variants"] = production_variants
                if tags is not None:
                    self._values["tags"] = tags

            @builtins.property
            def creation_time(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) CreationTime property.

                Specify an array of string values to match this event if the actual value of CreationTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("creation_time")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def endpoint_config_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) EndpointConfigArn property.

                Specify an array of string values to match this event if the actual value of EndpointConfigArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("endpoint_config_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def endpoint_config_name(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) EndpointConfigName property.

                Specify an array of string values to match this event if the actual value of EndpointConfigName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the EndpointConfig reference

                :stability: experimental
                '''
                result = self._values.get("endpoint_config_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def event_metadata(
                self,
            ) -> typing.Optional[_aws_cdk_ceddda9d.AWSEventMetadataProps]:
                '''(experimental) EventBridge event metadata.

                :default:

                -
                -

                :stability: experimental
                '''
                result = self._values.get("event_metadata")
                return typing.cast(typing.Optional[_aws_cdk_ceddda9d.AWSEventMetadataProps], result)

            @builtins.property
            def production_variants(
                self,
            ) -> typing.Optional[typing.List["EndpointConfigEvents.SageMakerEndpointConfigStateChange.SageMakerEndpointConfigStateChangeItem"]]:
                '''(experimental) ProductionVariants property.

                Specify an array of string values to match this event if the actual value of ProductionVariants is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("production_variants")
                return typing.cast(typing.Optional[typing.List["EndpointConfigEvents.SageMakerEndpointConfigStateChange.SageMakerEndpointConfigStateChangeItem"]], result)

            @builtins.property
            def tags(
                self,
            ) -> typing.Optional[typing.List["EndpointConfigEvents.SageMakerEndpointConfigStateChange.Tags"]]:
                '''(experimental) Tags property.

                Specify an array of string values to match this event if the actual value of Tags is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("tags")
                return typing.cast(typing.Optional[typing.List["EndpointConfigEvents.SageMakerEndpointConfigStateChange.Tags"]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "SageMakerEndpointConfigStateChangeProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_sagemaker.events.EndpointConfigEvents.SageMakerEndpointConfigStateChange.Tags",
            jsii_struct_bases=[],
            name_mapping={"key": "key", "value": "value"},
        )
        class Tags:
            def __init__(
                self,
                *,
                key: typing.Optional[typing.Sequence[builtins.str]] = None,
                value: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Tags.

                :param key: (experimental) Key property. Specify an array of string values to match this event if the actual value of Key is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param value: (experimental) Value property. Specify an array of string values to match this event if the actual value of Value is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_sagemaker import events as sagemaker_events
                    
                    tags = sagemaker_events.EndpointConfigEvents.SageMakerEndpointConfigStateChange.Tags(
                        key=["key"],
                        value=["value"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__3246be309f4cc6b74ac02c39d3f3ad5186a69a7867ba0e7e2e96518ba6dad458)
                    check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                    check_type(argname="argument value", value=value, expected_type=type_hints["value"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if key is not None:
                    self._values["key"] = key
                if value is not None:
                    self._values["value"] = value

            @builtins.property
            def key(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) Key property.

                Specify an array of string values to match this event if the actual value of Key is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("key")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def value(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) Value property.

                Specify an array of string values to match this event if the actual value of Value is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("value")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Tags(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )


class ModelEvents(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_sagemaker.events.ModelEvents",
):
    '''(experimental) EventBridge event patterns for Model.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_sagemaker import events as sagemaker_events
        from aws_cdk.interfaces import aws_sagemaker as interfaces_sagemaker
        
        # model_ref: interfaces_sagemaker.IModelRef
        
        model_events = sagemaker_events.ModelEvents.from_model(model_ref)
    '''

    @jsii.member(jsii_name="fromModel")
    @builtins.classmethod
    def from_model(
        cls,
        model_ref: _aws_cdk_interfaces_aws_sagemaker_ceddda9d.IModelRef,
    ) -> "ModelEvents":
        '''(experimental) Create ModelEvents from a Model reference.

        :param model_ref: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75b3d537208921a703482331e1a7b3030644a45dbb282db12533511a19899e48)
            check_type(argname="argument model_ref", value=model_ref, expected_type=type_hints["model_ref"])
        return typing.cast("ModelEvents", jsii.sinvoke(cls, "fromModel", [model_ref]))

    @jsii.member(jsii_name="awsAPICallViaCloudTrailPattern")
    def aws_api_call_via_cloud_trail_pattern(
        self,
        *,
        aws_region: typing.Optional[typing.Sequence[builtins.str]] = None,
        error_code: typing.Optional[typing.Sequence[builtins.str]] = None,
        error_message: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        event_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_source: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_time: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_type: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_version: typing.Optional[typing.Sequence[builtins.str]] = None,
        request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        request_parameters: typing.Optional[typing.Union["ModelEvents.AWSAPICallViaCloudTrail.RequestParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        response_elements: typing.Optional[typing.Union["ModelEvents.AWSAPICallViaCloudTrail.ResponseElements", typing.Dict[builtins.str, typing.Any]]] = None,
        source_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_agent: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_identity: typing.Optional[typing.Union["ModelEvents.AWSAPICallViaCloudTrail.UserIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Model AWS API Call via CloudTrail.

        :param aws_region: (experimental) awsRegion property. Specify an array of string values to match this event if the actual value of awsRegion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param error_code: (experimental) errorCode property. Specify an array of string values to match this event if the actual value of errorCode is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param error_message: (experimental) errorMessage property. Specify an array of string values to match this event if the actual value of errorMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_id: (experimental) eventID property. Specify an array of string values to match this event if the actual value of eventID is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param event_name: (experimental) eventName property. Specify an array of string values to match this event if the actual value of eventName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_source: (experimental) eventSource property. Specify an array of string values to match this event if the actual value of eventSource is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_time: (experimental) eventTime property. Specify an array of string values to match this event if the actual value of eventTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_type: (experimental) eventType property. Specify an array of string values to match this event if the actual value of eventType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_version: (experimental) eventVersion property. Specify an array of string values to match this event if the actual value of eventVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param request_id: (experimental) requestID property. Specify an array of string values to match this event if the actual value of requestID is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param request_parameters: (experimental) requestParameters property. Specify an array of string values to match this event if the actual value of requestParameters is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param response_elements: (experimental) responseElements property. Specify an array of string values to match this event if the actual value of responseElements is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param source_ip_address: (experimental) sourceIPAddress property. Specify an array of string values to match this event if the actual value of sourceIPAddress is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param user_agent: (experimental) userAgent property. Specify an array of string values to match this event if the actual value of userAgent is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param user_identity: (experimental) userIdentity property. Specify an array of string values to match this event if the actual value of userIdentity is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = ModelEvents.AWSAPICallViaCloudTrail.AWSAPICallViaCloudTrailProps(
            aws_region=aws_region,
            error_code=error_code,
            error_message=error_message,
            event_id=event_id,
            event_metadata=event_metadata,
            event_name=event_name,
            event_source=event_source,
            event_time=event_time,
            event_type=event_type,
            event_version=event_version,
            request_id=request_id,
            request_parameters=request_parameters,
            response_elements=response_elements,
            source_ip_address=source_ip_address,
            user_agent=user_agent,
            user_identity=user_identity,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "awsAPICallViaCloudTrailPattern", [options]))

    @jsii.member(jsii_name="sageMakerTransformJobStateChangePattern")
    def sage_maker_transform_job_state_change_pattern(
        self,
        *,
        creation_time: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        model_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["ModelEvents.SageMakerTransformJobStateChange.Tags", typing.Dict[builtins.str, typing.Any]]]] = None,
        transform_end_time: typing.Optional[typing.Sequence[builtins.str]] = None,
        transform_input: typing.Optional[typing.Union["ModelEvents.SageMakerTransformJobStateChange.TransformInput", typing.Dict[builtins.str, typing.Any]]] = None,
        transform_job_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
        transform_job_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        transform_job_status: typing.Optional[typing.Sequence[builtins.str]] = None,
        transform_output: typing.Optional[typing.Union["ModelEvents.SageMakerTransformJobStateChange.TransformOutput", typing.Dict[builtins.str, typing.Any]]] = None,
        transform_resources: typing.Optional[typing.Union["ModelEvents.SageMakerTransformJobStateChange.TransformResources", typing.Dict[builtins.str, typing.Any]]] = None,
        transform_start_time: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Model SageMaker Transform Job State Change.

        :param creation_time: (experimental) CreationTime property. Specify an array of string values to match this event if the actual value of CreationTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param model_name: (experimental) ModelName property. Specify an array of string values to match this event if the actual value of ModelName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Model reference
        :param tags: (experimental) Tags property. Specify an array of string values to match this event if the actual value of Tags is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param transform_end_time: (experimental) TransformEndTime property. Specify an array of string values to match this event if the actual value of TransformEndTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param transform_input: (experimental) TransformInput property. Specify an array of string values to match this event if the actual value of TransformInput is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param transform_job_arn: (experimental) TransformJobArn property. Specify an array of string values to match this event if the actual value of TransformJobArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param transform_job_name: (experimental) TransformJobName property. Specify an array of string values to match this event if the actual value of TransformJobName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param transform_job_status: (experimental) TransformJobStatus property. Specify an array of string values to match this event if the actual value of TransformJobStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param transform_output: (experimental) TransformOutput property. Specify an array of string values to match this event if the actual value of TransformOutput is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param transform_resources: (experimental) TransformResources property. Specify an array of string values to match this event if the actual value of TransformResources is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param transform_start_time: (experimental) TransformStartTime property. Specify an array of string values to match this event if the actual value of TransformStartTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = ModelEvents.SageMakerTransformJobStateChange.SageMakerTransformJobStateChangeProps(
            creation_time=creation_time,
            event_metadata=event_metadata,
            model_name=model_name,
            tags=tags,
            transform_end_time=transform_end_time,
            transform_input=transform_input,
            transform_job_arn=transform_job_arn,
            transform_job_name=transform_job_name,
            transform_job_status=transform_job_status,
            transform_output=transform_output,
            transform_resources=transform_resources,
            transform_start_time=transform_start_time,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "sageMakerTransformJobStateChangePattern", [options]))

    class AWSAPICallViaCloudTrail(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_sagemaker.events.ModelEvents.AWSAPICallViaCloudTrail",
    ):
        '''(experimental) aws.sagemaker@AWSAPICallViaCloudTrail event types for Model.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_sagemaker import events as sagemaker_events
            
            a_wSAPICall_via_cloud_trail = sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_sagemaker.events.ModelEvents.AWSAPICallViaCloudTrail.AWSAPICallViaCloudTrailProps",
            jsii_struct_bases=[],
            name_mapping={
                "aws_region": "awsRegion",
                "error_code": "errorCode",
                "error_message": "errorMessage",
                "event_id": "eventId",
                "event_metadata": "eventMetadata",
                "event_name": "eventName",
                "event_source": "eventSource",
                "event_time": "eventTime",
                "event_type": "eventType",
                "event_version": "eventVersion",
                "request_id": "requestId",
                "request_parameters": "requestParameters",
                "response_elements": "responseElements",
                "source_ip_address": "sourceIpAddress",
                "user_agent": "userAgent",
                "user_identity": "userIdentity",
            },
        )
        class AWSAPICallViaCloudTrailProps:
            def __init__(
                self,
                *,
                aws_region: typing.Optional[typing.Sequence[builtins.str]] = None,
                error_code: typing.Optional[typing.Sequence[builtins.str]] = None,
                error_message: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                event_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_source: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_time: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_version: typing.Optional[typing.Sequence[builtins.str]] = None,
                request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                request_parameters: typing.Optional[typing.Union["ModelEvents.AWSAPICallViaCloudTrail.RequestParameters", typing.Dict[builtins.str, typing.Any]]] = None,
                response_elements: typing.Optional[typing.Union["ModelEvents.AWSAPICallViaCloudTrail.ResponseElements", typing.Dict[builtins.str, typing.Any]]] = None,
                source_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
                user_agent: typing.Optional[typing.Sequence[builtins.str]] = None,
                user_identity: typing.Optional[typing.Union["ModelEvents.AWSAPICallViaCloudTrail.UserIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Props type for Model aws.sagemaker@AWSAPICallViaCloudTrail event.

                :param aws_region: (experimental) awsRegion property. Specify an array of string values to match this event if the actual value of awsRegion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param error_code: (experimental) errorCode property. Specify an array of string values to match this event if the actual value of errorCode is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param error_message: (experimental) errorMessage property. Specify an array of string values to match this event if the actual value of errorMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_id: (experimental) eventID property. Specify an array of string values to match this event if the actual value of eventID is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param event_name: (experimental) eventName property. Specify an array of string values to match this event if the actual value of eventName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_source: (experimental) eventSource property. Specify an array of string values to match this event if the actual value of eventSource is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_time: (experimental) eventTime property. Specify an array of string values to match this event if the actual value of eventTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_type: (experimental) eventType property. Specify an array of string values to match this event if the actual value of eventType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_version: (experimental) eventVersion property. Specify an array of string values to match this event if the actual value of eventVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param request_id: (experimental) requestID property. Specify an array of string values to match this event if the actual value of requestID is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param request_parameters: (experimental) requestParameters property. Specify an array of string values to match this event if the actual value of requestParameters is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param response_elements: (experimental) responseElements property. Specify an array of string values to match this event if the actual value of responseElements is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param source_ip_address: (experimental) sourceIPAddress property. Specify an array of string values to match this event if the actual value of sourceIPAddress is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param user_agent: (experimental) userAgent property. Specify an array of string values to match this event if the actual value of userAgent is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param user_identity: (experimental) userIdentity property. Specify an array of string values to match this event if the actual value of userIdentity is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_sagemaker import events as sagemaker_events
                    
                    # tags: Any
                    
                    a_wSAPICall_via_cloud_trail_props = sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.AWSAPICallViaCloudTrailProps(
                        aws_region=["awsRegion"],
                        error_code=["errorCode"],
                        error_message=["errorMessage"],
                        event_id=["eventId"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        event_name=["eventName"],
                        event_source=["eventSource"],
                        event_time=["eventTime"],
                        event_type=["eventType"],
                        event_version=["eventVersion"],
                        request_id=["requestId"],
                        request_parameters=sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.RequestParameters(
                            algorithm_specification=sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.AlgorithmSpecification(
                                training_image=["trainingImage"],
                                training_input_mode=["trainingInputMode"]
                            ),
                            enable_inter_container_traffic_encryption=["enableInterContainerTrafficEncryption"],
                            enable_managed_spot_training=["enableManagedSpotTraining"],
                            enable_network_isolation=["enableNetworkIsolation"],
                            endpoint_config_name=["endpointConfigName"],
                            endpoint_name=["endpointName"],
                            execution_role_arn=["executionRoleArn"],
                            hyper_parameters=sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.HyperParameters(
                                eval_metric=["evalMetric"],
                                num_round=["numRound"],
                                objective=["objective"]
                            ),
                            input_data_config=[sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.RequestParametersItem2(
                                channel_name=["channelName"],
                                content_type=["contentType"],
                                data_source=sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.DataSource1(
                                    s3_data_source=sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.S3DataSource1(
                                        s3_data_distribution_type=["s3DataDistributionType"],
                                        s3_data_type=["s3DataType"],
                                        s3_uri=["s3Uri"]
                                    )
                                )
                            )],
                            model_name=["modelName"],
                            output_data_config=sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.OutputDataConfig(
                                remove_job_name_from_s3_output_path=["removeJobNameFromS3OutputPath"],
                                s3_output_path=["s3OutputPath"]
                            ),
                            primary_container=sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.PrimaryContainer(
                                container_hostname=["containerHostname"],
                                image=["image"],
                                model_data_url=["modelDataUrl"]
                            ),
                            production_variants=[sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.RequestParametersItem(
                                initial_instance_count=["initialInstanceCount"],
                                initial_variant_weight=["initialVariantWeight"],
                                instance_type=["instanceType"],
                                model_name=["modelName"],
                                variant_name=["variantName"]
                            )],
                            resource_config=sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.ResourceConfig(
                                instance_count=["instanceCount"],
                                instance_type=["instanceType"],
                                volume_size_in_gb=["volumeSizeInGb"]
                            ),
                            role_arn=["roleArn"],
                            stopping_condition=sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.StoppingCondition(
                                max_runtime_in_seconds=["maxRuntimeInSeconds"]
                            ),
                            tags=[tags],
                            training_job_name=["trainingJobName"],
                            transform_input=sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.TransformInput(
                                compression_type=["compressionType"],
                                content_type=["contentType"],
                                data_source=sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.DataSource(
                                    s3_data_source=sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.S3DataSource(
                                        s3_data_type=["s3DataType"],
                                        s3_uri=["s3Uri"]
                                    )
                                )
                            ),
                            transform_job_name=["transformJobName"],
                            transform_output=sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.TransformOutput(
                                s3_output_path=["s3OutputPath"]
                            ),
                            transform_resources=sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.TransformResources(
                                instance_count=["instanceCount"],
                                instance_type=["instanceType"]
                            )
                        ),
                        response_elements=sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.ResponseElements(
                            endpoint_config_arn=["endpointConfigArn"],
                            model_arn=["modelArn"],
                            training_job_arn=["trainingJobArn"],
                            transform_job_arn=["transformJobArn"]
                        ),
                        source_ip_address=["sourceIpAddress"],
                        user_agent=["userAgent"],
                        user_identity=sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.UserIdentity(
                            access_key_id=["accessKeyId"],
                            account_id=["accountId"],
                            arn=["arn"],
                            invoked_by=["invokedBy"],
                            principal_id=["principalId"],
                            session_context=sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.SessionContext(
                                attributes=sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.Attributes(
                                    creation_date=["creationDate"],
                                    mfa_authenticated=["mfaAuthenticated"]
                                ),
                                session_issuer=sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.SessionIssuer(
                                    account_id=["accountId"],
                                    arn=["arn"],
                                    principal_id=["principalId"],
                                    type=["type"],
                                    user_name=["userName"]
                                ),
                                web_id_federation_data=["webIdFederationData"]
                            ),
                            type=["type"]
                        )
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(request_parameters, dict):
                    request_parameters = ModelEvents.AWSAPICallViaCloudTrail.RequestParameters(**request_parameters)
                if isinstance(response_elements, dict):
                    response_elements = ModelEvents.AWSAPICallViaCloudTrail.ResponseElements(**response_elements)
                if isinstance(user_identity, dict):
                    user_identity = ModelEvents.AWSAPICallViaCloudTrail.UserIdentity(**user_identity)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__59976df112754a4b69eeffe1c8b19bdd0e3b2cf34568123a71de0b6016864249)
                    check_type(argname="argument aws_region", value=aws_region, expected_type=type_hints["aws_region"])
                    check_type(argname="argument error_code", value=error_code, expected_type=type_hints["error_code"])
                    check_type(argname="argument error_message", value=error_message, expected_type=type_hints["error_message"])
                    check_type(argname="argument event_id", value=event_id, expected_type=type_hints["event_id"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument event_name", value=event_name, expected_type=type_hints["event_name"])
                    check_type(argname="argument event_source", value=event_source, expected_type=type_hints["event_source"])
                    check_type(argname="argument event_time", value=event_time, expected_type=type_hints["event_time"])
                    check_type(argname="argument event_type", value=event_type, expected_type=type_hints["event_type"])
                    check_type(argname="argument event_version", value=event_version, expected_type=type_hints["event_version"])
                    check_type(argname="argument request_id", value=request_id, expected_type=type_hints["request_id"])
                    check_type(argname="argument request_parameters", value=request_parameters, expected_type=type_hints["request_parameters"])
                    check_type(argname="argument response_elements", value=response_elements, expected_type=type_hints["response_elements"])
                    check_type(argname="argument source_ip_address", value=source_ip_address, expected_type=type_hints["source_ip_address"])
                    check_type(argname="argument user_agent", value=user_agent, expected_type=type_hints["user_agent"])
                    check_type(argname="argument user_identity", value=user_identity, expected_type=type_hints["user_identity"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if aws_region is not None:
                    self._values["aws_region"] = aws_region
                if error_code is not None:
                    self._values["error_code"] = error_code
                if error_message is not None:
                    self._values["error_message"] = error_message
                if event_id is not None:
                    self._values["event_id"] = event_id
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if event_name is not None:
                    self._values["event_name"] = event_name
                if event_source is not None:
                    self._values["event_source"] = event_source
                if event_time is not None:
                    self._values["event_time"] = event_time
                if event_type is not None:
                    self._values["event_type"] = event_type
                if event_version is not None:
                    self._values["event_version"] = event_version
                if request_id is not None:
                    self._values["request_id"] = request_id
                if request_parameters is not None:
                    self._values["request_parameters"] = request_parameters
                if response_elements is not None:
                    self._values["response_elements"] = response_elements
                if source_ip_address is not None:
                    self._values["source_ip_address"] = source_ip_address
                if user_agent is not None:
                    self._values["user_agent"] = user_agent
                if user_identity is not None:
                    self._values["user_identity"] = user_identity

            @builtins.property
            def aws_region(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) awsRegion property.

                Specify an array of string values to match this event if the actual value of awsRegion is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("aws_region")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def error_code(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) errorCode property.

                Specify an array of string values to match this event if the actual value of errorCode is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("error_code")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def error_message(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) errorMessage property.

                Specify an array of string values to match this event if the actual value of errorMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("error_message")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def event_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) eventID property.

                Specify an array of string values to match this event if the actual value of eventID is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("event_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def event_metadata(
                self,
            ) -> typing.Optional[_aws_cdk_ceddda9d.AWSEventMetadataProps]:
                '''(experimental) EventBridge event metadata.

                :default:

                -
                -

                :stability: experimental
                '''
                result = self._values.get("event_metadata")
                return typing.cast(typing.Optional[_aws_cdk_ceddda9d.AWSEventMetadataProps], result)

            @builtins.property
            def event_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) eventName property.

                Specify an array of string values to match this event if the actual value of eventName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("event_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def event_source(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) eventSource property.

                Specify an array of string values to match this event if the actual value of eventSource is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("event_source")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def event_time(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) eventTime property.

                Specify an array of string values to match this event if the actual value of eventTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("event_time")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def event_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) eventType property.

                Specify an array of string values to match this event if the actual value of eventType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("event_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def event_version(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) eventVersion property.

                Specify an array of string values to match this event if the actual value of eventVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("event_version")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def request_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) requestID property.

                Specify an array of string values to match this event if the actual value of requestID is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("request_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def request_parameters(
                self,
            ) -> typing.Optional["ModelEvents.AWSAPICallViaCloudTrail.RequestParameters"]:
                '''(experimental) requestParameters property.

                Specify an array of string values to match this event if the actual value of requestParameters is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("request_parameters")
                return typing.cast(typing.Optional["ModelEvents.AWSAPICallViaCloudTrail.RequestParameters"], result)

            @builtins.property
            def response_elements(
                self,
            ) -> typing.Optional["ModelEvents.AWSAPICallViaCloudTrail.ResponseElements"]:
                '''(experimental) responseElements property.

                Specify an array of string values to match this event if the actual value of responseElements is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("response_elements")
                return typing.cast(typing.Optional["ModelEvents.AWSAPICallViaCloudTrail.ResponseElements"], result)

            @builtins.property
            def source_ip_address(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) sourceIPAddress property.

                Specify an array of string values to match this event if the actual value of sourceIPAddress is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("source_ip_address")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def user_agent(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) userAgent property.

                Specify an array of string values to match this event if the actual value of userAgent is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("user_agent")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def user_identity(
                self,
            ) -> typing.Optional["ModelEvents.AWSAPICallViaCloudTrail.UserIdentity"]:
                '''(experimental) userIdentity property.

                Specify an array of string values to match this event if the actual value of userIdentity is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("user_identity")
                return typing.cast(typing.Optional["ModelEvents.AWSAPICallViaCloudTrail.UserIdentity"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "AWSAPICallViaCloudTrailProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_sagemaker.events.ModelEvents.AWSAPICallViaCloudTrail.AlgorithmSpecification",
            jsii_struct_bases=[],
            name_mapping={
                "training_image": "trainingImage",
                "training_input_mode": "trainingInputMode",
            },
        )
        class AlgorithmSpecification:
            def __init__(
                self,
                *,
                training_image: typing.Optional[typing.Sequence[builtins.str]] = None,
                training_input_mode: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for AlgorithmSpecification.

                :param training_image: (experimental) trainingImage property. Specify an array of string values to match this event if the actual value of trainingImage is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param training_input_mode: (experimental) trainingInputMode property. Specify an array of string values to match this event if the actual value of trainingInputMode is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_sagemaker import events as sagemaker_events
                    
                    algorithm_specification = sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.AlgorithmSpecification(
                        training_image=["trainingImage"],
                        training_input_mode=["trainingInputMode"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__025fd88659dde186ce3bddb0c631d4f651f75c0d50bb1627e61bb68ae9a1fc08)
                    check_type(argname="argument training_image", value=training_image, expected_type=type_hints["training_image"])
                    check_type(argname="argument training_input_mode", value=training_input_mode, expected_type=type_hints["training_input_mode"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if training_image is not None:
                    self._values["training_image"] = training_image
                if training_input_mode is not None:
                    self._values["training_input_mode"] = training_input_mode

            @builtins.property
            def training_image(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) trainingImage property.

                Specify an array of string values to match this event if the actual value of trainingImage is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("training_image")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def training_input_mode(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) trainingInputMode property.

                Specify an array of string values to match this event if the actual value of trainingInputMode is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("training_input_mode")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "AlgorithmSpecification(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_sagemaker.events.ModelEvents.AWSAPICallViaCloudTrail.Attributes",
            jsii_struct_bases=[],
            name_mapping={
                "creation_date": "creationDate",
                "mfa_authenticated": "mfaAuthenticated",
            },
        )
        class Attributes:
            def __init__(
                self,
                *,
                creation_date: typing.Optional[typing.Sequence[builtins.str]] = None,
                mfa_authenticated: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Attributes.

                :param creation_date: (experimental) creationDate property. Specify an array of string values to match this event if the actual value of creationDate is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param mfa_authenticated: (experimental) mfaAuthenticated property. Specify an array of string values to match this event if the actual value of mfaAuthenticated is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_sagemaker import events as sagemaker_events
                    
                    attributes = sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.Attributes(
                        creation_date=["creationDate"],
                        mfa_authenticated=["mfaAuthenticated"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__272bfcf6c7f0412f7eed2d4d039b0aa90fd7050911c9a24a85420a3234653088)
                    check_type(argname="argument creation_date", value=creation_date, expected_type=type_hints["creation_date"])
                    check_type(argname="argument mfa_authenticated", value=mfa_authenticated, expected_type=type_hints["mfa_authenticated"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if creation_date is not None:
                    self._values["creation_date"] = creation_date
                if mfa_authenticated is not None:
                    self._values["mfa_authenticated"] = mfa_authenticated

            @builtins.property
            def creation_date(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) creationDate property.

                Specify an array of string values to match this event if the actual value of creationDate is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("creation_date")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def mfa_authenticated(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) mfaAuthenticated property.

                Specify an array of string values to match this event if the actual value of mfaAuthenticated is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("mfa_authenticated")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Attributes(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_sagemaker.events.ModelEvents.AWSAPICallViaCloudTrail.DataSource",
            jsii_struct_bases=[],
            name_mapping={"s3_data_source": "s3DataSource"},
        )
        class DataSource:
            def __init__(
                self,
                *,
                s3_data_source: typing.Optional[typing.Union["ModelEvents.AWSAPICallViaCloudTrail.S3DataSource", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Type definition for DataSource.

                :param s3_data_source: (experimental) s3DataSource property. Specify an array of string values to match this event if the actual value of s3DataSource is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_sagemaker import events as sagemaker_events
                    
                    data_source = sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.DataSource(
                        s3_data_source=sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.S3DataSource(
                            s3_data_type=["s3DataType"],
                            s3_uri=["s3Uri"]
                        )
                    )
                '''
                if isinstance(s3_data_source, dict):
                    s3_data_source = ModelEvents.AWSAPICallViaCloudTrail.S3DataSource(**s3_data_source)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__51f3c542c907ee6bb855464586c77d7c4e813e977bee1290fb47c854af271d77)
                    check_type(argname="argument s3_data_source", value=s3_data_source, expected_type=type_hints["s3_data_source"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if s3_data_source is not None:
                    self._values["s3_data_source"] = s3_data_source

            @builtins.property
            def s3_data_source(
                self,
            ) -> typing.Optional["ModelEvents.AWSAPICallViaCloudTrail.S3DataSource"]:
                '''(experimental) s3DataSource property.

                Specify an array of string values to match this event if the actual value of s3DataSource is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("s3_data_source")
                return typing.cast(typing.Optional["ModelEvents.AWSAPICallViaCloudTrail.S3DataSource"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "DataSource(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_sagemaker.events.ModelEvents.AWSAPICallViaCloudTrail.DataSource1",
            jsii_struct_bases=[],
            name_mapping={"s3_data_source": "s3DataSource"},
        )
        class DataSource1:
            def __init__(
                self,
                *,
                s3_data_source: typing.Optional[typing.Union["ModelEvents.AWSAPICallViaCloudTrail.S3DataSource1", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Type definition for DataSource_1.

                :param s3_data_source: (experimental) s3DataSource property. Specify an array of string values to match this event if the actual value of s3DataSource is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_sagemaker import events as sagemaker_events
                    
                    data_source1 = sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.DataSource1(
                        s3_data_source=sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.S3DataSource1(
                            s3_data_distribution_type=["s3DataDistributionType"],
                            s3_data_type=["s3DataType"],
                            s3_uri=["s3Uri"]
                        )
                    )
                '''
                if isinstance(s3_data_source, dict):
                    s3_data_source = ModelEvents.AWSAPICallViaCloudTrail.S3DataSource1(**s3_data_source)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__3da07d750b87eab65a740bdc3a90d999d905503e6aa545684caeca0d0206e6ea)
                    check_type(argname="argument s3_data_source", value=s3_data_source, expected_type=type_hints["s3_data_source"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if s3_data_source is not None:
                    self._values["s3_data_source"] = s3_data_source

            @builtins.property
            def s3_data_source(
                self,
            ) -> typing.Optional["ModelEvents.AWSAPICallViaCloudTrail.S3DataSource1"]:
                '''(experimental) s3DataSource property.

                Specify an array of string values to match this event if the actual value of s3DataSource is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("s3_data_source")
                return typing.cast(typing.Optional["ModelEvents.AWSAPICallViaCloudTrail.S3DataSource1"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "DataSource1(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_sagemaker.events.ModelEvents.AWSAPICallViaCloudTrail.HyperParameters",
            jsii_struct_bases=[],
            name_mapping={
                "eval_metric": "evalMetric",
                "num_round": "numRound",
                "objective": "objective",
            },
        )
        class HyperParameters:
            def __init__(
                self,
                *,
                eval_metric: typing.Optional[typing.Sequence[builtins.str]] = None,
                num_round: typing.Optional[typing.Sequence[builtins.str]] = None,
                objective: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for HyperParameters.

                :param eval_metric: (experimental) eval_metric property. Specify an array of string values to match this event if the actual value of eval_metric is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param num_round: (experimental) num_round property. Specify an array of string values to match this event if the actual value of num_round is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param objective: (experimental) objective property. Specify an array of string values to match this event if the actual value of objective is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_sagemaker import events as sagemaker_events
                    
                    hyper_parameters = sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.HyperParameters(
                        eval_metric=["evalMetric"],
                        num_round=["numRound"],
                        objective=["objective"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__047b6674639d5ffcf470d358540af740464470c19e0491fe97ac1a3b27be6878)
                    check_type(argname="argument eval_metric", value=eval_metric, expected_type=type_hints["eval_metric"])
                    check_type(argname="argument num_round", value=num_round, expected_type=type_hints["num_round"])
                    check_type(argname="argument objective", value=objective, expected_type=type_hints["objective"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if eval_metric is not None:
                    self._values["eval_metric"] = eval_metric
                if num_round is not None:
                    self._values["num_round"] = num_round
                if objective is not None:
                    self._values["objective"] = objective

            @builtins.property
            def eval_metric(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) eval_metric property.

                Specify an array of string values to match this event if the actual value of eval_metric is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("eval_metric")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def num_round(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) num_round property.

                Specify an array of string values to match this event if the actual value of num_round is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("num_round")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def objective(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) objective property.

                Specify an array of string values to match this event if the actual value of objective is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("objective")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "HyperParameters(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_sagemaker.events.ModelEvents.AWSAPICallViaCloudTrail.OutputDataConfig",
            jsii_struct_bases=[],
            name_mapping={
                "remove_job_name_from_s3_output_path": "removeJobNameFromS3OutputPath",
                "s3_output_path": "s3OutputPath",
            },
        )
        class OutputDataConfig:
            def __init__(
                self,
                *,
                remove_job_name_from_s3_output_path: typing.Optional[typing.Sequence[builtins.str]] = None,
                s3_output_path: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for OutputDataConfig.

                :param remove_job_name_from_s3_output_path: (experimental) removeJobNameFromS3OutputPath property. Specify an array of string values to match this event if the actual value of removeJobNameFromS3OutputPath is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param s3_output_path: (experimental) s3OutputPath property. Specify an array of string values to match this event if the actual value of s3OutputPath is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_sagemaker import events as sagemaker_events
                    
                    output_data_config = sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.OutputDataConfig(
                        remove_job_name_from_s3_output_path=["removeJobNameFromS3OutputPath"],
                        s3_output_path=["s3OutputPath"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__9c1663b872db75bf51ef6b5997eb061a5d6d545b7ec0227f9739fece5de250df)
                    check_type(argname="argument remove_job_name_from_s3_output_path", value=remove_job_name_from_s3_output_path, expected_type=type_hints["remove_job_name_from_s3_output_path"])
                    check_type(argname="argument s3_output_path", value=s3_output_path, expected_type=type_hints["s3_output_path"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if remove_job_name_from_s3_output_path is not None:
                    self._values["remove_job_name_from_s3_output_path"] = remove_job_name_from_s3_output_path
                if s3_output_path is not None:
                    self._values["s3_output_path"] = s3_output_path

            @builtins.property
            def remove_job_name_from_s3_output_path(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) removeJobNameFromS3OutputPath property.

                Specify an array of string values to match this event if the actual value of removeJobNameFromS3OutputPath is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("remove_job_name_from_s3_output_path")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def s3_output_path(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) s3OutputPath property.

                Specify an array of string values to match this event if the actual value of s3OutputPath is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("s3_output_path")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "OutputDataConfig(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_sagemaker.events.ModelEvents.AWSAPICallViaCloudTrail.PrimaryContainer",
            jsii_struct_bases=[],
            name_mapping={
                "container_hostname": "containerHostname",
                "image": "image",
                "model_data_url": "modelDataUrl",
            },
        )
        class PrimaryContainer:
            def __init__(
                self,
                *,
                container_hostname: typing.Optional[typing.Sequence[builtins.str]] = None,
                image: typing.Optional[typing.Sequence[builtins.str]] = None,
                model_data_url: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for PrimaryContainer.

                :param container_hostname: (experimental) containerHostname property. Specify an array of string values to match this event if the actual value of containerHostname is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param image: (experimental) image property. Specify an array of string values to match this event if the actual value of image is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param model_data_url: (experimental) modelDataUrl property. Specify an array of string values to match this event if the actual value of modelDataUrl is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_sagemaker import events as sagemaker_events
                    
                    primary_container = sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.PrimaryContainer(
                        container_hostname=["containerHostname"],
                        image=["image"],
                        model_data_url=["modelDataUrl"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__f4da456a797d98ed80344f114612b2ab466c38d632a273b0a4760f0f30cb930d)
                    check_type(argname="argument container_hostname", value=container_hostname, expected_type=type_hints["container_hostname"])
                    check_type(argname="argument image", value=image, expected_type=type_hints["image"])
                    check_type(argname="argument model_data_url", value=model_data_url, expected_type=type_hints["model_data_url"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if container_hostname is not None:
                    self._values["container_hostname"] = container_hostname
                if image is not None:
                    self._values["image"] = image
                if model_data_url is not None:
                    self._values["model_data_url"] = model_data_url

            @builtins.property
            def container_hostname(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) containerHostname property.

                Specify an array of string values to match this event if the actual value of containerHostname is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("container_hostname")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def image(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) image property.

                Specify an array of string values to match this event if the actual value of image is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def model_data_url(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) modelDataUrl property.

                Specify an array of string values to match this event if the actual value of modelDataUrl is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("model_data_url")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "PrimaryContainer(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_sagemaker.events.ModelEvents.AWSAPICallViaCloudTrail.RequestParameters",
            jsii_struct_bases=[],
            name_mapping={
                "algorithm_specification": "algorithmSpecification",
                "enable_inter_container_traffic_encryption": "enableInterContainerTrafficEncryption",
                "enable_managed_spot_training": "enableManagedSpotTraining",
                "enable_network_isolation": "enableNetworkIsolation",
                "endpoint_config_name": "endpointConfigName",
                "endpoint_name": "endpointName",
                "execution_role_arn": "executionRoleArn",
                "hyper_parameters": "hyperParameters",
                "input_data_config": "inputDataConfig",
                "model_name": "modelName",
                "output_data_config": "outputDataConfig",
                "primary_container": "primaryContainer",
                "production_variants": "productionVariants",
                "resource_config": "resourceConfig",
                "role_arn": "roleArn",
                "stopping_condition": "stoppingCondition",
                "tags": "tags",
                "training_job_name": "trainingJobName",
                "transform_input": "transformInput",
                "transform_job_name": "transformJobName",
                "transform_output": "transformOutput",
                "transform_resources": "transformResources",
            },
        )
        class RequestParameters:
            def __init__(
                self,
                *,
                algorithm_specification: typing.Optional[typing.Union["ModelEvents.AWSAPICallViaCloudTrail.AlgorithmSpecification", typing.Dict[builtins.str, typing.Any]]] = None,
                enable_inter_container_traffic_encryption: typing.Optional[typing.Sequence[builtins.str]] = None,
                enable_managed_spot_training: typing.Optional[typing.Sequence[builtins.str]] = None,
                enable_network_isolation: typing.Optional[typing.Sequence[builtins.str]] = None,
                endpoint_config_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                endpoint_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                execution_role_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                hyper_parameters: typing.Optional[typing.Union["ModelEvents.AWSAPICallViaCloudTrail.HyperParameters", typing.Dict[builtins.str, typing.Any]]] = None,
                input_data_config: typing.Optional[typing.Sequence[typing.Union["ModelEvents.AWSAPICallViaCloudTrail.RequestParametersItem2", typing.Dict[builtins.str, typing.Any]]]] = None,
                model_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                output_data_config: typing.Optional[typing.Union["ModelEvents.AWSAPICallViaCloudTrail.OutputDataConfig", typing.Dict[builtins.str, typing.Any]]] = None,
                primary_container: typing.Optional[typing.Union["ModelEvents.AWSAPICallViaCloudTrail.PrimaryContainer", typing.Dict[builtins.str, typing.Any]]] = None,
                production_variants: typing.Optional[typing.Sequence[typing.Union["ModelEvents.AWSAPICallViaCloudTrail.RequestParametersItem", typing.Dict[builtins.str, typing.Any]]]] = None,
                resource_config: typing.Optional[typing.Union["ModelEvents.AWSAPICallViaCloudTrail.ResourceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
                role_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                stopping_condition: typing.Optional[typing.Union["ModelEvents.AWSAPICallViaCloudTrail.StoppingCondition", typing.Dict[builtins.str, typing.Any]]] = None,
                tags: typing.Optional[typing.Sequence[typing.Any]] = None,
                training_job_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                transform_input: typing.Optional[typing.Union["ModelEvents.AWSAPICallViaCloudTrail.TransformInput", typing.Dict[builtins.str, typing.Any]]] = None,
                transform_job_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                transform_output: typing.Optional[typing.Union["ModelEvents.AWSAPICallViaCloudTrail.TransformOutput", typing.Dict[builtins.str, typing.Any]]] = None,
                transform_resources: typing.Optional[typing.Union["ModelEvents.AWSAPICallViaCloudTrail.TransformResources", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Type definition for RequestParameters.

                :param algorithm_specification: (experimental) algorithmSpecification property. Specify an array of string values to match this event if the actual value of algorithmSpecification is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param enable_inter_container_traffic_encryption: (experimental) enableInterContainerTrafficEncryption property. Specify an array of string values to match this event if the actual value of enableInterContainerTrafficEncryption is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param enable_managed_spot_training: (experimental) enableManagedSpotTraining property. Specify an array of string values to match this event if the actual value of enableManagedSpotTraining is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param enable_network_isolation: (experimental) enableNetworkIsolation property. Specify an array of string values to match this event if the actual value of enableNetworkIsolation is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param endpoint_config_name: (experimental) endpointConfigName property. Specify an array of string values to match this event if the actual value of endpointConfigName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param endpoint_name: (experimental) endpointName property. Specify an array of string values to match this event if the actual value of endpointName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param execution_role_arn: (experimental) executionRoleArn property. Specify an array of string values to match this event if the actual value of executionRoleArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param hyper_parameters: (experimental) hyperParameters property. Specify an array of string values to match this event if the actual value of hyperParameters is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param input_data_config: (experimental) inputDataConfig property. Specify an array of string values to match this event if the actual value of inputDataConfig is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param model_name: (experimental) modelName property. Specify an array of string values to match this event if the actual value of modelName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param output_data_config: (experimental) outputDataConfig property. Specify an array of string values to match this event if the actual value of outputDataConfig is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param primary_container: (experimental) primaryContainer property. Specify an array of string values to match this event if the actual value of primaryContainer is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param production_variants: (experimental) productionVariants property. Specify an array of string values to match this event if the actual value of productionVariants is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param resource_config: (experimental) resourceConfig property. Specify an array of string values to match this event if the actual value of resourceConfig is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param role_arn: (experimental) roleArn property. Specify an array of string values to match this event if the actual value of roleArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param stopping_condition: (experimental) stoppingCondition property. Specify an array of string values to match this event if the actual value of stoppingCondition is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param tags: (experimental) tags property. Specify an array of string values to match this event if the actual value of tags is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param training_job_name: (experimental) trainingJobName property. Specify an array of string values to match this event if the actual value of trainingJobName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param transform_input: (experimental) transformInput property. Specify an array of string values to match this event if the actual value of transformInput is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param transform_job_name: (experimental) transformJobName property. Specify an array of string values to match this event if the actual value of transformJobName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param transform_output: (experimental) transformOutput property. Specify an array of string values to match this event if the actual value of transformOutput is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param transform_resources: (experimental) transformResources property. Specify an array of string values to match this event if the actual value of transformResources is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_sagemaker import events as sagemaker_events
                    
                    # tags: Any
                    
                    request_parameters = sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.RequestParameters(
                        algorithm_specification=sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.AlgorithmSpecification(
                            training_image=["trainingImage"],
                            training_input_mode=["trainingInputMode"]
                        ),
                        enable_inter_container_traffic_encryption=["enableInterContainerTrafficEncryption"],
                        enable_managed_spot_training=["enableManagedSpotTraining"],
                        enable_network_isolation=["enableNetworkIsolation"],
                        endpoint_config_name=["endpointConfigName"],
                        endpoint_name=["endpointName"],
                        execution_role_arn=["executionRoleArn"],
                        hyper_parameters=sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.HyperParameters(
                            eval_metric=["evalMetric"],
                            num_round=["numRound"],
                            objective=["objective"]
                        ),
                        input_data_config=[sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.RequestParametersItem2(
                            channel_name=["channelName"],
                            content_type=["contentType"],
                            data_source=sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.DataSource1(
                                s3_data_source=sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.S3DataSource1(
                                    s3_data_distribution_type=["s3DataDistributionType"],
                                    s3_data_type=["s3DataType"],
                                    s3_uri=["s3Uri"]
                                )
                            )
                        )],
                        model_name=["modelName"],
                        output_data_config=sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.OutputDataConfig(
                            remove_job_name_from_s3_output_path=["removeJobNameFromS3OutputPath"],
                            s3_output_path=["s3OutputPath"]
                        ),
                        primary_container=sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.PrimaryContainer(
                            container_hostname=["containerHostname"],
                            image=["image"],
                            model_data_url=["modelDataUrl"]
                        ),
                        production_variants=[sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.RequestParametersItem(
                            initial_instance_count=["initialInstanceCount"],
                            initial_variant_weight=["initialVariantWeight"],
                            instance_type=["instanceType"],
                            model_name=["modelName"],
                            variant_name=["variantName"]
                        )],
                        resource_config=sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.ResourceConfig(
                            instance_count=["instanceCount"],
                            instance_type=["instanceType"],
                            volume_size_in_gb=["volumeSizeInGb"]
                        ),
                        role_arn=["roleArn"],
                        stopping_condition=sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.StoppingCondition(
                            max_runtime_in_seconds=["maxRuntimeInSeconds"]
                        ),
                        tags=[tags],
                        training_job_name=["trainingJobName"],
                        transform_input=sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.TransformInput(
                            compression_type=["compressionType"],
                            content_type=["contentType"],
                            data_source=sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.DataSource(
                                s3_data_source=sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.S3DataSource(
                                    s3_data_type=["s3DataType"],
                                    s3_uri=["s3Uri"]
                                )
                            )
                        ),
                        transform_job_name=["transformJobName"],
                        transform_output=sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.TransformOutput(
                            s3_output_path=["s3OutputPath"]
                        ),
                        transform_resources=sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.TransformResources(
                            instance_count=["instanceCount"],
                            instance_type=["instanceType"]
                        )
                    )
                '''
                if isinstance(algorithm_specification, dict):
                    algorithm_specification = ModelEvents.AWSAPICallViaCloudTrail.AlgorithmSpecification(**algorithm_specification)
                if isinstance(hyper_parameters, dict):
                    hyper_parameters = ModelEvents.AWSAPICallViaCloudTrail.HyperParameters(**hyper_parameters)
                if isinstance(output_data_config, dict):
                    output_data_config = ModelEvents.AWSAPICallViaCloudTrail.OutputDataConfig(**output_data_config)
                if isinstance(primary_container, dict):
                    primary_container = ModelEvents.AWSAPICallViaCloudTrail.PrimaryContainer(**primary_container)
                if isinstance(resource_config, dict):
                    resource_config = ModelEvents.AWSAPICallViaCloudTrail.ResourceConfig(**resource_config)
                if isinstance(stopping_condition, dict):
                    stopping_condition = ModelEvents.AWSAPICallViaCloudTrail.StoppingCondition(**stopping_condition)
                if isinstance(transform_input, dict):
                    transform_input = ModelEvents.AWSAPICallViaCloudTrail.TransformInput(**transform_input)
                if isinstance(transform_output, dict):
                    transform_output = ModelEvents.AWSAPICallViaCloudTrail.TransformOutput(**transform_output)
                if isinstance(transform_resources, dict):
                    transform_resources = ModelEvents.AWSAPICallViaCloudTrail.TransformResources(**transform_resources)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__7cf8111b1f8c260680e46a5c90674821bf1a36c8efd8b80be753602f2ae51269)
                    check_type(argname="argument algorithm_specification", value=algorithm_specification, expected_type=type_hints["algorithm_specification"])
                    check_type(argname="argument enable_inter_container_traffic_encryption", value=enable_inter_container_traffic_encryption, expected_type=type_hints["enable_inter_container_traffic_encryption"])
                    check_type(argname="argument enable_managed_spot_training", value=enable_managed_spot_training, expected_type=type_hints["enable_managed_spot_training"])
                    check_type(argname="argument enable_network_isolation", value=enable_network_isolation, expected_type=type_hints["enable_network_isolation"])
                    check_type(argname="argument endpoint_config_name", value=endpoint_config_name, expected_type=type_hints["endpoint_config_name"])
                    check_type(argname="argument endpoint_name", value=endpoint_name, expected_type=type_hints["endpoint_name"])
                    check_type(argname="argument execution_role_arn", value=execution_role_arn, expected_type=type_hints["execution_role_arn"])
                    check_type(argname="argument hyper_parameters", value=hyper_parameters, expected_type=type_hints["hyper_parameters"])
                    check_type(argname="argument input_data_config", value=input_data_config, expected_type=type_hints["input_data_config"])
                    check_type(argname="argument model_name", value=model_name, expected_type=type_hints["model_name"])
                    check_type(argname="argument output_data_config", value=output_data_config, expected_type=type_hints["output_data_config"])
                    check_type(argname="argument primary_container", value=primary_container, expected_type=type_hints["primary_container"])
                    check_type(argname="argument production_variants", value=production_variants, expected_type=type_hints["production_variants"])
                    check_type(argname="argument resource_config", value=resource_config, expected_type=type_hints["resource_config"])
                    check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                    check_type(argname="argument stopping_condition", value=stopping_condition, expected_type=type_hints["stopping_condition"])
                    check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
                    check_type(argname="argument training_job_name", value=training_job_name, expected_type=type_hints["training_job_name"])
                    check_type(argname="argument transform_input", value=transform_input, expected_type=type_hints["transform_input"])
                    check_type(argname="argument transform_job_name", value=transform_job_name, expected_type=type_hints["transform_job_name"])
                    check_type(argname="argument transform_output", value=transform_output, expected_type=type_hints["transform_output"])
                    check_type(argname="argument transform_resources", value=transform_resources, expected_type=type_hints["transform_resources"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if algorithm_specification is not None:
                    self._values["algorithm_specification"] = algorithm_specification
                if enable_inter_container_traffic_encryption is not None:
                    self._values["enable_inter_container_traffic_encryption"] = enable_inter_container_traffic_encryption
                if enable_managed_spot_training is not None:
                    self._values["enable_managed_spot_training"] = enable_managed_spot_training
                if enable_network_isolation is not None:
                    self._values["enable_network_isolation"] = enable_network_isolation
                if endpoint_config_name is not None:
                    self._values["endpoint_config_name"] = endpoint_config_name
                if endpoint_name is not None:
                    self._values["endpoint_name"] = endpoint_name
                if execution_role_arn is not None:
                    self._values["execution_role_arn"] = execution_role_arn
                if hyper_parameters is not None:
                    self._values["hyper_parameters"] = hyper_parameters
                if input_data_config is not None:
                    self._values["input_data_config"] = input_data_config
                if model_name is not None:
                    self._values["model_name"] = model_name
                if output_data_config is not None:
                    self._values["output_data_config"] = output_data_config
                if primary_container is not None:
                    self._values["primary_container"] = primary_container
                if production_variants is not None:
                    self._values["production_variants"] = production_variants
                if resource_config is not None:
                    self._values["resource_config"] = resource_config
                if role_arn is not None:
                    self._values["role_arn"] = role_arn
                if stopping_condition is not None:
                    self._values["stopping_condition"] = stopping_condition
                if tags is not None:
                    self._values["tags"] = tags
                if training_job_name is not None:
                    self._values["training_job_name"] = training_job_name
                if transform_input is not None:
                    self._values["transform_input"] = transform_input
                if transform_job_name is not None:
                    self._values["transform_job_name"] = transform_job_name
                if transform_output is not None:
                    self._values["transform_output"] = transform_output
                if transform_resources is not None:
                    self._values["transform_resources"] = transform_resources

            @builtins.property
            def algorithm_specification(
                self,
            ) -> typing.Optional["ModelEvents.AWSAPICallViaCloudTrail.AlgorithmSpecification"]:
                '''(experimental) algorithmSpecification property.

                Specify an array of string values to match this event if the actual value of algorithmSpecification is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("algorithm_specification")
                return typing.cast(typing.Optional["ModelEvents.AWSAPICallViaCloudTrail.AlgorithmSpecification"], result)

            @builtins.property
            def enable_inter_container_traffic_encryption(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) enableInterContainerTrafficEncryption property.

                Specify an array of string values to match this event if the actual value of enableInterContainerTrafficEncryption is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("enable_inter_container_traffic_encryption")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def enable_managed_spot_training(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) enableManagedSpotTraining property.

                Specify an array of string values to match this event if the actual value of enableManagedSpotTraining is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("enable_managed_spot_training")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def enable_network_isolation(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) enableNetworkIsolation property.

                Specify an array of string values to match this event if the actual value of enableNetworkIsolation is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("enable_network_isolation")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def endpoint_config_name(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) endpointConfigName property.

                Specify an array of string values to match this event if the actual value of endpointConfigName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("endpoint_config_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def endpoint_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) endpointName property.

                Specify an array of string values to match this event if the actual value of endpointName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("endpoint_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def execution_role_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) executionRoleArn property.

                Specify an array of string values to match this event if the actual value of executionRoleArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("execution_role_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def hyper_parameters(
                self,
            ) -> typing.Optional["ModelEvents.AWSAPICallViaCloudTrail.HyperParameters"]:
                '''(experimental) hyperParameters property.

                Specify an array of string values to match this event if the actual value of hyperParameters is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("hyper_parameters")
                return typing.cast(typing.Optional["ModelEvents.AWSAPICallViaCloudTrail.HyperParameters"], result)

            @builtins.property
            def input_data_config(
                self,
            ) -> typing.Optional[typing.List["ModelEvents.AWSAPICallViaCloudTrail.RequestParametersItem2"]]:
                '''(experimental) inputDataConfig property.

                Specify an array of string values to match this event if the actual value of inputDataConfig is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("input_data_config")
                return typing.cast(typing.Optional[typing.List["ModelEvents.AWSAPICallViaCloudTrail.RequestParametersItem2"]], result)

            @builtins.property
            def model_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) modelName property.

                Specify an array of string values to match this event if the actual value of modelName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("model_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def output_data_config(
                self,
            ) -> typing.Optional["ModelEvents.AWSAPICallViaCloudTrail.OutputDataConfig"]:
                '''(experimental) outputDataConfig property.

                Specify an array of string values to match this event if the actual value of outputDataConfig is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("output_data_config")
                return typing.cast(typing.Optional["ModelEvents.AWSAPICallViaCloudTrail.OutputDataConfig"], result)

            @builtins.property
            def primary_container(
                self,
            ) -> typing.Optional["ModelEvents.AWSAPICallViaCloudTrail.PrimaryContainer"]:
                '''(experimental) primaryContainer property.

                Specify an array of string values to match this event if the actual value of primaryContainer is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("primary_container")
                return typing.cast(typing.Optional["ModelEvents.AWSAPICallViaCloudTrail.PrimaryContainer"], result)

            @builtins.property
            def production_variants(
                self,
            ) -> typing.Optional[typing.List["ModelEvents.AWSAPICallViaCloudTrail.RequestParametersItem"]]:
                '''(experimental) productionVariants property.

                Specify an array of string values to match this event if the actual value of productionVariants is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("production_variants")
                return typing.cast(typing.Optional[typing.List["ModelEvents.AWSAPICallViaCloudTrail.RequestParametersItem"]], result)

            @builtins.property
            def resource_config(
                self,
            ) -> typing.Optional["ModelEvents.AWSAPICallViaCloudTrail.ResourceConfig"]:
                '''(experimental) resourceConfig property.

                Specify an array of string values to match this event if the actual value of resourceConfig is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("resource_config")
                return typing.cast(typing.Optional["ModelEvents.AWSAPICallViaCloudTrail.ResourceConfig"], result)

            @builtins.property
            def role_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) roleArn property.

                Specify an array of string values to match this event if the actual value of roleArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("role_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def stopping_condition(
                self,
            ) -> typing.Optional["ModelEvents.AWSAPICallViaCloudTrail.StoppingCondition"]:
                '''(experimental) stoppingCondition property.

                Specify an array of string values to match this event if the actual value of stoppingCondition is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("stopping_condition")
                return typing.cast(typing.Optional["ModelEvents.AWSAPICallViaCloudTrail.StoppingCondition"], result)

            @builtins.property
            def tags(self) -> typing.Optional[typing.List[typing.Any]]:
                '''(experimental) tags property.

                Specify an array of string values to match this event if the actual value of tags is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("tags")
                return typing.cast(typing.Optional[typing.List[typing.Any]], result)

            @builtins.property
            def training_job_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) trainingJobName property.

                Specify an array of string values to match this event if the actual value of trainingJobName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("training_job_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def transform_input(
                self,
            ) -> typing.Optional["ModelEvents.AWSAPICallViaCloudTrail.TransformInput"]:
                '''(experimental) transformInput property.

                Specify an array of string values to match this event if the actual value of transformInput is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("transform_input")
                return typing.cast(typing.Optional["ModelEvents.AWSAPICallViaCloudTrail.TransformInput"], result)

            @builtins.property
            def transform_job_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) transformJobName property.

                Specify an array of string values to match this event if the actual value of transformJobName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("transform_job_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def transform_output(
                self,
            ) -> typing.Optional["ModelEvents.AWSAPICallViaCloudTrail.TransformOutput"]:
                '''(experimental) transformOutput property.

                Specify an array of string values to match this event if the actual value of transformOutput is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("transform_output")
                return typing.cast(typing.Optional["ModelEvents.AWSAPICallViaCloudTrail.TransformOutput"], result)

            @builtins.property
            def transform_resources(
                self,
            ) -> typing.Optional["ModelEvents.AWSAPICallViaCloudTrail.TransformResources"]:
                '''(experimental) transformResources property.

                Specify an array of string values to match this event if the actual value of transformResources is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("transform_resources")
                return typing.cast(typing.Optional["ModelEvents.AWSAPICallViaCloudTrail.TransformResources"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "RequestParameters(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_sagemaker.events.ModelEvents.AWSAPICallViaCloudTrail.RequestParametersItem",
            jsii_struct_bases=[],
            name_mapping={
                "initial_instance_count": "initialInstanceCount",
                "initial_variant_weight": "initialVariantWeight",
                "instance_type": "instanceType",
                "model_name": "modelName",
                "variant_name": "variantName",
            },
        )
        class RequestParametersItem:
            def __init__(
                self,
                *,
                initial_instance_count: typing.Optional[typing.Sequence[builtins.str]] = None,
                initial_variant_weight: typing.Optional[typing.Sequence[builtins.str]] = None,
                instance_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                model_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                variant_name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for RequestParametersItem.

                :param initial_instance_count: (experimental) initialInstanceCount property. Specify an array of string values to match this event if the actual value of initialInstanceCount is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param initial_variant_weight: (experimental) initialVariantWeight property. Specify an array of string values to match this event if the actual value of initialVariantWeight is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param instance_type: (experimental) instanceType property. Specify an array of string values to match this event if the actual value of instanceType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param model_name: (experimental) modelName property. Specify an array of string values to match this event if the actual value of modelName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Model reference
                :param variant_name: (experimental) variantName property. Specify an array of string values to match this event if the actual value of variantName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_sagemaker import events as sagemaker_events
                    
                    request_parameters_item = sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.RequestParametersItem(
                        initial_instance_count=["initialInstanceCount"],
                        initial_variant_weight=["initialVariantWeight"],
                        instance_type=["instanceType"],
                        model_name=["modelName"],
                        variant_name=["variantName"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__6b791bd0fec67770a5a59d1fe852f9c1eed2845d3d9832fd7b952dcd2d98eaad)
                    check_type(argname="argument initial_instance_count", value=initial_instance_count, expected_type=type_hints["initial_instance_count"])
                    check_type(argname="argument initial_variant_weight", value=initial_variant_weight, expected_type=type_hints["initial_variant_weight"])
                    check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
                    check_type(argname="argument model_name", value=model_name, expected_type=type_hints["model_name"])
                    check_type(argname="argument variant_name", value=variant_name, expected_type=type_hints["variant_name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if initial_instance_count is not None:
                    self._values["initial_instance_count"] = initial_instance_count
                if initial_variant_weight is not None:
                    self._values["initial_variant_weight"] = initial_variant_weight
                if instance_type is not None:
                    self._values["instance_type"] = instance_type
                if model_name is not None:
                    self._values["model_name"] = model_name
                if variant_name is not None:
                    self._values["variant_name"] = variant_name

            @builtins.property
            def initial_instance_count(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) initialInstanceCount property.

                Specify an array of string values to match this event if the actual value of initialInstanceCount is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("initial_instance_count")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def initial_variant_weight(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) initialVariantWeight property.

                Specify an array of string values to match this event if the actual value of initialVariantWeight is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("initial_variant_weight")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def instance_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) instanceType property.

                Specify an array of string values to match this event if the actual value of instanceType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("instance_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def model_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) modelName property.

                Specify an array of string values to match this event if the actual value of modelName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Model reference

                :stability: experimental
                '''
                result = self._values.get("model_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def variant_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) variantName property.

                Specify an array of string values to match this event if the actual value of variantName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("variant_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "RequestParametersItem(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_sagemaker.events.ModelEvents.AWSAPICallViaCloudTrail.RequestParametersItem2",
            jsii_struct_bases=[],
            name_mapping={
                "channel_name": "channelName",
                "content_type": "contentType",
                "data_source": "dataSource",
            },
        )
        class RequestParametersItem2:
            def __init__(
                self,
                *,
                channel_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                content_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                data_source: typing.Optional[typing.Union["ModelEvents.AWSAPICallViaCloudTrail.DataSource1", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Type definition for RequestParametersItem_2.

                :param channel_name: (experimental) channelName property. Specify an array of string values to match this event if the actual value of channelName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param content_type: (experimental) contentType property. Specify an array of string values to match this event if the actual value of contentType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param data_source: (experimental) dataSource property. Specify an array of string values to match this event if the actual value of dataSource is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_sagemaker import events as sagemaker_events
                    
                    request_parameters_item2 = sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.RequestParametersItem2(
                        channel_name=["channelName"],
                        content_type=["contentType"],
                        data_source=sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.DataSource1(
                            s3_data_source=sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.S3DataSource1(
                                s3_data_distribution_type=["s3DataDistributionType"],
                                s3_data_type=["s3DataType"],
                                s3_uri=["s3Uri"]
                            )
                        )
                    )
                '''
                if isinstance(data_source, dict):
                    data_source = ModelEvents.AWSAPICallViaCloudTrail.DataSource1(**data_source)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__f243485f908f48e61415d29fcb7df98322e8834b1c97ce323d7f8b0098e23877)
                    check_type(argname="argument channel_name", value=channel_name, expected_type=type_hints["channel_name"])
                    check_type(argname="argument content_type", value=content_type, expected_type=type_hints["content_type"])
                    check_type(argname="argument data_source", value=data_source, expected_type=type_hints["data_source"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if channel_name is not None:
                    self._values["channel_name"] = channel_name
                if content_type is not None:
                    self._values["content_type"] = content_type
                if data_source is not None:
                    self._values["data_source"] = data_source

            @builtins.property
            def channel_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) channelName property.

                Specify an array of string values to match this event if the actual value of channelName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("channel_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def content_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) contentType property.

                Specify an array of string values to match this event if the actual value of contentType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("content_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def data_source(
                self,
            ) -> typing.Optional["ModelEvents.AWSAPICallViaCloudTrail.DataSource1"]:
                '''(experimental) dataSource property.

                Specify an array of string values to match this event if the actual value of dataSource is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("data_source")
                return typing.cast(typing.Optional["ModelEvents.AWSAPICallViaCloudTrail.DataSource1"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "RequestParametersItem2(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_sagemaker.events.ModelEvents.AWSAPICallViaCloudTrail.ResourceConfig",
            jsii_struct_bases=[],
            name_mapping={
                "instance_count": "instanceCount",
                "instance_type": "instanceType",
                "volume_size_in_gb": "volumeSizeInGb",
            },
        )
        class ResourceConfig:
            def __init__(
                self,
                *,
                instance_count: typing.Optional[typing.Sequence[builtins.str]] = None,
                instance_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                volume_size_in_gb: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for ResourceConfig.

                :param instance_count: (experimental) instanceCount property. Specify an array of string values to match this event if the actual value of instanceCount is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param instance_type: (experimental) instanceType property. Specify an array of string values to match this event if the actual value of instanceType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param volume_size_in_gb: (experimental) volumeSizeInGB property. Specify an array of string values to match this event if the actual value of volumeSizeInGB is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_sagemaker import events as sagemaker_events
                    
                    resource_config = sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.ResourceConfig(
                        instance_count=["instanceCount"],
                        instance_type=["instanceType"],
                        volume_size_in_gb=["volumeSizeInGb"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__a332182e2db21f9732a4eaedda71fdef20b24869aa38b51194f965d5a257ef2a)
                    check_type(argname="argument instance_count", value=instance_count, expected_type=type_hints["instance_count"])
                    check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
                    check_type(argname="argument volume_size_in_gb", value=volume_size_in_gb, expected_type=type_hints["volume_size_in_gb"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if instance_count is not None:
                    self._values["instance_count"] = instance_count
                if instance_type is not None:
                    self._values["instance_type"] = instance_type
                if volume_size_in_gb is not None:
                    self._values["volume_size_in_gb"] = volume_size_in_gb

            @builtins.property
            def instance_count(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) instanceCount property.

                Specify an array of string values to match this event if the actual value of instanceCount is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("instance_count")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def instance_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) instanceType property.

                Specify an array of string values to match this event if the actual value of instanceType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("instance_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def volume_size_in_gb(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) volumeSizeInGB property.

                Specify an array of string values to match this event if the actual value of volumeSizeInGB is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("volume_size_in_gb")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ResourceConfig(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_sagemaker.events.ModelEvents.AWSAPICallViaCloudTrail.ResponseElements",
            jsii_struct_bases=[],
            name_mapping={
                "endpoint_config_arn": "endpointConfigArn",
                "model_arn": "modelArn",
                "training_job_arn": "trainingJobArn",
                "transform_job_arn": "transformJobArn",
            },
        )
        class ResponseElements:
            def __init__(
                self,
                *,
                endpoint_config_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                model_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                training_job_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                transform_job_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for ResponseElements.

                :param endpoint_config_arn: (experimental) endpointConfigArn property. Specify an array of string values to match this event if the actual value of endpointConfigArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param model_arn: (experimental) modelArn property. Specify an array of string values to match this event if the actual value of modelArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param training_job_arn: (experimental) trainingJobArn property. Specify an array of string values to match this event if the actual value of trainingJobArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param transform_job_arn: (experimental) transformJobArn property. Specify an array of string values to match this event if the actual value of transformJobArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_sagemaker import events as sagemaker_events
                    
                    response_elements = sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.ResponseElements(
                        endpoint_config_arn=["endpointConfigArn"],
                        model_arn=["modelArn"],
                        training_job_arn=["trainingJobArn"],
                        transform_job_arn=["transformJobArn"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__45e1fa8e4297fcbb22b8b74c88f371049fbeccadb9bd64a591c04044c54ddb89)
                    check_type(argname="argument endpoint_config_arn", value=endpoint_config_arn, expected_type=type_hints["endpoint_config_arn"])
                    check_type(argname="argument model_arn", value=model_arn, expected_type=type_hints["model_arn"])
                    check_type(argname="argument training_job_arn", value=training_job_arn, expected_type=type_hints["training_job_arn"])
                    check_type(argname="argument transform_job_arn", value=transform_job_arn, expected_type=type_hints["transform_job_arn"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if endpoint_config_arn is not None:
                    self._values["endpoint_config_arn"] = endpoint_config_arn
                if model_arn is not None:
                    self._values["model_arn"] = model_arn
                if training_job_arn is not None:
                    self._values["training_job_arn"] = training_job_arn
                if transform_job_arn is not None:
                    self._values["transform_job_arn"] = transform_job_arn

            @builtins.property
            def endpoint_config_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) endpointConfigArn property.

                Specify an array of string values to match this event if the actual value of endpointConfigArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("endpoint_config_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def model_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) modelArn property.

                Specify an array of string values to match this event if the actual value of modelArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("model_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def training_job_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) trainingJobArn property.

                Specify an array of string values to match this event if the actual value of trainingJobArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("training_job_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def transform_job_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) transformJobArn property.

                Specify an array of string values to match this event if the actual value of transformJobArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("transform_job_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ResponseElements(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_sagemaker.events.ModelEvents.AWSAPICallViaCloudTrail.S3DataSource",
            jsii_struct_bases=[],
            name_mapping={"s3_data_type": "s3DataType", "s3_uri": "s3Uri"},
        )
        class S3DataSource:
            def __init__(
                self,
                *,
                s3_data_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                s3_uri: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for S3DataSource.

                :param s3_data_type: (experimental) s3DataType property. Specify an array of string values to match this event if the actual value of s3DataType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param s3_uri: (experimental) s3Uri property. Specify an array of string values to match this event if the actual value of s3Uri is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_sagemaker import events as sagemaker_events
                    
                    s3_data_source = sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.S3DataSource(
                        s3_data_type=["s3DataType"],
                        s3_uri=["s3Uri"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__9367a1769f2149df90f63e019f999af7c330af75551a01a0c687e9f9a126f4b4)
                    check_type(argname="argument s3_data_type", value=s3_data_type, expected_type=type_hints["s3_data_type"])
                    check_type(argname="argument s3_uri", value=s3_uri, expected_type=type_hints["s3_uri"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if s3_data_type is not None:
                    self._values["s3_data_type"] = s3_data_type
                if s3_uri is not None:
                    self._values["s3_uri"] = s3_uri

            @builtins.property
            def s3_data_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) s3DataType property.

                Specify an array of string values to match this event if the actual value of s3DataType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("s3_data_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def s3_uri(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) s3Uri property.

                Specify an array of string values to match this event if the actual value of s3Uri is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("s3_uri")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "S3DataSource(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_sagemaker.events.ModelEvents.AWSAPICallViaCloudTrail.S3DataSource1",
            jsii_struct_bases=[],
            name_mapping={
                "s3_data_distribution_type": "s3DataDistributionType",
                "s3_data_type": "s3DataType",
                "s3_uri": "s3Uri",
            },
        )
        class S3DataSource1:
            def __init__(
                self,
                *,
                s3_data_distribution_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                s3_data_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                s3_uri: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for S3DataSource_1.

                :param s3_data_distribution_type: (experimental) s3DataDistributionType property. Specify an array of string values to match this event if the actual value of s3DataDistributionType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param s3_data_type: (experimental) s3DataType property. Specify an array of string values to match this event if the actual value of s3DataType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param s3_uri: (experimental) s3Uri property. Specify an array of string values to match this event if the actual value of s3Uri is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_sagemaker import events as sagemaker_events
                    
                    s3_data_source1 = sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.S3DataSource1(
                        s3_data_distribution_type=["s3DataDistributionType"],
                        s3_data_type=["s3DataType"],
                        s3_uri=["s3Uri"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__fd590b6938d9d94fc38fe557a152a15efc0acbfb1951019b07fccf3534daa293)
                    check_type(argname="argument s3_data_distribution_type", value=s3_data_distribution_type, expected_type=type_hints["s3_data_distribution_type"])
                    check_type(argname="argument s3_data_type", value=s3_data_type, expected_type=type_hints["s3_data_type"])
                    check_type(argname="argument s3_uri", value=s3_uri, expected_type=type_hints["s3_uri"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if s3_data_distribution_type is not None:
                    self._values["s3_data_distribution_type"] = s3_data_distribution_type
                if s3_data_type is not None:
                    self._values["s3_data_type"] = s3_data_type
                if s3_uri is not None:
                    self._values["s3_uri"] = s3_uri

            @builtins.property
            def s3_data_distribution_type(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) s3DataDistributionType property.

                Specify an array of string values to match this event if the actual value of s3DataDistributionType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("s3_data_distribution_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def s3_data_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) s3DataType property.

                Specify an array of string values to match this event if the actual value of s3DataType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("s3_data_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def s3_uri(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) s3Uri property.

                Specify an array of string values to match this event if the actual value of s3Uri is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("s3_uri")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "S3DataSource1(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_sagemaker.events.ModelEvents.AWSAPICallViaCloudTrail.SessionContext",
            jsii_struct_bases=[],
            name_mapping={
                "attributes": "attributes",
                "session_issuer": "sessionIssuer",
                "web_id_federation_data": "webIdFederationData",
            },
        )
        class SessionContext:
            def __init__(
                self,
                *,
                attributes: typing.Optional[typing.Union["ModelEvents.AWSAPICallViaCloudTrail.Attributes", typing.Dict[builtins.str, typing.Any]]] = None,
                session_issuer: typing.Optional[typing.Union["ModelEvents.AWSAPICallViaCloudTrail.SessionIssuer", typing.Dict[builtins.str, typing.Any]]] = None,
                web_id_federation_data: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for SessionContext.

                :param attributes: (experimental) attributes property. Specify an array of string values to match this event if the actual value of attributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param session_issuer: (experimental) sessionIssuer property. Specify an array of string values to match this event if the actual value of sessionIssuer is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param web_id_federation_data: (experimental) webIdFederationData property. Specify an array of string values to match this event if the actual value of webIdFederationData is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_sagemaker import events as sagemaker_events
                    
                    session_context = sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.SessionContext(
                        attributes=sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.Attributes(
                            creation_date=["creationDate"],
                            mfa_authenticated=["mfaAuthenticated"]
                        ),
                        session_issuer=sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.SessionIssuer(
                            account_id=["accountId"],
                            arn=["arn"],
                            principal_id=["principalId"],
                            type=["type"],
                            user_name=["userName"]
                        ),
                        web_id_federation_data=["webIdFederationData"]
                    )
                '''
                if isinstance(attributes, dict):
                    attributes = ModelEvents.AWSAPICallViaCloudTrail.Attributes(**attributes)
                if isinstance(session_issuer, dict):
                    session_issuer = ModelEvents.AWSAPICallViaCloudTrail.SessionIssuer(**session_issuer)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__198eae261d31dd8ded8e92c9915fd508a75878ff41c5eb30950850d41aed261e)
                    check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
                    check_type(argname="argument session_issuer", value=session_issuer, expected_type=type_hints["session_issuer"])
                    check_type(argname="argument web_id_federation_data", value=web_id_federation_data, expected_type=type_hints["web_id_federation_data"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if attributes is not None:
                    self._values["attributes"] = attributes
                if session_issuer is not None:
                    self._values["session_issuer"] = session_issuer
                if web_id_federation_data is not None:
                    self._values["web_id_federation_data"] = web_id_federation_data

            @builtins.property
            def attributes(
                self,
            ) -> typing.Optional["ModelEvents.AWSAPICallViaCloudTrail.Attributes"]:
                '''(experimental) attributes property.

                Specify an array of string values to match this event if the actual value of attributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("attributes")
                return typing.cast(typing.Optional["ModelEvents.AWSAPICallViaCloudTrail.Attributes"], result)

            @builtins.property
            def session_issuer(
                self,
            ) -> typing.Optional["ModelEvents.AWSAPICallViaCloudTrail.SessionIssuer"]:
                '''(experimental) sessionIssuer property.

                Specify an array of string values to match this event if the actual value of sessionIssuer is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("session_issuer")
                return typing.cast(typing.Optional["ModelEvents.AWSAPICallViaCloudTrail.SessionIssuer"], result)

            @builtins.property
            def web_id_federation_data(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) webIdFederationData property.

                Specify an array of string values to match this event if the actual value of webIdFederationData is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("web_id_federation_data")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "SessionContext(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_sagemaker.events.ModelEvents.AWSAPICallViaCloudTrail.SessionIssuer",
            jsii_struct_bases=[],
            name_mapping={
                "account_id": "accountId",
                "arn": "arn",
                "principal_id": "principalId",
                "type": "type",
                "user_name": "userName",
            },
        )
        class SessionIssuer:
            def __init__(
                self,
                *,
                account_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                principal_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                type: typing.Optional[typing.Sequence[builtins.str]] = None,
                user_name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for SessionIssuer.

                :param account_id: (experimental) accountId property. Specify an array of string values to match this event if the actual value of accountId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param arn: (experimental) arn property. Specify an array of string values to match this event if the actual value of arn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param principal_id: (experimental) principalId property. Specify an array of string values to match this event if the actual value of principalId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param type: (experimental) type property. Specify an array of string values to match this event if the actual value of type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param user_name: (experimental) userName property. Specify an array of string values to match this event if the actual value of userName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_sagemaker import events as sagemaker_events
                    
                    session_issuer = sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.SessionIssuer(
                        account_id=["accountId"],
                        arn=["arn"],
                        principal_id=["principalId"],
                        type=["type"],
                        user_name=["userName"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__56dc6a7dd2464d8a4bbd75e4e6bc9110237ecc8530b6256fe1825d5708f9dc1a)
                    check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
                    check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                    check_type(argname="argument principal_id", value=principal_id, expected_type=type_hints["principal_id"])
                    check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                    check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if account_id is not None:
                    self._values["account_id"] = account_id
                if arn is not None:
                    self._values["arn"] = arn
                if principal_id is not None:
                    self._values["principal_id"] = principal_id
                if type is not None:
                    self._values["type"] = type
                if user_name is not None:
                    self._values["user_name"] = user_name

            @builtins.property
            def account_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) accountId property.

                Specify an array of string values to match this event if the actual value of accountId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("account_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) arn property.

                Specify an array of string values to match this event if the actual value of arn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def principal_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) principalId property.

                Specify an array of string values to match this event if the actual value of principalId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("principal_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) type property.

                Specify an array of string values to match this event if the actual value of type is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def user_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) userName property.

                Specify an array of string values to match this event if the actual value of userName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("user_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "SessionIssuer(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_sagemaker.events.ModelEvents.AWSAPICallViaCloudTrail.StoppingCondition",
            jsii_struct_bases=[],
            name_mapping={"max_runtime_in_seconds": "maxRuntimeInSeconds"},
        )
        class StoppingCondition:
            def __init__(
                self,
                *,
                max_runtime_in_seconds: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for StoppingCondition.

                :param max_runtime_in_seconds: (experimental) maxRuntimeInSeconds property. Specify an array of string values to match this event if the actual value of maxRuntimeInSeconds is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_sagemaker import events as sagemaker_events
                    
                    stopping_condition = sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.StoppingCondition(
                        max_runtime_in_seconds=["maxRuntimeInSeconds"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__ac4b394826df33029b159337dc650b80147e45c95d23dd692af7aa276f5d8b59)
                    check_type(argname="argument max_runtime_in_seconds", value=max_runtime_in_seconds, expected_type=type_hints["max_runtime_in_seconds"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if max_runtime_in_seconds is not None:
                    self._values["max_runtime_in_seconds"] = max_runtime_in_seconds

            @builtins.property
            def max_runtime_in_seconds(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) maxRuntimeInSeconds property.

                Specify an array of string values to match this event if the actual value of maxRuntimeInSeconds is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("max_runtime_in_seconds")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "StoppingCondition(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_sagemaker.events.ModelEvents.AWSAPICallViaCloudTrail.TransformInput",
            jsii_struct_bases=[],
            name_mapping={
                "compression_type": "compressionType",
                "content_type": "contentType",
                "data_source": "dataSource",
            },
        )
        class TransformInput:
            def __init__(
                self,
                *,
                compression_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                content_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                data_source: typing.Optional[typing.Union["ModelEvents.AWSAPICallViaCloudTrail.DataSource", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Type definition for TransformInput.

                :param compression_type: (experimental) compressionType property. Specify an array of string values to match this event if the actual value of compressionType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param content_type: (experimental) contentType property. Specify an array of string values to match this event if the actual value of contentType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param data_source: (experimental) dataSource property. Specify an array of string values to match this event if the actual value of dataSource is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_sagemaker import events as sagemaker_events
                    
                    transform_input = sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.TransformInput(
                        compression_type=["compressionType"],
                        content_type=["contentType"],
                        data_source=sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.DataSource(
                            s3_data_source=sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.S3DataSource(
                                s3_data_type=["s3DataType"],
                                s3_uri=["s3Uri"]
                            )
                        )
                    )
                '''
                if isinstance(data_source, dict):
                    data_source = ModelEvents.AWSAPICallViaCloudTrail.DataSource(**data_source)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__f7260c8c10708a72cd81c2cdfed1d19c0f6843d5f1d431dad0e80ba74515c07f)
                    check_type(argname="argument compression_type", value=compression_type, expected_type=type_hints["compression_type"])
                    check_type(argname="argument content_type", value=content_type, expected_type=type_hints["content_type"])
                    check_type(argname="argument data_source", value=data_source, expected_type=type_hints["data_source"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if compression_type is not None:
                    self._values["compression_type"] = compression_type
                if content_type is not None:
                    self._values["content_type"] = content_type
                if data_source is not None:
                    self._values["data_source"] = data_source

            @builtins.property
            def compression_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) compressionType property.

                Specify an array of string values to match this event if the actual value of compressionType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("compression_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def content_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) contentType property.

                Specify an array of string values to match this event if the actual value of contentType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("content_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def data_source(
                self,
            ) -> typing.Optional["ModelEvents.AWSAPICallViaCloudTrail.DataSource"]:
                '''(experimental) dataSource property.

                Specify an array of string values to match this event if the actual value of dataSource is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("data_source")
                return typing.cast(typing.Optional["ModelEvents.AWSAPICallViaCloudTrail.DataSource"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "TransformInput(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_sagemaker.events.ModelEvents.AWSAPICallViaCloudTrail.TransformOutput",
            jsii_struct_bases=[],
            name_mapping={"s3_output_path": "s3OutputPath"},
        )
        class TransformOutput:
            def __init__(
                self,
                *,
                s3_output_path: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for TransformOutput.

                :param s3_output_path: (experimental) s3OutputPath property. Specify an array of string values to match this event if the actual value of s3OutputPath is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_sagemaker import events as sagemaker_events
                    
                    transform_output = sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.TransformOutput(
                        s3_output_path=["s3OutputPath"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__281b005b7fe01cff17492c1fe01950a129ab876d9054b119d6c926cef27ec5c2)
                    check_type(argname="argument s3_output_path", value=s3_output_path, expected_type=type_hints["s3_output_path"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if s3_output_path is not None:
                    self._values["s3_output_path"] = s3_output_path

            @builtins.property
            def s3_output_path(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) s3OutputPath property.

                Specify an array of string values to match this event if the actual value of s3OutputPath is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("s3_output_path")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "TransformOutput(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_sagemaker.events.ModelEvents.AWSAPICallViaCloudTrail.TransformResources",
            jsii_struct_bases=[],
            name_mapping={
                "instance_count": "instanceCount",
                "instance_type": "instanceType",
            },
        )
        class TransformResources:
            def __init__(
                self,
                *,
                instance_count: typing.Optional[typing.Sequence[builtins.str]] = None,
                instance_type: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for TransformResources.

                :param instance_count: (experimental) instanceCount property. Specify an array of string values to match this event if the actual value of instanceCount is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param instance_type: (experimental) instanceType property. Specify an array of string values to match this event if the actual value of instanceType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_sagemaker import events as sagemaker_events
                    
                    transform_resources = sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.TransformResources(
                        instance_count=["instanceCount"],
                        instance_type=["instanceType"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__d7b510aca4fb3d561130faf89b1910f3adb6891c9d119ad48942e8fe338eec3d)
                    check_type(argname="argument instance_count", value=instance_count, expected_type=type_hints["instance_count"])
                    check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if instance_count is not None:
                    self._values["instance_count"] = instance_count
                if instance_type is not None:
                    self._values["instance_type"] = instance_type

            @builtins.property
            def instance_count(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) instanceCount property.

                Specify an array of string values to match this event if the actual value of instanceCount is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("instance_count")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def instance_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) instanceType property.

                Specify an array of string values to match this event if the actual value of instanceType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("instance_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "TransformResources(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_sagemaker.events.ModelEvents.AWSAPICallViaCloudTrail.UserIdentity",
            jsii_struct_bases=[],
            name_mapping={
                "access_key_id": "accessKeyId",
                "account_id": "accountId",
                "arn": "arn",
                "invoked_by": "invokedBy",
                "principal_id": "principalId",
                "session_context": "sessionContext",
                "type": "type",
            },
        )
        class UserIdentity:
            def __init__(
                self,
                *,
                access_key_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                account_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                invoked_by: typing.Optional[typing.Sequence[builtins.str]] = None,
                principal_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                session_context: typing.Optional[typing.Union["ModelEvents.AWSAPICallViaCloudTrail.SessionContext", typing.Dict[builtins.str, typing.Any]]] = None,
                type: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for UserIdentity.

                :param access_key_id: (experimental) accessKeyId property. Specify an array of string values to match this event if the actual value of accessKeyId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param account_id: (experimental) accountId property. Specify an array of string values to match this event if the actual value of accountId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param arn: (experimental) arn property. Specify an array of string values to match this event if the actual value of arn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param invoked_by: (experimental) invokedBy property. Specify an array of string values to match this event if the actual value of invokedBy is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param principal_id: (experimental) principalId property. Specify an array of string values to match this event if the actual value of principalId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param session_context: (experimental) sessionContext property. Specify an array of string values to match this event if the actual value of sessionContext is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param type: (experimental) type property. Specify an array of string values to match this event if the actual value of type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_sagemaker import events as sagemaker_events
                    
                    user_identity = sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.UserIdentity(
                        access_key_id=["accessKeyId"],
                        account_id=["accountId"],
                        arn=["arn"],
                        invoked_by=["invokedBy"],
                        principal_id=["principalId"],
                        session_context=sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.SessionContext(
                            attributes=sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.Attributes(
                                creation_date=["creationDate"],
                                mfa_authenticated=["mfaAuthenticated"]
                            ),
                            session_issuer=sagemaker_events.ModelEvents.AWSAPICallViaCloudTrail.SessionIssuer(
                                account_id=["accountId"],
                                arn=["arn"],
                                principal_id=["principalId"],
                                type=["type"],
                                user_name=["userName"]
                            ),
                            web_id_federation_data=["webIdFederationData"]
                        ),
                        type=["type"]
                    )
                '''
                if isinstance(session_context, dict):
                    session_context = ModelEvents.AWSAPICallViaCloudTrail.SessionContext(**session_context)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__250de13230183286831d8501c8305aafd825c74fba36afcc25c3e9049bd9f857)
                    check_type(argname="argument access_key_id", value=access_key_id, expected_type=type_hints["access_key_id"])
                    check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
                    check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                    check_type(argname="argument invoked_by", value=invoked_by, expected_type=type_hints["invoked_by"])
                    check_type(argname="argument principal_id", value=principal_id, expected_type=type_hints["principal_id"])
                    check_type(argname="argument session_context", value=session_context, expected_type=type_hints["session_context"])
                    check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if access_key_id is not None:
                    self._values["access_key_id"] = access_key_id
                if account_id is not None:
                    self._values["account_id"] = account_id
                if arn is not None:
                    self._values["arn"] = arn
                if invoked_by is not None:
                    self._values["invoked_by"] = invoked_by
                if principal_id is not None:
                    self._values["principal_id"] = principal_id
                if session_context is not None:
                    self._values["session_context"] = session_context
                if type is not None:
                    self._values["type"] = type

            @builtins.property
            def access_key_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) accessKeyId property.

                Specify an array of string values to match this event if the actual value of accessKeyId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("access_key_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def account_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) accountId property.

                Specify an array of string values to match this event if the actual value of accountId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("account_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) arn property.

                Specify an array of string values to match this event if the actual value of arn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def invoked_by(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) invokedBy property.

                Specify an array of string values to match this event if the actual value of invokedBy is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("invoked_by")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def principal_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) principalId property.

                Specify an array of string values to match this event if the actual value of principalId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("principal_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def session_context(
                self,
            ) -> typing.Optional["ModelEvents.AWSAPICallViaCloudTrail.SessionContext"]:
                '''(experimental) sessionContext property.

                Specify an array of string values to match this event if the actual value of sessionContext is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("session_context")
                return typing.cast(typing.Optional["ModelEvents.AWSAPICallViaCloudTrail.SessionContext"], result)

            @builtins.property
            def type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) type property.

                Specify an array of string values to match this event if the actual value of type is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "UserIdentity(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class SageMakerTransformJobStateChange(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_sagemaker.events.ModelEvents.SageMakerTransformJobStateChange",
    ):
        '''(experimental) aws.sagemaker@SageMakerTransformJobStateChange event types for Model.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_sagemaker import events as sagemaker_events
            
            sage_maker_transform_job_state_change = sagemaker_events.ModelEvents.SageMakerTransformJobStateChange()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_sagemaker.events.ModelEvents.SageMakerTransformJobStateChange.DataSource",
            jsii_struct_bases=[],
            name_mapping={"s3_data_source": "s3DataSource"},
        )
        class DataSource:
            def __init__(
                self,
                *,
                s3_data_source: typing.Optional[typing.Union["ModelEvents.SageMakerTransformJobStateChange.S3DataSource", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Type definition for DataSource.

                :param s3_data_source: (experimental) S3DataSource property. Specify an array of string values to match this event if the actual value of S3DataSource is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_sagemaker import events as sagemaker_events
                    
                    data_source = sagemaker_events.ModelEvents.SageMakerTransformJobStateChange.DataSource(
                        s3_data_source=sagemaker_events.ModelEvents.SageMakerTransformJobStateChange.S3DataSource(
                            s3_data_type=["s3DataType"],
                            s3_uri=["s3Uri"]
                        )
                    )
                '''
                if isinstance(s3_data_source, dict):
                    s3_data_source = ModelEvents.SageMakerTransformJobStateChange.S3DataSource(**s3_data_source)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__321bf6350377a9142e1403fa4b7be5d6a7e2a14a60fb2cb876dd8f034f7708d8)
                    check_type(argname="argument s3_data_source", value=s3_data_source, expected_type=type_hints["s3_data_source"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if s3_data_source is not None:
                    self._values["s3_data_source"] = s3_data_source

            @builtins.property
            def s3_data_source(
                self,
            ) -> typing.Optional["ModelEvents.SageMakerTransformJobStateChange.S3DataSource"]:
                '''(experimental) S3DataSource property.

                Specify an array of string values to match this event if the actual value of S3DataSource is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("s3_data_source")
                return typing.cast(typing.Optional["ModelEvents.SageMakerTransformJobStateChange.S3DataSource"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "DataSource(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_sagemaker.events.ModelEvents.SageMakerTransformJobStateChange.S3DataSource",
            jsii_struct_bases=[],
            name_mapping={"s3_data_type": "s3DataType", "s3_uri": "s3Uri"},
        )
        class S3DataSource:
            def __init__(
                self,
                *,
                s3_data_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                s3_uri: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for S3DataSource.

                :param s3_data_type: (experimental) S3DataType property. Specify an array of string values to match this event if the actual value of S3DataType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param s3_uri: (experimental) S3Uri property. Specify an array of string values to match this event if the actual value of S3Uri is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_sagemaker import events as sagemaker_events
                    
                    s3_data_source = sagemaker_events.ModelEvents.SageMakerTransformJobStateChange.S3DataSource(
                        s3_data_type=["s3DataType"],
                        s3_uri=["s3Uri"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__ee40906b1100bda33387ff385fd766e1bbfb99cc53bfb27b350fd4c71fdbf685)
                    check_type(argname="argument s3_data_type", value=s3_data_type, expected_type=type_hints["s3_data_type"])
                    check_type(argname="argument s3_uri", value=s3_uri, expected_type=type_hints["s3_uri"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if s3_data_type is not None:
                    self._values["s3_data_type"] = s3_data_type
                if s3_uri is not None:
                    self._values["s3_uri"] = s3_uri

            @builtins.property
            def s3_data_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) S3DataType property.

                Specify an array of string values to match this event if the actual value of S3DataType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("s3_data_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def s3_uri(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) S3Uri property.

                Specify an array of string values to match this event if the actual value of S3Uri is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("s3_uri")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "S3DataSource(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_sagemaker.events.ModelEvents.SageMakerTransformJobStateChange.SageMakerTransformJobStateChangeProps",
            jsii_struct_bases=[],
            name_mapping={
                "creation_time": "creationTime",
                "event_metadata": "eventMetadata",
                "model_name": "modelName",
                "tags": "tags",
                "transform_end_time": "transformEndTime",
                "transform_input": "transformInput",
                "transform_job_arn": "transformJobArn",
                "transform_job_name": "transformJobName",
                "transform_job_status": "transformJobStatus",
                "transform_output": "transformOutput",
                "transform_resources": "transformResources",
                "transform_start_time": "transformStartTime",
            },
        )
        class SageMakerTransformJobStateChangeProps:
            def __init__(
                self,
                *,
                creation_time: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                model_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                tags: typing.Optional[typing.Sequence[typing.Union["ModelEvents.SageMakerTransformJobStateChange.Tags", typing.Dict[builtins.str, typing.Any]]]] = None,
                transform_end_time: typing.Optional[typing.Sequence[builtins.str]] = None,
                transform_input: typing.Optional[typing.Union["ModelEvents.SageMakerTransformJobStateChange.TransformInput", typing.Dict[builtins.str, typing.Any]]] = None,
                transform_job_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                transform_job_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                transform_job_status: typing.Optional[typing.Sequence[builtins.str]] = None,
                transform_output: typing.Optional[typing.Union["ModelEvents.SageMakerTransformJobStateChange.TransformOutput", typing.Dict[builtins.str, typing.Any]]] = None,
                transform_resources: typing.Optional[typing.Union["ModelEvents.SageMakerTransformJobStateChange.TransformResources", typing.Dict[builtins.str, typing.Any]]] = None,
                transform_start_time: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Model aws.sagemaker@SageMakerTransformJobStateChange event.

                :param creation_time: (experimental) CreationTime property. Specify an array of string values to match this event if the actual value of CreationTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param model_name: (experimental) ModelName property. Specify an array of string values to match this event if the actual value of ModelName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Model reference
                :param tags: (experimental) Tags property. Specify an array of string values to match this event if the actual value of Tags is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param transform_end_time: (experimental) TransformEndTime property. Specify an array of string values to match this event if the actual value of TransformEndTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param transform_input: (experimental) TransformInput property. Specify an array of string values to match this event if the actual value of TransformInput is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param transform_job_arn: (experimental) TransformJobArn property. Specify an array of string values to match this event if the actual value of TransformJobArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param transform_job_name: (experimental) TransformJobName property. Specify an array of string values to match this event if the actual value of TransformJobName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param transform_job_status: (experimental) TransformJobStatus property. Specify an array of string values to match this event if the actual value of TransformJobStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param transform_output: (experimental) TransformOutput property. Specify an array of string values to match this event if the actual value of TransformOutput is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param transform_resources: (experimental) TransformResources property. Specify an array of string values to match this event if the actual value of TransformResources is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param transform_start_time: (experimental) TransformStartTime property. Specify an array of string values to match this event if the actual value of TransformStartTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_sagemaker import events as sagemaker_events
                    
                    sage_maker_transform_job_state_change_props = sagemaker_events.ModelEvents.SageMakerTransformJobStateChange.SageMakerTransformJobStateChangeProps(
                        creation_time=["creationTime"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        model_name=["modelName"],
                        tags=[sagemaker_events.ModelEvents.SageMakerTransformJobStateChange.Tags(
                            key=["key"],
                            value=["value"]
                        )],
                        transform_end_time=["transformEndTime"],
                        transform_input=sagemaker_events.ModelEvents.SageMakerTransformJobStateChange.TransformInput(
                            compression_type=["compressionType"],
                            content_type=["contentType"],
                            data_source=sagemaker_events.ModelEvents.SageMakerTransformJobStateChange.DataSource(
                                s3_data_source=sagemaker_events.ModelEvents.SageMakerTransformJobStateChange.S3DataSource(
                                    s3_data_type=["s3DataType"],
                                    s3_uri=["s3Uri"]
                                )
                            ),
                            split_type=["splitType"]
                        ),
                        transform_job_arn=["transformJobArn"],
                        transform_job_name=["transformJobName"],
                        transform_job_status=["transformJobStatus"],
                        transform_output=sagemaker_events.ModelEvents.SageMakerTransformJobStateChange.TransformOutput(
                            assemble_with=["assembleWith"],
                            s3_output_path=["s3OutputPath"]
                        ),
                        transform_resources=sagemaker_events.ModelEvents.SageMakerTransformJobStateChange.TransformResources(
                            instance_count=["instanceCount"],
                            instance_type=["instanceType"]
                        ),
                        transform_start_time=["transformStartTime"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(transform_input, dict):
                    transform_input = ModelEvents.SageMakerTransformJobStateChange.TransformInput(**transform_input)
                if isinstance(transform_output, dict):
                    transform_output = ModelEvents.SageMakerTransformJobStateChange.TransformOutput(**transform_output)
                if isinstance(transform_resources, dict):
                    transform_resources = ModelEvents.SageMakerTransformJobStateChange.TransformResources(**transform_resources)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__5201163b77f017348d8fd20a971972ef6eabd749a025a4741ed0c262d80a19b7)
                    check_type(argname="argument creation_time", value=creation_time, expected_type=type_hints["creation_time"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument model_name", value=model_name, expected_type=type_hints["model_name"])
                    check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
                    check_type(argname="argument transform_end_time", value=transform_end_time, expected_type=type_hints["transform_end_time"])
                    check_type(argname="argument transform_input", value=transform_input, expected_type=type_hints["transform_input"])
                    check_type(argname="argument transform_job_arn", value=transform_job_arn, expected_type=type_hints["transform_job_arn"])
                    check_type(argname="argument transform_job_name", value=transform_job_name, expected_type=type_hints["transform_job_name"])
                    check_type(argname="argument transform_job_status", value=transform_job_status, expected_type=type_hints["transform_job_status"])
                    check_type(argname="argument transform_output", value=transform_output, expected_type=type_hints["transform_output"])
                    check_type(argname="argument transform_resources", value=transform_resources, expected_type=type_hints["transform_resources"])
                    check_type(argname="argument transform_start_time", value=transform_start_time, expected_type=type_hints["transform_start_time"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if creation_time is not None:
                    self._values["creation_time"] = creation_time
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if model_name is not None:
                    self._values["model_name"] = model_name
                if tags is not None:
                    self._values["tags"] = tags
                if transform_end_time is not None:
                    self._values["transform_end_time"] = transform_end_time
                if transform_input is not None:
                    self._values["transform_input"] = transform_input
                if transform_job_arn is not None:
                    self._values["transform_job_arn"] = transform_job_arn
                if transform_job_name is not None:
                    self._values["transform_job_name"] = transform_job_name
                if transform_job_status is not None:
                    self._values["transform_job_status"] = transform_job_status
                if transform_output is not None:
                    self._values["transform_output"] = transform_output
                if transform_resources is not None:
                    self._values["transform_resources"] = transform_resources
                if transform_start_time is not None:
                    self._values["transform_start_time"] = transform_start_time

            @builtins.property
            def creation_time(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) CreationTime property.

                Specify an array of string values to match this event if the actual value of CreationTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("creation_time")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def event_metadata(
                self,
            ) -> typing.Optional[_aws_cdk_ceddda9d.AWSEventMetadataProps]:
                '''(experimental) EventBridge event metadata.

                :default:

                -
                -

                :stability: experimental
                '''
                result = self._values.get("event_metadata")
                return typing.cast(typing.Optional[_aws_cdk_ceddda9d.AWSEventMetadataProps], result)

            @builtins.property
            def model_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) ModelName property.

                Specify an array of string values to match this event if the actual value of ModelName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Model reference

                :stability: experimental
                '''
                result = self._values.get("model_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def tags(
                self,
            ) -> typing.Optional[typing.List["ModelEvents.SageMakerTransformJobStateChange.Tags"]]:
                '''(experimental) Tags property.

                Specify an array of string values to match this event if the actual value of Tags is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("tags")
                return typing.cast(typing.Optional[typing.List["ModelEvents.SageMakerTransformJobStateChange.Tags"]], result)

            @builtins.property
            def transform_end_time(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) TransformEndTime property.

                Specify an array of string values to match this event if the actual value of TransformEndTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("transform_end_time")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def transform_input(
                self,
            ) -> typing.Optional["ModelEvents.SageMakerTransformJobStateChange.TransformInput"]:
                '''(experimental) TransformInput property.

                Specify an array of string values to match this event if the actual value of TransformInput is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("transform_input")
                return typing.cast(typing.Optional["ModelEvents.SageMakerTransformJobStateChange.TransformInput"], result)

            @builtins.property
            def transform_job_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) TransformJobArn property.

                Specify an array of string values to match this event if the actual value of TransformJobArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("transform_job_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def transform_job_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) TransformJobName property.

                Specify an array of string values to match this event if the actual value of TransformJobName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("transform_job_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def transform_job_status(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) TransformJobStatus property.

                Specify an array of string values to match this event if the actual value of TransformJobStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("transform_job_status")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def transform_output(
                self,
            ) -> typing.Optional["ModelEvents.SageMakerTransformJobStateChange.TransformOutput"]:
                '''(experimental) TransformOutput property.

                Specify an array of string values to match this event if the actual value of TransformOutput is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("transform_output")
                return typing.cast(typing.Optional["ModelEvents.SageMakerTransformJobStateChange.TransformOutput"], result)

            @builtins.property
            def transform_resources(
                self,
            ) -> typing.Optional["ModelEvents.SageMakerTransformJobStateChange.TransformResources"]:
                '''(experimental) TransformResources property.

                Specify an array of string values to match this event if the actual value of TransformResources is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("transform_resources")
                return typing.cast(typing.Optional["ModelEvents.SageMakerTransformJobStateChange.TransformResources"], result)

            @builtins.property
            def transform_start_time(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) TransformStartTime property.

                Specify an array of string values to match this event if the actual value of TransformStartTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("transform_start_time")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "SageMakerTransformJobStateChangeProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_sagemaker.events.ModelEvents.SageMakerTransformJobStateChange.Tags",
            jsii_struct_bases=[],
            name_mapping={"key": "key", "value": "value"},
        )
        class Tags:
            def __init__(
                self,
                *,
                key: typing.Optional[typing.Sequence[builtins.str]] = None,
                value: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Tags.

                :param key: (experimental) Key property. Specify an array of string values to match this event if the actual value of Key is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param value: (experimental) Value property. Specify an array of string values to match this event if the actual value of Value is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_sagemaker import events as sagemaker_events
                    
                    tags = sagemaker_events.ModelEvents.SageMakerTransformJobStateChange.Tags(
                        key=["key"],
                        value=["value"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__8cdf289069bb68e176352c6f21c65f736290af1c6496eb3a6b0b37997e9e3b9a)
                    check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                    check_type(argname="argument value", value=value, expected_type=type_hints["value"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if key is not None:
                    self._values["key"] = key
                if value is not None:
                    self._values["value"] = value

            @builtins.property
            def key(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) Key property.

                Specify an array of string values to match this event if the actual value of Key is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("key")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def value(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) Value property.

                Specify an array of string values to match this event if the actual value of Value is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("value")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Tags(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_sagemaker.events.ModelEvents.SageMakerTransformJobStateChange.TransformInput",
            jsii_struct_bases=[],
            name_mapping={
                "compression_type": "compressionType",
                "content_type": "contentType",
                "data_source": "dataSource",
                "split_type": "splitType",
            },
        )
        class TransformInput:
            def __init__(
                self,
                *,
                compression_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                content_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                data_source: typing.Optional[typing.Union["ModelEvents.SageMakerTransformJobStateChange.DataSource", typing.Dict[builtins.str, typing.Any]]] = None,
                split_type: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for TransformInput.

                :param compression_type: (experimental) CompressionType property. Specify an array of string values to match this event if the actual value of CompressionType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param content_type: (experimental) ContentType property. Specify an array of string values to match this event if the actual value of ContentType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param data_source: (experimental) DataSource property. Specify an array of string values to match this event if the actual value of DataSource is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param split_type: (experimental) SplitType property. Specify an array of string values to match this event if the actual value of SplitType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_sagemaker import events as sagemaker_events
                    
                    transform_input = sagemaker_events.ModelEvents.SageMakerTransformJobStateChange.TransformInput(
                        compression_type=["compressionType"],
                        content_type=["contentType"],
                        data_source=sagemaker_events.ModelEvents.SageMakerTransformJobStateChange.DataSource(
                            s3_data_source=sagemaker_events.ModelEvents.SageMakerTransformJobStateChange.S3DataSource(
                                s3_data_type=["s3DataType"],
                                s3_uri=["s3Uri"]
                            )
                        ),
                        split_type=["splitType"]
                    )
                '''
                if isinstance(data_source, dict):
                    data_source = ModelEvents.SageMakerTransformJobStateChange.DataSource(**data_source)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__3115c5e0766dd6a396be805e6652be7f5e87a3fbcc586919e49b1cc94b71c624)
                    check_type(argname="argument compression_type", value=compression_type, expected_type=type_hints["compression_type"])
                    check_type(argname="argument content_type", value=content_type, expected_type=type_hints["content_type"])
                    check_type(argname="argument data_source", value=data_source, expected_type=type_hints["data_source"])
                    check_type(argname="argument split_type", value=split_type, expected_type=type_hints["split_type"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if compression_type is not None:
                    self._values["compression_type"] = compression_type
                if content_type is not None:
                    self._values["content_type"] = content_type
                if data_source is not None:
                    self._values["data_source"] = data_source
                if split_type is not None:
                    self._values["split_type"] = split_type

            @builtins.property
            def compression_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) CompressionType property.

                Specify an array of string values to match this event if the actual value of CompressionType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("compression_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def content_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) ContentType property.

                Specify an array of string values to match this event if the actual value of ContentType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("content_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def data_source(
                self,
            ) -> typing.Optional["ModelEvents.SageMakerTransformJobStateChange.DataSource"]:
                '''(experimental) DataSource property.

                Specify an array of string values to match this event if the actual value of DataSource is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("data_source")
                return typing.cast(typing.Optional["ModelEvents.SageMakerTransformJobStateChange.DataSource"], result)

            @builtins.property
            def split_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) SplitType property.

                Specify an array of string values to match this event if the actual value of SplitType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("split_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "TransformInput(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_sagemaker.events.ModelEvents.SageMakerTransformJobStateChange.TransformOutput",
            jsii_struct_bases=[],
            name_mapping={
                "assemble_with": "assembleWith",
                "s3_output_path": "s3OutputPath",
            },
        )
        class TransformOutput:
            def __init__(
                self,
                *,
                assemble_with: typing.Optional[typing.Sequence[builtins.str]] = None,
                s3_output_path: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for TransformOutput.

                :param assemble_with: (experimental) AssembleWith property. Specify an array of string values to match this event if the actual value of AssembleWith is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param s3_output_path: (experimental) S3OutputPath property. Specify an array of string values to match this event if the actual value of S3OutputPath is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_sagemaker import events as sagemaker_events
                    
                    transform_output = sagemaker_events.ModelEvents.SageMakerTransformJobStateChange.TransformOutput(
                        assemble_with=["assembleWith"],
                        s3_output_path=["s3OutputPath"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__4b725f03df34857b7cedfe3f88f67106415f4021669f83f1603a1d116818e4b1)
                    check_type(argname="argument assemble_with", value=assemble_with, expected_type=type_hints["assemble_with"])
                    check_type(argname="argument s3_output_path", value=s3_output_path, expected_type=type_hints["s3_output_path"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if assemble_with is not None:
                    self._values["assemble_with"] = assemble_with
                if s3_output_path is not None:
                    self._values["s3_output_path"] = s3_output_path

            @builtins.property
            def assemble_with(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) AssembleWith property.

                Specify an array of string values to match this event if the actual value of AssembleWith is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("assemble_with")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def s3_output_path(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) S3OutputPath property.

                Specify an array of string values to match this event if the actual value of S3OutputPath is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("s3_output_path")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "TransformOutput(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_sagemaker.events.ModelEvents.SageMakerTransformJobStateChange.TransformResources",
            jsii_struct_bases=[],
            name_mapping={
                "instance_count": "instanceCount",
                "instance_type": "instanceType",
            },
        )
        class TransformResources:
            def __init__(
                self,
                *,
                instance_count: typing.Optional[typing.Sequence[builtins.str]] = None,
                instance_type: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for TransformResources.

                :param instance_count: (experimental) InstanceCount property. Specify an array of string values to match this event if the actual value of InstanceCount is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param instance_type: (experimental) InstanceType property. Specify an array of string values to match this event if the actual value of InstanceType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_sagemaker import events as sagemaker_events
                    
                    transform_resources = sagemaker_events.ModelEvents.SageMakerTransformJobStateChange.TransformResources(
                        instance_count=["instanceCount"],
                        instance_type=["instanceType"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__08c212c3b69f5e408bfe3dcc7c76721cbdf716fa2bc6ab2db269f51d7c506569)
                    check_type(argname="argument instance_count", value=instance_count, expected_type=type_hints["instance_count"])
                    check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if instance_count is not None:
                    self._values["instance_count"] = instance_count
                if instance_type is not None:
                    self._values["instance_type"] = instance_type

            @builtins.property
            def instance_count(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) InstanceCount property.

                Specify an array of string values to match this event if the actual value of InstanceCount is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("instance_count")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def instance_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) InstanceType property.

                Specify an array of string values to match this event if the actual value of InstanceType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("instance_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "TransformResources(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )


__all__ = [
    "EndpointConfigEvents",
    "ModelEvents",
]

publication.publish()

def _typecheckingstub__89bc78d1a42c6f2ff82f20a6a7795085c79302c38cfa5dd975930ba03b128982(
    endpoint_config_ref: _aws_cdk_interfaces_aws_sagemaker_ceddda9d.IEndpointConfigRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d60854929854047702e56f68c1eefd8fd7d8498b09f18bffdd3e9fa0565804f(
    *,
    initial_instance_count: typing.Optional[typing.Sequence[builtins.str]] = None,
    initial_variant_weight: typing.Optional[typing.Sequence[builtins.str]] = None,
    instance_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    model_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    variant_name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b901fbb36ee28e177f9275f75d0ca195e0b11174b79c79a47821e9882165cf5c(
    *,
    creation_time: typing.Optional[typing.Sequence[builtins.str]] = None,
    endpoint_config_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    endpoint_config_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    production_variants: typing.Optional[typing.Sequence[typing.Union[EndpointConfigEvents.SageMakerEndpointConfigStateChange.SageMakerEndpointConfigStateChangeItem, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[EndpointConfigEvents.SageMakerEndpointConfigStateChange.Tags, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3246be309f4cc6b74ac02c39d3f3ad5186a69a7867ba0e7e2e96518ba6dad458(
    *,
    key: typing.Optional[typing.Sequence[builtins.str]] = None,
    value: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75b3d537208921a703482331e1a7b3030644a45dbb282db12533511a19899e48(
    model_ref: _aws_cdk_interfaces_aws_sagemaker_ceddda9d.IModelRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59976df112754a4b69eeffe1c8b19bdd0e3b2cf34568123a71de0b6016864249(
    *,
    aws_region: typing.Optional[typing.Sequence[builtins.str]] = None,
    error_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    error_message: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    event_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_source: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_time: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_version: typing.Optional[typing.Sequence[builtins.str]] = None,
    request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    request_parameters: typing.Optional[typing.Union[ModelEvents.AWSAPICallViaCloudTrail.RequestParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    response_elements: typing.Optional[typing.Union[ModelEvents.AWSAPICallViaCloudTrail.ResponseElements, typing.Dict[builtins.str, typing.Any]]] = None,
    source_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_agent: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_identity: typing.Optional[typing.Union[ModelEvents.AWSAPICallViaCloudTrail.UserIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__025fd88659dde186ce3bddb0c631d4f651f75c0d50bb1627e61bb68ae9a1fc08(
    *,
    training_image: typing.Optional[typing.Sequence[builtins.str]] = None,
    training_input_mode: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__272bfcf6c7f0412f7eed2d4d039b0aa90fd7050911c9a24a85420a3234653088(
    *,
    creation_date: typing.Optional[typing.Sequence[builtins.str]] = None,
    mfa_authenticated: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51f3c542c907ee6bb855464586c77d7c4e813e977bee1290fb47c854af271d77(
    *,
    s3_data_source: typing.Optional[typing.Union[ModelEvents.AWSAPICallViaCloudTrail.S3DataSource, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3da07d750b87eab65a740bdc3a90d999d905503e6aa545684caeca0d0206e6ea(
    *,
    s3_data_source: typing.Optional[typing.Union[ModelEvents.AWSAPICallViaCloudTrail.S3DataSource1, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__047b6674639d5ffcf470d358540af740464470c19e0491fe97ac1a3b27be6878(
    *,
    eval_metric: typing.Optional[typing.Sequence[builtins.str]] = None,
    num_round: typing.Optional[typing.Sequence[builtins.str]] = None,
    objective: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c1663b872db75bf51ef6b5997eb061a5d6d545b7ec0227f9739fece5de250df(
    *,
    remove_job_name_from_s3_output_path: typing.Optional[typing.Sequence[builtins.str]] = None,
    s3_output_path: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4da456a797d98ed80344f114612b2ab466c38d632a273b0a4760f0f30cb930d(
    *,
    container_hostname: typing.Optional[typing.Sequence[builtins.str]] = None,
    image: typing.Optional[typing.Sequence[builtins.str]] = None,
    model_data_url: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cf8111b1f8c260680e46a5c90674821bf1a36c8efd8b80be753602f2ae51269(
    *,
    algorithm_specification: typing.Optional[typing.Union[ModelEvents.AWSAPICallViaCloudTrail.AlgorithmSpecification, typing.Dict[builtins.str, typing.Any]]] = None,
    enable_inter_container_traffic_encryption: typing.Optional[typing.Sequence[builtins.str]] = None,
    enable_managed_spot_training: typing.Optional[typing.Sequence[builtins.str]] = None,
    enable_network_isolation: typing.Optional[typing.Sequence[builtins.str]] = None,
    endpoint_config_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    endpoint_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    execution_role_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    hyper_parameters: typing.Optional[typing.Union[ModelEvents.AWSAPICallViaCloudTrail.HyperParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    input_data_config: typing.Optional[typing.Sequence[typing.Union[ModelEvents.AWSAPICallViaCloudTrail.RequestParametersItem2, typing.Dict[builtins.str, typing.Any]]]] = None,
    model_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    output_data_config: typing.Optional[typing.Union[ModelEvents.AWSAPICallViaCloudTrail.OutputDataConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    primary_container: typing.Optional[typing.Union[ModelEvents.AWSAPICallViaCloudTrail.PrimaryContainer, typing.Dict[builtins.str, typing.Any]]] = None,
    production_variants: typing.Optional[typing.Sequence[typing.Union[ModelEvents.AWSAPICallViaCloudTrail.RequestParametersItem, typing.Dict[builtins.str, typing.Any]]]] = None,
    resource_config: typing.Optional[typing.Union[ModelEvents.AWSAPICallViaCloudTrail.ResourceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    role_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    stopping_condition: typing.Optional[typing.Union[ModelEvents.AWSAPICallViaCloudTrail.StoppingCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Any]] = None,
    training_job_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    transform_input: typing.Optional[typing.Union[ModelEvents.AWSAPICallViaCloudTrail.TransformInput, typing.Dict[builtins.str, typing.Any]]] = None,
    transform_job_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    transform_output: typing.Optional[typing.Union[ModelEvents.AWSAPICallViaCloudTrail.TransformOutput, typing.Dict[builtins.str, typing.Any]]] = None,
    transform_resources: typing.Optional[typing.Union[ModelEvents.AWSAPICallViaCloudTrail.TransformResources, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b791bd0fec67770a5a59d1fe852f9c1eed2845d3d9832fd7b952dcd2d98eaad(
    *,
    initial_instance_count: typing.Optional[typing.Sequence[builtins.str]] = None,
    initial_variant_weight: typing.Optional[typing.Sequence[builtins.str]] = None,
    instance_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    model_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    variant_name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f243485f908f48e61415d29fcb7df98322e8834b1c97ce323d7f8b0098e23877(
    *,
    channel_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    content_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    data_source: typing.Optional[typing.Union[ModelEvents.AWSAPICallViaCloudTrail.DataSource1, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a332182e2db21f9732a4eaedda71fdef20b24869aa38b51194f965d5a257ef2a(
    *,
    instance_count: typing.Optional[typing.Sequence[builtins.str]] = None,
    instance_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    volume_size_in_gb: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45e1fa8e4297fcbb22b8b74c88f371049fbeccadb9bd64a591c04044c54ddb89(
    *,
    endpoint_config_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    model_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    training_job_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    transform_job_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9367a1769f2149df90f63e019f999af7c330af75551a01a0c687e9f9a126f4b4(
    *,
    s3_data_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    s3_uri: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd590b6938d9d94fc38fe557a152a15efc0acbfb1951019b07fccf3534daa293(
    *,
    s3_data_distribution_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    s3_data_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    s3_uri: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__198eae261d31dd8ded8e92c9915fd508a75878ff41c5eb30950850d41aed261e(
    *,
    attributes: typing.Optional[typing.Union[ModelEvents.AWSAPICallViaCloudTrail.Attributes, typing.Dict[builtins.str, typing.Any]]] = None,
    session_issuer: typing.Optional[typing.Union[ModelEvents.AWSAPICallViaCloudTrail.SessionIssuer, typing.Dict[builtins.str, typing.Any]]] = None,
    web_id_federation_data: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56dc6a7dd2464d8a4bbd75e4e6bc9110237ecc8530b6256fe1825d5708f9dc1a(
    *,
    account_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    principal_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    type: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac4b394826df33029b159337dc650b80147e45c95d23dd692af7aa276f5d8b59(
    *,
    max_runtime_in_seconds: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7260c8c10708a72cd81c2cdfed1d19c0f6843d5f1d431dad0e80ba74515c07f(
    *,
    compression_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    content_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    data_source: typing.Optional[typing.Union[ModelEvents.AWSAPICallViaCloudTrail.DataSource, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__281b005b7fe01cff17492c1fe01950a129ab876d9054b119d6c926cef27ec5c2(
    *,
    s3_output_path: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7b510aca4fb3d561130faf89b1910f3adb6891c9d119ad48942e8fe338eec3d(
    *,
    instance_count: typing.Optional[typing.Sequence[builtins.str]] = None,
    instance_type: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__250de13230183286831d8501c8305aafd825c74fba36afcc25c3e9049bd9f857(
    *,
    access_key_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    account_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    invoked_by: typing.Optional[typing.Sequence[builtins.str]] = None,
    principal_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    session_context: typing.Optional[typing.Union[ModelEvents.AWSAPICallViaCloudTrail.SessionContext, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__321bf6350377a9142e1403fa4b7be5d6a7e2a14a60fb2cb876dd8f034f7708d8(
    *,
    s3_data_source: typing.Optional[typing.Union[ModelEvents.SageMakerTransformJobStateChange.S3DataSource, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee40906b1100bda33387ff385fd766e1bbfb99cc53bfb27b350fd4c71fdbf685(
    *,
    s3_data_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    s3_uri: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5201163b77f017348d8fd20a971972ef6eabd749a025a4741ed0c262d80a19b7(
    *,
    creation_time: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    model_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[ModelEvents.SageMakerTransformJobStateChange.Tags, typing.Dict[builtins.str, typing.Any]]]] = None,
    transform_end_time: typing.Optional[typing.Sequence[builtins.str]] = None,
    transform_input: typing.Optional[typing.Union[ModelEvents.SageMakerTransformJobStateChange.TransformInput, typing.Dict[builtins.str, typing.Any]]] = None,
    transform_job_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    transform_job_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    transform_job_status: typing.Optional[typing.Sequence[builtins.str]] = None,
    transform_output: typing.Optional[typing.Union[ModelEvents.SageMakerTransformJobStateChange.TransformOutput, typing.Dict[builtins.str, typing.Any]]] = None,
    transform_resources: typing.Optional[typing.Union[ModelEvents.SageMakerTransformJobStateChange.TransformResources, typing.Dict[builtins.str, typing.Any]]] = None,
    transform_start_time: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cdf289069bb68e176352c6f21c65f736290af1c6496eb3a6b0b37997e9e3b9a(
    *,
    key: typing.Optional[typing.Sequence[builtins.str]] = None,
    value: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3115c5e0766dd6a396be805e6652be7f5e87a3fbcc586919e49b1cc94b71c624(
    *,
    compression_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    content_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    data_source: typing.Optional[typing.Union[ModelEvents.SageMakerTransformJobStateChange.DataSource, typing.Dict[builtins.str, typing.Any]]] = None,
    split_type: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b725f03df34857b7cedfe3f88f67106415f4021669f83f1603a1d116818e4b1(
    *,
    assemble_with: typing.Optional[typing.Sequence[builtins.str]] = None,
    s3_output_path: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08c212c3b69f5e408bfe3dcc7c76721cbdf716fa2bc6ab2db269f51d7c506569(
    *,
    instance_count: typing.Optional[typing.Sequence[builtins.str]] = None,
    instance_type: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
