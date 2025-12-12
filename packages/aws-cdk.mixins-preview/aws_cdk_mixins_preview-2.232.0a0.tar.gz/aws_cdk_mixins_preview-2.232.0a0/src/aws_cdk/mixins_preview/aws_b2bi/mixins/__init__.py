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
import aws_cdk.interfaces.aws_kinesisfirehose as _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d
import aws_cdk.interfaces.aws_logs as _aws_cdk_interfaces_aws_logs_ceddda9d
import aws_cdk.interfaces.aws_s3 as _aws_cdk_interfaces_aws_s3_ceddda9d
import constructs as _constructs_77d1e7e8
from ...aws_logs import ILogsDelivery as _ILogsDelivery_0d3c9e29
from ...core import IMixin as _IMixin_11e4b965, Mixin as _Mixin_a69446c0
from ...mixins import (
    CfnPropertyMixinOptions as _CfnPropertyMixinOptions_9cbff649,
    PropertyMergeStrategy as _PropertyMergeStrategy_49c157e8,
)


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_b2bi.mixins.CfnCapabilityMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "configuration": "configuration",
        "instructions_documents": "instructionsDocuments",
        "name": "name",
        "tags": "tags",
        "type": "type",
    },
)
class CfnCapabilityMixinProps:
    def __init__(
        self,
        *,
        configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCapabilityPropsMixin.CapabilityConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        instructions_documents: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCapabilityPropsMixin.S3LocationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnCapabilityPropsMixin.

        :param configuration: Specifies a structure that contains the details for a capability.
        :param instructions_documents: Specifies one or more locations in Amazon S3, each specifying an EDI document that can be used with this capability. Each item contains the name of the bucket and the key, to identify the document's location.
        :param name: The display name of the capability.
        :param tags: Specifies the key-value pairs assigned to ARNs that you can use to group and search for resources by type. You can attach this metadata to resources (capabilities, partnerships, and so on) for any purpose.
        :param type: Returns the type of the capability. Currently, only ``edi`` is supported.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-b2bi-capability.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_b2bi import mixins as b2bi_mixins
            
            cfn_capability_mixin_props = b2bi_mixins.CfnCapabilityMixinProps(
                configuration=b2bi_mixins.CfnCapabilityPropsMixin.CapabilityConfigurationProperty(
                    edi=b2bi_mixins.CfnCapabilityPropsMixin.EdiConfigurationProperty(
                        capability_direction="capabilityDirection",
                        input_location=b2bi_mixins.CfnCapabilityPropsMixin.S3LocationProperty(
                            bucket_name="bucketName",
                            key="key"
                        ),
                        output_location=b2bi_mixins.CfnCapabilityPropsMixin.S3LocationProperty(
                            bucket_name="bucketName",
                            key="key"
                        ),
                        transformer_id="transformerId",
                        type=b2bi_mixins.CfnCapabilityPropsMixin.EdiTypeProperty(
                            x12_details=b2bi_mixins.CfnCapabilityPropsMixin.X12DetailsProperty(
                                transaction_set="transactionSet",
                                version="version"
                            )
                        )
                    )
                ),
                instructions_documents=[b2bi_mixins.CfnCapabilityPropsMixin.S3LocationProperty(
                    bucket_name="bucketName",
                    key="key"
                )],
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dce9aca7b56830b8d70b8da41b731edab28ce419a8a49c235f2cc0fd5643ffda)
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument instructions_documents", value=instructions_documents, expected_type=type_hints["instructions_documents"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if configuration is not None:
            self._values["configuration"] = configuration
        if instructions_documents is not None:
            self._values["instructions_documents"] = instructions_documents
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCapabilityPropsMixin.CapabilityConfigurationProperty"]]:
        '''Specifies a structure that contains the details for a capability.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-b2bi-capability.html#cfn-b2bi-capability-configuration
        '''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCapabilityPropsMixin.CapabilityConfigurationProperty"]], result)

    @builtins.property
    def instructions_documents(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCapabilityPropsMixin.S3LocationProperty"]]]]:
        '''Specifies one or more locations in Amazon S3, each specifying an EDI document that can be used with this capability.

        Each item contains the name of the bucket and the key, to identify the document's location.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-b2bi-capability.html#cfn-b2bi-capability-instructionsdocuments
        '''
        result = self._values.get("instructions_documents")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCapabilityPropsMixin.S3LocationProperty"]]]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The display name of the capability.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-b2bi-capability.html#cfn-b2bi-capability-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Specifies the key-value pairs assigned to ARNs that you can use to group and search for resources by type.

        You can attach this metadata to resources (capabilities, partnerships, and so on) for any purpose.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-b2bi-capability.html#cfn-b2bi-capability-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Returns the type of the capability.

        Currently, only ``edi`` is supported.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-b2bi-capability.html#cfn-b2bi-capability-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCapabilityMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnCapabilityPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_b2bi.mixins.CfnCapabilityPropsMixin",
):
    '''Instantiates a capability based on the specified parameters.

    A trading capability contains the information required to transform incoming EDI documents into JSON or XML outputs.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-b2bi-capability.html
    :cloudformationResource: AWS::B2BI::Capability
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_b2bi import mixins as b2bi_mixins
        
        cfn_capability_props_mixin = b2bi_mixins.CfnCapabilityPropsMixin(b2bi_mixins.CfnCapabilityMixinProps(
            configuration=b2bi_mixins.CfnCapabilityPropsMixin.CapabilityConfigurationProperty(
                edi=b2bi_mixins.CfnCapabilityPropsMixin.EdiConfigurationProperty(
                    capability_direction="capabilityDirection",
                    input_location=b2bi_mixins.CfnCapabilityPropsMixin.S3LocationProperty(
                        bucket_name="bucketName",
                        key="key"
                    ),
                    output_location=b2bi_mixins.CfnCapabilityPropsMixin.S3LocationProperty(
                        bucket_name="bucketName",
                        key="key"
                    ),
                    transformer_id="transformerId",
                    type=b2bi_mixins.CfnCapabilityPropsMixin.EdiTypeProperty(
                        x12_details=b2bi_mixins.CfnCapabilityPropsMixin.X12DetailsProperty(
                            transaction_set="transactionSet",
                            version="version"
                        )
                    )
                )
            ),
            instructions_documents=[b2bi_mixins.CfnCapabilityPropsMixin.S3LocationProperty(
                bucket_name="bucketName",
                key="key"
            )],
            name="name",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            type="type"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnCapabilityMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::B2BI::Capability``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35d034b3ec61d31e902579638ba75dbc3d0b5be8b2acfd81e35609e8889d2e99)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a39687d9d6f7fea3063bffec9d0b6810aabd81dca1e18f407198df65364b4b9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d9cb4db8aad84e68aa3ded3a687acae65ae994a536311dc2743bbf877d2b095)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnCapabilityMixinProps:
        return typing.cast(CfnCapabilityMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_b2bi.mixins.CfnCapabilityPropsMixin.CapabilityConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"edi": "edi"},
    )
    class CapabilityConfigurationProperty:
        def __init__(
            self,
            *,
            edi: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCapabilityPropsMixin.EdiConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A capability object.

            Currently, only EDI (electronic data interchange) capabilities are supported. A trading capability contains the information required to transform incoming EDI documents into JSON or XML outputs.

            :param edi: An EDI (electronic data interchange) configuration object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-capability-capabilityconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_b2bi import mixins as b2bi_mixins
                
                capability_configuration_property = b2bi_mixins.CfnCapabilityPropsMixin.CapabilityConfigurationProperty(
                    edi=b2bi_mixins.CfnCapabilityPropsMixin.EdiConfigurationProperty(
                        capability_direction="capabilityDirection",
                        input_location=b2bi_mixins.CfnCapabilityPropsMixin.S3LocationProperty(
                            bucket_name="bucketName",
                            key="key"
                        ),
                        output_location=b2bi_mixins.CfnCapabilityPropsMixin.S3LocationProperty(
                            bucket_name="bucketName",
                            key="key"
                        ),
                        transformer_id="transformerId",
                        type=b2bi_mixins.CfnCapabilityPropsMixin.EdiTypeProperty(
                            x12_details=b2bi_mixins.CfnCapabilityPropsMixin.X12DetailsProperty(
                                transaction_set="transactionSet",
                                version="version"
                            )
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__07f4fe6f786f716906f55216151655d975837a17006622fddb63ddce3a58b30c)
                check_type(argname="argument edi", value=edi, expected_type=type_hints["edi"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if edi is not None:
                self._values["edi"] = edi

        @builtins.property
        def edi(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCapabilityPropsMixin.EdiConfigurationProperty"]]:
            '''An EDI (electronic data interchange) configuration object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-capability-capabilityconfiguration.html#cfn-b2bi-capability-capabilityconfiguration-edi
            '''
            result = self._values.get("edi")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCapabilityPropsMixin.EdiConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CapabilityConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_b2bi.mixins.CfnCapabilityPropsMixin.EdiConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "capability_direction": "capabilityDirection",
            "input_location": "inputLocation",
            "output_location": "outputLocation",
            "transformer_id": "transformerId",
            "type": "type",
        },
    )
    class EdiConfigurationProperty:
        def __init__(
            self,
            *,
            capability_direction: typing.Optional[builtins.str] = None,
            input_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCapabilityPropsMixin.S3LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            output_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCapabilityPropsMixin.S3LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            transformer_id: typing.Optional[builtins.str] = None,
            type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCapabilityPropsMixin.EdiTypeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the details for the EDI (electronic data interchange) transformation.

            :param capability_direction: Specifies whether this is capability is for inbound or outbound transformations.
            :param input_location: Contains the Amazon S3 bucket and prefix for the location of the input file, which is contained in an ``S3Location`` object.
            :param output_location: Contains the Amazon S3 bucket and prefix for the location of the output file, which is contained in an ``S3Location`` object.
            :param transformer_id: Returns the system-assigned unique identifier for the transformer.
            :param type: Returns the type of the capability. Currently, only ``edi`` is supported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-capability-ediconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_b2bi import mixins as b2bi_mixins
                
                edi_configuration_property = b2bi_mixins.CfnCapabilityPropsMixin.EdiConfigurationProperty(
                    capability_direction="capabilityDirection",
                    input_location=b2bi_mixins.CfnCapabilityPropsMixin.S3LocationProperty(
                        bucket_name="bucketName",
                        key="key"
                    ),
                    output_location=b2bi_mixins.CfnCapabilityPropsMixin.S3LocationProperty(
                        bucket_name="bucketName",
                        key="key"
                    ),
                    transformer_id="transformerId",
                    type=b2bi_mixins.CfnCapabilityPropsMixin.EdiTypeProperty(
                        x12_details=b2bi_mixins.CfnCapabilityPropsMixin.X12DetailsProperty(
                            transaction_set="transactionSet",
                            version="version"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6db49fa4bf41a35876584c803c3f863ce7a3128787e986fe0ab14198840f2928)
                check_type(argname="argument capability_direction", value=capability_direction, expected_type=type_hints["capability_direction"])
                check_type(argname="argument input_location", value=input_location, expected_type=type_hints["input_location"])
                check_type(argname="argument output_location", value=output_location, expected_type=type_hints["output_location"])
                check_type(argname="argument transformer_id", value=transformer_id, expected_type=type_hints["transformer_id"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if capability_direction is not None:
                self._values["capability_direction"] = capability_direction
            if input_location is not None:
                self._values["input_location"] = input_location
            if output_location is not None:
                self._values["output_location"] = output_location
            if transformer_id is not None:
                self._values["transformer_id"] = transformer_id
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def capability_direction(self) -> typing.Optional[builtins.str]:
            '''Specifies whether this is capability is for inbound or outbound transformations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-capability-ediconfiguration.html#cfn-b2bi-capability-ediconfiguration-capabilitydirection
            '''
            result = self._values.get("capability_direction")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def input_location(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCapabilityPropsMixin.S3LocationProperty"]]:
            '''Contains the Amazon S3 bucket and prefix for the location of the input file, which is contained in an ``S3Location`` object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-capability-ediconfiguration.html#cfn-b2bi-capability-ediconfiguration-inputlocation
            '''
            result = self._values.get("input_location")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCapabilityPropsMixin.S3LocationProperty"]], result)

        @builtins.property
        def output_location(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCapabilityPropsMixin.S3LocationProperty"]]:
            '''Contains the Amazon S3 bucket and prefix for the location of the output file, which is contained in an ``S3Location`` object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-capability-ediconfiguration.html#cfn-b2bi-capability-ediconfiguration-outputlocation
            '''
            result = self._values.get("output_location")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCapabilityPropsMixin.S3LocationProperty"]], result)

        @builtins.property
        def transformer_id(self) -> typing.Optional[builtins.str]:
            '''Returns the system-assigned unique identifier for the transformer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-capability-ediconfiguration.html#cfn-b2bi-capability-ediconfiguration-transformerid
            '''
            result = self._values.get("transformer_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCapabilityPropsMixin.EdiTypeProperty"]]:
            '''Returns the type of the capability.

            Currently, only ``edi`` is supported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-capability-ediconfiguration.html#cfn-b2bi-capability-ediconfiguration-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCapabilityPropsMixin.EdiTypeProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EdiConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_b2bi.mixins.CfnCapabilityPropsMixin.EdiTypeProperty",
        jsii_struct_bases=[],
        name_mapping={"x12_details": "x12Details"},
    )
    class EdiTypeProperty:
        def __init__(
            self,
            *,
            x12_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCapabilityPropsMixin.X12DetailsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param x12_details: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-capability-editype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_b2bi import mixins as b2bi_mixins
                
                edi_type_property = b2bi_mixins.CfnCapabilityPropsMixin.EdiTypeProperty(
                    x12_details=b2bi_mixins.CfnCapabilityPropsMixin.X12DetailsProperty(
                        transaction_set="transactionSet",
                        version="version"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c4a5968b6812b36ba00ddf6ad26d5988861e150c652ea518958da96f1a9397f4)
                check_type(argname="argument x12_details", value=x12_details, expected_type=type_hints["x12_details"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if x12_details is not None:
                self._values["x12_details"] = x12_details

        @builtins.property
        def x12_details(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCapabilityPropsMixin.X12DetailsProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-capability-editype.html#cfn-b2bi-capability-editype-x12details
            '''
            result = self._values.get("x12_details")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCapabilityPropsMixin.X12DetailsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EdiTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_b2bi.mixins.CfnCapabilityPropsMixin.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket_name": "bucketName", "key": "key"},
    )
    class S3LocationProperty:
        def __init__(
            self,
            *,
            bucket_name: typing.Optional[builtins.str] = None,
            key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the details for the Amazon S3 file location that is being used with AWS B2B Data Interchange.

            File locations in Amazon S3 are identified using a combination of the bucket and key.

            :param bucket_name: Specifies the name of the Amazon S3 bucket.
            :param key: Specifies the Amazon S3 key for the file location.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-capability-s3location.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_b2bi import mixins as b2bi_mixins
                
                s3_location_property = b2bi_mixins.CfnCapabilityPropsMixin.S3LocationProperty(
                    bucket_name="bucketName",
                    key="key"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9d5c22e56c407e45985642888fd2ad0df2eafc6da563993031a707306346e927)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_name is not None:
                self._values["bucket_name"] = bucket_name
            if key is not None:
                self._values["key"] = key

        @builtins.property
        def bucket_name(self) -> typing.Optional[builtins.str]:
            '''Specifies the name of the Amazon S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-capability-s3location.html#cfn-b2bi-capability-s3location-bucketname
            '''
            result = self._values.get("bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''Specifies the Amazon S3 key for the file location.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-capability-s3location.html#cfn-b2bi-capability-s3location-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_b2bi.mixins.CfnCapabilityPropsMixin.X12DetailsProperty",
        jsii_struct_bases=[],
        name_mapping={"transaction_set": "transactionSet", "version": "version"},
    )
    class X12DetailsProperty:
        def __init__(
            self,
            *,
            transaction_set: typing.Optional[builtins.str] = None,
            version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure that contains the X12 transaction set and version.

            The X12 structure is used when the system transforms an EDI (electronic data interchange) file.
            .. epigraph::

               If an EDI input file contains more than one transaction, each transaction must have the same transaction set and version, for example 214/4010. If not, the transformer cannot parse the file.

            :param transaction_set: Returns an enumerated type where each value identifies an X12 transaction set. Transaction sets are maintained by the X12 Accredited Standards Committee.
            :param version: Returns the version to use for the specified X12 transaction set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-capability-x12details.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_b2bi import mixins as b2bi_mixins
                
                x12_details_property = b2bi_mixins.CfnCapabilityPropsMixin.X12DetailsProperty(
                    transaction_set="transactionSet",
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d9042dd5f7af45302ad3970d80f730c4a3f9209aeb8d6b5ad96c27a580cfda2e)
                check_type(argname="argument transaction_set", value=transaction_set, expected_type=type_hints["transaction_set"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if transaction_set is not None:
                self._values["transaction_set"] = transaction_set
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def transaction_set(self) -> typing.Optional[builtins.str]:
            '''Returns an enumerated type where each value identifies an X12 transaction set.

            Transaction sets are maintained by the X12 Accredited Standards Committee.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-capability-x12details.html#cfn-b2bi-capability-x12details-transactionset
            '''
            result = self._values.get("transaction_set")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''Returns the version to use for the specified X12 transaction set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-capability-x12details.html#cfn-b2bi-capability-x12details-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "X12DetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_b2bi.mixins.CfnPartnershipMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "capabilities": "capabilities",
        "capability_options": "capabilityOptions",
        "email": "email",
        "name": "name",
        "phone": "phone",
        "profile_id": "profileId",
        "tags": "tags",
    },
)
class CfnPartnershipMixinProps:
    def __init__(
        self,
        *,
        capabilities: typing.Optional[typing.Sequence[builtins.str]] = None,
        capability_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPartnershipPropsMixin.CapabilityOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        email: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        phone: typing.Optional[builtins.str] = None,
        profile_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnPartnershipPropsMixin.

        :param capabilities: Returns one or more capabilities associated with this partnership.
        :param capability_options: Contains the details for an Outbound EDI capability.
        :param email: Specifies the email address associated with this trading partner.
        :param name: Returns the name of the partnership.
        :param phone: Specifies the phone number associated with the partnership.
        :param profile_id: Returns the unique, system-generated identifier for the profile connected to this partnership.
        :param tags: A key-value pair for a specific partnership. Tags are metadata that you can use to search for and group capabilities for various purposes.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-b2bi-partnership.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_b2bi import mixins as b2bi_mixins
            
            cfn_partnership_mixin_props = b2bi_mixins.CfnPartnershipMixinProps(
                capabilities=["capabilities"],
                capability_options=b2bi_mixins.CfnPartnershipPropsMixin.CapabilityOptionsProperty(
                    inbound_edi=b2bi_mixins.CfnPartnershipPropsMixin.InboundEdiOptionsProperty(
                        x12=b2bi_mixins.CfnPartnershipPropsMixin.X12InboundEdiOptionsProperty(
                            acknowledgment_options=b2bi_mixins.CfnPartnershipPropsMixin.X12AcknowledgmentOptionsProperty(
                                functional_acknowledgment="functionalAcknowledgment",
                                technical_acknowledgment="technicalAcknowledgment"
                            )
                        )
                    ),
                    outbound_edi=b2bi_mixins.CfnPartnershipPropsMixin.OutboundEdiOptionsProperty(
                        x12=b2bi_mixins.CfnPartnershipPropsMixin.X12EnvelopeProperty(
                            common=b2bi_mixins.CfnPartnershipPropsMixin.X12OutboundEdiHeadersProperty(
                                control_numbers=b2bi_mixins.CfnPartnershipPropsMixin.X12ControlNumbersProperty(
                                    starting_functional_group_control_number=123,
                                    starting_interchange_control_number=123,
                                    starting_transaction_set_control_number=123
                                ),
                                delimiters=b2bi_mixins.CfnPartnershipPropsMixin.X12DelimitersProperty(
                                    component_separator="componentSeparator",
                                    data_element_separator="dataElementSeparator",
                                    segment_terminator="segmentTerminator"
                                ),
                                functional_group_headers=b2bi_mixins.CfnPartnershipPropsMixin.X12FunctionalGroupHeadersProperty(
                                    application_receiver_code="applicationReceiverCode",
                                    application_sender_code="applicationSenderCode",
                                    responsible_agency_code="responsibleAgencyCode"
                                ),
                                gs05_time_format="gs05TimeFormat",
                                interchange_control_headers=b2bi_mixins.CfnPartnershipPropsMixin.X12InterchangeControlHeadersProperty(
                                    acknowledgment_requested_code="acknowledgmentRequestedCode",
                                    receiver_id="receiverId",
                                    receiver_id_qualifier="receiverIdQualifier",
                                    repetition_separator="repetitionSeparator",
                                    sender_id="senderId",
                                    sender_id_qualifier="senderIdQualifier",
                                    usage_indicator_code="usageIndicatorCode"
                                ),
                                validate_edi=False
                            ),
                            wrap_options=b2bi_mixins.CfnPartnershipPropsMixin.WrapOptionsProperty(
                                line_length=123,
                                line_terminator="lineTerminator",
                                wrap_by="wrapBy"
                            )
                        )
                    )
                ),
                email="email",
                name="name",
                phone="phone",
                profile_id="profileId",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8901d41f818f4201c5757adf696cccad27ccee9deab42badc7199427919b96cc)
            check_type(argname="argument capabilities", value=capabilities, expected_type=type_hints["capabilities"])
            check_type(argname="argument capability_options", value=capability_options, expected_type=type_hints["capability_options"])
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument phone", value=phone, expected_type=type_hints["phone"])
            check_type(argname="argument profile_id", value=profile_id, expected_type=type_hints["profile_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if capabilities is not None:
            self._values["capabilities"] = capabilities
        if capability_options is not None:
            self._values["capability_options"] = capability_options
        if email is not None:
            self._values["email"] = email
        if name is not None:
            self._values["name"] = name
        if phone is not None:
            self._values["phone"] = phone
        if profile_id is not None:
            self._values["profile_id"] = profile_id
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def capabilities(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Returns one or more capabilities associated with this partnership.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-b2bi-partnership.html#cfn-b2bi-partnership-capabilities
        '''
        result = self._values.get("capabilities")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def capability_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPartnershipPropsMixin.CapabilityOptionsProperty"]]:
        '''Contains the details for an Outbound EDI capability.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-b2bi-partnership.html#cfn-b2bi-partnership-capabilityoptions
        '''
        result = self._values.get("capability_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPartnershipPropsMixin.CapabilityOptionsProperty"]], result)

    @builtins.property
    def email(self) -> typing.Optional[builtins.str]:
        '''Specifies the email address associated with this trading partner.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-b2bi-partnership.html#cfn-b2bi-partnership-email
        '''
        result = self._values.get("email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Returns the name of the partnership.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-b2bi-partnership.html#cfn-b2bi-partnership-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def phone(self) -> typing.Optional[builtins.str]:
        '''Specifies the phone number associated with the partnership.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-b2bi-partnership.html#cfn-b2bi-partnership-phone
        '''
        result = self._values.get("phone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def profile_id(self) -> typing.Optional[builtins.str]:
        '''Returns the unique, system-generated identifier for the profile connected to this partnership.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-b2bi-partnership.html#cfn-b2bi-partnership-profileid
        '''
        result = self._values.get("profile_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A key-value pair for a specific partnership.

        Tags are metadata that you can use to search for and group capabilities for various purposes.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-b2bi-partnership.html#cfn-b2bi-partnership-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPartnershipMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPartnershipPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_b2bi.mixins.CfnPartnershipPropsMixin",
):
    '''Creates a partnership between a customer and a trading partner, based on the supplied parameters.

    A partnership represents the connection between you and your trading partner. It ties together a profile and one or more trading capabilities.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-b2bi-partnership.html
    :cloudformationResource: AWS::B2BI::Partnership
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_b2bi import mixins as b2bi_mixins
        
        cfn_partnership_props_mixin = b2bi_mixins.CfnPartnershipPropsMixin(b2bi_mixins.CfnPartnershipMixinProps(
            capabilities=["capabilities"],
            capability_options=b2bi_mixins.CfnPartnershipPropsMixin.CapabilityOptionsProperty(
                inbound_edi=b2bi_mixins.CfnPartnershipPropsMixin.InboundEdiOptionsProperty(
                    x12=b2bi_mixins.CfnPartnershipPropsMixin.X12InboundEdiOptionsProperty(
                        acknowledgment_options=b2bi_mixins.CfnPartnershipPropsMixin.X12AcknowledgmentOptionsProperty(
                            functional_acknowledgment="functionalAcknowledgment",
                            technical_acknowledgment="technicalAcknowledgment"
                        )
                    )
                ),
                outbound_edi=b2bi_mixins.CfnPartnershipPropsMixin.OutboundEdiOptionsProperty(
                    x12=b2bi_mixins.CfnPartnershipPropsMixin.X12EnvelopeProperty(
                        common=b2bi_mixins.CfnPartnershipPropsMixin.X12OutboundEdiHeadersProperty(
                            control_numbers=b2bi_mixins.CfnPartnershipPropsMixin.X12ControlNumbersProperty(
                                starting_functional_group_control_number=123,
                                starting_interchange_control_number=123,
                                starting_transaction_set_control_number=123
                            ),
                            delimiters=b2bi_mixins.CfnPartnershipPropsMixin.X12DelimitersProperty(
                                component_separator="componentSeparator",
                                data_element_separator="dataElementSeparator",
                                segment_terminator="segmentTerminator"
                            ),
                            functional_group_headers=b2bi_mixins.CfnPartnershipPropsMixin.X12FunctionalGroupHeadersProperty(
                                application_receiver_code="applicationReceiverCode",
                                application_sender_code="applicationSenderCode",
                                responsible_agency_code="responsibleAgencyCode"
                            ),
                            gs05_time_format="gs05TimeFormat",
                            interchange_control_headers=b2bi_mixins.CfnPartnershipPropsMixin.X12InterchangeControlHeadersProperty(
                                acknowledgment_requested_code="acknowledgmentRequestedCode",
                                receiver_id="receiverId",
                                receiver_id_qualifier="receiverIdQualifier",
                                repetition_separator="repetitionSeparator",
                                sender_id="senderId",
                                sender_id_qualifier="senderIdQualifier",
                                usage_indicator_code="usageIndicatorCode"
                            ),
                            validate_edi=False
                        ),
                        wrap_options=b2bi_mixins.CfnPartnershipPropsMixin.WrapOptionsProperty(
                            line_length=123,
                            line_terminator="lineTerminator",
                            wrap_by="wrapBy"
                        )
                    )
                )
            ),
            email="email",
            name="name",
            phone="phone",
            profile_id="profileId",
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
        props: typing.Union[CfnPartnershipMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::B2BI::Partnership``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4be908f6cc44b8659e34f1cf861a9e93fa8fd6f897164f38ed9e2157ee85d3c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__084bf1941ce36849245e0c5ce486b00e59893dbbccea076347b91b29c715d2d3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9204e83393f6b13c2507168754e578e97e182d69781a5fa3f8bddb3e4b26eca0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPartnershipMixinProps:
        return typing.cast(CfnPartnershipMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_b2bi.mixins.CfnPartnershipPropsMixin.CapabilityOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"inbound_edi": "inboundEdi", "outbound_edi": "outboundEdi"},
    )
    class CapabilityOptionsProperty:
        def __init__(
            self,
            *,
            inbound_edi: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPartnershipPropsMixin.InboundEdiOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            outbound_edi: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPartnershipPropsMixin.OutboundEdiOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains the details for an Outbound EDI capability.

            :param inbound_edi: A structure that contains the inbound EDI options for the capability.
            :param outbound_edi: A structure that contains the outbound EDI options.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-partnership-capabilityoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_b2bi import mixins as b2bi_mixins
                
                capability_options_property = b2bi_mixins.CfnPartnershipPropsMixin.CapabilityOptionsProperty(
                    inbound_edi=b2bi_mixins.CfnPartnershipPropsMixin.InboundEdiOptionsProperty(
                        x12=b2bi_mixins.CfnPartnershipPropsMixin.X12InboundEdiOptionsProperty(
                            acknowledgment_options=b2bi_mixins.CfnPartnershipPropsMixin.X12AcknowledgmentOptionsProperty(
                                functional_acknowledgment="functionalAcknowledgment",
                                technical_acknowledgment="technicalAcknowledgment"
                            )
                        )
                    ),
                    outbound_edi=b2bi_mixins.CfnPartnershipPropsMixin.OutboundEdiOptionsProperty(
                        x12=b2bi_mixins.CfnPartnershipPropsMixin.X12EnvelopeProperty(
                            common=b2bi_mixins.CfnPartnershipPropsMixin.X12OutboundEdiHeadersProperty(
                                control_numbers=b2bi_mixins.CfnPartnershipPropsMixin.X12ControlNumbersProperty(
                                    starting_functional_group_control_number=123,
                                    starting_interchange_control_number=123,
                                    starting_transaction_set_control_number=123
                                ),
                                delimiters=b2bi_mixins.CfnPartnershipPropsMixin.X12DelimitersProperty(
                                    component_separator="componentSeparator",
                                    data_element_separator="dataElementSeparator",
                                    segment_terminator="segmentTerminator"
                                ),
                                functional_group_headers=b2bi_mixins.CfnPartnershipPropsMixin.X12FunctionalGroupHeadersProperty(
                                    application_receiver_code="applicationReceiverCode",
                                    application_sender_code="applicationSenderCode",
                                    responsible_agency_code="responsibleAgencyCode"
                                ),
                                gs05_time_format="gs05TimeFormat",
                                interchange_control_headers=b2bi_mixins.CfnPartnershipPropsMixin.X12InterchangeControlHeadersProperty(
                                    acknowledgment_requested_code="acknowledgmentRequestedCode",
                                    receiver_id="receiverId",
                                    receiver_id_qualifier="receiverIdQualifier",
                                    repetition_separator="repetitionSeparator",
                                    sender_id="senderId",
                                    sender_id_qualifier="senderIdQualifier",
                                    usage_indicator_code="usageIndicatorCode"
                                ),
                                validate_edi=False
                            ),
                            wrap_options=b2bi_mixins.CfnPartnershipPropsMixin.WrapOptionsProperty(
                                line_length=123,
                                line_terminator="lineTerminator",
                                wrap_by="wrapBy"
                            )
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__847eced0fd08ab251eb1207df8f34934835e51bdb332854a5503d84447749b7e)
                check_type(argname="argument inbound_edi", value=inbound_edi, expected_type=type_hints["inbound_edi"])
                check_type(argname="argument outbound_edi", value=outbound_edi, expected_type=type_hints["outbound_edi"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if inbound_edi is not None:
                self._values["inbound_edi"] = inbound_edi
            if outbound_edi is not None:
                self._values["outbound_edi"] = outbound_edi

        @builtins.property
        def inbound_edi(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPartnershipPropsMixin.InboundEdiOptionsProperty"]]:
            '''A structure that contains the inbound EDI options for the capability.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-partnership-capabilityoptions.html#cfn-b2bi-partnership-capabilityoptions-inboundedi
            '''
            result = self._values.get("inbound_edi")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPartnershipPropsMixin.InboundEdiOptionsProperty"]], result)

        @builtins.property
        def outbound_edi(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPartnershipPropsMixin.OutboundEdiOptionsProperty"]]:
            '''A structure that contains the outbound EDI options.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-partnership-capabilityoptions.html#cfn-b2bi-partnership-capabilityoptions-outboundedi
            '''
            result = self._values.get("outbound_edi")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPartnershipPropsMixin.OutboundEdiOptionsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CapabilityOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_b2bi.mixins.CfnPartnershipPropsMixin.InboundEdiOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"x12": "x12"},
    )
    class InboundEdiOptionsProperty:
        def __init__(
            self,
            *,
            x12: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPartnershipPropsMixin.X12InboundEdiOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains options for processing inbound EDI files.

            These options allow for customizing how incoming EDI documents are processed.

            :param x12: A structure that contains X12-specific options for processing inbound X12 EDI files.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-partnership-inboundedioptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_b2bi import mixins as b2bi_mixins
                
                inbound_edi_options_property = b2bi_mixins.CfnPartnershipPropsMixin.InboundEdiOptionsProperty(
                    x12=b2bi_mixins.CfnPartnershipPropsMixin.X12InboundEdiOptionsProperty(
                        acknowledgment_options=b2bi_mixins.CfnPartnershipPropsMixin.X12AcknowledgmentOptionsProperty(
                            functional_acknowledgment="functionalAcknowledgment",
                            technical_acknowledgment="technicalAcknowledgment"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__af1fa34e48c90f45a20336ef1c9005aa89b55d638abf6ac833307ed7e0857680)
                check_type(argname="argument x12", value=x12, expected_type=type_hints["x12"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if x12 is not None:
                self._values["x12"] = x12

        @builtins.property
        def x12(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPartnershipPropsMixin.X12InboundEdiOptionsProperty"]]:
            '''A structure that contains X12-specific options for processing inbound X12 EDI files.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-partnership-inboundedioptions.html#cfn-b2bi-partnership-inboundedioptions-x12
            '''
            result = self._values.get("x12")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPartnershipPropsMixin.X12InboundEdiOptionsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InboundEdiOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_b2bi.mixins.CfnPartnershipPropsMixin.OutboundEdiOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"x12": "x12"},
    )
    class OutboundEdiOptionsProperty:
        def __init__(
            self,
            *,
            x12: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPartnershipPropsMixin.X12EnvelopeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A container for outbound EDI options.

            :param x12: A structure that contains an X12 envelope structure.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-partnership-outboundedioptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_b2bi import mixins as b2bi_mixins
                
                outbound_edi_options_property = b2bi_mixins.CfnPartnershipPropsMixin.OutboundEdiOptionsProperty(
                    x12=b2bi_mixins.CfnPartnershipPropsMixin.X12EnvelopeProperty(
                        common=b2bi_mixins.CfnPartnershipPropsMixin.X12OutboundEdiHeadersProperty(
                            control_numbers=b2bi_mixins.CfnPartnershipPropsMixin.X12ControlNumbersProperty(
                                starting_functional_group_control_number=123,
                                starting_interchange_control_number=123,
                                starting_transaction_set_control_number=123
                            ),
                            delimiters=b2bi_mixins.CfnPartnershipPropsMixin.X12DelimitersProperty(
                                component_separator="componentSeparator",
                                data_element_separator="dataElementSeparator",
                                segment_terminator="segmentTerminator"
                            ),
                            functional_group_headers=b2bi_mixins.CfnPartnershipPropsMixin.X12FunctionalGroupHeadersProperty(
                                application_receiver_code="applicationReceiverCode",
                                application_sender_code="applicationSenderCode",
                                responsible_agency_code="responsibleAgencyCode"
                            ),
                            gs05_time_format="gs05TimeFormat",
                            interchange_control_headers=b2bi_mixins.CfnPartnershipPropsMixin.X12InterchangeControlHeadersProperty(
                                acknowledgment_requested_code="acknowledgmentRequestedCode",
                                receiver_id="receiverId",
                                receiver_id_qualifier="receiverIdQualifier",
                                repetition_separator="repetitionSeparator",
                                sender_id="senderId",
                                sender_id_qualifier="senderIdQualifier",
                                usage_indicator_code="usageIndicatorCode"
                            ),
                            validate_edi=False
                        ),
                        wrap_options=b2bi_mixins.CfnPartnershipPropsMixin.WrapOptionsProperty(
                            line_length=123,
                            line_terminator="lineTerminator",
                            wrap_by="wrapBy"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__536954209d9dbcfbb5b414169b471990002c5699f25b3b248bbe16abf88a51f1)
                check_type(argname="argument x12", value=x12, expected_type=type_hints["x12"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if x12 is not None:
                self._values["x12"] = x12

        @builtins.property
        def x12(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPartnershipPropsMixin.X12EnvelopeProperty"]]:
            '''A structure that contains an X12 envelope structure.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-partnership-outboundedioptions.html#cfn-b2bi-partnership-outboundedioptions-x12
            '''
            result = self._values.get("x12")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPartnershipPropsMixin.X12EnvelopeProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OutboundEdiOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_b2bi.mixins.CfnPartnershipPropsMixin.WrapOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "line_length": "lineLength",
            "line_terminator": "lineTerminator",
            "wrap_by": "wrapBy",
        },
    )
    class WrapOptionsProperty:
        def __init__(
            self,
            *,
            line_length: typing.Optional[jsii.Number] = None,
            line_terminator: typing.Optional[builtins.str] = None,
            wrap_by: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains options for wrapping (line folding) in X12 EDI files.

            Wrapping controls how long lines are handled in the EDI output.

            :param line_length: Specifies the maximum length of a line before wrapping occurs. This value is used when ``wrapBy`` is set to ``LINE_LENGTH`` .
            :param line_terminator: Specifies the character sequence used to terminate lines when wrapping. Valid values:. - ``CRLF`` : carriage return and line feed - ``LF`` : line feed) - ``CR`` : carriage return
            :param wrap_by: Specifies the method used for wrapping lines in the EDI output. Valid values:. - ``SEGMENT`` : Wraps by segment. - ``ONE_LINE`` : Indicates that the entire content is on a single line. .. epigraph:: When you specify ``ONE_LINE`` , do not provide either the line length nor the line terminator value. - ``LINE_LENGTH`` : Wraps by character count, as specified by ``lineLength`` value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-partnership-wrapoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_b2bi import mixins as b2bi_mixins
                
                wrap_options_property = b2bi_mixins.CfnPartnershipPropsMixin.WrapOptionsProperty(
                    line_length=123,
                    line_terminator="lineTerminator",
                    wrap_by="wrapBy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3ede0729bb401813ab4ca6034dd6d10881ac5d0ad1886fc42824be9f507e6afb)
                check_type(argname="argument line_length", value=line_length, expected_type=type_hints["line_length"])
                check_type(argname="argument line_terminator", value=line_terminator, expected_type=type_hints["line_terminator"])
                check_type(argname="argument wrap_by", value=wrap_by, expected_type=type_hints["wrap_by"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if line_length is not None:
                self._values["line_length"] = line_length
            if line_terminator is not None:
                self._values["line_terminator"] = line_terminator
            if wrap_by is not None:
                self._values["wrap_by"] = wrap_by

        @builtins.property
        def line_length(self) -> typing.Optional[jsii.Number]:
            '''Specifies the maximum length of a line before wrapping occurs.

            This value is used when ``wrapBy`` is set to ``LINE_LENGTH`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-partnership-wrapoptions.html#cfn-b2bi-partnership-wrapoptions-linelength
            '''
            result = self._values.get("line_length")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def line_terminator(self) -> typing.Optional[builtins.str]:
            '''Specifies the character sequence used to terminate lines when wrapping. Valid values:.

            - ``CRLF`` : carriage return and line feed
            - ``LF`` : line feed)
            - ``CR`` : carriage return

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-partnership-wrapoptions.html#cfn-b2bi-partnership-wrapoptions-lineterminator
            '''
            result = self._values.get("line_terminator")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def wrap_by(self) -> typing.Optional[builtins.str]:
            '''Specifies the method used for wrapping lines in the EDI output. Valid values:.

            - ``SEGMENT`` : Wraps by segment.
            - ``ONE_LINE`` : Indicates that the entire content is on a single line.

            .. epigraph::

               When you specify ``ONE_LINE`` , do not provide either the line length nor the line terminator value.

            - ``LINE_LENGTH`` : Wraps by character count, as specified by ``lineLength`` value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-partnership-wrapoptions.html#cfn-b2bi-partnership-wrapoptions-wrapby
            '''
            result = self._values.get("wrap_by")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WrapOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_b2bi.mixins.CfnPartnershipPropsMixin.X12AcknowledgmentOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "functional_acknowledgment": "functionalAcknowledgment",
            "technical_acknowledgment": "technicalAcknowledgment",
        },
    )
    class X12AcknowledgmentOptionsProperty:
        def __init__(
            self,
            *,
            functional_acknowledgment: typing.Optional[builtins.str] = None,
            technical_acknowledgment: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains options for configuring X12 acknowledgments.

            These options control how functional and technical acknowledgments are handled.

            :param functional_acknowledgment: Specifies whether functional acknowledgments (997/999) should be generated for incoming X12 transactions. Valid values are ``DO_NOT_GENERATE`` , ``GENERATE_ALL_SEGMENTS`` and ``GENERATE_WITHOUT_TRANSACTION_SET_RESPONSE_LOOP`` . If you choose ``GENERATE_WITHOUT_TRANSACTION_SET_RESPONSE_LOOP`` , AWS B2B Data Interchange skips the AK2_Loop when generating an acknowledgment document.
            :param technical_acknowledgment: Specifies whether technical acknowledgments (TA1) should be generated for incoming X12 interchanges. Valid values are ``DO_NOT_GENERATE`` and ``GENERATE_ALL_SEGMENTS`` and.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-partnership-x12acknowledgmentoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_b2bi import mixins as b2bi_mixins
                
                x12_acknowledgment_options_property = b2bi_mixins.CfnPartnershipPropsMixin.X12AcknowledgmentOptionsProperty(
                    functional_acknowledgment="functionalAcknowledgment",
                    technical_acknowledgment="technicalAcknowledgment"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__afee50d24b583699fa6670b03b62f2e6f4bed730cb28b3c94aa8abf7c71fce14)
                check_type(argname="argument functional_acknowledgment", value=functional_acknowledgment, expected_type=type_hints["functional_acknowledgment"])
                check_type(argname="argument technical_acknowledgment", value=technical_acknowledgment, expected_type=type_hints["technical_acknowledgment"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if functional_acknowledgment is not None:
                self._values["functional_acknowledgment"] = functional_acknowledgment
            if technical_acknowledgment is not None:
                self._values["technical_acknowledgment"] = technical_acknowledgment

        @builtins.property
        def functional_acknowledgment(self) -> typing.Optional[builtins.str]:
            '''Specifies whether functional acknowledgments (997/999) should be generated for incoming X12 transactions.

            Valid values are ``DO_NOT_GENERATE`` , ``GENERATE_ALL_SEGMENTS`` and ``GENERATE_WITHOUT_TRANSACTION_SET_RESPONSE_LOOP`` .

            If you choose ``GENERATE_WITHOUT_TRANSACTION_SET_RESPONSE_LOOP`` , AWS B2B Data Interchange skips the AK2_Loop when generating an acknowledgment document.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-partnership-x12acknowledgmentoptions.html#cfn-b2bi-partnership-x12acknowledgmentoptions-functionalacknowledgment
            '''
            result = self._values.get("functional_acknowledgment")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def technical_acknowledgment(self) -> typing.Optional[builtins.str]:
            '''Specifies whether technical acknowledgments (TA1) should be generated for incoming X12 interchanges.

            Valid values are ``DO_NOT_GENERATE`` and ``GENERATE_ALL_SEGMENTS`` and.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-partnership-x12acknowledgmentoptions.html#cfn-b2bi-partnership-x12acknowledgmentoptions-technicalacknowledgment
            '''
            result = self._values.get("technical_acknowledgment")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "X12AcknowledgmentOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_b2bi.mixins.CfnPartnershipPropsMixin.X12ControlNumbersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "starting_functional_group_control_number": "startingFunctionalGroupControlNumber",
            "starting_interchange_control_number": "startingInterchangeControlNumber",
            "starting_transaction_set_control_number": "startingTransactionSetControlNumber",
        },
    )
    class X12ControlNumbersProperty:
        def __init__(
            self,
            *,
            starting_functional_group_control_number: typing.Optional[jsii.Number] = None,
            starting_interchange_control_number: typing.Optional[jsii.Number] = None,
            starting_transaction_set_control_number: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Contains configuration for X12 control numbers used in X12 EDI generation.

            Control numbers are used to uniquely identify interchanges, functional groups, and transaction sets.

            :param starting_functional_group_control_number: Specifies the starting functional group control number (GS06) to use for X12 EDI generation. This number is incremented for each new functional group. For the GS (functional group) envelope, AWS B2B Data Interchange generates a functional group control number that is unique to the sender ID, receiver ID, and functional identifier code combination.
            :param starting_interchange_control_number: Specifies the starting interchange control number (ISA13) to use for X12 EDI generation. This number is incremented for each new interchange. For the ISA (interchange) envelope, AWS B2B Data Interchange generates an interchange control number that is unique for the ISA05 and ISA06 (sender) & ISA07 and ISA08 (receiver) combination.
            :param starting_transaction_set_control_number: Specifies the starting transaction set control number (ST02) to use for X12 EDI generation. This number is incremented for each new transaction set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-partnership-x12controlnumbers.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_b2bi import mixins as b2bi_mixins
                
                x12_control_numbers_property = b2bi_mixins.CfnPartnershipPropsMixin.X12ControlNumbersProperty(
                    starting_functional_group_control_number=123,
                    starting_interchange_control_number=123,
                    starting_transaction_set_control_number=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2de771d93ba7c0e797ce0ddcc7fb6eb568f82f6da8fb77c13ea8ef8d958fb2c9)
                check_type(argname="argument starting_functional_group_control_number", value=starting_functional_group_control_number, expected_type=type_hints["starting_functional_group_control_number"])
                check_type(argname="argument starting_interchange_control_number", value=starting_interchange_control_number, expected_type=type_hints["starting_interchange_control_number"])
                check_type(argname="argument starting_transaction_set_control_number", value=starting_transaction_set_control_number, expected_type=type_hints["starting_transaction_set_control_number"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if starting_functional_group_control_number is not None:
                self._values["starting_functional_group_control_number"] = starting_functional_group_control_number
            if starting_interchange_control_number is not None:
                self._values["starting_interchange_control_number"] = starting_interchange_control_number
            if starting_transaction_set_control_number is not None:
                self._values["starting_transaction_set_control_number"] = starting_transaction_set_control_number

        @builtins.property
        def starting_functional_group_control_number(
            self,
        ) -> typing.Optional[jsii.Number]:
            '''Specifies the starting functional group control number (GS06) to use for X12 EDI generation.

            This number is incremented for each new functional group. For the GS (functional group) envelope, AWS B2B Data Interchange generates a functional group control number that is unique to the sender ID, receiver ID, and functional identifier code combination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-partnership-x12controlnumbers.html#cfn-b2bi-partnership-x12controlnumbers-startingfunctionalgroupcontrolnumber
            '''
            result = self._values.get("starting_functional_group_control_number")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def starting_interchange_control_number(self) -> typing.Optional[jsii.Number]:
            '''Specifies the starting interchange control number (ISA13) to use for X12 EDI generation.

            This number is incremented for each new interchange. For the ISA (interchange) envelope, AWS B2B Data Interchange generates an interchange control number that is unique for the ISA05 and ISA06 (sender) & ISA07 and ISA08 (receiver) combination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-partnership-x12controlnumbers.html#cfn-b2bi-partnership-x12controlnumbers-startinginterchangecontrolnumber
            '''
            result = self._values.get("starting_interchange_control_number")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def starting_transaction_set_control_number(
            self,
        ) -> typing.Optional[jsii.Number]:
            '''Specifies the starting transaction set control number (ST02) to use for X12 EDI generation.

            This number is incremented for each new transaction set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-partnership-x12controlnumbers.html#cfn-b2bi-partnership-x12controlnumbers-startingtransactionsetcontrolnumber
            '''
            result = self._values.get("starting_transaction_set_control_number")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "X12ControlNumbersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_b2bi.mixins.CfnPartnershipPropsMixin.X12DelimitersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "component_separator": "componentSeparator",
            "data_element_separator": "dataElementSeparator",
            "segment_terminator": "segmentTerminator",
        },
    )
    class X12DelimitersProperty:
        def __init__(
            self,
            *,
            component_separator: typing.Optional[builtins.str] = None,
            data_element_separator: typing.Optional[builtins.str] = None,
            segment_terminator: typing.Optional[builtins.str] = None,
        ) -> None:
            '''In X12 EDI messages, delimiters are used to mark the end of segments or elements, and are defined in the interchange control header.

            The delimiters are part of the message's syntax and divide up its different elements.

            :param component_separator: The component, or sub-element, separator. The default value is ``:`` (colon).
            :param data_element_separator: The data element separator. The default value is ``*`` (asterisk).
            :param segment_terminator: The segment terminator. The default value is ``~`` (tilde).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-partnership-x12delimiters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_b2bi import mixins as b2bi_mixins
                
                x12_delimiters_property = b2bi_mixins.CfnPartnershipPropsMixin.X12DelimitersProperty(
                    component_separator="componentSeparator",
                    data_element_separator="dataElementSeparator",
                    segment_terminator="segmentTerminator"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__da5b863b333408043ebf55c3775e6043b5a9a03247445a8f6f7d129ddb04d180)
                check_type(argname="argument component_separator", value=component_separator, expected_type=type_hints["component_separator"])
                check_type(argname="argument data_element_separator", value=data_element_separator, expected_type=type_hints["data_element_separator"])
                check_type(argname="argument segment_terminator", value=segment_terminator, expected_type=type_hints["segment_terminator"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if component_separator is not None:
                self._values["component_separator"] = component_separator
            if data_element_separator is not None:
                self._values["data_element_separator"] = data_element_separator
            if segment_terminator is not None:
                self._values["segment_terminator"] = segment_terminator

        @builtins.property
        def component_separator(self) -> typing.Optional[builtins.str]:
            '''The component, or sub-element, separator.

            The default value is ``:`` (colon).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-partnership-x12delimiters.html#cfn-b2bi-partnership-x12delimiters-componentseparator
            '''
            result = self._values.get("component_separator")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def data_element_separator(self) -> typing.Optional[builtins.str]:
            '''The data element separator.

            The default value is ``*`` (asterisk).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-partnership-x12delimiters.html#cfn-b2bi-partnership-x12delimiters-dataelementseparator
            '''
            result = self._values.get("data_element_separator")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def segment_terminator(self) -> typing.Optional[builtins.str]:
            '''The segment terminator.

            The default value is ``~`` (tilde).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-partnership-x12delimiters.html#cfn-b2bi-partnership-x12delimiters-segmentterminator
            '''
            result = self._values.get("segment_terminator")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "X12DelimitersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_b2bi.mixins.CfnPartnershipPropsMixin.X12EnvelopeProperty",
        jsii_struct_bases=[],
        name_mapping={"common": "common", "wrap_options": "wrapOptions"},
    )
    class X12EnvelopeProperty:
        def __init__(
            self,
            *,
            common: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPartnershipPropsMixin.X12OutboundEdiHeadersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            wrap_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPartnershipPropsMixin.WrapOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A wrapper structure for an X12 definition object.

            the X12 envelope ensures the integrity of the data and the efficiency of the information exchange. The X12 message structure has hierarchical levels. From highest to the lowest, they are:

            - Interchange Envelope
            - Functional Group
            - Transaction Set

            :param common: A container for the X12 outbound EDI headers.
            :param wrap_options: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-partnership-x12envelope.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_b2bi import mixins as b2bi_mixins
                
                x12_envelope_property = b2bi_mixins.CfnPartnershipPropsMixin.X12EnvelopeProperty(
                    common=b2bi_mixins.CfnPartnershipPropsMixin.X12OutboundEdiHeadersProperty(
                        control_numbers=b2bi_mixins.CfnPartnershipPropsMixin.X12ControlNumbersProperty(
                            starting_functional_group_control_number=123,
                            starting_interchange_control_number=123,
                            starting_transaction_set_control_number=123
                        ),
                        delimiters=b2bi_mixins.CfnPartnershipPropsMixin.X12DelimitersProperty(
                            component_separator="componentSeparator",
                            data_element_separator="dataElementSeparator",
                            segment_terminator="segmentTerminator"
                        ),
                        functional_group_headers=b2bi_mixins.CfnPartnershipPropsMixin.X12FunctionalGroupHeadersProperty(
                            application_receiver_code="applicationReceiverCode",
                            application_sender_code="applicationSenderCode",
                            responsible_agency_code="responsibleAgencyCode"
                        ),
                        gs05_time_format="gs05TimeFormat",
                        interchange_control_headers=b2bi_mixins.CfnPartnershipPropsMixin.X12InterchangeControlHeadersProperty(
                            acknowledgment_requested_code="acknowledgmentRequestedCode",
                            receiver_id="receiverId",
                            receiver_id_qualifier="receiverIdQualifier",
                            repetition_separator="repetitionSeparator",
                            sender_id="senderId",
                            sender_id_qualifier="senderIdQualifier",
                            usage_indicator_code="usageIndicatorCode"
                        ),
                        validate_edi=False
                    ),
                    wrap_options=b2bi_mixins.CfnPartnershipPropsMixin.WrapOptionsProperty(
                        line_length=123,
                        line_terminator="lineTerminator",
                        wrap_by="wrapBy"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__eeda8ef09642ee25c3440486b236b3c952fa37522bb7d25a7053159d7cef247b)
                check_type(argname="argument common", value=common, expected_type=type_hints["common"])
                check_type(argname="argument wrap_options", value=wrap_options, expected_type=type_hints["wrap_options"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if common is not None:
                self._values["common"] = common
            if wrap_options is not None:
                self._values["wrap_options"] = wrap_options

        @builtins.property
        def common(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPartnershipPropsMixin.X12OutboundEdiHeadersProperty"]]:
            '''A container for the X12 outbound EDI headers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-partnership-x12envelope.html#cfn-b2bi-partnership-x12envelope-common
            '''
            result = self._values.get("common")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPartnershipPropsMixin.X12OutboundEdiHeadersProperty"]], result)

        @builtins.property
        def wrap_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPartnershipPropsMixin.WrapOptionsProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-partnership-x12envelope.html#cfn-b2bi-partnership-x12envelope-wrapoptions
            '''
            result = self._values.get("wrap_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPartnershipPropsMixin.WrapOptionsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "X12EnvelopeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_b2bi.mixins.CfnPartnershipPropsMixin.X12FunctionalGroupHeadersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "application_receiver_code": "applicationReceiverCode",
            "application_sender_code": "applicationSenderCode",
            "responsible_agency_code": "responsibleAgencyCode",
        },
    )
    class X12FunctionalGroupHeadersProperty:
        def __init__(
            self,
            *,
            application_receiver_code: typing.Optional[builtins.str] = None,
            application_sender_code: typing.Optional[builtins.str] = None,
            responsible_agency_code: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Part of the X12 message structure.

            These are the functional group headers for the X12 EDI object.

            :param application_receiver_code: A value representing the code used to identify the party receiving a message, at position GS-03.
            :param application_sender_code: A value representing the code used to identify the party transmitting a message, at position GS-02.
            :param responsible_agency_code: A code that identifies the issuer of the standard, at position GS-07.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-partnership-x12functionalgroupheaders.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_b2bi import mixins as b2bi_mixins
                
                x12_functional_group_headers_property = b2bi_mixins.CfnPartnershipPropsMixin.X12FunctionalGroupHeadersProperty(
                    application_receiver_code="applicationReceiverCode",
                    application_sender_code="applicationSenderCode",
                    responsible_agency_code="responsibleAgencyCode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2f338bf82501a0b33b728a496c5cdf09cead195a794ca5ec693c7376e70bfe69)
                check_type(argname="argument application_receiver_code", value=application_receiver_code, expected_type=type_hints["application_receiver_code"])
                check_type(argname="argument application_sender_code", value=application_sender_code, expected_type=type_hints["application_sender_code"])
                check_type(argname="argument responsible_agency_code", value=responsible_agency_code, expected_type=type_hints["responsible_agency_code"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if application_receiver_code is not None:
                self._values["application_receiver_code"] = application_receiver_code
            if application_sender_code is not None:
                self._values["application_sender_code"] = application_sender_code
            if responsible_agency_code is not None:
                self._values["responsible_agency_code"] = responsible_agency_code

        @builtins.property
        def application_receiver_code(self) -> typing.Optional[builtins.str]:
            '''A value representing the code used to identify the party receiving a message, at position GS-03.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-partnership-x12functionalgroupheaders.html#cfn-b2bi-partnership-x12functionalgroupheaders-applicationreceivercode
            '''
            result = self._values.get("application_receiver_code")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def application_sender_code(self) -> typing.Optional[builtins.str]:
            '''A value representing the code used to identify the party transmitting a message, at position GS-02.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-partnership-x12functionalgroupheaders.html#cfn-b2bi-partnership-x12functionalgroupheaders-applicationsendercode
            '''
            result = self._values.get("application_sender_code")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def responsible_agency_code(self) -> typing.Optional[builtins.str]:
            '''A code that identifies the issuer of the standard, at position GS-07.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-partnership-x12functionalgroupheaders.html#cfn-b2bi-partnership-x12functionalgroupheaders-responsibleagencycode
            '''
            result = self._values.get("responsible_agency_code")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "X12FunctionalGroupHeadersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_b2bi.mixins.CfnPartnershipPropsMixin.X12InboundEdiOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"acknowledgment_options": "acknowledgmentOptions"},
    )
    class X12InboundEdiOptionsProperty:
        def __init__(
            self,
            *,
            acknowledgment_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPartnershipPropsMixin.X12AcknowledgmentOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains options specific to processing inbound X12 EDI files.

            :param acknowledgment_options: Specifies acknowledgment options for inbound X12 EDI files. These options control how functional and technical acknowledgments are handled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-partnership-x12inboundedioptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_b2bi import mixins as b2bi_mixins
                
                x12_inbound_edi_options_property = b2bi_mixins.CfnPartnershipPropsMixin.X12InboundEdiOptionsProperty(
                    acknowledgment_options=b2bi_mixins.CfnPartnershipPropsMixin.X12AcknowledgmentOptionsProperty(
                        functional_acknowledgment="functionalAcknowledgment",
                        technical_acknowledgment="technicalAcknowledgment"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__26ed6672cf4c94b27965ca050d73a7eaa48433741051e73d2cd971bd671494e5)
                check_type(argname="argument acknowledgment_options", value=acknowledgment_options, expected_type=type_hints["acknowledgment_options"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if acknowledgment_options is not None:
                self._values["acknowledgment_options"] = acknowledgment_options

        @builtins.property
        def acknowledgment_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPartnershipPropsMixin.X12AcknowledgmentOptionsProperty"]]:
            '''Specifies acknowledgment options for inbound X12 EDI files.

            These options control how functional and technical acknowledgments are handled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-partnership-x12inboundedioptions.html#cfn-b2bi-partnership-x12inboundedioptions-acknowledgmentoptions
            '''
            result = self._values.get("acknowledgment_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPartnershipPropsMixin.X12AcknowledgmentOptionsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "X12InboundEdiOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_b2bi.mixins.CfnPartnershipPropsMixin.X12InterchangeControlHeadersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "acknowledgment_requested_code": "acknowledgmentRequestedCode",
            "receiver_id": "receiverId",
            "receiver_id_qualifier": "receiverIdQualifier",
            "repetition_separator": "repetitionSeparator",
            "sender_id": "senderId",
            "sender_id_qualifier": "senderIdQualifier",
            "usage_indicator_code": "usageIndicatorCode",
        },
    )
    class X12InterchangeControlHeadersProperty:
        def __init__(
            self,
            *,
            acknowledgment_requested_code: typing.Optional[builtins.str] = None,
            receiver_id: typing.Optional[builtins.str] = None,
            receiver_id_qualifier: typing.Optional[builtins.str] = None,
            repetition_separator: typing.Optional[builtins.str] = None,
            sender_id: typing.Optional[builtins.str] = None,
            sender_id_qualifier: typing.Optional[builtins.str] = None,
            usage_indicator_code: typing.Optional[builtins.str] = None,
        ) -> None:
            '''In X12, the Interchange Control Header is the first segment of an EDI document and is part of the Interchange Envelope.

            It contains information about the sender and receiver, the date and time of transmission, and the X12 version being used. It also includes delivery information, such as the sender and receiver IDs.

            :param acknowledgment_requested_code: Located at position ISA-14 in the header. The value "1" indicates that the sender is requesting an interchange acknowledgment at receipt of the interchange. The value "0" is used otherwise.
            :param receiver_id: Located at position ISA-08 in the header. This value (along with the ``receiverIdQualifier`` ) identifies the intended recipient of the interchange.
            :param receiver_id_qualifier: Located at position ISA-07 in the header. Qualifier for the receiver ID. Together, the ID and qualifier uniquely identify the receiving trading partner.
            :param repetition_separator: Located at position ISA-11 in the header. This string makes it easier when you need to group similar adjacent element values together without using extra segments. .. epigraph:: This parameter is only honored for version greater than 401 ( ``VERSION_4010`` and higher). For versions less than 401, this field is called `StandardsId <https://docs.aws.amazon.com/https://www.stedi.com/edi/x12-004010/segment/ISA#ISA-11>`_ , in which case our service sets the value to ``U`` .
            :param sender_id: Located at position ISA-06 in the header. This value (along with the ``senderIdQualifier`` ) identifies the sender of the interchange.
            :param sender_id_qualifier: Located at position ISA-05 in the header. Qualifier for the sender ID. Together, the ID and qualifier uniquely identify the sending trading partner.
            :param usage_indicator_code: Located at position ISA-15 in the header. Specifies how this interchange is being used:. - ``T`` indicates this interchange is for testing. - ``P`` indicates this interchange is for production. - ``I`` indicates this interchange is informational.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-partnership-x12interchangecontrolheaders.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_b2bi import mixins as b2bi_mixins
                
                x12_interchange_control_headers_property = b2bi_mixins.CfnPartnershipPropsMixin.X12InterchangeControlHeadersProperty(
                    acknowledgment_requested_code="acknowledgmentRequestedCode",
                    receiver_id="receiverId",
                    receiver_id_qualifier="receiverIdQualifier",
                    repetition_separator="repetitionSeparator",
                    sender_id="senderId",
                    sender_id_qualifier="senderIdQualifier",
                    usage_indicator_code="usageIndicatorCode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__53f97ab1cdeae73a40eb360c14ed44bc065e61e43c3fbbc8473548853343f752)
                check_type(argname="argument acknowledgment_requested_code", value=acknowledgment_requested_code, expected_type=type_hints["acknowledgment_requested_code"])
                check_type(argname="argument receiver_id", value=receiver_id, expected_type=type_hints["receiver_id"])
                check_type(argname="argument receiver_id_qualifier", value=receiver_id_qualifier, expected_type=type_hints["receiver_id_qualifier"])
                check_type(argname="argument repetition_separator", value=repetition_separator, expected_type=type_hints["repetition_separator"])
                check_type(argname="argument sender_id", value=sender_id, expected_type=type_hints["sender_id"])
                check_type(argname="argument sender_id_qualifier", value=sender_id_qualifier, expected_type=type_hints["sender_id_qualifier"])
                check_type(argname="argument usage_indicator_code", value=usage_indicator_code, expected_type=type_hints["usage_indicator_code"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if acknowledgment_requested_code is not None:
                self._values["acknowledgment_requested_code"] = acknowledgment_requested_code
            if receiver_id is not None:
                self._values["receiver_id"] = receiver_id
            if receiver_id_qualifier is not None:
                self._values["receiver_id_qualifier"] = receiver_id_qualifier
            if repetition_separator is not None:
                self._values["repetition_separator"] = repetition_separator
            if sender_id is not None:
                self._values["sender_id"] = sender_id
            if sender_id_qualifier is not None:
                self._values["sender_id_qualifier"] = sender_id_qualifier
            if usage_indicator_code is not None:
                self._values["usage_indicator_code"] = usage_indicator_code

        @builtins.property
        def acknowledgment_requested_code(self) -> typing.Optional[builtins.str]:
            '''Located at position ISA-14 in the header.

            The value "1" indicates that the sender is requesting an interchange acknowledgment at receipt of the interchange. The value "0" is used otherwise.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-partnership-x12interchangecontrolheaders.html#cfn-b2bi-partnership-x12interchangecontrolheaders-acknowledgmentrequestedcode
            '''
            result = self._values.get("acknowledgment_requested_code")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def receiver_id(self) -> typing.Optional[builtins.str]:
            '''Located at position ISA-08 in the header.

            This value (along with the ``receiverIdQualifier`` ) identifies the intended recipient of the interchange.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-partnership-x12interchangecontrolheaders.html#cfn-b2bi-partnership-x12interchangecontrolheaders-receiverid
            '''
            result = self._values.get("receiver_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def receiver_id_qualifier(self) -> typing.Optional[builtins.str]:
            '''Located at position ISA-07 in the header.

            Qualifier for the receiver ID. Together, the ID and qualifier uniquely identify the receiving trading partner.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-partnership-x12interchangecontrolheaders.html#cfn-b2bi-partnership-x12interchangecontrolheaders-receiveridqualifier
            '''
            result = self._values.get("receiver_id_qualifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def repetition_separator(self) -> typing.Optional[builtins.str]:
            '''Located at position ISA-11 in the header.

            This string makes it easier when you need to group similar adjacent element values together without using extra segments.
            .. epigraph::

               This parameter is only honored for version greater than 401 ( ``VERSION_4010`` and higher).

               For versions less than 401, this field is called `StandardsId <https://docs.aws.amazon.com/https://www.stedi.com/edi/x12-004010/segment/ISA#ISA-11>`_ , in which case our service sets the value to ``U`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-partnership-x12interchangecontrolheaders.html#cfn-b2bi-partnership-x12interchangecontrolheaders-repetitionseparator
            '''
            result = self._values.get("repetition_separator")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sender_id(self) -> typing.Optional[builtins.str]:
            '''Located at position ISA-06 in the header.

            This value (along with the ``senderIdQualifier`` ) identifies the sender of the interchange.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-partnership-x12interchangecontrolheaders.html#cfn-b2bi-partnership-x12interchangecontrolheaders-senderid
            '''
            result = self._values.get("sender_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sender_id_qualifier(self) -> typing.Optional[builtins.str]:
            '''Located at position ISA-05 in the header.

            Qualifier for the sender ID. Together, the ID and qualifier uniquely identify the sending trading partner.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-partnership-x12interchangecontrolheaders.html#cfn-b2bi-partnership-x12interchangecontrolheaders-senderidqualifier
            '''
            result = self._values.get("sender_id_qualifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def usage_indicator_code(self) -> typing.Optional[builtins.str]:
            '''Located at position ISA-15 in the header. Specifies how this interchange is being used:.

            - ``T`` indicates this interchange is for testing.
            - ``P`` indicates this interchange is for production.
            - ``I`` indicates this interchange is informational.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-partnership-x12interchangecontrolheaders.html#cfn-b2bi-partnership-x12interchangecontrolheaders-usageindicatorcode
            '''
            result = self._values.get("usage_indicator_code")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "X12InterchangeControlHeadersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_b2bi.mixins.CfnPartnershipPropsMixin.X12OutboundEdiHeadersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "control_numbers": "controlNumbers",
            "delimiters": "delimiters",
            "functional_group_headers": "functionalGroupHeaders",
            "gs05_time_format": "gs05TimeFormat",
            "interchange_control_headers": "interchangeControlHeaders",
            "validate_edi": "validateEdi",
        },
    )
    class X12OutboundEdiHeadersProperty:
        def __init__(
            self,
            *,
            control_numbers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPartnershipPropsMixin.X12ControlNumbersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            delimiters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPartnershipPropsMixin.X12DelimitersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            functional_group_headers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPartnershipPropsMixin.X12FunctionalGroupHeadersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            gs05_time_format: typing.Optional[builtins.str] = None,
            interchange_control_headers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPartnershipPropsMixin.X12InterchangeControlHeadersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            validate_edi: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''A structure containing the details for an outbound EDI object.

            :param control_numbers: Specifies control number configuration for outbound X12 EDI headers. These settings determine the starting values for interchange, functional group, and transaction set control numbers.
            :param delimiters: The delimiters, for example semicolon ( ``;`` ), that separates sections of the headers for the X12 object.
            :param functional_group_headers: The functional group headers for the X12 object.
            :param gs05_time_format: Specifies the time format in the GS05 element (time) of the functional group header. The following formats use 24-hour clock time: - ``HHMM`` - Hours and minutes - ``HHMMSS`` - Hours, minutes, and seconds - ``HHMMSSDD`` - Hours, minutes, seconds, and decimal seconds Where: - ``HH`` - Hours (00-23) - ``MM`` - Minutes (00-59) - ``SS`` - Seconds (00-59) - ``DD`` - Hundredths of seconds (00-99)
            :param interchange_control_headers: In X12 EDI messages, delimiters are used to mark the end of segments or elements, and are defined in the interchange control header.
            :param validate_edi: Specifies whether or not to validate the EDI for this X12 object: ``TRUE`` or ``FALSE`` . When enabled, this performs both standard EDI validation and applies any configured custom validation rules including element length constraints, code list validations, and element requirement checks. Validation results are returned in the response validation messages.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-partnership-x12outboundediheaders.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_b2bi import mixins as b2bi_mixins
                
                x12_outbound_edi_headers_property = b2bi_mixins.CfnPartnershipPropsMixin.X12OutboundEdiHeadersProperty(
                    control_numbers=b2bi_mixins.CfnPartnershipPropsMixin.X12ControlNumbersProperty(
                        starting_functional_group_control_number=123,
                        starting_interchange_control_number=123,
                        starting_transaction_set_control_number=123
                    ),
                    delimiters=b2bi_mixins.CfnPartnershipPropsMixin.X12DelimitersProperty(
                        component_separator="componentSeparator",
                        data_element_separator="dataElementSeparator",
                        segment_terminator="segmentTerminator"
                    ),
                    functional_group_headers=b2bi_mixins.CfnPartnershipPropsMixin.X12FunctionalGroupHeadersProperty(
                        application_receiver_code="applicationReceiverCode",
                        application_sender_code="applicationSenderCode",
                        responsible_agency_code="responsibleAgencyCode"
                    ),
                    gs05_time_format="gs05TimeFormat",
                    interchange_control_headers=b2bi_mixins.CfnPartnershipPropsMixin.X12InterchangeControlHeadersProperty(
                        acknowledgment_requested_code="acknowledgmentRequestedCode",
                        receiver_id="receiverId",
                        receiver_id_qualifier="receiverIdQualifier",
                        repetition_separator="repetitionSeparator",
                        sender_id="senderId",
                        sender_id_qualifier="senderIdQualifier",
                        usage_indicator_code="usageIndicatorCode"
                    ),
                    validate_edi=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a1733a0a6210b67ad85c7912db4328b4d8fdbc1a4ad0ea2de97917067bc48741)
                check_type(argname="argument control_numbers", value=control_numbers, expected_type=type_hints["control_numbers"])
                check_type(argname="argument delimiters", value=delimiters, expected_type=type_hints["delimiters"])
                check_type(argname="argument functional_group_headers", value=functional_group_headers, expected_type=type_hints["functional_group_headers"])
                check_type(argname="argument gs05_time_format", value=gs05_time_format, expected_type=type_hints["gs05_time_format"])
                check_type(argname="argument interchange_control_headers", value=interchange_control_headers, expected_type=type_hints["interchange_control_headers"])
                check_type(argname="argument validate_edi", value=validate_edi, expected_type=type_hints["validate_edi"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if control_numbers is not None:
                self._values["control_numbers"] = control_numbers
            if delimiters is not None:
                self._values["delimiters"] = delimiters
            if functional_group_headers is not None:
                self._values["functional_group_headers"] = functional_group_headers
            if gs05_time_format is not None:
                self._values["gs05_time_format"] = gs05_time_format
            if interchange_control_headers is not None:
                self._values["interchange_control_headers"] = interchange_control_headers
            if validate_edi is not None:
                self._values["validate_edi"] = validate_edi

        @builtins.property
        def control_numbers(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPartnershipPropsMixin.X12ControlNumbersProperty"]]:
            '''Specifies control number configuration for outbound X12 EDI headers.

            These settings determine the starting values for interchange, functional group, and transaction set control numbers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-partnership-x12outboundediheaders.html#cfn-b2bi-partnership-x12outboundediheaders-controlnumbers
            '''
            result = self._values.get("control_numbers")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPartnershipPropsMixin.X12ControlNumbersProperty"]], result)

        @builtins.property
        def delimiters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPartnershipPropsMixin.X12DelimitersProperty"]]:
            '''The delimiters, for example semicolon ( ``;`` ), that separates sections of the headers for the X12 object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-partnership-x12outboundediheaders.html#cfn-b2bi-partnership-x12outboundediheaders-delimiters
            '''
            result = self._values.get("delimiters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPartnershipPropsMixin.X12DelimitersProperty"]], result)

        @builtins.property
        def functional_group_headers(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPartnershipPropsMixin.X12FunctionalGroupHeadersProperty"]]:
            '''The functional group headers for the X12 object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-partnership-x12outboundediheaders.html#cfn-b2bi-partnership-x12outboundediheaders-functionalgroupheaders
            '''
            result = self._values.get("functional_group_headers")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPartnershipPropsMixin.X12FunctionalGroupHeadersProperty"]], result)

        @builtins.property
        def gs05_time_format(self) -> typing.Optional[builtins.str]:
            '''Specifies the time format in the GS05 element (time) of the functional group header.

            The following formats use 24-hour clock time:

            - ``HHMM`` - Hours and minutes
            - ``HHMMSS`` - Hours, minutes, and seconds
            - ``HHMMSSDD`` - Hours, minutes, seconds, and decimal seconds

            Where:

            - ``HH`` - Hours (00-23)
            - ``MM`` - Minutes (00-59)
            - ``SS`` - Seconds (00-59)
            - ``DD`` - Hundredths of seconds (00-99)

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-partnership-x12outboundediheaders.html#cfn-b2bi-partnership-x12outboundediheaders-gs05timeformat
            '''
            result = self._values.get("gs05_time_format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def interchange_control_headers(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPartnershipPropsMixin.X12InterchangeControlHeadersProperty"]]:
            '''In X12 EDI messages, delimiters are used to mark the end of segments or elements, and are defined in the interchange control header.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-partnership-x12outboundediheaders.html#cfn-b2bi-partnership-x12outboundediheaders-interchangecontrolheaders
            '''
            result = self._values.get("interchange_control_headers")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPartnershipPropsMixin.X12InterchangeControlHeadersProperty"]], result)

        @builtins.property
        def validate_edi(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether or not to validate the EDI for this X12 object: ``TRUE`` or ``FALSE`` .

            When enabled, this performs both standard EDI validation and applies any configured custom validation rules including element length constraints, code list validations, and element requirement checks. Validation results are returned in the response validation messages.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-partnership-x12outboundediheaders.html#cfn-b2bi-partnership-x12outboundediheaders-validateedi
            '''
            result = self._values.get("validate_edi")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "X12OutboundEdiHeadersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_b2bi.mixins.CfnProfileMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "business_name": "businessName",
        "email": "email",
        "logging": "logging",
        "name": "name",
        "phone": "phone",
        "tags": "tags",
    },
)
class CfnProfileMixinProps:
    def __init__(
        self,
        *,
        business_name: typing.Optional[builtins.str] = None,
        email: typing.Optional[builtins.str] = None,
        logging: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        phone: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnProfilePropsMixin.

        :param business_name: Returns the name for the business associated with this profile.
        :param email: 
        :param logging: Specifies whether or not logging is enabled for this profile.
        :param name: Returns the display name for profile.
        :param phone: Specifies the phone number associated with the profile.
        :param tags: A key-value pair for a specific profile. Tags are metadata that you can use to search for and group capabilities for various purposes.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-b2bi-profile.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_b2bi import mixins as b2bi_mixins
            
            cfn_profile_mixin_props = b2bi_mixins.CfnProfileMixinProps(
                business_name="businessName",
                email="email",
                logging="logging",
                name="name",
                phone="phone",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2edd4778b6933db650b826d90509e3181a65fb5a08f9ccd8e4d9ac0f5d334109)
            check_type(argname="argument business_name", value=business_name, expected_type=type_hints["business_name"])
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument phone", value=phone, expected_type=type_hints["phone"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if business_name is not None:
            self._values["business_name"] = business_name
        if email is not None:
            self._values["email"] = email
        if logging is not None:
            self._values["logging"] = logging
        if name is not None:
            self._values["name"] = name
        if phone is not None:
            self._values["phone"] = phone
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def business_name(self) -> typing.Optional[builtins.str]:
        '''Returns the name for the business associated with this profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-b2bi-profile.html#cfn-b2bi-profile-businessname
        '''
        result = self._values.get("business_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def email(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-b2bi-profile.html#cfn-b2bi-profile-email
        '''
        result = self._values.get("email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging(self) -> typing.Optional[builtins.str]:
        '''Specifies whether or not logging is enabled for this profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-b2bi-profile.html#cfn-b2bi-profile-logging
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Returns the display name for profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-b2bi-profile.html#cfn-b2bi-profile-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def phone(self) -> typing.Optional[builtins.str]:
        '''Specifies the phone number associated with the profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-b2bi-profile.html#cfn-b2bi-profile-phone
        '''
        result = self._values.get("phone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A key-value pair for a specific profile.

        Tags are metadata that you can use to search for and group capabilities for various purposes.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-b2bi-profile.html#cfn-b2bi-profile-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnProfileMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnProfilePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_b2bi.mixins.CfnProfilePropsMixin",
):
    '''Creates a customer profile.

    You can have up to five customer profiles, each representing a distinct private network. A profile is the mechanism used to create the concept of a private network.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-b2bi-profile.html
    :cloudformationResource: AWS::B2BI::Profile
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_b2bi import mixins as b2bi_mixins
        
        cfn_profile_props_mixin = b2bi_mixins.CfnProfilePropsMixin(b2bi_mixins.CfnProfileMixinProps(
            business_name="businessName",
            email="email",
            logging="logging",
            name="name",
            phone="phone",
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
        props: typing.Union[CfnProfileMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::B2BI::Profile``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c08f57e36c1042b4df06075b9da2473ed3989c12029055370b342d8afd23ece5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1cf9c8541dfa3e81dd20f252afb3abc4fe3799389e04f59f71f46fca3a3a5b2e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3928225f970ef0f08144d846cdd063de1b0cee49b75c8ed2470db96c4e988b31)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnProfileMixinProps:
        return typing.cast(CfnProfileMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


class CfnTransformerB2biExecutionLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_b2bi.mixins.CfnTransformerB2biExecutionLogs",
):
    '''Builder for CfnTransformerLogsMixin to generate B2BI_EXECUTION_LOGS for CfnTransformer.

    :cloudformationResource: AWS::B2BI::Transformer
    :logType: B2BI_EXECUTION_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_b2bi import mixins as b2bi_mixins
        
        cfn_transformer_b2bi_execution_logs = b2bi_mixins.CfnTransformerB2biExecutionLogs()
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toFirehose")
    def to_firehose(
        self,
        delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
    ) -> "CfnTransformerLogsMixin":
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16408e4028bc631211cd0bccd9bf8215bc9815c503f3c25f7d34d1c7c79caab6)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast("CfnTransformerLogsMixin", jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> "CfnTransformerLogsMixin":
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92a63bb5b5864afd941042e5700224ec7f642532427283446d3d5d4a79b6b9be)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast("CfnTransformerLogsMixin", jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> "CfnTransformerLogsMixin":
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03e8b9e23c076b760ad21e3ae66aec97e2ec7e299c9371649d11151522c73da6)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast("CfnTransformerLogsMixin", jsii.invoke(self, "toS3", [bucket]))


@jsii.implements(_IMixin_11e4b965)
class CfnTransformerLogsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_b2bi.mixins.CfnTransformerLogsMixin",
):
    '''Creates a transformer. AWS B2B Data Interchange currently supports two scenarios:.

    - *Inbound EDI* : the AWS customer receives an EDI file from their trading partner. AWS B2B Data Interchange converts this EDI file into a JSON or XML file with a service-defined structure. A mapping template provided by the customer, in JSONata or XSLT format, is optionally applied to this file to produce a JSON or XML file with the structure the customer requires.
    - *Outbound EDI* : the AWS customer has a JSON or XML file containing data that they wish to use in an EDI file. A mapping template, provided by the customer (in either JSONata or XSLT format) is applied to this file to generate a JSON or XML file in the service-defined structure. This file is then converted to an EDI file.

    .. epigraph::

       The following fields are provided for backwards compatibility only: ``fileFormat`` , ``mappingTemplate`` , ``ediType`` , and ``sampleDocument`` .

       - Use the ``mapping`` data type in place of ``mappingTemplate`` and ``fileFormat``
       - Use the ``sampleDocuments`` data type in place of ``sampleDocument``
       - Use either the ``inputConversion`` or ``outputConversion`` in place of ``ediType``

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-b2bi-transformer.html
    :cloudformationResource: AWS::B2BI::Transformer
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import aws_logs as logs
        from aws_cdk.mixins_preview.aws_b2bi import mixins as b2bi_mixins
        
        # logs_delivery: logs.ILogsDelivery
        
        cfn_transformer_logs_mixin = b2bi_mixins.CfnTransformerLogsMixin("logType", logs_delivery)
    '''

    def __init__(
        self,
        log_type: builtins.str,
        log_delivery: _ILogsDelivery_0d3c9e29,
    ) -> None:
        '''Create a mixin to enable vended logs for ``AWS::B2BI::Transformer``.

        :param log_type: Type of logs that are getting vended.
        :param log_delivery: Object in charge of setting up the delivery destination and delivery connection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49e1205091e695f161a3b12f1acea77e61be1376c4a0bc172c3380485a9e122c)
            check_type(argname="argument log_type", value=log_type, expected_type=type_hints["log_type"])
            check_type(argname="argument log_delivery", value=log_delivery, expected_type=type_hints["log_delivery"])
        jsii.create(self.__class__, self, [log_type, log_delivery])

    @jsii.member(jsii_name="applyTo")
    def apply_to(
        self,
        resource: _constructs_77d1e7e8.IConstruct,
    ) -> _constructs_77d1e7e8.IConstruct:
        '''Apply vended logs configuration to the construct.

        :param resource: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dca4d57bb764d1e55be99a7cf3ba898fcbe2f684eb44945e17e27ebc384d7018)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [resource]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct (has vendedLogs property).

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6608ce7fc657ee3fd2a3e7bac5f1867eebf1fb635b5a1880a8cb920a6a4b0f5)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="B2BI_EXECUTION_LOGS")
    def B2_BI_EXECUTION_LOGS(cls) -> CfnTransformerB2biExecutionLogs:
        return typing.cast(CfnTransformerB2biExecutionLogs, jsii.sget(cls, "B2BI_EXECUTION_LOGS"))

    @builtins.property
    @jsii.member(jsii_name="logDelivery")
    def _log_delivery(self) -> _ILogsDelivery_0d3c9e29:
        return typing.cast(_ILogsDelivery_0d3c9e29, jsii.get(self, "logDelivery"))

    @builtins.property
    @jsii.member(jsii_name="logType")
    def _log_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logType"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_b2bi.mixins.CfnTransformerMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "edi_type": "ediType",
        "file_format": "fileFormat",
        "input_conversion": "inputConversion",
        "mapping": "mapping",
        "mapping_template": "mappingTemplate",
        "name": "name",
        "output_conversion": "outputConversion",
        "sample_document": "sampleDocument",
        "sample_documents": "sampleDocuments",
        "status": "status",
        "tags": "tags",
    },
)
class CfnTransformerMixinProps:
    def __init__(
        self,
        *,
        edi_type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.EdiTypeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        file_format: typing.Optional[builtins.str] = None,
        input_conversion: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.InputConversionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        mapping: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.MappingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        mapping_template: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        output_conversion: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.OutputConversionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        sample_document: typing.Optional[builtins.str] = None,
        sample_documents: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.SampleDocumentsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnTransformerPropsMixin.

        :param edi_type: 
        :param file_format: 
        :param input_conversion: Returns a structure that contains the format options for the transformation.
        :param mapping: Returns the structure that contains the mapping template and its language (either XSLT or JSONATA).
        :param mapping_template: (deprecated) This shape is deprecated: This is a legacy trait. Please use input-conversion or output-conversion.
        :param name: Returns the descriptive name for the transformer.
        :param output_conversion: Returns the ``OutputConversion`` object, which contains the format options for the outbound transformation.
        :param sample_document: (deprecated) This shape is deprecated: This is a legacy trait. Please use input-conversion or output-conversion.
        :param sample_documents: Returns a structure that contains the Amazon S3 bucket and an array of the corresponding keys used to identify the location for your sample documents.
        :param status: Returns the state of the newly created transformer. The transformer can be either ``active`` or ``inactive`` . For the transformer to be used in a capability, its status must ``active`` .
        :param tags: A key-value pair for a specific transformer. Tags are metadata that you can use to search for and group capabilities for various purposes.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-b2bi-transformer.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_b2bi import mixins as b2bi_mixins
            
            cfn_transformer_mixin_props = b2bi_mixins.CfnTransformerMixinProps(
                edi_type=b2bi_mixins.CfnTransformerPropsMixin.EdiTypeProperty(
                    x12_details=b2bi_mixins.CfnTransformerPropsMixin.X12DetailsProperty(
                        transaction_set="transactionSet",
                        version="version"
                    )
                ),
                file_format="fileFormat",
                input_conversion=b2bi_mixins.CfnTransformerPropsMixin.InputConversionProperty(
                    advanced_options=b2bi_mixins.CfnTransformerPropsMixin.AdvancedOptionsProperty(
                        x12=b2bi_mixins.CfnTransformerPropsMixin.X12AdvancedOptionsProperty(
                            split_options=b2bi_mixins.CfnTransformerPropsMixin.X12SplitOptionsProperty(
                                split_by="splitBy"
                            ),
                            validation_options=b2bi_mixins.CfnTransformerPropsMixin.X12ValidationOptionsProperty(
                                validation_rules=[b2bi_mixins.CfnTransformerPropsMixin.X12ValidationRuleProperty(
                                    code_list_validation_rule=b2bi_mixins.CfnTransformerPropsMixin.X12CodeListValidationRuleProperty(
                                        codes_to_add=["codesToAdd"],
                                        codes_to_remove=["codesToRemove"],
                                        element_id="elementId"
                                    ),
                                    element_length_validation_rule=b2bi_mixins.CfnTransformerPropsMixin.X12ElementLengthValidationRuleProperty(
                                        element_id="elementId",
                                        max_length=123,
                                        min_length=123
                                    ),
                                    element_requirement_validation_rule=b2bi_mixins.CfnTransformerPropsMixin.X12ElementRequirementValidationRuleProperty(
                                        element_position="elementPosition",
                                        requirement="requirement"
                                    )
                                )]
                            )
                        )
                    ),
                    format_options=b2bi_mixins.CfnTransformerPropsMixin.FormatOptionsProperty(
                        x12=b2bi_mixins.CfnTransformerPropsMixin.X12DetailsProperty(
                            transaction_set="transactionSet",
                            version="version"
                        )
                    ),
                    from_format="fromFormat"
                ),
                mapping=b2bi_mixins.CfnTransformerPropsMixin.MappingProperty(
                    template="template",
                    template_language="templateLanguage"
                ),
                mapping_template="mappingTemplate",
                name="name",
                output_conversion=b2bi_mixins.CfnTransformerPropsMixin.OutputConversionProperty(
                    advanced_options=b2bi_mixins.CfnTransformerPropsMixin.AdvancedOptionsProperty(
                        x12=b2bi_mixins.CfnTransformerPropsMixin.X12AdvancedOptionsProperty(
                            split_options=b2bi_mixins.CfnTransformerPropsMixin.X12SplitOptionsProperty(
                                split_by="splitBy"
                            ),
                            validation_options=b2bi_mixins.CfnTransformerPropsMixin.X12ValidationOptionsProperty(
                                validation_rules=[b2bi_mixins.CfnTransformerPropsMixin.X12ValidationRuleProperty(
                                    code_list_validation_rule=b2bi_mixins.CfnTransformerPropsMixin.X12CodeListValidationRuleProperty(
                                        codes_to_add=["codesToAdd"],
                                        codes_to_remove=["codesToRemove"],
                                        element_id="elementId"
                                    ),
                                    element_length_validation_rule=b2bi_mixins.CfnTransformerPropsMixin.X12ElementLengthValidationRuleProperty(
                                        element_id="elementId",
                                        max_length=123,
                                        min_length=123
                                    ),
                                    element_requirement_validation_rule=b2bi_mixins.CfnTransformerPropsMixin.X12ElementRequirementValidationRuleProperty(
                                        element_position="elementPosition",
                                        requirement="requirement"
                                    )
                                )]
                            )
                        )
                    ),
                    format_options=b2bi_mixins.CfnTransformerPropsMixin.FormatOptionsProperty(
                        x12=b2bi_mixins.CfnTransformerPropsMixin.X12DetailsProperty(
                            transaction_set="transactionSet",
                            version="version"
                        )
                    ),
                    to_format="toFormat"
                ),
                sample_document="sampleDocument",
                sample_documents=b2bi_mixins.CfnTransformerPropsMixin.SampleDocumentsProperty(
                    bucket_name="bucketName",
                    keys=[b2bi_mixins.CfnTransformerPropsMixin.SampleDocumentKeysProperty(
                        input="input",
                        output="output"
                    )]
                ),
                status="status",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c41eddd4788c420ee51aa348a0716316facde41557d8d7617831ca6a1058172)
            check_type(argname="argument edi_type", value=edi_type, expected_type=type_hints["edi_type"])
            check_type(argname="argument file_format", value=file_format, expected_type=type_hints["file_format"])
            check_type(argname="argument input_conversion", value=input_conversion, expected_type=type_hints["input_conversion"])
            check_type(argname="argument mapping", value=mapping, expected_type=type_hints["mapping"])
            check_type(argname="argument mapping_template", value=mapping_template, expected_type=type_hints["mapping_template"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument output_conversion", value=output_conversion, expected_type=type_hints["output_conversion"])
            check_type(argname="argument sample_document", value=sample_document, expected_type=type_hints["sample_document"])
            check_type(argname="argument sample_documents", value=sample_documents, expected_type=type_hints["sample_documents"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if edi_type is not None:
            self._values["edi_type"] = edi_type
        if file_format is not None:
            self._values["file_format"] = file_format
        if input_conversion is not None:
            self._values["input_conversion"] = input_conversion
        if mapping is not None:
            self._values["mapping"] = mapping
        if mapping_template is not None:
            self._values["mapping_template"] = mapping_template
        if name is not None:
            self._values["name"] = name
        if output_conversion is not None:
            self._values["output_conversion"] = output_conversion
        if sample_document is not None:
            self._values["sample_document"] = sample_document
        if sample_documents is not None:
            self._values["sample_documents"] = sample_documents
        if status is not None:
            self._values["status"] = status
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def edi_type(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.EdiTypeProperty"]]:
        '''
        :deprecated: this property has been deprecated

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-b2bi-transformer.html#cfn-b2bi-transformer-editype
        :stability: deprecated
        '''
        result = self._values.get("edi_type")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.EdiTypeProperty"]], result)

    @builtins.property
    def file_format(self) -> typing.Optional[builtins.str]:
        '''
        :deprecated: this property has been deprecated

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-b2bi-transformer.html#cfn-b2bi-transformer-fileformat
        :stability: deprecated
        '''
        result = self._values.get("file_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def input_conversion(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.InputConversionProperty"]]:
        '''Returns a structure that contains the format options for the transformation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-b2bi-transformer.html#cfn-b2bi-transformer-inputconversion
        '''
        result = self._values.get("input_conversion")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.InputConversionProperty"]], result)

    @builtins.property
    def mapping(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.MappingProperty"]]:
        '''Returns the structure that contains the mapping template and its language (either XSLT or JSONATA).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-b2bi-transformer.html#cfn-b2bi-transformer-mapping
        '''
        result = self._values.get("mapping")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.MappingProperty"]], result)

    @builtins.property
    def mapping_template(self) -> typing.Optional[builtins.str]:
        '''(deprecated) This shape is deprecated: This is a legacy trait.

        Please use input-conversion or output-conversion.

        :deprecated: this property has been deprecated

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-b2bi-transformer.html#cfn-b2bi-transformer-mappingtemplate
        :stability: deprecated
        '''
        result = self._values.get("mapping_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Returns the descriptive name for the transformer.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-b2bi-transformer.html#cfn-b2bi-transformer-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output_conversion(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.OutputConversionProperty"]]:
        '''Returns the ``OutputConversion`` object, which contains the format options for the outbound transformation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-b2bi-transformer.html#cfn-b2bi-transformer-outputconversion
        '''
        result = self._values.get("output_conversion")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.OutputConversionProperty"]], result)

    @builtins.property
    def sample_document(self) -> typing.Optional[builtins.str]:
        '''(deprecated) This shape is deprecated: This is a legacy trait.

        Please use input-conversion or output-conversion.

        :deprecated: this property has been deprecated

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-b2bi-transformer.html#cfn-b2bi-transformer-sampledocument
        :stability: deprecated
        '''
        result = self._values.get("sample_document")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sample_documents(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.SampleDocumentsProperty"]]:
        '''Returns a structure that contains the Amazon S3 bucket and an array of the corresponding keys used to identify the location for your sample documents.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-b2bi-transformer.html#cfn-b2bi-transformer-sampledocuments
        '''
        result = self._values.get("sample_documents")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.SampleDocumentsProperty"]], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Returns the state of the newly created transformer.

        The transformer can be either ``active`` or ``inactive`` . For the transformer to be used in a capability, its status must ``active`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-b2bi-transformer.html#cfn-b2bi-transformer-status
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A key-value pair for a specific transformer.

        Tags are metadata that you can use to search for and group capabilities for various purposes.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-b2bi-transformer.html#cfn-b2bi-transformer-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTransformerMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnTransformerPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_b2bi.mixins.CfnTransformerPropsMixin",
):
    '''Creates a transformer. AWS B2B Data Interchange currently supports two scenarios:.

    - *Inbound EDI* : the AWS customer receives an EDI file from their trading partner. AWS B2B Data Interchange converts this EDI file into a JSON or XML file with a service-defined structure. A mapping template provided by the customer, in JSONata or XSLT format, is optionally applied to this file to produce a JSON or XML file with the structure the customer requires.
    - *Outbound EDI* : the AWS customer has a JSON or XML file containing data that they wish to use in an EDI file. A mapping template, provided by the customer (in either JSONata or XSLT format) is applied to this file to generate a JSON or XML file in the service-defined structure. This file is then converted to an EDI file.

    .. epigraph::

       The following fields are provided for backwards compatibility only: ``fileFormat`` , ``mappingTemplate`` , ``ediType`` , and ``sampleDocument`` .

       - Use the ``mapping`` data type in place of ``mappingTemplate`` and ``fileFormat``
       - Use the ``sampleDocuments`` data type in place of ``sampleDocument``
       - Use either the ``inputConversion`` or ``outputConversion`` in place of ``ediType``

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-b2bi-transformer.html
    :cloudformationResource: AWS::B2BI::Transformer
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_b2bi import mixins as b2bi_mixins
        
        cfn_transformer_props_mixin = b2bi_mixins.CfnTransformerPropsMixin(b2bi_mixins.CfnTransformerMixinProps(
            edi_type=b2bi_mixins.CfnTransformerPropsMixin.EdiTypeProperty(
                x12_details=b2bi_mixins.CfnTransformerPropsMixin.X12DetailsProperty(
                    transaction_set="transactionSet",
                    version="version"
                )
            ),
            file_format="fileFormat",
            input_conversion=b2bi_mixins.CfnTransformerPropsMixin.InputConversionProperty(
                advanced_options=b2bi_mixins.CfnTransformerPropsMixin.AdvancedOptionsProperty(
                    x12=b2bi_mixins.CfnTransformerPropsMixin.X12AdvancedOptionsProperty(
                        split_options=b2bi_mixins.CfnTransformerPropsMixin.X12SplitOptionsProperty(
                            split_by="splitBy"
                        ),
                        validation_options=b2bi_mixins.CfnTransformerPropsMixin.X12ValidationOptionsProperty(
                            validation_rules=[b2bi_mixins.CfnTransformerPropsMixin.X12ValidationRuleProperty(
                                code_list_validation_rule=b2bi_mixins.CfnTransformerPropsMixin.X12CodeListValidationRuleProperty(
                                    codes_to_add=["codesToAdd"],
                                    codes_to_remove=["codesToRemove"],
                                    element_id="elementId"
                                ),
                                element_length_validation_rule=b2bi_mixins.CfnTransformerPropsMixin.X12ElementLengthValidationRuleProperty(
                                    element_id="elementId",
                                    max_length=123,
                                    min_length=123
                                ),
                                element_requirement_validation_rule=b2bi_mixins.CfnTransformerPropsMixin.X12ElementRequirementValidationRuleProperty(
                                    element_position="elementPosition",
                                    requirement="requirement"
                                )
                            )]
                        )
                    )
                ),
                format_options=b2bi_mixins.CfnTransformerPropsMixin.FormatOptionsProperty(
                    x12=b2bi_mixins.CfnTransformerPropsMixin.X12DetailsProperty(
                        transaction_set="transactionSet",
                        version="version"
                    )
                ),
                from_format="fromFormat"
            ),
            mapping=b2bi_mixins.CfnTransformerPropsMixin.MappingProperty(
                template="template",
                template_language="templateLanguage"
            ),
            mapping_template="mappingTemplate",
            name="name",
            output_conversion=b2bi_mixins.CfnTransformerPropsMixin.OutputConversionProperty(
                advanced_options=b2bi_mixins.CfnTransformerPropsMixin.AdvancedOptionsProperty(
                    x12=b2bi_mixins.CfnTransformerPropsMixin.X12AdvancedOptionsProperty(
                        split_options=b2bi_mixins.CfnTransformerPropsMixin.X12SplitOptionsProperty(
                            split_by="splitBy"
                        ),
                        validation_options=b2bi_mixins.CfnTransformerPropsMixin.X12ValidationOptionsProperty(
                            validation_rules=[b2bi_mixins.CfnTransformerPropsMixin.X12ValidationRuleProperty(
                                code_list_validation_rule=b2bi_mixins.CfnTransformerPropsMixin.X12CodeListValidationRuleProperty(
                                    codes_to_add=["codesToAdd"],
                                    codes_to_remove=["codesToRemove"],
                                    element_id="elementId"
                                ),
                                element_length_validation_rule=b2bi_mixins.CfnTransformerPropsMixin.X12ElementLengthValidationRuleProperty(
                                    element_id="elementId",
                                    max_length=123,
                                    min_length=123
                                ),
                                element_requirement_validation_rule=b2bi_mixins.CfnTransformerPropsMixin.X12ElementRequirementValidationRuleProperty(
                                    element_position="elementPosition",
                                    requirement="requirement"
                                )
                            )]
                        )
                    )
                ),
                format_options=b2bi_mixins.CfnTransformerPropsMixin.FormatOptionsProperty(
                    x12=b2bi_mixins.CfnTransformerPropsMixin.X12DetailsProperty(
                        transaction_set="transactionSet",
                        version="version"
                    )
                ),
                to_format="toFormat"
            ),
            sample_document="sampleDocument",
            sample_documents=b2bi_mixins.CfnTransformerPropsMixin.SampleDocumentsProperty(
                bucket_name="bucketName",
                keys=[b2bi_mixins.CfnTransformerPropsMixin.SampleDocumentKeysProperty(
                    input="input",
                    output="output"
                )]
            ),
            status="status",
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
        props: typing.Union[CfnTransformerMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::B2BI::Transformer``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2572390f2c49c4d247f7ec5f283de9ca993ab5212da3d3087e00abeff633c80)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c61ea097e78bb7bc6c1333cc4d612feaa5591f6f07755688b0870d70e3822a30)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2955ed91d7b227ae3583d40bea68d2f67e83f1ebd644c21c6b9e76f589a6661b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTransformerMixinProps:
        return typing.cast(CfnTransformerMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_b2bi.mixins.CfnTransformerPropsMixin.AdvancedOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"x12": "x12"},
    )
    class AdvancedOptionsProperty:
        def __init__(
            self,
            *,
            x12: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.X12AdvancedOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A structure that contains advanced options for EDI processing.

            Currently, only X12 advanced options are supported.

            :param x12: A structure that contains X12-specific advanced options, such as split options for processing X12 EDI files.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-advancedoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_b2bi import mixins as b2bi_mixins
                
                advanced_options_property = b2bi_mixins.CfnTransformerPropsMixin.AdvancedOptionsProperty(
                    x12=b2bi_mixins.CfnTransformerPropsMixin.X12AdvancedOptionsProperty(
                        split_options=b2bi_mixins.CfnTransformerPropsMixin.X12SplitOptionsProperty(
                            split_by="splitBy"
                        ),
                        validation_options=b2bi_mixins.CfnTransformerPropsMixin.X12ValidationOptionsProperty(
                            validation_rules=[b2bi_mixins.CfnTransformerPropsMixin.X12ValidationRuleProperty(
                                code_list_validation_rule=b2bi_mixins.CfnTransformerPropsMixin.X12CodeListValidationRuleProperty(
                                    codes_to_add=["codesToAdd"],
                                    codes_to_remove=["codesToRemove"],
                                    element_id="elementId"
                                ),
                                element_length_validation_rule=b2bi_mixins.CfnTransformerPropsMixin.X12ElementLengthValidationRuleProperty(
                                    element_id="elementId",
                                    max_length=123,
                                    min_length=123
                                ),
                                element_requirement_validation_rule=b2bi_mixins.CfnTransformerPropsMixin.X12ElementRequirementValidationRuleProperty(
                                    element_position="elementPosition",
                                    requirement="requirement"
                                )
                            )]
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3b01ba66cc5c8be9aacab05c48a6d19ab1eba19e0d3851e6e68cd62d28fc1f85)
                check_type(argname="argument x12", value=x12, expected_type=type_hints["x12"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if x12 is not None:
                self._values["x12"] = x12

        @builtins.property
        def x12(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.X12AdvancedOptionsProperty"]]:
            '''A structure that contains X12-specific advanced options, such as split options for processing X12 EDI files.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-advancedoptions.html#cfn-b2bi-transformer-advancedoptions-x12
            '''
            result = self._values.get("x12")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.X12AdvancedOptionsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AdvancedOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_b2bi.mixins.CfnTransformerPropsMixin.EdiTypeProperty",
        jsii_struct_bases=[],
        name_mapping={"x12_details": "x12Details"},
    )
    class EdiTypeProperty:
        def __init__(
            self,
            *,
            x12_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.X12DetailsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param x12_details: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-editype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_b2bi import mixins as b2bi_mixins
                
                edi_type_property = b2bi_mixins.CfnTransformerPropsMixin.EdiTypeProperty(
                    x12_details=b2bi_mixins.CfnTransformerPropsMixin.X12DetailsProperty(
                        transaction_set="transactionSet",
                        version="version"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__22522d308c9bdd06ba9f05f33d780765a9beab79f1dcc7b78ec14b6e4115117f)
                check_type(argname="argument x12_details", value=x12_details, expected_type=type_hints["x12_details"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if x12_details is not None:
                self._values["x12_details"] = x12_details

        @builtins.property
        def x12_details(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.X12DetailsProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-editype.html#cfn-b2bi-transformer-editype-x12details
            '''
            result = self._values.get("x12_details")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.X12DetailsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EdiTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_b2bi.mixins.CfnTransformerPropsMixin.FormatOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"x12": "x12"},
    )
    class FormatOptionsProperty:
        def __init__(
            self,
            *,
            x12: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.X12DetailsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A structure that contains the X12 transaction set and version.

            :param x12: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-formatoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_b2bi import mixins as b2bi_mixins
                
                format_options_property = b2bi_mixins.CfnTransformerPropsMixin.FormatOptionsProperty(
                    x12=b2bi_mixins.CfnTransformerPropsMixin.X12DetailsProperty(
                        transaction_set="transactionSet",
                        version="version"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fd308b9f36b92838587381b3051af45896cbf66722173b10184ef1122f1f852a)
                check_type(argname="argument x12", value=x12, expected_type=type_hints["x12"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if x12 is not None:
                self._values["x12"] = x12

        @builtins.property
        def x12(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.X12DetailsProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-formatoptions.html#cfn-b2bi-transformer-formatoptions-x12
            '''
            result = self._values.get("x12")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.X12DetailsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FormatOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_b2bi.mixins.CfnTransformerPropsMixin.InputConversionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "advanced_options": "advancedOptions",
            "format_options": "formatOptions",
            "from_format": "fromFormat",
        },
    )
    class InputConversionProperty:
        def __init__(
            self,
            *,
            advanced_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.AdvancedOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            format_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.FormatOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            from_format: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains the input formatting options for an inbound transformer (takes an X12-formatted EDI document as input and converts it to JSON or XML.

            :param advanced_options: Specifies advanced options for the input conversion process. These options provide additional control over how EDI files are processed during transformation.
            :param format_options: A structure that contains the formatting options for an inbound transformer.
            :param from_format: The format for the transformer input: currently on ``X12`` is supported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-inputconversion.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_b2bi import mixins as b2bi_mixins
                
                input_conversion_property = b2bi_mixins.CfnTransformerPropsMixin.InputConversionProperty(
                    advanced_options=b2bi_mixins.CfnTransformerPropsMixin.AdvancedOptionsProperty(
                        x12=b2bi_mixins.CfnTransformerPropsMixin.X12AdvancedOptionsProperty(
                            split_options=b2bi_mixins.CfnTransformerPropsMixin.X12SplitOptionsProperty(
                                split_by="splitBy"
                            ),
                            validation_options=b2bi_mixins.CfnTransformerPropsMixin.X12ValidationOptionsProperty(
                                validation_rules=[b2bi_mixins.CfnTransformerPropsMixin.X12ValidationRuleProperty(
                                    code_list_validation_rule=b2bi_mixins.CfnTransformerPropsMixin.X12CodeListValidationRuleProperty(
                                        codes_to_add=["codesToAdd"],
                                        codes_to_remove=["codesToRemove"],
                                        element_id="elementId"
                                    ),
                                    element_length_validation_rule=b2bi_mixins.CfnTransformerPropsMixin.X12ElementLengthValidationRuleProperty(
                                        element_id="elementId",
                                        max_length=123,
                                        min_length=123
                                    ),
                                    element_requirement_validation_rule=b2bi_mixins.CfnTransformerPropsMixin.X12ElementRequirementValidationRuleProperty(
                                        element_position="elementPosition",
                                        requirement="requirement"
                                    )
                                )]
                            )
                        )
                    ),
                    format_options=b2bi_mixins.CfnTransformerPropsMixin.FormatOptionsProperty(
                        x12=b2bi_mixins.CfnTransformerPropsMixin.X12DetailsProperty(
                            transaction_set="transactionSet",
                            version="version"
                        )
                    ),
                    from_format="fromFormat"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9541172c4126bd0ac1f2ef317cdf5fd25f23f60d9a7dc87fb303c9b7360c56b7)
                check_type(argname="argument advanced_options", value=advanced_options, expected_type=type_hints["advanced_options"])
                check_type(argname="argument format_options", value=format_options, expected_type=type_hints["format_options"])
                check_type(argname="argument from_format", value=from_format, expected_type=type_hints["from_format"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if advanced_options is not None:
                self._values["advanced_options"] = advanced_options
            if format_options is not None:
                self._values["format_options"] = format_options
            if from_format is not None:
                self._values["from_format"] = from_format

        @builtins.property
        def advanced_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.AdvancedOptionsProperty"]]:
            '''Specifies advanced options for the input conversion process.

            These options provide additional control over how EDI files are processed during transformation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-inputconversion.html#cfn-b2bi-transformer-inputconversion-advancedoptions
            '''
            result = self._values.get("advanced_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.AdvancedOptionsProperty"]], result)

        @builtins.property
        def format_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.FormatOptionsProperty"]]:
            '''A structure that contains the formatting options for an inbound transformer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-inputconversion.html#cfn-b2bi-transformer-inputconversion-formatoptions
            '''
            result = self._values.get("format_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.FormatOptionsProperty"]], result)

        @builtins.property
        def from_format(self) -> typing.Optional[builtins.str]:
            '''The format for the transformer input: currently on ``X12`` is supported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-inputconversion.html#cfn-b2bi-transformer-inputconversion-fromformat
            '''
            result = self._values.get("from_format")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputConversionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_b2bi.mixins.CfnTransformerPropsMixin.MappingProperty",
        jsii_struct_bases=[],
        name_mapping={"template": "template", "template_language": "templateLanguage"},
    )
    class MappingProperty:
        def __init__(
            self,
            *,
            template: typing.Optional[builtins.str] = None,
            template_language: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the mapping template for the transformer.

            This template is used to map the parsed EDI file using JSONata or XSLT.

            :param template: A string that represents the mapping template, in the transformation language specified in ``templateLanguage`` .
            :param template_language: The transformation language for the template, either XSLT or JSONATA.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-mapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_b2bi import mixins as b2bi_mixins
                
                mapping_property = b2bi_mixins.CfnTransformerPropsMixin.MappingProperty(
                    template="template",
                    template_language="templateLanguage"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__56e2db1fa32f4fde3b13288c103715e3be43ea80170f1c00fbfb5be1da341dec)
                check_type(argname="argument template", value=template, expected_type=type_hints["template"])
                check_type(argname="argument template_language", value=template_language, expected_type=type_hints["template_language"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if template is not None:
                self._values["template"] = template
            if template_language is not None:
                self._values["template_language"] = template_language

        @builtins.property
        def template(self) -> typing.Optional[builtins.str]:
            '''A string that represents the mapping template, in the transformation language specified in ``templateLanguage`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-mapping.html#cfn-b2bi-transformer-mapping-template
            '''
            result = self._values.get("template")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def template_language(self) -> typing.Optional[builtins.str]:
            '''The transformation language for the template, either XSLT or JSONATA.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-mapping.html#cfn-b2bi-transformer-mapping-templatelanguage
            '''
            result = self._values.get("template_language")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_b2bi.mixins.CfnTransformerPropsMixin.OutputConversionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "advanced_options": "advancedOptions",
            "format_options": "formatOptions",
            "to_format": "toFormat",
        },
    )
    class OutputConversionProperty:
        def __init__(
            self,
            *,
            advanced_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.AdvancedOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            format_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.FormatOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            to_format: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains the formatting options for an outbound transformer (takes JSON or XML as input and converts it to an EDI document (currently only X12 format is supported).

            :param advanced_options: 
            :param format_options: A structure that contains the X12 transaction set and version for the transformer output.
            :param to_format: The format for the output from an outbound transformer: only X12 is currently supported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-outputconversion.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_b2bi import mixins as b2bi_mixins
                
                output_conversion_property = b2bi_mixins.CfnTransformerPropsMixin.OutputConversionProperty(
                    advanced_options=b2bi_mixins.CfnTransformerPropsMixin.AdvancedOptionsProperty(
                        x12=b2bi_mixins.CfnTransformerPropsMixin.X12AdvancedOptionsProperty(
                            split_options=b2bi_mixins.CfnTransformerPropsMixin.X12SplitOptionsProperty(
                                split_by="splitBy"
                            ),
                            validation_options=b2bi_mixins.CfnTransformerPropsMixin.X12ValidationOptionsProperty(
                                validation_rules=[b2bi_mixins.CfnTransformerPropsMixin.X12ValidationRuleProperty(
                                    code_list_validation_rule=b2bi_mixins.CfnTransformerPropsMixin.X12CodeListValidationRuleProperty(
                                        codes_to_add=["codesToAdd"],
                                        codes_to_remove=["codesToRemove"],
                                        element_id="elementId"
                                    ),
                                    element_length_validation_rule=b2bi_mixins.CfnTransformerPropsMixin.X12ElementLengthValidationRuleProperty(
                                        element_id="elementId",
                                        max_length=123,
                                        min_length=123
                                    ),
                                    element_requirement_validation_rule=b2bi_mixins.CfnTransformerPropsMixin.X12ElementRequirementValidationRuleProperty(
                                        element_position="elementPosition",
                                        requirement="requirement"
                                    )
                                )]
                            )
                        )
                    ),
                    format_options=b2bi_mixins.CfnTransformerPropsMixin.FormatOptionsProperty(
                        x12=b2bi_mixins.CfnTransformerPropsMixin.X12DetailsProperty(
                            transaction_set="transactionSet",
                            version="version"
                        )
                    ),
                    to_format="toFormat"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__214910fc8aefbc361d91ce143bea47e4a0622a42103c0709ef91221a61730367)
                check_type(argname="argument advanced_options", value=advanced_options, expected_type=type_hints["advanced_options"])
                check_type(argname="argument format_options", value=format_options, expected_type=type_hints["format_options"])
                check_type(argname="argument to_format", value=to_format, expected_type=type_hints["to_format"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if advanced_options is not None:
                self._values["advanced_options"] = advanced_options
            if format_options is not None:
                self._values["format_options"] = format_options
            if to_format is not None:
                self._values["to_format"] = to_format

        @builtins.property
        def advanced_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.AdvancedOptionsProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-outputconversion.html#cfn-b2bi-transformer-outputconversion-advancedoptions
            '''
            result = self._values.get("advanced_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.AdvancedOptionsProperty"]], result)

        @builtins.property
        def format_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.FormatOptionsProperty"]]:
            '''A structure that contains the X12 transaction set and version for the transformer output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-outputconversion.html#cfn-b2bi-transformer-outputconversion-formatoptions
            '''
            result = self._values.get("format_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.FormatOptionsProperty"]], result)

        @builtins.property
        def to_format(self) -> typing.Optional[builtins.str]:
            '''The format for the output from an outbound transformer: only X12 is currently supported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-outputconversion.html#cfn-b2bi-transformer-outputconversion-toformat
            '''
            result = self._values.get("to_format")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OutputConversionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_b2bi.mixins.CfnTransformerPropsMixin.SampleDocumentKeysProperty",
        jsii_struct_bases=[],
        name_mapping={"input": "input", "output": "output"},
    )
    class SampleDocumentKeysProperty:
        def __init__(
            self,
            *,
            input: typing.Optional[builtins.str] = None,
            output: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An array of the Amazon S3 keys used to identify the location for your sample documents.

            :param input: An array of keys for your input sample documents.
            :param output: An array of keys for your output sample documents.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-sampledocumentkeys.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_b2bi import mixins as b2bi_mixins
                
                sample_document_keys_property = b2bi_mixins.CfnTransformerPropsMixin.SampleDocumentKeysProperty(
                    input="input",
                    output="output"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e462f759900f7c87eb45dfcf7cfdbbb8cf671b6bb458532145393381f63bc4df)
                check_type(argname="argument input", value=input, expected_type=type_hints["input"])
                check_type(argname="argument output", value=output, expected_type=type_hints["output"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if input is not None:
                self._values["input"] = input
            if output is not None:
                self._values["output"] = output

        @builtins.property
        def input(self) -> typing.Optional[builtins.str]:
            '''An array of keys for your input sample documents.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-sampledocumentkeys.html#cfn-b2bi-transformer-sampledocumentkeys-input
            '''
            result = self._values.get("input")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def output(self) -> typing.Optional[builtins.str]:
            '''An array of keys for your output sample documents.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-sampledocumentkeys.html#cfn-b2bi-transformer-sampledocumentkeys-output
            '''
            result = self._values.get("output")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SampleDocumentKeysProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_b2bi.mixins.CfnTransformerPropsMixin.SampleDocumentsProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket_name": "bucketName", "keys": "keys"},
    )
    class SampleDocumentsProperty:
        def __init__(
            self,
            *,
            bucket_name: typing.Optional[builtins.str] = None,
            keys: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.SampleDocumentKeysProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Describes a structure that contains the Amazon S3 bucket and an array of the corresponding keys used to identify the location for your sample documents.

            :param bucket_name: Contains the Amazon S3 bucket that is used to hold your sample documents.
            :param keys: Contains an array of the Amazon S3 keys used to identify the location for your sample documents.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-sampledocuments.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_b2bi import mixins as b2bi_mixins
                
                sample_documents_property = b2bi_mixins.CfnTransformerPropsMixin.SampleDocumentsProperty(
                    bucket_name="bucketName",
                    keys=[b2bi_mixins.CfnTransformerPropsMixin.SampleDocumentKeysProperty(
                        input="input",
                        output="output"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5d1c823b5edabc55200ae3df4d24271746964a2484ad336cc7e98424f44df934)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument keys", value=keys, expected_type=type_hints["keys"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_name is not None:
                self._values["bucket_name"] = bucket_name
            if keys is not None:
                self._values["keys"] = keys

        @builtins.property
        def bucket_name(self) -> typing.Optional[builtins.str]:
            '''Contains the Amazon S3 bucket that is used to hold your sample documents.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-sampledocuments.html#cfn-b2bi-transformer-sampledocuments-bucketname
            '''
            result = self._values.get("bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def keys(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.SampleDocumentKeysProperty"]]]]:
            '''Contains an array of the Amazon S3 keys used to identify the location for your sample documents.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-sampledocuments.html#cfn-b2bi-transformer-sampledocuments-keys
            '''
            result = self._values.get("keys")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.SampleDocumentKeysProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SampleDocumentsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_b2bi.mixins.CfnTransformerPropsMixin.X12AdvancedOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "split_options": "splitOptions",
            "validation_options": "validationOptions",
        },
    )
    class X12AdvancedOptionsProperty:
        def __init__(
            self,
            *,
            split_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.X12SplitOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            validation_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.X12ValidationOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains advanced options specific to X12 EDI processing, such as splitting large X12 files into smaller units.

            :param split_options: Specifies options for splitting X12 EDI files. These options control how large X12 files are divided into smaller, more manageable units.
            :param validation_options: Specifies validation options for X12 EDI processing. These options control how validation rules are applied during EDI document processing, including custom validation rules for element length constraints, code list validations, and element requirement checks.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-x12advancedoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_b2bi import mixins as b2bi_mixins
                
                x12_advanced_options_property = b2bi_mixins.CfnTransformerPropsMixin.X12AdvancedOptionsProperty(
                    split_options=b2bi_mixins.CfnTransformerPropsMixin.X12SplitOptionsProperty(
                        split_by="splitBy"
                    ),
                    validation_options=b2bi_mixins.CfnTransformerPropsMixin.X12ValidationOptionsProperty(
                        validation_rules=[b2bi_mixins.CfnTransformerPropsMixin.X12ValidationRuleProperty(
                            code_list_validation_rule=b2bi_mixins.CfnTransformerPropsMixin.X12CodeListValidationRuleProperty(
                                codes_to_add=["codesToAdd"],
                                codes_to_remove=["codesToRemove"],
                                element_id="elementId"
                            ),
                            element_length_validation_rule=b2bi_mixins.CfnTransformerPropsMixin.X12ElementLengthValidationRuleProperty(
                                element_id="elementId",
                                max_length=123,
                                min_length=123
                            ),
                            element_requirement_validation_rule=b2bi_mixins.CfnTransformerPropsMixin.X12ElementRequirementValidationRuleProperty(
                                element_position="elementPosition",
                                requirement="requirement"
                            )
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a256fd2f3d893f4d641923c73ad19921910b07af726adfee37d589d53662a851)
                check_type(argname="argument split_options", value=split_options, expected_type=type_hints["split_options"])
                check_type(argname="argument validation_options", value=validation_options, expected_type=type_hints["validation_options"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if split_options is not None:
                self._values["split_options"] = split_options
            if validation_options is not None:
                self._values["validation_options"] = validation_options

        @builtins.property
        def split_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.X12SplitOptionsProperty"]]:
            '''Specifies options for splitting X12 EDI files.

            These options control how large X12 files are divided into smaller, more manageable units.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-x12advancedoptions.html#cfn-b2bi-transformer-x12advancedoptions-splitoptions
            '''
            result = self._values.get("split_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.X12SplitOptionsProperty"]], result)

        @builtins.property
        def validation_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.X12ValidationOptionsProperty"]]:
            '''Specifies validation options for X12 EDI processing.

            These options control how validation rules are applied during EDI document processing, including custom validation rules for element length constraints, code list validations, and element requirement checks.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-x12advancedoptions.html#cfn-b2bi-transformer-x12advancedoptions-validationoptions
            '''
            result = self._values.get("validation_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.X12ValidationOptionsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "X12AdvancedOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_b2bi.mixins.CfnTransformerPropsMixin.X12CodeListValidationRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "codes_to_add": "codesToAdd",
            "codes_to_remove": "codesToRemove",
            "element_id": "elementId",
        },
    )
    class X12CodeListValidationRuleProperty:
        def __init__(
            self,
            *,
            codes_to_add: typing.Optional[typing.Sequence[builtins.str]] = None,
            codes_to_remove: typing.Optional[typing.Sequence[builtins.str]] = None,
            element_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Code list validation rule configuration.

            :param codes_to_add: Specifies a list of code values to add to the element's allowed values. These codes will be considered valid for the specified element in addition to the standard codes defined by the X12 specification.
            :param codes_to_remove: Specifies a list of code values to remove from the element's allowed values. These codes will be considered invalid for the specified element, even if they are part of the standard codes defined by the X12 specification.
            :param element_id: Specifies the four-digit element ID to which the code list modifications apply. This identifies which X12 element will have its allowed code values modified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-x12codelistvalidationrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_b2bi import mixins as b2bi_mixins
                
                x12_code_list_validation_rule_property = b2bi_mixins.CfnTransformerPropsMixin.X12CodeListValidationRuleProperty(
                    codes_to_add=["codesToAdd"],
                    codes_to_remove=["codesToRemove"],
                    element_id="elementId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d537f5a25a4e686a0dda2c99f1bda25a51b8e53bdeb0d83836631aa6a68547f8)
                check_type(argname="argument codes_to_add", value=codes_to_add, expected_type=type_hints["codes_to_add"])
                check_type(argname="argument codes_to_remove", value=codes_to_remove, expected_type=type_hints["codes_to_remove"])
                check_type(argname="argument element_id", value=element_id, expected_type=type_hints["element_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if codes_to_add is not None:
                self._values["codes_to_add"] = codes_to_add
            if codes_to_remove is not None:
                self._values["codes_to_remove"] = codes_to_remove
            if element_id is not None:
                self._values["element_id"] = element_id

        @builtins.property
        def codes_to_add(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Specifies a list of code values to add to the element's allowed values.

            These codes will be considered valid for the specified element in addition to the standard codes defined by the X12 specification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-x12codelistvalidationrule.html#cfn-b2bi-transformer-x12codelistvalidationrule-codestoadd
            '''
            result = self._values.get("codes_to_add")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def codes_to_remove(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Specifies a list of code values to remove from the element's allowed values.

            These codes will be considered invalid for the specified element, even if they are part of the standard codes defined by the X12 specification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-x12codelistvalidationrule.html#cfn-b2bi-transformer-x12codelistvalidationrule-codestoremove
            '''
            result = self._values.get("codes_to_remove")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def element_id(self) -> typing.Optional[builtins.str]:
            '''Specifies the four-digit element ID to which the code list modifications apply.

            This identifies which X12 element will have its allowed code values modified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-x12codelistvalidationrule.html#cfn-b2bi-transformer-x12codelistvalidationrule-elementid
            '''
            result = self._values.get("element_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "X12CodeListValidationRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_b2bi.mixins.CfnTransformerPropsMixin.X12DetailsProperty",
        jsii_struct_bases=[],
        name_mapping={"transaction_set": "transactionSet", "version": "version"},
    )
    class X12DetailsProperty:
        def __init__(
            self,
            *,
            transaction_set: typing.Optional[builtins.str] = None,
            version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure that contains the X12 transaction set and version.

            The X12 structure is used when the system transforms an EDI (electronic data interchange) file.
            .. epigraph::

               If an EDI input file contains more than one transaction, each transaction must have the same transaction set and version, for example 214/4010. If not, the transformer cannot parse the file.

            :param transaction_set: Returns an enumerated type where each value identifies an X12 transaction set. Transaction sets are maintained by the X12 Accredited Standards Committee.
            :param version: Returns the version to use for the specified X12 transaction set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-x12details.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_b2bi import mixins as b2bi_mixins
                
                x12_details_property = b2bi_mixins.CfnTransformerPropsMixin.X12DetailsProperty(
                    transaction_set="transactionSet",
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__60185b47e8f8f6eb1ef0a4038b70a1934b5db1540b520ed695fd786051245a72)
                check_type(argname="argument transaction_set", value=transaction_set, expected_type=type_hints["transaction_set"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if transaction_set is not None:
                self._values["transaction_set"] = transaction_set
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def transaction_set(self) -> typing.Optional[builtins.str]:
            '''Returns an enumerated type where each value identifies an X12 transaction set.

            Transaction sets are maintained by the X12 Accredited Standards Committee.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-x12details.html#cfn-b2bi-transformer-x12details-transactionset
            '''
            result = self._values.get("transaction_set")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''Returns the version to use for the specified X12 transaction set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-x12details.html#cfn-b2bi-transformer-x12details-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "X12DetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_b2bi.mixins.CfnTransformerPropsMixin.X12ElementLengthValidationRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "element_id": "elementId",
            "max_length": "maxLength",
            "min_length": "minLength",
        },
    )
    class X12ElementLengthValidationRuleProperty:
        def __init__(
            self,
            *,
            element_id: typing.Optional[builtins.str] = None,
            max_length: typing.Optional[jsii.Number] = None,
            min_length: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Defines a validation rule that specifies custom length constraints for a specific X12 element.

            This rule allows you to override the standard minimum and maximum length requirements for an element, enabling validation of trading partner-specific length requirements that may differ from the X12 specification. Both minimum and maximum length values must be specified.

            :param element_id: Specifies the four-digit element ID to which the length constraints will be applied. This identifies which X12 element will have its length requirements modified.
            :param max_length: Specifies the maximum allowed length for the identified element. This value defines the upper limit for the element's content length.
            :param min_length: Specifies the minimum required length for the identified element. This value defines the lower limit for the element's content length.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-x12elementlengthvalidationrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_b2bi import mixins as b2bi_mixins
                
                x12_element_length_validation_rule_property = b2bi_mixins.CfnTransformerPropsMixin.X12ElementLengthValidationRuleProperty(
                    element_id="elementId",
                    max_length=123,
                    min_length=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ace0f74726c1756fb60257bd813f851e803fa7d7b79c9dbf8236f56eee6cd3c3)
                check_type(argname="argument element_id", value=element_id, expected_type=type_hints["element_id"])
                check_type(argname="argument max_length", value=max_length, expected_type=type_hints["max_length"])
                check_type(argname="argument min_length", value=min_length, expected_type=type_hints["min_length"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if element_id is not None:
                self._values["element_id"] = element_id
            if max_length is not None:
                self._values["max_length"] = max_length
            if min_length is not None:
                self._values["min_length"] = min_length

        @builtins.property
        def element_id(self) -> typing.Optional[builtins.str]:
            '''Specifies the four-digit element ID to which the length constraints will be applied.

            This identifies which X12 element will have its length requirements modified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-x12elementlengthvalidationrule.html#cfn-b2bi-transformer-x12elementlengthvalidationrule-elementid
            '''
            result = self._values.get("element_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def max_length(self) -> typing.Optional[jsii.Number]:
            '''Specifies the maximum allowed length for the identified element.

            This value defines the upper limit for the element's content length.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-x12elementlengthvalidationrule.html#cfn-b2bi-transformer-x12elementlengthvalidationrule-maxlength
            '''
            result = self._values.get("max_length")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min_length(self) -> typing.Optional[jsii.Number]:
            '''Specifies the minimum required length for the identified element.

            This value defines the lower limit for the element's content length.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-x12elementlengthvalidationrule.html#cfn-b2bi-transformer-x12elementlengthvalidationrule-minlength
            '''
            result = self._values.get("min_length")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "X12ElementLengthValidationRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_b2bi.mixins.CfnTransformerPropsMixin.X12ElementRequirementValidationRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "element_position": "elementPosition",
            "requirement": "requirement",
        },
    )
    class X12ElementRequirementValidationRuleProperty:
        def __init__(
            self,
            *,
            element_position: typing.Optional[builtins.str] = None,
            requirement: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines a validation rule that modifies the requirement status of a specific X12 element within a segment.

            This rule allows you to make optional elements mandatory or mandatory elements optional, providing flexibility to accommodate different trading partner requirements and business rules. The rule targets a specific element position within a segment and sets its requirement status to either OPTIONAL or MANDATORY.

            :param element_position: Specifies the position of the element within an X12 segment for which the requirement status will be modified. The format follows the pattern of segment identifier followed by element position (e.g., "ST-01" for the first element of the ST segment).
            :param requirement: Specifies the requirement status for the element at the specified position. Valid values are OPTIONAL (the element may be omitted) or MANDATORY (the element must be present).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-x12elementrequirementvalidationrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_b2bi import mixins as b2bi_mixins
                
                x12_element_requirement_validation_rule_property = b2bi_mixins.CfnTransformerPropsMixin.X12ElementRequirementValidationRuleProperty(
                    element_position="elementPosition",
                    requirement="requirement"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f74ce594b1e1b21895c3d9567b2d26c4a89dfe335c177d208f8690e0129732b1)
                check_type(argname="argument element_position", value=element_position, expected_type=type_hints["element_position"])
                check_type(argname="argument requirement", value=requirement, expected_type=type_hints["requirement"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if element_position is not None:
                self._values["element_position"] = element_position
            if requirement is not None:
                self._values["requirement"] = requirement

        @builtins.property
        def element_position(self) -> typing.Optional[builtins.str]:
            '''Specifies the position of the element within an X12 segment for which the requirement status will be modified.

            The format follows the pattern of segment identifier followed by element position (e.g., "ST-01" for the first element of the ST segment).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-x12elementrequirementvalidationrule.html#cfn-b2bi-transformer-x12elementrequirementvalidationrule-elementposition
            '''
            result = self._values.get("element_position")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def requirement(self) -> typing.Optional[builtins.str]:
            '''Specifies the requirement status for the element at the specified position.

            Valid values are OPTIONAL (the element may be omitted) or MANDATORY (the element must be present).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-x12elementrequirementvalidationrule.html#cfn-b2bi-transformer-x12elementrequirementvalidationrule-requirement
            '''
            result = self._values.get("requirement")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "X12ElementRequirementValidationRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_b2bi.mixins.CfnTransformerPropsMixin.X12SplitOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"split_by": "splitBy"},
    )
    class X12SplitOptionsProperty:
        def __init__(self, *, split_by: typing.Optional[builtins.str] = None) -> None:
            '''Contains options for splitting X12 EDI files into smaller units.

            This is useful for processing large EDI files more efficiently.

            :param split_by: Specifies the method used to split X12 EDI files. Valid values include ``TRANSACTION`` (split by individual transaction sets), or ``NONE`` (no splitting).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-x12splitoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_b2bi import mixins as b2bi_mixins
                
                x12_split_options_property = b2bi_mixins.CfnTransformerPropsMixin.X12SplitOptionsProperty(
                    split_by="splitBy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__60a0457d05b697e4f2fc9ee3f52796a3043b4d2895f9ffba0f85f177664f4491)
                check_type(argname="argument split_by", value=split_by, expected_type=type_hints["split_by"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if split_by is not None:
                self._values["split_by"] = split_by

        @builtins.property
        def split_by(self) -> typing.Optional[builtins.str]:
            '''Specifies the method used to split X12 EDI files.

            Valid values include ``TRANSACTION`` (split by individual transaction sets), or ``NONE`` (no splitting).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-x12splitoptions.html#cfn-b2bi-transformer-x12splitoptions-splitby
            '''
            result = self._values.get("split_by")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "X12SplitOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_b2bi.mixins.CfnTransformerPropsMixin.X12ValidationOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"validation_rules": "validationRules"},
    )
    class X12ValidationOptionsProperty:
        def __init__(
            self,
            *,
            validation_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.X12ValidationRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Contains configuration options for X12 EDI validation.

            This structure allows you to specify custom validation rules that will be applied during EDI document processing, including element length constraints, code list modifications, and element requirement changes. These validation options provide flexibility to accommodate trading partner-specific requirements while maintaining EDI compliance. The validation rules are applied in addition to standard X12 validation to ensure documents meet both standard and custom requirements.

            :param validation_rules: Specifies a list of validation rules to apply during EDI document processing. These rules can include code list modifications, element length constraints, and element requirement changes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-x12validationoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_b2bi import mixins as b2bi_mixins
                
                x12_validation_options_property = b2bi_mixins.CfnTransformerPropsMixin.X12ValidationOptionsProperty(
                    validation_rules=[b2bi_mixins.CfnTransformerPropsMixin.X12ValidationRuleProperty(
                        code_list_validation_rule=b2bi_mixins.CfnTransformerPropsMixin.X12CodeListValidationRuleProperty(
                            codes_to_add=["codesToAdd"],
                            codes_to_remove=["codesToRemove"],
                            element_id="elementId"
                        ),
                        element_length_validation_rule=b2bi_mixins.CfnTransformerPropsMixin.X12ElementLengthValidationRuleProperty(
                            element_id="elementId",
                            max_length=123,
                            min_length=123
                        ),
                        element_requirement_validation_rule=b2bi_mixins.CfnTransformerPropsMixin.X12ElementRequirementValidationRuleProperty(
                            element_position="elementPosition",
                            requirement="requirement"
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d0287d05b7d2aa1fec7540b35064ed5cf53de479d0b0fc1168a30cd1c1895d6e)
                check_type(argname="argument validation_rules", value=validation_rules, expected_type=type_hints["validation_rules"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if validation_rules is not None:
                self._values["validation_rules"] = validation_rules

        @builtins.property
        def validation_rules(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.X12ValidationRuleProperty"]]]]:
            '''Specifies a list of validation rules to apply during EDI document processing.

            These rules can include code list modifications, element length constraints, and element requirement changes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-x12validationoptions.html#cfn-b2bi-transformer-x12validationoptions-validationrules
            '''
            result = self._values.get("validation_rules")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.X12ValidationRuleProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "X12ValidationOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_b2bi.mixins.CfnTransformerPropsMixin.X12ValidationRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "code_list_validation_rule": "codeListValidationRule",
            "element_length_validation_rule": "elementLengthValidationRule",
            "element_requirement_validation_rule": "elementRequirementValidationRule",
        },
    )
    class X12ValidationRuleProperty:
        def __init__(
            self,
            *,
            code_list_validation_rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.X12CodeListValidationRuleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            element_length_validation_rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.X12ElementLengthValidationRuleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            element_requirement_validation_rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.X12ElementRequirementValidationRuleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Represents a single validation rule that can be applied during X12 EDI processing.

            This is a union type that can contain one of several specific validation rule types: code list validation rules for modifying allowed element codes, element length validation rules for enforcing custom length constraints, or element requirement validation rules for changing mandatory/optional status. Each validation rule targets specific aspects of EDI document validation to ensure compliance with trading partner requirements and business rules.

            :param code_list_validation_rule: Specifies a code list validation rule that modifies the allowed code values for a specific X12 element. This rule enables you to customize which codes are considered valid for an element, allowing for trading partner-specific code requirements.
            :param element_length_validation_rule: Specifies an element length validation rule that defines custom length constraints for a specific X12 element. This rule allows you to enforce minimum and maximum length requirements that may differ from the standard X12 specification.
            :param element_requirement_validation_rule: Specifies an element requirement validation rule that modifies whether a specific X12 element is required or optional within a segment. This rule provides flexibility to accommodate different trading partner requirements for element presence.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-x12validationrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_b2bi import mixins as b2bi_mixins
                
                x12_validation_rule_property = b2bi_mixins.CfnTransformerPropsMixin.X12ValidationRuleProperty(
                    code_list_validation_rule=b2bi_mixins.CfnTransformerPropsMixin.X12CodeListValidationRuleProperty(
                        codes_to_add=["codesToAdd"],
                        codes_to_remove=["codesToRemove"],
                        element_id="elementId"
                    ),
                    element_length_validation_rule=b2bi_mixins.CfnTransformerPropsMixin.X12ElementLengthValidationRuleProperty(
                        element_id="elementId",
                        max_length=123,
                        min_length=123
                    ),
                    element_requirement_validation_rule=b2bi_mixins.CfnTransformerPropsMixin.X12ElementRequirementValidationRuleProperty(
                        element_position="elementPosition",
                        requirement="requirement"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e5950c72304c54a9368884fc95f5588830195a2d53c76cee79a488bf28e6d306)
                check_type(argname="argument code_list_validation_rule", value=code_list_validation_rule, expected_type=type_hints["code_list_validation_rule"])
                check_type(argname="argument element_length_validation_rule", value=element_length_validation_rule, expected_type=type_hints["element_length_validation_rule"])
                check_type(argname="argument element_requirement_validation_rule", value=element_requirement_validation_rule, expected_type=type_hints["element_requirement_validation_rule"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if code_list_validation_rule is not None:
                self._values["code_list_validation_rule"] = code_list_validation_rule
            if element_length_validation_rule is not None:
                self._values["element_length_validation_rule"] = element_length_validation_rule
            if element_requirement_validation_rule is not None:
                self._values["element_requirement_validation_rule"] = element_requirement_validation_rule

        @builtins.property
        def code_list_validation_rule(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.X12CodeListValidationRuleProperty"]]:
            '''Specifies a code list validation rule that modifies the allowed code values for a specific X12 element.

            This rule enables you to customize which codes are considered valid for an element, allowing for trading partner-specific code requirements.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-x12validationrule.html#cfn-b2bi-transformer-x12validationrule-codelistvalidationrule
            '''
            result = self._values.get("code_list_validation_rule")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.X12CodeListValidationRuleProperty"]], result)

        @builtins.property
        def element_length_validation_rule(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.X12ElementLengthValidationRuleProperty"]]:
            '''Specifies an element length validation rule that defines custom length constraints for a specific X12 element.

            This rule allows you to enforce minimum and maximum length requirements that may differ from the standard X12 specification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-x12validationrule.html#cfn-b2bi-transformer-x12validationrule-elementlengthvalidationrule
            '''
            result = self._values.get("element_length_validation_rule")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.X12ElementLengthValidationRuleProperty"]], result)

        @builtins.property
        def element_requirement_validation_rule(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.X12ElementRequirementValidationRuleProperty"]]:
            '''Specifies an element requirement validation rule that modifies whether a specific X12 element is required or optional within a segment.

            This rule provides flexibility to accommodate different trading partner requirements for element presence.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-b2bi-transformer-x12validationrule.html#cfn-b2bi-transformer-x12validationrule-elementrequirementvalidationrule
            '''
            result = self._values.get("element_requirement_validation_rule")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.X12ElementRequirementValidationRuleProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "X12ValidationRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnCapabilityMixinProps",
    "CfnCapabilityPropsMixin",
    "CfnPartnershipMixinProps",
    "CfnPartnershipPropsMixin",
    "CfnProfileMixinProps",
    "CfnProfilePropsMixin",
    "CfnTransformerB2biExecutionLogs",
    "CfnTransformerLogsMixin",
    "CfnTransformerMixinProps",
    "CfnTransformerPropsMixin",
]

publication.publish()

def _typecheckingstub__dce9aca7b56830b8d70b8da41b731edab28ce419a8a49c235f2cc0fd5643ffda(
    *,
    configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCapabilityPropsMixin.CapabilityConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    instructions_documents: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCapabilityPropsMixin.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35d034b3ec61d31e902579638ba75dbc3d0b5be8b2acfd81e35609e8889d2e99(
    props: typing.Union[CfnCapabilityMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a39687d9d6f7fea3063bffec9d0b6810aabd81dca1e18f407198df65364b4b9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d9cb4db8aad84e68aa3ded3a687acae65ae994a536311dc2743bbf877d2b095(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07f4fe6f786f716906f55216151655d975837a17006622fddb63ddce3a58b30c(
    *,
    edi: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCapabilityPropsMixin.EdiConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6db49fa4bf41a35876584c803c3f863ce7a3128787e986fe0ab14198840f2928(
    *,
    capability_direction: typing.Optional[builtins.str] = None,
    input_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCapabilityPropsMixin.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    output_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCapabilityPropsMixin.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    transformer_id: typing.Optional[builtins.str] = None,
    type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCapabilityPropsMixin.EdiTypeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4a5968b6812b36ba00ddf6ad26d5988861e150c652ea518958da96f1a9397f4(
    *,
    x12_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCapabilityPropsMixin.X12DetailsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d5c22e56c407e45985642888fd2ad0df2eafc6da563993031a707306346e927(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9042dd5f7af45302ad3970d80f730c4a3f9209aeb8d6b5ad96c27a580cfda2e(
    *,
    transaction_set: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8901d41f818f4201c5757adf696cccad27ccee9deab42badc7199427919b96cc(
    *,
    capabilities: typing.Optional[typing.Sequence[builtins.str]] = None,
    capability_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPartnershipPropsMixin.CapabilityOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    email: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    phone: typing.Optional[builtins.str] = None,
    profile_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4be908f6cc44b8659e34f1cf861a9e93fa8fd6f897164f38ed9e2157ee85d3c(
    props: typing.Union[CfnPartnershipMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__084bf1941ce36849245e0c5ce486b00e59893dbbccea076347b91b29c715d2d3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9204e83393f6b13c2507168754e578e97e182d69781a5fa3f8bddb3e4b26eca0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__847eced0fd08ab251eb1207df8f34934835e51bdb332854a5503d84447749b7e(
    *,
    inbound_edi: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPartnershipPropsMixin.InboundEdiOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    outbound_edi: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPartnershipPropsMixin.OutboundEdiOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af1fa34e48c90f45a20336ef1c9005aa89b55d638abf6ac833307ed7e0857680(
    *,
    x12: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPartnershipPropsMixin.X12InboundEdiOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__536954209d9dbcfbb5b414169b471990002c5699f25b3b248bbe16abf88a51f1(
    *,
    x12: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPartnershipPropsMixin.X12EnvelopeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ede0729bb401813ab4ca6034dd6d10881ac5d0ad1886fc42824be9f507e6afb(
    *,
    line_length: typing.Optional[jsii.Number] = None,
    line_terminator: typing.Optional[builtins.str] = None,
    wrap_by: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afee50d24b583699fa6670b03b62f2e6f4bed730cb28b3c94aa8abf7c71fce14(
    *,
    functional_acknowledgment: typing.Optional[builtins.str] = None,
    technical_acknowledgment: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2de771d93ba7c0e797ce0ddcc7fb6eb568f82f6da8fb77c13ea8ef8d958fb2c9(
    *,
    starting_functional_group_control_number: typing.Optional[jsii.Number] = None,
    starting_interchange_control_number: typing.Optional[jsii.Number] = None,
    starting_transaction_set_control_number: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da5b863b333408043ebf55c3775e6043b5a9a03247445a8f6f7d129ddb04d180(
    *,
    component_separator: typing.Optional[builtins.str] = None,
    data_element_separator: typing.Optional[builtins.str] = None,
    segment_terminator: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeda8ef09642ee25c3440486b236b3c952fa37522bb7d25a7053159d7cef247b(
    *,
    common: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPartnershipPropsMixin.X12OutboundEdiHeadersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    wrap_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPartnershipPropsMixin.WrapOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f338bf82501a0b33b728a496c5cdf09cead195a794ca5ec693c7376e70bfe69(
    *,
    application_receiver_code: typing.Optional[builtins.str] = None,
    application_sender_code: typing.Optional[builtins.str] = None,
    responsible_agency_code: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26ed6672cf4c94b27965ca050d73a7eaa48433741051e73d2cd971bd671494e5(
    *,
    acknowledgment_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPartnershipPropsMixin.X12AcknowledgmentOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53f97ab1cdeae73a40eb360c14ed44bc065e61e43c3fbbc8473548853343f752(
    *,
    acknowledgment_requested_code: typing.Optional[builtins.str] = None,
    receiver_id: typing.Optional[builtins.str] = None,
    receiver_id_qualifier: typing.Optional[builtins.str] = None,
    repetition_separator: typing.Optional[builtins.str] = None,
    sender_id: typing.Optional[builtins.str] = None,
    sender_id_qualifier: typing.Optional[builtins.str] = None,
    usage_indicator_code: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1733a0a6210b67ad85c7912db4328b4d8fdbc1a4ad0ea2de97917067bc48741(
    *,
    control_numbers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPartnershipPropsMixin.X12ControlNumbersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    delimiters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPartnershipPropsMixin.X12DelimitersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    functional_group_headers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPartnershipPropsMixin.X12FunctionalGroupHeadersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    gs05_time_format: typing.Optional[builtins.str] = None,
    interchange_control_headers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPartnershipPropsMixin.X12InterchangeControlHeadersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    validate_edi: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2edd4778b6933db650b826d90509e3181a65fb5a08f9ccd8e4d9ac0f5d334109(
    *,
    business_name: typing.Optional[builtins.str] = None,
    email: typing.Optional[builtins.str] = None,
    logging: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    phone: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c08f57e36c1042b4df06075b9da2473ed3989c12029055370b342d8afd23ece5(
    props: typing.Union[CfnProfileMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cf9c8541dfa3e81dd20f252afb3abc4fe3799389e04f59f71f46fca3a3a5b2e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3928225f970ef0f08144d846cdd063de1b0cee49b75c8ed2470db96c4e988b31(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16408e4028bc631211cd0bccd9bf8215bc9815c503f3c25f7d34d1c7c79caab6(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92a63bb5b5864afd941042e5700224ec7f642532427283446d3d5d4a79b6b9be(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03e8b9e23c076b760ad21e3ae66aec97e2ec7e299c9371649d11151522c73da6(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49e1205091e695f161a3b12f1acea77e61be1376c4a0bc172c3380485a9e122c(
    log_type: builtins.str,
    log_delivery: _ILogsDelivery_0d3c9e29,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dca4d57bb764d1e55be99a7cf3ba898fcbe2f684eb44945e17e27ebc384d7018(
    resource: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6608ce7fc657ee3fd2a3e7bac5f1867eebf1fb635b5a1880a8cb920a6a4b0f5(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c41eddd4788c420ee51aa348a0716316facde41557d8d7617831ca6a1058172(
    *,
    edi_type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.EdiTypeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    file_format: typing.Optional[builtins.str] = None,
    input_conversion: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.InputConversionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    mapping: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.MappingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    mapping_template: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    output_conversion: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.OutputConversionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sample_document: typing.Optional[builtins.str] = None,
    sample_documents: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.SampleDocumentsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2572390f2c49c4d247f7ec5f283de9ca993ab5212da3d3087e00abeff633c80(
    props: typing.Union[CfnTransformerMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c61ea097e78bb7bc6c1333cc4d612feaa5591f6f07755688b0870d70e3822a30(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2955ed91d7b227ae3583d40bea68d2f67e83f1ebd644c21c6b9e76f589a6661b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b01ba66cc5c8be9aacab05c48a6d19ab1eba19e0d3851e6e68cd62d28fc1f85(
    *,
    x12: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.X12AdvancedOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22522d308c9bdd06ba9f05f33d780765a9beab79f1dcc7b78ec14b6e4115117f(
    *,
    x12_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.X12DetailsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd308b9f36b92838587381b3051af45896cbf66722173b10184ef1122f1f852a(
    *,
    x12: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.X12DetailsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9541172c4126bd0ac1f2ef317cdf5fd25f23f60d9a7dc87fb303c9b7360c56b7(
    *,
    advanced_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.AdvancedOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    format_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.FormatOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    from_format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56e2db1fa32f4fde3b13288c103715e3be43ea80170f1c00fbfb5be1da341dec(
    *,
    template: typing.Optional[builtins.str] = None,
    template_language: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__214910fc8aefbc361d91ce143bea47e4a0622a42103c0709ef91221a61730367(
    *,
    advanced_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.AdvancedOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    format_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.FormatOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    to_format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e462f759900f7c87eb45dfcf7cfdbbb8cf671b6bb458532145393381f63bc4df(
    *,
    input: typing.Optional[builtins.str] = None,
    output: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d1c823b5edabc55200ae3df4d24271746964a2484ad336cc7e98424f44df934(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    keys: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.SampleDocumentKeysProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a256fd2f3d893f4d641923c73ad19921910b07af726adfee37d589d53662a851(
    *,
    split_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.X12SplitOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    validation_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.X12ValidationOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d537f5a25a4e686a0dda2c99f1bda25a51b8e53bdeb0d83836631aa6a68547f8(
    *,
    codes_to_add: typing.Optional[typing.Sequence[builtins.str]] = None,
    codes_to_remove: typing.Optional[typing.Sequence[builtins.str]] = None,
    element_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60185b47e8f8f6eb1ef0a4038b70a1934b5db1540b520ed695fd786051245a72(
    *,
    transaction_set: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ace0f74726c1756fb60257bd813f851e803fa7d7b79c9dbf8236f56eee6cd3c3(
    *,
    element_id: typing.Optional[builtins.str] = None,
    max_length: typing.Optional[jsii.Number] = None,
    min_length: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f74ce594b1e1b21895c3d9567b2d26c4a89dfe335c177d208f8690e0129732b1(
    *,
    element_position: typing.Optional[builtins.str] = None,
    requirement: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60a0457d05b697e4f2fc9ee3f52796a3043b4d2895f9ffba0f85f177664f4491(
    *,
    split_by: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0287d05b7d2aa1fec7540b35064ed5cf53de479d0b0fc1168a30cd1c1895d6e(
    *,
    validation_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.X12ValidationRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5950c72304c54a9368884fc95f5588830195a2d53c76cee79a488bf28e6d306(
    *,
    code_list_validation_rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.X12CodeListValidationRuleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    element_length_validation_rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.X12ElementLengthValidationRuleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    element_requirement_validation_rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.X12ElementRequirementValidationRuleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
