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
    jsii_type="@aws-cdk/mixins-preview.aws_omics.mixins.CfnAnnotationStoreMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "name": "name",
        "reference": "reference",
        "sse_config": "sseConfig",
        "store_format": "storeFormat",
        "store_options": "storeOptions",
        "tags": "tags",
    },
)
class CfnAnnotationStoreMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        reference: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnnotationStorePropsMixin.ReferenceItemProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        sse_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnnotationStorePropsMixin.SseConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        store_format: typing.Optional[builtins.str] = None,
        store_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnnotationStorePropsMixin.StoreOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnAnnotationStorePropsMixin.

        :param description: A description for the store.
        :param name: The name of the Annotation Store.
        :param reference: The genome reference for the store's annotations.
        :param sse_config: The store's server-side encryption (SSE) settings.
        :param store_format: The annotation file format of the store.
        :param store_options: File parsing options for the annotation store.
        :param tags: Tags for the store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-annotationstore.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_omics import mixins as omics_mixins
            
            # schema: Any
            
            cfn_annotation_store_mixin_props = omics_mixins.CfnAnnotationStoreMixinProps(
                description="description",
                name="name",
                reference=omics_mixins.CfnAnnotationStorePropsMixin.ReferenceItemProperty(
                    reference_arn="referenceArn"
                ),
                sse_config=omics_mixins.CfnAnnotationStorePropsMixin.SseConfigProperty(
                    key_arn="keyArn",
                    type="type"
                ),
                store_format="storeFormat",
                store_options=omics_mixins.CfnAnnotationStorePropsMixin.StoreOptionsProperty(
                    tsv_store_options=omics_mixins.CfnAnnotationStorePropsMixin.TsvStoreOptionsProperty(
                        annotation_type="annotationType",
                        format_to_header={
                            "format_to_header_key": "formatToHeader"
                        },
                        schema=schema
                    )
                ),
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fd1930d504019f85b2d4f5f092b3bf4ebcb5467e30d7ce356687164fd5d2596)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument reference", value=reference, expected_type=type_hints["reference"])
            check_type(argname="argument sse_config", value=sse_config, expected_type=type_hints["sse_config"])
            check_type(argname="argument store_format", value=store_format, expected_type=type_hints["store_format"])
            check_type(argname="argument store_options", value=store_options, expected_type=type_hints["store_options"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if reference is not None:
            self._values["reference"] = reference
        if sse_config is not None:
            self._values["sse_config"] = sse_config
        if store_format is not None:
            self._values["store_format"] = store_format
        if store_options is not None:
            self._values["store_options"] = store_options
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-annotationstore.html#cfn-omics-annotationstore-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the Annotation Store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-annotationstore.html#cfn-omics-annotationstore-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reference(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnnotationStorePropsMixin.ReferenceItemProperty"]]:
        '''The genome reference for the store's annotations.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-annotationstore.html#cfn-omics-annotationstore-reference
        '''
        result = self._values.get("reference")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnnotationStorePropsMixin.ReferenceItemProperty"]], result)

    @builtins.property
    def sse_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnnotationStorePropsMixin.SseConfigProperty"]]:
        '''The store's server-side encryption (SSE) settings.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-annotationstore.html#cfn-omics-annotationstore-sseconfig
        '''
        result = self._values.get("sse_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnnotationStorePropsMixin.SseConfigProperty"]], result)

    @builtins.property
    def store_format(self) -> typing.Optional[builtins.str]:
        '''The annotation file format of the store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-annotationstore.html#cfn-omics-annotationstore-storeformat
        '''
        result = self._values.get("store_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def store_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnnotationStorePropsMixin.StoreOptionsProperty"]]:
        '''File parsing options for the annotation store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-annotationstore.html#cfn-omics-annotationstore-storeoptions
        '''
        result = self._values.get("store_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnnotationStorePropsMixin.StoreOptionsProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Tags for the store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-annotationstore.html#cfn-omics-annotationstore-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAnnotationStoreMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAnnotationStorePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_omics.mixins.CfnAnnotationStorePropsMixin",
):
    '''.. epigraph::

   AWS HealthOmics variant stores and annotation stores are no longer open to new customers.

    Existing customers can continue to use the service as normal. For more information, see `AWS HealthOmics variant store and annotation store availability change <https://docs.aws.amazon.com/omics/latest/dev/variant-store-availability-change.html>`_ .

    Creates an annotation store.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-annotationstore.html
    :cloudformationResource: AWS::Omics::AnnotationStore
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_omics import mixins as omics_mixins
        
        # schema: Any
        
        cfn_annotation_store_props_mixin = omics_mixins.CfnAnnotationStorePropsMixin(omics_mixins.CfnAnnotationStoreMixinProps(
            description="description",
            name="name",
            reference=omics_mixins.CfnAnnotationStorePropsMixin.ReferenceItemProperty(
                reference_arn="referenceArn"
            ),
            sse_config=omics_mixins.CfnAnnotationStorePropsMixin.SseConfigProperty(
                key_arn="keyArn",
                type="type"
            ),
            store_format="storeFormat",
            store_options=omics_mixins.CfnAnnotationStorePropsMixin.StoreOptionsProperty(
                tsv_store_options=omics_mixins.CfnAnnotationStorePropsMixin.TsvStoreOptionsProperty(
                    annotation_type="annotationType",
                    format_to_header={
                        "format_to_header_key": "formatToHeader"
                    },
                    schema=schema
                )
            ),
            tags={
                "tags_key": "tags"
            }
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAnnotationStoreMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Omics::AnnotationStore``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffaa0ceb2e260e4b97b90f7226274ff4b656203315922e8a97de77a1457c0ce3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ffe126b7d5e1ebc80014efa43c2ccf2e7c197849e25d2398c5590a7b6672ca5)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2a72490bf6a1e859fe0e8a3a9a6d0751fb684ad04f4030220ebdae40df84dea)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAnnotationStoreMixinProps:
        return typing.cast(CfnAnnotationStoreMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_omics.mixins.CfnAnnotationStorePropsMixin.ReferenceItemProperty",
        jsii_struct_bases=[],
        name_mapping={"reference_arn": "referenceArn"},
    )
    class ReferenceItemProperty:
        def __init__(
            self,
            *,
            reference_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A genome reference.

            :param reference_arn: The reference's ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-annotationstore-referenceitem.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_omics import mixins as omics_mixins
                
                reference_item_property = omics_mixins.CfnAnnotationStorePropsMixin.ReferenceItemProperty(
                    reference_arn="referenceArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__88ec759af4fca909790631365468237109cb84de41d2990a6b77d2ab7a41cf61)
                check_type(argname="argument reference_arn", value=reference_arn, expected_type=type_hints["reference_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if reference_arn is not None:
                self._values["reference_arn"] = reference_arn

        @builtins.property
        def reference_arn(self) -> typing.Optional[builtins.str]:
            '''The reference's ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-annotationstore-referenceitem.html#cfn-omics-annotationstore-referenceitem-referencearn
            '''
            result = self._values.get("reference_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReferenceItemProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_omics.mixins.CfnAnnotationStorePropsMixin.SseConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"key_arn": "keyArn", "type": "type"},
    )
    class SseConfigProperty:
        def __init__(
            self,
            *,
            key_arn: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Server-side encryption (SSE) settings for a store.

            :param key_arn: An encryption key ARN.
            :param type: The encryption type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-annotationstore-sseconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_omics import mixins as omics_mixins
                
                sse_config_property = omics_mixins.CfnAnnotationStorePropsMixin.SseConfigProperty(
                    key_arn="keyArn",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5a93b4feb4760350e32723c91cf69e21702b85e0aa0986302b40543845774eb0)
                check_type(argname="argument key_arn", value=key_arn, expected_type=type_hints["key_arn"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key_arn is not None:
                self._values["key_arn"] = key_arn
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def key_arn(self) -> typing.Optional[builtins.str]:
            '''An encryption key ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-annotationstore-sseconfig.html#cfn-omics-annotationstore-sseconfig-keyarn
            '''
            result = self._values.get("key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The encryption type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-annotationstore-sseconfig.html#cfn-omics-annotationstore-sseconfig-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SseConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_omics.mixins.CfnAnnotationStorePropsMixin.StoreOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"tsv_store_options": "tsvStoreOptions"},
    )
    class StoreOptionsProperty:
        def __init__(
            self,
            *,
            tsv_store_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnnotationStorePropsMixin.TsvStoreOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The store's file parsing options.

            :param tsv_store_options: Formatting options for a TSV file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-annotationstore-storeoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_omics import mixins as omics_mixins
                
                # schema: Any
                
                store_options_property = omics_mixins.CfnAnnotationStorePropsMixin.StoreOptionsProperty(
                    tsv_store_options=omics_mixins.CfnAnnotationStorePropsMixin.TsvStoreOptionsProperty(
                        annotation_type="annotationType",
                        format_to_header={
                            "format_to_header_key": "formatToHeader"
                        },
                        schema=schema
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d57283f116b5ff96110bdf1ffa762216da84abd236f1c0cff3a3562122fe8d46)
                check_type(argname="argument tsv_store_options", value=tsv_store_options, expected_type=type_hints["tsv_store_options"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if tsv_store_options is not None:
                self._values["tsv_store_options"] = tsv_store_options

        @builtins.property
        def tsv_store_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnnotationStorePropsMixin.TsvStoreOptionsProperty"]]:
            '''Formatting options for a TSV file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-annotationstore-storeoptions.html#cfn-omics-annotationstore-storeoptions-tsvstoreoptions
            '''
            result = self._values.get("tsv_store_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnnotationStorePropsMixin.TsvStoreOptionsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StoreOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_omics.mixins.CfnAnnotationStorePropsMixin.TsvStoreOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "annotation_type": "annotationType",
            "format_to_header": "formatToHeader",
            "schema": "schema",
        },
    )
    class TsvStoreOptionsProperty:
        def __init__(
            self,
            *,
            annotation_type: typing.Optional[builtins.str] = None,
            format_to_header: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            schema: typing.Any = None,
        ) -> None:
            '''The store's parsing options.

            :param annotation_type: The store's annotation type.
            :param format_to_header: The store's header key to column name mapping.
            :param schema: The schema of an annotation store.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-annotationstore-tsvstoreoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_omics import mixins as omics_mixins
                
                # schema: Any
                
                tsv_store_options_property = omics_mixins.CfnAnnotationStorePropsMixin.TsvStoreOptionsProperty(
                    annotation_type="annotationType",
                    format_to_header={
                        "format_to_header_key": "formatToHeader"
                    },
                    schema=schema
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__58697273262149196841fe6d9baf4798e156827c6fd15f074d97fb9c4a79cd0a)
                check_type(argname="argument annotation_type", value=annotation_type, expected_type=type_hints["annotation_type"])
                check_type(argname="argument format_to_header", value=format_to_header, expected_type=type_hints["format_to_header"])
                check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if annotation_type is not None:
                self._values["annotation_type"] = annotation_type
            if format_to_header is not None:
                self._values["format_to_header"] = format_to_header
            if schema is not None:
                self._values["schema"] = schema

        @builtins.property
        def annotation_type(self) -> typing.Optional[builtins.str]:
            '''The store's annotation type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-annotationstore-tsvstoreoptions.html#cfn-omics-annotationstore-tsvstoreoptions-annotationtype
            '''
            result = self._values.get("annotation_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def format_to_header(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''The store's header key to column name mapping.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-annotationstore-tsvstoreoptions.html#cfn-omics-annotationstore-tsvstoreoptions-formattoheader
            '''
            result = self._values.get("format_to_header")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def schema(self) -> typing.Any:
            '''The schema of an annotation store.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-annotationstore-tsvstoreoptions.html#cfn-omics-annotationstore-tsvstoreoptions-schema
            '''
            result = self._values.get("schema")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TsvStoreOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_omics.mixins.CfnReferenceStoreMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "name": "name",
        "sse_config": "sseConfig",
        "tags": "tags",
    },
)
class CfnReferenceStoreMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        sse_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnReferenceStorePropsMixin.SseConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnReferenceStorePropsMixin.

        :param description: A description for the store.
        :param name: A name for the store.
        :param sse_config: Server-side encryption (SSE) settings for the store.
        :param tags: Tags for the store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-referencestore.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_omics import mixins as omics_mixins
            
            cfn_reference_store_mixin_props = omics_mixins.CfnReferenceStoreMixinProps(
                description="description",
                name="name",
                sse_config=omics_mixins.CfnReferenceStorePropsMixin.SseConfigProperty(
                    key_arn="keyArn",
                    type="type"
                ),
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08d373682e15ba8f7650ae17944f60651c594b6060862cfa30b1bfae95d4d9be)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument sse_config", value=sse_config, expected_type=type_hints["sse_config"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if sse_config is not None:
            self._values["sse_config"] = sse_config
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-referencestore.html#cfn-omics-referencestore-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A name for the store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-referencestore.html#cfn-omics-referencestore-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sse_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReferenceStorePropsMixin.SseConfigProperty"]]:
        '''Server-side encryption (SSE) settings for the store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-referencestore.html#cfn-omics-referencestore-sseconfig
        '''
        result = self._values.get("sse_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReferenceStorePropsMixin.SseConfigProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Tags for the store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-referencestore.html#cfn-omics-referencestore-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnReferenceStoreMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnReferenceStorePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_omics.mixins.CfnReferenceStorePropsMixin",
):
    '''Creates a reference store.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-referencestore.html
    :cloudformationResource: AWS::Omics::ReferenceStore
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_omics import mixins as omics_mixins
        
        cfn_reference_store_props_mixin = omics_mixins.CfnReferenceStorePropsMixin(omics_mixins.CfnReferenceStoreMixinProps(
            description="description",
            name="name",
            sse_config=omics_mixins.CfnReferenceStorePropsMixin.SseConfigProperty(
                key_arn="keyArn",
                type="type"
            ),
            tags={
                "tags_key": "tags"
            }
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnReferenceStoreMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Omics::ReferenceStore``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f3a1cf2336bc81f5cb5c2b72433504b3f3ee5c0faf70ee508dd63640e8799a0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a844aaa6c531e1c6feb54548e39cb8599cd81cb409bfc4d114b7bcea2a066e1f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f545595f6a2bc2f1a080f20a5fcd929f409164d65f3de851372922c777288711)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnReferenceStoreMixinProps:
        return typing.cast(CfnReferenceStoreMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_omics.mixins.CfnReferenceStorePropsMixin.SseConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"key_arn": "keyArn", "type": "type"},
    )
    class SseConfigProperty:
        def __init__(
            self,
            *,
            key_arn: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Server-side encryption (SSE) settings for a store.

            :param key_arn: An encryption key ARN.
            :param type: The encryption type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-referencestore-sseconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_omics import mixins as omics_mixins
                
                sse_config_property = omics_mixins.CfnReferenceStorePropsMixin.SseConfigProperty(
                    key_arn="keyArn",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7678d4c65dd8c5358fbd8fe0791d1a7a45f06d8039962aef0ae51cd7c5530d48)
                check_type(argname="argument key_arn", value=key_arn, expected_type=type_hints["key_arn"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key_arn is not None:
                self._values["key_arn"] = key_arn
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def key_arn(self) -> typing.Optional[builtins.str]:
            '''An encryption key ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-referencestore-sseconfig.html#cfn-omics-referencestore-sseconfig-keyarn
            '''
            result = self._values.get("key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The encryption type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-referencestore-sseconfig.html#cfn-omics-referencestore-sseconfig-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SseConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_omics.mixins.CfnRunGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "max_cpus": "maxCpus",
        "max_duration": "maxDuration",
        "max_gpus": "maxGpus",
        "max_runs": "maxRuns",
        "name": "name",
        "tags": "tags",
    },
)
class CfnRunGroupMixinProps:
    def __init__(
        self,
        *,
        max_cpus: typing.Optional[jsii.Number] = None,
        max_duration: typing.Optional[jsii.Number] = None,
        max_gpus: typing.Optional[jsii.Number] = None,
        max_runs: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnRunGroupPropsMixin.

        :param max_cpus: The group's maximum CPU count setting.
        :param max_duration: The group's maximum duration setting in minutes.
        :param max_gpus: The maximum GPUs that can be used by a run group.
        :param max_runs: The group's maximum concurrent run setting.
        :param name: The group's name.
        :param tags: Tags for the group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-rungroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_omics import mixins as omics_mixins
            
            cfn_run_group_mixin_props = omics_mixins.CfnRunGroupMixinProps(
                max_cpus=123,
                max_duration=123,
                max_gpus=123,
                max_runs=123,
                name="name",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fe9859866cf051f02716000b295c2d7e4aa3a604565dd6e013ade7ecea38dda)
            check_type(argname="argument max_cpus", value=max_cpus, expected_type=type_hints["max_cpus"])
            check_type(argname="argument max_duration", value=max_duration, expected_type=type_hints["max_duration"])
            check_type(argname="argument max_gpus", value=max_gpus, expected_type=type_hints["max_gpus"])
            check_type(argname="argument max_runs", value=max_runs, expected_type=type_hints["max_runs"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_cpus is not None:
            self._values["max_cpus"] = max_cpus
        if max_duration is not None:
            self._values["max_duration"] = max_duration
        if max_gpus is not None:
            self._values["max_gpus"] = max_gpus
        if max_runs is not None:
            self._values["max_runs"] = max_runs
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def max_cpus(self) -> typing.Optional[jsii.Number]:
        '''The group's maximum CPU count setting.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-rungroup.html#cfn-omics-rungroup-maxcpus
        '''
        result = self._values.get("max_cpus")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_duration(self) -> typing.Optional[jsii.Number]:
        '''The group's maximum duration setting in minutes.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-rungroup.html#cfn-omics-rungroup-maxduration
        '''
        result = self._values.get("max_duration")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_gpus(self) -> typing.Optional[jsii.Number]:
        '''The maximum GPUs that can be used by a run group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-rungroup.html#cfn-omics-rungroup-maxgpus
        '''
        result = self._values.get("max_gpus")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_runs(self) -> typing.Optional[jsii.Number]:
        '''The group's maximum concurrent run setting.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-rungroup.html#cfn-omics-rungroup-maxruns
        '''
        result = self._values.get("max_runs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The group's name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-rungroup.html#cfn-omics-rungroup-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Tags for the group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-rungroup.html#cfn-omics-rungroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRunGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnRunGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_omics.mixins.CfnRunGroupPropsMixin",
):
    '''Creates a run group to limit the compute resources for the runs that are added to the group.

    Returns an ARN, ID, and tags for the run group.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-rungroup.html
    :cloudformationResource: AWS::Omics::RunGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_omics import mixins as omics_mixins
        
        cfn_run_group_props_mixin = omics_mixins.CfnRunGroupPropsMixin(omics_mixins.CfnRunGroupMixinProps(
            max_cpus=123,
            max_duration=123,
            max_gpus=123,
            max_runs=123,
            name="name",
            tags={
                "tags_key": "tags"
            }
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnRunGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Omics::RunGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__644d1c24db634ad86dcb8b3c2b03c354596d676573943c00fff74a8b1afe935f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d2b75a7c5159ec80ae0456fbb2e91cfa73d4b4a2045c44a3cb84d5028c501b0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fd6edd4b58411606dc3003beabc7b183c0a01c44de00efb07d1fb996d7be874)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnRunGroupMixinProps:
        return typing.cast(CfnRunGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_omics.mixins.CfnSequenceStoreMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_log_location": "accessLogLocation",
        "description": "description",
        "e_tag_algorithm_family": "eTagAlgorithmFamily",
        "fallback_location": "fallbackLocation",
        "name": "name",
        "propagated_set_level_tags": "propagatedSetLevelTags",
        "s3_access_policy": "s3AccessPolicy",
        "sse_config": "sseConfig",
        "tags": "tags",
    },
)
class CfnSequenceStoreMixinProps:
    def __init__(
        self,
        *,
        access_log_location: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        e_tag_algorithm_family: typing.Optional[builtins.str] = None,
        fallback_location: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        propagated_set_level_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        s3_access_policy: typing.Any = None,
        sse_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSequenceStorePropsMixin.SseConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnSequenceStorePropsMixin.

        :param access_log_location: Location of the access logs.
        :param description: A description for the store.
        :param e_tag_algorithm_family: The algorithm family of the ETag.
        :param fallback_location: An S3 location that is used to store files that have failed a direct upload.
        :param name: A name for the store.
        :param propagated_set_level_tags: The tags keys to propagate to the S3 objects associated with read sets in the sequence store.
        :param s3_access_policy: The resource policy that controls S3 access on the store.
        :param sse_config: Server-side encryption (SSE) settings for the store.
        :param tags: Tags for the store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-sequencestore.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_omics import mixins as omics_mixins
            
            # s3_access_policy: Any
            
            cfn_sequence_store_mixin_props = omics_mixins.CfnSequenceStoreMixinProps(
                access_log_location="accessLogLocation",
                description="description",
                e_tag_algorithm_family="eTagAlgorithmFamily",
                fallback_location="fallbackLocation",
                name="name",
                propagated_set_level_tags=["propagatedSetLevelTags"],
                s3_access_policy=s3_access_policy,
                sse_config=omics_mixins.CfnSequenceStorePropsMixin.SseConfigProperty(
                    key_arn="keyArn",
                    type="type"
                ),
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e50fdeb3f1a17a7c134d4fbc5390a39229fcbd4b49e1dec67ced238c418f8f0)
            check_type(argname="argument access_log_location", value=access_log_location, expected_type=type_hints["access_log_location"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument e_tag_algorithm_family", value=e_tag_algorithm_family, expected_type=type_hints["e_tag_algorithm_family"])
            check_type(argname="argument fallback_location", value=fallback_location, expected_type=type_hints["fallback_location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument propagated_set_level_tags", value=propagated_set_level_tags, expected_type=type_hints["propagated_set_level_tags"])
            check_type(argname="argument s3_access_policy", value=s3_access_policy, expected_type=type_hints["s3_access_policy"])
            check_type(argname="argument sse_config", value=sse_config, expected_type=type_hints["sse_config"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_log_location is not None:
            self._values["access_log_location"] = access_log_location
        if description is not None:
            self._values["description"] = description
        if e_tag_algorithm_family is not None:
            self._values["e_tag_algorithm_family"] = e_tag_algorithm_family
        if fallback_location is not None:
            self._values["fallback_location"] = fallback_location
        if name is not None:
            self._values["name"] = name
        if propagated_set_level_tags is not None:
            self._values["propagated_set_level_tags"] = propagated_set_level_tags
        if s3_access_policy is not None:
            self._values["s3_access_policy"] = s3_access_policy
        if sse_config is not None:
            self._values["sse_config"] = sse_config
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def access_log_location(self) -> typing.Optional[builtins.str]:
        '''Location of the access logs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-sequencestore.html#cfn-omics-sequencestore-accessloglocation
        '''
        result = self._values.get("access_log_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-sequencestore.html#cfn-omics-sequencestore-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def e_tag_algorithm_family(self) -> typing.Optional[builtins.str]:
        '''The algorithm family of the ETag.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-sequencestore.html#cfn-omics-sequencestore-etagalgorithmfamily
        '''
        result = self._values.get("e_tag_algorithm_family")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fallback_location(self) -> typing.Optional[builtins.str]:
        '''An S3 location that is used to store files that have failed a direct upload.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-sequencestore.html#cfn-omics-sequencestore-fallbacklocation
        '''
        result = self._values.get("fallback_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A name for the store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-sequencestore.html#cfn-omics-sequencestore-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def propagated_set_level_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The tags keys to propagate to the S3 objects associated with read sets in the sequence store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-sequencestore.html#cfn-omics-sequencestore-propagatedsetleveltags
        '''
        result = self._values.get("propagated_set_level_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def s3_access_policy(self) -> typing.Any:
        '''The resource policy that controls S3 access on the store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-sequencestore.html#cfn-omics-sequencestore-s3accesspolicy
        '''
        result = self._values.get("s3_access_policy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def sse_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSequenceStorePropsMixin.SseConfigProperty"]]:
        '''Server-side encryption (SSE) settings for the store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-sequencestore.html#cfn-omics-sequencestore-sseconfig
        '''
        result = self._values.get("sse_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSequenceStorePropsMixin.SseConfigProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Tags for the store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-sequencestore.html#cfn-omics-sequencestore-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSequenceStoreMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSequenceStorePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_omics.mixins.CfnSequenceStorePropsMixin",
):
    '''Creates a sequence store.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-sequencestore.html
    :cloudformationResource: AWS::Omics::SequenceStore
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_omics import mixins as omics_mixins
        
        # s3_access_policy: Any
        
        cfn_sequence_store_props_mixin = omics_mixins.CfnSequenceStorePropsMixin(omics_mixins.CfnSequenceStoreMixinProps(
            access_log_location="accessLogLocation",
            description="description",
            e_tag_algorithm_family="eTagAlgorithmFamily",
            fallback_location="fallbackLocation",
            name="name",
            propagated_set_level_tags=["propagatedSetLevelTags"],
            s3_access_policy=s3_access_policy,
            sse_config=omics_mixins.CfnSequenceStorePropsMixin.SseConfigProperty(
                key_arn="keyArn",
                type="type"
            ),
            tags={
                "tags_key": "tags"
            }
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnSequenceStoreMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Omics::SequenceStore``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__034f622df244678961755e12f0d198ffc4435b8b12cc142ef015cf4e60a0ac3e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9dff85d1f5c8d4f0bdd6a056d4dee51a2d788dea513ee8cf1099ca0da8394d7c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__085a7483715ba6e727c69cd2398672e07d706a40cab9a275e5dbfe120b552d45)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSequenceStoreMixinProps:
        return typing.cast(CfnSequenceStoreMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_omics.mixins.CfnSequenceStorePropsMixin.SseConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"key_arn": "keyArn", "type": "type"},
    )
    class SseConfigProperty:
        def __init__(
            self,
            *,
            key_arn: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Server-side encryption (SSE) settings for a store.

            :param key_arn: An encryption key ARN.
            :param type: The encryption type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-sequencestore-sseconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_omics import mixins as omics_mixins
                
                sse_config_property = omics_mixins.CfnSequenceStorePropsMixin.SseConfigProperty(
                    key_arn="keyArn",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2071ecc260c3fba581a7ba46761e6a2e5aa1f3314e8eceb5cc6a00b29b29bbdc)
                check_type(argname="argument key_arn", value=key_arn, expected_type=type_hints["key_arn"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key_arn is not None:
                self._values["key_arn"] = key_arn
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def key_arn(self) -> typing.Optional[builtins.str]:
            '''An encryption key ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-sequencestore-sseconfig.html#cfn-omics-sequencestore-sseconfig-keyarn
            '''
            result = self._values.get("key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The encryption type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-sequencestore-sseconfig.html#cfn-omics-sequencestore-sseconfig-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SseConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_omics.mixins.CfnVariantStoreMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "name": "name",
        "reference": "reference",
        "sse_config": "sseConfig",
        "tags": "tags",
    },
)
class CfnVariantStoreMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        reference: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVariantStorePropsMixin.ReferenceItemProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        sse_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVariantStorePropsMixin.SseConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnVariantStorePropsMixin.

        :param description: A description for the store.
        :param name: A name for the store.
        :param reference: The genome reference for the store's variants.
        :param sse_config: Server-side encryption (SSE) settings for the store.
        :param tags: Tags for the store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-variantstore.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_omics import mixins as omics_mixins
            
            cfn_variant_store_mixin_props = omics_mixins.CfnVariantStoreMixinProps(
                description="description",
                name="name",
                reference=omics_mixins.CfnVariantStorePropsMixin.ReferenceItemProperty(
                    reference_arn="referenceArn"
                ),
                sse_config=omics_mixins.CfnVariantStorePropsMixin.SseConfigProperty(
                    key_arn="keyArn",
                    type="type"
                ),
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f3fb40c2dbe210e1fcce9e4baee95d8ad31a753546e7471faf54c3dede9471d)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument reference", value=reference, expected_type=type_hints["reference"])
            check_type(argname="argument sse_config", value=sse_config, expected_type=type_hints["sse_config"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if reference is not None:
            self._values["reference"] = reference
        if sse_config is not None:
            self._values["sse_config"] = sse_config
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-variantstore.html#cfn-omics-variantstore-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A name for the store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-variantstore.html#cfn-omics-variantstore-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reference(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVariantStorePropsMixin.ReferenceItemProperty"]]:
        '''The genome reference for the store's variants.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-variantstore.html#cfn-omics-variantstore-reference
        '''
        result = self._values.get("reference")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVariantStorePropsMixin.ReferenceItemProperty"]], result)

    @builtins.property
    def sse_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVariantStorePropsMixin.SseConfigProperty"]]:
        '''Server-side encryption (SSE) settings for the store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-variantstore.html#cfn-omics-variantstore-sseconfig
        '''
        result = self._values.get("sse_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVariantStorePropsMixin.SseConfigProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Tags for the store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-variantstore.html#cfn-omics-variantstore-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVariantStoreMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnVariantStorePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_omics.mixins.CfnVariantStorePropsMixin",
):
    '''Create a store for variant data.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-variantstore.html
    :cloudformationResource: AWS::Omics::VariantStore
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_omics import mixins as omics_mixins
        
        cfn_variant_store_props_mixin = omics_mixins.CfnVariantStorePropsMixin(omics_mixins.CfnVariantStoreMixinProps(
            description="description",
            name="name",
            reference=omics_mixins.CfnVariantStorePropsMixin.ReferenceItemProperty(
                reference_arn="referenceArn"
            ),
            sse_config=omics_mixins.CfnVariantStorePropsMixin.SseConfigProperty(
                key_arn="keyArn",
                type="type"
            ),
            tags={
                "tags_key": "tags"
            }
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnVariantStoreMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Omics::VariantStore``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e17b8ea2c7e45651b20aefc47cff22b5b19e88c136ab3f18db830671fd3bb8ed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__710ad934ede7ae69b91a77ab33aabf42f24ec976cb2e36d4a2a4b01b1f19f3bf)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fab8c7e5f4dc8a49dcbae0d5b01fed7c8137bd1ebaa875df758ff7c3d8096ba9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnVariantStoreMixinProps:
        return typing.cast(CfnVariantStoreMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_omics.mixins.CfnVariantStorePropsMixin.ReferenceItemProperty",
        jsii_struct_bases=[],
        name_mapping={"reference_arn": "referenceArn"},
    )
    class ReferenceItemProperty:
        def __init__(
            self,
            *,
            reference_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The read set's genome reference ARN.

            :param reference_arn: The reference's ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-variantstore-referenceitem.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_omics import mixins as omics_mixins
                
                reference_item_property = omics_mixins.CfnVariantStorePropsMixin.ReferenceItemProperty(
                    reference_arn="referenceArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__70d4747cd289a01303759c5fd0c0d87281d659a02ebc7b99b0a9c30ac5c9254c)
                check_type(argname="argument reference_arn", value=reference_arn, expected_type=type_hints["reference_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if reference_arn is not None:
                self._values["reference_arn"] = reference_arn

        @builtins.property
        def reference_arn(self) -> typing.Optional[builtins.str]:
            '''The reference's ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-variantstore-referenceitem.html#cfn-omics-variantstore-referenceitem-referencearn
            '''
            result = self._values.get("reference_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReferenceItemProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_omics.mixins.CfnVariantStorePropsMixin.SseConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"key_arn": "keyArn", "type": "type"},
    )
    class SseConfigProperty:
        def __init__(
            self,
            *,
            key_arn: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Server-side encryption (SSE) settings for a store.

            :param key_arn: An encryption key ARN.
            :param type: The encryption type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-variantstore-sseconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_omics import mixins as omics_mixins
                
                sse_config_property = omics_mixins.CfnVariantStorePropsMixin.SseConfigProperty(
                    key_arn="keyArn",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3c31a6e65a7dc2b9cde211ac816a12798d4386e7ee26eee153e898be3bbc2814)
                check_type(argname="argument key_arn", value=key_arn, expected_type=type_hints["key_arn"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key_arn is not None:
                self._values["key_arn"] = key_arn
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def key_arn(self) -> typing.Optional[builtins.str]:
            '''An encryption key ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-variantstore-sseconfig.html#cfn-omics-variantstore-sseconfig-keyarn
            '''
            result = self._values.get("key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The encryption type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-variantstore-sseconfig.html#cfn-omics-variantstore-sseconfig-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SseConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_omics.mixins.CfnWorkflowMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "accelerators": "accelerators",
        "container_registry_map": "containerRegistryMap",
        "container_registry_map_uri": "containerRegistryMapUri",
        "definition_repository": "definitionRepository",
        "definition_uri": "definitionUri",
        "description": "description",
        "engine": "engine",
        "main": "main",
        "name": "name",
        "parameter_template": "parameterTemplate",
        "parameter_template_path": "parameterTemplatePath",
        "readme_markdown": "readmeMarkdown",
        "readme_path": "readmePath",
        "readme_uri": "readmeUri",
        "storage_capacity": "storageCapacity",
        "storage_type": "storageType",
        "tags": "tags",
        "workflow_bucket_owner_id": "workflowBucketOwnerId",
    },
)
class CfnWorkflowMixinProps:
    def __init__(
        self,
        *,
        accelerators: typing.Optional[builtins.str] = None,
        container_registry_map: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkflowPropsMixin.ContainerRegistryMapProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        container_registry_map_uri: typing.Optional[builtins.str] = None,
        definition_repository: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkflowPropsMixin.DefinitionRepositoryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        definition_uri: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        engine: typing.Optional[builtins.str] = None,
        main: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        parameter_template: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkflowPropsMixin.WorkflowParameterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        parameter_template_path: typing.Optional[builtins.str] = None,
        readme_markdown: typing.Optional[builtins.str] = None,
        readme_path: typing.Optional[builtins.str] = None,
        readme_uri: typing.Optional[builtins.str] = None,
        storage_capacity: typing.Optional[jsii.Number] = None,
        storage_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        workflow_bucket_owner_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnWorkflowPropsMixin.

        :param accelerators: 
        :param container_registry_map: Use a container registry map to specify mappings between the ECR private repository and one or more upstream registries. For more information, see `Container images <https://docs.aws.amazon.com/omics/latest/dev/workflows-ecr.html>`_ in the *AWS HealthOmics User Guide* .
        :param container_registry_map_uri: 
        :param definition_repository: Contains information about a source code repository that hosts the workflow definition files.
        :param definition_uri: The URI of a definition for the workflow.
        :param description: The parameter's description.
        :param engine: An engine for the workflow.
        :param main: The path of the main definition file for the workflow.
        :param name: The workflow's name.
        :param parameter_template: The workflow's parameter template.
        :param parameter_template_path: Path to the primary workflow parameter template JSON file inside the repository.
        :param readme_markdown: The markdown content for the workflow's README file. This provides documentation and usage information for users of the workflow.
        :param readme_path: The path to the workflow README markdown file within the repository. This file provides documentation and usage information for the workflow. If not specified, the README.md file from the root directory of the repository will be used.
        :param readme_uri: The S3 URI of the README file for the workflow. This file provides documentation and usage information for the workflow. The S3 URI must begin with s3://USER-OWNED-BUCKET/. The requester must have access to the S3 bucket and object. The max README content length is 500 KiB.
        :param storage_capacity: The default static storage capacity (in gibibytes) for runs that use this workflow or workflow version. The ``storageCapacity`` can be overwritten at run time. The storage capacity is not required for runs with a ``DYNAMIC`` storage type.
        :param storage_type: 
        :param tags: Tags for the workflow.
        :param workflow_bucket_owner_id: Optional workflow bucket owner ID to verify the workflow bucket.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflow.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_omics import mixins as omics_mixins
            
            cfn_workflow_mixin_props = omics_mixins.CfnWorkflowMixinProps(
                accelerators="accelerators",
                container_registry_map=omics_mixins.CfnWorkflowPropsMixin.ContainerRegistryMapProperty(
                    image_mappings=[omics_mixins.CfnWorkflowPropsMixin.ImageMappingProperty(
                        destination_image="destinationImage",
                        source_image="sourceImage"
                    )],
                    registry_mappings=[omics_mixins.CfnWorkflowPropsMixin.RegistryMappingProperty(
                        ecr_account_id="ecrAccountId",
                        ecr_repository_prefix="ecrRepositoryPrefix",
                        upstream_registry_url="upstreamRegistryUrl",
                        upstream_repository_prefix="upstreamRepositoryPrefix"
                    )]
                ),
                container_registry_map_uri="containerRegistryMapUri",
                definition_repository=omics_mixins.CfnWorkflowPropsMixin.DefinitionRepositoryProperty(
                    connection_arn="connectionArn",
                    exclude_file_patterns=["excludeFilePatterns"],
                    full_repository_id="fullRepositoryId",
                    source_reference=omics_mixins.CfnWorkflowPropsMixin.SourceReferenceProperty(
                        type="type",
                        value="value"
                    )
                ),
                definition_uri="definitionUri",
                description="description",
                engine="engine",
                main="main",
                name="name",
                parameter_template={
                    "parameter_template_key": omics_mixins.CfnWorkflowPropsMixin.WorkflowParameterProperty(
                        description="description",
                        optional=False
                    )
                },
                parameter_template_path="parameterTemplatePath",
                readme_markdown="readmeMarkdown",
                readme_path="readmePath",
                readme_uri="readmeUri",
                storage_capacity=123,
                storage_type="storageType",
                tags={
                    "tags_key": "tags"
                },
                workflow_bucket_owner_id="workflowBucketOwnerId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__438aacdaa1fbffa26ad2da00febb74751eaa467bf2e329a901375faa13d6d3ab)
            check_type(argname="argument accelerators", value=accelerators, expected_type=type_hints["accelerators"])
            check_type(argname="argument container_registry_map", value=container_registry_map, expected_type=type_hints["container_registry_map"])
            check_type(argname="argument container_registry_map_uri", value=container_registry_map_uri, expected_type=type_hints["container_registry_map_uri"])
            check_type(argname="argument definition_repository", value=definition_repository, expected_type=type_hints["definition_repository"])
            check_type(argname="argument definition_uri", value=definition_uri, expected_type=type_hints["definition_uri"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument engine", value=engine, expected_type=type_hints["engine"])
            check_type(argname="argument main", value=main, expected_type=type_hints["main"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument parameter_template", value=parameter_template, expected_type=type_hints["parameter_template"])
            check_type(argname="argument parameter_template_path", value=parameter_template_path, expected_type=type_hints["parameter_template_path"])
            check_type(argname="argument readme_markdown", value=readme_markdown, expected_type=type_hints["readme_markdown"])
            check_type(argname="argument readme_path", value=readme_path, expected_type=type_hints["readme_path"])
            check_type(argname="argument readme_uri", value=readme_uri, expected_type=type_hints["readme_uri"])
            check_type(argname="argument storage_capacity", value=storage_capacity, expected_type=type_hints["storage_capacity"])
            check_type(argname="argument storage_type", value=storage_type, expected_type=type_hints["storage_type"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument workflow_bucket_owner_id", value=workflow_bucket_owner_id, expected_type=type_hints["workflow_bucket_owner_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accelerators is not None:
            self._values["accelerators"] = accelerators
        if container_registry_map is not None:
            self._values["container_registry_map"] = container_registry_map
        if container_registry_map_uri is not None:
            self._values["container_registry_map_uri"] = container_registry_map_uri
        if definition_repository is not None:
            self._values["definition_repository"] = definition_repository
        if definition_uri is not None:
            self._values["definition_uri"] = definition_uri
        if description is not None:
            self._values["description"] = description
        if engine is not None:
            self._values["engine"] = engine
        if main is not None:
            self._values["main"] = main
        if name is not None:
            self._values["name"] = name
        if parameter_template is not None:
            self._values["parameter_template"] = parameter_template
        if parameter_template_path is not None:
            self._values["parameter_template_path"] = parameter_template_path
        if readme_markdown is not None:
            self._values["readme_markdown"] = readme_markdown
        if readme_path is not None:
            self._values["readme_path"] = readme_path
        if readme_uri is not None:
            self._values["readme_uri"] = readme_uri
        if storage_capacity is not None:
            self._values["storage_capacity"] = storage_capacity
        if storage_type is not None:
            self._values["storage_type"] = storage_type
        if tags is not None:
            self._values["tags"] = tags
        if workflow_bucket_owner_id is not None:
            self._values["workflow_bucket_owner_id"] = workflow_bucket_owner_id

    @builtins.property
    def accelerators(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflow.html#cfn-omics-workflow-accelerators
        '''
        result = self._values.get("accelerators")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def container_registry_map(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkflowPropsMixin.ContainerRegistryMapProperty"]]:
        '''Use a container registry map to specify mappings between the ECR private repository and one or more upstream registries.

        For more information, see `Container images <https://docs.aws.amazon.com/omics/latest/dev/workflows-ecr.html>`_ in the *AWS HealthOmics User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflow.html#cfn-omics-workflow-containerregistrymap
        '''
        result = self._values.get("container_registry_map")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkflowPropsMixin.ContainerRegistryMapProperty"]], result)

    @builtins.property
    def container_registry_map_uri(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflow.html#cfn-omics-workflow-containerregistrymapuri
        '''
        result = self._values.get("container_registry_map_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def definition_repository(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkflowPropsMixin.DefinitionRepositoryProperty"]]:
        '''Contains information about a source code repository that hosts the workflow definition files.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflow.html#cfn-omics-workflow-definitionrepository
        '''
        result = self._values.get("definition_repository")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkflowPropsMixin.DefinitionRepositoryProperty"]], result)

    @builtins.property
    def definition_uri(self) -> typing.Optional[builtins.str]:
        '''The URI of a definition for the workflow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflow.html#cfn-omics-workflow-definitionuri
        '''
        result = self._values.get("definition_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The parameter's description.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflow.html#cfn-omics-workflow-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def engine(self) -> typing.Optional[builtins.str]:
        '''An engine for the workflow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflow.html#cfn-omics-workflow-engine
        '''
        result = self._values.get("engine")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def main(self) -> typing.Optional[builtins.str]:
        '''The path of the main definition file for the workflow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflow.html#cfn-omics-workflow-main
        '''
        result = self._values.get("main")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The workflow's name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflow.html#cfn-omics-workflow-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameter_template(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkflowPropsMixin.WorkflowParameterProperty"]]]]:
        '''The workflow's parameter template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflow.html#cfn-omics-workflow-parametertemplate
        '''
        result = self._values.get("parameter_template")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkflowPropsMixin.WorkflowParameterProperty"]]]], result)

    @builtins.property
    def parameter_template_path(self) -> typing.Optional[builtins.str]:
        '''Path to the primary workflow parameter template JSON file inside the repository.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflow.html#cfn-omics-workflow-parametertemplatepath
        '''
        result = self._values.get("parameter_template_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def readme_markdown(self) -> typing.Optional[builtins.str]:
        '''The markdown content for the workflow's README file.

        This provides documentation and usage information for users of the workflow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflow.html#cfn-omics-workflow-readmemarkdown
        '''
        result = self._values.get("readme_markdown")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def readme_path(self) -> typing.Optional[builtins.str]:
        '''The path to the workflow README markdown file within the repository.

        This file provides documentation and usage information for the workflow. If not specified, the README.md file from the root directory of the repository will be used.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflow.html#cfn-omics-workflow-readmepath
        '''
        result = self._values.get("readme_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def readme_uri(self) -> typing.Optional[builtins.str]:
        '''The S3 URI of the README file for the workflow.

        This file provides documentation and usage information for the workflow. The S3 URI must begin with s3://USER-OWNED-BUCKET/. The requester must have access to the S3 bucket and object. The max README content length is 500 KiB.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflow.html#cfn-omics-workflow-readmeuri
        '''
        result = self._values.get("readme_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_capacity(self) -> typing.Optional[jsii.Number]:
        '''The default static storage capacity (in gibibytes) for runs that use this workflow or workflow version.

        The ``storageCapacity`` can be overwritten at run time. The storage capacity is not required for runs with a ``DYNAMIC`` storage type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflow.html#cfn-omics-workflow-storagecapacity
        '''
        result = self._values.get("storage_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def storage_type(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflow.html#cfn-omics-workflow-storagetype
        '''
        result = self._values.get("storage_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Tags for the workflow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflow.html#cfn-omics-workflow-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def workflow_bucket_owner_id(self) -> typing.Optional[builtins.str]:
        '''Optional workflow bucket owner ID to verify the workflow bucket.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflow.html#cfn-omics-workflow-workflowbucketownerid
        '''
        result = self._values.get("workflow_bucket_owner_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWorkflowMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnWorkflowPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_omics.mixins.CfnWorkflowPropsMixin",
):
    '''Creates a private workflow. Before you create a private workflow, you must create and configure these required resources:.

    - *Workflow definition file:* A workflow definition file written in WDL, Nextflow, or CWL. The workflow definition specifies the inputs and outputs for runs that use the workflow. It also includes specifications for the runs and run tasks for your workflow, including compute and memory requirements. The workflow definition file must be in ``.zip`` format. For more information, see `Workflow definition files <https://docs.aws.amazon.com/omics/latest/dev/workflow-definition-files.html>`_ in AWS HealthOmics.
    - You can use Amazon Q CLI to build and validate your workflow definition files in WDL, Nextflow, and CWL. For more information, see `Example prompts for Amazon Q CLI <https://docs.aws.amazon.com/omics/latest/dev/getting-started.html#omics-q-prompts>`_ and the `AWS HealthOmics Agentic generative AI tutorial <https://docs.aws.amazon.com/https://github.com/aws-samples/aws-healthomics-tutorials/tree/main/generative-ai>`_ on GitHub.
    - *(Optional) Parameter template file:* A parameter template file written in JSON. Create the file to define the run parameters, or AWS HealthOmics generates the parameter template for you. For more information, see `Parameter template files for HealthOmics workflows <https://docs.aws.amazon.com/omics/latest/dev/parameter-templates.html>`_ .
    - *ECR container images:* Create container images for the workflow in a private ECR repository, or synchronize images from a supported upstream registry with your Amazon ECR private repository.
    - *(Optional) Sentieon licenses:* Request a Sentieon license to use the Sentieon software in private workflows.

    For more information, see `Creating or updating a private workflow in AWS HealthOmics <https://docs.aws.amazon.com/omics/latest/dev/creating-private-workflows.html>`_ in the *AWS HealthOmics User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflow.html
    :cloudformationResource: AWS::Omics::Workflow
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_omics import mixins as omics_mixins
        
        cfn_workflow_props_mixin = omics_mixins.CfnWorkflowPropsMixin(omics_mixins.CfnWorkflowMixinProps(
            accelerators="accelerators",
            container_registry_map=omics_mixins.CfnWorkflowPropsMixin.ContainerRegistryMapProperty(
                image_mappings=[omics_mixins.CfnWorkflowPropsMixin.ImageMappingProperty(
                    destination_image="destinationImage",
                    source_image="sourceImage"
                )],
                registry_mappings=[omics_mixins.CfnWorkflowPropsMixin.RegistryMappingProperty(
                    ecr_account_id="ecrAccountId",
                    ecr_repository_prefix="ecrRepositoryPrefix",
                    upstream_registry_url="upstreamRegistryUrl",
                    upstream_repository_prefix="upstreamRepositoryPrefix"
                )]
            ),
            container_registry_map_uri="containerRegistryMapUri",
            definition_repository=omics_mixins.CfnWorkflowPropsMixin.DefinitionRepositoryProperty(
                connection_arn="connectionArn",
                exclude_file_patterns=["excludeFilePatterns"],
                full_repository_id="fullRepositoryId",
                source_reference=omics_mixins.CfnWorkflowPropsMixin.SourceReferenceProperty(
                    type="type",
                    value="value"
                )
            ),
            definition_uri="definitionUri",
            description="description",
            engine="engine",
            main="main",
            name="name",
            parameter_template={
                "parameter_template_key": omics_mixins.CfnWorkflowPropsMixin.WorkflowParameterProperty(
                    description="description",
                    optional=False
                )
            },
            parameter_template_path="parameterTemplatePath",
            readme_markdown="readmeMarkdown",
            readme_path="readmePath",
            readme_uri="readmeUri",
            storage_capacity=123,
            storage_type="storageType",
            tags={
                "tags_key": "tags"
            },
            workflow_bucket_owner_id="workflowBucketOwnerId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnWorkflowMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Omics::Workflow``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec3d9acd00b3f5f58f11bd55765b54ff39e93ff04c38bed55917737e366f61aa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e19068365dd36d3c51d957f50f1ccc8c68d83c8a3b6de02e9c5ef9c1e8fce0d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6347f8877e0e5b3fd632db17788b818a561d14e1c060c1aa64fcde4b1a43b64)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnWorkflowMixinProps:
        return typing.cast(CfnWorkflowMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_omics.mixins.CfnWorkflowPropsMixin.ContainerRegistryMapProperty",
        jsii_struct_bases=[],
        name_mapping={
            "image_mappings": "imageMappings",
            "registry_mappings": "registryMappings",
        },
    )
    class ContainerRegistryMapProperty:
        def __init__(
            self,
            *,
            image_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkflowPropsMixin.ImageMappingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            registry_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkflowPropsMixin.RegistryMappingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Use a container registry map to specify mappings between the ECR private repository and one or more upstream registries.

            For more information, see `Container images <https://docs.aws.amazon.com/omics/latest/dev/workflows-ecr.html>`_ in the *AWS HealthOmics User Guide* .

            :param image_mappings: Image mappings specify path mappings between the ECR private repository and their corresponding external repositories.
            :param registry_mappings: Mapping that provides the ECR repository path where upstream container images are pulled and synchronized.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflow-containerregistrymap.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_omics import mixins as omics_mixins
                
                container_registry_map_property = omics_mixins.CfnWorkflowPropsMixin.ContainerRegistryMapProperty(
                    image_mappings=[omics_mixins.CfnWorkflowPropsMixin.ImageMappingProperty(
                        destination_image="destinationImage",
                        source_image="sourceImage"
                    )],
                    registry_mappings=[omics_mixins.CfnWorkflowPropsMixin.RegistryMappingProperty(
                        ecr_account_id="ecrAccountId",
                        ecr_repository_prefix="ecrRepositoryPrefix",
                        upstream_registry_url="upstreamRegistryUrl",
                        upstream_repository_prefix="upstreamRepositoryPrefix"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7d0d7eaa2f9d46704b83f12fac0f8940ed23339763fd79a1935b4deba03acc7d)
                check_type(argname="argument image_mappings", value=image_mappings, expected_type=type_hints["image_mappings"])
                check_type(argname="argument registry_mappings", value=registry_mappings, expected_type=type_hints["registry_mappings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if image_mappings is not None:
                self._values["image_mappings"] = image_mappings
            if registry_mappings is not None:
                self._values["registry_mappings"] = registry_mappings

        @builtins.property
        def image_mappings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkflowPropsMixin.ImageMappingProperty"]]]]:
            '''Image mappings specify path mappings between the ECR private repository and their corresponding external repositories.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflow-containerregistrymap.html#cfn-omics-workflow-containerregistrymap-imagemappings
            '''
            result = self._values.get("image_mappings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkflowPropsMixin.ImageMappingProperty"]]]], result)

        @builtins.property
        def registry_mappings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkflowPropsMixin.RegistryMappingProperty"]]]]:
            '''Mapping that provides the ECR repository path where upstream container images are pulled and synchronized.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflow-containerregistrymap.html#cfn-omics-workflow-containerregistrymap-registrymappings
            '''
            result = self._values.get("registry_mappings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkflowPropsMixin.RegistryMappingProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ContainerRegistryMapProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_omics.mixins.CfnWorkflowPropsMixin.DefinitionRepositoryProperty",
        jsii_struct_bases=[],
        name_mapping={
            "connection_arn": "connectionArn",
            "exclude_file_patterns": "excludeFilePatterns",
            "full_repository_id": "fullRepositoryId",
            "source_reference": "sourceReference",
        },
    )
    class DefinitionRepositoryProperty:
        def __init__(
            self,
            *,
            connection_arn: typing.Optional[builtins.str] = None,
            exclude_file_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
            full_repository_id: typing.Optional[builtins.str] = None,
            source_reference: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkflowPropsMixin.SourceReferenceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains information about a source code repository that hosts the workflow definition files.

            :param connection_arn: The Amazon Resource Name (ARN) of the connection to the source code repository.
            :param exclude_file_patterns: A list of file patterns to exclude when retrieving the workflow definition from the repository.
            :param full_repository_id: The full repository identifier, including the repository owner and name. For example, 'repository-owner/repository-name'.
            :param source_reference: The source reference for the repository, such as a branch name, tag, or commit ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflow-definitionrepository.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_omics import mixins as omics_mixins
                
                definition_repository_property = omics_mixins.CfnWorkflowPropsMixin.DefinitionRepositoryProperty(
                    connection_arn="connectionArn",
                    exclude_file_patterns=["excludeFilePatterns"],
                    full_repository_id="fullRepositoryId",
                    source_reference=omics_mixins.CfnWorkflowPropsMixin.SourceReferenceProperty(
                        type="type",
                        value="value"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fbff32ea4d5666b62265634f0aa0a0f94babd5ed53a54b60d6c14b8c789c52ac)
                check_type(argname="argument connection_arn", value=connection_arn, expected_type=type_hints["connection_arn"])
                check_type(argname="argument exclude_file_patterns", value=exclude_file_patterns, expected_type=type_hints["exclude_file_patterns"])
                check_type(argname="argument full_repository_id", value=full_repository_id, expected_type=type_hints["full_repository_id"])
                check_type(argname="argument source_reference", value=source_reference, expected_type=type_hints["source_reference"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if connection_arn is not None:
                self._values["connection_arn"] = connection_arn
            if exclude_file_patterns is not None:
                self._values["exclude_file_patterns"] = exclude_file_patterns
            if full_repository_id is not None:
                self._values["full_repository_id"] = full_repository_id
            if source_reference is not None:
                self._values["source_reference"] = source_reference

        @builtins.property
        def connection_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the connection to the source code repository.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflow-definitionrepository.html#cfn-omics-workflow-definitionrepository-connectionarn
            '''
            result = self._values.get("connection_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def exclude_file_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of file patterns to exclude when retrieving the workflow definition from the repository.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflow-definitionrepository.html#cfn-omics-workflow-definitionrepository-excludefilepatterns
            '''
            result = self._values.get("exclude_file_patterns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def full_repository_id(self) -> typing.Optional[builtins.str]:
            '''The full repository identifier, including the repository owner and name.

            For example, 'repository-owner/repository-name'.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflow-definitionrepository.html#cfn-omics-workflow-definitionrepository-fullrepositoryid
            '''
            result = self._values.get("full_repository_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_reference(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkflowPropsMixin.SourceReferenceProperty"]]:
            '''The source reference for the repository, such as a branch name, tag, or commit ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflow-definitionrepository.html#cfn-omics-workflow-definitionrepository-sourcereference
            '''
            result = self._values.get("source_reference")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkflowPropsMixin.SourceReferenceProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DefinitionRepositoryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_omics.mixins.CfnWorkflowPropsMixin.ImageMappingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_image": "destinationImage",
            "source_image": "sourceImage",
        },
    )
    class ImageMappingProperty:
        def __init__(
            self,
            *,
            destination_image: typing.Optional[builtins.str] = None,
            source_image: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies image mappings that workflow tasks can use.

            For example, you can replace all the task references of a public image to use an equivalent image in your private ECR repository. You can use image mappings with upstream registries that don't support pull through cache. You need to manually synchronize the upstream registry with your private repository.

            :param destination_image: Specifies the URI of the corresponding image in the private ECR registry.
            :param source_image: Specifies the URI of the source image in the upstream registry.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflow-imagemapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_omics import mixins as omics_mixins
                
                image_mapping_property = omics_mixins.CfnWorkflowPropsMixin.ImageMappingProperty(
                    destination_image="destinationImage",
                    source_image="sourceImage"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d9d50e088ae380494b46dad2fc59ffccb888d9f069336fd815d4a0a86fdbc2ae)
                check_type(argname="argument destination_image", value=destination_image, expected_type=type_hints["destination_image"])
                check_type(argname="argument source_image", value=source_image, expected_type=type_hints["source_image"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination_image is not None:
                self._values["destination_image"] = destination_image
            if source_image is not None:
                self._values["source_image"] = source_image

        @builtins.property
        def destination_image(self) -> typing.Optional[builtins.str]:
            '''Specifies the URI of the corresponding image in the private ECR registry.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflow-imagemapping.html#cfn-omics-workflow-imagemapping-destinationimage
            '''
            result = self._values.get("destination_image")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_image(self) -> typing.Optional[builtins.str]:
            '''Specifies the URI of the source image in the upstream registry.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflow-imagemapping.html#cfn-omics-workflow-imagemapping-sourceimage
            '''
            result = self._values.get("source_image")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ImageMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_omics.mixins.CfnWorkflowPropsMixin.RegistryMappingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ecr_account_id": "ecrAccountId",
            "ecr_repository_prefix": "ecrRepositoryPrefix",
            "upstream_registry_url": "upstreamRegistryUrl",
            "upstream_repository_prefix": "upstreamRepositoryPrefix",
        },
    )
    class RegistryMappingProperty:
        def __init__(
            self,
            *,
            ecr_account_id: typing.Optional[builtins.str] = None,
            ecr_repository_prefix: typing.Optional[builtins.str] = None,
            upstream_registry_url: typing.Optional[builtins.str] = None,
            upstream_repository_prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''If you are using the ECR pull through cache feature, the registry mapping maps between the ECR repository and the upstream registry where container images are pulled and synchronized.

            :param ecr_account_id: Account ID of the account that owns the upstream container image.
            :param ecr_repository_prefix: The repository prefix to use in the ECR private repository.
            :param upstream_registry_url: The URI of the upstream registry.
            :param upstream_repository_prefix: The repository prefix of the corresponding repository in the upstream registry.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflow-registrymapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_omics import mixins as omics_mixins
                
                registry_mapping_property = omics_mixins.CfnWorkflowPropsMixin.RegistryMappingProperty(
                    ecr_account_id="ecrAccountId",
                    ecr_repository_prefix="ecrRepositoryPrefix",
                    upstream_registry_url="upstreamRegistryUrl",
                    upstream_repository_prefix="upstreamRepositoryPrefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7065969cf0a0ddb15f11f31a6bb8f71899275a76dfd3d6b2c31336ad3ab56711)
                check_type(argname="argument ecr_account_id", value=ecr_account_id, expected_type=type_hints["ecr_account_id"])
                check_type(argname="argument ecr_repository_prefix", value=ecr_repository_prefix, expected_type=type_hints["ecr_repository_prefix"])
                check_type(argname="argument upstream_registry_url", value=upstream_registry_url, expected_type=type_hints["upstream_registry_url"])
                check_type(argname="argument upstream_repository_prefix", value=upstream_repository_prefix, expected_type=type_hints["upstream_repository_prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ecr_account_id is not None:
                self._values["ecr_account_id"] = ecr_account_id
            if ecr_repository_prefix is not None:
                self._values["ecr_repository_prefix"] = ecr_repository_prefix
            if upstream_registry_url is not None:
                self._values["upstream_registry_url"] = upstream_registry_url
            if upstream_repository_prefix is not None:
                self._values["upstream_repository_prefix"] = upstream_repository_prefix

        @builtins.property
        def ecr_account_id(self) -> typing.Optional[builtins.str]:
            '''Account ID of the account that owns the upstream container image.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflow-registrymapping.html#cfn-omics-workflow-registrymapping-ecraccountid
            '''
            result = self._values.get("ecr_account_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ecr_repository_prefix(self) -> typing.Optional[builtins.str]:
            '''The repository prefix to use in the ECR private repository.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflow-registrymapping.html#cfn-omics-workflow-registrymapping-ecrrepositoryprefix
            '''
            result = self._values.get("ecr_repository_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def upstream_registry_url(self) -> typing.Optional[builtins.str]:
            '''The URI of the upstream registry.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflow-registrymapping.html#cfn-omics-workflow-registrymapping-upstreamregistryurl
            '''
            result = self._values.get("upstream_registry_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def upstream_repository_prefix(self) -> typing.Optional[builtins.str]:
            '''The repository prefix of the corresponding repository in the upstream registry.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflow-registrymapping.html#cfn-omics-workflow-registrymapping-upstreamrepositoryprefix
            '''
            result = self._values.get("upstream_repository_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RegistryMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_omics.mixins.CfnWorkflowPropsMixin.SourceReferenceProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "value": "value"},
    )
    class SourceReferenceProperty:
        def __init__(
            self,
            *,
            type: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about the source reference in a code repository, such as a branch, tag, or commit.

            :param type: The type of source reference, such as branch, tag, or commit.
            :param value: The value of the source reference, such as the branch name, tag name, or commit ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflow-sourcereference.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_omics import mixins as omics_mixins
                
                source_reference_property = omics_mixins.CfnWorkflowPropsMixin.SourceReferenceProperty(
                    type="type",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__15444e47a78a0618c79f08cf7929c5fc3299b96d9b97f26503065c0226fc3693)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if type is not None:
                self._values["type"] = type
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of source reference, such as branch, tag, or commit.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflow-sourcereference.html#cfn-omics-workflow-sourcereference-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value of the source reference, such as the branch name, tag name, or commit ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflow-sourcereference.html#cfn-omics-workflow-sourcereference-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceReferenceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_omics.mixins.CfnWorkflowPropsMixin.WorkflowParameterProperty",
        jsii_struct_bases=[],
        name_mapping={"description": "description", "optional": "optional"},
    )
    class WorkflowParameterProperty:
        def __init__(
            self,
            *,
            description: typing.Optional[builtins.str] = None,
            optional: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''A workflow parameter.

            :param description: The parameter's description.
            :param optional: Whether the parameter is optional.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflow-workflowparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_omics import mixins as omics_mixins
                
                workflow_parameter_property = omics_mixins.CfnWorkflowPropsMixin.WorkflowParameterProperty(
                    description="description",
                    optional=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f39ef17cfe3250cd9d03177b3f93e9d1b138ae2cb0ae86aab078681401d832a5)
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument optional", value=optional, expected_type=type_hints["optional"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if description is not None:
                self._values["description"] = description
            if optional is not None:
                self._values["optional"] = optional

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The parameter's description.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflow-workflowparameter.html#cfn-omics-workflow-workflowparameter-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def optional(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Whether the parameter is optional.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflow-workflowparameter.html#cfn-omics-workflow-workflowparameter-optional
            '''
            result = self._values.get("optional")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WorkflowParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_omics.mixins.CfnWorkflowVersionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "accelerators": "accelerators",
        "container_registry_map": "containerRegistryMap",
        "container_registry_map_uri": "containerRegistryMapUri",
        "definition_repository": "definitionRepository",
        "definition_uri": "definitionUri",
        "description": "description",
        "engine": "engine",
        "main": "main",
        "parameter_template": "parameterTemplate",
        "parameter_template_path": "parameterTemplatePath",
        "readme_markdown": "readmeMarkdown",
        "readme_path": "readmePath",
        "readme_uri": "readmeUri",
        "storage_capacity": "storageCapacity",
        "storage_type": "storageType",
        "tags": "tags",
        "version_name": "versionName",
        "workflow_bucket_owner_id": "workflowBucketOwnerId",
        "workflow_id": "workflowId",
    },
)
class CfnWorkflowVersionMixinProps:
    def __init__(
        self,
        *,
        accelerators: typing.Optional[builtins.str] = None,
        container_registry_map: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkflowVersionPropsMixin.ContainerRegistryMapProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        container_registry_map_uri: typing.Optional[builtins.str] = None,
        definition_repository: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkflowVersionPropsMixin.DefinitionRepositoryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        definition_uri: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        engine: typing.Optional[builtins.str] = None,
        main: typing.Optional[builtins.str] = None,
        parameter_template: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkflowVersionPropsMixin.WorkflowParameterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        parameter_template_path: typing.Optional[builtins.str] = None,
        readme_markdown: typing.Optional[builtins.str] = None,
        readme_path: typing.Optional[builtins.str] = None,
        readme_uri: typing.Optional[builtins.str] = None,
        storage_capacity: typing.Optional[jsii.Number] = None,
        storage_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        version_name: typing.Optional[builtins.str] = None,
        workflow_bucket_owner_id: typing.Optional[builtins.str] = None,
        workflow_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnWorkflowVersionPropsMixin.

        :param accelerators: 
        :param container_registry_map: Use a container registry map to specify mappings between the ECR private repository and one or more upstream registries. For more information, see `Container images <https://docs.aws.amazon.com/omics/latest/dev/workflows-ecr.html>`_ in the *AWS HealthOmics User Guide* .
        :param container_registry_map_uri: 
        :param definition_repository: Contains information about a source code repository that hosts the workflow definition files.
        :param definition_uri: 
        :param description: The description of the workflow version.
        :param engine: 
        :param main: 
        :param parameter_template: 
        :param parameter_template_path: Path to the primary workflow parameter template JSON file inside the repository.
        :param readme_markdown: The markdown content for the workflow's README file. This provides documentation and usage information for users of the workflow.
        :param readme_path: The path to the workflow README markdown file within the repository. This file provides documentation and usage information for the workflow. If not specified, the README.md file from the root directory of the repository will be used.
        :param readme_uri: The S3 URI of the README file for the workflow. This file provides documentation and usage information for the workflow. The S3 URI must begin with s3://USER-OWNED-BUCKET/. The requester must have access to the S3 bucket and object. The max README content length is 500 KiB.
        :param storage_capacity: 
        :param storage_type: 
        :param tags: A map of resource tags.
        :param version_name: The name of the workflow version.
        :param workflow_bucket_owner_id: 
        :param workflow_id: The workflow's ID.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflowversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_omics import mixins as omics_mixins
            
            cfn_workflow_version_mixin_props = omics_mixins.CfnWorkflowVersionMixinProps(
                accelerators="accelerators",
                container_registry_map=omics_mixins.CfnWorkflowVersionPropsMixin.ContainerRegistryMapProperty(
                    image_mappings=[omics_mixins.CfnWorkflowVersionPropsMixin.ImageMappingProperty(
                        destination_image="destinationImage",
                        source_image="sourceImage"
                    )],
                    registry_mappings=[omics_mixins.CfnWorkflowVersionPropsMixin.RegistryMappingProperty(
                        ecr_account_id="ecrAccountId",
                        ecr_repository_prefix="ecrRepositoryPrefix",
                        upstream_registry_url="upstreamRegistryUrl",
                        upstream_repository_prefix="upstreamRepositoryPrefix"
                    )]
                ),
                container_registry_map_uri="containerRegistryMapUri",
                definition_repository=omics_mixins.CfnWorkflowVersionPropsMixin.DefinitionRepositoryProperty(
                    connection_arn="connectionArn",
                    exclude_file_patterns=["excludeFilePatterns"],
                    full_repository_id="fullRepositoryId",
                    source_reference=omics_mixins.CfnWorkflowVersionPropsMixin.SourceReferenceProperty(
                        type="type",
                        value="value"
                    )
                ),
                definition_uri="definitionUri",
                description="description",
                engine="engine",
                main="main",
                parameter_template={
                    "parameter_template_key": omics_mixins.CfnWorkflowVersionPropsMixin.WorkflowParameterProperty(
                        description="description",
                        optional=False
                    )
                },
                parameter_template_path="parameterTemplatePath",
                readme_markdown="readmeMarkdown",
                readme_path="readmePath",
                readme_uri="readmeUri",
                storage_capacity=123,
                storage_type="storageType",
                tags={
                    "tags_key": "tags"
                },
                version_name="versionName",
                workflow_bucket_owner_id="workflowBucketOwnerId",
                workflow_id="workflowId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5c614a882083328766c3036a05054e08e9bb3e634f6aebbadcb7bb32bc49d68)
            check_type(argname="argument accelerators", value=accelerators, expected_type=type_hints["accelerators"])
            check_type(argname="argument container_registry_map", value=container_registry_map, expected_type=type_hints["container_registry_map"])
            check_type(argname="argument container_registry_map_uri", value=container_registry_map_uri, expected_type=type_hints["container_registry_map_uri"])
            check_type(argname="argument definition_repository", value=definition_repository, expected_type=type_hints["definition_repository"])
            check_type(argname="argument definition_uri", value=definition_uri, expected_type=type_hints["definition_uri"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument engine", value=engine, expected_type=type_hints["engine"])
            check_type(argname="argument main", value=main, expected_type=type_hints["main"])
            check_type(argname="argument parameter_template", value=parameter_template, expected_type=type_hints["parameter_template"])
            check_type(argname="argument parameter_template_path", value=parameter_template_path, expected_type=type_hints["parameter_template_path"])
            check_type(argname="argument readme_markdown", value=readme_markdown, expected_type=type_hints["readme_markdown"])
            check_type(argname="argument readme_path", value=readme_path, expected_type=type_hints["readme_path"])
            check_type(argname="argument readme_uri", value=readme_uri, expected_type=type_hints["readme_uri"])
            check_type(argname="argument storage_capacity", value=storage_capacity, expected_type=type_hints["storage_capacity"])
            check_type(argname="argument storage_type", value=storage_type, expected_type=type_hints["storage_type"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument version_name", value=version_name, expected_type=type_hints["version_name"])
            check_type(argname="argument workflow_bucket_owner_id", value=workflow_bucket_owner_id, expected_type=type_hints["workflow_bucket_owner_id"])
            check_type(argname="argument workflow_id", value=workflow_id, expected_type=type_hints["workflow_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accelerators is not None:
            self._values["accelerators"] = accelerators
        if container_registry_map is not None:
            self._values["container_registry_map"] = container_registry_map
        if container_registry_map_uri is not None:
            self._values["container_registry_map_uri"] = container_registry_map_uri
        if definition_repository is not None:
            self._values["definition_repository"] = definition_repository
        if definition_uri is not None:
            self._values["definition_uri"] = definition_uri
        if description is not None:
            self._values["description"] = description
        if engine is not None:
            self._values["engine"] = engine
        if main is not None:
            self._values["main"] = main
        if parameter_template is not None:
            self._values["parameter_template"] = parameter_template
        if parameter_template_path is not None:
            self._values["parameter_template_path"] = parameter_template_path
        if readme_markdown is not None:
            self._values["readme_markdown"] = readme_markdown
        if readme_path is not None:
            self._values["readme_path"] = readme_path
        if readme_uri is not None:
            self._values["readme_uri"] = readme_uri
        if storage_capacity is not None:
            self._values["storage_capacity"] = storage_capacity
        if storage_type is not None:
            self._values["storage_type"] = storage_type
        if tags is not None:
            self._values["tags"] = tags
        if version_name is not None:
            self._values["version_name"] = version_name
        if workflow_bucket_owner_id is not None:
            self._values["workflow_bucket_owner_id"] = workflow_bucket_owner_id
        if workflow_id is not None:
            self._values["workflow_id"] = workflow_id

    @builtins.property
    def accelerators(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflowversion.html#cfn-omics-workflowversion-accelerators
        '''
        result = self._values.get("accelerators")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def container_registry_map(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkflowVersionPropsMixin.ContainerRegistryMapProperty"]]:
        '''Use a container registry map to specify mappings between the ECR private repository and one or more upstream registries.

        For more information, see `Container images <https://docs.aws.amazon.com/omics/latest/dev/workflows-ecr.html>`_ in the *AWS HealthOmics User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflowversion.html#cfn-omics-workflowversion-containerregistrymap
        '''
        result = self._values.get("container_registry_map")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkflowVersionPropsMixin.ContainerRegistryMapProperty"]], result)

    @builtins.property
    def container_registry_map_uri(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflowversion.html#cfn-omics-workflowversion-containerregistrymapuri
        '''
        result = self._values.get("container_registry_map_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def definition_repository(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkflowVersionPropsMixin.DefinitionRepositoryProperty"]]:
        '''Contains information about a source code repository that hosts the workflow definition files.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflowversion.html#cfn-omics-workflowversion-definitionrepository
        '''
        result = self._values.get("definition_repository")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkflowVersionPropsMixin.DefinitionRepositoryProperty"]], result)

    @builtins.property
    def definition_uri(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflowversion.html#cfn-omics-workflowversion-definitionuri
        '''
        result = self._values.get("definition_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the workflow version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflowversion.html#cfn-omics-workflowversion-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def engine(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflowversion.html#cfn-omics-workflowversion-engine
        '''
        result = self._values.get("engine")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def main(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflowversion.html#cfn-omics-workflowversion-main
        '''
        result = self._values.get("main")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameter_template(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkflowVersionPropsMixin.WorkflowParameterProperty"]]]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflowversion.html#cfn-omics-workflowversion-parametertemplate
        '''
        result = self._values.get("parameter_template")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkflowVersionPropsMixin.WorkflowParameterProperty"]]]], result)

    @builtins.property
    def parameter_template_path(self) -> typing.Optional[builtins.str]:
        '''Path to the primary workflow parameter template JSON file inside the repository.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflowversion.html#cfn-omics-workflowversion-parametertemplatepath
        '''
        result = self._values.get("parameter_template_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def readme_markdown(self) -> typing.Optional[builtins.str]:
        '''The markdown content for the workflow's README file.

        This provides documentation and usage information for users of the workflow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflowversion.html#cfn-omics-workflowversion-readmemarkdown
        '''
        result = self._values.get("readme_markdown")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def readme_path(self) -> typing.Optional[builtins.str]:
        '''The path to the workflow README markdown file within the repository.

        This file provides documentation and usage information for the workflow. If not specified, the README.md file from the root directory of the repository will be used.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflowversion.html#cfn-omics-workflowversion-readmepath
        '''
        result = self._values.get("readme_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def readme_uri(self) -> typing.Optional[builtins.str]:
        '''The S3 URI of the README file for the workflow.

        This file provides documentation and usage information for the workflow. The S3 URI must begin with s3://USER-OWNED-BUCKET/. The requester must have access to the S3 bucket and object. The max README content length is 500 KiB.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflowversion.html#cfn-omics-workflowversion-readmeuri
        '''
        result = self._values.get("readme_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_capacity(self) -> typing.Optional[jsii.Number]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflowversion.html#cfn-omics-workflowversion-storagecapacity
        '''
        result = self._values.get("storage_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def storage_type(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflowversion.html#cfn-omics-workflowversion-storagetype
        '''
        result = self._values.get("storage_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of resource tags.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflowversion.html#cfn-omics-workflowversion-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def version_name(self) -> typing.Optional[builtins.str]:
        '''The name of the workflow version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflowversion.html#cfn-omics-workflowversion-versionname
        '''
        result = self._values.get("version_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workflow_bucket_owner_id(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflowversion.html#cfn-omics-workflowversion-workflowbucketownerid
        '''
        result = self._values.get("workflow_bucket_owner_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workflow_id(self) -> typing.Optional[builtins.str]:
        '''The workflow's ID.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflowversion.html#cfn-omics-workflowversion-workflowid
        '''
        result = self._values.get("workflow_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWorkflowVersionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnWorkflowVersionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_omics.mixins.CfnWorkflowVersionPropsMixin",
):
    '''Creates a new workflow version for the workflow that you specify with the ``workflowId`` parameter.

    When you create a new version of a workflow, you need to specify the configuration for the new version. It doesn't inherit any configuration values from the workflow.

    Provide a version name that is unique for this workflow. You cannot change the name after HealthOmics creates the version.
    .. epigraph::

       Don't include any personally identifiable information (PII) in the version name. Version names appear in the workflow version ARN.

    For more information, see `Workflow versioning in AWS HealthOmics <https://docs.aws.amazon.com/omics/latest/dev/workflow-versions.html>`_ in the *AWS HealthOmics User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflowversion.html
    :cloudformationResource: AWS::Omics::WorkflowVersion
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_omics import mixins as omics_mixins
        
        cfn_workflow_version_props_mixin = omics_mixins.CfnWorkflowVersionPropsMixin(omics_mixins.CfnWorkflowVersionMixinProps(
            accelerators="accelerators",
            container_registry_map=omics_mixins.CfnWorkflowVersionPropsMixin.ContainerRegistryMapProperty(
                image_mappings=[omics_mixins.CfnWorkflowVersionPropsMixin.ImageMappingProperty(
                    destination_image="destinationImage",
                    source_image="sourceImage"
                )],
                registry_mappings=[omics_mixins.CfnWorkflowVersionPropsMixin.RegistryMappingProperty(
                    ecr_account_id="ecrAccountId",
                    ecr_repository_prefix="ecrRepositoryPrefix",
                    upstream_registry_url="upstreamRegistryUrl",
                    upstream_repository_prefix="upstreamRepositoryPrefix"
                )]
            ),
            container_registry_map_uri="containerRegistryMapUri",
            definition_repository=omics_mixins.CfnWorkflowVersionPropsMixin.DefinitionRepositoryProperty(
                connection_arn="connectionArn",
                exclude_file_patterns=["excludeFilePatterns"],
                full_repository_id="fullRepositoryId",
                source_reference=omics_mixins.CfnWorkflowVersionPropsMixin.SourceReferenceProperty(
                    type="type",
                    value="value"
                )
            ),
            definition_uri="definitionUri",
            description="description",
            engine="engine",
            main="main",
            parameter_template={
                "parameter_template_key": omics_mixins.CfnWorkflowVersionPropsMixin.WorkflowParameterProperty(
                    description="description",
                    optional=False
                )
            },
            parameter_template_path="parameterTemplatePath",
            readme_markdown="readmeMarkdown",
            readme_path="readmePath",
            readme_uri="readmeUri",
            storage_capacity=123,
            storage_type="storageType",
            tags={
                "tags_key": "tags"
            },
            version_name="versionName",
            workflow_bucket_owner_id="workflowBucketOwnerId",
            workflow_id="workflowId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnWorkflowVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Omics::WorkflowVersion``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89e4ce7b47495166b2898e02f5a0d9f3f99b61f435215612773e4f3d79175462)
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
            type_hints = typing.get_type_hints(_typecheckingstub__23b4f30def0d9320b0386b674c3e099c1d19bdabcdc6b80f2e7daec5fc706800)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7622b13513619777fbb7db7429b245728ee66570c17c3e7b5185ba868aba67d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnWorkflowVersionMixinProps:
        return typing.cast(CfnWorkflowVersionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_omics.mixins.CfnWorkflowVersionPropsMixin.ContainerRegistryMapProperty",
        jsii_struct_bases=[],
        name_mapping={
            "image_mappings": "imageMappings",
            "registry_mappings": "registryMappings",
        },
    )
    class ContainerRegistryMapProperty:
        def __init__(
            self,
            *,
            image_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkflowVersionPropsMixin.ImageMappingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            registry_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkflowVersionPropsMixin.RegistryMappingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Use a container registry map to specify mappings between the ECR private repository and one or more upstream registries.

            For more information, see `Container images <https://docs.aws.amazon.com/omics/latest/dev/workflows-ecr.html>`_ in the *AWS HealthOmics User Guide* .

            :param image_mappings: Image mappings specify path mappings between the ECR private repository and their corresponding external repositories.
            :param registry_mappings: Mapping that provides the ECR repository path where upstream container images are pulled and synchronized.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflowversion-containerregistrymap.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_omics import mixins as omics_mixins
                
                container_registry_map_property = omics_mixins.CfnWorkflowVersionPropsMixin.ContainerRegistryMapProperty(
                    image_mappings=[omics_mixins.CfnWorkflowVersionPropsMixin.ImageMappingProperty(
                        destination_image="destinationImage",
                        source_image="sourceImage"
                    )],
                    registry_mappings=[omics_mixins.CfnWorkflowVersionPropsMixin.RegistryMappingProperty(
                        ecr_account_id="ecrAccountId",
                        ecr_repository_prefix="ecrRepositoryPrefix",
                        upstream_registry_url="upstreamRegistryUrl",
                        upstream_repository_prefix="upstreamRepositoryPrefix"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c908dc0d7533ff0f647ef36f4b5cf3f6dbd6f56b37098b5e10d9b48616f2a094)
                check_type(argname="argument image_mappings", value=image_mappings, expected_type=type_hints["image_mappings"])
                check_type(argname="argument registry_mappings", value=registry_mappings, expected_type=type_hints["registry_mappings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if image_mappings is not None:
                self._values["image_mappings"] = image_mappings
            if registry_mappings is not None:
                self._values["registry_mappings"] = registry_mappings

        @builtins.property
        def image_mappings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkflowVersionPropsMixin.ImageMappingProperty"]]]]:
            '''Image mappings specify path mappings between the ECR private repository and their corresponding external repositories.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflowversion-containerregistrymap.html#cfn-omics-workflowversion-containerregistrymap-imagemappings
            '''
            result = self._values.get("image_mappings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkflowVersionPropsMixin.ImageMappingProperty"]]]], result)

        @builtins.property
        def registry_mappings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkflowVersionPropsMixin.RegistryMappingProperty"]]]]:
            '''Mapping that provides the ECR repository path where upstream container images are pulled and synchronized.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflowversion-containerregistrymap.html#cfn-omics-workflowversion-containerregistrymap-registrymappings
            '''
            result = self._values.get("registry_mappings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkflowVersionPropsMixin.RegistryMappingProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ContainerRegistryMapProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_omics.mixins.CfnWorkflowVersionPropsMixin.DefinitionRepositoryProperty",
        jsii_struct_bases=[],
        name_mapping={
            "connection_arn": "connectionArn",
            "exclude_file_patterns": "excludeFilePatterns",
            "full_repository_id": "fullRepositoryId",
            "source_reference": "sourceReference",
        },
    )
    class DefinitionRepositoryProperty:
        def __init__(
            self,
            *,
            connection_arn: typing.Optional[builtins.str] = None,
            exclude_file_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
            full_repository_id: typing.Optional[builtins.str] = None,
            source_reference: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkflowVersionPropsMixin.SourceReferenceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains information about a source code repository that hosts the workflow definition files.

            :param connection_arn: The Amazon Resource Name (ARN) of the connection to the source code repository.
            :param exclude_file_patterns: A list of file patterns to exclude when retrieving the workflow definition from the repository.
            :param full_repository_id: The full repository identifier, including the repository owner and name. For example, 'repository-owner/repository-name'.
            :param source_reference: The source reference for the repository, such as a branch name, tag, or commit ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflowversion-definitionrepository.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_omics import mixins as omics_mixins
                
                definition_repository_property = omics_mixins.CfnWorkflowVersionPropsMixin.DefinitionRepositoryProperty(
                    connection_arn="connectionArn",
                    exclude_file_patterns=["excludeFilePatterns"],
                    full_repository_id="fullRepositoryId",
                    source_reference=omics_mixins.CfnWorkflowVersionPropsMixin.SourceReferenceProperty(
                        type="type",
                        value="value"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1b32add453d6d98bdc68729d569ebbc4ad09d25fb446e496f5084482a7b0982d)
                check_type(argname="argument connection_arn", value=connection_arn, expected_type=type_hints["connection_arn"])
                check_type(argname="argument exclude_file_patterns", value=exclude_file_patterns, expected_type=type_hints["exclude_file_patterns"])
                check_type(argname="argument full_repository_id", value=full_repository_id, expected_type=type_hints["full_repository_id"])
                check_type(argname="argument source_reference", value=source_reference, expected_type=type_hints["source_reference"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if connection_arn is not None:
                self._values["connection_arn"] = connection_arn
            if exclude_file_patterns is not None:
                self._values["exclude_file_patterns"] = exclude_file_patterns
            if full_repository_id is not None:
                self._values["full_repository_id"] = full_repository_id
            if source_reference is not None:
                self._values["source_reference"] = source_reference

        @builtins.property
        def connection_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the connection to the source code repository.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflowversion-definitionrepository.html#cfn-omics-workflowversion-definitionrepository-connectionarn
            '''
            result = self._values.get("connection_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def exclude_file_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of file patterns to exclude when retrieving the workflow definition from the repository.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflowversion-definitionrepository.html#cfn-omics-workflowversion-definitionrepository-excludefilepatterns
            '''
            result = self._values.get("exclude_file_patterns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def full_repository_id(self) -> typing.Optional[builtins.str]:
            '''The full repository identifier, including the repository owner and name.

            For example, 'repository-owner/repository-name'.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflowversion-definitionrepository.html#cfn-omics-workflowversion-definitionrepository-fullrepositoryid
            '''
            result = self._values.get("full_repository_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_reference(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkflowVersionPropsMixin.SourceReferenceProperty"]]:
            '''The source reference for the repository, such as a branch name, tag, or commit ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflowversion-definitionrepository.html#cfn-omics-workflowversion-definitionrepository-sourcereference
            '''
            result = self._values.get("source_reference")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkflowVersionPropsMixin.SourceReferenceProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DefinitionRepositoryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_omics.mixins.CfnWorkflowVersionPropsMixin.ImageMappingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_image": "destinationImage",
            "source_image": "sourceImage",
        },
    )
    class ImageMappingProperty:
        def __init__(
            self,
            *,
            destination_image: typing.Optional[builtins.str] = None,
            source_image: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies image mappings that workflow tasks can use.

            For example, you can replace all the task references of a public image to use an equivalent image in your private ECR repository. You can use image mappings with upstream registries that don't support pull through cache. You need to manually synchronize the upstream registry with your private repository.

            :param destination_image: Specifies the URI of the corresponding image in the private ECR registry.
            :param source_image: Specifies the URI of the source image in the upstream registry.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflowversion-imagemapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_omics import mixins as omics_mixins
                
                image_mapping_property = omics_mixins.CfnWorkflowVersionPropsMixin.ImageMappingProperty(
                    destination_image="destinationImage",
                    source_image="sourceImage"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__55635076a1d3476178dacdb6667123af3ef39b100eb7e29c4693a7f0e9401571)
                check_type(argname="argument destination_image", value=destination_image, expected_type=type_hints["destination_image"])
                check_type(argname="argument source_image", value=source_image, expected_type=type_hints["source_image"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination_image is not None:
                self._values["destination_image"] = destination_image
            if source_image is not None:
                self._values["source_image"] = source_image

        @builtins.property
        def destination_image(self) -> typing.Optional[builtins.str]:
            '''Specifies the URI of the corresponding image in the private ECR registry.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflowversion-imagemapping.html#cfn-omics-workflowversion-imagemapping-destinationimage
            '''
            result = self._values.get("destination_image")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_image(self) -> typing.Optional[builtins.str]:
            '''Specifies the URI of the source image in the upstream registry.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflowversion-imagemapping.html#cfn-omics-workflowversion-imagemapping-sourceimage
            '''
            result = self._values.get("source_image")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ImageMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_omics.mixins.CfnWorkflowVersionPropsMixin.RegistryMappingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ecr_account_id": "ecrAccountId",
            "ecr_repository_prefix": "ecrRepositoryPrefix",
            "upstream_registry_url": "upstreamRegistryUrl",
            "upstream_repository_prefix": "upstreamRepositoryPrefix",
        },
    )
    class RegistryMappingProperty:
        def __init__(
            self,
            *,
            ecr_account_id: typing.Optional[builtins.str] = None,
            ecr_repository_prefix: typing.Optional[builtins.str] = None,
            upstream_registry_url: typing.Optional[builtins.str] = None,
            upstream_repository_prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''If you are using the ECR pull through cache feature, the registry mapping maps between the ECR repository and the upstream registry where container images are pulled and synchronized.

            :param ecr_account_id: Account ID of the account that owns the upstream container image.
            :param ecr_repository_prefix: The repository prefix to use in the ECR private repository.
            :param upstream_registry_url: The URI of the upstream registry.
            :param upstream_repository_prefix: The repository prefix of the corresponding repository in the upstream registry.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflowversion-registrymapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_omics import mixins as omics_mixins
                
                registry_mapping_property = omics_mixins.CfnWorkflowVersionPropsMixin.RegistryMappingProperty(
                    ecr_account_id="ecrAccountId",
                    ecr_repository_prefix="ecrRepositoryPrefix",
                    upstream_registry_url="upstreamRegistryUrl",
                    upstream_repository_prefix="upstreamRepositoryPrefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__434bdbf3f9121658be2fd6a32d6752dce5ebb2192d6183a651550a7600c59812)
                check_type(argname="argument ecr_account_id", value=ecr_account_id, expected_type=type_hints["ecr_account_id"])
                check_type(argname="argument ecr_repository_prefix", value=ecr_repository_prefix, expected_type=type_hints["ecr_repository_prefix"])
                check_type(argname="argument upstream_registry_url", value=upstream_registry_url, expected_type=type_hints["upstream_registry_url"])
                check_type(argname="argument upstream_repository_prefix", value=upstream_repository_prefix, expected_type=type_hints["upstream_repository_prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ecr_account_id is not None:
                self._values["ecr_account_id"] = ecr_account_id
            if ecr_repository_prefix is not None:
                self._values["ecr_repository_prefix"] = ecr_repository_prefix
            if upstream_registry_url is not None:
                self._values["upstream_registry_url"] = upstream_registry_url
            if upstream_repository_prefix is not None:
                self._values["upstream_repository_prefix"] = upstream_repository_prefix

        @builtins.property
        def ecr_account_id(self) -> typing.Optional[builtins.str]:
            '''Account ID of the account that owns the upstream container image.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflowversion-registrymapping.html#cfn-omics-workflowversion-registrymapping-ecraccountid
            '''
            result = self._values.get("ecr_account_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ecr_repository_prefix(self) -> typing.Optional[builtins.str]:
            '''The repository prefix to use in the ECR private repository.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflowversion-registrymapping.html#cfn-omics-workflowversion-registrymapping-ecrrepositoryprefix
            '''
            result = self._values.get("ecr_repository_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def upstream_registry_url(self) -> typing.Optional[builtins.str]:
            '''The URI of the upstream registry.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflowversion-registrymapping.html#cfn-omics-workflowversion-registrymapping-upstreamregistryurl
            '''
            result = self._values.get("upstream_registry_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def upstream_repository_prefix(self) -> typing.Optional[builtins.str]:
            '''The repository prefix of the corresponding repository in the upstream registry.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflowversion-registrymapping.html#cfn-omics-workflowversion-registrymapping-upstreamrepositoryprefix
            '''
            result = self._values.get("upstream_repository_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RegistryMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_omics.mixins.CfnWorkflowVersionPropsMixin.SourceReferenceProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "value": "value"},
    )
    class SourceReferenceProperty:
        def __init__(
            self,
            *,
            type: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about the source reference in a code repository, such as a branch, tag, or commit.

            :param type: The type of source reference, such as branch, tag, or commit.
            :param value: The value of the source reference, such as the branch name, tag name, or commit ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflowversion-sourcereference.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_omics import mixins as omics_mixins
                
                source_reference_property = omics_mixins.CfnWorkflowVersionPropsMixin.SourceReferenceProperty(
                    type="type",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5c4d4b659903987c3f10211981068e4779ac0f2db08fddb030303f2fc118f342)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if type is not None:
                self._values["type"] = type
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of source reference, such as branch, tag, or commit.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflowversion-sourcereference.html#cfn-omics-workflowversion-sourcereference-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value of the source reference, such as the branch name, tag name, or commit ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflowversion-sourcereference.html#cfn-omics-workflowversion-sourcereference-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceReferenceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_omics.mixins.CfnWorkflowVersionPropsMixin.WorkflowParameterProperty",
        jsii_struct_bases=[],
        name_mapping={"description": "description", "optional": "optional"},
    )
    class WorkflowParameterProperty:
        def __init__(
            self,
            *,
            description: typing.Optional[builtins.str] = None,
            optional: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''A workflow parameter.

            :param description: The parameter's description.
            :param optional: Whether the parameter is optional.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflowversion-workflowparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_omics import mixins as omics_mixins
                
                workflow_parameter_property = omics_mixins.CfnWorkflowVersionPropsMixin.WorkflowParameterProperty(
                    description="description",
                    optional=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2c27231769673386a21aa7afb39bb8209c7f8344c7518d3ade314723f4711bec)
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument optional", value=optional, expected_type=type_hints["optional"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if description is not None:
                self._values["description"] = description
            if optional is not None:
                self._values["optional"] = optional

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The parameter's description.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflowversion-workflowparameter.html#cfn-omics-workflowversion-workflowparameter-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def optional(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Whether the parameter is optional.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflowversion-workflowparameter.html#cfn-omics-workflowversion-workflowparameter-optional
            '''
            result = self._values.get("optional")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WorkflowParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnAnnotationStoreMixinProps",
    "CfnAnnotationStorePropsMixin",
    "CfnReferenceStoreMixinProps",
    "CfnReferenceStorePropsMixin",
    "CfnRunGroupMixinProps",
    "CfnRunGroupPropsMixin",
    "CfnSequenceStoreMixinProps",
    "CfnSequenceStorePropsMixin",
    "CfnVariantStoreMixinProps",
    "CfnVariantStorePropsMixin",
    "CfnWorkflowMixinProps",
    "CfnWorkflowPropsMixin",
    "CfnWorkflowVersionMixinProps",
    "CfnWorkflowVersionPropsMixin",
]

publication.publish()

def _typecheckingstub__7fd1930d504019f85b2d4f5f092b3bf4ebcb5467e30d7ce356687164fd5d2596(
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    reference: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnnotationStorePropsMixin.ReferenceItemProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sse_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnnotationStorePropsMixin.SseConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    store_format: typing.Optional[builtins.str] = None,
    store_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnnotationStorePropsMixin.StoreOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffaa0ceb2e260e4b97b90f7226274ff4b656203315922e8a97de77a1457c0ce3(
    props: typing.Union[CfnAnnotationStoreMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ffe126b7d5e1ebc80014efa43c2ccf2e7c197849e25d2398c5590a7b6672ca5(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2a72490bf6a1e859fe0e8a3a9a6d0751fb684ad04f4030220ebdae40df84dea(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88ec759af4fca909790631365468237109cb84de41d2990a6b77d2ab7a41cf61(
    *,
    reference_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a93b4feb4760350e32723c91cf69e21702b85e0aa0986302b40543845774eb0(
    *,
    key_arn: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d57283f116b5ff96110bdf1ffa762216da84abd236f1c0cff3a3562122fe8d46(
    *,
    tsv_store_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnnotationStorePropsMixin.TsvStoreOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58697273262149196841fe6d9baf4798e156827c6fd15f074d97fb9c4a79cd0a(
    *,
    annotation_type: typing.Optional[builtins.str] = None,
    format_to_header: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    schema: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08d373682e15ba8f7650ae17944f60651c594b6060862cfa30b1bfae95d4d9be(
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    sse_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnReferenceStorePropsMixin.SseConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f3a1cf2336bc81f5cb5c2b72433504b3f3ee5c0faf70ee508dd63640e8799a0(
    props: typing.Union[CfnReferenceStoreMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a844aaa6c531e1c6feb54548e39cb8599cd81cb409bfc4d114b7bcea2a066e1f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f545595f6a2bc2f1a080f20a5fcd929f409164d65f3de851372922c777288711(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7678d4c65dd8c5358fbd8fe0791d1a7a45f06d8039962aef0ae51cd7c5530d48(
    *,
    key_arn: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fe9859866cf051f02716000b295c2d7e4aa3a604565dd6e013ade7ecea38dda(
    *,
    max_cpus: typing.Optional[jsii.Number] = None,
    max_duration: typing.Optional[jsii.Number] = None,
    max_gpus: typing.Optional[jsii.Number] = None,
    max_runs: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__644d1c24db634ad86dcb8b3c2b03c354596d676573943c00fff74a8b1afe935f(
    props: typing.Union[CfnRunGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d2b75a7c5159ec80ae0456fbb2e91cfa73d4b4a2045c44a3cb84d5028c501b0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fd6edd4b58411606dc3003beabc7b183c0a01c44de00efb07d1fb996d7be874(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e50fdeb3f1a17a7c134d4fbc5390a39229fcbd4b49e1dec67ced238c418f8f0(
    *,
    access_log_location: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    e_tag_algorithm_family: typing.Optional[builtins.str] = None,
    fallback_location: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    propagated_set_level_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    s3_access_policy: typing.Any = None,
    sse_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSequenceStorePropsMixin.SseConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__034f622df244678961755e12f0d198ffc4435b8b12cc142ef015cf4e60a0ac3e(
    props: typing.Union[CfnSequenceStoreMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dff85d1f5c8d4f0bdd6a056d4dee51a2d788dea513ee8cf1099ca0da8394d7c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__085a7483715ba6e727c69cd2398672e07d706a40cab9a275e5dbfe120b552d45(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2071ecc260c3fba581a7ba46761e6a2e5aa1f3314e8eceb5cc6a00b29b29bbdc(
    *,
    key_arn: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f3fb40c2dbe210e1fcce9e4baee95d8ad31a753546e7471faf54c3dede9471d(
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    reference: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVariantStorePropsMixin.ReferenceItemProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sse_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVariantStorePropsMixin.SseConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e17b8ea2c7e45651b20aefc47cff22b5b19e88c136ab3f18db830671fd3bb8ed(
    props: typing.Union[CfnVariantStoreMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__710ad934ede7ae69b91a77ab33aabf42f24ec976cb2e36d4a2a4b01b1f19f3bf(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fab8c7e5f4dc8a49dcbae0d5b01fed7c8137bd1ebaa875df758ff7c3d8096ba9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70d4747cd289a01303759c5fd0c0d87281d659a02ebc7b99b0a9c30ac5c9254c(
    *,
    reference_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c31a6e65a7dc2b9cde211ac816a12798d4386e7ee26eee153e898be3bbc2814(
    *,
    key_arn: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__438aacdaa1fbffa26ad2da00febb74751eaa467bf2e329a901375faa13d6d3ab(
    *,
    accelerators: typing.Optional[builtins.str] = None,
    container_registry_map: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkflowPropsMixin.ContainerRegistryMapProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    container_registry_map_uri: typing.Optional[builtins.str] = None,
    definition_repository: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkflowPropsMixin.DefinitionRepositoryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    definition_uri: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    engine: typing.Optional[builtins.str] = None,
    main: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    parameter_template: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkflowPropsMixin.WorkflowParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    parameter_template_path: typing.Optional[builtins.str] = None,
    readme_markdown: typing.Optional[builtins.str] = None,
    readme_path: typing.Optional[builtins.str] = None,
    readme_uri: typing.Optional[builtins.str] = None,
    storage_capacity: typing.Optional[jsii.Number] = None,
    storage_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    workflow_bucket_owner_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec3d9acd00b3f5f58f11bd55765b54ff39e93ff04c38bed55917737e366f61aa(
    props: typing.Union[CfnWorkflowMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e19068365dd36d3c51d957f50f1ccc8c68d83c8a3b6de02e9c5ef9c1e8fce0d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6347f8877e0e5b3fd632db17788b818a561d14e1c060c1aa64fcde4b1a43b64(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d0d7eaa2f9d46704b83f12fac0f8940ed23339763fd79a1935b4deba03acc7d(
    *,
    image_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkflowPropsMixin.ImageMappingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    registry_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkflowPropsMixin.RegistryMappingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbff32ea4d5666b62265634f0aa0a0f94babd5ed53a54b60d6c14b8c789c52ac(
    *,
    connection_arn: typing.Optional[builtins.str] = None,
    exclude_file_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    full_repository_id: typing.Optional[builtins.str] = None,
    source_reference: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkflowPropsMixin.SourceReferenceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9d50e088ae380494b46dad2fc59ffccb888d9f069336fd815d4a0a86fdbc2ae(
    *,
    destination_image: typing.Optional[builtins.str] = None,
    source_image: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7065969cf0a0ddb15f11f31a6bb8f71899275a76dfd3d6b2c31336ad3ab56711(
    *,
    ecr_account_id: typing.Optional[builtins.str] = None,
    ecr_repository_prefix: typing.Optional[builtins.str] = None,
    upstream_registry_url: typing.Optional[builtins.str] = None,
    upstream_repository_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15444e47a78a0618c79f08cf7929c5fc3299b96d9b97f26503065c0226fc3693(
    *,
    type: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f39ef17cfe3250cd9d03177b3f93e9d1b138ae2cb0ae86aab078681401d832a5(
    *,
    description: typing.Optional[builtins.str] = None,
    optional: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5c614a882083328766c3036a05054e08e9bb3e634f6aebbadcb7bb32bc49d68(
    *,
    accelerators: typing.Optional[builtins.str] = None,
    container_registry_map: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkflowVersionPropsMixin.ContainerRegistryMapProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    container_registry_map_uri: typing.Optional[builtins.str] = None,
    definition_repository: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkflowVersionPropsMixin.DefinitionRepositoryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    definition_uri: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    engine: typing.Optional[builtins.str] = None,
    main: typing.Optional[builtins.str] = None,
    parameter_template: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkflowVersionPropsMixin.WorkflowParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    parameter_template_path: typing.Optional[builtins.str] = None,
    readme_markdown: typing.Optional[builtins.str] = None,
    readme_path: typing.Optional[builtins.str] = None,
    readme_uri: typing.Optional[builtins.str] = None,
    storage_capacity: typing.Optional[jsii.Number] = None,
    storage_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    version_name: typing.Optional[builtins.str] = None,
    workflow_bucket_owner_id: typing.Optional[builtins.str] = None,
    workflow_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89e4ce7b47495166b2898e02f5a0d9f3f99b61f435215612773e4f3d79175462(
    props: typing.Union[CfnWorkflowVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23b4f30def0d9320b0386b674c3e099c1d19bdabcdc6b80f2e7daec5fc706800(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7622b13513619777fbb7db7429b245728ee66570c17c3e7b5185ba868aba67d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c908dc0d7533ff0f647ef36f4b5cf3f6dbd6f56b37098b5e10d9b48616f2a094(
    *,
    image_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkflowVersionPropsMixin.ImageMappingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    registry_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkflowVersionPropsMixin.RegistryMappingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b32add453d6d98bdc68729d569ebbc4ad09d25fb446e496f5084482a7b0982d(
    *,
    connection_arn: typing.Optional[builtins.str] = None,
    exclude_file_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    full_repository_id: typing.Optional[builtins.str] = None,
    source_reference: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkflowVersionPropsMixin.SourceReferenceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55635076a1d3476178dacdb6667123af3ef39b100eb7e29c4693a7f0e9401571(
    *,
    destination_image: typing.Optional[builtins.str] = None,
    source_image: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__434bdbf3f9121658be2fd6a32d6752dce5ebb2192d6183a651550a7600c59812(
    *,
    ecr_account_id: typing.Optional[builtins.str] = None,
    ecr_repository_prefix: typing.Optional[builtins.str] = None,
    upstream_registry_url: typing.Optional[builtins.str] = None,
    upstream_repository_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c4d4b659903987c3f10211981068e4779ac0f2db08fddb030303f2fc118f342(
    *,
    type: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c27231769673386a21aa7afb39bb8209c7f8344c7518d3ade314723f4711bec(
    *,
    description: typing.Optional[builtins.str] = None,
    optional: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass
