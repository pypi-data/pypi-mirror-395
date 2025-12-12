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
    jsii_type="@aws-cdk/mixins-preview.aws_panorama.mixins.CfnApplicationInstanceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_instance_id_to_replace": "applicationInstanceIdToReplace",
        "default_runtime_context_device": "defaultRuntimeContextDevice",
        "description": "description",
        "manifest_overrides_payload": "manifestOverridesPayload",
        "manifest_payload": "manifestPayload",
        "name": "name",
        "runtime_role_arn": "runtimeRoleArn",
        "tags": "tags",
    },
)
class CfnApplicationInstanceMixinProps:
    def __init__(
        self,
        *,
        application_instance_id_to_replace: typing.Optional[builtins.str] = None,
        default_runtime_context_device: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        manifest_overrides_payload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationInstancePropsMixin.ManifestOverridesPayloadProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        manifest_payload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationInstancePropsMixin.ManifestPayloadProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        runtime_role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnApplicationInstancePropsMixin.

        :param application_instance_id_to_replace: The ID of an application instance to replace with the new instance.
        :param default_runtime_context_device: The device's ID.
        :param description: A description for the application instance.
        :param manifest_overrides_payload: Setting overrides for the application manifest.
        :param manifest_payload: The application's manifest document.
        :param name: A name for the application instance.
        :param runtime_role_arn: The ARN of a runtime role for the application instance.
        :param tags: Tags for the application instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-applicationinstance.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_panorama import mixins as panorama_mixins
            
            cfn_application_instance_mixin_props = panorama_mixins.CfnApplicationInstanceMixinProps(
                application_instance_id_to_replace="applicationInstanceIdToReplace",
                default_runtime_context_device="defaultRuntimeContextDevice",
                description="description",
                manifest_overrides_payload=panorama_mixins.CfnApplicationInstancePropsMixin.ManifestOverridesPayloadProperty(
                    payload_data="payloadData"
                ),
                manifest_payload=panorama_mixins.CfnApplicationInstancePropsMixin.ManifestPayloadProperty(
                    payload_data="payloadData"
                ),
                name="name",
                runtime_role_arn="runtimeRoleArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5661377230ec8d3ddbc1c69462380df211d85b91d0670d4c1a04dd4d6ba35ab8)
            check_type(argname="argument application_instance_id_to_replace", value=application_instance_id_to_replace, expected_type=type_hints["application_instance_id_to_replace"])
            check_type(argname="argument default_runtime_context_device", value=default_runtime_context_device, expected_type=type_hints["default_runtime_context_device"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument manifest_overrides_payload", value=manifest_overrides_payload, expected_type=type_hints["manifest_overrides_payload"])
            check_type(argname="argument manifest_payload", value=manifest_payload, expected_type=type_hints["manifest_payload"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument runtime_role_arn", value=runtime_role_arn, expected_type=type_hints["runtime_role_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_instance_id_to_replace is not None:
            self._values["application_instance_id_to_replace"] = application_instance_id_to_replace
        if default_runtime_context_device is not None:
            self._values["default_runtime_context_device"] = default_runtime_context_device
        if description is not None:
            self._values["description"] = description
        if manifest_overrides_payload is not None:
            self._values["manifest_overrides_payload"] = manifest_overrides_payload
        if manifest_payload is not None:
            self._values["manifest_payload"] = manifest_payload
        if name is not None:
            self._values["name"] = name
        if runtime_role_arn is not None:
            self._values["runtime_role_arn"] = runtime_role_arn
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def application_instance_id_to_replace(self) -> typing.Optional[builtins.str]:
        '''The ID of an application instance to replace with the new instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-applicationinstance.html#cfn-panorama-applicationinstance-applicationinstanceidtoreplace
        '''
        result = self._values.get("application_instance_id_to_replace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_runtime_context_device(self) -> typing.Optional[builtins.str]:
        '''The device's ID.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-applicationinstance.html#cfn-panorama-applicationinstance-defaultruntimecontextdevice
        '''
        result = self._values.get("default_runtime_context_device")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the application instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-applicationinstance.html#cfn-panorama-applicationinstance-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def manifest_overrides_payload(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationInstancePropsMixin.ManifestOverridesPayloadProperty"]]:
        '''Setting overrides for the application manifest.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-applicationinstance.html#cfn-panorama-applicationinstance-manifestoverridespayload
        '''
        result = self._values.get("manifest_overrides_payload")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationInstancePropsMixin.ManifestOverridesPayloadProperty"]], result)

    @builtins.property
    def manifest_payload(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationInstancePropsMixin.ManifestPayloadProperty"]]:
        '''The application's manifest document.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-applicationinstance.html#cfn-panorama-applicationinstance-manifestpayload
        '''
        result = self._values.get("manifest_payload")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationInstancePropsMixin.ManifestPayloadProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A name for the application instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-applicationinstance.html#cfn-panorama-applicationinstance-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime_role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of a runtime role for the application instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-applicationinstance.html#cfn-panorama-applicationinstance-runtimerolearn
        '''
        result = self._values.get("runtime_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Tags for the application instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-applicationinstance.html#cfn-panorama-applicationinstance-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationInstanceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnApplicationInstancePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_panorama.mixins.CfnApplicationInstancePropsMixin",
):
    '''.. epigraph::

   End of support notice: On May 31, 2026, AWS will end support for AWS Panorama .

    After May 31, 2026,
    .. epigraph::

       you will no longer be able to access the AWS Panorama console or AWS Panorama resources. For more information, see `AWS Panorama end of support <https://docs.aws.amazon.com/panorama/latest/dev/panorama-end-of-support.html>`_ .

    Creates an application instance and deploys it to a device.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-applicationinstance.html
    :cloudformationResource: AWS::Panorama::ApplicationInstance
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_panorama import mixins as panorama_mixins
        
        cfn_application_instance_props_mixin = panorama_mixins.CfnApplicationInstancePropsMixin(panorama_mixins.CfnApplicationInstanceMixinProps(
            application_instance_id_to_replace="applicationInstanceIdToReplace",
            default_runtime_context_device="defaultRuntimeContextDevice",
            description="description",
            manifest_overrides_payload=panorama_mixins.CfnApplicationInstancePropsMixin.ManifestOverridesPayloadProperty(
                payload_data="payloadData"
            ),
            manifest_payload=panorama_mixins.CfnApplicationInstancePropsMixin.ManifestPayloadProperty(
                payload_data="payloadData"
            ),
            name="name",
            runtime_role_arn="runtimeRoleArn",
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
        props: typing.Union[CfnApplicationInstanceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Panorama::ApplicationInstance``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d5053c35eaaf3a2c9cd612ae46d7ab3df74f3e86ccc98df976c640e7af47f54)
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
            type_hints = typing.get_type_hints(_typecheckingstub__03e84ef9f842f2becfd805b792e6d4bf5bd70db9886a06a9629c4b807650f5ec)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fd1962ef89cdabb4ce22f9d28e0c97319f59aa83fd89b10eba3cdac231ac659)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnApplicationInstanceMixinProps:
        return typing.cast(CfnApplicationInstanceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_panorama.mixins.CfnApplicationInstancePropsMixin.ManifestOverridesPayloadProperty",
        jsii_struct_bases=[],
        name_mapping={"payload_data": "payloadData"},
    )
    class ManifestOverridesPayloadProperty:
        def __init__(
            self,
            *,
            payload_data: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Parameter overrides for an application instance.

            This is a JSON document that has a single key ( ``PayloadData`` ) where the value is an escaped string representation of the overrides document.

            :param payload_data: The overrides document.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-panorama-applicationinstance-manifestoverridespayload.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_panorama import mixins as panorama_mixins
                
                manifest_overrides_payload_property = panorama_mixins.CfnApplicationInstancePropsMixin.ManifestOverridesPayloadProperty(
                    payload_data="payloadData"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__529a9c713d3ae8f6b4aa6f1c04e9c96e4600eb02934241990d0c1dcf6e638674)
                check_type(argname="argument payload_data", value=payload_data, expected_type=type_hints["payload_data"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if payload_data is not None:
                self._values["payload_data"] = payload_data

        @builtins.property
        def payload_data(self) -> typing.Optional[builtins.str]:
            '''The overrides document.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-panorama-applicationinstance-manifestoverridespayload.html#cfn-panorama-applicationinstance-manifestoverridespayload-payloaddata
            '''
            result = self._values.get("payload_data")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ManifestOverridesPayloadProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_panorama.mixins.CfnApplicationInstancePropsMixin.ManifestPayloadProperty",
        jsii_struct_bases=[],
        name_mapping={"payload_data": "payloadData"},
    )
    class ManifestPayloadProperty:
        def __init__(
            self,
            *,
            payload_data: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A application verion's manifest file.

            This is a JSON document that has a single key ( ``PayloadData`` ) where the value is an escaped string representation of the application manifest ( ``graph.json`` ). This file is located in the ``graphs`` folder in your application source.

            :param payload_data: The application manifest.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-panorama-applicationinstance-manifestpayload.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_panorama import mixins as panorama_mixins
                
                manifest_payload_property = panorama_mixins.CfnApplicationInstancePropsMixin.ManifestPayloadProperty(
                    payload_data="payloadData"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2d7ba63fdab6af0cdc6fff8d44bb7fc059c171dca1c7b33ba84b58e37e9faa4f)
                check_type(argname="argument payload_data", value=payload_data, expected_type=type_hints["payload_data"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if payload_data is not None:
                self._values["payload_data"] = payload_data

        @builtins.property
        def payload_data(self) -> typing.Optional[builtins.str]:
            '''The application manifest.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-panorama-applicationinstance-manifestpayload.html#cfn-panorama-applicationinstance-manifestpayload-payloaddata
            '''
            result = self._values.get("payload_data")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ManifestPayloadProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_panorama.mixins.CfnPackageMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "package_name": "packageName",
        "storage_location": "storageLocation",
        "tags": "tags",
    },
)
class CfnPackageMixinProps:
    def __init__(
        self,
        *,
        package_name: typing.Optional[builtins.str] = None,
        storage_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPackagePropsMixin.StorageLocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnPackagePropsMixin.

        :param package_name: A name for the package.
        :param storage_location: A storage location.
        :param tags: Tags for the package.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-package.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_panorama import mixins as panorama_mixins
            
            cfn_package_mixin_props = panorama_mixins.CfnPackageMixinProps(
                package_name="packageName",
                storage_location=panorama_mixins.CfnPackagePropsMixin.StorageLocationProperty(
                    binary_prefix_location="binaryPrefixLocation",
                    bucket="bucket",
                    generated_prefix_location="generatedPrefixLocation",
                    manifest_prefix_location="manifestPrefixLocation",
                    repo_prefix_location="repoPrefixLocation"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1836616033ffe8e8b5b17d3b0b3ab8daaa59241ae10615c21227fc2b6ebf887d)
            check_type(argname="argument package_name", value=package_name, expected_type=type_hints["package_name"])
            check_type(argname="argument storage_location", value=storage_location, expected_type=type_hints["storage_location"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if package_name is not None:
            self._values["package_name"] = package_name
        if storage_location is not None:
            self._values["storage_location"] = storage_location
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def package_name(self) -> typing.Optional[builtins.str]:
        '''A name for the package.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-package.html#cfn-panorama-package-packagename
        '''
        result = self._values.get("package_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_location(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackagePropsMixin.StorageLocationProperty"]]:
        '''A storage location.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-package.html#cfn-panorama-package-storagelocation
        '''
        result = self._values.get("storage_location")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackagePropsMixin.StorageLocationProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Tags for the package.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-package.html#cfn-panorama-package-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPackageMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPackagePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_panorama.mixins.CfnPackagePropsMixin",
):
    '''.. epigraph::

   End of support notice: On May 31, 2026, AWS will end support for AWS Panorama .

    After May 31, 2026,
    .. epigraph::

       you will no longer be able to access the AWS Panorama console or AWS Panorama resources. For more information, see `AWS Panorama end of support <https://docs.aws.amazon.com/panorama/latest/dev/panorama-end-of-support.html>`_ .

    Creates a package and storage location in an Amazon S3 access point.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-package.html
    :cloudformationResource: AWS::Panorama::Package
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_panorama import mixins as panorama_mixins
        
        cfn_package_props_mixin = panorama_mixins.CfnPackagePropsMixin(panorama_mixins.CfnPackageMixinProps(
            package_name="packageName",
            storage_location=panorama_mixins.CfnPackagePropsMixin.StorageLocationProperty(
                binary_prefix_location="binaryPrefixLocation",
                bucket="bucket",
                generated_prefix_location="generatedPrefixLocation",
                manifest_prefix_location="manifestPrefixLocation",
                repo_prefix_location="repoPrefixLocation"
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
        props: typing.Union[CfnPackageMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Panorama::Package``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ab410ec40fb8439134a4c49cd6ac473fe1516ccb91aef56901d796872efd610)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b4ff3b6fab24b8d8899d8ee2adbef76248dd482bb1c50d83a37ae3e18d0a7de)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5611acef06d676925e772856163c9a08b5acdaa8d9a9a0ad937b6ddd2a735cd9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPackageMixinProps:
        return typing.cast(CfnPackageMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_panorama.mixins.CfnPackagePropsMixin.StorageLocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "binary_prefix_location": "binaryPrefixLocation",
            "bucket": "bucket",
            "generated_prefix_location": "generatedPrefixLocation",
            "manifest_prefix_location": "manifestPrefixLocation",
            "repo_prefix_location": "repoPrefixLocation",
        },
    )
    class StorageLocationProperty:
        def __init__(
            self,
            *,
            binary_prefix_location: typing.Optional[builtins.str] = None,
            bucket: typing.Optional[builtins.str] = None,
            generated_prefix_location: typing.Optional[builtins.str] = None,
            manifest_prefix_location: typing.Optional[builtins.str] = None,
            repo_prefix_location: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A storage location.

            :param binary_prefix_location: The location's binary prefix.
            :param bucket: The location's bucket.
            :param generated_prefix_location: The location's generated prefix.
            :param manifest_prefix_location: The location's manifest prefix.
            :param repo_prefix_location: The location's repo prefix.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-panorama-package-storagelocation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_panorama import mixins as panorama_mixins
                
                storage_location_property = panorama_mixins.CfnPackagePropsMixin.StorageLocationProperty(
                    binary_prefix_location="binaryPrefixLocation",
                    bucket="bucket",
                    generated_prefix_location="generatedPrefixLocation",
                    manifest_prefix_location="manifestPrefixLocation",
                    repo_prefix_location="repoPrefixLocation"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1718d6e76a21aa97221a786e77ee84b5da8ca1b813661e11e132fd4c4523f69b)
                check_type(argname="argument binary_prefix_location", value=binary_prefix_location, expected_type=type_hints["binary_prefix_location"])
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument generated_prefix_location", value=generated_prefix_location, expected_type=type_hints["generated_prefix_location"])
                check_type(argname="argument manifest_prefix_location", value=manifest_prefix_location, expected_type=type_hints["manifest_prefix_location"])
                check_type(argname="argument repo_prefix_location", value=repo_prefix_location, expected_type=type_hints["repo_prefix_location"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if binary_prefix_location is not None:
                self._values["binary_prefix_location"] = binary_prefix_location
            if bucket is not None:
                self._values["bucket"] = bucket
            if generated_prefix_location is not None:
                self._values["generated_prefix_location"] = generated_prefix_location
            if manifest_prefix_location is not None:
                self._values["manifest_prefix_location"] = manifest_prefix_location
            if repo_prefix_location is not None:
                self._values["repo_prefix_location"] = repo_prefix_location

        @builtins.property
        def binary_prefix_location(self) -> typing.Optional[builtins.str]:
            '''The location's binary prefix.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-panorama-package-storagelocation.html#cfn-panorama-package-storagelocation-binaryprefixlocation
            '''
            result = self._values.get("binary_prefix_location")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bucket(self) -> typing.Optional[builtins.str]:
            '''The location's bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-panorama-package-storagelocation.html#cfn-panorama-package-storagelocation-bucket
            '''
            result = self._values.get("bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def generated_prefix_location(self) -> typing.Optional[builtins.str]:
            '''The location's generated prefix.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-panorama-package-storagelocation.html#cfn-panorama-package-storagelocation-generatedprefixlocation
            '''
            result = self._values.get("generated_prefix_location")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def manifest_prefix_location(self) -> typing.Optional[builtins.str]:
            '''The location's manifest prefix.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-panorama-package-storagelocation.html#cfn-panorama-package-storagelocation-manifestprefixlocation
            '''
            result = self._values.get("manifest_prefix_location")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def repo_prefix_location(self) -> typing.Optional[builtins.str]:
            '''The location's repo prefix.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-panorama-package-storagelocation.html#cfn-panorama-package-storagelocation-repoprefixlocation
            '''
            result = self._values.get("repo_prefix_location")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StorageLocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_panorama.mixins.CfnPackageVersionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "mark_latest": "markLatest",
        "owner_account": "ownerAccount",
        "package_id": "packageId",
        "package_version": "packageVersion",
        "patch_version": "patchVersion",
        "updated_latest_patch_version": "updatedLatestPatchVersion",
    },
)
class CfnPackageVersionMixinProps:
    def __init__(
        self,
        *,
        mark_latest: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        owner_account: typing.Optional[builtins.str] = None,
        package_id: typing.Optional[builtins.str] = None,
        package_version: typing.Optional[builtins.str] = None,
        patch_version: typing.Optional[builtins.str] = None,
        updated_latest_patch_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnPackageVersionPropsMixin.

        :param mark_latest: Whether to mark the new version as the latest version.
        :param owner_account: An owner account.
        :param package_id: A package ID.
        :param package_version: A package version.
        :param patch_version: A patch version.
        :param updated_latest_patch_version: If the version was marked latest, the new version to maker as latest.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-packageversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_panorama import mixins as panorama_mixins
            
            cfn_package_version_mixin_props = panorama_mixins.CfnPackageVersionMixinProps(
                mark_latest=False,
                owner_account="ownerAccount",
                package_id="packageId",
                package_version="packageVersion",
                patch_version="patchVersion",
                updated_latest_patch_version="updatedLatestPatchVersion"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f4aae689f586c027fe03b254126a6db7cab71654b151a95dc4022de81722796)
            check_type(argname="argument mark_latest", value=mark_latest, expected_type=type_hints["mark_latest"])
            check_type(argname="argument owner_account", value=owner_account, expected_type=type_hints["owner_account"])
            check_type(argname="argument package_id", value=package_id, expected_type=type_hints["package_id"])
            check_type(argname="argument package_version", value=package_version, expected_type=type_hints["package_version"])
            check_type(argname="argument patch_version", value=patch_version, expected_type=type_hints["patch_version"])
            check_type(argname="argument updated_latest_patch_version", value=updated_latest_patch_version, expected_type=type_hints["updated_latest_patch_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if mark_latest is not None:
            self._values["mark_latest"] = mark_latest
        if owner_account is not None:
            self._values["owner_account"] = owner_account
        if package_id is not None:
            self._values["package_id"] = package_id
        if package_version is not None:
            self._values["package_version"] = package_version
        if patch_version is not None:
            self._values["patch_version"] = patch_version
        if updated_latest_patch_version is not None:
            self._values["updated_latest_patch_version"] = updated_latest_patch_version

    @builtins.property
    def mark_latest(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Whether to mark the new version as the latest version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-packageversion.html#cfn-panorama-packageversion-marklatest
        '''
        result = self._values.get("mark_latest")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def owner_account(self) -> typing.Optional[builtins.str]:
        '''An owner account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-packageversion.html#cfn-panorama-packageversion-owneraccount
        '''
        result = self._values.get("owner_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def package_id(self) -> typing.Optional[builtins.str]:
        '''A package ID.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-packageversion.html#cfn-panorama-packageversion-packageid
        '''
        result = self._values.get("package_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def package_version(self) -> typing.Optional[builtins.str]:
        '''A package version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-packageversion.html#cfn-panorama-packageversion-packageversion
        '''
        result = self._values.get("package_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def patch_version(self) -> typing.Optional[builtins.str]:
        '''A patch version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-packageversion.html#cfn-panorama-packageversion-patchversion
        '''
        result = self._values.get("patch_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def updated_latest_patch_version(self) -> typing.Optional[builtins.str]:
        '''If the version was marked latest, the new version to maker as latest.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-packageversion.html#cfn-panorama-packageversion-updatedlatestpatchversion
        '''
        result = self._values.get("updated_latest_patch_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPackageVersionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPackageVersionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_panorama.mixins.CfnPackageVersionPropsMixin",
):
    '''.. epigraph::

   End of support notice: On May 31, 2026, AWS will end support for AWS Panorama .

    After May 31, 2026,
    .. epigraph::

       you will no longer be able to access the AWS Panorama console or AWS Panorama resources. For more information, see `AWS Panorama end of support <https://docs.aws.amazon.com/panorama/latest/dev/panorama-end-of-support.html>`_ .

    Registers a package version.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-packageversion.html
    :cloudformationResource: AWS::Panorama::PackageVersion
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_panorama import mixins as panorama_mixins
        
        cfn_package_version_props_mixin = panorama_mixins.CfnPackageVersionPropsMixin(panorama_mixins.CfnPackageVersionMixinProps(
            mark_latest=False,
            owner_account="ownerAccount",
            package_id="packageId",
            package_version="packageVersion",
            patch_version="patchVersion",
            updated_latest_patch_version="updatedLatestPatchVersion"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnPackageVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Panorama::PackageVersion``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8de9cae60ca14adf4a38449ea9d388ea3c6e89a5286b8ac35b3a39c6fd0aa7ab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbabe2a9fc401ffb1ca40ad40cb9a28aa802ad63a064374738764949addc1aa1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3fd64853e1e8e83cd5ee3a1c8df167cd2d76e8e59bfa8e958ca1e338c5cc4f3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPackageVersionMixinProps:
        return typing.cast(CfnPackageVersionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnApplicationInstanceMixinProps",
    "CfnApplicationInstancePropsMixin",
    "CfnPackageMixinProps",
    "CfnPackagePropsMixin",
    "CfnPackageVersionMixinProps",
    "CfnPackageVersionPropsMixin",
]

publication.publish()

def _typecheckingstub__5661377230ec8d3ddbc1c69462380df211d85b91d0670d4c1a04dd4d6ba35ab8(
    *,
    application_instance_id_to_replace: typing.Optional[builtins.str] = None,
    default_runtime_context_device: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    manifest_overrides_payload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationInstancePropsMixin.ManifestOverridesPayloadProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    manifest_payload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationInstancePropsMixin.ManifestPayloadProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    runtime_role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d5053c35eaaf3a2c9cd612ae46d7ab3df74f3e86ccc98df976c640e7af47f54(
    props: typing.Union[CfnApplicationInstanceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03e84ef9f842f2becfd805b792e6d4bf5bd70db9886a06a9629c4b807650f5ec(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fd1962ef89cdabb4ce22f9d28e0c97319f59aa83fd89b10eba3cdac231ac659(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__529a9c713d3ae8f6b4aa6f1c04e9c96e4600eb02934241990d0c1dcf6e638674(
    *,
    payload_data: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d7ba63fdab6af0cdc6fff8d44bb7fc059c171dca1c7b33ba84b58e37e9faa4f(
    *,
    payload_data: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1836616033ffe8e8b5b17d3b0b3ab8daaa59241ae10615c21227fc2b6ebf887d(
    *,
    package_name: typing.Optional[builtins.str] = None,
    storage_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPackagePropsMixin.StorageLocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ab410ec40fb8439134a4c49cd6ac473fe1516ccb91aef56901d796872efd610(
    props: typing.Union[CfnPackageMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b4ff3b6fab24b8d8899d8ee2adbef76248dd482bb1c50d83a37ae3e18d0a7de(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5611acef06d676925e772856163c9a08b5acdaa8d9a9a0ad937b6ddd2a735cd9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1718d6e76a21aa97221a786e77ee84b5da8ca1b813661e11e132fd4c4523f69b(
    *,
    binary_prefix_location: typing.Optional[builtins.str] = None,
    bucket: typing.Optional[builtins.str] = None,
    generated_prefix_location: typing.Optional[builtins.str] = None,
    manifest_prefix_location: typing.Optional[builtins.str] = None,
    repo_prefix_location: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f4aae689f586c027fe03b254126a6db7cab71654b151a95dc4022de81722796(
    *,
    mark_latest: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    owner_account: typing.Optional[builtins.str] = None,
    package_id: typing.Optional[builtins.str] = None,
    package_version: typing.Optional[builtins.str] = None,
    patch_version: typing.Optional[builtins.str] = None,
    updated_latest_patch_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8de9cae60ca14adf4a38449ea9d388ea3c6e89a5286b8ac35b3a39c6fd0aa7ab(
    props: typing.Union[CfnPackageVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbabe2a9fc401ffb1ca40ad40cb9a28aa802ad63a064374738764949addc1aa1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3fd64853e1e8e83cd5ee3a1c8df167cd2d76e8e59bfa8e958ca1e338c5cc4f3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
