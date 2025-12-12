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

from .._jsii import *


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.mixins.CfnPropertyMixinOptions",
    jsii_struct_bases=[],
    name_mapping={"strategy": "strategy"},
)
class CfnPropertyMixinOptions:
    def __init__(
        self,
        *,
        strategy: typing.Optional["PropertyMergeStrategy"] = None,
    ) -> None:
        '''(experimental) Options for applying CfnProperty mixins.

        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # bucket: s3.CfnBucket
            
            
            # MERGE (default): Deep merges properties with existing values
            Mixins.of(bucket).apply(CfnBucketPropsMixin(CfnBucketMixinProps(versioning_configuration=CfnBucketPropsMixin.VersioningConfigurationProperty(status="Enabled")), strategy=PropertyMergeStrategy.MERGE))
            
            # OVERRIDE: Replaces existing property values
            Mixins.of(bucket).apply(CfnBucketPropsMixin(CfnBucketMixinProps(versioning_configuration=CfnBucketPropsMixin.VersioningConfigurationProperty(status="Enabled")), strategy=PropertyMergeStrategy.OVERRIDE))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9865ada8b2b5ada4c816d68c9dc18c8c68b5bdbb0c4a2c470b695c3a6ed861a1)
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if strategy is not None:
            self._values["strategy"] = strategy

    @builtins.property
    def strategy(self) -> typing.Optional["PropertyMergeStrategy"]:
        '''(experimental) Strategy for merging nested properties.

        :default: - PropertyMergeStrategy.MERGE

        :stability: experimental
        '''
        result = self._values.get("strategy")
        return typing.cast(typing.Optional["PropertyMergeStrategy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPropertyMixinOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/mixins-preview.mixins.PropertyMergeStrategy")
class PropertyMergeStrategy(enum.Enum):
    '''(experimental) Strategy for handling nested properties in L1 property mixins.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # bucket: s3.CfnBucket
        
        
        # MERGE (default): Deep merges properties with existing values
        Mixins.of(bucket).apply(CfnBucketPropsMixin(CfnBucketMixinProps(versioning_configuration=CfnBucketPropsMixin.VersioningConfigurationProperty(status="Enabled")), strategy=PropertyMergeStrategy.MERGE))
        
        # OVERRIDE: Replaces existing property values
        Mixins.of(bucket).apply(CfnBucketPropsMixin(CfnBucketMixinProps(versioning_configuration=CfnBucketPropsMixin.VersioningConfigurationProperty(status="Enabled")), strategy=PropertyMergeStrategy.OVERRIDE))
    '''

    OVERRIDE = "OVERRIDE"
    '''(experimental) Override all properties.

    :stability: experimental
    '''
    MERGE = "MERGE"
    '''(experimental) Deep merge nested objects, override primitives and arrays.

    :stability: experimental
    '''


__all__ = [
    "CfnPropertyMixinOptions",
    "PropertyMergeStrategy",
]

publication.publish()

def _typecheckingstub__9865ada8b2b5ada4c816d68c9dc18c8c68b5bdbb0c4a2c470b695c3a6ed861a1(
    *,
    strategy: typing.Optional[PropertyMergeStrategy] = None,
) -> None:
    """Type checking stubs"""
    pass
