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
    jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnAppBlockBuilderMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_endpoints": "accessEndpoints",
        "app_block_arns": "appBlockArns",
        "description": "description",
        "display_name": "displayName",
        "enable_default_internet_access": "enableDefaultInternetAccess",
        "iam_role_arn": "iamRoleArn",
        "instance_type": "instanceType",
        "name": "name",
        "platform": "platform",
        "tags": "tags",
        "vpc_config": "vpcConfig",
    },
)
class CfnAppBlockBuilderMixinProps:
    def __init__(
        self,
        *,
        access_endpoints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAppBlockBuilderPropsMixin.AccessEndpointProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        app_block_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        enable_default_internet_access: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        iam_role_arn: typing.Optional[builtins.str] = None,
        instance_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        platform: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAppBlockBuilderPropsMixin.VpcConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnAppBlockBuilderPropsMixin.

        :param access_endpoints: The access endpoints of the app block builder.
        :param app_block_arns: The ARN of the app block. *Maximum* : ``1``
        :param description: The description of the app block builder.
        :param display_name: The display name of the app block builder.
        :param enable_default_internet_access: Indicates whether default internet access is enabled for the app block builder.
        :param iam_role_arn: The ARN of the IAM role that is applied to the app block builder.
        :param instance_type: The instance type of the app block builder.
        :param name: The name of the app block builder.
        :param platform: The platform of the app block builder. *Allowed values* : ``WINDOWS_SERVER_2019``
        :param tags: The tags of the app block builder.
        :param vpc_config: The VPC configuration for the app block builder.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-appblockbuilder.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
            
            cfn_app_block_builder_mixin_props = appstream_mixins.CfnAppBlockBuilderMixinProps(
                access_endpoints=[appstream_mixins.CfnAppBlockBuilderPropsMixin.AccessEndpointProperty(
                    endpoint_type="endpointType",
                    vpce_id="vpceId"
                )],
                app_block_arns=["appBlockArns"],
                description="description",
                display_name="displayName",
                enable_default_internet_access=False,
                iam_role_arn="iamRoleArn",
                instance_type="instanceType",
                name="name",
                platform="platform",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vpc_config=appstream_mixins.CfnAppBlockBuilderPropsMixin.VpcConfigProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d3dbb9050e6835996877b6e957e37de7f874926c6e62768c615c362a5ddade9)
            check_type(argname="argument access_endpoints", value=access_endpoints, expected_type=type_hints["access_endpoints"])
            check_type(argname="argument app_block_arns", value=app_block_arns, expected_type=type_hints["app_block_arns"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument enable_default_internet_access", value=enable_default_internet_access, expected_type=type_hints["enable_default_internet_access"])
            check_type(argname="argument iam_role_arn", value=iam_role_arn, expected_type=type_hints["iam_role_arn"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc_config", value=vpc_config, expected_type=type_hints["vpc_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_endpoints is not None:
            self._values["access_endpoints"] = access_endpoints
        if app_block_arns is not None:
            self._values["app_block_arns"] = app_block_arns
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if enable_default_internet_access is not None:
            self._values["enable_default_internet_access"] = enable_default_internet_access
        if iam_role_arn is not None:
            self._values["iam_role_arn"] = iam_role_arn
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if name is not None:
            self._values["name"] = name
        if platform is not None:
            self._values["platform"] = platform
        if tags is not None:
            self._values["tags"] = tags
        if vpc_config is not None:
            self._values["vpc_config"] = vpc_config

    @builtins.property
    def access_endpoints(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppBlockBuilderPropsMixin.AccessEndpointProperty"]]]]:
        '''The access endpoints of the app block builder.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-appblockbuilder.html#cfn-appstream-appblockbuilder-accessendpoints
        '''
        result = self._values.get("access_endpoints")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppBlockBuilderPropsMixin.AccessEndpointProperty"]]]], result)

    @builtins.property
    def app_block_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The ARN of the app block.

        *Maximum* : ``1``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-appblockbuilder.html#cfn-appstream-appblockbuilder-appblockarns
        '''
        result = self._values.get("app_block_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the app block builder.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-appblockbuilder.html#cfn-appstream-appblockbuilder-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name of the app block builder.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-appblockbuilder.html#cfn-appstream-appblockbuilder-displayname
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_default_internet_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Indicates whether default internet access is enabled for the app block builder.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-appblockbuilder.html#cfn-appstream-appblockbuilder-enabledefaultinternetaccess
        '''
        result = self._values.get("enable_default_internet_access")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def iam_role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the IAM role that is applied to the app block builder.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-appblockbuilder.html#cfn-appstream-appblockbuilder-iamrolearn
        '''
        result = self._values.get("iam_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[builtins.str]:
        '''The instance type of the app block builder.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-appblockbuilder.html#cfn-appstream-appblockbuilder-instancetype
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the app block builder.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-appblockbuilder.html#cfn-appstream-appblockbuilder-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def platform(self) -> typing.Optional[builtins.str]:
        '''The platform of the app block builder.

        *Allowed values* : ``WINDOWS_SERVER_2019``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-appblockbuilder.html#cfn-appstream-appblockbuilder-platform
        '''
        result = self._values.get("platform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags of the app block builder.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-appblockbuilder.html#cfn-appstream-appblockbuilder-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def vpc_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppBlockBuilderPropsMixin.VpcConfigProperty"]]:
        '''The VPC configuration for the app block builder.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-appblockbuilder.html#cfn-appstream-appblockbuilder-vpcconfig
        '''
        result = self._values.get("vpc_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppBlockBuilderPropsMixin.VpcConfigProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAppBlockBuilderMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAppBlockBuilderPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnAppBlockBuilderPropsMixin",
):
    '''Creates an app block builder.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-appblockbuilder.html
    :cloudformationResource: AWS::AppStream::AppBlockBuilder
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
        
        cfn_app_block_builder_props_mixin = appstream_mixins.CfnAppBlockBuilderPropsMixin(appstream_mixins.CfnAppBlockBuilderMixinProps(
            access_endpoints=[appstream_mixins.CfnAppBlockBuilderPropsMixin.AccessEndpointProperty(
                endpoint_type="endpointType",
                vpce_id="vpceId"
            )],
            app_block_arns=["appBlockArns"],
            description="description",
            display_name="displayName",
            enable_default_internet_access=False,
            iam_role_arn="iamRoleArn",
            instance_type="instanceType",
            name="name",
            platform="platform",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            vpc_config=appstream_mixins.CfnAppBlockBuilderPropsMixin.VpcConfigProperty(
                security_group_ids=["securityGroupIds"],
                subnet_ids=["subnetIds"]
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAppBlockBuilderMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AppStream::AppBlockBuilder``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3633662d446d4fb6292bb778f2cf89900e9d3ada8c7490589ff827af6f725eb7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5faadeaa706ddb70178eb2a07a71bfeb0c2bdd689f3da800d602d61ae2d55e09)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5265f376d8c62b0f84a886bd7190ee33a4ed94a9564fe48d608b90faa2f87982)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAppBlockBuilderMixinProps:
        return typing.cast(CfnAppBlockBuilderMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnAppBlockBuilderPropsMixin.AccessEndpointProperty",
        jsii_struct_bases=[],
        name_mapping={"endpoint_type": "endpointType", "vpce_id": "vpceId"},
    )
    class AccessEndpointProperty:
        def __init__(
            self,
            *,
            endpoint_type: typing.Optional[builtins.str] = None,
            vpce_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes an interface VPC endpoint (interface endpoint) that lets you create a private connection between the virtual private cloud (VPC) that you specify and AppStream 2.0. When you specify an interface endpoint for a stack, users of the stack can connect to AppStream 2.0 only through that endpoint. When you specify an interface endpoint for an image builder, administrators can connect to the image builder only through that endpoint.

            :param endpoint_type: The type of interface endpoint.
            :param vpce_id: The identifier (ID) of the VPC in which the interface endpoint is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-appblockbuilder-accessendpoint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
                
                access_endpoint_property = appstream_mixins.CfnAppBlockBuilderPropsMixin.AccessEndpointProperty(
                    endpoint_type="endpointType",
                    vpce_id="vpceId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7c16509f404ab735fab41cf647e96b31c8b1647971e44a5e04c3ec817218cc0f)
                check_type(argname="argument endpoint_type", value=endpoint_type, expected_type=type_hints["endpoint_type"])
                check_type(argname="argument vpce_id", value=vpce_id, expected_type=type_hints["vpce_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if endpoint_type is not None:
                self._values["endpoint_type"] = endpoint_type
            if vpce_id is not None:
                self._values["vpce_id"] = vpce_id

        @builtins.property
        def endpoint_type(self) -> typing.Optional[builtins.str]:
            '''The type of interface endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-appblockbuilder-accessendpoint.html#cfn-appstream-appblockbuilder-accessendpoint-endpointtype
            '''
            result = self._values.get("endpoint_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vpce_id(self) -> typing.Optional[builtins.str]:
            '''The identifier (ID) of the VPC in which the interface endpoint is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-appblockbuilder-accessendpoint.html#cfn-appstream-appblockbuilder-accessendpoint-vpceid
            '''
            result = self._values.get("vpce_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessEndpointProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnAppBlockBuilderPropsMixin.VpcConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
        },
    )
    class VpcConfigProperty:
        def __init__(
            self,
            *,
            security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Describes VPC configuration information for fleets and image builders.

            :param security_group_ids: The identifiers of the security groups for the fleet or image builder.
            :param subnet_ids: The identifiers of the subnets to which a network interface is attached from the fleet instance or image builder instance. Fleet instances use one or more subnets. Image builder instances use one subnet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-appblockbuilder-vpcconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
                
                vpc_config_property = appstream_mixins.CfnAppBlockBuilderPropsMixin.VpcConfigProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__11641d1f3823b74a3bd6b95eb5a6b3af99fe1f4a1590a8f2e52db2e589973ea5)
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
                check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnet_ids is not None:
                self._values["subnet_ids"] = subnet_ids

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The identifiers of the security groups for the fleet or image builder.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-appblockbuilder-vpcconfig.html#cfn-appstream-appblockbuilder-vpcconfig-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The identifiers of the subnets to which a network interface is attached from the fleet instance or image builder instance.

            Fleet instances use one or more subnets. Image builder instances use one subnet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-appblockbuilder-vpcconfig.html#cfn-appstream-appblockbuilder-vpcconfig-subnetids
            '''
            result = self._values.get("subnet_ids")
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
    jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnAppBlockMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "display_name": "displayName",
        "name": "name",
        "packaging_type": "packagingType",
        "post_setup_script_details": "postSetupScriptDetails",
        "setup_script_details": "setupScriptDetails",
        "source_s3_location": "sourceS3Location",
        "tags": "tags",
    },
)
class CfnAppBlockMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        packaging_type: typing.Optional[builtins.str] = None,
        post_setup_script_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAppBlockPropsMixin.ScriptDetailsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        setup_script_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAppBlockPropsMixin.ScriptDetailsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        source_s3_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAppBlockPropsMixin.S3LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnAppBlockPropsMixin.

        :param description: The description of the app block.
        :param display_name: The display name of the app block.
        :param name: The name of the app block. *Pattern* : ``^[a-zA-Z0-9][a-zA-Z0-9_.-]{0,100}$``
        :param packaging_type: The packaging type of the app block.
        :param post_setup_script_details: The post setup script details of the app block.
        :param setup_script_details: The setup script details of the app block.
        :param source_s3_location: The source S3 location of the app block.
        :param tags: The tags of the app block.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-appblock.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
            
            cfn_app_block_mixin_props = appstream_mixins.CfnAppBlockMixinProps(
                description="description",
                display_name="displayName",
                name="name",
                packaging_type="packagingType",
                post_setup_script_details=appstream_mixins.CfnAppBlockPropsMixin.ScriptDetailsProperty(
                    executable_parameters="executableParameters",
                    executable_path="executablePath",
                    script_s3_location=appstream_mixins.CfnAppBlockPropsMixin.S3LocationProperty(
                        s3_bucket="s3Bucket",
                        s3_key="s3Key"
                    ),
                    timeout_in_seconds=123
                ),
                setup_script_details=appstream_mixins.CfnAppBlockPropsMixin.ScriptDetailsProperty(
                    executable_parameters="executableParameters",
                    executable_path="executablePath",
                    script_s3_location=appstream_mixins.CfnAppBlockPropsMixin.S3LocationProperty(
                        s3_bucket="s3Bucket",
                        s3_key="s3Key"
                    ),
                    timeout_in_seconds=123
                ),
                source_s3_location=appstream_mixins.CfnAppBlockPropsMixin.S3LocationProperty(
                    s3_bucket="s3Bucket",
                    s3_key="s3Key"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23582a1c3bc01d0c577008bc5b6a11ca06a45bd4f9733a74571410b0ad03ae32)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument packaging_type", value=packaging_type, expected_type=type_hints["packaging_type"])
            check_type(argname="argument post_setup_script_details", value=post_setup_script_details, expected_type=type_hints["post_setup_script_details"])
            check_type(argname="argument setup_script_details", value=setup_script_details, expected_type=type_hints["setup_script_details"])
            check_type(argname="argument source_s3_location", value=source_s3_location, expected_type=type_hints["source_s3_location"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if name is not None:
            self._values["name"] = name
        if packaging_type is not None:
            self._values["packaging_type"] = packaging_type
        if post_setup_script_details is not None:
            self._values["post_setup_script_details"] = post_setup_script_details
        if setup_script_details is not None:
            self._values["setup_script_details"] = setup_script_details
        if source_s3_location is not None:
            self._values["source_s3_location"] = source_s3_location
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the app block.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-appblock.html#cfn-appstream-appblock-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name of the app block.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-appblock.html#cfn-appstream-appblock-displayname
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the app block.

        *Pattern* : ``^[a-zA-Z0-9][a-zA-Z0-9_.-]{0,100}$``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-appblock.html#cfn-appstream-appblock-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def packaging_type(self) -> typing.Optional[builtins.str]:
        '''The packaging type of the app block.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-appblock.html#cfn-appstream-appblock-packagingtype
        '''
        result = self._values.get("packaging_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def post_setup_script_details(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppBlockPropsMixin.ScriptDetailsProperty"]]:
        '''The post setup script details of the app block.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-appblock.html#cfn-appstream-appblock-postsetupscriptdetails
        '''
        result = self._values.get("post_setup_script_details")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppBlockPropsMixin.ScriptDetailsProperty"]], result)

    @builtins.property
    def setup_script_details(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppBlockPropsMixin.ScriptDetailsProperty"]]:
        '''The setup script details of the app block.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-appblock.html#cfn-appstream-appblock-setupscriptdetails
        '''
        result = self._values.get("setup_script_details")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppBlockPropsMixin.ScriptDetailsProperty"]], result)

    @builtins.property
    def source_s3_location(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppBlockPropsMixin.S3LocationProperty"]]:
        '''The source S3 location of the app block.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-appblock.html#cfn-appstream-appblock-sources3location
        '''
        result = self._values.get("source_s3_location")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppBlockPropsMixin.S3LocationProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags of the app block.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-appblock.html#cfn-appstream-appblock-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAppBlockMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAppBlockPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnAppBlockPropsMixin",
):
    '''This resource creates an app block.

    App blocks store details about the virtual hard disk that contains the files for the application in an S3 bucket. It also stores the setup script with details about how to mount the virtual hard disk. App blocks are only supported for Elastic fleets.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-appblock.html
    :cloudformationResource: AWS::AppStream::AppBlock
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
        
        cfn_app_block_props_mixin = appstream_mixins.CfnAppBlockPropsMixin(appstream_mixins.CfnAppBlockMixinProps(
            description="description",
            display_name="displayName",
            name="name",
            packaging_type="packagingType",
            post_setup_script_details=appstream_mixins.CfnAppBlockPropsMixin.ScriptDetailsProperty(
                executable_parameters="executableParameters",
                executable_path="executablePath",
                script_s3_location=appstream_mixins.CfnAppBlockPropsMixin.S3LocationProperty(
                    s3_bucket="s3Bucket",
                    s3_key="s3Key"
                ),
                timeout_in_seconds=123
            ),
            setup_script_details=appstream_mixins.CfnAppBlockPropsMixin.ScriptDetailsProperty(
                executable_parameters="executableParameters",
                executable_path="executablePath",
                script_s3_location=appstream_mixins.CfnAppBlockPropsMixin.S3LocationProperty(
                    s3_bucket="s3Bucket",
                    s3_key="s3Key"
                ),
                timeout_in_seconds=123
            ),
            source_s3_location=appstream_mixins.CfnAppBlockPropsMixin.S3LocationProperty(
                s3_bucket="s3Bucket",
                s3_key="s3Key"
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
        props: typing.Union[CfnAppBlockMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AppStream::AppBlock``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73464241f1cc7bde8bdbc6c4b98fbacbd5572e73a8216fbf00370122d5484dd2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f9eae4d6e1384bd6bddc76e815f444bac613e741a9c8b230c40b52296870014)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51466f31cee1d8d5163cdae1860c98403ec45f1c0f5aea334c5b0e8517b727b8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAppBlockMixinProps:
        return typing.cast(CfnAppBlockMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnAppBlockPropsMixin.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_bucket": "s3Bucket", "s3_key": "s3Key"},
    )
    class S3LocationProperty:
        def __init__(
            self,
            *,
            s3_bucket: typing.Optional[builtins.str] = None,
            s3_key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The S3 location of the app block.

            :param s3_bucket: The S3 bucket of the app block.
            :param s3_key: The S3 key of the S3 object of the virtual hard disk. This is required when it's used by ``SetupScriptDetails`` and ``PostSetupScriptDetails`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-appblock-s3location.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
                
                s3_location_property = appstream_mixins.CfnAppBlockPropsMixin.S3LocationProperty(
                    s3_bucket="s3Bucket",
                    s3_key="s3Key"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9d19ee18f356d5cb83a525aaa649654488e98d79da492e1ed53db686f987f455)
                check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
                check_type(argname="argument s3_key", value=s3_key, expected_type=type_hints["s3_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3_bucket is not None:
                self._values["s3_bucket"] = s3_bucket
            if s3_key is not None:
                self._values["s3_key"] = s3_key

        @builtins.property
        def s3_bucket(self) -> typing.Optional[builtins.str]:
            '''The S3 bucket of the app block.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-appblock-s3location.html#cfn-appstream-appblock-s3location-s3bucket
            '''
            result = self._values.get("s3_bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_key(self) -> typing.Optional[builtins.str]:
            '''The S3 key of the S3 object of the virtual hard disk.

            This is required when it's used by ``SetupScriptDetails`` and ``PostSetupScriptDetails`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-appblock-s3location.html#cfn-appstream-appblock-s3location-s3key
            '''
            result = self._values.get("s3_key")
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
        jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnAppBlockPropsMixin.ScriptDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "executable_parameters": "executableParameters",
            "executable_path": "executablePath",
            "script_s3_location": "scriptS3Location",
            "timeout_in_seconds": "timeoutInSeconds",
        },
    )
    class ScriptDetailsProperty:
        def __init__(
            self,
            *,
            executable_parameters: typing.Optional[builtins.str] = None,
            executable_path: typing.Optional[builtins.str] = None,
            script_s3_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAppBlockPropsMixin.S3LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            timeout_in_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The details of the script.

            :param executable_parameters: The parameters used in the run path for the script.
            :param executable_path: The run path for the script.
            :param script_s3_location: The S3 object location of the script.
            :param timeout_in_seconds: The run timeout, in seconds, for the script.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-appblock-scriptdetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
                
                script_details_property = appstream_mixins.CfnAppBlockPropsMixin.ScriptDetailsProperty(
                    executable_parameters="executableParameters",
                    executable_path="executablePath",
                    script_s3_location=appstream_mixins.CfnAppBlockPropsMixin.S3LocationProperty(
                        s3_bucket="s3Bucket",
                        s3_key="s3Key"
                    ),
                    timeout_in_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fbadbd783a1580f14d6c506c8516b0d678e06de949aceaf4cc00fafde6657c7f)
                check_type(argname="argument executable_parameters", value=executable_parameters, expected_type=type_hints["executable_parameters"])
                check_type(argname="argument executable_path", value=executable_path, expected_type=type_hints["executable_path"])
                check_type(argname="argument script_s3_location", value=script_s3_location, expected_type=type_hints["script_s3_location"])
                check_type(argname="argument timeout_in_seconds", value=timeout_in_seconds, expected_type=type_hints["timeout_in_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if executable_parameters is not None:
                self._values["executable_parameters"] = executable_parameters
            if executable_path is not None:
                self._values["executable_path"] = executable_path
            if script_s3_location is not None:
                self._values["script_s3_location"] = script_s3_location
            if timeout_in_seconds is not None:
                self._values["timeout_in_seconds"] = timeout_in_seconds

        @builtins.property
        def executable_parameters(self) -> typing.Optional[builtins.str]:
            '''The parameters used in the run path for the script.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-appblock-scriptdetails.html#cfn-appstream-appblock-scriptdetails-executableparameters
            '''
            result = self._values.get("executable_parameters")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def executable_path(self) -> typing.Optional[builtins.str]:
            '''The run path for the script.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-appblock-scriptdetails.html#cfn-appstream-appblock-scriptdetails-executablepath
            '''
            result = self._values.get("executable_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def script_s3_location(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppBlockPropsMixin.S3LocationProperty"]]:
            '''The S3 object location of the script.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-appblock-scriptdetails.html#cfn-appstream-appblock-scriptdetails-scripts3location
            '''
            result = self._values.get("script_s3_location")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppBlockPropsMixin.S3LocationProperty"]], result)

        @builtins.property
        def timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''The run timeout, in seconds, for the script.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-appblock-scriptdetails.html#cfn-appstream-appblock-scriptdetails-timeoutinseconds
            '''
            result = self._values.get("timeout_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScriptDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnApplicationEntitlementAssociationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_identifier": "applicationIdentifier",
        "entitlement_name": "entitlementName",
        "stack_name": "stackName",
    },
)
class CfnApplicationEntitlementAssociationMixinProps:
    def __init__(
        self,
        *,
        application_identifier: typing.Optional[builtins.str] = None,
        entitlement_name: typing.Optional[builtins.str] = None,
        stack_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnApplicationEntitlementAssociationPropsMixin.

        :param application_identifier: The identifier of the application.
        :param entitlement_name: The name of the entitlement.
        :param stack_name: The name of the stack.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-applicationentitlementassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
            
            cfn_application_entitlement_association_mixin_props = appstream_mixins.CfnApplicationEntitlementAssociationMixinProps(
                application_identifier="applicationIdentifier",
                entitlement_name="entitlementName",
                stack_name="stackName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__909d0dd63c8e2ae45d84e79fa0c090471fea06e20d4a889ef71cf8d843f82193)
            check_type(argname="argument application_identifier", value=application_identifier, expected_type=type_hints["application_identifier"])
            check_type(argname="argument entitlement_name", value=entitlement_name, expected_type=type_hints["entitlement_name"])
            check_type(argname="argument stack_name", value=stack_name, expected_type=type_hints["stack_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_identifier is not None:
            self._values["application_identifier"] = application_identifier
        if entitlement_name is not None:
            self._values["entitlement_name"] = entitlement_name
        if stack_name is not None:
            self._values["stack_name"] = stack_name

    @builtins.property
    def application_identifier(self) -> typing.Optional[builtins.str]:
        '''The identifier of the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-applicationentitlementassociation.html#cfn-appstream-applicationentitlementassociation-applicationidentifier
        '''
        result = self._values.get("application_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def entitlement_name(self) -> typing.Optional[builtins.str]:
        '''The name of the entitlement.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-applicationentitlementassociation.html#cfn-appstream-applicationentitlementassociation-entitlementname
        '''
        result = self._values.get("entitlement_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stack_name(self) -> typing.Optional[builtins.str]:
        '''The name of the stack.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-applicationentitlementassociation.html#cfn-appstream-applicationentitlementassociation-stackname
        '''
        result = self._values.get("stack_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationEntitlementAssociationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnApplicationEntitlementAssociationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnApplicationEntitlementAssociationPropsMixin",
):
    '''Associates an application to an entitlement.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-applicationentitlementassociation.html
    :cloudformationResource: AWS::AppStream::ApplicationEntitlementAssociation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
        
        cfn_application_entitlement_association_props_mixin = appstream_mixins.CfnApplicationEntitlementAssociationPropsMixin(appstream_mixins.CfnApplicationEntitlementAssociationMixinProps(
            application_identifier="applicationIdentifier",
            entitlement_name="entitlementName",
            stack_name="stackName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnApplicationEntitlementAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AppStream::ApplicationEntitlementAssociation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__add0f318bcb24299f040cfc70ef723fe520b79480eb205d1036ac2ede8706c96)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ce5cdc60718dd561ecbd56b331ae85836855a5154f3b78b61ec643c68cba27b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9421982fd69ddb1c49776fe989ba89b3bff021a79c7ec65cbbab6e4cd69a807)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnApplicationEntitlementAssociationMixinProps:
        return typing.cast(CfnApplicationEntitlementAssociationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnApplicationFleetAssociationMixinProps",
    jsii_struct_bases=[],
    name_mapping={"application_arn": "applicationArn", "fleet_name": "fleetName"},
)
class CfnApplicationFleetAssociationMixinProps:
    def __init__(
        self,
        *,
        application_arn: typing.Optional[builtins.str] = None,
        fleet_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnApplicationFleetAssociationPropsMixin.

        :param application_arn: The ARN of the application.
        :param fleet_name: The name of the fleet.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-applicationfleetassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
            
            cfn_application_fleet_association_mixin_props = appstream_mixins.CfnApplicationFleetAssociationMixinProps(
                application_arn="applicationArn",
                fleet_name="fleetName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__860ac7e6ddf61493f6085473ce2bfa66f302ef1d9536fc59d1516dbde7482710)
            check_type(argname="argument application_arn", value=application_arn, expected_type=type_hints["application_arn"])
            check_type(argname="argument fleet_name", value=fleet_name, expected_type=type_hints["fleet_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_arn is not None:
            self._values["application_arn"] = application_arn
        if fleet_name is not None:
            self._values["fleet_name"] = fleet_name

    @builtins.property
    def application_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-applicationfleetassociation.html#cfn-appstream-applicationfleetassociation-applicationarn
        '''
        result = self._values.get("application_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fleet_name(self) -> typing.Optional[builtins.str]:
        '''The name of the fleet.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-applicationfleetassociation.html#cfn-appstream-applicationfleetassociation-fleetname
        '''
        result = self._values.get("fleet_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationFleetAssociationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnApplicationFleetAssociationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnApplicationFleetAssociationPropsMixin",
):
    '''This resource associates the specified application with the specified fleet.

    This is only supported for Elastic fleets.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-applicationfleetassociation.html
    :cloudformationResource: AWS::AppStream::ApplicationFleetAssociation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
        
        cfn_application_fleet_association_props_mixin = appstream_mixins.CfnApplicationFleetAssociationPropsMixin(appstream_mixins.CfnApplicationFleetAssociationMixinProps(
            application_arn="applicationArn",
            fleet_name="fleetName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnApplicationFleetAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AppStream::ApplicationFleetAssociation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55de10d1f18dae7acbc4487a49198ae3feb80bb57d061145073b214c3bfc1ab2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__32c1c80097e34c5352429402eb45efd3b6cba3c0dd5c9dcc2a39f24656201818)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__177ae14003d8eaee59965ce5cb645a7943e99738c8d0e217a348a8101e1e3d01)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnApplicationFleetAssociationMixinProps:
        return typing.cast(CfnApplicationFleetAssociationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnApplicationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "app_block_arn": "appBlockArn",
        "attributes_to_delete": "attributesToDelete",
        "description": "description",
        "display_name": "displayName",
        "icon_s3_location": "iconS3Location",
        "instance_families": "instanceFamilies",
        "launch_parameters": "launchParameters",
        "launch_path": "launchPath",
        "name": "name",
        "platforms": "platforms",
        "tags": "tags",
        "working_directory": "workingDirectory",
    },
)
class CfnApplicationMixinProps:
    def __init__(
        self,
        *,
        app_block_arn: typing.Optional[builtins.str] = None,
        attributes_to_delete: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        icon_s3_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.S3LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        instance_families: typing.Optional[typing.Sequence[builtins.str]] = None,
        launch_parameters: typing.Optional[builtins.str] = None,
        launch_path: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        platforms: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        working_directory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnApplicationPropsMixin.

        :param app_block_arn: The app block ARN with which the application should be associated.
        :param attributes_to_delete: A list of attributes to delete from an application.
        :param description: The description of the application.
        :param display_name: The display name of the application. This name is visible to users in the application catalog.
        :param icon_s3_location: The icon S3 location of the application.
        :param instance_families: The instance families the application supports. *Allowed Values* : ``GENERAL_PURPOSE`` | ``GRAPHICS_G4``
        :param launch_parameters: The launch parameters of the application.
        :param launch_path: The launch path of the application.
        :param name: The name of the application. This name is visible to users when a name is not specified in the DisplayName property. *Pattern* : ``^[a-zA-Z0-9][a-zA-Z0-9_.-]{0,100}$``
        :param platforms: The platforms the application supports. *Allowed Values* : ``WINDOWS_SERVER_2019`` | ``AMAZON_LINUX2``
        :param tags: The tags of the application.
        :param working_directory: The working directory of the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-application.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
            
            cfn_application_mixin_props = appstream_mixins.CfnApplicationMixinProps(
                app_block_arn="appBlockArn",
                attributes_to_delete=["attributesToDelete"],
                description="description",
                display_name="displayName",
                icon_s3_location=appstream_mixins.CfnApplicationPropsMixin.S3LocationProperty(
                    s3_bucket="s3Bucket",
                    s3_key="s3Key"
                ),
                instance_families=["instanceFamilies"],
                launch_parameters="launchParameters",
                launch_path="launchPath",
                name="name",
                platforms=["platforms"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                working_directory="workingDirectory"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1da3bc4dd264b1d0f55a542896e88cc88b5628b2a306f6200770fec455462d44)
            check_type(argname="argument app_block_arn", value=app_block_arn, expected_type=type_hints["app_block_arn"])
            check_type(argname="argument attributes_to_delete", value=attributes_to_delete, expected_type=type_hints["attributes_to_delete"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument icon_s3_location", value=icon_s3_location, expected_type=type_hints["icon_s3_location"])
            check_type(argname="argument instance_families", value=instance_families, expected_type=type_hints["instance_families"])
            check_type(argname="argument launch_parameters", value=launch_parameters, expected_type=type_hints["launch_parameters"])
            check_type(argname="argument launch_path", value=launch_path, expected_type=type_hints["launch_path"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument platforms", value=platforms, expected_type=type_hints["platforms"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument working_directory", value=working_directory, expected_type=type_hints["working_directory"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if app_block_arn is not None:
            self._values["app_block_arn"] = app_block_arn
        if attributes_to_delete is not None:
            self._values["attributes_to_delete"] = attributes_to_delete
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if icon_s3_location is not None:
            self._values["icon_s3_location"] = icon_s3_location
        if instance_families is not None:
            self._values["instance_families"] = instance_families
        if launch_parameters is not None:
            self._values["launch_parameters"] = launch_parameters
        if launch_path is not None:
            self._values["launch_path"] = launch_path
        if name is not None:
            self._values["name"] = name
        if platforms is not None:
            self._values["platforms"] = platforms
        if tags is not None:
            self._values["tags"] = tags
        if working_directory is not None:
            self._values["working_directory"] = working_directory

    @builtins.property
    def app_block_arn(self) -> typing.Optional[builtins.str]:
        '''The app block ARN with which the application should be associated.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-application.html#cfn-appstream-application-appblockarn
        '''
        result = self._values.get("app_block_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def attributes_to_delete(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of attributes to delete from an application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-application.html#cfn-appstream-application-attributestodelete
        '''
        result = self._values.get("attributes_to_delete")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-application.html#cfn-appstream-application-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name of the application.

        This name is visible to users in the application catalog.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-application.html#cfn-appstream-application-displayname
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def icon_s3_location(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.S3LocationProperty"]]:
        '''The icon S3 location of the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-application.html#cfn-appstream-application-icons3location
        '''
        result = self._values.get("icon_s3_location")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.S3LocationProperty"]], result)

    @builtins.property
    def instance_families(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The instance families the application supports.

        *Allowed Values* : ``GENERAL_PURPOSE`` | ``GRAPHICS_G4``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-application.html#cfn-appstream-application-instancefamilies
        '''
        result = self._values.get("instance_families")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def launch_parameters(self) -> typing.Optional[builtins.str]:
        '''The launch parameters of the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-application.html#cfn-appstream-application-launchparameters
        '''
        result = self._values.get("launch_parameters")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def launch_path(self) -> typing.Optional[builtins.str]:
        '''The launch path of the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-application.html#cfn-appstream-application-launchpath
        '''
        result = self._values.get("launch_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the application.

        This name is visible to users when a name is not specified in the DisplayName property.

        *Pattern* : ``^[a-zA-Z0-9][a-zA-Z0-9_.-]{0,100}$``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-application.html#cfn-appstream-application-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def platforms(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The platforms the application supports.

        *Allowed Values* : ``WINDOWS_SERVER_2019`` | ``AMAZON_LINUX2``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-application.html#cfn-appstream-application-platforms
        '''
        result = self._values.get("platforms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags of the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-application.html#cfn-appstream-application-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def working_directory(self) -> typing.Optional[builtins.str]:
        '''The working directory of the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-application.html#cfn-appstream-application-workingdirectory
        '''
        result = self._values.get("working_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnApplicationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnApplicationPropsMixin",
):
    '''This resource creates an application.

    Applications store the details about how to launch applications on streaming instances. This is only supported for Elastic fleets.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-application.html
    :cloudformationResource: AWS::AppStream::Application
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
        
        cfn_application_props_mixin = appstream_mixins.CfnApplicationPropsMixin(appstream_mixins.CfnApplicationMixinProps(
            app_block_arn="appBlockArn",
            attributes_to_delete=["attributesToDelete"],
            description="description",
            display_name="displayName",
            icon_s3_location=appstream_mixins.CfnApplicationPropsMixin.S3LocationProperty(
                s3_bucket="s3Bucket",
                s3_key="s3Key"
            ),
            instance_families=["instanceFamilies"],
            launch_parameters="launchParameters",
            launch_path="launchPath",
            name="name",
            platforms=["platforms"],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            working_directory="workingDirectory"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnApplicationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AppStream::Application``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__405843b4bc61e754ab93e9f2fd179b65ef001932219b80037e7963a9de2ea72f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0796352dc6e35320ba983bf95f9e941812ce4c6671e85eb252daeda1af156a87)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ed5441a01aa97ef656ab6f146dd693f6cf37094046ee6c2f3d4745a53bc8ecd)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnApplicationMixinProps:
        return typing.cast(CfnApplicationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnApplicationPropsMixin.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_bucket": "s3Bucket", "s3_key": "s3Key"},
    )
    class S3LocationProperty:
        def __init__(
            self,
            *,
            s3_bucket: typing.Optional[builtins.str] = None,
            s3_key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The S3 location of the application icon.

            :param s3_bucket: The S3 bucket of the S3 object.
            :param s3_key: The S3 key of the S3 object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-application-s3location.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
                
                s3_location_property = appstream_mixins.CfnApplicationPropsMixin.S3LocationProperty(
                    s3_bucket="s3Bucket",
                    s3_key="s3Key"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4d1489105f9496ff5d1fbb605e34bc742bd8c17a67143b25c7b6494754748423)
                check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
                check_type(argname="argument s3_key", value=s3_key, expected_type=type_hints["s3_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3_bucket is not None:
                self._values["s3_bucket"] = s3_bucket
            if s3_key is not None:
                self._values["s3_key"] = s3_key

        @builtins.property
        def s3_bucket(self) -> typing.Optional[builtins.str]:
            '''The S3 bucket of the S3 object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-application-s3location.html#cfn-appstream-application-s3location-s3bucket
            '''
            result = self._values.get("s3_bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_key(self) -> typing.Optional[builtins.str]:
            '''The S3 key of the S3 object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-application-s3location.html#cfn-appstream-application-s3location-s3key
            '''
            result = self._values.get("s3_key")
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
    jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnDirectoryConfigMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_based_auth_properties": "certificateBasedAuthProperties",
        "directory_name": "directoryName",
        "organizational_unit_distinguished_names": "organizationalUnitDistinguishedNames",
        "service_account_credentials": "serviceAccountCredentials",
    },
)
class CfnDirectoryConfigMixinProps:
    def __init__(
        self,
        *,
        certificate_based_auth_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDirectoryConfigPropsMixin.CertificateBasedAuthPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        directory_name: typing.Optional[builtins.str] = None,
        organizational_unit_distinguished_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        service_account_credentials: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDirectoryConfigPropsMixin.ServiceAccountCredentialsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDirectoryConfigPropsMixin.

        :param certificate_based_auth_properties: The certificate-based authentication properties used to authenticate SAML 2.0 Identity Provider (IdP) user identities to Active Directory domain-joined streaming instances.
        :param directory_name: The fully qualified name of the directory (for example, corp.example.com).
        :param organizational_unit_distinguished_names: The distinguished names of the organizational units for computer accounts.
        :param service_account_credentials: The credentials for the service account used by the streaming instance to connect to the directory. Do not use this parameter directly. Use ``ServiceAccountCredentials`` as an input parameter with ``noEcho`` as shown in the `Parameters <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html>`_ . For best practices information, see `Do Not Embed Credentials in Your Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/best-practices.html#creds>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-directoryconfig.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
            
            cfn_directory_config_mixin_props = appstream_mixins.CfnDirectoryConfigMixinProps(
                certificate_based_auth_properties=appstream_mixins.CfnDirectoryConfigPropsMixin.CertificateBasedAuthPropertiesProperty(
                    certificate_authority_arn="certificateAuthorityArn",
                    status="status"
                ),
                directory_name="directoryName",
                organizational_unit_distinguished_names=["organizationalUnitDistinguishedNames"],
                service_account_credentials=appstream_mixins.CfnDirectoryConfigPropsMixin.ServiceAccountCredentialsProperty(
                    account_name="accountName",
                    account_password="accountPassword"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e4984c7c8ccd5c686d9f2759c297af96c1bba8ca306f3e93837e335d9831701)
            check_type(argname="argument certificate_based_auth_properties", value=certificate_based_auth_properties, expected_type=type_hints["certificate_based_auth_properties"])
            check_type(argname="argument directory_name", value=directory_name, expected_type=type_hints["directory_name"])
            check_type(argname="argument organizational_unit_distinguished_names", value=organizational_unit_distinguished_names, expected_type=type_hints["organizational_unit_distinguished_names"])
            check_type(argname="argument service_account_credentials", value=service_account_credentials, expected_type=type_hints["service_account_credentials"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if certificate_based_auth_properties is not None:
            self._values["certificate_based_auth_properties"] = certificate_based_auth_properties
        if directory_name is not None:
            self._values["directory_name"] = directory_name
        if organizational_unit_distinguished_names is not None:
            self._values["organizational_unit_distinguished_names"] = organizational_unit_distinguished_names
        if service_account_credentials is not None:
            self._values["service_account_credentials"] = service_account_credentials

    @builtins.property
    def certificate_based_auth_properties(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDirectoryConfigPropsMixin.CertificateBasedAuthPropertiesProperty"]]:
        '''The certificate-based authentication properties used to authenticate SAML 2.0 Identity Provider (IdP) user identities to Active Directory domain-joined streaming instances.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-directoryconfig.html#cfn-appstream-directoryconfig-certificatebasedauthproperties
        '''
        result = self._values.get("certificate_based_auth_properties")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDirectoryConfigPropsMixin.CertificateBasedAuthPropertiesProperty"]], result)

    @builtins.property
    def directory_name(self) -> typing.Optional[builtins.str]:
        '''The fully qualified name of the directory (for example, corp.example.com).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-directoryconfig.html#cfn-appstream-directoryconfig-directoryname
        '''
        result = self._values.get("directory_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def organizational_unit_distinguished_names(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''The distinguished names of the organizational units for computer accounts.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-directoryconfig.html#cfn-appstream-directoryconfig-organizationalunitdistinguishednames
        '''
        result = self._values.get("organizational_unit_distinguished_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def service_account_credentials(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDirectoryConfigPropsMixin.ServiceAccountCredentialsProperty"]]:
        '''The credentials for the service account used by the streaming instance to connect to the directory.

        Do not use this parameter directly. Use ``ServiceAccountCredentials`` as an input parameter with ``noEcho`` as shown in the `Parameters <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html>`_ . For best practices information, see `Do Not Embed Credentials in Your Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/best-practices.html#creds>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-directoryconfig.html#cfn-appstream-directoryconfig-serviceaccountcredentials
        '''
        result = self._values.get("service_account_credentials")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDirectoryConfigPropsMixin.ServiceAccountCredentialsProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDirectoryConfigMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDirectoryConfigPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnDirectoryConfigPropsMixin",
):
    '''The ``AWS::AppStream::DirectoryConfig`` resource specifies the configuration information required to join Amazon AppStream 2.0 fleets and image builders to Microsoft Active Directory domains.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-directoryconfig.html
    :cloudformationResource: AWS::AppStream::DirectoryConfig
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
        
        cfn_directory_config_props_mixin = appstream_mixins.CfnDirectoryConfigPropsMixin(appstream_mixins.CfnDirectoryConfigMixinProps(
            certificate_based_auth_properties=appstream_mixins.CfnDirectoryConfigPropsMixin.CertificateBasedAuthPropertiesProperty(
                certificate_authority_arn="certificateAuthorityArn",
                status="status"
            ),
            directory_name="directoryName",
            organizational_unit_distinguished_names=["organizationalUnitDistinguishedNames"],
            service_account_credentials=appstream_mixins.CfnDirectoryConfigPropsMixin.ServiceAccountCredentialsProperty(
                account_name="accountName",
                account_password="accountPassword"
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDirectoryConfigMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AppStream::DirectoryConfig``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bfcbc149e7522867e82149dce66808bce698a74906ecb7a9b6fc86965deaad7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e328e7f62f80432df375e768ea15b19c164c872b7e940201f44748cbf29c208)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5fae9e70de512ccd159d7ffe1deaa024f9aba9a58f6adb21892bc75a3ce001a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDirectoryConfigMixinProps:
        return typing.cast(CfnDirectoryConfigMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnDirectoryConfigPropsMixin.CertificateBasedAuthPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate_authority_arn": "certificateAuthorityArn",
            "status": "status",
        },
    )
    class CertificateBasedAuthPropertiesProperty:
        def __init__(
            self,
            *,
            certificate_authority_arn: typing.Optional[builtins.str] = None,
            status: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The certificate-based authentication properties used to authenticate SAML 2.0 Identity Provider (IdP) user identities to Active Directory domain-joined streaming instances.

            :param certificate_authority_arn: The ARN of the AWS Certificate Manager Private CA resource.
            :param status: The status of the certificate-based authentication properties. Fallback is turned on by default when certificate-based authentication is *Enabled* . Fallback allows users to log in using their AD domain password if certificate-based authentication is unsuccessful, or to unlock a desktop lock screen. *Enabled_no_directory_login_fallback* enables certificate-based authentication, but does not allow users to log in using their AD domain password. Users will be disconnected to re-authenticate using certificates.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-directoryconfig-certificatebasedauthproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
                
                certificate_based_auth_properties_property = appstream_mixins.CfnDirectoryConfigPropsMixin.CertificateBasedAuthPropertiesProperty(
                    certificate_authority_arn="certificateAuthorityArn",
                    status="status"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a757d8154f83ac5294f28b4d65804caf11afccd8c8c2dffba084c614db7c8064)
                check_type(argname="argument certificate_authority_arn", value=certificate_authority_arn, expected_type=type_hints["certificate_authority_arn"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate_authority_arn is not None:
                self._values["certificate_authority_arn"] = certificate_authority_arn
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def certificate_authority_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the AWS Certificate Manager Private CA resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-directoryconfig-certificatebasedauthproperties.html#cfn-appstream-directoryconfig-certificatebasedauthproperties-certificateauthorityarn
            '''
            result = self._values.get("certificate_authority_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''The status of the certificate-based authentication properties.

            Fallback is turned on by default when certificate-based authentication is *Enabled* . Fallback allows users to log in using their AD domain password if certificate-based authentication is unsuccessful, or to unlock a desktop lock screen. *Enabled_no_directory_login_fallback* enables certificate-based authentication, but does not allow users to log in using their AD domain password. Users will be disconnected to re-authenticate using certificates.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-directoryconfig-certificatebasedauthproperties.html#cfn-appstream-directoryconfig-certificatebasedauthproperties-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CertificateBasedAuthPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnDirectoryConfigPropsMixin.ServiceAccountCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "account_name": "accountName",
            "account_password": "accountPassword",
        },
    )
    class ServiceAccountCredentialsProperty:
        def __init__(
            self,
            *,
            account_name: typing.Optional[builtins.str] = None,
            account_password: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The credentials for the service account used by the streaming instance to connect to the directory.

            :param account_name: The user name of the account. This account must have the following privileges: create computer objects, join computers to the domain, and change/reset the password on descendant computer objects for the organizational units specified.
            :param account_password: The password for the account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-directoryconfig-serviceaccountcredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
                
                service_account_credentials_property = appstream_mixins.CfnDirectoryConfigPropsMixin.ServiceAccountCredentialsProperty(
                    account_name="accountName",
                    account_password="accountPassword"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__eeb2bc418dec631dd440af9730a4f760bdd1bfda8ae36345596767f1771f9e0b)
                check_type(argname="argument account_name", value=account_name, expected_type=type_hints["account_name"])
                check_type(argname="argument account_password", value=account_password, expected_type=type_hints["account_password"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if account_name is not None:
                self._values["account_name"] = account_name
            if account_password is not None:
                self._values["account_password"] = account_password

        @builtins.property
        def account_name(self) -> typing.Optional[builtins.str]:
            '''The user name of the account.

            This account must have the following privileges: create computer objects, join computers to the domain, and change/reset the password on descendant computer objects for the organizational units specified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-directoryconfig-serviceaccountcredentials.html#cfn-appstream-directoryconfig-serviceaccountcredentials-accountname
            '''
            result = self._values.get("account_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def account_password(self) -> typing.Optional[builtins.str]:
            '''The password for the account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-directoryconfig-serviceaccountcredentials.html#cfn-appstream-directoryconfig-serviceaccountcredentials-accountpassword
            '''
            result = self._values.get("account_password")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServiceAccountCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnEntitlementMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "app_visibility": "appVisibility",
        "attributes": "attributes",
        "description": "description",
        "name": "name",
        "stack_name": "stackName",
    },
)
class CfnEntitlementMixinProps:
    def __init__(
        self,
        *,
        app_visibility: typing.Optional[builtins.str] = None,
        attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEntitlementPropsMixin.AttributeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        stack_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnEntitlementPropsMixin.

        :param app_visibility: Specifies whether to entitle all apps or only selected apps.
        :param attributes: The attributes of the entitlement.
        :param description: The description of the entitlement.
        :param name: The name of the entitlement.
        :param stack_name: The name of the stack.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-entitlement.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
            
            cfn_entitlement_mixin_props = appstream_mixins.CfnEntitlementMixinProps(
                app_visibility="appVisibility",
                attributes=[appstream_mixins.CfnEntitlementPropsMixin.AttributeProperty(
                    name="name",
                    value="value"
                )],
                description="description",
                name="name",
                stack_name="stackName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bb5f8be7ce260eb862b0ba0880ce6dc54d38f3cd52455a74fc88d17e2305f49)
            check_type(argname="argument app_visibility", value=app_visibility, expected_type=type_hints["app_visibility"])
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument stack_name", value=stack_name, expected_type=type_hints["stack_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if app_visibility is not None:
            self._values["app_visibility"] = app_visibility
        if attributes is not None:
            self._values["attributes"] = attributes
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if stack_name is not None:
            self._values["stack_name"] = stack_name

    @builtins.property
    def app_visibility(self) -> typing.Optional[builtins.str]:
        '''Specifies whether to entitle all apps or only selected apps.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-entitlement.html#cfn-appstream-entitlement-appvisibility
        '''
        result = self._values.get("app_visibility")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def attributes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEntitlementPropsMixin.AttributeProperty"]]]]:
        '''The attributes of the entitlement.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-entitlement.html#cfn-appstream-entitlement-attributes
        '''
        result = self._values.get("attributes")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEntitlementPropsMixin.AttributeProperty"]]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the entitlement.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-entitlement.html#cfn-appstream-entitlement-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the entitlement.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-entitlement.html#cfn-appstream-entitlement-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stack_name(self) -> typing.Optional[builtins.str]:
        '''The name of the stack.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-entitlement.html#cfn-appstream-entitlement-stackname
        '''
        result = self._values.get("stack_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEntitlementMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnEntitlementPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnEntitlementPropsMixin",
):
    '''Creates an entitlement to control access, based on user attributes, to specific applications within a stack.

    Entitlements apply to SAML 2.0 federated user identities. Amazon AppStream 2.0 user pool and streaming URL users are entitled to all applications in a stack. Entitlements don't apply to the desktop stream view application or to applications managed by a dynamic app provider using the Dynamic Application Framework.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-entitlement.html
    :cloudformationResource: AWS::AppStream::Entitlement
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
        
        cfn_entitlement_props_mixin = appstream_mixins.CfnEntitlementPropsMixin(appstream_mixins.CfnEntitlementMixinProps(
            app_visibility="appVisibility",
            attributes=[appstream_mixins.CfnEntitlementPropsMixin.AttributeProperty(
                name="name",
                value="value"
            )],
            description="description",
            name="name",
            stack_name="stackName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnEntitlementMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AppStream::Entitlement``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19a8f5f22b027bf94b5c0d3f84ce0c2b5da915af58dce3a8bf9045742c8d763c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__32afee813dc85d9238c519012a43f87ba4e1b8237429df7af0dd3aa311e3359c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7c61193dc841c219b2921082b9c90682ccaeeba6149aa2c0176c1808d24e569)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnEntitlementMixinProps:
        return typing.cast(CfnEntitlementMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnEntitlementPropsMixin.AttributeProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class AttributeProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An attribute that belongs to an entitlement.

            Application entitlements work by matching a supported SAML 2.0 attribute name to a value when a user identity federates to an AppStream 2.0 SAML application.

            :param name: A supported AWS IAM SAML PrincipalTag attribute that is matched to a value when a user identity federates to an AppStream 2.0 SAML application. The following are supported values: - roles - department - organization - groups - title - costCenter - userType
            :param value: A value that is matched to a supported SAML attribute name when a user identity federates to an AppStream 2.0 SAML application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-entitlement-attribute.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
                
                attribute_property = appstream_mixins.CfnEntitlementPropsMixin.AttributeProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4ac5252bf4501eb0880b563afd03638ebfb571dc267811cf39e774b9213eda9c)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''A supported AWS IAM SAML PrincipalTag attribute that is matched to a value when a user identity federates to an AppStream 2.0 SAML application.

            The following are supported values:

            - roles
            - department
            - organization
            - groups
            - title
            - costCenter
            - userType

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-entitlement-attribute.html#cfn-appstream-entitlement-attribute-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''A value that is matched to a supported SAML attribute name when a user identity federates to an AppStream 2.0 SAML application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-entitlement-attribute.html#cfn-appstream-entitlement-attribute-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AttributeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnFleetMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "compute_capacity": "computeCapacity",
        "description": "description",
        "disconnect_timeout_in_seconds": "disconnectTimeoutInSeconds",
        "display_name": "displayName",
        "domain_join_info": "domainJoinInfo",
        "enable_default_internet_access": "enableDefaultInternetAccess",
        "fleet_type": "fleetType",
        "iam_role_arn": "iamRoleArn",
        "idle_disconnect_timeout_in_seconds": "idleDisconnectTimeoutInSeconds",
        "image_arn": "imageArn",
        "image_name": "imageName",
        "instance_type": "instanceType",
        "max_concurrent_sessions": "maxConcurrentSessions",
        "max_sessions_per_instance": "maxSessionsPerInstance",
        "max_user_duration_in_seconds": "maxUserDurationInSeconds",
        "name": "name",
        "platform": "platform",
        "root_volume_config": "rootVolumeConfig",
        "session_script_s3_location": "sessionScriptS3Location",
        "stream_view": "streamView",
        "tags": "tags",
        "usb_device_filter_strings": "usbDeviceFilterStrings",
        "vpc_config": "vpcConfig",
    },
)
class CfnFleetMixinProps:
    def __init__(
        self,
        *,
        compute_capacity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFleetPropsMixin.ComputeCapacityProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        disconnect_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        display_name: typing.Optional[builtins.str] = None,
        domain_join_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFleetPropsMixin.DomainJoinInfoProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        enable_default_internet_access: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        fleet_type: typing.Optional[builtins.str] = None,
        iam_role_arn: typing.Optional[builtins.str] = None,
        idle_disconnect_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        image_arn: typing.Optional[builtins.str] = None,
        image_name: typing.Optional[builtins.str] = None,
        instance_type: typing.Optional[builtins.str] = None,
        max_concurrent_sessions: typing.Optional[jsii.Number] = None,
        max_sessions_per_instance: typing.Optional[jsii.Number] = None,
        max_user_duration_in_seconds: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        platform: typing.Optional[builtins.str] = None,
        root_volume_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFleetPropsMixin.VolumeConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        session_script_s3_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFleetPropsMixin.S3LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        stream_view: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        usb_device_filter_strings: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpc_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFleetPropsMixin.VpcConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnFleetPropsMixin.

        :param compute_capacity: The desired capacity for the fleet. This is not allowed for Elastic fleets.
        :param description: The description to display.
        :param disconnect_timeout_in_seconds: The amount of time that a streaming session remains active after users disconnect. If users try to reconnect to the streaming session after a disconnection or network interruption within this time interval, they are connected to their previous session. Otherwise, they are connected to a new session with a new streaming instance. Specify a value between 60 and 36000.
        :param display_name: The fleet name to display.
        :param domain_join_info: The name of the directory and organizational unit (OU) to use to join the fleet to a Microsoft Active Directory domain. This is not allowed for Elastic fleets.
        :param enable_default_internet_access: Enables or disables default internet access for the fleet.
        :param fleet_type: The fleet type. - **ALWAYS_ON** - Provides users with instant-on access to their apps. You are charged for all running instances in your fleet, even if no users are streaming apps. - **ON_DEMAND** - Provide users with access to applications after they connect, which takes one to two minutes. You are charged for instance streaming when users are connected and a small hourly fee for instances that are not streaming apps. - **ELASTIC** - The pool of streaming instances is managed by Amazon AppStream 2.0. When a user selects their application or desktop to launch, they will start streaming after the app block has been downloaded and mounted to a streaming instance. *Allowed Values* : ``ALWAYS_ON`` | ``ELASTIC`` | ``ON_DEMAND``
        :param iam_role_arn: The ARN of the IAM role that is applied to the fleet. To assume a role, the fleet instance calls the AWS Security Token Service ``AssumeRole`` API operation and passes the ARN of the role to use. The operation creates a new session with temporary credentials. AppStream 2.0 retrieves the temporary credentials and creates the *appstream_machine_role* credential profile on the instance. For more information, see `Using an IAM Role to Grant Permissions to Applications and Scripts Running on AppStream 2.0 Streaming Instances <https://docs.aws.amazon.com/appstream2/latest/developerguide/using-iam-roles-to-grant-permissions-to-applications-scripts-streaming-instances.html>`_ in the *Amazon AppStream 2.0 Administration Guide* .
        :param idle_disconnect_timeout_in_seconds: The amount of time that users can be idle (inactive) before they are disconnected from their streaming session and the ``DisconnectTimeoutInSeconds`` time interval begins. Users are notified before they are disconnected due to inactivity. If they try to reconnect to the streaming session before the time interval specified in ``DisconnectTimeoutInSeconds`` elapses, they are connected to their previous session. Users are considered idle when they stop providing keyboard or mouse input during their streaming session. File uploads and downloads, audio in, audio out, and pixels changing do not qualify as user activity. If users continue to be idle after the time interval in ``IdleDisconnectTimeoutInSeconds`` elapses, they are disconnected. To prevent users from being disconnected due to inactivity, specify a value of 0. Otherwise, specify a value between 60 and 36000. If you enable this feature, we recommend that you specify a value that corresponds exactly to a whole number of minutes (for example, 60, 120, and 180). If you don't do this, the value is rounded to the nearest minute. For example, if you specify a value of 70, users are disconnected after 1 minute of inactivity. If you specify a value that is at the midpoint between two different minutes, the value is rounded up. For example, if you specify a value of 90, users are disconnected after 2 minutes of inactivity.
        :param image_arn: The ARN of the public, private, or shared image to use.
        :param image_name: The name of the image used to create the fleet.
        :param instance_type: The instance type to use when launching fleet instances. The following instance types are available for non-Elastic fleets:. - stream.standard.small - stream.standard.medium - stream.standard.large - stream.compute.large - stream.compute.xlarge - stream.compute.2xlarge - stream.compute.4xlarge - stream.compute.8xlarge - stream.memory.large - stream.memory.xlarge - stream.memory.2xlarge - stream.memory.4xlarge - stream.memory.8xlarge - stream.memory.z1d.large - stream.memory.z1d.xlarge - stream.memory.z1d.2xlarge - stream.memory.z1d.3xlarge - stream.memory.z1d.6xlarge - stream.memory.z1d.12xlarge - stream.graphics-design.large - stream.graphics-design.xlarge - stream.graphics-design.2xlarge - stream.graphics-design.4xlarge - stream.graphics.g4dn.xlarge - stream.graphics.g4dn.2xlarge - stream.graphics.g4dn.4xlarge - stream.graphics.g4dn.8xlarge - stream.graphics.g4dn.12xlarge - stream.graphics.g4dn.16xlarge - stream.graphics.g5.xlarge - stream.graphics.g5.2xlarge - stream.graphics.g5.4xlarge - stream.graphics.g5.8xlarge - stream.graphics.g5.16xlarge - stream.graphics.g5.12xlarge - stream.graphics.g5.24xlarge - stream.graphics.g6.xlarge - stream.graphics.g6.2xlarge - stream.graphics.g6.4xlarge - stream.graphics.g6.8xlarge - stream.graphics.g6.16xlarge - stream.graphics.g6.12xlarge - stream.graphics.g6.24xlarge - stream.graphics.gr6.4xlarge - stream.graphics.gr6.8xlarge - stream.graphics.g6f.large - stream.graphics.g6f.xlarge - stream.graphics.g6f.2xlarge - stream.graphics.g6f.4xlarge - stream.graphics.gr6f.4xlarge The following instance types are available for Elastic fleets: - stream.standard.small - stream.standard.medium
        :param max_concurrent_sessions: The maximum number of concurrent sessions that can be run on an Elastic fleet. This setting is required for Elastic fleets, but is not used for other fleet types.
        :param max_sessions_per_instance: Max number of user sessions on an instance. This is applicable only for multi-session fleets.
        :param max_user_duration_in_seconds: The maximum amount of time that a streaming session can remain active, in seconds. If users are still connected to a streaming instance five minutes before this limit is reached, they are prompted to save any open documents before being disconnected. After this time elapses, the instance is terminated and replaced by a new instance. Specify a value between 600 and 432000.
        :param name: A unique name for the fleet.
        :param platform: The platform of the fleet. Platform is a required setting for Elastic fleets, and is not used for other fleet types.
        :param root_volume_config: 
        :param session_script_s3_location: The S3 location of the session scripts configuration zip file. This only applies to Elastic fleets.
        :param stream_view: The WorkSpaces Applications view that is displayed to your users when they stream from the fleet. When ``APP`` is specified, only the windows of applications opened by users display. When ``DESKTOP`` is specified, the standard desktop that is provided by the operating system displays. The default value is ``APP`` .
        :param tags: An array of key-value pairs.
        :param usb_device_filter_strings: The USB device filter strings that specify which USB devices a user can redirect to the fleet streaming session, when using the Windows native client. This is allowed but not required for Elastic fleets.
        :param vpc_config: The VPC configuration for the fleet. This is required for Elastic fleets, but not required for other fleet types.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
            
            cfn_fleet_mixin_props = appstream_mixins.CfnFleetMixinProps(
                compute_capacity=appstream_mixins.CfnFleetPropsMixin.ComputeCapacityProperty(
                    desired_instances=123,
                    desired_sessions=123
                ),
                description="description",
                disconnect_timeout_in_seconds=123,
                display_name="displayName",
                domain_join_info=appstream_mixins.CfnFleetPropsMixin.DomainJoinInfoProperty(
                    directory_name="directoryName",
                    organizational_unit_distinguished_name="organizationalUnitDistinguishedName"
                ),
                enable_default_internet_access=False,
                fleet_type="fleetType",
                iam_role_arn="iamRoleArn",
                idle_disconnect_timeout_in_seconds=123,
                image_arn="imageArn",
                image_name="imageName",
                instance_type="instanceType",
                max_concurrent_sessions=123,
                max_sessions_per_instance=123,
                max_user_duration_in_seconds=123,
                name="name",
                platform="platform",
                root_volume_config=appstream_mixins.CfnFleetPropsMixin.VolumeConfigProperty(
                    volume_size_in_gb=123
                ),
                session_script_s3_location=appstream_mixins.CfnFleetPropsMixin.S3LocationProperty(
                    s3_bucket="s3Bucket",
                    s3_key="s3Key"
                ),
                stream_view="streamView",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                usb_device_filter_strings=["usbDeviceFilterStrings"],
                vpc_config=appstream_mixins.CfnFleetPropsMixin.VpcConfigProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c470bfc842df5c5f11a47c5060c3483498eb2c208a8d80b0d68e81416ca3ea6b)
            check_type(argname="argument compute_capacity", value=compute_capacity, expected_type=type_hints["compute_capacity"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disconnect_timeout_in_seconds", value=disconnect_timeout_in_seconds, expected_type=type_hints["disconnect_timeout_in_seconds"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument domain_join_info", value=domain_join_info, expected_type=type_hints["domain_join_info"])
            check_type(argname="argument enable_default_internet_access", value=enable_default_internet_access, expected_type=type_hints["enable_default_internet_access"])
            check_type(argname="argument fleet_type", value=fleet_type, expected_type=type_hints["fleet_type"])
            check_type(argname="argument iam_role_arn", value=iam_role_arn, expected_type=type_hints["iam_role_arn"])
            check_type(argname="argument idle_disconnect_timeout_in_seconds", value=idle_disconnect_timeout_in_seconds, expected_type=type_hints["idle_disconnect_timeout_in_seconds"])
            check_type(argname="argument image_arn", value=image_arn, expected_type=type_hints["image_arn"])
            check_type(argname="argument image_name", value=image_name, expected_type=type_hints["image_name"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument max_concurrent_sessions", value=max_concurrent_sessions, expected_type=type_hints["max_concurrent_sessions"])
            check_type(argname="argument max_sessions_per_instance", value=max_sessions_per_instance, expected_type=type_hints["max_sessions_per_instance"])
            check_type(argname="argument max_user_duration_in_seconds", value=max_user_duration_in_seconds, expected_type=type_hints["max_user_duration_in_seconds"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
            check_type(argname="argument root_volume_config", value=root_volume_config, expected_type=type_hints["root_volume_config"])
            check_type(argname="argument session_script_s3_location", value=session_script_s3_location, expected_type=type_hints["session_script_s3_location"])
            check_type(argname="argument stream_view", value=stream_view, expected_type=type_hints["stream_view"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument usb_device_filter_strings", value=usb_device_filter_strings, expected_type=type_hints["usb_device_filter_strings"])
            check_type(argname="argument vpc_config", value=vpc_config, expected_type=type_hints["vpc_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if compute_capacity is not None:
            self._values["compute_capacity"] = compute_capacity
        if description is not None:
            self._values["description"] = description
        if disconnect_timeout_in_seconds is not None:
            self._values["disconnect_timeout_in_seconds"] = disconnect_timeout_in_seconds
        if display_name is not None:
            self._values["display_name"] = display_name
        if domain_join_info is not None:
            self._values["domain_join_info"] = domain_join_info
        if enable_default_internet_access is not None:
            self._values["enable_default_internet_access"] = enable_default_internet_access
        if fleet_type is not None:
            self._values["fleet_type"] = fleet_type
        if iam_role_arn is not None:
            self._values["iam_role_arn"] = iam_role_arn
        if idle_disconnect_timeout_in_seconds is not None:
            self._values["idle_disconnect_timeout_in_seconds"] = idle_disconnect_timeout_in_seconds
        if image_arn is not None:
            self._values["image_arn"] = image_arn
        if image_name is not None:
            self._values["image_name"] = image_name
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if max_concurrent_sessions is not None:
            self._values["max_concurrent_sessions"] = max_concurrent_sessions
        if max_sessions_per_instance is not None:
            self._values["max_sessions_per_instance"] = max_sessions_per_instance
        if max_user_duration_in_seconds is not None:
            self._values["max_user_duration_in_seconds"] = max_user_duration_in_seconds
        if name is not None:
            self._values["name"] = name
        if platform is not None:
            self._values["platform"] = platform
        if root_volume_config is not None:
            self._values["root_volume_config"] = root_volume_config
        if session_script_s3_location is not None:
            self._values["session_script_s3_location"] = session_script_s3_location
        if stream_view is not None:
            self._values["stream_view"] = stream_view
        if tags is not None:
            self._values["tags"] = tags
        if usb_device_filter_strings is not None:
            self._values["usb_device_filter_strings"] = usb_device_filter_strings
        if vpc_config is not None:
            self._values["vpc_config"] = vpc_config

    @builtins.property
    def compute_capacity(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.ComputeCapacityProperty"]]:
        '''The desired capacity for the fleet.

        This is not allowed for Elastic fleets.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-computecapacity
        '''
        result = self._values.get("compute_capacity")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.ComputeCapacityProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description to display.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disconnect_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''The amount of time that a streaming session remains active after users disconnect.

        If users try to reconnect to the streaming session after a disconnection or network interruption within this time interval, they are connected to their previous session. Otherwise, they are connected to a new session with a new streaming instance.

        Specify a value between 60 and 36000.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-disconnecttimeoutinseconds
        '''
        result = self._values.get("disconnect_timeout_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The fleet name to display.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-displayname
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_join_info(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.DomainJoinInfoProperty"]]:
        '''The name of the directory and organizational unit (OU) to use to join the fleet to a Microsoft Active Directory domain.

        This is not allowed for Elastic fleets.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-domainjoininfo
        '''
        result = self._values.get("domain_join_info")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.DomainJoinInfoProperty"]], result)

    @builtins.property
    def enable_default_internet_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Enables or disables default internet access for the fleet.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-enabledefaultinternetaccess
        '''
        result = self._values.get("enable_default_internet_access")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def fleet_type(self) -> typing.Optional[builtins.str]:
        '''The fleet type.

        - **ALWAYS_ON** - Provides users with instant-on access to their apps. You are charged for all running instances in your fleet, even if no users are streaming apps.
        - **ON_DEMAND** - Provide users with access to applications after they connect, which takes one to two minutes. You are charged for instance streaming when users are connected and a small hourly fee for instances that are not streaming apps.
        - **ELASTIC** - The pool of streaming instances is managed by Amazon AppStream 2.0. When a user selects their application or desktop to launch, they will start streaming after the app block has been downloaded and mounted to a streaming instance.

        *Allowed Values* : ``ALWAYS_ON`` | ``ELASTIC`` | ``ON_DEMAND``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-fleettype
        '''
        result = self._values.get("fleet_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iam_role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the IAM role that is applied to the fleet.

        To assume a role, the fleet instance calls the AWS Security Token Service ``AssumeRole`` API operation and passes the ARN of the role to use. The operation creates a new session with temporary credentials. AppStream 2.0 retrieves the temporary credentials and creates the *appstream_machine_role* credential profile on the instance.

        For more information, see `Using an IAM Role to Grant Permissions to Applications and Scripts Running on AppStream 2.0 Streaming Instances <https://docs.aws.amazon.com/appstream2/latest/developerguide/using-iam-roles-to-grant-permissions-to-applications-scripts-streaming-instances.html>`_ in the *Amazon AppStream 2.0 Administration Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-iamrolearn
        '''
        result = self._values.get("iam_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def idle_disconnect_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''The amount of time that users can be idle (inactive) before they are disconnected from their streaming session and the ``DisconnectTimeoutInSeconds`` time interval begins.

        Users are notified before they are disconnected due to inactivity. If they try to reconnect to the streaming session before the time interval specified in ``DisconnectTimeoutInSeconds`` elapses, they are connected to their previous session. Users are considered idle when they stop providing keyboard or mouse input during their streaming session. File uploads and downloads, audio in, audio out, and pixels changing do not qualify as user activity. If users continue to be idle after the time interval in ``IdleDisconnectTimeoutInSeconds`` elapses, they are disconnected.

        To prevent users from being disconnected due to inactivity, specify a value of 0. Otherwise, specify a value between 60 and 36000.

        If you enable this feature, we recommend that you specify a value that corresponds exactly to a whole number of minutes (for example, 60, 120, and 180). If you don't do this, the value is rounded to the nearest minute. For example, if you specify a value of 70, users are disconnected after 1 minute of inactivity. If you specify a value that is at the midpoint between two different minutes, the value is rounded up. For example, if you specify a value of 90, users are disconnected after 2 minutes of inactivity.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-idledisconnecttimeoutinseconds
        '''
        result = self._values.get("idle_disconnect_timeout_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def image_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the public, private, or shared image to use.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-imagearn
        '''
        result = self._values.get("image_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_name(self) -> typing.Optional[builtins.str]:
        '''The name of the image used to create the fleet.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-imagename
        '''
        result = self._values.get("image_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[builtins.str]:
        '''The instance type to use when launching fleet instances. The following instance types are available for non-Elastic fleets:.

        - stream.standard.small
        - stream.standard.medium
        - stream.standard.large
        - stream.compute.large
        - stream.compute.xlarge
        - stream.compute.2xlarge
        - stream.compute.4xlarge
        - stream.compute.8xlarge
        - stream.memory.large
        - stream.memory.xlarge
        - stream.memory.2xlarge
        - stream.memory.4xlarge
        - stream.memory.8xlarge
        - stream.memory.z1d.large
        - stream.memory.z1d.xlarge
        - stream.memory.z1d.2xlarge
        - stream.memory.z1d.3xlarge
        - stream.memory.z1d.6xlarge
        - stream.memory.z1d.12xlarge
        - stream.graphics-design.large
        - stream.graphics-design.xlarge
        - stream.graphics-design.2xlarge
        - stream.graphics-design.4xlarge
        - stream.graphics.g4dn.xlarge
        - stream.graphics.g4dn.2xlarge
        - stream.graphics.g4dn.4xlarge
        - stream.graphics.g4dn.8xlarge
        - stream.graphics.g4dn.12xlarge
        - stream.graphics.g4dn.16xlarge
        - stream.graphics.g5.xlarge
        - stream.graphics.g5.2xlarge
        - stream.graphics.g5.4xlarge
        - stream.graphics.g5.8xlarge
        - stream.graphics.g5.16xlarge
        - stream.graphics.g5.12xlarge
        - stream.graphics.g5.24xlarge
        - stream.graphics.g6.xlarge
        - stream.graphics.g6.2xlarge
        - stream.graphics.g6.4xlarge
        - stream.graphics.g6.8xlarge
        - stream.graphics.g6.16xlarge
        - stream.graphics.g6.12xlarge
        - stream.graphics.g6.24xlarge
        - stream.graphics.gr6.4xlarge
        - stream.graphics.gr6.8xlarge
        - stream.graphics.g6f.large
        - stream.graphics.g6f.xlarge
        - stream.graphics.g6f.2xlarge
        - stream.graphics.g6f.4xlarge
        - stream.graphics.gr6f.4xlarge

        The following instance types are available for Elastic fleets:

        - stream.standard.small
        - stream.standard.medium

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-instancetype
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_concurrent_sessions(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of concurrent sessions that can be run on an Elastic fleet.

        This setting is required for Elastic fleets, but is not used for other fleet types.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-maxconcurrentsessions
        '''
        result = self._values.get("max_concurrent_sessions")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_sessions_per_instance(self) -> typing.Optional[jsii.Number]:
        '''Max number of user sessions on an instance.

        This is applicable only for multi-session fleets.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-maxsessionsperinstance
        '''
        result = self._values.get("max_sessions_per_instance")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_user_duration_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''The maximum amount of time that a streaming session can remain active, in seconds.

        If users are still connected to a streaming instance five minutes before this limit is reached, they are prompted to save any open documents before being disconnected. After this time elapses, the instance is terminated and replaced by a new instance.

        Specify a value between 600 and 432000.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-maxuserdurationinseconds
        '''
        result = self._values.get("max_user_duration_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A unique name for the fleet.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def platform(self) -> typing.Optional[builtins.str]:
        '''The platform of the fleet.

        Platform is a required setting for Elastic fleets, and is not used for other fleet types.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-platform
        '''
        result = self._values.get("platform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def root_volume_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.VolumeConfigProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-rootvolumeconfig
        '''
        result = self._values.get("root_volume_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.VolumeConfigProperty"]], result)

    @builtins.property
    def session_script_s3_location(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.S3LocationProperty"]]:
        '''The S3 location of the session scripts configuration zip file.

        This only applies to Elastic fleets.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-sessionscripts3location
        '''
        result = self._values.get("session_script_s3_location")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.S3LocationProperty"]], result)

    @builtins.property
    def stream_view(self) -> typing.Optional[builtins.str]:
        '''The WorkSpaces Applications view that is displayed to your users when they stream from the fleet.

        When ``APP`` is specified, only the windows of applications opened by users display. When ``DESKTOP`` is specified, the standard desktop that is provided by the operating system displays.

        The default value is ``APP`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-streamview
        '''
        result = self._values.get("stream_view")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def usb_device_filter_strings(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The USB device filter strings that specify which USB devices a user can redirect to the fleet streaming session, when using the Windows native client.

        This is allowed but not required for Elastic fleets.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-usbdevicefilterstrings
        '''
        result = self._values.get("usb_device_filter_strings")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def vpc_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.VpcConfigProperty"]]:
        '''The VPC configuration for the fleet.

        This is required for Elastic fleets, but not required for other fleet types.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-vpcconfig
        '''
        result = self._values.get("vpc_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.VpcConfigProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFleetMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnFleetPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnFleetPropsMixin",
):
    '''The ``AWS::AppStream::Fleet`` resource creates a fleet for Amazon AppStream 2.0. A fleet consists of streaming instances that run a specified image when using Always-On or On-Demand.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html
    :cloudformationResource: AWS::AppStream::Fleet
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
        
        cfn_fleet_props_mixin = appstream_mixins.CfnFleetPropsMixin(appstream_mixins.CfnFleetMixinProps(
            compute_capacity=appstream_mixins.CfnFleetPropsMixin.ComputeCapacityProperty(
                desired_instances=123,
                desired_sessions=123
            ),
            description="description",
            disconnect_timeout_in_seconds=123,
            display_name="displayName",
            domain_join_info=appstream_mixins.CfnFleetPropsMixin.DomainJoinInfoProperty(
                directory_name="directoryName",
                organizational_unit_distinguished_name="organizationalUnitDistinguishedName"
            ),
            enable_default_internet_access=False,
            fleet_type="fleetType",
            iam_role_arn="iamRoleArn",
            idle_disconnect_timeout_in_seconds=123,
            image_arn="imageArn",
            image_name="imageName",
            instance_type="instanceType",
            max_concurrent_sessions=123,
            max_sessions_per_instance=123,
            max_user_duration_in_seconds=123,
            name="name",
            platform="platform",
            root_volume_config=appstream_mixins.CfnFleetPropsMixin.VolumeConfigProperty(
                volume_size_in_gb=123
            ),
            session_script_s3_location=appstream_mixins.CfnFleetPropsMixin.S3LocationProperty(
                s3_bucket="s3Bucket",
                s3_key="s3Key"
            ),
            stream_view="streamView",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            usb_device_filter_strings=["usbDeviceFilterStrings"],
            vpc_config=appstream_mixins.CfnFleetPropsMixin.VpcConfigProperty(
                security_group_ids=["securityGroupIds"],
                subnet_ids=["subnetIds"]
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnFleetMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AppStream::Fleet``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ac40daef75c5d4050ff01631c874cb064b94c4efeb106057e98a35d5c48e2b9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab8e9b104696da0d10b0171cdfd24172a1c3badbb6a78ebd60f1af851b077107)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__649336311ed24a2dfdc65f192a8ec7c8badb380aa7f6cf4233c9de491f0e19c7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnFleetMixinProps:
        return typing.cast(CfnFleetMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnFleetPropsMixin.ComputeCapacityProperty",
        jsii_struct_bases=[],
        name_mapping={
            "desired_instances": "desiredInstances",
            "desired_sessions": "desiredSessions",
        },
    )
    class ComputeCapacityProperty:
        def __init__(
            self,
            *,
            desired_instances: typing.Optional[jsii.Number] = None,
            desired_sessions: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The desired capacity for a fleet.

            :param desired_instances: The desired number of streaming instances.
            :param desired_sessions: The desired capacity in terms of number of user sessions, for the multi-session fleet. This is not allowed for single-session fleets. When you create a fleet, you must set define either the DesiredSessions or DesiredInstances attribute, based on the type of fleet you create. You can’t define both attributes or leave both attributes blank.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-fleet-computecapacity.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
                
                compute_capacity_property = appstream_mixins.CfnFleetPropsMixin.ComputeCapacityProperty(
                    desired_instances=123,
                    desired_sessions=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__57ca039cb516bc13df6cf163a4cf70b71f8670da28428574faea23a4e78c2a00)
                check_type(argname="argument desired_instances", value=desired_instances, expected_type=type_hints["desired_instances"])
                check_type(argname="argument desired_sessions", value=desired_sessions, expected_type=type_hints["desired_sessions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if desired_instances is not None:
                self._values["desired_instances"] = desired_instances
            if desired_sessions is not None:
                self._values["desired_sessions"] = desired_sessions

        @builtins.property
        def desired_instances(self) -> typing.Optional[jsii.Number]:
            '''The desired number of streaming instances.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-fleet-computecapacity.html#cfn-appstream-fleet-computecapacity-desiredinstances
            '''
            result = self._values.get("desired_instances")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def desired_sessions(self) -> typing.Optional[jsii.Number]:
            '''The desired capacity in terms of number of user sessions, for the multi-session fleet.

            This is not allowed for single-session fleets.

            When you create a fleet, you must set define either the DesiredSessions or DesiredInstances attribute, based on the type of fleet you create. You can’t define both attributes or leave both attributes blank.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-fleet-computecapacity.html#cfn-appstream-fleet-computecapacity-desiredsessions
            '''
            result = self._values.get("desired_sessions")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComputeCapacityProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnFleetPropsMixin.DomainJoinInfoProperty",
        jsii_struct_bases=[],
        name_mapping={
            "directory_name": "directoryName",
            "organizational_unit_distinguished_name": "organizationalUnitDistinguishedName",
        },
    )
    class DomainJoinInfoProperty:
        def __init__(
            self,
            *,
            directory_name: typing.Optional[builtins.str] = None,
            organizational_unit_distinguished_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The name of the directory and organizational unit (OU) to use to join a fleet to a Microsoft Active Directory domain.

            :param directory_name: The fully qualified name of the directory (for example, corp.example.com).
            :param organizational_unit_distinguished_name: The distinguished name of the organizational unit for computer accounts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-fleet-domainjoininfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
                
                domain_join_info_property = appstream_mixins.CfnFleetPropsMixin.DomainJoinInfoProperty(
                    directory_name="directoryName",
                    organizational_unit_distinguished_name="organizationalUnitDistinguishedName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__49807a51ac206f3c1c9f7293383e1a0c7f8acb9cab90ab1b0ed3b6f008167656)
                check_type(argname="argument directory_name", value=directory_name, expected_type=type_hints["directory_name"])
                check_type(argname="argument organizational_unit_distinguished_name", value=organizational_unit_distinguished_name, expected_type=type_hints["organizational_unit_distinguished_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if directory_name is not None:
                self._values["directory_name"] = directory_name
            if organizational_unit_distinguished_name is not None:
                self._values["organizational_unit_distinguished_name"] = organizational_unit_distinguished_name

        @builtins.property
        def directory_name(self) -> typing.Optional[builtins.str]:
            '''The fully qualified name of the directory (for example, corp.example.com).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-fleet-domainjoininfo.html#cfn-appstream-fleet-domainjoininfo-directoryname
            '''
            result = self._values.get("directory_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def organizational_unit_distinguished_name(
            self,
        ) -> typing.Optional[builtins.str]:
            '''The distinguished name of the organizational unit for computer accounts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-fleet-domainjoininfo.html#cfn-appstream-fleet-domainjoininfo-organizationalunitdistinguishedname
            '''
            result = self._values.get("organizational_unit_distinguished_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DomainJoinInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnFleetPropsMixin.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_bucket": "s3Bucket", "s3_key": "s3Key"},
    )
    class S3LocationProperty:
        def __init__(
            self,
            *,
            s3_bucket: typing.Optional[builtins.str] = None,
            s3_key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the S3 location.

            :param s3_bucket: The S3 bucket of the S3 object.
            :param s3_key: The S3 key of the S3 object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-fleet-s3location.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
                
                s3_location_property = appstream_mixins.CfnFleetPropsMixin.S3LocationProperty(
                    s3_bucket="s3Bucket",
                    s3_key="s3Key"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cbfdac7c844b13a4d0a878b6859efe346be40d4898e5b0abf7fb096a532a5ded)
                check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
                check_type(argname="argument s3_key", value=s3_key, expected_type=type_hints["s3_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3_bucket is not None:
                self._values["s3_bucket"] = s3_bucket
            if s3_key is not None:
                self._values["s3_key"] = s3_key

        @builtins.property
        def s3_bucket(self) -> typing.Optional[builtins.str]:
            '''The S3 bucket of the S3 object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-fleet-s3location.html#cfn-appstream-fleet-s3location-s3bucket
            '''
            result = self._values.get("s3_bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_key(self) -> typing.Optional[builtins.str]:
            '''The S3 key of the S3 object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-fleet-s3location.html#cfn-appstream-fleet-s3location-s3key
            '''
            result = self._values.get("s3_key")
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
        jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnFleetPropsMixin.VolumeConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"volume_size_in_gb": "volumeSizeInGb"},
    )
    class VolumeConfigProperty:
        def __init__(
            self,
            *,
            volume_size_in_gb: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param volume_size_in_gb: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-fleet-volumeconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
                
                volume_config_property = appstream_mixins.CfnFleetPropsMixin.VolumeConfigProperty(
                    volume_size_in_gb=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c92a1e162a8fca19844bfb04d4b0b38503ab5d758d8c9a55097487f917bb1d0c)
                check_type(argname="argument volume_size_in_gb", value=volume_size_in_gb, expected_type=type_hints["volume_size_in_gb"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if volume_size_in_gb is not None:
                self._values["volume_size_in_gb"] = volume_size_in_gb

        @builtins.property
        def volume_size_in_gb(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-fleet-volumeconfig.html#cfn-appstream-fleet-volumeconfig-volumesizeingb
            '''
            result = self._values.get("volume_size_in_gb")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VolumeConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnFleetPropsMixin.VpcConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
        },
    )
    class VpcConfigProperty:
        def __init__(
            self,
            *,
            security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The VPC configuration information for the fleet.

            :param security_group_ids: The identifiers of the security groups for the fleet.
            :param subnet_ids: The identifiers of the subnets to which a network interface is attached from the fleet instance. Fleet instances can use one or two subnets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-fleet-vpcconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
                
                vpc_config_property = appstream_mixins.CfnFleetPropsMixin.VpcConfigProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dcd0de05377106672aad34890479e3529144d1d1525bec704a3316010e6f495a)
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
                check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnet_ids is not None:
                self._values["subnet_ids"] = subnet_ids

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The identifiers of the security groups for the fleet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-fleet-vpcconfig.html#cfn-appstream-fleet-vpcconfig-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The identifiers of the subnets to which a network interface is attached from the fleet instance.

            Fleet instances can use one or two subnets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-fleet-vpcconfig.html#cfn-appstream-fleet-vpcconfig-subnetids
            '''
            result = self._values.get("subnet_ids")
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
    jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnImageBuilderMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_endpoints": "accessEndpoints",
        "appstream_agent_version": "appstreamAgentVersion",
        "description": "description",
        "display_name": "displayName",
        "domain_join_info": "domainJoinInfo",
        "enable_default_internet_access": "enableDefaultInternetAccess",
        "iam_role_arn": "iamRoleArn",
        "image_arn": "imageArn",
        "image_name": "imageName",
        "instance_type": "instanceType",
        "name": "name",
        "tags": "tags",
        "vpc_config": "vpcConfig",
    },
)
class CfnImageBuilderMixinProps:
    def __init__(
        self,
        *,
        access_endpoints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnImageBuilderPropsMixin.AccessEndpointProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        appstream_agent_version: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        domain_join_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnImageBuilderPropsMixin.DomainJoinInfoProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        enable_default_internet_access: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        iam_role_arn: typing.Optional[builtins.str] = None,
        image_arn: typing.Optional[builtins.str] = None,
        image_name: typing.Optional[builtins.str] = None,
        instance_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnImageBuilderPropsMixin.VpcConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnImageBuilderPropsMixin.

        :param access_endpoints: The list of virtual private cloud (VPC) interface endpoint objects. Administrators can connect to the image builder only through the specified endpoints.
        :param appstream_agent_version: The version of the WorkSpaces Applications agent to use for this image builder. To use the latest version of the WorkSpaces Applications agent, specify [LATEST].
        :param description: The description to display.
        :param display_name: The image builder name to display.
        :param domain_join_info: The name of the directory and organizational unit (OU) to use to join the image builder to a Microsoft Active Directory domain.
        :param enable_default_internet_access: Enables or disables default internet access for the image builder.
        :param iam_role_arn: The ARN of the IAM role that is applied to the image builder. To assume a role, the image builder calls the AWS Security Token Service ``AssumeRole`` API operation and passes the ARN of the role to use. The operation creates a new session with temporary credentials. AppStream 2.0 retrieves the temporary credentials and creates the *appstream_machine_role* credential profile on the instance. For more information, see `Using an IAM Role to Grant Permissions to Applications and Scripts Running on AppStream 2.0 Streaming Instances <https://docs.aws.amazon.com/appstream2/latest/developerguide/using-iam-roles-to-grant-permissions-to-applications-scripts-streaming-instances.html>`_ in the *Amazon AppStream 2.0 Administration Guide* .
        :param image_arn: The ARN of the public, private, or shared image to use.
        :param image_name: The name of the image used to create the image builder.
        :param instance_type: The instance type to use when launching the image builder. The following instance types are available:. - stream.standard.small - stream.standard.medium - stream.standard.large - stream.compute.large - stream.compute.xlarge - stream.compute.2xlarge - stream.compute.4xlarge - stream.compute.8xlarge - stream.memory.large - stream.memory.xlarge - stream.memory.2xlarge - stream.memory.4xlarge - stream.memory.8xlarge - stream.memory.z1d.large - stream.memory.z1d.xlarge - stream.memory.z1d.2xlarge - stream.memory.z1d.3xlarge - stream.memory.z1d.6xlarge - stream.memory.z1d.12xlarge - stream.graphics-design.large - stream.graphics-design.xlarge - stream.graphics-design.2xlarge - stream.graphics-design.4xlarge - stream.graphics.g4dn.xlarge - stream.graphics.g4dn.2xlarge - stream.graphics.g4dn.4xlarge - stream.graphics.g4dn.8xlarge - stream.graphics.g4dn.12xlarge - stream.graphics.g4dn.16xlarge - stream.graphics.g5.xlarge - stream.graphics.g5.2xlarge - stream.graphics.g5.4xlarge - stream.graphics.g5.8xlarge - stream.graphics.g5.16xlarge - stream.graphics.g5.12xlarge - stream.graphics.g5.24xlarge - stream.graphics.g6.xlarge - stream.graphics.g6.2xlarge - stream.graphics.g6.4xlarge - stream.graphics.g6.8xlarge - stream.graphics.g6.16xlarge - stream.graphics.g6.12xlarge - stream.graphics.g6.24xlarge - stream.graphics.gr6.4xlarge - stream.graphics.gr6.8xlarge - stream.graphics.g6f.large - stream.graphics.g6f.xlarge - stream.graphics.g6f.2xlarge - stream.graphics.g6f.4xlarge - stream.graphics.gr6f.4xlarge
        :param name: A unique name for the image builder.
        :param tags: An array of key-value pairs.
        :param vpc_config: The VPC configuration for the image builder. You can specify only one subnet.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
            
            cfn_image_builder_mixin_props = appstream_mixins.CfnImageBuilderMixinProps(
                access_endpoints=[appstream_mixins.CfnImageBuilderPropsMixin.AccessEndpointProperty(
                    endpoint_type="endpointType",
                    vpce_id="vpceId"
                )],
                appstream_agent_version="appstreamAgentVersion",
                description="description",
                display_name="displayName",
                domain_join_info=appstream_mixins.CfnImageBuilderPropsMixin.DomainJoinInfoProperty(
                    directory_name="directoryName",
                    organizational_unit_distinguished_name="organizationalUnitDistinguishedName"
                ),
                enable_default_internet_access=False,
                iam_role_arn="iamRoleArn",
                image_arn="imageArn",
                image_name="imageName",
                instance_type="instanceType",
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vpc_config=appstream_mixins.CfnImageBuilderPropsMixin.VpcConfigProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03ffb03096557b9c4a6c6352cfc42ac94c5a6026e18c420bfdc974304c2c21cc)
            check_type(argname="argument access_endpoints", value=access_endpoints, expected_type=type_hints["access_endpoints"])
            check_type(argname="argument appstream_agent_version", value=appstream_agent_version, expected_type=type_hints["appstream_agent_version"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument domain_join_info", value=domain_join_info, expected_type=type_hints["domain_join_info"])
            check_type(argname="argument enable_default_internet_access", value=enable_default_internet_access, expected_type=type_hints["enable_default_internet_access"])
            check_type(argname="argument iam_role_arn", value=iam_role_arn, expected_type=type_hints["iam_role_arn"])
            check_type(argname="argument image_arn", value=image_arn, expected_type=type_hints["image_arn"])
            check_type(argname="argument image_name", value=image_name, expected_type=type_hints["image_name"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc_config", value=vpc_config, expected_type=type_hints["vpc_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_endpoints is not None:
            self._values["access_endpoints"] = access_endpoints
        if appstream_agent_version is not None:
            self._values["appstream_agent_version"] = appstream_agent_version
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if domain_join_info is not None:
            self._values["domain_join_info"] = domain_join_info
        if enable_default_internet_access is not None:
            self._values["enable_default_internet_access"] = enable_default_internet_access
        if iam_role_arn is not None:
            self._values["iam_role_arn"] = iam_role_arn
        if image_arn is not None:
            self._values["image_arn"] = image_arn
        if image_name is not None:
            self._values["image_name"] = image_name
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags
        if vpc_config is not None:
            self._values["vpc_config"] = vpc_config

    @builtins.property
    def access_endpoints(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImageBuilderPropsMixin.AccessEndpointProperty"]]]]:
        '''The list of virtual private cloud (VPC) interface endpoint objects.

        Administrators can connect to the image builder only through the specified endpoints.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-accessendpoints
        '''
        result = self._values.get("access_endpoints")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImageBuilderPropsMixin.AccessEndpointProperty"]]]], result)

    @builtins.property
    def appstream_agent_version(self) -> typing.Optional[builtins.str]:
        '''The version of the WorkSpaces Applications agent to use for this image builder.

        To use the latest version of the WorkSpaces Applications agent, specify [LATEST].

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-appstreamagentversion
        '''
        result = self._values.get("appstream_agent_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description to display.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The image builder name to display.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-displayname
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_join_info(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImageBuilderPropsMixin.DomainJoinInfoProperty"]]:
        '''The name of the directory and organizational unit (OU) to use to join the image builder to a Microsoft Active Directory domain.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-domainjoininfo
        '''
        result = self._values.get("domain_join_info")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImageBuilderPropsMixin.DomainJoinInfoProperty"]], result)

    @builtins.property
    def enable_default_internet_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Enables or disables default internet access for the image builder.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-enabledefaultinternetaccess
        '''
        result = self._values.get("enable_default_internet_access")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def iam_role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the IAM role that is applied to the image builder.

        To assume a role, the image builder calls the AWS Security Token Service ``AssumeRole`` API operation and passes the ARN of the role to use. The operation creates a new session with temporary credentials. AppStream 2.0 retrieves the temporary credentials and creates the *appstream_machine_role* credential profile on the instance.

        For more information, see `Using an IAM Role to Grant Permissions to Applications and Scripts Running on AppStream 2.0 Streaming Instances <https://docs.aws.amazon.com/appstream2/latest/developerguide/using-iam-roles-to-grant-permissions-to-applications-scripts-streaming-instances.html>`_ in the *Amazon AppStream 2.0 Administration Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-iamrolearn
        '''
        result = self._values.get("iam_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the public, private, or shared image to use.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-imagearn
        '''
        result = self._values.get("image_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_name(self) -> typing.Optional[builtins.str]:
        '''The name of the image used to create the image builder.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-imagename
        '''
        result = self._values.get("image_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[builtins.str]:
        '''The instance type to use when launching the image builder. The following instance types are available:.

        - stream.standard.small
        - stream.standard.medium
        - stream.standard.large
        - stream.compute.large
        - stream.compute.xlarge
        - stream.compute.2xlarge
        - stream.compute.4xlarge
        - stream.compute.8xlarge
        - stream.memory.large
        - stream.memory.xlarge
        - stream.memory.2xlarge
        - stream.memory.4xlarge
        - stream.memory.8xlarge
        - stream.memory.z1d.large
        - stream.memory.z1d.xlarge
        - stream.memory.z1d.2xlarge
        - stream.memory.z1d.3xlarge
        - stream.memory.z1d.6xlarge
        - stream.memory.z1d.12xlarge
        - stream.graphics-design.large
        - stream.graphics-design.xlarge
        - stream.graphics-design.2xlarge
        - stream.graphics-design.4xlarge
        - stream.graphics.g4dn.xlarge
        - stream.graphics.g4dn.2xlarge
        - stream.graphics.g4dn.4xlarge
        - stream.graphics.g4dn.8xlarge
        - stream.graphics.g4dn.12xlarge
        - stream.graphics.g4dn.16xlarge
        - stream.graphics.g5.xlarge
        - stream.graphics.g5.2xlarge
        - stream.graphics.g5.4xlarge
        - stream.graphics.g5.8xlarge
        - stream.graphics.g5.16xlarge
        - stream.graphics.g5.12xlarge
        - stream.graphics.g5.24xlarge
        - stream.graphics.g6.xlarge
        - stream.graphics.g6.2xlarge
        - stream.graphics.g6.4xlarge
        - stream.graphics.g6.8xlarge
        - stream.graphics.g6.16xlarge
        - stream.graphics.g6.12xlarge
        - stream.graphics.g6.24xlarge
        - stream.graphics.gr6.4xlarge
        - stream.graphics.gr6.8xlarge
        - stream.graphics.g6f.large
        - stream.graphics.g6f.xlarge
        - stream.graphics.g6f.2xlarge
        - stream.graphics.g6f.4xlarge
        - stream.graphics.gr6f.4xlarge

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-instancetype
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A unique name for the image builder.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def vpc_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImageBuilderPropsMixin.VpcConfigProperty"]]:
        '''The VPC configuration for the image builder.

        You can specify only one subnet.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-vpcconfig
        '''
        result = self._values.get("vpc_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImageBuilderPropsMixin.VpcConfigProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnImageBuilderMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnImageBuilderPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnImageBuilderPropsMixin",
):
    '''The ``AWS::AppStream::ImageBuilder`` resource creates an image builder for Amazon AppStream 2.0. An image builder is a virtual machine that is used to create an image.

    The initial state of the image builder is ``PENDING`` . When it is ready, the state is ``RUNNING`` .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html
    :cloudformationResource: AWS::AppStream::ImageBuilder
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
        
        cfn_image_builder_props_mixin = appstream_mixins.CfnImageBuilderPropsMixin(appstream_mixins.CfnImageBuilderMixinProps(
            access_endpoints=[appstream_mixins.CfnImageBuilderPropsMixin.AccessEndpointProperty(
                endpoint_type="endpointType",
                vpce_id="vpceId"
            )],
            appstream_agent_version="appstreamAgentVersion",
            description="description",
            display_name="displayName",
            domain_join_info=appstream_mixins.CfnImageBuilderPropsMixin.DomainJoinInfoProperty(
                directory_name="directoryName",
                organizational_unit_distinguished_name="organizationalUnitDistinguishedName"
            ),
            enable_default_internet_access=False,
            iam_role_arn="iamRoleArn",
            image_arn="imageArn",
            image_name="imageName",
            instance_type="instanceType",
            name="name",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            vpc_config=appstream_mixins.CfnImageBuilderPropsMixin.VpcConfigProperty(
                security_group_ids=["securityGroupIds"],
                subnet_ids=["subnetIds"]
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnImageBuilderMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AppStream::ImageBuilder``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4d2f72d605b685c0cf79a662d4dd99ea92367ef864a9adcc50dcaf53fa9f282)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba22a45fde17620d8aab4d70878de095ebacc0f6bb377da81b1fa6e356ffba35)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46f5e2ee7881162930e3b6e914f3f4fc88b2c6fa2b885d2c0278ca22f8e4092b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnImageBuilderMixinProps:
        return typing.cast(CfnImageBuilderMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnImageBuilderPropsMixin.AccessEndpointProperty",
        jsii_struct_bases=[],
        name_mapping={"endpoint_type": "endpointType", "vpce_id": "vpceId"},
    )
    class AccessEndpointProperty:
        def __init__(
            self,
            *,
            endpoint_type: typing.Optional[builtins.str] = None,
            vpce_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes an interface VPC endpoint (interface endpoint) that lets you create a private connection between the virtual private cloud (VPC) that you specify and WorkSpaces Applications.

            When you specify an interface endpoint for a stack, users of the stack can connect to WorkSpaces Applications only through that endpoint. When you specify an interface endpoint for an image builder, administrators can connect to the image builder only through that endpoint.

            :param endpoint_type: The type of interface endpoint.
            :param vpce_id: The identifier (ID) of the VPC in which the interface endpoint is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-imagebuilder-accessendpoint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
                
                access_endpoint_property = appstream_mixins.CfnImageBuilderPropsMixin.AccessEndpointProperty(
                    endpoint_type="endpointType",
                    vpce_id="vpceId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b85d22e2015f24c4ee0669f618ea4c4dbe67084fd84aa37f9838025ee24e4383)
                check_type(argname="argument endpoint_type", value=endpoint_type, expected_type=type_hints["endpoint_type"])
                check_type(argname="argument vpce_id", value=vpce_id, expected_type=type_hints["vpce_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if endpoint_type is not None:
                self._values["endpoint_type"] = endpoint_type
            if vpce_id is not None:
                self._values["vpce_id"] = vpce_id

        @builtins.property
        def endpoint_type(self) -> typing.Optional[builtins.str]:
            '''The type of interface endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-imagebuilder-accessendpoint.html#cfn-appstream-imagebuilder-accessendpoint-endpointtype
            '''
            result = self._values.get("endpoint_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vpce_id(self) -> typing.Optional[builtins.str]:
            '''The identifier (ID) of the VPC in which the interface endpoint is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-imagebuilder-accessendpoint.html#cfn-appstream-imagebuilder-accessendpoint-vpceid
            '''
            result = self._values.get("vpce_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessEndpointProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnImageBuilderPropsMixin.DomainJoinInfoProperty",
        jsii_struct_bases=[],
        name_mapping={
            "directory_name": "directoryName",
            "organizational_unit_distinguished_name": "organizationalUnitDistinguishedName",
        },
    )
    class DomainJoinInfoProperty:
        def __init__(
            self,
            *,
            directory_name: typing.Optional[builtins.str] = None,
            organizational_unit_distinguished_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The name of the directory and organizational unit (OU) to use to join the image builder to a Microsoft Active Directory domain.

            :param directory_name: The fully qualified name of the directory (for example, corp.example.com).
            :param organizational_unit_distinguished_name: The distinguished name of the organizational unit for computer accounts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-imagebuilder-domainjoininfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
                
                domain_join_info_property = appstream_mixins.CfnImageBuilderPropsMixin.DomainJoinInfoProperty(
                    directory_name="directoryName",
                    organizational_unit_distinguished_name="organizationalUnitDistinguishedName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__42123400051a5cc72d84a4796998aadef000c9f8b5b58e96ef05c1039a024d40)
                check_type(argname="argument directory_name", value=directory_name, expected_type=type_hints["directory_name"])
                check_type(argname="argument organizational_unit_distinguished_name", value=organizational_unit_distinguished_name, expected_type=type_hints["organizational_unit_distinguished_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if directory_name is not None:
                self._values["directory_name"] = directory_name
            if organizational_unit_distinguished_name is not None:
                self._values["organizational_unit_distinguished_name"] = organizational_unit_distinguished_name

        @builtins.property
        def directory_name(self) -> typing.Optional[builtins.str]:
            '''The fully qualified name of the directory (for example, corp.example.com).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-imagebuilder-domainjoininfo.html#cfn-appstream-imagebuilder-domainjoininfo-directoryname
            '''
            result = self._values.get("directory_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def organizational_unit_distinguished_name(
            self,
        ) -> typing.Optional[builtins.str]:
            '''The distinguished name of the organizational unit for computer accounts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-imagebuilder-domainjoininfo.html#cfn-appstream-imagebuilder-domainjoininfo-organizationalunitdistinguishedname
            '''
            result = self._values.get("organizational_unit_distinguished_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DomainJoinInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnImageBuilderPropsMixin.VpcConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
        },
    )
    class VpcConfigProperty:
        def __init__(
            self,
            *,
            security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The VPC configuration for the image builder.

            :param security_group_ids: The identifiers of the security groups for the image builder.
            :param subnet_ids: The identifier of the subnet to which a network interface is attached from the image builder instance. An image builder instance can use one subnet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-imagebuilder-vpcconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
                
                vpc_config_property = appstream_mixins.CfnImageBuilderPropsMixin.VpcConfigProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f61336147383bcc34f09611022be6aaf289a72234c078aaa924bba59900997de)
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
                check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnet_ids is not None:
                self._values["subnet_ids"] = subnet_ids

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The identifiers of the security groups for the image builder.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-imagebuilder-vpcconfig.html#cfn-appstream-imagebuilder-vpcconfig-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The identifier of the subnet to which a network interface is attached from the image builder instance.

            An image builder instance can use one subnet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-imagebuilder-vpcconfig.html#cfn-appstream-imagebuilder-vpcconfig-subnetids
            '''
            result = self._values.get("subnet_ids")
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
    jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnStackFleetAssociationMixinProps",
    jsii_struct_bases=[],
    name_mapping={"fleet_name": "fleetName", "stack_name": "stackName"},
)
class CfnStackFleetAssociationMixinProps:
    def __init__(
        self,
        *,
        fleet_name: typing.Optional[builtins.str] = None,
        stack_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnStackFleetAssociationPropsMixin.

        :param fleet_name: The name of the fleet. To associate a fleet with a stack, you must specify a dependency on the fleet resource. For more information, see `DependsOn Attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html>`_ .
        :param stack_name: The name of the stack. To associate a fleet with a stack, you must specify a dependency on the stack resource. For more information, see `DependsOn Attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackfleetassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
            
            cfn_stack_fleet_association_mixin_props = appstream_mixins.CfnStackFleetAssociationMixinProps(
                fleet_name="fleetName",
                stack_name="stackName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eba4d8611ccc1174e0837bb1664375462ace7933440f186684aecf8a71549a2)
            check_type(argname="argument fleet_name", value=fleet_name, expected_type=type_hints["fleet_name"])
            check_type(argname="argument stack_name", value=stack_name, expected_type=type_hints["stack_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if fleet_name is not None:
            self._values["fleet_name"] = fleet_name
        if stack_name is not None:
            self._values["stack_name"] = stack_name

    @builtins.property
    def fleet_name(self) -> typing.Optional[builtins.str]:
        '''The name of the fleet.

        To associate a fleet with a stack, you must specify a dependency on the fleet resource. For more information, see `DependsOn Attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackfleetassociation.html#cfn-appstream-stackfleetassociation-fleetname
        '''
        result = self._values.get("fleet_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stack_name(self) -> typing.Optional[builtins.str]:
        '''The name of the stack.

        To associate a fleet with a stack, you must specify a dependency on the stack resource. For more information, see `DependsOn Attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackfleetassociation.html#cfn-appstream-stackfleetassociation-stackname
        '''
        result = self._values.get("stack_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStackFleetAssociationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnStackFleetAssociationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnStackFleetAssociationPropsMixin",
):
    '''The ``AWS::AppStream::StackFleetAssociation`` resource associates the specified fleet with the specified stack for Amazon AppStream 2.0.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackfleetassociation.html
    :cloudformationResource: AWS::AppStream::StackFleetAssociation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
        
        cfn_stack_fleet_association_props_mixin = appstream_mixins.CfnStackFleetAssociationPropsMixin(appstream_mixins.CfnStackFleetAssociationMixinProps(
            fleet_name="fleetName",
            stack_name="stackName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnStackFleetAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AppStream::StackFleetAssociation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5064ae7c908740667cdcfe7bd6858099a49c7409af98d0cc1531f11108f73474)
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
            type_hints = typing.get_type_hints(_typecheckingstub__65dff8fd5c01edca44bdf9b8efdc0f496fe3265c8d4fa9ab71d37427d15be291)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__404536828bf27fa73afa80343dba5609b953966042f16ee76938822cf672b3da)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnStackFleetAssociationMixinProps:
        return typing.cast(CfnStackFleetAssociationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnStackMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_endpoints": "accessEndpoints",
        "application_settings": "applicationSettings",
        "attributes_to_delete": "attributesToDelete",
        "delete_storage_connectors": "deleteStorageConnectors",
        "description": "description",
        "display_name": "displayName",
        "embed_host_domains": "embedHostDomains",
        "feedback_url": "feedbackUrl",
        "name": "name",
        "redirect_url": "redirectUrl",
        "storage_connectors": "storageConnectors",
        "streaming_experience_settings": "streamingExperienceSettings",
        "tags": "tags",
        "user_settings": "userSettings",
    },
)
class CfnStackMixinProps:
    def __init__(
        self,
        *,
        access_endpoints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStackPropsMixin.AccessEndpointProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        application_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStackPropsMixin.ApplicationSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        attributes_to_delete: typing.Optional[typing.Sequence[builtins.str]] = None,
        delete_storage_connectors: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        embed_host_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        feedback_url: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        redirect_url: typing.Optional[builtins.str] = None,
        storage_connectors: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStackPropsMixin.StorageConnectorProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        streaming_experience_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStackPropsMixin.StreamingExperienceSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        user_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStackPropsMixin.UserSettingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnStackPropsMixin.

        :param access_endpoints: The list of virtual private cloud (VPC) interface endpoint objects. Users of the stack can connect to WorkSpaces Applications only through the specified endpoints.
        :param application_settings: The persistent application settings for users of the stack. When these settings are enabled, changes that users make to applications and Windows settings are automatically saved after each session and applied to the next session.
        :param attributes_to_delete: The stack attributes to delete.
        :param delete_storage_connectors: *This parameter has been deprecated.*. Deletes the storage connectors currently enabled for the stack.
        :param description: The description to display.
        :param display_name: The stack name to display.
        :param embed_host_domains: The domains where WorkSpaces Applications streaming sessions can be embedded in an iframe. You must approve the domains that you want to host embedded WorkSpaces Applications streaming sessions.
        :param feedback_url: The URL that users are redirected to after they click the Send Feedback link. If no URL is specified, no Send Feedback link is displayed.
        :param name: The name of the stack.
        :param redirect_url: The URL that users are redirected to after their streaming session ends.
        :param storage_connectors: The storage connectors to enable.
        :param streaming_experience_settings: The streaming protocol that you want your stack to prefer. This can be UDP or TCP. Currently, UDP is only supported in the Windows native client.
        :param tags: An array of key-value pairs.
        :param user_settings: The actions that are enabled or disabled for users during their streaming sessions. By default, these actions are enabled.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
            
            cfn_stack_mixin_props = appstream_mixins.CfnStackMixinProps(
                access_endpoints=[appstream_mixins.CfnStackPropsMixin.AccessEndpointProperty(
                    endpoint_type="endpointType",
                    vpce_id="vpceId"
                )],
                application_settings=appstream_mixins.CfnStackPropsMixin.ApplicationSettingsProperty(
                    enabled=False,
                    settings_group="settingsGroup"
                ),
                attributes_to_delete=["attributesToDelete"],
                delete_storage_connectors=False,
                description="description",
                display_name="displayName",
                embed_host_domains=["embedHostDomains"],
                feedback_url="feedbackUrl",
                name="name",
                redirect_url="redirectUrl",
                storage_connectors=[appstream_mixins.CfnStackPropsMixin.StorageConnectorProperty(
                    connector_type="connectorType",
                    domains=["domains"],
                    resource_identifier="resourceIdentifier"
                )],
                streaming_experience_settings=appstream_mixins.CfnStackPropsMixin.StreamingExperienceSettingsProperty(
                    preferred_protocol="preferredProtocol"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                user_settings=[appstream_mixins.CfnStackPropsMixin.UserSettingProperty(
                    action="action",
                    maximum_length=123,
                    permission="permission"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f795953f7b7027b8d95aaf397585dbaa1ed064d42bb8a5b88d9c5a4416230025)
            check_type(argname="argument access_endpoints", value=access_endpoints, expected_type=type_hints["access_endpoints"])
            check_type(argname="argument application_settings", value=application_settings, expected_type=type_hints["application_settings"])
            check_type(argname="argument attributes_to_delete", value=attributes_to_delete, expected_type=type_hints["attributes_to_delete"])
            check_type(argname="argument delete_storage_connectors", value=delete_storage_connectors, expected_type=type_hints["delete_storage_connectors"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument embed_host_domains", value=embed_host_domains, expected_type=type_hints["embed_host_domains"])
            check_type(argname="argument feedback_url", value=feedback_url, expected_type=type_hints["feedback_url"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument redirect_url", value=redirect_url, expected_type=type_hints["redirect_url"])
            check_type(argname="argument storage_connectors", value=storage_connectors, expected_type=type_hints["storage_connectors"])
            check_type(argname="argument streaming_experience_settings", value=streaming_experience_settings, expected_type=type_hints["streaming_experience_settings"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument user_settings", value=user_settings, expected_type=type_hints["user_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_endpoints is not None:
            self._values["access_endpoints"] = access_endpoints
        if application_settings is not None:
            self._values["application_settings"] = application_settings
        if attributes_to_delete is not None:
            self._values["attributes_to_delete"] = attributes_to_delete
        if delete_storage_connectors is not None:
            self._values["delete_storage_connectors"] = delete_storage_connectors
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if embed_host_domains is not None:
            self._values["embed_host_domains"] = embed_host_domains
        if feedback_url is not None:
            self._values["feedback_url"] = feedback_url
        if name is not None:
            self._values["name"] = name
        if redirect_url is not None:
            self._values["redirect_url"] = redirect_url
        if storage_connectors is not None:
            self._values["storage_connectors"] = storage_connectors
        if streaming_experience_settings is not None:
            self._values["streaming_experience_settings"] = streaming_experience_settings
        if tags is not None:
            self._values["tags"] = tags
        if user_settings is not None:
            self._values["user_settings"] = user_settings

    @builtins.property
    def access_endpoints(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStackPropsMixin.AccessEndpointProperty"]]]]:
        '''The list of virtual private cloud (VPC) interface endpoint objects.

        Users of the stack can connect to WorkSpaces Applications only through the specified endpoints.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-accessendpoints
        '''
        result = self._values.get("access_endpoints")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStackPropsMixin.AccessEndpointProperty"]]]], result)

    @builtins.property
    def application_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStackPropsMixin.ApplicationSettingsProperty"]]:
        '''The persistent application settings for users of the stack.

        When these settings are enabled, changes that users make to applications and Windows settings are automatically saved after each session and applied to the next session.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-applicationsettings
        '''
        result = self._values.get("application_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStackPropsMixin.ApplicationSettingsProperty"]], result)

    @builtins.property
    def attributes_to_delete(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The stack attributes to delete.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-attributestodelete
        '''
        result = self._values.get("attributes_to_delete")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def delete_storage_connectors(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''*This parameter has been deprecated.*.

        Deletes the storage connectors currently enabled for the stack.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-deletestorageconnectors
        '''
        result = self._values.get("delete_storage_connectors")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description to display.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The stack name to display.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-displayname
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def embed_host_domains(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The domains where WorkSpaces Applications streaming sessions can be embedded in an iframe.

        You must approve the domains that you want to host embedded WorkSpaces Applications streaming sessions.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-embedhostdomains
        '''
        result = self._values.get("embed_host_domains")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def feedback_url(self) -> typing.Optional[builtins.str]:
        '''The URL that users are redirected to after they click the Send Feedback link.

        If no URL is specified, no Send Feedback link is displayed.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-feedbackurl
        '''
        result = self._values.get("feedback_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the stack.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redirect_url(self) -> typing.Optional[builtins.str]:
        '''The URL that users are redirected to after their streaming session ends.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-redirecturl
        '''
        result = self._values.get("redirect_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_connectors(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStackPropsMixin.StorageConnectorProperty"]]]]:
        '''The storage connectors to enable.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-storageconnectors
        '''
        result = self._values.get("storage_connectors")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStackPropsMixin.StorageConnectorProperty"]]]], result)

    @builtins.property
    def streaming_experience_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStackPropsMixin.StreamingExperienceSettingsProperty"]]:
        '''The streaming protocol that you want your stack to prefer.

        This can be UDP or TCP. Currently, UDP is only supported in the Windows native client.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-streamingexperiencesettings
        '''
        result = self._values.get("streaming_experience_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStackPropsMixin.StreamingExperienceSettingsProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def user_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStackPropsMixin.UserSettingProperty"]]]]:
        '''The actions that are enabled or disabled for users during their streaming sessions.

        By default, these actions are enabled.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-usersettings
        '''
        result = self._values.get("user_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStackPropsMixin.UserSettingProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStackMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnStackPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnStackPropsMixin",
):
    '''The ``AWS::AppStream::Stack`` resource creates a stack to start streaming applications to Amazon AppStream 2.0 users. A stack consists of an associated fleet, user access policies, and storage configurations.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html
    :cloudformationResource: AWS::AppStream::Stack
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
        
        cfn_stack_props_mixin = appstream_mixins.CfnStackPropsMixin(appstream_mixins.CfnStackMixinProps(
            access_endpoints=[appstream_mixins.CfnStackPropsMixin.AccessEndpointProperty(
                endpoint_type="endpointType",
                vpce_id="vpceId"
            )],
            application_settings=appstream_mixins.CfnStackPropsMixin.ApplicationSettingsProperty(
                enabled=False,
                settings_group="settingsGroup"
            ),
            attributes_to_delete=["attributesToDelete"],
            delete_storage_connectors=False,
            description="description",
            display_name="displayName",
            embed_host_domains=["embedHostDomains"],
            feedback_url="feedbackUrl",
            name="name",
            redirect_url="redirectUrl",
            storage_connectors=[appstream_mixins.CfnStackPropsMixin.StorageConnectorProperty(
                connector_type="connectorType",
                domains=["domains"],
                resource_identifier="resourceIdentifier"
            )],
            streaming_experience_settings=appstream_mixins.CfnStackPropsMixin.StreamingExperienceSettingsProperty(
                preferred_protocol="preferredProtocol"
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            user_settings=[appstream_mixins.CfnStackPropsMixin.UserSettingProperty(
                action="action",
                maximum_length=123,
                permission="permission"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnStackMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AppStream::Stack``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbf1d41fe8eef03fb8cf12f5da76cc04528beec1ebfcd2402ce50b22402c082b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac51e2c66fce9df734bec460c0a28523d207c7e6898fd07b50703af6693903d1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d1b60dec4c5d6ffa48925c039bca3e4d9e0af294de2b7f989d555d53a3240b7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnStackMixinProps:
        return typing.cast(CfnStackMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnStackPropsMixin.AccessEndpointProperty",
        jsii_struct_bases=[],
        name_mapping={"endpoint_type": "endpointType", "vpce_id": "vpceId"},
    )
    class AccessEndpointProperty:
        def __init__(
            self,
            *,
            endpoint_type: typing.Optional[builtins.str] = None,
            vpce_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes an interface VPC endpoint (interface endpoint) that lets you create a private connection between the virtual private cloud (VPC) that you specify and WorkSpaces Applications.

            When you specify an interface endpoint for a stack, users of the stack can connect to WorkSpaces Applications only through that endpoint. When you specify an interface endpoint for an image builder, administrators can connect to the image builder only through that endpoint.

            :param endpoint_type: The type of interface endpoint.
            :param vpce_id: The identifier (ID) of the VPC in which the interface endpoint is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-accessendpoint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
                
                access_endpoint_property = appstream_mixins.CfnStackPropsMixin.AccessEndpointProperty(
                    endpoint_type="endpointType",
                    vpce_id="vpceId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3c6ec8646c5f0595f1923a1a10b09eb514fee9edfe02db450f798a00e03b8269)
                check_type(argname="argument endpoint_type", value=endpoint_type, expected_type=type_hints["endpoint_type"])
                check_type(argname="argument vpce_id", value=vpce_id, expected_type=type_hints["vpce_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if endpoint_type is not None:
                self._values["endpoint_type"] = endpoint_type
            if vpce_id is not None:
                self._values["vpce_id"] = vpce_id

        @builtins.property
        def endpoint_type(self) -> typing.Optional[builtins.str]:
            '''The type of interface endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-accessendpoint.html#cfn-appstream-stack-accessendpoint-endpointtype
            '''
            result = self._values.get("endpoint_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vpce_id(self) -> typing.Optional[builtins.str]:
            '''The identifier (ID) of the VPC in which the interface endpoint is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-accessendpoint.html#cfn-appstream-stack-accessendpoint-vpceid
            '''
            result = self._values.get("vpce_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessEndpointProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnStackPropsMixin.ApplicationSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled", "settings_group": "settingsGroup"},
    )
    class ApplicationSettingsProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            settings_group: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The persistent application settings for users of a stack.

            :param enabled: Enables or disables persistent application settings for users during their streaming sessions.
            :param settings_group: The path prefix for the S3 bucket where users’ persistent application settings are stored. You can allow the same persistent application settings to be used across multiple stacks by specifying the same settings group for each stack.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-applicationsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
                
                application_settings_property = appstream_mixins.CfnStackPropsMixin.ApplicationSettingsProperty(
                    enabled=False,
                    settings_group="settingsGroup"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__76bb8b969a66e24577cc1638ad2fa7d13877f7c9cdf337c6b66ddfeab0115e9e)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument settings_group", value=settings_group, expected_type=type_hints["settings_group"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if settings_group is not None:
                self._values["settings_group"] = settings_group

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Enables or disables persistent application settings for users during their streaming sessions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-applicationsettings.html#cfn-appstream-stack-applicationsettings-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def settings_group(self) -> typing.Optional[builtins.str]:
            '''The path prefix for the S3 bucket where users’ persistent application settings are stored.

            You can allow the same persistent application settings to be used across multiple stacks by specifying the same settings group for each stack.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-applicationsettings.html#cfn-appstream-stack-applicationsettings-settingsgroup
            '''
            result = self._values.get("settings_group")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApplicationSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnStackPropsMixin.StorageConnectorProperty",
        jsii_struct_bases=[],
        name_mapping={
            "connector_type": "connectorType",
            "domains": "domains",
            "resource_identifier": "resourceIdentifier",
        },
    )
    class StorageConnectorProperty:
        def __init__(
            self,
            *,
            connector_type: typing.Optional[builtins.str] = None,
            domains: typing.Optional[typing.Sequence[builtins.str]] = None,
            resource_identifier: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A connector that enables persistent storage for users.

            :param connector_type: The type of storage connector.
            :param domains: The names of the domains for the account.
            :param resource_identifier: The ARN of the storage connector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-storageconnector.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
                
                storage_connector_property = appstream_mixins.CfnStackPropsMixin.StorageConnectorProperty(
                    connector_type="connectorType",
                    domains=["domains"],
                    resource_identifier="resourceIdentifier"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__99bd542ec9dfd0e8ee7678524140a5c2f3a9f1c86db3da307f365bc4e7c2e0f4)
                check_type(argname="argument connector_type", value=connector_type, expected_type=type_hints["connector_type"])
                check_type(argname="argument domains", value=domains, expected_type=type_hints["domains"])
                check_type(argname="argument resource_identifier", value=resource_identifier, expected_type=type_hints["resource_identifier"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if connector_type is not None:
                self._values["connector_type"] = connector_type
            if domains is not None:
                self._values["domains"] = domains
            if resource_identifier is not None:
                self._values["resource_identifier"] = resource_identifier

        @builtins.property
        def connector_type(self) -> typing.Optional[builtins.str]:
            '''The type of storage connector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-storageconnector.html#cfn-appstream-stack-storageconnector-connectortype
            '''
            result = self._values.get("connector_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def domains(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The names of the domains for the account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-storageconnector.html#cfn-appstream-stack-storageconnector-domains
            '''
            result = self._values.get("domains")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def resource_identifier(self) -> typing.Optional[builtins.str]:
            '''The ARN of the storage connector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-storageconnector.html#cfn-appstream-stack-storageconnector-resourceidentifier
            '''
            result = self._values.get("resource_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StorageConnectorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnStackPropsMixin.StreamingExperienceSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"preferred_protocol": "preferredProtocol"},
    )
    class StreamingExperienceSettingsProperty:
        def __init__(
            self,
            *,
            preferred_protocol: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The streaming protocol that you want your stack to prefer.

            This can be UDP or TCP. Currently, UDP is only supported in the Windows native client.

            :param preferred_protocol: The preferred protocol that you want to use while streaming your application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-streamingexperiencesettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
                
                streaming_experience_settings_property = appstream_mixins.CfnStackPropsMixin.StreamingExperienceSettingsProperty(
                    preferred_protocol="preferredProtocol"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c978db65d8629aa53b264c6f7a981ed9cef01ff8dc58c7fbb77e1227b766ab24)
                check_type(argname="argument preferred_protocol", value=preferred_protocol, expected_type=type_hints["preferred_protocol"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if preferred_protocol is not None:
                self._values["preferred_protocol"] = preferred_protocol

        @builtins.property
        def preferred_protocol(self) -> typing.Optional[builtins.str]:
            '''The preferred protocol that you want to use while streaming your application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-streamingexperiencesettings.html#cfn-appstream-stack-streamingexperiencesettings-preferredprotocol
            '''
            result = self._values.get("preferred_protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StreamingExperienceSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnStackPropsMixin.UserSettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "maximum_length": "maximumLength",
            "permission": "permission",
        },
    )
    class UserSettingProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[builtins.str] = None,
            maximum_length: typing.Optional[jsii.Number] = None,
            permission: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies an action and whether the action is enabled or disabled for users during their streaming sessions.

            :param action: The action that is enabled or disabled.
            :param maximum_length: Specifies the number of characters that can be copied by end users from the local device to the remote session, and to the local device from the remote session. This can be specified only for the ``CLIPBOARD_COPY_FROM_LOCAL_DEVICE`` and ``CLIPBOARD_COPY_TO_LOCAL_DEVICE`` actions. This defaults to 20,971,520 (20 MB) when unspecified and the permission is ``ENABLED`` . This can't be specified when the permission is ``DISABLED`` . The value can be between 1 and 20,971,520 (20 MB).
            :param permission: Indicates whether the action is enabled or disabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-usersetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
                
                user_setting_property = appstream_mixins.CfnStackPropsMixin.UserSettingProperty(
                    action="action",
                    maximum_length=123,
                    permission="permission"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__eab0289127c9e583c43470e6bdbd75f1e045d5ddfdda9648bd2ee81649efda4b)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument maximum_length", value=maximum_length, expected_type=type_hints["maximum_length"])
                check_type(argname="argument permission", value=permission, expected_type=type_hints["permission"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if maximum_length is not None:
                self._values["maximum_length"] = maximum_length
            if permission is not None:
                self._values["permission"] = permission

        @builtins.property
        def action(self) -> typing.Optional[builtins.str]:
            '''The action that is enabled or disabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-usersetting.html#cfn-appstream-stack-usersetting-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def maximum_length(self) -> typing.Optional[jsii.Number]:
            '''Specifies the number of characters that can be copied by end users from the local device to the remote session, and to the local device from the remote session.

            This can be specified only for the ``CLIPBOARD_COPY_FROM_LOCAL_DEVICE`` and ``CLIPBOARD_COPY_TO_LOCAL_DEVICE`` actions.

            This defaults to 20,971,520 (20 MB) when unspecified and the permission is ``ENABLED`` . This can't be specified when the permission is ``DISABLED`` .

            The value can be between 1 and 20,971,520 (20 MB).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-usersetting.html#cfn-appstream-stack-usersetting-maximumlength
            '''
            result = self._values.get("maximum_length")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def permission(self) -> typing.Optional[builtins.str]:
            '''Indicates whether the action is enabled or disabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-usersetting.html#cfn-appstream-stack-usersetting-permission
            '''
            result = self._values.get("permission")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UserSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnStackUserAssociationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "authentication_type": "authenticationType",
        "send_email_notification": "sendEmailNotification",
        "stack_name": "stackName",
        "user_name": "userName",
    },
)
class CfnStackUserAssociationMixinProps:
    def __init__(
        self,
        *,
        authentication_type: typing.Optional[builtins.str] = None,
        send_email_notification: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        stack_name: typing.Optional[builtins.str] = None,
        user_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnStackUserAssociationPropsMixin.

        :param authentication_type: The authentication type for the user who is associated with the stack. You must specify USERPOOL.
        :param send_email_notification: Specifies whether a welcome email is sent to a user after the user is created in the user pool.
        :param stack_name: The name of the stack that is associated with the user.
        :param user_name: The email address of the user who is associated with the stack. .. epigraph:: Users' email addresses are case-sensitive.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackuserassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
            
            cfn_stack_user_association_mixin_props = appstream_mixins.CfnStackUserAssociationMixinProps(
                authentication_type="authenticationType",
                send_email_notification=False,
                stack_name="stackName",
                user_name="userName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e04b7d77106417f36f198017a279df1620a89d58e207794d02e61882c17e591)
            check_type(argname="argument authentication_type", value=authentication_type, expected_type=type_hints["authentication_type"])
            check_type(argname="argument send_email_notification", value=send_email_notification, expected_type=type_hints["send_email_notification"])
            check_type(argname="argument stack_name", value=stack_name, expected_type=type_hints["stack_name"])
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if authentication_type is not None:
            self._values["authentication_type"] = authentication_type
        if send_email_notification is not None:
            self._values["send_email_notification"] = send_email_notification
        if stack_name is not None:
            self._values["stack_name"] = stack_name
        if user_name is not None:
            self._values["user_name"] = user_name

    @builtins.property
    def authentication_type(self) -> typing.Optional[builtins.str]:
        '''The authentication type for the user who is associated with the stack.

        You must specify USERPOOL.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackuserassociation.html#cfn-appstream-stackuserassociation-authenticationtype
        '''
        result = self._values.get("authentication_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def send_email_notification(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether a welcome email is sent to a user after the user is created in the user pool.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackuserassociation.html#cfn-appstream-stackuserassociation-sendemailnotification
        '''
        result = self._values.get("send_email_notification")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def stack_name(self) -> typing.Optional[builtins.str]:
        '''The name of the stack that is associated with the user.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackuserassociation.html#cfn-appstream-stackuserassociation-stackname
        '''
        result = self._values.get("stack_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_name(self) -> typing.Optional[builtins.str]:
        '''The email address of the user who is associated with the stack.

        .. epigraph::

           Users' email addresses are case-sensitive.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackuserassociation.html#cfn-appstream-stackuserassociation-username
        '''
        result = self._values.get("user_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStackUserAssociationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnStackUserAssociationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnStackUserAssociationPropsMixin",
):
    '''The ``AWS::AppStream::StackUserAssociation`` resource associates the specified users with the specified stacks for Amazon AppStream 2.0. Users in an AppStream 2.0 user pool cannot be assigned to stacks with fleets that are joined to an Active Directory domain.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackuserassociation.html
    :cloudformationResource: AWS::AppStream::StackUserAssociation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
        
        cfn_stack_user_association_props_mixin = appstream_mixins.CfnStackUserAssociationPropsMixin(appstream_mixins.CfnStackUserAssociationMixinProps(
            authentication_type="authenticationType",
            send_email_notification=False,
            stack_name="stackName",
            user_name="userName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnStackUserAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AppStream::StackUserAssociation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caac28c6a8391fc62380e9947347014421b95bc83f73538b4fa0449eeca514a3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7344763ed9a22fd4bd5ce09566d678f83a8f52d7c59692d4023454797eb0ca71)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07f2992095ed4e682eca006f7e30e10a229e99b375c70e74423dbcc95989f294)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnStackUserAssociationMixinProps:
        return typing.cast(CfnStackUserAssociationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnUserMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "authentication_type": "authenticationType",
        "first_name": "firstName",
        "last_name": "lastName",
        "message_action": "messageAction",
        "user_name": "userName",
    },
)
class CfnUserMixinProps:
    def __init__(
        self,
        *,
        authentication_type: typing.Optional[builtins.str] = None,
        first_name: typing.Optional[builtins.str] = None,
        last_name: typing.Optional[builtins.str] = None,
        message_action: typing.Optional[builtins.str] = None,
        user_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnUserPropsMixin.

        :param authentication_type: The authentication type for the user. You must specify USERPOOL.
        :param first_name: The first name, or given name, of the user.
        :param last_name: The last name, or surname, of the user.
        :param message_action: The action to take for the welcome email that is sent to a user after the user is created in the user pool. If you specify SUPPRESS, no email is sent. If you specify RESEND, do not specify the first name or last name of the user. If the value is null, the email is sent. .. epigraph:: The temporary password in the welcome email is valid for only 7 days. If users don’t set their passwords within 7 days, you must send them a new welcome email.
        :param user_name: The email address of the user. Users' email addresses are case-sensitive. During login, if they specify an email address that doesn't use the same capitalization as the email address specified when their user pool account was created, a "user does not exist" error message displays.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-user.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
            
            cfn_user_mixin_props = appstream_mixins.CfnUserMixinProps(
                authentication_type="authenticationType",
                first_name="firstName",
                last_name="lastName",
                message_action="messageAction",
                user_name="userName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23ecae1572bf3bd85e58aa428e08cb01dbf333b9ffd2edd30337643c5b7b31aa)
            check_type(argname="argument authentication_type", value=authentication_type, expected_type=type_hints["authentication_type"])
            check_type(argname="argument first_name", value=first_name, expected_type=type_hints["first_name"])
            check_type(argname="argument last_name", value=last_name, expected_type=type_hints["last_name"])
            check_type(argname="argument message_action", value=message_action, expected_type=type_hints["message_action"])
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if authentication_type is not None:
            self._values["authentication_type"] = authentication_type
        if first_name is not None:
            self._values["first_name"] = first_name
        if last_name is not None:
            self._values["last_name"] = last_name
        if message_action is not None:
            self._values["message_action"] = message_action
        if user_name is not None:
            self._values["user_name"] = user_name

    @builtins.property
    def authentication_type(self) -> typing.Optional[builtins.str]:
        '''The authentication type for the user.

        You must specify USERPOOL.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-user.html#cfn-appstream-user-authenticationtype
        '''
        result = self._values.get("authentication_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def first_name(self) -> typing.Optional[builtins.str]:
        '''The first name, or given name, of the user.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-user.html#cfn-appstream-user-firstname
        '''
        result = self._values.get("first_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def last_name(self) -> typing.Optional[builtins.str]:
        '''The last name, or surname, of the user.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-user.html#cfn-appstream-user-lastname
        '''
        result = self._values.get("last_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def message_action(self) -> typing.Optional[builtins.str]:
        '''The action to take for the welcome email that is sent to a user after the user is created in the user pool.

        If you specify SUPPRESS, no email is sent. If you specify RESEND, do not specify the first name or last name of the user. If the value is null, the email is sent.
        .. epigraph::

           The temporary password in the welcome email is valid for only 7 days. If users don’t set their passwords within 7 days, you must send them a new welcome email.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-user.html#cfn-appstream-user-messageaction
        '''
        result = self._values.get("message_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_name(self) -> typing.Optional[builtins.str]:
        '''The email address of the user.

        Users' email addresses are case-sensitive. During login, if they specify an email address that doesn't use the same capitalization as the email address specified when their user pool account was created, a "user does not exist" error message displays.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-user.html#cfn-appstream-user-username
        '''
        result = self._values.get("user_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnUserPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_appstream.mixins.CfnUserPropsMixin",
):
    '''The ``AWS::AppStream::User`` resource creates a new user in the AppStream 2.0 user pool.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-user.html
    :cloudformationResource: AWS::AppStream::User
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_appstream import mixins as appstream_mixins
        
        cfn_user_props_mixin = appstream_mixins.CfnUserPropsMixin(appstream_mixins.CfnUserMixinProps(
            authentication_type="authenticationType",
            first_name="firstName",
            last_name="lastName",
            message_action="messageAction",
            user_name="userName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnUserMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AppStream::User``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fac6ef1fe226d09b56899930b64706c73075b881cc9cfc1b15f56b3d6a50c122)
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
            type_hints = typing.get_type_hints(_typecheckingstub__86dbc195a942b54ec09b5f1dd24cb7af650fc45bef36b95714978aaae118fad5)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86bc99a0c3d46f7cf5e0f2a1947e8f8912f11d7981234cabfdf9c430ba2f776d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnUserMixinProps:
        return typing.cast(CfnUserMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnAppBlockBuilderMixinProps",
    "CfnAppBlockBuilderPropsMixin",
    "CfnAppBlockMixinProps",
    "CfnAppBlockPropsMixin",
    "CfnApplicationEntitlementAssociationMixinProps",
    "CfnApplicationEntitlementAssociationPropsMixin",
    "CfnApplicationFleetAssociationMixinProps",
    "CfnApplicationFleetAssociationPropsMixin",
    "CfnApplicationMixinProps",
    "CfnApplicationPropsMixin",
    "CfnDirectoryConfigMixinProps",
    "CfnDirectoryConfigPropsMixin",
    "CfnEntitlementMixinProps",
    "CfnEntitlementPropsMixin",
    "CfnFleetMixinProps",
    "CfnFleetPropsMixin",
    "CfnImageBuilderMixinProps",
    "CfnImageBuilderPropsMixin",
    "CfnStackFleetAssociationMixinProps",
    "CfnStackFleetAssociationPropsMixin",
    "CfnStackMixinProps",
    "CfnStackPropsMixin",
    "CfnStackUserAssociationMixinProps",
    "CfnStackUserAssociationPropsMixin",
    "CfnUserMixinProps",
    "CfnUserPropsMixin",
]

publication.publish()

def _typecheckingstub__6d3dbb9050e6835996877b6e957e37de7f874926c6e62768c615c362a5ddade9(
    *,
    access_endpoints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAppBlockBuilderPropsMixin.AccessEndpointProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    app_block_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    enable_default_internet_access: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    iam_role_arn: typing.Optional[builtins.str] = None,
    instance_type: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    platform: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAppBlockBuilderPropsMixin.VpcConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3633662d446d4fb6292bb778f2cf89900e9d3ada8c7490589ff827af6f725eb7(
    props: typing.Union[CfnAppBlockBuilderMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5faadeaa706ddb70178eb2a07a71bfeb0c2bdd689f3da800d602d61ae2d55e09(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5265f376d8c62b0f84a886bd7190ee33a4ed94a9564fe48d608b90faa2f87982(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c16509f404ab735fab41cf647e96b31c8b1647971e44a5e04c3ec817218cc0f(
    *,
    endpoint_type: typing.Optional[builtins.str] = None,
    vpce_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11641d1f3823b74a3bd6b95eb5a6b3af99fe1f4a1590a8f2e52db2e589973ea5(
    *,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23582a1c3bc01d0c577008bc5b6a11ca06a45bd4f9733a74571410b0ad03ae32(
    *,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    packaging_type: typing.Optional[builtins.str] = None,
    post_setup_script_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAppBlockPropsMixin.ScriptDetailsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    setup_script_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAppBlockPropsMixin.ScriptDetailsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    source_s3_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAppBlockPropsMixin.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73464241f1cc7bde8bdbc6c4b98fbacbd5572e73a8216fbf00370122d5484dd2(
    props: typing.Union[CfnAppBlockMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f9eae4d6e1384bd6bddc76e815f444bac613e741a9c8b230c40b52296870014(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51466f31cee1d8d5163cdae1860c98403ec45f1c0f5aea334c5b0e8517b727b8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d19ee18f356d5cb83a525aaa649654488e98d79da492e1ed53db686f987f455(
    *,
    s3_bucket: typing.Optional[builtins.str] = None,
    s3_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbadbd783a1580f14d6c506c8516b0d678e06de949aceaf4cc00fafde6657c7f(
    *,
    executable_parameters: typing.Optional[builtins.str] = None,
    executable_path: typing.Optional[builtins.str] = None,
    script_s3_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAppBlockPropsMixin.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    timeout_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__909d0dd63c8e2ae45d84e79fa0c090471fea06e20d4a889ef71cf8d843f82193(
    *,
    application_identifier: typing.Optional[builtins.str] = None,
    entitlement_name: typing.Optional[builtins.str] = None,
    stack_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__add0f318bcb24299f040cfc70ef723fe520b79480eb205d1036ac2ede8706c96(
    props: typing.Union[CfnApplicationEntitlementAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ce5cdc60718dd561ecbd56b331ae85836855a5154f3b78b61ec643c68cba27b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9421982fd69ddb1c49776fe989ba89b3bff021a79c7ec65cbbab6e4cd69a807(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__860ac7e6ddf61493f6085473ce2bfa66f302ef1d9536fc59d1516dbde7482710(
    *,
    application_arn: typing.Optional[builtins.str] = None,
    fleet_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55de10d1f18dae7acbc4487a49198ae3feb80bb57d061145073b214c3bfc1ab2(
    props: typing.Union[CfnApplicationFleetAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32c1c80097e34c5352429402eb45efd3b6cba3c0dd5c9dcc2a39f24656201818(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__177ae14003d8eaee59965ce5cb645a7943e99738c8d0e217a348a8101e1e3d01(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1da3bc4dd264b1d0f55a542896e88cc88b5628b2a306f6200770fec455462d44(
    *,
    app_block_arn: typing.Optional[builtins.str] = None,
    attributes_to_delete: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    icon_s3_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    instance_families: typing.Optional[typing.Sequence[builtins.str]] = None,
    launch_parameters: typing.Optional[builtins.str] = None,
    launch_path: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    platforms: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    working_directory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__405843b4bc61e754ab93e9f2fd179b65ef001932219b80037e7963a9de2ea72f(
    props: typing.Union[CfnApplicationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0796352dc6e35320ba983bf95f9e941812ce4c6671e85eb252daeda1af156a87(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ed5441a01aa97ef656ab6f146dd693f6cf37094046ee6c2f3d4745a53bc8ecd(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d1489105f9496ff5d1fbb605e34bc742bd8c17a67143b25c7b6494754748423(
    *,
    s3_bucket: typing.Optional[builtins.str] = None,
    s3_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e4984c7c8ccd5c686d9f2759c297af96c1bba8ca306f3e93837e335d9831701(
    *,
    certificate_based_auth_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDirectoryConfigPropsMixin.CertificateBasedAuthPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    directory_name: typing.Optional[builtins.str] = None,
    organizational_unit_distinguished_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    service_account_credentials: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDirectoryConfigPropsMixin.ServiceAccountCredentialsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bfcbc149e7522867e82149dce66808bce698a74906ecb7a9b6fc86965deaad7(
    props: typing.Union[CfnDirectoryConfigMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e328e7f62f80432df375e768ea15b19c164c872b7e940201f44748cbf29c208(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5fae9e70de512ccd159d7ffe1deaa024f9aba9a58f6adb21892bc75a3ce001a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a757d8154f83ac5294f28b4d65804caf11afccd8c8c2dffba084c614db7c8064(
    *,
    certificate_authority_arn: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeb2bc418dec631dd440af9730a4f760bdd1bfda8ae36345596767f1771f9e0b(
    *,
    account_name: typing.Optional[builtins.str] = None,
    account_password: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bb5f8be7ce260eb862b0ba0880ce6dc54d38f3cd52455a74fc88d17e2305f49(
    *,
    app_visibility: typing.Optional[builtins.str] = None,
    attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEntitlementPropsMixin.AttributeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    stack_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19a8f5f22b027bf94b5c0d3f84ce0c2b5da915af58dce3a8bf9045742c8d763c(
    props: typing.Union[CfnEntitlementMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32afee813dc85d9238c519012a43f87ba4e1b8237429df7af0dd3aa311e3359c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7c61193dc841c219b2921082b9c90682ccaeeba6149aa2c0176c1808d24e569(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ac5252bf4501eb0880b563afd03638ebfb571dc267811cf39e774b9213eda9c(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c470bfc842df5c5f11a47c5060c3483498eb2c208a8d80b0d68e81416ca3ea6b(
    *,
    compute_capacity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFleetPropsMixin.ComputeCapacityProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    disconnect_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    display_name: typing.Optional[builtins.str] = None,
    domain_join_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFleetPropsMixin.DomainJoinInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    enable_default_internet_access: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    fleet_type: typing.Optional[builtins.str] = None,
    iam_role_arn: typing.Optional[builtins.str] = None,
    idle_disconnect_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    image_arn: typing.Optional[builtins.str] = None,
    image_name: typing.Optional[builtins.str] = None,
    instance_type: typing.Optional[builtins.str] = None,
    max_concurrent_sessions: typing.Optional[jsii.Number] = None,
    max_sessions_per_instance: typing.Optional[jsii.Number] = None,
    max_user_duration_in_seconds: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    platform: typing.Optional[builtins.str] = None,
    root_volume_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFleetPropsMixin.VolumeConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    session_script_s3_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFleetPropsMixin.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    stream_view: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    usb_device_filter_strings: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFleetPropsMixin.VpcConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ac40daef75c5d4050ff01631c874cb064b94c4efeb106057e98a35d5c48e2b9(
    props: typing.Union[CfnFleetMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab8e9b104696da0d10b0171cdfd24172a1c3badbb6a78ebd60f1af851b077107(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__649336311ed24a2dfdc65f192a8ec7c8badb380aa7f6cf4233c9de491f0e19c7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57ca039cb516bc13df6cf163a4cf70b71f8670da28428574faea23a4e78c2a00(
    *,
    desired_instances: typing.Optional[jsii.Number] = None,
    desired_sessions: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49807a51ac206f3c1c9f7293383e1a0c7f8acb9cab90ab1b0ed3b6f008167656(
    *,
    directory_name: typing.Optional[builtins.str] = None,
    organizational_unit_distinguished_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbfdac7c844b13a4d0a878b6859efe346be40d4898e5b0abf7fb096a532a5ded(
    *,
    s3_bucket: typing.Optional[builtins.str] = None,
    s3_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c92a1e162a8fca19844bfb04d4b0b38503ab5d758d8c9a55097487f917bb1d0c(
    *,
    volume_size_in_gb: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcd0de05377106672aad34890479e3529144d1d1525bec704a3316010e6f495a(
    *,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03ffb03096557b9c4a6c6352cfc42ac94c5a6026e18c420bfdc974304c2c21cc(
    *,
    access_endpoints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnImageBuilderPropsMixin.AccessEndpointProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    appstream_agent_version: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    domain_join_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnImageBuilderPropsMixin.DomainJoinInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    enable_default_internet_access: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    iam_role_arn: typing.Optional[builtins.str] = None,
    image_arn: typing.Optional[builtins.str] = None,
    image_name: typing.Optional[builtins.str] = None,
    instance_type: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnImageBuilderPropsMixin.VpcConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4d2f72d605b685c0cf79a662d4dd99ea92367ef864a9adcc50dcaf53fa9f282(
    props: typing.Union[CfnImageBuilderMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba22a45fde17620d8aab4d70878de095ebacc0f6bb377da81b1fa6e356ffba35(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46f5e2ee7881162930e3b6e914f3f4fc88b2c6fa2b885d2c0278ca22f8e4092b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b85d22e2015f24c4ee0669f618ea4c4dbe67084fd84aa37f9838025ee24e4383(
    *,
    endpoint_type: typing.Optional[builtins.str] = None,
    vpce_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42123400051a5cc72d84a4796998aadef000c9f8b5b58e96ef05c1039a024d40(
    *,
    directory_name: typing.Optional[builtins.str] = None,
    organizational_unit_distinguished_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f61336147383bcc34f09611022be6aaf289a72234c078aaa924bba59900997de(
    *,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eba4d8611ccc1174e0837bb1664375462ace7933440f186684aecf8a71549a2(
    *,
    fleet_name: typing.Optional[builtins.str] = None,
    stack_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5064ae7c908740667cdcfe7bd6858099a49c7409af98d0cc1531f11108f73474(
    props: typing.Union[CfnStackFleetAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65dff8fd5c01edca44bdf9b8efdc0f496fe3265c8d4fa9ab71d37427d15be291(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__404536828bf27fa73afa80343dba5609b953966042f16ee76938822cf672b3da(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f795953f7b7027b8d95aaf397585dbaa1ed064d42bb8a5b88d9c5a4416230025(
    *,
    access_endpoints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStackPropsMixin.AccessEndpointProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    application_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStackPropsMixin.ApplicationSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    attributes_to_delete: typing.Optional[typing.Sequence[builtins.str]] = None,
    delete_storage_connectors: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    embed_host_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    feedback_url: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    redirect_url: typing.Optional[builtins.str] = None,
    storage_connectors: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStackPropsMixin.StorageConnectorProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    streaming_experience_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStackPropsMixin.StreamingExperienceSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    user_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStackPropsMixin.UserSettingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbf1d41fe8eef03fb8cf12f5da76cc04528beec1ebfcd2402ce50b22402c082b(
    props: typing.Union[CfnStackMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac51e2c66fce9df734bec460c0a28523d207c7e6898fd07b50703af6693903d1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d1b60dec4c5d6ffa48925c039bca3e4d9e0af294de2b7f989d555d53a3240b7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c6ec8646c5f0595f1923a1a10b09eb514fee9edfe02db450f798a00e03b8269(
    *,
    endpoint_type: typing.Optional[builtins.str] = None,
    vpce_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76bb8b969a66e24577cc1638ad2fa7d13877f7c9cdf337c6b66ddfeab0115e9e(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    settings_group: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99bd542ec9dfd0e8ee7678524140a5c2f3a9f1c86db3da307f365bc4e7c2e0f4(
    *,
    connector_type: typing.Optional[builtins.str] = None,
    domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c978db65d8629aa53b264c6f7a981ed9cef01ff8dc58c7fbb77e1227b766ab24(
    *,
    preferred_protocol: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eab0289127c9e583c43470e6bdbd75f1e045d5ddfdda9648bd2ee81649efda4b(
    *,
    action: typing.Optional[builtins.str] = None,
    maximum_length: typing.Optional[jsii.Number] = None,
    permission: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e04b7d77106417f36f198017a279df1620a89d58e207794d02e61882c17e591(
    *,
    authentication_type: typing.Optional[builtins.str] = None,
    send_email_notification: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    stack_name: typing.Optional[builtins.str] = None,
    user_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caac28c6a8391fc62380e9947347014421b95bc83f73538b4fa0449eeca514a3(
    props: typing.Union[CfnStackUserAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7344763ed9a22fd4bd5ce09566d678f83a8f52d7c59692d4023454797eb0ca71(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07f2992095ed4e682eca006f7e30e10a229e99b375c70e74423dbcc95989f294(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23ecae1572bf3bd85e58aa428e08cb01dbf333b9ffd2edd30337643c5b7b31aa(
    *,
    authentication_type: typing.Optional[builtins.str] = None,
    first_name: typing.Optional[builtins.str] = None,
    last_name: typing.Optional[builtins.str] = None,
    message_action: typing.Optional[builtins.str] = None,
    user_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fac6ef1fe226d09b56899930b64706c73075b881cc9cfc1b15f56b3d6a50c122(
    props: typing.Union[CfnUserMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86dbc195a942b54ec09b5f1dd24cb7af650fc45bef36b95714978aaae118fad5(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86bc99a0c3d46f7cf5e0f2a1947e8f8912f11d7981234cabfdf9c430ba2f776d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
