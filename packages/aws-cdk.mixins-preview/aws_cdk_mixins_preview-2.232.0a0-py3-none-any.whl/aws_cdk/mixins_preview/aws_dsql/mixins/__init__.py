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
    jsii_type="@aws-cdk/mixins-preview.aws_dsql.mixins.CfnClusterMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "deletion_protection_enabled": "deletionProtectionEnabled",
        "kms_encryption_key": "kmsEncryptionKey",
        "multi_region_properties": "multiRegionProperties",
        "policy_document": "policyDocument",
        "tags": "tags",
    },
)
class CfnClusterMixinProps:
    def __init__(
        self,
        *,
        deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        kms_encryption_key: typing.Optional[builtins.str] = None,
        multi_region_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.MultiRegionPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        policy_document: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnClusterPropsMixin.

        :param deletion_protection_enabled: Whether deletion protection is enabled on this cluster.
        :param kms_encryption_key: The KMS key that encrypts data on the cluster.
        :param multi_region_properties: Defines the structure for multi-Region cluster configurations, containing the witness Region and peered cluster settings.
        :param policy_document: A resource-based policy document in JSON format. Length constraints: Minimum length of 1. Maximum length of 20480 characters (approximately 20KB).
        :param tags: A map of key and value pairs this cluster is tagged with.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dsql-cluster.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_dsql import mixins as dsql_mixins
            
            cfn_cluster_mixin_props = dsql_mixins.CfnClusterMixinProps(
                deletion_protection_enabled=False,
                kms_encryption_key="kmsEncryptionKey",
                multi_region_properties=dsql_mixins.CfnClusterPropsMixin.MultiRegionPropertiesProperty(
                    clusters=["clusters"],
                    witness_region="witnessRegion"
                ),
                policy_document="policyDocument",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5aad8f637f0b0c11e5c7a73d1a67f7901fd09baa81675e9304202f8c08c3d98a)
            check_type(argname="argument deletion_protection_enabled", value=deletion_protection_enabled, expected_type=type_hints["deletion_protection_enabled"])
            check_type(argname="argument kms_encryption_key", value=kms_encryption_key, expected_type=type_hints["kms_encryption_key"])
            check_type(argname="argument multi_region_properties", value=multi_region_properties, expected_type=type_hints["multi_region_properties"])
            check_type(argname="argument policy_document", value=policy_document, expected_type=type_hints["policy_document"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if deletion_protection_enabled is not None:
            self._values["deletion_protection_enabled"] = deletion_protection_enabled
        if kms_encryption_key is not None:
            self._values["kms_encryption_key"] = kms_encryption_key
        if multi_region_properties is not None:
            self._values["multi_region_properties"] = multi_region_properties
        if policy_document is not None:
            self._values["policy_document"] = policy_document
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def deletion_protection_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Whether deletion protection is enabled on this cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dsql-cluster.html#cfn-dsql-cluster-deletionprotectionenabled
        '''
        result = self._values.get("deletion_protection_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def kms_encryption_key(self) -> typing.Optional[builtins.str]:
        '''The KMS key that encrypts data on the cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dsql-cluster.html#cfn-dsql-cluster-kmsencryptionkey
        '''
        result = self._values.get("kms_encryption_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def multi_region_properties(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.MultiRegionPropertiesProperty"]]:
        '''Defines the structure for multi-Region cluster configurations, containing the witness Region and peered cluster settings.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dsql-cluster.html#cfn-dsql-cluster-multiregionproperties
        '''
        result = self._values.get("multi_region_properties")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.MultiRegionPropertiesProperty"]], result)

    @builtins.property
    def policy_document(self) -> typing.Optional[builtins.str]:
        '''A resource-based policy document in JSON format.

        Length constraints: Minimum length of 1. Maximum length of 20480 characters (approximately 20KB).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dsql-cluster.html#cfn-dsql-cluster-policydocument
        '''
        result = self._values.get("policy_document")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A map of key and value pairs this cluster is tagged with.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dsql-cluster.html#cfn-dsql-cluster-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnClusterMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnClusterPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_dsql.mixins.CfnClusterPropsMixin",
):
    '''The ``AWS::DSQL::Cluster`` resource specifies an cluster. You can use this resource to create, modify, and manage clusters.

    This resource supports both single-Region clusters and multi-Region clusters through the ``MultiRegionProperties`` parameter.
    .. epigraph::

       Creating multi-Region clusters requires additional IAM permissions beyond those needed for single-Region clusters. > - The witness Region specified in ``multiRegionProperties.witnessRegion`` cannot be the same as the cluster's Region.

    *Required permissions*

    - **dsql:CreateCluster** - Required to create a cluster.

    Resources: ``arn:aws:dsql:region:account-id:cluster/*``

    - **dsql:TagResource** - Permission to add tags to a resource.

    Resources: ``arn:aws:dsql:region:account-id:cluster/*``

    - **dsql:PutMultiRegionProperties** - Permission to configure multi-Region properties for a cluster.

    Resources: ``arn:aws:dsql:region:account-id:cluster/*``

    - **dsql:AddPeerCluster** - When specifying ``multiRegionProperties.clusters`` , permission to add peer clusters.

    Resources:

    - Local cluster: ``arn:aws:dsql:region:account-id:cluster/*``
    - Each peer cluster: exact ARN of each specified peer cluster
    - **dsql:PutWitnessRegion** - When specifying ``multiRegionProperties.witnessRegion`` , permission to set a witness Region. This permission is checked both in the cluster Region and in the witness Region.

    Resources: ``arn:aws:dsql:region:account-id:cluster/*``

    Condition Keys: ``dsql:WitnessRegion`` (matching the specified witness region)

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dsql-cluster.html
    :cloudformationResource: AWS::DSQL::Cluster
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_dsql import mixins as dsql_mixins
        
        cfn_cluster_props_mixin = dsql_mixins.CfnClusterPropsMixin(dsql_mixins.CfnClusterMixinProps(
            deletion_protection_enabled=False,
            kms_encryption_key="kmsEncryptionKey",
            multi_region_properties=dsql_mixins.CfnClusterPropsMixin.MultiRegionPropertiesProperty(
                clusters=["clusters"],
                witness_region="witnessRegion"
            ),
            policy_document="policyDocument",
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
        props: typing.Union[CfnClusterMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DSQL::Cluster``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd83a71f4d97e9bfc388d7e25f6c498f8773fa07d6be9150e9c53e50463cdc93)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f11bc7b5f4e25f993f34a49e5d5ce94efdd882be0f2282727cf2735536af0ee2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30260929d2e146067515f51510f529be7e2d27fab5ba3e42448d2a7ee4e76d97)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnClusterMixinProps:
        return typing.cast(CfnClusterMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dsql.mixins.CfnClusterPropsMixin.EncryptionDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "encryption_status": "encryptionStatus",
            "encryption_type": "encryptionType",
            "kms_key_arn": "kmsKeyArn",
        },
    )
    class EncryptionDetailsProperty:
        def __init__(
            self,
            *,
            encryption_status: typing.Optional[builtins.str] = None,
            encryption_type: typing.Optional[builtins.str] = None,
            kms_key_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration details about encryption for the cluster including the AWS  key ARN, encryption type, and encryption status.

            :param encryption_status: The status of encryption for the cluster.
            :param encryption_type: The type of encryption that protects the data on your cluster.
            :param kms_key_arn: The ARN of the AWS key that encrypts data in the cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dsql-cluster-encryptiondetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dsql import mixins as dsql_mixins
                
                encryption_details_property = dsql_mixins.CfnClusterPropsMixin.EncryptionDetailsProperty(
                    encryption_status="encryptionStatus",
                    encryption_type="encryptionType",
                    kms_key_arn="kmsKeyArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1aa835daea66465d2d4fd8103582feac4babd2bce34b88e3b0561da9b6904170)
                check_type(argname="argument encryption_status", value=encryption_status, expected_type=type_hints["encryption_status"])
                check_type(argname="argument encryption_type", value=encryption_type, expected_type=type_hints["encryption_type"])
                check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encryption_status is not None:
                self._values["encryption_status"] = encryption_status
            if encryption_type is not None:
                self._values["encryption_type"] = encryption_type
            if kms_key_arn is not None:
                self._values["kms_key_arn"] = kms_key_arn

        @builtins.property
        def encryption_status(self) -> typing.Optional[builtins.str]:
            '''The status of encryption for the cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dsql-cluster-encryptiondetails.html#cfn-dsql-cluster-encryptiondetails-encryptionstatus
            '''
            result = self._values.get("encryption_status")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def encryption_type(self) -> typing.Optional[builtins.str]:
            '''The type of encryption that protects the data on your cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dsql-cluster-encryptiondetails.html#cfn-dsql-cluster-encryptiondetails-encryptiontype
            '''
            result = self._values.get("encryption_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def kms_key_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the AWS  key that encrypts data in the cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dsql-cluster-encryptiondetails.html#cfn-dsql-cluster-encryptiondetails-kmskeyarn
            '''
            result = self._values.get("kms_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dsql.mixins.CfnClusterPropsMixin.MultiRegionPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"clusters": "clusters", "witness_region": "witnessRegion"},
    )
    class MultiRegionPropertiesProperty:
        def __init__(
            self,
            *,
            clusters: typing.Optional[typing.Sequence[builtins.str]] = None,
            witness_region: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines the structure for multi-Region cluster configurations, containing the witness Region and peered cluster settings.

            :param clusters: The set of peered clusters that form the multi-Region cluster configuration. Each peered cluster represents a database instance in a different Region.
            :param witness_region: The Region that serves as the witness Region for a multi-Region cluster. The witness Region helps maintain cluster consistency and quorum.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dsql-cluster-multiregionproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dsql import mixins as dsql_mixins
                
                multi_region_properties_property = dsql_mixins.CfnClusterPropsMixin.MultiRegionPropertiesProperty(
                    clusters=["clusters"],
                    witness_region="witnessRegion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__829e1e48d1150a4a26d27184ac82523d2ffffa0b236bd323115243b5733b2932)
                check_type(argname="argument clusters", value=clusters, expected_type=type_hints["clusters"])
                check_type(argname="argument witness_region", value=witness_region, expected_type=type_hints["witness_region"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if clusters is not None:
                self._values["clusters"] = clusters
            if witness_region is not None:
                self._values["witness_region"] = witness_region

        @builtins.property
        def clusters(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The set of peered clusters that form the multi-Region cluster configuration.

            Each peered cluster represents a database instance in a different Region.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dsql-cluster-multiregionproperties.html#cfn-dsql-cluster-multiregionproperties-clusters
            '''
            result = self._values.get("clusters")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def witness_region(self) -> typing.Optional[builtins.str]:
            '''The Region that serves as the witness Region for a multi-Region cluster.

            The witness Region helps maintain cluster consistency and quorum.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dsql-cluster-multiregionproperties.html#cfn-dsql-cluster-multiregionproperties-witnessregion
            '''
            result = self._values.get("witness_region")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MultiRegionPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnClusterMixinProps",
    "CfnClusterPropsMixin",
]

publication.publish()

def _typecheckingstub__5aad8f637f0b0c11e5c7a73d1a67f7901fd09baa81675e9304202f8c08c3d98a(
    *,
    deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    kms_encryption_key: typing.Optional[builtins.str] = None,
    multi_region_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.MultiRegionPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    policy_document: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd83a71f4d97e9bfc388d7e25f6c498f8773fa07d6be9150e9c53e50463cdc93(
    props: typing.Union[CfnClusterMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f11bc7b5f4e25f993f34a49e5d5ce94efdd882be0f2282727cf2735536af0ee2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30260929d2e146067515f51510f529be7e2d27fab5ba3e42448d2a7ee4e76d97(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aa835daea66465d2d4fd8103582feac4babd2bce34b88e3b0561da9b6904170(
    *,
    encryption_status: typing.Optional[builtins.str] = None,
    encryption_type: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__829e1e48d1150a4a26d27184ac82523d2ffffa0b236bd323115243b5733b2932(
    *,
    clusters: typing.Optional[typing.Sequence[builtins.str]] = None,
    witness_region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
