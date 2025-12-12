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
    jsii_type="@aws-cdk/mixins-preview.aws_s3vectors.mixins.CfnIndexMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "data_type": "dataType",
        "dimension": "dimension",
        "distance_metric": "distanceMetric",
        "index_name": "indexName",
        "metadata_configuration": "metadataConfiguration",
        "vector_bucket_arn": "vectorBucketArn",
        "vector_bucket_name": "vectorBucketName",
    },
)
class CfnIndexMixinProps:
    def __init__(
        self,
        *,
        data_type: typing.Optional[builtins.str] = None,
        dimension: typing.Optional[jsii.Number] = None,
        distance_metric: typing.Optional[builtins.str] = None,
        index_name: typing.Optional[builtins.str] = None,
        metadata_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIndexPropsMixin.MetadataConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        vector_bucket_arn: typing.Optional[builtins.str] = None,
        vector_bucket_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnIndexPropsMixin.

        :param data_type: The data type of the vectors to be inserted into the vector index. Currently, only ``float32`` is supported, which represents 32-bit floating-point numbers.
        :param dimension: The dimensions of the vectors to be inserted into the vector index. This value must be between 1 and 4096, inclusive. All vectors stored in the index must have the same number of dimensions. The dimension value affects the storage requirements and search performance. Higher dimensions require more storage space and may impact search latency.
        :param distance_metric: The distance metric to be used for similarity search. Valid values are:. - ``cosine`` - Measures the cosine of the angle between two vectors. - ``euclidean`` - Measures the straight-line distance between two points in multi-dimensional space. Lower values indicate greater similarity.
        :param index_name: The name of the vector index to create. The index name must be between 3 and 63 characters long and can contain only lowercase letters, numbers, hyphens (-), and dots (.). The index name must be unique within the vector bucket. If you don't specify a name, AWS CloudFormation generates a unique ID and uses that ID for the index name. .. epigraph:: If you specify a name, you can't perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you need to replace the resource, specify a new name.
        :param metadata_configuration: The metadata configuration for the vector index.
        :param vector_bucket_arn: The Amazon Resource Name (ARN) of the vector bucket that contains the vector index.
        :param vector_bucket_name: The name of the vector bucket that contains the vector index.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3vectors-index.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_s3vectors import mixins as s3vectors_mixins
            
            cfn_index_mixin_props = s3vectors_mixins.CfnIndexMixinProps(
                data_type="dataType",
                dimension=123,
                distance_metric="distanceMetric",
                index_name="indexName",
                metadata_configuration=s3vectors_mixins.CfnIndexPropsMixin.MetadataConfigurationProperty(
                    non_filterable_metadata_keys=["nonFilterableMetadataKeys"]
                ),
                vector_bucket_arn="vectorBucketArn",
                vector_bucket_name="vectorBucketName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__960ae119e0f2da97dd595889e579ed9d8a454385fd48bb4d4a34aeffe9783111)
            check_type(argname="argument data_type", value=data_type, expected_type=type_hints["data_type"])
            check_type(argname="argument dimension", value=dimension, expected_type=type_hints["dimension"])
            check_type(argname="argument distance_metric", value=distance_metric, expected_type=type_hints["distance_metric"])
            check_type(argname="argument index_name", value=index_name, expected_type=type_hints["index_name"])
            check_type(argname="argument metadata_configuration", value=metadata_configuration, expected_type=type_hints["metadata_configuration"])
            check_type(argname="argument vector_bucket_arn", value=vector_bucket_arn, expected_type=type_hints["vector_bucket_arn"])
            check_type(argname="argument vector_bucket_name", value=vector_bucket_name, expected_type=type_hints["vector_bucket_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data_type is not None:
            self._values["data_type"] = data_type
        if dimension is not None:
            self._values["dimension"] = dimension
        if distance_metric is not None:
            self._values["distance_metric"] = distance_metric
        if index_name is not None:
            self._values["index_name"] = index_name
        if metadata_configuration is not None:
            self._values["metadata_configuration"] = metadata_configuration
        if vector_bucket_arn is not None:
            self._values["vector_bucket_arn"] = vector_bucket_arn
        if vector_bucket_name is not None:
            self._values["vector_bucket_name"] = vector_bucket_name

    @builtins.property
    def data_type(self) -> typing.Optional[builtins.str]:
        '''The data type of the vectors to be inserted into the vector index.

        Currently, only ``float32`` is supported, which represents 32-bit floating-point numbers.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3vectors-index.html#cfn-s3vectors-index-datatype
        '''
        result = self._values.get("data_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dimension(self) -> typing.Optional[jsii.Number]:
        '''The dimensions of the vectors to be inserted into the vector index.

        This value must be between 1 and 4096, inclusive. All vectors stored in the index must have the same number of dimensions.

        The dimension value affects the storage requirements and search performance. Higher dimensions require more storage space and may impact search latency.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3vectors-index.html#cfn-s3vectors-index-dimension
        '''
        result = self._values.get("dimension")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def distance_metric(self) -> typing.Optional[builtins.str]:
        '''The distance metric to be used for similarity search. Valid values are:.

        - ``cosine`` - Measures the cosine of the angle between two vectors.
        - ``euclidean`` - Measures the straight-line distance between two points in multi-dimensional space. Lower values indicate greater similarity.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3vectors-index.html#cfn-s3vectors-index-distancemetric
        '''
        result = self._values.get("distance_metric")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def index_name(self) -> typing.Optional[builtins.str]:
        '''The name of the vector index to create.

        The index name must be between 3 and 63 characters long and can contain only lowercase letters, numbers, hyphens (-), and dots (.). The index name must be unique within the vector bucket.

        If you don't specify a name, AWS CloudFormation generates a unique ID and uses that ID for the index name.
        .. epigraph::

           If you specify a name, you can't perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you need to replace the resource, specify a new name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3vectors-index.html#cfn-s3vectors-index-indexname
        '''
        result = self._values.get("index_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metadata_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIndexPropsMixin.MetadataConfigurationProperty"]]:
        '''The metadata configuration for the vector index.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3vectors-index.html#cfn-s3vectors-index-metadataconfiguration
        '''
        result = self._values.get("metadata_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIndexPropsMixin.MetadataConfigurationProperty"]], result)

    @builtins.property
    def vector_bucket_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the vector bucket that contains the vector index.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3vectors-index.html#cfn-s3vectors-index-vectorbucketarn
        '''
        result = self._values.get("vector_bucket_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vector_bucket_name(self) -> typing.Optional[builtins.str]:
        '''The name of the vector bucket that contains the vector index.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3vectors-index.html#cfn-s3vectors-index-vectorbucketname
        '''
        result = self._values.get("vector_bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIndexMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnIndexPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_s3vectors.mixins.CfnIndexPropsMixin",
):
    '''The ``AWS::S3Vectors::Index`` resource defines a vector index within an Amazon S3 vector bucket.

    For more information, see `Creating a vector index in a vector bucket <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-create-index.html>`_ in the *Amazon Simple Storage Service User Guide* .

    You must specify either ``VectorBucketName`` or ``VectorBucketArn`` to identify the bucket that contains the index.

    To control how AWS CloudFormation handles the vector index when the stack is deleted, you can set a deletion policy for your index. You can choose to *retain* the index or to *delete* the index. For more information, see `DeletionPolicy attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-deletionpolicy.html>`_ .

    - **Permissions** - The required permissions for CloudFormation to use are based on the operations that are performed on the stack.
    - Create
    - s3vectors:CreateIndex
    - s3vectors:GetIndex
    - Read
    - s3vectors:GetIndex
    - Delete
    - s3vectors:DeleteIndex
    - s3vectors:GetIndex
    - List
    - s3vectors:ListIndexes

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3vectors-index.html
    :cloudformationResource: AWS::S3Vectors::Index
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_s3vectors import mixins as s3vectors_mixins
        
        cfn_index_props_mixin = s3vectors_mixins.CfnIndexPropsMixin(s3vectors_mixins.CfnIndexMixinProps(
            data_type="dataType",
            dimension=123,
            distance_metric="distanceMetric",
            index_name="indexName",
            metadata_configuration=s3vectors_mixins.CfnIndexPropsMixin.MetadataConfigurationProperty(
                non_filterable_metadata_keys=["nonFilterableMetadataKeys"]
            ),
            vector_bucket_arn="vectorBucketArn",
            vector_bucket_name="vectorBucketName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnIndexMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::S3Vectors::Index``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__690afe9340310cdd3d17c8405113fc6defa9fef6a580abc86d550dc292ee6f45)
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
            type_hints = typing.get_type_hints(_typecheckingstub__63fdc0d8b1fbb63086e60cb9faa06d1d2b4a80929fbe6a80917573e7910b653f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb3f9b274ae8897ce5d0ab9602c65710b484034abace8699b40b0632913175e4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnIndexMixinProps:
        return typing.cast(CfnIndexMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3vectors.mixins.CfnIndexPropsMixin.MetadataConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"non_filterable_metadata_keys": "nonFilterableMetadataKeys"},
    )
    class MetadataConfigurationProperty:
        def __init__(
            self,
            *,
            non_filterable_metadata_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The metadata configuration for the vector index.

            This configuration allows you to specify which metadata keys should be treated as non-filterable.

            :param non_filterable_metadata_keys: Non-filterable metadata keys allow you to enrich vectors with additional context during storage and retrieval. Unlike default metadata keys, these keys can't be used as query filters. Non-filterable metadata keys can be retrieved but can't be searched, queried, or filtered. You can access non-filterable metadata keys of your vectors after finding the vectors. You can specify 1 to 10 non-filterable metadata keys. Each key must be 1 to 63 characters long.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3vectors-index-metadataconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3vectors import mixins as s3vectors_mixins
                
                metadata_configuration_property = s3vectors_mixins.CfnIndexPropsMixin.MetadataConfigurationProperty(
                    non_filterable_metadata_keys=["nonFilterableMetadataKeys"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d1017c547f56c250f6412b8fc5f89fd9281645540834cf89552848f094f63a7c)
                check_type(argname="argument non_filterable_metadata_keys", value=non_filterable_metadata_keys, expected_type=type_hints["non_filterable_metadata_keys"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if non_filterable_metadata_keys is not None:
                self._values["non_filterable_metadata_keys"] = non_filterable_metadata_keys

        @builtins.property
        def non_filterable_metadata_keys(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''Non-filterable metadata keys allow you to enrich vectors with additional context during storage and retrieval.

            Unlike default metadata keys, these keys can't be used as query filters. Non-filterable metadata keys can be retrieved but can't be searched, queried, or filtered. You can access non-filterable metadata keys of your vectors after finding the vectors.

            You can specify 1 to 10 non-filterable metadata keys. Each key must be 1 to 63 characters long.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3vectors-index-metadataconfiguration.html#cfn-s3vectors-index-metadataconfiguration-nonfilterablemetadatakeys
            '''
            result = self._values.get("non_filterable_metadata_keys")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetadataConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_s3vectors.mixins.CfnVectorBucketMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "encryption_configuration": "encryptionConfiguration",
        "vector_bucket_name": "vectorBucketName",
    },
)
class CfnVectorBucketMixinProps:
    def __init__(
        self,
        *,
        encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVectorBucketPropsMixin.EncryptionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        vector_bucket_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnVectorBucketPropsMixin.

        :param encryption_configuration: The encryption configuration for the vector bucket.
        :param vector_bucket_name: A name for the vector bucket. The bucket name must contain only lowercase letters, numbers, and hyphens (-). The bucket name must be unique in the same AWS account for each AWS Region. If you don't specify a name, AWS CloudFormation generates a unique ID and uses that ID for the bucket name. The bucket name must be between 3 and 63 characters long and must not contain uppercase characters or underscores. .. epigraph:: If you specify a name, you can't perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you need to replace the resource, specify a new name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3vectors-vectorbucket.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_s3vectors import mixins as s3vectors_mixins
            
            cfn_vector_bucket_mixin_props = s3vectors_mixins.CfnVectorBucketMixinProps(
                encryption_configuration=s3vectors_mixins.CfnVectorBucketPropsMixin.EncryptionConfigurationProperty(
                    kms_key_arn="kmsKeyArn",
                    sse_type="sseType"
                ),
                vector_bucket_name="vectorBucketName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69bd4c725192e5b7137418d437f412e43d75cc01d4ac0d55dfd4980a3c7345f8)
            check_type(argname="argument encryption_configuration", value=encryption_configuration, expected_type=type_hints["encryption_configuration"])
            check_type(argname="argument vector_bucket_name", value=vector_bucket_name, expected_type=type_hints["vector_bucket_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if encryption_configuration is not None:
            self._values["encryption_configuration"] = encryption_configuration
        if vector_bucket_name is not None:
            self._values["vector_bucket_name"] = vector_bucket_name

    @builtins.property
    def encryption_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVectorBucketPropsMixin.EncryptionConfigurationProperty"]]:
        '''The encryption configuration for the vector bucket.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3vectors-vectorbucket.html#cfn-s3vectors-vectorbucket-encryptionconfiguration
        '''
        result = self._values.get("encryption_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVectorBucketPropsMixin.EncryptionConfigurationProperty"]], result)

    @builtins.property
    def vector_bucket_name(self) -> typing.Optional[builtins.str]:
        '''A name for the vector bucket.

        The bucket name must contain only lowercase letters, numbers, and hyphens (-). The bucket name must be unique in the same AWS account for each AWS Region. If you don't specify a name, AWS CloudFormation generates a unique ID and uses that ID for the bucket name.

        The bucket name must be between 3 and 63 characters long and must not contain uppercase characters or underscores.
        .. epigraph::

           If you specify a name, you can't perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you need to replace the resource, specify a new name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3vectors-vectorbucket.html#cfn-s3vectors-vectorbucket-vectorbucketname
        '''
        result = self._values.get("vector_bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVectorBucketMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_s3vectors.mixins.CfnVectorBucketPolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "policy": "policy",
        "vector_bucket_arn": "vectorBucketArn",
        "vector_bucket_name": "vectorBucketName",
    },
)
class CfnVectorBucketPolicyMixinProps:
    def __init__(
        self,
        *,
        policy: typing.Any = None,
        vector_bucket_arn: typing.Optional[builtins.str] = None,
        vector_bucket_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnVectorBucketPolicyPropsMixin.

        :param policy: A policy document containing permissions to add to the specified vector bucket. In IAM , you must provide policy documents in JSON format. However, in CloudFormation you can provide the policy in JSON or YAML format because CloudFormation converts YAML to JSON before submitting it to IAM .
        :param vector_bucket_arn: The Amazon Resource Name (ARN) of the S3 vector bucket to which the policy applies.
        :param vector_bucket_name: The name of the S3 vector bucket to which the policy applies.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3vectors-vectorbucketpolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_s3vectors import mixins as s3vectors_mixins
            
            # policy: Any
            
            cfn_vector_bucket_policy_mixin_props = s3vectors_mixins.CfnVectorBucketPolicyMixinProps(
                policy=policy,
                vector_bucket_arn="vectorBucketArn",
                vector_bucket_name="vectorBucketName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bf8470ba8bb868dfa395e51b2a444b9bfb581f17100c77f13d6da5071eb8eaa)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument vector_bucket_arn", value=vector_bucket_arn, expected_type=type_hints["vector_bucket_arn"])
            check_type(argname="argument vector_bucket_name", value=vector_bucket_name, expected_type=type_hints["vector_bucket_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if policy is not None:
            self._values["policy"] = policy
        if vector_bucket_arn is not None:
            self._values["vector_bucket_arn"] = vector_bucket_arn
        if vector_bucket_name is not None:
            self._values["vector_bucket_name"] = vector_bucket_name

    @builtins.property
    def policy(self) -> typing.Any:
        '''A policy document containing permissions to add to the specified vector bucket.

        In IAM , you must provide policy documents in JSON format. However, in CloudFormation you can provide the policy in JSON or YAML format because CloudFormation converts YAML to JSON before submitting it to IAM .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3vectors-vectorbucketpolicy.html#cfn-s3vectors-vectorbucketpolicy-policy
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def vector_bucket_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the S3 vector bucket to which the policy applies.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3vectors-vectorbucketpolicy.html#cfn-s3vectors-vectorbucketpolicy-vectorbucketarn
        '''
        result = self._values.get("vector_bucket_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vector_bucket_name(self) -> typing.Optional[builtins.str]:
        '''The name of the S3 vector bucket to which the policy applies.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3vectors-vectorbucketpolicy.html#cfn-s3vectors-vectorbucketpolicy-vectorbucketname
        '''
        result = self._values.get("vector_bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVectorBucketPolicyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnVectorBucketPolicyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_s3vectors.mixins.CfnVectorBucketPolicyPropsMixin",
):
    '''The ``AWS::S3Vectors::VectorBucketPolicy`` resource defines an Amazon S3 vector bucket policy to control access to an Amazon S3 vector bucket.

    Vector bucket policies are written in JSON and allow you to grant or deny permissions across all (or a subset of) objects within a vector bucket.

    You must specify either ``VectorBucketName`` or ``VectorBucketArn`` to identify the target bucket.

    To control how AWS CloudFormation handles the vector bucket policy when the stack is deleted, you can set a deletion policy for your policy. You can choose to *retain* the policy or to *delete* the policy. For more information, see `DeletionPolicy attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-deletionpolicy.html>`_ .

    - **Permissions** - The required permissions for CloudFormation to use are based on the operations that are performed on the stack.
    - Create
    - s3vectors:GetVectorBucketPolicy
    - s3vectors:PutVectorBucketPolicy
    - Read
    - s3vectors:GetVectorBucketPolicy
    - Update
    - s3vectors:GetVectorBucketPolicy
    - s3vectors:PutVectorBucketPolicy
    - Delete
    - s3vectors:GetVectorBucketPolicy
    - s3vectors:DeleteVectorBucketPolicy
    - List
    - s3vectors:GetVectorBucketPolicy
    - s3vectors:ListVectorBuckets

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3vectors-vectorbucketpolicy.html
    :cloudformationResource: AWS::S3Vectors::VectorBucketPolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_s3vectors import mixins as s3vectors_mixins
        
        # policy: Any
        
        cfn_vector_bucket_policy_props_mixin = s3vectors_mixins.CfnVectorBucketPolicyPropsMixin(s3vectors_mixins.CfnVectorBucketPolicyMixinProps(
            policy=policy,
            vector_bucket_arn="vectorBucketArn",
            vector_bucket_name="vectorBucketName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnVectorBucketPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::S3Vectors::VectorBucketPolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__594bc53c58286a94f1a265d28aece327023dedf0493d67d97db61879c7155946)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c171a731b7bb2a675e509fbdf6716fcc70ca7281d09a8840b67c7f0d482a69a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1477ec6ac9a95977a2e202d1107fb95e26efa92047c8a78f9370ff3deff5a3dd)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnVectorBucketPolicyMixinProps:
        return typing.cast(CfnVectorBucketPolicyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.implements(_IMixin_11e4b965)
class CfnVectorBucketPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_s3vectors.mixins.CfnVectorBucketPropsMixin",
):
    '''Defines an Amazon S3 vector bucket in the same AWS Region where you create the AWS CloudFormation stack.

    Vector buckets are specialized storage containers designed for storing and managing vector data used in machine learning and AI applications. They provide optimized storage and retrieval capabilities for high-dimensional vector data.

    To control how AWS CloudFormation handles the bucket when the stack is deleted, you can set a deletion policy for your bucket. You can choose to *retain* the bucket or to *delete* the bucket. For more information, see `DeletionPolicy attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-deletionpolicy.html>`_ .
    .. epigraph::

       You can only delete empty vector buckets. Deletion fails for buckets that have contents.

    - **Permissions** - The required permissions for CloudFormation to use are based on the operations that are performed on the stack.
    - Create
    - s3vectors:CreateVectorBucket
    - s3vectors:GetVectorBucket
    - kms:GenerateDataKey (if using KMS encryption)
    - Read
    - s3vectors:GetVectorBucket
    - kms:GenerateDataKey (if using KMS encryption)
    - Delete
    - s3vectors:DeleteVectorBucket
    - s3vectors:GetVectorBucket
    - kms:GenerateDataKey (if using KMS encryption)
    - List
    - s3vectors:ListVectorBuckets
    - kms:GenerateDataKey (if using KMS encryption)

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3vectors-vectorbucket.html
    :cloudformationResource: AWS::S3Vectors::VectorBucket
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_s3vectors import mixins as s3vectors_mixins
        
        cfn_vector_bucket_props_mixin = s3vectors_mixins.CfnVectorBucketPropsMixin(s3vectors_mixins.CfnVectorBucketMixinProps(
            encryption_configuration=s3vectors_mixins.CfnVectorBucketPropsMixin.EncryptionConfigurationProperty(
                kms_key_arn="kmsKeyArn",
                sse_type="sseType"
            ),
            vector_bucket_name="vectorBucketName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnVectorBucketMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::S3Vectors::VectorBucket``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5738e6ac745d02c3c90a0aa94354d3e8dee23131420bfbe9c25e1234eec3d15b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a93ebfe7e83b5e0cfdb3fac60336ad4656c72a5dc0417fbf132751794dc8adeb)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d53cb9cf557cce0aa46d1f3ced0c6402b410dbfe56f33e9bf414e42be5d8ee4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnVectorBucketMixinProps:
        return typing.cast(CfnVectorBucketMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3vectors.mixins.CfnVectorBucketPropsMixin.EncryptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"kms_key_arn": "kmsKeyArn", "sse_type": "sseType"},
    )
    class EncryptionConfigurationProperty:
        def __init__(
            self,
            *,
            kms_key_arn: typing.Optional[builtins.str] = None,
            sse_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the encryption configuration for the vector bucket.

            By default, all new vectors in Amazon S3 vector buckets use server-side encryption with Amazon S3 managed keys (SSE-S3), specifically AES256.

            :param kms_key_arn: AWS Key Management Service (KMS) customer managed key ARN to use for the encryption configuration. This parameter is required if and only if ``SseType`` is set to ``aws:kms`` . You must specify the full ARN of the KMS key. Key IDs or key aliases aren't supported. .. epigraph:: Amazon S3 Vectors only supports symmetric encryption KMS keys. For more information, see `Asymmetric keys in AWS KMS <https://docs.aws.amazon.com//kms/latest/developerguide/symmetric-asymmetric.html>`_ in the *AWS Key Management Service Developer Guide* .
            :param sse_type: The server-side encryption type to use for the encryption configuration of the vector bucket. Valid values are ``AES256`` for Amazon S3 managed keys and ``aws:kms`` for AWS KMS keys. Default: - "AES256"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3vectors-vectorbucket-encryptionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3vectors import mixins as s3vectors_mixins
                
                encryption_configuration_property = s3vectors_mixins.CfnVectorBucketPropsMixin.EncryptionConfigurationProperty(
                    kms_key_arn="kmsKeyArn",
                    sse_type="sseType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b0ed5926433a415594ae711ba53689e42f67af40b857fce7fc4d8629e1a7bb5b)
                check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
                check_type(argname="argument sse_type", value=sse_type, expected_type=type_hints["sse_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kms_key_arn is not None:
                self._values["kms_key_arn"] = kms_key_arn
            if sse_type is not None:
                self._values["sse_type"] = sse_type

        @builtins.property
        def kms_key_arn(self) -> typing.Optional[builtins.str]:
            '''AWS Key Management Service (KMS) customer managed key ARN to use for the encryption configuration.

            This parameter is required if and only if ``SseType`` is set to ``aws:kms`` .

            You must specify the full ARN of the KMS key. Key IDs or key aliases aren't supported.
            .. epigraph::

               Amazon S3 Vectors only supports symmetric encryption KMS keys. For more information, see `Asymmetric keys in AWS KMS <https://docs.aws.amazon.com//kms/latest/developerguide/symmetric-asymmetric.html>`_ in the *AWS Key Management Service Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3vectors-vectorbucket-encryptionconfiguration.html#cfn-s3vectors-vectorbucket-encryptionconfiguration-kmskeyarn
            '''
            result = self._values.get("kms_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sse_type(self) -> typing.Optional[builtins.str]:
            '''The server-side encryption type to use for the encryption configuration of the vector bucket.

            Valid values are ``AES256`` for Amazon S3 managed keys and ``aws:kms`` for AWS KMS keys.

            :default: - "AES256"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3vectors-vectorbucket-encryptionconfiguration.html#cfn-s3vectors-vectorbucket-encryptionconfiguration-ssetype
            '''
            result = self._values.get("sse_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnIndexMixinProps",
    "CfnIndexPropsMixin",
    "CfnVectorBucketMixinProps",
    "CfnVectorBucketPolicyMixinProps",
    "CfnVectorBucketPolicyPropsMixin",
    "CfnVectorBucketPropsMixin",
]

publication.publish()

def _typecheckingstub__960ae119e0f2da97dd595889e579ed9d8a454385fd48bb4d4a34aeffe9783111(
    *,
    data_type: typing.Optional[builtins.str] = None,
    dimension: typing.Optional[jsii.Number] = None,
    distance_metric: typing.Optional[builtins.str] = None,
    index_name: typing.Optional[builtins.str] = None,
    metadata_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIndexPropsMixin.MetadataConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    vector_bucket_arn: typing.Optional[builtins.str] = None,
    vector_bucket_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__690afe9340310cdd3d17c8405113fc6defa9fef6a580abc86d550dc292ee6f45(
    props: typing.Union[CfnIndexMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63fdc0d8b1fbb63086e60cb9faa06d1d2b4a80929fbe6a80917573e7910b653f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb3f9b274ae8897ce5d0ab9602c65710b484034abace8699b40b0632913175e4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1017c547f56c250f6412b8fc5f89fd9281645540834cf89552848f094f63a7c(
    *,
    non_filterable_metadata_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69bd4c725192e5b7137418d437f412e43d75cc01d4ac0d55dfd4980a3c7345f8(
    *,
    encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVectorBucketPropsMixin.EncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    vector_bucket_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bf8470ba8bb868dfa395e51b2a444b9bfb581f17100c77f13d6da5071eb8eaa(
    *,
    policy: typing.Any = None,
    vector_bucket_arn: typing.Optional[builtins.str] = None,
    vector_bucket_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__594bc53c58286a94f1a265d28aece327023dedf0493d67d97db61879c7155946(
    props: typing.Union[CfnVectorBucketPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c171a731b7bb2a675e509fbdf6716fcc70ca7281d09a8840b67c7f0d482a69a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1477ec6ac9a95977a2e202d1107fb95e26efa92047c8a78f9370ff3deff5a3dd(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5738e6ac745d02c3c90a0aa94354d3e8dee23131420bfbe9c25e1234eec3d15b(
    props: typing.Union[CfnVectorBucketMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a93ebfe7e83b5e0cfdb3fac60336ad4656c72a5dc0417fbf132751794dc8adeb(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d53cb9cf557cce0aa46d1f3ced0c6402b410dbfe56f33e9bf414e42be5d8ee4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0ed5926433a415594ae711ba53689e42f67af40b857fce7fc4d8629e1a7bb5b(
    *,
    kms_key_arn: typing.Optional[builtins.str] = None,
    sse_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
