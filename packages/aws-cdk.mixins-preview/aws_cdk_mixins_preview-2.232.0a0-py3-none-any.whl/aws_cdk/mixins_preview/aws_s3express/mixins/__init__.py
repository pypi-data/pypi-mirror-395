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
    jsii_type="@aws-cdk/mixins-preview.aws_s3express.mixins.CfnAccessPointMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "bucket_account_id": "bucketAccountId",
        "name": "name",
        "policy": "policy",
        "public_access_block_configuration": "publicAccessBlockConfiguration",
        "scope": "scope",
        "tags": "tags",
        "vpc_configuration": "vpcConfiguration",
    },
)
class CfnAccessPointMixinProps:
    def __init__(
        self,
        *,
        bucket: typing.Optional[builtins.str] = None,
        bucket_account_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        policy: typing.Any = None,
        public_access_block_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAccessPointPropsMixin.PublicAccessBlockConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        scope: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAccessPointPropsMixin.ScopeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAccessPointPropsMixin.VpcConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnAccessPointPropsMixin.

        :param bucket: The name of the bucket that you want to associate the access point with.
        :param bucket_account_id: The AWS account ID that owns the bucket associated with this access point.
        :param name: An access point name consists of a base name you provide, followed by the zoneID ( AWS Local Zone) followed by the prefix ``--xa-s3`` . For example, accesspointname--zoneID--xa-s3.
        :param policy: The access point policy associated with the specified access point.
        :param public_access_block_configuration: Public access is blocked by default to access points for directory buckets.
        :param scope: You can use the access point scope to restrict access to specific prefixes, API operations, or a combination of both. For more information, see `Manage the scope of your access points for directory buckets. <https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-points-directory-buckets-manage-scope.html>`_
        :param tags: An array of tags that you can apply to access points. Tags are key-value pairs of metadata used to categorize your access points and control access. For more information, see `Using tags for attribute-based access control (ABAC) <https://docs.aws.amazon.com/AmazonS3/latest/userguide/tagging.html#using-tags-for-abac>`_ .
        :param vpc_configuration: If you include this field, Amazon S3 restricts access to this access point to requests from the specified virtual private cloud (VPC).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3express-accesspoint.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_s3express import mixins as s3express_mixins
            
            # policy: Any
            
            cfn_access_point_mixin_props = s3express_mixins.CfnAccessPointMixinProps(
                bucket="bucket",
                bucket_account_id="bucketAccountId",
                name="name",
                policy=policy,
                public_access_block_configuration=s3express_mixins.CfnAccessPointPropsMixin.PublicAccessBlockConfigurationProperty(
                    block_public_acls=False,
                    block_public_policy=False,
                    ignore_public_acls=False,
                    restrict_public_buckets=False
                ),
                scope=s3express_mixins.CfnAccessPointPropsMixin.ScopeProperty(
                    permissions=["permissions"],
                    prefixes=["prefixes"]
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vpc_configuration=s3express_mixins.CfnAccessPointPropsMixin.VpcConfigurationProperty(
                    vpc_id="vpcId"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be7e73dd333a9342e80591d8090b408f7af396e3bffab120ef39c46e7322e757)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument bucket_account_id", value=bucket_account_id, expected_type=type_hints["bucket_account_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument public_access_block_configuration", value=public_access_block_configuration, expected_type=type_hints["public_access_block_configuration"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc_configuration", value=vpc_configuration, expected_type=type_hints["vpc_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket is not None:
            self._values["bucket"] = bucket
        if bucket_account_id is not None:
            self._values["bucket_account_id"] = bucket_account_id
        if name is not None:
            self._values["name"] = name
        if policy is not None:
            self._values["policy"] = policy
        if public_access_block_configuration is not None:
            self._values["public_access_block_configuration"] = public_access_block_configuration
        if scope is not None:
            self._values["scope"] = scope
        if tags is not None:
            self._values["tags"] = tags
        if vpc_configuration is not None:
            self._values["vpc_configuration"] = vpc_configuration

    @builtins.property
    def bucket(self) -> typing.Optional[builtins.str]:
        '''The name of the bucket that you want to associate the access point with.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3express-accesspoint.html#cfn-s3express-accesspoint-bucket
        '''
        result = self._values.get("bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_account_id(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID that owns the bucket associated with this access point.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3express-accesspoint.html#cfn-s3express-accesspoint-bucketaccountid
        '''
        result = self._values.get("bucket_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''An access point name consists of a base name you provide, followed by the zoneID ( AWS Local Zone) followed by the prefix ``--xa-s3`` .

        For example, accesspointname--zoneID--xa-s3.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3express-accesspoint.html#cfn-s3express-accesspoint-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy(self) -> typing.Any:
        '''The access point policy associated with the specified access point.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3express-accesspoint.html#cfn-s3express-accesspoint-policy
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def public_access_block_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAccessPointPropsMixin.PublicAccessBlockConfigurationProperty"]]:
        '''Public access is blocked by default to access points for directory buckets.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3express-accesspoint.html#cfn-s3express-accesspoint-publicaccessblockconfiguration
        '''
        result = self._values.get("public_access_block_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAccessPointPropsMixin.PublicAccessBlockConfigurationProperty"]], result)

    @builtins.property
    def scope(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAccessPointPropsMixin.ScopeProperty"]]:
        '''You can use the access point scope to restrict access to specific prefixes, API operations, or a combination of both.

        For more information, see `Manage the scope of your access points for directory buckets. <https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-points-directory-buckets-manage-scope.html>`_

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3express-accesspoint.html#cfn-s3express-accesspoint-scope
        '''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAccessPointPropsMixin.ScopeProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of tags that you can apply to access points.

        Tags are key-value pairs of metadata used to categorize your access points and control access. For more information, see `Using tags for attribute-based access control (ABAC) <https://docs.aws.amazon.com/AmazonS3/latest/userguide/tagging.html#using-tags-for-abac>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3express-accesspoint.html#cfn-s3express-accesspoint-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def vpc_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAccessPointPropsMixin.VpcConfigurationProperty"]]:
        '''If you include this field, Amazon S3 restricts access to this access point to requests from the specified virtual private cloud (VPC).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3express-accesspoint.html#cfn-s3express-accesspoint-vpcconfiguration
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
    jsii_type="@aws-cdk/mixins-preview.aws_s3express.mixins.CfnAccessPointPropsMixin",
):
    '''Access points simplify managing data access at scale for shared datasets in Amazon S3 .

    Access points are unique hostnames you create to enforce distinct permissions and network controls for all requests made through an access point. You can create hundreds of access points per bucket, each with a distinct name and permissions customized for each application. Each access point works in conjunction with the bucket policy that is attached to the underlying bucket. For more information, see `Managing access to shared datasets in directory buckets with access points <https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-points-directory-buckets.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3express-accesspoint.html
    :cloudformationResource: AWS::S3Express::AccessPoint
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_s3express import mixins as s3express_mixins
        
        # policy: Any
        
        cfn_access_point_props_mixin = s3express_mixins.CfnAccessPointPropsMixin(s3express_mixins.CfnAccessPointMixinProps(
            bucket="bucket",
            bucket_account_id="bucketAccountId",
            name="name",
            policy=policy,
            public_access_block_configuration=s3express_mixins.CfnAccessPointPropsMixin.PublicAccessBlockConfigurationProperty(
                block_public_acls=False,
                block_public_policy=False,
                ignore_public_acls=False,
                restrict_public_buckets=False
            ),
            scope=s3express_mixins.CfnAccessPointPropsMixin.ScopeProperty(
                permissions=["permissions"],
                prefixes=["prefixes"]
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            vpc_configuration=s3express_mixins.CfnAccessPointPropsMixin.VpcConfigurationProperty(
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
        '''Create a mixin to apply properties to ``AWS::S3Express::AccessPoint``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__435a037703b82814e4af12b45a9b6358a24d36639fb4d203ef95521a92392c75)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d1ac1c31725219c4c13a58b263c7e826a707771dbc186039f853fcf18f03f48)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__393f5bc391614c0a9e6a6ec9cc7fca040053f3303a1e6c2c8e268c9554352219)
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
        jsii_type="@aws-cdk/mixins-preview.aws_s3express.mixins.CfnAccessPointPropsMixin.PublicAccessBlockConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "block_public_acls": "blockPublicAcls",
            "block_public_policy": "blockPublicPolicy",
            "ignore_public_acls": "ignorePublicAcls",
            "restrict_public_buckets": "restrictPublicBuckets",
        },
    )
    class PublicAccessBlockConfigurationProperty:
        def __init__(
            self,
            *,
            block_public_acls: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            block_public_policy: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            ignore_public_acls: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            restrict_public_buckets: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Public access is blocked by default to access points for directory buckets.

            :param block_public_acls: Specifies whether Amazon S3 should block public access control lists (ACLs) for this bucket and objects in this bucket. Setting this element to ``TRUE`` causes the following behavior: - PUT Bucket ACL and PUT Object ACL calls fail if the specified ACL is public. - PUT Object calls fail if the request includes a public ACL. - PUT Bucket calls fail if the request includes a public ACL. Enabling this setting doesn't affect existing policies or ACLs.
            :param block_public_policy: Specifies whether Amazon S3 should block public bucket policies for this bucket. Setting this element to ``TRUE`` causes Amazon S3 to reject calls to PUT Bucket policy if the specified bucket policy allows public access. Enabling this setting doesn't affect existing bucket policies.
            :param ignore_public_acls: Specifies whether Amazon S3 should ignore public ACLs for this bucket and objects in this bucket. Setting this element to ``TRUE`` causes Amazon S3 to ignore all public ACLs on this bucket and objects in this bucket. Enabling this setting doesn't affect the persistence of any existing ACLs and doesn't prevent new public ACLs from being set.
            :param restrict_public_buckets: Specifies whether Amazon S3 should restrict public bucket policies for this bucket. Setting this element to ``TRUE`` restricts access to this bucket to only AWS service principals and authorized users within this account if the bucket has a public policy. Enabling this setting doesn't affect previously stored bucket policies, except that public and cross-account access within any public bucket policy, including non-public delegation to specific accounts, is blocked.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3express-accesspoint-publicaccessblockconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3express import mixins as s3express_mixins
                
                public_access_block_configuration_property = s3express_mixins.CfnAccessPointPropsMixin.PublicAccessBlockConfigurationProperty(
                    block_public_acls=False,
                    block_public_policy=False,
                    ignore_public_acls=False,
                    restrict_public_buckets=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9c5199913c725b0905fe0303bb493f49f0391fdc1b37b07188be03e1504e7f62)
                check_type(argname="argument block_public_acls", value=block_public_acls, expected_type=type_hints["block_public_acls"])
                check_type(argname="argument block_public_policy", value=block_public_policy, expected_type=type_hints["block_public_policy"])
                check_type(argname="argument ignore_public_acls", value=ignore_public_acls, expected_type=type_hints["ignore_public_acls"])
                check_type(argname="argument restrict_public_buckets", value=restrict_public_buckets, expected_type=type_hints["restrict_public_buckets"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if block_public_acls is not None:
                self._values["block_public_acls"] = block_public_acls
            if block_public_policy is not None:
                self._values["block_public_policy"] = block_public_policy
            if ignore_public_acls is not None:
                self._values["ignore_public_acls"] = ignore_public_acls
            if restrict_public_buckets is not None:
                self._values["restrict_public_buckets"] = restrict_public_buckets

        @builtins.property
        def block_public_acls(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether Amazon S3 should block public access control lists (ACLs) for this bucket and objects in this bucket.

            Setting this element to ``TRUE`` causes the following behavior:

            - PUT Bucket ACL and PUT Object ACL calls fail if the specified ACL is public.
            - PUT Object calls fail if the request includes a public ACL.
            - PUT Bucket calls fail if the request includes a public ACL.

            Enabling this setting doesn't affect existing policies or ACLs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3express-accesspoint-publicaccessblockconfiguration.html#cfn-s3express-accesspoint-publicaccessblockconfiguration-blockpublicacls
            '''
            result = self._values.get("block_public_acls")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def block_public_policy(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether Amazon S3 should block public bucket policies for this bucket.

            Setting this element to ``TRUE`` causes Amazon S3 to reject calls to PUT Bucket policy if the specified bucket policy allows public access.

            Enabling this setting doesn't affect existing bucket policies.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3express-accesspoint-publicaccessblockconfiguration.html#cfn-s3express-accesspoint-publicaccessblockconfiguration-blockpublicpolicy
            '''
            result = self._values.get("block_public_policy")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def ignore_public_acls(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether Amazon S3 should ignore public ACLs for this bucket and objects in this bucket.

            Setting this element to ``TRUE`` causes Amazon S3 to ignore all public ACLs on this bucket and objects in this bucket.

            Enabling this setting doesn't affect the persistence of any existing ACLs and doesn't prevent new public ACLs from being set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3express-accesspoint-publicaccessblockconfiguration.html#cfn-s3express-accesspoint-publicaccessblockconfiguration-ignorepublicacls
            '''
            result = self._values.get("ignore_public_acls")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def restrict_public_buckets(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether Amazon S3 should restrict public bucket policies for this bucket.

            Setting this element to ``TRUE`` restricts access to this bucket to only AWS service principals and authorized users within this account if the bucket has a public policy.

            Enabling this setting doesn't affect previously stored bucket policies, except that public and cross-account access within any public bucket policy, including non-public delegation to specific accounts, is blocked.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3express-accesspoint-publicaccessblockconfiguration.html#cfn-s3express-accesspoint-publicaccessblockconfiguration-restrictpublicbuckets
            '''
            result = self._values.get("restrict_public_buckets")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PublicAccessBlockConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3express.mixins.CfnAccessPointPropsMixin.ScopeProperty",
        jsii_struct_bases=[],
        name_mapping={"permissions": "permissions", "prefixes": "prefixes"},
    )
    class ScopeProperty:
        def __init__(
            self,
            *,
            permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
            prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''You can use the access point scope to restrict access to specific prefixes, API operations, or a combination of both.

            For more information, see `Manage the scope of your access points for directory buckets. <https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-points-directory-buckets-manage-scope.html>`_

            :param permissions: You can include one or more API operations as permissions.
            :param prefixes: You can specify any amount of prefixes, but the total length of characters of all prefixes must be less than 256 bytes in size.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3express-accesspoint-scope.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3express import mixins as s3express_mixins
                
                scope_property = s3express_mixins.CfnAccessPointPropsMixin.ScopeProperty(
                    permissions=["permissions"],
                    prefixes=["prefixes"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4f67aa87849a2d4ec5199533690e1a2e4c9851417b8d620c527d0d8e5860e551)
                check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
                check_type(argname="argument prefixes", value=prefixes, expected_type=type_hints["prefixes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if permissions is not None:
                self._values["permissions"] = permissions
            if prefixes is not None:
                self._values["prefixes"] = prefixes

        @builtins.property
        def permissions(self) -> typing.Optional[typing.List[builtins.str]]:
            '''You can include one or more API operations as permissions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3express-accesspoint-scope.html#cfn-s3express-accesspoint-scope-permissions
            '''
            result = self._values.get("permissions")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
            '''You can specify any amount of prefixes, but the total length of characters of all prefixes must be less than 256 bytes in size.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3express-accesspoint-scope.html#cfn-s3express-accesspoint-scope-prefixes
            '''
            result = self._values.get("prefixes")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScopeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3express.mixins.CfnAccessPointPropsMixin.VpcConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"vpc_id": "vpcId"},
    )
    class VpcConfigurationProperty:
        def __init__(self, *, vpc_id: typing.Optional[builtins.str] = None) -> None:
            '''The Virtual Private Cloud (VPC) configuration for a bucket access point.

            :param vpc_id: If this field is specified, this access point will only allow connections from the specified VPC ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3express-accesspoint-vpcconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3express import mixins as s3express_mixins
                
                vpc_configuration_property = s3express_mixins.CfnAccessPointPropsMixin.VpcConfigurationProperty(
                    vpc_id="vpcId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9a77ef7d79f83b5c468bdeaba609779389ab16bbd41b81d4f1c96a4ecdb4998d)
                check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if vpc_id is not None:
                self._values["vpc_id"] = vpc_id

        @builtins.property
        def vpc_id(self) -> typing.Optional[builtins.str]:
            '''If this field is specified, this access point will only allow connections from the specified VPC ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3express-accesspoint-vpcconfiguration.html#cfn-s3express-accesspoint-vpcconfiguration-vpcid
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
    jsii_type="@aws-cdk/mixins-preview.aws_s3express.mixins.CfnBucketPolicyMixinProps",
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

        :param bucket: The name of the S3 directory bucket to which the policy applies.
        :param policy_document: A policy document containing permissions to add to the specified bucket. In IAM, you must provide policy documents in JSON format. However, in CloudFormation you can provide the policy in JSON or YAML format because CloudFormation converts YAML to JSON before submitting it to IAM. For more information, see the AWS::IAM::Policy `PolicyDocument <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-policydocument>`_ resource description in this guide and `Policies and Permissions in Amazon S3 <https://docs.aws.amazon.com/AmazonS3/latest/dev/access-policy-language-overview.html>`_ in the *Amazon S3 User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3express-bucketpolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_s3express import mixins as s3express_mixins
            
            # policy_document: Any
            
            cfn_bucket_policy_mixin_props = s3express_mixins.CfnBucketPolicyMixinProps(
                bucket="bucket",
                policy_document=policy_document
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9b6748888b18f86ecdef864c8d8c67caf9c22365352fc1eb813c8f127f5403a)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument policy_document", value=policy_document, expected_type=type_hints["policy_document"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket is not None:
            self._values["bucket"] = bucket
        if policy_document is not None:
            self._values["policy_document"] = policy_document

    @builtins.property
    def bucket(self) -> typing.Optional[builtins.str]:
        '''The name of the S3 directory bucket to which the policy applies.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3express-bucketpolicy.html#cfn-s3express-bucketpolicy-bucket
        '''
        result = self._values.get("bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_document(self) -> typing.Any:
        '''A policy document containing permissions to add to the specified bucket.

        In IAM, you must provide policy documents in JSON format. However, in CloudFormation you can provide the policy in JSON or YAML format because CloudFormation converts YAML to JSON before submitting it to IAM. For more information, see the AWS::IAM::Policy `PolicyDocument <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-policydocument>`_ resource description in this guide and `Policies and Permissions in Amazon S3 <https://docs.aws.amazon.com/AmazonS3/latest/dev/access-policy-language-overview.html>`_ in the *Amazon S3 User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3express-bucketpolicy.html#cfn-s3express-bucketpolicy-policydocument
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
    jsii_type="@aws-cdk/mixins-preview.aws_s3express.mixins.CfnBucketPolicyPropsMixin",
):
    '''The ``AWS::S3Express::BucketPolicy`` resource defines an Amazon S3 bucket policy to an Amazon S3 directory bucket.

    - **Permissions** - If you are using an identity other than the root user of the AWS account that owns the bucket, the calling identity must both have the required permissions on the specified bucket and belong to the bucket owner's account in order to use this operation. For more information about directory bucket policies and permissions, see `AWS Identity and Access Management (IAM) for S3 Express One Zone <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-express-security-iam.html>`_ in the *Amazon S3 User Guide* .

    .. epigraph::

       To ensure that bucket owners don't inadvertently lock themselves out of their own buckets, the root principal in a bucket owner's AWS account can perform the ``GetBucketPolicy`` , ``PutBucketPolicy`` , and ``DeleteBucketPolicy`` API actions, even if their bucket policy explicitly denies the root principal's access. Bucket owner root principals can only be blocked from performing these API actions by VPC endpoint policies and AWS Organizations policies.

    The required permissions for CloudFormation to use are based on the operations that are performed on the stack.

    - Create
    - s3express:GetBucketPolicy
    - s3express:PutBucketPolicy
    - Read
    - s3express:GetBucketPolicy
    - Update
    - s3express:GetBucketPolicy
    - s3express:PutBucketPolicy
    - Delete
    - s3express:GetBucketPolicy
    - s3express:DeleteBucketPolicy
    - List
    - s3express:GetBucketPolicy
    - s3express:ListAllMyDirectoryBuckets

    For more information about example bucket policies, see `Example bucket policies for S3 Express One Zone <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-express-security-iam-example-bucket-policies.html>`_ in the *Amazon S3 User Guide* .

    The following operations are related to ``AWS::S3Express::BucketPolicy`` :

    - `PutBucketPolicy <https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutBucketPolicy.html>`_
    - `GetBucketPolicy <https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetBucketPolicy.html>`_
    - `DeleteBucketPolicy <https://docs.aws.amazon.com/AmazonS3/latest/API/API_DeleteBucketPolicy.html>`_
    - `ListDirectoryBuckets <https://docs.aws.amazon.com/AmazonS3/latest/API/API_ListDirectoryBuckets.html>`_

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3express-bucketpolicy.html
    :cloudformationResource: AWS::S3Express::BucketPolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_s3express import mixins as s3express_mixins
        
        # policy_document: Any
        
        cfn_bucket_policy_props_mixin = s3express_mixins.CfnBucketPolicyPropsMixin(s3express_mixins.CfnBucketPolicyMixinProps(
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
        '''Create a mixin to apply properties to ``AWS::S3Express::BucketPolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__988db520962cef371e5f946d70ee0f5ad0da0820b41e9f314f731351de35bb0c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7abfa2882583991246d9514cde8138b37be9af7a4d130a5ab9e2c9293615cae4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45f6c804d0bde61ac7fdd0937521abf381a2e3953ec2a7f4124cfd951a72f8dd)
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


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_s3express.mixins.CfnDirectoryBucketMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_encryption": "bucketEncryption",
        "bucket_name": "bucketName",
        "data_redundancy": "dataRedundancy",
        "lifecycle_configuration": "lifecycleConfiguration",
        "location_name": "locationName",
        "tags": "tags",
    },
)
class CfnDirectoryBucketMixinProps:
    def __init__(
        self,
        *,
        bucket_encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDirectoryBucketPropsMixin.BucketEncryptionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        bucket_name: typing.Optional[builtins.str] = None,
        data_redundancy: typing.Optional[builtins.str] = None,
        lifecycle_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDirectoryBucketPropsMixin.LifecycleConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        location_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDirectoryBucketPropsMixin.

        :param bucket_encryption: Specifies default encryption for a bucket using server-side encryption with Amazon S3 managed keys (SSE-S3) or AWS KMS keys (SSE-KMS). For information about default encryption for directory buckets, see `Setting and monitoring default encryption for directory buckets <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-express-bucket-encryption.html>`_ in the *Amazon S3 User Guide* .
        :param bucket_name: A name for the bucket. The bucket name must contain only lowercase letters, numbers, and hyphens (-). A directory bucket name must be unique in the chosen Zone (Availability Zone or Local Zone). The bucket name must also follow the format ``*bucket_base_name* -- *zone_id* --x-s3`` (for example, ``*bucket_base_name* -- *usw2-az1* --x-s3`` ). If you don't specify a name, AWS CloudFormation generates a unique ID and uses that ID for the bucket name. For information about bucket naming restrictions, see `Directory bucket naming rules <https://docs.aws.amazon.com/AmazonS3/latest/userguide/directory-bucket-naming-rules.html>`_ in the *Amazon S3 User Guide* . .. epigraph:: If you specify a name, you can't perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you need to replace the resource, specify a new name.
        :param data_redundancy: The number of Zone (Availability Zone or Local Zone) that's used for redundancy for the bucket.
        :param lifecycle_configuration: Container for lifecycle rules. You can add as many as 1000 rules. For more information see, `Creating and managing a lifecycle configuration for directory buckets <https://docs.aws.amazon.com/AmazonS3/latest/userguide/directory-buckets-objects-lifecycle.html>`_ in the *Amazon S3 User Guide* .
        :param location_name: The name of the location where the bucket will be created. For directory buckets, the name of the location is the Zone ID of the Availability Zone (AZ) or Local Zone (LZ) where the bucket will be created. An example AZ ID value is ``usw2-az1`` .
        :param tags: An array of tags that you can apply to the S3 directory bucket. Tags are key-value pairs of metadata used to categorize and organize your buckets, track costs, and control access. For more information, see `Using tags with directory buckets <https://docs.aws.amazon.com/AmazonS3/latest/userguide/directory-buckets-tagging.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3express-directorybucket.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_s3express import mixins as s3express_mixins
            
            cfn_directory_bucket_mixin_props = s3express_mixins.CfnDirectoryBucketMixinProps(
                bucket_encryption=s3express_mixins.CfnDirectoryBucketPropsMixin.BucketEncryptionProperty(
                    server_side_encryption_configuration=[s3express_mixins.CfnDirectoryBucketPropsMixin.ServerSideEncryptionRuleProperty(
                        bucket_key_enabled=False,
                        server_side_encryption_by_default=s3express_mixins.CfnDirectoryBucketPropsMixin.ServerSideEncryptionByDefaultProperty(
                            kms_master_key_id="kmsMasterKeyId",
                            sse_algorithm="sseAlgorithm"
                        )
                    )]
                ),
                bucket_name="bucketName",
                data_redundancy="dataRedundancy",
                lifecycle_configuration=s3express_mixins.CfnDirectoryBucketPropsMixin.LifecycleConfigurationProperty(
                    rules=[s3express_mixins.CfnDirectoryBucketPropsMixin.RuleProperty(
                        abort_incomplete_multipart_upload=s3express_mixins.CfnDirectoryBucketPropsMixin.AbortIncompleteMultipartUploadProperty(
                            days_after_initiation=123
                        ),
                        expiration_in_days=123,
                        id="id",
                        object_size_greater_than="objectSizeGreaterThan",
                        object_size_less_than="objectSizeLessThan",
                        prefix="prefix",
                        status="status"
                    )]
                ),
                location_name="locationName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d5dddf6cc814065ba5a6cab38c6d1de04bd333773f2688fe3e570711b471873)
            check_type(argname="argument bucket_encryption", value=bucket_encryption, expected_type=type_hints["bucket_encryption"])
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument data_redundancy", value=data_redundancy, expected_type=type_hints["data_redundancy"])
            check_type(argname="argument lifecycle_configuration", value=lifecycle_configuration, expected_type=type_hints["lifecycle_configuration"])
            check_type(argname="argument location_name", value=location_name, expected_type=type_hints["location_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_encryption is not None:
            self._values["bucket_encryption"] = bucket_encryption
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if data_redundancy is not None:
            self._values["data_redundancy"] = data_redundancy
        if lifecycle_configuration is not None:
            self._values["lifecycle_configuration"] = lifecycle_configuration
        if location_name is not None:
            self._values["location_name"] = location_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def bucket_encryption(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDirectoryBucketPropsMixin.BucketEncryptionProperty"]]:
        '''Specifies default encryption for a bucket using server-side encryption with Amazon S3 managed keys (SSE-S3) or AWS KMS keys (SSE-KMS).

        For information about default encryption for directory buckets, see `Setting and monitoring default encryption for directory buckets <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-express-bucket-encryption.html>`_ in the *Amazon S3 User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3express-directorybucket.html#cfn-s3express-directorybucket-bucketencryption
        '''
        result = self._values.get("bucket_encryption")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDirectoryBucketPropsMixin.BucketEncryptionProperty"]], result)

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''A name for the bucket.

        The bucket name must contain only lowercase letters, numbers, and hyphens (-). A directory bucket name must be unique in the chosen Zone (Availability Zone or Local Zone). The bucket name must also follow the format ``*bucket_base_name* -- *zone_id* --x-s3`` (for example, ``*bucket_base_name* -- *usw2-az1* --x-s3`` ). If you don't specify a name, AWS CloudFormation generates a unique ID and uses that ID for the bucket name. For information about bucket naming restrictions, see `Directory bucket naming rules <https://docs.aws.amazon.com/AmazonS3/latest/userguide/directory-bucket-naming-rules.html>`_ in the *Amazon S3 User Guide* .
        .. epigraph::

           If you specify a name, you can't perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you need to replace the resource, specify a new name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3express-directorybucket.html#cfn-s3express-directorybucket-bucketname
        '''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_redundancy(self) -> typing.Optional[builtins.str]:
        '''The number of Zone (Availability Zone or Local Zone) that's used for redundancy for the bucket.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3express-directorybucket.html#cfn-s3express-directorybucket-dataredundancy
        '''
        result = self._values.get("data_redundancy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lifecycle_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDirectoryBucketPropsMixin.LifecycleConfigurationProperty"]]:
        '''Container for lifecycle rules. You can add as many as 1000 rules.

        For more information see, `Creating and managing a lifecycle configuration for directory buckets <https://docs.aws.amazon.com/AmazonS3/latest/userguide/directory-buckets-objects-lifecycle.html>`_ in the *Amazon S3 User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3express-directorybucket.html#cfn-s3express-directorybucket-lifecycleconfiguration
        '''
        result = self._values.get("lifecycle_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDirectoryBucketPropsMixin.LifecycleConfigurationProperty"]], result)

    @builtins.property
    def location_name(self) -> typing.Optional[builtins.str]:
        '''The name of the location where the bucket will be created.

        For directory buckets, the name of the location is the Zone ID of the Availability Zone (AZ) or Local Zone (LZ) where the bucket will be created. An example AZ ID value is ``usw2-az1`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3express-directorybucket.html#cfn-s3express-directorybucket-locationname
        '''
        result = self._values.get("location_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of tags that you can apply to the S3 directory bucket.

        Tags are key-value pairs of metadata used to categorize and organize your buckets, track costs, and control access. For more information, see `Using tags with directory buckets <https://docs.aws.amazon.com/AmazonS3/latest/userguide/directory-buckets-tagging.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3express-directorybucket.html#cfn-s3express-directorybucket-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDirectoryBucketMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDirectoryBucketPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_s3express.mixins.CfnDirectoryBucketPropsMixin",
):
    '''The ``AWS::S3Express::DirectoryBucket`` resource defines an Amazon S3 directory bucket in the same AWS Region where you create the AWS CloudFormation stack.

    To control how AWS CloudFormation handles the bucket when the stack is deleted, you can set a deletion policy for your bucket. You can choose to *retain* the bucket or to *delete* the bucket. For more information, see `DeletionPolicy attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-deletionpolicy.html>`_ .
    .. epigraph::

       You can only delete empty buckets. Deletion fails for buckets that have contents.

    - **Permissions** - The required permissions for CloudFormation to use are based on the operations that are performed on the stack.
    - Create
    - s3express:CreateBucket
    - s3express:ListAllMyDirectoryBuckets
    - Read
    - s3express:ListAllMyDirectoryBuckets
    - ec2:DescribeAvailabilityZones
    - Delete
    - s3express:DeleteBucket
    - s3express:ListAllMyDirectoryBuckets
    - List
    - s3express:ListAllMyDirectoryBuckets
    - PutBucketEncryption
    - s3express:PutEncryptionConfiguration
    - To set a directory bucket default encryption with SSE-KMS, you must also have the kms:GenerateDataKey and kms:Decrypt permissions in IAM identity-based policies and AWS KMS key policies for the target AWS KMS key.
    - GetBucketEncryption
    - s3express:GetBucketEncryption
    - DeleteBucketEncryption
    - s3express:PutEncryptionConfiguration

    The following operations are related to ``AWS::S3Express::DirectoryBucket`` :

    - `CreateBucket <https://docs.aws.amazon.com/AmazonS3/latest/API/API_CreateBucket.html>`_
    - `ListDirectoryBuckets <https://docs.aws.amazon.com/AmazonS3/latest/API/API_ListDirectoryBuckets.html>`_
    - `DeleteBucket <https://docs.aws.amazon.com/AmazonS3/latest/API/API_DeleteBucket.html>`_

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3express-directorybucket.html
    :cloudformationResource: AWS::S3Express::DirectoryBucket
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_s3express import mixins as s3express_mixins
        
        cfn_directory_bucket_props_mixin = s3express_mixins.CfnDirectoryBucketPropsMixin(s3express_mixins.CfnDirectoryBucketMixinProps(
            bucket_encryption=s3express_mixins.CfnDirectoryBucketPropsMixin.BucketEncryptionProperty(
                server_side_encryption_configuration=[s3express_mixins.CfnDirectoryBucketPropsMixin.ServerSideEncryptionRuleProperty(
                    bucket_key_enabled=False,
                    server_side_encryption_by_default=s3express_mixins.CfnDirectoryBucketPropsMixin.ServerSideEncryptionByDefaultProperty(
                        kms_master_key_id="kmsMasterKeyId",
                        sse_algorithm="sseAlgorithm"
                    )
                )]
            ),
            bucket_name="bucketName",
            data_redundancy="dataRedundancy",
            lifecycle_configuration=s3express_mixins.CfnDirectoryBucketPropsMixin.LifecycleConfigurationProperty(
                rules=[s3express_mixins.CfnDirectoryBucketPropsMixin.RuleProperty(
                    abort_incomplete_multipart_upload=s3express_mixins.CfnDirectoryBucketPropsMixin.AbortIncompleteMultipartUploadProperty(
                        days_after_initiation=123
                    ),
                    expiration_in_days=123,
                    id="id",
                    object_size_greater_than="objectSizeGreaterThan",
                    object_size_less_than="objectSizeLessThan",
                    prefix="prefix",
                    status="status"
                )]
            ),
            location_name="locationName",
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
        props: typing.Union[CfnDirectoryBucketMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::S3Express::DirectoryBucket``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__306087ce0d958a42a41ebbf44f3067ff1afb06d43866cc35c97d01d9e3e8fc85)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ceb2d73ddfde02d7895f17c3ad793468199234d9fb5d74bd0d6ff7a98e3b5b7e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4db982765e7d4e62eaa41c1977e79178111e4dec05b4702cba1d889bf7c26c42)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDirectoryBucketMixinProps:
        return typing.cast(CfnDirectoryBucketMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3express.mixins.CfnDirectoryBucketPropsMixin.AbortIncompleteMultipartUploadProperty",
        jsii_struct_bases=[],
        name_mapping={"days_after_initiation": "daysAfterInitiation"},
    )
    class AbortIncompleteMultipartUploadProperty:
        def __init__(
            self,
            *,
            days_after_initiation: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies the days since the initiation of an incomplete multipart upload that Amazon S3 will wait before permanently removing all parts of the upload.

            For more information, see `Aborting Incomplete Multipart Uploads Using a Bucket Lifecycle Configuration <https://docs.aws.amazon.com/AmazonS3/latest/dev/mpuoverview.html#mpu-abort-incomplete-mpu-lifecycle-config>`_ in the *Amazon S3 User Guide* .

            :param days_after_initiation: Specifies the number of days after which Amazon S3 aborts an incomplete multipart upload.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3express-directorybucket-abortincompletemultipartupload.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3express import mixins as s3express_mixins
                
                abort_incomplete_multipart_upload_property = s3express_mixins.CfnDirectoryBucketPropsMixin.AbortIncompleteMultipartUploadProperty(
                    days_after_initiation=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__749a7f16ab9b43633857462b788a161317fb70a78db91df4f43face6e1bea144)
                check_type(argname="argument days_after_initiation", value=days_after_initiation, expected_type=type_hints["days_after_initiation"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if days_after_initiation is not None:
                self._values["days_after_initiation"] = days_after_initiation

        @builtins.property
        def days_after_initiation(self) -> typing.Optional[jsii.Number]:
            '''Specifies the number of days after which Amazon S3 aborts an incomplete multipart upload.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3express-directorybucket-abortincompletemultipartupload.html#cfn-s3express-directorybucket-abortincompletemultipartupload-daysafterinitiation
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
        jsii_type="@aws-cdk/mixins-preview.aws_s3express.mixins.CfnDirectoryBucketPropsMixin.BucketEncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "server_side_encryption_configuration": "serverSideEncryptionConfiguration",
        },
    )
    class BucketEncryptionProperty:
        def __init__(
            self,
            *,
            server_side_encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDirectoryBucketPropsMixin.ServerSideEncryptionRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Specifies default encryption for a bucket using server-side encryption with Amazon S3 managed keys (SSE-S3) or AWS KMS keys (SSE-KMS).

            For information about default encryption for directory buckets, see `Setting and monitoring default encryption for directory buckets <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-express-bucket-encryption.html>`_ in the *Amazon S3 User Guide* .

            :param server_side_encryption_configuration: Specifies the default server-side-encryption configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3express-directorybucket-bucketencryption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3express import mixins as s3express_mixins
                
                bucket_encryption_property = s3express_mixins.CfnDirectoryBucketPropsMixin.BucketEncryptionProperty(
                    server_side_encryption_configuration=[s3express_mixins.CfnDirectoryBucketPropsMixin.ServerSideEncryptionRuleProperty(
                        bucket_key_enabled=False,
                        server_side_encryption_by_default=s3express_mixins.CfnDirectoryBucketPropsMixin.ServerSideEncryptionByDefaultProperty(
                            kms_master_key_id="kmsMasterKeyId",
                            sse_algorithm="sseAlgorithm"
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__39caeff27209703b6493924e003201ff22a5be78c250d92a73a23e01dbdf8e1a)
                check_type(argname="argument server_side_encryption_configuration", value=server_side_encryption_configuration, expected_type=type_hints["server_side_encryption_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if server_side_encryption_configuration is not None:
                self._values["server_side_encryption_configuration"] = server_side_encryption_configuration

        @builtins.property
        def server_side_encryption_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDirectoryBucketPropsMixin.ServerSideEncryptionRuleProperty"]]]]:
            '''Specifies the default server-side-encryption configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3express-directorybucket-bucketencryption.html#cfn-s3express-directorybucket-bucketencryption-serversideencryptionconfiguration
            '''
            result = self._values.get("server_side_encryption_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDirectoryBucketPropsMixin.ServerSideEncryptionRuleProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BucketEncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3express.mixins.CfnDirectoryBucketPropsMixin.LifecycleConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"rules": "rules"},
    )
    class LifecycleConfigurationProperty:
        def __init__(
            self,
            *,
            rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDirectoryBucketPropsMixin.RuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Container for lifecycle rules. You can add as many as 1000 rules.

            For more information see, `Creating and managing a lifecycle configuration for directory buckets <https://docs.aws.amazon.com/AmazonS3/latest/userguide/directory-buckets-objects-lifecycle.html>`_ in the *Amazon S3 User Guide* .

            :param rules: A lifecycle rule for individual objects in an Amazon S3 Express bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3express-directorybucket-lifecycleconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3express import mixins as s3express_mixins
                
                lifecycle_configuration_property = s3express_mixins.CfnDirectoryBucketPropsMixin.LifecycleConfigurationProperty(
                    rules=[s3express_mixins.CfnDirectoryBucketPropsMixin.RuleProperty(
                        abort_incomplete_multipart_upload=s3express_mixins.CfnDirectoryBucketPropsMixin.AbortIncompleteMultipartUploadProperty(
                            days_after_initiation=123
                        ),
                        expiration_in_days=123,
                        id="id",
                        object_size_greater_than="objectSizeGreaterThan",
                        object_size_less_than="objectSizeLessThan",
                        prefix="prefix",
                        status="status"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__18f3c219cd561244807756baf8ac1d16c10374e2934d913daef8f587c1d7fa99)
                check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if rules is not None:
                self._values["rules"] = rules

        @builtins.property
        def rules(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDirectoryBucketPropsMixin.RuleProperty"]]]]:
            '''A lifecycle rule for individual objects in an Amazon S3 Express bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3express-directorybucket-lifecycleconfiguration.html#cfn-s3express-directorybucket-lifecycleconfiguration-rules
            '''
            result = self._values.get("rules")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDirectoryBucketPropsMixin.RuleProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LifecycleConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3express.mixins.CfnDirectoryBucketPropsMixin.RuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "abort_incomplete_multipart_upload": "abortIncompleteMultipartUpload",
            "expiration_in_days": "expirationInDays",
            "id": "id",
            "object_size_greater_than": "objectSizeGreaterThan",
            "object_size_less_than": "objectSizeLessThan",
            "prefix": "prefix",
            "status": "status",
        },
    )
    class RuleProperty:
        def __init__(
            self,
            *,
            abort_incomplete_multipart_upload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDirectoryBucketPropsMixin.AbortIncompleteMultipartUploadProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            expiration_in_days: typing.Optional[jsii.Number] = None,
            id: typing.Optional[builtins.str] = None,
            object_size_greater_than: typing.Optional[builtins.str] = None,
            object_size_less_than: typing.Optional[builtins.str] = None,
            prefix: typing.Optional[builtins.str] = None,
            status: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies lifecycle rules for an Amazon S3 bucket.

            For more information, see `Put Bucket Lifecycle Configuration <https://docs.aws.amazon.com/AmazonS3/latest/API/RESTBucketPUTlifecycle.html>`_ in the *Amazon S3 API Reference* . For examples, see `Put Bucket Lifecycle Configuration Examples <https://docs.aws.amazon.com//AmazonS3/latest/API/API_PutBucketLifecycleConfiguration.html#API_PutBucketLifecycleConfiguration_Examples>`_ .

            You must specify at least one of the following properties: ``AbortIncompleteMultipartUpload`` , or ``ExpirationInDays`` .

            :param abort_incomplete_multipart_upload: Specifies the days since the initiation of an incomplete multipart upload that Amazon S3 will wait before permanently removing all parts of the upload.
            :param expiration_in_days: Indicates the number of days after creation when objects are deleted from Amazon S3 and Amazon S3 Glacier. If you specify an expiration and transition time, you must use the same time unit for both properties (either in days or by date). The expiration time must also be later than the transition time.
            :param id: Unique identifier for the rule. The value can't be longer than 255 characters.
            :param object_size_greater_than: Specifies the minimum object size in bytes for this rule to apply to. Objects must be larger than this value in bytes. For more information about size based rules, see `Lifecycle configuration using size-based rules <https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-configuration-examples.html#lc-size-rules>`_ in the *Amazon S3 User Guide* .
            :param object_size_less_than: Specifies the maximum object size in bytes for this rule to apply to. Objects must be smaller than this value in bytes. For more information about sized based rules, see `Lifecycle configuration using size-based rules <https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-configuration-examples.html#lc-size-rules>`_ in the *Amazon S3 User Guide* .
            :param prefix: Object key prefix that identifies one or more objects to which this rule applies. .. epigraph:: Replacement must be made for object keys containing special characters (such as carriage returns) when using XML requests. For more information, see `XML related object key constraints <https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-keys.html#object-key-xml-related-constraints>`_ .
            :param status: If ``Enabled`` , the rule is currently being applied. If ``Disabled`` , the rule is not currently being applied.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3express-directorybucket-rule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3express import mixins as s3express_mixins
                
                rule_property = s3express_mixins.CfnDirectoryBucketPropsMixin.RuleProperty(
                    abort_incomplete_multipart_upload=s3express_mixins.CfnDirectoryBucketPropsMixin.AbortIncompleteMultipartUploadProperty(
                        days_after_initiation=123
                    ),
                    expiration_in_days=123,
                    id="id",
                    object_size_greater_than="objectSizeGreaterThan",
                    object_size_less_than="objectSizeLessThan",
                    prefix="prefix",
                    status="status"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__106739c0f4ef55fee0345e2c005dd1434f8400b13dfd6693af2a9a80304d1105)
                check_type(argname="argument abort_incomplete_multipart_upload", value=abort_incomplete_multipart_upload, expected_type=type_hints["abort_incomplete_multipart_upload"])
                check_type(argname="argument expiration_in_days", value=expiration_in_days, expected_type=type_hints["expiration_in_days"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument object_size_greater_than", value=object_size_greater_than, expected_type=type_hints["object_size_greater_than"])
                check_type(argname="argument object_size_less_than", value=object_size_less_than, expected_type=type_hints["object_size_less_than"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if abort_incomplete_multipart_upload is not None:
                self._values["abort_incomplete_multipart_upload"] = abort_incomplete_multipart_upload
            if expiration_in_days is not None:
                self._values["expiration_in_days"] = expiration_in_days
            if id is not None:
                self._values["id"] = id
            if object_size_greater_than is not None:
                self._values["object_size_greater_than"] = object_size_greater_than
            if object_size_less_than is not None:
                self._values["object_size_less_than"] = object_size_less_than
            if prefix is not None:
                self._values["prefix"] = prefix
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def abort_incomplete_multipart_upload(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDirectoryBucketPropsMixin.AbortIncompleteMultipartUploadProperty"]]:
            '''Specifies the days since the initiation of an incomplete multipart upload that Amazon S3 will wait before permanently removing all parts of the upload.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3express-directorybucket-rule.html#cfn-s3express-directorybucket-rule-abortincompletemultipartupload
            '''
            result = self._values.get("abort_incomplete_multipart_upload")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDirectoryBucketPropsMixin.AbortIncompleteMultipartUploadProperty"]], result)

        @builtins.property
        def expiration_in_days(self) -> typing.Optional[jsii.Number]:
            '''Indicates the number of days after creation when objects are deleted from Amazon S3 and Amazon S3 Glacier.

            If you specify an expiration and transition time, you must use the same time unit for both properties (either in days or by date). The expiration time must also be later than the transition time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3express-directorybucket-rule.html#cfn-s3express-directorybucket-rule-expirationindays
            '''
            result = self._values.get("expiration_in_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''Unique identifier for the rule.

            The value can't be longer than 255 characters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3express-directorybucket-rule.html#cfn-s3express-directorybucket-rule-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def object_size_greater_than(self) -> typing.Optional[builtins.str]:
            '''Specifies the minimum object size in bytes for this rule to apply to.

            Objects must be larger than this value in bytes. For more information about size based rules, see `Lifecycle configuration using size-based rules <https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-configuration-examples.html#lc-size-rules>`_ in the *Amazon S3 User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3express-directorybucket-rule.html#cfn-s3express-directorybucket-rule-objectsizegreaterthan
            '''
            result = self._values.get("object_size_greater_than")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def object_size_less_than(self) -> typing.Optional[builtins.str]:
            '''Specifies the maximum object size in bytes for this rule to apply to.

            Objects must be smaller than this value in bytes. For more information about sized based rules, see `Lifecycle configuration using size-based rules <https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-configuration-examples.html#lc-size-rules>`_ in the *Amazon S3 User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3express-directorybucket-rule.html#cfn-s3express-directorybucket-rule-objectsizelessthan
            '''
            result = self._values.get("object_size_less_than")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''Object key prefix that identifies one or more objects to which this rule applies.

            .. epigraph::

               Replacement must be made for object keys containing special characters (such as carriage returns) when using XML requests. For more information, see `XML related object key constraints <https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-keys.html#object-key-xml-related-constraints>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3express-directorybucket-rule.html#cfn-s3express-directorybucket-rule-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''If ``Enabled`` , the rule is currently being applied.

            If ``Disabled`` , the rule is not currently being applied.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3express-directorybucket-rule.html#cfn-s3express-directorybucket-rule-status
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
        jsii_type="@aws-cdk/mixins-preview.aws_s3express.mixins.CfnDirectoryBucketPropsMixin.ServerSideEncryptionByDefaultProperty",
        jsii_struct_bases=[],
        name_mapping={
            "kms_master_key_id": "kmsMasterKeyId",
            "sse_algorithm": "sseAlgorithm",
        },
    )
    class ServerSideEncryptionByDefaultProperty:
        def __init__(
            self,
            *,
            kms_master_key_id: typing.Optional[builtins.str] = None,
            sse_algorithm: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the default server-side encryption to apply to new objects in the bucket.

            If a PUT Object request doesn't specify any server-side encryption, this default encryption will be applied. For more information, see `PutBucketEncryption <https://docs.aws.amazon.com/AmazonS3/latest/API/RESTBucketPUTencryption.html>`_ in the *Amazon S3 API Reference* .

            :param kms_master_key_id: AWS Key Management Service (KMS) customer managed key ID to use for the default encryption. This parameter is allowed only if ``SSEAlgorithm`` is set to ``aws:kms`` . You can specify this parameter with the key ID or the Amazon Resource Name (ARN) of the KMS key. You can’t use the key alias of the KMS key. - Key ID: ``1234abcd-12ab-34cd-56ef-1234567890ab`` - Key ARN: ``arn:aws:kms:us-east-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab`` If you are using encryption with cross-account or AWS service operations, you must use a fully qualified KMS key ARN. For more information, see `Using encryption for cross-account operations <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-express-bucket-encryption.html#s3-express-bucket-encryption-update-bucket-policy>`_ . .. epigraph:: Your SSE-KMS configuration can only support 1 `customer managed key <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#customer-cmk>`_ per directory bucket for the lifetime of the bucket. `AWS managed key <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#aws-managed-cmk>`_ ( ``aws/s3`` ) isn't supported. Also, after you specify a customer managed key for SSE-KMS and upload objects with this configuration, you can't override the customer managed key for your SSE-KMS configuration. To use a new customer manager key for your data, we recommend copying your existing objects to a new directory bucket with a new customer managed key. > Amazon S3 only supports symmetric encryption KMS keys. For more information, see `Asymmetric keys in AWS KMS <https://docs.aws.amazon.com//kms/latest/developerguide/symmetric-asymmetric.html>`_ in the *AWS Key Management Service Developer Guide* .
            :param sse_algorithm: Server-side encryption algorithm to use for the default encryption. .. epigraph:: For directory buckets, there are only two supported values for server-side encryption: ``AES256`` and ``aws:kms`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3express-directorybucket-serversideencryptionbydefault.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3express import mixins as s3express_mixins
                
                server_side_encryption_by_default_property = s3express_mixins.CfnDirectoryBucketPropsMixin.ServerSideEncryptionByDefaultProperty(
                    kms_master_key_id="kmsMasterKeyId",
                    sse_algorithm="sseAlgorithm"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3933f20b833276874b5ae87eb3c52509dc8041c134f280cdb005dff3e595c571)
                check_type(argname="argument kms_master_key_id", value=kms_master_key_id, expected_type=type_hints["kms_master_key_id"])
                check_type(argname="argument sse_algorithm", value=sse_algorithm, expected_type=type_hints["sse_algorithm"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kms_master_key_id is not None:
                self._values["kms_master_key_id"] = kms_master_key_id
            if sse_algorithm is not None:
                self._values["sse_algorithm"] = sse_algorithm

        @builtins.property
        def kms_master_key_id(self) -> typing.Optional[builtins.str]:
            '''AWS Key Management Service (KMS) customer managed key ID to use for the default encryption.

            This parameter is allowed only if ``SSEAlgorithm`` is set to ``aws:kms`` .

            You can specify this parameter with the key ID or the Amazon Resource Name (ARN) of the KMS key. You can’t use the key alias of the KMS key.

            - Key ID: ``1234abcd-12ab-34cd-56ef-1234567890ab``
            - Key ARN: ``arn:aws:kms:us-east-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab``

            If you are using encryption with cross-account or AWS service operations, you must use a fully qualified KMS key ARN. For more information, see `Using encryption for cross-account operations <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-express-bucket-encryption.html#s3-express-bucket-encryption-update-bucket-policy>`_ .
            .. epigraph::

               Your SSE-KMS configuration can only support 1 `customer managed key <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#customer-cmk>`_ per directory bucket for the lifetime of the bucket. `AWS managed key <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#aws-managed-cmk>`_ ( ``aws/s3`` ) isn't supported. Also, after you specify a customer managed key for SSE-KMS and upload objects with this configuration, you can't override the customer managed key for your SSE-KMS configuration. To use a new customer manager key for your data, we recommend copying your existing objects to a new directory bucket with a new customer managed key. > Amazon S3 only supports symmetric encryption KMS keys. For more information, see `Asymmetric keys in AWS KMS <https://docs.aws.amazon.com//kms/latest/developerguide/symmetric-asymmetric.html>`_ in the *AWS Key Management Service Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3express-directorybucket-serversideencryptionbydefault.html#cfn-s3express-directorybucket-serversideencryptionbydefault-kmsmasterkeyid
            '''
            result = self._values.get("kms_master_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sse_algorithm(self) -> typing.Optional[builtins.str]:
            '''Server-side encryption algorithm to use for the default encryption.

            .. epigraph::

               For directory buckets, there are only two supported values for server-side encryption: ``AES256`` and ``aws:kms`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3express-directorybucket-serversideencryptionbydefault.html#cfn-s3express-directorybucket-serversideencryptionbydefault-ssealgorithm
            '''
            result = self._values.get("sse_algorithm")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServerSideEncryptionByDefaultProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3express.mixins.CfnDirectoryBucketPropsMixin.ServerSideEncryptionRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_key_enabled": "bucketKeyEnabled",
            "server_side_encryption_by_default": "serverSideEncryptionByDefault",
        },
    )
    class ServerSideEncryptionRuleProperty:
        def __init__(
            self,
            *,
            bucket_key_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            server_side_encryption_by_default: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDirectoryBucketPropsMixin.ServerSideEncryptionByDefaultProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the default server-side encryption configuration.

            :param bucket_key_enabled: Specifies whether Amazon S3 should use an S3 Bucket Key with server-side encryption using KMS (SSE-KMS) for new objects in the bucket. S3 Bucket Keys are always enabled for ``GET`` and ``PUT`` operations on a directory bucket and can’t be disabled. It's only allowed to set the ``BucketKeyEnabled`` element to ``true`` . S3 Bucket Keys aren't supported, when you copy SSE-KMS encrypted objects from general purpose buckets to directory buckets, from directory buckets to general purpose buckets, or between directory buckets, through `CopyObject <https://docs.aws.amazon.com/AmazonS3/latest/API/API_CopyObject.html>`_ , `UploadPartCopy <https://docs.aws.amazon.com/AmazonS3/latest/API/API_UploadPartCopy.html>`_ , `the Copy operation in Batch Operations <https://docs.aws.amazon.com/AmazonS3/latest/userguide/directory-buckets-objects-Batch-Ops>`_ , or `the import jobs <https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-import-job>`_ . In this case, Amazon S3 makes a call to AWS KMS every time a copy request is made for a KMS-encrypted object. For more information, see `Amazon S3 Bucket Keys <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-express-UsingKMSEncryption.html#s3-express-sse-kms-bucket-keys>`_ in the *Amazon S3 User Guide* .
            :param server_side_encryption_by_default: Specifies the default server-side encryption to apply to new objects in the bucket. If a PUT Object request doesn't specify any server-side encryption, this default encryption will be applied.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3express-directorybucket-serversideencryptionrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3express import mixins as s3express_mixins
                
                server_side_encryption_rule_property = s3express_mixins.CfnDirectoryBucketPropsMixin.ServerSideEncryptionRuleProperty(
                    bucket_key_enabled=False,
                    server_side_encryption_by_default=s3express_mixins.CfnDirectoryBucketPropsMixin.ServerSideEncryptionByDefaultProperty(
                        kms_master_key_id="kmsMasterKeyId",
                        sse_algorithm="sseAlgorithm"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__46f616f1cc54effa2c7265e6c1f9d344504974c6547a8e9d61b9c3d92a5e15b4)
                check_type(argname="argument bucket_key_enabled", value=bucket_key_enabled, expected_type=type_hints["bucket_key_enabled"])
                check_type(argname="argument server_side_encryption_by_default", value=server_side_encryption_by_default, expected_type=type_hints["server_side_encryption_by_default"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_key_enabled is not None:
                self._values["bucket_key_enabled"] = bucket_key_enabled
            if server_side_encryption_by_default is not None:
                self._values["server_side_encryption_by_default"] = server_side_encryption_by_default

        @builtins.property
        def bucket_key_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether Amazon S3 should use an S3 Bucket Key with server-side encryption using KMS (SSE-KMS) for new objects in the bucket.

            S3 Bucket Keys are always enabled for ``GET`` and ``PUT`` operations on a directory bucket and can’t be disabled. It's only allowed to set the ``BucketKeyEnabled`` element to ``true`` .

            S3 Bucket Keys aren't supported, when you copy SSE-KMS encrypted objects from general purpose buckets to directory buckets, from directory buckets to general purpose buckets, or between directory buckets, through `CopyObject <https://docs.aws.amazon.com/AmazonS3/latest/API/API_CopyObject.html>`_ , `UploadPartCopy <https://docs.aws.amazon.com/AmazonS3/latest/API/API_UploadPartCopy.html>`_ , `the Copy operation in Batch Operations <https://docs.aws.amazon.com/AmazonS3/latest/userguide/directory-buckets-objects-Batch-Ops>`_ , or `the import jobs <https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-import-job>`_ . In this case, Amazon S3 makes a call to AWS KMS every time a copy request is made for a KMS-encrypted object.

            For more information, see `Amazon S3 Bucket Keys <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-express-UsingKMSEncryption.html#s3-express-sse-kms-bucket-keys>`_ in the *Amazon S3 User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3express-directorybucket-serversideencryptionrule.html#cfn-s3express-directorybucket-serversideencryptionrule-bucketkeyenabled
            '''
            result = self._values.get("bucket_key_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def server_side_encryption_by_default(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDirectoryBucketPropsMixin.ServerSideEncryptionByDefaultProperty"]]:
            '''Specifies the default server-side encryption to apply to new objects in the bucket.

            If a PUT Object request doesn't specify any server-side encryption, this default encryption will be applied.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3express-directorybucket-serversideencryptionrule.html#cfn-s3express-directorybucket-serversideencryptionrule-serversideencryptionbydefault
            '''
            result = self._values.get("server_side_encryption_by_default")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDirectoryBucketPropsMixin.ServerSideEncryptionByDefaultProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServerSideEncryptionRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnAccessPointMixinProps",
    "CfnAccessPointPropsMixin",
    "CfnBucketPolicyMixinProps",
    "CfnBucketPolicyPropsMixin",
    "CfnDirectoryBucketMixinProps",
    "CfnDirectoryBucketPropsMixin",
]

publication.publish()

def _typecheckingstub__be7e73dd333a9342e80591d8090b408f7af396e3bffab120ef39c46e7322e757(
    *,
    bucket: typing.Optional[builtins.str] = None,
    bucket_account_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    policy: typing.Any = None,
    public_access_block_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAccessPointPropsMixin.PublicAccessBlockConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    scope: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAccessPointPropsMixin.ScopeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAccessPointPropsMixin.VpcConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__435a037703b82814e4af12b45a9b6358a24d36639fb4d203ef95521a92392c75(
    props: typing.Union[CfnAccessPointMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d1ac1c31725219c4c13a58b263c7e826a707771dbc186039f853fcf18f03f48(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__393f5bc391614c0a9e6a6ec9cc7fca040053f3303a1e6c2c8e268c9554352219(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c5199913c725b0905fe0303bb493f49f0391fdc1b37b07188be03e1504e7f62(
    *,
    block_public_acls: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    block_public_policy: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    ignore_public_acls: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    restrict_public_buckets: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f67aa87849a2d4ec5199533690e1a2e4c9851417b8d620c527d0d8e5860e551(
    *,
    permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
    prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a77ef7d79f83b5c468bdeaba609779389ab16bbd41b81d4f1c96a4ecdb4998d(
    *,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9b6748888b18f86ecdef864c8d8c67caf9c22365352fc1eb813c8f127f5403a(
    *,
    bucket: typing.Optional[builtins.str] = None,
    policy_document: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__988db520962cef371e5f946d70ee0f5ad0da0820b41e9f314f731351de35bb0c(
    props: typing.Union[CfnBucketPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7abfa2882583991246d9514cde8138b37be9af7a4d130a5ab9e2c9293615cae4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45f6c804d0bde61ac7fdd0937521abf381a2e3953ec2a7f4124cfd951a72f8dd(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d5dddf6cc814065ba5a6cab38c6d1de04bd333773f2688fe3e570711b471873(
    *,
    bucket_encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDirectoryBucketPropsMixin.BucketEncryptionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    bucket_name: typing.Optional[builtins.str] = None,
    data_redundancy: typing.Optional[builtins.str] = None,
    lifecycle_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDirectoryBucketPropsMixin.LifecycleConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    location_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__306087ce0d958a42a41ebbf44f3067ff1afb06d43866cc35c97d01d9e3e8fc85(
    props: typing.Union[CfnDirectoryBucketMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceb2d73ddfde02d7895f17c3ad793468199234d9fb5d74bd0d6ff7a98e3b5b7e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4db982765e7d4e62eaa41c1977e79178111e4dec05b4702cba1d889bf7c26c42(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__749a7f16ab9b43633857462b788a161317fb70a78db91df4f43face6e1bea144(
    *,
    days_after_initiation: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39caeff27209703b6493924e003201ff22a5be78c250d92a73a23e01dbdf8e1a(
    *,
    server_side_encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDirectoryBucketPropsMixin.ServerSideEncryptionRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18f3c219cd561244807756baf8ac1d16c10374e2934d913daef8f587c1d7fa99(
    *,
    rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDirectoryBucketPropsMixin.RuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__106739c0f4ef55fee0345e2c005dd1434f8400b13dfd6693af2a9a80304d1105(
    *,
    abort_incomplete_multipart_upload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDirectoryBucketPropsMixin.AbortIncompleteMultipartUploadProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    expiration_in_days: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    object_size_greater_than: typing.Optional[builtins.str] = None,
    object_size_less_than: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3933f20b833276874b5ae87eb3c52509dc8041c134f280cdb005dff3e595c571(
    *,
    kms_master_key_id: typing.Optional[builtins.str] = None,
    sse_algorithm: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46f616f1cc54effa2c7265e6c1f9d344504974c6547a8e9d61b9c3d92a5e15b4(
    *,
    bucket_key_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    server_side_encryption_by_default: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDirectoryBucketPropsMixin.ServerSideEncryptionByDefaultProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
