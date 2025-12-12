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
    jsii_type="@aws-cdk/mixins-preview.aws_s3outposts.mixins.CfnAccessPointMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "name": "name",
        "policy": "policy",
        "vpc_configuration": "vpcConfiguration",
    },
)
class CfnAccessPointMixinProps:
    def __init__(
        self,
        *,
        bucket: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        policy: typing.Any = None,
        vpc_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAccessPointPropsMixin.VpcConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnAccessPointPropsMixin.

        :param bucket: The Amazon Resource Name (ARN) of the S3 on Outposts bucket that is associated with this access point.
        :param name: The name of this access point.
        :param policy: The access point policy associated with this access point.
        :param vpc_configuration: The virtual private cloud (VPC) configuration for this access point, if one exists.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-accesspoint.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_s3outposts import mixins as s3outposts_mixins
            
            # policy: Any
            
            cfn_access_point_mixin_props = s3outposts_mixins.CfnAccessPointMixinProps(
                bucket="bucket",
                name="name",
                policy=policy,
                vpc_configuration=s3outposts_mixins.CfnAccessPointPropsMixin.VpcConfigurationProperty(
                    vpc_id="vpcId"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__461e36dd2f2b960cc7523d5e3bed444873d1b211e622ed7aece0a8ff1f30c436)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument vpc_configuration", value=vpc_configuration, expected_type=type_hints["vpc_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket is not None:
            self._values["bucket"] = bucket
        if name is not None:
            self._values["name"] = name
        if policy is not None:
            self._values["policy"] = policy
        if vpc_configuration is not None:
            self._values["vpc_configuration"] = vpc_configuration

    @builtins.property
    def bucket(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the S3 on Outposts bucket that is associated with this access point.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-accesspoint.html#cfn-s3outposts-accesspoint-bucket
        '''
        result = self._values.get("bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of this access point.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-accesspoint.html#cfn-s3outposts-accesspoint-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy(self) -> typing.Any:
        '''The access point policy associated with this access point.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-accesspoint.html#cfn-s3outposts-accesspoint-policy
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def vpc_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAccessPointPropsMixin.VpcConfigurationProperty"]]:
        '''The virtual private cloud (VPC) configuration for this access point, if one exists.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-accesspoint.html#cfn-s3outposts-accesspoint-vpcconfiguration
        '''
        result = self._values.get("vpc_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAccessPointPropsMixin.VpcConfigurationProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAccessPointMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAccessPointPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_s3outposts.mixins.CfnAccessPointPropsMixin",
):
    '''The AWS::S3Outposts::AccessPoint resource specifies an access point and associates it with the specified Amazon S3 on Outposts bucket.

    For more information, see `Managing data access with Amazon S3 access points <https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-points.html>`_ .
    .. epigraph::

       S3 on Outposts supports only VPC-style access points.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-accesspoint.html
    :cloudformationResource: AWS::S3Outposts::AccessPoint
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_s3outposts import mixins as s3outposts_mixins
        
        # policy: Any
        
        cfn_access_point_props_mixin = s3outposts_mixins.CfnAccessPointPropsMixin(s3outposts_mixins.CfnAccessPointMixinProps(
            bucket="bucket",
            name="name",
            policy=policy,
            vpc_configuration=s3outposts_mixins.CfnAccessPointPropsMixin.VpcConfigurationProperty(
                vpc_id="vpcId"
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAccessPointMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::S3Outposts::AccessPoint``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05b78b9d2b4dc0ec23f35cc8c51f8bb2c80c01032e4050e6d99dc4856b406564)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b76fd7c85824547a7833841c2e13b1d1e32d8d7314c0d00d0720e91487c67cf)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5745edb401983932e61c0af35d61c56d3e238fa82e76ed1f1d7bb91ef936fd1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAccessPointMixinProps:
        return typing.cast(CfnAccessPointMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3outposts.mixins.CfnAccessPointPropsMixin.VpcConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"vpc_id": "vpcId"},
    )
    class VpcConfigurationProperty:
        def __init__(self, *, vpc_id: typing.Optional[builtins.str] = None) -> None:
            '''Contains the virtual private cloud (VPC) configuration for the specified access point.

            :param vpc_id: Virtual Private Cloud (VPC) Id from which AccessPoint will allow requests.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3outposts-accesspoint-vpcconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3outposts import mixins as s3outposts_mixins
                
                vpc_configuration_property = s3outposts_mixins.CfnAccessPointPropsMixin.VpcConfigurationProperty(
                    vpc_id="vpcId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6c46939368cb8276066ff7186489a499f482b8ba10061ffc977df7a2a68a6daf)
                check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if vpc_id is not None:
                self._values["vpc_id"] = vpc_id

        @builtins.property
        def vpc_id(self) -> typing.Optional[builtins.str]:
            '''Virtual Private Cloud (VPC) Id from which AccessPoint will allow requests.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3outposts-accesspoint-vpcconfiguration.html#cfn-s3outposts-accesspoint-vpcconfiguration-vpcid
            '''
            result = self._values.get("vpc_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_s3outposts.mixins.CfnBucketMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "lifecycle_configuration": "lifecycleConfiguration",
        "outpost_id": "outpostId",
        "tags": "tags",
    },
)
class CfnBucketMixinProps:
    def __init__(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        lifecycle_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.LifecycleConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        outpost_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnBucketPropsMixin.

        :param bucket_name: A name for the S3 on Outposts bucket. If you don't specify a name, AWS CloudFormation generates a unique ID and uses that ID for the bucket name. The bucket name must contain only lowercase letters, numbers, periods (.), and dashes (-) and must follow `Amazon S3 bucket restrictions and limitations <https://docs.aws.amazon.com/AmazonS3/latest/userguide/BucketRestrictions.html>`_ . For more information, see `Bucket naming rules <https://docs.aws.amazon.com/AmazonS3/latest/userguide/BucketRestrictions.html#bucketnamingrules>`_ . .. epigraph:: If you specify a name, you can't perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you need to replace the resource, specify a new name.
        :param lifecycle_configuration: Creates a new lifecycle configuration for the S3 on Outposts bucket or replaces an existing lifecycle configuration. Outposts buckets only support lifecycle configurations that delete/expire objects after a certain period of time and abort incomplete multipart uploads.
        :param outpost_id: The ID of the Outpost of the specified bucket.
        :param tags: Sets the tags for an S3 on Outposts bucket. For more information, see `Using Amazon S3 on Outposts <https://docs.aws.amazon.com/AmazonS3/latest/userguide/S3onOutposts.html>`_ . Use tags to organize your AWS bill to reflect your own cost structure. To do this, sign up to get your AWS account bill with tag key values included. Then, to see the cost of combined resources, organize your billing information according to resources with the same tag key values. For example, you can tag several resources with a specific application name, and then organize your billing information to see the total cost of that application across several services. For more information, see `Cost allocation and tags <https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html>`_ . .. epigraph:: Within a bucket, if you add a tag that has the same key as an existing tag, the new value overwrites the old value. For more information, see `Using cost allocation and bucket tags <https://docs.aws.amazon.com/AmazonS3/latest/userguide/CostAllocTagging.html>`_ . To use this resource, you must have permissions to perform the ``s3-outposts:PutBucketTagging`` . The S3 on Outposts bucket owner has this permission by default and can grant this permission to others. For more information about permissions, see `Permissions Related to Bucket Subresource Operations <https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-with-s3-actions.html#using-with-s3-actions-related-to-bucket-subresources>`_ and `Managing access permissions to your Amazon S3 resources <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-access-control.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-bucket.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_s3outposts import mixins as s3outposts_mixins
            
            # filter: Any
            
            cfn_bucket_mixin_props = s3outposts_mixins.CfnBucketMixinProps(
                bucket_name="bucketName",
                lifecycle_configuration=s3outposts_mixins.CfnBucketPropsMixin.LifecycleConfigurationProperty(
                    rules=[s3outposts_mixins.CfnBucketPropsMixin.RuleProperty(
                        abort_incomplete_multipart_upload=s3outposts_mixins.CfnBucketPropsMixin.AbortIncompleteMultipartUploadProperty(
                            days_after_initiation=123
                        ),
                        expiration_date="expirationDate",
                        expiration_in_days=123,
                        filter=filter,
                        id="id",
                        status="status"
                    )]
                ),
                outpost_id="outpostId",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fed3e07f928ecc7aa71609fb3ec54a08021c44a7b6c6f628744e146e00ce5550)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument lifecycle_configuration", value=lifecycle_configuration, expected_type=type_hints["lifecycle_configuration"])
            check_type(argname="argument outpost_id", value=outpost_id, expected_type=type_hints["outpost_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if lifecycle_configuration is not None:
            self._values["lifecycle_configuration"] = lifecycle_configuration
        if outpost_id is not None:
            self._values["outpost_id"] = outpost_id
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''A name for the S3 on Outposts bucket.

        If you don't specify a name, AWS CloudFormation generates a unique ID and uses that ID for the bucket name. The bucket name must contain only lowercase letters, numbers, periods (.), and dashes (-) and must follow `Amazon S3 bucket restrictions and limitations <https://docs.aws.amazon.com/AmazonS3/latest/userguide/BucketRestrictions.html>`_ . For more information, see `Bucket naming rules <https://docs.aws.amazon.com/AmazonS3/latest/userguide/BucketRestrictions.html#bucketnamingrules>`_ .
        .. epigraph::

           If you specify a name, you can't perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you need to replace the resource, specify a new name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-bucket.html#cfn-s3outposts-bucket-bucketname
        '''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lifecycle_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.LifecycleConfigurationProperty"]]:
        '''Creates a new lifecycle configuration for the S3 on Outposts bucket or replaces an existing lifecycle configuration.

        Outposts buckets only support lifecycle configurations that delete/expire objects after a certain period of time and abort incomplete multipart uploads.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-bucket.html#cfn-s3outposts-bucket-lifecycleconfiguration
        '''
        result = self._values.get("lifecycle_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.LifecycleConfigurationProperty"]], result)

    @builtins.property
    def outpost_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the Outpost of the specified bucket.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-bucket.html#cfn-s3outposts-bucket-outpostid
        '''
        result = self._values.get("outpost_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Sets the tags for an S3 on Outposts bucket. For more information, see `Using Amazon S3 on Outposts <https://docs.aws.amazon.com/AmazonS3/latest/userguide/S3onOutposts.html>`_ .

        Use tags to organize your AWS bill to reflect your own cost structure. To do this, sign up to get your AWS account bill with tag key values included. Then, to see the cost of combined resources, organize your billing information according to resources with the same tag key values. For example, you can tag several resources with a specific application name, and then organize your billing information to see the total cost of that application across several services. For more information, see `Cost allocation and tags <https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html>`_ .
        .. epigraph::

           Within a bucket, if you add a tag that has the same key as an existing tag, the new value overwrites the old value. For more information, see `Using cost allocation and bucket tags <https://docs.aws.amazon.com/AmazonS3/latest/userguide/CostAllocTagging.html>`_ .

        To use this resource, you must have permissions to perform the ``s3-outposts:PutBucketTagging`` . The S3 on Outposts bucket owner has this permission by default and can grant this permission to others. For more information about permissions, see `Permissions Related to Bucket Subresource Operations <https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-with-s3-actions.html#using-with-s3-actions-related-to-bucket-subresources>`_ and `Managing access permissions to your Amazon S3 resources <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-access-control.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-bucket.html#cfn-s3outposts-bucket-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBucketMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_s3outposts.mixins.CfnBucketPolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "policy_document": "policyDocument"},
)
class CfnBucketPolicyMixinProps:
    def __init__(
        self,
        *,
        bucket: typing.Optional[builtins.str] = None,
        policy_document: typing.Any = None,
    ) -> None:
        '''Properties for CfnBucketPolicyPropsMixin.

        :param bucket: The name of the Amazon S3 Outposts bucket to which the policy applies.
        :param policy_document: A policy document containing permissions to add to the specified bucket. In IAM, you must provide policy documents in JSON format. However, in CloudFormation, you can provide the policy in JSON or YAML format because CloudFormation converts YAML to JSON before submitting it to IAM. For more information, see the AWS::IAM::Policy `PolicyDocument <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-policydocument>`_ resource description in this guide and `Access Policy Language Overview <https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-policy-language-overview.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-bucketpolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_s3outposts import mixins as s3outposts_mixins
            
            # policy_document: Any
            
            cfn_bucket_policy_mixin_props = s3outposts_mixins.CfnBucketPolicyMixinProps(
                bucket="bucket",
                policy_document=policy_document
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d34b2dea83be572be5f47d996f175fbcbcb026d5f4bd5481bf4f1fe007580a3)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument policy_document", value=policy_document, expected_type=type_hints["policy_document"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket is not None:
            self._values["bucket"] = bucket
        if policy_document is not None:
            self._values["policy_document"] = policy_document

    @builtins.property
    def bucket(self) -> typing.Optional[builtins.str]:
        '''The name of the Amazon S3 Outposts bucket to which the policy applies.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-bucketpolicy.html#cfn-s3outposts-bucketpolicy-bucket
        '''
        result = self._values.get("bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_document(self) -> typing.Any:
        '''A policy document containing permissions to add to the specified bucket.

        In IAM, you must provide policy documents in JSON format. However, in CloudFormation, you can provide the policy in JSON or YAML format because CloudFormation converts YAML to JSON before submitting it to IAM. For more information, see the AWS::IAM::Policy `PolicyDocument <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-policydocument>`_ resource description in this guide and `Access Policy Language Overview <https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-policy-language-overview.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-bucketpolicy.html#cfn-s3outposts-bucketpolicy-policydocument
        '''
        result = self._values.get("policy_document")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBucketPolicyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnBucketPolicyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_s3outposts.mixins.CfnBucketPolicyPropsMixin",
):
    '''This resource applies a bucket policy to an Amazon S3 on Outposts bucket.

    If you are using an identity other than the root user of the AWS account that owns the S3 on Outposts bucket, the calling identity must have the ``s3-outposts:PutBucketPolicy`` permissions on the specified Outposts bucket and belong to the bucket owner's account in order to use this resource.

    If you don't have ``s3-outposts:PutBucketPolicy`` permissions, S3 on Outposts returns a ``403 Access Denied`` error.
    .. epigraph::

       The root user of the AWS account that owns an Outposts bucket can *always* use this resource, even if the policy explicitly denies the root user the ability to perform actions on this resource.

    For more information, see the AWS::IAM::Policy `PolicyDocument <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-policydocument>`_ resource description in this guide and `Access Policy Language Overview <https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-policy-language-overview.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-bucketpolicy.html
    :cloudformationResource: AWS::S3Outposts::BucketPolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_s3outposts import mixins as s3outposts_mixins
        
        # policy_document: Any
        
        cfn_bucket_policy_props_mixin = s3outposts_mixins.CfnBucketPolicyPropsMixin(s3outposts_mixins.CfnBucketPolicyMixinProps(
            bucket="bucket",
            policy_document=policy_document
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnBucketPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::S3Outposts::BucketPolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df979b27424226625cf0cab4d43db5ab57692d3bab49ecc4d97e6f98fe4d9cde)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ac7b73945db89067714a28595e17032da8920afed26eb6c0e139b58a87e2478)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbbd28db56dfdac9a85c183fabab5063a35ef736d8bd25481eed844cd4988751)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnBucketPolicyMixinProps:
        return typing.cast(CfnBucketPolicyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.implements(_IMixin_11e4b965)
class CfnBucketPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_s3outposts.mixins.CfnBucketPropsMixin",
):
    '''The AWS::S3Outposts::Bucket resource specifies a new Amazon S3 on Outposts bucket.

    To create an S3 on Outposts bucket, you must have S3 on Outposts capacity provisioned on your Outpost. For more information, see `Using Amazon S3 on Outposts <https://docs.aws.amazon.com/AmazonS3/latest/userguide/S3onOutposts.html>`_ .

    S3 on Outposts buckets support the following:

    - Tags
    - Lifecycle configuration rules for deleting expired objects

    For a complete list of restrictions and Amazon S3 feature limitations on S3 on Outposts, see `Amazon S3 on Outposts Restrictions and Limitations <https://docs.aws.amazon.com/AmazonS3/latest/userguide/S3OnOutpostsRestrictionsLimitations.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-bucket.html
    :cloudformationResource: AWS::S3Outposts::Bucket
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_s3outposts import mixins as s3outposts_mixins
        
        # filter: Any
        
        cfn_bucket_props_mixin = s3outposts_mixins.CfnBucketPropsMixin(s3outposts_mixins.CfnBucketMixinProps(
            bucket_name="bucketName",
            lifecycle_configuration=s3outposts_mixins.CfnBucketPropsMixin.LifecycleConfigurationProperty(
                rules=[s3outposts_mixins.CfnBucketPropsMixin.RuleProperty(
                    abort_incomplete_multipart_upload=s3outposts_mixins.CfnBucketPropsMixin.AbortIncompleteMultipartUploadProperty(
                        days_after_initiation=123
                    ),
                    expiration_date="expirationDate",
                    expiration_in_days=123,
                    filter=filter,
                    id="id",
                    status="status"
                )]
            ),
            outpost_id="outpostId",
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
        props: typing.Union[CfnBucketMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::S3Outposts::Bucket``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43920ed55255fba7f0c95fbc8fa699cd896c7dee010830e7548ec7f08e986399)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc86340ab50bf0dced0a3b812aef78847d1662f89cf40c7f5cfb6230584c598d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b416aba79c499f042f022f2aa8ccfceec2766a41fa7ca6b562053c5521752e89)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnBucketMixinProps:
        return typing.cast(CfnBucketMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3outposts.mixins.CfnBucketPropsMixin.AbortIncompleteMultipartUploadProperty",
        jsii_struct_bases=[],
        name_mapping={"days_after_initiation": "daysAfterInitiation"},
    )
    class AbortIncompleteMultipartUploadProperty:
        def __init__(
            self,
            *,
            days_after_initiation: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies the days since the initiation of an incomplete multipart upload that Amazon S3 on Outposts waits before permanently removing all parts of the upload.

            For more information, see `Aborting Incomplete Multipart Uploads Using a Bucket Lifecycle Policy <https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html#mpu-abort-incomplete-mpu-lifecycle-config>`_ .

            :param days_after_initiation: Specifies the number of days after initiation that Amazon S3 on Outposts aborts an incomplete multipart upload.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3outposts-bucket-abortincompletemultipartupload.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3outposts import mixins as s3outposts_mixins
                
                abort_incomplete_multipart_upload_property = s3outposts_mixins.CfnBucketPropsMixin.AbortIncompleteMultipartUploadProperty(
                    days_after_initiation=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__367a4dd19d72cc0109b607d77ceb80e395004b232a644536dc2f121cc929a850)
                check_type(argname="argument days_after_initiation", value=days_after_initiation, expected_type=type_hints["days_after_initiation"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if days_after_initiation is not None:
                self._values["days_after_initiation"] = days_after_initiation

        @builtins.property
        def days_after_initiation(self) -> typing.Optional[jsii.Number]:
            '''Specifies the number of days after initiation that Amazon S3 on Outposts aborts an incomplete multipart upload.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3outposts-bucket-abortincompletemultipartupload.html#cfn-s3outposts-bucket-abortincompletemultipartupload-daysafterinitiation
            '''
            result = self._values.get("days_after_initiation")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AbortIncompleteMultipartUploadProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3outposts.mixins.CfnBucketPropsMixin.LifecycleConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"rules": "rules"},
    )
    class LifecycleConfigurationProperty:
        def __init__(
            self,
            *,
            rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.RuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The container for the lifecycle configuration for the objects stored in an S3 on Outposts bucket.

            :param rules: The container for the lifecycle configuration rules for the objects stored in the S3 on Outposts bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3outposts-bucket-lifecycleconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3outposts import mixins as s3outposts_mixins
                
                # filter: Any
                
                lifecycle_configuration_property = s3outposts_mixins.CfnBucketPropsMixin.LifecycleConfigurationProperty(
                    rules=[s3outposts_mixins.CfnBucketPropsMixin.RuleProperty(
                        abort_incomplete_multipart_upload=s3outposts_mixins.CfnBucketPropsMixin.AbortIncompleteMultipartUploadProperty(
                            days_after_initiation=123
                        ),
                        expiration_date="expirationDate",
                        expiration_in_days=123,
                        filter=filter,
                        id="id",
                        status="status"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e9e96b84a339d0358f6387e74a9b2818f031ed675ecaa6ebd8c7e34c18909c49)
                check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if rules is not None:
                self._values["rules"] = rules

        @builtins.property
        def rules(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.RuleProperty"]]]]:
            '''The container for the lifecycle configuration rules for the objects stored in the S3 on Outposts bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3outposts-bucket-lifecycleconfiguration.html#cfn-s3outposts-bucket-lifecycleconfiguration-rules
            '''
            result = self._values.get("rules")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.RuleProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LifecycleConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3outposts.mixins.CfnBucketPropsMixin.RuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "abort_incomplete_multipart_upload": "abortIncompleteMultipartUpload",
            "expiration_date": "expirationDate",
            "expiration_in_days": "expirationInDays",
            "filter": "filter",
            "id": "id",
            "status": "status",
        },
    )
    class RuleProperty:
        def __init__(
            self,
            *,
            abort_incomplete_multipart_upload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.AbortIncompleteMultipartUploadProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            expiration_date: typing.Optional[builtins.str] = None,
            expiration_in_days: typing.Optional[jsii.Number] = None,
            filter: typing.Any = None,
            id: typing.Optional[builtins.str] = None,
            status: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A container for an Amazon S3 on Outposts bucket lifecycle rule.

            :param abort_incomplete_multipart_upload: The container for the abort incomplete multipart upload rule.
            :param expiration_date: Specifies the expiration for the lifecycle of the object by specifying an expiry date.
            :param expiration_in_days: Specifies the expiration for the lifecycle of the object in the form of days that the object has been in the S3 on Outposts bucket.
            :param filter: The container for the filter of the lifecycle rule.
            :param id: Unique identifier for the lifecycle rule. The value can't be longer than 255 characters.
            :param status: If ``Enabled`` , the rule is currently being applied. If ``Disabled`` , the rule is not currently being applied.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3outposts-bucket-rule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3outposts import mixins as s3outposts_mixins
                
                # filter: Any
                
                rule_property = s3outposts_mixins.CfnBucketPropsMixin.RuleProperty(
                    abort_incomplete_multipart_upload=s3outposts_mixins.CfnBucketPropsMixin.AbortIncompleteMultipartUploadProperty(
                        days_after_initiation=123
                    ),
                    expiration_date="expirationDate",
                    expiration_in_days=123,
                    filter=filter,
                    id="id",
                    status="status"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bf9a425b4bef4537588c16ecb8a38eb3266288249134472b1d9a539daae82496)
                check_type(argname="argument abort_incomplete_multipart_upload", value=abort_incomplete_multipart_upload, expected_type=type_hints["abort_incomplete_multipart_upload"])
                check_type(argname="argument expiration_date", value=expiration_date, expected_type=type_hints["expiration_date"])
                check_type(argname="argument expiration_in_days", value=expiration_in_days, expected_type=type_hints["expiration_in_days"])
                check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if abort_incomplete_multipart_upload is not None:
                self._values["abort_incomplete_multipart_upload"] = abort_incomplete_multipart_upload
            if expiration_date is not None:
                self._values["expiration_date"] = expiration_date
            if expiration_in_days is not None:
                self._values["expiration_in_days"] = expiration_in_days
            if filter is not None:
                self._values["filter"] = filter
            if id is not None:
                self._values["id"] = id
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def abort_incomplete_multipart_upload(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.AbortIncompleteMultipartUploadProperty"]]:
            '''The container for the abort incomplete multipart upload rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3outposts-bucket-rule.html#cfn-s3outposts-bucket-rule-abortincompletemultipartupload
            '''
            result = self._values.get("abort_incomplete_multipart_upload")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.AbortIncompleteMultipartUploadProperty"]], result)

        @builtins.property
        def expiration_date(self) -> typing.Optional[builtins.str]:
            '''Specifies the expiration for the lifecycle of the object by specifying an expiry date.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3outposts-bucket-rule.html#cfn-s3outposts-bucket-rule-expirationdate
            '''
            result = self._values.get("expiration_date")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def expiration_in_days(self) -> typing.Optional[jsii.Number]:
            '''Specifies the expiration for the lifecycle of the object in the form of days that the object has been in the S3 on Outposts bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3outposts-bucket-rule.html#cfn-s3outposts-bucket-rule-expirationindays
            '''
            result = self._values.get("expiration_in_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def filter(self) -> typing.Any:
            '''The container for the filter of the lifecycle rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3outposts-bucket-rule.html#cfn-s3outposts-bucket-rule-filter
            '''
            result = self._values.get("filter")
            return typing.cast(typing.Any, result)

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''Unique identifier for the lifecycle rule.

            The value can't be longer than 255 characters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3outposts-bucket-rule.html#cfn-s3outposts-bucket-rule-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''If ``Enabled`` , the rule is currently being applied.

            If ``Disabled`` , the rule is not currently being applied.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3outposts-bucket-rule.html#cfn-s3outposts-bucket-rule-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_s3outposts.mixins.CfnEndpointMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_type": "accessType",
        "customer_owned_ipv4_pool": "customerOwnedIpv4Pool",
        "failed_reason": "failedReason",
        "outpost_id": "outpostId",
        "security_group_id": "securityGroupId",
        "subnet_id": "subnetId",
    },
)
class CfnEndpointMixinProps:
    def __init__(
        self,
        *,
        access_type: typing.Optional[builtins.str] = None,
        customer_owned_ipv4_pool: typing.Optional[builtins.str] = None,
        failed_reason: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEndpointPropsMixin.FailedReasonProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        outpost_id: typing.Optional[builtins.str] = None,
        security_group_id: typing.Optional[builtins.str] = None,
        subnet_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnEndpointPropsMixin.

        :param access_type: The container for the type of connectivity used to access the Amazon S3 on Outposts endpoint. To use the Amazon VPC , choose ``Private`` . To use the endpoint with an on-premises network, choose ``CustomerOwnedIp`` . If you choose ``CustomerOwnedIp`` , you must also provide the customer-owned IP address pool (CoIP pool). .. epigraph:: ``Private`` is the default access type value. Default: - "Private"
        :param customer_owned_ipv4_pool: The ID of the customer-owned IPv4 address pool (CoIP pool) for the endpoint. IP addresses are allocated from this pool for the endpoint.
        :param failed_reason: The failure reason, if any, for a create or delete endpoint operation.
        :param outpost_id: The ID of the Outpost.
        :param security_group_id: The ID of the security group used for the endpoint.
        :param subnet_id: The ID of the subnet used for the endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-endpoint.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_s3outposts import mixins as s3outposts_mixins
            
            cfn_endpoint_mixin_props = s3outposts_mixins.CfnEndpointMixinProps(
                access_type="accessType",
                customer_owned_ipv4_pool="customerOwnedIpv4Pool",
                failed_reason=s3outposts_mixins.CfnEndpointPropsMixin.FailedReasonProperty(
                    error_code="errorCode",
                    message="message"
                ),
                outpost_id="outpostId",
                security_group_id="securityGroupId",
                subnet_id="subnetId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70ed83b8d095e6b8328fd1754d6e0d524bc8011fe91a71718c27a0eed4c32b7e)
            check_type(argname="argument access_type", value=access_type, expected_type=type_hints["access_type"])
            check_type(argname="argument customer_owned_ipv4_pool", value=customer_owned_ipv4_pool, expected_type=type_hints["customer_owned_ipv4_pool"])
            check_type(argname="argument failed_reason", value=failed_reason, expected_type=type_hints["failed_reason"])
            check_type(argname="argument outpost_id", value=outpost_id, expected_type=type_hints["outpost_id"])
            check_type(argname="argument security_group_id", value=security_group_id, expected_type=type_hints["security_group_id"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_type is not None:
            self._values["access_type"] = access_type
        if customer_owned_ipv4_pool is not None:
            self._values["customer_owned_ipv4_pool"] = customer_owned_ipv4_pool
        if failed_reason is not None:
            self._values["failed_reason"] = failed_reason
        if outpost_id is not None:
            self._values["outpost_id"] = outpost_id
        if security_group_id is not None:
            self._values["security_group_id"] = security_group_id
        if subnet_id is not None:
            self._values["subnet_id"] = subnet_id

    @builtins.property
    def access_type(self) -> typing.Optional[builtins.str]:
        '''The container for the type of connectivity used to access the Amazon S3 on Outposts endpoint.

        To use the Amazon VPC , choose ``Private`` . To use the endpoint with an on-premises network, choose ``CustomerOwnedIp`` . If you choose ``CustomerOwnedIp`` , you must also provide the customer-owned IP address pool (CoIP pool).
        .. epigraph::

           ``Private`` is the default access type value.

        :default: - "Private"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-endpoint.html#cfn-s3outposts-endpoint-accesstype
        '''
        result = self._values.get("access_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def customer_owned_ipv4_pool(self) -> typing.Optional[builtins.str]:
        '''The ID of the customer-owned IPv4 address pool (CoIP pool) for the endpoint.

        IP addresses are allocated from this pool for the endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-endpoint.html#cfn-s3outposts-endpoint-customerownedipv4pool
        '''
        result = self._values.get("customer_owned_ipv4_pool")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def failed_reason(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEndpointPropsMixin.FailedReasonProperty"]]:
        '''The failure reason, if any, for a create or delete endpoint operation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-endpoint.html#cfn-s3outposts-endpoint-failedreason
        '''
        result = self._values.get("failed_reason")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEndpointPropsMixin.FailedReasonProperty"]], result)

    @builtins.property
    def outpost_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the Outpost.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-endpoint.html#cfn-s3outposts-endpoint-outpostid
        '''
        result = self._values.get("outpost_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_group_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the security group used for the endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-endpoint.html#cfn-s3outposts-endpoint-securitygroupid
        '''
        result = self._values.get("security_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the subnet used for the endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-endpoint.html#cfn-s3outposts-endpoint-subnetid
        '''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEndpointMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnEndpointPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_s3outposts.mixins.CfnEndpointPropsMixin",
):
    '''This AWS::S3Outposts::Endpoint resource specifies an endpoint and associates it with the specified Outpost.

    Amazon S3 on Outposts access points simplify managing data access at scale for shared datasets in S3 on Outposts. S3 on Outposts uses endpoints to connect to S3 on Outposts buckets so that you can perform actions within your virtual private cloud (VPC). For more information, see `Accessing S3 on Outposts using VPC-only access points <https://docs.aws.amazon.com/AmazonS3/latest/userguide/AccessingS3Outposts.html>`_ .
    .. epigraph::

       It can take up to 5 minutes for this resource to be created.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-endpoint.html
    :cloudformationResource: AWS::S3Outposts::Endpoint
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_s3outposts import mixins as s3outposts_mixins
        
        cfn_endpoint_props_mixin = s3outposts_mixins.CfnEndpointPropsMixin(s3outposts_mixins.CfnEndpointMixinProps(
            access_type="accessType",
            customer_owned_ipv4_pool="customerOwnedIpv4Pool",
            failed_reason=s3outposts_mixins.CfnEndpointPropsMixin.FailedReasonProperty(
                error_code="errorCode",
                message="message"
            ),
            outpost_id="outpostId",
            security_group_id="securityGroupId",
            subnet_id="subnetId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnEndpointMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::S3Outposts::Endpoint``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41f2448ac08b8b2faa8e54c49bb79642d87d4c67c47272335b6230709a8ed21a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a9488f6207f856adf3c596aa69068f6223f32c09b0021d6a67dc3ac46377c54)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2269077fd8bd61b8583c9531906d1b91631160eec5b9f9ba420b5ad40ccde874)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnEndpointMixinProps:
        return typing.cast(CfnEndpointMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3outposts.mixins.CfnEndpointPropsMixin.FailedReasonProperty",
        jsii_struct_bases=[],
        name_mapping={"error_code": "errorCode", "message": "message"},
    )
    class FailedReasonProperty:
        def __init__(
            self,
            *,
            error_code: typing.Optional[builtins.str] = None,
            message: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The failure reason, if any, for a create or delete endpoint operation.

            :param error_code: The failure code, if any, for a create or delete endpoint operation.
            :param message: Additional error details describing the endpoint failure and recommended action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3outposts-endpoint-failedreason.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3outposts import mixins as s3outposts_mixins
                
                failed_reason_property = s3outposts_mixins.CfnEndpointPropsMixin.FailedReasonProperty(
                    error_code="errorCode",
                    message="message"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a1aec069c65ab9a5fe03afd032ae56c9b58af18a657d78a080243446d3ca6dae)
                check_type(argname="argument error_code", value=error_code, expected_type=type_hints["error_code"])
                check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if error_code is not None:
                self._values["error_code"] = error_code
            if message is not None:
                self._values["message"] = message

        @builtins.property
        def error_code(self) -> typing.Optional[builtins.str]:
            '''The failure code, if any, for a create or delete endpoint operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3outposts-endpoint-failedreason.html#cfn-s3outposts-endpoint-failedreason-errorcode
            '''
            result = self._values.get("error_code")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def message(self) -> typing.Optional[builtins.str]:
            '''Additional error details describing the endpoint failure and recommended action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3outposts-endpoint-failedreason.html#cfn-s3outposts-endpoint-failedreason-message
            '''
            result = self._values.get("message")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FailedReasonProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3outposts.mixins.CfnEndpointPropsMixin.NetworkInterfaceProperty",
        jsii_struct_bases=[],
        name_mapping={"network_interface_id": "networkInterfaceId"},
    )
    class NetworkInterfaceProperty:
        def __init__(
            self,
            *,
            network_interface_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The container for the network interface.

            :param network_interface_id: The ID for the network interface.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3outposts-endpoint-networkinterface.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3outposts import mixins as s3outposts_mixins
                
                network_interface_property = s3outposts_mixins.CfnEndpointPropsMixin.NetworkInterfaceProperty(
                    network_interface_id="networkInterfaceId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__99182f193b20052ec3e23616fe77830e7f6a7a872718274b524b2fb8ca0e79eb)
                check_type(argname="argument network_interface_id", value=network_interface_id, expected_type=type_hints["network_interface_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if network_interface_id is not None:
                self._values["network_interface_id"] = network_interface_id

        @builtins.property
        def network_interface_id(self) -> typing.Optional[builtins.str]:
            '''The ID for the network interface.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3outposts-endpoint-networkinterface.html#cfn-s3outposts-endpoint-networkinterface-networkinterfaceid
            '''
            result = self._values.get("network_interface_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NetworkInterfaceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnAccessPointMixinProps",
    "CfnAccessPointPropsMixin",
    "CfnBucketMixinProps",
    "CfnBucketPolicyMixinProps",
    "CfnBucketPolicyPropsMixin",
    "CfnBucketPropsMixin",
    "CfnEndpointMixinProps",
    "CfnEndpointPropsMixin",
]

publication.publish()

def _typecheckingstub__461e36dd2f2b960cc7523d5e3bed444873d1b211e622ed7aece0a8ff1f30c436(
    *,
    bucket: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    policy: typing.Any = None,
    vpc_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAccessPointPropsMixin.VpcConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05b78b9d2b4dc0ec23f35cc8c51f8bb2c80c01032e4050e6d99dc4856b406564(
    props: typing.Union[CfnAccessPointMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b76fd7c85824547a7833841c2e13b1d1e32d8d7314c0d00d0720e91487c67cf(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5745edb401983932e61c0af35d61c56d3e238fa82e76ed1f1d7bb91ef936fd1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c46939368cb8276066ff7186489a499f482b8ba10061ffc977df7a2a68a6daf(
    *,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fed3e07f928ecc7aa71609fb3ec54a08021c44a7b6c6f628744e146e00ce5550(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    lifecycle_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.LifecycleConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    outpost_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d34b2dea83be572be5f47d996f175fbcbcb026d5f4bd5481bf4f1fe007580a3(
    *,
    bucket: typing.Optional[builtins.str] = None,
    policy_document: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df979b27424226625cf0cab4d43db5ab57692d3bab49ecc4d97e6f98fe4d9cde(
    props: typing.Union[CfnBucketPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ac7b73945db89067714a28595e17032da8920afed26eb6c0e139b58a87e2478(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbbd28db56dfdac9a85c183fabab5063a35ef736d8bd25481eed844cd4988751(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43920ed55255fba7f0c95fbc8fa699cd896c7dee010830e7548ec7f08e986399(
    props: typing.Union[CfnBucketMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc86340ab50bf0dced0a3b812aef78847d1662f89cf40c7f5cfb6230584c598d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b416aba79c499f042f022f2aa8ccfceec2766a41fa7ca6b562053c5521752e89(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__367a4dd19d72cc0109b607d77ceb80e395004b232a644536dc2f121cc929a850(
    *,
    days_after_initiation: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9e96b84a339d0358f6387e74a9b2818f031ed675ecaa6ebd8c7e34c18909c49(
    *,
    rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.RuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf9a425b4bef4537588c16ecb8a38eb3266288249134472b1d9a539daae82496(
    *,
    abort_incomplete_multipart_upload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.AbortIncompleteMultipartUploadProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    expiration_date: typing.Optional[builtins.str] = None,
    expiration_in_days: typing.Optional[jsii.Number] = None,
    filter: typing.Any = None,
    id: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70ed83b8d095e6b8328fd1754d6e0d524bc8011fe91a71718c27a0eed4c32b7e(
    *,
    access_type: typing.Optional[builtins.str] = None,
    customer_owned_ipv4_pool: typing.Optional[builtins.str] = None,
    failed_reason: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEndpointPropsMixin.FailedReasonProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    outpost_id: typing.Optional[builtins.str] = None,
    security_group_id: typing.Optional[builtins.str] = None,
    subnet_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41f2448ac08b8b2faa8e54c49bb79642d87d4c67c47272335b6230709a8ed21a(
    props: typing.Union[CfnEndpointMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a9488f6207f856adf3c596aa69068f6223f32c09b0021d6a67dc3ac46377c54(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2269077fd8bd61b8583c9531906d1b91631160eec5b9f9ba420b5ad40ccde874(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1aec069c65ab9a5fe03afd032ae56c9b58af18a657d78a080243446d3ca6dae(
    *,
    error_code: typing.Optional[builtins.str] = None,
    message: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99182f193b20052ec3e23616fe77830e7f6a7a872718274b524b2fb8ca0e79eb(
    *,
    network_interface_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
