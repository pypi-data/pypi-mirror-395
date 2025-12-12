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
    jsii_type="@aws-cdk/mixins-preview.aws_comprehend.mixins.CfnDocumentClassifierMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "data_access_role_arn": "dataAccessRoleArn",
        "document_classifier_name": "documentClassifierName",
        "input_data_config": "inputDataConfig",
        "language_code": "languageCode",
        "mode": "mode",
        "model_kms_key_id": "modelKmsKeyId",
        "model_policy": "modelPolicy",
        "output_data_config": "outputDataConfig",
        "tags": "tags",
        "version_name": "versionName",
        "volume_kms_key_id": "volumeKmsKeyId",
        "vpc_config": "vpcConfig",
    },
)
class CfnDocumentClassifierMixinProps:
    def __init__(
        self,
        *,
        data_access_role_arn: typing.Optional[builtins.str] = None,
        document_classifier_name: typing.Optional[builtins.str] = None,
        input_data_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDocumentClassifierPropsMixin.DocumentClassifierInputDataConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        language_code: typing.Optional[builtins.str] = None,
        mode: typing.Optional[builtins.str] = None,
        model_kms_key_id: typing.Optional[builtins.str] = None,
        model_policy: typing.Optional[builtins.str] = None,
        output_data_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDocumentClassifierPropsMixin.DocumentClassifierOutputDataConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        version_name: typing.Optional[builtins.str] = None,
        volume_kms_key_id: typing.Optional[builtins.str] = None,
        vpc_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDocumentClassifierPropsMixin.VpcConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDocumentClassifierPropsMixin.

        :param data_access_role_arn: The Amazon Resource Name (ARN) of the IAM role that grants Amazon Comprehend read access to your input data.
        :param document_classifier_name: The name of the document classifier.
        :param input_data_config: Specifies the format and location of the input data for the job.
        :param language_code: The language of the input documents. You can specify any of the languages supported by Amazon Comprehend. All documents must be in the same language.
        :param mode: Indicates the mode in which the classifier will be trained. The classifier can be trained in multi-class (single-label) mode or multi-label mode. Multi-class mode identifies a single class label for each document and multi-label mode identifies one or more class labels for each document. Multiple labels for an individual document are separated by a delimiter. The default delimiter between labels is a pipe (|).
        :param model_kms_key_id: ID for the AWS key that Amazon Comprehend uses to encrypt trained custom models. The ModelKmsKeyId can be either of the following formats: - KMS Key ID: ``"1234abcd-12ab-34cd-56ef-1234567890ab"`` - Amazon Resource Name (ARN) of a KMS Key: ``"arn:aws:kms:us-west-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab"``
        :param model_policy: The resource-based policy to attach to your custom document classifier model. You can use this policy to allow another AWS account to import your custom model. Provide your policy as a JSON body that you enter as a UTF-8 encoded string without line breaks. To provide valid JSON, enclose the attribute names and values in double quotes. If the JSON body is also enclosed in double quotes, then you must escape the double quotes that are inside the policy: ``"{\\"attribute\\": \\"value\\", \\"attribute\\": [\\"value\\"]}"`` To avoid escaping quotes, you can use single quotes to enclose the policy and double quotes to enclose the JSON names and values: ``'{"attribute": "value", "attribute": ["value"]}'``
        :param output_data_config: Provides output results configuration parameters for custom classifier jobs.
        :param tags: Tags to associate with the document classifier. A tag is a key-value pair that adds as a metadata to a resource used by Amazon Comprehend. For example, a tag with "Sales" as the key might be added to a resource to indicate its use by the sales department.
        :param version_name: The version name given to the newly created classifier. Version names can have a maximum of 256 characters. Alphanumeric characters, hyphens (-) and underscores (_) are allowed. The version name must be unique among all models with the same classifier name in the AWS account / AWS Region .
        :param volume_kms_key_id: ID for the AWS Key Management Service (KMS) key that Amazon Comprehend uses to encrypt data on the storage volume attached to the ML compute instance(s) that process the analysis job. The VolumeKmsKeyId can be either of the following formats: - KMS Key ID: ``"1234abcd-12ab-34cd-56ef-1234567890ab"`` - Amazon Resource Name (ARN) of a KMS Key: ``"arn:aws:kms:us-west-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab"``
        :param vpc_config: Configuration parameters for a private Virtual Private Cloud (VPC) containing the resources you are using for your custom classifier. For more information, see `Amazon VPC <https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-comprehend-documentclassifier.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_comprehend import mixins as comprehend_mixins
            
            cfn_document_classifier_mixin_props = comprehend_mixins.CfnDocumentClassifierMixinProps(
                data_access_role_arn="dataAccessRoleArn",
                document_classifier_name="documentClassifierName",
                input_data_config=comprehend_mixins.CfnDocumentClassifierPropsMixin.DocumentClassifierInputDataConfigProperty(
                    augmented_manifests=[comprehend_mixins.CfnDocumentClassifierPropsMixin.AugmentedManifestsListItemProperty(
                        attribute_names=["attributeNames"],
                        s3_uri="s3Uri",
                        split="split"
                    )],
                    data_format="dataFormat",
                    document_reader_config=comprehend_mixins.CfnDocumentClassifierPropsMixin.DocumentReaderConfigProperty(
                        document_read_action="documentReadAction",
                        document_read_mode="documentReadMode",
                        feature_types=["featureTypes"]
                    ),
                    documents=comprehend_mixins.CfnDocumentClassifierPropsMixin.DocumentClassifierDocumentsProperty(
                        s3_uri="s3Uri",
                        test_s3_uri="testS3Uri"
                    ),
                    document_type="documentType",
                    label_delimiter="labelDelimiter",
                    s3_uri="s3Uri",
                    test_s3_uri="testS3Uri"
                ),
                language_code="languageCode",
                mode="mode",
                model_kms_key_id="modelKmsKeyId",
                model_policy="modelPolicy",
                output_data_config=comprehend_mixins.CfnDocumentClassifierPropsMixin.DocumentClassifierOutputDataConfigProperty(
                    kms_key_id="kmsKeyId",
                    s3_uri="s3Uri"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                version_name="versionName",
                volume_kms_key_id="volumeKmsKeyId",
                vpc_config=comprehend_mixins.CfnDocumentClassifierPropsMixin.VpcConfigProperty(
                    security_group_ids=["securityGroupIds"],
                    subnets=["subnets"]
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc3a17ab812d4b57d244ac6f4632fb7cc793fc399d79c192735e179081ed25f5)
            check_type(argname="argument data_access_role_arn", value=data_access_role_arn, expected_type=type_hints["data_access_role_arn"])
            check_type(argname="argument document_classifier_name", value=document_classifier_name, expected_type=type_hints["document_classifier_name"])
            check_type(argname="argument input_data_config", value=input_data_config, expected_type=type_hints["input_data_config"])
            check_type(argname="argument language_code", value=language_code, expected_type=type_hints["language_code"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument model_kms_key_id", value=model_kms_key_id, expected_type=type_hints["model_kms_key_id"])
            check_type(argname="argument model_policy", value=model_policy, expected_type=type_hints["model_policy"])
            check_type(argname="argument output_data_config", value=output_data_config, expected_type=type_hints["output_data_config"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument version_name", value=version_name, expected_type=type_hints["version_name"])
            check_type(argname="argument volume_kms_key_id", value=volume_kms_key_id, expected_type=type_hints["volume_kms_key_id"])
            check_type(argname="argument vpc_config", value=vpc_config, expected_type=type_hints["vpc_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data_access_role_arn is not None:
            self._values["data_access_role_arn"] = data_access_role_arn
        if document_classifier_name is not None:
            self._values["document_classifier_name"] = document_classifier_name
        if input_data_config is not None:
            self._values["input_data_config"] = input_data_config
        if language_code is not None:
            self._values["language_code"] = language_code
        if mode is not None:
            self._values["mode"] = mode
        if model_kms_key_id is not None:
            self._values["model_kms_key_id"] = model_kms_key_id
        if model_policy is not None:
            self._values["model_policy"] = model_policy
        if output_data_config is not None:
            self._values["output_data_config"] = output_data_config
        if tags is not None:
            self._values["tags"] = tags
        if version_name is not None:
            self._values["version_name"] = version_name
        if volume_kms_key_id is not None:
            self._values["volume_kms_key_id"] = volume_kms_key_id
        if vpc_config is not None:
            self._values["vpc_config"] = vpc_config

    @builtins.property
    def data_access_role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the IAM role that grants Amazon Comprehend read access to your input data.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-comprehend-documentclassifier.html#cfn-comprehend-documentclassifier-dataaccessrolearn
        '''
        result = self._values.get("data_access_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def document_classifier_name(self) -> typing.Optional[builtins.str]:
        '''The name of the document classifier.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-comprehend-documentclassifier.html#cfn-comprehend-documentclassifier-documentclassifiername
        '''
        result = self._values.get("document_classifier_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def input_data_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDocumentClassifierPropsMixin.DocumentClassifierInputDataConfigProperty"]]:
        '''Specifies the format and location of the input data for the job.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-comprehend-documentclassifier.html#cfn-comprehend-documentclassifier-inputdataconfig
        '''
        result = self._values.get("input_data_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDocumentClassifierPropsMixin.DocumentClassifierInputDataConfigProperty"]], result)

    @builtins.property
    def language_code(self) -> typing.Optional[builtins.str]:
        '''The language of the input documents.

        You can specify any of the languages supported by Amazon Comprehend. All documents must be in the same language.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-comprehend-documentclassifier.html#cfn-comprehend-documentclassifier-languagecode
        '''
        result = self._values.get("language_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Indicates the mode in which the classifier will be trained.

        The classifier can be trained in multi-class (single-label) mode or multi-label mode. Multi-class mode identifies a single class label for each document and multi-label mode identifies one or more class labels for each document. Multiple labels for an individual document are separated by a delimiter. The default delimiter between labels is a pipe (|).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-comprehend-documentclassifier.html#cfn-comprehend-documentclassifier-mode
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def model_kms_key_id(self) -> typing.Optional[builtins.str]:
        '''ID for the AWS  key that Amazon Comprehend uses to encrypt trained custom models.

        The ModelKmsKeyId can be either of the following formats:

        - KMS Key ID: ``"1234abcd-12ab-34cd-56ef-1234567890ab"``
        - Amazon Resource Name (ARN) of a KMS Key: ``"arn:aws:kms:us-west-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab"``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-comprehend-documentclassifier.html#cfn-comprehend-documentclassifier-modelkmskeyid
        '''
        result = self._values.get("model_kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def model_policy(self) -> typing.Optional[builtins.str]:
        '''The resource-based policy to attach to your custom document classifier model.

        You can use this policy to allow another AWS account to import your custom model.

        Provide your policy as a JSON body that you enter as a UTF-8 encoded string without line breaks. To provide valid JSON, enclose the attribute names and values in double quotes. If the JSON body is also enclosed in double quotes, then you must escape the double quotes that are inside the policy:

        ``"{\\"attribute\\": \\"value\\", \\"attribute\\": [\\"value\\"]}"``

        To avoid escaping quotes, you can use single quotes to enclose the policy and double quotes to enclose the JSON names and values:

        ``'{"attribute": "value", "attribute": ["value"]}'``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-comprehend-documentclassifier.html#cfn-comprehend-documentclassifier-modelpolicy
        '''
        result = self._values.get("model_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output_data_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDocumentClassifierPropsMixin.DocumentClassifierOutputDataConfigProperty"]]:
        '''Provides output results configuration parameters for custom classifier jobs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-comprehend-documentclassifier.html#cfn-comprehend-documentclassifier-outputdataconfig
        '''
        result = self._values.get("output_data_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDocumentClassifierPropsMixin.DocumentClassifierOutputDataConfigProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Tags to associate with the document classifier.

        A tag is a key-value pair that adds as a metadata to a resource used by Amazon Comprehend. For example, a tag with "Sales" as the key might be added to a resource to indicate its use by the sales department.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-comprehend-documentclassifier.html#cfn-comprehend-documentclassifier-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def version_name(self) -> typing.Optional[builtins.str]:
        '''The version name given to the newly created classifier.

        Version names can have a maximum of 256 characters. Alphanumeric characters, hyphens (-) and underscores (_) are allowed. The version name must be unique among all models with the same classifier name in the AWS account / AWS Region .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-comprehend-documentclassifier.html#cfn-comprehend-documentclassifier-versionname
        '''
        result = self._values.get("version_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def volume_kms_key_id(self) -> typing.Optional[builtins.str]:
        '''ID for the AWS Key Management Service (KMS) key that Amazon Comprehend uses to encrypt data on the storage volume attached to the ML compute instance(s) that process the analysis job.

        The VolumeKmsKeyId can be either of the following formats:

        - KMS Key ID: ``"1234abcd-12ab-34cd-56ef-1234567890ab"``
        - Amazon Resource Name (ARN) of a KMS Key: ``"arn:aws:kms:us-west-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab"``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-comprehend-documentclassifier.html#cfn-comprehend-documentclassifier-volumekmskeyid
        '''
        result = self._values.get("volume_kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDocumentClassifierPropsMixin.VpcConfigProperty"]]:
        '''Configuration parameters for a private Virtual Private Cloud (VPC) containing the resources you are using for your custom classifier.

        For more information, see `Amazon VPC <https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-comprehend-documentclassifier.html#cfn-comprehend-documentclassifier-vpcconfig
        '''
        result = self._values.get("vpc_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDocumentClassifierPropsMixin.VpcConfigProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDocumentClassifierMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDocumentClassifierPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_comprehend.mixins.CfnDocumentClassifierPropsMixin",
):
    '''This resource creates and trains a document classifier to categorize documents.

    You provide a set of training documents that are labeled with the categories that you want to identify. After the classifier is trained you can use it to categorize a set of labeled documents into the categories. For more information, see `Document Classification <https://docs.aws.amazon.com/comprehend/latest/dg/how-document-classification.html>`_ in the Comprehend Developer Guide.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-comprehend-documentclassifier.html
    :cloudformationResource: AWS::Comprehend::DocumentClassifier
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_comprehend import mixins as comprehend_mixins
        
        cfn_document_classifier_props_mixin = comprehend_mixins.CfnDocumentClassifierPropsMixin(comprehend_mixins.CfnDocumentClassifierMixinProps(
            data_access_role_arn="dataAccessRoleArn",
            document_classifier_name="documentClassifierName",
            input_data_config=comprehend_mixins.CfnDocumentClassifierPropsMixin.DocumentClassifierInputDataConfigProperty(
                augmented_manifests=[comprehend_mixins.CfnDocumentClassifierPropsMixin.AugmentedManifestsListItemProperty(
                    attribute_names=["attributeNames"],
                    s3_uri="s3Uri",
                    split="split"
                )],
                data_format="dataFormat",
                document_reader_config=comprehend_mixins.CfnDocumentClassifierPropsMixin.DocumentReaderConfigProperty(
                    document_read_action="documentReadAction",
                    document_read_mode="documentReadMode",
                    feature_types=["featureTypes"]
                ),
                documents=comprehend_mixins.CfnDocumentClassifierPropsMixin.DocumentClassifierDocumentsProperty(
                    s3_uri="s3Uri",
                    test_s3_uri="testS3Uri"
                ),
                document_type="documentType",
                label_delimiter="labelDelimiter",
                s3_uri="s3Uri",
                test_s3_uri="testS3Uri"
            ),
            language_code="languageCode",
            mode="mode",
            model_kms_key_id="modelKmsKeyId",
            model_policy="modelPolicy",
            output_data_config=comprehend_mixins.CfnDocumentClassifierPropsMixin.DocumentClassifierOutputDataConfigProperty(
                kms_key_id="kmsKeyId",
                s3_uri="s3Uri"
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            version_name="versionName",
            volume_kms_key_id="volumeKmsKeyId",
            vpc_config=comprehend_mixins.CfnDocumentClassifierPropsMixin.VpcConfigProperty(
                security_group_ids=["securityGroupIds"],
                subnets=["subnets"]
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDocumentClassifierMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Comprehend::DocumentClassifier``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb1f4b953355999ccb398fb17d65cf81067fa905f0352969e5b08d56a85ef8dd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__14557a9874e622c857c2aed15cf00b09d5cef28a43b13ec0e1fe77ce96682227)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b57304ba28bd9bf57921f71649ad64b462dfe55d31db7ccc9dd6bb09fd435f8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDocumentClassifierMixinProps:
        return typing.cast(CfnDocumentClassifierMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_comprehend.mixins.CfnDocumentClassifierPropsMixin.AugmentedManifestsListItemProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attribute_names": "attributeNames",
            "s3_uri": "s3Uri",
            "split": "split",
        },
    )
    class AugmentedManifestsListItemProperty:
        def __init__(
            self,
            *,
            attribute_names: typing.Optional[typing.Sequence[builtins.str]] = None,
            s3_uri: typing.Optional[builtins.str] = None,
            split: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An augmented manifest file that provides training data for your custom model.

            An augmented manifest file is a labeled dataset that is produced by Amazon SageMaker Ground Truth.

            :param attribute_names: The JSON attribute that contains the annotations for your training documents. The number of attribute names that you specify depends on whether your augmented manifest file is the output of a single labeling job or a chained labeling job. If your file is the output of a single labeling job, specify the LabelAttributeName key that was used when the job was created in Ground Truth. If your file is the output of a chained labeling job, specify the LabelAttributeName key for one or more jobs in the chain. Each LabelAttributeName key provides the annotations from an individual job.
            :param s3_uri: The Amazon S3 location of the augmented manifest file.
            :param split: The purpose of the data you've provided in the augmented manifest. You can either train or test this data. If you don't specify, the default is train. TRAIN - all of the documents in the manifest will be used for training. If no test documents are provided, Amazon Comprehend will automatically reserve a portion of the training documents for testing. TEST - all of the documents in the manifest will be used for testing.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-comprehend-documentclassifier-augmentedmanifestslistitem.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_comprehend import mixins as comprehend_mixins
                
                augmented_manifests_list_item_property = comprehend_mixins.CfnDocumentClassifierPropsMixin.AugmentedManifestsListItemProperty(
                    attribute_names=["attributeNames"],
                    s3_uri="s3Uri",
                    split="split"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b88b4edc438acadab0f532fe0b1b5ca2c663ff861d94029cab6073c84f70518b)
                check_type(argname="argument attribute_names", value=attribute_names, expected_type=type_hints["attribute_names"])
                check_type(argname="argument s3_uri", value=s3_uri, expected_type=type_hints["s3_uri"])
                check_type(argname="argument split", value=split, expected_type=type_hints["split"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attribute_names is not None:
                self._values["attribute_names"] = attribute_names
            if s3_uri is not None:
                self._values["s3_uri"] = s3_uri
            if split is not None:
                self._values["split"] = split

        @builtins.property
        def attribute_names(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The JSON attribute that contains the annotations for your training documents.

            The number of attribute names that you specify depends on whether your augmented manifest file is the output of a single labeling job or a chained labeling job.

            If your file is the output of a single labeling job, specify the LabelAttributeName key that was used when the job was created in Ground Truth.

            If your file is the output of a chained labeling job, specify the LabelAttributeName key for one or more jobs in the chain. Each LabelAttributeName key provides the annotations from an individual job.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-comprehend-documentclassifier-augmentedmanifestslistitem.html#cfn-comprehend-documentclassifier-augmentedmanifestslistitem-attributenames
            '''
            result = self._values.get("attribute_names")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def s3_uri(self) -> typing.Optional[builtins.str]:
            '''The Amazon S3 location of the augmented manifest file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-comprehend-documentclassifier-augmentedmanifestslistitem.html#cfn-comprehend-documentclassifier-augmentedmanifestslistitem-s3uri
            '''
            result = self._values.get("s3_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def split(self) -> typing.Optional[builtins.str]:
            '''The purpose of the data you've provided in the augmented manifest.

            You can either train or test this data. If you don't specify, the default is train.

            TRAIN - all of the documents in the manifest will be used for training. If no test documents are provided, Amazon Comprehend will automatically reserve a portion of the training documents for testing.

            TEST - all of the documents in the manifest will be used for testing.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-comprehend-documentclassifier-augmentedmanifestslistitem.html#cfn-comprehend-documentclassifier-augmentedmanifestslistitem-split
            '''
            result = self._values.get("split")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AugmentedManifestsListItemProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_comprehend.mixins.CfnDocumentClassifierPropsMixin.DocumentClassifierDocumentsProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_uri": "s3Uri", "test_s3_uri": "testS3Uri"},
    )
    class DocumentClassifierDocumentsProperty:
        def __init__(
            self,
            *,
            s3_uri: typing.Optional[builtins.str] = None,
            test_s3_uri: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The location of the training documents.

            This parameter is required in a request to create a semi-structured document classification model.

            :param s3_uri: The S3 URI location of the training documents specified in the S3Uri CSV file.
            :param test_s3_uri: The S3 URI location of the test documents included in the TestS3Uri CSV file. This field is not required if you do not specify a test CSV file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-comprehend-documentclassifier-documentclassifierdocuments.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_comprehend import mixins as comprehend_mixins
                
                document_classifier_documents_property = comprehend_mixins.CfnDocumentClassifierPropsMixin.DocumentClassifierDocumentsProperty(
                    s3_uri="s3Uri",
                    test_s3_uri="testS3Uri"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ac7910fd041b1311369f2ea8dcd35e9fb1cdce69c82e64a47a3e2e743b02896d)
                check_type(argname="argument s3_uri", value=s3_uri, expected_type=type_hints["s3_uri"])
                check_type(argname="argument test_s3_uri", value=test_s3_uri, expected_type=type_hints["test_s3_uri"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3_uri is not None:
                self._values["s3_uri"] = s3_uri
            if test_s3_uri is not None:
                self._values["test_s3_uri"] = test_s3_uri

        @builtins.property
        def s3_uri(self) -> typing.Optional[builtins.str]:
            '''The S3 URI location of the training documents specified in the S3Uri CSV file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-comprehend-documentclassifier-documentclassifierdocuments.html#cfn-comprehend-documentclassifier-documentclassifierdocuments-s3uri
            '''
            result = self._values.get("s3_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def test_s3_uri(self) -> typing.Optional[builtins.str]:
            '''The S3 URI location of the test documents included in the TestS3Uri CSV file.

            This field is not required if you do not specify a test CSV file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-comprehend-documentclassifier-documentclassifierdocuments.html#cfn-comprehend-documentclassifier-documentclassifierdocuments-tests3uri
            '''
            result = self._values.get("test_s3_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DocumentClassifierDocumentsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_comprehend.mixins.CfnDocumentClassifierPropsMixin.DocumentClassifierInputDataConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "augmented_manifests": "augmentedManifests",
            "data_format": "dataFormat",
            "document_reader_config": "documentReaderConfig",
            "documents": "documents",
            "document_type": "documentType",
            "label_delimiter": "labelDelimiter",
            "s3_uri": "s3Uri",
            "test_s3_uri": "testS3Uri",
        },
    )
    class DocumentClassifierInputDataConfigProperty:
        def __init__(
            self,
            *,
            augmented_manifests: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDocumentClassifierPropsMixin.AugmentedManifestsListItemProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            data_format: typing.Optional[builtins.str] = None,
            document_reader_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDocumentClassifierPropsMixin.DocumentReaderConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            documents: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDocumentClassifierPropsMixin.DocumentClassifierDocumentsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            document_type: typing.Optional[builtins.str] = None,
            label_delimiter: typing.Optional[builtins.str] = None,
            s3_uri: typing.Optional[builtins.str] = None,
            test_s3_uri: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The input properties for training a document classifier.

            For more information on how the input file is formatted, see `Preparing training data <https://docs.aws.amazon.com/comprehend/latest/dg/prep-classifier-data.html>`_ in the Comprehend Developer Guide.

            :param augmented_manifests: A list of augmented manifest files that provide training data for your custom model. An augmented manifest file is a labeled dataset that is produced by Amazon SageMaker Ground Truth. This parameter is required if you set ``DataFormat`` to ``AUGMENTED_MANIFEST`` .
            :param data_format: The format of your training data:. - ``COMPREHEND_CSV`` : A two-column CSV file, where labels are provided in the first column, and documents are provided in the second. If you use this value, you must provide the ``S3Uri`` parameter in your request. - ``AUGMENTED_MANIFEST`` : A labeled dataset that is produced by Amazon SageMaker Ground Truth. This file is in JSON lines format. Each line is a complete JSON object that contains a training document and its associated labels. If you use this value, you must provide the ``AugmentedManifests`` parameter in your request. If you don't specify a value, Amazon Comprehend uses ``COMPREHEND_CSV`` as the default.
            :param document_reader_config: 
            :param documents: The S3 location of the training documents. This parameter is required in a request to create a native document model.
            :param document_type: The type of input documents for training the model. Provide plain-text documents to create a plain-text model, and provide semi-structured documents to create a native document model.
            :param label_delimiter: Indicates the delimiter used to separate each label for training a multi-label classifier. The default delimiter between labels is a pipe (|). You can use a different character as a delimiter (if it's an allowed character) by specifying it under Delimiter for labels. If the training documents use a delimiter other than the default or the delimiter you specify, the labels on that line will be combined to make a single unique label, such as LABELLABELLABEL.
            :param s3_uri: The Amazon S3 URI for the input data. The S3 bucket must be in the same Region as the API endpoint that you are calling. The URI can point to a single input file or it can provide the prefix for a collection of input files. For example, if you use the URI ``S3://bucketName/prefix`` , if the prefix is a single file, Amazon Comprehend uses that file as input. If more than one file begins with the prefix, Amazon Comprehend uses all of them as input. This parameter is required if you set ``DataFormat`` to ``COMPREHEND_CSV`` .
            :param test_s3_uri: This specifies the Amazon S3 location that contains the test annotations for the document classifier. The URI must be in the same AWS Region as the API endpoint that you are calling.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-comprehend-documentclassifier-documentclassifierinputdataconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_comprehend import mixins as comprehend_mixins
                
                document_classifier_input_data_config_property = comprehend_mixins.CfnDocumentClassifierPropsMixin.DocumentClassifierInputDataConfigProperty(
                    augmented_manifests=[comprehend_mixins.CfnDocumentClassifierPropsMixin.AugmentedManifestsListItemProperty(
                        attribute_names=["attributeNames"],
                        s3_uri="s3Uri",
                        split="split"
                    )],
                    data_format="dataFormat",
                    document_reader_config=comprehend_mixins.CfnDocumentClassifierPropsMixin.DocumentReaderConfigProperty(
                        document_read_action="documentReadAction",
                        document_read_mode="documentReadMode",
                        feature_types=["featureTypes"]
                    ),
                    documents=comprehend_mixins.CfnDocumentClassifierPropsMixin.DocumentClassifierDocumentsProperty(
                        s3_uri="s3Uri",
                        test_s3_uri="testS3Uri"
                    ),
                    document_type="documentType",
                    label_delimiter="labelDelimiter",
                    s3_uri="s3Uri",
                    test_s3_uri="testS3Uri"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fd2db49bab8a4884a2fe378375bd9df65119a0f7d67a1567ab85c562d971ae7b)
                check_type(argname="argument augmented_manifests", value=augmented_manifests, expected_type=type_hints["augmented_manifests"])
                check_type(argname="argument data_format", value=data_format, expected_type=type_hints["data_format"])
                check_type(argname="argument document_reader_config", value=document_reader_config, expected_type=type_hints["document_reader_config"])
                check_type(argname="argument documents", value=documents, expected_type=type_hints["documents"])
                check_type(argname="argument document_type", value=document_type, expected_type=type_hints["document_type"])
                check_type(argname="argument label_delimiter", value=label_delimiter, expected_type=type_hints["label_delimiter"])
                check_type(argname="argument s3_uri", value=s3_uri, expected_type=type_hints["s3_uri"])
                check_type(argname="argument test_s3_uri", value=test_s3_uri, expected_type=type_hints["test_s3_uri"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if augmented_manifests is not None:
                self._values["augmented_manifests"] = augmented_manifests
            if data_format is not None:
                self._values["data_format"] = data_format
            if document_reader_config is not None:
                self._values["document_reader_config"] = document_reader_config
            if documents is not None:
                self._values["documents"] = documents
            if document_type is not None:
                self._values["document_type"] = document_type
            if label_delimiter is not None:
                self._values["label_delimiter"] = label_delimiter
            if s3_uri is not None:
                self._values["s3_uri"] = s3_uri
            if test_s3_uri is not None:
                self._values["test_s3_uri"] = test_s3_uri

        @builtins.property
        def augmented_manifests(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDocumentClassifierPropsMixin.AugmentedManifestsListItemProperty"]]]]:
            '''A list of augmented manifest files that provide training data for your custom model.

            An augmented manifest file is a labeled dataset that is produced by Amazon SageMaker Ground Truth.

            This parameter is required if you set ``DataFormat`` to ``AUGMENTED_MANIFEST`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-comprehend-documentclassifier-documentclassifierinputdataconfig.html#cfn-comprehend-documentclassifier-documentclassifierinputdataconfig-augmentedmanifests
            '''
            result = self._values.get("augmented_manifests")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDocumentClassifierPropsMixin.AugmentedManifestsListItemProperty"]]]], result)

        @builtins.property
        def data_format(self) -> typing.Optional[builtins.str]:
            '''The format of your training data:.

            - ``COMPREHEND_CSV`` : A two-column CSV file, where labels are provided in the first column, and documents are provided in the second. If you use this value, you must provide the ``S3Uri`` parameter in your request.
            - ``AUGMENTED_MANIFEST`` : A labeled dataset that is produced by Amazon SageMaker Ground Truth. This file is in JSON lines format. Each line is a complete JSON object that contains a training document and its associated labels.

            If you use this value, you must provide the ``AugmentedManifests`` parameter in your request.

            If you don't specify a value, Amazon Comprehend uses ``COMPREHEND_CSV`` as the default.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-comprehend-documentclassifier-documentclassifierinputdataconfig.html#cfn-comprehend-documentclassifier-documentclassifierinputdataconfig-dataformat
            '''
            result = self._values.get("data_format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def document_reader_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDocumentClassifierPropsMixin.DocumentReaderConfigProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-comprehend-documentclassifier-documentclassifierinputdataconfig.html#cfn-comprehend-documentclassifier-documentclassifierinputdataconfig-documentreaderconfig
            '''
            result = self._values.get("document_reader_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDocumentClassifierPropsMixin.DocumentReaderConfigProperty"]], result)

        @builtins.property
        def documents(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDocumentClassifierPropsMixin.DocumentClassifierDocumentsProperty"]]:
            '''The S3 location of the training documents.

            This parameter is required in a request to create a native document model.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-comprehend-documentclassifier-documentclassifierinputdataconfig.html#cfn-comprehend-documentclassifier-documentclassifierinputdataconfig-documents
            '''
            result = self._values.get("documents")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDocumentClassifierPropsMixin.DocumentClassifierDocumentsProperty"]], result)

        @builtins.property
        def document_type(self) -> typing.Optional[builtins.str]:
            '''The type of input documents for training the model.

            Provide plain-text documents to create a plain-text model, and provide semi-structured documents to create a native document model.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-comprehend-documentclassifier-documentclassifierinputdataconfig.html#cfn-comprehend-documentclassifier-documentclassifierinputdataconfig-documenttype
            '''
            result = self._values.get("document_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def label_delimiter(self) -> typing.Optional[builtins.str]:
            '''Indicates the delimiter used to separate each label for training a multi-label classifier.

            The default delimiter between labels is a pipe (|). You can use a different character as a delimiter (if it's an allowed character) by specifying it under Delimiter for labels. If the training documents use a delimiter other than the default or the delimiter you specify, the labels on that line will be combined to make a single unique label, such as LABELLABELLABEL.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-comprehend-documentclassifier-documentclassifierinputdataconfig.html#cfn-comprehend-documentclassifier-documentclassifierinputdataconfig-labeldelimiter
            '''
            result = self._values.get("label_delimiter")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_uri(self) -> typing.Optional[builtins.str]:
            '''The Amazon S3 URI for the input data.

            The S3 bucket must be in the same Region as the API endpoint that you are calling. The URI can point to a single input file or it can provide the prefix for a collection of input files.

            For example, if you use the URI ``S3://bucketName/prefix`` , if the prefix is a single file, Amazon Comprehend uses that file as input. If more than one file begins with the prefix, Amazon Comprehend uses all of them as input.

            This parameter is required if you set ``DataFormat`` to ``COMPREHEND_CSV`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-comprehend-documentclassifier-documentclassifierinputdataconfig.html#cfn-comprehend-documentclassifier-documentclassifierinputdataconfig-s3uri
            '''
            result = self._values.get("s3_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def test_s3_uri(self) -> typing.Optional[builtins.str]:
            '''This specifies the Amazon S3 location that contains the test annotations for the document classifier.

            The URI must be in the same AWS Region as the API endpoint that you are calling.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-comprehend-documentclassifier-documentclassifierinputdataconfig.html#cfn-comprehend-documentclassifier-documentclassifierinputdataconfig-tests3uri
            '''
            result = self._values.get("test_s3_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DocumentClassifierInputDataConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_comprehend.mixins.CfnDocumentClassifierPropsMixin.DocumentClassifierOutputDataConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"kms_key_id": "kmsKeyId", "s3_uri": "s3Uri"},
    )
    class DocumentClassifierOutputDataConfigProperty:
        def __init__(
            self,
            *,
            kms_key_id: typing.Optional[builtins.str] = None,
            s3_uri: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provide the location for output data from a custom classifier job.

            This field is mandatory if you are training a native document model.

            :param kms_key_id: ID for the AWS Key Management Service (KMS) key that Amazon Comprehend uses to encrypt the output results from an analysis job. The KmsKeyId can be one of the following formats: - KMS Key ID: ``"1234abcd-12ab-34cd-56ef-1234567890ab"`` - Amazon Resource Name (ARN) of a KMS Key: ``"arn:aws:kms:us-west-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab"`` - KMS Key Alias: ``"alias/ExampleAlias"`` - ARN of a KMS Key Alias: ``"arn:aws:kms:us-west-2:111122223333:alias/ExampleAlias"``
            :param s3_uri: When you use the ``OutputDataConfig`` object while creating a custom classifier, you specify the Amazon S3 location where you want to write the confusion matrix and other output files. The URI must be in the same Region as the API endpoint that you are calling. The location is used as the prefix for the actual location of this output file. When the custom classifier job is finished, the service creates the output file in a directory specific to the job. The ``S3Uri`` field contains the location of the output file, called ``output.tar.gz`` . It is a compressed archive that contains the confusion matrix.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-comprehend-documentclassifier-documentclassifieroutputdataconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_comprehend import mixins as comprehend_mixins
                
                document_classifier_output_data_config_property = comprehend_mixins.CfnDocumentClassifierPropsMixin.DocumentClassifierOutputDataConfigProperty(
                    kms_key_id="kmsKeyId",
                    s3_uri="s3Uri"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d1914fbbf9313205c8d60dded06983e779238cd1f302a6b741705552fb4bf2ee)
                check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
                check_type(argname="argument s3_uri", value=s3_uri, expected_type=type_hints["s3_uri"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kms_key_id is not None:
                self._values["kms_key_id"] = kms_key_id
            if s3_uri is not None:
                self._values["s3_uri"] = s3_uri

        @builtins.property
        def kms_key_id(self) -> typing.Optional[builtins.str]:
            '''ID for the AWS Key Management Service (KMS) key that Amazon Comprehend uses to encrypt the output results from an analysis job.

            The KmsKeyId can be one of the following formats:

            - KMS Key ID: ``"1234abcd-12ab-34cd-56ef-1234567890ab"``
            - Amazon Resource Name (ARN) of a KMS Key: ``"arn:aws:kms:us-west-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab"``
            - KMS Key Alias: ``"alias/ExampleAlias"``
            - ARN of a KMS Key Alias: ``"arn:aws:kms:us-west-2:111122223333:alias/ExampleAlias"``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-comprehend-documentclassifier-documentclassifieroutputdataconfig.html#cfn-comprehend-documentclassifier-documentclassifieroutputdataconfig-kmskeyid
            '''
            result = self._values.get("kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_uri(self) -> typing.Optional[builtins.str]:
            '''When you use the ``OutputDataConfig`` object while creating a custom classifier, you specify the Amazon S3 location where you want to write the confusion matrix and other output files.

            The URI must be in the same Region as the API endpoint that you are calling. The location is used as the prefix for the actual location of this output file.

            When the custom classifier job is finished, the service creates the output file in a directory specific to the job. The ``S3Uri`` field contains the location of the output file, called ``output.tar.gz`` . It is a compressed archive that contains the confusion matrix.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-comprehend-documentclassifier-documentclassifieroutputdataconfig.html#cfn-comprehend-documentclassifier-documentclassifieroutputdataconfig-s3uri
            '''
            result = self._values.get("s3_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DocumentClassifierOutputDataConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_comprehend.mixins.CfnDocumentClassifierPropsMixin.DocumentReaderConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "document_read_action": "documentReadAction",
            "document_read_mode": "documentReadMode",
            "feature_types": "featureTypes",
        },
    )
    class DocumentReaderConfigProperty:
        def __init__(
            self,
            *,
            document_read_action: typing.Optional[builtins.str] = None,
            document_read_mode: typing.Optional[builtins.str] = None,
            feature_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Provides configuration parameters to override the default actions for extracting text from PDF documents and image files.

            By default, Amazon Comprehend performs the following actions to extract text from files, based on the input file type:

            - *Word files* - Amazon Comprehend parser extracts the text.
            - *Digital PDF files* - Amazon Comprehend parser extracts the text.
            - *Image files and scanned PDF files* - Amazon Comprehend uses the Amazon Textract ``DetectDocumentText`` API to extract the text.

            ``DocumentReaderConfig`` does not apply to plain text files or Word files.

            For image files and PDF documents, you can override these default actions using the fields listed below. For more information, see `Setting text extraction options <https://docs.aws.amazon.com/comprehend/latest/dg/idp-set-textract-options.html>`_ in the Comprehend Developer Guide.

            :param document_read_action: This field defines the Amazon Textract API operation that Amazon Comprehend uses to extract text from PDF files and image files. Enter one of the following values: - ``TEXTRACT_DETECT_DOCUMENT_TEXT`` - The Amazon Comprehend service uses the ``DetectDocumentText`` API operation. - ``TEXTRACT_ANALYZE_DOCUMENT`` - The Amazon Comprehend service uses the ``AnalyzeDocument`` API operation.
            :param document_read_mode: Determines the text extraction actions for PDF files. Enter one of the following values:. - ``SERVICE_DEFAULT`` - use the Amazon Comprehend service defaults for PDF files. - ``FORCE_DOCUMENT_READ_ACTION`` - Amazon Comprehend uses the Textract API specified by DocumentReadAction for all PDF files, including digital PDF files.
            :param feature_types: Specifies the type of Amazon Textract features to apply. If you chose ``TEXTRACT_ANALYZE_DOCUMENT`` as the read action, you must specify one or both of the following values: - ``TABLES`` - Returns additional information about any tables that are detected in the input document. - ``FORMS`` - Returns additional information about any forms that are detected in the input document.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-comprehend-documentclassifier-documentreaderconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_comprehend import mixins as comprehend_mixins
                
                document_reader_config_property = comprehend_mixins.CfnDocumentClassifierPropsMixin.DocumentReaderConfigProperty(
                    document_read_action="documentReadAction",
                    document_read_mode="documentReadMode",
                    feature_types=["featureTypes"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__187ad126cd3d12bb6e4601dc6f1633408029cc47e38136d3580ac85cd77a3fef)
                check_type(argname="argument document_read_action", value=document_read_action, expected_type=type_hints["document_read_action"])
                check_type(argname="argument document_read_mode", value=document_read_mode, expected_type=type_hints["document_read_mode"])
                check_type(argname="argument feature_types", value=feature_types, expected_type=type_hints["feature_types"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if document_read_action is not None:
                self._values["document_read_action"] = document_read_action
            if document_read_mode is not None:
                self._values["document_read_mode"] = document_read_mode
            if feature_types is not None:
                self._values["feature_types"] = feature_types

        @builtins.property
        def document_read_action(self) -> typing.Optional[builtins.str]:
            '''This field defines the Amazon Textract API operation that Amazon Comprehend uses to extract text from PDF files and image files.

            Enter one of the following values:

            - ``TEXTRACT_DETECT_DOCUMENT_TEXT`` - The Amazon Comprehend service uses the ``DetectDocumentText`` API operation.
            - ``TEXTRACT_ANALYZE_DOCUMENT`` - The Amazon Comprehend service uses the ``AnalyzeDocument`` API operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-comprehend-documentclassifier-documentreaderconfig.html#cfn-comprehend-documentclassifier-documentreaderconfig-documentreadaction
            '''
            result = self._values.get("document_read_action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def document_read_mode(self) -> typing.Optional[builtins.str]:
            '''Determines the text extraction actions for PDF files. Enter one of the following values:.

            - ``SERVICE_DEFAULT`` - use the Amazon Comprehend service defaults for PDF files.
            - ``FORCE_DOCUMENT_READ_ACTION`` - Amazon Comprehend uses the Textract API specified by DocumentReadAction for all PDF files, including digital PDF files.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-comprehend-documentclassifier-documentreaderconfig.html#cfn-comprehend-documentclassifier-documentreaderconfig-documentreadmode
            '''
            result = self._values.get("document_read_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def feature_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Specifies the type of Amazon Textract features to apply.

            If you chose ``TEXTRACT_ANALYZE_DOCUMENT`` as the read action, you must specify one or both of the following values:

            - ``TABLES`` - Returns additional information about any tables that are detected in the input document.
            - ``FORMS`` - Returns additional information about any forms that are detected in the input document.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-comprehend-documentclassifier-documentreaderconfig.html#cfn-comprehend-documentclassifier-documentreaderconfig-featuretypes
            '''
            result = self._values.get("feature_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DocumentReaderConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_comprehend.mixins.CfnDocumentClassifierPropsMixin.VpcConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"security_group_ids": "securityGroupIds", "subnets": "subnets"},
    )
    class VpcConfigProperty:
        def __init__(
            self,
            *,
            security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Configuration parameters for an optional private Virtual Private Cloud (VPC) containing the resources you are using for the job.

            For more information, see `Amazon VPC <https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html>`_ .

            :param security_group_ids: The ID number for a security group on an instance of your private VPC. Security groups on your VPC function serve as a virtual firewall to control inbound and outbound traffic and provides security for the resources that you’ll be accessing on the VPC. This ID number is preceded by "sg-", for instance: "sg-03b388029b0a285ea". For more information, see `Security Groups for your VPC <https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html>`_ .
            :param subnets: The ID for each subnet being used in your private VPC. This subnet is a subset of the a range of IPv4 addresses used by the VPC and is specific to a given availability zone in the VPC’s Region. This ID number is preceded by "subnet-", for instance: "subnet-04ccf456919e69055". For more information, see `VPCs and Subnets <https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-comprehend-documentclassifier-vpcconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_comprehend import mixins as comprehend_mixins
                
                vpc_config_property = comprehend_mixins.CfnDocumentClassifierPropsMixin.VpcConfigProperty(
                    security_group_ids=["securityGroupIds"],
                    subnets=["subnets"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cea775617dcd53ad5462b38f231d902f6db3bd24a500faabee915807044656bd)
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
                check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnets is not None:
                self._values["subnets"] = subnets

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The ID number for a security group on an instance of your private VPC.

            Security groups on your VPC function serve as a virtual firewall to control inbound and outbound traffic and provides security for the resources that you’ll be accessing on the VPC. This ID number is preceded by "sg-", for instance: "sg-03b388029b0a285ea". For more information, see `Security Groups for your VPC <https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-comprehend-documentclassifier-vpcconfig.html#cfn-comprehend-documentclassifier-vpcconfig-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnets(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The ID for each subnet being used in your private VPC.

            This subnet is a subset of the a range of IPv4 addresses used by the VPC and is specific to a given availability zone in the VPC’s Region. This ID number is preceded by "subnet-", for instance: "subnet-04ccf456919e69055". For more information, see `VPCs and Subnets <https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-comprehend-documentclassifier-vpcconfig.html#cfn-comprehend-documentclassifier-vpcconfig-subnets
            '''
            result = self._values.get("subnets")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_comprehend.mixins.CfnFlywheelMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "active_model_arn": "activeModelArn",
        "data_access_role_arn": "dataAccessRoleArn",
        "data_lake_s3_uri": "dataLakeS3Uri",
        "data_security_config": "dataSecurityConfig",
        "flywheel_name": "flywheelName",
        "model_type": "modelType",
        "tags": "tags",
        "task_config": "taskConfig",
    },
)
class CfnFlywheelMixinProps:
    def __init__(
        self,
        *,
        active_model_arn: typing.Optional[builtins.str] = None,
        data_access_role_arn: typing.Optional[builtins.str] = None,
        data_lake_s3_uri: typing.Optional[builtins.str] = None,
        data_security_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlywheelPropsMixin.DataSecurityConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        flywheel_name: typing.Optional[builtins.str] = None,
        model_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        task_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlywheelPropsMixin.TaskConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnFlywheelPropsMixin.

        :param active_model_arn: The Amazon Resource Number (ARN) of the active model version.
        :param data_access_role_arn: The Amazon Resource Name (ARN) of the IAM role that grants Amazon Comprehend permission to access the flywheel data.
        :param data_lake_s3_uri: Amazon S3 URI of the data lake location.
        :param data_security_config: Data security configuration.
        :param flywheel_name: Name for the flywheel.
        :param model_type: Model type of the flywheel's model.
        :param tags: Tags associated with the endpoint being created. A tag is a key-value pair that adds metadata to the endpoint. For example, a tag with "Sales" as the key might be added to an endpoint to indicate its use by the sales department.
        :param task_config: Configuration about the model associated with a flywheel.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-comprehend-flywheel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_comprehend import mixins as comprehend_mixins
            
            cfn_flywheel_mixin_props = comprehend_mixins.CfnFlywheelMixinProps(
                active_model_arn="activeModelArn",
                data_access_role_arn="dataAccessRoleArn",
                data_lake_s3_uri="dataLakeS3Uri",
                data_security_config=comprehend_mixins.CfnFlywheelPropsMixin.DataSecurityConfigProperty(
                    data_lake_kms_key_id="dataLakeKmsKeyId",
                    model_kms_key_id="modelKmsKeyId",
                    volume_kms_key_id="volumeKmsKeyId",
                    vpc_config=comprehend_mixins.CfnFlywheelPropsMixin.VpcConfigProperty(
                        security_group_ids=["securityGroupIds"],
                        subnets=["subnets"]
                    )
                ),
                flywheel_name="flywheelName",
                model_type="modelType",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                task_config=comprehend_mixins.CfnFlywheelPropsMixin.TaskConfigProperty(
                    document_classification_config=comprehend_mixins.CfnFlywheelPropsMixin.DocumentClassificationConfigProperty(
                        labels=["labels"],
                        mode="mode"
                    ),
                    entity_recognition_config=comprehend_mixins.CfnFlywheelPropsMixin.EntityRecognitionConfigProperty(
                        entity_types=[comprehend_mixins.CfnFlywheelPropsMixin.EntityTypesListItemProperty(
                            type="type"
                        )]
                    ),
                    language_code="languageCode"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cebadd5c8b222d89d306d203598a8fd18137f8cada3111b74c7ddac86833ec32)
            check_type(argname="argument active_model_arn", value=active_model_arn, expected_type=type_hints["active_model_arn"])
            check_type(argname="argument data_access_role_arn", value=data_access_role_arn, expected_type=type_hints["data_access_role_arn"])
            check_type(argname="argument data_lake_s3_uri", value=data_lake_s3_uri, expected_type=type_hints["data_lake_s3_uri"])
            check_type(argname="argument data_security_config", value=data_security_config, expected_type=type_hints["data_security_config"])
            check_type(argname="argument flywheel_name", value=flywheel_name, expected_type=type_hints["flywheel_name"])
            check_type(argname="argument model_type", value=model_type, expected_type=type_hints["model_type"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument task_config", value=task_config, expected_type=type_hints["task_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if active_model_arn is not None:
            self._values["active_model_arn"] = active_model_arn
        if data_access_role_arn is not None:
            self._values["data_access_role_arn"] = data_access_role_arn
        if data_lake_s3_uri is not None:
            self._values["data_lake_s3_uri"] = data_lake_s3_uri
        if data_security_config is not None:
            self._values["data_security_config"] = data_security_config
        if flywheel_name is not None:
            self._values["flywheel_name"] = flywheel_name
        if model_type is not None:
            self._values["model_type"] = model_type
        if tags is not None:
            self._values["tags"] = tags
        if task_config is not None:
            self._values["task_config"] = task_config

    @builtins.property
    def active_model_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Number (ARN) of the active model version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-comprehend-flywheel.html#cfn-comprehend-flywheel-activemodelarn
        '''
        result = self._values.get("active_model_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_access_role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the IAM role that grants Amazon Comprehend permission to access the flywheel data.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-comprehend-flywheel.html#cfn-comprehend-flywheel-dataaccessrolearn
        '''
        result = self._values.get("data_access_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_lake_s3_uri(self) -> typing.Optional[builtins.str]:
        '''Amazon S3 URI of the data lake location.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-comprehend-flywheel.html#cfn-comprehend-flywheel-datalakes3uri
        '''
        result = self._values.get("data_lake_s3_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_security_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlywheelPropsMixin.DataSecurityConfigProperty"]]:
        '''Data security configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-comprehend-flywheel.html#cfn-comprehend-flywheel-datasecurityconfig
        '''
        result = self._values.get("data_security_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlywheelPropsMixin.DataSecurityConfigProperty"]], result)

    @builtins.property
    def flywheel_name(self) -> typing.Optional[builtins.str]:
        '''Name for the flywheel.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-comprehend-flywheel.html#cfn-comprehend-flywheel-flywheelname
        '''
        result = self._values.get("flywheel_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def model_type(self) -> typing.Optional[builtins.str]:
        '''Model type of the flywheel's model.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-comprehend-flywheel.html#cfn-comprehend-flywheel-modeltype
        '''
        result = self._values.get("model_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Tags associated with the endpoint being created.

        A tag is a key-value pair that adds metadata to the endpoint. For example, a tag with "Sales" as the key might be added to an endpoint to indicate its use by the sales department.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-comprehend-flywheel.html#cfn-comprehend-flywheel-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def task_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlywheelPropsMixin.TaskConfigProperty"]]:
        '''Configuration about the model associated with a flywheel.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-comprehend-flywheel.html#cfn-comprehend-flywheel-taskconfig
        '''
        result = self._values.get("task_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlywheelPropsMixin.TaskConfigProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFlywheelMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnFlywheelPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_comprehend.mixins.CfnFlywheelPropsMixin",
):
    '''A flywheel is an AWS resource that orchestrates the ongoing training of a model for custom classification or custom entity recognition.

    You can create a flywheel to start with an existing trained model, or Comprehend can create and train a new model.

    When you create the flywheel, Comprehend creates a data lake in your account. The data lake holds the training data and test data for all versions of the model.

    To use a flywheel with an existing trained model, you specify the active model version. Comprehend copies the model's training data and test data into the flywheel's data lake.

    To use the flywheel with a new model, you need to provide a dataset for training data (and optional test data) when you create the flywheel.

    For more information about flywheels, see `Flywheel overview <https://docs.aws.amazon.com/comprehend/latest/dg/flywheels-about.html>`_ in the *Amazon Comprehend Developer Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-comprehend-flywheel.html
    :cloudformationResource: AWS::Comprehend::Flywheel
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_comprehend import mixins as comprehend_mixins
        
        cfn_flywheel_props_mixin = comprehend_mixins.CfnFlywheelPropsMixin(comprehend_mixins.CfnFlywheelMixinProps(
            active_model_arn="activeModelArn",
            data_access_role_arn="dataAccessRoleArn",
            data_lake_s3_uri="dataLakeS3Uri",
            data_security_config=comprehend_mixins.CfnFlywheelPropsMixin.DataSecurityConfigProperty(
                data_lake_kms_key_id="dataLakeKmsKeyId",
                model_kms_key_id="modelKmsKeyId",
                volume_kms_key_id="volumeKmsKeyId",
                vpc_config=comprehend_mixins.CfnFlywheelPropsMixin.VpcConfigProperty(
                    security_group_ids=["securityGroupIds"],
                    subnets=["subnets"]
                )
            ),
            flywheel_name="flywheelName",
            model_type="modelType",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            task_config=comprehend_mixins.CfnFlywheelPropsMixin.TaskConfigProperty(
                document_classification_config=comprehend_mixins.CfnFlywheelPropsMixin.DocumentClassificationConfigProperty(
                    labels=["labels"],
                    mode="mode"
                ),
                entity_recognition_config=comprehend_mixins.CfnFlywheelPropsMixin.EntityRecognitionConfigProperty(
                    entity_types=[comprehend_mixins.CfnFlywheelPropsMixin.EntityTypesListItemProperty(
                        type="type"
                    )]
                ),
                language_code="languageCode"
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnFlywheelMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Comprehend::Flywheel``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9bd10a85f0a7407657a1ff026961fc9c77c70f62105dec2ad083971b273c6a8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__59a70dfde31bd6e0b97c9693643626015ce47fd3e3d70087785af14aac5f84e6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fb77dc1c8faaed1fa816b2a475d13787d17a230f904632c39ccee1912b1418e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnFlywheelMixinProps:
        return typing.cast(CfnFlywheelMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_comprehend.mixins.CfnFlywheelPropsMixin.DataSecurityConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_lake_kms_key_id": "dataLakeKmsKeyId",
            "model_kms_key_id": "modelKmsKeyId",
            "volume_kms_key_id": "volumeKmsKeyId",
            "vpc_config": "vpcConfig",
        },
    )
    class DataSecurityConfigProperty:
        def __init__(
            self,
            *,
            data_lake_kms_key_id: typing.Optional[builtins.str] = None,
            model_kms_key_id: typing.Optional[builtins.str] = None,
            volume_kms_key_id: typing.Optional[builtins.str] = None,
            vpc_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlywheelPropsMixin.VpcConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Data security configuration.

            :param data_lake_kms_key_id: ID for the AWS key that Amazon Comprehend uses to encrypt the data in the data lake.
            :param model_kms_key_id: ID for the AWS key that Amazon Comprehend uses to encrypt trained custom models. The ModelKmsKeyId can be either of the following formats: - KMS Key ID: ``"1234abcd-12ab-34cd-56ef-1234567890ab"`` - Amazon Resource Name (ARN) of a KMS Key: ``"arn:aws:kms:us-west-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab"``
            :param volume_kms_key_id: ID for the AWS key that Amazon Comprehend uses to encrypt the volume.
            :param vpc_config: Configuration parameters for an optional private Virtual Private Cloud (VPC) containing the resources you are using for the job. For more information, see `Amazon VPC <https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-comprehend-flywheel-datasecurityconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_comprehend import mixins as comprehend_mixins
                
                data_security_config_property = comprehend_mixins.CfnFlywheelPropsMixin.DataSecurityConfigProperty(
                    data_lake_kms_key_id="dataLakeKmsKeyId",
                    model_kms_key_id="modelKmsKeyId",
                    volume_kms_key_id="volumeKmsKeyId",
                    vpc_config=comprehend_mixins.CfnFlywheelPropsMixin.VpcConfigProperty(
                        security_group_ids=["securityGroupIds"],
                        subnets=["subnets"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7c613de91838473b49a4195bdff22d6ca46dedffb60624f99e1edff64bd7858c)
                check_type(argname="argument data_lake_kms_key_id", value=data_lake_kms_key_id, expected_type=type_hints["data_lake_kms_key_id"])
                check_type(argname="argument model_kms_key_id", value=model_kms_key_id, expected_type=type_hints["model_kms_key_id"])
                check_type(argname="argument volume_kms_key_id", value=volume_kms_key_id, expected_type=type_hints["volume_kms_key_id"])
                check_type(argname="argument vpc_config", value=vpc_config, expected_type=type_hints["vpc_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data_lake_kms_key_id is not None:
                self._values["data_lake_kms_key_id"] = data_lake_kms_key_id
            if model_kms_key_id is not None:
                self._values["model_kms_key_id"] = model_kms_key_id
            if volume_kms_key_id is not None:
                self._values["volume_kms_key_id"] = volume_kms_key_id
            if vpc_config is not None:
                self._values["vpc_config"] = vpc_config

        @builtins.property
        def data_lake_kms_key_id(self) -> typing.Optional[builtins.str]:
            '''ID for the AWS  key that Amazon Comprehend uses to encrypt the data in the data lake.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-comprehend-flywheel-datasecurityconfig.html#cfn-comprehend-flywheel-datasecurityconfig-datalakekmskeyid
            '''
            result = self._values.get("data_lake_kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def model_kms_key_id(self) -> typing.Optional[builtins.str]:
            '''ID for the AWS  key that Amazon Comprehend uses to encrypt trained custom models.

            The ModelKmsKeyId can be either of the following formats:

            - KMS Key ID: ``"1234abcd-12ab-34cd-56ef-1234567890ab"``
            - Amazon Resource Name (ARN) of a KMS Key: ``"arn:aws:kms:us-west-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab"``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-comprehend-flywheel-datasecurityconfig.html#cfn-comprehend-flywheel-datasecurityconfig-modelkmskeyid
            '''
            result = self._values.get("model_kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def volume_kms_key_id(self) -> typing.Optional[builtins.str]:
            '''ID for the AWS  key that Amazon Comprehend uses to encrypt the volume.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-comprehend-flywheel-datasecurityconfig.html#cfn-comprehend-flywheel-datasecurityconfig-volumekmskeyid
            '''
            result = self._values.get("volume_kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vpc_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlywheelPropsMixin.VpcConfigProperty"]]:
            '''Configuration parameters for an optional private Virtual Private Cloud (VPC) containing the resources you are using for the job.

            For more information, see `Amazon VPC <https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-comprehend-flywheel-datasecurityconfig.html#cfn-comprehend-flywheel-datasecurityconfig-vpcconfig
            '''
            result = self._values.get("vpc_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlywheelPropsMixin.VpcConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataSecurityConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_comprehend.mixins.CfnFlywheelPropsMixin.DocumentClassificationConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"labels": "labels", "mode": "mode"},
    )
    class DocumentClassificationConfigProperty:
        def __init__(
            self,
            *,
            labels: typing.Optional[typing.Sequence[builtins.str]] = None,
            mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration required for a document classification model.

            :param labels: One or more labels to associate with the custom classifier.
            :param mode: Classification mode indicates whether the documents are ``MULTI_CLASS`` or ``MULTI_LABEL`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-comprehend-flywheel-documentclassificationconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_comprehend import mixins as comprehend_mixins
                
                document_classification_config_property = comprehend_mixins.CfnFlywheelPropsMixin.DocumentClassificationConfigProperty(
                    labels=["labels"],
                    mode="mode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ff69541604b131f4d80d7a8d310332c1b6003fcde29995b2fae7dbe06904df5b)
                check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
                check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if labels is not None:
                self._values["labels"] = labels
            if mode is not None:
                self._values["mode"] = mode

        @builtins.property
        def labels(self) -> typing.Optional[typing.List[builtins.str]]:
            '''One or more labels to associate with the custom classifier.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-comprehend-flywheel-documentclassificationconfig.html#cfn-comprehend-flywheel-documentclassificationconfig-labels
            '''
            result = self._values.get("labels")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def mode(self) -> typing.Optional[builtins.str]:
            '''Classification mode indicates whether the documents are ``MULTI_CLASS`` or ``MULTI_LABEL`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-comprehend-flywheel-documentclassificationconfig.html#cfn-comprehend-flywheel-documentclassificationconfig-mode
            '''
            result = self._values.get("mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DocumentClassificationConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_comprehend.mixins.CfnFlywheelPropsMixin.EntityRecognitionConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"entity_types": "entityTypes"},
    )
    class EntityRecognitionConfigProperty:
        def __init__(
            self,
            *,
            entity_types: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlywheelPropsMixin.EntityTypesListItemProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Configuration required for an entity recognition model.

            :param entity_types: Up to 25 entity types that the model is trained to recognize.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-comprehend-flywheel-entityrecognitionconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_comprehend import mixins as comprehend_mixins
                
                entity_recognition_config_property = comprehend_mixins.CfnFlywheelPropsMixin.EntityRecognitionConfigProperty(
                    entity_types=[comprehend_mixins.CfnFlywheelPropsMixin.EntityTypesListItemProperty(
                        type="type"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3282ca5f97fc66d9dba4cfb3e3d8e116c8e33ce25ccf9d7d1b5a74aff4a6f800)
                check_type(argname="argument entity_types", value=entity_types, expected_type=type_hints["entity_types"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if entity_types is not None:
                self._values["entity_types"] = entity_types

        @builtins.property
        def entity_types(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlywheelPropsMixin.EntityTypesListItemProperty"]]]]:
            '''Up to 25 entity types that the model is trained to recognize.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-comprehend-flywheel-entityrecognitionconfig.html#cfn-comprehend-flywheel-entityrecognitionconfig-entitytypes
            '''
            result = self._values.get("entity_types")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlywheelPropsMixin.EntityTypesListItemProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EntityRecognitionConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_comprehend.mixins.CfnFlywheelPropsMixin.EntityTypesListItemProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type"},
    )
    class EntityTypesListItemProperty:
        def __init__(self, *, type: typing.Optional[builtins.str] = None) -> None:
            '''An entity type within a labeled training dataset that Amazon Comprehend uses to train a custom entity recognizer.

            :param type: An entity type within a labeled training dataset that Amazon Comprehend uses to train a custom entity recognizer. Entity types must not contain the following invalid characters: \\n (line break), \\n (escaped line break, \\r (carriage return), \\r (escaped carriage return), \\t (tab), \\t (escaped tab), and , (comma).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-comprehend-flywheel-entitytypeslistitem.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_comprehend import mixins as comprehend_mixins
                
                entity_types_list_item_property = comprehend_mixins.CfnFlywheelPropsMixin.EntityTypesListItemProperty(
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0ffe0a7bcf39224c6b0fd702d947789d008943a81419e9fa9e75c1584d2d2247)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''An entity type within a labeled training dataset that Amazon Comprehend uses to train a custom entity recognizer.

            Entity types must not contain the following invalid characters: \\n (line break), \\n (escaped line break, \\r (carriage return), \\r (escaped carriage return), \\t (tab), \\t (escaped tab), and , (comma).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-comprehend-flywheel-entitytypeslistitem.html#cfn-comprehend-flywheel-entitytypeslistitem-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EntityTypesListItemProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_comprehend.mixins.CfnFlywheelPropsMixin.TaskConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "document_classification_config": "documentClassificationConfig",
            "entity_recognition_config": "entityRecognitionConfig",
            "language_code": "languageCode",
        },
    )
    class TaskConfigProperty:
        def __init__(
            self,
            *,
            document_classification_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlywheelPropsMixin.DocumentClassificationConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            entity_recognition_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlywheelPropsMixin.EntityRecognitionConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            language_code: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration about the model associated with a flywheel.

            :param document_classification_config: Configuration required for a document classification model.
            :param entity_recognition_config: Configuration required for an entity recognition model.
            :param language_code: Language code for the language that the model supports.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-comprehend-flywheel-taskconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_comprehend import mixins as comprehend_mixins
                
                task_config_property = comprehend_mixins.CfnFlywheelPropsMixin.TaskConfigProperty(
                    document_classification_config=comprehend_mixins.CfnFlywheelPropsMixin.DocumentClassificationConfigProperty(
                        labels=["labels"],
                        mode="mode"
                    ),
                    entity_recognition_config=comprehend_mixins.CfnFlywheelPropsMixin.EntityRecognitionConfigProperty(
                        entity_types=[comprehend_mixins.CfnFlywheelPropsMixin.EntityTypesListItemProperty(
                            type="type"
                        )]
                    ),
                    language_code="languageCode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b3ab0b62f44e25137bd2e35b5b86abe2512186f218a9078e8630f5fefc6e1fcb)
                check_type(argname="argument document_classification_config", value=document_classification_config, expected_type=type_hints["document_classification_config"])
                check_type(argname="argument entity_recognition_config", value=entity_recognition_config, expected_type=type_hints["entity_recognition_config"])
                check_type(argname="argument language_code", value=language_code, expected_type=type_hints["language_code"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if document_classification_config is not None:
                self._values["document_classification_config"] = document_classification_config
            if entity_recognition_config is not None:
                self._values["entity_recognition_config"] = entity_recognition_config
            if language_code is not None:
                self._values["language_code"] = language_code

        @builtins.property
        def document_classification_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlywheelPropsMixin.DocumentClassificationConfigProperty"]]:
            '''Configuration required for a document classification model.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-comprehend-flywheel-taskconfig.html#cfn-comprehend-flywheel-taskconfig-documentclassificationconfig
            '''
            result = self._values.get("document_classification_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlywheelPropsMixin.DocumentClassificationConfigProperty"]], result)

        @builtins.property
        def entity_recognition_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlywheelPropsMixin.EntityRecognitionConfigProperty"]]:
            '''Configuration required for an entity recognition model.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-comprehend-flywheel-taskconfig.html#cfn-comprehend-flywheel-taskconfig-entityrecognitionconfig
            '''
            result = self._values.get("entity_recognition_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlywheelPropsMixin.EntityRecognitionConfigProperty"]], result)

        @builtins.property
        def language_code(self) -> typing.Optional[builtins.str]:
            '''Language code for the language that the model supports.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-comprehend-flywheel-taskconfig.html#cfn-comprehend-flywheel-taskconfig-languagecode
            '''
            result = self._values.get("language_code")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TaskConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_comprehend.mixins.CfnFlywheelPropsMixin.VpcConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"security_group_ids": "securityGroupIds", "subnets": "subnets"},
    )
    class VpcConfigProperty:
        def __init__(
            self,
            *,
            security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Configuration parameters for an optional private Virtual Private Cloud (VPC) containing the resources you are using for the job.

            For more information, see `Amazon VPC <https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html>`_ .

            :param security_group_ids: The ID number for a security group on an instance of your private VPC. Security groups on your VPC function serve as a virtual firewall to control inbound and outbound traffic and provides security for the resources that you’ll be accessing on the VPC. This ID number is preceded by "sg-", for instance: "sg-03b388029b0a285ea". For more information, see `Security Groups for your VPC <https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html>`_ .
            :param subnets: The ID for each subnet being used in your private VPC. This subnet is a subset of the a range of IPv4 addresses used by the VPC and is specific to a given availability zone in the VPC’s Region. This ID number is preceded by "subnet-", for instance: "subnet-04ccf456919e69055". For more information, see `VPCs and Subnets <https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-comprehend-flywheel-vpcconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_comprehend import mixins as comprehend_mixins
                
                vpc_config_property = comprehend_mixins.CfnFlywheelPropsMixin.VpcConfigProperty(
                    security_group_ids=["securityGroupIds"],
                    subnets=["subnets"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__100ca759a0e9e867f96a60aad2fc2c61922fc67f4ca3a48e0c6f42fd7badf16c)
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
                check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnets is not None:
                self._values["subnets"] = subnets

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The ID number for a security group on an instance of your private VPC.

            Security groups on your VPC function serve as a virtual firewall to control inbound and outbound traffic and provides security for the resources that you’ll be accessing on the VPC. This ID number is preceded by "sg-", for instance: "sg-03b388029b0a285ea". For more information, see `Security Groups for your VPC <https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-comprehend-flywheel-vpcconfig.html#cfn-comprehend-flywheel-vpcconfig-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnets(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The ID for each subnet being used in your private VPC.

            This subnet is a subset of the a range of IPv4 addresses used by the VPC and is specific to a given availability zone in the VPC’s Region. This ID number is preceded by "subnet-", for instance: "subnet-04ccf456919e69055". For more information, see `VPCs and Subnets <https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-comprehend-flywheel-vpcconfig.html#cfn-comprehend-flywheel-vpcconfig-subnets
            '''
            result = self._values.get("subnets")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnDocumentClassifierMixinProps",
    "CfnDocumentClassifierPropsMixin",
    "CfnFlywheelMixinProps",
    "CfnFlywheelPropsMixin",
]

publication.publish()

def _typecheckingstub__dc3a17ab812d4b57d244ac6f4632fb7cc793fc399d79c192735e179081ed25f5(
    *,
    data_access_role_arn: typing.Optional[builtins.str] = None,
    document_classifier_name: typing.Optional[builtins.str] = None,
    input_data_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDocumentClassifierPropsMixin.DocumentClassifierInputDataConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    language_code: typing.Optional[builtins.str] = None,
    mode: typing.Optional[builtins.str] = None,
    model_kms_key_id: typing.Optional[builtins.str] = None,
    model_policy: typing.Optional[builtins.str] = None,
    output_data_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDocumentClassifierPropsMixin.DocumentClassifierOutputDataConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    version_name: typing.Optional[builtins.str] = None,
    volume_kms_key_id: typing.Optional[builtins.str] = None,
    vpc_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDocumentClassifierPropsMixin.VpcConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb1f4b953355999ccb398fb17d65cf81067fa905f0352969e5b08d56a85ef8dd(
    props: typing.Union[CfnDocumentClassifierMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14557a9874e622c857c2aed15cf00b09d5cef28a43b13ec0e1fe77ce96682227(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b57304ba28bd9bf57921f71649ad64b462dfe55d31db7ccc9dd6bb09fd435f8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b88b4edc438acadab0f532fe0b1b5ca2c663ff861d94029cab6073c84f70518b(
    *,
    attribute_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    s3_uri: typing.Optional[builtins.str] = None,
    split: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac7910fd041b1311369f2ea8dcd35e9fb1cdce69c82e64a47a3e2e743b02896d(
    *,
    s3_uri: typing.Optional[builtins.str] = None,
    test_s3_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd2db49bab8a4884a2fe378375bd9df65119a0f7d67a1567ab85c562d971ae7b(
    *,
    augmented_manifests: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDocumentClassifierPropsMixin.AugmentedManifestsListItemProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    data_format: typing.Optional[builtins.str] = None,
    document_reader_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDocumentClassifierPropsMixin.DocumentReaderConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    documents: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDocumentClassifierPropsMixin.DocumentClassifierDocumentsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    document_type: typing.Optional[builtins.str] = None,
    label_delimiter: typing.Optional[builtins.str] = None,
    s3_uri: typing.Optional[builtins.str] = None,
    test_s3_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1914fbbf9313205c8d60dded06983e779238cd1f302a6b741705552fb4bf2ee(
    *,
    kms_key_id: typing.Optional[builtins.str] = None,
    s3_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__187ad126cd3d12bb6e4601dc6f1633408029cc47e38136d3580ac85cd77a3fef(
    *,
    document_read_action: typing.Optional[builtins.str] = None,
    document_read_mode: typing.Optional[builtins.str] = None,
    feature_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cea775617dcd53ad5462b38f231d902f6db3bd24a500faabee915807044656bd(
    *,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cebadd5c8b222d89d306d203598a8fd18137f8cada3111b74c7ddac86833ec32(
    *,
    active_model_arn: typing.Optional[builtins.str] = None,
    data_access_role_arn: typing.Optional[builtins.str] = None,
    data_lake_s3_uri: typing.Optional[builtins.str] = None,
    data_security_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlywheelPropsMixin.DataSecurityConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    flywheel_name: typing.Optional[builtins.str] = None,
    model_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    task_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlywheelPropsMixin.TaskConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9bd10a85f0a7407657a1ff026961fc9c77c70f62105dec2ad083971b273c6a8(
    props: typing.Union[CfnFlywheelMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59a70dfde31bd6e0b97c9693643626015ce47fd3e3d70087785af14aac5f84e6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fb77dc1c8faaed1fa816b2a475d13787d17a230f904632c39ccee1912b1418e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c613de91838473b49a4195bdff22d6ca46dedffb60624f99e1edff64bd7858c(
    *,
    data_lake_kms_key_id: typing.Optional[builtins.str] = None,
    model_kms_key_id: typing.Optional[builtins.str] = None,
    volume_kms_key_id: typing.Optional[builtins.str] = None,
    vpc_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlywheelPropsMixin.VpcConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff69541604b131f4d80d7a8d310332c1b6003fcde29995b2fae7dbe06904df5b(
    *,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3282ca5f97fc66d9dba4cfb3e3d8e116c8e33ce25ccf9d7d1b5a74aff4a6f800(
    *,
    entity_types: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlywheelPropsMixin.EntityTypesListItemProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ffe0a7bcf39224c6b0fd702d947789d008943a81419e9fa9e75c1584d2d2247(
    *,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3ab0b62f44e25137bd2e35b5b86abe2512186f218a9078e8630f5fefc6e1fcb(
    *,
    document_classification_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlywheelPropsMixin.DocumentClassificationConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    entity_recognition_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlywheelPropsMixin.EntityRecognitionConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    language_code: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__100ca759a0e9e867f96a60aad2fc2c61922fc67f4ca3a48e0c6f42fd7badf16c(
    *,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
