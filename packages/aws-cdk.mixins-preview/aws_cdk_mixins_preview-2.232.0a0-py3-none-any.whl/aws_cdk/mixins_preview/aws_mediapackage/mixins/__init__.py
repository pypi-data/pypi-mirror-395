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
    jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.mixins.CfnAssetMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "egress_endpoints": "egressEndpoints",
        "id": "id",
        "packaging_group_id": "packagingGroupId",
        "resource_id": "resourceId",
        "source_arn": "sourceArn",
        "source_role_arn": "sourceRoleArn",
        "tags": "tags",
    },
)
class CfnAssetMixinProps:
    def __init__(
        self,
        *,
        egress_endpoints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAssetPropsMixin.EgressEndpointProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        packaging_group_id: typing.Optional[builtins.str] = None,
        resource_id: typing.Optional[builtins.str] = None,
        source_arn: typing.Optional[builtins.str] = None,
        source_role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnAssetPropsMixin.

        :param egress_endpoints: List of playback endpoints that are available for this asset.
        :param id: Unique identifier that you assign to the asset.
        :param packaging_group_id: The ID of the packaging group associated with this asset.
        :param resource_id: Unique identifier for this asset, as it's configured in the key provider service.
        :param source_arn: The ARN for the source content in Amazon S3.
        :param source_role_arn: The ARN for the IAM role that provides AWS Elemental MediaPackage access to the Amazon S3 bucket where the source content is stored. Valid format: arn:aws:iam::{accountID}:role/{name}
        :param tags: The tags to assign to the asset.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-asset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_mediapackage import mixins as mediapackage_mixins
            
            cfn_asset_mixin_props = mediapackage_mixins.CfnAssetMixinProps(
                egress_endpoints=[mediapackage_mixins.CfnAssetPropsMixin.EgressEndpointProperty(
                    packaging_configuration_id="packagingConfigurationId",
                    url="url"
                )],
                id="id",
                packaging_group_id="packagingGroupId",
                resource_id="resourceId",
                source_arn="sourceArn",
                source_role_arn="sourceRoleArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0df7bf8ea84ee7bff12f83c47c9580e26b066d2a5f30620d771850d7689bc1d9)
            check_type(argname="argument egress_endpoints", value=egress_endpoints, expected_type=type_hints["egress_endpoints"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument packaging_group_id", value=packaging_group_id, expected_type=type_hints["packaging_group_id"])
            check_type(argname="argument resource_id", value=resource_id, expected_type=type_hints["resource_id"])
            check_type(argname="argument source_arn", value=source_arn, expected_type=type_hints["source_arn"])
            check_type(argname="argument source_role_arn", value=source_role_arn, expected_type=type_hints["source_role_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if egress_endpoints is not None:
            self._values["egress_endpoints"] = egress_endpoints
        if id is not None:
            self._values["id"] = id
        if packaging_group_id is not None:
            self._values["packaging_group_id"] = packaging_group_id
        if resource_id is not None:
            self._values["resource_id"] = resource_id
        if source_arn is not None:
            self._values["source_arn"] = source_arn
        if source_role_arn is not None:
            self._values["source_role_arn"] = source_role_arn
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def egress_endpoints(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssetPropsMixin.EgressEndpointProperty"]]]]:
        '''List of playback endpoints that are available for this asset.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-asset.html#cfn-mediapackage-asset-egressendpoints
        '''
        result = self._values.get("egress_endpoints")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssetPropsMixin.EgressEndpointProperty"]]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Unique identifier that you assign to the asset.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-asset.html#cfn-mediapackage-asset-id
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def packaging_group_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the packaging group associated with this asset.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-asset.html#cfn-mediapackage-asset-packaginggroupid
        '''
        result = self._values.get("packaging_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_id(self) -> typing.Optional[builtins.str]:
        '''Unique identifier for this asset, as it's configured in the key provider service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-asset.html#cfn-mediapackage-asset-resourceid
        '''
        result = self._values.get("resource_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN for the source content in Amazon S3.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-asset.html#cfn-mediapackage-asset-sourcearn
        '''
        result = self._values.get("source_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN for the IAM role that provides AWS Elemental MediaPackage access to the Amazon S3 bucket where the source content is stored.

        Valid format: arn:aws:iam::{accountID}:role/{name}

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-asset.html#cfn-mediapackage-asset-sourcerolearn
        '''
        result = self._values.get("source_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags to assign to the asset.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-asset.html#cfn-mediapackage-asset-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAssetMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAssetPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.mixins.CfnAssetPropsMixin",
):
    '''Creates an asset to ingest VOD content.

    After it's created, the asset starts ingesting content and generates playback URLs for the packaging configurations associated with it. When ingest is complete, downstream devices use the appropriate URL to request VOD content from AWS Elemental MediaPackage .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-asset.html
    :cloudformationResource: AWS::MediaPackage::Asset
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_mediapackage import mixins as mediapackage_mixins
        
        cfn_asset_props_mixin = mediapackage_mixins.CfnAssetPropsMixin(mediapackage_mixins.CfnAssetMixinProps(
            egress_endpoints=[mediapackage_mixins.CfnAssetPropsMixin.EgressEndpointProperty(
                packaging_configuration_id="packagingConfigurationId",
                url="url"
            )],
            id="id",
            packaging_group_id="packagingGroupId",
            resource_id="resourceId",
            source_arn="sourceArn",
            source_role_arn="sourceRoleArn",
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
        props: typing.Union[CfnAssetMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::MediaPackage::Asset``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e9febc4eb1b1f204893cfbfe1623af3415e3df1d1b764fb10e1c6dbf43e4d6b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__841d713efad38377d211fc906ba12af565040112bd7dd7c64b8ebfcac8164f18)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05e42bb7b80bba68eef730e876a7450ce036769080c3d9f33dc5faea45e6b82b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAssetMixinProps:
        return typing.cast(CfnAssetMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.mixins.CfnAssetPropsMixin.EgressEndpointProperty",
        jsii_struct_bases=[],
        name_mapping={
            "packaging_configuration_id": "packagingConfigurationId",
            "url": "url",
        },
    )
    class EgressEndpointProperty:
        def __init__(
            self,
            *,
            packaging_configuration_id: typing.Optional[builtins.str] = None,
            url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The playback endpoint for a packaging configuration on an asset.

            :param packaging_configuration_id: The ID of a packaging configuration that's applied to this asset.
            :param url: The URL that's used to request content from this endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-asset-egressendpoint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackage import mixins as mediapackage_mixins
                
                egress_endpoint_property = mediapackage_mixins.CfnAssetPropsMixin.EgressEndpointProperty(
                    packaging_configuration_id="packagingConfigurationId",
                    url="url"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d09dec6d7e849ac98bb1bb6803c3331e07c4af19a5af27155c15672e8f5b55a6)
                check_type(argname="argument packaging_configuration_id", value=packaging_configuration_id, expected_type=type_hints["packaging_configuration_id"])
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if packaging_configuration_id is not None:
                self._values["packaging_configuration_id"] = packaging_configuration_id
            if url is not None:
                self._values["url"] = url

        @builtins.property
        def packaging_configuration_id(self) -> typing.Optional[builtins.str]:
            '''The ID of a packaging configuration that's applied to this asset.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-asset-egressendpoint.html#cfn-mediapackage-asset-egressendpoint-packagingconfigurationid
            '''
            result = self._values.get("packaging_configuration_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            '''The URL that's used to request content from this endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-asset-egressendpoint.html#cfn-mediapackage-asset-egressendpoint-url
            '''
            result = self._values.get("url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EgressEndpointProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.mixins.CfnChannelMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "egress_access_logs": "egressAccessLogs",
        "hls_ingest": "hlsIngest",
        "id": "id",
        "ingress_access_logs": "ingressAccessLogs",
        "tags": "tags",
    },
)
class CfnChannelMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        egress_access_logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnChannelPropsMixin.LogConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        hls_ingest: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnChannelPropsMixin.HlsIngestProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        id: typing.Optional[builtins.str] = None,
        ingress_access_logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnChannelPropsMixin.LogConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnChannelPropsMixin.

        :param description: Any descriptive information that you want to add to the channel for future identification purposes.
        :param egress_access_logs: Configures egress access logs.
        :param hls_ingest: The input URL where the source stream should be sent.
        :param id: Unique identifier that you assign to the channel.
        :param ingress_access_logs: Configures ingress access logs.
        :param tags: The tags to assign to the channel.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-channel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_mediapackage import mixins as mediapackage_mixins
            
            cfn_channel_mixin_props = mediapackage_mixins.CfnChannelMixinProps(
                description="description",
                egress_access_logs=mediapackage_mixins.CfnChannelPropsMixin.LogConfigurationProperty(
                    log_group_name="logGroupName"
                ),
                hls_ingest=mediapackage_mixins.CfnChannelPropsMixin.HlsIngestProperty(
                    ingest_endpoints=[mediapackage_mixins.CfnChannelPropsMixin.IngestEndpointProperty(
                        id="id",
                        password="password",
                        url="url",
                        username="username"
                    )]
                ),
                id="id",
                ingress_access_logs=mediapackage_mixins.CfnChannelPropsMixin.LogConfigurationProperty(
                    log_group_name="logGroupName"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c845133e9599091587a7f9d866767c7e1c8503d4002375c8c3ac247d30ee0823)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument egress_access_logs", value=egress_access_logs, expected_type=type_hints["egress_access_logs"])
            check_type(argname="argument hls_ingest", value=hls_ingest, expected_type=type_hints["hls_ingest"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ingress_access_logs", value=ingress_access_logs, expected_type=type_hints["ingress_access_logs"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if egress_access_logs is not None:
            self._values["egress_access_logs"] = egress_access_logs
        if hls_ingest is not None:
            self._values["hls_ingest"] = hls_ingest
        if id is not None:
            self._values["id"] = id
        if ingress_access_logs is not None:
            self._values["ingress_access_logs"] = ingress_access_logs
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Any descriptive information that you want to add to the channel for future identification purposes.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-channel.html#cfn-mediapackage-channel-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def egress_access_logs(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelPropsMixin.LogConfigurationProperty"]]:
        '''Configures egress access logs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-channel.html#cfn-mediapackage-channel-egressaccesslogs
        '''
        result = self._values.get("egress_access_logs")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelPropsMixin.LogConfigurationProperty"]], result)

    @builtins.property
    def hls_ingest(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelPropsMixin.HlsIngestProperty"]]:
        '''The input URL where the source stream should be sent.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-channel.html#cfn-mediapackage-channel-hlsingest
        '''
        result = self._values.get("hls_ingest")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelPropsMixin.HlsIngestProperty"]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Unique identifier that you assign to the channel.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-channel.html#cfn-mediapackage-channel-id
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ingress_access_logs(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelPropsMixin.LogConfigurationProperty"]]:
        '''Configures ingress access logs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-channel.html#cfn-mediapackage-channel-ingressaccesslogs
        '''
        result = self._values.get("ingress_access_logs")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelPropsMixin.LogConfigurationProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags to assign to the channel.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-channel.html#cfn-mediapackage-channel-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnChannelMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnChannelPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.mixins.CfnChannelPropsMixin",
):
    '''Creates a channel to receive content.

    After it's created, a channel provides static input URLs. These URLs remain the same throughout the lifetime of the channel, regardless of any failures or upgrades that might occur. Use these URLs to configure the outputs of your upstream encoder.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-channel.html
    :cloudformationResource: AWS::MediaPackage::Channel
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_mediapackage import mixins as mediapackage_mixins
        
        cfn_channel_props_mixin = mediapackage_mixins.CfnChannelPropsMixin(mediapackage_mixins.CfnChannelMixinProps(
            description="description",
            egress_access_logs=mediapackage_mixins.CfnChannelPropsMixin.LogConfigurationProperty(
                log_group_name="logGroupName"
            ),
            hls_ingest=mediapackage_mixins.CfnChannelPropsMixin.HlsIngestProperty(
                ingest_endpoints=[mediapackage_mixins.CfnChannelPropsMixin.IngestEndpointProperty(
                    id="id",
                    password="password",
                    url="url",
                    username="username"
                )]
            ),
            id="id",
            ingress_access_logs=mediapackage_mixins.CfnChannelPropsMixin.LogConfigurationProperty(
                log_group_name="logGroupName"
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
        props: typing.Union[CfnChannelMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::MediaPackage::Channel``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0f9b149b0426af1fc0e60876b44cbed500fe314a1cad7fc7ac08c5f3f48b71a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__644d3de8d9d45775e11ae63846e02cc50218d49da36eb0f1d0925d6015695bc3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab219c43e6582abc1dd20672180343ab1b24f707f798647df2c9771ef235a9bb)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnChannelMixinProps:
        return typing.cast(CfnChannelMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.mixins.CfnChannelPropsMixin.HlsIngestProperty",
        jsii_struct_bases=[],
        name_mapping={"ingest_endpoints": "ingestEndpoints"},
    )
    class HlsIngestProperty:
        def __init__(
            self,
            *,
            ingest_endpoints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnChannelPropsMixin.IngestEndpointProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''HLS ingest configuration.

            :param ingest_endpoints: The input URL where the source stream should be sent.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-channel-hlsingest.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackage import mixins as mediapackage_mixins
                
                hls_ingest_property = mediapackage_mixins.CfnChannelPropsMixin.HlsIngestProperty(
                    ingest_endpoints=[mediapackage_mixins.CfnChannelPropsMixin.IngestEndpointProperty(
                        id="id",
                        password="password",
                        url="url",
                        username="username"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__91be515a47d53eaf3ab2265fffce9f8b02e98c53c9a29d6dc2a204e4c8780615)
                check_type(argname="argument ingest_endpoints", value=ingest_endpoints, expected_type=type_hints["ingest_endpoints"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ingest_endpoints is not None:
                self._values["ingest_endpoints"] = ingest_endpoints

        @builtins.property
        def ingest_endpoints(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelPropsMixin.IngestEndpointProperty"]]]]:
            '''The input URL where the source stream should be sent.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-channel-hlsingest.html#cfn-mediapackage-channel-hlsingest-ingestendpoints
            '''
            result = self._values.get("ingest_endpoints")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelPropsMixin.IngestEndpointProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HlsIngestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.mixins.CfnChannelPropsMixin.IngestEndpointProperty",
        jsii_struct_bases=[],
        name_mapping={
            "id": "id",
            "password": "password",
            "url": "url",
            "username": "username",
        },
    )
    class IngestEndpointProperty:
        def __init__(
            self,
            *,
            id: typing.Optional[builtins.str] = None,
            password: typing.Optional[builtins.str] = None,
            url: typing.Optional[builtins.str] = None,
            username: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An endpoint for ingesting source content for a channel.

            :param id: The endpoint identifier.
            :param password: The system-generated password for WebDAV input authentication.
            :param url: The input URL where the source stream should be sent.
            :param username: The system-generated username for WebDAV input authentication.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-channel-ingestendpoint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackage import mixins as mediapackage_mixins
                
                ingest_endpoint_property = mediapackage_mixins.CfnChannelPropsMixin.IngestEndpointProperty(
                    id="id",
                    password="password",
                    url="url",
                    username="username"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__02b0ab0d96c8fc6451858c05d9272dcb33ae4fe06559b4ff8091c8ad5fd7d246)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument password", value=password, expected_type=type_hints["password"])
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
                check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if id is not None:
                self._values["id"] = id
            if password is not None:
                self._values["password"] = password
            if url is not None:
                self._values["url"] = url
            if username is not None:
                self._values["username"] = username

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''The endpoint identifier.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-channel-ingestendpoint.html#cfn-mediapackage-channel-ingestendpoint-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def password(self) -> typing.Optional[builtins.str]:
            '''The system-generated password for WebDAV input authentication.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-channel-ingestendpoint.html#cfn-mediapackage-channel-ingestendpoint-password
            '''
            result = self._values.get("password")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            '''The input URL where the source stream should be sent.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-channel-ingestendpoint.html#cfn-mediapackage-channel-ingestendpoint-url
            '''
            result = self._values.get("url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def username(self) -> typing.Optional[builtins.str]:
            '''The system-generated username for WebDAV input authentication.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-channel-ingestendpoint.html#cfn-mediapackage-channel-ingestendpoint-username
            '''
            result = self._values.get("username")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IngestEndpointProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.mixins.CfnChannelPropsMixin.LogConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"log_group_name": "logGroupName"},
    )
    class LogConfigurationProperty:
        def __init__(
            self,
            *,
            log_group_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The access log configuration parameters for your channel.

            :param log_group_name: Sets a custom Amazon CloudWatch log group name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-channel-logconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackage import mixins as mediapackage_mixins
                
                log_configuration_property = mediapackage_mixins.CfnChannelPropsMixin.LogConfigurationProperty(
                    log_group_name="logGroupName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__688eef1c6e42421bdf9d4d3c0d4cffa16374360d795be739c325207ed9ac1fe4)
                check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if log_group_name is not None:
                self._values["log_group_name"] = log_group_name

        @builtins.property
        def log_group_name(self) -> typing.Optional[builtins.str]:
            '''Sets a custom Amazon CloudWatch log group name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-channel-logconfiguration.html#cfn-mediapackage-channel-logconfiguration-loggroupname
            '''
            result = self._values.get("log_group_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.mixins.CfnOriginEndpointMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "authorization": "authorization",
        "channel_id": "channelId",
        "cmaf_package": "cmafPackage",
        "dash_package": "dashPackage",
        "description": "description",
        "hls_package": "hlsPackage",
        "id": "id",
        "manifest_name": "manifestName",
        "mss_package": "mssPackage",
        "origination": "origination",
        "startover_window_seconds": "startoverWindowSeconds",
        "tags": "tags",
        "time_delay_seconds": "timeDelaySeconds",
        "whitelist": "whitelist",
    },
)
class CfnOriginEndpointMixinProps:
    def __init__(
        self,
        *,
        authorization: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.AuthorizationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        channel_id: typing.Optional[builtins.str] = None,
        cmaf_package: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.CmafPackageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        dash_package: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.DashPackageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        hls_package: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.HlsPackageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        id: typing.Optional[builtins.str] = None,
        manifest_name: typing.Optional[builtins.str] = None,
        mss_package: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.MssPackageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        origination: typing.Optional[builtins.str] = None,
        startover_window_seconds: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        time_delay_seconds: typing.Optional[jsii.Number] = None,
        whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for CfnOriginEndpointPropsMixin.

        :param authorization: Parameters for CDN authorization.
        :param channel_id: The ID of the channel associated with this endpoint.
        :param cmaf_package: Parameters for Common Media Application Format (CMAF) packaging.
        :param dash_package: Parameters for DASH packaging.
        :param description: Any descriptive information that you want to add to the endpoint for future identification purposes.
        :param hls_package: Parameters for Apple HLS packaging.
        :param id: The manifest ID is required and must be unique within the OriginEndpoint. The ID can't be changed after the endpoint is created.
        :param manifest_name: A short string that's appended to the end of the endpoint URL to create a unique path to this endpoint.
        :param mss_package: Parameters for Microsoft Smooth Streaming packaging.
        :param origination: Controls video origination from this endpoint. Valid values: - ``ALLOW`` - enables this endpoint to serve content to requesting devices. - ``DENY`` - prevents this endpoint from serving content. Denying origination is helpful for harvesting live-to-VOD assets. For more information about harvesting and origination, see `Live-to-VOD Requirements <https://docs.aws.amazon.com/mediapackage/latest/ug/ltov-reqmts.html>`_ .
        :param startover_window_seconds: Maximum duration (seconds) of content to retain for startover playback. Omit this attribute or enter ``0`` to indicate that startover playback is disabled for this endpoint.
        :param tags: The tags to assign to the endpoint.
        :param time_delay_seconds: Minimum duration (seconds) of delay to enforce on the playback of live content. Omit this attribute or enter ``0`` to indicate that there is no time delay in effect for this endpoint.
        :param whitelist: The IP addresses that can access this endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-originendpoint.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_mediapackage import mixins as mediapackage_mixins
            
            cfn_origin_endpoint_mixin_props = mediapackage_mixins.CfnOriginEndpointMixinProps(
                authorization=mediapackage_mixins.CfnOriginEndpointPropsMixin.AuthorizationProperty(
                    cdn_identifier_secret="cdnIdentifierSecret",
                    secrets_role_arn="secretsRoleArn"
                ),
                channel_id="channelId",
                cmaf_package=mediapackage_mixins.CfnOriginEndpointPropsMixin.CmafPackageProperty(
                    encryption=mediapackage_mixins.CfnOriginEndpointPropsMixin.CmafEncryptionProperty(
                        constant_initialization_vector="constantInitializationVector",
                        encryption_method="encryptionMethod",
                        key_rotation_interval_seconds=123,
                        speke_key_provider=mediapackage_mixins.CfnOriginEndpointPropsMixin.SpekeKeyProviderProperty(
                            certificate_arn="certificateArn",
                            encryption_contract_configuration=mediapackage_mixins.CfnOriginEndpointPropsMixin.EncryptionContractConfigurationProperty(
                                preset_speke20_audio="presetSpeke20Audio",
                                preset_speke20_video="presetSpeke20Video"
                            ),
                            resource_id="resourceId",
                            role_arn="roleArn",
                            system_ids=["systemIds"],
                            url="url"
                        )
                    ),
                    hls_manifests=[mediapackage_mixins.CfnOriginEndpointPropsMixin.HlsManifestProperty(
                        ad_markers="adMarkers",
                        ads_on_delivery_restrictions="adsOnDeliveryRestrictions",
                        ad_triggers=["adTriggers"],
                        id="id",
                        include_iframe_only_stream=False,
                        manifest_name="manifestName",
                        playlist_type="playlistType",
                        playlist_window_seconds=123,
                        program_date_time_interval_seconds=123,
                        url="url"
                    )],
                    segment_duration_seconds=123,
                    segment_prefix="segmentPrefix",
                    stream_selection=mediapackage_mixins.CfnOriginEndpointPropsMixin.StreamSelectionProperty(
                        max_video_bits_per_second=123,
                        min_video_bits_per_second=123,
                        stream_order="streamOrder"
                    )
                ),
                dash_package=mediapackage_mixins.CfnOriginEndpointPropsMixin.DashPackageProperty(
                    ads_on_delivery_restrictions="adsOnDeliveryRestrictions",
                    ad_triggers=["adTriggers"],
                    encryption=mediapackage_mixins.CfnOriginEndpointPropsMixin.DashEncryptionProperty(
                        key_rotation_interval_seconds=123,
                        speke_key_provider=mediapackage_mixins.CfnOriginEndpointPropsMixin.SpekeKeyProviderProperty(
                            certificate_arn="certificateArn",
                            encryption_contract_configuration=mediapackage_mixins.CfnOriginEndpointPropsMixin.EncryptionContractConfigurationProperty(
                                preset_speke20_audio="presetSpeke20Audio",
                                preset_speke20_video="presetSpeke20Video"
                            ),
                            resource_id="resourceId",
                            role_arn="roleArn",
                            system_ids=["systemIds"],
                            url="url"
                        )
                    ),
                    include_iframe_only_stream=False,
                    manifest_layout="manifestLayout",
                    manifest_window_seconds=123,
                    min_buffer_time_seconds=123,
                    min_update_period_seconds=123,
                    period_triggers=["periodTriggers"],
                    profile="profile",
                    segment_duration_seconds=123,
                    segment_template_format="segmentTemplateFormat",
                    stream_selection=mediapackage_mixins.CfnOriginEndpointPropsMixin.StreamSelectionProperty(
                        max_video_bits_per_second=123,
                        min_video_bits_per_second=123,
                        stream_order="streamOrder"
                    ),
                    suggested_presentation_delay_seconds=123,
                    utc_timing="utcTiming",
                    utc_timing_uri="utcTimingUri"
                ),
                description="description",
                hls_package=mediapackage_mixins.CfnOriginEndpointPropsMixin.HlsPackageProperty(
                    ad_markers="adMarkers",
                    ads_on_delivery_restrictions="adsOnDeliveryRestrictions",
                    ad_triggers=["adTriggers"],
                    encryption=mediapackage_mixins.CfnOriginEndpointPropsMixin.HlsEncryptionProperty(
                        constant_initialization_vector="constantInitializationVector",
                        encryption_method="encryptionMethod",
                        key_rotation_interval_seconds=123,
                        repeat_ext_xKey=False,
                        speke_key_provider=mediapackage_mixins.CfnOriginEndpointPropsMixin.SpekeKeyProviderProperty(
                            certificate_arn="certificateArn",
                            encryption_contract_configuration=mediapackage_mixins.CfnOriginEndpointPropsMixin.EncryptionContractConfigurationProperty(
                                preset_speke20_audio="presetSpeke20Audio",
                                preset_speke20_video="presetSpeke20Video"
                            ),
                            resource_id="resourceId",
                            role_arn="roleArn",
                            system_ids=["systemIds"],
                            url="url"
                        )
                    ),
                    include_dvb_subtitles=False,
                    include_iframe_only_stream=False,
                    playlist_type="playlistType",
                    playlist_window_seconds=123,
                    program_date_time_interval_seconds=123,
                    segment_duration_seconds=123,
                    stream_selection=mediapackage_mixins.CfnOriginEndpointPropsMixin.StreamSelectionProperty(
                        max_video_bits_per_second=123,
                        min_video_bits_per_second=123,
                        stream_order="streamOrder"
                    ),
                    use_audio_rendition_group=False
                ),
                id="id",
                manifest_name="manifestName",
                mss_package=mediapackage_mixins.CfnOriginEndpointPropsMixin.MssPackageProperty(
                    encryption=mediapackage_mixins.CfnOriginEndpointPropsMixin.MssEncryptionProperty(
                        speke_key_provider=mediapackage_mixins.CfnOriginEndpointPropsMixin.SpekeKeyProviderProperty(
                            certificate_arn="certificateArn",
                            encryption_contract_configuration=mediapackage_mixins.CfnOriginEndpointPropsMixin.EncryptionContractConfigurationProperty(
                                preset_speke20_audio="presetSpeke20Audio",
                                preset_speke20_video="presetSpeke20Video"
                            ),
                            resource_id="resourceId",
                            role_arn="roleArn",
                            system_ids=["systemIds"],
                            url="url"
                        )
                    ),
                    manifest_window_seconds=123,
                    segment_duration_seconds=123,
                    stream_selection=mediapackage_mixins.CfnOriginEndpointPropsMixin.StreamSelectionProperty(
                        max_video_bits_per_second=123,
                        min_video_bits_per_second=123,
                        stream_order="streamOrder"
                    )
                ),
                origination="origination",
                startover_window_seconds=123,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                time_delay_seconds=123,
                whitelist=["whitelist"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82977f54939485256df122f4611462d11e3def1637a024ed9be447f9f6b4a9d5)
            check_type(argname="argument authorization", value=authorization, expected_type=type_hints["authorization"])
            check_type(argname="argument channel_id", value=channel_id, expected_type=type_hints["channel_id"])
            check_type(argname="argument cmaf_package", value=cmaf_package, expected_type=type_hints["cmaf_package"])
            check_type(argname="argument dash_package", value=dash_package, expected_type=type_hints["dash_package"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument hls_package", value=hls_package, expected_type=type_hints["hls_package"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument manifest_name", value=manifest_name, expected_type=type_hints["manifest_name"])
            check_type(argname="argument mss_package", value=mss_package, expected_type=type_hints["mss_package"])
            check_type(argname="argument origination", value=origination, expected_type=type_hints["origination"])
            check_type(argname="argument startover_window_seconds", value=startover_window_seconds, expected_type=type_hints["startover_window_seconds"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument time_delay_seconds", value=time_delay_seconds, expected_type=type_hints["time_delay_seconds"])
            check_type(argname="argument whitelist", value=whitelist, expected_type=type_hints["whitelist"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if authorization is not None:
            self._values["authorization"] = authorization
        if channel_id is not None:
            self._values["channel_id"] = channel_id
        if cmaf_package is not None:
            self._values["cmaf_package"] = cmaf_package
        if dash_package is not None:
            self._values["dash_package"] = dash_package
        if description is not None:
            self._values["description"] = description
        if hls_package is not None:
            self._values["hls_package"] = hls_package
        if id is not None:
            self._values["id"] = id
        if manifest_name is not None:
            self._values["manifest_name"] = manifest_name
        if mss_package is not None:
            self._values["mss_package"] = mss_package
        if origination is not None:
            self._values["origination"] = origination
        if startover_window_seconds is not None:
            self._values["startover_window_seconds"] = startover_window_seconds
        if tags is not None:
            self._values["tags"] = tags
        if time_delay_seconds is not None:
            self._values["time_delay_seconds"] = time_delay_seconds
        if whitelist is not None:
            self._values["whitelist"] = whitelist

    @builtins.property
    def authorization(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.AuthorizationProperty"]]:
        '''Parameters for CDN authorization.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-originendpoint.html#cfn-mediapackage-originendpoint-authorization
        '''
        result = self._values.get("authorization")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.AuthorizationProperty"]], result)

    @builtins.property
    def channel_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the channel associated with this endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-originendpoint.html#cfn-mediapackage-originendpoint-channelid
        '''
        result = self._values.get("channel_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cmaf_package(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.CmafPackageProperty"]]:
        '''Parameters for Common Media Application Format (CMAF) packaging.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-originendpoint.html#cfn-mediapackage-originendpoint-cmafpackage
        '''
        result = self._values.get("cmaf_package")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.CmafPackageProperty"]], result)

    @builtins.property
    def dash_package(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.DashPackageProperty"]]:
        '''Parameters for DASH packaging.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-originendpoint.html#cfn-mediapackage-originendpoint-dashpackage
        '''
        result = self._values.get("dash_package")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.DashPackageProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Any descriptive information that you want to add to the endpoint for future identification purposes.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-originendpoint.html#cfn-mediapackage-originendpoint-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hls_package(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.HlsPackageProperty"]]:
        '''Parameters for Apple HLS packaging.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-originendpoint.html#cfn-mediapackage-originendpoint-hlspackage
        '''
        result = self._values.get("hls_package")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.HlsPackageProperty"]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''The manifest ID is required and must be unique within the OriginEndpoint.

        The ID can't be changed after the endpoint is created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-originendpoint.html#cfn-mediapackage-originendpoint-id
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def manifest_name(self) -> typing.Optional[builtins.str]:
        '''A short string that's appended to the end of the endpoint URL to create a unique path to this endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-originendpoint.html#cfn-mediapackage-originendpoint-manifestname
        '''
        result = self._values.get("manifest_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mss_package(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.MssPackageProperty"]]:
        '''Parameters for Microsoft Smooth Streaming packaging.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-originendpoint.html#cfn-mediapackage-originendpoint-msspackage
        '''
        result = self._values.get("mss_package")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.MssPackageProperty"]], result)

    @builtins.property
    def origination(self) -> typing.Optional[builtins.str]:
        '''Controls video origination from this endpoint.

        Valid values:

        - ``ALLOW`` - enables this endpoint to serve content to requesting devices.
        - ``DENY`` - prevents this endpoint from serving content. Denying origination is helpful for harvesting live-to-VOD assets. For more information about harvesting and origination, see `Live-to-VOD Requirements <https://docs.aws.amazon.com/mediapackage/latest/ug/ltov-reqmts.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-originendpoint.html#cfn-mediapackage-originendpoint-origination
        '''
        result = self._values.get("origination")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def startover_window_seconds(self) -> typing.Optional[jsii.Number]:
        '''Maximum duration (seconds) of content to retain for startover playback.

        Omit this attribute or enter ``0`` to indicate that startover playback is disabled for this endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-originendpoint.html#cfn-mediapackage-originendpoint-startoverwindowseconds
        '''
        result = self._values.get("startover_window_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags to assign to the endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-originendpoint.html#cfn-mediapackage-originendpoint-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def time_delay_seconds(self) -> typing.Optional[jsii.Number]:
        '''Minimum duration (seconds) of delay to enforce on the playback of live content.

        Omit this attribute or enter ``0`` to indicate that there is no time delay in effect for this endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-originendpoint.html#cfn-mediapackage-originendpoint-timedelayseconds
        '''
        result = self._values.get("time_delay_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def whitelist(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The IP addresses that can access this endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-originendpoint.html#cfn-mediapackage-originendpoint-whitelist
        '''
        result = self._values.get("whitelist")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnOriginEndpointMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnOriginEndpointPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.mixins.CfnOriginEndpointPropsMixin",
):
    '''Create an endpoint on an AWS Elemental MediaPackage channel.

    An endpoint represents a single delivery point of a channel, and defines content output handling through various components, such as packaging protocols, DRM and encryption integration, and more.

    After it's created, an endpoint provides a fixed public URL. This URL remains the same throughout the lifetime of the endpoint, regardless of any failures or upgrades that might occur. Integrate the URL with a downstream CDN (such as Amazon CloudFront) or playback device.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-originendpoint.html
    :cloudformationResource: AWS::MediaPackage::OriginEndpoint
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_mediapackage import mixins as mediapackage_mixins
        
        cfn_origin_endpoint_props_mixin = mediapackage_mixins.CfnOriginEndpointPropsMixin(mediapackage_mixins.CfnOriginEndpointMixinProps(
            authorization=mediapackage_mixins.CfnOriginEndpointPropsMixin.AuthorizationProperty(
                cdn_identifier_secret="cdnIdentifierSecret",
                secrets_role_arn="secretsRoleArn"
            ),
            channel_id="channelId",
            cmaf_package=mediapackage_mixins.CfnOriginEndpointPropsMixin.CmafPackageProperty(
                encryption=mediapackage_mixins.CfnOriginEndpointPropsMixin.CmafEncryptionProperty(
                    constant_initialization_vector="constantInitializationVector",
                    encryption_method="encryptionMethod",
                    key_rotation_interval_seconds=123,
                    speke_key_provider=mediapackage_mixins.CfnOriginEndpointPropsMixin.SpekeKeyProviderProperty(
                        certificate_arn="certificateArn",
                        encryption_contract_configuration=mediapackage_mixins.CfnOriginEndpointPropsMixin.EncryptionContractConfigurationProperty(
                            preset_speke20_audio="presetSpeke20Audio",
                            preset_speke20_video="presetSpeke20Video"
                        ),
                        resource_id="resourceId",
                        role_arn="roleArn",
                        system_ids=["systemIds"],
                        url="url"
                    )
                ),
                hls_manifests=[mediapackage_mixins.CfnOriginEndpointPropsMixin.HlsManifestProperty(
                    ad_markers="adMarkers",
                    ads_on_delivery_restrictions="adsOnDeliveryRestrictions",
                    ad_triggers=["adTriggers"],
                    id="id",
                    include_iframe_only_stream=False,
                    manifest_name="manifestName",
                    playlist_type="playlistType",
                    playlist_window_seconds=123,
                    program_date_time_interval_seconds=123,
                    url="url"
                )],
                segment_duration_seconds=123,
                segment_prefix="segmentPrefix",
                stream_selection=mediapackage_mixins.CfnOriginEndpointPropsMixin.StreamSelectionProperty(
                    max_video_bits_per_second=123,
                    min_video_bits_per_second=123,
                    stream_order="streamOrder"
                )
            ),
            dash_package=mediapackage_mixins.CfnOriginEndpointPropsMixin.DashPackageProperty(
                ads_on_delivery_restrictions="adsOnDeliveryRestrictions",
                ad_triggers=["adTriggers"],
                encryption=mediapackage_mixins.CfnOriginEndpointPropsMixin.DashEncryptionProperty(
                    key_rotation_interval_seconds=123,
                    speke_key_provider=mediapackage_mixins.CfnOriginEndpointPropsMixin.SpekeKeyProviderProperty(
                        certificate_arn="certificateArn",
                        encryption_contract_configuration=mediapackage_mixins.CfnOriginEndpointPropsMixin.EncryptionContractConfigurationProperty(
                            preset_speke20_audio="presetSpeke20Audio",
                            preset_speke20_video="presetSpeke20Video"
                        ),
                        resource_id="resourceId",
                        role_arn="roleArn",
                        system_ids=["systemIds"],
                        url="url"
                    )
                ),
                include_iframe_only_stream=False,
                manifest_layout="manifestLayout",
                manifest_window_seconds=123,
                min_buffer_time_seconds=123,
                min_update_period_seconds=123,
                period_triggers=["periodTriggers"],
                profile="profile",
                segment_duration_seconds=123,
                segment_template_format="segmentTemplateFormat",
                stream_selection=mediapackage_mixins.CfnOriginEndpointPropsMixin.StreamSelectionProperty(
                    max_video_bits_per_second=123,
                    min_video_bits_per_second=123,
                    stream_order="streamOrder"
                ),
                suggested_presentation_delay_seconds=123,
                utc_timing="utcTiming",
                utc_timing_uri="utcTimingUri"
            ),
            description="description",
            hls_package=mediapackage_mixins.CfnOriginEndpointPropsMixin.HlsPackageProperty(
                ad_markers="adMarkers",
                ads_on_delivery_restrictions="adsOnDeliveryRestrictions",
                ad_triggers=["adTriggers"],
                encryption=mediapackage_mixins.CfnOriginEndpointPropsMixin.HlsEncryptionProperty(
                    constant_initialization_vector="constantInitializationVector",
                    encryption_method="encryptionMethod",
                    key_rotation_interval_seconds=123,
                    repeat_ext_xKey=False,
                    speke_key_provider=mediapackage_mixins.CfnOriginEndpointPropsMixin.SpekeKeyProviderProperty(
                        certificate_arn="certificateArn",
                        encryption_contract_configuration=mediapackage_mixins.CfnOriginEndpointPropsMixin.EncryptionContractConfigurationProperty(
                            preset_speke20_audio="presetSpeke20Audio",
                            preset_speke20_video="presetSpeke20Video"
                        ),
                        resource_id="resourceId",
                        role_arn="roleArn",
                        system_ids=["systemIds"],
                        url="url"
                    )
                ),
                include_dvb_subtitles=False,
                include_iframe_only_stream=False,
                playlist_type="playlistType",
                playlist_window_seconds=123,
                program_date_time_interval_seconds=123,
                segment_duration_seconds=123,
                stream_selection=mediapackage_mixins.CfnOriginEndpointPropsMixin.StreamSelectionProperty(
                    max_video_bits_per_second=123,
                    min_video_bits_per_second=123,
                    stream_order="streamOrder"
                ),
                use_audio_rendition_group=False
            ),
            id="id",
            manifest_name="manifestName",
            mss_package=mediapackage_mixins.CfnOriginEndpointPropsMixin.MssPackageProperty(
                encryption=mediapackage_mixins.CfnOriginEndpointPropsMixin.MssEncryptionProperty(
                    speke_key_provider=mediapackage_mixins.CfnOriginEndpointPropsMixin.SpekeKeyProviderProperty(
                        certificate_arn="certificateArn",
                        encryption_contract_configuration=mediapackage_mixins.CfnOriginEndpointPropsMixin.EncryptionContractConfigurationProperty(
                            preset_speke20_audio="presetSpeke20Audio",
                            preset_speke20_video="presetSpeke20Video"
                        ),
                        resource_id="resourceId",
                        role_arn="roleArn",
                        system_ids=["systemIds"],
                        url="url"
                    )
                ),
                manifest_window_seconds=123,
                segment_duration_seconds=123,
                stream_selection=mediapackage_mixins.CfnOriginEndpointPropsMixin.StreamSelectionProperty(
                    max_video_bits_per_second=123,
                    min_video_bits_per_second=123,
                    stream_order="streamOrder"
                )
            ),
            origination="origination",
            startover_window_seconds=123,
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            time_delay_seconds=123,
            whitelist=["whitelist"]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnOriginEndpointMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::MediaPackage::OriginEndpoint``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c82cdcb6373ea0631858d58c6052cb18fd1e48e5351290e8265d019c27f7601)
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
            type_hints = typing.get_type_hints(_typecheckingstub__08f61c382d971d27740b766125ba45a38522302cd6db336f16fb14d4c421d1a8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6257233aa05faa718918e5d2cc805ba1d51f680b11a1c0c5caecebe58c34f4c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnOriginEndpointMixinProps:
        return typing.cast(CfnOriginEndpointMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.mixins.CfnOriginEndpointPropsMixin.AuthorizationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cdn_identifier_secret": "cdnIdentifierSecret",
            "secrets_role_arn": "secretsRoleArn",
        },
    )
    class AuthorizationProperty:
        def __init__(
            self,
            *,
            cdn_identifier_secret: typing.Optional[builtins.str] = None,
            secrets_role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Parameters for enabling CDN authorization on the endpoint.

            :param cdn_identifier_secret: The Amazon Resource Name (ARN) for the secret in AWS Secrets Manager that your Content Delivery Network (CDN) uses for authorization to access your endpoint.
            :param secrets_role_arn: The Amazon Resource Name (ARN) for the IAM role that allows AWS Elemental MediaPackage to communicate with AWS Secrets Manager .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-authorization.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackage import mixins as mediapackage_mixins
                
                authorization_property = mediapackage_mixins.CfnOriginEndpointPropsMixin.AuthorizationProperty(
                    cdn_identifier_secret="cdnIdentifierSecret",
                    secrets_role_arn="secretsRoleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0b392d35d5c91b98e4b01e13bdfda00996ddcab443969faa62cb790e5c7e81ab)
                check_type(argname="argument cdn_identifier_secret", value=cdn_identifier_secret, expected_type=type_hints["cdn_identifier_secret"])
                check_type(argname="argument secrets_role_arn", value=secrets_role_arn, expected_type=type_hints["secrets_role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cdn_identifier_secret is not None:
                self._values["cdn_identifier_secret"] = cdn_identifier_secret
            if secrets_role_arn is not None:
                self._values["secrets_role_arn"] = secrets_role_arn

        @builtins.property
        def cdn_identifier_secret(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) for the secret in AWS Secrets Manager that your Content Delivery Network (CDN) uses for authorization to access your endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-authorization.html#cfn-mediapackage-originendpoint-authorization-cdnidentifiersecret
            '''
            result = self._values.get("cdn_identifier_secret")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secrets_role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) for the IAM role that allows AWS Elemental MediaPackage to communicate with AWS Secrets Manager .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-authorization.html#cfn-mediapackage-originendpoint-authorization-secretsrolearn
            '''
            result = self._values.get("secrets_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthorizationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.mixins.CfnOriginEndpointPropsMixin.CmafEncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "constant_initialization_vector": "constantInitializationVector",
            "encryption_method": "encryptionMethod",
            "key_rotation_interval_seconds": "keyRotationIntervalSeconds",
            "speke_key_provider": "spekeKeyProvider",
        },
    )
    class CmafEncryptionProperty:
        def __init__(
            self,
            *,
            constant_initialization_vector: typing.Optional[builtins.str] = None,
            encryption_method: typing.Optional[builtins.str] = None,
            key_rotation_interval_seconds: typing.Optional[jsii.Number] = None,
            speke_key_provider: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.SpekeKeyProviderProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Holds encryption information so that access to the content can be controlled by a DRM solution.

            :param constant_initialization_vector: An optional 128-bit, 16-byte hex value represented by a 32-character string, used in conjunction with the key for encrypting blocks. If you don't specify a value, then AWS Elemental MediaPackage creates the constant initialization vector (IV).
            :param encryption_method: The encryption method to use.
            :param key_rotation_interval_seconds: Number of seconds before AWS Elemental MediaPackage rotates to a new key. By default, rotation is set to 60 seconds. Set to ``0`` to disable key rotation.
            :param speke_key_provider: Parameters for the SPEKE key provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-cmafencryption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackage import mixins as mediapackage_mixins
                
                cmaf_encryption_property = mediapackage_mixins.CfnOriginEndpointPropsMixin.CmafEncryptionProperty(
                    constant_initialization_vector="constantInitializationVector",
                    encryption_method="encryptionMethod",
                    key_rotation_interval_seconds=123,
                    speke_key_provider=mediapackage_mixins.CfnOriginEndpointPropsMixin.SpekeKeyProviderProperty(
                        certificate_arn="certificateArn",
                        encryption_contract_configuration=mediapackage_mixins.CfnOriginEndpointPropsMixin.EncryptionContractConfigurationProperty(
                            preset_speke20_audio="presetSpeke20Audio",
                            preset_speke20_video="presetSpeke20Video"
                        ),
                        resource_id="resourceId",
                        role_arn="roleArn",
                        system_ids=["systemIds"],
                        url="url"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d74b82d728039352b424e39a4bfdd8afbf512b6d09f94e427aa42926cba5823a)
                check_type(argname="argument constant_initialization_vector", value=constant_initialization_vector, expected_type=type_hints["constant_initialization_vector"])
                check_type(argname="argument encryption_method", value=encryption_method, expected_type=type_hints["encryption_method"])
                check_type(argname="argument key_rotation_interval_seconds", value=key_rotation_interval_seconds, expected_type=type_hints["key_rotation_interval_seconds"])
                check_type(argname="argument speke_key_provider", value=speke_key_provider, expected_type=type_hints["speke_key_provider"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if constant_initialization_vector is not None:
                self._values["constant_initialization_vector"] = constant_initialization_vector
            if encryption_method is not None:
                self._values["encryption_method"] = encryption_method
            if key_rotation_interval_seconds is not None:
                self._values["key_rotation_interval_seconds"] = key_rotation_interval_seconds
            if speke_key_provider is not None:
                self._values["speke_key_provider"] = speke_key_provider

        @builtins.property
        def constant_initialization_vector(self) -> typing.Optional[builtins.str]:
            '''An optional 128-bit, 16-byte hex value represented by a 32-character string, used in conjunction with the key for encrypting blocks.

            If you don't specify a value, then AWS Elemental MediaPackage creates the constant initialization vector (IV).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-cmafencryption.html#cfn-mediapackage-originendpoint-cmafencryption-constantinitializationvector
            '''
            result = self._values.get("constant_initialization_vector")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def encryption_method(self) -> typing.Optional[builtins.str]:
            '''The encryption method to use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-cmafencryption.html#cfn-mediapackage-originendpoint-cmafencryption-encryptionmethod
            '''
            result = self._values.get("encryption_method")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key_rotation_interval_seconds(self) -> typing.Optional[jsii.Number]:
            '''Number of seconds before AWS Elemental MediaPackage rotates to a new key.

            By default, rotation is set to 60 seconds. Set to ``0`` to disable key rotation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-cmafencryption.html#cfn-mediapackage-originendpoint-cmafencryption-keyrotationintervalseconds
            '''
            result = self._values.get("key_rotation_interval_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def speke_key_provider(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.SpekeKeyProviderProperty"]]:
            '''Parameters for the SPEKE key provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-cmafencryption.html#cfn-mediapackage-originendpoint-cmafencryption-spekekeyprovider
            '''
            result = self._values.get("speke_key_provider")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.SpekeKeyProviderProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CmafEncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.mixins.CfnOriginEndpointPropsMixin.CmafPackageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "encryption": "encryption",
            "hls_manifests": "hlsManifests",
            "segment_duration_seconds": "segmentDurationSeconds",
            "segment_prefix": "segmentPrefix",
            "stream_selection": "streamSelection",
        },
    )
    class CmafPackageProperty:
        def __init__(
            self,
            *,
            encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.CmafEncryptionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            hls_manifests: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.HlsManifestProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            segment_duration_seconds: typing.Optional[jsii.Number] = None,
            segment_prefix: typing.Optional[builtins.str] = None,
            stream_selection: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.StreamSelectionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Parameters for Common Media Application Format (CMAF) packaging.

            :param encryption: Parameters for encrypting content.
            :param hls_manifests: A list of HLS manifest configurations that are available from this endpoint.
            :param segment_duration_seconds: Duration (in seconds) of each segment. Actual segments are rounded to the nearest multiple of the source segment duration.
            :param segment_prefix: An optional custom string that is prepended to the name of each segment. If not specified, the segment prefix defaults to the ChannelId.
            :param stream_selection: Limitations for outputs from the endpoint, based on the video bitrate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-cmafpackage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackage import mixins as mediapackage_mixins
                
                cmaf_package_property = mediapackage_mixins.CfnOriginEndpointPropsMixin.CmafPackageProperty(
                    encryption=mediapackage_mixins.CfnOriginEndpointPropsMixin.CmafEncryptionProperty(
                        constant_initialization_vector="constantInitializationVector",
                        encryption_method="encryptionMethod",
                        key_rotation_interval_seconds=123,
                        speke_key_provider=mediapackage_mixins.CfnOriginEndpointPropsMixin.SpekeKeyProviderProperty(
                            certificate_arn="certificateArn",
                            encryption_contract_configuration=mediapackage_mixins.CfnOriginEndpointPropsMixin.EncryptionContractConfigurationProperty(
                                preset_speke20_audio="presetSpeke20Audio",
                                preset_speke20_video="presetSpeke20Video"
                            ),
                            resource_id="resourceId",
                            role_arn="roleArn",
                            system_ids=["systemIds"],
                            url="url"
                        )
                    ),
                    hls_manifests=[mediapackage_mixins.CfnOriginEndpointPropsMixin.HlsManifestProperty(
                        ad_markers="adMarkers",
                        ads_on_delivery_restrictions="adsOnDeliveryRestrictions",
                        ad_triggers=["adTriggers"],
                        id="id",
                        include_iframe_only_stream=False,
                        manifest_name="manifestName",
                        playlist_type="playlistType",
                        playlist_window_seconds=123,
                        program_date_time_interval_seconds=123,
                        url="url"
                    )],
                    segment_duration_seconds=123,
                    segment_prefix="segmentPrefix",
                    stream_selection=mediapackage_mixins.CfnOriginEndpointPropsMixin.StreamSelectionProperty(
                        max_video_bits_per_second=123,
                        min_video_bits_per_second=123,
                        stream_order="streamOrder"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b777c2f2cfa22aa9587c33291dd88839d00a23a73151c30bc211900bb257b8e5)
                check_type(argname="argument encryption", value=encryption, expected_type=type_hints["encryption"])
                check_type(argname="argument hls_manifests", value=hls_manifests, expected_type=type_hints["hls_manifests"])
                check_type(argname="argument segment_duration_seconds", value=segment_duration_seconds, expected_type=type_hints["segment_duration_seconds"])
                check_type(argname="argument segment_prefix", value=segment_prefix, expected_type=type_hints["segment_prefix"])
                check_type(argname="argument stream_selection", value=stream_selection, expected_type=type_hints["stream_selection"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encryption is not None:
                self._values["encryption"] = encryption
            if hls_manifests is not None:
                self._values["hls_manifests"] = hls_manifests
            if segment_duration_seconds is not None:
                self._values["segment_duration_seconds"] = segment_duration_seconds
            if segment_prefix is not None:
                self._values["segment_prefix"] = segment_prefix
            if stream_selection is not None:
                self._values["stream_selection"] = stream_selection

        @builtins.property
        def encryption(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.CmafEncryptionProperty"]]:
            '''Parameters for encrypting content.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-cmafpackage.html#cfn-mediapackage-originendpoint-cmafpackage-encryption
            '''
            result = self._values.get("encryption")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.CmafEncryptionProperty"]], result)

        @builtins.property
        def hls_manifests(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.HlsManifestProperty"]]]]:
            '''A list of HLS manifest configurations that are available from this endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-cmafpackage.html#cfn-mediapackage-originendpoint-cmafpackage-hlsmanifests
            '''
            result = self._values.get("hls_manifests")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.HlsManifestProperty"]]]], result)

        @builtins.property
        def segment_duration_seconds(self) -> typing.Optional[jsii.Number]:
            '''Duration (in seconds) of each segment.

            Actual segments are rounded to the nearest multiple of the source segment duration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-cmafpackage.html#cfn-mediapackage-originendpoint-cmafpackage-segmentdurationseconds
            '''
            result = self._values.get("segment_duration_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def segment_prefix(self) -> typing.Optional[builtins.str]:
            '''An optional custom string that is prepended to the name of each segment.

            If not specified, the segment prefix defaults to the ChannelId.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-cmafpackage.html#cfn-mediapackage-originendpoint-cmafpackage-segmentprefix
            '''
            result = self._values.get("segment_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def stream_selection(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.StreamSelectionProperty"]]:
            '''Limitations for outputs from the endpoint, based on the video bitrate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-cmafpackage.html#cfn-mediapackage-originendpoint-cmafpackage-streamselection
            '''
            result = self._values.get("stream_selection")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.StreamSelectionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CmafPackageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.mixins.CfnOriginEndpointPropsMixin.DashEncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "key_rotation_interval_seconds": "keyRotationIntervalSeconds",
            "speke_key_provider": "spekeKeyProvider",
        },
    )
    class DashEncryptionProperty:
        def __init__(
            self,
            *,
            key_rotation_interval_seconds: typing.Optional[jsii.Number] = None,
            speke_key_provider: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.SpekeKeyProviderProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Holds encryption information so that access to the content can be controlled by a DRM solution.

            :param key_rotation_interval_seconds: Number of seconds before AWS Elemental MediaPackage rotates to a new key. By default, rotation is set to 60 seconds. Set to ``0`` to disable key rotation.
            :param speke_key_provider: Parameters for the SPEKE key provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-dashencryption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackage import mixins as mediapackage_mixins
                
                dash_encryption_property = mediapackage_mixins.CfnOriginEndpointPropsMixin.DashEncryptionProperty(
                    key_rotation_interval_seconds=123,
                    speke_key_provider=mediapackage_mixins.CfnOriginEndpointPropsMixin.SpekeKeyProviderProperty(
                        certificate_arn="certificateArn",
                        encryption_contract_configuration=mediapackage_mixins.CfnOriginEndpointPropsMixin.EncryptionContractConfigurationProperty(
                            preset_speke20_audio="presetSpeke20Audio",
                            preset_speke20_video="presetSpeke20Video"
                        ),
                        resource_id="resourceId",
                        role_arn="roleArn",
                        system_ids=["systemIds"],
                        url="url"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7a0dcebfe3ea2121178a4b62e1ee60706cd338a19ac3eab8ad621d06ec1a78c8)
                check_type(argname="argument key_rotation_interval_seconds", value=key_rotation_interval_seconds, expected_type=type_hints["key_rotation_interval_seconds"])
                check_type(argname="argument speke_key_provider", value=speke_key_provider, expected_type=type_hints["speke_key_provider"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key_rotation_interval_seconds is not None:
                self._values["key_rotation_interval_seconds"] = key_rotation_interval_seconds
            if speke_key_provider is not None:
                self._values["speke_key_provider"] = speke_key_provider

        @builtins.property
        def key_rotation_interval_seconds(self) -> typing.Optional[jsii.Number]:
            '''Number of seconds before AWS Elemental MediaPackage rotates to a new key.

            By default, rotation is set to 60 seconds. Set to ``0`` to disable key rotation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-dashencryption.html#cfn-mediapackage-originendpoint-dashencryption-keyrotationintervalseconds
            '''
            result = self._values.get("key_rotation_interval_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def speke_key_provider(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.SpekeKeyProviderProperty"]]:
            '''Parameters for the SPEKE key provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-dashencryption.html#cfn-mediapackage-originendpoint-dashencryption-spekekeyprovider
            '''
            result = self._values.get("speke_key_provider")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.SpekeKeyProviderProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DashEncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.mixins.CfnOriginEndpointPropsMixin.DashPackageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ads_on_delivery_restrictions": "adsOnDeliveryRestrictions",
            "ad_triggers": "adTriggers",
            "encryption": "encryption",
            "include_iframe_only_stream": "includeIframeOnlyStream",
            "manifest_layout": "manifestLayout",
            "manifest_window_seconds": "manifestWindowSeconds",
            "min_buffer_time_seconds": "minBufferTimeSeconds",
            "min_update_period_seconds": "minUpdatePeriodSeconds",
            "period_triggers": "periodTriggers",
            "profile": "profile",
            "segment_duration_seconds": "segmentDurationSeconds",
            "segment_template_format": "segmentTemplateFormat",
            "stream_selection": "streamSelection",
            "suggested_presentation_delay_seconds": "suggestedPresentationDelaySeconds",
            "utc_timing": "utcTiming",
            "utc_timing_uri": "utcTimingUri",
        },
    )
    class DashPackageProperty:
        def __init__(
            self,
            *,
            ads_on_delivery_restrictions: typing.Optional[builtins.str] = None,
            ad_triggers: typing.Optional[typing.Sequence[builtins.str]] = None,
            encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.DashEncryptionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            include_iframe_only_stream: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            manifest_layout: typing.Optional[builtins.str] = None,
            manifest_window_seconds: typing.Optional[jsii.Number] = None,
            min_buffer_time_seconds: typing.Optional[jsii.Number] = None,
            min_update_period_seconds: typing.Optional[jsii.Number] = None,
            period_triggers: typing.Optional[typing.Sequence[builtins.str]] = None,
            profile: typing.Optional[builtins.str] = None,
            segment_duration_seconds: typing.Optional[jsii.Number] = None,
            segment_template_format: typing.Optional[builtins.str] = None,
            stream_selection: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.StreamSelectionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            suggested_presentation_delay_seconds: typing.Optional[jsii.Number] = None,
            utc_timing: typing.Optional[builtins.str] = None,
            utc_timing_uri: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Parameters for DASH packaging.

            :param ads_on_delivery_restrictions: The flags on SCTE-35 segmentation descriptors that have to be present for AWS Elemental MediaPackage to insert ad markers in the output manifest. For information about SCTE-35 in AWS Elemental MediaPackage , see `SCTE-35 Message Options in AWS Elemental MediaPackage <https://docs.aws.amazon.com/mediapackage/latest/ug/scte.html>`_ .
            :param ad_triggers: Specifies the SCTE-35 message types that AWS Elemental MediaPackage treats as ad markers in the output manifest. Valid values: - ``BREAK`` - ``DISTRIBUTOR_ADVERTISEMENT`` - ``DISTRIBUTOR_OVERLAY_PLACEMENT_OPPORTUNITY`` . - ``DISTRIBUTOR_PLACEMENT_OPPORTUNITY`` . - ``PROVIDER_ADVERTISEMENT`` . - ``PROVIDER_OVERLAY_PLACEMENT_OPPORTUNITY`` . - ``PROVIDER_PLACEMENT_OPPORTUNITY`` . - ``SPLICE_INSERT`` .
            :param encryption: Parameters for encrypting content.
            :param include_iframe_only_stream: This applies only to stream sets with a single video track. When true, the stream set includes an additional I-frame trick-play only stream, along with the other tracks. If false, this extra stream is not included.
            :param manifest_layout: Determines the position of some tags in the manifest. Valid values: - ``FULL`` - Elements like ``SegmentTemplate`` and ``ContentProtection`` are included in each ``Representation`` . - ``COMPACT`` - Duplicate elements are combined and presented at the ``AdaptationSet`` level.
            :param manifest_window_seconds: Time window (in seconds) contained in each manifest.
            :param min_buffer_time_seconds: Minimum amount of content (measured in seconds) that a player must keep available in the buffer.
            :param min_update_period_seconds: Minimum amount of time (in seconds) that the player should wait before requesting updates to the manifest.
            :param period_triggers: Controls whether AWS Elemental MediaPackage produces single-period or multi-period DASH manifests. For more information about periods, see `Multi-period DASH in AWS Elemental MediaPackage <https://docs.aws.amazon.com/mediapackage/latest/ug/multi-period.html>`_ . Valid values: - ``ADS`` - AWS Elemental MediaPackage will produce multi-period DASH manifests. Periods are created based on the SCTE-35 ad markers present in the input manifest. - *No value* - AWS Elemental MediaPackage will produce single-period DASH manifests. This is the default setting.
            :param profile: The DASH profile for the output. Valid values: - ``NONE`` - The output doesn't use a DASH profile. - ``HBBTV_1_5`` - The output is compliant with HbbTV v1.5. - ``DVB_DASH_2014`` - The output is compliant with DVB-DASH 2014.
            :param segment_duration_seconds: Duration (in seconds) of each fragment. Actual fragments are rounded to the nearest multiple of the source fragment duration.
            :param segment_template_format: Determines the type of variable used in the ``media`` URL of the ``SegmentTemplate`` tag in the manifest. Also specifies if segment timeline information is included in ``SegmentTimeline`` or ``SegmentTemplate`` . Valid values: - ``NUMBER_WITH_TIMELINE`` - The ``$Number$`` variable is used in the ``media`` URL. The value of this variable is the sequential number of the segment. A full ``SegmentTimeline`` object is presented in each ``SegmentTemplate`` . - ``NUMBER_WITH_DURATION`` - The ``$Number$`` variable is used in the ``media`` URL and a ``duration`` attribute is added to the segment template. The ``SegmentTimeline`` object is removed from the representation. - ``TIME_WITH_TIMELINE`` - The ``$Time$`` variable is used in the ``media`` URL. The value of this variable is the timestamp of when the segment starts. A full ``SegmentTimeline`` object is presented in each ``SegmentTemplate`` .
            :param stream_selection: Limitations for outputs from the endpoint, based on the video bitrate.
            :param suggested_presentation_delay_seconds: Amount of time (in seconds) that the player should be from the live point at the end of the manifest.
            :param utc_timing: Determines the type of UTC timing included in the DASH Media Presentation Description (MPD).
            :param utc_timing_uri: Specifies the value attribute of the UTC timing field when utcTiming is set to HTTP-ISO or HTTP-HEAD.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-dashpackage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackage import mixins as mediapackage_mixins
                
                dash_package_property = mediapackage_mixins.CfnOriginEndpointPropsMixin.DashPackageProperty(
                    ads_on_delivery_restrictions="adsOnDeliveryRestrictions",
                    ad_triggers=["adTriggers"],
                    encryption=mediapackage_mixins.CfnOriginEndpointPropsMixin.DashEncryptionProperty(
                        key_rotation_interval_seconds=123,
                        speke_key_provider=mediapackage_mixins.CfnOriginEndpointPropsMixin.SpekeKeyProviderProperty(
                            certificate_arn="certificateArn",
                            encryption_contract_configuration=mediapackage_mixins.CfnOriginEndpointPropsMixin.EncryptionContractConfigurationProperty(
                                preset_speke20_audio="presetSpeke20Audio",
                                preset_speke20_video="presetSpeke20Video"
                            ),
                            resource_id="resourceId",
                            role_arn="roleArn",
                            system_ids=["systemIds"],
                            url="url"
                        )
                    ),
                    include_iframe_only_stream=False,
                    manifest_layout="manifestLayout",
                    manifest_window_seconds=123,
                    min_buffer_time_seconds=123,
                    min_update_period_seconds=123,
                    period_triggers=["periodTriggers"],
                    profile="profile",
                    segment_duration_seconds=123,
                    segment_template_format="segmentTemplateFormat",
                    stream_selection=mediapackage_mixins.CfnOriginEndpointPropsMixin.StreamSelectionProperty(
                        max_video_bits_per_second=123,
                        min_video_bits_per_second=123,
                        stream_order="streamOrder"
                    ),
                    suggested_presentation_delay_seconds=123,
                    utc_timing="utcTiming",
                    utc_timing_uri="utcTimingUri"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f6f25b74519cc5c9c610c9e025b52e0b21c1070662a37ed36073a1d962a9ef83)
                check_type(argname="argument ads_on_delivery_restrictions", value=ads_on_delivery_restrictions, expected_type=type_hints["ads_on_delivery_restrictions"])
                check_type(argname="argument ad_triggers", value=ad_triggers, expected_type=type_hints["ad_triggers"])
                check_type(argname="argument encryption", value=encryption, expected_type=type_hints["encryption"])
                check_type(argname="argument include_iframe_only_stream", value=include_iframe_only_stream, expected_type=type_hints["include_iframe_only_stream"])
                check_type(argname="argument manifest_layout", value=manifest_layout, expected_type=type_hints["manifest_layout"])
                check_type(argname="argument manifest_window_seconds", value=manifest_window_seconds, expected_type=type_hints["manifest_window_seconds"])
                check_type(argname="argument min_buffer_time_seconds", value=min_buffer_time_seconds, expected_type=type_hints["min_buffer_time_seconds"])
                check_type(argname="argument min_update_period_seconds", value=min_update_period_seconds, expected_type=type_hints["min_update_period_seconds"])
                check_type(argname="argument period_triggers", value=period_triggers, expected_type=type_hints["period_triggers"])
                check_type(argname="argument profile", value=profile, expected_type=type_hints["profile"])
                check_type(argname="argument segment_duration_seconds", value=segment_duration_seconds, expected_type=type_hints["segment_duration_seconds"])
                check_type(argname="argument segment_template_format", value=segment_template_format, expected_type=type_hints["segment_template_format"])
                check_type(argname="argument stream_selection", value=stream_selection, expected_type=type_hints["stream_selection"])
                check_type(argname="argument suggested_presentation_delay_seconds", value=suggested_presentation_delay_seconds, expected_type=type_hints["suggested_presentation_delay_seconds"])
                check_type(argname="argument utc_timing", value=utc_timing, expected_type=type_hints["utc_timing"])
                check_type(argname="argument utc_timing_uri", value=utc_timing_uri, expected_type=type_hints["utc_timing_uri"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ads_on_delivery_restrictions is not None:
                self._values["ads_on_delivery_restrictions"] = ads_on_delivery_restrictions
            if ad_triggers is not None:
                self._values["ad_triggers"] = ad_triggers
            if encryption is not None:
                self._values["encryption"] = encryption
            if include_iframe_only_stream is not None:
                self._values["include_iframe_only_stream"] = include_iframe_only_stream
            if manifest_layout is not None:
                self._values["manifest_layout"] = manifest_layout
            if manifest_window_seconds is not None:
                self._values["manifest_window_seconds"] = manifest_window_seconds
            if min_buffer_time_seconds is not None:
                self._values["min_buffer_time_seconds"] = min_buffer_time_seconds
            if min_update_period_seconds is not None:
                self._values["min_update_period_seconds"] = min_update_period_seconds
            if period_triggers is not None:
                self._values["period_triggers"] = period_triggers
            if profile is not None:
                self._values["profile"] = profile
            if segment_duration_seconds is not None:
                self._values["segment_duration_seconds"] = segment_duration_seconds
            if segment_template_format is not None:
                self._values["segment_template_format"] = segment_template_format
            if stream_selection is not None:
                self._values["stream_selection"] = stream_selection
            if suggested_presentation_delay_seconds is not None:
                self._values["suggested_presentation_delay_seconds"] = suggested_presentation_delay_seconds
            if utc_timing is not None:
                self._values["utc_timing"] = utc_timing
            if utc_timing_uri is not None:
                self._values["utc_timing_uri"] = utc_timing_uri

        @builtins.property
        def ads_on_delivery_restrictions(self) -> typing.Optional[builtins.str]:
            '''The flags on SCTE-35 segmentation descriptors that have to be present for AWS Elemental MediaPackage to insert ad markers in the output manifest.

            For information about SCTE-35 in AWS Elemental MediaPackage , see `SCTE-35 Message Options in AWS Elemental MediaPackage <https://docs.aws.amazon.com/mediapackage/latest/ug/scte.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-dashpackage.html#cfn-mediapackage-originendpoint-dashpackage-adsondeliveryrestrictions
            '''
            result = self._values.get("ads_on_delivery_restrictions")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ad_triggers(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Specifies the SCTE-35 message types that AWS Elemental MediaPackage treats as ad markers in the output manifest.

            Valid values:

            - ``BREAK``
            - ``DISTRIBUTOR_ADVERTISEMENT``
            - ``DISTRIBUTOR_OVERLAY_PLACEMENT_OPPORTUNITY`` .
            - ``DISTRIBUTOR_PLACEMENT_OPPORTUNITY`` .
            - ``PROVIDER_ADVERTISEMENT`` .
            - ``PROVIDER_OVERLAY_PLACEMENT_OPPORTUNITY`` .
            - ``PROVIDER_PLACEMENT_OPPORTUNITY`` .
            - ``SPLICE_INSERT`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-dashpackage.html#cfn-mediapackage-originendpoint-dashpackage-adtriggers
            '''
            result = self._values.get("ad_triggers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def encryption(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.DashEncryptionProperty"]]:
            '''Parameters for encrypting content.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-dashpackage.html#cfn-mediapackage-originendpoint-dashpackage-encryption
            '''
            result = self._values.get("encryption")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.DashEncryptionProperty"]], result)

        @builtins.property
        def include_iframe_only_stream(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''This applies only to stream sets with a single video track.

            When true, the stream set includes an additional I-frame trick-play only stream, along with the other tracks. If false, this extra stream is not included.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-dashpackage.html#cfn-mediapackage-originendpoint-dashpackage-includeiframeonlystream
            '''
            result = self._values.get("include_iframe_only_stream")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def manifest_layout(self) -> typing.Optional[builtins.str]:
            '''Determines the position of some tags in the manifest.

            Valid values:

            - ``FULL`` - Elements like ``SegmentTemplate`` and ``ContentProtection`` are included in each ``Representation`` .
            - ``COMPACT`` - Duplicate elements are combined and presented at the ``AdaptationSet`` level.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-dashpackage.html#cfn-mediapackage-originendpoint-dashpackage-manifestlayout
            '''
            result = self._values.get("manifest_layout")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def manifest_window_seconds(self) -> typing.Optional[jsii.Number]:
            '''Time window (in seconds) contained in each manifest.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-dashpackage.html#cfn-mediapackage-originendpoint-dashpackage-manifestwindowseconds
            '''
            result = self._values.get("manifest_window_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min_buffer_time_seconds(self) -> typing.Optional[jsii.Number]:
            '''Minimum amount of content (measured in seconds) that a player must keep available in the buffer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-dashpackage.html#cfn-mediapackage-originendpoint-dashpackage-minbuffertimeseconds
            '''
            result = self._values.get("min_buffer_time_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min_update_period_seconds(self) -> typing.Optional[jsii.Number]:
            '''Minimum amount of time (in seconds) that the player should wait before requesting updates to the manifest.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-dashpackage.html#cfn-mediapackage-originendpoint-dashpackage-minupdateperiodseconds
            '''
            result = self._values.get("min_update_period_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def period_triggers(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Controls whether AWS Elemental MediaPackage produces single-period or multi-period DASH manifests.

            For more information about periods, see `Multi-period DASH in AWS Elemental MediaPackage <https://docs.aws.amazon.com/mediapackage/latest/ug/multi-period.html>`_ .

            Valid values:

            - ``ADS`` - AWS Elemental MediaPackage will produce multi-period DASH manifests. Periods are created based on the SCTE-35 ad markers present in the input manifest.
            - *No value* - AWS Elemental MediaPackage will produce single-period DASH manifests. This is the default setting.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-dashpackage.html#cfn-mediapackage-originendpoint-dashpackage-periodtriggers
            '''
            result = self._values.get("period_triggers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def profile(self) -> typing.Optional[builtins.str]:
            '''The DASH profile for the output.

            Valid values:

            - ``NONE`` - The output doesn't use a DASH profile.
            - ``HBBTV_1_5`` - The output is compliant with HbbTV v1.5.
            - ``DVB_DASH_2014`` - The output is compliant with DVB-DASH 2014.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-dashpackage.html#cfn-mediapackage-originendpoint-dashpackage-profile
            '''
            result = self._values.get("profile")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def segment_duration_seconds(self) -> typing.Optional[jsii.Number]:
            '''Duration (in seconds) of each fragment.

            Actual fragments are rounded to the nearest multiple of the source fragment duration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-dashpackage.html#cfn-mediapackage-originendpoint-dashpackage-segmentdurationseconds
            '''
            result = self._values.get("segment_duration_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def segment_template_format(self) -> typing.Optional[builtins.str]:
            '''Determines the type of variable used in the ``media`` URL of the ``SegmentTemplate`` tag in the manifest.

            Also specifies if segment timeline information is included in ``SegmentTimeline`` or ``SegmentTemplate`` .

            Valid values:

            - ``NUMBER_WITH_TIMELINE`` - The ``$Number$`` variable is used in the ``media`` URL. The value of this variable is the sequential number of the segment. A full ``SegmentTimeline`` object is presented in each ``SegmentTemplate`` .
            - ``NUMBER_WITH_DURATION`` - The ``$Number$`` variable is used in the ``media`` URL and a ``duration`` attribute is added to the segment template. The ``SegmentTimeline`` object is removed from the representation.
            - ``TIME_WITH_TIMELINE`` - The ``$Time$`` variable is used in the ``media`` URL. The value of this variable is the timestamp of when the segment starts. A full ``SegmentTimeline`` object is presented in each ``SegmentTemplate`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-dashpackage.html#cfn-mediapackage-originendpoint-dashpackage-segmenttemplateformat
            '''
            result = self._values.get("segment_template_format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def stream_selection(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.StreamSelectionProperty"]]:
            '''Limitations for outputs from the endpoint, based on the video bitrate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-dashpackage.html#cfn-mediapackage-originendpoint-dashpackage-streamselection
            '''
            result = self._values.get("stream_selection")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.StreamSelectionProperty"]], result)

        @builtins.property
        def suggested_presentation_delay_seconds(self) -> typing.Optional[jsii.Number]:
            '''Amount of time (in seconds) that the player should be from the live point at the end of the manifest.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-dashpackage.html#cfn-mediapackage-originendpoint-dashpackage-suggestedpresentationdelayseconds
            '''
            result = self._values.get("suggested_presentation_delay_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def utc_timing(self) -> typing.Optional[builtins.str]:
            '''Determines the type of UTC timing included in the DASH Media Presentation Description (MPD).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-dashpackage.html#cfn-mediapackage-originendpoint-dashpackage-utctiming
            '''
            result = self._values.get("utc_timing")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def utc_timing_uri(self) -> typing.Optional[builtins.str]:
            '''Specifies the value attribute of the UTC timing field when utcTiming is set to HTTP-ISO or HTTP-HEAD.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-dashpackage.html#cfn-mediapackage-originendpoint-dashpackage-utctiminguri
            '''
            result = self._values.get("utc_timing_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DashPackageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.mixins.CfnOriginEndpointPropsMixin.EncryptionContractConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "preset_speke20_audio": "presetSpeke20Audio",
            "preset_speke20_video": "presetSpeke20Video",
        },
    )
    class EncryptionContractConfigurationProperty:
        def __init__(
            self,
            *,
            preset_speke20_audio: typing.Optional[builtins.str] = None,
            preset_speke20_video: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Use ``encryptionContractConfiguration`` to configure one or more content encryption keys for your endpoints that use SPEKE Version 2.0. The encryption contract defines the content keys used to encrypt the audio and video tracks in your stream. To configure the encryption contract, specify which audio and video encryption presets to use. For more information about these presets, see `SPEKE Version 2.0 Presets <https://docs.aws.amazon.com/mediapackage/latest/ug/drm-content-speke-v2-presets.html>`_ .

            Note the following considerations when using ``encryptionContractConfiguration`` :

            - You can use ``encryptionContractConfiguration`` for DASH endpoints that use SPEKE Version 2.0. SPEKE Version 2.0 relies on the CPIX Version 2.3 specification.
            - You cannot combine an ``UNENCRYPTED`` preset with ``UNENCRYPTED`` or ``SHARED`` presets across ``presetSpeke20Audio`` and ``presetSpeke20Video`` .
            - When you use a ``SHARED`` preset, you must use it for both ``presetSpeke20Audio`` and ``presetSpeke20Video`` .

            :param preset_speke20_audio: A collection of audio encryption presets. Value description: - ``PRESET-AUDIO-1`` - Use one content key to encrypt all of the audio tracks in your stream. - ``PRESET-AUDIO-2`` - Use one content key to encrypt all of the stereo audio tracks and one content key to encrypt all of the multichannel audio tracks. - ``PRESET-AUDIO-3`` - Use one content key to encrypt all of the stereo audio tracks, one content key to encrypt all of the multichannel audio tracks with 3 to 6 channels, and one content key to encrypt all of the multichannel audio tracks with more than 6 channels. - ``SHARED`` - Use the same content key for all of the audio and video tracks in your stream. - ``UNENCRYPTED`` - Don't encrypt any of the audio tracks in your stream.
            :param preset_speke20_video: A collection of video encryption presets. Value description: - ``PRESET-VIDEO-1`` - Use one content key to encrypt all of the video tracks in your stream. - ``PRESET-VIDEO-2`` - Use one content key to encrypt all of the SD video tracks and one content key for all HD and higher resolutions video tracks. - ``PRESET-VIDEO-3`` - Use one content key to encrypt all of the SD video tracks, one content key for HD video tracks and one content key for all UHD video tracks. - ``PRESET-VIDEO-4`` - Use one content key to encrypt all of the SD video tracks, one content key for HD video tracks, one content key for all UHD1 video tracks and one content key for all UHD2 video tracks. - ``PRESET-VIDEO-5`` - Use one content key to encrypt all of the SD video tracks, one content key for HD1 video tracks, one content key for HD2 video tracks, one content key for all UHD1 video tracks and one content key for all UHD2 video tracks. - ``PRESET-VIDEO-6`` - Use one content key to encrypt all of the SD video tracks, one content key for HD1 video tracks, one content key for HD2 video tracks and one content key for all UHD video tracks. - ``PRESET-VIDEO-7`` - Use one content key to encrypt all of the SD+HD1 video tracks, one content key for HD2 video tracks and one content key for all UHD video tracks. - ``PRESET-VIDEO-8`` - Use one content key to encrypt all of the SD+HD1 video tracks, one content key for HD2 video tracks, one content key for all UHD1 video tracks and one content key for all UHD2 video tracks. - ``SHARED`` - Use the same content key for all of the video and audio tracks in your stream. - ``UNENCRYPTED`` - Don't encrypt any of the video tracks in your stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-encryptioncontractconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackage import mixins as mediapackage_mixins
                
                encryption_contract_configuration_property = mediapackage_mixins.CfnOriginEndpointPropsMixin.EncryptionContractConfigurationProperty(
                    preset_speke20_audio="presetSpeke20Audio",
                    preset_speke20_video="presetSpeke20Video"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2ca8ad2eba097ad61909c8108e91199aa63ec9b7c61cfb8321351d346c0b53ad)
                check_type(argname="argument preset_speke20_audio", value=preset_speke20_audio, expected_type=type_hints["preset_speke20_audio"])
                check_type(argname="argument preset_speke20_video", value=preset_speke20_video, expected_type=type_hints["preset_speke20_video"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if preset_speke20_audio is not None:
                self._values["preset_speke20_audio"] = preset_speke20_audio
            if preset_speke20_video is not None:
                self._values["preset_speke20_video"] = preset_speke20_video

        @builtins.property
        def preset_speke20_audio(self) -> typing.Optional[builtins.str]:
            '''A collection of audio encryption presets.

            Value description:

            - ``PRESET-AUDIO-1`` - Use one content key to encrypt all of the audio tracks in your stream.
            - ``PRESET-AUDIO-2`` - Use one content key to encrypt all of the stereo audio tracks and one content key to encrypt all of the multichannel audio tracks.
            - ``PRESET-AUDIO-3`` - Use one content key to encrypt all of the stereo audio tracks, one content key to encrypt all of the multichannel audio tracks with 3 to 6 channels, and one content key to encrypt all of the multichannel audio tracks with more than 6 channels.
            - ``SHARED`` - Use the same content key for all of the audio and video tracks in your stream.
            - ``UNENCRYPTED`` - Don't encrypt any of the audio tracks in your stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-encryptioncontractconfiguration.html#cfn-mediapackage-originendpoint-encryptioncontractconfiguration-presetspeke20audio
            '''
            result = self._values.get("preset_speke20_audio")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def preset_speke20_video(self) -> typing.Optional[builtins.str]:
            '''A collection of video encryption presets.

            Value description:

            - ``PRESET-VIDEO-1`` - Use one content key to encrypt all of the video tracks in your stream.
            - ``PRESET-VIDEO-2`` - Use one content key to encrypt all of the SD video tracks and one content key for all HD and higher resolutions video tracks.
            - ``PRESET-VIDEO-3`` - Use one content key to encrypt all of the SD video tracks, one content key for HD video tracks and one content key for all UHD video tracks.
            - ``PRESET-VIDEO-4`` - Use one content key to encrypt all of the SD video tracks, one content key for HD video tracks, one content key for all UHD1 video tracks and one content key for all UHD2 video tracks.
            - ``PRESET-VIDEO-5`` - Use one content key to encrypt all of the SD video tracks, one content key for HD1 video tracks, one content key for HD2 video tracks, one content key for all UHD1 video tracks and one content key for all UHD2 video tracks.
            - ``PRESET-VIDEO-6`` - Use one content key to encrypt all of the SD video tracks, one content key for HD1 video tracks, one content key for HD2 video tracks and one content key for all UHD video tracks.
            - ``PRESET-VIDEO-7`` - Use one content key to encrypt all of the SD+HD1 video tracks, one content key for HD2 video tracks and one content key for all UHD video tracks.
            - ``PRESET-VIDEO-8`` - Use one content key to encrypt all of the SD+HD1 video tracks, one content key for HD2 video tracks, one content key for all UHD1 video tracks and one content key for all UHD2 video tracks.
            - ``SHARED`` - Use the same content key for all of the video and audio tracks in your stream.
            - ``UNENCRYPTED`` - Don't encrypt any of the video tracks in your stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-encryptioncontractconfiguration.html#cfn-mediapackage-originendpoint-encryptioncontractconfiguration-presetspeke20video
            '''
            result = self._values.get("preset_speke20_video")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionContractConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.mixins.CfnOriginEndpointPropsMixin.HlsEncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "constant_initialization_vector": "constantInitializationVector",
            "encryption_method": "encryptionMethod",
            "key_rotation_interval_seconds": "keyRotationIntervalSeconds",
            "repeat_ext_x_key": "repeatExtXKey",
            "speke_key_provider": "spekeKeyProvider",
        },
    )
    class HlsEncryptionProperty:
        def __init__(
            self,
            *,
            constant_initialization_vector: typing.Optional[builtins.str] = None,
            encryption_method: typing.Optional[builtins.str] = None,
            key_rotation_interval_seconds: typing.Optional[jsii.Number] = None,
            repeat_ext_x_key: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            speke_key_provider: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.SpekeKeyProviderProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Holds encryption information so that access to the content can be controlled by a DRM solution.

            :param constant_initialization_vector: A 128-bit, 16-byte hex value represented by a 32-character string, used with the key for encrypting blocks.
            :param encryption_method: HLS encryption type.
            :param key_rotation_interval_seconds: Number of seconds before AWS Elemental MediaPackage rotates to a new key. By default, rotation is set to 60 seconds. Set to ``0`` to disable key rotation.
            :param repeat_ext_x_key: Repeat the ``EXT-X-KEY`` directive for every media segment. This might result in an increase in client requests to the DRM server.
            :param speke_key_provider: Parameters for the SPEKE key provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlsencryption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackage import mixins as mediapackage_mixins
                
                hls_encryption_property = mediapackage_mixins.CfnOriginEndpointPropsMixin.HlsEncryptionProperty(
                    constant_initialization_vector="constantInitializationVector",
                    encryption_method="encryptionMethod",
                    key_rotation_interval_seconds=123,
                    repeat_ext_xKey=False,
                    speke_key_provider=mediapackage_mixins.CfnOriginEndpointPropsMixin.SpekeKeyProviderProperty(
                        certificate_arn="certificateArn",
                        encryption_contract_configuration=mediapackage_mixins.CfnOriginEndpointPropsMixin.EncryptionContractConfigurationProperty(
                            preset_speke20_audio="presetSpeke20Audio",
                            preset_speke20_video="presetSpeke20Video"
                        ),
                        resource_id="resourceId",
                        role_arn="roleArn",
                        system_ids=["systemIds"],
                        url="url"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c56efdb9121ff2acfb5317b841a80b3cd0fc30160ac6a835533dc841d6c84247)
                check_type(argname="argument constant_initialization_vector", value=constant_initialization_vector, expected_type=type_hints["constant_initialization_vector"])
                check_type(argname="argument encryption_method", value=encryption_method, expected_type=type_hints["encryption_method"])
                check_type(argname="argument key_rotation_interval_seconds", value=key_rotation_interval_seconds, expected_type=type_hints["key_rotation_interval_seconds"])
                check_type(argname="argument repeat_ext_x_key", value=repeat_ext_x_key, expected_type=type_hints["repeat_ext_x_key"])
                check_type(argname="argument speke_key_provider", value=speke_key_provider, expected_type=type_hints["speke_key_provider"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if constant_initialization_vector is not None:
                self._values["constant_initialization_vector"] = constant_initialization_vector
            if encryption_method is not None:
                self._values["encryption_method"] = encryption_method
            if key_rotation_interval_seconds is not None:
                self._values["key_rotation_interval_seconds"] = key_rotation_interval_seconds
            if repeat_ext_x_key is not None:
                self._values["repeat_ext_x_key"] = repeat_ext_x_key
            if speke_key_provider is not None:
                self._values["speke_key_provider"] = speke_key_provider

        @builtins.property
        def constant_initialization_vector(self) -> typing.Optional[builtins.str]:
            '''A 128-bit, 16-byte hex value represented by a 32-character string, used with the key for encrypting blocks.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlsencryption.html#cfn-mediapackage-originendpoint-hlsencryption-constantinitializationvector
            '''
            result = self._values.get("constant_initialization_vector")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def encryption_method(self) -> typing.Optional[builtins.str]:
            '''HLS encryption type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlsencryption.html#cfn-mediapackage-originendpoint-hlsencryption-encryptionmethod
            '''
            result = self._values.get("encryption_method")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key_rotation_interval_seconds(self) -> typing.Optional[jsii.Number]:
            '''Number of seconds before AWS Elemental MediaPackage rotates to a new key.

            By default, rotation is set to 60 seconds. Set to ``0`` to disable key rotation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlsencryption.html#cfn-mediapackage-originendpoint-hlsencryption-keyrotationintervalseconds
            '''
            result = self._values.get("key_rotation_interval_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def repeat_ext_x_key(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Repeat the ``EXT-X-KEY`` directive for every media segment.

            This might result in an increase in client requests to the DRM server.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlsencryption.html#cfn-mediapackage-originendpoint-hlsencryption-repeatextxkey
            '''
            result = self._values.get("repeat_ext_x_key")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def speke_key_provider(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.SpekeKeyProviderProperty"]]:
            '''Parameters for the SPEKE key provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlsencryption.html#cfn-mediapackage-originendpoint-hlsencryption-spekekeyprovider
            '''
            result = self._values.get("speke_key_provider")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.SpekeKeyProviderProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HlsEncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.mixins.CfnOriginEndpointPropsMixin.HlsManifestProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ad_markers": "adMarkers",
            "ads_on_delivery_restrictions": "adsOnDeliveryRestrictions",
            "ad_triggers": "adTriggers",
            "id": "id",
            "include_iframe_only_stream": "includeIframeOnlyStream",
            "manifest_name": "manifestName",
            "playlist_type": "playlistType",
            "playlist_window_seconds": "playlistWindowSeconds",
            "program_date_time_interval_seconds": "programDateTimeIntervalSeconds",
            "url": "url",
        },
    )
    class HlsManifestProperty:
        def __init__(
            self,
            *,
            ad_markers: typing.Optional[builtins.str] = None,
            ads_on_delivery_restrictions: typing.Optional[builtins.str] = None,
            ad_triggers: typing.Optional[typing.Sequence[builtins.str]] = None,
            id: typing.Optional[builtins.str] = None,
            include_iframe_only_stream: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            manifest_name: typing.Optional[builtins.str] = None,
            playlist_type: typing.Optional[builtins.str] = None,
            playlist_window_seconds: typing.Optional[jsii.Number] = None,
            program_date_time_interval_seconds: typing.Optional[jsii.Number] = None,
            url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An HTTP Live Streaming (HLS) manifest configuration on a CMAF endpoint.

            :param ad_markers: Controls how ad markers are included in the packaged endpoint. Valid values: - ``NONE`` - Omits all SCTE-35 ad markers from the output. - ``PASSTHROUGH`` - Creates a copy in the output of the SCTE-35 ad markers (comments) taken directly from the input manifest. - ``SCTE35_ENHANCED`` - Generates ad markers and blackout tags in the output based on the SCTE-35 messages from the input manifest.
            :param ads_on_delivery_restrictions: The flags on SCTE-35 segmentation descriptors that have to be present for AWS Elemental MediaPackage to insert ad markers in the output manifest. For information about SCTE-35 in AWS Elemental MediaPackage , see `SCTE-35 Message Options in AWS Elemental MediaPackage <https://docs.aws.amazon.com/mediapackage/latest/ug/scte.html>`_ .
            :param ad_triggers: Specifies the SCTE-35 message types that AWS Elemental MediaPackage treats as ad markers in the output manifest. Valid values: - ``BREAK`` - ``DISTRIBUTOR_ADVERTISEMENT`` - ``DISTRIBUTOR_OVERLAY_PLACEMENT_OPPORTUNITY`` - ``DISTRIBUTOR_PLACEMENT_OPPORTUNITY`` - ``PROVIDER_ADVERTISEMENT`` - ``PROVIDER_OVERLAY_PLACEMENT_OPPORTUNITY`` - ``PROVIDER_PLACEMENT_OPPORTUNITY`` - ``SPLICE_INSERT``
            :param id: The manifest ID is required and must be unique within the OriginEndpoint. The ID can't be changed after the endpoint is created.
            :param include_iframe_only_stream: Applies to stream sets with a single video track only. When true, the stream set includes an additional I-frame only stream, along with the other tracks. If false, this extra stream is not included.
            :param manifest_name: A short string that's appended to the end of the endpoint URL to create a unique path to this endpoint. The manifestName on the HLSManifest object overrides the manifestName that you provided on the originEndpoint object.
            :param playlist_type: When specified as either ``event`` or ``vod`` , a corresponding ``EXT-X-PLAYLIST-TYPE`` entry is included in the media playlist. Indicates if the playlist is live-to-VOD content.
            :param playlist_window_seconds: Time window (in seconds) contained in each parent manifest.
            :param program_date_time_interval_seconds: Inserts ``EXT-X-PROGRAM-DATE-TIME`` tags in the output manifest at the interval that you specify. Irrespective of this parameter, if any ID3Timed metadata is in the HLS input, it is passed through to the HLS output. Omit this attribute or enter ``0`` to indicate that the ``EXT-X-PROGRAM-DATE-TIME`` tags are not included in the manifest.
            :param url: The URL that's used to request this manifest from this endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlsmanifest.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackage import mixins as mediapackage_mixins
                
                hls_manifest_property = mediapackage_mixins.CfnOriginEndpointPropsMixin.HlsManifestProperty(
                    ad_markers="adMarkers",
                    ads_on_delivery_restrictions="adsOnDeliveryRestrictions",
                    ad_triggers=["adTriggers"],
                    id="id",
                    include_iframe_only_stream=False,
                    manifest_name="manifestName",
                    playlist_type="playlistType",
                    playlist_window_seconds=123,
                    program_date_time_interval_seconds=123,
                    url="url"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__12812e1bde15011cf3510d1138d3ff6454a5c6fb1d0d9d00a63587cec893a024)
                check_type(argname="argument ad_markers", value=ad_markers, expected_type=type_hints["ad_markers"])
                check_type(argname="argument ads_on_delivery_restrictions", value=ads_on_delivery_restrictions, expected_type=type_hints["ads_on_delivery_restrictions"])
                check_type(argname="argument ad_triggers", value=ad_triggers, expected_type=type_hints["ad_triggers"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument include_iframe_only_stream", value=include_iframe_only_stream, expected_type=type_hints["include_iframe_only_stream"])
                check_type(argname="argument manifest_name", value=manifest_name, expected_type=type_hints["manifest_name"])
                check_type(argname="argument playlist_type", value=playlist_type, expected_type=type_hints["playlist_type"])
                check_type(argname="argument playlist_window_seconds", value=playlist_window_seconds, expected_type=type_hints["playlist_window_seconds"])
                check_type(argname="argument program_date_time_interval_seconds", value=program_date_time_interval_seconds, expected_type=type_hints["program_date_time_interval_seconds"])
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ad_markers is not None:
                self._values["ad_markers"] = ad_markers
            if ads_on_delivery_restrictions is not None:
                self._values["ads_on_delivery_restrictions"] = ads_on_delivery_restrictions
            if ad_triggers is not None:
                self._values["ad_triggers"] = ad_triggers
            if id is not None:
                self._values["id"] = id
            if include_iframe_only_stream is not None:
                self._values["include_iframe_only_stream"] = include_iframe_only_stream
            if manifest_name is not None:
                self._values["manifest_name"] = manifest_name
            if playlist_type is not None:
                self._values["playlist_type"] = playlist_type
            if playlist_window_seconds is not None:
                self._values["playlist_window_seconds"] = playlist_window_seconds
            if program_date_time_interval_seconds is not None:
                self._values["program_date_time_interval_seconds"] = program_date_time_interval_seconds
            if url is not None:
                self._values["url"] = url

        @builtins.property
        def ad_markers(self) -> typing.Optional[builtins.str]:
            '''Controls how ad markers are included in the packaged endpoint.

            Valid values:

            - ``NONE`` - Omits all SCTE-35 ad markers from the output.
            - ``PASSTHROUGH`` - Creates a copy in the output of the SCTE-35 ad markers (comments) taken directly from the input manifest.
            - ``SCTE35_ENHANCED`` - Generates ad markers and blackout tags in the output based on the SCTE-35 messages from the input manifest.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlsmanifest.html#cfn-mediapackage-originendpoint-hlsmanifest-admarkers
            '''
            result = self._values.get("ad_markers")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ads_on_delivery_restrictions(self) -> typing.Optional[builtins.str]:
            '''The flags on SCTE-35 segmentation descriptors that have to be present for AWS Elemental MediaPackage to insert ad markers in the output manifest.

            For information about SCTE-35 in AWS Elemental MediaPackage , see `SCTE-35 Message Options in AWS Elemental MediaPackage <https://docs.aws.amazon.com/mediapackage/latest/ug/scte.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlsmanifest.html#cfn-mediapackage-originendpoint-hlsmanifest-adsondeliveryrestrictions
            '''
            result = self._values.get("ads_on_delivery_restrictions")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ad_triggers(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Specifies the SCTE-35 message types that AWS Elemental MediaPackage treats as ad markers in the output manifest.

            Valid values:

            - ``BREAK``
            - ``DISTRIBUTOR_ADVERTISEMENT``
            - ``DISTRIBUTOR_OVERLAY_PLACEMENT_OPPORTUNITY``
            - ``DISTRIBUTOR_PLACEMENT_OPPORTUNITY``
            - ``PROVIDER_ADVERTISEMENT``
            - ``PROVIDER_OVERLAY_PLACEMENT_OPPORTUNITY``
            - ``PROVIDER_PLACEMENT_OPPORTUNITY``
            - ``SPLICE_INSERT``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlsmanifest.html#cfn-mediapackage-originendpoint-hlsmanifest-adtriggers
            '''
            result = self._values.get("ad_triggers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''The manifest ID is required and must be unique within the OriginEndpoint.

            The ID can't be changed after the endpoint is created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlsmanifest.html#cfn-mediapackage-originendpoint-hlsmanifest-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def include_iframe_only_stream(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Applies to stream sets with a single video track only.

            When true, the stream set includes an additional I-frame only stream, along with the other tracks. If false, this extra stream is not included.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlsmanifest.html#cfn-mediapackage-originendpoint-hlsmanifest-includeiframeonlystream
            '''
            result = self._values.get("include_iframe_only_stream")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def manifest_name(self) -> typing.Optional[builtins.str]:
            '''A short string that's appended to the end of the endpoint URL to create a unique path to this endpoint.

            The manifestName on the HLSManifest object overrides the manifestName that you provided on the originEndpoint object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlsmanifest.html#cfn-mediapackage-originendpoint-hlsmanifest-manifestname
            '''
            result = self._values.get("manifest_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def playlist_type(self) -> typing.Optional[builtins.str]:
            '''When specified as either ``event`` or ``vod`` , a corresponding ``EXT-X-PLAYLIST-TYPE`` entry is included in the media playlist.

            Indicates if the playlist is live-to-VOD content.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlsmanifest.html#cfn-mediapackage-originendpoint-hlsmanifest-playlisttype
            '''
            result = self._values.get("playlist_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def playlist_window_seconds(self) -> typing.Optional[jsii.Number]:
            '''Time window (in seconds) contained in each parent manifest.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlsmanifest.html#cfn-mediapackage-originendpoint-hlsmanifest-playlistwindowseconds
            '''
            result = self._values.get("playlist_window_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def program_date_time_interval_seconds(self) -> typing.Optional[jsii.Number]:
            '''Inserts ``EXT-X-PROGRAM-DATE-TIME`` tags in the output manifest at the interval that you specify.

            Irrespective of this parameter, if any ID3Timed metadata is in the HLS input, it is passed through to the HLS output.

            Omit this attribute or enter ``0`` to indicate that the ``EXT-X-PROGRAM-DATE-TIME`` tags are not included in the manifest.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlsmanifest.html#cfn-mediapackage-originendpoint-hlsmanifest-programdatetimeintervalseconds
            '''
            result = self._values.get("program_date_time_interval_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            '''The URL that's used to request this manifest from this endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlsmanifest.html#cfn-mediapackage-originendpoint-hlsmanifest-url
            '''
            result = self._values.get("url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HlsManifestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.mixins.CfnOriginEndpointPropsMixin.HlsPackageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ad_markers": "adMarkers",
            "ads_on_delivery_restrictions": "adsOnDeliveryRestrictions",
            "ad_triggers": "adTriggers",
            "encryption": "encryption",
            "include_dvb_subtitles": "includeDvbSubtitles",
            "include_iframe_only_stream": "includeIframeOnlyStream",
            "playlist_type": "playlistType",
            "playlist_window_seconds": "playlistWindowSeconds",
            "program_date_time_interval_seconds": "programDateTimeIntervalSeconds",
            "segment_duration_seconds": "segmentDurationSeconds",
            "stream_selection": "streamSelection",
            "use_audio_rendition_group": "useAudioRenditionGroup",
        },
    )
    class HlsPackageProperty:
        def __init__(
            self,
            *,
            ad_markers: typing.Optional[builtins.str] = None,
            ads_on_delivery_restrictions: typing.Optional[builtins.str] = None,
            ad_triggers: typing.Optional[typing.Sequence[builtins.str]] = None,
            encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.HlsEncryptionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            include_dvb_subtitles: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            include_iframe_only_stream: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            playlist_type: typing.Optional[builtins.str] = None,
            playlist_window_seconds: typing.Optional[jsii.Number] = None,
            program_date_time_interval_seconds: typing.Optional[jsii.Number] = None,
            segment_duration_seconds: typing.Optional[jsii.Number] = None,
            stream_selection: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.StreamSelectionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            use_audio_rendition_group: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Parameters for Apple HLS packaging.

            :param ad_markers: Controls how ad markers are included in the packaged endpoint. Valid values: - ``NONE`` - Omits all SCTE-35 ad markers from the output. - ``PASSTHROUGH`` - Creates a copy in the output of the SCTE-35 ad markers (comments) taken directly from the input manifest. - ``SCTE35_ENHANCED`` - Generates ad markers and blackout tags in the output based on the SCTE-35 messages from the input manifest.
            :param ads_on_delivery_restrictions: The flags on SCTE-35 segmentation descriptors that have to be present for AWS Elemental MediaPackage to insert ad markers in the output manifest. For information about SCTE-35 in AWS Elemental MediaPackage , see `SCTE-35 Message Options in AWS Elemental MediaPackage <https://docs.aws.amazon.com/mediapackage/latest/ug/scte.html>`_ .
            :param ad_triggers: Specifies the SCTE-35 message types that AWS Elemental MediaPackage treats as ad markers in the output manifest. Valid values: - ``BREAK`` - ``DISTRIBUTOR_ADVERTISEMENT`` - ``DISTRIBUTOR_OVERLAY_PLACEMENT_OPPORTUNITY`` - ``DISTRIBUTOR_PLACEMENT_OPPORTUNITY`` - ``PROVIDER_ADVERTISEMENT`` - ``PROVIDER_OVERLAY_PLACEMENT_OPPORTUNITY`` - ``PROVIDER_PLACEMENT_OPPORTUNITY`` - ``SPLICE_INSERT``
            :param encryption: Parameters for encrypting content.
            :param include_dvb_subtitles: When enabled, MediaPackage passes through digital video broadcasting (DVB) subtitles into the output.
            :param include_iframe_only_stream: Only applies to stream sets with a single video track. When true, the stream set includes an additional I-frame only stream, along with the other tracks. If false, this extra stream is not included.
            :param playlist_type: When specified as either ``event`` or ``vod`` , a corresponding ``EXT-X-PLAYLIST-TYPE`` entry is included in the media playlist. Indicates if the playlist is live-to-VOD content.
            :param playlist_window_seconds: Time window (in seconds) contained in each parent manifest.
            :param program_date_time_interval_seconds: Inserts ``EXT-X-PROGRAM-DATE-TIME`` tags in the output manifest at the interval that you specify. Irrespective of this parameter, if any ID3Timed metadata is in the HLS input, it is passed through to the HLS output. Omit this attribute or enter ``0`` to indicate that the ``EXT-X-PROGRAM-DATE-TIME`` tags are not included in the manifest.
            :param segment_duration_seconds: Duration (in seconds) of each fragment. Actual fragments are rounded to the nearest multiple of the source fragment duration.
            :param stream_selection: Limitations for outputs from the endpoint, based on the video bitrate.
            :param use_audio_rendition_group: When true, AWS Elemental MediaPackage bundles all audio tracks in a rendition group. All other tracks in the stream can be used with any audio rendition from the group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlspackage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackage import mixins as mediapackage_mixins
                
                hls_package_property = mediapackage_mixins.CfnOriginEndpointPropsMixin.HlsPackageProperty(
                    ad_markers="adMarkers",
                    ads_on_delivery_restrictions="adsOnDeliveryRestrictions",
                    ad_triggers=["adTriggers"],
                    encryption=mediapackage_mixins.CfnOriginEndpointPropsMixin.HlsEncryptionProperty(
                        constant_initialization_vector="constantInitializationVector",
                        encryption_method="encryptionMethod",
                        key_rotation_interval_seconds=123,
                        repeat_ext_xKey=False,
                        speke_key_provider=mediapackage_mixins.CfnOriginEndpointPropsMixin.SpekeKeyProviderProperty(
                            certificate_arn="certificateArn",
                            encryption_contract_configuration=mediapackage_mixins.CfnOriginEndpointPropsMixin.EncryptionContractConfigurationProperty(
                                preset_speke20_audio="presetSpeke20Audio",
                                preset_speke20_video="presetSpeke20Video"
                            ),
                            resource_id="resourceId",
                            role_arn="roleArn",
                            system_ids=["systemIds"],
                            url="url"
                        )
                    ),
                    include_dvb_subtitles=False,
                    include_iframe_only_stream=False,
                    playlist_type="playlistType",
                    playlist_window_seconds=123,
                    program_date_time_interval_seconds=123,
                    segment_duration_seconds=123,
                    stream_selection=mediapackage_mixins.CfnOriginEndpointPropsMixin.StreamSelectionProperty(
                        max_video_bits_per_second=123,
                        min_video_bits_per_second=123,
                        stream_order="streamOrder"
                    ),
                    use_audio_rendition_group=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5480fd065b06ca7153648da95392151b192ac1d7277c5b900e53cc90cd0cd681)
                check_type(argname="argument ad_markers", value=ad_markers, expected_type=type_hints["ad_markers"])
                check_type(argname="argument ads_on_delivery_restrictions", value=ads_on_delivery_restrictions, expected_type=type_hints["ads_on_delivery_restrictions"])
                check_type(argname="argument ad_triggers", value=ad_triggers, expected_type=type_hints["ad_triggers"])
                check_type(argname="argument encryption", value=encryption, expected_type=type_hints["encryption"])
                check_type(argname="argument include_dvb_subtitles", value=include_dvb_subtitles, expected_type=type_hints["include_dvb_subtitles"])
                check_type(argname="argument include_iframe_only_stream", value=include_iframe_only_stream, expected_type=type_hints["include_iframe_only_stream"])
                check_type(argname="argument playlist_type", value=playlist_type, expected_type=type_hints["playlist_type"])
                check_type(argname="argument playlist_window_seconds", value=playlist_window_seconds, expected_type=type_hints["playlist_window_seconds"])
                check_type(argname="argument program_date_time_interval_seconds", value=program_date_time_interval_seconds, expected_type=type_hints["program_date_time_interval_seconds"])
                check_type(argname="argument segment_duration_seconds", value=segment_duration_seconds, expected_type=type_hints["segment_duration_seconds"])
                check_type(argname="argument stream_selection", value=stream_selection, expected_type=type_hints["stream_selection"])
                check_type(argname="argument use_audio_rendition_group", value=use_audio_rendition_group, expected_type=type_hints["use_audio_rendition_group"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ad_markers is not None:
                self._values["ad_markers"] = ad_markers
            if ads_on_delivery_restrictions is not None:
                self._values["ads_on_delivery_restrictions"] = ads_on_delivery_restrictions
            if ad_triggers is not None:
                self._values["ad_triggers"] = ad_triggers
            if encryption is not None:
                self._values["encryption"] = encryption
            if include_dvb_subtitles is not None:
                self._values["include_dvb_subtitles"] = include_dvb_subtitles
            if include_iframe_only_stream is not None:
                self._values["include_iframe_only_stream"] = include_iframe_only_stream
            if playlist_type is not None:
                self._values["playlist_type"] = playlist_type
            if playlist_window_seconds is not None:
                self._values["playlist_window_seconds"] = playlist_window_seconds
            if program_date_time_interval_seconds is not None:
                self._values["program_date_time_interval_seconds"] = program_date_time_interval_seconds
            if segment_duration_seconds is not None:
                self._values["segment_duration_seconds"] = segment_duration_seconds
            if stream_selection is not None:
                self._values["stream_selection"] = stream_selection
            if use_audio_rendition_group is not None:
                self._values["use_audio_rendition_group"] = use_audio_rendition_group

        @builtins.property
        def ad_markers(self) -> typing.Optional[builtins.str]:
            '''Controls how ad markers are included in the packaged endpoint.

            Valid values:

            - ``NONE`` - Omits all SCTE-35 ad markers from the output.
            - ``PASSTHROUGH`` - Creates a copy in the output of the SCTE-35 ad markers (comments) taken directly from the input manifest.
            - ``SCTE35_ENHANCED`` - Generates ad markers and blackout tags in the output based on the SCTE-35 messages from the input manifest.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlspackage.html#cfn-mediapackage-originendpoint-hlspackage-admarkers
            '''
            result = self._values.get("ad_markers")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ads_on_delivery_restrictions(self) -> typing.Optional[builtins.str]:
            '''The flags on SCTE-35 segmentation descriptors that have to be present for AWS Elemental MediaPackage to insert ad markers in the output manifest.

            For information about SCTE-35 in AWS Elemental MediaPackage , see `SCTE-35 Message Options in AWS Elemental MediaPackage <https://docs.aws.amazon.com/mediapackage/latest/ug/scte.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlspackage.html#cfn-mediapackage-originendpoint-hlspackage-adsondeliveryrestrictions
            '''
            result = self._values.get("ads_on_delivery_restrictions")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ad_triggers(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Specifies the SCTE-35 message types that AWS Elemental MediaPackage treats as ad markers in the output manifest.

            Valid values:

            - ``BREAK``
            - ``DISTRIBUTOR_ADVERTISEMENT``
            - ``DISTRIBUTOR_OVERLAY_PLACEMENT_OPPORTUNITY``
            - ``DISTRIBUTOR_PLACEMENT_OPPORTUNITY``
            - ``PROVIDER_ADVERTISEMENT``
            - ``PROVIDER_OVERLAY_PLACEMENT_OPPORTUNITY``
            - ``PROVIDER_PLACEMENT_OPPORTUNITY``
            - ``SPLICE_INSERT``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlspackage.html#cfn-mediapackage-originendpoint-hlspackage-adtriggers
            '''
            result = self._values.get("ad_triggers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def encryption(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.HlsEncryptionProperty"]]:
            '''Parameters for encrypting content.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlspackage.html#cfn-mediapackage-originendpoint-hlspackage-encryption
            '''
            result = self._values.get("encryption")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.HlsEncryptionProperty"]], result)

        @builtins.property
        def include_dvb_subtitles(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When enabled, MediaPackage passes through digital video broadcasting (DVB) subtitles into the output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlspackage.html#cfn-mediapackage-originendpoint-hlspackage-includedvbsubtitles
            '''
            result = self._values.get("include_dvb_subtitles")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def include_iframe_only_stream(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Only applies to stream sets with a single video track.

            When true, the stream set includes an additional I-frame only stream, along with the other tracks. If false, this extra stream is not included.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlspackage.html#cfn-mediapackage-originendpoint-hlspackage-includeiframeonlystream
            '''
            result = self._values.get("include_iframe_only_stream")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def playlist_type(self) -> typing.Optional[builtins.str]:
            '''When specified as either ``event`` or ``vod`` , a corresponding ``EXT-X-PLAYLIST-TYPE`` entry is included in the media playlist.

            Indicates if the playlist is live-to-VOD content.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlspackage.html#cfn-mediapackage-originendpoint-hlspackage-playlisttype
            '''
            result = self._values.get("playlist_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def playlist_window_seconds(self) -> typing.Optional[jsii.Number]:
            '''Time window (in seconds) contained in each parent manifest.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlspackage.html#cfn-mediapackage-originendpoint-hlspackage-playlistwindowseconds
            '''
            result = self._values.get("playlist_window_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def program_date_time_interval_seconds(self) -> typing.Optional[jsii.Number]:
            '''Inserts ``EXT-X-PROGRAM-DATE-TIME`` tags in the output manifest at the interval that you specify.

            Irrespective of this parameter, if any ID3Timed metadata is in the HLS input, it is passed through to the HLS output.

            Omit this attribute or enter ``0`` to indicate that the ``EXT-X-PROGRAM-DATE-TIME`` tags are not included in the manifest.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlspackage.html#cfn-mediapackage-originendpoint-hlspackage-programdatetimeintervalseconds
            '''
            result = self._values.get("program_date_time_interval_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def segment_duration_seconds(self) -> typing.Optional[jsii.Number]:
            '''Duration (in seconds) of each fragment.

            Actual fragments are rounded to the nearest multiple of the source fragment duration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlspackage.html#cfn-mediapackage-originendpoint-hlspackage-segmentdurationseconds
            '''
            result = self._values.get("segment_duration_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def stream_selection(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.StreamSelectionProperty"]]:
            '''Limitations for outputs from the endpoint, based on the video bitrate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlspackage.html#cfn-mediapackage-originendpoint-hlspackage-streamselection
            '''
            result = self._values.get("stream_selection")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.StreamSelectionProperty"]], result)

        @builtins.property
        def use_audio_rendition_group(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When true, AWS Elemental MediaPackage bundles all audio tracks in a rendition group.

            All other tracks in the stream can be used with any audio rendition from the group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlspackage.html#cfn-mediapackage-originendpoint-hlspackage-useaudiorenditiongroup
            '''
            result = self._values.get("use_audio_rendition_group")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HlsPackageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.mixins.CfnOriginEndpointPropsMixin.MssEncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={"speke_key_provider": "spekeKeyProvider"},
    )
    class MssEncryptionProperty:
        def __init__(
            self,
            *,
            speke_key_provider: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.SpekeKeyProviderProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Holds encryption information so that access to the content can be controlled by a DRM solution.

            :param speke_key_provider: Parameters for the SPEKE key provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-mssencryption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackage import mixins as mediapackage_mixins
                
                mss_encryption_property = mediapackage_mixins.CfnOriginEndpointPropsMixin.MssEncryptionProperty(
                    speke_key_provider=mediapackage_mixins.CfnOriginEndpointPropsMixin.SpekeKeyProviderProperty(
                        certificate_arn="certificateArn",
                        encryption_contract_configuration=mediapackage_mixins.CfnOriginEndpointPropsMixin.EncryptionContractConfigurationProperty(
                            preset_speke20_audio="presetSpeke20Audio",
                            preset_speke20_video="presetSpeke20Video"
                        ),
                        resource_id="resourceId",
                        role_arn="roleArn",
                        system_ids=["systemIds"],
                        url="url"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__aef4645bed246e5e8bcedf6899c51634315a62dcd507fff8671b304647250a52)
                check_type(argname="argument speke_key_provider", value=speke_key_provider, expected_type=type_hints["speke_key_provider"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if speke_key_provider is not None:
                self._values["speke_key_provider"] = speke_key_provider

        @builtins.property
        def speke_key_provider(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.SpekeKeyProviderProperty"]]:
            '''Parameters for the SPEKE key provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-mssencryption.html#cfn-mediapackage-originendpoint-mssencryption-spekekeyprovider
            '''
            result = self._values.get("speke_key_provider")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.SpekeKeyProviderProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MssEncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.mixins.CfnOriginEndpointPropsMixin.MssPackageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "encryption": "encryption",
            "manifest_window_seconds": "manifestWindowSeconds",
            "segment_duration_seconds": "segmentDurationSeconds",
            "stream_selection": "streamSelection",
        },
    )
    class MssPackageProperty:
        def __init__(
            self,
            *,
            encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.MssEncryptionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            manifest_window_seconds: typing.Optional[jsii.Number] = None,
            segment_duration_seconds: typing.Optional[jsii.Number] = None,
            stream_selection: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.StreamSelectionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Parameters for Microsoft Smooth Streaming packaging.

            :param encryption: Parameters for encrypting content.
            :param manifest_window_seconds: Time window (in seconds) contained in each manifest.
            :param segment_duration_seconds: Duration (in seconds) of each fragment. Actual fragments are rounded to the nearest multiple of the source fragment duration.
            :param stream_selection: Limitations for outputs from the endpoint, based on the video bitrate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-msspackage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackage import mixins as mediapackage_mixins
                
                mss_package_property = mediapackage_mixins.CfnOriginEndpointPropsMixin.MssPackageProperty(
                    encryption=mediapackage_mixins.CfnOriginEndpointPropsMixin.MssEncryptionProperty(
                        speke_key_provider=mediapackage_mixins.CfnOriginEndpointPropsMixin.SpekeKeyProviderProperty(
                            certificate_arn="certificateArn",
                            encryption_contract_configuration=mediapackage_mixins.CfnOriginEndpointPropsMixin.EncryptionContractConfigurationProperty(
                                preset_speke20_audio="presetSpeke20Audio",
                                preset_speke20_video="presetSpeke20Video"
                            ),
                            resource_id="resourceId",
                            role_arn="roleArn",
                            system_ids=["systemIds"],
                            url="url"
                        )
                    ),
                    manifest_window_seconds=123,
                    segment_duration_seconds=123,
                    stream_selection=mediapackage_mixins.CfnOriginEndpointPropsMixin.StreamSelectionProperty(
                        max_video_bits_per_second=123,
                        min_video_bits_per_second=123,
                        stream_order="streamOrder"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8a42e05c0e9e2703fee06f8929df9cee11c822c4bd402797e8830aba68b259be)
                check_type(argname="argument encryption", value=encryption, expected_type=type_hints["encryption"])
                check_type(argname="argument manifest_window_seconds", value=manifest_window_seconds, expected_type=type_hints["manifest_window_seconds"])
                check_type(argname="argument segment_duration_seconds", value=segment_duration_seconds, expected_type=type_hints["segment_duration_seconds"])
                check_type(argname="argument stream_selection", value=stream_selection, expected_type=type_hints["stream_selection"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encryption is not None:
                self._values["encryption"] = encryption
            if manifest_window_seconds is not None:
                self._values["manifest_window_seconds"] = manifest_window_seconds
            if segment_duration_seconds is not None:
                self._values["segment_duration_seconds"] = segment_duration_seconds
            if stream_selection is not None:
                self._values["stream_selection"] = stream_selection

        @builtins.property
        def encryption(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.MssEncryptionProperty"]]:
            '''Parameters for encrypting content.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-msspackage.html#cfn-mediapackage-originendpoint-msspackage-encryption
            '''
            result = self._values.get("encryption")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.MssEncryptionProperty"]], result)

        @builtins.property
        def manifest_window_seconds(self) -> typing.Optional[jsii.Number]:
            '''Time window (in seconds) contained in each manifest.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-msspackage.html#cfn-mediapackage-originendpoint-msspackage-manifestwindowseconds
            '''
            result = self._values.get("manifest_window_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def segment_duration_seconds(self) -> typing.Optional[jsii.Number]:
            '''Duration (in seconds) of each fragment.

            Actual fragments are rounded to the nearest multiple of the source fragment duration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-msspackage.html#cfn-mediapackage-originendpoint-msspackage-segmentdurationseconds
            '''
            result = self._values.get("segment_duration_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def stream_selection(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.StreamSelectionProperty"]]:
            '''Limitations for outputs from the endpoint, based on the video bitrate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-msspackage.html#cfn-mediapackage-originendpoint-msspackage-streamselection
            '''
            result = self._values.get("stream_selection")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.StreamSelectionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MssPackageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.mixins.CfnOriginEndpointPropsMixin.SpekeKeyProviderProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate_arn": "certificateArn",
            "encryption_contract_configuration": "encryptionContractConfiguration",
            "resource_id": "resourceId",
            "role_arn": "roleArn",
            "system_ids": "systemIds",
            "url": "url",
        },
    )
    class SpekeKeyProviderProperty:
        def __init__(
            self,
            *,
            certificate_arn: typing.Optional[builtins.str] = None,
            encryption_contract_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.EncryptionContractConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            resource_id: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
            system_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Key provider settings for DRM.

            :param certificate_arn: The Amazon Resource Name (ARN) for the certificate that you imported to Certificate Manager to add content key encryption to this endpoint. For this feature to work, your DRM key provider must support content key encryption.
            :param encryption_contract_configuration: Use ``encryptionContractConfiguration`` to configure one or more content encryption keys for your endpoints that use SPEKE Version 2.0. The encryption contract defines which content keys are used to encrypt the audio and video tracks in your stream. To configure the encryption contract, specify which audio and video encryption presets to use.
            :param resource_id: Unique identifier for this endpoint, as it is configured in the key provider service.
            :param role_arn: The ARN for the IAM role that's granted by the key provider to provide access to the key provider API. This role must have a trust policy that allows AWS Elemental MediaPackage to assume the role, and it must have a sufficient permissions policy to allow access to the specific key retrieval URL. Valid format: arn:aws:iam::{accountID}:role/{name}
            :param system_ids: List of unique identifiers for the DRM systems to use, as defined in the CPIX specification.
            :param url: URL for the key provider’s key retrieval API endpoint. Must start with https://.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-spekekeyprovider.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackage import mixins as mediapackage_mixins
                
                speke_key_provider_property = mediapackage_mixins.CfnOriginEndpointPropsMixin.SpekeKeyProviderProperty(
                    certificate_arn="certificateArn",
                    encryption_contract_configuration=mediapackage_mixins.CfnOriginEndpointPropsMixin.EncryptionContractConfigurationProperty(
                        preset_speke20_audio="presetSpeke20Audio",
                        preset_speke20_video="presetSpeke20Video"
                    ),
                    resource_id="resourceId",
                    role_arn="roleArn",
                    system_ids=["systemIds"],
                    url="url"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__93a222a198872450c1324041ba8378b346756ecc8d134da21ff803d550e22361)
                check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
                check_type(argname="argument encryption_contract_configuration", value=encryption_contract_configuration, expected_type=type_hints["encryption_contract_configuration"])
                check_type(argname="argument resource_id", value=resource_id, expected_type=type_hints["resource_id"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument system_ids", value=system_ids, expected_type=type_hints["system_ids"])
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate_arn is not None:
                self._values["certificate_arn"] = certificate_arn
            if encryption_contract_configuration is not None:
                self._values["encryption_contract_configuration"] = encryption_contract_configuration
            if resource_id is not None:
                self._values["resource_id"] = resource_id
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if system_ids is not None:
                self._values["system_ids"] = system_ids
            if url is not None:
                self._values["url"] = url

        @builtins.property
        def certificate_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) for the certificate that you imported to Certificate Manager to add content key encryption to this endpoint.

            For this feature to work, your DRM key provider must support content key encryption.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-spekekeyprovider.html#cfn-mediapackage-originendpoint-spekekeyprovider-certificatearn
            '''
            result = self._values.get("certificate_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def encryption_contract_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.EncryptionContractConfigurationProperty"]]:
            '''Use ``encryptionContractConfiguration`` to configure one or more content encryption keys for your endpoints that use SPEKE Version 2.0. The encryption contract defines which content keys are used to encrypt the audio and video tracks in your stream. To configure the encryption contract, specify which audio and video encryption presets to use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-spekekeyprovider.html#cfn-mediapackage-originendpoint-spekekeyprovider-encryptioncontractconfiguration
            '''
            result = self._values.get("encryption_contract_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.EncryptionContractConfigurationProperty"]], result)

        @builtins.property
        def resource_id(self) -> typing.Optional[builtins.str]:
            '''Unique identifier for this endpoint, as it is configured in the key provider service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-spekekeyprovider.html#cfn-mediapackage-originendpoint-spekekeyprovider-resourceid
            '''
            result = self._values.get("resource_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN for the IAM role that's granted by the key provider to provide access to the key provider API.

            This role must have a trust policy that allows AWS Elemental MediaPackage to assume the role, and it must have a sufficient permissions policy to allow access to the specific key retrieval URL. Valid format: arn:aws:iam::{accountID}:role/{name}

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-spekekeyprovider.html#cfn-mediapackage-originendpoint-spekekeyprovider-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def system_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''List of unique identifiers for the DRM systems to use, as defined in the CPIX specification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-spekekeyprovider.html#cfn-mediapackage-originendpoint-spekekeyprovider-systemids
            '''
            result = self._values.get("system_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            '''URL for the key provider’s key retrieval API endpoint.

            Must start with https://.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-spekekeyprovider.html#cfn-mediapackage-originendpoint-spekekeyprovider-url
            '''
            result = self._values.get("url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SpekeKeyProviderProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.mixins.CfnOriginEndpointPropsMixin.StreamSelectionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "max_video_bits_per_second": "maxVideoBitsPerSecond",
            "min_video_bits_per_second": "minVideoBitsPerSecond",
            "stream_order": "streamOrder",
        },
    )
    class StreamSelectionProperty:
        def __init__(
            self,
            *,
            max_video_bits_per_second: typing.Optional[jsii.Number] = None,
            min_video_bits_per_second: typing.Optional[jsii.Number] = None,
            stream_order: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Limitations for outputs from the endpoint, based on the video bitrate.

            :param max_video_bits_per_second: The upper limit of the bitrates that this endpoint serves. If the video track exceeds this threshold, then AWS Elemental MediaPackage excludes it from output. If you don't specify a value, it defaults to 2147483647 bits per second.
            :param min_video_bits_per_second: The lower limit of the bitrates that this endpoint serves. If the video track is below this threshold, then AWS Elemental MediaPackage excludes it from output. If you don't specify a value, it defaults to 0 bits per second.
            :param stream_order: Order in which the different video bitrates are presented to the player. Valid values: ``ORIGINAL`` , ``VIDEO_BITRATE_ASCENDING`` , ``VIDEO_BITRATE_DESCENDING`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-streamselection.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackage import mixins as mediapackage_mixins
                
                stream_selection_property = mediapackage_mixins.CfnOriginEndpointPropsMixin.StreamSelectionProperty(
                    max_video_bits_per_second=123,
                    min_video_bits_per_second=123,
                    stream_order="streamOrder"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6aafb1ed86e376940d2e55063c951654059bc362442e00d674ffd32916741a74)
                check_type(argname="argument max_video_bits_per_second", value=max_video_bits_per_second, expected_type=type_hints["max_video_bits_per_second"])
                check_type(argname="argument min_video_bits_per_second", value=min_video_bits_per_second, expected_type=type_hints["min_video_bits_per_second"])
                check_type(argname="argument stream_order", value=stream_order, expected_type=type_hints["stream_order"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_video_bits_per_second is not None:
                self._values["max_video_bits_per_second"] = max_video_bits_per_second
            if min_video_bits_per_second is not None:
                self._values["min_video_bits_per_second"] = min_video_bits_per_second
            if stream_order is not None:
                self._values["stream_order"] = stream_order

        @builtins.property
        def max_video_bits_per_second(self) -> typing.Optional[jsii.Number]:
            '''The upper limit of the bitrates that this endpoint serves.

            If the video track exceeds this threshold, then AWS Elemental MediaPackage excludes it from output. If you don't specify a value, it defaults to 2147483647 bits per second.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-streamselection.html#cfn-mediapackage-originendpoint-streamselection-maxvideobitspersecond
            '''
            result = self._values.get("max_video_bits_per_second")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min_video_bits_per_second(self) -> typing.Optional[jsii.Number]:
            '''The lower limit of the bitrates that this endpoint serves.

            If the video track is below this threshold, then AWS Elemental MediaPackage excludes it from output. If you don't specify a value, it defaults to 0 bits per second.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-streamselection.html#cfn-mediapackage-originendpoint-streamselection-minvideobitspersecond
            '''
            result = self._values.get("min_video_bits_per_second")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def stream_order(self) -> typing.Optional[builtins.str]:
            '''Order in which the different video bitrates are presented to the player.

            Valid values: ``ORIGINAL`` , ``VIDEO_BITRATE_ASCENDING`` , ``VIDEO_BITRATE_DESCENDING`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-streamselection.html#cfn-mediapackage-originendpoint-streamselection-streamorder
            '''
            result = self._values.get("stream_order")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StreamSelectionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.mixins.CfnPackagingConfigurationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "cmaf_package": "cmafPackage",
        "dash_package": "dashPackage",
        "hls_package": "hlsPackage",
        "id": "id",
        "mss_package": "mssPackage",
        "packaging_group_id": "packagingGroupId",
        "tags": "tags",
    },
)
class CfnPackagingConfigurationMixinProps:
    def __init__(
        self,
        *,
        cmaf_package: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPackagingConfigurationPropsMixin.CmafPackageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        dash_package: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPackagingConfigurationPropsMixin.DashPackageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        hls_package: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPackagingConfigurationPropsMixin.HlsPackageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        id: typing.Optional[builtins.str] = None,
        mss_package: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPackagingConfigurationPropsMixin.MssPackageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        packaging_group_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnPackagingConfigurationPropsMixin.

        :param cmaf_package: Parameters for CMAF packaging.
        :param dash_package: Parameters for DASH-ISO packaging.
        :param hls_package: Parameters for Apple HLS packaging.
        :param id: Unique identifier that you assign to the packaging configuration.
        :param mss_package: Parameters for Microsoft Smooth Streaming packaging.
        :param packaging_group_id: The ID of the packaging group associated with this packaging configuration.
        :param tags: The tags to assign to the packaging configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-packagingconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_mediapackage import mixins as mediapackage_mixins
            
            cfn_packaging_configuration_mixin_props = mediapackage_mixins.CfnPackagingConfigurationMixinProps(
                cmaf_package=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.CmafPackageProperty(
                    encryption=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.CmafEncryptionProperty(
                        speke_key_provider=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.SpekeKeyProviderProperty(
                            encryption_contract_configuration=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.EncryptionContractConfigurationProperty(
                                preset_speke20_audio="presetSpeke20Audio",
                                preset_speke20_video="presetSpeke20Video"
                            ),
                            role_arn="roleArn",
                            system_ids=["systemIds"],
                            url="url"
                        )
                    ),
                    hls_manifests=[mediapackage_mixins.CfnPackagingConfigurationPropsMixin.HlsManifestProperty(
                        ad_markers="adMarkers",
                        include_iframe_only_stream=False,
                        manifest_name="manifestName",
                        program_date_time_interval_seconds=123,
                        repeat_ext_xKey=False,
                        stream_selection=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.StreamSelectionProperty(
                            max_video_bits_per_second=123,
                            min_video_bits_per_second=123,
                            stream_order="streamOrder"
                        )
                    )],
                    include_encoder_configuration_in_segments=False,
                    segment_duration_seconds=123
                ),
                dash_package=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.DashPackageProperty(
                    dash_manifests=[mediapackage_mixins.CfnPackagingConfigurationPropsMixin.DashManifestProperty(
                        manifest_layout="manifestLayout",
                        manifest_name="manifestName",
                        min_buffer_time_seconds=123,
                        profile="profile",
                        scte_markers_source="scteMarkersSource",
                        stream_selection=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.StreamSelectionProperty(
                            max_video_bits_per_second=123,
                            min_video_bits_per_second=123,
                            stream_order="streamOrder"
                        )
                    )],
                    encryption=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.DashEncryptionProperty(
                        speke_key_provider=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.SpekeKeyProviderProperty(
                            encryption_contract_configuration=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.EncryptionContractConfigurationProperty(
                                preset_speke20_audio="presetSpeke20Audio",
                                preset_speke20_video="presetSpeke20Video"
                            ),
                            role_arn="roleArn",
                            system_ids=["systemIds"],
                            url="url"
                        )
                    ),
                    include_encoder_configuration_in_segments=False,
                    include_iframe_only_stream=False,
                    period_triggers=["periodTriggers"],
                    segment_duration_seconds=123,
                    segment_template_format="segmentTemplateFormat"
                ),
                hls_package=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.HlsPackageProperty(
                    encryption=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.HlsEncryptionProperty(
                        constant_initialization_vector="constantInitializationVector",
                        encryption_method="encryptionMethod",
                        speke_key_provider=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.SpekeKeyProviderProperty(
                            encryption_contract_configuration=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.EncryptionContractConfigurationProperty(
                                preset_speke20_audio="presetSpeke20Audio",
                                preset_speke20_video="presetSpeke20Video"
                            ),
                            role_arn="roleArn",
                            system_ids=["systemIds"],
                            url="url"
                        )
                    ),
                    hls_manifests=[mediapackage_mixins.CfnPackagingConfigurationPropsMixin.HlsManifestProperty(
                        ad_markers="adMarkers",
                        include_iframe_only_stream=False,
                        manifest_name="manifestName",
                        program_date_time_interval_seconds=123,
                        repeat_ext_xKey=False,
                        stream_selection=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.StreamSelectionProperty(
                            max_video_bits_per_second=123,
                            min_video_bits_per_second=123,
                            stream_order="streamOrder"
                        )
                    )],
                    include_dvb_subtitles=False,
                    segment_duration_seconds=123,
                    use_audio_rendition_group=False
                ),
                id="id",
                mss_package=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.MssPackageProperty(
                    encryption=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.MssEncryptionProperty(
                        speke_key_provider=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.SpekeKeyProviderProperty(
                            encryption_contract_configuration=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.EncryptionContractConfigurationProperty(
                                preset_speke20_audio="presetSpeke20Audio",
                                preset_speke20_video="presetSpeke20Video"
                            ),
                            role_arn="roleArn",
                            system_ids=["systemIds"],
                            url="url"
                        )
                    ),
                    mss_manifests=[mediapackage_mixins.CfnPackagingConfigurationPropsMixin.MssManifestProperty(
                        manifest_name="manifestName",
                        stream_selection=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.StreamSelectionProperty(
                            max_video_bits_per_second=123,
                            min_video_bits_per_second=123,
                            stream_order="streamOrder"
                        )
                    )],
                    segment_duration_seconds=123
                ),
                packaging_group_id="packagingGroupId",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7088d4f64726c066c6585da16d81634be33085526d661beed9cbcabcd933805e)
            check_type(argname="argument cmaf_package", value=cmaf_package, expected_type=type_hints["cmaf_package"])
            check_type(argname="argument dash_package", value=dash_package, expected_type=type_hints["dash_package"])
            check_type(argname="argument hls_package", value=hls_package, expected_type=type_hints["hls_package"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument mss_package", value=mss_package, expected_type=type_hints["mss_package"])
            check_type(argname="argument packaging_group_id", value=packaging_group_id, expected_type=type_hints["packaging_group_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cmaf_package is not None:
            self._values["cmaf_package"] = cmaf_package
        if dash_package is not None:
            self._values["dash_package"] = dash_package
        if hls_package is not None:
            self._values["hls_package"] = hls_package
        if id is not None:
            self._values["id"] = id
        if mss_package is not None:
            self._values["mss_package"] = mss_package
        if packaging_group_id is not None:
            self._values["packaging_group_id"] = packaging_group_id
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def cmaf_package(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackagingConfigurationPropsMixin.CmafPackageProperty"]]:
        '''Parameters for CMAF packaging.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-packagingconfiguration.html#cfn-mediapackage-packagingconfiguration-cmafpackage
        '''
        result = self._values.get("cmaf_package")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackagingConfigurationPropsMixin.CmafPackageProperty"]], result)

    @builtins.property
    def dash_package(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackagingConfigurationPropsMixin.DashPackageProperty"]]:
        '''Parameters for DASH-ISO packaging.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-packagingconfiguration.html#cfn-mediapackage-packagingconfiguration-dashpackage
        '''
        result = self._values.get("dash_package")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackagingConfigurationPropsMixin.DashPackageProperty"]], result)

    @builtins.property
    def hls_package(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackagingConfigurationPropsMixin.HlsPackageProperty"]]:
        '''Parameters for Apple HLS packaging.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-packagingconfiguration.html#cfn-mediapackage-packagingconfiguration-hlspackage
        '''
        result = self._values.get("hls_package")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackagingConfigurationPropsMixin.HlsPackageProperty"]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Unique identifier that you assign to the packaging configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-packagingconfiguration.html#cfn-mediapackage-packagingconfiguration-id
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mss_package(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackagingConfigurationPropsMixin.MssPackageProperty"]]:
        '''Parameters for Microsoft Smooth Streaming packaging.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-packagingconfiguration.html#cfn-mediapackage-packagingconfiguration-msspackage
        '''
        result = self._values.get("mss_package")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackagingConfigurationPropsMixin.MssPackageProperty"]], result)

    @builtins.property
    def packaging_group_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the packaging group associated with this packaging configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-packagingconfiguration.html#cfn-mediapackage-packagingconfiguration-packaginggroupid
        '''
        result = self._values.get("packaging_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags to assign to the packaging configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-packagingconfiguration.html#cfn-mediapackage-packagingconfiguration-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPackagingConfigurationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPackagingConfigurationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.mixins.CfnPackagingConfigurationPropsMixin",
):
    '''Creates a packaging configuration in a packaging group.

    The packaging configuration represents a single delivery point for an asset. It determines the format and setting for the egressing content. Specify only one package format per configuration, such as ``HlsPackage`` .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-packagingconfiguration.html
    :cloudformationResource: AWS::MediaPackage::PackagingConfiguration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_mediapackage import mixins as mediapackage_mixins
        
        cfn_packaging_configuration_props_mixin = mediapackage_mixins.CfnPackagingConfigurationPropsMixin(mediapackage_mixins.CfnPackagingConfigurationMixinProps(
            cmaf_package=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.CmafPackageProperty(
                encryption=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.CmafEncryptionProperty(
                    speke_key_provider=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.SpekeKeyProviderProperty(
                        encryption_contract_configuration=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.EncryptionContractConfigurationProperty(
                            preset_speke20_audio="presetSpeke20Audio",
                            preset_speke20_video="presetSpeke20Video"
                        ),
                        role_arn="roleArn",
                        system_ids=["systemIds"],
                        url="url"
                    )
                ),
                hls_manifests=[mediapackage_mixins.CfnPackagingConfigurationPropsMixin.HlsManifestProperty(
                    ad_markers="adMarkers",
                    include_iframe_only_stream=False,
                    manifest_name="manifestName",
                    program_date_time_interval_seconds=123,
                    repeat_ext_xKey=False,
                    stream_selection=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.StreamSelectionProperty(
                        max_video_bits_per_second=123,
                        min_video_bits_per_second=123,
                        stream_order="streamOrder"
                    )
                )],
                include_encoder_configuration_in_segments=False,
                segment_duration_seconds=123
            ),
            dash_package=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.DashPackageProperty(
                dash_manifests=[mediapackage_mixins.CfnPackagingConfigurationPropsMixin.DashManifestProperty(
                    manifest_layout="manifestLayout",
                    manifest_name="manifestName",
                    min_buffer_time_seconds=123,
                    profile="profile",
                    scte_markers_source="scteMarkersSource",
                    stream_selection=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.StreamSelectionProperty(
                        max_video_bits_per_second=123,
                        min_video_bits_per_second=123,
                        stream_order="streamOrder"
                    )
                )],
                encryption=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.DashEncryptionProperty(
                    speke_key_provider=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.SpekeKeyProviderProperty(
                        encryption_contract_configuration=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.EncryptionContractConfigurationProperty(
                            preset_speke20_audio="presetSpeke20Audio",
                            preset_speke20_video="presetSpeke20Video"
                        ),
                        role_arn="roleArn",
                        system_ids=["systemIds"],
                        url="url"
                    )
                ),
                include_encoder_configuration_in_segments=False,
                include_iframe_only_stream=False,
                period_triggers=["periodTriggers"],
                segment_duration_seconds=123,
                segment_template_format="segmentTemplateFormat"
            ),
            hls_package=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.HlsPackageProperty(
                encryption=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.HlsEncryptionProperty(
                    constant_initialization_vector="constantInitializationVector",
                    encryption_method="encryptionMethod",
                    speke_key_provider=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.SpekeKeyProviderProperty(
                        encryption_contract_configuration=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.EncryptionContractConfigurationProperty(
                            preset_speke20_audio="presetSpeke20Audio",
                            preset_speke20_video="presetSpeke20Video"
                        ),
                        role_arn="roleArn",
                        system_ids=["systemIds"],
                        url="url"
                    )
                ),
                hls_manifests=[mediapackage_mixins.CfnPackagingConfigurationPropsMixin.HlsManifestProperty(
                    ad_markers="adMarkers",
                    include_iframe_only_stream=False,
                    manifest_name="manifestName",
                    program_date_time_interval_seconds=123,
                    repeat_ext_xKey=False,
                    stream_selection=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.StreamSelectionProperty(
                        max_video_bits_per_second=123,
                        min_video_bits_per_second=123,
                        stream_order="streamOrder"
                    )
                )],
                include_dvb_subtitles=False,
                segment_duration_seconds=123,
                use_audio_rendition_group=False
            ),
            id="id",
            mss_package=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.MssPackageProperty(
                encryption=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.MssEncryptionProperty(
                    speke_key_provider=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.SpekeKeyProviderProperty(
                        encryption_contract_configuration=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.EncryptionContractConfigurationProperty(
                            preset_speke20_audio="presetSpeke20Audio",
                            preset_speke20_video="presetSpeke20Video"
                        ),
                        role_arn="roleArn",
                        system_ids=["systemIds"],
                        url="url"
                    )
                ),
                mss_manifests=[mediapackage_mixins.CfnPackagingConfigurationPropsMixin.MssManifestProperty(
                    manifest_name="manifestName",
                    stream_selection=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.StreamSelectionProperty(
                        max_video_bits_per_second=123,
                        min_video_bits_per_second=123,
                        stream_order="streamOrder"
                    )
                )],
                segment_duration_seconds=123
            ),
            packaging_group_id="packagingGroupId",
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
        props: typing.Union[CfnPackagingConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::MediaPackage::PackagingConfiguration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bdb086c754c7b2b93255a12787e828455999dacbbeec8d7fcc41bf0435240ea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__af2606a0cd65fb9eda013af9d6f15eb93dbbfde8368bf1105de67de3cb44cc2e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8bcae51d0a877205a3714fb6aaf55e3f882b0db8c2c28000c0f69871191d107)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPackagingConfigurationMixinProps:
        return typing.cast(CfnPackagingConfigurationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.mixins.CfnPackagingConfigurationPropsMixin.CmafEncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={"speke_key_provider": "spekeKeyProvider"},
    )
    class CmafEncryptionProperty:
        def __init__(
            self,
            *,
            speke_key_provider: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPackagingConfigurationPropsMixin.SpekeKeyProviderProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Holds encryption information so that access to the content can be controlled by a DRM solution.

            :param speke_key_provider: Parameters for the SPEKE key provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-cmafencryption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackage import mixins as mediapackage_mixins
                
                cmaf_encryption_property = mediapackage_mixins.CfnPackagingConfigurationPropsMixin.CmafEncryptionProperty(
                    speke_key_provider=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.SpekeKeyProviderProperty(
                        encryption_contract_configuration=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.EncryptionContractConfigurationProperty(
                            preset_speke20_audio="presetSpeke20Audio",
                            preset_speke20_video="presetSpeke20Video"
                        ),
                        role_arn="roleArn",
                        system_ids=["systemIds"],
                        url="url"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5892a9204d3a84825d62a469c891b27f89cc3ca5402ef8c07a14bf8b294eaecc)
                check_type(argname="argument speke_key_provider", value=speke_key_provider, expected_type=type_hints["speke_key_provider"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if speke_key_provider is not None:
                self._values["speke_key_provider"] = speke_key_provider

        @builtins.property
        def speke_key_provider(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackagingConfigurationPropsMixin.SpekeKeyProviderProperty"]]:
            '''Parameters for the SPEKE key provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-cmafencryption.html#cfn-mediapackage-packagingconfiguration-cmafencryption-spekekeyprovider
            '''
            result = self._values.get("speke_key_provider")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackagingConfigurationPropsMixin.SpekeKeyProviderProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CmafEncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.mixins.CfnPackagingConfigurationPropsMixin.CmafPackageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "encryption": "encryption",
            "hls_manifests": "hlsManifests",
            "include_encoder_configuration_in_segments": "includeEncoderConfigurationInSegments",
            "segment_duration_seconds": "segmentDurationSeconds",
        },
    )
    class CmafPackageProperty:
        def __init__(
            self,
            *,
            encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPackagingConfigurationPropsMixin.CmafEncryptionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            hls_manifests: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPackagingConfigurationPropsMixin.HlsManifestProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            include_encoder_configuration_in_segments: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            segment_duration_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Parameters for a packaging configuration that uses Common Media Application Format (CMAF) packaging.

            :param encryption: Parameters for encrypting content.
            :param hls_manifests: A list of HLS manifest configurations that are available from this endpoint.
            :param include_encoder_configuration_in_segments: When includeEncoderConfigurationInSegments is set to true, AWS Elemental MediaPackage places your encoder's Sequence Parameter Set (SPS), Picture Parameter Set (PPS), and Video Parameter Set (VPS) metadata in every video segment instead of in the init fragment. This lets you use different SPS/PPS/VPS settings for your assets during content playback.
            :param segment_duration_seconds: Duration (in seconds) of each segment. Actual segments are rounded to the nearest multiple of the source fragment duration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-cmafpackage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackage import mixins as mediapackage_mixins
                
                cmaf_package_property = mediapackage_mixins.CfnPackagingConfigurationPropsMixin.CmafPackageProperty(
                    encryption=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.CmafEncryptionProperty(
                        speke_key_provider=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.SpekeKeyProviderProperty(
                            encryption_contract_configuration=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.EncryptionContractConfigurationProperty(
                                preset_speke20_audio="presetSpeke20Audio",
                                preset_speke20_video="presetSpeke20Video"
                            ),
                            role_arn="roleArn",
                            system_ids=["systemIds"],
                            url="url"
                        )
                    ),
                    hls_manifests=[mediapackage_mixins.CfnPackagingConfigurationPropsMixin.HlsManifestProperty(
                        ad_markers="adMarkers",
                        include_iframe_only_stream=False,
                        manifest_name="manifestName",
                        program_date_time_interval_seconds=123,
                        repeat_ext_xKey=False,
                        stream_selection=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.StreamSelectionProperty(
                            max_video_bits_per_second=123,
                            min_video_bits_per_second=123,
                            stream_order="streamOrder"
                        )
                    )],
                    include_encoder_configuration_in_segments=False,
                    segment_duration_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__24e97281281520157d186f6e4c2e1cddcd3a42f0f253d5248a2551339582624b)
                check_type(argname="argument encryption", value=encryption, expected_type=type_hints["encryption"])
                check_type(argname="argument hls_manifests", value=hls_manifests, expected_type=type_hints["hls_manifests"])
                check_type(argname="argument include_encoder_configuration_in_segments", value=include_encoder_configuration_in_segments, expected_type=type_hints["include_encoder_configuration_in_segments"])
                check_type(argname="argument segment_duration_seconds", value=segment_duration_seconds, expected_type=type_hints["segment_duration_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encryption is not None:
                self._values["encryption"] = encryption
            if hls_manifests is not None:
                self._values["hls_manifests"] = hls_manifests
            if include_encoder_configuration_in_segments is not None:
                self._values["include_encoder_configuration_in_segments"] = include_encoder_configuration_in_segments
            if segment_duration_seconds is not None:
                self._values["segment_duration_seconds"] = segment_duration_seconds

        @builtins.property
        def encryption(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackagingConfigurationPropsMixin.CmafEncryptionProperty"]]:
            '''Parameters for encrypting content.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-cmafpackage.html#cfn-mediapackage-packagingconfiguration-cmafpackage-encryption
            '''
            result = self._values.get("encryption")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackagingConfigurationPropsMixin.CmafEncryptionProperty"]], result)

        @builtins.property
        def hls_manifests(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackagingConfigurationPropsMixin.HlsManifestProperty"]]]]:
            '''A list of HLS manifest configurations that are available from this endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-cmafpackage.html#cfn-mediapackage-packagingconfiguration-cmafpackage-hlsmanifests
            '''
            result = self._values.get("hls_manifests")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackagingConfigurationPropsMixin.HlsManifestProperty"]]]], result)

        @builtins.property
        def include_encoder_configuration_in_segments(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When includeEncoderConfigurationInSegments is set to true, AWS Elemental MediaPackage places your encoder's Sequence Parameter Set (SPS), Picture Parameter Set (PPS), and Video Parameter Set (VPS) metadata in every video segment instead of in the init fragment.

            This lets you use different SPS/PPS/VPS settings for your assets during content playback.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-cmafpackage.html#cfn-mediapackage-packagingconfiguration-cmafpackage-includeencoderconfigurationinsegments
            '''
            result = self._values.get("include_encoder_configuration_in_segments")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def segment_duration_seconds(self) -> typing.Optional[jsii.Number]:
            '''Duration (in seconds) of each segment.

            Actual segments are rounded to the nearest multiple of the source fragment duration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-cmafpackage.html#cfn-mediapackage-packagingconfiguration-cmafpackage-segmentdurationseconds
            '''
            result = self._values.get("segment_duration_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CmafPackageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.mixins.CfnPackagingConfigurationPropsMixin.DashEncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={"speke_key_provider": "spekeKeyProvider"},
    )
    class DashEncryptionProperty:
        def __init__(
            self,
            *,
            speke_key_provider: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPackagingConfigurationPropsMixin.SpekeKeyProviderProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Holds encryption information so that access to the content can be controlled by a DRM solution.

            :param speke_key_provider: Parameters for the SPEKE key provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-dashencryption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackage import mixins as mediapackage_mixins
                
                dash_encryption_property = mediapackage_mixins.CfnPackagingConfigurationPropsMixin.DashEncryptionProperty(
                    speke_key_provider=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.SpekeKeyProviderProperty(
                        encryption_contract_configuration=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.EncryptionContractConfigurationProperty(
                            preset_speke20_audio="presetSpeke20Audio",
                            preset_speke20_video="presetSpeke20Video"
                        ),
                        role_arn="roleArn",
                        system_ids=["systemIds"],
                        url="url"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4abd35d6daa8a319b174d185026e9ac00e5e9974bbe6b72b9a35f378bd074a91)
                check_type(argname="argument speke_key_provider", value=speke_key_provider, expected_type=type_hints["speke_key_provider"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if speke_key_provider is not None:
                self._values["speke_key_provider"] = speke_key_provider

        @builtins.property
        def speke_key_provider(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackagingConfigurationPropsMixin.SpekeKeyProviderProperty"]]:
            '''Parameters for the SPEKE key provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-dashencryption.html#cfn-mediapackage-packagingconfiguration-dashencryption-spekekeyprovider
            '''
            result = self._values.get("speke_key_provider")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackagingConfigurationPropsMixin.SpekeKeyProviderProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DashEncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.mixins.CfnPackagingConfigurationPropsMixin.DashManifestProperty",
        jsii_struct_bases=[],
        name_mapping={
            "manifest_layout": "manifestLayout",
            "manifest_name": "manifestName",
            "min_buffer_time_seconds": "minBufferTimeSeconds",
            "profile": "profile",
            "scte_markers_source": "scteMarkersSource",
            "stream_selection": "streamSelection",
        },
    )
    class DashManifestProperty:
        def __init__(
            self,
            *,
            manifest_layout: typing.Optional[builtins.str] = None,
            manifest_name: typing.Optional[builtins.str] = None,
            min_buffer_time_seconds: typing.Optional[jsii.Number] = None,
            profile: typing.Optional[builtins.str] = None,
            scte_markers_source: typing.Optional[builtins.str] = None,
            stream_selection: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPackagingConfigurationPropsMixin.StreamSelectionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Parameters for a DASH manifest.

            :param manifest_layout: Determines the position of some tags in the Media Presentation Description (MPD). When set to ``FULL`` , elements like ``SegmentTemplate`` and ``ContentProtection`` are included in each ``Representation`` . When set to ``COMPACT`` , duplicate elements are combined and presented at the AdaptationSet level.
            :param manifest_name: A short string that's appended to the end of the endpoint URL to create a unique path to this packaging configuration.
            :param min_buffer_time_seconds: Minimum amount of content (measured in seconds) that a player must keep available in the buffer.
            :param profile: The DASH profile type. When set to ``HBBTV_1_5`` , the content is compliant with HbbTV 1.5.
            :param scte_markers_source: The source of scte markers used. Value description: - ``SEGMENTS`` - The scte markers are sourced from the segments of the ingested content. - ``MANIFEST`` - the scte markers are sourced from the manifest of the ingested content. The MANIFEST value is compatible with source HLS playlists using the SCTE-35 Enhanced syntax ( ``EXT-OATCLS-SCTE35`` tags). SCTE-35 Elemental and SCTE-35 Daterange syntaxes are not supported with this option.
            :param stream_selection: Limitations for outputs from the endpoint, based on the video bitrate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-dashmanifest.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackage import mixins as mediapackage_mixins
                
                dash_manifest_property = mediapackage_mixins.CfnPackagingConfigurationPropsMixin.DashManifestProperty(
                    manifest_layout="manifestLayout",
                    manifest_name="manifestName",
                    min_buffer_time_seconds=123,
                    profile="profile",
                    scte_markers_source="scteMarkersSource",
                    stream_selection=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.StreamSelectionProperty(
                        max_video_bits_per_second=123,
                        min_video_bits_per_second=123,
                        stream_order="streamOrder"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__194677f0f3a6af0c3f9a4cbb8a1e5937c9d93c1aa47e446775d66fd46ba770b3)
                check_type(argname="argument manifest_layout", value=manifest_layout, expected_type=type_hints["manifest_layout"])
                check_type(argname="argument manifest_name", value=manifest_name, expected_type=type_hints["manifest_name"])
                check_type(argname="argument min_buffer_time_seconds", value=min_buffer_time_seconds, expected_type=type_hints["min_buffer_time_seconds"])
                check_type(argname="argument profile", value=profile, expected_type=type_hints["profile"])
                check_type(argname="argument scte_markers_source", value=scte_markers_source, expected_type=type_hints["scte_markers_source"])
                check_type(argname="argument stream_selection", value=stream_selection, expected_type=type_hints["stream_selection"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if manifest_layout is not None:
                self._values["manifest_layout"] = manifest_layout
            if manifest_name is not None:
                self._values["manifest_name"] = manifest_name
            if min_buffer_time_seconds is not None:
                self._values["min_buffer_time_seconds"] = min_buffer_time_seconds
            if profile is not None:
                self._values["profile"] = profile
            if scte_markers_source is not None:
                self._values["scte_markers_source"] = scte_markers_source
            if stream_selection is not None:
                self._values["stream_selection"] = stream_selection

        @builtins.property
        def manifest_layout(self) -> typing.Optional[builtins.str]:
            '''Determines the position of some tags in the Media Presentation Description (MPD).

            When set to ``FULL`` , elements like ``SegmentTemplate`` and ``ContentProtection`` are included in each ``Representation`` . When set to ``COMPACT`` , duplicate elements are combined and presented at the AdaptationSet level.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-dashmanifest.html#cfn-mediapackage-packagingconfiguration-dashmanifest-manifestlayout
            '''
            result = self._values.get("manifest_layout")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def manifest_name(self) -> typing.Optional[builtins.str]:
            '''A short string that's appended to the end of the endpoint URL to create a unique path to this packaging configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-dashmanifest.html#cfn-mediapackage-packagingconfiguration-dashmanifest-manifestname
            '''
            result = self._values.get("manifest_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def min_buffer_time_seconds(self) -> typing.Optional[jsii.Number]:
            '''Minimum amount of content (measured in seconds) that a player must keep available in the buffer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-dashmanifest.html#cfn-mediapackage-packagingconfiguration-dashmanifest-minbuffertimeseconds
            '''
            result = self._values.get("min_buffer_time_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def profile(self) -> typing.Optional[builtins.str]:
            '''The DASH profile type.

            When set to ``HBBTV_1_5`` , the content is compliant with HbbTV 1.5.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-dashmanifest.html#cfn-mediapackage-packagingconfiguration-dashmanifest-profile
            '''
            result = self._values.get("profile")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def scte_markers_source(self) -> typing.Optional[builtins.str]:
            '''The source of scte markers used.

            Value description:

            - ``SEGMENTS`` - The scte markers are sourced from the segments of the ingested content.
            - ``MANIFEST`` - the scte markers are sourced from the manifest of the ingested content. The MANIFEST value is compatible with source HLS playlists using the SCTE-35 Enhanced syntax ( ``EXT-OATCLS-SCTE35`` tags). SCTE-35 Elemental and SCTE-35 Daterange syntaxes are not supported with this option.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-dashmanifest.html#cfn-mediapackage-packagingconfiguration-dashmanifest-sctemarkerssource
            '''
            result = self._values.get("scte_markers_source")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def stream_selection(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackagingConfigurationPropsMixin.StreamSelectionProperty"]]:
            '''Limitations for outputs from the endpoint, based on the video bitrate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-dashmanifest.html#cfn-mediapackage-packagingconfiguration-dashmanifest-streamselection
            '''
            result = self._values.get("stream_selection")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackagingConfigurationPropsMixin.StreamSelectionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DashManifestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.mixins.CfnPackagingConfigurationPropsMixin.DashPackageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dash_manifests": "dashManifests",
            "encryption": "encryption",
            "include_encoder_configuration_in_segments": "includeEncoderConfigurationInSegments",
            "include_iframe_only_stream": "includeIframeOnlyStream",
            "period_triggers": "periodTriggers",
            "segment_duration_seconds": "segmentDurationSeconds",
            "segment_template_format": "segmentTemplateFormat",
        },
    )
    class DashPackageProperty:
        def __init__(
            self,
            *,
            dash_manifests: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPackagingConfigurationPropsMixin.DashManifestProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPackagingConfigurationPropsMixin.DashEncryptionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            include_encoder_configuration_in_segments: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            include_iframe_only_stream: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            period_triggers: typing.Optional[typing.Sequence[builtins.str]] = None,
            segment_duration_seconds: typing.Optional[jsii.Number] = None,
            segment_template_format: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Parameters for a packaging configuration that uses Dynamic Adaptive Streaming over HTTP (DASH) packaging.

            :param dash_manifests: A list of DASH manifest configurations that are available from this endpoint.
            :param encryption: Parameters for encrypting content.
            :param include_encoder_configuration_in_segments: When includeEncoderConfigurationInSegments is set to true, AWS Elemental MediaPackage places your encoder's Sequence Parameter Set (SPS), Picture Parameter Set (PPS), and Video Parameter Set (VPS) metadata in every video segment instead of in the init fragment. This lets you use different SPS/PPS/VPS settings for your assets during content playback.
            :param include_iframe_only_stream: This applies only to stream sets with a single video track. When true, the stream set includes an additional I-frame trick-play only stream, along with the other tracks. If false, this extra stream is not included.
            :param period_triggers: Controls whether AWS Elemental MediaPackage produces single-period or multi-period DASH manifests. For more information about periods, see `Multi-period DASH in AWS Elemental MediaPackage <https://docs.aws.amazon.com/mediapackage/latest/ug/multi-period.html>`_ . Valid values: - ``ADS`` - AWS Elemental MediaPackage will produce multi-period DASH manifests. Periods are created based on the SCTE-35 ad markers present in the input manifest. - *No value* - AWS Elemental MediaPackage will produce single-period DASH manifests. This is the default setting.
            :param segment_duration_seconds: Duration (in seconds) of each fragment. Actual fragments are rounded to the nearest multiple of the source segment duration.
            :param segment_template_format: Determines the type of SegmentTemplate included in the Media Presentation Description (MPD). When set to ``NUMBER_WITH_TIMELINE`` , a full timeline is presented in each SegmentTemplate, with $Number$ media URLs. When set to ``TIME_WITH_TIMELINE`` , a full timeline is presented in each SegmentTemplate, with $Time$ media URLs. When set to ``NUMBER_WITH_DURATION`` , only a duration is included in each SegmentTemplate, with $Number$ media URLs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-dashpackage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackage import mixins as mediapackage_mixins
                
                dash_package_property = mediapackage_mixins.CfnPackagingConfigurationPropsMixin.DashPackageProperty(
                    dash_manifests=[mediapackage_mixins.CfnPackagingConfigurationPropsMixin.DashManifestProperty(
                        manifest_layout="manifestLayout",
                        manifest_name="manifestName",
                        min_buffer_time_seconds=123,
                        profile="profile",
                        scte_markers_source="scteMarkersSource",
                        stream_selection=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.StreamSelectionProperty(
                            max_video_bits_per_second=123,
                            min_video_bits_per_second=123,
                            stream_order="streamOrder"
                        )
                    )],
                    encryption=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.DashEncryptionProperty(
                        speke_key_provider=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.SpekeKeyProviderProperty(
                            encryption_contract_configuration=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.EncryptionContractConfigurationProperty(
                                preset_speke20_audio="presetSpeke20Audio",
                                preset_speke20_video="presetSpeke20Video"
                            ),
                            role_arn="roleArn",
                            system_ids=["systemIds"],
                            url="url"
                        )
                    ),
                    include_encoder_configuration_in_segments=False,
                    include_iframe_only_stream=False,
                    period_triggers=["periodTriggers"],
                    segment_duration_seconds=123,
                    segment_template_format="segmentTemplateFormat"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__add89095b13db65cd87b4a48473e935951d0dbcc8014f0096a3f4af39fdedbe6)
                check_type(argname="argument dash_manifests", value=dash_manifests, expected_type=type_hints["dash_manifests"])
                check_type(argname="argument encryption", value=encryption, expected_type=type_hints["encryption"])
                check_type(argname="argument include_encoder_configuration_in_segments", value=include_encoder_configuration_in_segments, expected_type=type_hints["include_encoder_configuration_in_segments"])
                check_type(argname="argument include_iframe_only_stream", value=include_iframe_only_stream, expected_type=type_hints["include_iframe_only_stream"])
                check_type(argname="argument period_triggers", value=period_triggers, expected_type=type_hints["period_triggers"])
                check_type(argname="argument segment_duration_seconds", value=segment_duration_seconds, expected_type=type_hints["segment_duration_seconds"])
                check_type(argname="argument segment_template_format", value=segment_template_format, expected_type=type_hints["segment_template_format"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dash_manifests is not None:
                self._values["dash_manifests"] = dash_manifests
            if encryption is not None:
                self._values["encryption"] = encryption
            if include_encoder_configuration_in_segments is not None:
                self._values["include_encoder_configuration_in_segments"] = include_encoder_configuration_in_segments
            if include_iframe_only_stream is not None:
                self._values["include_iframe_only_stream"] = include_iframe_only_stream
            if period_triggers is not None:
                self._values["period_triggers"] = period_triggers
            if segment_duration_seconds is not None:
                self._values["segment_duration_seconds"] = segment_duration_seconds
            if segment_template_format is not None:
                self._values["segment_template_format"] = segment_template_format

        @builtins.property
        def dash_manifests(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackagingConfigurationPropsMixin.DashManifestProperty"]]]]:
            '''A list of DASH manifest configurations that are available from this endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-dashpackage.html#cfn-mediapackage-packagingconfiguration-dashpackage-dashmanifests
            '''
            result = self._values.get("dash_manifests")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackagingConfigurationPropsMixin.DashManifestProperty"]]]], result)

        @builtins.property
        def encryption(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackagingConfigurationPropsMixin.DashEncryptionProperty"]]:
            '''Parameters for encrypting content.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-dashpackage.html#cfn-mediapackage-packagingconfiguration-dashpackage-encryption
            '''
            result = self._values.get("encryption")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackagingConfigurationPropsMixin.DashEncryptionProperty"]], result)

        @builtins.property
        def include_encoder_configuration_in_segments(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When includeEncoderConfigurationInSegments is set to true, AWS Elemental MediaPackage places your encoder's Sequence Parameter Set (SPS), Picture Parameter Set (PPS), and Video Parameter Set (VPS) metadata in every video segment instead of in the init fragment.

            This lets you use different SPS/PPS/VPS settings for your assets during content playback.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-dashpackage.html#cfn-mediapackage-packagingconfiguration-dashpackage-includeencoderconfigurationinsegments
            '''
            result = self._values.get("include_encoder_configuration_in_segments")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def include_iframe_only_stream(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''This applies only to stream sets with a single video track.

            When true, the stream set includes an additional I-frame trick-play only stream, along with the other tracks. If false, this extra stream is not included.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-dashpackage.html#cfn-mediapackage-packagingconfiguration-dashpackage-includeiframeonlystream
            '''
            result = self._values.get("include_iframe_only_stream")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def period_triggers(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Controls whether AWS Elemental MediaPackage produces single-period or multi-period DASH manifests.

            For more information about periods, see `Multi-period DASH in AWS Elemental MediaPackage <https://docs.aws.amazon.com/mediapackage/latest/ug/multi-period.html>`_ .

            Valid values:

            - ``ADS`` - AWS Elemental MediaPackage will produce multi-period DASH manifests. Periods are created based on the SCTE-35 ad markers present in the input manifest.
            - *No value* - AWS Elemental MediaPackage will produce single-period DASH manifests. This is the default setting.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-dashpackage.html#cfn-mediapackage-packagingconfiguration-dashpackage-periodtriggers
            '''
            result = self._values.get("period_triggers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def segment_duration_seconds(self) -> typing.Optional[jsii.Number]:
            '''Duration (in seconds) of each fragment.

            Actual fragments are rounded to the nearest multiple of the source segment duration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-dashpackage.html#cfn-mediapackage-packagingconfiguration-dashpackage-segmentdurationseconds
            '''
            result = self._values.get("segment_duration_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def segment_template_format(self) -> typing.Optional[builtins.str]:
            '''Determines the type of SegmentTemplate included in the Media Presentation Description (MPD).

            When set to ``NUMBER_WITH_TIMELINE`` , a full timeline is presented in each SegmentTemplate, with $Number$ media URLs. When set to ``TIME_WITH_TIMELINE`` , a full timeline is presented in each SegmentTemplate, with $Time$ media URLs. When set to ``NUMBER_WITH_DURATION`` , only a duration is included in each SegmentTemplate, with $Number$ media URLs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-dashpackage.html#cfn-mediapackage-packagingconfiguration-dashpackage-segmenttemplateformat
            '''
            result = self._values.get("segment_template_format")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DashPackageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.mixins.CfnPackagingConfigurationPropsMixin.EncryptionContractConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "preset_speke20_audio": "presetSpeke20Audio",
            "preset_speke20_video": "presetSpeke20Video",
        },
    )
    class EncryptionContractConfigurationProperty:
        def __init__(
            self,
            *,
            preset_speke20_audio: typing.Optional[builtins.str] = None,
            preset_speke20_video: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Use ``encryptionContractConfiguration`` to configure one or more content encryption keys for your endpoints that use SPEKE Version 2.0. The encryption contract defines the content keys used to encrypt the audio and video tracks in your stream. To configure the encryption contract, specify which audio and video encryption presets to use. For more information about these presets, see `SPEKE Version 2.0 Presets <https://docs.aws.amazon.com/mediapackage/latest/ug/drm-content-speke-v2-presets.html>`_ .

            Note the following considerations when using ``encryptionContractConfiguration`` :

            - You can use ``encryptionContractConfiguration`` for DASH endpoints that use SPEKE Version 2.0. SPEKE Version 2.0 relies on the CPIX Version 2.3 specification.
            - You cannot combine an ``UNENCRYPTED`` preset with ``UNENCRYPTED`` or ``SHARED`` presets across ``presetSpeke20Audio`` and ``presetSpeke20Video`` .
            - When you use a ``SHARED`` preset, you must use it for both ``presetSpeke20Audio`` and ``presetSpeke20Video`` .

            :param preset_speke20_audio: A collection of audio encryption presets. Value description: - ``PRESET-AUDIO-1`` - Use one content key to encrypt all of the audio tracks in your stream. - ``PRESET-AUDIO-2`` - Use one content key to encrypt all of the stereo audio tracks and one content key to encrypt all of the multichannel audio tracks. - ``PRESET-AUDIO-3`` - Use one content key to encrypt all of the stereo audio tracks, one content key to encrypt all of the multichannel audio tracks with 3 to 6 channels, and one content key to encrypt all of the multichannel audio tracks with more than 6 channels. - ``SHARED`` - Use the same content key for all of the audio and video tracks in your stream. - ``UNENCRYPTED`` - Don't encrypt any of the audio tracks in your stream.
            :param preset_speke20_video: A collection of video encryption presets. Value description: - ``PRESET-VIDEO-1`` - Use one content key to encrypt all of the video tracks in your stream. - ``PRESET-VIDEO-2`` - Use one content key to encrypt all of the SD video tracks and one content key for all HD and higher resolutions video tracks. - ``PRESET-VIDEO-3`` - Use one content key to encrypt all of the SD video tracks, one content key for HD video tracks and one content key for all UHD video tracks. - ``PRESET-VIDEO-4`` - Use one content key to encrypt all of the SD video tracks, one content key for HD video tracks, one content key for all UHD1 video tracks and one content key for all UHD2 video tracks. - ``PRESET-VIDEO-5`` - Use one content key to encrypt all of the SD video tracks, one content key for HD1 video tracks, one content key for HD2 video tracks, one content key for all UHD1 video tracks and one content key for all UHD2 video tracks. - ``PRESET-VIDEO-6`` - Use one content key to encrypt all of the SD video tracks, one content key for HD1 video tracks, one content key for HD2 video tracks and one content key for all UHD video tracks. - ``PRESET-VIDEO-7`` - Use one content key to encrypt all of the SD+HD1 video tracks, one content key for HD2 video tracks and one content key for all UHD video tracks. - ``PRESET-VIDEO-8`` - Use one content key to encrypt all of the SD+HD1 video tracks, one content key for HD2 video tracks, one content key for all UHD1 video tracks and one content key for all UHD2 video tracks. - ``SHARED`` - Use the same content key for all of the video and audio tracks in your stream. - ``UNENCRYPTED`` - Don't encrypt any of the video tracks in your stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-encryptioncontractconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackage import mixins as mediapackage_mixins
                
                encryption_contract_configuration_property = mediapackage_mixins.CfnPackagingConfigurationPropsMixin.EncryptionContractConfigurationProperty(
                    preset_speke20_audio="presetSpeke20Audio",
                    preset_speke20_video="presetSpeke20Video"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4cf6f0b748a4843992ee087a943f2f9117f3b89720c0bacf115b9d8216adb465)
                check_type(argname="argument preset_speke20_audio", value=preset_speke20_audio, expected_type=type_hints["preset_speke20_audio"])
                check_type(argname="argument preset_speke20_video", value=preset_speke20_video, expected_type=type_hints["preset_speke20_video"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if preset_speke20_audio is not None:
                self._values["preset_speke20_audio"] = preset_speke20_audio
            if preset_speke20_video is not None:
                self._values["preset_speke20_video"] = preset_speke20_video

        @builtins.property
        def preset_speke20_audio(self) -> typing.Optional[builtins.str]:
            '''A collection of audio encryption presets.

            Value description:

            - ``PRESET-AUDIO-1`` - Use one content key to encrypt all of the audio tracks in your stream.
            - ``PRESET-AUDIO-2`` - Use one content key to encrypt all of the stereo audio tracks and one content key to encrypt all of the multichannel audio tracks.
            - ``PRESET-AUDIO-3`` - Use one content key to encrypt all of the stereo audio tracks, one content key to encrypt all of the multichannel audio tracks with 3 to 6 channels, and one content key to encrypt all of the multichannel audio tracks with more than 6 channels.
            - ``SHARED`` - Use the same content key for all of the audio and video tracks in your stream.
            - ``UNENCRYPTED`` - Don't encrypt any of the audio tracks in your stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-encryptioncontractconfiguration.html#cfn-mediapackage-packagingconfiguration-encryptioncontractconfiguration-presetspeke20audio
            '''
            result = self._values.get("preset_speke20_audio")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def preset_speke20_video(self) -> typing.Optional[builtins.str]:
            '''A collection of video encryption presets.

            Value description:

            - ``PRESET-VIDEO-1`` - Use one content key to encrypt all of the video tracks in your stream.
            - ``PRESET-VIDEO-2`` - Use one content key to encrypt all of the SD video tracks and one content key for all HD and higher resolutions video tracks.
            - ``PRESET-VIDEO-3`` - Use one content key to encrypt all of the SD video tracks, one content key for HD video tracks and one content key for all UHD video tracks.
            - ``PRESET-VIDEO-4`` - Use one content key to encrypt all of the SD video tracks, one content key for HD video tracks, one content key for all UHD1 video tracks and one content key for all UHD2 video tracks.
            - ``PRESET-VIDEO-5`` - Use one content key to encrypt all of the SD video tracks, one content key for HD1 video tracks, one content key for HD2 video tracks, one content key for all UHD1 video tracks and one content key for all UHD2 video tracks.
            - ``PRESET-VIDEO-6`` - Use one content key to encrypt all of the SD video tracks, one content key for HD1 video tracks, one content key for HD2 video tracks and one content key for all UHD video tracks.
            - ``PRESET-VIDEO-7`` - Use one content key to encrypt all of the SD+HD1 video tracks, one content key for HD2 video tracks and one content key for all UHD video tracks.
            - ``PRESET-VIDEO-8`` - Use one content key to encrypt all of the SD+HD1 video tracks, one content key for HD2 video tracks, one content key for all UHD1 video tracks and one content key for all UHD2 video tracks.
            - ``SHARED`` - Use the same content key for all of the video and audio tracks in your stream.
            - ``UNENCRYPTED`` - Don't encrypt any of the video tracks in your stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-encryptioncontractconfiguration.html#cfn-mediapackage-packagingconfiguration-encryptioncontractconfiguration-presetspeke20video
            '''
            result = self._values.get("preset_speke20_video")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionContractConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.mixins.CfnPackagingConfigurationPropsMixin.HlsEncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "constant_initialization_vector": "constantInitializationVector",
            "encryption_method": "encryptionMethod",
            "speke_key_provider": "spekeKeyProvider",
        },
    )
    class HlsEncryptionProperty:
        def __init__(
            self,
            *,
            constant_initialization_vector: typing.Optional[builtins.str] = None,
            encryption_method: typing.Optional[builtins.str] = None,
            speke_key_provider: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPackagingConfigurationPropsMixin.SpekeKeyProviderProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Holds encryption information so that access to the content can be controlled by a DRM solution.

            :param constant_initialization_vector: A 128-bit, 16-byte hex value represented by a 32-character string, used with the key for encrypting blocks. If you don't specify a constant initialization vector (IV), AWS Elemental MediaPackage periodically rotates the IV.
            :param encryption_method: HLS encryption type.
            :param speke_key_provider: Parameters for the SPEKE key provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-hlsencryption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackage import mixins as mediapackage_mixins
                
                hls_encryption_property = mediapackage_mixins.CfnPackagingConfigurationPropsMixin.HlsEncryptionProperty(
                    constant_initialization_vector="constantInitializationVector",
                    encryption_method="encryptionMethod",
                    speke_key_provider=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.SpekeKeyProviderProperty(
                        encryption_contract_configuration=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.EncryptionContractConfigurationProperty(
                            preset_speke20_audio="presetSpeke20Audio",
                            preset_speke20_video="presetSpeke20Video"
                        ),
                        role_arn="roleArn",
                        system_ids=["systemIds"],
                        url="url"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cde63a457777d587a2b07830d2b06642dc0c6299f59e6506c6655d3050d956bd)
                check_type(argname="argument constant_initialization_vector", value=constant_initialization_vector, expected_type=type_hints["constant_initialization_vector"])
                check_type(argname="argument encryption_method", value=encryption_method, expected_type=type_hints["encryption_method"])
                check_type(argname="argument speke_key_provider", value=speke_key_provider, expected_type=type_hints["speke_key_provider"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if constant_initialization_vector is not None:
                self._values["constant_initialization_vector"] = constant_initialization_vector
            if encryption_method is not None:
                self._values["encryption_method"] = encryption_method
            if speke_key_provider is not None:
                self._values["speke_key_provider"] = speke_key_provider

        @builtins.property
        def constant_initialization_vector(self) -> typing.Optional[builtins.str]:
            '''A 128-bit, 16-byte hex value represented by a 32-character string, used with the key for encrypting blocks.

            If you don't specify a constant initialization vector (IV), AWS Elemental MediaPackage periodically rotates the IV.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-hlsencryption.html#cfn-mediapackage-packagingconfiguration-hlsencryption-constantinitializationvector
            '''
            result = self._values.get("constant_initialization_vector")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def encryption_method(self) -> typing.Optional[builtins.str]:
            '''HLS encryption type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-hlsencryption.html#cfn-mediapackage-packagingconfiguration-hlsencryption-encryptionmethod
            '''
            result = self._values.get("encryption_method")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def speke_key_provider(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackagingConfigurationPropsMixin.SpekeKeyProviderProperty"]]:
            '''Parameters for the SPEKE key provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-hlsencryption.html#cfn-mediapackage-packagingconfiguration-hlsencryption-spekekeyprovider
            '''
            result = self._values.get("speke_key_provider")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackagingConfigurationPropsMixin.SpekeKeyProviderProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HlsEncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.mixins.CfnPackagingConfigurationPropsMixin.HlsManifestProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ad_markers": "adMarkers",
            "include_iframe_only_stream": "includeIframeOnlyStream",
            "manifest_name": "manifestName",
            "program_date_time_interval_seconds": "programDateTimeIntervalSeconds",
            "repeat_ext_x_key": "repeatExtXKey",
            "stream_selection": "streamSelection",
        },
    )
    class HlsManifestProperty:
        def __init__(
            self,
            *,
            ad_markers: typing.Optional[builtins.str] = None,
            include_iframe_only_stream: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            manifest_name: typing.Optional[builtins.str] = None,
            program_date_time_interval_seconds: typing.Optional[jsii.Number] = None,
            repeat_ext_x_key: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            stream_selection: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPackagingConfigurationPropsMixin.StreamSelectionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Parameters for an HLS manifest.

            :param ad_markers: This setting controls ad markers in the packaged content. Valid values: - ``NONE`` - Omits all SCTE-35 ad markers from the output. - ``PASSTHROUGH`` - Creates a copy in the output of the SCTE-35 ad markers (comments) taken directly from the input manifest. - ``SCTE35_ENHANCED`` - Generates ad markers and blackout tags in the output based on the SCTE-35 messages from the input manifest.
            :param include_iframe_only_stream: Applies to stream sets with a single video track only. When enabled, the output includes an additional I-frame only stream, along with the other tracks.
            :param manifest_name: A short string that's appended to the end of the endpoint URL to create a unique path to this packaging configuration.
            :param program_date_time_interval_seconds: Inserts ``EXT-X-PROGRAM-DATE-TIME`` tags in the output manifest at the interval that you specify. Irrespective of this parameter, if any ID3Timed metadata is in the HLS input, it is passed through to the HLS output. Omit this attribute or enter ``0`` to indicate that the ``EXT-X-PROGRAM-DATE-TIME`` tags are not included in the manifest.
            :param repeat_ext_x_key: Repeat the ``EXT-X-KEY`` directive for every media segment. This might result in an increase in client requests to the DRM server.
            :param stream_selection: Video bitrate limitations for outputs from this packaging configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-hlsmanifest.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackage import mixins as mediapackage_mixins
                
                hls_manifest_property = mediapackage_mixins.CfnPackagingConfigurationPropsMixin.HlsManifestProperty(
                    ad_markers="adMarkers",
                    include_iframe_only_stream=False,
                    manifest_name="manifestName",
                    program_date_time_interval_seconds=123,
                    repeat_ext_xKey=False,
                    stream_selection=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.StreamSelectionProperty(
                        max_video_bits_per_second=123,
                        min_video_bits_per_second=123,
                        stream_order="streamOrder"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6de31ebdf780e8d6dfe79ee0353727ac74c5eadfa49fbf355d0f8f42ba4107eb)
                check_type(argname="argument ad_markers", value=ad_markers, expected_type=type_hints["ad_markers"])
                check_type(argname="argument include_iframe_only_stream", value=include_iframe_only_stream, expected_type=type_hints["include_iframe_only_stream"])
                check_type(argname="argument manifest_name", value=manifest_name, expected_type=type_hints["manifest_name"])
                check_type(argname="argument program_date_time_interval_seconds", value=program_date_time_interval_seconds, expected_type=type_hints["program_date_time_interval_seconds"])
                check_type(argname="argument repeat_ext_x_key", value=repeat_ext_x_key, expected_type=type_hints["repeat_ext_x_key"])
                check_type(argname="argument stream_selection", value=stream_selection, expected_type=type_hints["stream_selection"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ad_markers is not None:
                self._values["ad_markers"] = ad_markers
            if include_iframe_only_stream is not None:
                self._values["include_iframe_only_stream"] = include_iframe_only_stream
            if manifest_name is not None:
                self._values["manifest_name"] = manifest_name
            if program_date_time_interval_seconds is not None:
                self._values["program_date_time_interval_seconds"] = program_date_time_interval_seconds
            if repeat_ext_x_key is not None:
                self._values["repeat_ext_x_key"] = repeat_ext_x_key
            if stream_selection is not None:
                self._values["stream_selection"] = stream_selection

        @builtins.property
        def ad_markers(self) -> typing.Optional[builtins.str]:
            '''This setting controls ad markers in the packaged content.

            Valid values:

            - ``NONE`` - Omits all SCTE-35 ad markers from the output.
            - ``PASSTHROUGH`` - Creates a copy in the output of the SCTE-35 ad markers (comments) taken directly from the input manifest.
            - ``SCTE35_ENHANCED`` - Generates ad markers and blackout tags in the output based on the SCTE-35 messages from the input manifest.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-hlsmanifest.html#cfn-mediapackage-packagingconfiguration-hlsmanifest-admarkers
            '''
            result = self._values.get("ad_markers")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def include_iframe_only_stream(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Applies to stream sets with a single video track only.

            When enabled, the output includes an additional I-frame only stream, along with the other tracks.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-hlsmanifest.html#cfn-mediapackage-packagingconfiguration-hlsmanifest-includeiframeonlystream
            '''
            result = self._values.get("include_iframe_only_stream")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def manifest_name(self) -> typing.Optional[builtins.str]:
            '''A short string that's appended to the end of the endpoint URL to create a unique path to this packaging configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-hlsmanifest.html#cfn-mediapackage-packagingconfiguration-hlsmanifest-manifestname
            '''
            result = self._values.get("manifest_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def program_date_time_interval_seconds(self) -> typing.Optional[jsii.Number]:
            '''Inserts ``EXT-X-PROGRAM-DATE-TIME`` tags in the output manifest at the interval that you specify.

            Irrespective of this parameter, if any ID3Timed metadata is in the HLS input, it is passed through to the HLS output.

            Omit this attribute or enter ``0`` to indicate that the ``EXT-X-PROGRAM-DATE-TIME`` tags are not included in the manifest.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-hlsmanifest.html#cfn-mediapackage-packagingconfiguration-hlsmanifest-programdatetimeintervalseconds
            '''
            result = self._values.get("program_date_time_interval_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def repeat_ext_x_key(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Repeat the ``EXT-X-KEY`` directive for every media segment.

            This might result in an increase in client requests to the DRM server.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-hlsmanifest.html#cfn-mediapackage-packagingconfiguration-hlsmanifest-repeatextxkey
            '''
            result = self._values.get("repeat_ext_x_key")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def stream_selection(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackagingConfigurationPropsMixin.StreamSelectionProperty"]]:
            '''Video bitrate limitations for outputs from this packaging configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-hlsmanifest.html#cfn-mediapackage-packagingconfiguration-hlsmanifest-streamselection
            '''
            result = self._values.get("stream_selection")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackagingConfigurationPropsMixin.StreamSelectionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HlsManifestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.mixins.CfnPackagingConfigurationPropsMixin.HlsPackageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "encryption": "encryption",
            "hls_manifests": "hlsManifests",
            "include_dvb_subtitles": "includeDvbSubtitles",
            "segment_duration_seconds": "segmentDurationSeconds",
            "use_audio_rendition_group": "useAudioRenditionGroup",
        },
    )
    class HlsPackageProperty:
        def __init__(
            self,
            *,
            encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPackagingConfigurationPropsMixin.HlsEncryptionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            hls_manifests: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPackagingConfigurationPropsMixin.HlsManifestProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            include_dvb_subtitles: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            segment_duration_seconds: typing.Optional[jsii.Number] = None,
            use_audio_rendition_group: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Parameters for a packaging configuration that uses HTTP Live Streaming (HLS) packaging.

            :param encryption: Parameters for encrypting content.
            :param hls_manifests: A list of HLS manifest configurations that are available from this endpoint.
            :param include_dvb_subtitles: When enabled, MediaPackage passes through digital video broadcasting (DVB) subtitles into the output.
            :param segment_duration_seconds: Duration (in seconds) of each fragment. Actual fragments are rounded to the nearest multiple of the source fragment duration.
            :param use_audio_rendition_group: When true, AWS Elemental MediaPackage bundles all audio tracks in a rendition group. All other tracks in the stream can be used with any audio rendition from the group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-hlspackage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackage import mixins as mediapackage_mixins
                
                hls_package_property = mediapackage_mixins.CfnPackagingConfigurationPropsMixin.HlsPackageProperty(
                    encryption=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.HlsEncryptionProperty(
                        constant_initialization_vector="constantInitializationVector",
                        encryption_method="encryptionMethod",
                        speke_key_provider=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.SpekeKeyProviderProperty(
                            encryption_contract_configuration=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.EncryptionContractConfigurationProperty(
                                preset_speke20_audio="presetSpeke20Audio",
                                preset_speke20_video="presetSpeke20Video"
                            ),
                            role_arn="roleArn",
                            system_ids=["systemIds"],
                            url="url"
                        )
                    ),
                    hls_manifests=[mediapackage_mixins.CfnPackagingConfigurationPropsMixin.HlsManifestProperty(
                        ad_markers="adMarkers",
                        include_iframe_only_stream=False,
                        manifest_name="manifestName",
                        program_date_time_interval_seconds=123,
                        repeat_ext_xKey=False,
                        stream_selection=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.StreamSelectionProperty(
                            max_video_bits_per_second=123,
                            min_video_bits_per_second=123,
                            stream_order="streamOrder"
                        )
                    )],
                    include_dvb_subtitles=False,
                    segment_duration_seconds=123,
                    use_audio_rendition_group=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__29c37aeaf6dd3db9ccd1821e6df190363505ab2e54a711460c0fe96f79466025)
                check_type(argname="argument encryption", value=encryption, expected_type=type_hints["encryption"])
                check_type(argname="argument hls_manifests", value=hls_manifests, expected_type=type_hints["hls_manifests"])
                check_type(argname="argument include_dvb_subtitles", value=include_dvb_subtitles, expected_type=type_hints["include_dvb_subtitles"])
                check_type(argname="argument segment_duration_seconds", value=segment_duration_seconds, expected_type=type_hints["segment_duration_seconds"])
                check_type(argname="argument use_audio_rendition_group", value=use_audio_rendition_group, expected_type=type_hints["use_audio_rendition_group"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encryption is not None:
                self._values["encryption"] = encryption
            if hls_manifests is not None:
                self._values["hls_manifests"] = hls_manifests
            if include_dvb_subtitles is not None:
                self._values["include_dvb_subtitles"] = include_dvb_subtitles
            if segment_duration_seconds is not None:
                self._values["segment_duration_seconds"] = segment_duration_seconds
            if use_audio_rendition_group is not None:
                self._values["use_audio_rendition_group"] = use_audio_rendition_group

        @builtins.property
        def encryption(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackagingConfigurationPropsMixin.HlsEncryptionProperty"]]:
            '''Parameters for encrypting content.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-hlspackage.html#cfn-mediapackage-packagingconfiguration-hlspackage-encryption
            '''
            result = self._values.get("encryption")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackagingConfigurationPropsMixin.HlsEncryptionProperty"]], result)

        @builtins.property
        def hls_manifests(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackagingConfigurationPropsMixin.HlsManifestProperty"]]]]:
            '''A list of HLS manifest configurations that are available from this endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-hlspackage.html#cfn-mediapackage-packagingconfiguration-hlspackage-hlsmanifests
            '''
            result = self._values.get("hls_manifests")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackagingConfigurationPropsMixin.HlsManifestProperty"]]]], result)

        @builtins.property
        def include_dvb_subtitles(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When enabled, MediaPackage passes through digital video broadcasting (DVB) subtitles into the output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-hlspackage.html#cfn-mediapackage-packagingconfiguration-hlspackage-includedvbsubtitles
            '''
            result = self._values.get("include_dvb_subtitles")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def segment_duration_seconds(self) -> typing.Optional[jsii.Number]:
            '''Duration (in seconds) of each fragment.

            Actual fragments are rounded to the nearest multiple of the source fragment duration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-hlspackage.html#cfn-mediapackage-packagingconfiguration-hlspackage-segmentdurationseconds
            '''
            result = self._values.get("segment_duration_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def use_audio_rendition_group(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When true, AWS Elemental MediaPackage bundles all audio tracks in a rendition group.

            All other tracks in the stream can be used with any audio rendition from the group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-hlspackage.html#cfn-mediapackage-packagingconfiguration-hlspackage-useaudiorenditiongroup
            '''
            result = self._values.get("use_audio_rendition_group")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HlsPackageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.mixins.CfnPackagingConfigurationPropsMixin.MssEncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={"speke_key_provider": "spekeKeyProvider"},
    )
    class MssEncryptionProperty:
        def __init__(
            self,
            *,
            speke_key_provider: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPackagingConfigurationPropsMixin.SpekeKeyProviderProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Holds encryption information so that access to the content can be controlled by a DRM solution.

            :param speke_key_provider: Parameters for the SPEKE key provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-mssencryption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackage import mixins as mediapackage_mixins
                
                mss_encryption_property = mediapackage_mixins.CfnPackagingConfigurationPropsMixin.MssEncryptionProperty(
                    speke_key_provider=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.SpekeKeyProviderProperty(
                        encryption_contract_configuration=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.EncryptionContractConfigurationProperty(
                            preset_speke20_audio="presetSpeke20Audio",
                            preset_speke20_video="presetSpeke20Video"
                        ),
                        role_arn="roleArn",
                        system_ids=["systemIds"],
                        url="url"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3665fe2318af90067f7ddfd07990c53ab8559282dbd27796052e441294af38e1)
                check_type(argname="argument speke_key_provider", value=speke_key_provider, expected_type=type_hints["speke_key_provider"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if speke_key_provider is not None:
                self._values["speke_key_provider"] = speke_key_provider

        @builtins.property
        def speke_key_provider(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackagingConfigurationPropsMixin.SpekeKeyProviderProperty"]]:
            '''Parameters for the SPEKE key provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-mssencryption.html#cfn-mediapackage-packagingconfiguration-mssencryption-spekekeyprovider
            '''
            result = self._values.get("speke_key_provider")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackagingConfigurationPropsMixin.SpekeKeyProviderProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MssEncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.mixins.CfnPackagingConfigurationPropsMixin.MssManifestProperty",
        jsii_struct_bases=[],
        name_mapping={
            "manifest_name": "manifestName",
            "stream_selection": "streamSelection",
        },
    )
    class MssManifestProperty:
        def __init__(
            self,
            *,
            manifest_name: typing.Optional[builtins.str] = None,
            stream_selection: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPackagingConfigurationPropsMixin.StreamSelectionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Parameters for a Microsoft Smooth manifest.

            :param manifest_name: A short string that's appended to the end of the endpoint URL to create a unique path to this packaging configuration.
            :param stream_selection: Video bitrate limitations for outputs from this packaging configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-mssmanifest.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackage import mixins as mediapackage_mixins
                
                mss_manifest_property = mediapackage_mixins.CfnPackagingConfigurationPropsMixin.MssManifestProperty(
                    manifest_name="manifestName",
                    stream_selection=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.StreamSelectionProperty(
                        max_video_bits_per_second=123,
                        min_video_bits_per_second=123,
                        stream_order="streamOrder"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5641ef148eee972b2a5f7ed9b2f2cf71b8bb2a7559bee6947c1f1032ffdc0a52)
                check_type(argname="argument manifest_name", value=manifest_name, expected_type=type_hints["manifest_name"])
                check_type(argname="argument stream_selection", value=stream_selection, expected_type=type_hints["stream_selection"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if manifest_name is not None:
                self._values["manifest_name"] = manifest_name
            if stream_selection is not None:
                self._values["stream_selection"] = stream_selection

        @builtins.property
        def manifest_name(self) -> typing.Optional[builtins.str]:
            '''A short string that's appended to the end of the endpoint URL to create a unique path to this packaging configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-mssmanifest.html#cfn-mediapackage-packagingconfiguration-mssmanifest-manifestname
            '''
            result = self._values.get("manifest_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def stream_selection(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackagingConfigurationPropsMixin.StreamSelectionProperty"]]:
            '''Video bitrate limitations for outputs from this packaging configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-mssmanifest.html#cfn-mediapackage-packagingconfiguration-mssmanifest-streamselection
            '''
            result = self._values.get("stream_selection")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackagingConfigurationPropsMixin.StreamSelectionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MssManifestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.mixins.CfnPackagingConfigurationPropsMixin.MssPackageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "encryption": "encryption",
            "mss_manifests": "mssManifests",
            "segment_duration_seconds": "segmentDurationSeconds",
        },
    )
    class MssPackageProperty:
        def __init__(
            self,
            *,
            encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPackagingConfigurationPropsMixin.MssEncryptionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            mss_manifests: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPackagingConfigurationPropsMixin.MssManifestProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            segment_duration_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Parameters for a packaging configuration that uses Microsoft Smooth Streaming (MSS) packaging.

            :param encryption: Parameters for encrypting content.
            :param mss_manifests: A list of Microsoft Smooth manifest configurations that are available from this endpoint.
            :param segment_duration_seconds: Duration (in seconds) of each fragment. Actual fragments are rounded to the nearest multiple of the source fragment duration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-msspackage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackage import mixins as mediapackage_mixins
                
                mss_package_property = mediapackage_mixins.CfnPackagingConfigurationPropsMixin.MssPackageProperty(
                    encryption=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.MssEncryptionProperty(
                        speke_key_provider=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.SpekeKeyProviderProperty(
                            encryption_contract_configuration=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.EncryptionContractConfigurationProperty(
                                preset_speke20_audio="presetSpeke20Audio",
                                preset_speke20_video="presetSpeke20Video"
                            ),
                            role_arn="roleArn",
                            system_ids=["systemIds"],
                            url="url"
                        )
                    ),
                    mss_manifests=[mediapackage_mixins.CfnPackagingConfigurationPropsMixin.MssManifestProperty(
                        manifest_name="manifestName",
                        stream_selection=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.StreamSelectionProperty(
                            max_video_bits_per_second=123,
                            min_video_bits_per_second=123,
                            stream_order="streamOrder"
                        )
                    )],
                    segment_duration_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e54c00e46ec1d6fb4546d1b162a50329c98696cd68332f1243e9cf1cf56d49d9)
                check_type(argname="argument encryption", value=encryption, expected_type=type_hints["encryption"])
                check_type(argname="argument mss_manifests", value=mss_manifests, expected_type=type_hints["mss_manifests"])
                check_type(argname="argument segment_duration_seconds", value=segment_duration_seconds, expected_type=type_hints["segment_duration_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encryption is not None:
                self._values["encryption"] = encryption
            if mss_manifests is not None:
                self._values["mss_manifests"] = mss_manifests
            if segment_duration_seconds is not None:
                self._values["segment_duration_seconds"] = segment_duration_seconds

        @builtins.property
        def encryption(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackagingConfigurationPropsMixin.MssEncryptionProperty"]]:
            '''Parameters for encrypting content.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-msspackage.html#cfn-mediapackage-packagingconfiguration-msspackage-encryption
            '''
            result = self._values.get("encryption")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackagingConfigurationPropsMixin.MssEncryptionProperty"]], result)

        @builtins.property
        def mss_manifests(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackagingConfigurationPropsMixin.MssManifestProperty"]]]]:
            '''A list of Microsoft Smooth manifest configurations that are available from this endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-msspackage.html#cfn-mediapackage-packagingconfiguration-msspackage-mssmanifests
            '''
            result = self._values.get("mss_manifests")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackagingConfigurationPropsMixin.MssManifestProperty"]]]], result)

        @builtins.property
        def segment_duration_seconds(self) -> typing.Optional[jsii.Number]:
            '''Duration (in seconds) of each fragment.

            Actual fragments are rounded to the nearest multiple of the source fragment duration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-msspackage.html#cfn-mediapackage-packagingconfiguration-msspackage-segmentdurationseconds
            '''
            result = self._values.get("segment_duration_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MssPackageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.mixins.CfnPackagingConfigurationPropsMixin.SpekeKeyProviderProperty",
        jsii_struct_bases=[],
        name_mapping={
            "encryption_contract_configuration": "encryptionContractConfiguration",
            "role_arn": "roleArn",
            "system_ids": "systemIds",
            "url": "url",
        },
    )
    class SpekeKeyProviderProperty:
        def __init__(
            self,
            *,
            encryption_contract_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPackagingConfigurationPropsMixin.EncryptionContractConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            role_arn: typing.Optional[builtins.str] = None,
            system_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A configuration for accessing an external Secure Packager and Encoder Key Exchange (SPEKE) service that provides encryption keys.

            :param encryption_contract_configuration: Use ``encryptionContractConfiguration`` to configure one or more content encryption keys for your endpoints that use SPEKE Version 2.0. The encryption contract defines which content keys are used to encrypt the audio and video tracks in your stream. To configure the encryption contract, specify which audio and video encryption presets to use.
            :param role_arn: The ARN for the IAM role that's granted by the key provider to provide access to the key provider API. Valid format: arn:aws:iam::{accountID}:role/{name}
            :param system_ids: List of unique identifiers for the DRM systems to use, as defined in the CPIX specification.
            :param url: URL for the key provider's key retrieval API endpoint. Must start with https://.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-spekekeyprovider.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackage import mixins as mediapackage_mixins
                
                speke_key_provider_property = mediapackage_mixins.CfnPackagingConfigurationPropsMixin.SpekeKeyProviderProperty(
                    encryption_contract_configuration=mediapackage_mixins.CfnPackagingConfigurationPropsMixin.EncryptionContractConfigurationProperty(
                        preset_speke20_audio="presetSpeke20Audio",
                        preset_speke20_video="presetSpeke20Video"
                    ),
                    role_arn="roleArn",
                    system_ids=["systemIds"],
                    url="url"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2c5478ec17015a7ef143c1e0e7cd6fd51905de4230ae72a3fbbf44a4884ab2b0)
                check_type(argname="argument encryption_contract_configuration", value=encryption_contract_configuration, expected_type=type_hints["encryption_contract_configuration"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument system_ids", value=system_ids, expected_type=type_hints["system_ids"])
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encryption_contract_configuration is not None:
                self._values["encryption_contract_configuration"] = encryption_contract_configuration
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if system_ids is not None:
                self._values["system_ids"] = system_ids
            if url is not None:
                self._values["url"] = url

        @builtins.property
        def encryption_contract_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackagingConfigurationPropsMixin.EncryptionContractConfigurationProperty"]]:
            '''Use ``encryptionContractConfiguration`` to configure one or more content encryption keys for your endpoints that use SPEKE Version 2.0. The encryption contract defines which content keys are used to encrypt the audio and video tracks in your stream. To configure the encryption contract, specify which audio and video encryption presets to use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-spekekeyprovider.html#cfn-mediapackage-packagingconfiguration-spekekeyprovider-encryptioncontractconfiguration
            '''
            result = self._values.get("encryption_contract_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackagingConfigurationPropsMixin.EncryptionContractConfigurationProperty"]], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN for the IAM role that's granted by the key provider to provide access to the key provider API.

            Valid format: arn:aws:iam::{accountID}:role/{name}

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-spekekeyprovider.html#cfn-mediapackage-packagingconfiguration-spekekeyprovider-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def system_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''List of unique identifiers for the DRM systems to use, as defined in the CPIX specification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-spekekeyprovider.html#cfn-mediapackage-packagingconfiguration-spekekeyprovider-systemids
            '''
            result = self._values.get("system_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            '''URL for the key provider's key retrieval API endpoint.

            Must start with https://.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-spekekeyprovider.html#cfn-mediapackage-packagingconfiguration-spekekeyprovider-url
            '''
            result = self._values.get("url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SpekeKeyProviderProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.mixins.CfnPackagingConfigurationPropsMixin.StreamSelectionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "max_video_bits_per_second": "maxVideoBitsPerSecond",
            "min_video_bits_per_second": "minVideoBitsPerSecond",
            "stream_order": "streamOrder",
        },
    )
    class StreamSelectionProperty:
        def __init__(
            self,
            *,
            max_video_bits_per_second: typing.Optional[jsii.Number] = None,
            min_video_bits_per_second: typing.Optional[jsii.Number] = None,
            stream_order: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Limitations for outputs from the endpoint, based on the video bitrate.

            :param max_video_bits_per_second: The upper limit of the bitrates that this endpoint serves. If the video track exceeds this threshold, then AWS Elemental MediaPackage excludes it from output. If you don't specify a value, it defaults to 2147483647 bits per second.
            :param min_video_bits_per_second: The lower limit of the bitrates that this endpoint serves. If the video track is below this threshold, then AWS Elemental MediaPackage excludes it from output. If you don't specify a value, it defaults to 0 bits per second.
            :param stream_order: Order in which the different video bitrates are presented to the player. Valid values: ``ORIGINAL`` , ``VIDEO_BITRATE_ASCENDING`` , ``VIDEO_BITRATE_DESCENDING`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-streamselection.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackage import mixins as mediapackage_mixins
                
                stream_selection_property = mediapackage_mixins.CfnPackagingConfigurationPropsMixin.StreamSelectionProperty(
                    max_video_bits_per_second=123,
                    min_video_bits_per_second=123,
                    stream_order="streamOrder"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c3e8a496f34d30a0bb1ce1e2a0f3f94677284613fcce84b9d8fb2e6e859bc686)
                check_type(argname="argument max_video_bits_per_second", value=max_video_bits_per_second, expected_type=type_hints["max_video_bits_per_second"])
                check_type(argname="argument min_video_bits_per_second", value=min_video_bits_per_second, expected_type=type_hints["min_video_bits_per_second"])
                check_type(argname="argument stream_order", value=stream_order, expected_type=type_hints["stream_order"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_video_bits_per_second is not None:
                self._values["max_video_bits_per_second"] = max_video_bits_per_second
            if min_video_bits_per_second is not None:
                self._values["min_video_bits_per_second"] = min_video_bits_per_second
            if stream_order is not None:
                self._values["stream_order"] = stream_order

        @builtins.property
        def max_video_bits_per_second(self) -> typing.Optional[jsii.Number]:
            '''The upper limit of the bitrates that this endpoint serves.

            If the video track exceeds this threshold, then AWS Elemental MediaPackage excludes it from output. If you don't specify a value, it defaults to 2147483647 bits per second.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-streamselection.html#cfn-mediapackage-packagingconfiguration-streamselection-maxvideobitspersecond
            '''
            result = self._values.get("max_video_bits_per_second")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min_video_bits_per_second(self) -> typing.Optional[jsii.Number]:
            '''The lower limit of the bitrates that this endpoint serves.

            If the video track is below this threshold, then AWS Elemental MediaPackage excludes it from output. If you don't specify a value, it defaults to 0 bits per second.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-streamselection.html#cfn-mediapackage-packagingconfiguration-streamselection-minvideobitspersecond
            '''
            result = self._values.get("min_video_bits_per_second")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def stream_order(self) -> typing.Optional[builtins.str]:
            '''Order in which the different video bitrates are presented to the player.

            Valid values: ``ORIGINAL`` , ``VIDEO_BITRATE_ASCENDING`` , ``VIDEO_BITRATE_DESCENDING`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-streamselection.html#cfn-mediapackage-packagingconfiguration-streamselection-streamorder
            '''
            result = self._values.get("stream_order")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StreamSelectionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.mixins.CfnPackagingGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "authorization": "authorization",
        "egress_access_logs": "egressAccessLogs",
        "id": "id",
        "tags": "tags",
    },
)
class CfnPackagingGroupMixinProps:
    def __init__(
        self,
        *,
        authorization: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPackagingGroupPropsMixin.AuthorizationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        egress_access_logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPackagingGroupPropsMixin.LogConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnPackagingGroupPropsMixin.

        :param authorization: Parameters for CDN authorization.
        :param egress_access_logs: The configuration parameters for egress access logging.
        :param id: Unique identifier that you assign to the packaging group.
        :param tags: The tags to assign to the packaging group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-packaginggroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_mediapackage import mixins as mediapackage_mixins
            
            cfn_packaging_group_mixin_props = mediapackage_mixins.CfnPackagingGroupMixinProps(
                authorization=mediapackage_mixins.CfnPackagingGroupPropsMixin.AuthorizationProperty(
                    cdn_identifier_secret="cdnIdentifierSecret",
                    secrets_role_arn="secretsRoleArn"
                ),
                egress_access_logs=mediapackage_mixins.CfnPackagingGroupPropsMixin.LogConfigurationProperty(
                    log_group_name="logGroupName"
                ),
                id="id",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__312ed733e2b0f9516021c1982c7fe7f5d763959ce5cce6e8b548f88f4eb9d223)
            check_type(argname="argument authorization", value=authorization, expected_type=type_hints["authorization"])
            check_type(argname="argument egress_access_logs", value=egress_access_logs, expected_type=type_hints["egress_access_logs"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if authorization is not None:
            self._values["authorization"] = authorization
        if egress_access_logs is not None:
            self._values["egress_access_logs"] = egress_access_logs
        if id is not None:
            self._values["id"] = id
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def authorization(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackagingGroupPropsMixin.AuthorizationProperty"]]:
        '''Parameters for CDN authorization.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-packaginggroup.html#cfn-mediapackage-packaginggroup-authorization
        '''
        result = self._values.get("authorization")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackagingGroupPropsMixin.AuthorizationProperty"]], result)

    @builtins.property
    def egress_access_logs(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackagingGroupPropsMixin.LogConfigurationProperty"]]:
        '''The configuration parameters for egress access logging.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-packaginggroup.html#cfn-mediapackage-packaginggroup-egressaccesslogs
        '''
        result = self._values.get("egress_access_logs")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackagingGroupPropsMixin.LogConfigurationProperty"]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Unique identifier that you assign to the packaging group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-packaginggroup.html#cfn-mediapackage-packaginggroup-id
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags to assign to the packaging group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-packaginggroup.html#cfn-mediapackage-packaginggroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPackagingGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPackagingGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.mixins.CfnPackagingGroupPropsMixin",
):
    '''Creates a packaging group.

    The packaging group holds one or more packaging configurations. When you create an asset, you specify the packaging group associated with the asset. The asset has playback endpoints for each packaging configuration within the group.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-packaginggroup.html
    :cloudformationResource: AWS::MediaPackage::PackagingGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_mediapackage import mixins as mediapackage_mixins
        
        cfn_packaging_group_props_mixin = mediapackage_mixins.CfnPackagingGroupPropsMixin(mediapackage_mixins.CfnPackagingGroupMixinProps(
            authorization=mediapackage_mixins.CfnPackagingGroupPropsMixin.AuthorizationProperty(
                cdn_identifier_secret="cdnIdentifierSecret",
                secrets_role_arn="secretsRoleArn"
            ),
            egress_access_logs=mediapackage_mixins.CfnPackagingGroupPropsMixin.LogConfigurationProperty(
                log_group_name="logGroupName"
            ),
            id="id",
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
        props: typing.Union[CfnPackagingGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::MediaPackage::PackagingGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d7f3622f65e8837ec9d00ce98b2914825388a84635f32a49716e7ccb8d647eb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5aacb7260465b24b528cbfc760f9729a0e5dc5117390b46bed10b101fc99538a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c65b90b7b1823ccb9d86169600487a6e0a1178e3362362df63570b9a240ad6b5)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPackagingGroupMixinProps:
        return typing.cast(CfnPackagingGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.mixins.CfnPackagingGroupPropsMixin.AuthorizationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cdn_identifier_secret": "cdnIdentifierSecret",
            "secrets_role_arn": "secretsRoleArn",
        },
    )
    class AuthorizationProperty:
        def __init__(
            self,
            *,
            cdn_identifier_secret: typing.Optional[builtins.str] = None,
            secrets_role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Parameters for enabling CDN authorization.

            :param cdn_identifier_secret: The Amazon Resource Name (ARN) for the secret in AWS Secrets Manager that is used for CDN authorization.
            :param secrets_role_arn: The Amazon Resource Name (ARN) for the IAM role that allows AWS Elemental MediaPackage to communicate with AWS Secrets Manager .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packaginggroup-authorization.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackage import mixins as mediapackage_mixins
                
                authorization_property = mediapackage_mixins.CfnPackagingGroupPropsMixin.AuthorizationProperty(
                    cdn_identifier_secret="cdnIdentifierSecret",
                    secrets_role_arn="secretsRoleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0a5dd88ab74f8edf8315d9b5a5c23ee3e37873682c4755df499973451dc59af8)
                check_type(argname="argument cdn_identifier_secret", value=cdn_identifier_secret, expected_type=type_hints["cdn_identifier_secret"])
                check_type(argname="argument secrets_role_arn", value=secrets_role_arn, expected_type=type_hints["secrets_role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cdn_identifier_secret is not None:
                self._values["cdn_identifier_secret"] = cdn_identifier_secret
            if secrets_role_arn is not None:
                self._values["secrets_role_arn"] = secrets_role_arn

        @builtins.property
        def cdn_identifier_secret(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) for the secret in AWS Secrets Manager that is used for CDN authorization.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packaginggroup-authorization.html#cfn-mediapackage-packaginggroup-authorization-cdnidentifiersecret
            '''
            result = self._values.get("cdn_identifier_secret")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secrets_role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) for the IAM role that allows AWS Elemental MediaPackage to communicate with AWS Secrets Manager .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packaginggroup-authorization.html#cfn-mediapackage-packaginggroup-authorization-secretsrolearn
            '''
            result = self._values.get("secrets_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthorizationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.mixins.CfnPackagingGroupPropsMixin.LogConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"log_group_name": "logGroupName"},
    )
    class LogConfigurationProperty:
        def __init__(
            self,
            *,
            log_group_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Sets a custom Amazon CloudWatch log group name for egress logs.

            If a log group name isn't specified, the default name is used: /aws/MediaPackage/EgressAccessLogs.

            :param log_group_name: Sets a custom Amazon CloudWatch log group name for egress logs. If a log group name isn't specified, the default name is used: /aws/MediaPackage/EgressAccessLogs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packaginggroup-logconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackage import mixins as mediapackage_mixins
                
                log_configuration_property = mediapackage_mixins.CfnPackagingGroupPropsMixin.LogConfigurationProperty(
                    log_group_name="logGroupName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cadb27ef0bb1195c1317b631c54369f7092bc2e836995027124059f9c7c0115a)
                check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if log_group_name is not None:
                self._values["log_group_name"] = log_group_name

        @builtins.property
        def log_group_name(self) -> typing.Optional[builtins.str]:
            '''Sets a custom Amazon CloudWatch log group name for egress logs.

            If a log group name isn't specified, the default name is used: /aws/MediaPackage/EgressAccessLogs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packaginggroup-logconfiguration.html#cfn-mediapackage-packaginggroup-logconfiguration-loggroupname
            '''
            result = self._values.get("log_group_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnAssetMixinProps",
    "CfnAssetPropsMixin",
    "CfnChannelMixinProps",
    "CfnChannelPropsMixin",
    "CfnOriginEndpointMixinProps",
    "CfnOriginEndpointPropsMixin",
    "CfnPackagingConfigurationMixinProps",
    "CfnPackagingConfigurationPropsMixin",
    "CfnPackagingGroupMixinProps",
    "CfnPackagingGroupPropsMixin",
]

publication.publish()

def _typecheckingstub__0df7bf8ea84ee7bff12f83c47c9580e26b066d2a5f30620d771850d7689bc1d9(
    *,
    egress_endpoints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAssetPropsMixin.EgressEndpointProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    packaging_group_id: typing.Optional[builtins.str] = None,
    resource_id: typing.Optional[builtins.str] = None,
    source_arn: typing.Optional[builtins.str] = None,
    source_role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e9febc4eb1b1f204893cfbfe1623af3415e3df1d1b764fb10e1c6dbf43e4d6b(
    props: typing.Union[CfnAssetMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__841d713efad38377d211fc906ba12af565040112bd7dd7c64b8ebfcac8164f18(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05e42bb7b80bba68eef730e876a7450ce036769080c3d9f33dc5faea45e6b82b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d09dec6d7e849ac98bb1bb6803c3331e07c4af19a5af27155c15672e8f5b55a6(
    *,
    packaging_configuration_id: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c845133e9599091587a7f9d866767c7e1c8503d4002375c8c3ac247d30ee0823(
    *,
    description: typing.Optional[builtins.str] = None,
    egress_access_logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnChannelPropsMixin.LogConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    hls_ingest: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnChannelPropsMixin.HlsIngestProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    id: typing.Optional[builtins.str] = None,
    ingress_access_logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnChannelPropsMixin.LogConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0f9b149b0426af1fc0e60876b44cbed500fe314a1cad7fc7ac08c5f3f48b71a(
    props: typing.Union[CfnChannelMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__644d3de8d9d45775e11ae63846e02cc50218d49da36eb0f1d0925d6015695bc3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab219c43e6582abc1dd20672180343ab1b24f707f798647df2c9771ef235a9bb(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91be515a47d53eaf3ab2265fffce9f8b02e98c53c9a29d6dc2a204e4c8780615(
    *,
    ingest_endpoints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnChannelPropsMixin.IngestEndpointProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02b0ab0d96c8fc6451858c05d9272dcb33ae4fe06559b4ff8091c8ad5fd7d246(
    *,
    id: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__688eef1c6e42421bdf9d4d3c0d4cffa16374360d795be739c325207ed9ac1fe4(
    *,
    log_group_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82977f54939485256df122f4611462d11e3def1637a024ed9be447f9f6b4a9d5(
    *,
    authorization: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.AuthorizationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    channel_id: typing.Optional[builtins.str] = None,
    cmaf_package: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.CmafPackageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dash_package: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.DashPackageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    hls_package: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.HlsPackageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    id: typing.Optional[builtins.str] = None,
    manifest_name: typing.Optional[builtins.str] = None,
    mss_package: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.MssPackageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    origination: typing.Optional[builtins.str] = None,
    startover_window_seconds: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    time_delay_seconds: typing.Optional[jsii.Number] = None,
    whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c82cdcb6373ea0631858d58c6052cb18fd1e48e5351290e8265d019c27f7601(
    props: typing.Union[CfnOriginEndpointMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08f61c382d971d27740b766125ba45a38522302cd6db336f16fb14d4c421d1a8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6257233aa05faa718918e5d2cc805ba1d51f680b11a1c0c5caecebe58c34f4c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b392d35d5c91b98e4b01e13bdfda00996ddcab443969faa62cb790e5c7e81ab(
    *,
    cdn_identifier_secret: typing.Optional[builtins.str] = None,
    secrets_role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d74b82d728039352b424e39a4bfdd8afbf512b6d09f94e427aa42926cba5823a(
    *,
    constant_initialization_vector: typing.Optional[builtins.str] = None,
    encryption_method: typing.Optional[builtins.str] = None,
    key_rotation_interval_seconds: typing.Optional[jsii.Number] = None,
    speke_key_provider: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.SpekeKeyProviderProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b777c2f2cfa22aa9587c33291dd88839d00a23a73151c30bc211900bb257b8e5(
    *,
    encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.CmafEncryptionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    hls_manifests: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.HlsManifestProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    segment_duration_seconds: typing.Optional[jsii.Number] = None,
    segment_prefix: typing.Optional[builtins.str] = None,
    stream_selection: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.StreamSelectionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a0dcebfe3ea2121178a4b62e1ee60706cd338a19ac3eab8ad621d06ec1a78c8(
    *,
    key_rotation_interval_seconds: typing.Optional[jsii.Number] = None,
    speke_key_provider: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.SpekeKeyProviderProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6f25b74519cc5c9c610c9e025b52e0b21c1070662a37ed36073a1d962a9ef83(
    *,
    ads_on_delivery_restrictions: typing.Optional[builtins.str] = None,
    ad_triggers: typing.Optional[typing.Sequence[builtins.str]] = None,
    encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.DashEncryptionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    include_iframe_only_stream: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    manifest_layout: typing.Optional[builtins.str] = None,
    manifest_window_seconds: typing.Optional[jsii.Number] = None,
    min_buffer_time_seconds: typing.Optional[jsii.Number] = None,
    min_update_period_seconds: typing.Optional[jsii.Number] = None,
    period_triggers: typing.Optional[typing.Sequence[builtins.str]] = None,
    profile: typing.Optional[builtins.str] = None,
    segment_duration_seconds: typing.Optional[jsii.Number] = None,
    segment_template_format: typing.Optional[builtins.str] = None,
    stream_selection: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.StreamSelectionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    suggested_presentation_delay_seconds: typing.Optional[jsii.Number] = None,
    utc_timing: typing.Optional[builtins.str] = None,
    utc_timing_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ca8ad2eba097ad61909c8108e91199aa63ec9b7c61cfb8321351d346c0b53ad(
    *,
    preset_speke20_audio: typing.Optional[builtins.str] = None,
    preset_speke20_video: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c56efdb9121ff2acfb5317b841a80b3cd0fc30160ac6a835533dc841d6c84247(
    *,
    constant_initialization_vector: typing.Optional[builtins.str] = None,
    encryption_method: typing.Optional[builtins.str] = None,
    key_rotation_interval_seconds: typing.Optional[jsii.Number] = None,
    repeat_ext_x_key: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    speke_key_provider: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.SpekeKeyProviderProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12812e1bde15011cf3510d1138d3ff6454a5c6fb1d0d9d00a63587cec893a024(
    *,
    ad_markers: typing.Optional[builtins.str] = None,
    ads_on_delivery_restrictions: typing.Optional[builtins.str] = None,
    ad_triggers: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    include_iframe_only_stream: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    manifest_name: typing.Optional[builtins.str] = None,
    playlist_type: typing.Optional[builtins.str] = None,
    playlist_window_seconds: typing.Optional[jsii.Number] = None,
    program_date_time_interval_seconds: typing.Optional[jsii.Number] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5480fd065b06ca7153648da95392151b192ac1d7277c5b900e53cc90cd0cd681(
    *,
    ad_markers: typing.Optional[builtins.str] = None,
    ads_on_delivery_restrictions: typing.Optional[builtins.str] = None,
    ad_triggers: typing.Optional[typing.Sequence[builtins.str]] = None,
    encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.HlsEncryptionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    include_dvb_subtitles: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    include_iframe_only_stream: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    playlist_type: typing.Optional[builtins.str] = None,
    playlist_window_seconds: typing.Optional[jsii.Number] = None,
    program_date_time_interval_seconds: typing.Optional[jsii.Number] = None,
    segment_duration_seconds: typing.Optional[jsii.Number] = None,
    stream_selection: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.StreamSelectionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    use_audio_rendition_group: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aef4645bed246e5e8bcedf6899c51634315a62dcd507fff8671b304647250a52(
    *,
    speke_key_provider: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.SpekeKeyProviderProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a42e05c0e9e2703fee06f8929df9cee11c822c4bd402797e8830aba68b259be(
    *,
    encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.MssEncryptionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    manifest_window_seconds: typing.Optional[jsii.Number] = None,
    segment_duration_seconds: typing.Optional[jsii.Number] = None,
    stream_selection: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.StreamSelectionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93a222a198872450c1324041ba8378b346756ecc8d134da21ff803d550e22361(
    *,
    certificate_arn: typing.Optional[builtins.str] = None,
    encryption_contract_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.EncryptionContractConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    resource_id: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    system_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aafb1ed86e376940d2e55063c951654059bc362442e00d674ffd32916741a74(
    *,
    max_video_bits_per_second: typing.Optional[jsii.Number] = None,
    min_video_bits_per_second: typing.Optional[jsii.Number] = None,
    stream_order: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7088d4f64726c066c6585da16d81634be33085526d661beed9cbcabcd933805e(
    *,
    cmaf_package: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPackagingConfigurationPropsMixin.CmafPackageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dash_package: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPackagingConfigurationPropsMixin.DashPackageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    hls_package: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPackagingConfigurationPropsMixin.HlsPackageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    id: typing.Optional[builtins.str] = None,
    mss_package: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPackagingConfigurationPropsMixin.MssPackageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    packaging_group_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bdb086c754c7b2b93255a12787e828455999dacbbeec8d7fcc41bf0435240ea(
    props: typing.Union[CfnPackagingConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af2606a0cd65fb9eda013af9d6f15eb93dbbfde8368bf1105de67de3cb44cc2e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8bcae51d0a877205a3714fb6aaf55e3f882b0db8c2c28000c0f69871191d107(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5892a9204d3a84825d62a469c891b27f89cc3ca5402ef8c07a14bf8b294eaecc(
    *,
    speke_key_provider: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPackagingConfigurationPropsMixin.SpekeKeyProviderProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24e97281281520157d186f6e4c2e1cddcd3a42f0f253d5248a2551339582624b(
    *,
    encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPackagingConfigurationPropsMixin.CmafEncryptionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    hls_manifests: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPackagingConfigurationPropsMixin.HlsManifestProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    include_encoder_configuration_in_segments: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    segment_duration_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4abd35d6daa8a319b174d185026e9ac00e5e9974bbe6b72b9a35f378bd074a91(
    *,
    speke_key_provider: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPackagingConfigurationPropsMixin.SpekeKeyProviderProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__194677f0f3a6af0c3f9a4cbb8a1e5937c9d93c1aa47e446775d66fd46ba770b3(
    *,
    manifest_layout: typing.Optional[builtins.str] = None,
    manifest_name: typing.Optional[builtins.str] = None,
    min_buffer_time_seconds: typing.Optional[jsii.Number] = None,
    profile: typing.Optional[builtins.str] = None,
    scte_markers_source: typing.Optional[builtins.str] = None,
    stream_selection: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPackagingConfigurationPropsMixin.StreamSelectionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__add89095b13db65cd87b4a48473e935951d0dbcc8014f0096a3f4af39fdedbe6(
    *,
    dash_manifests: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPackagingConfigurationPropsMixin.DashManifestProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPackagingConfigurationPropsMixin.DashEncryptionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    include_encoder_configuration_in_segments: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    include_iframe_only_stream: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    period_triggers: typing.Optional[typing.Sequence[builtins.str]] = None,
    segment_duration_seconds: typing.Optional[jsii.Number] = None,
    segment_template_format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cf6f0b748a4843992ee087a943f2f9117f3b89720c0bacf115b9d8216adb465(
    *,
    preset_speke20_audio: typing.Optional[builtins.str] = None,
    preset_speke20_video: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cde63a457777d587a2b07830d2b06642dc0c6299f59e6506c6655d3050d956bd(
    *,
    constant_initialization_vector: typing.Optional[builtins.str] = None,
    encryption_method: typing.Optional[builtins.str] = None,
    speke_key_provider: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPackagingConfigurationPropsMixin.SpekeKeyProviderProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6de31ebdf780e8d6dfe79ee0353727ac74c5eadfa49fbf355d0f8f42ba4107eb(
    *,
    ad_markers: typing.Optional[builtins.str] = None,
    include_iframe_only_stream: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    manifest_name: typing.Optional[builtins.str] = None,
    program_date_time_interval_seconds: typing.Optional[jsii.Number] = None,
    repeat_ext_x_key: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    stream_selection: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPackagingConfigurationPropsMixin.StreamSelectionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29c37aeaf6dd3db9ccd1821e6df190363505ab2e54a711460c0fe96f79466025(
    *,
    encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPackagingConfigurationPropsMixin.HlsEncryptionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    hls_manifests: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPackagingConfigurationPropsMixin.HlsManifestProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    include_dvb_subtitles: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    segment_duration_seconds: typing.Optional[jsii.Number] = None,
    use_audio_rendition_group: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3665fe2318af90067f7ddfd07990c53ab8559282dbd27796052e441294af38e1(
    *,
    speke_key_provider: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPackagingConfigurationPropsMixin.SpekeKeyProviderProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5641ef148eee972b2a5f7ed9b2f2cf71b8bb2a7559bee6947c1f1032ffdc0a52(
    *,
    manifest_name: typing.Optional[builtins.str] = None,
    stream_selection: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPackagingConfigurationPropsMixin.StreamSelectionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e54c00e46ec1d6fb4546d1b162a50329c98696cd68332f1243e9cf1cf56d49d9(
    *,
    encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPackagingConfigurationPropsMixin.MssEncryptionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    mss_manifests: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPackagingConfigurationPropsMixin.MssManifestProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    segment_duration_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c5478ec17015a7ef143c1e0e7cd6fd51905de4230ae72a3fbbf44a4884ab2b0(
    *,
    encryption_contract_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPackagingConfigurationPropsMixin.EncryptionContractConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    role_arn: typing.Optional[builtins.str] = None,
    system_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3e8a496f34d30a0bb1ce1e2a0f3f94677284613fcce84b9d8fb2e6e859bc686(
    *,
    max_video_bits_per_second: typing.Optional[jsii.Number] = None,
    min_video_bits_per_second: typing.Optional[jsii.Number] = None,
    stream_order: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__312ed733e2b0f9516021c1982c7fe7f5d763959ce5cce6e8b548f88f4eb9d223(
    *,
    authorization: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPackagingGroupPropsMixin.AuthorizationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    egress_access_logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPackagingGroupPropsMixin.LogConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d7f3622f65e8837ec9d00ce98b2914825388a84635f32a49716e7ccb8d647eb(
    props: typing.Union[CfnPackagingGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aacb7260465b24b528cbfc760f9729a0e5dc5117390b46bed10b101fc99538a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c65b90b7b1823ccb9d86169600487a6e0a1178e3362362df63570b9a240ad6b5(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a5dd88ab74f8edf8315d9b5a5c23ee3e37873682c4755df499973451dc59af8(
    *,
    cdn_identifier_secret: typing.Optional[builtins.str] = None,
    secrets_role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cadb27ef0bb1195c1317b631c54369f7092bc2e836995027124059f9c7c0115a(
    *,
    log_group_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
